#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List

import pytest
from clickgen.core import Bitmap


def test_static_Bitmap_as_str(static_png) -> None:
    str_static_png = str(static_png)
    bmp = Bitmap(str_static_png, (0, 0))

    with pytest.raises(AttributeError):
        bmp.grouped_png
    assert bmp.png == static_png
    assert bmp.animated == False
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test-0"
    assert bmp.x_hot == 0
    assert bmp.y_hot == 0


def test_static_Bitmap_as_Path(static_png) -> None:
    bmp = Bitmap(static_png, (2, 2))

    with pytest.raises(AttributeError):
        bmp.grouped_png
    assert bmp.png == static_png
    assert bmp.animated == False
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test-0"
    assert bmp.x_hot == 2
    assert bmp.y_hot == 2


def test_animated_Bitmap_as_str(animated_png) -> None:
    str_animated_png: List[str] = list(map(lambda x: str(x.absolute()), animated_png))
    bmp = Bitmap(str_animated_png, (13, 14))

    with pytest.raises(AttributeError):
        bmp.png
    assert bmp.grouped_png == animated_png
    assert bmp.animated == True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == 13
    assert bmp.y_hot == 14


def test_animated_Bitmap_as_Path(animated_png) -> None:
    bmp = Bitmap(animated_png, (4, 7))

    with pytest.raises(AttributeError):
        bmp.png
    assert bmp.grouped_png == animated_png
    assert bmp.animated == True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == 4
    assert bmp.y_hot == 7


def test_static_Bitmap_hotspot_underflow_exception(static_png) -> None:
    with pytest.raises(ValueError):
        Bitmap(static_png, (2, -3))
        Bitmap(static_png, (-2, 3))
        Bitmap(static_png, (-2, -3))


def test_static_Bitmap_hotspot_overflow_exception(static_png) -> None:
    with pytest.raises(ValueError):
        Bitmap(static_png, (12, 60))
        Bitmap(static_png, (55, 3))
        Bitmap(static_png, (55, 60))


def test_animated_Bitmap_hotspot_underflow_exception(animated_png) -> None:
    with pytest.raises(ValueError):
        Bitmap(animated_png, (2, -3))
        Bitmap(animated_png, (-2, 3))
        Bitmap(animated_png, (-2, -3))


def test_animated_Bitmap_hotspot_overflow_exception(animated_png) -> None:
    with pytest.raises(ValueError):
        Bitmap(animated_png, (12, 60))
        Bitmap(animated_png, (55, 3))
        Bitmap(animated_png, (55, 60))
