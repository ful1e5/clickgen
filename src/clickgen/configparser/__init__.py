import configparser

from clickgen.configparser.sections import ClickgenConfig, parse_sections

__all__ = ["parse_config_file", "ClickgenConfig"]


def parse_config_file(fp: str) -> ClickgenConfig:
    config = configparser.ConfigParser()
    config.read(fp)
    return parse_sections(config)
