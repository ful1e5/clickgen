#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
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

    db: Database = Database()
    dir: str = ""
    is_tmp_dir: bool = False

    def __init__(
        self, dir: str, valid_src: bool = False, db: Database = Database()
    ) -> None:
        self.db = db
        self.is_tmp_dir: bool = not valid_src

        # Cursor validation
        if valid_src:
            super().__init__(dir)
            self.dir = dir
        else:
            tmp_dir = tempfile.mkdtemp(prefix="clickgen_bits")
            for png in ThemeBitmapsProvider(dir).pngs:
                src = path.join(dir, png)
                dst = path.join(tmp_dir, png)
                shutil.copy(src, dst)

            super().__init__(tmp_dir)
            self.dir = tmp_dir

    def free_space(self):
        if self.is_tmp_dir:
            os.remove(self.dir)

    def rename_bitmap_png_file(self, old: str, new: str) -> None:
        try:
            # Moving cursors path
            src = path.join(self.dir, f"{old}.png")
            dst = path.join(self.dir, f"{new}.png")
            shutil.move(src, dst)
        except Exception:
            raise Exception(f"Unavailable to move cursor bitmap '{old}'")

    def static_bitmaps(self) -> List[str]:
        curs: List[str] = super().static_bitmaps()

        for c in curs:
            c = path.splitext(c)[0]
            ren_c = self.db.smart_seed(c)
            if ren_c:
                print(f" Renaming '{ren_c.old}' to '{ren_c.new}'")
                self.rename_bitmap_png_file(ren_c.old, ren_c.new)

                # Updating cursor list
                curs.remove(f"{ren_c.old}.png")
                curs.append(f"{ren_c.new}.png")
        return sorted(curs)

    def animated_bitmaps(self) -> List[str]:
        main_dict: Dict[str, List[str]] = super().animated_bitmaps()
        curs: Dict[str, List[str]] = {}

        for g in main_dict:
            ren_c = self.db.smart_seed(g)
            if ren_c:
                print(f" Renaming '{ren_c.old}' to '{ren_c.new}'")
                l: List[str] = []
                for png in main_dict[ren_c.old]:
                    pattern = "-(.*?).png"
                    frame = re.search(pattern, png).group(1)

                    cur = f"{ren_c.new}-{frame}.png"
                    l.append(cur)

                    png = path.splitext(png)[0]
                    cur = path.splitext(cur)[0]
                    self.rename_bitmap_png_file(png, cur)

                # Updating cursor dictionary
                curs[ren_c.new] = l
        return curs
