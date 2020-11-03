#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple
from unittest.mock import PropertyMock, patch

import pytest

from clickgen.providers.themeconfig import ThemeConfigsProvider, _clean_cur_name

clean_cur_name_parameters: List[Tuple[str, str]] = [
    ("/foo/bar-01", "/foo/bar"),
    ("/foo/b-000000001", "/foo/b"),
    ("/foo/b", "/foo/b"),
    ("/foo/bsd-gg", "/foo/bsd"),
    ("/foo/rr.ds=ds-rf", "/foo/rr"),
]


@pytest.mark.parametrize("arg, result", clean_cur_name_parameters)
def test_clean_cur_name(arg, result) -> None:
    assert _clean_cur_name(arg) == result


def test_themeconfig_provider_sizes(bitmaps_dir, sizes, hotspots) -> None:
    with patch.object(
        ThemeConfigsProvider, "_ThemeConfigsProvider__sizes", new_callable=PropertyMock
    ) as mock_sizes:
        tcp = ThemeConfigsProvider(bitmaps_dir, hotspots, sizes=mock_sizes)

        mock_sizes.return_value = sizes
        assert sizes == tcp._ThemeConfigsProvider__sizes  # type: ignore


def test_themeconfig_provider_bitmaps_dir(bitmaps_dir, sizes, hotspots) -> None:
    with patch.object(
        ThemeConfigsProvider,
        "_ThemeConfigsProvider__bitmaps_dir",
        new_callable=PropertyMock,
    ) as mock_bitmaps_dir:
        tcp = ThemeConfigsProvider(mock_bitmaps_dir, hotspots, sizes)

        mock_bitmaps_dir.return_value = bitmaps_dir
        assert bitmaps_dir == tcp._ThemeConfigsProvider__bitmaps_dir  # type: ignore