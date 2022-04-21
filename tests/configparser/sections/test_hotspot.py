from clickgen.configparser.sections.hotspots import parse_hotspot_section


def test_parse_hotspot_section(cp):
    o = parse_hotspot_section(cp)
    assert isinstance(o["a"], tuple)
    assert o["a"] == (10, 10)
    assert isinstance(o["b"], tuple)
    assert o["b"] == (10, 10)
