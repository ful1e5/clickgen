from _typeshed import Incomplete
from clickgen.cursors import CursorFrame as CursorFrame, CursorImage as CursorImage
from clickgen.parser.base import BaseParser as BaseParser

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
    def __init__(self, blob: bytes, hotspot: tuple[int, int], sizes: list[int | str] | None = None, delay: int | None = None) -> None: ...

class MultiPNGParser(BaseParser):
    @classmethod
    def can_parse(cls, blobs: list[bytes]) -> bool: ...
    frames: Incomplete
    def __init__(self, blobs: list[bytes], hotspot: tuple[int, int], sizes: list[int | str] | None = None, delay: int | None = None) -> None: ...
