#!/usr/bin/env python
# encoding: utf-8

import os

from .__main__ import main
from .configsgen.__main__ import main as configsgen
from .types import Path, IntegerList
from .helpers import TemporaryDirectory


# TODO: Tests
def build_win_curosr_theme(name: str, image_dir: Path, cursor_sizes: IntegerList, hotspots: any = None, out_path: Path = os.getcwd(), archive: bool = False):

    # generate configs to temporary directory
    with TemporaryDirectory() as configs:
        configsgen(image_dir, cursor_sizes, hotspots, out_dir=configs)

        main(name=name, config_dir=configs, out_path=out_path,
             x11=False, win=True, archive=archive, logs=True)


# TODO: Tests
def build_x11_curosr_theme(name: str, image_dir: Path, cursor_sizes: IntegerList, hotspots: any = None, out_path: Path = os.getcwd(), archive: bool = False):

    # generate configs to temporary directory
    with TemporaryDirectory() as configs:
        configsgen(image_dir, cursor_sizes, hotspots, out_dir=configs)

        main(name=name, config_dir=configs, out_path=out_path,
             x11=True, win=False, archive=archive, logs=True)


# TODO: Tests
def build_cursor_theme(name: str, image_dir: Path, cursor_sizes: IntegerList, hotspots: any = None, out_path: Path = os.getcwd(), archive: bool = False):

    # generate configs to temporary directory
    with TemporaryDirectory() as configs:
        configsgen(image_dir, cursor_sizes, hotspots, out_dir=configs)

        # build package
        main(name=name, config_dir=configs, out_path=out_path,
             x11=True, win=True, archive=archive, logs=True)
