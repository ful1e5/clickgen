#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import path
from typing import List

import pytest

from clickgen.configs import ThemeInfo
from clickgen.providers.jsonparser import Hotspots
from clickgen.providers.themeconfig import ThemeConfigsProvider

from . import __path__ as root


@pytest.fixture(scope="module")
def ti() -> ThemeInfo:
    return ThemeInfo(theme_name="foo", author="bar")


@pytest.fixture(scope="module")
def sizes() -> List[int]:
    return [1, 2]


@pytest.fixture(scope="module")
def bitmaps_dir() -> str:
    return path.abspath(path.join(root[0], "assets", "bitmaps"))


@pytest.fixture(scope="module")
def hotspots() -> Hotspots:
    return {
        "a": {"xhot": 20, "yhot": 50},
        "b": {"xhot": 88, "yhot": 42},
        "c": {"xhot": 33, "yhot": 56},
    }


@pytest.fixture(scope="module")
def tcp(bitmaps_dir, hotspots, sizes) -> ThemeConfigsProvider:
    return ThemeConfigsProvider(bitmaps_dir, hotspots, sizes)


@pytest.fixture(scope="module")
def config_dir(tcp: ThemeConfigsProvider) -> str:
    return tcp.generate(50)


@pytest.fixture(scope="module")
def pngs() -> List[str]:
    return ["a.png", "b.png", "c-01.png", "c-02.png"]


@pytest.fixture(scope="module")
def cfg_lines() -> List[str]:
    return [
        "1 0 0 1x1/a.png\n",
        "2 0 0 2x2/a.png",
        "1 0 0 1x1/b.png\n",
        "2 1 0 2x2/b.png",
        "1 0 0 1x1/c-01.png 50\n",
        "1 0 0 1x1/c-02.png 50\n",
        "2 0 1 2x2/c-01.png 50\n",
        "2 0 1 2x2/c-02.png 50",
    ]


@pytest.fixture(scope="module")
def lines() -> List[str]:
    return ["firstline", "secondline"]
