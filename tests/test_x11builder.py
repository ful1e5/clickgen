#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
from unittest.mock import PropertyMock, patch

from clickgen.builders.x11builder import X11CursorsBuilder


@patch.object(
    X11CursorsBuilder, "_X11CursorsBuilder__config_dir", new_callable=PropertyMock
)
def test_x11builder_config_dir(mock_config_dir: str) -> None:
    x = X11CursorsBuilder(mock_config_dir, "/foo/out")
    mock_config_dir.return_value = "/foo/"
    assert "/foo/" == x._X11CursorsBuilder__config_dir  # type: ignore


@patch.object(
    X11CursorsBuilder, "_X11CursorsBuilder__out_dir", new_callable=PropertyMock
)
def test_x11builder_out_dir(mock_out_dir: str) -> None:
    x = X11CursorsBuilder("/foo/", mock_out_dir)
    mock_out_dir.return_value = "/foo/out/"
    assert "/foo/out/" == x._X11CursorsBuilder__out_dir  # type: ignore


def test_x11builder_out_dir_files(config_dir: str, out_dir: str) -> None:
    X11CursorsBuilder(config_dir, out_dir).build()
    assert len(os.listdir(out_dir)) > 0


def test_x11builder_out_dir_contain_cursors_directory(xcursors_dir: str) -> None:
    assert path.exists(xcursors_dir)


def test_x11builder_out_dir_xcursors(xcursors_dir: str) -> None:
    for c in os.listdir(xcursors_dir):
        assert c in ["a", "b", "c"]


def test_x11builder_out_dir_xcursors_file_sizes(xcursors_dir: str) -> None:
    curs = os.listdir(xcursors_dir)

    for c in curs:
        assert path.getsize(path.join(xcursors_dir, c)) > 0
