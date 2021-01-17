#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from string import Template
from typing import Dict, Iterator, List, Optional, Set


# --- X11

THEME_FILES_TEMPLATES: Dict[str, Template] = {
    "cursor.theme": Template('[Icon Theme]\nName=$theme_name\nInherits="hicolor"'),
    "index.theme": Template(
        '[Icon Theme]\nName=$theme_name\nComment=$comment\nInherits="hicolor"'
    ),
}


def XPackager(directory: Path, theme_name: str, comment: str) -> None:
    """ Create a crispy `XCursors` theme package. """

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
CUR_DIR       = "Cursors\\$theme_name Cursors"
SCHEME_NAME   = "$theme_name Cursors"
pointer       = "$Default"
help		  = "$Help"
work		  = "$Work"
busy		  = "$Busy"
cross		  = "$Cross"
text		  = "$IBeam"
hand		  = "$Handwriting"
unavailiable  = "$Unavailiable"
vert		  = "$Vertical"   
horz		  = "$Horizontal"
dgn1		  = "$Diagonal_1"
dgn2		  = "$Diagonal_2"
move		  = "$Move"
alternate	  = "$Alternate"
link		  = "$Link"
"""
)

REQUIRED_WIN_CURSORS: Iterator[str] = {
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


def WindowsPackager(
    directory: Path,
    theme_name: str,
    comment: str,
    author: str,
    website_url: Optional[str] = None,
) -> None:
    """ Create a crispy `Windows` cursor theme package. """

    files: Iterator[Path] = []

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
        comment: str = f"{comment}\n{website_url}"

    # Real magic of python
    # replace $Default => Default.ani | Default.cur (as file was provided)
    cursor_data: Dict[str, str] = {}
    for cur in cursors:
        cursor_data[cur.stem] = cur.name

    data: str = INSTALL_INF.safe_substitute(
        theme_name=theme_name, comment=comment, author=author, **cursor_data
    )

    # Store install.inf file
    install_inf: Path = directory / "install.inf"
    install_inf.write_text(data)