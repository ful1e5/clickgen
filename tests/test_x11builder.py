#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tests.conftest import config_dir, out_dir
from clickgen.builders.x11builder import X11CursorsBuilder
from unittest.mock import PropertyMock, patch


@patch.object(
    X11CursorsBuilder, "_X11CursorsBuilder__config_dir", new_callable=PropertyMock
)
def test_x11builder_config_dir(mock_config_dir) -> None:
    x = X11CursorsBuilder(mock_config_dir, "/foo/")
    mock_config_dir.return_value = "/foo/out/"
    assert "/foo/out/" == x._X11CursorsBuilder__config_dir  # type: ignore
