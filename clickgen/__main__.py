#!/usr/bin/env python
# encoding: utf-8

import sys
import glob
import logging
import os
import shutil

from .linker import link_cursors
from .template import create_x11_template
from .win import main as win_gen
from .x11 import main as x11_gen

from .helpers import TemporaryDirectory, create_dir, get_logger

# config variables
config_ext = ('*.in', '*.ini')
# Note: 'zip' formate remove symbolic links,replace with normal files.That can affect the archive size.
archive_format = 'tar'


def get_configs(dir: str) -> list:
    """
        To get all config_files name with extension in Directory.
        'dir' is where config_files stored.
    """
    configs_grabbed = []

    for ext in config_ext:
        configs_grabbed.extend(
            glob.glob(os.path.abspath(os.path.join(dir, ext))))
    return configs_grabbed


def is_animated(config: str) -> bool:
    """
       check config_file have animation or not.
       'config' is name of .in or .ini config file.
       config_file contains following information for each size:

        <size> <xhot> <yhot> <path_to_png> <delay>
            ^      ^      ^         ^          ^
            |      |      |         |          |
        column1 column2 column3  column4    colums5
        
        <delay> is optional information, This function is designed only for read first line of config. 
    """

    try:
        with open(config, 'r') as config:
            line = config.readline()
            columns = line.split(" ")

            # animated cursor config have 5 columns,or more
            if (len(columns) > 4):
                return True
            else:
                return False
    except IOError as err:
        print('Error: ', err)


def get_cur_name(config: str, type: str) -> str:
    """
        Get the cursor's extension by providing `type` to this function.
        
        window extension => .cur , .ani
            watch.ani, left_ptr.cur

        x11 extension => `null`
            watch, left_ptr
    """
    config_name = os.path.basename(config)
    animated = is_animated(config)

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
         out_path: str = os.getcwd(),
         x11: bool = False,
         win: bool = False,
         archive: bool = False,
         logs: bool = False) -> None:
    """
        Generate 'Window' or 'X11' cursor package from configs.
        'name' is the Display Name of the cursor. That reflects a gnome-tweak-tool, KDE-settings,.. etc. In 'Window' is doesn't matter but it reflects an archive name.
        'config_dir' is where all config files stored, only .in or .ini config files supported.sample config_files => <https://github.com/ubuntu/yaru/tree/master/icons/src/cursors/bitmaps>
        'out_path' is where cursor archive or directory stored.absolute or relative path both eligible.
        'x11' & 'win' are platforms flags.Using these flag to output package platforms,like 'win' for "Window OS" and 'x11' for "FreeDesktop" that used in "Linux".Default both flags are "False".
        'archive' flag to compress cursor package to 'tar'.In python zip compression method symbolic links replace by normal file, that increase size of the output file.
        'logs' is for extra information
    """

    # logs disabled default
    logger = get_logger('clickgen')
    logging.disable(logging.CRITICAL)
    # enabling logs
    if (logs):
        logging.disable(logging.NOTSET)

    # If platforms  flags disabled
    try:
        if (x11 == False and win == False):
            raise ValueError('🚨 Cursor generate type missing')

    except ValueError as valerr:
        print('Error:', valerr)
        sys.exit(1)

    # passing configs path
    in_path = os.path.abspath(config_dir)

    try:
        configs = get_configs(config_dir)
        if (len(configs) <= 0):
            raise FileNotFoundError('🚨 No configs found in %s' % in_path)

    except FileNotFoundError as err:
        print(err)
        sys.exit(1)

    out = os.path.abspath(os.path.join(out_path, name))

    # set png prefix
    prefix = os.path.abspath(config_dir)

    # generate cursor based on flags
    if (win):
        print('👷 Building Windows cursors..')

        with TemporaryDirectory() as win_work_dir:

            for config in configs:
                cur_name = get_cur_name(config, type='win')
                cur_out = os.path.join(win_work_dir, cur_name)
                win_gen(input_config=config,
                        output_file=cur_out,
                        prefix=prefix)
                logger.info('Window: cursor generated to %s' % cur_out)

            link_cursors(win_work_dir, win=True)
            win_out = os.path.join(out, 'win')

            # deleting existed win directory
            if (os.path.exists(win_out)):
                shutil.rmtree(win_out)

            shutil.copytree(win_work_dir, win_out)

    if (x11):
        print('👷 Building X11 cursors..')

        with TemporaryDirectory() as x11_work_dir:
            x11_cursors_dir = os.path.join(x11_work_dir, 'cursors')
            create_dir(x11_cursors_dir)

            for config in configs:
                cur_name = get_cur_name(config, type='x11')

                cur_out = os.path.join(x11_cursors_dir, cur_name)
                x11_gen(input_config=config,
                        output_file=cur_out,
                        prefix=prefix)

                logger.info('X11: cursor generated to %s' % cur_out)

            link_cursors(x11_cursors_dir)
            create_x11_template(name=name, dir=x11_work_dir)
            x11_out = os.path.join(out, 'x11')

            # deleting existed x11 directory
            if (os.path.exists(x11_out)):
                shutil.rmtree(x11_out)

            shutil.copytree(x11_work_dir, x11_out, symlinks=True)

    if (archive):
        shutil.make_archive(out, archive_format, out)
        shutil.rmtree(out)