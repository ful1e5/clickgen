#!/usr/bin/env python
# -*- coding: utf-8 -*-

import itertools
import os
import re
import tempfile
from difflib import SequenceMatcher as SM
from typing import List, NamedTuple, Optional

from tinydb import TinyDB
from tinydb.queries import where
from tinydb.table import Document

# Windows cursors are inside "__"
cursor_groups: List[List[str]] = [
    ["X_cursor", "x-cursor", "kill", "pirate"],
    ["kill", "pirate"],
    ["all-scroll", "fleur", "size_all"],
    [
        "bd_double_arrow",
        "c7088f0f3e6c8088236ef8e1e3e70000",
        "38c5dff7c7b8962045400281044508d2",
        "size_fdiag",
        "nwse-resize",
        "__Diagonal_1__",
    ],  # Windows
    ["bottom_left_corner", "sw-resize"],
    ["bottom_right_corner", "se-resize"],
    ["bottom_side", "s-resize"],
    ["bottom_tee"],
    ["center_ptr"],
    ["circle", "forbidden", "__Unavailiable__"],  # Windows
    ["context-menu"],
    [
        "1081e37283d90000800003c07f3ef6bf",
        "6407b0e94181790501fd1e167b474872",
        "b66166c04f8c3109214a4fbd64a50fc8",
        "08ffe1cb5fe6fc01f906f1c063814ccf",
        "copy",
    ],
    ["cross", "cross_reverse", "diamond_cross", "_Cross_"],  # Windows
    ["crossed_circle", "03b6e0fcb3499374a867c041f52298f0", "not-allowed"],
    ["crosshair"],
    ["dnd-ask"],
    ["dnd-copy"],
    ["dnd-link", "alias"],
    ["dnd-move"],
    [
        "dnd-none",
        "closedhand",
        "208530c400c041818281048008011002",
        "fcf21c00b30f7e3f83fe0dfd12e71cff",
    ],
    ["dnd_no_drop", "no-drop"],
    ["dotbox", "dot_box_mask", "draped_box", "icon", "target"],
    [
        "fcf1c3c7cd4491d801f1e1c78f100000",
        "50585d75b494802d0151028115016902",
        "fd_double_arrow",
        "nesw-resize",
        "size_bdiag",
        "__Diagonal_2__",
    ],  # Windows
    ["grabbing"],
    ["hand"],
    [
        "hand1",
        "grab",
        "5aca4d189052212118709018842178c0",
        "openhand",
        "__Move__",
    ],  # Windows
    [
        "9d800788f1b08800ae810202380a0822",
        "e29285e634086352946a0e7090d73106",
        "hand2",
        "pointer",
        "pointing_hand",
        "__Link__",
    ],  # Windows
    ["left_ptr", "arrow", "default", "_Default_"],  # Windows
    [
        "00000000000000020006000e7e9ffc3f",
        "08e8e1c95fe2fc01f976f1e063a24ccd",
        "3ecb610c1bf2410f44200f48c40d3599",
        "9116a3ea924ed2162ecab71ba103b17f",
        "left_ptr_watch",
        "progress",
        "__Work__",
    ],  # Windows
    ["left_side", "w-resize"],
    ["left_tee"],
    [
        "3085a0e285430894940527032f8b26df",
        "640fb0e74195791501fd1ed57b41487f",
        "a2a266d0498c3104214a47bd64ab0fc8",
        "0876e1c15ff2fc01f906f1c363074c0f",
        "link",
    ],
    ["ll_angle"],
    ["lr_angle"],
    [
        "4498f0e0c1937ffe01fd06f973665830",
        "9081237383d90e509aa00f00170e968f",
        "move",
    ],
    ["pencil", "draft", "__Handwriting__"],  # Windows
    ["plus", "cell"],
    ["pointer-move"],
    [
        "5c6cd98b3f3ebcb1f9c7f1c204630408",
        "d9ce0ab605698f320427677b458ad60b",
        "gumby",
        "help",
        "left_ptr_help",
        "question_arrow",
        "whats_this",
        "__Help__",
    ],  # Windows
    ["right_ptr", "draft_large", "draft_small", "__Alternate__"],  # Windows
    ["right_side", "e-resize"],
    ["right_tee"],
    ["sb_down_arrow", "down-arrow"],
    [
        "028006030e0e7ebffc7f7070c0600140",
        "14fef782d02440884392942c11205230",
        "043a9f68147c53184671403ffa811cc5",
        "col-resize",
        "ew-resize",
        "h_double_arrow",
        "sb_h_double_arrow",
        "size-hor",
        "size_hor",
        "split_h",
        "__Horizontal__",
    ],  # Windows
    ["sb_left_arrow", "left-arrow"],
    ["sb_right_arrow", "right-arrow"],
    ["sb_up_arrow", "up-arrow"],
    [
        "00008160000006810000408080010102",
        "c07385c7190e701020ff7ffffd08103c",
        "2870a09082c103050810ffdffffe0204",
        "double_arrow",
        "ns-resize",
        "row-resize",
        "sb_v_double_arrow",
        "size-ver",
        "size_ver",
        "split_v",
        "v_double_arrow",
        "__Vertical__",
    ],  # Windows
    ["tcross", "color-picker"],
    ["top_left_corner", "nw-resize"],
    ["top_right_corner", "ne-resize"],
    ["top_side", "n-resize"],
    ["top_tee"],
    ["ul_angle"],
    ["ur_angle"],
    ["vertical-text", "048008013003cff3c00c801001200000"],
    [
        "watch",
        "clock",
        "wait",
        "0426c94ea35c87780ff01dc239897213",
        "__Busy__",
    ],  # Windows
    ["wayland-cursor"],
    ["xterm", "text", "ibeam", "__IBeam__"],  # Windows
    ["zoom-in", "f41c0e382c94c0958e07017e42b00462"],
    ["zoom-out", "f41c0e382c97c0938e07017e42800402"],
]


