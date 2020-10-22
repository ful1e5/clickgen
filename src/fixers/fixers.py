#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path, listdir, remove, rename
import sys
import itertools
from typing import Callable, List

from .db import CursorDB


class WinCursorsFixer(CursorDB):
    """ Rename Windows cursors accordinf to local database. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def run(self) -> List[str]:
        """ Run fixer. """
        for ext in ("*.ani", "*.cur"):
            self.__files.extend(glob(path.join(super().dir, ext)))

        if len(self.__files) == 0:
            print(
                f"'Windows' cursors not found in '{super().dir}'",
                file=sys.stderr,
            )

        # Renaming cursors according to master DB
        super().rename(self.__files)

        # Renaming cursors according to Win DB
        curs = listdir(super().dir)
        for cur, key in itertools.product(curs, super().win_db):
            ext: str = path.splitext(cur)[1]
            func: Callable[[str], str] = lambda x: f"{x}{ext}"
            l: List[str] = list(map(func, super().win_db[key]))

            if cur in l:
                src: str = path.join(super().dir, cur)
                dst: str = path.join(super().dir, key)

                print(f"Renaming '{cur}' to '{key}'")
                rename(src, dst)

        # Removing other cursors, That's not in Win DB
        rm_list: List[str] = list(listdir(super().dir) - super().win_db.keys())
        for e in rm_list:
            print(f"Removing '{path.basename(e)}'")
            remove(path.join(super().dir, e))

        return listdir(super().dir)


class XCursorLinker(CursorDB):
    """ Create symblinks of missing `XCursors`. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def run(self) -> List[str]:
        """ Run linker. """
        func: Callable[[str], bool] = lambda x: x.split(".")[0] == x
        self.__files.extend(list(filter(func, glob(path.join(super().dir, "*")))))

        if len(self.__files) == 0:
            print(
                f"'XCursors' not found in '{super().dir}'",
                file=sys.stderr,
            )

        super().rename(self.__files)

        return listdir(super().dir)


if __name__ == "__main__":
    WinCursorsFixer(dir="/home/kaiz/w").run()
