#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, NamedTuple

from clickgen.Type.image import Hotspot


class DBDocument(NamedTuple):
    name: str
    symlink: List[str]
    hotspot: Hotspot
