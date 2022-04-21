#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Optional, Tuple, Type, Union

from clickgen.parser.base import BaseParser
from clickgen.parser.png import MultiPNGParser, SinglePNGParser

__all__ = ["SinglePNGParser", "MultiPNGParser", "open_blob"]

PARSERS: List[Type[BaseParser]] = [SinglePNGParser, MultiPNGParser]


def open_blob(
    blob: Union[bytes, List[bytes]],
    hotspot: Tuple[int, int],
    sizes: Optional[List[int]] = None,
    delay: Optional[int] = None,
) -> BaseParser:
    for parser in PARSERS:
        if parser.can_parse(blob):
            return parser(blob, hotspot, sizes, delay)  # type: ignore
    raise ValueError("Unsupported file format")
