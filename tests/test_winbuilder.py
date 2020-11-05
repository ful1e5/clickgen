#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.builders.winbuilder import WinCursorsBuilder
from unittest.mock import PropertyMock, patch


@patch.object(
    WinCursorsBuilder, "_WinCursorsBuilder__config_dir", new_callable=PropertyMock
)
def test_winbuilder_config_dir(mock_config_dir) -> None:
    x = WinCursorsBuilder(mock_config_dir, "/foo/out")
    mock_config_dir.return_value = "/foo/"
    assert "/foo/" == x._WinCursorsBuilder__config_dir  # type: ignore
