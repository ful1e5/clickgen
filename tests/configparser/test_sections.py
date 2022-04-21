from clickgen.configparser.sections import ClickgenConfig, parse_sections
from clickgen.configparser.sections.config import ConfigSection
from clickgen.configparser.sections.theme import ThemeSection


def test_parse_sections(cp):
    o = parse_sections(cp)
    assert isinstance(o, ClickgenConfig)
    assert isinstance(o.theme, ThemeSection)
    assert isinstance(o.config, ConfigSection)
    assert isinstance(o.hotspots, dict)
    assert isinstance(o.symlinks, dict)
