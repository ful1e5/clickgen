#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path, PosixPath
from string import Template
from typing import Dict, Iterator, List, Optional


# --- X11

THEME_FILES_TEMPLATES: Dict[str, Template] = {
    "cursor.theme": Template('[Icon Theme]\nName=$theme_name\nInherits="hicolor"'),
    "index.theme": Template(
        '[Icon Theme]\nName=$theme_name\nComment=$comment\nInherits="hicolor"'
    ),
}


def XPackager(dir: Path, theme_name: str, comment: str) -> None:
    """ Create a crispy `XCursors` theme package. """

    # Writing all .theme files
    files: Dict[str, str] = {}
    for file, template in THEME_FILES_TEMPLATES.items():
        files[file] = template.safe_substitute(theme_name=theme_name, comment=comment)

    for f, data in files.items():
        fp: Path = dir / f
        fp.write_text(data)


# --- Windows

INSTALL_INF = Template(
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

REQUIRED_WIN_CURSORS: Iterator[str] = [
    "Work"
    "Busy"
    "Default"
    "Help"
    "Link"
    "Move"
    "Diagonal_2"
    "Vertical"
    "Horizontal"
    "Diagonal_1"
    "Handwriting"
    "Cross"
    "IBeam"
    "Unavailiable"
    "Alternate"
]


def WinPackager(
    dir: Path,
    theme_name: str,
    comment: str,
    author: str,
    website_url: Optional[str] = None,
) -> None:
    """ Create a crispy `Windows` cursor theme package. """

    cursors: List[PosixPath] = []

    for ext in ("*.ani", "*.cur"):
        for i in sorted(dir.glob(ext)):
            cursors.append(i)

    # Checking cursor files
    if not cursors:
        raise FileNotFoundError(f"Windows cursors not found in {dir}")
    # TODO: Check all cursors

    if website_url:
        comment: str = f"{comment}\n{website_url}"

    data: str = INSTALL_INF.safe_substitute(
        theme_name=theme_name, comment=comment, author=author
    )

    # Change cursors extension (.cur||.ani) in install.inf, According to cursor files provided.
    for p in cursors:
        if p.name in data:
            continue
        else:
            old_ext: List[str] = [".ani", ".cur"]
            old_ext.remove(p.suffix)
            data = data.replace(f"{p.stem}{old_ext[0]}", p.name)

    # Store install.inf file
    install_inf: Path = dir / "install.inf"
    install_inf.write_text(data)