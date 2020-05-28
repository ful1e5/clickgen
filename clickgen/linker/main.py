import os
import json
from difflib import SequenceMatcher as SM

basedir = os.path.abspath(os.path.dirname(__file__))
data_file = os.path.join(basedir, 'data.json')


def match_to_directory(name: str, directory: list) -> str:
    prev_ratio = 0
    match = ''

    for word in directory:
        ratio = SM(None, name.lower(), word.lower()).ratio()
        if ratio > prev_ratio:
            prev_ratio = ratio
            match = word

    return match


def load_data() -> [list]:
    with open(data_file) as f:
        data = json.loads(f.read())

    common = data['common']
    symblink = data['symblink']
    all = common

    for c in symblink:
        links = symblink[c]
        for l in links:
            all.append(l)

    return common, symblink, all


def create_linked_cursors(x11_dir: str) -> None:
    x11_dir = os.path.abspath(x11_dir)
    isExists = os.path.exists(x11_dir)

    cursors = []

    try:
        if isExists == False:
            raise FileNotFoundError('x11 directory not found')

        for file in os.listdir(x11_dir):
            cursors.append(file)

        if (len(cursors) <= 0):
            raise FileNotFoundError('directory is empty')

    except FileNotFoundError as err:
        print('Error: ', err)

    common_cursors, symblink_cursors, all_cursors = load_data()
    # rename cursor with proper name
    for index, cursor in enumerate(cursors):
        fix_cur = match_to_directory(cursor, all_cursors)
        if fix_cur not in all_cursors:
            print('Warning: %s undefined cursor' % fix_cur)
        elif (fix_cur != cursor):
            old_path = os.path.join(x11_dir, cursor)
            new_path = os.path.join(x11_dir, fix_cur)
            os.rename(old_path, new_path)

            cursors[index] = fix_cur

            print('Fixed: %s ==> %s' % (cursor, fix_cur))

    # # TODO:generate symblinks cursors
    # for cursor in cursors:
    #     print(cursor)


def symlink_rel(src: str, dst: str) -> None:
    rel_path_src = os.path.relpath(src, os.path.dirname(dst))
    os.symlink(rel_path_src, dst)
