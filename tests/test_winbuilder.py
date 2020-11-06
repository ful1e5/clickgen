#!/usr/bin/env python
# -*- coding: utf-8 -*-

from unittest.mock import PropertyMock, patch

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


# def test_winbuilder_out_dir_files(config_dir, out_dir) -> None:
#     # try:
#     WinCursorsBuilder(config_dir, out_dir).build()
#     # except Exception:
#     # print(traceback.format_exc)

#     assert len(os.listdir(out_dir)) > 0
