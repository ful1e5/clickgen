#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from typing import List

import pytest
from clickgen.core import Bitmap

from .utils import create_test_image


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


@pytest.mark.parametrize(
    "png",
    [
        bytes(),
        [bytes()],
        [bytes(), bytes()],
        (2),
        [(2)],
        [(2), (2)],
        [2],
        [[2]],
        [[2], [2]],
        2,
        [2],
        [2, 2],
    ],
)
def test_Bitmap_png_type_error_exception(png) -> None:
    with pytest.raises(TypeError):
        assert Bitmap(png, (0, 0))


notfound = "notfound.png"
notfound_path = Path.cwd() / notfound


@pytest.mark.parametrize(
    "png",
    [
        notfound,
        [notfound],
        [notfound, notfound, notfound],
        notfound_path,
        [notfound_path],
        [notfound_path, notfound_path, notfound_path],
    ],
)
def test_Bitmap_png_not_found_exception(png) -> None:
    with pytest.raises(FileNotFoundError):
        assert Bitmap(png, (0, 0))


def test_Bitmap_non_png_exception(test_file) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(test_file, (0, 0))


def test_static_Bitmap_hotspot_underflow_exception(static_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(static_png, (2, -3))
        assert Bitmap(static_png, (-2, -3))


def test_static_Bitmap_hotspot_overflow_exception(static_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(static_png, (12, 60))
        assert Bitmap(static_png, (55, 60))


def test_animated_Bitmap_hotspot_underflow_exception(animated_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(animated_png, (2, -3))
        assert Bitmap(animated_png, (-2, -3))


def test_animated_Bitmap_hotspot_overflow_exception(animated_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(animated_png, (12, 60))
        assert Bitmap(animated_png, (55, 60))


def test_Bitmap_png_must_had_equal_width_and_height_exception(image_dir) -> None:
    png = create_test_image(image_dir, 1, size=(2, 3))
    with pytest.raises(ValueError):
        assert Bitmap(png, (0, 0))


def test_animated_Bitmap_all_png_size_must_be_equal_exception(image_dir) -> None:
    png = create_test_image(image_dir, 2, size=(2, 2))
    png.append(create_test_image(image_dir, 1, size=(3, 6)))
    png.append(create_test_image(image_dir, 1, size=(3, 3)))

    with pytest.raises(ValueError):
        assert Bitmap(png, (0, 0))


def test_invalid_animated_Bitmap_name_exception(image_dir) -> None:
    png = []
    images = create_test_image(image_dir, 3, size=(5, 5))

    for idx, p in enumerate(images):
        target = p.with_name(f"notvalidframe{idx}.png")
        p.rename(target)
        png.append(target)

    with pytest.raises(ValueError):
        assert Bitmap(png, (1, 1))


def test_animated_Bitmap_group_had_same_key_exception(image_dir) -> None:
    png = []
    images = create_test_image(image_dir, 3, size=(5, 5))

    for idx, p in enumerate(images):
        target = p.with_name(f"{str(randint(9999,453334))}-{idx}.png")
        p.rename(target)
        png.append(target)

    with pytest.raises(ValueError):
        assert Bitmap(png, (1, 1))
