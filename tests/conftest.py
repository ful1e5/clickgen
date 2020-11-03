#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.providers.themeconfig import ThemeConfigsProvider
from typing import List

import pytest

from clickgen.configs import ThemeInfo
from clickgen.providers.jsonparser import Hotspots


@pytest.fixture(scope="module")
def ti() -> ThemeInfo:
    return ThemeInfo(theme_name="foo", author="bar")


@pytest.fixture(scope="module")
def sizes() -> List[int]:
    return [1, 2]


@pytest.fixture(scope="module")
def bitmaps_dir() -> str:
    return "foo"


@pytest.fixture(scope="module")
def hotspots() -> Hotspots:
    return {"a": {"xhot": 20, "yhot": 50}, "b": {"xhot": 88, "yhot": 42}}


@pytest.fixture(scope="module")
def tcp(bitmaps_dir, hotspots, sizes) -> ThemeConfigsProvider:
    return ThemeConfigsProvider(bitmaps_dir, sizes, hotspots)


@pytest.fixture(scope="module")
def pngs() -> List[str]:
    return ["a.png", "b.png", "c-01.png", "c-02.png"]