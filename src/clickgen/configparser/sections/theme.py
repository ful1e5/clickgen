from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class ThemeSection:
    name: str
    comment: str
    author: str
    website: str


def parse_theme_section(cp: ConfigParser) -> ThemeSection:
    name = cp.get("theme", "name")
    comment = cp.get("theme", "comment")
    author = cp.get("theme", "author")
    website = cp.get("theme", "website")
    return ThemeSection(name, comment, author, website)
