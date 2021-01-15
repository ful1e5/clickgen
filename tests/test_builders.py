#!/usr/bin/env python
# -*- coding: utf-8 -*-

from random import randint
from tests.utils import create_test_image
from build.lib.clickgen.core import CursorAlias
from pathlib import Path

import pytest
from clickgen.builders import AnicursorgenArgs, WindowsCursor, XCursor

#
# XCursor
#


def test_XCursor_config_file_not_found_exception(image_dir) -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        XCursor(image_dir, image_dir)
    assert str(excinfo.value) == f"'{image_dir.name}' is not found or not a config file"


def test_XCursor(static_config, image_dir) -> None:
    x = XCursor(static_config, image_dir)
    assert x.config_file == static_config

    # We know 'out_dir' is not exists
    assert x.out_dir.exists() is True
    assert x.out_dir == image_dir / "cursors"


def test_XCursor_generate_exception(image_dir) -> None:
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
    x = XCursor(static_config, image_dir)
    x.generate()

    assert x.out.exists() is True
    assert x.out.__sizeof__() > 0


def test_XCursor_generate_with_animated_config(animated_config, image_dir) -> None:
    x = XCursor(animated_config, image_dir)
    x.generate()

    assert x.out.exists() is True
    assert x.out.__sizeof__() > 0


def test_XCursor_create_with_static_config(static_config, image_dir) -> None:
    x = XCursor.create(static_config, image_dir)
    assert x.exists() is True
    assert x.__sizeof__() > 0


def test_XCursor_create_with_animated_config(animated_config, image_dir) -> None:
    x = XCursor.create(animated_config, image_dir)
    assert x.exists() is True
    assert x.__sizeof__() > 0


def test_WindowsCursor_exceptions(static_config, image_dir) -> None:
    win = WindowsCursor(static_config, image_dir, args=AnicursorgenArgs())

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


def test_WindowsCursor(static_config, image_dir) -> None:
    win = WindowsCursor(static_config, image_dir, args=AnicursorgenArgs())
    assert win.config_file == static_config

    # We know 'out_dir' is not exists
    assert win.out_dir.exists() is True


def test_WindowsCursor_generate_with_static_config(static_config, image_dir) -> None:
    win = WindowsCursor(static_config, image_dir, args=AnicursorgenArgs())
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".cur"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_generate_with_animated_config(
    animated_config, image_dir
) -> None:
    win = WindowsCursor(animated_config, image_dir, args=AnicursorgenArgs())
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".ani"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_generate_with_static_config_and_shadow(
    static_config, image_dir
) -> None:
    args = AnicursorgenArgs(add_shadows=True)
    win = WindowsCursor(static_config, image_dir, args)
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".cur"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_generate_with_animated_config_and_shadow(
    animated_config, image_dir
) -> None:
    args = AnicursorgenArgs(add_shadows=True)
    win = WindowsCursor(animated_config, image_dir, args)
    win.generate()

    assert win.out.exists() is True
    assert win.out.suffix == ".ani"
    assert win.out.__sizeof__() > 0


def test_WindowsCursor_create_with_static_config(static_config, image_dir) -> None:
    with WindowsCursor.create(static_config, image_dir) as win:
        assert win.exists() is True
        assert win.suffix == ".cur"
        assert win.__sizeof__() > 0


def test_WindowsCursor_create_with_animated_config(hotspot, image_dir) -> None:
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
