#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
import tempfile
from os import getcwd, symlink
from pathlib import Path

import pytest
from clickgen import util
from clickgen.util import PNGProvider, chdir

from tests.utils import create_test_image


def test_chdir() -> None:
    current = getcwd()
    with chdir(tempfile.tempdir):
        assert tempfile.tempdir == getcwd()
    assert getcwd() == current


def test_remove_util() -> None:
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_file = Path(tempfile.mkstemp()[1])
    tmp_link = tmp_dir / "link"
    symlink(tmp_file, tmp_link)

    util.remove_util(tmp_dir)
    assert tmp_dir.exists() is False

    util.remove_util(tmp_file)
    assert tmp_file.exists() is False

    util.remove_util(tmp_link)
    assert tmp_link.exists() is False


def test_PNGProvider_exception(tmpdir_factory: pytest.TempdirFactory) -> None:
    directory = Path(tmpdir_factory.mktemp("tt"))
    with pytest.raises(FileNotFoundError) as excinfo:
        PNGProvider(directory)
    assert str(excinfo.value) == f"'*.png' files not found in '{directory.absolute()}'"
    shutil.rmtree(directory)


def test_PNGProvider(image_dir) -> None:
    create_test_image(image_dir, 3)
    p = PNGProvider(image_dir)
    p_str = PNGProvider(str(image_dir))
    assert p.bitmaps_dir == p_str.bitmaps_dir


def test_PNGProvider_get(tmpdir_factory: pytest.TempdirFactory) -> None:
    d = tmpdir_factory.mktemp("ffff")
    directory = Path(d)

    # static
    images = create_test_image(directory, 1, key="static")
    p = PNGProvider(directory)
    assert p.get("static") == images[0]

    # animated
    images1 = create_test_image(directory, 4, key="animated")
    p1 = PNGProvider(directory)
    assert sorted(p1.get("animated")) == sorted(images1)

    shutil.rmtree(d)
