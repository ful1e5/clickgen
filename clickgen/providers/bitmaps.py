#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import tempfile
from os import path
from pathlib import Path
from typing import Callable, Dict, List, Literal, Optional, Set, Tuple, Union

from PIL import Image, ImageFilter

from .._constants import WIN_BITMAPS_SIZE, WIN_CURSOR_SIZE, WIN_CURSORS
from .._typing import (
    Hotspot,
    ImageSize,
    JsonData,
    MappedBitmaps,
    Hotspot,
    WindowsCursorsConfig,
)
from .db import Database


class PNG:
    """ Provide cursors bitmaps."""

    bitmap_dir: Path = ""

    def __init__(self, bitmaps_dir: Path) -> None:
        self.bitmap_dir = bitmaps_dir

    def bitmaps(self, d: Path) -> MappedBitmaps:
        original_dir: Path = self.bitmap_dir

        self.bitmap_dir = d
        bitmaps: MappedBitmaps = MappedBitmaps(
            static=self.static_pngs(), animated=self.animated_pngs()
        )

        self.bitmap_dir = original_dir
        return bitmaps

    def pngs(self) -> List[str]:
        pngs = list(map(lambda x: x.name, self.bitmap_dir.glob("*.png")))
        if len(pngs) <= 0:
            raise FileNotFoundError(".png files not found")
        return pngs

    def bitmap_type(self, f: str) -> Union[Literal["static"], Literal["animated"]]:
        f_name = path.splitext(f)[0]
        po_fix = f_name.rsplit("-", 1)[-1]
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

        g_func: Callable[[str], str] = lambda x: x.rsplit("-", 1)[0]
        grps: Set[str] = sorted(list(map(g_func, an_pngs)))

        d: Dict[str, List[str]] = {}
        for g in grps:
            func: Callable[[str], bool] = lambda x: x.find(g) >= 0
            d[g] = sorted(list(filter(func, an_pngs)))

        return d


