#!/usr/bin/env python
# -*- coding: utf-8 -*-


from typing import Dict


WIN_CURSORS_CFG: Dict[str, Dict[str, str]] = {
    "Alternate": {"from": "right_ptr", "placement": "top_left"},
    "Busy": {"from": "wait"},
    "Cross": {"from": "cross"},
    "Default": {"from": "left_ptr", "placement": "top_left"},
    "Diagonal_1": {"from": "fd_double_arrow"},
    "Diagonal_2": {"from": "bd_double_arrow"},
    "Handwriting": {"from": "pencil"},
    "Help": {"from": "help", "placement": "top_left"},
    "Horizontal": {"from": "sb_h_double_arrow"},
    "IBeam": {"from": "xterm", "placement": "top_left"},
    "Link": {"from": "hand2", "placement": "top_left"},
    "Move": {"from": "hand1"},
    "Unavailiable": {"from": "circle", "placement": "top_left"},
    "Vertical": {"from": "sb_v_double_arrow"},
    "Work": {"from": "left_ptr_watch", "placement": "top_left"},
}