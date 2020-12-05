#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from os import path
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

from PIL import Image

from .._typing import Hotspot, ImageSize, OptionalHotspot
from .bitmaps import PNG
from .jsonparser import Hotspots, HotspotsParser


def _clean_cur_name(name: str) -> str:
    """ Remove framing postfix. """
    return path.splitext(name)[0].split("-")[0]


class ThemeConfigsProvider:
    """ Provide `.in` files for 'xcursorgen' & 'anicursorgen' builder. """

    __sizes: List[int] = []
    __bitmaps: PNG = PNG("")
    __cords: HotspotsParser = HotspotsParser({})
    config_dir: str = tempfile.mkdtemp(prefix="clickgen_")

    def __init__(self, bitmaps_dir: str, hotspots: Hotspots, sizes: List[int]) -> None:
        self.__sizes = sizes
        self.__bitmaps = PNG(bitmaps_dir)
        self.__cords = HotspotsParser(hotspots)

    def __resize_cursor(self, cur: str, size: int) -> Tuple[int, int]:
        """ Resize cursor .png file as @size. """
        in_path = path.join(self.__bitmaps.bitmap_dir, cur)
        out_dir = path.join(self.config_dir, f"{size}x{size}")
        out_path = path.join(out_dir, cur)
        if not path.exists(out_dir):
            os.makedirs(out_dir)

        # opening original image
        image = Image.open(in_path)
        width: int = image.size[0]
        height: int = image.size[1]

        if (width, height) != (size, size):
            aspect: float = width / height
            ideal_width: int = size
            ideal_height: int = size
            ideal_aspect: float = ideal_width / float(ideal_height)

            if aspect > ideal_aspect:
                # Then crop the left and right edges:
                new_width: int = int(ideal_aspect * height)
                offset: float = (width - new_width) / 2
                resize = (offset, 0, width - offset, height)
            else:
                # ... crop the top and bottom:
                new_height = int(width / ideal_aspect)
                offset: float = (height - new_height) / 2
                resize = (0, offset, width, height - offset)

            # save resized image
            thumb = image.crop(resize).resize(
                (ideal_width, ideal_height), Image.ANTIALIAS
            )
            thumb.save(out_path, quality=100)

            image.close()
            thumb.close()

        return self.__cords.get_hotspots(_clean_cur_name(cur), (width, height), size)

    def __write_cfg_file(self, cur: str, lines: List[str]) -> None:
        """ Write {@cur.in} file in @self.config_dir. """
        # sort line, So all lines in order according to size (24x24, 28x28, ..)
        lines.sort()

        # remove newline from EOF
        lines[-1] = lines[-1].rstrip("\n")
        cfg_path = path.join(self.config_dir, f"{_clean_cur_name(cur)}.in")

        with open(cfg_path, "w") as f:
            f.writelines(lines)

    def __generate_cursor(self, cur: str, delay: Union[int, None] = None) -> List[str]:
        """ Resize cursor & return `.in` file content. """
        lines: List[str] = []

        for size in self.__sizes:
            (xhot, yhot) = self.__resize_cursor(cur, size)
            if delay:
                lines.append(f"{size} {xhot} {yhot} {size}x{size}/{cur} {delay}\n")
            else:
                lines.append(f"{size} {xhot} {yhot} {size}x{size}/{cur}\n")

        return lines

    def __generate_static_cfgs(self) -> None:
        """ Generate static cursors `.in` config files according to @self.__sizes. """
        cursors = self.__bitmaps.static_pngs()
        for cur in cursors:
            lines: List[str] = self.__generate_cursor(cur)
            self.__write_cfg_file(cur, lines)

    def __generate_animated_cfgs(self, delay: int) -> None:
        """ Generate animated cursors `.in` config files according to @self.__sizes. """
        d: Dict[str, List[str]] = self.__bitmaps.animated_pngs()

        for key in d:
            lines: List[str] = []
            for cur in d.get(key):
                lines.extend(self.__generate_cursor(cur, delay))
            self.__write_cfg_file(key, lines)

    def generate(self, animation_delay: int) -> str:
        """ Generate `.in` config files of `.png` inside @self.__bitmaps. """
        self.__generate_animated_cfgs(animation_delay)
        self.__generate_static_cfgs()

        return self.config_dir


