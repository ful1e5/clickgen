#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import sys
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Union


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
