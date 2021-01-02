#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, List, Tuple

from clickgen.builders.windows import WindowsCursor
from clickgen.builders.x11 import XCursor
from clickgen.core import CursorAlias
from clickgen.packagers import WinPackager, XPackager

from configure import get_config

X_SIZES: List[Tuple[int, int]] = [(24, 24), (32, 32)]

x_out_dir = Path("themes") / "Xpro"
win_out_dir = Path("themes") / "Xpro-Windows"


def win_build(item: Any, alias: CursorAlias) -> None:
    position = item["position"]
    size = item["size"]
    win_key = item["win_key"]
    canvas_size = item["canvas_size"]

    win_cfg = alias.reproduce(size, canvas_size, position, delay=3).rename(win_key)
    WindowsCursor.build_from(win_cfg, win_out_dir)


def build() -> None:
    config = get_config()

    # Building
    for _, item in config.items():
        png = item["png"]
        hotspot = item["hotspot"]
        delay = item["delay"]

        with CursorAlias.create_from(png, hotspot) as alias:
            x_cfg = alias.alias(X_SIZES, delay)
            XCursor.build_from(x_cfg, x_out_dir)

            if item.get("win_key"):
                win_build(item, alias)

    theme_name: str = "Example"
    comment: str = "Example theme generated from clickgen"
    author: str = "Kaiz Khatri"
    url: str = "https://github.com/ful1e5/clickgen/tree/main/examples"

    XPackager(x_out_dir, theme_name, comment)
    WinPackager(win_out_dir, theme_name, comment, author, url)


build()