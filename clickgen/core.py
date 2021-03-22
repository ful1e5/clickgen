#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from copy import deepcopy
from pathlib import Path
from tempfile import mkdtemp
from typing import Dict, List, Optional, Tuple, Union

from PIL import Image as Img
from PIL.Image import Image

from clickgen.util import remove_util

# Typing
Size = Tuple[int, int]
LikePath = Union[str, Path]
LikePathList = Union[List[str], List[Path]]


class Bitmap(object):
    """The ``Bitmap`` class is used to represent a ``.png`` or sequences of 
    ``.png`` image. The class also provides a number of factory functions, \
    including functions to **rename** ``.png`` images from files, and \
    **reproduce** size of same image/s.
    """

    animated: bool
    png: Path
    grouped_png: List[Path]

    key: str

    x_hot: int
    y_hot: int

    size: Tuple[int, int]
    width: int
    height: int

    compress: int = 0

    def __init__(
        self,
        png: Union[LikePath, LikePathList],
        hotspot: Tuple[int, int],
    ) -> None:
        """
        :param png: File location. Use ``List`` for animated Cursor.
        :type png: Union[LikePath, LikePathList]

        :param hotspot: Hotspot is coordinate value in Tuple. Cursor change \
                        state is calculated from this value.
        :type hotspot: Tuple[int, int]

        :raise TypeError: If provided ``.png`` file/s location is not type \
                          **str** or **pathlib.Path**
        """
        super().__init__()

        # Is png == _P             => 'static' bitmap
        # Or png == [_P, _P, ...]  => 'animated' bitmap
        # Or png == [_P]           => 'static' bitmap
        # else TypeError()

        err: str = f"argument should be a 'str' object or 'Path' object , not \
              {type(png)}"

        if isinstance(png, (str, Path)):
            self.__set_as_static(png, hotspot)

        elif isinstance(png, list):
            if len(png) == 1:
                self.__set_as_static(png[0], hotspot)
            else:
                self.__set_as_animated(png, hotspot)
        else:
            raise TypeError(err)

    def __str__(self) -> str:
        common: str = f"key={self.key}, animated={self.animated}, size={self.size}, width={self.width}, height={self.height}, x_hot={self.x_hot}, y_hot={self.y_hot}"
        if self.animated:
            return f"Bitmap(grouped_png={self.grouped_png}, {common})"
        return f"Bitmap(png={self.png}, {common})"

    def __repr__(self) -> str:
        common: str = f"'key':'{self.key}', 'animated':{self.animated}, 'size':{self.size}, 'width':{self.width}, 'height':{self.height}, 'x_hot':{self.x_hot}, 'y_hot':{self.y_hot}"
        if self.animated:
            return f"{{ 'grouped_png':{self.grouped_png}, {common} }}"
        return f"{{ 'png':{self.png}, {common} }}"

    # Context manager support
    def __enter__(self) -> "Bitmap":
        return self

    def __exit__(self, exception_type, exception_value, traceback):  # type: ignore
        return

    #
    # Private methods
    #
    def __set_as_static(self, png: LikePath, hotspot: Tuple[int, int]) -> None:
        """Set this Bitmap as **static**, It means this bitmap hold single ``png``.

                .. note:: This method called by ``self.__init__``.

        :param png: ``.png`` file location.
        :type png: Union[str,Path]

        :param hotspot: Hotspot is coordinate value in Tuple. Cursor change \
                        state is calculated from this value.
        :type hotspot: Tuple[int, int]

        :raise FileNotFoundError: If ``.png`` file not found
        :raise ValueError: If provided bitmap is not ``.png``
        :raise ValueError: If image width & height are not same
        :raise ValueError: If grouped ``.png`` files naming is invalid
        :raise ValueError: If hotspot is set higher or lower then image pixels
        """
        self.png = self._check_bitmap(png)
        self._set_key(self.png, check=False)
        self._set_size(self.png)
        self._set_hotspot(self.png, hotspot)
        self.animated = False

    def __set_as_animated(self, png: LikePathList, hotspot: Tuple[int, int]) -> None:
        """Set this Bitmap as **animated**, It means this bitmap holds multiple ``png``.

                .. note:: This method called by ``self.__init__``.

        :param png: ``.png`` file location ***List***.
        :type png: List[Union[str,Path]]

        :param hotspot: Hotspot is coordinate value in Tuple. Cursor change \
                        state is calculated from this value.
        :type hotspot: Tuple[int, int]

        :raise FileNotFoundError: If ``.png`` file not found
        :raise ValueError: If provided bitmap is not ``.png``
        :raise ValueError: If image width & height are not same
        :raise ValueError: If grouped ``.png`` files naming is invalid
        :raise ValueError: If hotspot is set higher or lower then image pixels
        """
        self.grouped_png = []
        for p in png:
            frame: Path = self._check_bitmap(p)

            self.grouped_png.append(frame)
            self._set_key(frame, check=True)
            self._set_size(frame)

        self.grouped_png.sort()

        # Don't worry, All images sizes are equal.
        self._set_hotspot(self.grouped_png[0], hotspot)
        self.animated = True

    #
    # Protected methods
    #
    def _check_bitmap(self, bmp_path: LikePath) -> Path:
        """Checks bitmap is supported by clickgen.

        :param bmp_path: Bitmap file location.
        :type bmp_path: Union[str, Path]

        :raise FileNotFoundError: If ``.png`` file not found
        :raise ValueError: If provided bitmap is not ``.png``

        :returns: Return the ``pathlib.Path`` instant, If provided **bitmap path** checks passed.
        :rtype: Path
        """
        p: Path = Path(bmp_path)
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

    def _set_size(self, bmp_path: Path, prev_check: bool = True) -> None:
        """Set or overwrite size of this bitmap.

        :param bmp_path: Bitmap file location.
        :type bmp_path: Path

        :param prev_check: If you want to match size with previous size. This flag is useful for grouped ``png``.(@default True )
        :type prev_check: bool

        :raise ValueError: If image width & height are not same
        """
        with Img.open(bmp_path) as i:

            def __set() -> None:
                self.size = i.size
                self.width = i.width
                self.height = i.height

            if i.width == i.height:
                if prev_check:

                    try:
                        if self.size != i.size:
                            raise ValueError("All .png file's size must be equal")
                        __set()
                    except AttributeError:
                        __set()

                else:
                    __set()
            else:
                raise ValueError(
                    f"frame '{bmp_path.name}' must had equal width & height."
                )

    def _set_key(self, bmp_path: Path, check: bool) -> None:
        """Set unique identity for this bitmap.

        :param bmp_path: Bitmap file location.
        :type bmp_path: Path

        :param check: If you want sure multiple ``png`` files identity is same
        :type check: bool

        :raise ValueError: If grouped png indexing invalid.
        :raise ValueError: If new identity not matched with old.
        """
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
                self.key = k
            except AttributeError:
                self.key = k
        else:
            self.key = bmp_path.stem

    def _set_hotspot(self, img_path: Path, hotspot: Tuple[int, int]) -> None:
        """Set this bitmap reaction state.

        :param img_path: Bitmap file location.
        :type img_path: Path

        :param hotspot: ``xy`` coordinates for this bitmap.
        :type hotspot: Tuple[int, int]
        """
        x = hotspot[0]
        y = hotspot[1]
        with Img.open(img_path) as i:
            if x > i.width or y > i.height:
                raise ValueError("'Hotspot' value is an overflow")

            if x < 0 or y < 0:
                raise ValueError("'Hotspot' value is an underflow")

            self.x_hot = x
            self.y_hot = y

    def _update_hotspots(self, new_size: Size) -> None:
        """Update this bitmap reaction state.

        :param new_size: Bitmap width & height tuple (in pixel)
        :type new_size: Tuple[int, int]
        """
        if self.size != new_size:
            self.x_hot = int(round(new_size[0] / self.width * self.x_hot))
            self.y_hot = int(round(new_size[1] / self.height * self.y_hot))

    #
    # Public methods
    #
    def resize(
        self,
        size: Size,
        resample: int = Img.NONE,
        save: bool = True,
    ) -> Optional[Union[Image, List[Image]]]:
        """Resize this bitmap.

        :param size: New width & height in pixel.
        :type size: Tuple[int, int]

        :param resample: Pillow resample algorithm.
        :type resample: int

        :param save: If you want to overwrite resized bitmap to actual png file. \
                     Neither it return pillow ``Image`` buffer.
        :type save: bool

        :returns: Returns image buffers, If *save* flag is set to ``False``
        :rtype: Optional[Union[Image, List[Image]]]

        :raise ValueError: If image width & height are not same.
        """

        def __resize(p: Path, frame: int) -> Image:
            img: Image = Img.open(p)

            # Preventing image quality degrades
            if img.size != size:
                img = img.resize(size, resample=resample)
                # If save => Update attribute
                if save:
                    self._set_size(p)
                    if frame == 0:
                        self._update_hotspots(size)
                    img.save(p, compress=self.compress)
            return img

        if self.animated:
            images: List[Image] = []
            for i, png in enumerate(self.grouped_png):
                img: Image = __resize(png, i)
                images.append(img)
            if not save:
                return images
            return None

        img: Image = __resize(self.png, 0)
        if not save:
            return img
        return None

    def reproduce(
        self,
        size: Size = (24, 24),
        canvas_size: Size = (32, 32),
        position: str = "center",
        save=True,
    ) -> Optional[Union[Image, List[Image]]]:
        """Resize bitmap with more options.

        :param size: Bitmap width & height in pixel.
        :type size: Tuple[int, int]

        :param canvas_size: Bitmap's canvas width & height in pixel.
        :type canvas_size: Tuple[int, int]

        :param position: Bitmap's canvas width & height in pixel. (@default "center")
        :type position: "center" | "top_left" | "top_right" | "bottom_left" | "bottom_right"

        :param save: If you want to overwrite resized bitmap to actual png \
                       file. Neither it return pillow ``Image`` buffer.
        :type save: bool

        :returns: Returns image buffers, If *save* flag is set to ``False``
        :rtype: Optional[Union[Image, List[Image]]]

        :raise ValueError: If image width & height are not same.
        """

        def __reproduce(p: Path) -> Image:
            frame: Image = Img.open(p).resize(size, resample=Img.BICUBIC)
            x, y = tuple(map(lambda i, j: i - j, canvas_size, size))

            switch: Dict[str, Tuple[int, int]] = {
                "top_left": (0, 0),
                "top_right": (x, 0),
                "bottom_left": (0, y),
                "bottom_right": (x, y),
                "center": (round(x / 2), round(y / 2)),
            }

            box: Tuple[int, int] = switch[position]

            canvas: Image = Img.new("RGBA", canvas_size, color=(256, 0, 0, 0))
            canvas.paste(frame, box=box)

            if save:
                canvas.save(p, compress=self.compress)
                self.x_hot = int(round(size[0] / self.width * self.x_hot) + box[0])
                self.y_hot = int(round(size[1] / self.height * self.y_hot) + box[1])
                self._set_size(p, prev_check=False)
            return canvas

        if self.animated:
            images: List[Image] = []
            for png in self.grouped_png:
                images.append(__reproduce(png))
            if not save:
                return images
            return None

        image: Image = __reproduce(self.png)
        if not save:
            return image
        return None

    def rename(self, key: str) -> None:
        """Rename unique identity of bitmap.

        :param key: Bitmap unique identity.
        :type key: str

        :raise ValueError: If grouped png indexing invalid.
        :raise ValueError: If new identity not matched with old.
        """
        old_key = self.key
        if key != old_key:

            def __rename(png: Path, check: bool) -> Path:
                name: str = f"{png.stem.replace(old_key, key, 1)}{png.suffix}"
                renamed_path: Path = png.with_name(name)
                png.rename(renamed_path)
                self._set_key(renamed_path, check)
                return renamed_path

            if self.animated:
                new_pngs = []
                self.key = key
                for png in self.grouped_png:
                    new_pngs.append(__rename(png, check=True))
                self.grouped_png = new_pngs
            else:
                self.png = __rename(self.png, check=False)

    def copy(self, path: Optional[LikePath] = None) -> "Bitmap":
        """Generate deepcopy of this bitmap.

        :param path: Provide custom path to store deepcopy bitmaps. \
                     Set ``None`` to store in temporary directory. \
                     (@default None)
        :type path: str

        :returns: deepcopy of this bitmap state.
        :rtype: Bitmap

        :raise NotADirectoryError: If provided path is not directory.
        """
        if not path:
            p_obj: Path = Path(mkdtemp(prefix=f"{self.key}__copy__"))
        else:
            p_obj: Path = Path(path)

        if p_obj.is_file():
            raise NotADirectoryError(f"path '{p_obj.absolute()}' is not a directory")

        p_obj.mkdir(parents=True, exist_ok=True)

        def __copy(src: Path) -> Path:
            dst: Path = p_obj / src.name
            shutil.copy2(src, dst)
            return dst

        if self.animated:
            pngs: List[Path] = []
            for p in self.grouped_png:
                pngs.append(__copy(p))
            return Bitmap(pngs, (self.x_hot, self.y_hot))

        p = __copy(self.png)
        return Bitmap(p, (self.x_hot, self.y_hot))


