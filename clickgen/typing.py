#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, NamedTuple, Optional


# ***** Importants *****


JsonData = Dict[str, Dict[str, int]]
WindowsConfig = Dict[str, Dict[str, str]]


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
    windows_cfg: Optional[WindowsConfig] = None


class Config:
    """ Configure `clickgen` modules. """

    def __init__(
        self,
        info: ThemeInfo,
        settings: ThemeSettings,
    ) -> None:
        # Default "comment" for cursor theme
        comment: str = f"{info.theme_name} By {info.author}"
        if info.comment:
            comment = info.comment

        self.info: ThemeInfo = ThemeInfo(
            theme_name=info.theme_name,
            author=info.author,
            comment=comment,
            url=info.url,
        )

        self.settings: ThemeSettings = settings


# ***** Image Related *****


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


# ***** Database Related *****


class DBDocument(NamedTuple):
    name: str
    symlink: List[str]
    hotspot: Hotspot
