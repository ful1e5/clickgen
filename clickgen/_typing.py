#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, Literal, NamedTuple, Optional


JsonData = Dict[str, Dict[str, int]]


class Hotspot(NamedTuple):
    x: int
    y: int


class OptionalHotspot(NamedTuple):
    x: Optional[int]
    y: Optional[int]


class ImageSize(NamedTuple):
    width: int
    height: int


class RenameCursor(NamedTuple):
    old: str
    new: str


class MappedBitmaps(NamedTuple):
    static: List[str]
    animated: Dict[str, List[str]]


WindowsCursorsConfig = Dict[str, Dict[str, str]]
WindowsSizes = Literal["normal", "large"]
