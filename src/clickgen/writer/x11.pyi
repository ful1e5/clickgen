from typing import Any, List
from wxcursors.cursors import CursorFrame as CursorFrame

MAGIC: bytes
VERSION: int
FILE_HEADER: Any
TOC_CHUNK: Any
CHUNK_IMAGE: int
IMAGE_HEADER: Any

def to_x11(frames: List[CursorFrame]) -> bytes: ...