class Bitmaps(PNG):
    """ .pngs files with cursors information """

    db: Database = Database()
    hotspots: JsonData = {}

    win_cursors_cfg: WindowsCursorsConfig = WIN_CURSORS
    win_bitmaps_size: ImageSize = WIN_BITMAPS_SIZE
    win_cursors_size: ImageSize = WIN_CURSOR_SIZE

    x_bitmaps_dir: Path = Path()
    win_bitmaps_dir: Path = Path()
    using_tmp_dir: bool = True

    def __init__(
        self,
        bitmap_dir: Path,
        hotspots: JsonData,
        win_cursors_cfg: Optional[WindowsCursorsConfig],
        win_cursors_size: Optional[ImageSize] = None,
        win_bitmaps_size: Optional[ImageSize] = None,
        valid_src: bool = False,
        db: Database = Database(),
    ) -> None:
        self.db = db
        self.hotspots = hotspots
        self.using_tmp_dir = not valid_src

        # Setting Windows Cursors settings
        if win_cursors_cfg:
            self.win_cursors_cfg: WindowsCursorsConfig = win_cursors_cfg
        if win_bitmaps_size:
            self.win_cursors_size = win_bitmaps_size
        if win_cursors_size:
            self.win_cursors_size = win_cursors_size

        self.__entry_win_info(list(self.win_cursors_cfg.keys()))

        # Cursor validation
        if valid_src:
            self.x_bitmaps_dir = bitmap_dir
        else:
            tmp_dir = Path(tempfile.mkdtemp(prefix="clickgen_x_bitmaps_"))
            for png in PNG(bitmap_dir).pngs():
                os.symlink(bitmap_dir / png, tmp_dir / png)
            self.x_bitmaps_dir = tmp_dir

        super().__init__(self.x_bitmaps_dir)
        self.win_bitmaps_dir = Path(tempfile.mkdtemp(prefix="clickgen_win_bitmaps_"))

        # Seeding data to local database
        self.__seed_static_bitmaps()
        self.__seed_animated_bitmaps()
        self.__seed_windows_bitmaps()

    def __entry_win_info(self, entry: Union[str, List[str]]) -> None:
        if isinstance(entry, str):
            self.db.db_cursors.append(entry)
        elif isinstance(entry, list):
            for e in entry:
                self.db.db_cursors.append(e)
        else:
            raise TypeError(f"'entry' argument must 'str' or 'List[str]'")

    def remove_tmp_bitmaps(self):
        if self.using_tmp_dir:
            shutil.rmtree(self.x_bitmaps_dir)
        shutil.rmtree(self.win_bitmaps_dir)

    def get_hotspots(self, key) -> Hotspot:
        try:
            x = self.hotspots[key]["xhot"]
            y = self.hotspots[key]["yhot"]
            return Hotspot(x, y)
        except KeyError:
            return Hotspot(x=None, y=None)

    def __relink_file(self, old: str, new: str) -> None:
        try:
            src = self.x_bitmaps_dir / f"{old}.png"
            parent = os.readlink(src)
            os.unlink(src)
            dst = self.x_bitmaps_dir / f"{new}.png"

            os.symlink(parent, dst)
        except Exception:
            raise Exception(f"Unavailable to rename cursor .png files '{old}'")

    def __seed_static_bitmaps(self) -> None:
        main_curs: List[str] = self.static_pngs()

        for c in main_curs:
            cursor = path.splitext(c)[0]
            hot = self.get_hotspots(cursor)
            ren_c = self.db.smart_seed(cursor, hot)
            if ren_c:
                # print(f"-- Renaming '{ren_c.old}' to '{ren_c.new}'")
                self.__relink_file(ren_c.old, ren_c.new)
            else:
                continue

    def __seed_animated_bitmaps(self) -> None:
        main_dict: Dict[str, List[str]] = self.animated_pngs()

        for g in main_dict.keys():
            hot = self.get_hotspots(g)
            ren_c = self.db.smart_seed(g, hot)
            if ren_c:
                # print(f"-- Renaming '{ren_c.old}' to '{ren_c.new}'...")
                for png in main_dict[ren_c.old]:
                    pattern = "-(.*?).png"
                    frame: str = re.search(pattern, png).group(1)
                    png = path.splitext(png)[0]

                    cur = f"{ren_c.new}-{frame}"
                    self.__relink_file(png, cur)
            else:
                continue

    def _canvas_cursor_cords(
        self,
        image: ImageSize,
        placement: Literal[
            "top_left", "top_right", "bottom_right", "bottom_right", "center"
        ] = "center",
    ) -> Tuple[int, int]:

        x = WIN_BITMAPS_SIZE.width - image.width
        y = WIN_BITMAPS_SIZE.height - image.height

        switch = {
            "top_left": (0, 0),
            "top_right": (x, 0),
            "bottom_left": (0, y),
            "bottom_right": (x, y),
            "center": (round(x / 2), round(y / 2)),
        }

        return switch.get(placement, "center")

    def fetch_x_cursor_hotspot(self, x_key: str, size: ImageSize) -> Hotspot:
        node = self.db.cursor_node_by_name(x_key)
        x: int = int(round(size.width / 2))
        y: int = int(round(size.height / 2))
        try:
            hot = Hotspot(*node["hotspots"])
            x: int = hot.x
            y: int = hot.y
            if not hot.x:
                x: int = x
            if not hot.y:
                y: int = y
            return Hotspot(x, y)
        except Exception:
            return Hotspot(x, y)

    def create_win_bitmap(
        self, src_p: Union[str, Path], out_p: Union[str, Path], placement: str
    ) -> Hotspot:

        canvas: Image = Image.new("RGBA", self.win_bitmaps_size, (255, 0, 0, 0))
        box = self._canvas_cursor_cords(self.win_cursors_size, placement)

        image: Image = Image.open(src_p)
        image_size: ImageSize = ImageSize(width=image.size[0], height=image.size[1])

        cursor: Image = image.resize(self.win_cursors_size, Image.LANCZOS).filter(
            ImageFilter.SHARPEN
        )
        canvas.paste(cursor, box, cursor)
        canvas.save(out_p, compress_level=0)

        # Calculate Hotspot
        x_hotspot: Hotspot = self.fetch_x_cursor_hotspot(src_p.stem, image_size)
        x: int = int(
            round(self.win_cursors_size.width / image_size.width * x_hotspot.x) + box[0]
        )
        y: int = int(
            round(self.win_cursors_size.height / image_size.height * x_hotspot.y)
            + box[1]
        )

        return Hotspot(x, y)

    def __seed_windows_bitmaps(self) -> None:
        static_pngs: List[str] = self.static_pngs()
        animated_pngs: Dict[str, List[str]] = self.animated_pngs()

        for win_key, data in self.win_cursors_cfg.items():
            x_key: str = data.get("xcursor")
            x_png: str = f"{x_key}.png"
            win_png: str = f"{win_key}.png"

            # Replace to original png file, If "symlink cursor" provided in `win_cfg`
            symlink = self.db.cursor_node_by_symlink(x_key)
            if symlink != None:
                x_png = f"{symlink.name}.png"

            placement: str = (
                data.get("placement") if data.get("placement") != None else "center"
            )

            # checking it's really static png!
            if x_png in static_pngs:
                src: Path = self.x_bitmaps_dir / x_png
                dest: Path = self.win_bitmaps_dir / win_png

                # Creating Windows cursor bitmap,1
                hotspot = self.create_win_bitmap(src, dest, placement)

                # Insert Windows Cursors data to database
                self.db.seed(win_key, hotspot)

            # We know it's animated, Because pngs are filtered
            elif x_key in animated_pngs.keys():
                pngs: List[str] = animated_pngs.get(x_key)
                hotspot: Hotspot = Hotspot(0, 0)
                for png in pngs:
                    src: Path = self.x_bitmaps_dir / png
                    cur: str = png.replace(png.rsplit("-", 1)[0], win_key)
                    dest: Path = self.win_bitmaps_dir / cur

                    # Creating Windows cursor bitmap
                    hotspot = self.create_win_bitmap(src, dest, placement)

                # Insert Windows Cursors data to database
                self.db.seed(win_key, hotspot)

            else:
                raise FileNotFoundError(f"Unable to find '{x_key}' for '{win_key}'")

    def win_bitmaps(self) -> MappedBitmaps:
        return self.bitmaps(self.win_bitmaps_dir)

    def x_bitmaps(self) -> MappedBitmaps:
        return self.bitmaps(self.x_bitmaps_dir)
