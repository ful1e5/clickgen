#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import path
import os
import tempfile
from typing import AnyStr, Callable, Dict, List, Tuple, Union

from PIL import Image

from clickgen.providers.json_parser import HotspotsParser


class ThemeConfigsProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(
        self, bitmaps_dir: str, hotspots_file: AnyStr, sizes: List[int]
    ) -> None:
        self.__bitmaps_dir = bitmaps_dir
        self.__cords_parser: HotspotsParser = HotspotsParser(hotspots_file)
        self.__sizes = sizes
        self.config_dir = tempfile.mkdtemp(prefix="clickgen_")

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
        func: Callable[[str], bool] = lambda x: x.find("-") >= 0
        an_pngs: List[str] = list(filter(func, self.__get_png_files()))

        g_func: Callable[[str], str] = lambda x: x.split("-")[0]
        grps: List[str] = list(set(map(g_func, an_pngs)))

        d: Dict[str, List[str]] = {}

        for g in grps:
            func: Callable[[str], bool] = lambda x: x.find(g) >= 0
            d[g] = sorted(list(filter(func, an_pngs)))

        return d

    def __clean_cur_name(self, name: str) -> str:
        """ Remove framing postfix. """
        return path.splitext(name)[0].split("-")[0]

    def __resize_cursor(self, cur: str, size: int) -> Tuple[int, int]:
        """ Resize cursor .png file as @size. """
        in_path = path.join(self.__bitmaps_dir, cur)
        out_dir = path.join(self.config_dir, f"{size}x{size}")
        out_path = path.join(out_dir, cur)
        if not path.exists(out_dir):
            os.makedirs(out_dir)

        # opening original image
        image = Image.open(in_path)
        width: int = image.size[0]
        height: int = image.size[1]

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
            self.__clean_cur_name(cur), (width, height), size
        )

    def __write_cfg_file(self, cur: str, lines: List[str]) -> None:
        """ Write {@cur.in} file in @self.config_dir. """
        # sort line, So all lines in order according to size (24x24, 28x28, ..)
        lines.sort()
        # remove newline from EOF
        lines[-1] = lines[-1].rstrip("\n")
        cfg_path = path.join(self.config_dir, f"{self.__clean_cur_name(cur)}.in")
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
        cursors = self.__list_static_png()
        for cur in cursors:
            lines: List[str] = self.__generate_cursor(cur)
            self.__write_cfg_file(cur, lines)

    def __generate_animated_cfgs(self, delay: int) -> None:
        """ Generate animated cursors `.in` config files according to @self.__sizes. """
        d: Dict[str, List[str]] = self.__list_animated_png()

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
