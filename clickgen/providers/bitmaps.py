#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import tempfile
from glob import glob
from os import path
from typing import Callable, Dict, List

from ..db import Database


class ThemeBitmapsProvider:
    """ Provide cursors bitmaps."""

    dir: str = ""

    def __init__(self, bitmaps_dir) -> None:
        self.dir = bitmaps_dir

        func: Callable[[str], str] = lambda x: path.basename(x)
        self.pngs: List[str] = []

        self.pngs.extend(list(map(func, glob(path.join(self.dir, "*.png")))))
        if len(self.pngs) <= 0:
            raise FileNotFoundError("Cursors .png files not found")

    def static_bitmaps(self) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") <= 0
        st_pngs: List[str] = list(filter(func, self.pngs))

        return st_pngs

    def animated_bitmaps(self) -> Dict[str, List[str]]:
        """ Return cursors list inside `bitmaps_dir` that had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") >= 0
        an_pngs: List[str] = list(filter(func, self.pngs))

        g_func: Callable[[str], str] = lambda x: x.split("-")[0]
        grps: List[str] = list(set(map(g_func, an_pngs)))

        d: Dict[str, List[str]] = {}

        for g in grps:
            func: Callable[[str], bool] = lambda x: x.find(g) >= 0
            d[g] = sorted(list(filter(func, an_pngs)))

        return d


class Bitmaps(ThemeBitmapsProvider):
    """ .pngs files with cursors information """

    def __init__(self, dir: str, valid_src: bool = True) -> None:
        self.db = Database()

        # Cursor validation
        if valid_src:
            super().__init__(dir)
        else:
            tmp_dir = tempfile.mkdtemp(prefix="clickgen_bits")
            for png in ThemeBitmapsProvider(dir).pngs:
                src = path.join(dir, png)
                dst = path.join(tmp_dir, png)
                shutil.copy(src, dst)

            super().__init__(tmp_dir)

    def static_bitmaps(self) -> List[str]:
        curs: List[str] = super().static_bitmaps()
        req_validation = self.db.valid_cursors()
