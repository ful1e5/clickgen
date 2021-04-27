from pathlib import Path
from string import Template
from typing import Any, Optional

THEME_FILES_TEMPLATES: dict[str, Template]

def XPackager(directory: Path, theme_name: str, comment: str) -> None: ...

INSTALL_INF: Any
REQUIRED_WIN_CURSORS: set[str]

def WindowsPackager(directory: Path, theme_name: str, comment: str, author: str, website_url: Optional[str]=...) -> None: ...
