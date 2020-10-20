#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import makedirs, path
from typing import Any, List, Literal, NamedTuple
from glob import glob
import sys


class BuildArguments(NamedTuple):
    """ `anicursorgen.py` CLI arguments structure."""

    add_shadows: bool
    blur: float
    color: Any
    down_shift: float
    right_shift: float


class WinCursorsBuilder:
    """
    Inspired by `anicursorgen.py`.
    https://github.com/ubuntu/yaru/blob/master/icons/src/cursors/anicursorgen.py
    """

    def __init__(self, config_dir: str, out_dir: str) -> None:
        self.__config_dir = config_dir
        self.__out_dir = out_dir

    def __anicursorgen(self, cfg_file: str) -> Literal[0, 1]:
        """ Generate Windows cursor from `.in` file."""

        args = BuildArguments(
            add_shadows=False,
            blur=3.125,
            color="0x00000040",
            down_shift=3.125,
            right_shift=9.375,
        )

        try:
            if (
                args.color[0] != "0"
                or args.color[1] not in ["x", "X"]
                or len(args.color) != 10
            ):
                raise ValueError

            args.color = (
                int(args.color[2:4], 16),
                int(args.color[4:6], 16),
                int(args.color[6:8], 16),
                int(args.color[8:10], 16),
            )
        except:
            print("Can't parse the color '{}'".format(args.color), file=sys.stderr)
            return 1

        out: str = path.join(
            self.__out_dir, f"{path.splitext(path.basename(cfg_file))[0]}"
        )
        in_cfg_buffer = open(cfg_file, "rb")
        out_buffer = open(out, "wb")

        # result = make_cursor_from(input_config, output_file, args)

        in_cfg_buffer.close()
        out_buffer.close()

        return 0

    def build(self) -> None:
        """ Generate Windows cursors from config files(look inside @self.__config_dir). """
        if not path.exists(self.__out_dir):
            makedirs(self.__out_dir)

        configs: List[str] = glob(f"{self.__config_dir}/*.in")

        try:
            if len(configs) <= 0:
                raise IOError(f"configs files not found in {self.__config_dir}")
            for config in configs:
                self.__anicursorgen(config)
        except IOError as error:
            print(error)
