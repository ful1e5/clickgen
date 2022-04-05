from typing import Any, List, Optional, Tuple
from wxcursors.parser.base import BaseParser

SIZES: Any
DELAY: int

class SinglePNGParser(BaseParser):
    MAGIC: Any
    @classmethod
    def can_parse(cls, blob: bytes) -> bool: ...
    sizes: Any
    delay: Any
    hotspot: Any
    frames: Any
    def __init__(self, blob: bytes, hotspot: Tuple[int, int], sizes: Optional[List[int]] = ..., delay: Optional[int] = ...) -> None: ...

class MultiPNGParser(BaseParser):
    @classmethod
    def can_parse(cls, blobs: List[bytes]) -> bool: ...
    frames: Any
    def __init__(self, blobs: List[bytes], hotspot: Tuple[int, int], sizes: Optional[List[int]] = ..., delay: Optional[int] = ...) -> None: ...
