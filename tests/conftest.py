#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from typing import List

import pytest
from PIL import Image


def create_test_image(dir: Path, count: int, size=(20, 20)) -> List[Path]:
    images: List[Path] = []
    for c in range(count):
        file = dir / f"test-{c}.png"
        Image.new(
            "RGBA",
            size=size,
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
        ).save(file, "png", compress=0)
        images.append(file)
    return images


@pytest.fixture(scope="session")
def image_dir(tmpdir_factory: pytest.TempdirFactory):
    return Path(tmpdir_factory.mktemp("test_image"))


@pytest.fixture(scope="module")
def test_file(image_dir):
    file: Path = image_dir / "test.test"
    file.write_text("testing")
    return file


@pytest.fixture(scope="module")
def static_png(image_dir):
    p = create_test_image(image_dir, 1)
    return p[0]


@pytest.fixture(scope="module")
def animated_png(image_dir):
    p = create_test_image(image_dir, randint(2, 5))
    return p
