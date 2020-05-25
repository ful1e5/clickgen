import glob
import os

from clickgen.x11 import main as x11_gen
from clickgen.win import main as win_gen

config_ext = ('*.in', '*.ini')


def have_configs(dir: str) -> bool:
    files_grabbed = []

    for files in config_ext:
        files_grabbed.extend(glob.glob(files))

    if len(files_grabbed) >= 0:
        return True
    else:
        return False


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

    try:
        flag = have_configs(config_dir)
        if (flag == True):
            raise FileNotFoundError('no configs files found in %s' % in_path)
    except FileNotFoundError as err:
        print('Error:', err)
