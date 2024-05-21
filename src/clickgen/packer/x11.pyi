from pathlib import Path
from string import Template

FILE_TEMPLATES: dict[str, Template]

def pack_x11(dir: Path, theme_name: str, comment: str) -> None: ...
