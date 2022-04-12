from configparser import ConfigParser
from dataclasses import dataclass
from typing import Dict, List, Tuple

from clickgen.configparser.sections.config import ConfigSection, parse_config_section
from clickgen.configparser.sections.hotspots import parse_hotspot_section
from clickgen.configparser.sections.symlinks import parse_symlinks_section
from clickgen.configparser.sections.theme import ThemeSection, parse_theme_section

__all__ = [
    "parse_sections",
    "parse_theme_section",
    "parse_config_section",
    "parse_hotspot_section",
    "parse_symlinks_section",
]


@dataclass
class ClickgenConfig:
    theme: ThemeSection
    config: ConfigSection
    hotspots: Dict[str, Tuple[int, int]]
    symlinks: Dict[str, List[str]]


def parse_sections(cp: ConfigParser) -> ClickgenConfig:
    theme = parse_theme_section(cp)
    config = parse_config_section(cp)
    hotspots = parse_hotspot_section(cp)
    symlinks = parse_symlinks_section(cp)
    return ClickgenConfig(theme, config, hotspots, symlinks)
