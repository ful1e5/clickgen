#!/usr/bin/env python
# -*- coding: utf-8 -*-

from io import BufferedReader, BufferedWriter
from os import makedirs, path
from sys import prefix
from typing import Any, List, Literal, NamedTuple, Optional, Set, Tuple
from glob import glob
import sys
import shlex


class AnicursorgenArgs(NamedTuple):
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

    def __get_out_file(self, cfg_file: str) -> str:
        out: str = path.join(
            self.__out_dir, f"{path.splitext(path.basename(cfg_file))[0]}"
        )
        with open(cfg_file, "r") as f:
            l = f.readline()
            words = shlex.split(l.rstrip("\n").rstrip("\r"))
            if len(words) > 4:
                out = f"{out}.ani"
            else:
                out = f"{out}.cur"

        return out

    def __parse_config_from(
        self, in_buffer: BufferedReader, prefix: str
    ) -> List[Tuple[int, int, int, str, int]]:
        """ Parse `.in` config file buffer. """
        frames: List[Tuple[int, int, int, str, int]] = []

        for line in in_buffer.readlines():
            line = line.decode()
            words = shlex.split(line.rstrip("\n").rstrip("\r"))
            # print(words)
            if len(words) < 4:
                continue

            try:
                size = int(words[0])
                xhot = int(words[1]) - 1
                yhot = int(words[2]) - 1
                filename = words[3]
                if not path.isabs(filename):
                    filename = path.join(prefix, filename)
            except:
                continue

            if len(words) > 4:
                try:
                    duration = int(words[4])
                except:
                    continue
            else:
                duration = 0

            frames.append((size, xhot, yhot, filename, duration))

        return frames

    def __frames_have_animation(
        self, frames: List[Tuple[int, int, int, str, int]]
    ) -> bool:
        """ For checking @frames have animation. """
        sizes: Set[int] = set()
        for frame in frames:
            if frame[4] == 0:
                continue
            if frame[0] in sizes:
                return True
            sizes.add(frame[0])

        return False

    def __make_cursor_from(
        self,
        in_buffer: BufferedReader,
        out_buffer: BufferedWriter,
        args: AnicursorgenArgs,
    ) -> Literal[0, 1]:
        """ Generate Windows cursor from `.in` file."""

        exec_code: Literal[0, 1] = 0
        frames = self.__parse_config_from(in_buffer, prefix=self.__config_dir)

        animated = self.__frames_have_animation(frames)

        # if animated:
        #     exec_code = make_ani(frames, out, args)
        # else:
        #     buf = make_cur(frames, args)
        #     copy_to(out, buf)

        return exec_code

    def __anicursorgen(self, cfg_file: str, args: AnicursorgenArgs) -> Literal[0, 1]:
        """ `anicursorgen.py` @main function. """

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

        in_cfg_buffer = open(cfg_file, "rb")
        out_buffer = open(self.__get_out_file(cfg_file), "wb")

        exec_code = self.__make_cursor_from(in_cfg_buffer, out_buffer, args)

        in_cfg_buffer.close()
        out_buffer.close()

        return exec_code

    def build(self) -> None:
        """ Generate Windows cursors from config files(look inside @self.__config_dir). """
        if not path.exists(self.__out_dir):
            makedirs(self.__out_dir)

        configs: List[str] = glob(f"{self.__config_dir}/*.in")
        args = AnicursorgenArgs(
            add_shadows=False,
            blur=3.125,
            color="0x00000040",
            down_shift=3.125,
            right_shift=9.375,
        )

        try:
            if len(configs) <= 0:
                raise IOError(f"configs files not found in {self.__config_dir}")
            for config in configs:
                self.__anicursorgen(config, args)
        except IOError as error:
            print(error)
