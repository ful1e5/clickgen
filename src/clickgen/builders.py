#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Generate Cursors without hassle.

.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

import ctypes
import io
import math
import shlex
from ctypes import CDLL
from pathlib import Path
from struct import pack
from typing import Any, List, NamedTuple, Tuple, Union

from PIL import Image, ImageFilter

from clickgen import __path__
from clickgen.core import CursorAlias
from clickgen.util import remove_util

clickgen_pypi_path = "".join(map(str, __path__))


class XCursor:
    """Build `XCursor` from the ``.in`` config file. \
    This class call ``xcursorgen`` for generating static \
    and animated ``xcursor``.
    """

    config_file: Path
    prefix: Path
    out_dir: Path
    out: Path

    # main function ctypes define
    _lib_location: Path = Path(clickgen_pypi_path) / "xcursorgen.so"
    _lib: CDLL = CDLL(str(_lib_location.absolute()))
    _LP_c_char = ctypes.POINTER(ctypes.c_char)
    _LP_LP_c_char = ctypes.POINTER(_LP_c_char)
    _lib.main.argtypes = (ctypes.c_int, _LP_LP_c_char)

    def __init__(self, config_file: Path, out_dir: Path) -> None:
        """
        :param config_file: Cursor config file location.
        :type config_file: ``pathlib.Path``

        :param out_dir: directory path where ``xcursor`` generated.
        :type out_dir: ``pathlib.Path``

        :raise FileNotFoundError: If ``config_file`` not existed on \
                filesystem.
        """
        if not config_file.exists() or not config_file.is_file():
            raise FileNotFoundError(
                f"'{config_file.name}' is not found or not a config file"
            )

        self.config_file: Path = config_file
        self.prefix = config_file.parent
        self.out_dir = out_dir / "cursors"
        self.out_dir.mkdir(parents=True, exist_ok=True)
        self.out = self.out_dir / self.config_file.stem

    def gen_argv_ctypes(self, argv: List[str]) -> Any:
        """Convert `string` arguments to `ctypes` pointer.

        :param argv: ``xcursorgen`` command-line arguments. First argument \
                must be named of program, Here it's ``xcursorgen``.
        :type argv: List[str]

        :returns: **Casted** command line arguments for *xcursorgen* with \
                ``ctype``.
        :rtype: ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
        """
        p = (self._LP_c_char * len(argv))()  # type: ignore

        for i, arg in enumerate(argv):
            enc_arg: bytes = str(arg).encode("utf-8")
            p[i] = ctypes.create_string_buffer(enc_arg)

        return ctypes.cast(p, self._LP_LP_c_char)

    def generate(self) -> None:
        """ Generate the ``xcursor`` at ``out_dir``.

        :raise RuntimeError: unable to generate ``xcursor`` from \
                ``config_file``.
        """
        # remove old cursor file
        remove_util(self.out)

        argv: List[str] = [
            "xcursorgen",
            # prefix args for xcursorgen (do not remove)
            "-p",
            str(self.prefix.absolute()),
            # cursor's config/alias file
            str(self.config_file.absolute()),
            # xcursor/output path
            str(self.out.absolute()),
        ]

        kwargs: ctypes.pointer[ctypes.c_char] = self.gen_argv_ctypes(argv)
        args: ctypes.c_int = ctypes.c_int(len(argv))

        exec_with_error: bool = bool(self._lib.main(args, kwargs))
        if exec_with_error:
            raise RuntimeError(
                f"'xcursorgen' failed to generate XCursor from '{self.config_file.name}'"
            )

    @classmethod
    def create(cls, alias_file: Path, out_dir: Path) -> Path:
        """ Class method for generate ``xcursor`` from cursor's \
        config files.

        This method gives ability to generate ``xcursor`` with initiate the \
        XCursor object.

        :returns: Generated ``XCursor`` pathlib.Path object.
        :rtype: ``pathlib.Path``

        """
        cursor = cls(alias_file, out_dir)
        cursor.generate()
        return cursor.out

    @classmethod
    def from_bitmap(cls, **kwargs) -> Path:
        if "png" not in kwargs:
            raise KeyError("argument 'png' required")
        elif "hotspot" not in kwargs:
            raise KeyError("argument 'hotspot' required")
        elif "x_sizes" not in kwargs:
            raise KeyError("argument 'x_sizes' required")
        elif "out_dir" not in kwargs:
            raise KeyError("argument 'out_dir' required")

        with CursorAlias.from_bitmap(kwargs["png"], kwargs["hotspot"]) as alias:
            x_cfg: Path
            if alias.bitmap.animated:
                if "delay" not in kwargs:
                    raise KeyError("argument 'delay' required")
                else:
                    x_cfg = alias.create(kwargs["x_sizes"], kwargs["delay"])
            else:
                x_cfg = alias.create(kwargs["x_sizes"])
            cursor = cls(x_cfg, kwargs["out_dir"])
            cursor.generate()
            return cursor.out


