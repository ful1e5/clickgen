#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from os import path
from typing import List, NamedTuple, Optional
from .providers.jsonparser import Hotspots


class ThemeInfo(NamedTuple):
    """ Metadata for cursor theme. """

    theme_name: str
    author: str
    url: str = "Unknown Source!"
    comment: Optional[str] = None


class ThemeSettings(NamedTuple):
    """ Core settings for building custom cursor theme. """

    bitmaps_dir: str
    sizes: List[int]
    hotspots: Hotspots
    animation_delay: int = 50
    out_dir: str = os.getcwd()


class Config:
    """ Configure `clickgen` cursor building process. """

    def __init__(
        self,
        info: ThemeInfo,
        settings: ThemeSettings,
    ) -> None:
        # Default Theme comment & url
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
        )

        # Logging config
        self.logs = False
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def toggle_logging(self) -> None:
        """
        Enable/Disable logging in clickgen. (@default Disable)
        """
        self.logs = not self.logs

        if self.logs:
            logging.disable(logging.NOTSET)
        else:
            logging.disable(logging.CRITICAL)

    def get_logger(self, name: str) -> logging.Logger:
        """ Get custom logger."""
        logger = logging.getLogger(name)
        return logger