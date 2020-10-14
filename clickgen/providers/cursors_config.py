#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.providers.json_parser import HotspotsParser
from os import PathLike
from typing import AnyStr, Union


class CursorsConfigFileProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(
        self, bitmaps_dir: PathLike[AnyStr], hotspots_file=PathLike[AnyStr]
    ) -> None:
        self.__bitmaps_dir = bitmaps_dir
        self.__cor_parser = HotspotsParser(hotspots_file)

    def __list_static_cursors(self, is_animated: bool = False) -> list[str]:
        """ Return cursors list inside `bitmaps_dir`"""
        l: list[str] = ["a", "b"]
        return l

    def get_config(self, cursor_name: str) -> Union[PathLike[AnyStr], str]:
        """ Return Config(`.in`) file path. """
        return cursor_name
