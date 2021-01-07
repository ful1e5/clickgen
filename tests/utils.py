#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from random import randint
from typing import List

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
