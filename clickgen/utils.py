import os
from clickgen.x11 import main as x11_gen
from clickgen.win import main as win_gen


def main(config_dir: str,
         out_path: str,
         name: str,
         x11: bool = True,
         win: bool = True,
         archive: bool = False) -> None:

    try:
        if (x11 == False & win == False):
            raise ValueError('cursor generation type missing')
    except ValueError as valerr:
        print('Error:', valerr)

    in_path = os.path.abspath(config_dir)
    out_path = os.path.abspath(out_path)

    x11_gen(in_path, out_path)
