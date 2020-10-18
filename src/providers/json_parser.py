#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import AnyStr, Tuple


class HotspotsParser:
    """ Parse json file,that contains the hotspots."""

    def __init__(self, f: AnyStr) -> None:
        data = open(f, "r")
        self.__hotspots = json.loads(data.read())

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
