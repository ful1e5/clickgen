from contextlib import contextmanager
import glob
import os
import shutil
import tempfile

from .linker import create_linked_cursors
from .win import main as win_gen
from .x11 import main as x11_gen

config_ext = ('*.in', '*.ini')


@contextmanager
def TemporaryDirectory():
    name = tempfile.mkdtemp()
    try:
        yield name
    finally:
        shutil.rmtree(name)


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


def _is_animated(config: str) -> bool:
    try:
        with open(config, 'r') as config:
            line = config.readline()
            columns = line.split(" ")
            if (len(columns) > 4):
                return True
            else:
                return False
    except IOError as err:
        print('Error: ', err)


def get_cur_name(config: str, type: str) -> str:
    config_name = os.path.basename(config)
    animated = _is_animated(config)
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
        if (x11 and win):
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

    # set png prefix
    prefix = os.path.abspath(config_dir)

    if (win):
        print('Building win cursors..')
        with TemporaryDirectory() as win_work_dir:
            for config in configs:
                cur_name = get_cur_name(config, type='win')
                cur_out = os.path.join(win_work_dir, cur_name)
                win_gen(input_config=config,
                        output_file=cur_out,
                        prefix=prefix)

    if (x11):
        print('Building x11 cursors..')
        with TemporaryDirectory() as x11_work_dir:
            for config in configs:
                cur_name = get_cur_name(config, type='x11')
                cur_out = os.path.join(x11_work_dir, cur_name)
                x11_gen(input_config=config,
                        output_file=cur_out,
                        prefix=prefix)

            create_linked_cursors(x11_work_dir)
