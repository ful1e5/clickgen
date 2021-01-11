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
        i = Image.new(
            "RGBA",
            size=size,
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        i.save(file, "png", compress=0)
        i.close()
        images.append(file)
    return images
