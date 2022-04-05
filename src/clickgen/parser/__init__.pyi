from typing import List, Optional, Tuple, Union
from wxcursors.parser.base import BaseParser
from wxcursors.parser.png import MultiPNGParser as MultiPNGParser, SinglePNGParser as SinglePNGParser

def open_blob(blob: Union[bytes, List[bytes]], hotspot: Tuple[int, int], sizes: Optional[List[int]] = ..., delay: Optional[int] = ...) -> BaseParser: ...
