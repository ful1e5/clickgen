#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import Tuple, TypeVar

_T = TypeVar("_T")
_P = TypeVar("_P", str, Path, PathLike)
_Size = Tuple[int, int]
