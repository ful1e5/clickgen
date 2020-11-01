#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from typing import Dict
import unittest

from clickgen.configs import ThemeInfo, ThemeSettings


class ConfigTest(unittest.TestCase):
    def setUp(self) -> None:
        self.t = ThemeInfo(theme_name="foo", author="bar")
        self.ts = ThemeSettings(
            bitmaps_dir="foo", sizes=[1, 2], hotspots={"a": {"xhot": 1, "yhot": 2}}
        )

    def test_theme_info(self) -> None:
        assert isinstance(self.t, ThemeInfo)

        assert self.t.comment == None
        assert isinstance(self.t.theme_name, str)
        assert isinstance(self.t.author, str)
        assert self.t.url == "Unknown Source!"

    def test_theme_settings(self) -> None:
        assert isinstance(self.ts, ThemeSettings)

        assert isinstance(self.ts.sizes[0], int)

        assert self.ts.animation_delay == 50
        assert self.ts.out_dir == os.getcwd()

        assert isinstance(self.ts.hotspots, Dict)
        assert isinstance(self.ts.hotspots.get("a"), Dict)
        assert isinstance(self.ts.hotspots.get("a").get("xhot"), int)
        assert isinstance(self.ts.hotspots.get("a").get("yhot"), int)
