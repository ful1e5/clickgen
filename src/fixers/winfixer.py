#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .fixer import Fixer


class WinDirFixer(Fixer):
    """ Remove & Create symblinks for cursors. """

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def fix(self) -> None:
        print("hello")


wdf = WinDirFixer(dir="")
wdf.fix()