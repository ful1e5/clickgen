from pathlib import Path
from typing import Any, Dict, List, TypeVar, Union

import toml
from attr import dataclass

from clickgen.parser import open_blob
from clickgen.parser.png import DELAY
from clickgen.writer.windows import to_win
from clickgen.writer.x11 import to_x11


@dataclass
class ThemeSection:
    name: str
    comment: str
    website: str


def parse_toml_theme_section(d: Dict[str, Any], **kwargs) -> ThemeSection:
    t = d["theme"]
    return ThemeSection(
        name=kwargs.get("name", t["name"]),
        comment=kwargs.get("comment", t["comment"]),
        website=kwargs.get("website", t["website"]),
    )


@dataclass
class ConfigSection:
    bitmaps_dir: Path
    out_dir: Path
    platforms: List[str]
    x11_sizes: List[int]
    win_size: int


def parse_toml_config_section(fp: str, d: Dict[str, Any], **kwargs) -> ConfigSection:
    c = d["config"]
    p = Path(fp).parent

    def absolute_path(path: str) -> Path:
        if Path(path).is_absolute():
            return Path(path)
        return (p / path).absolute()

    return ConfigSection(
        bitmaps_dir=kwargs.get("bitmaps_dir", absolute_path(c["bitmaps_dir"])),
        out_dir=kwargs.get("out_dir", absolute_path(c["out_dir"])),
        platforms=kwargs.get("platforms", c["platforms"]),
        x11_sizes=kwargs.get("x11_sizes", c["x11_sizes"]),
        win_size=kwargs.get("win_size", c["win_size"]),
    )


T = TypeVar("T")


@dataclass
class CursorSection:
    x11_cursor_name: str
    x11_cursor: bytes
    x11_symlinks: List[str]
    win_cursor_name: Union[str, None]
    win_cursor: Union[bytes, None]


def parse_toml_cursors_section(
    d: Dict[str, Any], config: ConfigSection
) -> List[CursorSection]:
    result: List[CursorSection] = []

    fb = d["cursors"]["fallback_settings"]
    del d["cursors"]["fallback_settings"]

    def get_value_with_fallback(key: str, deflt: T) -> T:
        return v.get(key, fb.get(key, deflt))

    for _, v in d["cursors"].items():
        hotspot = (
            get_value_with_fallback("x_hotspot", 0),
            get_value_with_fallback("y_hotspot", 0),
        )
        x11_delay = get_value_with_fallback("x11_delay", DELAY)
        win_delay = get_value_with_fallback("win_delay", DELAY)

        blobs = [f.read_bytes() for f in sorted(config.bitmaps_dir.glob(v["png"]))]

        x11_blob = open_blob(blobs, hotspot, config.x11_sizes, x11_delay)
        x11_cursor = to_x11(x11_blob.frames)

        # Because all cursors don't have windows configuration
        win_cursor: Union[bytes, None] = None
        win_cursor_name: Union[str, None] = None
        if "win_name" in v:
            win_blob = open_blob(blobs, hotspot, [config.win_size], win_delay)
            ext, win_cursor = to_win(win_blob.frames)
            win_cursor_name = v["win_name"] + ext

        result.append(
            CursorSection(
                x11_cursor=x11_cursor,
                x11_cursor_name=v["x11_name"],
                x11_symlinks=v.get("x11_symlinks", []),
                win_cursor=win_cursor,
                win_cursor_name=win_cursor_name,
            )
        )

    return result


@dataclass
class ClickgenConfig:
    theme: ThemeSection
    config: ConfigSection
    cursors: List[CursorSection]


def parse_toml_file(fp: str, **kwargs) -> ClickgenConfig:
    d: Dict[str, Any] = toml.load(fp)
    theme = parse_toml_theme_section(d, **kwargs)
    config = parse_toml_config_section(fp, d, **kwargs)
    cursors = parse_toml_cursors_section(d, config)

    return ClickgenConfig(theme, config, cursors)
