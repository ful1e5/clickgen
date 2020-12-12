#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
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
