#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
from typing import Dict, List, Optional, Set
from difflib import SequenceMatcher as SM

# Typing
Data = List[Set[str]]

DATA: Data = [
    {
        "X_cursor",
        "x-cursor",
        "kill",
        "pirate",
    },
    {"kill", "pirate"},
    {"all-scroll", "fleur", "size_all"},
    {
        "bd_double_arrow",
        "c7088f0f3e6c8088236ef8e1e3e70000",
        "38c5dff7c7b8962045400281044508d2",
        "size_fdiag",
        "nwse-resize",
    },
    {"bottom_left_corner", "sw-resize"},
    {"bottom_right_corner", "se-resize"},
    {"bottom_side", "s-resize"},
    {"bottom_tee"},
    {"center_ptr"},
    {
        "circle",
        "forbidden",
    },
    {"context-menu"},
    {
        "1081e37283d90000800003c07f3ef6bf",
        "6407b0e94181790501fd1e167b474872",
        "b66166c04f8c3109214a4fbd64a50fc8",
        "08ffe1cb5fe6fc01f906f1c063814ccf",
        "copy",
    },
    {
        "cross",
        "cross_reverse",
        "diamond_cross",
    },
    {"crossed_circle", "03b6e0fcb3499374a867c041f52298f0", "not-allowed"},
    {"crosshair"},
    {"dnd-ask"},
    {"dnd-copy"},
    {"dnd-link", "alias"},
    {"dnd-move"},
    {
        "dnd-none",
        "closedhand",
        "208530c400c041818281048008011002",
        "fcf21c00b30f7e3f83fe0dfd12e71cff",
    },
    {"dnd_no_drop", "no-drop"},
    {"dotbox", "dot_box_mask", "draped_box", "icon", "target"},
    {
        "fcf1c3c7cd4491d801f1e1c78f100000",
        "50585d75b494802d0151028115016902",
        "fd_double_arrow",
        "nesw-resize",
        "size_bdiag",
    },
    {"grabbing"},
    {"hand"},
    {
        "hand1",
        "grab",
        "5aca4d189052212118709018842178c0",
        "openhand",
    },
    {
        "9d800788f1b08800ae810202380a0822",
        "e29285e634086352946a0e7090d73106",
        "hand2",
        "pointer",
        "pointing_hand",
    },
    {
        "left_ptr",
        "arrow",
        "default",
    },
    {
        "00000000000000020006000e7e9ffc3f",
        "08e8e1c95fe2fc01f976f1e063a24ccd",
        "3ecb610c1bf2410f44200f48c40d3599",
        "9116a3ea924ed2162ecab71ba103b17f",
        "left_ptr_watch",
        "progress",
    },
    {"left_side", "w-resize"},
    {"left_tee"},
    {
        "3085a0e285430894940527032f8b26df",
        "640fb0e74195791501fd1ed57b41487f",
        "a2a266d0498c3104214a47bd64ab0fc8",
        "0876e1c15ff2fc01f906f1c363074c0f",
        "link",
    },
    {"ll_angle"},
    {"lr_angle"},
    {
        "4498f0e0c1937ffe01fd06f973665830",
        "9081237383d90e509aa00f00170e968f",
        "move",
    },
    {
        "pencil",
        "draft",
    },
    {"plus", "cell"},
    {"pointer-move"},
    {
        "5c6cd98b3f3ebcb1f9c7f1c204630408",
        "d9ce0ab605698f320427677b458ad60b",
        "gumby",
        "help",
        "left_ptr_help",
        "question_arrow",
        "whats_this",
    },
    {
        "right_ptr",
        "draft_large",
        "draft_small",
    },
    {"right_side", "e-resize"},
    {"right_tee"},
    {"sb_down_arrow", "down-arrow"},
    {
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
    },
    {"sb_left_arrow", "left-arrow"},
    {"sb_right_arrow", "right-arrow"},
    {"sb_up_arrow", "up-arrow"},
    {
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
    },
    {"tcross", "color-picker"},
    {"top_left_corner", "nw-resize"},
    {"top_right_corner", "ne-resize"},
    {"top_side", "n-resize"},
    {"top_tee"},
    {"ul_angle"},
    {"ur_angle"},
    {"vertical-text", "048008013003cff3c00c801001200000"},
    {
        "watch",
        "clock",
        "wait",
        "0426c94ea35c87780ff01dc239897213",
    },
    {"wayland-cursor"},
    {
        "xterm",
        "text",
        "ibeam",
    },
    {"zoom-in", "f41c0e382c94c0958e07017e42b00462"},
    {"zoom-out", "f41c0e382c97c0938e07017e42800402"},
]


class CursorDB(object):
    data: Dict[str, List[str]] = {}

    def __init__(self, data: Data) -> None:
        super().__init__()
        self.__seed(data)

    def __str__(self) -> str:
        string: List[str] = []
        for k, v in self.data.items():
            string.append(f"{k}={v}")
        return f"CursorDB({', '.join(string)})"

    def __repr__(self) -> str:
        return f"{self.data!r}"

    def __seed(self, data: Data) -> None:
        if not isinstance(data, list):
            raise TypeError(f"'data' is not type of 'List'")
        for item in sorted(data):
            if not isinstance(item, set):
                raise TypeError(f"Item '{item}' is not type of 'Set'")
            for i in sorted(item):
                symlinks: List[str] = list(item)
                symlinks.remove(i)
                self.data[i] = symlinks

    def search_symlinks(
        self, key: str, find_similar: bool = False
    ) -> Optional[List[str]]:
        if find_similar:
            key = self.__find_similar(key)

        return self.data.get(key)

    def __find_similar(self, key: str) -> str:
        compare_ratio: float = 0.5
        result: str = key
        for e in self.data.keys():
            ratio: float = SM(None, key.lower(), e.lower()).ratio()
            if ratio > compare_ratio:
                compare_ratio = ratio
                result = e

        return result

    def rename_file(self, p: Path) -> Optional[Path]:
        if not p.is_file():
            raise FileNotFoundError(f"'{p.absolute()}' is not file")
        key: str = self.__find_similar(p.stem)
        if key != p.stem:
            return p.with_name(f"{key}{p.suffix}")
        return None
