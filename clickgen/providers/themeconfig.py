#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pathlib import Path
import tempfile
from os import path
from typing import Dict, List, Tuple, Union

from PIL import Image

from .jsonparser import Hotspots, HotspotsParser
from .bitmaps import PNG
from .._typing import ImageSize, Hotspot, JsonData


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


class HotspotJsonParser:
    """ Parse json file,that contains the hotspots."""

    hotspots: JsonData = {}

    def __init__(self, hotspots: JsonData) -> None:
        self.__hotspots = hotspots

    def get_hotspot(
        self, key: str, old_size: ImageSize, new_size: ImageSize
    ) -> Hotspot:
        try:
            key = path.splitext(key)[0]
            x = self.__hotspots[key]["xhot"]
            y = self.__hotspots[key]["yhot"]

            xhot = int(round(new_size.width / old_size.width * x))
            yhot = int(round(new_size.height / old_size.height * y))

            return Hotspot(xhot, yhot)

        except KeyError as key:
            xhot = int(new_size / 2)
            yhot = int(new_size / 2)
            print(
                f"{key} hotspots not provided for {new_size.width}x{new_size.height}, Setting to ({xhot},{yhot})"
            )

            return Hotspot(xhot, yhot)


class CursorConfig:
    src_png: Path = Path()
    sizes: List[ImageSize]
    hotspot: HotspotJsonParser
    config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_"))

    def __init__(
        self,
        fp: Path,
        hotspot: JsonData,
        sizes: List[ImageSize],
    ) -> None:

        if fp.suffix != "png":
            raise IOError(f"Invalid file format '{fp.suffix}' in {fp.name}")

        self.src_png = fp
        self.cursor = self.src_png.stem
        self.sizes = sizes
        self.hotspot = HotspotJsonParser(hotspot)

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

        hotspot: Hotspot = self.hotspot.get_hotspot(self.cursor, image_size, new_size)
        return hotspot

    def write_cfg_file(self, lines: List[str]) -> None:
        """ Write {@cur.in} file in @self.config_dir. """
        # sort line, So all lines in order according to size (24x24, 28x28, ..)
        lines.sort()

        # remove newline from EOF
        lines[-1] = lines[-1].rstrip("\n")
        cfg_path = self.config_dir / f"{self.cursor}.in"

        # TODO: writing with pathlib
        with open(cfg_path, "w") as f:
            f.writelines(lines)

    def generate_cursor(self, delay: Union[int, None] = None) -> List[str]:
        """ Resize cursor & return `.in` file content. """
        lines: List[str] = []

        for size in self.sizes:
            (xhot, yhot) = self.__resize_cursor(size)
            if delay:
                lines.append(
                    f"{size.width} {xhot} {yhot} {size.width}x{size.height}/{self.cursor} {delay}\n"
                )
            else:
                lines.append(
                    f"{size.width} {xhot} {yhot} {size.width}x{size.height}/{self.cursor}\n"
                )

        return lines

    def create_static(self) -> Path:

        return self.config_dir