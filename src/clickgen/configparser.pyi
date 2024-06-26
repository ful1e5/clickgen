from clickgen.libs.colors import print_warning as print_warning
from clickgen.parser import open_blob as open_blob
from clickgen.parser.png import DELAY as DELAY, SIZES as SIZES
from clickgen.writer.windows import to_win as to_win
from clickgen.writer.x11 import to_x11 as to_x11
from pathlib import Path
from typing import Any, TypeVar

class ThemeSection:
    name: str
    comment: str
    website: str
    def __init__(self, name, comment, website) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_theme_section(d: dict[str, Any], **kwargs) -> ThemeSection: ...

class ConfigSection:
    bitmaps_dir: Path
    out_dir: Path
    platforms: list[str]
    def __init__(self, bitmaps_dir, out_dir, platforms) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_config_section(fp: Path, d: dict[str, Any], **kwargs) -> ConfigSection: ...
T = TypeVar('T')

class CursorSection:
    x11_cursor_name: str | None
    x11_cursor: bytes | None
    x11_symlinks: list[str]
    win_cursor_name: str | None
    win_cursor: bytes | None
    def __init__(self, x11_cursor_name, x11_cursor, x11_symlinks, win_cursor_name, win_cursor) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_cursors_section(d: dict[str, Any], config: ConfigSection, **kwargs) -> list[CursorSection]: ...

class ClickgenConfig:
    theme: ThemeSection
    config: ConfigSection
    cursors: list[CursorSection]
    def __init__(self, theme, config, cursors) -> None: ...
    def __lt__(self, other): ...
    def __le__(self, other): ...
    def __gt__(self, other): ...
    def __ge__(self, other): ...

def parse_toml_file(fp: Path, **kwargs) -> ClickgenConfig: ...
def parse_yaml_file(fp: Path, **kwargs) -> ClickgenConfig: ...
def parse_json_file(fp: Path, **kwargs) -> ClickgenConfig: ...
def parse_config_file(fp: Path, **kwargs) -> ClickgenConfig: ...
