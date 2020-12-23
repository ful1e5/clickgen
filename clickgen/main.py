#!/usr/bin/env python
# -*- coding: utf-8 -*-

from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import List, Literal, Optional, Tuple, TypeVar, Union

from PIL import Image as Img
from PIL.Image import Image

_P = TypeVar("_P", str, Path, PathLike)
_Size = Tuple[int, int]


class Bmp(object):
    animated: bool
    png: Path
    grouped_png: List[Path]
    key: str

    compress: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 0

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

    def resize(
        self,
        size: _Size,
        save: bool = True,
        resample: int = Img.NONE,
    ) -> Optional[Union[Image, List[Image]]]:
        def __resize(p: Path) -> Image:
            img: Image = Img.open(p)

            # Preventing image quality degrades
            if img.size != size:
                img = img.resize(size, resample=resample)
                if save:
                    img.save(p, compress=self.compress)
            return img

        try:
            images: List[Image] = []
            for png in self.grouped_png:
                img: Image = __resize(png)
                images.append(img)
            if not save:
                return images
            else:
                return None

        except AttributeError:
            img: Image = __resize(self.png)
            if not save:
                return img
            else:
                return None

    def rename(self, key: str) -> "Bmp":

        copy_obj = deepcopy(self)
        old_key = copy_obj.key

        def __rename(png: Path, check: bool) -> None:
            name: str = png.name.replace(old_key, key)
            path: Path = png.with_name(name)
            png.rename(path)
            copy_obj._set_key(png, check)

        try:
            for png in copy_obj.grouped_png:
                __rename(png, check=True)
        except AttributeError:
            __rename(copy_obj.png, check=False)

        return copy_obj

    def reproduce(
        self,
        size: Tuple[int, int] = (24, 24),
        canvas_size: Tuple[int, int] = (32, 32),
        position: Literal[
            "top_left", "top_right", "bottom_right", "bottom_right", "center"
        ] = "center",
        save=True,
    ) -> Optional[Union[Image, List[Image]]]:
        def __reproduce(p: Path) -> Image:
            x = canvas_size[0] - size[0]
            y = canvas_size[1] - size[1]

            switch = {
                "top_left": (0, 0),
                "top_right": (x, 0),
                "bottom_left": (0, y),
                "bottom_right": (x, y),
                "center": (round(x / 2), round(y / 2)),
            }

            box: Tuple[int, int] = switch.get(position)

            canvas: Image = Img.new("RGBA", canvas_size, color=(256, 0, 0, 0))
            i: Image = Img.open(p).resize(size, resample=Img.BICUBIC)
            canvas.paste(i, box=box)
            if save:
                canvas.save(p, compress=self.compress)
            return canvas

        try:
            images: List[Image] = []
            for png in self.grouped_png:
                images.append(__reproduce(png))
            if not save:
                return images
            else:
                return None

        except AttributeError:
            image: Image = __reproduce(self.png)
            if not save:
                return image
            else:
                return None


f = Bmp("b.png").reproduce(position="top_left")
