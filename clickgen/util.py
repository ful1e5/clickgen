#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import re
import shutil
import time
from contextlib import contextmanager
from copy import deepcopy
from os import PathLike
from pathlib import Path, PosixPath
from typing import Callable, Iterable, List, Set, Union

from clickgen.db import DATA, CursorDB
from clickgen.types import _P, _T


def replica(obj: _T) -> _T:
    return deepcopy(obj)


def to_path(p: _P) -> Path:
    if isinstance(p, str) or isinstance(p, PathLike):
        return Path(p)
    elif isinstance(p, Path):
        return p
    else:
        raise TypeError(
            f"Unable to convert parameter 'p' to 'Path' with 'TypeVar('_P', str, Path, PathLike)'"
        )


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


def add_missing_xcursors(
    dir: Path, data: List[Set[str]] = DATA, rename: bool = False, force: bool = False
) -> bool:
    if not dir.exists() or not dir.is_dir():
        raise NotADirectoryError(dir.absolute())

    db: CursorDB = CursorDB(data)

    # Removing all symlinks cursors
    if force:
        for xcursor in dir.iterdir():
            if xcursor.is_symlink():
                xcursor.unlink(xcursor)

    xcursors = sorted(dir.iterdir())

    for xcursor in xcursors:
        # Rename Xcursor according to Database, If necessary
        if rename:
            db.rename_file(xcursor)

        # Creating symlinks
        links = db.search_symlinks(xcursor.stem)
        if links:
            for link in links:
                with chdir(dir):
                    try:
                        os.symlink(xcursor, link)
                    except FileExistsError as f:
                        if os.path.islink(f.filename2):
                            os.unlink(f.filename2)
                            os.symlink(f.filename, f.filename2)
                        else:
                            raise FileExistsError(f)


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
