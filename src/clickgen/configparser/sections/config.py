from configparser import ConfigParser
from dataclasses import dataclass
from pathlib import Path
from typing import List

from clickgen.configparser.utils import str_to_list


@dataclass
class ConfigSection:
    bitmaps_dir: Path
    out_dir: Path
    sizes: List[int]
    platforms: List[str]


def parse_config_section(cp: ConfigParser) -> ConfigSection:
    bitmaps_dir = Path(cp.get("config", "bitmaps"))
    out_dir = Path(cp.get("config", "out"))
    sizes = list(map(int, str_to_list(cp.get("config", "sizes"))))
    platforms = str_to_list(cp.get("config", "platforms"))

    return ConfigSection(bitmaps_dir, out_dir, sizes, platforms)
