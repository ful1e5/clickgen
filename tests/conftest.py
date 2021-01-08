#!/usr/bin/env python
# -*- coding: utf-8 -*-

import shutil
from pathlib import Path
from random import randint

import pytest

from .utils import create_test_image


@pytest.fixture(scope="module")
def image_dir(tmpdir_factory: pytest.TempdirFactory):
    dir = Path(tmpdir_factory.mktemp("test_image"))
    yield dir
    shutil.rmtree(dir)


@pytest.fixture(scope="function")
def test_file(image_dir):
    file: Path = image_dir / "test.test"
    file.write_text("testing")
    return file


@pytest.fixture(scope="function")
def static_png(image_dir):
    p = create_test_image(image_dir, 1)
    return p[0]


@pytest.fixture(scope="function")
def animated_png(image_dir):
    p = create_test_image(image_dir, randint(2, 5))
    return p


@pytest.fixture(scope="function")
def hotspot():
    return (0, 0)
