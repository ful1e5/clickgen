#!/usr/bin/env python
# -*- coding: utf-8 -*-

import functools
import os
import re
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from typing import List, Set, TypeVar, Union

from clickgen.db import DATA, CursorDB

LikePath = TypeVar("LikePath", str, Path)


@contextmanager
def chdir(directory: LikePath):
    """Temporary change `working` directory.

    :directory: path to directory.
    """

    prev_cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def remove_util(p: LikePath) -> None:
    """Remove this file, directory or symlink. If Path exits on filesystem.

    :p: path to directory.
    """

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
    """Provide organized `.png` files."""

    bitmaps_dir: Path
    __pngs: List[str] = []

    def __init__(self, bitmaps_dir: LikePath) -> None:
        """Init `PNGProvider`.

        :bitmaps_dir: path to directory where `.png` files are stored.
        """
        super().__init__()
        self.bitmaps_dir = Path(bitmaps_dir)
        for f in sorted(self.bitmaps_dir.iterdir()):
            self.__pngs.append(f.name)

        if len(self.__pngs) == 0:
            raise FileNotFoundError(
                f"'*.png' files not found in '{self.bitmaps_dir.absolute()}'"
            )

    def get(self, key: str) -> Union[List[Path], Path]:
        """Get `.png` file/s from key.
        This method return file location in `pathlib.Path` instance.

        Also, this method is not supported directory sync, Which means creating a new file or deleting a file not affect this method.

        The only way to sync the directory is, By creating a new instance of the `PNGProvider` class.

        :key: `.png` filename without extension.
        """
        r = re.compile(key)
        matched_pngs = filter(r.match, self.__pngs)

        paths = list(set(map(lambda x: self.bitmaps_dir / x, matched_pngs)))
        if len(paths) == 1:
            return paths[0]
        return paths


def add_missing_xcursors(
    directory: Path,
    data: List[Set[str]] = DATA,
    rename: bool = False,
    force: bool = False,
) -> bool:
    if not directory.exists() or not directory.is_dir():
        raise NotADirectoryError(directory.absolute())

    db: CursorDB = CursorDB(data)

    # Removing all symlinks cursors
    if force:
        for xcursor in directory.iterdir():
            if xcursor.is_symlink():
                xcursor.unlink(xcursor)

    xcursors = sorted(directory.iterdir())

    for xcursor in xcursors:
        # Rename Xcursor according to Database, If necessary
        if rename:
            new_path = db.rename_file(xcursor)
            if new_path:
                xcursor = xcursor.rename(new_path)

        # Creating symlinks
        links = db.search_symlinks(xcursor.stem)
        if links:
            for link in links:
                with chdir(directory):
                    os.symlink(xcursor, link)


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
