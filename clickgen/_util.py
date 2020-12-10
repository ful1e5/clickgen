#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from typing import Union


def remove_directory(directory: Union[str, Path]) -> None:
    """ Utility for removing directory if directory is existed in filesystem. """
    if isinstance(directory, str):
        d: Path = Path(directory)
    else:
        d: Path = directory

    if d.exists():
        shutil.rmtree(d)
