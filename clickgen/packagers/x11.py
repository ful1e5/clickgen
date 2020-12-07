#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from string import Template
from typing import Dict

from ..configs import ThemeInfo

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
