from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class ConfigSection:
    bitmaps_dir: Path
    out_dir: Path
    sizes: List[int]
    platforms: List[str]


def parse_config_section(cp: ConfigParser) -> ConfigSection:
    bitmaps_dir = Path(cp.get("config", "bitmaps"))
    out_dir = Path(cp.get("config", "out"))
    sizes = list(map(int, cp.get("config", "sizes").split(",")))
    platforms = [x.strip(" ") for x in cp.get("config", "platforms").split(",")]

    return ConfigSection(bitmaps_dir, out_dir, sizes, platforms)
