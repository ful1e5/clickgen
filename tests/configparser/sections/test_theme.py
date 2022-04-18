from clickgen.configparser.sections.theme import parse_theme_section


def test_parse_theme_section(cp):
    o = parse_theme_section(cp)
    assert o.name == "Sample"
    assert o.author == "Sam"
    assert o.comment == "This is sample cursor theme"
    assert o.website == "https://www.example.com/"
