#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path, PosixPath
from typing import List

from clickgen.templates import INSTALL_INF
from clickgen.typing.core import ThemeInfo


class WinPackager:
    """ Create a crispy `Windows` cursor theme package. """

    dir: Path = Path()
    info: ThemeInfo = ThemeInfo(theme_name="click!", author="clickgen")
    cursors: List[PosixPath] = []

    def __init__(self, dir: Path, info: ThemeInfo, cursors: List[str]) -> None:
        self.dir = dir
        self.info: ThemeInfo = info

        for ext in ("*.ani", "*.cur"):
            for i in sorted(self.dir.glob(ext)):
                self.cursors.append(i)

        if not self.cursors:
            raise FileNotFoundError(f"Windows cursors not found in {self.dir}")
        else:
            for c in self.cursors:
                if not c.stem in cursors:
                    raise FileNotFoundError(f"'{c.name}' not found")

    def save(self) -> None:
        """ Make Windows cursors directory installable. """
        comment = self.info.comment

        if self.info.url:
            comment: str = f"{comment}\n{self.info.url}"

        data: str = INSTALL_INF.safe_substitute(
            theme_name=self.info.theme_name,
            comment=comment,
            author=self.info.author,
        )

        # Change cursors extension (.cur||.ani) according to cursor files provided.
        for p in self.cursors:
            if p.name in data:
                continue
            else:
                old_ext: List[str] = [".ani", ".cur"]
                old_ext.remove(p.suffix)
                data = data.replace(f"{p.stem}{old_ext[0]}", p.name)

        # Store install.inf file
        install_inf: Path = self.dir / "install.inf"
        install_inf.write_text(data)
