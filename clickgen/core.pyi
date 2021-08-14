from PIL import Image
from clickgen.util import remove_util as remove_util
from pathlib import Path
from typing import List, Optional, Tuple, Union

Size = Tuple[int, int]
LikePath = Union[str, Path]
LikePathList = Union[List[str], List[Path]]

class Bitmap:
    animated: bool
    png: Path
    grouped_png: List[Path]
    key: str
    x_hot: int
    y_hot: int
    size: Tuple[int, int]
    width: int
    height: int
    compress: int
    def __init__(self, png: Union[LikePath, LikePathList], hotspot: Tuple[int, int]) -> None: ...
    def __enter__(self) -> Bitmap: ...
    def __exit__(self, exception_type, exception_value, traceback) -> None: ...
    def resize(self, size: Size, resample: int = ..., save: bool = ...) -> Optional[Union[Image.Image, List[Image.Image]]]: ...
    def reproduce(self, size: Size = ..., canvas_size: Size = ..., position: str = ..., save: bool = ...) -> Optional[Union[Image.Image, List[Image.Image]]]: ...
    def rename(self, key: str) -> None: ...
    def copy(self, path: Optional[LikePath] = ...) -> Bitmap: ...

class CursorAlias:
    bitmap: Bitmap
    prefix: str
    alias_dir: Path
    alias_file: Path
    garbage_dirs: List[Path]
    def __init__(self, bitmap: Bitmap) -> None: ...
    def __enter__(self) -> CursorAlias: ...
    def __exit__(self, exception_type, exception_value, traceback) -> None: ...
    @classmethod
    def from_bitmap(cls, png: Union[LikePath, LikePathList], hotspot: Tuple[int, int]) -> CursorAlias: ...
    def create(self, sizes: Union[Size, List[Size]], delay: int = ...) -> Path: ...
    def check_alias(self) -> None: ...
    def extension(self, ext: Optional[str] = ...) -> Union[str, Path]: ...
    def copy(self, dst: Optional[LikePath] = ...) -> CursorAlias: ...
    def rename(self, key: str) -> Path: ...
    def reproduce(self, size: Size = ..., canvas_size: Size = ..., position: str = ..., delay: int = ...) -> CursorAlias: ...
