from _typeshed import Incomplete
from clickgen.cursors import CursorFrame as CursorFrame
from typing import List

MAGIC: bytes
VERSION: int
FILE_HEADER: Incomplete
TOC_CHUNK: Incomplete
CHUNK_IMAGE: int
IMAGE_HEADER: Incomplete

def premultiply_alpha(source: bytes) -> bytes: ...
def to_x11(frames: List[CursorFrame]) -> bytes: ...
