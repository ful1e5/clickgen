from configparser import ConfigParser
from typing import Dict, List


def parse_symlinks_section(cp: ConfigParser) -> Dict[str, List[str]]:
    d = cp["config.x11.symlinks"]
    result: Dict[str, List[str]] = {}
    for key, value in d.items():
        result[key] = value.split(",")
    return result
