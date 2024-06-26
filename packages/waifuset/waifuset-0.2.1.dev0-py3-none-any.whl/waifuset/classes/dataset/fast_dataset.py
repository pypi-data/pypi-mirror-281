import requests
import os
import platform
from pathlib import Path
from typing import Dict, List, Any, Literal
from .auto_dataset import AutoDataset
from .dataset import Dataset
from ..data.huggingface_data import HuggingFaceData
from ...utils import log_utils
from ...const import IMAGE_EXTS
from ...tools import mapping

logger = log_utils.get_logger("dataset")


class FastDataset(object):
    def __new__(cls, source, dataset_cls=None, **default_kwargs) -> Dataset:
        return load_fast_dataset(source, dataset_cls=dataset_cls, **default_kwargs)

    def __init__(self, source, dataset_cls=None, **default_kwargs) -> Dataset:
        r"""
        Initialize the dataset from a specified source.

        @param source: The source of the dataset(s). This can be one or multiple sources, each of which can be of the following types:
            - str or Path: The name or path to a local dataset (e.g., image directory, CSV, JSON, SQLite3) or a HuggingFace dataset (repository ID).
            - dict: The configuration for a local dataset or a HuggingFace dataset, with the following keys:
                - name_or_path: The name or path to a local dataset or a HuggingFace dataset.
                - primary_key: The primary key of the dataset. Default is 'image_key'.
                - column_mapping: The mapping of the dataset columns.
                - match_columns: Indicates whether to match the dataset columns. If True, columns not in the column_mapping will be removed.
                - fp_key: The key for the file path in the dataset. Default is 'image_path'. Applicable only for local datasets.
                - exts: The extensions of the images. Default is common image extensions ('jpg', 'jpeg', 'png', 'webp', 'jfif'). Applicable only for local datasets.
                - recur: Specifies whether to recursively search for images in the directory. Default is True. Applicable only for local datasets.
                - tbname: The table name of the SQLite3 dataset. Default is None, which means the dataset is assumed to be in a single table format. Applicable only for SQLite3 datasets.

        @param dataset_cls: An optional class to use for the dataset. If not provided, a default dataset class will be used.
        @param **default_kwargs: Additional keyword arguments to pass to the dataset constructor.

        @returns: An instance of the Dataset class.
        """


def get_platform() -> Literal['Windows', 'Linux', 'macOS', 'Other POSIX', 'Unknown']:
    if os.name == 'nt':
        return "Windows"
    elif os.name == 'posix':
        if platform.system() == 'Linux':
            return "Linux"
        elif platform.system() == 'Darwin':
            return "macOS"
        else:
            return "Other POSIX"
    else:
        return "Unknown"


def load_fast_dataset(
    source: List[str],
    skip_missing=False,
    dataset_cls=None,
    **default_kwargs,
) -> Dataset:
    source = parse_source_input(source)
    if not source:
        return dataset_cls.from_dict({})
    datasets = []
    fp_keys = [src.get('fp_key', 'image_path') for src in source]
    for src in source:
        name_or_path = src.pop('name_or_path')
        primary_key = src.pop('primary_key', 'image_key')
        if os.path.exists(name_or_path):
            dataset = load_local_dataset(
                name_or_path,
                dataset_cls=dataset_cls,
                primary_key=primary_key,
                column_mapping=src.pop('column_mapping', default_kwargs.get('column_mapping', None)),
                match_columns=src.pop('match_columns', default_kwargs.get('match_columns', True)),
                fp_key=src.pop('fp_key', default_kwargs.get('fp_key', 'image_path')),
                recur=src.pop('recur', default_kwargs.get('recur', False)),
                exts=src.pop('exts', default_kwargs.get('exts', IMAGE_EXTS)),
                tbname=src.pop('tbname', default_kwargs.get('tbname', None)),
                verbose=src.pop('verbose', default_kwargs.get('verbose', False)),
                **src,
            )
        else:
            dataset = load_huggingface_dataset(
                name_or_path=name_or_path,
                primary_key=primary_key,
                column_mapping=src.pop('column_mapping', default_kwargs.get('column_mapping', {k: 'image' for k in ('image', 'png', 'jpg', 'jpeg', 'webp', 'jfif')})),
                match_columns=src.pop('match_columns', default_kwargs.get('match_columns', True)),
                cache_dir=src.pop('cache_dir', default_kwargs.get('cache_dir', None)),
                token=src.pop('token', default_kwargs.get('token', None)),
                split=src.pop('split', default_kwargs.get('split', 'train')),
                max_retries=src.pop('max_retries', default_kwargs.get('max_retries', None)),
                dataset_cls=dataset_cls,
                verbose=src.pop('verbose', default_kwargs.get('verbose', False)),
                **src,
            )
        datasets.append(dataset)
    dataset = accumulate_datasets(datasets)
    if get_platform() != 'Windows' and (fp_keys := [k for k in fp_keys if k in dataset.header]):
        dataset.apply_map(mapping.as_posix_path, columns=fp_keys)
    if skip_missing:
        dataset = dataset.subset(lambda img_md: isinstance(img_md, HuggingFaceData) or any(os.path.exists(img_md.get(fp_key, '')) for fp_key in fp_keys))
    return dataset


