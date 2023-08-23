#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TypeVar, Union

import toml
import yaml
from attr import dataclass

from clickgen.libs.colors import print_warning
from clickgen.parser import open_blob
from clickgen.parser.png import DELAY, SIZES
from clickgen.writer.windows import to_win
from clickgen.writer.x11 import to_x11


@dataclass
class ThemeSection:
    name: str
    comment: str
    website: str


def parse_theme_section(d: Dict[str, Any], **kwargs) -> ThemeSection:
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


def parse_config_section(fp: str, d: Dict[str, Any], **kwargs) -> ConfigSection:
    c = d["config"]
    p = Path(fp).parent

    def absolute_path(path: str) -> Path:
        if Path(path).is_absolute():
            return Path(path)
        return (p / path).absolute()

    # Deprecation
    deprecated_opts = {"win_size": "win_sizes", "x11_sizes": "x11_sizes"}
    for opt in deprecated_opts:
        if c.get(opt):
            print_warning(
                f"The '{opt}' option is deprecated."
                f" Please use '{deprecated_opts.get(opt)}' within individual cursor settings or set it to '[cursor.fallback_settings]'."
                " For more information, visit: https://github.com/ful1e5/clickgen/discussions/59#discussioncomment-6747666"
            )

    return ConfigSection(
        bitmaps_dir=kwargs.get("bitmaps_dir", absolute_path(c["bitmaps_dir"])),
        out_dir=kwargs.get("out_dir", absolute_path(c["out_dir"])),
        platforms=kwargs.get("platforms", c["platforms"]),
    )


T = TypeVar("T")


@dataclass
class CursorSection:
    x11_cursor_name: str
    x11_cursor: bytes
    x11_symlinks: List[str]
    win_cursor_name: Union[str, None]
    win_cursor: Union[bytes, None]


def parse_cursors_section(
    d: Dict[str, Any], config: ConfigSection, **kwargs
) -> List[CursorSection]:
    def get_value(k: str, def_val: Optional[T] = None) -> T:
        return kwargs.get(k, v.get(k, fb.get(k, def_val)))

    def size_typing(s: Union[int, List[int]]) -> List[int]:
        if isinstance(s, int):
            return [s]
        elif isinstance(s, List):
            return s

    result: List[CursorSection] = []

    fb = d["cursors"]["fallback_settings"]
    del d["cursors"]["fallback_settings"]

    for _, v in d["cursors"].items():
        hotspot = (
            get_value("x_hotspot"),
            get_value("y_hotspot"),
        )
        x11_delay = get_value("x11_delay", DELAY)
        win_delay = get_value("win_delay", DELAY)

        x11_sizes = size_typing(get_value("x11_sizes", SIZES))
        win_sizes = size_typing(get_value("win_sizes", SIZES))

        blobs = [f.read_bytes() for f in sorted(config.bitmaps_dir.glob(v["png"]))]

        x11_blob = open_blob(blobs, hotspot, x11_sizes, x11_delay)
        x11_cursor = to_x11(x11_blob.frames)

        # Because all cursors don't have windows configuration
        win_cursor: Union[bytes, None] = None
        win_cursor_name: Union[str, None] = None
        if "win_name" in v:
            win_blob = open_blob(blobs, hotspot, win_sizes, win_delay)
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
    theme = parse_theme_section(d, **kwargs)
    config = parse_config_section(fp, d, **kwargs)
    cursors = parse_cursors_section(d, config, **kwargs)

    return ClickgenConfig(theme, config, cursors)


def parse_yaml_file(fp: str, **kwargs) -> ClickgenConfig:
    d: Dict[str, Any] = {}

    with open(fp, "r") as file:
        d = yaml.safe_load(file)

    theme = parse_theme_section(d, **kwargs)
    config = parse_config_section(fp, d, **kwargs)
    cursors = parse_cursors_section(d, config, **kwargs)

    return ClickgenConfig(theme, config, cursors)


def parse_json_file(fp: str, **kwargs) -> ClickgenConfig:
    d: Dict[str, Any] = {}

    with open(fp, "r") as file:
        d = json.load(file)

    theme = parse_theme_section(d, **kwargs)
    config = parse_config_section(fp, d, **kwargs)
    cursors = parse_cursors_section(d, config, **kwargs)

    return ClickgenConfig(theme, config, cursors)


def parse_config_file(fp: str, **kwargs) -> ClickgenConfig:
    ext = fp.split(".")[1]
    config: ClickgenConfig

    if ext == "yml" or ext == "yaml":
        config = parse_yaml_file(fp, **kwargs)
    elif ext == "json":
        config = parse_json_file(fp, **kwargs)
    elif ext == "toml":
        config = parse_toml_file(fp, **kwargs)
    else:
        raise IOError("Configuration File type is not supported")

    return config
