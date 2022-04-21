from clickgen.parser.base import BaseParser
from clickgen.parser.png import MultiPNGParser as MultiPNGParser, SinglePNGParser as SinglePNGParser
from typing import List, Optional, Tuple, Union

def open_blob(blob: Union[bytes, List[bytes]], hotspot: Tuple[int, int], sizes: Optional[List[int]] = ..., delay: Optional[int] = ...) -> BaseParser: ...
