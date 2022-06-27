from _typeshed import Incomplete
from clickgen.cursors import CursorFrame as CursorFrame, CursorImage as CursorImage
from clickgen.parser.base import BaseParser as BaseParser
from typing import List, Optional, Tuple

SIZES: Incomplete
DELAY: int

class SinglePNGParser(BaseParser):
    MAGIC: Incomplete
    @classmethod
    def can_parse(cls, blob: bytes) -> bool: ...
    sizes: Incomplete
    delay: Incomplete
    hotspot: Incomplete
    frames: Incomplete
    def __init__(self, blob: bytes, hotspot: Tuple[int, int], sizes: Optional[List[int]] = ..., delay: Optional[int] = ...) -> None: ...

class MultiPNGParser(BaseParser):
    @classmethod
    def can_parse(cls, blobs: List[bytes]) -> bool: ...
    frames: Incomplete
    def __init__(self, blobs: List[bytes], hotspot: Tuple[int, int], sizes: Optional[List[int]] = ..., delay: Optional[int] = ...) -> None: ...
