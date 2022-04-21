#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
from typing import Any, List

from clickgen.cursors import CursorFrame


class BaseParser(metaclass=ABCMeta):
    blob: bytes
    frames: List[CursorFrame]

    @abstractmethod
    def __init__(self, blob: bytes) -> None:
        self.blob = blob

    @classmethod
    @abstractmethod
    def can_parse(cls, blob: Any) -> bool:
        raise NotImplementedError()
