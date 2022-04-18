from clickgen.configparser import parse_config_file
from clickgen.configparser.sections import ClickgenConfig


def test_parse_config_file(cp_path):
    o = parse_config_file(cp_path)
    assert isinstance(o, ClickgenConfig)
