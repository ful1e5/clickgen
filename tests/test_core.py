#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from typing import List

import pytest
from clickgen.core import Bitmap
from PIL import Image

from .utils import create_test_image


def test_static_Bitmap_as_str(static_png, hotspot) -> None:
    str_static_png = str(static_png)
    bmp = Bitmap(str_static_png, hotspot)

    with pytest.raises(AttributeError):
        assert bmp.grouped_png
    assert bmp.png == static_png
    assert bmp.animated == False
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test-0"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


def test_static_Bitmap_as_Path(static_png, hotspot) -> None:
    bmp = Bitmap(static_png, hotspot)

    with pytest.raises(AttributeError):
        assert bmp.grouped_png
    assert bmp.png == static_png
    assert bmp.animated == False
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test-0"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


def test_animated_Bitmap_as_str(animated_png, hotspot) -> None:
    str_animated_png: List[str] = list(map(lambda x: str(x.absolute()), animated_png))
    bmp = Bitmap(str_animated_png, hotspot)

    with pytest.raises(AttributeError):
        assert bmp.png
    assert bmp.grouped_png == animated_png
    assert bmp.animated == True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


def test_animated_Bitmap_as_Path(animated_png, hotspot) -> None:
    bmp = Bitmap(animated_png, hotspot)

    with pytest.raises(AttributeError):
        assert bmp.png
    assert bmp.grouped_png == animated_png
    assert bmp.animated == True
    assert bmp.height == 20
    assert bmp.width == 20
    assert bmp.compress == 0
    assert bmp.key == "test"
    assert bmp.x_hot == hotspot[0]
    assert bmp.y_hot == hotspot[1]


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
def test_Bitmap_png_type_error_exception(png, hotspot) -> None:
    with pytest.raises(TypeError):
        assert Bitmap(png, hotspot)


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
def test_Bitmap_png_not_found_exception(png, hotspot) -> None:
    with pytest.raises(FileNotFoundError):
        assert Bitmap(png, hotspot)


def test_Bitmap_non_png_exception(test_file, hotspot) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(test_file, hotspot)


