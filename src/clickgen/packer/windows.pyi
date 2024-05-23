from _typeshed import Incomplete
from pathlib import Path
from string import Template

FILE_TEMPLETES: dict[str, Template]
all_wreg: Incomplete

def pack_win(dir: Path, theme_name: str, comment: str, website: str | None = None) -> None: ...
