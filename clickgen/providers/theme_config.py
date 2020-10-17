#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
import itertools
from os import path
import tempfile
from typing import AnyStr, Callable, List

from json_parser import HotspotsParser


class ThemeConfigsProvider:
    """ Configure `clickgen` cursor building process. """

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

    def __get_cfg_file(self, png_file: AnyStr) -> str:
        """ Generate .in file according to @png_file. """
        cfg: str = f"{path.splitext(png_file)[0].split('-')[0]}.in"
        return cfg

    def __init__(
        self, bitmaps_dir: str, hotspots_file: AnyStr, sizes: List[int]
    ) -> None:
        self.__bitmaps_dir = bitmaps_dir
        self.__cords_parser = HotspotsParser(hotspots_file)
        self.__pngs = self.__get_png_files()
        self.__sizes = sizes
        self.config_dir = tempfile.mkdtemp()

    def __list_static_png(self, is_animated: bool = False) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") <= 0
        st_pngs: List[str] = list(filter(func, self.__pngs))
        return st_pngs

    def __list_animated_png(self, is_animated: bool = False) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") >= 0
        an_pngs: List[str] = list(filter(func, self.__pngs))
        return an_pngs

    def __generate_static_cfgs(self) -> None:
        cursors = self.__list_static_png()

        for i, j in itertools.product(self.__sizes, cursors):
            print(f"{i} xxxxxx {j}")

    def __generate_animated_cfgs(self) -> None:
        self.__list_animated_png()

    def generate(self) -> None:
        self.__generate_animated_cfgs()
        self.__generate_static_cfgs()


if __name__ == "__main__":
    t = ThemeConfigsProvider(
        bitmaps_dir="/home/kaiz/Github/clickgen/examples/bitmaps",
        hotspots_file="/home/kaiz/Github/clickgen/examples/hotspots.json",
        sizes=[24, 28],
    )
    t.generate()
