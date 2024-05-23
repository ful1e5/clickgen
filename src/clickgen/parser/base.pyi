from abc import ABCMeta, abstractmethod
from clickgen.cursors import CursorFrame as CursorFrame
from typing import Any

class BaseParser(metaclass=ABCMeta):
    blob: bytes
    frames: list[CursorFrame]
    @abstractmethod
    def __init__(self, blob: bytes): ...
    @classmethod
    @abstractmethod
    def can_parse(cls, blob: Any) -> bool: ...
