from configparser import ConfigParser

class ThemeSection:
    name: str
    comment: str
    website: str
    def __init__(self, name, comment, website) -> None: ...

def parse_theme_section(cp: ConfigParser) -> ThemeSection: ...
