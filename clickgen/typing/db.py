#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, NamedTuple

from clickgen.typing.image import Hotspot


class DBDocument(NamedTuple):
    name: str
    symlink: List[str]
    hotspot: Hotspot
