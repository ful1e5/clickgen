from configparser import ConfigParser
from pathlib import Path
from typing import List

class ConfigSection:
    bitmaps_dir: Path
    out_dir: Path
    sizes: List[int]
    platforms: List[str]
    def __init__(self, bitmaps_dir, out_dir, sizes, platforms) -> None: ...

def parse_config_section(cp: ConfigParser) -> ConfigSection: ...
