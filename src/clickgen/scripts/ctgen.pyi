from clickgen.configparser import parse_config_file as parse_config_file
from clickgen.libs.colors import blue as blue, bold as bold, cyan as cyan, fail as fail, magenta as magenta, print_done as print_done, print_info as print_info, print_subtext as print_subtext, print_text as print_text, yellow as yellow
from clickgen.packer.windows import pack_win as pack_win
from clickgen.packer.x11 import pack_x11 as pack_x11
from typing import Any, Dict, Generator

def get_kwargs(args) -> Dict[str, Any]: ...
def cwd(path) -> Generator[None, None, None]: ...
def main() -> None: ...
