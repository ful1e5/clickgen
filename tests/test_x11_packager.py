#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path

import pytest
from clickgen.packagers.x11 import X11Packager


def test_x11_package(xcursors_dir, ti, hotspots) -> None:
    directory = path.abspath(path.join(xcursors_dir, "../"))
    X11Packager(directory, ti).pack()

    assert pytest.approx(
        os.listdir(directory) == ["cursors", "index.theme", "cursor.theme"]
    )

    assert pytest.approx(os.listdir(xcursors_dir) == hotspots.keys())

    i_lns = open(path.join(directory, "index.theme"), "r").readlines()
    assert i_lns == ["[Icon Theme]\n", "Name=foo\n", "Comment=None"]

    c_lns = open(path.join(directory, "cursor.theme"), "r").readlines()
    assert c_lns == ["[Icon Theme]\n", "Inherits=foo"]
