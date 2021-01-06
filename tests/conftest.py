#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from tempfile import mkdtemp
from typing import List

import pytest
from PIL import Image


def create_test_image(count: int, size=(20, 20)) -> List[Path]:
    tmp_dir = Path(mkdtemp())
    images: List[Path] = []

    for c in range(count):
        file = tmp_dir / f"test-{c}.png"
        Image.new(
            "RGBA",
            size=size,
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
        ).save(file, "png", compress=0)
        images.append(file)

    return images


@pytest.fixture(scope="module")
def static_png():
    p = create_test_image(1)
    return p[0]


@pytest.fixture(scope="module")
def animated_png():
    return create_test_image(randint(2, 5))
