#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
import tempfile
from difflib import SequenceMatcher as SM
from typing import List, NamedTuple, Optional

from tinydb import TinyDB
from tinydb.queries import where
from tinydb.table import Document

seed_data = [
    # Animated cursors
    {
        "name": "wait",
        "symlink": ["watch", "clock", "0426c94ea35c87780ff01dc239897213"],
    },
    {
        "name": "left_ptr_watch",
        "symlink": [
            "progress",
            "half_busy",
            "half-busy",
            "00000000000000020006000e7e9ffc3f",
            "08e8e1c95fe2fc01f976f1e063a24ccd",
            "3ecb610c1bf2410f44200f48c40d3599",
            "9116a3ea924ed2162ecab71ba103b17f",
        ],
    },
    {
        "name": "half_busy",
        "symlink": [
            "half-busy",
            "progress",
            "left_ptr_watch",
            "00000000000000020006000e7e9ffc3f",
            "08e8e1c95fe2fc01f976f1e063a24ccd",
            "3ecb610c1bf2410f44200f48c40d3599",
            "9116a3ea924ed2162ecab71ba103b17f",
        ],
    },
    # Static or Semi-Animated cursors
    {
        "name": "default",
        "symlink": ["left_ptr", "top_left_arrow", "left-arrow"],
    },
    {
        "name": "arrow",
        "symlink": ["right_ptr", "top_right_arrow", "right-arrow"],
    },
    {"name": "center_ptr", "symlink": []},
    {
        "name": "link",
        "symlink": [
            "alias",
            "0876e1c15ff2fc01f906f1c363074c0f",
            "3085a0e285430894940527032f8b26df",
            "640fb0e74195791501fd1ed57b41487f",
            "a2a266d0498c3104214a47bd64ab0fc8",
        ],
    },
    {"name": "dnd_link", "symlink": ["dnd-link"]},
    {"name": "forbidden", "symlink": ["not-allowed"]},
    {
        "name": "crossed_circle",
        "symlink": ["03b6e0fcb3499374a867c041f52298f0"],
    },
    {"name": "circle", "symlink": []},
    {
        "name": "dnd_no_drop",
        "symlink": [
            "dnd-no-drop",
            "no-drop",
            "03b6e0fcb3499374a867c041f52298f0",
            "03b6e0fcb3499374a867d041f52298f0",
        ],
    },
    {"name": "pirate", "symlink": ["kill"]},
    {"name": "pencil", "symlink": []},
    {
        "name": "help",
        "symlink": [
            "question_arrow",
            "whats_this",
            "gumby",
            "5c6cd98b3f3ebcb1f9c7f1c204630408",
            "d9ce0ab605698f320427677b458ad60b",
        ],
    },
    {"name": "dnd_ask", "symlink": ["dnd-ask"]},
    {
        "name": "ns_resize",
        "symlink": [
            "ns-resize",
            "size_ver",
            "v_double_arrow",
            "double_arrow",
            "00008160000006810000408080010102",
        ],
    },
    {"name": "n_resize", "symlink": ["n-resize", "top_side"]},
    {"name": "s_resize", "symlink": ["s-resize", "bottom_side"]},
    {
        "name": "ew_resize",
        "symlink": [
            "ew-resize",
            "size_hor",
            "h_double_arrow",
            "028006030e0e7ebffc7f7070c0600140",
        ],
    },
    {"name": "e_resize", "symlink": ["e-resize", "right_side"]},
    {"name": "w_resize", "symlink": ["w-resize", "left_side"]},
    {"name": "nw_resize", "symlink": ["nw-resize", "top_left_corner"]},
    {"name": "se_resize", "symlink": ["se-resize", "bottom_right_corner"]},
    {
        "name": "size_fdiag",
        "symlink": [
            "nwse-resize",
            "38c5dff7c7b8962045400281044508d2",
            "c7088f0f3e6c8088236ef8e1e3e70000",
        ],
    },
    {"name": "ne_resize", "symlink": ["ne-resize", "top_right_corner"]},
    {"name": "sw_resize", "symlink": ["sw-resize", "bottom_left_corner"]},
    {
        "name": "size_bdiag",
        "symlink": [
            "nesw-resize",
            "50585d75b494802d0151028115016902",
            "fcf1c3c7cd4491d801f1e1c78f100000",
        ],
    },
    {"name": "size_all", "symlink": ["size_all"]},
    {
        "name": "move",
        "symlink": [
            "fleur",
            "4498f0e0c1937ffe01fd06f973665830",
            "9081237383d90e509aa00f00170e968f",
            "fcf21c00b30f7e3f83fe0dfd12e71cff",
        ],
    },
    {"name": "dnd_move", "symlink": ["dnd-move"]},
    {"name": "all_scroll", "symlink": ["all-scroll"]},
    {
        "name": "closedhand",
        "symlink": ["grabbing", "208530c400c041818281048008011002"],
    },
    {"name": "dnd_none", "symlink": ["dnd-none"]},
    {
        "name": "openhand",
        "symlink": [
            "5aca4d189052212118709018842178c0",
            "9d800788f1b08800ae810202380a0822",
        ],
    },
    {"name": "up_arrow", "symlink": []},
    {"name": "color_picker", "symlink": ["color-picker"]},
    {"name": "text", "symlink": ["ibeam", "xterm"]},
    {
        "name": "vertical_text",
        "symlink": ["vertical-text", "048008013003cff3c00c801001200000"],
    },
    {"name": "crosshair", "symlink": []},
    {
        "name": "copy",
        "symlink": [
            "08ffe1cb5fe6fc01f906f1c063814ccf",
            "1081e37283d90000800003c07f3ef6bf",
            "6407b0e94181790501fd1e167b474872",
            "b66166c04f8c3109214a4fbd64a50fc8",
        ],
    },
    {"name": "dnd_copy", "symlink": ["dnd-copy"]},
    {
        "name": "pointer",
        "symlink": [
            "pointing_hand",
            "hand1",
            "e29285e634086352946a0e7090d73106",
        ],
    },
    {"name": "hand2", "symlink": []},
    {"name": "cross", "symlink": ["diamond_cross", "target"]},
    {"name": "cell", "symlink": []},
    {
        "name": "col_resize",
        "symlink": [
            "col-resize",
            "sb_h_double_arrow",
            "043a9f68147c53184671403ffa811cc5",
            "14fef782d02440884392942c11205230",
        ],
    },
    {"name": "split_h", "symlink": []},
    {
        "name": "row_resize",
        "symlink": [
            "row-resize",
            "sb_v_double_arrow",
            "2870a09082c103050810ffdffffe0204",
            "c07385c7190e701020ff7ffffd08103c",
        ],
    },
    {"name": "split_v", "symlink": []},
    {"name": "plus", "symlink": []},
    {"name": "X_cursor", "symlink": ["X_cursor", "X-cursor"]},
    {
        "name": "context_menu",
        "symlink": ["context-menu", "08ffe1e65f80fcfdf9fff11263e74c48"],
    },
    {"name": "zoom", "symlink": []},
    {
        "name": "zoom_out",
        "symlink": ["zoom-out", "f41c0e382c97c0938e07017e42800402"],
    },
    {
        "name": "zoom_in",
        "symlink": ["zoom-in", "f41c0e382c94c0958e07017e42b00462"],
    },
]