def load_local_dataset(
    name_or_path: str,
    primary_key: str = 'image_key',
    column_mapping: Dict[str, str] = None,
    match_columns: List[str] = True,
    fp_key: str = 'image_path',
    exts: List[str] = IMAGE_EXTS,
    recur: bool = False,
    tbname: str = None,
    verbose: bool = False,
    read_attr: bool = False,
    dataset_cls: type = None,
    **kwargs: Dict[str, Any],
):
    localset = AutoDataset(
        name_or_path,
        dataset_cls=dataset_cls,
        fp_key=fp_key,
        exts=exts,
        primary_key=primary_key,
        recur=recur,
        tbname=tbname,
        verbose=verbose,
        **kwargs,
    )
    if read_attr:
        from waifuset.classes.data.data_utils import read_attrs

        def read_data_attr(img_md):
            attrs = read_attrs(img_md[fp_key])
            img_md.update(attrs)
            return img_md
        localset.apply_map(read_data_attr)
    if column_mapping:
        if match_columns:
            localset.remove_columns([k for k in localset.header if k not in column_mapping])
        localset.rename_columns({k: v for k, v in column_mapping.items() if k != v and k in localset.header})
    if primary_key not in localset.header:
        localset = patch_key(localset, primary_key)
    return localset


def load_huggingface_dataset(
    name_or_path: str,
    primary_key: str = 'image_key',
    column_mapping: Dict[str, str] = None,
    match_columns: List[str] = True,
    cache_dir: str = None,
    token: str = None,
    split: str = 'train',
    max_retries: int = None,
    verbose: bool = False,
    dataset_cls: type = None,
    **kwargs: Dict[str, Any],
) -> Dataset:
    r"""
    Load dataset from HuggingFace and convert it to `dataset_cls`.
    """
    import datasets
    try:
        import huggingface_hub.utils._errors
    except ImportError:
        raise ImportError("Please install huggingface-hub by `pip install huggingface-hub` to load dataset from HuggingFace.")
    if dataset_cls is None:
        from .dict_dataset import DictDataset
        dataset_cls = DictDataset
    retries = 0
    while True:
        try:
            hfset: datasets.Dataset = datasets.load_dataset(
                name_or_path,
                cache_dir=cache_dir,
                split=split,
                token=token,
                **kwargs,
            )
            break
        except (huggingface_hub.utils._errors.HfHubHTTPError, ConnectionError, requests.exceptions.HTTPError):
            logger.print(log_utils.yellow(f"Connection error when downloading dataset `{name_or_path}` from HuggingFace. Retrying..."))
            if max_retries is not None and retries >= max_retries:
                raise
            retries += 1
            pass

    if '__key__' in hfset.column_names:
        column_mapping['__key__'] = primary_key
    if column_mapping:
        if match_columns:
            hfset = hfset.remove_columns([k for k in hfset.column_names if k not in column_mapping])
        hfset = hfset.rename_columns({k: v for k, v in column_mapping.items() if k != v and k in hfset.column_names})

    dic = {}
    if primary_key not in hfset.column_names:
        for index in range(len(hfset)):
            img_key = str(index)
            dic[img_key] = HuggingFaceData(hfset, index=index, **{primary_key: img_key})
    else:
        for index, img_key in enumerate(hfset[primary_key]):
            dic[img_key] = HuggingFaceData(hfset, index=index, **{primary_key: img_key})
    return dataset_cls.from_dict(dic, verbose=verbose)


def parse_source_input(source) -> List[Dict[str, Any]]:
    if source is None:
        return []
    if not isinstance(source, list):
        source = [source]
    source = [dict(name_or_path=src) if isinstance(src, (str, Path)) else src for src in source]
    return source


def patch_key(dataset, primary_key) -> Dataset:
    for key, value in dataset.items():
        value[primary_key] = key
    return dataset


def accumulate_datasets(datasets, verbose=True) -> Dataset:
    if len(datasets) == 1:
        return datasets[0]
    elif len(datasets) > 1 and not all(isinstance(ds, datasets[0].__class__) for ds in datasets):
        logger.warning(f"Accumulating datasets with different types: {[ds.__class__.__name__ for ds in datasets]}, the type of the first dataset, {datasets[0].__class__.__name__}, will be used.")
    pivotset, datasets = datasets[0], datasets[1:]
    for ds in logger.tqdm(datasets, desc='accumulate datasets', disable=not verbose, position=1, leave=False):
        for img_key, new_img_md in logger.tqdm(ds.items(), total=len(ds), desc='accumulate data', disable=not verbose, position=2, leave=False):
            if (old_img_md := pivotset.get(img_key)) is not None:
                old_img_md.update(new_img_md)
                if issubclass(new_img_md.__class__, old_img_md.__class__):
                    new_img_md.update(old_img_md)
                    pivotset[img_key] = new_img_md
            else:
                pivotset[img_key] = new_img_md
    return pivotset
