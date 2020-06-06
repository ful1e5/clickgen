#!/usr/bin/env python
# encoding: utf-8

import os

from ..helpers import create_dir, get_logger

basedir = os.path.abspath(os.path.dirname(__file__))
cursor_file_path = os.path.join(basedir, 'cursor.theme')
index_file_path = os.path.join(basedir, 'index.theme')


def create_x11_template(dir: str, name: str, comment: str = '') -> None:
    """
        Copy metadata files to the cursor package directory.
        'dir' is a path to the cursor package directory.
        'name' & 'comment' is Metadata for cursor package.
    """
    logger = get_logger('clickgen:template')
    abs_dir = os.path.abspath(dir)
    cursor_file_out_path = os.path.join(abs_dir, 'cursor.theme')
    index_file_out_path = os.path.join(abs_dir, 'index.theme')

    # helper
    create_dir(dir)

    with open(cursor_file_path, 'r') as cursor_file:
        with open(cursor_file_out_path, 'w') as cursor_file_out:
            lines = cursor_file.readlines()

            for line in lines:
                cursor_file_out.write(line.replace('<Name>', name))

            logger.info('cursor.theme file generated for %s at %s' %
                        (name, cursor_file_out_path))

    with open(index_file_path, 'r') as index_file:
        with open(index_file_out_path, 'w') as index_file_out:
            lines = index_file.readlines()

            for line in lines:
                temp_line = line.replace('<Name>', name)

                if (comment != ''):
                    temp_line = temp_line.replace('<Comment>', comment)
                else:
                    temp_line = temp_line.replace('<Comment>',
                                                  '%s cursor theme' % name)

                index_file_out.write(temp_line)

            logger.info('index.theme file generated for %s at %s' %
                        (name, index_file_out_path))