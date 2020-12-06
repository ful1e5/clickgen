#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from pathlib import Path
from string import Template
from typing import Dict, List

from ..configs import ThemeInfo
from .fixers.fixers import XCursorLinker

templates: Dict[str, Template] = {
    "cursor.theme": Template("[Icon Theme]\nInherits=$theme_name"),
    "index.theme": Template("[Icon Theme]\nName=$theme_name\nComment=$comment"),
}


class XPackager:
    """ Create a crispy `XCursors` theme package. """

    dir: Path = Path()
    package_info: ThemeInfo

    def __init__(self, dir: Path, info: ThemeInfo) -> None:
        self.dir: Path = dir
        self.package_info: ThemeInfo = info

    def index_files(self) -> Dict[str, str]:
        """ XCursors theme files. """
        files: Dict[str, str] = {}
        for key in templates:
            files[key] = templates[key].safe_substitute(
                theme_name=self.package_info.theme_name,
                comment=self.package_info.comment,
            )

        return files

    def save(self):
        """ Make XCursor theme. """
        # Write .theme files
        files: Dict[str, str] = self.index_files()

        for f, data in files.items():
            fp: Path = self.dir / f
            fp.write_text(data)


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
        print("Linking XCursors...")

        # Link & Rename XCursors according to db.py
        cursors: List[str] = XCursorLinker(path.join(self.__dir, "cursors")).run()

        # Write .theme files
        files: Dict[str, str] = self.__index_files()

        for f in files:
            theme_file = open(path.join(self.__dir, f), "w")
            theme_file.write(files[f])
            theme_file.close()

        print(f"Total XCursors = {len(cursors)}")
        print("Linking XCursors... Done")
