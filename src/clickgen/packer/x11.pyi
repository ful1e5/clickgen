from pathlib import Path
from string import Template
from typing import Dict

FILE_TEMPLATES: Dict[str, Template]

def pack_x11(dir: Path, theme_name: str, comment: str) -> None: ...
