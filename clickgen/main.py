#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import List, Union

_P = Union[str, Path, PathLike]


class Bmp(object):
    animated: bool
    png: Path
    grouped_png: List[Path] = []
    key: str

    def __init__(self, png: Union[_P, List[_P]]) -> None:
        if isinstance(png, str) or isinstance(png, Path):
            self.png = self.__get_Path(png)
            self.__set_key(self.png, check=False)
            self.animated = False

        elif isinstance(png, list):
            for index, p in enumerate(png):
                self.grouped_png.append(self.__get_Path(p))
                self.__set_key(self.grouped_png[index], check=True)

            self.grouped_png.sort()
            self.animated = True

        else:
            raise TypeError(
                f"argument should be a 'str' object , 'Path' object or an 'os.PathLike' object returning str, not {type(png)}"
            )

    def __get_Path(self, p: _P) -> Path:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(
                f"Not a such file '{path.name}' in '{path.parent.absolute()}'"
            )
        return path

    def __set_key(self, p: Path, check: bool) -> None:
        def key(s: str) -> str:
            try:
                k, value = s.rsplit("-", 1)
            except ValueError:
                raise ValueError(
                    f"Invalid Bitmap name '{s}': Grouped Bitmaps must-have frame number followed by '-'. Like 'bitmap-001.png'"
                ) from None

            return k

        k: str = key(p.name)

        try:
            if check and self.key != k:
                raise IOError(
                    "Bitmaps group's key not matched, Provide a Grouped Bitmaps with frame number followed by '-'.  Like 'bitmap-001.png','image-002.png' "
                )
            else:
                self.key = k
        except AttributeError as e:
            self.key = k


print(Bmp(["a-002.png", "a.png", "a-003.png"]).grouped_png[0].absolute())
