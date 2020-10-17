#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
import os
import tempfile
from typing import AnyStr, Callable, Dict, List, Tuple

from PIL import Image

from json_parser import HotspotsParser


class ThemeConfigsProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(
        self, bitmaps_dir: str, hotspots_file: AnyStr, sizes: List[int]
    ) -> None:
        self.__bitmaps_dir = bitmaps_dir
        self.__cords_parser: HotspotsParser = HotspotsParser(hotspots_file)
        self.__sizes = sizes
        self.config_dir = tempfile.mkdtemp()

    def __get_png_files(self) -> List[str]:
        """ Return list of .png files in `bitmaps_dir`. """
        func: Callable[[str], str] = lambda x: path.basename(x)
        pngs: List[str] = []

        try:
            pngs.extend(list(map(func, glob(path.join(self.__bitmaps_dir, "*.png")))))
            if len(pngs) <= 0:
                raise Exception("Cursors .png files not found")
        except Exception as e:
            print(e)

        return pngs

    def __get_png_files(self) -> List[str]:
        """ Return list of .png files in `bitmaps_dir`. """
        func: Callable[[str], str] = lambda x: path.basename(x)
        pngs: List[str] = []

        try:
            pngs.extend(list(map(func, glob(path.join(self.__bitmaps_dir, "*.png")))))
            if len(pngs) <= 0:
                raise Exception("Cursors .png files not found")
        except Exception as e:
            print(e)

        return pngs

    def __list_static_png(self) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") <= 0
        st_pngs: List[str] = list(filter(func, self.__get_png_files()))
        return st_pngs

    def __list_animated_png(self) -> Dict[str, List[str]]:
        """ Return cursors list inside `bitmaps_dir` that had frames. """
        func: Callable[[str], bool] = lambda x: x.find(f"-") >= 0
        pngs: List[str] = list(filter(func, self.__get_png_files()))

        grp_func: Callable[[str], str] = lambda x: x.split("-")[0]
        grp: List[str] = list(set(map(grp_func, pngs)))
        an_pngs: Dict[str, List[str]] = {}

        for g in grp:
            f: Callable[[str], bool] = lambda x: x.find(f"{g}-") >= 0
            p: List[str] = sorted(list(filter(f, pngs)))
            an_pngs[g] = p

        return an_pngs

    def __resize_cursor(self, cur: str, size: int) -> Tuple[int, int]:
        """ Resize cursor .png file as @size """
        in_path = path.join(self.__bitmaps_dir, cur)
        out_dir = path.join(self.config_dir, f"{size}x{size}")
        out_path = path.join(out_dir, cur)
        if not path.exists(out_dir):
            os.makedirs(out_dir)

        # opening original image
        image = Image.open(in_path)
        width: float = image.size[0]
        height: float = image.size[1]

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
        thumb = image.crop(resize).resize((ideal_width, ideal_height), Image.ANTIALIAS)
        thumb.save(out_path)

        image.close()
        thumb.close()

        return self.__cords_parser.get_hotspots(
            path.splitext(cur)[0], (width, height), size
        )

    def __get_cfg_file(self, png_file: AnyStr) -> str:
        """ Generate .in file according to @png_file. """
        cfg: str = f"{path.splitext(png_file)[0].split('-')[0]}.in"
        return cfg

    def __write_cfg_file(self, cur: str, lines: List[str]) -> None:
        """ Write {@cur.in} file in @self.config_dir. """
        # sort line, So all lines in order according to size (24x24, 28x28, ..)
        lines.sort()
        # remove newline from EOF
        lines[-1] = lines[-1].rstrip("\n")
        with open(self.__get_cfg_file(cur), "w") as config_file:
            for line in lines:
                config_file.write(line)

    def __generate_static_cfgs(self) -> None:
        """ Generate static cursors `.in` config files according to @self.__sizes. """
        cursors = self.__list_static_png()
        for cur in cursors:
            lines: List[str] = []
            for size in self.__sizes:
                (xhot, yhot) = self.__resize_cursor(cur, size)
                lines.append(f"{size} {xhot} {yhot} {size}x{size}/{cur}\n")
            self.__write_cfg_file(cur, lines)

    def __generate_animated_cfgs(self) -> None:
        """ Generate animated cursors `.in` config files according to @self.__sizes. """
        self.__list_animated_png()

    def generate(self) -> None:
        self.__generate_animated_cfgs()
        self.__generate_static_cfgs()


if __name__ == "__main__":
    t = ThemeConfigsProvider(
        bitmaps_dir="/home/kaiz/Github/clickgen/examples/bitmaps",
        hotspots_file="/home/kaiz/Github/clickgen/examples/hotspots.json",
        sizes=[24, 25],
    )
    t.generate()
