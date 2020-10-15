#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import PathLike, path
from typing import AnyStr, List, Union, Callable
from clickgen.providers.json_parser import HotspotsParser


class ThemeConfigsProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(self, bitmaps_dir: str, hotspots_file=PathLike[AnyStr]) -> None:
        self.__bitmaps_dir = bitmaps_dir
        self.__cords_parser = HotspotsParser(hotspots_file)
        self.__pngs = self.__get_png_files()

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

    def __list_static_png(self, is_animated: bool = False) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") <= 0
        pngs: List[str] = list(filter(func, self.__pngs))
        return pngs

    def __list_animated_png(self, is_animated: bool = False) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        func: Callable[[str], bool] = lambda x: x.find("-") >= 0
        pngs: List[str] = list(filter(func, self.__pngs))
        return pngs

    def get_cfg_dir(self, cursor_name: str) -> Union[PathLike[AnyStr], str]:
        """ Return `.in` file path. """
        return cursor_name
