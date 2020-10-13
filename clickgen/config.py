#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import PathLike, path
from typing import AnyStr


class ConfigProvider:
    """Configure `clickgen` cursor building process."""

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
