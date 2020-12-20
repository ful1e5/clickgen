#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import List, Union

_P = Union[str, Path, PathLike]


class Bmp:
    animated: bool
    png: Path
    grouped_png: List[Path] = []
    key: str

    def __init__(self, png: Union[_P, List[_P]]) -> None:
        if isinstance(png, str) or isinstance(png, Path):
            self.png = self.__get_Path(png)
            self.key = self.png.stem
            self.animated = False

        elif isinstance(png, list):
            for p in png:
                self.grouped_png.append(self.__get_Path(p))
            self.key = self.grouped_png[0].stem.rsplit("-", 1)

            self.grouped_png.sort()
            self.animated = True

        else:
            raise TypeError(
                f"argument should be a 'str' object , 'Path' object or an 'os.PathLike' object returning str, not {type(png)}"
            )

    def __get_Path(self, p: _P) -> Path:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(f"Not such file in '{path.absolute()}'")
        return path


print(Bmp(["b.png", "a.png"]).grouped_png[0].absolute())
