#!/usr/bin/env python
# -*- coding: utf-8 -*-


#
# XCursor
#

from pathlib import Path
import pytest
from clickgen.builders import AnicursorgenArgs, WindowsCursor, XCursor


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
