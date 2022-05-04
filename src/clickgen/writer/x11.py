#!/usr/bin/env python
# -*- coding: utf-8 -*-

import struct
from itertools import chain
from operator import itemgetter
from typing import List

from clickgen.cursors import CursorFrame

# XCURSOR FILE FORMAT
MAGIC = b"Xcur"
VERSION = 0x1_0000
FILE_HEADER = struct.Struct("<4sIII")
TOC_CHUNK = struct.Struct("<III")
CHUNK_IMAGE = 0xFFFD0002
IMAGE_HEADER = struct.Struct("<IIIIIIIII")


def to_x11(frames: List[CursorFrame]) -> bytes:
    chunks = []

    for frame in frames:
        for cursor in frame:
            hx, hy = cursor.hotspot
            header = IMAGE_HEADER.pack(
                IMAGE_HEADER.size,
                CHUNK_IMAGE,
                cursor.nominal,
                1,
                cursor.image.width,
                cursor.image.height,
                hx,
                hy,
                int(frame.delay),
            )
            chunks.append(
                (
                    CHUNK_IMAGE,
                    cursor.nominal,
                    header + cursor.image.tobytes("raw", "BGRA"),
                )
            )

    header = FILE_HEADER.pack(
        MAGIC,
        FILE_HEADER.size,
        VERSION,
        len(chunks),
    )

    offset = FILE_HEADER.size + len(chunks) * TOC_CHUNK.size
    toc = []
    for chunk_type, chunk_subtype, chunk in chunks:
        toc.append(
            TOC_CHUNK.pack(
                chunk_type,
                chunk_subtype,
                offset,
            )
        )
        offset += len(chunk)

    return b"".join(chain([header], toc, map(itemgetter(2), chunks)))
