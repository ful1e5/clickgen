#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from clickgen.packagers.windows import WindowsPackager


def test_win_package(wincursors_dir, ti) -> None:
    with pytest.raises(FileNotFoundError):
        WindowsPackager(wincursors_dir, ti).pack()
