#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Literal, NamedTuple, Optional

from clickgen.Type.image import ImageSize

JsonData = Dict[str, Dict[str, int]]


class WinConfigData(NamedTuple):
    x_cursor: str
    size: ImageSize = ImageSize(24, 24)
    placement: Literal[
        "top_left", "top_right", "bottom_right", "bottom_right", "center"
    ] = "center"
    bitmap_size: ImageSize = ImageSize(32, 32)


WindowsConfig = Dict[str, WinConfigData]


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
