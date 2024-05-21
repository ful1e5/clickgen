from clickgen.parser.base import BaseParser
from clickgen.parser.png import MultiPNGParser as MultiPNGParser, SinglePNGParser as SinglePNGParser

__all__ = ['SinglePNGParser', 'MultiPNGParser', 'open_blob']

def open_blob(blob: bytes | list[bytes], hotspot: tuple[int, int], sizes: list[int] | None = None, delay: int | None = None) -> BaseParser: ...
