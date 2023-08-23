#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from string import Template
from typing import Dict

FILE_TEMPLATES: Dict[str, Template] = {
    "cursor.theme": Template('[Icon Theme]\nName=$theme_name\nInherits="$theme_name"'),
    "index.theme": Template(
        '[Icon Theme]\nName=$theme_name\nComment=$comment\nInherits="hicolor"'
    ),
}


def pack_x11(dir: Path, theme_name: str, comment: str) -> None:
    """This method generates ``cursor.theme`` & ``index.theme`` files at \
        ``directory``.

    :param dir: Path where ``.theme`` files save.
    :param dir: ``pathlib.Path``

    :param theme_name: Name of theme.
    :param theme_name: ``str``

    :param comment: Extra information about theme.
    :param comment: ``str``

    :returns: None.
    :rtype: ``None``
    """

    for fname, template in FILE_TEMPLATES.items():
        data = template.safe_substitute(theme_name=theme_name, comment=comment)
        fp: Path = dir / fname
        fp.write_text(data)