def test_static_Bitmap_hotspot_underflow_exception(static_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(static_png, (2, -3))
        assert Bitmap(static_png, (-2, -3))


def test_static_Bitmap_hotspot_overflow_exception(static_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(static_png, (12, 60))
        assert Bitmap(static_png, (55, 60))


def test_static_Bitmap_str(static_png, hotspot) -> None:
    assert (
        Bitmap(static_png, hotspot).__str__()
        == f"Bitmap(png={static_png}, key={static_png.stem}, animated=False, size=(20, 20), width=20, height=20, x_hot={hotspot[0]}, y_hot={hotspot[1]})"
    )


def test_static_Bitmap_repr(static_png, hotspot) -> None:
    assert (
        Bitmap(static_png, hotspot).__repr__()
        == f"{{ 'png':{static_png}, 'key':'test-0', 'animated':False, 'size':(20, 20), 'width':20, 'height':20, 'x_hot':{hotspot[0]}, 'y_hot':{hotspot[1]} }}"
    )


def test_static_Bitmap_context_manager(static_png, hotspot) -> None:
    with Bitmap(static_png, hotspot) as bmp:
        with pytest.raises(AttributeError):
            assert bmp.grouped_png
        assert bmp.png == static_png
        assert bmp.animated == False
        assert bmp.height == 20
        assert bmp.width == 20
        assert bmp.compress == 0
        assert bmp.key == "test-0"
        assert bmp.x_hot == hotspot[0]
        assert bmp.y_hot == hotspot[1]

    assert bmp.png == None
    assert bmp.animated == None
    assert bmp.height == None
    assert bmp.width == None
    assert bmp.compress == None
    assert bmp.key == None
    assert bmp.x_hot == None
    assert bmp.y_hot == None


def test_animated_Bitmap_hotspot_underflow_exception(animated_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(animated_png, (2, -3))
        assert Bitmap(animated_png, (-2, -3))


def test_animated_Bitmap_hotspot_overflow_exception(animated_png) -> None:
    with pytest.raises(ValueError):
        assert Bitmap(animated_png, (12, 60))
        assert Bitmap(animated_png, (55, 60))


def test_animated_Bitmap_str(animated_png, hotspot) -> None:
    assert (
        Bitmap(animated_png, hotspot).__str__()
        == f"Bitmap(grouped_png={animated_png}, key={animated_png[0].stem.rsplit('-',1)[0]}, animated=True, size=(20, 20), width=20, height=20, x_hot={hotspot[0]}, y_hot={hotspot[1]})"
    )


def test_animated_Bitmap_repr(animated_png, hotspot) -> None:
    assert (
        Bitmap(animated_png, hotspot).__repr__()
        == f"{{ 'grouped_png':{animated_png}, 'key':'test', 'animated':True, 'size':(20, 20), 'width':20, 'height':20, 'x_hot':{hotspot[0]}, 'y_hot':{hotspot[1]} }}"
    )


def test_animated_Bitmap_context_manager(animated_png, hotspot) -> None:
    with Bitmap(animated_png, hotspot) as bmp:
        with pytest.raises(AttributeError):
            assert bmp.png
        assert bmp.grouped_png == animated_png
        assert bmp.animated == True
        assert bmp.height == 20
        assert bmp.width == 20
        assert bmp.compress == 0
        assert bmp.key == "test"
        assert bmp.x_hot == hotspot[0]
        assert bmp.y_hot == hotspot[1]

    assert bmp.grouped_png == None
    assert bmp.animated == None
    assert bmp.height == None
    assert bmp.width == None
    assert bmp.compress == None
    assert bmp.key == None
    assert bmp.x_hot == None
    assert bmp.y_hot == None


def test_static_Bitmap_resize_with_save_is_updating_hotspot(static_png) -> None:
    new_size = (10, 10)
    with Bitmap(static_png, (10, 10)) as b:
        assert b.x_hot == 10
        assert b.y_hot == 10
        b.resize(size=new_size, save=True)
        assert b.x_hot == 5
        assert b.y_hot == 5


def test_static_Bitmap_resize_without_save_is_not_updating_hotspot(static_png) -> None:
    new_size = (10, 10)
    with Bitmap(static_png, (10, 10)) as b:
        assert b.x_hot == 10
        assert b.y_hot == 10
        b.resize(size=new_size, save=False)
        assert b.x_hot == 10
        assert b.y_hot == 10


def test_static_Bitmap_resize_without_save(static_png, hotspot) -> None:
    new_size = (10, 10)
    return_image = Bitmap(static_png, hotspot).resize(size=new_size, save=False)
    assert return_image != None

    assert return_image.size == new_size


def test_static_Bitmap_resize_with_save(static_png, hotspot) -> None:
    new_size = (10, 10)
    is_return = Bitmap(static_png, hotspot).resize(size=new_size, save=True)
    assert is_return == None
    with Image.open(static_png) as i:
        assert i.size == new_size


def test_Bitmap_png_must_had_equal_width_and_height_exception(
    image_dir, hotspot
) -> None:
    png = create_test_image(image_dir, 1, size=(2, 3))
    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


def test_animated_Bitmap_all_png_size_must_be_equal_exception(
    image_dir, hotspot
) -> None:
    png = create_test_image(image_dir, 2, size=(2, 2))
    png.append(create_test_image(image_dir, 1, size=(3, 6)))
    png.append(create_test_image(image_dir, 1, size=(3, 3)))

    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


def test_invalid_animated_Bitmap_name_exception(image_dir, hotspot) -> None:
    png = []
    images = create_test_image(image_dir, 3, size=(5, 5))

    for idx, p in enumerate(images):
        target = p.with_name(f"notvalidframe{idx}.png")
        p.rename(target)
        png.append(target)

    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)


def test_animated_Bitmap_group_had_same_key_exception(image_dir, hotspot) -> None:
    png = []
    images = create_test_image(image_dir, 3, size=(5, 5))

    for idx, p in enumerate(images):
        target = p.with_name(f"{str(randint(9999,453334))}-{idx}.png")
        p.rename(target)
        png.append(target)

    with pytest.raises(ValueError):
        assert Bitmap(png, hotspot)
