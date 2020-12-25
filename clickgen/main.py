#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tempfile import mkdtemp
from copy import deepcopy
from os import PathLike
from pathlib import Path
from typing import List, Literal, Optional, Tuple, TypeVar, Union

import shutil
from PIL import Image as Img
from PIL.Image import Image

_P = TypeVar("_P", str, Path, PathLike)
_Size = Tuple[int, int]


class Bitmap(object):
    animated: bool
    png: Path
    grouped_png: List[Path]
    key: str

    compress: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 0

    def __init__(self, png: Union[_P, List[_P]], key: Optional[str] = None) -> None:
        super().__init__()

        # Is png == _P        => 'static' bitmap
        # Or png == [_P]      => 'animated' bitmap
        # else TypeError()

        if isinstance(png, str) or isinstance(png, Path):
            self.png = self._get_Path(png)
            self._set_key(self.png, check=False)
            self.animated = False
            self.png

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

    def __str__(self) -> str:
        if self.animated:
            return f"{self.__class__.__name__}(grouped_png={self.grouped_png}, key={self.key}, animated={self.animated})"
        else:
            return f"{self.__class__.__name__}(png={self.png}, key={self.key}, animated={self.animated})"

    def __repr__(self) -> str:

        if self.animated:
            return f"{{ 'grouped_png':{self.grouped_png}, 'key':{self.key}, 'animated':{self.animated} }}"
        else:
            return (
                f"{{ 'png':{self.png}, 'key':{self.key}, 'animated':{self.animated} }}"
            )

    # Context manager support
    def __enter__(self) -> "Bitmap":
        return self

    def __exit__(self, *args) -> None:
        self.animated = None
        self.key = None
        if hasattr(self, "grouped_png"):
            self.grouped_png = None
        else:
            self.png = None

    def _get_Path(self, p: _P) -> Path:
        path = Path(p)
        if not path.exists():
            raise FileNotFoundError(
                f"Not a such file '{path.name}' in '{path.parent.absolute()}'"
            )

        # Supported bitmap extension
        # => *.png
        for path_pattern in ("*.png",):
            if not path.match(path_pattern):
                raise IOError(
                    f"{self.__class__} only supports '.png' bitmaps type, not ''"
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
        if self.animated:
            return self.grouped_png
        else:
            return self.png

    def resize(
        self,
        size: _Size,
        resample: int = Img.NONE,
        save: bool = True,
    ) -> Optional[Union[Image, List[Image]]]:
        def __resize(p: Path) -> Image:
            img: Image = Img.open(p)

            # Preventing image quality degrades
            if img.size != size:
                img = img.resize(size, resample=resample)
                if save:
                    img.save(p, compress=self.compress)
            return img

        if self.animated:
            images: List[Image] = []
            for png in self.grouped_png:
                img: Image = __resize(png)
                images.append(img)
            if not save:
                return images
            else:
                return None

        else:
            img: Image = __resize(self.png)
            if not save:
                return img
            else:
                return None

    def rename(self, key: str) -> "Bitmap":

        old_key = self.key
        if key != old_key:
            copy_obj = deepcopy(self)

            def __rename(png: Path, check: bool) -> None:
                name: str = png.name.replace(old_key, key)
                path: Path = png.with_name(name)
                # TODO:Check path & png is equal or not
                png.rename(path)
                copy_obj._set_key(png, check)

            if self.animated:
                for png in copy_obj.grouped_png:
                    __rename(png, check=True)
            else:
                __rename(copy_obj.png, check=False)

            return copy_obj

        else:
            return self

    def copy(self, path: Path) -> "Bitmap":
        copy_obj = deepcopy(self)

        if path.is_file():
            raise NotADirectoryError(f"path '{path.absolute()}' is not a directory")

        path.mkdir(parents=True, exist_ok=True)

        def __copy(src: Path) -> Path:
            dst: Path = path / src.name
            shutil.copy2(src, dst)
            return dst

        if self.animated:
            for index, png in enumerate(copy_obj.grouped_png):
                copy_obj[index] = __copy(png)
        else:
            copy_obj.png = __copy(copy_obj.png)

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
            x, y = tuple(map(lambda i, j: i - j, canvas_size, size))

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

        if self.animated:
            images: List[Image] = []
            for png in self.grouped_png:
                images.append(__reproduce(png))
            if not save:
                return images
            else:
                return None

        else:
            image: Image = __reproduce(self.png)
            if not save:
                return image
            else:
                return None


class CursorAlias(object):
    bitmap: Bitmap
    prefix: Path
    x: int
    y: int
    alias_p: Path

    def __init__(
        self,
        bitmap: Bitmap,
        hotspot: Tuple[int, int],
        directory: _P = mkdtemp(prefix="clickgen_alias_"),
    ) -> None:
        super().__init__()

        self.bitmap = bitmap
        self.x = hotspot[0]
        self.y = hotspot[1]
        self.prefix = Path(directory)

    # Context manager support
    def __enter__(self) -> "CursorAlias":
        return self

    def __exit__(self, *args) -> None:
        # Bitmap attr
        self.bitmap.__exit__()
        self.bitmap = None

        # Clean files
        if hasattr(self, "alias_p"):
            shutil.rmtree(self.prefix)
            self.alias_p = None

        # Current attr
        self.prefix = None
        self.hotspot = None

    @classmethod
    def open(
        cls,
        png: Union[_P, List[_P]],
        hotspot: Tuple[int, int],
        key: Optional[str] = None,
    ) -> "CursorAlias":
        bmp: Bitmap = Bitmap(png, key)
        return cls(bmp, hotspot)

    def alias(self, sizes: Union[_Size, List[_Size]], delay: int = 10) -> Path:
        def __generate(size: _Size) -> List[str]:

            if size[0] == size[1]:
                d: Path = self.prefix / f"{size[0]}x{size[1]}"

                bmp: Bitmap = self.bitmap.copy(d)
                bmp.resize(size, resample=Img.BICUBIC)

                # TODO: Hotspots calc

                l: List[str] = []
                for file in d.glob("*.png"):
                    fp: str = f"{file.relative_to(self.prefix)}"

                    line: str = f"{size[0]} {self.x} {self.y} {fp}"
                    if self.bitmap.animated:
                        line = f"{line} {delay}"

                    l.append(f"{line}\n")
                return l

            else:
                raise ValueError(f"Got different width & height in argument 'size'.")

        def __write_alias(lines: List[str]) -> Path:
            # sort line, So all lines in order according to size (24x24, 28x28, ..)
            lines.sort()

            # remove newline from EOF
            lines[-1] = lines[-1].rstrip("\n")
            cfg: Path = self.prefix / f"{self.bitmap.key}.alias"

            with cfg.open("w") as f:
                f.writelines(lines)

            self.alias_p = cfg

        if isinstance(sizes, list):
            lines: List[str] = []
            for size in sizes:
                lines.append(__generate(size))
            __write_alias(lines)

        elif isinstance(sizes, tuple):
            lines = __generate(sizes)
            __write_alias(lines)
        else:
            raise TypeError(
                f"argument 'sizes' should be Tuple[int, int] type or List[Tuple[int, int]]."
            )

        return self.alias_p


with CursorAlias.open("a.png", (30, 30)) as b:
    pp = b.alias((20, 20))
    print(pp.read_text())
