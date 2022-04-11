from configparser import ConfigParser
from typing import Dict, Tuple


def parse_hotspot_section(cp: ConfigParser) -> Dict[str, Tuple[int, int]]:
    d = cp["config.hotspots"]
    result: Dict[str, Tuple[int, int]] = {}
    for key, value in d.items():
        hotspot = tuple(int(k.strip()) for k in value[1:-1].split(","))
        result[key] = hotspot
    return result
