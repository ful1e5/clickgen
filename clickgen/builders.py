#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ctypes
import io
import math
import shlex
from ctypes import CDLL
from pathlib import Path
from struct import pack
from typing import Any, List, Literal, NamedTuple, Tuple

from PIL import Image, ImageFilter

from clickgen import __path__ as clickgen_pkg_root
from clickgen.util import remove_util

# Typings
Frame = Tuple[int, int, int, str, int]
Frames = List[Frame]
Color = Tuple[int, int, int, int]


class XCursor:
    """
    Build `XCursor` from the `.in` config file. This class is using `xcursorgen` internally.
    """

    config_file: Path
    prefix: Path
    out_dir: Path
    out: Path

    # main function ctypes define
    _lib_location: Path = Path(clickgen_pkg_root[0]) / "xcursorgen.so"
    _lib: CDLL = CDLL(_lib_location)
    _LP_c_char = ctypes.POINTER(ctypes.c_char)
    _LP_LP_c_char = ctypes.POINTER(_LP_c_char)
    _lib.main.argtypes = (ctypes.c_int, _LP_LP_c_char)

    def __init__(self, config_file: Path, out_dir: Path) -> None:
        if not config_file.exists() or not config_file.is_file():
            raise FileNotFoundError(
                f"'{config_file.name}' is not found or not a config file"
            )

        self.config_file: Path = config_file
        self.prefix: Path = config_file.parent

        self.out_dir: Path = out_dir / "cursors"

        self.out_dir.mkdir(parents=True, exist_ok=True)

        self.out: Path = self.out_dir / self.config_file.stem

    def gen_argv_ctypes(self, argv: List[str]) -> Any:
        """ Convert `string` arguments to `ctypes` pointer. """
        p = (self._LP_c_char * len(argv))()

        for i, arg in enumerate(argv):
            enc_arg: bytes = str(arg).encode("utf-8")
            p[i] = ctypes.create_string_buffer(enc_arg)

        return ctypes.cast(p, self._LP_LP_c_char)

    def generate(self) -> None:
        """ Generate x11 cursor from `.in` file."""

        # remove old cursor file
        remove_util(self.out)

        argv: List[str] = [
            "xcursorgen",
            "-p",  # prefix args for xcursorgen (do not remove)
            self.prefix.absolute(),  # prefix args for xcursorgen (do not remove)
            self.config_file.absolute(),  # cursor's config/alias file
            self.out.absolute(),  # xcursor/output path
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
        cursor = cls(alias_file, out_dir)
        cursor.generate()
        return cursor.out


class AnicursorgenArgs(NamedTuple):
    """
    Structure `anicursorgen.py` CLI arguments.

    @add_shadow : Do not generate shadows for cursors (assign False to cancel its effect).

    @blur: Blur radius, in percentage of the canvas size (default is 3.125, set to 0 to disable blurring).

    @color: Shadow color in (RR,GG,BB,AA) (default is (0, 0, 0, 64)).

    @down_shift: Shift shadow down by this percentage of the canvas size (default is 3.125).

    @right_shift: Shift shadow right by this percentage of the canvas size (default is 9.375).
    """

    add_shadows: bool = False
    blur: float = 3.125
    color: Color = (0, 0, 0, 64)
    down_shift: float = 3.125
    right_shift: float = 9.375


class WindowsCursor:
    """
    Build Windows cursors from `.in` configs files. Code inspiration from `anicursorgen.py`.

    anicursorgen

    https://github.com/ubuntu/yaru/blob/master/icons/src/cursors/anicursorgen.py

    Copyright (C) 2015 Руслан Ижбулатов <lrn1986@gmail.com>

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

    args: AnicursorgenArgs
    config_file: Path
    prefix: Path
    out_dir: Path
    out: Path

    def __init__(self, config_dir: Path, out_dir: Path, args: AnicursorgenArgs) -> None:
        self.config_file = config_dir
        self.prefix = config_dir.parent
        self.out_dir = out_dir
        self.args = args

        self.out_dir.mkdir(exist_ok=True, parents=True)

    def get_frames(self) -> Frames:
        in_buffer = self.config_file.open("rb")
        frames: Frames = []

        for line in in_buffer.readlines():
            line = line.decode()
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
    def frames_have_animation(frames: Frames) -> bool:
        sizes = set()
        for frame in frames:
            if frame[4] == 0:
                continue
            if frame[0] in sizes:
                return True
            sizes.add(frame[0])

        return False

    @staticmethod
    def make_framesets(frames: Frames) -> Frames:
        framesets: Frames = []
        sizes = set()

        # This assumes that frames are sorted
        size = counter = 0
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
                        f"Frameset {i} has duration {int(frameset[i][4])} for framesize {int(frameset[i][0])}, but {int(frameset[i - 1][4])} for framesize {int(frameset[i - 1][0])}",
                    )
        framesets = sorted(framesets, reverse=True)

        return framesets

    @staticmethod
    def copy_to(out: io.BufferedWriter, buf: io.BytesIO) -> None:
        buf.seek(0, io.SEEK_SET)
        while True:
            b = buf.read(1024)
            if len(b) == 0:
                break
            out.write(b)

    def make_ani(
        self,
        frames: Frames,
        out_buffer: io.BufferedWriter,
    ) -> None:
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

        rates = set()
        for frameset in framesets:
            rates.add(int(frameset[0][4]))

        if len(rates) != 1:
            buf.write(b"rate")
            buf.write(pack("<I", len(framesets) * 4))
            for frameset in framesets:
                buf.write(pack("<I", int(frameset[0][4])))

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
    def shadowize(shadow: Image, orig: Image, color: Color) -> None:
        o_pxs = orig.load()
        s_pxs = shadow.load()
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

    def create_shadow(self, orig: Image) -> Tuple[Literal[0], Any]:
        blur_px = orig.size[0] / 100.0 * self.args.blur
        right_px = int(orig.size[0] / 100.0 * self.args.right_shift)
        down_px = int(orig.size[1] / 100.0 * self.args.down_shift)

        shadow = Image.new("RGBA", orig.size, (0, 0, 0, 0))
        self.shadowize(shadow, orig, self.args.color)
        shadow.load()

        if self.args.blur > 0:
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

        shadowed: Image = Image.new("RGBA", orig.size, (0, 0, 0, 0))
        shadowed.paste(shadow, (right_px, down_px))
        shadowed.crop((0, 0, orig.size[0], orig.size[1]))
        shadowed = Image.alpha_composite(shadowed, orig)

        return (0, shadowed)

    @staticmethod
    def write_png(out: io.BufferedWriter, frame_png: Image) -> None:
        frame_png.save(out, "png", optimize=True)

    @staticmethod
    def write_cur(out: io.BufferedWriter, frame: Frame, frame_png: Image) -> None:
        pixels = frame_png.load()

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

    def make_cur(self, frames: Frames, animated: bool = False) -> io.BytesIO:
        buf = io.BytesIO()
        buf.write(pack("<HHH", 0, 2, len(frames)))
        frame_offsets = []

        frames = sorted(frames, reverse=True)

        for frame in frames:
            width = frame[0]
            if width > 255:
                width = 0
            height = width

            a = 0 if frame[1] == -1 else frame[1]
            b = 0 if frame[2] == -1 else frame[2]

            buf.write(pack("<BBBB HH", width, height, 0, 0, a, b))
            size_offset_pos = buf.seek(0, io.SEEK_CUR)

            buf.write(pack("<II", 0, 0))
            frame_offsets.append([size_offset_pos])

        for i, frame in enumerate(frames):
            frame_offset = buf.seek(0, io.SEEK_CUR)
            frame_offsets[i].append(frame_offset)

            frame_png = Image.open(frame[3])

            if self.args.add_shadows:
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
        frames = self.get_frames()
        animated = self.frames_have_animation(frames)

        name = self.config_file.stem
        ani_name = f"{name}.ani"
        cur_name = f"{name}.cur"

        cursor = ani_name if animated else cur_name
        self.out = self.out_dir / cursor

        # Remove Windows cursor, Which has the same 'name' inside 'output' directory.
        # This is useful for rebuilding the cursor to 'semi-animated'.
        # Remove only one extension can generate issues in the `WindowsPackager` module.
        remove_util(self.out_dir / ani_name)
        remove_util(self.out_dir / cur_name)

        if animated:
            with self.out.open("wb") as out:
                self.make_ani(frames, out)
        else:
            with self.out.open("wb") as out:
                buf = self.make_cur(frames)
                self.copy_to(out, buf)

    @classmethod
    def create(cls, alias_file: Path, out_dir: Path, args=AnicursorgenArgs()) -> Path:
        cursor = cls(alias_file, out_dir, args)
        cursor.generate()
        return cursor.out
