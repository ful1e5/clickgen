#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path

import pytest
from clickgen.core import Bitmap


def test_static_Bitmap_as_str(static_png) -> None:
    png = static_png
    bitmap = Bitmap(str(png))

    with pytest.raises(AttributeError):
        bitmap.grouped_png
    assert bitmap.png == png
    assert bitmap.animated == False
    assert bitmap.height == 20
    assert bitmap.width == 20
    assert bitmap.compress == 0
    assert bitmap.key == "test-0"
    assert bitmap.x_hot == 0
    assert bitmap.y_hot == 0


def test_static_Bitmap_as_Path(static_png) -> None:
    png = static_png
    bitmap = Bitmap(png)

    with pytest.raises(AttributeError):
        bitmap.grouped_png
    assert bitmap.png == png
    assert bitmap.animated == False
    assert bitmap.height == 20
    assert bitmap.width == 20
    assert bitmap.compress == 0
    assert bitmap.key == "test-0"
    assert bitmap.x_hot == 0
    assert bitmap.y_hot == 0


def test_animated_Bitmap_as_Path_without_key_and_hotspot(animated_png) -> None:
    png = animated_png
    bitmap = Bitmap(png)

    with pytest.raises(AttributeError):
        bitmap.png
    assert bitmap.grouped_png == png
    assert bitmap.animated == True
    assert bitmap.height == 20
    assert bitmap.width == 20
    assert bitmap.compress == 0
    assert bitmap.key == "test"
    assert bitmap.x_hot == 0
    assert bitmap.y_hot == 0
