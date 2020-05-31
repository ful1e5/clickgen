import glob
import os
import shutil

from .linker import link_cursors
from .template import create_x11_template
from .win import main as win_gen
from .x11 import main as x11_gen

from .helpers import create_dir, TemporaryDirectory

config_ext = ('*.in', '*.ini')


def get_configs(dir: str) -> list:
    configs_grabbed = []

    for ext in config_ext:
        configs_grabbed.extend(
            glob.glob(os.path.abspath(os.path.join(dir, ext))))
    return configs_grabbed


def is_animated(config: str) -> bool:
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
    animated = is_animated(config)
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


def main(name: str,
         config_dir: str,
         out_path: str = os.curdir,
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

            link_cursors(win_work_dir, win=True)
            win_out = os.path.join(out, 'win')

            # deleting existed win directory
            if (os.path.exists(win_out)):
                shutil.rmtree(win_out)

            shutil.copytree(win_work_dir, win_out)

    if (x11):
        print('Building x11 cursors..')

        with TemporaryDirectory() as x11_work_dir:
            x11_cursors_dir = os.path.join(x11_work_dir, 'cursors')
            create_dir(x11_cursors_dir)
            for config in configs:
                cur_name = get_cur_name(config, type='x11')

                cur_out = os.path.join(x11_cursors_dir, cur_name)
                x11_gen(input_config=config,
                        output_file=cur_out,
                        prefix=prefix)

            link_cursors(x11_cursors_dir)
            create_x11_template(name=name, dir=x11_work_dir)
            x11_out = os.path.join(out, 'x11')

            # deleting existed x11 directory
            if (os.path.exists(x11_out)):
                shutil.rmtree(x11_out)

            shutil.copytree(x11_work_dir, x11_out, symlinks=True)

    if (archive):
        # 'tar' archive store symbolic link ,'zip' transfer to normal files
        shutil.make_archive(out, 'tar', out)
        shutil.rmtree(out)