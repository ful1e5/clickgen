#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, NamedTuple, Optional


class Hotspot(NamedTuple):
    x: Optional[int] = None
    y: Optional[int] = None


class ImageSize(NamedTuple):
    width: int
    height: int


class MappedBitmaps(NamedTuple):
    static: List[str]
    animated: Dict[str, List[str]]
