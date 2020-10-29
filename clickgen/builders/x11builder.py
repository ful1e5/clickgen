#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
from ctypes import CDLL, c_char, pointer
from glob import glob
from os import makedirs, path, remove
import sys
from typing import Any, List

from .. import __path__ as pkg_root

lib_xcursorgen: str = path.join(pkg_root[0], "xcursorgen.so")


class X11CursorsBuilder:
    """ Build X11 cursors from `.in` configs files. """

    def __init__(
        self,
        config_dir: str,
        out_dir: str,
    ) -> None:
        self.__config_dir = config_dir
        self.__out_dir = out_dir
        self.__cursors_dir = path.join(self.__out_dir, "cursors")

        # main function ctypes define
        self.__lib: CDLL = CDLL(lib_xcursorgen)
        self.__LP_c_char = ctypes.POINTER(ctypes.c_char)
        self.__LP_LP_c_char = ctypes.POINTER(self.__LP_c_char)
        self.__lib.main.argtypes = (ctypes.c_int, self.__LP_LP_c_char)

    def __gen_argv_ctypes(self, argv: List[str]) -> Any:
        """ Convert `string` arguments to `ctypes` pointer. """
        p = (self.__LP_c_char * len(argv))()

        for i, arg in enumerate(argv):
            enc_arg: bytes = str(arg).encode("utf-8")
            p[i] = ctypes.create_string_buffer(enc_arg)

        return ctypes.cast(p, self.__LP_LP_c_char)

    def __generate_x11_cursor(
        self,
        cfg_file: str,
    ) -> None:
        """ Generate x11 cursor from `.in` file."""
        out: str = path.join(
            self.__cursors_dir, path.splitext(path.basename(cfg_file))[0]
        )

        # remove old cursor file
        if path.exists(out):
            remove(out)

        argv: List[str] = [
            "xcursorgen",
            "-p",  # prefix args for xcursorgen (do not remove)
            self.__config_dir,  # prefix args for xcursorgen (do not remove)
            cfg_file,  # {cursor}.in file
            out,
        ]
        kwargs: pointer[c_char] = self.__gen_argv_ctypes(argv)
        args: ctypes.c_int = ctypes.c_int(len(argv))
        self.__lib.main(args, kwargs)

    def build(self) -> None:
        """ Generate x11 cursors from config files(look inside @self.__config_dir). """
        if not path.exists(self.__cursors_dir):
            makedirs(self.__cursors_dir)

        configs: List[str] = glob(f"{self.__config_dir}/*.in")

        if len(configs) <= 0:
            print(f"Cursors configs not found in {self.__config_dir}", file=sys.stderr)
        else:
            for config in configs:
                self.__generate_x11_cursor(config)
