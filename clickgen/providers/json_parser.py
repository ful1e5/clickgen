#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from typing import AnyStr, Tuple


class HotspotsParser:
    """ Parse json file,that contains the hotspots."""

    def __init__(self, f: AnyStr) -> None:
        data = open(f, "r")
        self.__hotspots = json.loads(data.read())

    def get_hotspots(self, c: str, old_size: int, new_size: int) -> Tuple[int, int]:
        xhot = yhot = int(new_size / 2)

        x = self.__hotspots[c]["xhot"]
        y = self.__hotspots[c]["yhot"]

        if x:
            xhot = x
        else:
            xhot = round(old_size / new_size * x)

        if y:
            yhot = y
        else:
            yhot = round(old_size / new_size * y)

        return (xhot, yhot)
