from pathlib import Path

from clickgen.configparser.sections.config import parse_config_section


def test_parse_config_section(cp):
    o = parse_config_section(cp)
    assert isinstance(o.bitmaps_dir, Path)
    assert isinstance(o.out_dir, Path)
    assert o.sizes == [22, 24, 28, 32, 40, 48, 56, 64, 72, 80, 88, 96]
    assert o.platforms == ["windows", "x11"]
