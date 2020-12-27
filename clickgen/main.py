#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from copy import deepcopy
from os import PathLike
from pathlib import Path
from tempfile import mkdtemp
from typing import List, Literal, Optional, Tuple, TypeVar, Union, overload

from PIL import Image as Img
from PIL.Image import Image

_T = TypeVar("_T")
_P = TypeVar("_P", str, Path, PathLike)
_Size = Tuple[int, int]


def replica(obj: _T) -> _T:
    return deepcopy(obj)


def to_path(p: _P) -> Path:
    if isinstance(p, str) or isinstance(p, PathLike):
        return Path(p)
    elif isinstance(p, Path):
        return p
    else:
        raise TypeError(
            f"Unable to convert parameter 'p' to 'Path' with 'TypeVar('_P', str, Path, PathLike)'"
        )


class Bitmap(object):
    animated: bool
    png: Path
    grouped_png: List[Path]

    key: str

    x_hot: int
    y_hot: int

    size: Tuple[int, int]
    width: int
    height: int

    compress: Literal[0, 1, 2, 3, 4, 5, 6, 7, 8, 9] = 0

    def __init__(
        self,
        png: Union[_P, List[_P]],
        hotspot: Tuple[int, int] = (0, 0),
        key: Optional[str] = None,
    ) -> None:
        super().__init__()

        self.x_hot = hotspot[0]
        self.y_hot = hotspot[1]

        # Is png == _P        => 'static' bitmap
        # Or png == [_P, _P]  => 'animated' bitmap
        # Or png == [_P]      => 'static' bitmap
        # else TypeError()
        err: str = f"argument should be a 'str' object , 'Path' object or an 'os.PathLike' object returning str, not {type(png)}"

        if isinstance(png, str) or isinstance(png, Path):
            self.__set_as_static(png)

        elif isinstance(png, list):
            if key:
                self.key, _ = key.rsplit("-", 1)

            if len(png) == 1:
                self.__set_as_static(png[0])
            else:
                self.__set_as_animated(png)
        else:
            raise TypeError(err)

    def __str__(self) -> str:
        common: str = f"key={self.key}, animated={self.animated}, size={self.size}, width={self.width}, height={self.height}"
        if self.animated:
            return (
                f"{self.__class__.__name__}(grouped_png={self.grouped_png}, {common})"
            )
        else:
            return (
                f"{self.__class__.__name__}(png={self.png}, key={self.key}, {common})"
            )

    def __repr__(self) -> str:
        common: str = f"'key':{self.key}, 'animated':{self.animated} 'size':{self.size}, 'width':{self.width}, 'height':{self.height}"
        if self.animated:
            return f"{{ 'grouped_png':{self.grouped_png}, {common}}}"
        else:
            return f"{{ 'png':{self.png}, {common}}}"

    # Context manager support
    def __enter__(self) -> "Bitmap":
        return self

    def __exit__(self, *args) -> None:
        self.animated = None
        self.key = None
        self.size = None
        self.height = None
        self.width = None
        if hasattr(self, "grouped_png"):
            self.grouped_png = None
        else:
            self.png = None

    #
    # Private methods
    #
    def __set_as_static(self, png: _P) -> None:
        self.png = self._check_bitmap(png)

        self._set_key(self.png, check=False)
        self._set_size(self.png)
        self.animated = False

    def __set_as_animated(self, png: List[_P]) -> None:

        self.grouped_png = []
        for p in png:
            frame: Path = self._check_bitmap(p)

            self.grouped_png.append(frame)
            self._set_key(frame, check=True)
            self._set_size(frame)

        self.grouped_png.sort()
        self.animated = True

    #
    # Protected methods
    #
    def _check_bitmap(self, bmp_path: _P) -> Path:
        p: Path = to_path(bmp_path)
        if not p.exists():
            raise FileNotFoundError(
                f"Not a such file '{p.name}' in '{p.parent.absolute()}'"
            )

        # Supported bitmap type
        # => *.png
        for bmp_pattern in ("*.png",):
            if not p.match(bmp_pattern):
                raise ValueError(
                    f"{self.__class__} supports '{bmp_pattern}' bitmaps type, not '{p.suffix}'"
                )
        return p

    def _set_size(self, bmp_path: Path) -> None:
        with Img.open(bmp_path) as i:
            if i.width == i.height:

                def __set() -> None:
                    self.size = i.size
                    self.width = i.width
                    self.height = i.height

                try:
                    if self.size != i.size:
                        raise IOError("All .png file's size must be equal")
                    else:
                        pass
                except AttributeError:
                    __set()

            else:
                raise IOError(f"frame '{bmp_path.name}' must had equal width & height.")

    def _set_key(self, bmp_path: Path, check: bool) -> None:
        if check:
            try:
                k, _ = bmp_path.stem.rsplit("-", 1)
            except ValueError:
                raise ValueError(
                    f"Invalid Bitmap name '{bmp_path.name}': Grouped Bitmaps must-have frame number followed by '-'. Like 'bitmap-000.png'"
                ) from None

            try:
                if self.key != k:
                    raise ValueError(
                        f"Bitmap '{bmp_path.name}' not matched with key '{self.key}'. Provide a Grouped Bitmaps with frame number followed by '-'.  Like 'bitmap-000.png','bitmap-001.png' "
                    )
                else:
                    self.key = k
            except AttributeError:
                self.key = k
        else:
            self.key = bmp_path.stem

    def _update_hotspots(self, new_size: _Size) -> None:
        self.x_hot = int(round(new_size[0] / self.width * self.x_hot))
        self.y_hot = int(round(new_size[1] / self.height * self.y_hot))

    #
    # Public methods
    #
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
                    self._set_size(p)
                    self._update_hotspots(size)
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

    def reproduce(
        self,
        size: _Size = (24, 24),
        canvas_size: _Size = (32, 32),
        position: Literal[
            "top_left", "top_right", "bottom_right", "bottom_right", "center"
        ] = "center",
        save=True,
    ) -> Optional[Union[Image, List[Image]]]:
        def __reproduce(p: Path) -> Image:
            i: Image = Img.open(p).resize(size, resample=Img.BICUBIC)
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
            canvas.paste(i, box=box)

            if save:
                self._set_size(p)
                self._update_hotspots(canvas_size)
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

    def rename(self, key: str) -> "Bitmap":
        old_key = self.key
        if key != old_key:
            replica_object = replica(self)

            def __rename(png: Path, check: bool) -> None:
                name: str = f"{png.stem.replace(old_key, key)}{png.suffix}"
                path: Path = png.with_name(name)
                png.rename(path)
                replica_object._set_key(png, check)

            if self.animated:
                for png in replica_object.grouped_png:
                    __rename(png, check=True)
            else:
                __rename(replica_object.png, check=False)

            return replica_object

        else:
            return self

    def copy(self, path: _P) -> "Bitmap":
        path: Path = to_path(path)

        if path.is_file():
            raise NotADirectoryError(f"path '{path.absolute()}' is not a directory")

        replica_object = replica(self)
        path.mkdir(parents=True, exist_ok=True)

        def __copy(src: Path) -> Path:
            dst: Path = path / src.name
            shutil.copy2(src, dst)
            return dst

        if self.animated:
            for index, png in enumerate(replica_object.grouped_png):
                replica_object.grouped_png[index] = __copy(png)
        else:
            replica_object.png = __copy(replica_object.png)

        return replica_object


