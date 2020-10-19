#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
from ctypes import CDLL, c_char, pointer
from os import path
from typing import Any, List

lib_path: str = path.join(__file__, path.abspath("../../libs/xcursorgen.so"))
xcursorgen: CDLL = CDLL(lib_path)

# main function ctypes define
LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_LP_c_char = ctypes.POINTER(LP_c_char)
xcursorgen.main.argtypes = (ctypes.c_int, LP_LP_c_char)


def gen_argv_ctypes(argv: List[str]) -> Any:
    """ Convert `string` arguments to `ctypes` pointer. """
    p = (LP_c_char * len(argv))()

    for i, arg in enumerate(argv):
        enc_arg: bytes = str(arg).encode("utf-8")
        p[i] = ctypes.create_string_buffer(enc_arg)

    return ctypes.cast(p, LP_LP_c_char)


def generate_x11_cursor(cfg_file_path: str, out_path: str, prefix: str) -> None:
    """ Generate x11 cursor from `.in` file."""
    argv: List[str] = ["xcursorgen", "-p", prefix, cfg_file_path, out_path]

    kwargs: pointer[c_char] = gen_argv_ctypes(argv)
    args: ctypes.c_int = ctypes.c_int(len(argv))

    xcursorgen.main(args, kwargs)
