#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, NamedTuple, Optional


JsonData = Dict[str, Dict[str, int]]


class Hotspot(NamedTuple):
    x: int
    y: int

class OptionalHotspot(NamedTuple):
    x:Optional[int]
    y:Optional[int]

class ImageSize(NamedTuple):
    width: int
    height: int


class MappedBitmaps(NamedTuple):
    static: List[str]
    animated: Dict[str, List[str]]


WindowsCursorsConfig = Dict[str, Dict[str, str]]
