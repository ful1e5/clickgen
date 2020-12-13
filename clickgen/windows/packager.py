#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from string import Template
from typing import List

from ..configs import ThemeInfo

_inf_template = Template(
    """[Version]
signature="$CHICAGO$"
$comment
$url

[DefaultInstall]
CopyFiles = Scheme.Cur, Scheme.Txt
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"

[Scheme.Reg]
HKCU,"Control Panel\Cursors\Schemes","%SCHEME_NAME%",,"%10%\%CUR_DIR%\%pointer%,%10%\%CUR_DIR%\%help%,%10%\%CUR_DIR%\%work%,%10%\%CUR_DIR%\%busy%,%10%\%CUR_DIR%\%cross%,%10%\%CUR_DIR%\%Text%,%10%\%CUR_DIR%\%Hand%,%10%\%CUR_DIR%\%unavailiable%,%10%\%CUR_DIR%\%Vert%,%10%\%CUR_DIR%\%Horz%,%10%\%CUR_DIR%\%Dgn1%,%10%\%CUR_DIR%\%Dgn2%,%10%\%CUR_DIR%\%move%,%10%\%CUR_DIR%\%alternate%,%10%\%CUR_DIR%\%link%"

; -- Installed files

[Scheme.Cur]
Work.ani
Busy.ani
Default.cur
Help.cur
Link.cur
Move.cur
Diagonal_2.cur
install.inf
Vertical.cur
Horizontal.cur
Diagonal_1.cur
Handwriting.cur
Cross.cur       
IBeam.cur
Unavailiable.cur
Alternate.cur

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

    def __init__(self, dir: Path, info: ThemeInfo) -> None:
        self.dir = dir
        self.info: ThemeInfo = info

        cursors: List[str] = []
        for ext in ("*.ani", "*.cur"):
            cursors.append(self.dir.glob(ext))

        if not cursors:
            raise FileNotFoundError(f"Windows cursors not found in {self.dir}")

    def save(self) -> None:
        """ Make Windows cursors directory installable. """
        data: str = _inf_template.safe_substitute(
            theme_name=self.info.theme_name,
            comment=self.info.comment,
            author=self.info.author,
            url=self.info.url,
        )

        # Store install.inf file
        install_inf: Path = self.dir / "install.inf"
        install_inf.write_text(data)
