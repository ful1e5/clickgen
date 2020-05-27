import os
import json
from difflib import SequenceMatcher as SM


def create_symblic(configs: list) -> None:
    with open('common.json') as f:
        common_cursors = json.load(f)


def symlink_rel(src: str, dst: str) -> None:
    rel_path_src = os.path.relpath(src, os.path.dirname(dst))
    os.symlink(rel_path_src, dst)
