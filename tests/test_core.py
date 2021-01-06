#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import List

import pytest
from clickgen.core import Bitmap


def test_static_Bitmap_as_str(static_png) -> None:
    str_static_png = str(static_png)
    bmp = Bitmap(str_static_png)

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
    bmp = Bitmap(static_png)

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


def test_animated_Bitmap_as_str(animated_png) -> None:
    str_animated_png: List[str] = list(map(lambda x: str(x.absolute()), animated_png))
    bmp = Bitmap(str_animated_png)

    with pytest.raises(AttributeError):
        bmp.png
    assert bmp.grouped_png == animated_png
    assert bmp.animated == True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == 0
    assert bmp.y_hot == 0


def test_animated_Bitmap_as_Path(animated_png) -> None:
    bmp = Bitmap(animated_png)

    with pytest.raises(AttributeError):
        bmp.png
    assert bmp.grouped_png == animated_png
    assert bmp.animated == True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == 0
    assert bmp.y_hot == 0


def test_key_not_affecting_in_static_Bitmap(static_png) -> None:
    bmp = Bitmap(static_png, key="Testing")
    bmp.key == "test-0"
