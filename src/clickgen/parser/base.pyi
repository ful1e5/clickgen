from abc import ABCMeta, abstractmethod
from typing import List
from wxcursors.cursors import CursorFrame as CursorFrame

class BaseParser(metaclass=ABCMeta):
    blob: bytes
    frames: List[CursorFrame]
    @abstractmethod
    def __init__(self, blob: bytes): ...
    @classmethod
    @abstractmethod
    def can_parse(cls, blob: bytes) -> bool: ...
