#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.conftest import out_dir
from clickgen.providers.themeconfig import ThemeConfigsProvider
import os
from unittest.mock import PropertyMock, patch
import pytest

from clickgen.builders.winbuilder import WinCursorsBuilder


@patch.object(
    WinCursorsBuilder, "_WinCursorsBuilder__config_dir", new_callable=PropertyMock
)
def test_winbuilder_config_dir(mock_config_dir) -> None:
    x = WinCursorsBuilder(mock_config_dir, "/foo/out")
    mock_config_dir.return_value = "/foo/"
    assert "/foo/" == x._WinCursorsBuilder__config_dir  # type: ignore


@patch.object(
    WinCursorsBuilder, "_WinCursorsBuilder__out_dir", new_callable=PropertyMock
)
def test_winbuilder_out_dir(mock_out_dir) -> None:
    x = WinCursorsBuilder("/foo/", mock_out_dir)
    mock_out_dir.return_value = "/foo/out/"
    assert "/foo/out/" == x._WinCursorsBuilder__out_dir  # type: ignore


def test_winbuilder_out_dir_files(config_dir, out_dir) -> None:
    WinCursorsBuilder(config_dir, out_dir).build()
    assert len(os.listdir(out_dir)) == 3


def test_winbuilder_lower_resolution_exception(
    bitmaps_dir, hotspots, delay, out_dir
) -> None:
    # Exception occur in lower pixel sizes 1, 2, 3, 4, 5
    # ex: struct.error: ushort format requires 0 <= number <= (0x7fff * 2 + 1)

    for s in [[1], [2], [3], [4], [5]]:
        tcp = ThemeConfigsProvider(bitmaps_dir, hotspots, s)
        c = tcp.generate(delay)
        with pytest.raises(Exception):
            WinCursorsBuilder(c, out_dir).build()
