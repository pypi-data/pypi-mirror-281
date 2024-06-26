import logging
import re
import time
from pathlib import Path
from tqdm import tqdm
from typing import Iterable, Literal


def track_tqdm(pbar: tqdm, n: int = 1):
    def wrapper(func):
        def inner(*args, **kwargs):
            res = func(*args, **kwargs)
            pbar.update(n)
            return res
        return inner
    return wrapper


def stylize(string: str, *ansi_styles, format_spec: str = "", newline: bool = False) -> str:
    r"""
    Stylize a string by a list of ANSI styles.
    """
    if not isinstance(string, str):
        string = format(string, format_spec)
    if len(ansi_styles) == 0:
        return string
    ansi_styles = ''.join(ansi_styles)
    if newline:
        ansi_styles = ANSI.NEWLINE + ansi_styles
    return ansi_styles + string + ANSI.RESET


class ANSI:
    BLACK = '\033[30m'  # basic colors
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    BRIGHT_BLACK = '\033[90m'  # bright colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    F = '\033[F'
    K = '\033[K'
    NEWLINE = F + K


def camel_to_snake(name):
    # 将所有连续的大写字母转换为小写，但在最后一个大写字母前加下划线
    name = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)

    # 将剩余的大写字母转换为小写，同时在它们前面加上下划线
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def color2ansi(color: str):
    return getattr(ANSI, color.upper(), "")


class ConsoleLogger:
    _loggers = {}
    _default_color = ANSI.BRIGHT_BLUE
    _level2color = {
        'debug': ANSI.BRIGHT_MAGENTA,
        'info': ANSI.BRIGHT_WHITE,
        'warning': ANSI.BRIGHT_YELLOW,
        'error': ANSI.BRIGHT_RED,
        'critical': ANSI.BRIGHT_RED,
    }

    def __new__(cls, name, *args, **kwargs):
        if name not in cls._loggers:
            cls._loggers[name] = super().__new__(cls)
        return cls._loggers[name]

    def __init__(self, name, prefix_msg=None, color=None, disable: bool = False):
        self.name = name
        self.prefix_msg = prefix_msg or name
        self.color = color2ansi(color) if isinstance(color, str) else (color or self._default_color)
        self.disable = disable

    def get_prefix(self, level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info', prefix_msg=None, prefix_color=None):
        prefixes = []
        level_color = self._level2color.get(level, "")
        if level != 'info':
            level_str = f"({stylize(level, level_color)})"
            prefixes.append(level_str)
        prefix_msg = prefix_msg or self.prefix_msg
        prefix_color = prefix_color or self.color
        if prefix_msg:
            prefix_str = f"[{stylize(prefix_msg, prefix_color)}]"
            prefixes.append(prefix_str)
        return ' '.join(prefixes)

    def print(self, *msg: str, level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info', prefix_msg=None, prefix_color=None, no_prefix=False, disable=None, **kwargs):
        disable = disable if disable is not None else self.disable
        if not disable:
            msg = kwargs.pop('sep', ' ').join(msg)
            if not no_prefix:
                prefix = self.get_prefix(level, prefix_msg, prefix_color)
                msg = prefix + ' ' + msg
            print(msg, **kwargs)

    def info(self, *msg: str, **kwargs):
        self.print(*msg, level='info', **kwargs)

    def debug(self, *msg: str, **kwargs):
        self.print(*msg, level='debug', **kwargs)

    def warning(self, *msg: str, **kwargs):
        self.print(*msg, level='warning', **kwargs)

    def error(self, *msg: str, **kwargs):
        self.print(*msg, level='error', **kwargs)

    def critical(self, *msg: str, **kwargs):
        self.print(*msg, level='critical', **kwargs)

    def tqdm(self, *args, level: Literal['debug', 'info', 'warning', 'error', 'critical'] = 'info', prefix_msg=None, prefix_color=None, no_prefix=False, **kwargs):
        from tqdm import tqdm
        desc = []
        if not no_prefix:
            prefix = self.get_prefix(level, prefix_msg, prefix_color)
            desc.append(prefix)
        if 'desc' in kwargs:
            desc.append(kwargs['desc'])
        kwargs["desc"] = ' '.join(desc)
        kwargs["disable"] = kwargs.get('disable', self.disable)
        return tqdm(*args, **kwargs)

    def timer(self, name=None):
        return timer(name, self)

    def __deepcopy__(self, memo):
        new_instance = self.__class__(
            name=self.name,
            prefix_str=self.prefix_msg,
            color=self.color,
            disable=self.disable
        )
        return new_instance


def get_logger(name, prefix_str=None, color=None, disable: bool = False):
    return ConsoleLogger(name, prefix_str, color, disable)


def get_all_loggers():
    return ConsoleLogger._loggers


debug_logger = get_logger('debug', color='bright_yellow')


def info(msg: str, *args, **kwargs):
    print('[INFO] ' + stylize(msg), *args, **kwargs)


def warn(msg: str, *args, **kwargs):
    print('[WARNING] ' + stylize(msg, ANSI.YELLOW), *args, **kwargs)


def error(msg: str, *args, **kwargs):
    print('[ERROR] ' + stylize(msg, ANSI.BRIGHT_RED), *args, **kwargs)


def success(msg: str, *args, **kwargs):
    print('[INFO] ' + stylize(msg, ANSI.BRIGHT_GREEN), *args, **kwargs)


def red(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_RED, format_spec=format_spec, newline=newline)


def green(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_GREEN, format_spec=format_spec, newline=newline)


def yellow(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_YELLOW, format_spec=format_spec, newline=newline)


def blue(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_BLUE, format_spec=format_spec, newline=newline)


def magenta(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_MAGENTA, format_spec=format_spec, newline=newline)


def cyan(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_CYAN, format_spec=format_spec, newline=newline)


def white(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_WHITE, format_spec=format_spec, newline=newline)


def black(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BRIGHT_BLACK, format_spec=format_spec, newline=newline)


def bold(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.BOLD, format_spec=format_spec, newline=newline)


def underline(msg: str, format_spec: str = "", newline: bool = False):
    return stylize(msg, ANSI.UNDERLINE, format_spec=format_spec, newline=newline)


class timer:
    def __init__(self, name=None, logger=debug_logger):
        self.name = name
        self.logger = logger

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        end_time = time.time()
        prefix = f"`{self.name}`: " if self.name else ""
        self.logger.print(prefix + f"{end_time - self.start_time:.2f}s", level='debug')

    def __call__(self, func):
        def inner(*args, **kwargs):
            with timer(self.name, self.logger):
                return func(*args, **kwargs)
        return inner
