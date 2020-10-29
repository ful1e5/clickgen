#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import Dict, Tuple

# typing
Hotspots = Dict[str, Dict[str, int]]


class HotspotsParser:
    """ Parse json file,that contains the hotspots."""

    __hotspots: Hotspots = {}

    def __init__(self, hotspots: Hotspots) -> None:
        self.__hotspots = hotspots

    def get_hotspots(
        self, c: str, old_size: Tuple[int, int], new_size: int
    ) -> Tuple[int, int]:

        x = self.__hotspots[c]["xhot"]
        y = self.__hotspots[c]["yhot"]
        (width, height) = old_size

        if x is None or y is None:
            xhot = yhot = int(new_size / 2)
        else:
            xhot = int(round(new_size / width * x))
            yhot = int(round(new_size / height * y))

        return (xhot, yhot)
