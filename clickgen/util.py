#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import re
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from typing import Callable, List, Set, Union

from clickgen.core import LikePath
from clickgen.db import DATA, CursorDB


@contextmanager
def chdir(dir: Union[str, Path]):
    """
    Temporary change `working` directory. Use this in `with` syntax.

    :dir: path to directory.
    """

    prev_cwd = os.getcwd()
    os.chdir(dir)
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


class PNGProvider(object):
    bitmaps_dir: Path
    __pngs: List[str] = []

    def __init__(self, bitmaps_dir: LikePath) -> None:
        super().__init__()
        self.bitmaps_dir = Path(bitmaps_dir)
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


#
# Useful for development
#
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
