#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

from random import randint

import pytest

from clickgen.builders import Options, WindowsCursor
from clickgen.core import CursorAlias
from tests.utils import create_test_image

#
# WindowsCursor
#


def test_WindowsCursor_from_bitmap_with_static_png(
    static_png, hotspot, image_dir
) -> None:
    """Testing WindowsCursor `form_bitmap` classmethod for generating **static** cursor."""
    win = WindowsCursor.from_bitmap(
        png=static_png,
        hotspot=hotspot,
        size=(5, 5),
        canvas_size=(10, 10),
        out_dir=image_dir,
    )
    assert win.exists() is True
    assert win.__sizeof__() > 0


def test_WindowsCursor_from_bitmap_with_static_png_exceptions(
    static_png, hotspot
) -> None:
    """Testing WindowsCursor `form_bitmap` classmethod exceptions for generating **static** cursor."""
    with pytest.raises(KeyError) as excinfo1:
        WindowsCursor.from_bitmap()
    assert str(excinfo1.value) == "\"argument 'png' required\""

    with pytest.raises(KeyError) as excinfo2:
        WindowsCursor.from_bitmap(png=static_png)
    assert str(excinfo2.value) == "\"argument 'hotspot' required\""

    with pytest.raises(KeyError) as excinfo3:
        WindowsCursor.from_bitmap(png=static_png, hotspot=hotspot)
    assert str(excinfo3.value) == "\"argument 'size' required\""

    with pytest.raises(KeyError) as excinfo4:
        WindowsCursor.from_bitmap(png=static_png, hotspot=hotspot, canvas_size=(10, 10))
    assert str(excinfo4.value) == "\"argument 'size' required\""

    with pytest.raises(KeyError) as excinfo5:
        WindowsCursor.from_bitmap(
            png=static_png, hotspot=hotspot, canvas_size=(10, 10), size=(5, 5)
        )
    assert str(excinfo5.value) == "\"argument 'out_dir' required\""


def test_WindowsCursor_from_bitmap_with_animated_png(
    animated_png, hotspot, image_dir
) -> None:
    """Testing WindowsCursor `form_bitmap` classmethod for generating **animated** cursor."""
    win = WindowsCursor.from_bitmap(
        png=animated_png,
        hotspot=hotspot,
        size=(5, 5),
        canvas_size=(10, 10),
        out_dir=image_dir,
        delay=1,
    )
    assert win.exists() is True
    assert win.__sizeof__() > 0


def test_WindowsCursor_from_bitmap_with_animated_png_exceptions(
    animated_png, hotspot, image_dir
) -> None:
    """Testing WindowsCursor `form_bitmap` classmethod exceptions for generating **animated** \
    cursor.
    """
    with pytest.raises(KeyError) as excinfo1:
        WindowsCursor.from_bitmap()
    assert str(excinfo1.value) == "\"argument 'png' required\""

    with pytest.raises(KeyError) as excinfo2:
        WindowsCursor.from_bitmap(png=animated_png)
    assert str(excinfo2.value) == "\"argument 'hotspot' required\""

    with pytest.raises(KeyError) as excinfo3:
        WindowsCursor.from_bitmap(png=animated_png, hotspot=hotspot)
    assert str(excinfo3.value) == "\"argument 'size' required\""

    with pytest.raises(KeyError) as excinfo4:
        WindowsCursor.from_bitmap(
            png=animated_png, hotspot=hotspot, canvas_size=(10, 10)
        )
    assert str(excinfo4.value) == "\"argument 'size' required\""

    with pytest.raises(KeyError) as excinfo5:
        WindowsCursor.from_bitmap(
            png=animated_png, hotspot=hotspot, canvas_size=(10, 10), size=(5, 5)
        )
    assert str(excinfo5.value) == "\"argument 'out_dir' required\""

    with pytest.raises(KeyError) as excinfo6:
        WindowsCursor.from_bitmap(
            png=animated_png,
            hotspot=hotspot,
            canvas_size=(10, 10),
            size=(5, 5),
            out_dir=image_dir,
        )
    assert str(excinfo6.value) == "\"argument 'delay' required\""


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
