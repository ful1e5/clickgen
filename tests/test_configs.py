#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
from typing import Dict

import pytest

from clickgen.configs import Config, ThemeInfo, ThemeSettings


@pytest.fixture
def ts(bitmaps_dir, sizes, hotspots) -> ThemeSettings:
    return ThemeSettings(bitmaps_dir, sizes, hotspots)


def test_theme_info(ti) -> None:
    assert isinstance(ti, ThemeInfo)

    assert ti.comment == None
    assert isinstance(ti.theme_name, str)
    assert isinstance(ti.author, str)
    assert ti.url == "Unknown Source!"


def test_theme_settings(ts) -> None:
    assert isinstance(ts, ThemeSettings)

    for s in ts.sizes:
        assert s in [1, 2]
        assert isinstance(s, int)

    assert isinstance(ts.animation_delay, int)
    assert ts.animation_delay == 50
    assert ts.out_dir == os.getcwd()

    assert isinstance(ts.hotspots, Dict)
    assert ts.hotspots.get("a") == pytest.approx({"xhot": 20, "yhot": 50})
    assert isinstance(ts.hotspots.get("a").get("xhot"), int)
    assert ts.hotspots.get("a").get("xhot") == 20
    assert isinstance(ts.hotspots.get("a").get("yhot"), int)
    assert ts.hotspots.get("a").get("yhot") == 50


def test_config(ti, ts) -> None:
    c = Config(ti, ts)

    assert isinstance(c.settings, ThemeSettings)
    assert isinstance(c.info, ThemeInfo)

    # check paths
    assert path.isabs(c.settings.bitmaps_dir)
    assert path.isabs(c.settings.out_dir)

    assert c.info.theme_name == ti.theme_name
    assert c.info.author == ti.author
    assert c.info.comment == "foo By bar"
