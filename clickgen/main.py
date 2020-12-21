#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from typing import List, Optional, Union

_P = Union[str, Path, PathLike]


class Bmp(object):
    animated: bool
    png: Path
    grouped_png: List[Path]
    key: str

    def __init__(self, png: Union[_P, List[_P]], key: Optional[str] = None) -> None:

        # Is png == str|Path        => 'static' bitmap
        # Or png == [str|Path]      => 'animated' bitmap
        # else TypeError()

        if isinstance(png, str) or isinstance(png, Path):
            self.png = self.__get_Path(png)
            self.__set_key(self.png, check=False)
            self.animated = False

        elif isinstance(png, list):
            if key:
                self.key, _ = key.rsplit("-", 1)

            self.grouped_png = []
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
        if check:
            try:
                k, _ = p.stem.rsplit("-", 1)
            except ValueError:
                raise ValueError(
                    f"Invalid Bitmap name '{p.name}': Grouped Bitmaps must-have frame number followed by '-'. Like 'bitmap-000.png'"
                ) from None

            try:
                if self.key != k:
                    raise IOError(
                        f"Bitmap '{p.name}' not matched with key '{self.key}'. Provide a Grouped Bitmaps with frame number followed by '-'.  Like 'bitmap-000.png','bitmap-001.png' "
                    )
                else:
                    self.key = k
            except AttributeError as e:
                self.key = k
        else:
            self.key = p.stem
