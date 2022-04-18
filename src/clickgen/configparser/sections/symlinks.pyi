from clickgen.configparser.utils import str_to_list as str_to_list
from configparser import ConfigParser
from typing import Dict, List

def parse_symlinks_section(cp: ConfigParser) -> Dict[str, List[str]]: ...
