#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import io
from typing import List, Optional, Tuple, Union

from PIL import Image

from clickgen.cursors import CursorFrame, CursorImage
from clickgen.parser.base import BaseParser

SIZES = [16, 20, 22, 24, 28, 32, 40, 48, 56, 64, 72, 80, 88, 96]
DELAY = 0


class SinglePNGParser(BaseParser):
    MAGIC = bytes.fromhex("89504e47")

    @classmethod
    def can_parse(cls, blob: bytes) -> bool:
        return blob[: len(cls.MAGIC)] == cls.MAGIC

    def __init__(
        self,
        blob: bytes,
        hotspot: Tuple[int, int],
        sizes: Optional[List[Union[int, str]]] = None,
        delay: Optional[int] = None,
    ) -> None:
        super().__init__(blob)
        self._image = Image.open(io.BytesIO(self.blob))

        # 'set' to prevent value duplication
        if not sizes:
            self.sizes = set(SIZES)
        else:
            self.sizes = set(sizes)

        if not delay:
            self.delay = DELAY
        else:
            self.delay = delay

        if hotspot[0] > self._image.size[0]:
            raise ValueError(f"Hotspot x-coordinate too large: {hotspot[0]}")
        if hotspot[1] > self._image.size[1]:
            raise ValueError(f"Hotspot x-coordinate too large: {hotspot[1]}")
        self.hotspot = hotspot

        self.frames = self._parse()

    def _cal_hotspot(self, res_img: Image.Image) -> Tuple[int, int]:
        def _dim(i: int) -> int:
            return int((self.hotspot[i] * (res_img.size[i] / self._image.size[i])))

        return _dim(0), _dim(1)

    def _parse(self) -> List[CursorFrame]:
        images: List[CursorImage] = []
        for s in sorted(self.sizes):
            size: int = 0
            canvas_size: int = 0

            if isinstance(s, str):
                try:
                    if ":" in s:
                        size_str, canvas_size_str = s.split(":")
                        size = int(size_str)
                        canvas_size = int(canvas_size_str)
                    else:
                        size = int(s)
                        canvas_size = size
                except ValueError:
                    raise ValueError(
                        f"'sizes' input '{s}' must be an integer or integers separated by ':'."
                    )
            elif isinstance(s, int):
                size = s
                canvas_size = s
            else:
                raise TypeError(
                    "Input must be 'cursor_size:canvas_size' or an integer."
                )

            res_img = self._image.resize((size, size), 1)

            if size != canvas_size:
                canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
                canvas.paste(res_img, (0, 0))
                res_img = canvas

            res_hotspot = self._cal_hotspot(res_img)
            images.append(
                CursorImage(
                    image=res_img,
                    hotspot=res_hotspot,
                    nominal=canvas_size,
                    re_canvas=size != canvas_size,
                )
            )

        return [CursorFrame(images, delay=self.delay)]


class MultiPNGParser(BaseParser):
    @classmethod
    def can_parse(cls, blobs: List[bytes]) -> bool:
        checks: List[bool] = []
        for blob in blobs:
            checks.append(SinglePNGParser.can_parse(blob))
        return all(checks)

    def __init__(
        self,
        blobs: List[bytes],
        hotspot: Tuple[int, int],
        sizes: Optional[List[Union[int, str]]] = None,
        delay: Optional[int] = None,
    ) -> None:
        super().__init__(blobs[0])
        self.frames = []
        for blob in blobs:
            png = SinglePNGParser(blob, hotspot, sizes, delay)
            self.frames.append(png.frames[0])
