#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from typing import List

from PIL import Image


def create_test_image(
    directory: Path, count: int, size=(20, 20), key: str = "test"
) -> List[Path]:
    images: List[Path] = []
    for c in range(count):
        file = directory / f"{key}-{c}.png"
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
    file = directory / name
    i = Image.new(
        "RGBA",
        size=(2, 2),
        color=(randint(0, 255), randint(0, 255), randint(0, 255)),
    )
    i.save(file, "png", compress=0)
    i.close()
    return file