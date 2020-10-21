#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
import sys
from typing import List

from .db import CursorDB


class WinDirFixer(CursorDB):
    """ Remove & Create symblinks for cursors. """

    __cursors: List[str] = []

    def __init__(self, dir: str) -> None:
        self.__dir: str = dir

    def fix(self) -> None:

        for ext in ("*.cur", "*.ani"):
            self.__cursors.extend(glob(path.join(self.__dir, ext)))

        if len(self.__cursors) == 0:
            print(
                f".ani or .cur cursors not found in '{self.__dir}'",
                file=sys.stderr,
            )

        for cur in self.__cursors:
            print(cur)


wdf = WinDirFixer(dir="/tmp/out")
wdf.fix()