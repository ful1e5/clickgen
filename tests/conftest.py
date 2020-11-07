#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tempfile
from os import path
from typing import List

import pytest
from clickgen.builders.winbuilder import WinCursorsBuilder
from clickgen.builders.x11builder import X11CursorsBuilder
from clickgen.configs import ThemeInfo
from clickgen.providers.jsonparser import Hotspots
from clickgen.providers.themeconfig import ThemeConfigsProvider

from . import __path__ as root


@pytest.fixture(scope="module")
def ti() -> ThemeInfo:
    return ThemeInfo(theme_name="foo", author="bar")


@pytest.fixture(scope="module")
def sizes() -> List[int]:
    return [24, 32]


@pytest.fixture(scope="module")
def delay() -> int:
    return 50


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
def out_dir() -> str:
    return tempfile.mkdtemp()


@pytest.fixture(scope="module")
def tcp(bitmaps_dir, hotspots, sizes) -> ThemeConfigsProvider:
    return ThemeConfigsProvider(bitmaps_dir, hotspots, sizes)


@pytest.fixture(scope="module")
def config_dir(tcp: ThemeConfigsProvider, delay) -> str:
    return tcp.generate(delay)


@pytest.fixture(scope="module")
def xcursors_dir(config_dir, out_dir) -> str:
    X11CursorsBuilder(config_dir, out_dir).build()
    return path.join(out_dir, "cursors")


@pytest.fixture(scope="module")
def wincursors_dir(bitmaps_dir, hotspots, sizes, delay, out_dir) -> str:
    cfg_dir = ThemeConfigsProvider(bitmaps_dir, hotspots, sizes).generate(delay)
    WinCursorsBuilder(cfg_dir, out_dir).build()
    return out_dir


@pytest.fixture(scope="module")
def pngs() -> List[str]:
    return ["a.png", "b.png", "c-01.png", "c-02.png"]


@pytest.fixture(scope="module")
def cfg_lines(delay) -> List[str]:
    return [
        "24 2 6 24x24/a.png\n",
        "32 3 8 32x32/a.png",
        "24 11 5 24x24/b.png\n",
        "32 14 7 32x32/b.png",
        f"24 4 7 24x24/c-01.png {delay}\n",
        f"24 4 7 24x24/c-02.png {delay}\n",
        f"32 5 9 32x32/c-01.png {delay}\n",
        f"32 5 9 32x32/c-02.png {delay}",
    ]


@pytest.fixture(scope="module")
def lines() -> List[str]:
    return ["firstline", "secondline"]
