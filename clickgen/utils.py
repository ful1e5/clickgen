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


def create_dir(path: str) -> None:
    isExists = os.path.exists(path)

    if (isExists == False):
        os.mkdir(path)


def get_cur_name(config: str, type: str, animated: bool) -> str:
    config_name = os.path.basename(config)

    try:
        if (type == None):
            raise ValueError("`type` not defined in get_cur_name()")
        if (animated == None):
            raise ValueError("`animated` not deined in get_cur_name()")
    except ValueError as err:
        print('Error:', err)

    if (type == 'win' and animated == False):
        return config_name.replace('.in', '.cur')
    elif (type == 'win' and animated == True):
        return config_name.replace('.in', '.ani')
    elif (type == 'x11'):
        return config_name.replace('.in', '')
    else:
        return ""


def main(config_dir: str,
         out_path: str,
         name: str,
         x11: bool = False,
         win: bool = False,
         archive: bool = False) -> None:

    try:
        if (x11 == False and win == False):
            raise ValueError('cursor generation type missing')
    except ValueError as valerr:
        print('Error:', valerr)

    in_path = os.path.abspath(config_dir)

    try:
        configs = get_configs(config_dir)
        if (len(configs) <= 0):
            raise FileNotFoundError('no configs found in %s' % in_path)
    except FileNotFoundError as err:
        print(err)

    out = os.path.abspath(os.path.join(out_path, name))
    create_dir(out)

    # set output directory as `out_path`
    win_work_dir = x11_work_dir = out

    if (win == True and x11 == True):
        win_work_dir = os.path.join(out, 'win')
        x11_work_dir = os.path.join(out, 'x11')

    if (win == True):
        print('Building win cursors..')
        for config in configs:
            print(config_name)

    if (x11 == True):
        print('Building x11 cursors..')