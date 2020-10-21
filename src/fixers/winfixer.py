#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
import sys
from typing import List, Tuple

from db import CursorDB


class WinDirFixer(CursorDB):
    """ Remove & Create symblinks for cursors. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        self.__dir: str = dir

    def fix(self) -> None:

        for ext in ("*.cur", "*.ani"):
            self.__files.extend(glob(path.join(self.__dir, ext)))

        if len(self.__files) == 0:
            print(
                f".ani or .cur cursors not found in '{self.__dir}'",
                file=sys.stderr,
            )

        for f in self.__files:

            cur: str = path.splitext(path.basename(f))[0]
            result: str = super().match_to_db(cur)


wdf = WinDirFixer(dir="/home/kaiz/test/win_out")
wdf.fix()