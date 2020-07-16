#!/usr/bin/env python
# encoding: utf-8

import pathlib
from logging import Logger
from typing import List, Union, Tuple

Path = Union[str, pathlib.Path]

StringList = List[str]

IntegerList = List[int]

IntegerTuple = Tuple[int, int]
CoordinateTuple = Union[Tuple[int, int], None]
