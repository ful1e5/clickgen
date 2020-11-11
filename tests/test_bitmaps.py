#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.providers.bitmaps import ThemeBitmapsProvider


def test_theme_bitmaps_provider_dir(bitmaps_dir: str) -> None:
    t = ThemeBitmapsProvider(bitmaps_dir)
    assert t.dir == bitmaps_dir


def test_theme_bitmaps_provider_animated_bitmaps(
    bitmaps_provider: ThemeBitmapsProvider,
) -> None:
    assert bitmaps_provider.animated_bitmaps() == {"c": ["c-01.png", "c-02.png"]}


def test_theme_bitmaps_provider_static_bitmaps(
    bitmaps_provider: ThemeBitmapsProvider,
) -> None:
    assert bitmaps_provider.static_bitmaps() == ["a.png", "b.png"]