class CursorAlias(object):
    bitmap: Bitmap
    prefix: str
    alias_dir: Path
    alias_file: Path
    garbage_dirs: List[Path] = []

    """Cursor Config ``.in`` or ``.alias`` file provider."""

    def __init__(
        self,
        bitmap: Bitmap,
    ) -> None:
        """
        :param bitmap: Cursor :py:class:`~clickgen.core.Bitmap` instant.
        :type bitmap: Bitmap
        """
        super().__init__()

        self.bitmap = bitmap
        self.prefix = f"{self.bitmap.key}__alias"
        self.alias_dir = Path(mkdtemp(prefix=self.prefix))

    def __get_alias_file(self) -> Optional[Path]:
        """
        :returns: Return cursor alias file path, If it's exists.
        :rtype: Optional[Path]
        """
        if hasattr(self, "alias_file"):
            return self.alias_file
        return None

    def __str__(self) -> str:
        return f"CursorAlias(bitmap={self.bitmap!s}, prefix={self.prefix}, alias_dir={self.alias_dir}, alias_file={self.__get_alias_file()}, garbage_dirs={self.garbage_dirs})"

    def __repr__(self) -> str:
        return f"{{ 'bitmap':{self.bitmap!r}, 'prefix':{self.prefix}, 'alias_dir':{self.alias_dir}, 'alias_file':{self.__get_alias_file()}, 'garbage_dirs':{self.garbage_dirs} }}"

    # Context manager support
    def __enter__(self) -> "CursorAlias":
        return self

    def __exit__(self, exception_type, exception_value, traceback):  # type: ignore

        if hasattr(self, "alias_dir"):
            remove_util(self.alias_dir)

        if hasattr(self, "garbage_dirs"):
            for p in self.garbage_dirs:
                remove_util(p)

    @classmethod
    def from_bitmap(
        cls,
        png: Union[LikePath, LikePathList],
        hotspot: Tuple[int, int],
    ) -> "CursorAlias":
        """Create cursor alias config file from ``.png`` files instant.

        :param png: File location. Use ``List`` for animated Cursor.
        :type png: Union[LikePath, LikePathList]

        :param hotspot: Hotspot is coordinate value in Tuple. Cursor change \
                        state is calculated from this value.
        :type hotspot: Tuple[int, int]

        :raise TypeError: If provided ``.png`` file/s location is not type \
                          **str** or **pathlib.Path**
        """
        bmp: Bitmap = Bitmap(png, hotspot)
        return cls(bmp)

    def create(
        self,
        sizes: Union[Size, List[Size]],
        delay: int = 10,
    ) -> Path:
        """Generate and store cursor's config file at ``temporary`` storage.

        :param sizes: Cursor pixel size tuple.
        :type sizes: Union[Tuple[int, int], List[Tuple[int, int]]]

        :param delay: Delay between every cursor frame.(Affect on only \
                animated :py:class:`~clickgen.core.Bitmap`)
        :type delay: int

        :returns: Cursor alias file path.
        :rtype: Path

        :raise TypeError: If provided ``size`` is not type of Tuple[int, int] \
                or List of Tuple[int, int]
        """

        def __generate(size: Size) -> List[str]:
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
            self.alias_file = cfg

        sizes_type_err: str = (
            "argument 'sizes' should be Tuple[int, int] type or List[Tuple[int, int]]."
        )

        # Multiple sizes
        if isinstance(sizes, list):
            # Removing duplicate sizes
            sizes = sorted(set(sizes))

            lines: List[str] = []
            for size in sizes:
                if isinstance(size, tuple):
                    lines.extend(__generate(size))
                else:
                    raise TypeError(sizes_type_err)

            __write_alias(lines)

        # Single size
        elif isinstance(sizes, tuple):
            lines = __generate(sizes)
            __write_alias(lines)

        else:
            raise TypeError(sizes_type_err)

        return self.alias_file

    def check_alias(self) -> None:
        """Checks cursor  config file exists on filesystem.

        :raise FileNotFoundError:  If cursor config file not generate. \
                Calling :py:meth:`~clickgen.core.CursorAlias.create` to \
                recreate it.
        """
        if not any(self.alias_dir.iterdir()):
            raise FileNotFoundError("Alias directory is empty or not exists.")

    def extension(self, ext: Optional[str] = None) -> Union[str, Path]:
        """``get`` or ``change`` cursor config file extension. This method helps \
        to change default config extension ``.alias`` to ``.in``.

        :param ext: Provide custom cursor's config file extension. Like \
                    ``o.extension(ext = ".in")``. (@default None)
        :type ext: Optional[str]

        :returns: Provide ``None`` value to retrieve current extension. \
                Either returns the updated cursor's config file path.
        :rtype: Union[str, Path]
        """
        self.check_alias()
        if ext:
            new_path: Path = self.alias_file.with_suffix(ext)
            self.alias_file = self.alias_file.rename(new_path)
            return self.alias_file

        return self.alias_file.suffix

    def copy(self, dst: Optional[LikePath] = None) -> "CursorAlias":
        """Copy current bitmap config to directory.

             .. note::
                 This method **creates** the ``dst`` directory if not exists.

        :param dst: Custom directory path for store deepcopy of cursor config \
                file and it's bitmaps. Provide ``None`` value to store at \
                temporary storage.
        :type dst: Optional[Union[str, Path]]

        :returns: deepcopy object of current ``CursorAlias`` state.
        :rtype: CursorAlias

        :raise FileNotFoundError:  If cursor config file not generate. \
                Calling :py:meth:`~clickgen.core.CursorAlias.create` to \
                recreate it.
        :raise NotADirectoryError: If provided ``dst`` is not a directory.
        """
        self.check_alias()

        if not dst:
            dst = mkdtemp(prefix=self.prefix)
        dst = Path(dst)

        if dst.is_file():
            raise NotADirectoryError(f"path '{dst.absolute()}' is not a directory")

        replica_object = deepcopy(self)

        shutil.copytree(
            self.alias_dir, dst, dirs_exist_ok=True, copy_function=shutil.copy
        )
        replica_object.alias_dir = dst
        replica_object.prefix = dst.stem
        replica_object.alias_file = dst / self.alias_file.name

        return replica_object

    def rename(self, key: str) -> Path:
        """Rename current cursor's config file.

        Renaming cursor config is affects naming of bitmaps. \
        This method is calls :py:meth:`~clickgen.core.Bitmap.rename` \
        internaly for renaming bitmaps name.

        :param key: Unique identity.
        :type key: str

        :returns: Renamed config file path.
        :rtype: Path

        :raise FileNotFoundError:  If cursor config file not generate. \
                Calling :py:meth:`~clickgen.core.CursorAlias.create` to \
                recreate it.
        :raise ValueError: If grouped png indexing invalid.
        :raise ValueError: If new identity not matched with old.
        """
        self.check_alias()
        old_key: str = self.bitmap.key

        if old_key != key:
            # Setting new_prefix & renaming alias directory
            new_prefix = f"{key}__alias"
            new_alias_dir = self.alias_dir.with_name(
                self.alias_dir.name.replace(self.prefix, new_prefix)
            )
            shutil.move(f"{self.alias_dir.absolute()}", new_alias_dir)
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
                elif f.is_file or f.absolute() == self.alias_file.absolute():
                    updated_data: str = f.read_text().replace(old_key, key)
                    f.write_text(updated_data)
                    self.alias_file = __rename(f)

        return self.alias_file

    def reproduce(
        self,
        size: Size = (24, 24),
        canvas_size: Size = (32, 32),
        position: str = "center",
        delay: int = 3,
    ) -> "CursorAlias":
        """Resize cursor config and bitmap.

        :param size: Bitmap width & height in pixel.
        :type size: Tuple[int, int]

        :param canvas_size: Bitmap's canvas width & height in pixel.
        :type canvas_size: Tuple[int, int]

        :param position: Bitmap's canvas width & height in pixel. (@default "center")
        :type position: "center" | "top_left" | "top_right" | "bottom_left" | "bottom_right"

        :param save: If you want to overwrite resized bitmap to actual png \
                       file. Neither it return pillow ``Image`` buffer.
        :type save: bool

        :returns: Returns reproduced ``CursorAlias`` object.
        :rtype: CursorAlias

        :raise FileNotFoundError:  If cursor config file not generate. \
                Calling :py:meth:`~clickgen.core.CursorAlias.create` to \
                recreate it.
        :raise ValueError: If image width & height are not same.
        """
        self.check_alias()

        tmp_bitmaps_dir: Path = Path(mkdtemp(prefix=f"{self.prefix}__garbage_bmps__"))
        tmp_bitmap = self.bitmap.copy(tmp_bitmaps_dir)
        tmp_bitmap.reproduce(size, canvas_size, position)

        # Will Deleted, When __exit__ being called
        self.garbage_dirs.append(tmp_bitmaps_dir)

        cls: CursorAlias = CursorAlias(tmp_bitmap)
        cls.create(canvas_size, delay)

        return cls
