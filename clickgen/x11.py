#!/usr/bin/env python
# encoding: utf-8

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
    """
        Call to xcursorgen.c 'main' function.
        'argc' is length of arguments,i.e: length of list.
        'argv' is list of arguments. Each command-line argument separated by ' '(Space) in C, but here by 'elements' of list.
        for example:

        In Terminal:
            ~$ xcursorgen -v

        In list:
            ['xcursorgen','-v']
            ['xcursorgen','-p','<png_dir>','<path_to_input_config>','<path_to_output_file>']

        In list binary_name as the first element is mandatory for executing the binary here is 'xcursorgen'.
    """
    na = gen_argv_ctypes(argv)
    dll.main(argc, na)


def main(input_config: str, output_file: str, prefix: str) -> None:
    """
         xcursorgen.c python api
        'input_config' is path to config_file.
        'output_file' is a path to store process cursor.
        In 'input_config' & 'output_file' absolute or relative both aceptable.
        'prefix' is a path to '.png files' link in the config_file, if relative path implemented.
    """
    # binary name as first argument
    argv = ['xcursorgen', '-p', prefix, input_config, output_file]
    argc = len(argv)

    generate(argc, argv)
