from PIL.Image import Image as Image
from typing import Iterator

class CursorImage:
    image: Image
    hotspot: tuple[int, int]
    nominal: int
    re_canvas: bool
    def __init__(self, image: Image, hotspot: tuple[int, int], nominal: int, re_canvas: bool = False) -> None: ...

class CursorFrame:
    images: list[CursorImage]
    delay: int
    def __init__(self, images: list[CursorImage], delay: int = 0) -> None: ...
    def __getitem__(self, item: int) -> CursorImage: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> Iterator[CursorImage]: ...
