#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import tempfile
from os import makedirs, path
from pathlib import Path
from typing import List

from ._typing import ImageSize
from .builders.winbuilder import WinCursorsBuilder
from .builders.x11builder import X11CursorsBuilder
from .configs import Config, ThemeInfo, ThemeSettings
from .db import Database
from .packagers.windows import WindowsPackager
from .packagers.x11 import X11Packager
from .providers.bitmaps import Bitmaps
from .providers.themeconfig import CursorConfig, ThemeConfigsProvider


def create_theme(config: Config) -> None:
    """ Create cursors theme from `bitmaps`. """
    info: ThemeInfo = config.info
    sett: ThemeSettings = config.settings

    # Cursors '.in' files generator
    config_dir: str = ThemeConfigsProvider(
        bitmaps_dir=sett.bitmaps_dir,
        hotspots=sett.hotspots,
        sizes=sett.sizes,
    ).generate(sett.animation_delay)

    # Setup temporary directories
    xtmp: str = tempfile.mkdtemp(prefix="xbu")
    wtmp: str = tempfile.mkdtemp(prefix="wbu")

    # Building Themes
    WinCursorsBuilder(config_dir, wtmp).build()
    WindowsPackager(wtmp, info).pack()

    X11CursorsBuilder(config_dir, xtmp).build()
    X11Packager(xtmp, info).pack()

    # Move themes to @out_dir
    if not path.exists(sett.out_dir):
        makedirs(sett.out_dir)

    xdst: str = path.join(sett.out_dir, info.theme_name)
    if path.exists(xdst):
        shutil.rmtree(xdst)
    shutil.move(xtmp, xdst)

    wdst: str = path.join(sett.out_dir, f"{info.theme_name}-Windows")
    if path.exists(wdst):
        shutil.rmtree(wdst)
    shutil.move(wtmp, wdst)


def create_theme_with_db(config: Config):
    info: ThemeInfo = config.info
    sett: ThemeSettings = config.settings

    db = Database()

    bits_dir = Path(sett.bitmaps_dir)
    sizes: List[ImageSize] = []
    for s in sett.sizes:
        sizes.append(ImageSize(width=s, height=s))

    bits = Bitmaps(bits_dir, db=db, windows_cursors=sett.windows_cfg)

    # Creating 'XCursors'
    x_bitmaps = bits.x_bitmaps()
    for png in x_bitmaps.static:
        fp: Path = bits.x_bitmaps_dir / png
        CursorConfig(fp, hotspot=sett.hotspots, sizes=sizes)
