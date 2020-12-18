#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.typing.core import WindowsConfig, ImageSize, WinConfigData

# -- Windows bitmaps constants
WIN_BITMAPS_SIZE: ImageSize = ImageSize(width=32, height=32)
WIN_CURSOR_NORMAL_SIZE: ImageSize = ImageSize(width=24, height=24)
WIN_CURSOR_LARGE_SIZE: ImageSize = ImageSize(width=28, height=28)

WIN_CURSORS_CFG: WindowsConfig = {
    "Alternate": WinConfigData(x_cursor="right_ptr", placement="top_left"),
    "Busy": WinConfigData(x_cursor="wait", size=WIN_CURSOR_LARGE_SIZE),
    "Cross": WinConfigData(x_cursor="cross"),
    "Default": WinConfigData(x_cursor="left_ptr", placement="top_left"),
    "Diagonal_1": WinConfigData(x_cursor="fd_double_arrow"),
    "Diagonal_2": WinConfigData(x_cursor="bd_double_arrow"),
    "Handwriting": WinConfigData(x_cursor="pencil"),
    "Help": WinConfigData(x_cursor="help", placement="top_left"),
    "Horizontal": WinConfigData(x_cursor="sb_h_double_arrow"),
    "IBeam": WinConfigData(x_cursor="xterm", placement="top_left"),
    "Link": WinConfigData(x_cursor="hand2", placement="top_left"),
    "Move": WinConfigData(x_cursor="hand1"),
    "Unavailiable": WinConfigData(x_cursor="circle", placement="top_left"),
    "Vertical": WinConfigData(x_cursor="sb_v_double_arrow"),
    "Work": WinConfigData(
        x_cursor="left_ptr_watch", placement="top_left", size=WIN_CURSOR_LARGE_SIZE
    ),
}