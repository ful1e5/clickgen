#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from string import Template
from typing import Dict, List, Optional, Set

FILE_TEMPLATES: Dict[str, Template] = {
    "install.inf": Template(
        """[Version]
signature="$CHICAGO$"
$info

[DefaultInstall]
CopyFiles = Scheme.Cur, Scheme.Txt
AddReg    = Scheme.Reg

[DestinationDirs]
Scheme.Cur = 10,"%CUR_DIR%"
Scheme.Txt = 10,"%CUR_DIR%"

[Scheme.Reg]
HKCU,"Control Panel\\Cursors\\Schemes","%SCHEME_NAME%",,"%10%\\%CUR_DIR%\\%pointer%,%10%\\%CUR_DIR%\\%help%,%10%\\%CUR_DIR%\\%work%,%10%\\%CUR_DIR%\\%busy%,%10%\\%CUR_DIR%\\%Cross%,%10%\\%CUR_DIR%\\%Text%,%10%\\%CUR_DIR%\\%Hand%,%10%\\%CUR_DIR%\\%Unavailiable%,%10%\\%CUR_DIR%\\%Vert%,%10%\\%CUR_DIR%\\%Horz%,%10%\\%CUR_DIR%\\%Dgn1%,%10%\\%CUR_DIR%\\%Dgn2%,%10%\\%CUR_DIR%\\%move%,%10%\\%CUR_DIR%\\%alternate%,%10%\\%CUR_DIR%\\%link%"

; -- Installed files

[Scheme.Cur]
"$Work"
"$Busy"
"$Default"
"$Help"
"$Link"
"$Move"
"$Diagonal_2"
"$Vertical"
"$Horizontal"
"$Diagonal_1"
"$Handwriting"
"$Cross"
"$IBeam"
"$Unavailiable"
"$Alternate"

[Strings]
CUR_DIR           = "Cursors\\$theme_name"
SCHEME_NAME       = "$theme_name"
pointer           = "$Default"
help              = "$Help"
work              = "$Work"
busy              = "$Busy"
cross             = "$Cross"
text              = "$IBeam"
hand              = "$Handwriting"
unavailiable      = "$Unavailiable"
vert              = "$Vertical"
horz              = "$Horizontal"
dgn1              = "$Diagonal_1"
dgn2              = "$Diagonal_2"
move              = "$Move"
alternate         = "$Alternate"
link              = "$Link"
"""
    ),
    "uninstall.bat": Template(
        """@echo off
:: ===========================================================
::
:: Replace the name of cursor according to the cursor schemes.
:: Credit: https://github.com/smit-sms
:: More Information: https://github.com/ful1e5/apple_cursor/issues/79
::
:: ===========================================================

REG DELETE "HKCU\\Control Panel\\Cursors\\Schemes" /v "$theme_name" /f

:: ===============================================================================
:: This enables a popup message box to indicate a user for the operation complete.
:: ===============================================================================
echo x=msgbox("Successfully deleted the cursor!", 0+64, "Cursor") > %tmp%\tmp.vbs
wscript %tmp%\tmp.vbs
del %tmp%\tmp.vbs
"""
    ),
}

REQUIRED_CURSORS: Set[str] = {
    "Work",
    "Busy",
    "Default",
    "Help",
    "Link",
    "Move",
    "Diagonal_2",
    "Vertical",
    "Horizontal",
    "Diagonal_1",
    "Handwriting",
    "Cross",
    "IBeam",
    "Unavailiable",
    "Alternate",
}


def pack_win(
    dir: Path,
    theme_name: str,
    comment: str,
    website: Optional[str] = None,
) -> None:
    """This packager generates ``install.inf`` files at ``directory``. Also, \
    Cursor extensions is identified by its type (.cur/.ani).

    :param dir: Path where ``.theme`` files save.
    :param dir: ``pathlib.Path``

    :param theme_name: Name of theme.
    :param theme_name: ``str``

    :param comment: Extra information about theme.
    :param comment: ``str``

    :param website: Website web address.(Useful for **bug reports**)
    :param website: ``str`` or ``None``

    :returns: None.
    :rtype: ``None``

    :raise FileNotFoundError: If Windows cursors are not exists on \
            provided directory.
    """

    files: List[Path] = []

    for ext in ("*.ani", "*.cur"):
        for i in sorted(dir.glob(ext)):
            if i.stem in REQUIRED_CURSORS:
                files.append(i)

    cursors = set(files)

    if len(cursors) < len(REQUIRED_CURSORS):
        # Some cursors are missing
        c = set(map(lambda x: x.stem, cursors))
        missing = sorted(REQUIRED_CURSORS - set(c))
        raise FileNotFoundError(f"Windows cursors are missing {missing}")

    info: str = ""
    if website:
        info = f"{comment}\n{website}"

    # replace $Default => Default.ani | Default.cur
    cursor_data: Dict[str, str] = {}
    for cur in cursors:
        cursor_data[cur.stem] = cur.name

    for fname, template in FILE_TEMPLATES.items():
        data: str = template.safe_substitute(
            theme_name=f"{theme_name} Cursors",
            info=info,
            **cursor_data,
        )
        f = dir / fname
        f.write_text(data)
