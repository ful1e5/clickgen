#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
import sys
from typing import Callable, List

from .db import CursorDB


## ----- Private


class _WinCursorsFixer(CursorDB):
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

        return super().rename(self.__files)


class _XCursorLinker(CursorDB):
    """ Create symblinks of missing `XCursors`. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def run(self) -> List[str]:
        """ Run linker. """
        func: Callable[[str], str] = lambda x: x.split(".")[0]
        self.__files.extend(list(map(func, glob(path.join(super().dir, "*")))))

        if len(self.__files) == 0:
            print(
                f"'XCursors' not found in '{super().dir}'",
                file=sys.stderr,
            )

        return super().rename(self.__files)


# ----- Public


def fix(win_dir: str, x11_dir: str) -> None:
    """ Fix cursors names with appropriate symblinks. """
    _WinCursorsFixer(dir=win_dir).run()
    _XCursorLinker(dir=x11_dir).run()
