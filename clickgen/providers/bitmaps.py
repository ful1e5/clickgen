#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import shutil
import tempfile
from os import path
from pathlib import Path
from typing import Callable, Dict, List, Literal, Optional, Tuple, Union

from PIL import Image, ImageEnhance, ImageFilter

from .._constants import WIN_BITMAPS_SIZE, WIN_CURSOR_SIZE, WIN_CURSORS
from .._typing import (
    Hotspot,
    ImageSize,
    JsonData,
    MappedBitmaps,
    OptionalHotspot,
    WindowsCursorsConfig,
)
from .db import Database


class PNG:
    """ Provide cursors bitmaps."""

    bitmap_dir: Path = ""

    def __init__(self, bitmaps_dir: Path) -> None:
        self.bitmap_dir = bitmaps_dir

    def bitmaps(self, d: str) -> MappedBitmaps:
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


class Bitmaps(PNG):
    """ .pngs files with cursors information """

    db: Database = Database()
    hotspots: JsonData = {}

    win_cursors: WindowsCursorsConfig = WIN_CURSORS
    win_bitmaps_size: ImageSize = WIN_BITMAPS_SIZE
    win_cursors_size: ImageSize = WIN_CURSOR_SIZE

    x_bitmaps_dir: Path = Path()
    win_bitmaps_dir: Path = Path()
    using_tmp_dir: bool = True

    def __init__(
        self,
        bitmap_dir: Path,
        hotspots: JsonData,
        win_cursors: Optional[WindowsCursorsConfig],
        win_cursors_size: Optional[ImageSize] = None,
        win_bitmaps_size: Optional[ImageSize] = None,
        valid_src: bool = False,
        db: Database = Database(),
    ) -> None:
        self.db = db
        self.hotspots = hotspots
        self.using_tmp_dir = not valid_src

        # Setting Windows Cursors settings
        if win_cursors:
            self.win_cursors: WindowsCursorsConfig = win_cursors
        if win_bitmaps_size:
            self.win_cursors_size = win_bitmaps_size
        if win_cursors_size:
            self.win_cursors_size = win_cursors_size

        self.__entry_win_info(list(self.win_cursors.keys()))

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
        self._seed_static_bitmaps()
        self._seed_animated_bitmaps()
        self._seed_windows_bitmaps()

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

    def update_hotspots_key(self, old_key: str, new_key: str) -> None:

        if new_key != old_key:
            try:
                self.hotspots[new_key] = self.hotspots[old_key]
                del self.hotspots[old_key]
            except KeyError:
                self.hotspots[new_key] = {"xhot": None, "yhot": None}

    def get_hotspots(self, key) -> OptionalHotspot:
        try:
            x = self.hotspots[key]["xhot"]
            y = self.hotspots[key]["yhot"]
            return OptionalHotspot(x, y)
        except KeyError:
            return OptionalHotspot(x=None, y=None)

    def __relink_file(self, old: str, new: str) -> None:
        try:
            src = self.x_bitmaps_dir / f"{old}.png"
            parent = os.readlink(src)
            os.unlink(src)
            dst = self.x_bitmaps_dir / f"{new}.png"

            os.symlink(parent, dst)
        except Exception:
            raise Exception(f"Unavailable to rename cursor .png files '{old}'")

    def _seed_static_bitmaps(self) -> None:
        main_curs: List[str] = super().static_pngs()

        for c in main_curs:
            cursor = path.splitext(c)[0]
            hot = self.get_hotspots(cursor)
            ren_c = self.db.smart_seed(cursor, hot)
            if ren_c:
                print(f"-- Renaming '{ren_c.old}' to '{ren_c.new}'")
                self.update_hotspots_key(ren_c.old, ren_c.new)
                self.__relink_file(ren_c.old, ren_c.new)
            else:
                continue

    def _seed_animated_bitmaps(self) -> None:
        main_dict: Dict[str, List[str]] = super().animated_pngs()

        for g in main_dict:
            hot = self.get_hotspots(g)
            ren_c = self.db.smart_seed(g, hot)
            if ren_c:
                print(f"-- Renaming '{ren_c.old}' to '{ren_c.new}'...")
                self.update_hotspots_key(ren_c.old, ren_c.new)
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
            hot = OptionalHotspot(*node["hotspots"])
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

        canvas: Image = Image.new("RGBA", WIN_BITMAPS_SIZE, (255, 0, 0, 0))
        box = self._canvas_cursor_cords(self.win_cursors_size, placement)

        original_image: Image = Image.open(src_p)
        draw: Image = original_image.resize(self.win_cursors_size, Image.BICUBIC)
        canvas.paste(draw, box, draw)
        draw.close()

        out = ImageEnhance.Sharpness(canvas).enhance(1.6)
        canvas.close()

        out.filter(ImageFilter.SHARPEN)
        out.save(out_p, compress_level=0, dpi=(600, 600))
        out.close()

        size: ImageSize = ImageSize(
            width=original_image.size[0], height=original_image.size[1]
        )

        original_image.close()
        # Calculate Hotspot
        x_hotspot: Hotspot = self.fetch_x_cursor_hotspot(src_p.stem, size)
        x: int = int(
            round(self.win_cursors_size.width / size.width * x_hotspot.x) + box[0]
        )
        y: int = int(
            round(self.win_cursors_size.height / size.height * x_hotspot.y) + box[1]
        )

        return Hotspot(x, y)

    def _seed_windows_bitmaps(self) -> MappedBitmaps:
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
                src: Path = self.x_bitmaps_dir / x_png
                dest: Path = self.win_bitmaps_dir / win_png

                # Creating Windows cursor bitmap
                hotspot = self.create_win_bitmap(src, dest, placement)
                s_pngs.append(win_png)

                # Insert Windows Cursors data to database
                self.db.seed(win_key, hotspot)

            # We know it's animated, Because pngs are filtered
            elif x_key in animated_pngs.keys():
                pngs: List[str] = animated_pngs.get(x_key)
                l: List[str] = []
                hotspot: Hotspot = Hotspot(0, 0)
                for png in pngs:
                    src: Path = self.x_bitmaps_dir / png
                    cur: str = png.replace(png.split("-")[0], win_key)
                    dest: Path = self.win_bitmaps_dir / cur

                    # Creating Windows cursor bitmap
                    hotspot = self.create_win_bitmap(src, dest, placement)
                    l.append(cur)
                a_pngs[win_key] = l

                # Insert Windows Cursors data to database
                self.db.seed(win_key, hotspot)

            else:
                raise FileNotFoundError(f"Unable to find '{x_key}' for '{win_key}'")

        bitmaps: MappedBitmaps = MappedBitmaps(static=s_pngs, animated=a_pngs)
        return bitmaps

    def win_bitmaps(self) -> MappedBitmaps:
        return self.bitmaps(self.win_bitmaps_dir)

    def x_bitmaps(self) -> MappedBitmaps:
        return self.bitmaps(self.x_bitmaps_dir)
