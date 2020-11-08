#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path

import pytest
from clickgen.packagers.x11 import X11Packager


def test_x11_package(xcursors_dir, ti) -> None:
    dir = path.abspath(path.join(xcursors_dir, "../"))
    X11Packager(dir, ti).pack()

    assert pytest.approx(os.listdir(dir) == ["cursors", "index.theme", "cursor.theme"])
