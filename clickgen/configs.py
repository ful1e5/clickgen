#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional
from ._typing import JsonData


class ThemeInfo(NamedTuple):
    """ Information of cursor theme. """

    theme_name: str
    author: str
    url: str = "Unknown Source!"
    comment: Optional[str] = None


class ThemeSettings(NamedTuple):
    """ Core settings of cursor theme. """

    bitmaps_dir: Path
    sizes: List[int]
    hotspots: JsonData
    animation_delay: int = 50
    out_dir: Path = Path.cwd()
    windows_cfg: Optional[Dict[str, str]] = None


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
