#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict

from string import Template

# '.theme' extension tagged in `ref:XPackager` module

THEME_FILES_TEMPLATES: Dict[str, Template] = {
    "cursor.theme": Template('[Icon Theme]\nName=$theme_name\nInherits="hicolor"'),
    "index.theme": Template(
        '[Icon Theme]\nName=$theme_name\nComment=$comment\nInherits="hicolor"'
    ),
}


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