class CursorAlias(object):
    bitmap: Bitmap
    prefix: str
    alias_dir: Path
    alias_p: Path

    def __init__(
        self,
        bitmap: Bitmap,
        alias_directory: Optional[_P] = None,
    ) -> None:
        super().__init__()

        self.bitmap = bitmap
        self.prefix = f"{self.bitmap.key}__alias"

        if alias_directory:
            self.alias_dir = to_path(alias_directory)
        else:
            self.alias_dir = Path(mkdtemp(prefix=self.prefix))

    # helper method
    def check_alias(self) -> None:
        if not any(self.alias_dir.iterdir()):
            raise Exception(f"Alias directory is empty or not exists.")
        else:
            return None

    # Context manager support
    def __enter__(self) -> "CursorAlias":
        return self

    def __exit__(self, *args) -> None:
        # Bitmap attr
        self.bitmap.__exit__()
        self.bitmap = None
        self.prefix = None

        # Clean files
        if hasattr(self, "alias_p"):
            shutil.rmtree(self.alias_dir)
            self.alias_p = None

        # Current attr
        self.alias_dir = None
        self.hotspot = None

    @classmethod
    def open(
        cls,
        png: Union[_P, List[_P]],
        hotspot: Tuple[int, int] = (0, 0),
        key: Optional[str] = None,
        alias_directory: Optional[_P] = None,
    ) -> "CursorAlias":
        bmp: Bitmap = Bitmap(png, hotspot=hotspot, key=key)
        return cls(bmp, alias_directory)

    def alias(self, sizes: Union[_Size, List[_Size]], delay: int = 10) -> Path:
        def __generate(size: _Size) -> List[str]:
            d: Path = self.alias_dir / f"{size[0]}x{size[1]}"

            bmp: Bitmap = self.bitmap.copy(d)
            bmp.resize(size, resample=Img.BICUBIC)

            l: List[str] = []

            for file in d.glob("*.png"):
                fp: str = f"{file.relative_to(self.alias_dir)}"

                line: str = f"{size[0]} {bmp.x_hot} {bmp.y_hot} {fp}"
                if self.bitmap.animated:
                    line = f"{line} {delay}"

                l.append(f"{line}\n")
            return l

        def __write_alias(lines: List[str]) -> None:
            # sorting all lines according to size (24x24, 28x28, ..)
            lines.sort()
            # remove newline from EOF
            lines[-1] = lines[-1].rstrip("\n")

            cfg: Path = self.alias_dir / f"{self.bitmap.key}.alias"
            with cfg.open("w") as f:
                f.writelines(lines)
            self.alias_p = cfg

        sizes_type_err: str = (
            f"argument 'sizes' should be Tuple[int, int] type or List[Tuple[int, int]]."
        )

        if isinstance(sizes, list):
            lines: List[str] = []
            for size in sizes:
                if isinstance(size, tuple):
                    lines.extend(__generate(size))
                else:
                    raise TypeError(sizes_type_err)
            __write_alias(lines)

        elif isinstance(sizes, tuple):
            lines = __generate(sizes)
            __write_alias(lines)
        else:
            raise TypeError(sizes_type_err)

        return self.alias_p

    @overload
    def extension(self) -> str:
        ...

    @overload
    def extension(self, ext: str) -> Path:
        ...

    def extension(self, ext: Optional[str] = None) -> Union[str, Path]:
        self.check_alias()
        if ext:
            new_path: Path = self.alias_p.with_suffix(ext)
            self.alias_p = self.alias_p.rename(new_path)

            return self.alias_p
        else:
            return self.alias_p.suffix

    def copy(self, dst: Optional[_P] = None) -> "CursorAlias":
        self.check_alias()

        if not dst:
            dst = mkdtemp(prefix=self.prefix)
        dst: Path = to_path(dst)

        if dst.is_file():
            raise NotADirectoryError(f"path '{dst.absolute()}' is not a directory")

        replica_object = replica(self)

        shutil.copytree(self.alias_dir, dst, copy_function=shutil.copy)
        replica_object.alias_dir = dst
        replica_object.prefix = dst.stem
        replica_object.alias_p = dst / self.alias_p.name

        return replica_object

    def rename(self, key: str) -> Path:
        self.check_alias()
        old_key: str = self.bitmap.key

        # Setting new_prefix & renaming alias directory
        new_prefix = f"{key}__alias"
        new_alias_dir = self.alias_dir.with_name(
            self.alias_dir.name.replace(self.prefix, new_prefix)
        )
        shutil.move(str(self.alias_dir), str(new_alias_dir))
        self.prefix = new_prefix
        self.alias_dir = new_alias_dir

        # Renaming content
        def __rename(p: Path) -> Path:
            name: str = f"{p.stem.replace(old_key, key, 1)}{p.suffix}"
            path: Path = p.with_name(name)
            return p.rename(path)

        for f in self.alias_dir.iterdir():
            if f.is_dir():
                for png in f.glob("*.png"):
                    png = __rename(png)
            elif f.is_file or f.absolute() == self.alias_p.absolute():
                updated_data: str = f.read_text().replace(old_key, key)
                f.write_text(updated_data)

                self.alias_p = __rename(f)
            else:
                pass

        return self.alias_p
