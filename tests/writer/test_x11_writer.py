import struct
from typing import Any, List, Tuple

from clickgen.writer.x11 import to_x11

# Helpers
MAGIC = b"Xcur"
VERSION = 0x1_0000
FILE_HEADER = struct.Struct("<4sIII")
TOC_CHUNK = struct.Struct("<III")
CHUNK_IMAGE = 0xFFFD0002
IMAGE_HEADER = struct.Struct("<IIIIIIIII")


def _unpack(blob, struct_cls: struct.Struct, offset: int) -> Tuple[Any, ...]:
    return struct_cls.unpack(blob[offset : offset + struct_cls.size])


def test_static_xcursor_file_formate(cursor_frame):
    blob = to_x11([cursor_frame])

    assert isinstance(blob, bytes)

    magic, header_size, version, toc_size = _unpack(blob, FILE_HEADER, 0)

    assert magic == MAGIC
    assert version == VERSION

    offset = FILE_HEADER.size
    chunks: List[Tuple[int, int, int]] = []
    for _ in range(toc_size):
        chunk_type, chunk_subtype, position = _unpack(blob, TOC_CHUNK, offset)
        chunks.append((chunk_type, chunk_subtype, position))
        offset += TOC_CHUNK.size

    for chunk_type, chunk_subtype, position in chunks:
        if chunk_type != CHUNK_IMAGE:
            continue

        (
            size,
            actual_type,
            nominal_size,
            version,
            width,
            height,
            x_offset,
            y_offset,
            delay,
        ) = _unpack(blob, IMAGE_HEADER, position)
        delay /= 1000

        assert size == IMAGE_HEADER.size

        assert actual_type == chunk_type

        assert nominal_size == chunk_subtype
        assert nominal_size == 24

        assert width < 0x7FFF
        assert width == 200
        assert height < 0x7FFF
        assert height == 200

        assert x_offset < width
        assert x_offset == 100

        assert y_offset < height
        assert y_offset == 105

        image_start = position + IMAGE_HEADER.size
        image_size = width * height * 4
        new_blob = blob[image_start : image_start + image_size]
        assert len(new_blob) == image_size
