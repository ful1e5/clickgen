from abc import ABCMeta, abstractmethod
from clickgen.cursors import CursorFrame as CursorFrame
from typing import Any, List

class BaseParser(metaclass=ABCMeta):
    blob: bytes
    frames: List[CursorFrame]
    @abstractmethod
    def __init__(self, blob: bytes): ...
    @classmethod
    @abstractmethod
    def can_parse(cls, blob: Any) -> bool: ...
