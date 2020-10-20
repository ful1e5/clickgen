#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Dict, List


class Fixer:
    # TODO
    _db: Dict[[str], List[str]] = {"": ["", ""]}

    def __init__(self, dir: str) -> None:
        self._dir: str = dir


class WinDirFixer(Fixer):
    """ Remove & Create symblinks for cursors. """

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def fix(self) -> None:
        print("hello")


wdf = WinDirFixer(dir="")
wdf.fix()
