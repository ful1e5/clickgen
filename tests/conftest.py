from typing import List, Tuple

import pytest
from PIL.Image import Image

from clickgen.cursors import CursorFrame, CursorImage


@pytest.fixture
def image() -> Image:
    return Image()


@pytest.fixture
def hotspot() -> Tuple[int, int]:
    return (0, 0)


@pytest.fixture
def nominal() -> int:
    return 24


@pytest.fixture
def cursor_image(image, hotspot, nominal) -> CursorImage:
    return CursorImage(image, hotspot, nominal)


@pytest.fixture
def images(cursor_image) -> List[CursorImage]:
    return [cursor_image, cursor_image, cursor_image]


@pytest.fixture
def delay() -> int:
    return 5


@pytest.fixture
def cursor_frame(images, delay) -> CursorFrame:
    return CursorFrame(images, delay)
