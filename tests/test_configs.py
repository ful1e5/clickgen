#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict

from clickgen.configs import ThemeInfo, ThemeSettings


def test_theme_info():
    t = ThemeInfo(theme_name="foo", author="bar")
    assert isinstance(t, ThemeInfo)

    assert t.comment == None
    assert isinstance(t.theme_name, str)
    assert isinstance(t.author, str)
    assert t.url == "Unknown Source!"


def test_theme_settings():
    ts = ThemeSettings(
        bitmaps_dir="foo", sizes=[1, 2], hotspots={"a": {"xhot": 1, "yhot": 2}}
    )

    assert isinstance(ts, ThemeSettings)

    assert isinstance(ts.sizes[0], int)

    assert ts.animation_delay == 50
    assert ts.out_dir == os.getcwd()

    assert isinstance(ts.hotspots, Dict)
    assert isinstance(ts.hotspots.get("a"), Dict)
    assert isinstance(ts.hotspots.get("a").get("xhot"), int)
    assert isinstance(ts.hotspots.get("a").get("yhot"), int)
