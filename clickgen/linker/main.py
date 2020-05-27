import os
import json
from difflib import SequenceMatcher as SM

basedir = os.path.abspath(os.path.dirname(__file__))
common_json_file = os.path.join(basedir, 'common.json')


def match_to_directory(name: str, directory: list) -> str:
    prev_ratio = 0
    match = ''
    for word in directory:
        ratio = SM(None, name.lower(), word.lower()).ratio()
        if ratio > prev_ratio:
            prev_ratio = ratio
            match = word

    return match


def create_linked_cursors(configs: list) -> None:
    with open(common_json_file) as f:
        common_cursors = json.loads(f.read())

    temp = []
    for config in configs:
        in_cur = os.path.basename(config).split('.')[0]
        temp.append(match_to_directory(in_cur, common_cursors))


def symlink_rel(src: str, dst: str) -> None:
    rel_path_src = os.path.relpath(src, os.path.dirname(dst))
    os.symlink(rel_path_src, dst)
