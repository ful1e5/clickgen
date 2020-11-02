#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import PropertyMock, patch

import pytest

from clickgen.providers.jsonparser import Hotspots, HotspotsParser


@pytest.fixture
def hotspots() -> Hotspots:
    return {"a": {"xhot": 1, "yhot": 2}, "b": {"xhot": 3, "yhot": 4}}


def test_hotspots_parser(hotspots) -> None:
    with patch.object(
        HotspotsParser, "_HotspotsParser__hotspots", new_callable=PropertyMock
    ) as mock_hotspots:
        h = HotspotsParser(mock_hotspots)

        mock_hotspots.return_value = hotspots
        assert hotspots == h._HotspotsParser__hotspots
