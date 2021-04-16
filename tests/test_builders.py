#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

from pathlib import Path
from random import randint

import pytest

from clickgen.builders import Options, WindowsCursor, XCursor
from clickgen.core import CursorAlias
from tests.utils import create_test_image

#
# XCursor
#


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


def test_WindowsCursor_exceptions(static_config, image_dir) -> None:
    """Testing WindowsCursor `framesets` Exceptions."""
    win = WindowsCursor(static_config, image_dir, options=Options())

    f1 = [
        (10, -1, -1, "test-0.png", 10),
        (9, -1, -1, "test-0.png", 10),
        (10, -1, -1, "test-1.png", 10),
        (9, -1, -1, "test-1.png", 10),
        (10, -1, -1, "test-2.png", 10),
        (9, -1, -1, "test-2.png", 10),
        (10, -1, -1, "test-3.png", 10),
        (9, -1, -1, "test-3.png", 10),
    ]

    with pytest.raises(ValueError) as excinfo:
        win.make_framesets(f1)

    assert (
        str(excinfo.value)
        == "Frames are not sorted: frame 2 has size 10, but we have seen that already"
    )

    f2 = [
        (10, -1, -1, "test-0.png", 10),
        (10, -1, -1, "test-1.png", 10),
        (10, -1, -1, "test-2.png", 10),
        (10, -1, -1, "test-3.png", 10),
        (9, -1, -1, "test-0.png", 10),
        (9, -1, -1, "test-1.png", 10),
        (9, -1, -1, "test-2.png", 10),
    ]

    with pytest.raises(ValueError) as excinfo:
        win.make_framesets(f2)

    assert str(excinfo.value) == "Frameset 3 has size 1, expected 2"

    f3 = [
        (10, -1, -1, "test-0.png", 10),
        (10, -1, -1, "test-1.png", 10),
        (10, -1, -1, "test-2.png", 10),
        (10, -1, -1, "test-3.png", 10),
        (9, -1, -1, "test-0.png", 10),
        (9, -1, -1, "test-1.png", 10),
        (9, -1, -1, "test-2.png", 10),
        (9, -1, -1, "test-3.png", 1),
    ]

    with pytest.raises(ValueError) as excinfo:
        win.make_framesets(f3)

    assert (
        str(excinfo.value)
        == "Frameset 1 has duration 1 for framesize 9, but 10 for framesize 10"
    )

    f4 = [
        (10, -1, -1, "test-0.png", 10),
        (10, -1, -1, "test-1.png", 10),
        (10, -1, -1, "test-2.png", 10),
        (10, -1, -1, "test-3.png", 10),
        (9, -1, -1, "test-0.png", 10),
        (9, -1, -1, "test-1.png", 10),
        (9, -1, -1, "test-2.png", 10),
        (9, -1, -1, "test-3.png", 10),
    ]
    framesets = win.make_framesets(f4)
    ff = framesets[0][0]
    print(ff[0])


def test_WindowsCursor(static_config, image_dir) -> None:
    """Testing WindowsCursor members value."""
    win = WindowsCursor(static_config, image_dir, options=Options())
    assert win.config_file == static_config

    # We know 'out_dir' is not exists
    assert win.out_dir.exists() is True


def test_WindowsCursor_generate_with_static_config(static_config, image_dir) -> None:
    """Testing WindowsCursor generate method for generating static (.cur) \
    cursor.
    """
    win = WindowsCursor(static_config, image_dir, options=Options())
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".cur"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_generate_with_animated_config(
    animated_config, image_dir
) -> None:
    """Testing WindowsCursor generate method for generating animated (.ani) \
    cursor.
    """
    win = WindowsCursor(animated_config, image_dir, options=Options())
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".ani"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_generate_with_static_config_and_shadow(
    static_config, image_dir
) -> None:
    """Testing WindowsCursor generate method for generating static (.cur) \
    cursor with shadows.
    """
    options = Options(add_shadows=True)
    win = WindowsCursor(static_config, image_dir, options)
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".cur"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_generate_with_animated_config_and_shadow(
    animated_config, image_dir
) -> None:
    """Testing WindowsCursor generate method for generating animated (.ani) \
    cursor with shadows.
    """
    options = Options(add_shadows=True)
    win = WindowsCursor(animated_config, image_dir, options)
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".ani"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_create_with_static_config(static_config, image_dir) -> None:
    """Testing WindowsCursor generate static (.cur) cursor with ``create`` \
    classmethod.
    """
    with WindowsCursor.create(static_config, image_dir) as win:
        assert win.exists() is True
        assert win.suffix == ".cur"
        assert win.__sizeof__() > 0


def test_WindowsCursor_create_with_animated_config(hotspot, image_dir) -> None:
    """Testing WindowsCursor generate animated (.ani) cursor with ``create`` \
    classmethod.
    """
    animated_png = create_test_image(image_dir, 4)
    with CursorAlias.from_bitmap(animated_png, hotspot) as alias:
        cfg = alias.create((10, 10), delay=999999999)

        # Cover more than one delay sets
        new_lines = []
        with cfg.open("r") as f:
            lines = f.readlines()
            for l in lines:
                new_lines.append(l.replace("999999999", str(randint(20, 30))))
        with cfg.open("w") as f:
            f.writelines(new_lines)

        with WindowsCursor.create(cfg, image_dir) as win:
            assert win.exists() is True
            assert win.suffix == ".ani"
            assert win.__sizeof__() > 0