Color = Tuple[int, int, int, int]


class Options(NamedTuple):
    """Structure `anicursorgen.py` CLI arguments.

    :param add_shadow: Do not generate shadows for cursors \
            (assign False to cancel its effect).
    :type add_shadow: bool

    :param blur: Blur radius, in percentage of the canvas size \
            (default is 3.125, set to 0 to disable blurring).
    :type blur: float

    :param color: Shadow color in (RR,GG,BB,AA) \
            (default is (0, 0, 0, 64)).
    :type color: Tuple[int, int, int, int]

    :param down_shift: Shift shadow down by this percentage of the \
            canvas size (default is 3.125)
    :type down_shift: float

    :param right_shift: Shift shadow right by this percentage of the\
            canvas size (default is 9.375).
    :type right_shift: float
    """

    add_shadows: bool = False
    blur: float = 3.125
    color: Color = (0, 0, 0, 64)
    down_shift: float = 3.125
    right_shift: float = 9.375


ConfigFrame = Tuple[int, int, int, str, int]


class WindowsCursor:
    """Build **Windows cursors** from ``.in`` configs files. This class \
    code is inspired on `anicursorgen.py`.

    Yaru Icons \
        <https://github.com/ubuntu/yaru/blob/master/icons/src/cursors/anicursorgen.py>

    Copyright (C) 2015 Руслан Ижбулатов <lrn1986@gmail.com>
    Copyright (C) 2021 Kaiz Khatri <kaizmandhu@gmail.com>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
    """

    options: Options
    config_file: Path
    prefix: Path
    out_dir: Path
    out: Path

    def __init__(self, config_file: Path, out_dir: Path, options: Options) -> None:
        """Initiate WindowsCursor instance.

        :param config_file: Cursor config file location.
        :type config_file: ``pathlib.Path``

        :param out_dir: directory path where ``Windows Cursor`` generated.
        :type out_dir: ``pathlib.Path``

        :param options: ``anicursorgen`` commandline arguments.
        :type options: Options

        :returns: None.
        :rtype: ``None``
        """

        self.config_file = config_file
        self.prefix = config_file.parent
        self.out_dir = out_dir
        self.options = options

        self.out_dir.mkdir(exist_ok=True, parents=True)

    def get_frames(self) -> List[ConfigFrame]:
        """Internal method for passing cursor's config file to ``List``.

        :returns: This method is return frames of ``config_file``. **Frames** \
                are basically line of config file structure with python \
                typing ``Tuple``.
        :rtype: ``List[ConfigFrame]``
        """

        in_buffer = self.config_file.open("r")
        frames = []

        for line in in_buffer.readlines():
            words = shlex.split(line.rstrip("\n").rstrip("\r"))

            size = int(words[0])
            xhot = int(words[1]) - 1
            yhot = int(words[2]) - 1
            filename = words[3]
            if not Path(filename).is_absolute():
                filename = str(self.prefix / filename)

            if len(words) > 4:
                duration = int(words[4])
            else:
                duration = 0

            frames.append((size, xhot, yhot, filename, duration))

        in_buffer.close()
        return frames

    @staticmethod
    def frames_have_animation(frames: List[ConfigFrame]) -> bool:
        """Internal **static method** for checking passed ``config_file`` is \
                animated or not.

        :returns: ``True`` for animated and ``False`` for static.
        :rtype: ``bool``
        """

        sizes = set()
        for frame in frames:
            if frame[4] == 0:
                continue
            if frame[0] in sizes:
                return True
            sizes.add(frame[0])

        return False

    @staticmethod
    def make_framesets(frames: List[ConfigFrame]) -> List[List[ConfigFrame]]:
        """Internal **static method** for convert ``frames`` to ``framessets``.

        **framessets** are group of similar pixel sizes. Each **frameset** is \
                structured with python structure ``List``.

        :param frames: ``config_file`` lines with List & Tuple typing.
        :type frames: ``List[ConfigFrame]``

        :returns: Grouped frames in ``List`` structure.
        :rtype: ``List[List[ConfigFrame]]``

        :raise ValueError: If config_file lines are not sorted with pixel \
                size & frame number.
        :raise ValueError: If some frames are missing from pixel size inside \
                config_file.
        :raise ValueError: If frame's **animation durations** are not same \
                as other frame.
        """

        framesets: List[List[ConfigFrame]] = []
        sizes = set()

        # This assumes that frames are sorted
        size: int = 0
        counter: int = 0
        for i, frame in enumerate(frames):

            if size == 0 or frame[0] != size:
                counter = 0
                size = frame[0]

                if size in sizes:
                    raise ValueError(
                        f"Frames are not sorted: frame {i} has size {size}, but we have seen that already"
                    )

                sizes.add(size)

            if counter >= len(framesets):
                framesets.append([])

            framesets[counter].append(frame)
            counter += 1

        for i in range(1, len(framesets)):
            if len(framesets[i - 1]) != len(framesets[i]):
                raise ValueError(
                    f"Frameset {i} has size {len(framesets[i])}, expected {len(framesets[i - 1])}"
                )

        for frameset in framesets:
            for i in range(1, len(frameset)):
                if frameset[i - 1][4] != frameset[i][4]:
                    raise ValueError(
                        f"Frameset {i} has duration {int(frameset[i][4])} for framesize {int(frameset[i][0])}, but {int(frameset[i - 1][4])} for framesize {int(frameset[i - 1][0])}"
                    )
        framesets = sorted(framesets, reverse=True)

        return framesets

    @staticmethod
    def copy_to(out: Union[io.BytesIO, io.BufferedWriter], buf: io.BytesIO) -> None:
        """Internal **static method** for copy buffer value to another.

        :param out: Buffer where value copied.
        :type out: ``io.BytesIO`` or ``io.BufferedWriter``

        :param buf: input Buffer.
        :type buf: ``io.BytesIO``

        :returns: None.
        :rtype: ``None``
        """

        buf.seek(0, io.SEEK_SET)
        while True:
            b = buf.read(1024)
            if len(b) == 0:
                break
            out.write(b)

    def make_ani(
        self,
        frames: List[ConfigFrame],
        out_buffer: Union[io.BytesIO, io.BufferedWriter],
    ) -> None:
        """Generate `.ani` from config file's ``frames``.

        :param frames: List of ``config_file`` lines.
        :type frames: ``List[ConfigFrame]``

        :param out_buffer: Where `.ani` cursor data stored.
        :type out_buffer: ``io.BytesIO`` or ``io.BufferedWriter``

        :returns: None.
        :rtype: ``None``
        """

        framesets = self.make_framesets(frames)

        buf = io.BytesIO()

        buf.write(b"RIFF")
        riff_len_pos = buf.seek(0, io.SEEK_CUR)
        buf.write(pack("<I", 0))
        riff_len_start = buf.seek(0, io.SEEK_CUR)

        buf.write(b"ACON")
        buf.write(b"anih")
        buf.write(
            pack(
                "<IIIIIIIIII",
                36,
                36,
                len(framesets),
                len(framesets),
                0,
                0,
                32,
                1,
                int(framesets[0][0][4]),
                0x01,
            )
        )
        rates = {frameset[0][4] for frameset in framesets}
        if len(rates) != 1:
            buf.write(b"rate")
            buf.write(pack("<I", len(framesets) * 4))
            for frameset in framesets:
                buf.write(pack("<I", frameset[0][4]))

        buf.write(b"LIST")
        list_len_pos = buf.seek(0, io.SEEK_CUR)
        buf.write(pack("<I", 0))
        list_len_start = buf.seek(0, io.SEEK_CUR)

        buf.write(b"fram")

        for frameset in framesets:
            buf.write(b"icon")
            cur = self.make_cur(frameset, animated=True)
            cur_size = cur.seek(0, io.SEEK_END)
            # aligned_cur_size = cur_size
            # if cur_size % 4 != 0:
            #  aligned_cur_size += 4 - cur_size % 2
            buf.write(pack("<i", cur_size))
            self.copy_to(buf, cur)
            pos = buf.seek(0, io.SEEK_END)
            if pos % 2 != 0:
                buf.write(("\x00" * (2 - (pos % 2))).encode())

        end_at = buf.seek(0, io.SEEK_CUR)
        buf.seek(riff_len_pos, io.SEEK_SET)
        buf.write(pack("<I", end_at - riff_len_start))
        buf.seek(list_len_pos, io.SEEK_SET)
        buf.write(pack("<I", end_at - list_len_start))

        self.copy_to(out_buffer, buf)

    @staticmethod
    def shadowize(shadow: Image.Image, orig: Image.Image, color: Color) -> None:
        """Create shadow effect to the cursor.

        This effect is enable by providing ``options`` parameter \
        inside constructor

        :param shadow: PIL.Image.Image instance where shadowed image will stored.
        :type frames: ``PIL.Image.Image``

        :param orig: Cursor PIL.Image.Image instance frame.
        :type orig: ``PIL.Image.Image``

        :param color: Shadow color in ``Tuple`` structure.(RGBA format)
        :type color: ``Tuple[int, int, int, int]``

        :returns: None.
        :rtype: ``None``
        """

        o_pxs: Any = orig.load()
        s_pxs: Any = shadow.load()
        for y in range(orig.size[1]):
            for x in range(orig.size[0]):
                o_px = o_pxs[x, y]
                if o_px[3] > 0:
                    s_pxs[x, y] = (
                        int(color[0]),
                        int(color[1]),
                        int(color[2]),
                        int(color[3] * (o_px[3] / 255.0)),
                    )

    def create_shadow(self, orig: Image.Image) -> Tuple[int, Image.Image]:
        """Add shadows to Windows Cursor.

        This effect is enable by providing ``options`` parameter \
        inside constructor

        :param orig: Cursor PIL.Image.Image instance frame.
        :type orig: ``PIL.Image.Image``

        :returns: Tuple of code status and Image instance.
        :rtype: ``Tuple[int, PIL.Image.Image]``
        """

        blur_px = orig.size[0] / 100.0 * self.options.blur
        right_px = int(orig.size[0] / 100.0 * self.options.right_shift)
        down_px = int(orig.size[1] / 100.0 * self.options.down_shift)

        shadow = Image.new("RGBA", orig.size, (0, 0, 0, 0))
        self.shadowize(shadow, orig, self.options.color)
        shadow.load()

        if self.options.blur > 0:
            crop = (
                int(math.floor(-blur_px)),
                int(math.floor(-blur_px)),
                orig.size[0] + int(math.ceil(blur_px)),
                orig.size[1] + int(math.ceil(blur_px)),
            )
            right_px += int(math.floor(-blur_px))
            down_px += int(math.floor(-blur_px))
            shadow = shadow.crop(crop)
            flt = ImageFilter.GaussianBlur(blur_px)
            shadow = shadow.filter(flt)
        shadow.load()

        shadowed = Image.new("RGBA", orig.size, (0, 0, 0, 0))
        shadowed.paste(shadow, (right_px, down_px))
        shadowed.crop((0, 0, orig.size[0], orig.size[1]))
        shadowed = Image.alpha_composite(shadowed, orig)

        return (0, shadowed)

    @staticmethod
    def write_png(
        out: Union[io.BytesIO, io.BufferedWriter], frame_png: Image.Image
    ) -> None:
        """Write buffer value to PIL.Image.Image instance.

        :param out: Buffer of `.png` frame.
        :type out: ``io.BytesIO`` or ``io.BufferedWriter``

        :param frame_png: ``.png`` frame PIL.Image.Image instance.
        :type frame_png: ``PIL.Image.Image``

        :returns: None.
        :rtype: ``None``
        """

        frame_png.save(out, "png", optimize=True)

    @staticmethod
    def write_cur(
        out: Union[io.BytesIO, io.BufferedWriter],
        frame: ConfigFrame,
        frame_png: Image.Image,
    ) -> None:
        """Generate Windows Cursor data of single frame.

        :param out: Buffer of `.png` frame.
        :type out: ``io.BytesIO`` or ``io.BufferedWriter``

        :param frame: ``config_file`` lines.
        :type frame: ConfigFrame

        :param frame_png: ``.png`` frame PIL.Image.Image instance.
        :type frame_png: ``PIL.Image.Image``

        :returns: None.
        :rtype: ``None``
        """

        pixels: Any = frame_png.load()

        out.write(
            pack("<I II HH IIIIII", 40, frame[0], frame[0] * 2, 1, 32, 0, 0, 0, 0, 0, 0)
        )

        for y in reversed(list(range(frame[0]))):
            for x in range(frame[0]):
                pixel = pixels[x, y]
                out.write(pack("<BBBB", pixel[2], pixel[1], pixel[0], pixel[3]))

        acc = 0
        acc_pos = 0
        for y in reversed(list(range(frame[0]))):
            wrote = 0
            for x in range(frame[0]):
                if pixels[x, y][3] <= 127:
                    acc = acc | (1 << acc_pos)
                acc_pos += 1
                if acc_pos == 8:
                    acc_pos = 0
                    out.write(chr(acc).encode())
                    wrote += 1
            if wrote % 4 != 0:
                out.write(b"\x00" * (4 - wrote % 4))

    def make_cur(self, frames: List[ConfigFrame], animated: bool = False) -> io.BytesIO:
        """Generate `.cur` from config file's ``frames``.

        :param frames: List of ``config_file`` lines.
        :type frames: ``List[ConfigFrame]``

        :param animated: Enable for compression.
        :type animated: ``bool``

        :returns: Buffer of `.cur` typed cursor.
        :rtype: ``io.BytesIO``
        """

        buf = io.BytesIO()
        buf.write(pack("<HHH", 0, 2, len(frames)))
        frame_offsets = []

        frames = sorted(frames, reverse=True)

        for frame in frames:
            width = frame[0]
            if width > 255:
                width = 0
            height = width

            xhot = 0 if frame[1] == -1 else frame[1]
            yhot = 0 if frame[2] == -1 else frame[2]

            buf.write(pack("<BBBB HH", width, height, 0, 0, xhot, yhot))
            size_offset_pos = buf.seek(0, io.SEEK_CUR)

            buf.write(pack("<II", 0, 0))
            frame_offsets.append([size_offset_pos])

        for i, frame in enumerate(frames):
            frame_offset = buf.seek(0, io.SEEK_CUR)
            frame_offsets[i].append(frame_offset)

            frame_png = Image.open(frame[3])

            if self.options.add_shadows:
                succeeded, shadowed = self.create_shadow(frame_png)
                if succeeded == 0:
                    frame_png.close()
                    frame_png = shadowed

            #   Windows 10 fails to read PNG-compressed cursors for some reason
            #   and the information about storing PNG-compressed cursors is
            #   sparse. This is why PNG compression is not used.
            #   Previously this was conditional on cursor size (<= 48 to be uncompressed).
            compressed = False

            #   On the other hand, Windows 10 refuses to read very large
            #   uncompressed animated cursor files, but does accept
            #   PNG-compressed animated cursors for some reason. Go figure.
            if animated:
                compressed = True

            if compressed:
                self.write_png(buf, frame_png)
            else:
                self.write_cur(buf, frame, frame_png)

            frame_png.close()

            frame_end = buf.seek(0, io.SEEK_CUR)
            frame_offsets[i].append(frame_end - frame_offset)

        for frame_offset in frame_offsets:
            buf.seek(frame_offset[0])
            buf.write(pack("<II", frame_offset[2], frame_offset[1]))

        return buf

    def generate(self) -> None:
        """Generate Windows Cursor from ``config_file``.
        Automatically identify cursor type ``.ani`` or ``.cur``.

        :returns: None.
        :rtype: ``None``
        """

        frames = self.get_frames()
        is_animated = self.frames_have_animation(frames)

        name = self.config_file.stem
        ani_name = f"{name}.ani"
        cur_name = f"{name}.cur"

        cursor = ani_name if is_animated else cur_name
        self.out = self.out_dir / cursor

        # Remove Windows cursor, Which has the same 'name' inside 'output' directory.
        # This is useful for rebuilding the cursor to 'semi-animated'.
        # Remove only one extension can generate issues in the `WindowsPackager` module.
        remove_util(self.out_dir / ani_name)
        remove_util(self.out_dir / cur_name)

        with self.out.open("wb") as out:
            if is_animated:
                self.make_ani(frames, out)
            else:
                buf = self.make_cur(frames)
                self.copy_to(out, buf)

    @classmethod
    def create(cls, alias_file: Path, out_dir: Path, options=Options()) -> Path:
        """This method gives ability to generate ``Windows Cursor`` without \
        initiate the WindowsCursor object.

        :param alias_file: Cursor config file location.
        :type alias_file: ``pathlib.Path``

        :param out_dir: directory path where ``Windows Cursor`` generated.
        :type out_dir: ``pathlib.Path``

        :param options: ``anicursorgen`` commandline arguments.
        :type options: Options

        :returns: Generated ``Windows Cursor`` pathlib.Path object.
        :rtype: ``pathlib.Path``
        """

        cursor = cls(alias_file, out_dir, options)
        cursor.generate()
        return cursor.out

    @classmethod
    def from_bitmap(cls, **kwargs) -> Path:

        if "png" not in kwargs:
            raise KeyError("argument 'png' required")
        elif "hotspot" not in kwargs:
            raise KeyError("argument 'hotspot' required")
        elif "size" not in kwargs:
            raise KeyError("argument 'size' required")
        elif "canvas_size" not in kwargs:
            raise KeyError("argument 'canvas_size' required")
        elif "out_dir" not in kwargs:
            raise KeyError("argument 'out_dir' required")

        position: str
        if "position" in kwargs:
            position = kwargs["position"]
        else:
            position = "center"

        options: Options
        if "options" in kwargs:
            options = kwargs["options"]
        else:
            options = Options()

        with CursorAlias.from_bitmap(kwargs["png"], kwargs["hotspot"]) as alias:
            if alias.bitmap.animated:
                if "delay" not in kwargs:
                    raise KeyError("argument 'delay' required")
                else:
                    alias.create(kwargs["size"], kwargs["delay"])
                    alias.reproduce(
                        kwargs["size"], kwargs["canvas_size"], position, kwargs["delay"]
                    )
            else:
                alias.create(kwargs["size"])
                alias.reproduce(kwargs["size"], kwargs["canvas_size"], position)

            cursor = cls(alias.alias_file, kwargs["out_dir"], options)
            cursor.generate()
            return cursor.out
