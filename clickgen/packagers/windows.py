#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from string import Template
from typing import List

from ..configs import ThemeInfo
from .fixers.fixers import WinCursorsFixer

_inf_template = Template(
    """[Version]
signature="$CHICAGO$"
$comment
$url

[DefaultInstall]
CopyFiles = Scheme.Cur
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"

[Scheme.Reg]
HKCU,"Control Panel\\Cursors\\Schemes","%SCHEME_NAME%",,"%10%\\%CUR_DIR%\\%pointer%,%10%\\%CUR_DIR%\\%help%,%10%\\%CUR_DIR%\\%work%,%10%\\%CUR_DIR%\\%busy%,%10%\\%CUR_DIR%\\%Cross%,%10%\\%CUR_DIR%\\%Text%,%10%\\%CUR_DIR%\\%Hand%,%10%\\%CUR_DIR%\\%Unavailiable%,%10%\\%CUR_DIR%\\%Vert%,%10%\\%CUR_DIR%\\%Horz%,%10%\\%CUR_DIR%\\%Dgn1%,%10%\\%CUR_DIR%\\%Dgn2%,%10%\\%CUR_DIR%\\%move%,%10%\\%CUR_DIR%\\%alternate%,%10%\\%CUR_DIR%\\%link%"

; -- Installed files

[Scheme.Cur]
"Default.cur"
"Help.cur"
"Work.ani"
"Busy.ani"
"Cross.cur"       
"IBeam.cur"
"Handwriting.cur"
"Unavailiable.cur"
"Vertical.cur"
"Horizontal.cur"
"Diagonal_1.cur"
"Diagonal_2.cur"
"Move.cur"
"Alternate.cur"
"Link.cur"

CUR_DIR       = "Cursors\\$theme_name"
SCHEME_NAME   = "$theme_name"
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


class WindowsPackager:
    """ Create a crispy `Windows` cursor theme package. """

    def __init__(self, dir: str, info: ThemeInfo) -> None:
        self.__dir: str = dir
        self.__info: ThemeInfo = info

    def __install_file(self) -> str:
        content: str = _inf_template.safe_substitute(
            theme_name=self.__info.theme_name,
            comment=self.__info.comment,
            author=self.__info.author,
            url=self.__info.url,
        )

        return content

    def pack(self) -> None:
        """ Make Windows cursors directory installable. """
        print("Windows package...")

        # Remove unnecessary cursors
        cursors: List[str] = WinCursorsFixer(self.__dir).run()

        if len(cursors) == 0:
            raise FileNotFoundError(f"Windows cursor not found in {self.__dir}")

        # Store install.inf file
        content: str = self.__install_file()
        f = open(path.join(self.__dir, "install.inf"), "w")
        f.write(content)
        f.close()

        print(f"Total {len(cursors)} Windows cursors packed.")
        print("Windows package... Done")
