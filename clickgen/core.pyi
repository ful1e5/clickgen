from PIL import Image
from clickgen.util import remove_util as remove_util
from pathlib import Path
from typing import Any, Optional, Union

Size = tuple[int, int]
LikePath = Union[str, Path]
LikePathList = Union[list[str], list[Path]]

class Bitmap:
    animated: bool
    png: Path
    grouped_png: list[Path]
    key: str
    x_hot: int
    y_hot: int
    size: tuple[int, int]
    width: int
    height: int
    compress: int = ...
    def __init__(self, png: Union[LikePath, LikePathList], hotspot: tuple[int, int]) -> None: ...
    def __enter__(self) -> Bitmap: ...
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None: ...
    def resize(self, size: Size, resample: int=..., save: bool=...) -> Optional[Union[Image.Image, list[Image.Image]]]: ...
    def reproduce(self, size: Size=..., canvas_size: Size=..., position: str=..., save: Any=...) -> Optional[Union[Image.Image, list[Image.Image]]]: ...
    def rename(self, key: str) -> None: ...
    def copy(self, path: Optional[LikePath]=...) -> Bitmap: ...

class CursorAlias:
    bitmap: Bitmap
    prefix: str
    alias_dir: Path
    alias_file: Path
    garbage_dirs: list[Path] = ...
    def __init__(self, bitmap: Bitmap) -> None: ...
    def __enter__(self) -> CursorAlias: ...
    def __exit__(self, exception_type: Any, exception_value: Any, traceback: Any) -> None: ...
    @classmethod
    def from_bitmap(cls: Any, png: Union[LikePath, LikePathList], hotspot: tuple[int, int]) -> CursorAlias: ...
    def create(self, sizes: Union[Size, list[Size]], delay: int=...) -> Path: ...
    def check_alias(self) -> None: ...
    def extension(self, ext: Optional[str]=...) -> Union[str, Path]: ...
    def copy(self, dst: Optional[LikePath]=...) -> CursorAlias: ...
    def rename(self, key: str) -> Path: ...
    def reproduce(self, size: Size=..., canvas_size: Size=..., position: str=..., delay: int=...) -> CursorAlias: ...
