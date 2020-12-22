#!/usr/bin/env python
# -*- coding: utf-8 -*-

from build.lib.clickgen.Type.image import ImageSize
from os import PathLike
from pathlib import Path
from typing import List, Literal, Optional, Tuple, TypeVar, Union

from PIL.Image import Image

_P = TypeVar("_P", str, Path, PathLike)


class Bmp(object):
    animated: bool
    png: Path
    grouped_png: List[Path]
    key: str

    def __init__(self, png: Union[_P, List[_P]], key: Optional[str] = None) -> None:

        # Is png == _P        => 'static' bitmap
        # Or png == [_P]      => 'animated' bitmap
        # else TypeError()

        if isinstance(png, str) or isinstance(png, Path):
            self.png = self._get_Path(png)
            self._set_key(self.png, check=False)
            self.animated = False

        elif isinstance(png, list):
            if key:
                self.key, _ = key.rsplit("-", 1)

            self.grouped_png = []
            for index, p in enumerate(png):
                self.grouped_png.append(self._get_Path(p))
                self._set_key(self.grouped_png[index], check=True)

            self.grouped_png.sort()
            self.animated = True

        else:
            raise TypeError(
                f"argument should be a 'str' object , 'Path' object or an 'os.PathLike' object returning str, not {type(png)}"
            )

    def _get_Path(self, p: _P) -> Path:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(
                f"Not a such file '{path.name}' in '{path.parent.absolute()}'"
            )

        # Supported bitmap extension
        # => *.png
        ext: str = path.suffix
        if ext != ".png":
            raise IOError(
                f"{self.__class__} only supports '.png' bitmaps type, not '{ext}'"
            )
        return path

    def _set_key(self, p: Path, check: bool) -> None:
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

    def bitmap(self) -> Union[Path, List[Path]]:
        try:
            return self.grouped_png
        except AttributeError:
            return self.png

    @classmethod
    def rename(cls, name: str, key: Optional[str]) -> "Bmp":

        try:
            for png in cls.grouped_png:
                path: Path = png.parent

        except AttributeError:
            pass

    @classmethod
    def reposition(
        self,
        position: Literal[
            "top_left", "top_right", "bottom_right", "bottom_right", "center"
        ] = "center",
    ) -> "Bmp":

        try:
            for png in super().grouped_png:
                pass

        except AttributeError:
            pass
