#!/usr/bin/env python
# -*- coding: utf-8 -*-

from glob import glob
from os import PathLike, path
from typing import AnyStr, List, Union, Callable
from clickgen.providers.json_parser import HotspotsParser


class CursorsConfigFileProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(self, bitmaps_dir: str, hotspots_file=PathLike[AnyStr]) -> None:
        self.__bitmaps_dir = bitmaps_dir
        self.__cords_parser = HotspotsParser(hotspots_file)

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

    def __list_static_cursors(self, is_animated: bool = False) -> List[str]:
        """ Return cursors list inside `bitmaps_dir` that doesn't had frames. """
        pngs: List[str] = self.__get_png_files()

        return pngs

    def get_config(self, cursor_name: str) -> Union[PathLike[AnyStr], str]:
        """ Return `.in` file path. """
        return cursor_name
