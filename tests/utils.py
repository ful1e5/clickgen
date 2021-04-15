#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from typing import List

from PIL import Image


def create_test_image(
    directory: Path, count: int, size=(20, 20), key: str = "test"
) -> List[Path]:
    """Create test ``.png`` image file with random color.

    :param directory: Directory where test image will stored.
    :type directory: pathlib.Path

    :param count: Count of images you wants to generate.
    :type count: int

    :param key: Name of the image without extension. More than \
            one images will prefix by number. *(default is **test**)*
    :type key: str
    """

    images: List[Path] = []
    for i in range(count):
        file = directory / f"{key}-{i}.png"
        i = Image.new(
            "RGBA",
            size=size,
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        i.save(file, "png", compress=0)
        i.close()
        images.append(file)
    return images


def create_test_cursor(directory: Path, name: str = "test.png") -> Path:
    """Generate the test cursor file.

    :param directory: Directory where test image will stored.
    :type directory: pathlib.Path

    :param name: Name of the image without extension. More than \
            one images will prefix by number. *(default is **test**)*
    :type name: str
    """

    file = directory / name
    i = Image.new(
        "RGBA",
        size=(2, 2),
        color=(randint(0, 255), randint(0, 255), randint(0, 255)),
    )
    i.save(file, "png", compress=0)
    i.close()
    return file
