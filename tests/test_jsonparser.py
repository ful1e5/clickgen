#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple
from unittest.mock import PropertyMock, patch

import pytest

from clickgen.providers.jsonparser import Hotspots, HotspotsParser


@pytest.fixture
def hotspots() -> Hotspots:
    return {"a": {"xhot": 20, "yhot": 50}, "b": {"xhot": 88, "yhot": 42}}


def test_hotspots_parser(hotspots) -> None:
    with patch.object(
        HotspotsParser, "_HotspotsParser__hotspots", new_callable=PropertyMock
    ) as mock_hotspots:
        h = HotspotsParser(mock_hotspots)

        mock_hotspots.return_value = hotspots
        assert hotspots == h._HotspotsParser__hotspots


testdata: List[Tuple[str, Tuple[int, int], int, int, int]] = [
    ("a", (200, 200), 22, 2, 6),
    ("a", (200, 200), 24, 2, 6),
    ("a", (200, 200), 28, 3, 7),
    ("a", (200, 200), 32, 3, 8),
    ("a", (200, 200), 200, 20, 50),
    ("b", (200, 200), 38, 17, 8),
    ("b", (200, 200), 42, 18, 9),
    ("b", (200, 200), 48, 21, 10),
    ("b", (200, 200), 52, 23, 11),
    ("b", (200, 200), 58, 26, 12),
    ("b", (200, 200), 200, 88, 42),
]


@pytest.mark.parametrize("c, os, ns, x, y", testdata)
def test_get_hotspots(hotspots, c, os, ns, x, y) -> None:
    h = HotspotsParser(hotspots)
    cords = h.get_hotspots(c, os, ns)

    assert cords[0] == x
    assert cords[1] == y
