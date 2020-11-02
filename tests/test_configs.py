#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict

from clickgen.configs import ThemeInfo, ThemeSettings
import pytest


@pytest.fixture
def ti() -> ThemeInfo:
    return ThemeInfo(theme_name="foo", author="bar")


@pytest.fixture
def ts() -> ThemeSettings:
    return ThemeSettings(
        bitmaps_dir="foo", sizes=[1, 2], hotspots={"a": {"xhot": 1, "yhot": 2}}
    )


def test_theme_info(ti) -> None:
    assert isinstance(ti, ThemeInfo)

    assert ti.comment == None
    assert isinstance(ti.theme_name, str)
    assert isinstance(ti.author, str)
    assert ti.url == "Unknown Source!"


def test_theme_settings(ts) -> None:
    assert isinstance(ts, ThemeSettings)

    assert isinstance(ts.sizes[0], int)

    assert ts.animation_delay == 50
    assert ts.out_dir == os.getcwd()

    assert isinstance(ts.hotspots, Dict)
    assert isinstance(ts.hotspots.get("a"), Dict)
    assert isinstance(ts.hotspots.get("a").get("xhot"), int)
    assert isinstance(ts.hotspots.get("a").get("yhot"), int)
