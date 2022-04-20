from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class ThemeSection:
    name: str
    comment: str
    website: str


def parse_theme_section(cp: ConfigParser) -> ThemeSection:
    name = cp.get("theme", "name")
    comment = cp.get("theme", "comment")
    website = cp.get("theme", "website")
    return ThemeSection(name, comment, website)
