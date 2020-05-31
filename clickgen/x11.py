"""
    xcursorgen.c python api
"""

import ctypes
import os

basedir = os.path.abspath(os.path.dirname(__file__))
libpath = os.path.join(basedir, 'xcursorgen.so')

dll = ctypes.CDLL(libpath)

# main function ctypes define
LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_LP_c_char = ctypes.POINTER(LP_c_char)

dll.main.argtypes = (ctypes.c_int, LP_LP_c_char)


def gen_argv_ctypes(argv: list) -> LP_LP_c_char:
    p = (LP_c_char * len(argv))()

    for i, arg in enumerate(argv):  # not sys.argv, but argv!!!
        enc_arg = str(arg).encode('utf-8')
        p[i] = ctypes.create_string_buffer(enc_arg)

    return ctypes.cast(p, LP_LP_c_char)


def generate(argc: int, argv: list) -> None:
    na = gen_argv_ctypes(argv)
    dll.main(argc, na)


def main(input_config: str, output_file: str, prefix: str) -> None:

    # binary name as first argument
    argv = ['xcursorgen', '-p', prefix, input_config, output_file]
    argc = len(argv)

    generate(argc, argv)
