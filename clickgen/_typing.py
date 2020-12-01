#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, List, NamedTuple, Tuple, Union


class Hotspot(NamedTuple):
    x: int
    y: int


IntegerTuple = Tuple[int, int]
Sizes = Union[IntegerTuple, List[IntegerTuple]]

WindowsCursorsConfig = Dict[str, Dict[str, str]]
