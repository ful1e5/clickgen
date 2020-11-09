#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import pytest
from clickgen.packagers.windows import WindowsPackager


def test_win_packager_exception(wincursors_dir, ti) -> None:
    with pytest.raises(FileNotFoundError):
        WindowsPackager(wincursors_dir, ti).pack()


def test_win_packager() -> None:
    # assert os.listdir(win_1_dir) == []
    pass