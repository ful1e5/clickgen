#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import logging
from os import PathLike, path
from typing import AnyStr


class ConfigProvider:
    """ Configure `clickgen` cursor building process. """

    def __init__(
        self,
        theme_name: str,
        comment: str,
        configs_dir: PathLike[AnyStr],
        out_dir: PathLike[AnyStr] = None,
    ) -> None:
        self._theme_name = theme_name
        self._comment = comment

        self._configs_dir = path.abspath(configs_dir)
        if out_dir is None:
            # Set out_dir to Current Work Directory (Default)
            self._out_dir = path.abspath(os.getcwd())
        else:
            self._out_dir = path.abspath(out_dir)

        # Cursor platforms
        self.x11: bool = True
        self.win: bool = True

        # Logging config
        self.logs = False
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

    @property
    def get_platforms(self) -> list[str]:
        """  Provide platforms for building cursors theme. """
        platform: list[str] = []

        if self.x11:
            platform.append("X11")
        if self.win:
            platform.append("WINDOWS")

        return platform

    @property
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