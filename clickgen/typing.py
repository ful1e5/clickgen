#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

JsonData = Dict[str, Dict[str, int]]


class ThemeInfo(NamedTuple):
    """ Information of cursor theme. """

    theme_name: str
    author: str
    url: Optional[str] = None
    comment: Optional[str] = None


class ThemeSettings(NamedTuple):
    """ Core settings of cursor theme. """

    bitmaps_dir: Path
    sizes: List[int]
    hotspots: JsonData
    animation_delay: int = 50
    out_dir: Path = Path.cwd()
    windows_cfg: Optional[Dict[str, str]] = None


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