class CursorConfig:
    bitmaps_dir: Path = Path()
    src_png: Path = Path()
    cursor: str = ""
    sizes: List[ImageSize]
    hotspot: OptionalHotspot
    config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_"))

    def __init__(
        self,
        bitmaps_dir: Path,
        hotspot: OptionalHotspot,
        sizes: List[ImageSize],
        config_dir: Optional[Path] = None,
    ) -> None:
        self.bitmaps_dir = bitmaps_dir
        if config_dir:
            self.config_dir = config_dir
        self.sizes = sizes
        self.hotspot = hotspot

    def set_cursor_info(self, png_file: str, key: Optional[str] = None) -> None:
        self.src_png = self.bitmaps_dir / png_file
        if self.src_png.suffix != ".png":
            raise IOError(
                f"Invalid file format '{self.src_png.suffix}' in {self.src_png.name}"
            )

        if not key:
            self.cursor = self.src_png.stem
        else:
            self.cursor = key

    def calc_hotspot(self, old_size: ImageSize, new_size: ImageSize) -> Hotspot:

        if not self.hotspot.x and not self.hotspot.y:
            x = int(new_size.width / 2)
            y = int(new_size.height / 2)
            print(
                f"-- Apply Default Hotspots: {self.cursor} => ({x},{y}), size={new_size.width}x{new_size.height}"
            )

            return Hotspot(x, y)
        else:
            x = int(round(new_size.width / old_size.width * self.hotspot.x))
            y = int(round(new_size.height / old_size.height * self.hotspot.y))

            return Hotspot(x, y)

    def resize_cursor(self, new_size: ImageSize) -> Hotspot:
        """ Resize cursor .png file as @size. """
        out_dir: Path = self.config_dir / f"{new_size.width}x{new_size.height}"
        out_path: Path = out_dir / self.src_png.name

        if not out_dir.exists():
            os.makedirs(out_dir)

        # opening original image
        image = Image.open(self.src_png)
        image_size: ImageSize = ImageSize(width=image.size[0], height=image.size[1])

        if image_size != new_size:
            aspect: float = image_size.width / image_size.height
            ideal_width: int = new_size.width
            ideal_height: int = new_size.height
            ideal_aspect: float = ideal_width / float(ideal_height)

            if aspect > ideal_aspect:
                # Then crop the left and right edges:
                new_width: int = int(ideal_aspect * image_size.height)
                offset: float = (image_size.width - new_width) / 2
                resize = (offset, 0, image_size.width - offset, image_size.height)
            else:
                # ... crop the top and bottom:
                new_height = int(image_size.width / ideal_aspect)
                offset: float = (image_size.height - new_height) / 2
                resize = (0, offset, image_size.width, image_size.height - offset)

            # save resized image
            thumb = image.crop(resize).resize(
                (ideal_width, ideal_height), Image.ANTIALIAS
            )
            thumb.save(out_path, quality=100)

            image.close()
            thumb.close()

            hotspot: Hotspot = self.calc_hotspot(image_size, new_size)
            return hotspot
        else:
            os.symlink(self.src_png, out_path)
            return Hotspot(self.hotspot.x, self.hotspot.y)

    def write_cfg_file(self, lines: List[str]) -> None:
        """ Write {@cur.in} file in @self.config_dir. """
        # sort line, So all lines in order according to size (24x24, 28x28, ..)
        lines.sort()

        # remove newline from EOF
        lines[-1] = lines[-1].rstrip("\n")
        cfg_file: Path = self.config_dir / f"{self.cursor}.in"

        with cfg_file.open(mode="w") as f:
            f.writelines(lines)

    def prepare_cfg_file(self, delay: Optional[int] = None) -> List[str]:
        """ Resize cursor & return `.in` file content. """
        lines: List[str] = []

        for size in self.sizes:
            hotspot: Hotspot = self.resize_cursor(size)
            if delay:
                lines.append(
                    f"{size.width} {hotspot.x} {hotspot.y} {size.width}x{size.height}/{self.src_png.name} {delay}\n"
                )
            else:
                lines.append(
                    f"{size.width} {hotspot.x} {hotspot.y} {size.width}x{size.height}/{self.src_png.name}\n"
                )

        return lines

    def create_static(self, png: str) -> Path:
        self.set_cursor_info(png)
        # delay=None means static
        lines: List[str] = self.prepare_cfg_file(delay=None)
        self.write_cfg_file(lines)
        return self.config_dir

    def create_animated(self, key: str, pngs: List[str], delay: int) -> Path:
        lines: List[str] = []
        for png in pngs:
            self.set_cursor_info(png, key)
            lines.extend(self.prepare_cfg_file(delay))
        self.write_cfg_file(lines)
        return self.config_dir
