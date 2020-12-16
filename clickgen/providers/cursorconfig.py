#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from pathlib import Path
from typing import List, Optional

from clickgen.typing import Hotspot, ImageSize
from PIL import Image


class CursorConfig:
    bitmaps_dir: Path = Path()
    hotspot: Hotspot
    sizes: List[ImageSize]
    config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_"))

    src_png: Path = Path()
    cfg_file: Path = Path()
    cursor: str = ""

    def __init__(
        self,
        bitmaps_dir: Path,
        hotspot: Hotspot,
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
            # print(
            #     f"-- Apply Default Hotspots: {self.cursor} => ({x},{y}), size={new_size.width}x{new_size.height}"
            # )

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
                (ideal_width, ideal_height), Image.LANCZOS
            )
            thumb.save(out_path, compress_level=0)

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
        self.cfg_file: Path = self.config_dir / f"{self.cursor}.in"

        with self.cfg_file.open(mode="w") as f:
            f.writelines(lines)

    def prepare_cfg_file(self, delay: Optional[int] = None) -> List[str]:
        """ Resize cursor & return `.in` file content. """
        lines: List[str] = []

        for size in self.sizes:
            # Creating .in file line
            hotspot: Hotspot = self.resize_cursor(size)
            line: str = f"{size.width} {hotspot.x} {hotspot.y} {size.width}x{size.height}/{self.src_png.name}"

            if delay:
                lines.append(f"{line} {delay}\n")
            else:
                lines.append(f"{line}\n")

        return lines

    def create_static(self, png: str) -> Path:
        self.set_cursor_info(png)
        # delay=None means static
        lines: List[str] = self.prepare_cfg_file(delay=None)
        self.write_cfg_file(lines)
        return self.cfg_file

    def create_animated(self, key: str, pngs: List[str], delay: int) -> Path:
        lines: List[str] = []
        for png in pngs:
            self.set_cursor_info(png, key)
            lines.extend(self.prepare_cfg_file(delay=delay))
        self.write_cfg_file(lines)
        return self.cfg_file
