#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from tests.utils import create_test_cursor
import pytest
from pathlib import Path
from clickgen.packagers import WindowsPackager, XPackager


def test_XPackger(image_dir: Path) -> None:
    XPackager(image_dir, theme_name="test", comment="testing")

    cur_theme = image_dir / "cursor.theme"
    idx_theme = image_dir / "index.theme"

    assert cur_theme.exists() is True
    assert idx_theme.exists() is True

    with cur_theme.open() as f:
        assert f.readlines() == ["[Icon Theme]\n", "Name=test\n", 'Inherits="hicolor"']

    with idx_theme.open() as f:
        assert f.readlines() == [
            "[Icon Theme]\n",
            "Name=test\n",
            "Comment=testing\n",
            'Inherits="hicolor"',
        ]


def test_WindowsPackager_empty_dir_exception(image_dir: Path) -> None:
    with pytest.raises(FileNotFoundError) as excinfo:
        WindowsPackager(image_dir, theme_name="test", comment="testing", author="😎")

    assert (
        str(excinfo.value)
        == f"Windows cursors '*.cur' or '*.ani' not found in '{image_dir}'"
    )


def test_WindowsPackager_missing_cur_exception(image_dir: Path) -> None:
    create_test_cursor(image_dir, "Work.ani")
    create_test_cursor(image_dir, "Busy.ani")
    create_test_cursor(image_dir, "Default.cur")
    create_test_cursor(image_dir, "Help.cur")
    create_test_cursor(image_dir, "Link.cur")
    create_test_cursor(image_dir, "Move.cur")
    create_test_cursor(image_dir, "Diagonal_2.cur")
    create_test_cursor(image_dir, "Vertical.cur")
    create_test_cursor(image_dir, "Horizontal.cur")
    create_test_cursor(image_dir, "Diagonal_1.cur")
    create_test_cursor(image_dir, "Handwriting.cur")
    create_test_cursor(image_dir, "Cross.cur")
    create_test_cursor(image_dir, "IBeam.cur")
    with pytest.raises(FileNotFoundError) as excinfo:
        WindowsPackager(image_dir, theme_name="test", comment="testing", author="😎")

    assert (
        str(excinfo.value)
        == "Windows cursors are missing ['Alternate', 'Unavailiable']"
    )


def test_WindowsPackager_with_semi_animated_cursors(
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.ani")
    create_test_cursor(d, "Help.ani")
    create_test_cursor(d, "Link.ani")
    create_test_cursor(d, "Move.ani")
    create_test_cursor(d, "Diagonal_2.ani")
    create_test_cursor(d, "Vertical.ani")
    create_test_cursor(d, "Horizontal.ani")
    create_test_cursor(d, "Diagonal_1.ani")
    create_test_cursor(d, "Handwriting.ani")
    create_test_cursor(d, "Cross.ani")
    create_test_cursor(d, "IBeam.ani")
    create_test_cursor(d, "Unavailiable.ani")
    create_test_cursor(d, "Alternate.ani")

    WindowsPackager(d, theme_name="test", comment="testing", author="😎")

    install_file = d / "install.inf"

    assert install_file.exists() is True
    data = install_file.read_text()

    assert "Work.ani" in data
    assert "Busy.ani" in data
    assert "Default.ani" in data
    assert "Help.ani" in data
    assert "Link.ani" in data
    assert "Move.ani" in data
    assert "Diagonal_2.ani" in data
    assert "Vertical.ani" in data
    assert "Horizontal.ani" in data
    assert "Diagonal_1.ani" in data
    assert "Handwriting.ani" in data
    assert "Cross.ani" in data
    assert "IBeam.ani" in data
    assert "Unavailiable.ani" in data
    assert "Alternate.ani" in data

    shutil.rmtree(d)


def test_WindowsPackager_without_website_url(
    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.cur")
    create_test_cursor(d, "Help.cur")
    create_test_cursor(d, "Link.cur")
    create_test_cursor(d, "Move.cur")
    create_test_cursor(d, "Diagonal_2.cur")
    create_test_cursor(d, "Vertical.cur")
    create_test_cursor(d, "Horizontal.cur")
    create_test_cursor(d, "Diagonal_1.cur")
    create_test_cursor(d, "Handwriting.cur")
    create_test_cursor(d, "Cross.cur")
    create_test_cursor(d, "IBeam.cur")
    create_test_cursor(d, "Unavailiable.cur")
    create_test_cursor(d, "Alternate.cur")

    WindowsPackager(d, theme_name="test", comment="testing", author="😎")

    install_file = d / "install.inf"

    assert install_file.exists() is True
    data = install_file.read_text()

    assert "Work.ani" in data
    assert "Busy.ani" in data
    assert "Default.cur" in data
    assert "Help.cur" in data
    assert "Link.cur" in data
    assert "Move.cur" in data
    assert "Diagonal_2.cur" in data
    assert "Vertical.cur" in data
    assert "Horizontal.cur" in data
    assert "Diagonal_1.cur" in data
    assert "Handwriting.cur" in data
    assert "Cross.cur" in data
    assert "IBeam.cur" in data
    assert "Unavailiable.cur" in data
    assert "Alternate.cur" in data

    shutil.rmtree(d)

def test_WindowsPackager_with_website_url(

    tmpdir_factory: pytest.TempdirFactory,
) -> None:
    d = Path(tmpdir_factory.mktemp("test_image"))
    create_test_cursor(d, "Work.ani")
    create_test_cursor(d, "Busy.ani")
    create_test_cursor(d, "Default.cur")
    create_test_cursor(d, "Help.cur")
    create_test_cursor(d, "Link.cur")
    create_test_cursor(d, "Move.cur")
    create_test_cursor(d, "Diagonal_2.cur")
    create_test_cursor(d, "Vertical.cur")
    create_test_cursor(d, "Horizontal.cur")
    create_test_cursor(d, "Diagonal_1.cur")
    create_test_cursor(d, "Handwriting.cur")
    create_test_cursor(d, "Cross.cur")
    create_test_cursor(d, "IBeam.cur")
    create_test_cursor(d, "Unavailiable.cur")
    create_test_cursor(d, "Alternate.cur")

    WindowsPackager(d, theme_name="test", comment="testing", author="😎",website_url="testing.test")

    install_file = d / "install.inf"

    assert install_file.exists() is True
    data = install_file.read_text()

    assert "Work.ani" in data
    assert "Busy.ani" in data
    assert "Default.cur" in data
    assert "Help.cur" in data
    assert "Link.cur" in data
    assert "Move.cur" in data
    assert "Diagonal_2.cur" in data
    assert "Vertical.cur" in data
    assert "Horizontal.cur" in data
    assert "Diagonal_1.cur" in data
    assert "Handwriting.cur" in data
    assert "Cross.cur" in data
    assert "IBeam.cur" in data
    assert "Unavailiable.cur" in data
    assert "Alternate.cur" in data

    assert "testing.test" in data

    shutil.rmtree(d)