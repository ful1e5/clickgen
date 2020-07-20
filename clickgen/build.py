#!/usr/bin/env python
# encoding: utf-8

import os

from .__main__ import main
from .configsgen.__main__ import main as configsgen
from .configsgen.__main__ import DELAY

from .types import Path, IntegerList
from .helpers import TemporaryDirectory


def build_win_curosr_theme(name: str, image_dir: Path, cursor_sizes: IntegerList, hotspots: any = None, out_path: Path = os.getcwd(), archive: bool = False, delay: int = DELAY):
    """
    Build Functions for Windows Cursor Theme.
    `name` is folder name.
    `image_dir` is where all images are stored.Cursor naming is based on `image name`.
    `cursor_sizes` is pixel size for generating cursor(basically in `ineteger array`)
    `hotspots` is `JSON` data each cursor have `xhot` and `yhot` member.
     example:
        {
            "all_scroll": {
                "xhot":2
                "yhot":4
            }
        }
    """

    # generate configs to temporary directory
    with TemporaryDirectory() as configs:
        configsgen(image_dir, cursor_sizes, hotspots,
                   out_dir=configs, delay=delay)

        main(name=name, config_dir=configs, out_path=out_path,
             x11=False, win=True, archive=archive, logs=True)


def build_x11_curosr_theme(name: str, image_dir: Path, cursor_sizes: IntegerList, hotspots: any = None, out_path: Path = os.getcwd(), archive: bool = False, delay: int = DELAY):
    """
    Build Functions for Windows Cursor Theme.
    `name` is folder name.
    `image_dir` is where all images are stored.Cursor naming is based on `image name`.
    `cursor_sizes` is pixel size for generating cursor(basically in `ineteger array`)
    `hotspots` is `JSON` data each cursor have `xhot` and `yhot` member.
     example:
        {
            "all_scroll": {
                "xhot":2
                "yhot":4
            }
        }
    """

    # generate configs to temporary directory
    with TemporaryDirectory() as configs:
        configsgen(image_dir, cursor_sizes, hotspots,
                   out_dir=configs, delay=delay)

        main(name=name, config_dir=configs, out_path=out_path,
             x11=True, win=False, archive=archive, logs=True)


def build_cursor_theme(name: str, image_dir: Path, cursor_sizes: IntegerList, hotspots: any = None, out_path: Path = os.getcwd(), archive: bool = False, delay: int = DELAY):
    """
    Build Functions for Windows Cursor Theme.
    `name` is folder name.
    `image_dir` is where all images are stored.Cursor naming is based on `image name`.
    `cursor_sizes` is pixel size for generating cursor(basically in `ineteger array`)
    `hotspots` is `JSON` data each cursor have `xhot` and `yhot` member.
     example:
        {
            "all_scroll": {
                "xhot":2
                "yhot":4
            }
        }
    """

    # generate configs to temporary directory
    with TemporaryDirectory() as configs:
        configsgen(image_dir, cursor_sizes, hotspots,
                   out_dir=configs, delay=delay)

        # build package
        main(name=name, config_dir=configs, out_path=out_path,
             x11=True, win=True, archive=archive, logs=True)
