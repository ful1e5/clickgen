#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, NamedTuple


class Hotspot(NamedTuple):
    x: int
    y: int


class ImageSize(NamedTuple):
    width: int
    height: int


class Bitmaps(NamedTuple):
    static: List[str]
    animated: Dict[str, List[str]]


WindowsCursorsConfig = Dict[str, Dict[str, str]]
