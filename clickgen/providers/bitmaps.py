#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import shutil
import tempfile
from glob import glob
from os import path
from typing import Callable, Dict, List, Literal, NamedTuple, Tuple, Union

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


WINDOWS_CURSORS: Dict[str, Dict[str, str]] = {
    "Alternate": {"xcursor": "right_ptr", "placement": "top_left"},
    "Busy": {"xcursor": "wait"},
    "Cross": {"xcursor": "cross"},
    "Default": {"xcursor": "left_ptr", "placement": "top_left"},
    "Diagonal_1": {"xcursor": "fd_double_arrow"},
    "Diagonal_2": {"xcursor": "bd_double_arrow"},
    "Handwriting": {"xcursor": "pencil"},
    "Help": {"xcursor": "help", "placement": "top_left"},
    "Horizontal": {"xcursor": "sb_h_double_arrow"},
    "IBeam": {"xcursor": "xterm", "placement": "top_left"},
    "Link": {"xcursor": "hand2", "placement": "top_left"},
    "Move": {"xcursor": "hand1"},
    "Unavailiable": {"xcursor": "circle", "placement": "top_left"},
    "Vertical": {"xcursor": "sb_v_double_arrow"},
    "Work": {"xcursor": "left_ptr_watch", "placement": "top_left"},
}


class BITMAPS(NamedTuple):
    static: List[str]
    animated: Dict[str, List[str]]


class Bitmaps(PNG):
    """ .pngs files with cursors information """

    db: Database = Database()
    x_dir: str = ""
    win_dir: str = ""
    is_tmp_dir: bool = True
    CANVAS_SIZE: Tuple[int, int] = (32, 32)
    LARGE_SIZE: Tuple[int, int] = (20, 20)
    NORMAL_SIZE: Tuple[int, int] = (16, 16)

    def __init__(
        self,
        dir: str,
        valid_src: bool = False,
        db: Database = Database(),
        windows_cursors: Dict[str, Dict[str, str]] = WINDOWS_CURSORS,
    ) -> None:
        self.db = db
        self.is_tmp_dir = not valid_src
        self.win_cursors = windows_cursors

        # Cursor validation
        if valid_src:
            super().__init__(dir)
            self.x_dir = dir
        else:
            tmp_dir = tempfile.mkdtemp(prefix="clickgen_x_bitmaps_")
            for png in PNG(dir).pngs():
                src = path.join(dir, png)
                dst = path.join(tmp_dir, png)
                shutil.copy(src, dst)

            super().__init__(tmp_dir)
            self.x_dir = tmp_dir

        self.win_dir = tempfile.mkdtemp(prefix="clickgen_win_bitmaps_")
        # Seeding data to local database
        self._seed_animated_bitmaps()
        self._seed_static_bitmaps()

    def free_space(self):
        if self.is_tmp_dir:
            shutil.rmtree(self.x_dir)

    def __rename_bitmap_png_file(self, old: str, new: str) -> None:
        try:
            src = path.join(self.x_dir, f"{old}.png")
            dst = path.join(self.x_dir, f"{new}.png")
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
                    frame: str = re.search(pattern, png).group(1)
                    png = path.splitext(png)[0]

                    cur = f"{ren_c.new}-{frame}"
                    self.__rename_bitmap_png_file(png, cur)
            else:
                continue

    def x_bitmaps(self) -> BITMAPS:
        return BITMAPS(static=self.static_pngs(), animated=self.animated_pngs())

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
        placement: str,
        size: Literal["normal", "large"] = "normal",
    ) -> None:

        canvas: Image = Image.new("RGBA", self.CANVAS_SIZE, (255, 0, 0, 0))
        draw_size: int = self.LARGE_SIZE if size == "large" else self.NORMAL_SIZE
        cords: Tuple[int, int] = self.canvas_cursor_cords(draw_size, placement)

        draw: Image = Image.open(png_path).resize(draw_size, Image.ANTIALIAS)
        canvas.paste(draw, cords, draw)
        canvas.save(out_path, quality=100)

        canvas.close()
        draw.close()

    def windows_bitmaps(
        self,
        size: Literal["normal", "large"] = "normal",
    ) -> BITMAPS:
        static_pngs: List[str] = self.static_pngs()
        animated_pngs: Dict[str, List[str]] = self.animated_pngs()

        s_pngs: List[str] = []
        a_pngs: Dict[str, List[str]] = {}

        for win_key, data in self.win_cursors.items():
            x_key: str = data.get("xcursor")
            x_png: str = f"{x_key}.png"
            win_png: str = f"{win_key}.png"

            # Replace to original png file, If "symlink cursor" provided in `win_cfg`
            symlink = self.db.cursor_node_by_symlink(x_key)
            if symlink != None:
                name: str = symlink["name"]
                x_png = f"{name}.png"

            placement: str = (
                data.get("placement") if data.get("placement") != None else "center"
            )

            # checking it's really static png!
            if x_png in static_pngs:
                src = path.join(self.x_dir, x_png)
                dest = path.join(self.win_dir, win_png)

                # Creating Windows cursor bitmap
                self.create_win_bitmap(src, dest, placement, size)
                s_pngs.append(win_png)

            # We know it's animated, Because pngs are filtered
            elif x_key in animated_pngs.keys():
                pngs: List[str] = animated_pngs.get(x_key)
                l: List[str] = []
                for png in pngs:
                    src = path.join(self.x_dir, png)
                    cur: str = png.replace(png.split("-")[0], win_key)
                    dest = path.join(self.win_dir, cur)

                    # Creating Windows cursor bitmap
                    self.create_win_bitmap(src, dest, placement, size)
                    l.append(cur)
                a_pngs[win_key] = l

            else:
                raise FileNotFoundError(f"Unable to find '{x_key}' for '{win_key}'")

        bitmaps: BITMAPS = BITMAPS(static=s_pngs, animated=a_pngs)
        return bitmaps
