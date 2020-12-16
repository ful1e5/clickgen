#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.typing import WindowsCursorsConfig, ImageSize

# -- Windows Bitmaps Constants

WIN_CURSORS_CFG: WindowsCursorsConfig = {
    "Alternate": {"xcursor": "right_ptr", "placement": "top_left"},
    "Busy": {"xcursor": "wait"},
    "Cross": {"xcursor": "cross"},
    "Default": {"xcursor": "left_ptr", "placement": "top_left"},
    "Diagonal_1": {"xcursor": "fd_double_arrow"},
    "Diagonal_2": {"xcursor": "bd_double_arrow"},
    "Handwriting": {"xcursor": "pencil"},
    "Help": {"xcursor": "help", "placement": "top_left"},
    "Horizontal": {"xcursor": "sb_h_double_arrow"},
    "IBeam": {"xcursor": "xterm", "placement": "top_left"},
    "Link": {"xcursor": "hand2", "placement": "top_left"},
    "Move": {"xcursor": "hand1"},
    "Unavailiable": {"xcursor": "circle", "placement": "top_left"},
    "Vertical": {"xcursor": "sb_v_double_arrow"},
    "Work": {"xcursor": "left_ptr_watch", "placement": "top_left"},
}
WIN_BITMAPS_SIZE: ImageSize = ImageSize(width=32, height=32)
WIN_CURSOR_SIZE: ImageSize = ImageSize(width=24, height=24)