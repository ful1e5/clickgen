#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tinydb import TinyDB

seed_data = {
    {
        "cursor": "default",
        "symblinks": ("default", "left_ptr", "top_left_arrow", "left-arrow"),
    },
    {
        "cursor": "arrow",
        "symblinks": ("arrow", "right_ptr", "top_right_arrow", "right-arrow"),
    },
    {"cursor": "center_ptr", "symblinks": ("center_ptr")},
    {
        "cursor": "link",
        "symblinks": (
            "link",
            "alias",
            "0876e1c15ff2fc01f906f1c363074c0f",
            "3085a0e285430894940527032f8b26df",
            "640fb0e74195791501fd1ed57b41487f",
            "a2a266d0498c3104214a47bd64ab0fc8",
        ),
    },
    {"cursor": "dnd_link", "symblinks": ("dnd-link")},
    {"cursor": "forbidden", "symblinks": ("forbidden", "not-allowed")},
    {
        "cursor": "crossed_circle",
        "symblinks": ("crossed_circle", "03b6e0fcb3499374a867c041f52298f0"),
    },
    {"cursor": "circle", "symblinks": ("circle")},
    {
        "cursor": "dnd_no_drop",
        "symblinks": (
            "dnd-no-drop",
            "no-drop",
            "03b6e0fcb3499374a867c041f52298f0",
            "03b6e0fcb3499374a867d041f52298f0",
        ),
    },
    {"cursor": "pirate", "symblinks": ("pirate", "kill")},
    {"cursor": "pencil", "symblinks": ("pencil")},
    {
        "cursor": "wait",
        "symblinks": ("wait", "watch", "clock", "0426c94ea35c87780ff01dc239897213"),
    },
    {
        "cursor": "half_busy",
        "symblinks": (
            "half-busy",
            "progress",
            "left_ptr_watch",
            "00000000000000020006000e7e9ffc3f",
            "08e8e1c95fe2fc01f976f1e063a24ccd",
            "3ecb610c1bf2410f44200f48c40d3599",
            "9116a3ea924ed2162ecab71ba103b17f",
        ),
    },
    {
        "cursor": "help",
        "symblinks": (
            "help",
            "question_arrow",
            "whats_this",
            "gumby",
            "5c6cd98b3f3ebcb1f9c7f1c204630408",
            "d9ce0ab605698f320427677b458ad60b",
        ),
    },
    {"cursor": "dnd_ask", "symblinks": ("dnd-ask")},
    {
        "cursor": "ns_resize",
        "symblinks": (
            "ns-resize",
            "size_ver",
            "v_double_arrow",
            "double_arrow",
            "00008160000006810000408080010102",
        ),
    },
    {"cursor": "n_resize", "symblinks": ("n-resize", "top_side")},
    {"cursor": "s_resize", "symblinks": ("s-resize", "bottom_side")},
    {
        "cursor": "ew_resize",
        "symblinks": (
            "ew-resize",
            "size_hor",
            "h_double_arrow",
            "028006030e0e7ebffc7f7070c0600140",
        ),
    },
    {"cursor": "e_resize", "symblinks": ("e-resize", "right_side")},
    {"cursor": "w_resize", "symblinks": ("w-resize", "left_side")},
    {"cursor": "nw_resize", "symblinks": ("nw-resize", "top_left_corner")},
    {"cursor": "se_resize", "symblinks": ("se-resize", "bottom_right_corner")},
    {
        "cursor": "size_fdiag",
        "symblinks": (
            "size_fdiag",
            "nwse-resize",
            "38c5dff7c7b8962045400281044508d2",
            "c7088f0f3e6c8088236ef8e1e3e70000",
        ),
    },
    {"cursor": "ne_resize", "symblinks": ("ne-resize", "top_right_corner")},
    {"cursor": "sw_resize", "symblinks": ("sw-resize", "bottom_left_corner")},
    {
        "cursor": "size_bdiag",
        "symblinks": (
            "size_bdiag",
            "nesw-resize",
            "50585d75b494802d0151028115016902",
            "fcf1c3c7cd4491d801f1e1c78f100000",
        ),
    },
    {"cursor": "size_all", "symblinks": ("size_all")},
    {
        "cursor": "move",
        "symblinks": (
            "move",
            "fleur",
            "4498f0e0c1937ffe01fd06f973665830",
            "9081237383d90e509aa00f00170e968f",
            "fcf21c00b30f7e3f83fe0dfd12e71cff",
        ),
    },
    {"cursor": "dnd_move", "symblinks": ("dnd-move")},
    {"cursor": "all_scroll", "symblinks": ("all-scroll")},
    {
        "cursor": "closedhand",
        "symblinks": ("closedhand", "grabbing", "208530c400c041818281048008011002"),
    },
    {"cursor": "dnd_none", "symblinks": ("dnd-none")},
    {
        "cursor": "openhand",
        "symblinks": (
            "openhand",
            "5aca4d189052212118709018842178c0",
            "9d800788f1b08800ae810202380a0822",
        ),
    },
    {"cursor": "up_arrow", "symblinks": ("up_arrow")},
    {"cursor": "color_picker", "symblinks": ("color-picker")},
    {"cursor": "text", "symblinks": ("text", "ibeam", "xterm")},
    {
        "cursor": "vertical_text",
        "symblinks": ("vertical-text", "048008013003cff3c00c801001200000"),
    },
    {"cursor": "crosshair", "symblinks": ("crosshair")},
    {
        "cursor": "copy",
        "symblinks": (
            "copy",
            "08ffe1cb5fe6fc01f906f1c063814ccf",
            "1081e37283d90000800003c07f3ef6bf",
            "6407b0e94181790501fd1e167b474872",
            "b66166c04f8c3109214a4fbd64a50fc8",
        ),
    },
    {"cursor": "dnd_copy", "symblinks": ("dnd-copy")},
    {
        "cursor": "pointer",
        "symblinks": (
            "pointer",
            "pointing_hand",
            "hand1",
            "e29285e634086352946a0e7090d73106",
        ),
    },
    {"cursor": "hand2", "symblinks": ("hand2")},
    {"cursor": "cross", "symblinks": ("cross", "diamond_cross", "target")},
    {"cursor": "cell", "symblinks": ("cell")},
    {
        "cursor": "col_resize",
        "symblinks": (
            "col-resize",
            "sb_h_double_arrow",
            "043a9f68147c53184671403ffa811cc5",
            "14fef782d02440884392942c11205230",
        ),
    },
    {"cursor": "split_h", "symblinks": ("split_h")},
    {
        "cursor": "row_resize",
        "symblinks": (
            "row-resize",
            "sb_v_double_arrow",
            "2870a09082c103050810ffdffffe0204",
            "c07385c7190e701020ff7ffffd08103c",
        ),
    },
    {"cursor": "split_v", "symblinks": ("split_v")},
    {"cursor": "plus", "symblinks": ("plus")},
    {"cursor": "X_cursor", "symblinks": ("X_cursor", "X-cursor")},
    {
        "cursor": "context_menu",
        "symblinks": ("context-menu", "08ffe1e65f80fcfdf9fff11263e74c48"),
    },
    {"cursor": "zoom", "symblinks": ("zoom")},
    {
        "cursor": "zoom_out",
        "symblinks": ("zoom-out", "zoom_out", "f41c0e382c97c0938e07017e42800402"),
    },
    {
        "cursor": "zoom_in",
        "symblinks": ("zoom-in", "zoom_in", "f41c0e382c94c0958e07017e42b00462"),
    },
}


class CursorDatabase:
    """Processed cursors information with database."""

    db: TinyDB = TinyDB("db.json")

    def __init__(self, data) -> None:
        self.db.insert({})
