#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import re
import shutil
import time
from contextlib import contextmanager
from pathlib import Path, PosixPath
from typing import Callable, Iterable, List, Union

from clickgen.core import _P, to_path


def remove_util(p: Union[str, Path]) -> None:
    """ Remove this file, directory or symlink. If Path exits on filesystem."""

    if isinstance(p, str):
        p: Path = Path(p)

    if p.exists():
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
    else:
        pass


@contextmanager
def chdir(dir: Union[str, Path]):
    """
    Temporary change `working` directory. Use this in `with` syntax.

    :dir: path to directory.
    """

    prev_cwd = os.getcwd()
    os.chdir(str(dir))
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def timer(func):
    """Print the runtime of the decorated function"""

    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()

        value = func(*args, **kwargs)

        end_time = time.perf_counter()
        run_time = end_time - start_time
        print(f"Finished {func.__name__!r} in {run_time:.6f} secs")

        return value

    return wrapper_timer


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]  # 1
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # 2
        signature = ", ".join(args_repr + kwargs_repr)  # 3

        print(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")  # 4

        return value

    return wrapper_debug


def provide_pngs(bitmaps_dir: _P, pattern: str) -> List[Union[Path, List[Path]]]:
    bmp_dir: Path = to_path(bitmaps_dir)

    animated: List[PosixPath] = []
    static: List[PosixPath] = []

    keys: Iterable[str] = []

    for file in sorted(bmp_dir.glob("*.png")):
        match = re.search(pattern, file.name)
        if match:
            animated.append(file)
            key, _ = file.name.split(match.group(0))
            keys.append(key)
        else:
            static.append(file)

    result: List[Union[Path, List[Path]]] = static
    keys = set(keys)

    for key in keys:
        group = list(filter(lambda f: key in f.stem, animated))
        result.append(group)

    return result


class PNGProvider(object):
    bitmaps_dir: Path
    __pngs: List[str] = []

    def __init__(self, bitmaps_dir: _P) -> None:
        super().__init__()
        self.bitmaps_dir = to_path(bitmaps_dir)
        for f in sorted(self.bitmaps_dir.iterdir()):
            self.__pngs.append(f.name)

    def get(self, key: str) -> Union[List[Path], Path]:
        r = re.compile(key)
        convert_to_path: Callable[[str], Path] = lambda x: self.bitmaps_dir / x

        paths = list(map(convert_to_path, filter(r.match, self.__pngs)))

        if len(paths) == 1:
            return paths[0]
        else:
            return paths
