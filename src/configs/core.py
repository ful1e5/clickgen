#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from os import path
from typing import NamedTuple, Optional


class Platforms(NamedTuple):
    """ Platforms settings(Default True in all platforms). """

    x11: bool = True
    win: bool = True


class CursorInfo(NamedTuple):
    """ Metadata for cursor theme. """

    theme_name: str
    author: str
    comment: Optional[str]
    url: Optional[str]


class Config:
    """ Configure `clickgen` cursor building process. """

    def __init__(
        self,
        info: CursorInfo,
        configs_dir: str,
        out_dir: Optional[str] = None,
    ) -> None:
        # Default Theme comment & url
        self.info: CursorInfo = info
        if not self.info.comment:
            self.info.comment = f"{self.info.theme_name} By {self.info.author}"
        if not self.info.url:
            self.info.url = ""

        self._configs_dir: str = path.abspath(configs_dir)
        if out_dir is None:
            # Set out_dir to Current Work Directory (Default)
            self._out_dir: str = path.abspath(os.getcwd())
        else:
            self._out_dir: str = path.abspath(out_dir)

        # Cursor platforms
        self.__platforms = Platforms()

        # Logging config
        self.logs = False
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    def set_platforms(self, x11: bool, win: bool) -> None:
        self.__platforms: Platforms = Platforms(x11=x11, win=win)

    def get_platforms(self) -> Platforms:
        return self.__platforms

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