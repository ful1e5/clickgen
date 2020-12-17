#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil
import sys
from contextlib import contextmanager
from difflib import SequenceMatcher as SM
from pathlib import Path
from typing import List, Optional, Union


def remove(p: Union[str, Path]) -> None:
    """ Utility for removing file, directory or symlink, If it's existed in filesystem. """

    if isinstance(p, str):
        p: Path = Path(p)

    if p.exists():
        if p.is_dir():
            shutil.rmtree(p)
        else:
            p.unlink()
    else:
        pass


@contextmanager
def goto_cursors_dir(dir: Path):
    """ Temporary change directory to `cursors` using contextmanager. """

    CWD = os.getcwd()
    os.chdir(dir.absolute())
    try:
        yield
    except:
        raise Exception(f" Exception caught: {sys.exc_info()[0]}")
    finally:
        os.chdir(CWD)


def match_string(s: str, l: List[str]) -> Optional[str]:
    compare_ratio: float = 0.5
    result: str = s

    for e in l:
        ratio: float = SM(None, s.lower(), e.lower()).ratio()
        if ratio > compare_ratio:
            compare_ratio = ratio
            result = e
        else:
            continue

    if s != result:
        return result
    else:
        return None
