#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import shutil
import tempfile
from glob import glob
from os import path
from typing import Callable, Dict, List, Literal, Tuple, Union

from PIL import Image

from ..db import Database


class PNG:
    """ Provide cursors bitmaps."""

    dir: str = ""

    def __init__(self, bitmaps_dir) -> None:
        self.dir = bitmaps_dir

    def pngs(self) -> List[str]:
        func: Callable[[str], str] = lambda x: path.basename(x)
        pngs = list(map(func, glob(path.join(self.dir, "*.png"))))
        if len(pngs) <= 0:
            raise FileNotFoundError("Cursors .png files not found")
        return pngs

    def bitmap_type(self, f: str) -> Union[Literal["static"], Literal["animated"]]:
        f_name = path.splitext(f)[0]
        po_fix = f_name.split("-")[-1]
        if po_fix.isnumeric():
            return "animated"
        else:
            return "static"

    def static_pngs(self) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        func: Callable[[str], bool] = lambda x: self.bitmap_type(x) == "static"
        st_pngs: List[str] = list(filter(func, self.pngs()))

        return sorted(st_pngs)

    def animated_pngs(self) -> Dict[str, List[str]]:
        """ Return cursors list inside `bitmaps_dir` that had frames. """
        func: Callable[[str], bool] = lambda x: self.bitmap_type(x) == "animated"
        an_pngs: List[str] = list(filter(func, self.pngs()))

        g_func: Callable[[str], str] = lambda x: x.split("-")[0]
        grps: List[str] = sorted(list(set(map(g_func, an_pngs))))

        d: Dict[str, List[str]] = {}

        for g in grps:
            func: Callable[[str], bool] = lambda x: x.find(g) >= 0
            d[g] = sorted(list(filter(func, an_pngs)))

        return d


WINDOWS_CURSORS: Dict[str, str] = {
    "Alternate": "right_ptr",
    "Busy": "wait",
    "Cross": "cross",
    "Default": "left_ptr",
    "Diagonal_1": "bd_double_arrow",
    "Diagonal_2": "fd_double_arrow",
    "Handwriting": "pencil",
    "Help": "help",
    "Horizontal": "sb_h_double_arrow",
    "IBeam": "xterm",
    "Link": "hand2",
    "Move": "hand1",
    "Unavailiable": "circle",
    "Vertical": "sb_v_double_arrow",
    "Work": "left_ptr_watch",
}


class Bitmaps(PNG):
    """ .pngs files with cursors information """

    db: Database = Database()
    dir: str = ""
    is_tmp_dir: bool = True
    CANVAS_SIZE: Tuple[int, int] = (32, 32)
    LARGE_SIZE: Tuple[int, int] = (20, 20)
    NORMAL_SIZE: Tuple[int, int] = (16, 16)

    def __init__(
        self,
        dir: str,
        valid_src: bool = False,
        db: Database = Database(),
        windows_cursors: Dict[str, str] = WINDOWS_CURSORS,
    ) -> None:
        self.db = db
        self.is_tmp_dir = not valid_src
        self.win_cursors = windows_cursors

        # Cursor validation
        if valid_src:
            super().__init__(dir)
            self.dir = dir
        else:
            tmp_dir = tempfile.mkdtemp(prefix="clickgen_bitmaps_")
            for png in PNG(dir).pngs():
                src = path.join(dir, png)
                dst = path.join(tmp_dir, png)
                shutil.copy(src, dst)

            super().__init__(tmp_dir)
            self.dir = tmp_dir

        # Seeding data to local database
        self._seed_animated_bitmaps()
        self._seed_static_bitmaps()

    def free_space(self):
        if self.is_tmp_dir:
            shutil.rmtree(self.dir)

    def __rename_bitmap_png_file(self, old: str, new: str) -> None:
        try:
            src = path.join(self.dir, f"{old}.png")
            dst = path.join(self.dir, f"{new}.png")
            shutil.move(src, dst)
        except Exception:
            raise Exception(f"Unavailable to rename cursor .png files '{old}'")

    def _seed_static_bitmaps(self) -> None:
        main_curs: List[str] = super().static_pngs()

        for c in main_curs:
            cursor = path.splitext(c)[0]
            ren_c = self.db.smart_seed(cursor)
            if ren_c:
                print(f" Renaming '{ren_c.old}' to '{ren_c.new}'")
                self.__rename_bitmap_png_file(ren_c.old, ren_c.new)
            else:
                continue

    def _seed_animated_bitmaps(self) -> None:
        main_dict: Dict[str, List[str]] = super().animated_pngs()

        for g in main_dict:
            ren_c = self.db.smart_seed(g)
            if ren_c:
                print(f" Renaming '{ren_c.old}' to '{ren_c.new}'...")
                for png in main_dict[ren_c.old]:
                    pattern = "-(.*?).png"
                    frame = re.search(pattern, png).group(1)
                    png = path.splitext(png)[0]

                    cur = f"{ren_c.new}-{frame}"
                    self.__rename_bitmap_png_file(png, cur)
            else:
                continue

    def static_xcursors_bitmaps(self) -> List[str]:
        return super().static_pngs()

    def animated_xcursors_bitmaps(self) -> Dict[str, List[str]]:
        return super().animated_pngs()

    def canvas_cursor_cords(
        self,
        cursor_size: Tuple[int, int],
        placement: Literal[
            "top_left", "top_right", "bottom_right", "bottom_right", "center"
        ] = "center",
    ) -> Tuple[int, int]:
        (canvas_width, canvas_height) = self.CANVAS_SIZE
        (width, height) = cursor_size

        x = canvas_width - width
        y = canvas_height - height
        cords = {
            "top_left": (0, 0),
            "top_right": (x, 0),
            "bottom_left": (0, y),
            "bottom_right": (x, y),
            "center": (round(x / 2), round(y / 2)),
        }

        return cords.get(placement, "center")

    def create_win_bitmap(
        self,
        png_path: str,
        out_path: str,
        size: Literal["normal", "large"] = "normal",
    ) -> None:

        canvas: Image = Image.new("RGBA", self.CANVAS_SIZE, (255, 0, 0, 0))
        draw_size: int = self.LARGE_SIZE if size == "large" else self.NORMAL_SIZE
        cords: Tuple[int, int] = self.canvas_cursor_cords(
            draw_size, placement="top_left"
        )

        draw: Image = Image.open(png_path).resize(draw_size, Image.ANTIALIAS)
        canvas.paste(draw, cords, draw)
        canvas.save(out_path, quality=100)

        canvas.close()
        draw.close()

    def static_windows_bitmaps(self) -> List[str]:
        pngs: List[str] = self.static_pngs()
        bitmaps: List[str] = []

        for win_png, x_png in self.win_cursors.items():
            win_png: str = f"{win_png}.png"
            x_png: str = f"{x_png}.png"

            if x_png in pngs:
                src = path.join(self.dir, x_png)
                dest = path.join(self.dir, win_png)

                # Recreating already provided Windows cursor bitmap
                self.create_win_bitmap(src, dest)
                bitmaps.append(win_png)
            else:
                continue
        print(self.dir)
        return bitmaps
