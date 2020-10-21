#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path, rename
import sys
from typing import List, Optional

from db import CursorDB


class WinCursorsFixer(CursorDB):
    """ Fix Windows cursors. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        self.__dir: str = dir

    def run(self, types: List[str] = ["*.cur", "*.ani"]) -> List[str]:
        """ Rename cursors according local Database. """
        for ext in types:
            self.__files.extend(glob(path.join(self.__dir, ext)))

        if len(self.__files) == 0:
            print(
                f"Zero 'Windows' cursors not found in '{self.__dir}'",
                file=sys.stderr,
            )

        cursors: List[str] = []
        for f in self.__files:
            cur, ext = path.splitext(path.basename(f))
            result: Optional[str] = super().match_to_db(cur)

            if result:
                src: str = path.join(self.__dir, f"{cur}{ext}")
                dst: str = path.join(self.__dir, f"{result}{ext}")
                rename(src, dst)
                cursors.append(dst)
            else:
                cursors.append(cur)

        return cursors


class XCursorSymblinks(WinCursorsFixer):
    """ Rename X11 cursors according local Database. """

    def __init__(self, dir: str) -> None:
        super().__init__(dir)
        self.__d = dir
        self.__cursors: List[str] = list(
            filter(lambda x: not x.find("."), super().run(types=["*"]))
        )

    def generate(self) -> None:
        """ Generate cursor symblinks that's missing. """
        if len(self.__cursors) == 0:
            print(
                f"Zero 'XCursors' not found in '{self.__d}'",
                file=sys.stderr,
            )


if __name__ == "__main__":
    t = XCursorSymblinks("/home/kaiz/test/win_out/").generate()
