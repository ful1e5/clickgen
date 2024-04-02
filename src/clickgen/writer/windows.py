#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
from io import BytesIO
from itertools import chain
from typing import List, Tuple

from PIL import Image

from clickgen.cursors import CursorFrame

# .CUR FILE FORMAT
MAGIC = b"\0\0\02\0"
ICO_TYPE_CUR = 2
ICON_DIR = struct.Struct("<HHH")
ICON_DIR_ENTRY = struct.Struct("<BBBBHHII")


def to_cur(frame: CursorFrame) -> bytes:
    header = ICON_DIR.pack(0, ICO_TYPE_CUR, len(frame))
    directory: List[bytes] = []
    image_data: List[bytes] = []
    offset = ICON_DIR.size + len(frame) * ICON_DIR_ENTRY.size

    for image in frame:
        clone = image.image.copy()
        width, height = clone.size
        if width > 256 or height > 256:
            raise ValueError(f"Image too big for CUR format: {width}x{height}")

        # Place cursor image in 32x32 canvas if png is smaller.
        # Otherwise Cursors looks blurry
        blob = BytesIO()
        if width <= 32 or height <= 32:
            canvas = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
            canvas.paste(clone, (0, 0))
            canvas.save(blob, "PNG")
        else:
            image.image.save(blob, "PNG")

        blob.seek(0)
        image_data.append(blob.read())
        x_offset, y_offset = image.hotspot
        directory.append(
            ICON_DIR_ENTRY.pack(
                height & 0xFF,
                height & 0xFF,
                0,
                0,
                x_offset,
                y_offset,
                blob.getbuffer().nbytes,
                offset,
            )
        )
        offset += blob.getbuffer().nbytes

    return b"".join(chain([header], directory, image_data))


# .ANI FILE FORMAT
SIGNATURE = b"RIFF"
ANI_TYPE = b"ACON"
HEADER_CHUNK = b"anih"
LIST_CHUNK = b"LIST"
SEQ_CHUNK = b"seq "
RATE_CHUNK = b"rate"
FRAME_TYPE = b"fram"
ICON_CHUNK = b"icon"
RIFF_HEADER = struct.Struct("<4sI4s")
CHUNK_HEADER = struct.Struct("<4sI")
ANIH_HEADER = struct.Struct("<IIIIIIIII")
UNSIGNED = struct.Struct("<I")
SEQUENCE_FLAG = 0x2
ICON_FLAG = 0x1


def get_ani_cur_list(frames: List[CursorFrame]) -> bytes:
    io = BytesIO()
    for frame in frames:
        cur_file = to_cur(frame)
        io.write(CHUNK_HEADER.pack(ICON_CHUNK, len(cur_file)))
        io.write(cur_file)
        if len(cur_file) & 1:
            io.write(b"\0")
    return io.getvalue()


def get_ani_rate_chunk(frames: List[CursorFrame]) -> bytes:
    io = BytesIO()
    io.write(CHUNK_HEADER.pack(RATE_CHUNK, UNSIGNED.size * len(frames)))
    for frame in frames:
        io.write(UNSIGNED.pack(int(round(frame.delay * 2))))
    return io.getvalue()


def to_ani(frames: List[CursorFrame]) -> bytes:
    ani_header = ANIH_HEADER.pack(
        ANIH_HEADER.size, len(frames), len(frames), 0, 0, 32, 1, 1, ICON_FLAG
    )

    cur_list = get_ani_cur_list(frames)
    chunks = [
        CHUNK_HEADER.pack(HEADER_CHUNK, len(ani_header)),
        ani_header,
        RIFF_HEADER.pack(LIST_CHUNK, len(cur_list) + 4, FRAME_TYPE),
        cur_list,
        get_ani_rate_chunk(frames),
    ]
    body = b"".join(chunks)
    riff_header: bytes = RIFF_HEADER.pack(SIGNATURE, len(body) + 4, ANI_TYPE)
    return riff_header + body


def to_win(frames: List[CursorFrame]) -> Tuple[str, bytes]:
    if len(frames) == 1:
        return ".cur", to_cur(frames[0])
    else:
        return ".ani", to_ani(frames)
