import glob
import os

from clickgen.x11 import main as x11_gen
from clickgen.win import main as win_gen

config_ext = ('*.in', '*.ini')


def get_configs(dir: str) -> list:
    configs_grabbed = []

    for ext in config_ext:
        configs_grabbed.extend(
            glob.glob(os.path.abspath(os.path.join(dir, ext))))
    return configs_grabbed


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
        configs = get_configs(config_dir)
        if (len(configs) <= 0):
            raise FileNotFoundError('no configs found in %s' % in_path)
    except FileNotFoundError as err:
        print('Error:', err)
