#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..configs.core import CursorInfo
from .fixers.fixers import XCursorLinker


class X11Packager:
    """ Create a crispy `XCursors` theme package. """

    def __init__(self, dir: str, info: CursorInfo) -> None:
        self.__dir: str = dir
        self.__info: CursorInfo = info