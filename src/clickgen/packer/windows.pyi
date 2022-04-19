from pathlib import Path
from string import Template
from typing import Dict, Optional, Set

FILE_TEMPLATES: Dict[str, Template]
REQUIRED_CURSORS: Set[str]

def pack_win(dir: Path, theme_name: str, comment: str, website: Optional[str] = ...) -> None: ...
