#!/usr/bin/env python
# -*- coding: utf-8 -*-


from clickgen.providers.bitmaps import ThemeBitmapsProvider


def test_theme_bitmaps_provider_dir(bitmaps_dir: str) -> None:
    t = ThemeBitmapsProvider(bitmaps_dir)
    assert t.dir == bitmaps_dir
