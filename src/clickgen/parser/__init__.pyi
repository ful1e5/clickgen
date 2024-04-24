from clickgen.parser.base import BaseParser
from clickgen.parser.png import MultiPNGParser as MultiPNGParser, SinglePNGParser as SinglePNGParser
from typing import List, Tuple

__all__ = ['SinglePNGParser', 'MultiPNGParser', 'open_blob']

def open_blob(blob: bytes | List[bytes], hotspot: Tuple[int, int], sizes: List[int] | None = None, delay: int | None = None) -> BaseParser: ...
