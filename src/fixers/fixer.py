#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path, rename
import sys
from typing import List, Optional

from .db import CursorDB


class Fixer(CursorDB):
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

        for idx, f in enumerate(self.__files):

            cur, ext = path.splitext(path.basename(f))
            result: Optional[str] = super().match_to_db(cur)

            if result:
                src: str = path.join(self.__dir, f"{cur}{ext}")
                dst: str = path.join(self.__dir, f"{result}{ext}")
                rename(src, dst)
                self.__files[idx] = dst
