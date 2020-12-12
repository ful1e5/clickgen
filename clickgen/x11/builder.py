#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
from ctypes import CDLL
from pathlib import Path
from typing import Any, List

from .. import __path__ as pkg_root
from .._util import remove


class XCursorBuilder:
    """ Build X11 cursor from `.in` config file. """

    # main function ctypes define
    _lib_location: Path = Path(pkg_root[0]) / "xcursorgen.so"
    _lib: CDLL = CDLL(_lib_location)
    _LP_c_char = ctypes.POINTER(ctypes.c_char)
    _LP_LP_c_char = ctypes.POINTER(_LP_c_char)
    _lib.main.argtypes = (ctypes.c_int, _LP_LP_c_char)

    def __init__(
        self,
        config_file: Path,
        out_dir: Path,
    ) -> None:
        if not config_file.exists() or not config_file.is_file():
            raise FileNotFoundError(f"'{config_file.name}' Config file not found")

        self.config_file: Path = config_file
        self.prefix: Path = config_file.parent
        self.out_dir: Path = out_dir
        self.cursors_dir: Path = self.out_dir / "cursors"

        if not self.cursors_dir.exists():
            self.cursors_dir.mkdir()

        self.out: Path = self.cursors_dir / self.config_file.stem

    def gen_argv_ctypes(self, argv: List[str]) -> Any:
        """ Convert `string` arguments to `ctypes` pointer. """
        p = (self._LP_c_char * len(argv))()

        for i, arg in enumerate(argv):
            enc_arg: bytes = str(arg).encode("utf-8")
            p[i] = ctypes.create_string_buffer(enc_arg)

        return ctypes.cast(p, self._LP_LP_c_char)

    def generate(self) -> None:
        """ Generate x11 cursor from `.in` file."""

        # remove old cursor file
        remove(self.out)

        argv: List[str] = [
            "xcursorgen",
            "-p",  # prefix args for xcursorgen (do not remove)
            self.prefix.absolute(),  # prefix args for xcursorgen (do not remove)
            self.config_file.absolute(),  # {cursor}.in file
            self.out.absolute(),
        ]

        kwargs: ctypes.pointer[ctypes.c_char] = self.gen_argv_ctypes(argv)
        args: ctypes.c_int = ctypes.c_int(len(argv))

        self._lib.main(args, kwargs)
