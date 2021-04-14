#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

import shutil
from pathlib import Path
from random import randint

import pytest
from clickgen.core import Bitmap, CursorAlias

from .utils import create_test_image


@pytest.fixture(scope="module")
def image_dir(tmpdir_factory: pytest.TempdirFactory):
    """Autoremoved directory for storing images, Using \
    ``TempdirFactory`` understood."""

    directory = Path(tmpdir_factory.mktemp("test_image"))
    yield directory
    shutil.rmtree(directory)


@pytest.fixture(scope="function")
def test_file(image_dir):
    """provide single test file named ``test.test``."""

    file: Path = image_dir / "test.test"
    file.write_text("testing")
    return file


@pytest.fixture(scope="function")
def static_png(image_dir):
    """provide single test image file with ``.png`` type."""

    p = create_test_image(image_dir, 1)
    return p[0]


@pytest.fixture(scope="function")
def animated_png(image_dir):
    """provide multiple test image file with ``.png`` type."""
    p = create_test_image(image_dir, randint(2, 5))

    return p


@pytest.fixture(scope="function")
def hotspot():
    """Mock hotspot tuple."""

    return (0, 0)


@pytest.fixture(scope="function")
def static_bitmap(static_png, hotspot):
    """Mock static bitmap instace."""

    return Bitmap(static_png, hotspot)


@pytest.fixture(scope="function")
def animated_bitmap(animated_png, hotspot):
    """Mock animated bitmap instace."""

    return Bitmap(animated_png, hotspot)


@pytest.fixture(scope="function")
def static_config(static_bitmap):
    """Mock static cursor config file."""
    alias = CursorAlias(static_bitmap)
    yield alias.create((10, 10))

    shutil.rmtree(alias.alias_dir)


@pytest.fixture(scope="function")
def animated_config(animated_bitmap):
    """Mock animated cursor config file."""

    alias = CursorAlias(animated_bitmap)
    yield alias.create((10, 10))

    shutil.rmtree(alias.alias_dir)


@pytest.fixture(scope="function")
def data():
    """Mock cursor data dict."""

    return [{"aa"}, {"bb", "cc"}, {"ddddd", "ffffff"}]
