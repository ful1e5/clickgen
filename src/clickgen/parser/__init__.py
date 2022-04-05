from typing import List, Optional, Tuple, Union

from wxcursors.parser.base import BaseParser
from wxcursors.parser.png import MultiPNGParser, SinglePNGParser

__all__ = ["SinglePNGParser", "MultiPNGParser", "open_blob"]

PARSERS = [SinglePNGParser, MultiPNGParser]


def open_blob(
    blob: Union[bytes, List[bytes]],
    hotspot: Tuple[int, int],
    sizes: Optional[List[int]] = None,
    delay: Optional[int] = None,
) -> BaseParser:
    for parser in PARSERS:
        if parser.can_parse(blob):
            return parser(blob, hotspot, sizes, delay)
    raise ValueError("Unsupported file format")
