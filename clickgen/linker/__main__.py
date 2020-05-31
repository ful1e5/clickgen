from difflib import SequenceMatcher as SM
import itertools
import json
import os

from ..helpers import cd, symlink

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'data.json')


def match_to_directory(name: str, directory: list) -> str:
    compare_ratio = 0.5
    match = name

    for word in directory:
        ratio = SM(None, name.lower(), word.lower()).ratio()
        if ratio > compare_ratio:
            compare_ratio = ratio
            match = word

    return match


def load_data() -> [list]:
    with open(data_file) as f:
        data = json.loads(f.read())

    cursors = data['cursors']
    all = list(itertools.chain.from_iterable(cursors))

    return cursors, all


def link_cursors(dir: str, win=False) -> None:
    dir = os.path.abspath(dir)
    isExists = os.path.exists(dir)

    # user have cursors fot symblink
    cursors = []

    try:
        if not isExists:
            raise FileNotFoundError('x11 directory not found')

        for file in os.listdir(dir):
            cursors.append(file)

        if (len(cursors) <= 0):
            raise FileNotFoundError('directory is empty')

    except FileNotFoundError as err:
        print('Error: ', err)

    known_cursors, all_cursors = load_data()

    # rename cursor with proper name
    for index, cursor in enumerate(cursors):
        fix_cur = match_to_directory(cursor, all_cursors)

        if fix_cur not in all_cursors:
            print('Warning: %s is unknown cursor' % fix_cur)

        elif (fix_cur != cursor):
            old_path = os.path.join(dir, cursor)
            new_path = os.path.join(dir, fix_cur)
            os.rename(old_path, new_path)

            cursors[index] = fix_cur

            print('Fixed: %s ==> %s' % (cursor, fix_cur))

    # For relative links
    if not win:
        with cd(dir):
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
                            print('symblink: %s ==> ' % (cursor), *relative)
