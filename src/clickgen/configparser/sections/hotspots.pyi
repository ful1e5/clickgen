from configparser import ConfigParser
from typing import Dict, Tuple

def parse_hotspot_section(cp: ConfigParser) -> Dict[str, Tuple[int, int]]: ...
