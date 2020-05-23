import ctypes
import os

basedir = os.path.abspath(os.path.dirname(__file__))
libpath = os.path.join(basedir, 'xcursorgen.so')

dll = ctypes.CDLL(libpath)

LP_c_char = ctypes.POINTER(ctypes.c_char)
LP_LP_c_char = ctypes.POINTER(LP_c_char)

dll.main.argtypes = (ctypes.c_int, LP_LP_c_char)
dll.main.restypes = ctypes.c_int


def __gen_argv_ctypes(argv: list):
    p = (LP_c_char*len(argv))()
    for i, arg in enumerate(argv):  # not sys.argv, but argv!!!
        enc_arg = arg.encode('utf-8')
        p[i] = ctypes.create_string_buffer(enc_arg)
    return ctypes.cast(p, LP_LP_c_char)


def generate(argv: list):
    # add null at first position, unless xcurosrgen.c break
    argv.insert(0, '')
    argc = len(argv)

    na = __gen_argv_ctypes(argv)

    res = dll.main(argc, na)
    return res
