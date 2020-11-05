#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import PropertyMock, patch

from clickgen.builders.x11builder import X11CursorsBuilder


@patch.object(
    X11CursorsBuilder, "_X11CursorsBuilder__config_dir", new_callable=PropertyMock
)
def test_x11builder_config_dir(mock_config_dir) -> None:
    x = X11CursorsBuilder(mock_config_dir, "/foo/out")
    mock_config_dir.return_value = "/foo/"
    assert "/foo/" == x._X11CursorsBuilder__config_dir  # type: ignore


@patch.object(
    X11CursorsBuilder, "_X11CursorsBuilder__out_dir", new_callable=PropertyMock
)
def test_x11builder_out_dir(mock_out_dir) -> None:
    x = X11CursorsBuilder("/foo/", mock_out_dir)
    mock_out_dir.return_value = "/foo/out/"
    assert "/foo/out/" == x._X11CursorsBuilder__out_dir  # type: ignore
