#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict

from clickgen.typing.core import ThemeInfo
from clickgen.templates import THEME_FILES_TEMPLATES


class XPackager:
    """ Create a crispy `XCursors` theme package. """

    def __init__(self, dir: Path, info: ThemeInfo) -> None:
        self.dir: Path = dir
        self.package_info: ThemeInfo = info

    def theme_files(self) -> Dict[str, str]:
        """ XCursors theme files. """
        files: Dict[str, str] = {}
        for file, template in THEME_FILES_TEMPLATES.items():
            files[file] = template.safe_substitute(
                theme_name=self.package_info.theme_name,
                comment=self.package_info.comment,
            )

        return files

    def save(self):
        """ Make XCursor theme. """
        # Write .theme files
        files: Dict[str, str] = self.theme_files()

        for f, data in files.items():
            fp: Path = self.dir / f
            fp.write_text(data)
