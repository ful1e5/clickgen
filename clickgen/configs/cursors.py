#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import PathLike
from typing import AnyStr


class CursorsConfigFileProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(self, bitmaps_dir: PathLike[AnyStr]) -> None:
        self._bitmaps_dir = bitmaps_dir