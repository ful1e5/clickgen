#!/usr/bin/env python
# -*- coding: utf-8 -*-

from os import PathLike
from pathlib import Path
from random import randint
from tempfile import mkdtemp
from typing import List, Union

import pytest
from clickgen.core import LikePath
from PIL import Image


def create_test_image(count: int, return_Path: bool) -> Union[List[LikePath], LikePath]:

    tmp_dir = Path(mkdtemp())

    def __create(name: str) -> LikePath:
        file = tmp_dir / name
        image = Image.new(
            "RGBA",
            size=(200, 200),
            color=(randint(0, 255), randint(0, 255), randint(0, 255)),
        )
        image.save(file, "png", compress=0)

        if not return_Path:
            return str(file.absolute())
        return file

    if count == 1:
        return __create("test.png")
    else:
        l: List[PathLike] = []
        while count == 0:
            __create(f"test-{count}.png")
            count -= count
        return l


@pytest.fixture(scope="module")
def static_png_as_Path():
    return create_test_image(1, True)


@pytest.fixture(scope="module")
def animated_png_as_Path():
    return create_test_image(randint(1, 20), True)


@pytest.fixture(scope="module")
def static_png_as_str():
    return create_test_image(1, False)


@pytest.fixture(scope="module")
def animated_png_as_str():
    return create_test_image(randint(1, 20), False)
