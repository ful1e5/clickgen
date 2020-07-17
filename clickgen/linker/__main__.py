#!/usr/bin/env python
# encoding: utf-8

from difflib import SequenceMatcher as SM
from pathlib import Path
import itertools
import json
import os

from ..helpers import cd, get_logger, symlink
from ..types import Path, StringList, Logger

# cursor data paths
basedir: Path = os.path.abspath(os.path.dirname(__file__))
data_file: Path = os.path.join(basedir, 'data.json')

# Logger
logger: Logger = get_logger('clickgen:linker')


def match_to_directory(name: str, directory: StringList) -> str:
    """
        Match `name` with `directory` with 0.5 ratio. That can fix `name` typo by searching inside directory.
        Example:
            z00m => zoom
    """

    compare_ratio = 0.5
    match = name

    for word in directory:
        ratio = SM(None, name.lower(), word.lower()).ratio()
        if ratio > compare_ratio:
            compare_ratio = ratio
            match = word

    logger.info('"%s" match to "%s" with "%s" ratio' %
                (name, match, compare_ratio))

    return match


def load_data() -> [StringList]:
    """
        Load ./data.json file and return processed two lists.i.e.:cursors, all_cursors
        `cursors` is `group` of similar cursors, Means one cursor from them satisfied all other cursors by generating the symbolic link.
        `all` is used as a `directory` where all cursors return as a list without any `group`.
    """
    with open(data_file) as f:
        data = json.loads(f.read())

    cursors = data['cursors']
    all = list(itertools.chain.from_iterable(cursors))

    return cursors, all


def link_cursors(directory: Path, win: bool = False) -> None:
    """
        Generate missing cursors have similar endpoint inside `directory`.
        `win` flag is `False` default, If it `True` this function only fix the name of cursors because `Windows` does not support symblinks.
    """
    directory = os.path.abspath(directory)
    isExists = os.path.exists(directory)

    # user have cursors fot symblink
    cursors = []

    try:
        if not isExists:
            raise FileNotFoundError('x11 directory not found')

        for file in os.listdir(directory):
            cursors.append(file)

        if (len(cursors) <= 0):
            raise FileNotFoundError('directory is empty')

    except FileNotFoundError as err:
        print('Error: ', err)

    known_cursors, all_cursors = load_data()

    # rename cursor with proper name
    for index, cursor in enumerate(cursors):
        cursor, extension = os.path.splitext(cursor)
        fix_cur = match_to_directory(cursor, all_cursors)

        if fix_cur not in all_cursors:
            msg = '%s is unknown cursor' % fix_cur
            logger.warning(msg)
            print(msg)

        elif (fix_cur != cursor):
            old_path = os.path.join(directory, cursor + extension)
            new_path = os.path.join(directory, fix_cur + extension)
            os.rename(old_path, new_path)

            cursors[index] = fix_cur

            msg = 'Fixed: %s ==> %s' % (cursor, fix_cur)
            logger.info(msg)
            print(msg)

    # symbolic links only for x11
    if not win:
        # cd for relative links
        with cd(directory):
            for cursor in cursors:
                for relative in known_cursors:
                    if cursor in relative:
                        # remove source cursor
                        relative.remove(cursor)

                        # links to other if not empty
                        if len(relative) != 0:
                            for link in relative:
                                src = './' + cursor
                                dst = './' + link
                                symlink(src, dst, overwrite=True)
                            print('Symbolic link: %s ==> ' % (cursor),
                                  *relative)
