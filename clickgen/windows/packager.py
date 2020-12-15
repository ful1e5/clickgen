#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path, PosixPath
from string import Template
from typing import List

from ..configs import ThemeInfo

_inf_template = Template(
    """[Version]
signature="$CHICAGO$"
$comment

[DefaultInstall]
CopyFiles = Scheme.Cur
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"

[Scheme.Reg]
HKCU,"Control Panel\Cursors\Schemes","%SCHEME_NAME%",,"%10%\%CUR_DIR%\%pointer%,%10%\%CUR_DIR%\%help%,%10%\%CUR_DIR%\%work%,%10%\%CUR_DIR%\%busy%,%10%\%CUR_DIR%\%Cross%,%10%\%CUR_DIR%\%Text%,%10%\%CUR_DIR%\%Hand%,%10%\%CUR_DIR%\%Unavailiable%,%10%\%CUR_DIR%\%Vert%,%10%\%CUR_DIR%\%Horz%,%10%\%CUR_DIR%\%Dgn1%,%10%\%CUR_DIR%\%Dgn2%,%10%\%CUR_DIR%\%move%,%10%\%CUR_DIR%\%alternate%,%10%\%CUR_DIR%\%link%"

; -- Installed files

[Scheme.Cur]
"Work.ani"
"Busy.ani"
"Default.cur"
"Help.cur"
"Link.cur"
"Move.cur"
"Diagonal_2.cur"
"Vertical.cur"
"Horizontal.cur"
"Diagonal_1.cur"
"Handwriting.cur"
"Cross.cur"       
"IBeam.cur"
"Unavailiable.cur"
"Alternate.cur"

[Strings]
CUR_DIR       = "Cursors\\$theme_name Cursors"
SCHEME_NAME   = "$theme_name Cursors"
pointer       = "Default.cur"
help		  = "Help.cur"
work		  = "Work.ani"
busy		  = "Busy.ani"
cross		  = "Cross.cur"
text		  = "IBeam.cur"
hand		  = "Handwriting.cur"
unavailiable  = "Unavailiable.cur"
vert		  = "Vertical.cur"   
horz		  = "Horizontal.cur"
dgn1		  = "Diagonal_1.cur"
dgn2		  = "Diagonal_2.cur"
move		  = "Move.cur"
alternate	  = "Alternate.cur"
link		  = "Link.cur"
"""
)


class WinPackager:
    """ Create a crispy `Windows` cursor theme package. """

    dir: Path = Path()
    info: ThemeInfo = ThemeInfo(theme_name="Unknown", author="clickgen")
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

        data: str = _inf_template.safe_substitute(
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
