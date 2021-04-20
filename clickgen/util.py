#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate Cursors without hassle.

.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

import functools
import os
import re
import shutil
import time
from contextlib import contextmanager
from pathlib import Path
from typing import List, Set, Union

from clickgen.db import DATA, CursorDB


@contextmanager
def chdir(directory: Union[str, Path]):
    """Temporary change working directory using `with` syntax.

    :param directory: path to directory.
    :type directory: Union[str, pathlib.Path]
    """
    prev_cwd = os.getcwd()
    os.chdir(directory)
    try:
        yield
    finally:
        os.chdir(prev_cwd)


def remove_util(p: Union[str, Path]) -> None:
    """Remove this file, directory or symlink.

    :param p: path to directory.
    :type p: Union[str, pathlib.Path]

    :return: None
    :rtype: None
    """
    p_obj: Path = Path(p)

    if p_obj.exists():
        if p_obj.is_dir():
            shutil.rmtree(p_obj)
        else:
            p_obj.unlink()
    else:
        pass


class PNGProvider:
    """Provide organized `.png` files."""

    bitmaps_dir: Path
    __pngs: List[str] = []

    def __init__(self, bitmaps_dir: Union[str, Path]) -> None:
        """Init `PNGProvider`.

        :param bitmaps_dir: Path to directory where `.png` files are stored.
        :type bitmaps_dir: Union[str, Path]
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
        """Retrieve `pathlib.Path` of filtered `.png` file/s.

        This method return file location in `pathlib.Path` object.

        Runtime directory `sync` is **not supported**, Which means creating \
        or deleting a file on programs execution is not update class `__pngs` \
        state.

        :param key: `key` is filename
        :type key: str

        :returns: Returns `pathlib.Path` object or `list` of `pathlib.Path`
                 object/s.
        :rtype: List[Path] or path
        """
        k = key.split(".")
        if len(k) == 1:
            reg = re.compile(fr"^{k[0]}(?:-\d+)?.png$")
        else:
            reg = re.compile(fr"^{k[0]}(?:-\d+)?.{k[1]}$")

        matched_pngs = filter(reg.match, self.__pngs)

        paths = list(set(map(lambda x: self.bitmaps_dir / x, matched_pngs)))
        if len(paths) == 1:
            return paths[0]
        return paths


def add_missing_xcursors(
    directory: Path,
    data: List[Set[str]] = DATA,
    rename: bool = False,
    force: bool = False,
) -> None:
    """Create symlinks of missing ``Xcursor``"""
    if not directory.exists() or not directory.is_dir():
        raise NotADirectoryError(directory.absolute())

    db: CursorDB = CursorDB(data)

    # Removing all symlinks cursors
    if force:
        for xcursor in directory.iterdir():
            if xcursor.is_symlink():
                xcursor.unlink(missing_ok=True)

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
