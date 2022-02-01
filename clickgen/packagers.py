#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate Cursors without hassle.

.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

from pathlib import Path
from string import Template
from typing import Dict, List, Optional, Set

# --- X11

THEME_FILES_TEMPLATES: Dict[str, Template] = {
    "cursor.theme": Template('[Icon Theme]\nName=$theme_name\nInherits="$theme_name"'),
    "index.theme": Template(
        '[Icon Theme]\nName=$theme_name\nComment=$comment\nInherits="hicolor"'
    ),
}


def XPackager(directory: Path, theme_name: str, comment: str) -> None:
    """This packager generates ``cursor.theme`` & ``index.theme`` files at \
        ``directory``.

    :param directory: Path where ``.theme`` files save.
    :param directory: ``pathlib.Path``

    :param theme_name: Cursor theme name.
    :param theme_name: ``str``

    :param comment: Extra information about this cursor theme.
    :param comment: ``str``

    :returns: None.
    :rtype: ``None``
    """

    # Writing all .theme files
    files: Dict[str, str] = {}
    for file, template in THEME_FILES_TEMPLATES.items():
        files[file] = template.safe_substitute(theme_name=theme_name, comment=comment)

    for f, data in files.items():
        fp: Path = directory / f
        fp.write_text(data)


# --- Windows

INSTALL_INF = Template(
    """[Version]
signature="$CHICAGO$"
$comment

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
CUR_DIR           = "Cursors\\$theme_name Cursors"
SCHEME_NAME       = "$theme_name Cursors"
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
)

REQUIRED_WIN_CURSORS: Set[str] = {
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

UNINSTALL_BAT = Template(
    """@echo off
:: ===========================================================
::
:: Replace the name of cursor according to the cursor schemes.
:: Credit: https://github.com/smit-sms
:: More Information: https://github.com/ful1e5/apple_cursor/issues/79
::
:: ===========================================================

REG DELETE "HKCU\\Control Panel\\Cursors\\Schemes" /v "$theme_name Cursors" /f

:: ===============================================================================
:: This enables a popup message box to indicate a user for the operation complete.
:: ===============================================================================
echo x=msgbox("Successfully deleted the cursor!", 0+64, "Cursor") > %tmp%\tmp.vbs
wscript %tmp%\tmp.vbs
del %tmp%\tmp.vbs
"""
)


def WindowsPackager(
    directory: Path,
    theme_name: str,
    comment: str,
    author: str,
    website_url: Optional[str] = None,
) -> None:
    """This packager generates ``install.inf`` files at ``directory``. Also, \
    Cursor extensions is identified by its type (.cur/.ani).

    :param directory: Path where ``.theme`` files save.
    :param directory: ``pathlib.Path``

    :param theme_name: Cursor theme name.
    :param theme_name: ``str``

    :param comment: Extra information about this cursor theme.
    :param comment: ``str``

    :param author: Author name.
    :param author: ``str``

    :param website_url: Website web address.(Useful for **bug reports**)
    :param author: ``str`` or ``None``

    :returns: None.
    :rtype: ``None``

    :raise FileNotFoundError: If Windows cursors are not exists on \
            provided directory.
    """

    files: List[Path] = []

    for extensions in ("*.ani", "*.cur"):
        for i in sorted(directory.glob(extensions)):
            if i.stem in REQUIRED_WIN_CURSORS:
                files.append(i)

    cursors: Set[Path] = set(files)

    # Checking cursor files
    if not cursors:
        raise FileNotFoundError(
            f"Windows cursors '*.cur' or '*.ani' not found in '{directory}'"
        )

    if len(cursors) < len(REQUIRED_WIN_CURSORS):
        # Some cursors are missing
        c = set(map(lambda x: x.stem, cursors))
        missing = sorted(REQUIRED_WIN_CURSORS - set(c))
        raise FileNotFoundError(f"Windows cursors are missing {missing}")

    if website_url:
        comment = f"{comment}\n{website_url}"

    # Real magic of python
    # replace $Default => Default.ani | Default.cur (as file was provided)
    cursor_data: Dict[str, str] = {}
    for cur in cursors:
        cursor_data[cur.stem] = cur.name

    # Store install.inf file
    data: str = INSTALL_INF.safe_substitute(
        theme_name=theme_name, comment=comment, author=author, **cursor_data
    )
    install_inf: Path = directory / "install.inf"
    install_inf.write_text(data)

    # Store uninstall.bat file
    uninstall_bat: Path = directory / "uninstall.bat"
    uninstall_bat.write_text(UNINSTALL_BAT.safe_substitute(theme_name=theme_name))
