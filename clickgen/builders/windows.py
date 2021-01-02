#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import math
import shlex
import struct
import sys
from io import BufferedReader, BufferedWriter, BytesIO
from os import makedirs, path, remove
from pathlib import Path
from typing import Any, List, Literal, NamedTuple, Optional, Tuple

from PIL import Image, ImageFilter

p = struct.pack


class AnicursorgenArgs(NamedTuple):
    """
    Structure `anicursorgen.py` CLI arguments.

    @add_shadow : Do not generate shadows for cursors (assign False to cancel its effect).

    @blur: Blur radius, in percentage of the canvas size (default is 3.125, set to 0 to disable blurring).

    @color: Shadow color in (RR,GG,BB,AA) form (default is (0, 0, 0, 64)).

    @down_shift: Shift shadow down by this percentage of the canvas size (default is 3.125).

    @right_shift: Shift shadow right by this percentage of the canvas size (default is 9.375).
    """

    add_shadows: bool = False
    blur: float = 3.125
    color: Tuple[int, int, int, int] = (
        0,
        0,
        0,
        64,
    )
    down_shift: float = 3.125
    right_shift: float = 9.375


class WindowsCursor:
    """
    Build Windows cursors from `.in` configs files. Code inspiration from `anicursorgen.py`.
    https://github.com/ubuntu/yaru/blob/master/icons/src/cursors/anicursorgen.py
    """

    config_file: Path = Path()
    out_dir: Path = Path()
    prefix: Path = Path()
    out: Path = Path()

    def __init__(self, config_dir: Path, out_dir: Path) -> None:
        self.config_file = config_dir
        self.prefix = config_dir.parent
        stem = self.config_file.stem

        self.out_dir = out_dir
        if not self.out_dir.exists():
            makedirs(self.out_dir)

        # Determine cursor extension
        self.out = self.out_dir / f"{stem}.cur"
        with self.config_file.open() as f:
            line = f.readline()
            words = shlex.split(line.rstrip("\n").rstrip("\r"))
            if len(words) > 4:
                self.out = self.out_dir / f"{stem}.ani"

    @staticmethod
    def parse_config_from(
        in_buffer: BufferedReader, prefix: str
    ) -> List[Tuple[int, int, int, str, int]]:
        frames: List[Tuple[int, int, int, str, int]] = []

        for line in in_buffer.readlines():
            line = line.decode()
            words = shlex.split(line.rstrip("\n").rstrip("\r"))
            if len(words) < 4:
                continue

            size = int(words[0])
            xhot = int(words[1]) - 1
            yhot = int(words[2]) - 1
            filename = words[3]
            if not path.isabs(filename):
                filename = path.join(prefix, filename)

            if len(words) > 4:
                duration = int(words[4])
            else:
                duration = 0

            frames.append((size, xhot, yhot, filename, duration))

        return frames

    @staticmethod
    def frames_have_animation(frames: List[Tuple[int, int, int, str, int]]) -> bool:
        sizes = set()
        for frame in frames:
            if frame[4] == 0:
                continue
            if frame[0] in sizes:
                return True
            sizes.add(frame[0])

        return False

    @staticmethod
    def make_framesets(frames: List[Any]) -> Optional[List[Any]]:
        framesets: List[Any] = []
        sizes = set()

        # This assumes that frames are sorted
        size = counter = 0
        for i, frame in enumerate(frames):

            if size == 0 or frame[0] != size:
                counter = 0
                size = frame[0]

                if size in sizes:
                    print(
                        f"Frames are not sorted: frame {i} has size {size}, but we have seen that already",
                        file=sys.stderr,
                    )
                    return None

                sizes.add(size)

            if counter >= len(framesets):
                framesets.append([])

            framesets[counter].append(frame)
            counter += 1

        for i in range(1, len(framesets)):
            if len(framesets[i - 1]) != len(framesets[i]):
                print(
                    f"Frameset {i} has size {len(framesets[i])}, expected {len(framesets[i - 1])}",
                    file=sys.stderr,
                )
                return None

        for frameset in framesets:
            for i in range(1, len(frameset)):
                if frameset[i - 1][4] != frameset[i][4]:
                    print(
                        f"Frameset {i} has duration {int(frameset[i][4])} for framesize {int(frameset[i][0])}, but {int(frameset[i - 1][4])} for framesize {int(frameset[i - 1][0])}",
                        file=sys.stderr,
                    )
                    return None
        framesets = sorted(framesets, reverse=True)

        return framesets

    @staticmethod
    def copy_to(out: Any, buf: BytesIO) -> None:
        buf.seek(0, io.SEEK_SET)
        while True:
            b = buf.read(1024)
            if len(b) == 0:
                break
            out.write(b)

    def make_ani(
        self,
        frames: List[Tuple[int, int, int, str, int]],
        out_buffer: BufferedWriter,
        args: AnicursorgenArgs,
    ) -> Literal[0, 1]:
        framesets = self.make_framesets(frames)

        if framesets is None:
            return 1

        buf = io.BytesIO()

        buf.write(b"RIFF")
        riff_len_pos = buf.seek(0, io.SEEK_CUR)
        buf.write(p("<I", 0))
        riff_len_start = buf.seek(0, io.SEEK_CUR)

        buf.write(b"ACON")
        buf.write(b"anih")
        buf.write(
            p(
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
            buf.write(p("<I", len(framesets) * 4))
            for frameset in framesets:
                buf.write(p("<I", int(frameset[0][4])))

        buf.write(b"LIST")
        list_len_pos = buf.seek(0, io.SEEK_CUR)
        buf.write(p("<I", 0))
        list_len_start = buf.seek(0, io.SEEK_CUR)

        buf.write(b"fram")

        for frameset in framesets:
            buf.write(b"icon")
            cur = self.make_cur(frameset, args, animated=True)
            cur_size = cur.seek(0, io.SEEK_END)
            # aligned_cur_size = cur_size
            # if cur_size % 4 != 0:
            #  aligned_cur_size += 4 - cur_size % 2
            buf.write(p("<i", cur_size))
            self.copy_to(buf, cur)
            pos = buf.seek(0, io.SEEK_END)
            if pos % 2 != 0:
                buf.write(("\x00" * (2 - (pos % 2))).encode())

        end_at = buf.seek(0, io.SEEK_CUR)
        buf.seek(riff_len_pos, io.SEEK_SET)
        buf.write(p("<I", end_at - riff_len_start))
        buf.seek(list_len_pos, io.SEEK_SET)
        buf.write(p("<I", end_at - list_len_start))

        self.copy_to(out_buffer, buf)

        return 0

    @staticmethod
    def shadowize(shadow: Image, orig, color) -> None:
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

    def create_shadow(
        self, orig: Any, args: AnicursorgenArgs
    ) -> Tuple[Literal[0], Any]:
        blur_px = orig.size[0] / 100.0 * args.blur
        right_px = int(orig.size[0] / 100.0 * args.right_shift)
        down_px = int(orig.size[1] / 100.0 * args.down_shift)

        shadow = Image.new("RGBA", orig.size, (0, 0, 0, 0))
        self.shadowize(shadow, orig, args.color)
        shadow.load()

        if args.blur > 0:
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
        shadowed: Image = Image.alpha_composite(shadowed, orig)

        return (0, shadowed)

    @staticmethod
    def write_png(out: Any, frame_png: Any) -> None:
        frame_png.save(out, "png", optimize=True)

    @staticmethod
    def write_cur(out: Any, frame: Any, frame_png: Any) -> None:
        pixels = frame_png.load()

        out.write(
            p("<I II HH IIIIII", 40, frame[0], frame[0] * 2, 1, 32, 0, 0, 0, 0, 0, 0)
        )

        for y in reversed(list(range(frame[0]))):
            for x in range(frame[0]):
                pixel = pixels[x, y]
                out.write(p("<BBBB", pixel[2], pixel[1], pixel[0], pixel[3]))

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

    def make_cur(
        self, frames: List[Any], args: AnicursorgenArgs, animated: bool = False
    ) -> BytesIO:
        buf = io.BytesIO()
        buf.write(p("<HHH", 0, 2, len(frames)))
        frame_offsets = []

        frames = sorted(frames, reverse=True)

        for frame in frames:
            width = frame[0]
            if width > 255:
                width = 0
            height = width

            a = 0 if frame[1] == -1 else frame[1]
            b = 0 if frame[2] == -1 else frame[2]

            buf.write(p("<BBBB HH", width, height, 0, 0, a, b))
            size_offset_pos = buf.seek(0, io.SEEK_CUR)

            buf.write(p("<II", 0, 0))
            frame_offsets.append([size_offset_pos])

        for i, frame in enumerate(frames):
            frame_offset = buf.seek(0, io.SEEK_CUR)
            frame_offsets[i].append(frame_offset)

            frame_png = Image.open(frame[3])

            if args.add_shadows:
                succeeded, shadowed = self.create_shadow(frame_png, args)
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
            buf.write(p("<II", frame_offset[2], frame_offset[1]))

        return buf

    def make_cursor_from(
        self,
        in_buffer: BufferedReader,
        out_buffer: BufferedWriter,
        args: AnicursorgenArgs,
    ) -> Literal[0, 1]:

        exec_code: Literal[0, 1] = 0
        frames = self.parse_config_from(in_buffer, prefix=self.prefix.absolute())

        animated = self.frames_have_animation(frames)

        if animated:
            exec_code = self.make_ani(frames, out_buffer, args)
        else:
            buf = self.make_cur(frames, args)
            self.copy_to(out_buffer, buf)

        return exec_code

    def anicursorgen(self, args: AnicursorgenArgs) -> Literal[0, 1]:

        in_cfg_buffer = self.config_file.open(mode="rb")

        # remove old cursor file
        if self.out.exists():
            remove(self.out)

        out_buffer = self.out.open(mode="wb")
        exec_code = self.make_cursor_from(in_cfg_buffer, out_buffer, args)

        in_cfg_buffer.close()
        out_buffer.close()

        return exec_code

    def generate(self, args: AnicursorgenArgs = AnicursorgenArgs()) -> None:

        exec_code = self.anicursorgen(args)
        if exec_code == 1:
            raise Exception(
                f"'{self.__class__.__name__}' can't genrate Windows cursor from {self.config_file.name}"
            )

    @classmethod
    def build_from(cls, alias_file: Path, out_dir: Path) -> Path:
        builder: WindowsCursor = cls(alias_file, out_dir)
        builder.generate()
        return builder.out
