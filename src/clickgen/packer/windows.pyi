from _typeshed import Incomplete
from pathlib import Path
from string import Template
from typing import Dict, Optional

FILE_TEMPLETES: Dict[str, Template]
all_wreg: Incomplete

def pack_win(dir: Path, theme_name: str, comment: str, website: Optional[str] = ...) -> None: ...
