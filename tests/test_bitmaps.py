#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.providers.bitmaps import PNG


def test_theme_bitmaps_provider_dir(bitmaps_dir: str) -> None:
    t = PNG(bitmaps_dir)
    assert t.bitmap_dir == bitmaps_dir


def test_theme_bitmaps_provider_animated_bitmaps(
    bitmaps_provider: PNG,
) -> None:
    assert bitmaps_provider.animated_pngs() == {"c": ["c-01.png", "c-02.png"]}


def test_theme_bitmaps_provider_static_bitmaps(
    bitmaps_provider: PNG,
) -> None:
    assert sorted(bitmaps_provider.static_pngs()) == ["a.png", "b.png"]
