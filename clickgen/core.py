#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import tempfile
from pathlib import Path, PurePath
from typing import List, Sequence, Union

from clickgen.constants import WIN_BITMAPS_SIZE
from clickgen.providers.bitmaps import Bitmaps
from clickgen.providers.config import CursorConfig
from clickgen.typing.core import Config, ThemeInfo, ThemeSettings
from clickgen.typing.image import ImageSize
from clickgen.util import goto_cursors_dir, remove
from clickgen.windows.builder import WinCursorBuilder
from clickgen.windows.packager import WinPackager
from clickgen.x11.builder import XCursorBuilder
from clickgen.x11.packager import XPackager


def link_missing_cursors(cursors_dir: Path, root: str, symlink: List[str]) -> None:
    with goto_cursors_dir(cursors_dir):
        for link in symlink:
            try:
                os.symlink(root, link)
            except FileExistsError:
                continue


def create_theme(config: Config):
    info: ThemeInfo = config.info
    sett: ThemeSettings = config.settings

    sizes: List[ImageSize] = []
    for s in sett.sizes:
        sizes.append(ImageSize(width=s, height=s))

    # Setup temporary directories
    x_config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_x_configs_"))
    win_config_dir: Path = Path(tempfile.mkdtemp(prefix="clickgen_win_configs_"))

    xtmp: Path = Path(tempfile.mkdtemp(prefix="xbu"))
    wtmp: Path = Path(tempfile.mkdtemp(prefix="wbu"))

    bits = Bitmaps(
        sett.bitmaps_dir.absolute(),
        hotspots=sett.hotspots,
        win_cursors_cfg=sett.windows_cfg,
    )

    # Creating 'XCursors'
    x_bitmaps = bits.x_bitmaps()
    for png in x_bitmaps.static:
        node = bits.db.cursor_node_by_name(png.split(".")[0])
        hotspot = node.hotspot

        cfg_file: Path = CursorConfig(
            bits.x_bitmaps_dir, hotspot, sizes=sizes, config_dir=x_config_dir
        ).create_static(png)
        x = XCursorBuilder(cfg_file, xtmp)
        x.generate()

        if node.symlink:
            link_missing_cursors(x.cursors_dir, cfg_file.stem, node.symlink)

    for key, pngs in x_bitmaps.animated.items():
        node = bits.db.cursor_node_by_name(key)

        hotspot = node.hotspot

        cfg_file: Path = CursorConfig(
            bits.x_bitmaps_dir, hotspot, sizes=sizes, config_dir=x_config_dir
        ).create_animated(key, pngs, sett.animation_delay)
        x = XCursorBuilder(cfg_file, xtmp)
        x.generate()

        if node.symlink:
            link_missing_cursors(x.cursors_dir, cfg_file.stem, node.symlink)

    XPackager(xtmp, info).save()

    # Creating 'Windows Cursors'
    win_bitmaps = bits.win_bitmaps()
    win_size: List[ImageSize] = [WIN_BITMAPS_SIZE]
    for png in win_bitmaps.static:
        node = bits.db.cursor_node_by_name(png.split(".")[0])
        hotspot = node.hotspot

        cfg_file: Path = CursorConfig(
            bits.win_bitmaps_dir,
            hotspot,
            sizes=win_size,
            config_dir=win_config_dir,
        ).create_static(png)
        WinCursorBuilder(cfg_file, wtmp).generate()

    for key, pngs in win_bitmaps.animated.items():
        node = bits.db.cursor_node_by_name(key)
        hotspot = node.hotspot

        cfg_file: Path = CursorConfig(
            bits.win_bitmaps_dir,
            hotspot,
            sizes=win_size,
            config_dir=win_config_dir,
        ).create_animated(key, pngs, delay=3)
        WinCursorBuilder(cfg_file, wtmp).generate()

    WinPackager(wtmp, info, cursors=bits.win_cursors_cfg.keys()).save()

    if not sett.out_dir.exists():
        os.makedirs(sett.out_dir)

    x_dir = sett.out_dir / info.theme_name
    win_dir = sett.out_dir / f"{info.theme_name}-Windows"
    remove(win_dir)
    remove(x_dir)

    shutil.copytree(xtmp, x_dir)
    shutil.copytree(wtmp, win_dir)

    bits.remove_tmp_bitmaps()
    shutil.rmtree(xtmp)
    shutil.rmtree(wtmp)


_P = Union[str, Path]
_PSequence = List[_P]

PurePath


class CursorBitmap:
    animated: bool
    png: Path
    cursor_key: str
    pngs: List[Path] = []

    def __init__(self, png: Union[_P, _PSequence]) -> None:
        if isinstance(png, str) or isinstance(png, Path):
            self.animated = False
            self.png = Path(png)
            self.cursor_key = self.png.stem
        elif isinstance(png, list):
            for p in png.sort():
                self.pngs.append(Path(p))
            self.animated = True
            self.cursor_key = self.pngs[0].stem.rsplit("-", 1)
        else:
            raise Exception(
                f"CursorBitmap: Unable to parse argument 'png' with Type {type(png)}"
            )
