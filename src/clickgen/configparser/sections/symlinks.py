from configparser import ConfigParser
from typing import Dict


def parse_symlinks_section(cp: ConfigParser) -> Dict[str, str]:
    d = cp["config.x11.symlinks"]
    result: Dict[str, str] = {}
    for key, value in d.items():
        result[key] = value
    return result
