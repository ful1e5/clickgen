#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
from clickgen.core import Bitmap


def test_static_Bitmap_as_str_without_key(static_png_as_str) -> None:
    png = static_png_as_str
    bitmap = Bitmap(png)

    with pytest.raises(AttributeError):
        bitmap.grouped_png
    assert bitmap.png == Path(png)
    assert bitmap.animated == False
    assert bitmap.size == (200, 200)
    assert bitmap.height == 200
    assert bitmap.width == 200
    assert bitmap.compress == 0
    assert bitmap.key == "test"


def test_static_Bitmap_as_Path_without_key(static_png_as_Path) -> None:
    png = static_png_as_Path
    bitmap = Bitmap(png)

    with pytest.raises(AttributeError):
        bitmap.grouped_png
    assert bitmap.png == png
    assert bitmap.animated == False
    assert bitmap.size == (200, 200)
    assert bitmap.height == 200
    assert bitmap.width == 200
    assert bitmap.compress == 0
    assert bitmap.key == "test"