class RenameCursor(NamedTuple):
    """ Rename cursor name according @old to @new  """

    old: str
    new: str


class Database:
    """Database Api."""

    def __init__(self) -> None:
        self.db_file = tempfile.NamedTemporaryFile(
            prefix="clickgen_db_", suffix=".json"
        ).name
        self.db: TinyDB = TinyDB(self.db_file)
        for d in seed_data:
            self.db.insert(d)

        def __del__() -> None:
            self.db.close()
            os.remove(self.db)

    def get_field_data(self, field: str) -> List[str]:
        try:
            return [r[field] for r in self.db]
        except KeyError as e:
            raise KeyError(f"{e} Field not found in 'clickgen' database")

    def cursors(self) -> List[str]:
        return self.get_field_data("name")

    def symlinks(self, cursor: str) -> Optional[List[str]]:
        try:
            item: List[str] = list(self.cursor_node_by_name(cursor).get("symlink"))
            item.remove(cursor)

            if item:
                return item
            else:
                return None
        except ValueError:
            pass
        except TypeError:
            raise Exception(
                f"'{cursor}' cursor's information not found in 'clickgen' database"
            )

    def cursor_node_by_name(self, s: str) -> Optional[Document]:
        """ Fetch one node from db by cursor `name`. """
        node = self.db.search(where("name") == s)

        if node:
            return node[0]
        else:
            return None

    def cursor_node_by_symlink(self, s: str) -> Optional[Document]:
        """ Fetch one node from db by cursors `symlinks`"""
        node = self.db.search((where("symlink").any([s])))

        if node:
            return node[0]
        else:
            return None

    def match_string(self, s: str, l: List[str]) -> Optional[str]:
        compare_ratio: float = 0.5
        result: str = s

        for e in l:
            ratio: float = SM(None, s.lower(), e.lower()).ratio()
            if ratio > compare_ratio:
                compare_ratio = ratio
                result = e
            else:
                continue

        if s != result:
            return result
        else:
            return None

    def valid_cursors(self, l: List[str]) -> Optional[List[RenameCursor]]:
        rename_list: List[RenameCursor] = []

        for s in l:
            s = path.splitext(s)[0]
            n1 = self.cursor_node_by_symlink(s)
            if n1:
                if n1["name"] != s:
                    rename_list.append(RenameCursor(old=s, new=n1["name"]))
                continue

            if not self.cursor_node_by_name(s):
                new = self.match_string(s, self.cursors())
                if new:
                    rename_list.append(RenameCursor(old=s, new=new))
                else:
                    print(f"{s} is Unknown Cursor")
                    continue

        if rename_list:
            return rename_list
        else:
            None
