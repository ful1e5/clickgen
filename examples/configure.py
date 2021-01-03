#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Any, Dict, List, Tuple, Union

from clickgen.util import PNGProvider

# XCursor
X_DELAY: int = 10

# Windows Cursor
CANVAS_SIZE = (32, 32)
SIZE = (24, 24)
WIN_DELAY = 3

X_CURSORS_CFG: Dict[str, Dict[str, int]] = {
    #
    # Static
    #
    "dotbox.png": {"xhot": 100, "yhot": 100},
    "move.png": {"xhot": 100, "yhot": 100},
    "plus.png": {"xhot": 100, "yhot": 100},
    "vertical_text.png": {"xhot": 100, "yhot": 100},
    "wayland_cursor.png": {"xhot": 100, "yhot": 100},
    "x_cursor.png": {"xhot": 100, "yhot": 100},
    "xterm.png": {"xhot": 100, "yhot": 100},
    "bd_double_arrow.png": {"xhot": 98, "yhot": 100},
    "fd_double_arrow.png": {"xhot": 98, "yhot": 100},
    "bottom_left_corner.png": {"xhot": 31, "yhot": 172},
    "bottom_right_corner.png": {"xhot": 170, "yhot": 172},
    "bottom_side.png": {"xhot": 100, "yhot": 164},
    "bottom_tee.png": {"xhot": 100, "yhot": 164},
    "center_ptr.png": {"xhot": 98, "yhot": 131},
    "circle.png": {"xhot": 48, "yhot": 25},
    "context_menu.png": {"xhot": 48, "yhot": 25},
    "copy.png": {"xhot": 48, "yhot": 25},
    "link.png": {"xhot": 48, "yhot": 25},
    "pointer_move.png": {"xhot": 48, "yhot": 25},
    "cross.png": {"xhot": 98, "yhot": 96},
    "crossed_circle.png": {"xhot": 100, "yhot": 100},
    "crosshair.png": {"xhot": 99, "yhot": 99},
    "dnd_ask.png": {"xhot": 86, "yhot": 79},
    "dnd_copy.png": {"xhot": 86, "yhot": 79},
    "dnd_link.png": {"xhot": 86, "yhot": 79},
    "dnd_move.png": {"xhot": 86, "yhot": 79},
    "dnd_no_drop.png": {"xhot": 86, "yhot": 79},
    "dnd_none.png": {"xhot": 99, "yhot": 98},
    "grabbing.png": {"xhot": 106, "yhot": 79},
    "hand1.png": {"xhot": 113, "yhot": 95},
    "hand2.png": {"xhot": 88, "yhot": 32},
    "left_ptr.png": {"xhot": 53, "yhot": 36},
    "left_side.png": {"xhot": 35, "yhot": 100},
    "left_tee.png": {"xhot": 165, "yhot": 95},
    "ll_angle.png": {"xhot": 34, "yhot": 165},
    "lr_angle.png": {"xhot": 167, "yhot": 164},
    "pencil.png": {"xhot": 37, "yhot": 161},
    "question_arrow.png": {"xhot": 102, "yhot": 102},
    "right_ptr.png": {"xhot": 150, "yhot": 29},
    "right_side.png": {"xhot": 163, "yhot": 98},
    "right_tee.png": {"xhot": 30, "yhot": 96},
    "sb_down_arrow.png": {"xhot": 100, "yhot": 126},
    "sb_h_double_arrow.png": {"xhot": 100, "yhot": 100},
    "sb_v_double_arrow.png": {"xhot": 100, "yhot": 100},
    "sb_left_arrow.png": {"xhot": 86, "yhot": 100},
    "sb_right_arrow.png": {"xhot": 113, "yhot": 100},
    "sb_up_arrow.png": {"xhot": 99, "yhot": 86},
    "tcross.png": {"xhot": 98, "yhot": 100},
    "top_left_corner.png": {"xhot": 29, "yhot": 27},
    "top_right_corner.png": {"xhot": 170, "yhot": 28},
    "top_side.png": {"xhot": 98, "yhot": 34},
    "top_tee.png": {"xhot": 98, "yhot": 29},
    "ul_angle.png": {"xhot": 34, "yhot": 35},
    "ur_angle.png": {"xhot": 164, "yhot": 34},
    "zoom_in.png": {"xhot": 90, "yhot": 89},
    "zoom_out.png": {"xhot": 93, "yhot": 90},
    #
    # Animated
    #
    # Note: Animated cursors not need any extension & frames number
    "left_ptr_watch": {"xhot": 50, "yhot": 28, "delay": 20},
    "wait": {"xhot": 100, "yhot": 100, "delay": 20},
}

WIN_CURSORS_CFG: Dict[str, Dict[str, str]] = {
    #
    # Static
    #
    "right_ptr.png": {"to": "Alternate", "position": "top_left"},
    "cross.png": {"to": "Cross"},
    "left_ptr.png": {"to": "Default", "position": "top_left"},
    "fd_double_arrow.png": {"to": "Diagonal_1"},
    "bd_double_arrow.png": {"to": "Diagonal_2"},
    "pencil.png": {"to": "Handwriting"},
    "question_arrow.png": {"to": "Help", "position.png": "top_left"},
    "sb_h_double_arrow.png": {"to": "Horizontal"},
    "xterm.png": {"to": "IBeam", "position": "top_left"},
    "hand2.png": {"to": "Link", "position": "top_left"},
    "hand1.png": {"to": "Move"},
    "circle.png": {"to": "Unavailiable", "position": "top_left"},
    "sb_v_double_arrow.png": {"to": "Vertical"},
    #
    # Animated
    #
    # Note: Animated cursors not need any extension & frames number
    "wait": {"to": "Busy", "size": (28, 28)},
    "left_ptr_watch": {"to": "Work", "position": "top_left", "size": (28, 28)},
}


def get_config() -> Dict[str, Any]:

    png = PNGProvider("bitmaps")
    config: Dict[str, Any] = {}

    for key, item in X_CURSORS_CFG.items():
        x_hot: int = item.get("x_hot", 0)
        y_hot: int = item.get("y_hot", 0)
        hotspot: Tuple[int, int] = (x_hot, y_hot)

        delay: int = item.get("delay", X_DELAY)
        p: Union[List[Path], Path] = png.get(key)

        data = {
            "png": p,
            "hotspot": hotspot,
            "delay": delay,
        }

        win_data = WIN_CURSORS_CFG.get(key)

        if win_data:
            win_key = win_data.get("to")

            position = win_data.get("position", "center")
            canvas_size: Tuple[int, int] = win_data.get("canvas_size", CANVAS_SIZE)
            size: Tuple[int, int] = win_data.get("size", SIZE)
            win_delay: int = win_data.get("delay", WIN_DELAY)

            config[key] = {
                **data,
                "win_key": win_key,
                "position": position,
                "canvas_size": canvas_size,
                "size": size,
                "win_delay": win_delay,
            }
        else:
            config[key] = data

    return config
