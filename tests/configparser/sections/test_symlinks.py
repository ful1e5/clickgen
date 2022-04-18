from clickgen.configparser.sections.symlinks import parse_symlinks_section


def test_parse_symlinks_section(cp):
    o = parse_symlinks_section(cp)

    assert isinstance(o["a"], list)
    assert o["a"] == ["c"]

    assert isinstance(o["b"], list)
    assert o["b"] == ["d", "e", "f"]
