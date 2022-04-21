from clickgen.configparser.sections.config import ConfigSection, parse_config_section as parse_config_section
from clickgen.configparser.sections.hotspots import parse_hotspot_section as parse_hotspot_section
from clickgen.configparser.sections.symlinks import parse_symlinks_section as parse_symlinks_section
from clickgen.configparser.sections.theme import ThemeSection, parse_theme_section as parse_theme_section
from configparser import ConfigParser
from typing import Dict, List, Tuple

class ClickgenConfig:
    theme: ThemeSection
    config: ConfigSection
    hotspots: Dict[str, Tuple[int, int]]
    symlinks: Dict[str, List[str]]
    def __init__(self, theme, config, hotspots, symlinks) -> None: ...

def parse_sections(cp: ConfigParser) -> ClickgenConfig: ...
