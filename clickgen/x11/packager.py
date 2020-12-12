#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from string import Template
from typing import Dict

from ..configs import ThemeInfo


class XPackager:
    """ Create a crispy `XCursors` theme package. """

    templates: Dict[str, Template] = {
        "cursor.theme": Template('[Icon Theme]\nName=$theme_name\nInherits="hicolor"'),
        "index.theme": Template(
            '[Icon Theme]\nName=$theme_name\nComment=$comment\nInherits="hicolor"'
        ),
    }

    def __init__(self, dir: Path, info: ThemeInfo) -> None:
        self.dir: Path = dir
        self.package_info: ThemeInfo = info

    def index_files(self) -> Dict[str, str]:
        """ XCursors theme files. """
        files: Dict[str, str] = {}
        for key in self.templates:
            files[key] = self.templates[key].safe_substitute(
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
