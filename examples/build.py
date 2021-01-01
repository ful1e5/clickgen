from clickgen.builders.windows import WindowsCursor
import json
from pathlib import Path
from typing import Any, Dict, Tuple

from clickgen.core import CursorAlias
from clickgen.util import PNGProvider
from clickgen.builders.x11 import XCursor
from clickgen.packagers import XPackager

x_out_dir = Path("themes") / "xpro"
win_out_dir = Path("themes") / "xpro-windows"
png = PNGProvider("bitmaps")

DELAY: int = 10

# XCursor
X_SIZES = [(20, 20)]

# Windows Cursor
CANVAS_SIZE = (32, 32)
SIZE = (24, 24)


WIN_CURSORS_CFG: Dict[str, Dict[str, str]] = {
    "right_ptr.png": {"to": "Alternate", "position": "top_left"},
    "cross.png": {"to": "Cross"},
    "left_ptr.png": {"to": "Default", "position": "top_left"},
    "fd_double_arrow.png": {"to": "Diagonal_1"},
    "bd_double_arrow.png": {"to": "Diagonal_2"},
    "pencil.png": {"to": "Handwriting"},
    "help": {"to": "Help", "position.png": "top_left"},
    "sb_h_double_arrow.png": {"to": "Horizontal"},
    "xterm.png": {"to": "IBeam", "position": "top_left"},
    "hand2.png": {"to": "Link", "position": "top_left"},
    "hand1.png": {"to": "Move"},
    "circle.png": {"to": "Unavailiable", "position": "top_left"},
    "sb_v_double_arrow.png": {"to": "Vertical"},
    "wait": {"to": "Busy"},
    "left_ptr_watch": {"to": "Work", "position": "top_left"},
}

with open("data.json", "r") as f:
    data: Dict[str, Dict[str, int]] = json.loads(f.read())


config: Dict[str, Any] = {}

for key, item in data.items():
    x_hot: int = item.get("x_hot", 0)
    y_hot: int = item.get("y_hot", 0)
    hotspot: Tuple[int, int] = (x_hot, y_hot)

    delay: int = item.get("delay", DELAY)
    p = png.get(key)

    win_data = WIN_CURSORS_CFG.get(key)
    if not win_data:
        config[key] = {
            "png": p,
            "hotspot": hotspot,
            "delay": delay,
        }
    else:
        win_key = win_data.get("to")
        position = win_data.get("position", "center")
        config[key] = {
            "png": p,
            "hotspot": hotspot,
            "delay": delay,
            "win_key": win_key,
            "position": position,
        }

for key, item in config.items():
    also_windows: bool = False

    if item.get("win_key"):
        also_windows: bool = True

    png = item["png"]
    hotspot = item["hotspot"]
    delay = item["delay"]

    with CursorAlias.create_from(png, hotspot) as alias:
        x_cfg = alias.alias(X_SIZES, delay)
        XCursor.build_from(x_cfg, x_out_dir)

        if also_windows:
            position = item["position"]
            win_cfg = alias.reproduce(SIZE, CANVAS_SIZE, position)
            WindowsCursor.build_from(win_cfg, win_out_dir)

# XPackager(out_dir, theme_name="xpro", comment="Xcursor pro version")
