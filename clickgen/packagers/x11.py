#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from string import Template
from typing import Dict

from ..configs import ThemeInfo
from .fixers.fixers import XCursorLinker

templates: Dict[str, Template] = {
    "cursor.theme": Template("[Icon Theme]\nInherits=$theme_name"),
    "index.theme": Template("[Icon Theme]\nName=$theme_name\nComment=$comment"),
}


class X11Packager:
    """ Create a crispy `XCursors` theme package. """

    def __init__(self, dir: str, info: ThemeInfo) -> None:
        self.__dir: str = dir
        self.__info: ThemeInfo = info

    def __index_files(self) -> Dict[str, str]:
        """ XCursors theme files. """
        files: Dict[str, str] = {}
        for key in templates:
            files[key] = templates[key].safe_substitute(
                theme_name=self.__info.theme_name, comment=self.__info.comment
            )

        return files

    def pack(self):
        """ Make XCursor theme. """
        print("XCursors package...")

        # Link & Rename XCursors according to db.py
        XCursorLinker(path.join(self.__dir, "cursors")).run()

        # Write .theme files
        files: Dict[str, str] = self.__index_files()

        for f in files:
            theme_file = open(path.join(self.__dir, f), "w")
            theme_file.write(files[f])
            theme_file.close()

        print("XCursors package... Done")
