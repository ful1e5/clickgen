#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

from pathlib import Path

import pytest

from clickgen.builders import XCursor


def test_XCursor_config_file_not_found_exception(image_dir) -> None:
    """Testing XCursor raises **FileNotFoundError** for config_file or not."""
    with pytest.raises(FileNotFoundError) as excinfo:
        XCursor(image_dir, image_dir)
    assert str(excinfo.value) == f"'{image_dir.name}' is not found or not a config file"


def test_XCursor(static_config, image_dir) -> None:
    """Testing XCursor members value."""

    x = XCursor(static_config, image_dir)
    assert x.config_file == static_config

    # We know 'out_dir' is not exists
    assert x.out_dir.exists() is True
    assert x.out_dir == image_dir / "cursors"


def test_XCursor_generate_exception(image_dir) -> None:
    """Testing XCursor generate **RuntimeError** exception."""
    cfg: Path = image_dir / "test.alias"
    cfg.write_text("10 10 10 test/test.png")
    x = XCursor(cfg, image_dir)
    with pytest.raises(RuntimeError) as excinfo:
        x.generate()

    assert (
        str(excinfo.value)
        == "'xcursorgen' failed to generate XCursor from 'test.alias'"
    )


def test_XCursor_generate_with_static_config(static_config, image_dir) -> None:
    """Testing XCursor generate **static** cursors."""
    x = XCursor(static_config, image_dir)
    x.generate()

    assert x.out.exists() is True
    assert x.out.__sizeof__() > 0


def test_XCursor_generate_with_animated_config(animated_config, image_dir) -> None:
    """Testing XCursor generate **animated** cursors."""
    x = XCursor(animated_config, image_dir)
    x.generate()

    assert x.out.exists() is True
    assert x.out.__sizeof__() > 0


def test_XCursor_create_with_static_config(static_config, image_dir) -> None:
    """Testing XCursor `create` classmethod for generating **static** \
    cursor.
    """
    x = XCursor.create(static_config, image_dir)
    assert x.exists() is True
    assert x.__sizeof__() > 0


def test_XCursor_create_with_animated_config(animated_config, image_dir) -> None:
    """Testing XCursor `create` classmethod for generating **animated** \
    cursor.
    """
    x = XCursor.create(animated_config, image_dir)
    assert x.exists() is True
    assert x.__sizeof__() > 0


def test_XCursor_from_bitmap_with_static_png(static_png, hotspot, image_dir) -> None:
    """Testing XCursor `form_bitmap` classmethod for generating **static** \
    cursor.
    """
    x = XCursor.from_bitmap(
        png=static_png, hotspot=hotspot, x_sizes=(10, 10), out_dir=image_dir
    )
    assert x.exists() is True
    assert x.__sizeof__() > 0

    x1 = XCursor.from_bitmap(
        png=static_png, hotspot=hotspot, x_sizes=[(10, 10)], out_dir=image_dir
    )
    assert x1.exists() is True
    assert x1.__sizeof__() > 0

    x2 = XCursor.from_bitmap(
        png=static_png, hotspot=hotspot, x_sizes=[(10, 10), (20, 20)], out_dir=image_dir
    )
    assert x2.exists() is True
    assert x2.__sizeof__() > 0


def test_XCursor_from_bitmap_with_static_png_exceptions(static_png, hotspot) -> None:
    """Testing XCursor `form_bitmap` classmethod exceptions for generating **static** \
    cursor.
    """
    with pytest.raises(KeyError) as excinfo1:
        XCursor.from_bitmap()
    assert str(excinfo1.value) == "\"argument 'png' required\""

    with pytest.raises(KeyError) as excinfo2:
        XCursor.from_bitmap(png=static_png)
    assert str(excinfo2.value) == "\"argument 'hotspot' required\""

    with pytest.raises(KeyError) as excinfo3:
        XCursor.from_bitmap(png=static_png, hotspot=hotspot)
    assert str(excinfo3.value) == "\"argument 'x_sizes' required\""

    with pytest.raises(KeyError) as excinfo4:
        XCursor.from_bitmap(png=static_png, hotspot=hotspot, x_sizes=(10, 10))
    assert str(excinfo4.value) == "\"argument 'out_dir' required\""


def test_XCursor_from_bitmap_with_animated_png(
    animated_png, hotspot, image_dir
) -> None:
    """Testing XCursor `form_bitmap` classmethod for generating **animated** \
    cursor.
    """
    # testing with single size
    x = XCursor.from_bitmap(
        png=animated_png,
        hotspot=hotspot,
        x_sizes=[(10, 10)],
        out_dir=image_dir,
        delay=1,
    )
    assert x.exists() is True
    assert x.__sizeof__() > 0

    x1 = XCursor.from_bitmap(
        png=animated_png, hotspot=hotspot, x_sizes=(10, 10), out_dir=image_dir, delay=1
    )
    assert x1.exists() is True
    assert x1.__sizeof__() > 0

    # testing with multiple sizes
    x2 = XCursor.from_bitmap(
        png=animated_png,
        hotspot=hotspot,
        x_sizes=[(10, 10), (20, 20)],
        out_dir=image_dir,
        delay=1,
    )
    assert x2.exists() is True
    assert x2.__sizeof__() > 0


def test_XCursor_from_bitmap_with_animated_png_exceptions(
    animated_png, hotspot, image_dir
) -> None:
    """Testing XCursor `form_bitmap` classmethod exceptions for generating **animated** \
    cursor.
    """
    with pytest.raises(KeyError) as excinfo1:
        XCursor.from_bitmap()
    assert str(excinfo1.value) == "\"argument 'png' required\""

    with pytest.raises(KeyError) as excinfo2:
        XCursor.from_bitmap(png=animated_png)
    assert str(excinfo2.value) == "\"argument 'hotspot' required\""

    with pytest.raises(KeyError) as excinfo3:
        XCursor.from_bitmap(png=animated_png, hotspot=hotspot)
    assert str(excinfo3.value) == "\"argument 'x_sizes' required\""

    with pytest.raises(KeyError) as excinfo4:
        XCursor.from_bitmap(png=animated_png, hotspot=hotspot, x_sizes=(10, 10))
    assert str(excinfo4.value) == "\"argument 'out_dir' required\""

    with pytest.raises(KeyError) as excinfo5:
        XCursor.from_bitmap(
            png=animated_png, hotspot=hotspot, x_sizes=(10, 10), out_dir=image_dir
        )
    assert str(excinfo5.value) == "\"argument 'delay' required\""