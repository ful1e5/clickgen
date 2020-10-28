#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import path
from string import Template

from ..configs.core import CursorInfo
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
"Arrow.cur"
"Help.cur"
"AppStarting.ani"
"Wait.ani"
"Cross.cur"       
"IBeam.cur"
"Handwriting.cur"
"NO.cur"
"SizeNS.cur"
"SizeWE.cur"
"SizeNWSE.cur"
"SizeNESW.cur"
"SizeAll.cur"
"UpArrow.cur"
"Hand.cur"

[Strings]
CUR_DIR       = "Cursors\\$theme_name"
SCHEME_NAME   = "$theme_name"
pointer       = "Arrow.cur"
help		  = "Help.cur"
work		  = "AppStarting.ani"
busy		  = "Wait.ani"
cross		  = "Cross.cur"
text		  = "IBeam.cur"
hand		  = "Handwriting.cur"
unavailiable  = "NO.cur"
vert		  = "SizeNS.cur"   
horz		  = "SizeWE.cur"
dgn1		  = "SizeNWSE.cur"
dgn2		  = "SizeNESW.cur"
move		  = "SizeAll.cur"
alternate	  = "UpArrow.cur"
link		  = "Hand.cur"
"""
)


class WindowsPackager:
    """ Create a crispy `Windows` cursor theme package. """

    def __init__(self, dir: str, info: CursorInfo) -> None:
        self.__dir: str = dir
        self.__info: CursorInfo = info

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
        WinCursorsFixer(self.__dir).run()

        # Store install.inf file
        content: str = self.__install_file()
        f = open(path.join(self.__dir, "install.inf", "w"))
        f.write(content)
        f.close()

        print("Windows package... Done")
