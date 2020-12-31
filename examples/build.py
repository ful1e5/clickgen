import json
from pathlib import Path
from typing import Dict, Tuple

from clickgen.core import CursorAlias
from clickgen.util import PNGProvider
from clickgen.builders.x11 import XCursor
from clickgen.packagers import XPackager

out_dir = Path("themes") / "xpro"
png = PNGProvider("bitmaps")

SIZES = [(20, 20)]
DELAY: int = 10

with open("data.json", "r") as f:
    data: Dict[str, Dict[str, int]] = json.loads(f.read())


for key, data in data.items():
    hotspot: Tuple[int, int] = (data["xhot"], data["yhot"])

    try:
        delay = data["delay"]
    except KeyError:
        delay = DELAY

    p = png.get(key)

    with CursorAlias.create_from(p, hotspot) as alias:
        config_file = alias.alias(SIZES, delay)
        XCursor.build_from(config_file, out_dir)

    XPackager(out_dir, theme_name="xpro", comment="Xcursor pro version")