class RenameCursor(NamedTuple):
    """ Rename cursor name according @old to @new  """

    old: str
    new: str


class Database:
    """Database Api."""

    db_file: str = tempfile.NamedTemporaryFile(
        prefix="clickgen_db_", suffix=".json"
    ).name
    db_cursors: List[str] = list(itertools.chain.from_iterable(cursor_groups))
    __data_skeleton = {"name": "", "symlinks": []}

    def __init__(self) -> None:
        # Creating database file
        self.db: TinyDB = TinyDB(self.db_file)

        # Deconstructor
        def __del__() -> None:
            self.db.close()
            os.remove(self.db)

    def seed(self, cursor: str) -> None:
        try:
            group = list(filter(lambda group: cursor in group, cursor_groups))
            group = group[0]
            data = self.__data_skeleton
            wsym: str = "__"

            if group != []:
                group.remove(cursor)
                data["name"] = cursor
                if group:
                    raw = "\t".join(group)
                    if wsym in raw:
                        win_cursor = re.search(f"{wsym}(.*?){wsym}", raw).group(1)
                        group.remove(f"{wsym}{win_cursor}{wsym}")

                        print(f" Setting Windows cursor '{win_cursor}' from '{cursor}'")
                        data["windows"] = win_cursor

                    print(f" Linking '{cursor}' ==> {group}")
                    data["symlinks"] = group
                self.db.insert(data)

            else:
                print(f"'{cursor}' is Unknown cursor")

                data["name"] = cursor
                self.db.insert(data)
        except IndexError:
            pass

    def smart_seed(self, cursor: str) -> Optional[RenameCursor]:
        if cursor not in self.db_cursors:
            match = self.match_string(cursor, self.db_cursors)
            self.seed(match)

            if match:
                return RenameCursor(old=cursor, new=match)
            else:
                return None
        else:
            self.seed(cursor)
            return None

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
