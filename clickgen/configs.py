#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
from typing import Dict, List, NamedTuple, Optional, Union

from .providers.jsonparser import Hotspots


class ThemeInfo(NamedTuple):
    """ Information of cursor theme. """

    theme_name: str
    author: str
    url: str = "Unknown Source!"
    comment: Optional[str] = None


class ThemeSettings(NamedTuple):
    """ Core settings of cursor theme. """

    bitmaps_dir: str
    sizes: List[int]
    hotspots: Hotspots
    animation_delay: int = 50
    out_dir: str = os.getcwd()
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

        self.settings: ThemeSettings = ThemeSettings(
            bitmaps_dir=path.abspath(settings.bitmaps_dir),
            sizes=settings.sizes,
            hotspots=settings.hotspots,
            animation_delay=settings.animation_delay,
            out_dir=path.abspath(settings.out_dir),
            windows_cfg=settings.windows_cfg,
        )
