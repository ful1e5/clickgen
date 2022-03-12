from clickgen.db import CursorDB as CursorDB, DATA as DATA
from pathlib import Path
from typing import List, Union

def chdir(directory: Union[str, Path]): ...
def remove_util(p: Union[str, Path]) -> None: ...

class PNGProvider:
    bitmaps_dir: Path
    def __init__(self, bitmaps_dir: Union[str, Path]) -> None: ...
    def get(self, key: str) -> Union[List[Path], Path]: ...

def add_missing_xcursors(directory: Path, data: List = ..., rename: bool = ..., force: bool = ...) -> None: ...