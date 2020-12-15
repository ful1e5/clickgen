#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, NamedTuple, Optional

JsonData = Dict[str, Dict[str, int]]


class Hotspot(NamedTuple):
    x: Optional[int] = None
    y: Optional[int] = None


class ImageSize(NamedTuple):
    width: int
    height: int


class RenameCursor(NamedTuple):
    old: str
    new: str


class MappedBitmaps(NamedTuple):
    static: List[str]
    animated: Dict[str, List[str]]


class DBDocument(NamedTuple):
    name: str
    symlink: List[str]
    hotspot: Hotspot


WindowsCursorsConfig = Dict[str, Dict[str, str]]
