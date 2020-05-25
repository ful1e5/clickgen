import os
from . import x11, win


def main(config_dir, out_path, name, x11=True, win=True, archive=False):

    try:
        if (x11 == False & win == False):
            raise ValueError('cursor generation type missing')
    except ValueError as valerr:
        print('Error:', valerr)

    in_path = os.path.abspath(config_dir)
    out_path = os.path.abspath(out_path)

    print(in_path, out_path, name)
