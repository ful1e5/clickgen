#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple
from unittest.mock import PropertyMock, patch

import pytest

from clickgen.providers.jsonparser import HotspotsParser
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


def test_theme_configs_provider_sizes(bitmaps_dir, sizes, hotspots) -> None:
    with patch.object(
        ThemeConfigsProvider, "_ThemeConfigsProvider__sizes", new_callable=PropertyMock
    ) as mock_sizes:
        tcp = ThemeConfigsProvider(bitmaps_dir, hotspots, sizes=mock_sizes)

        mock_sizes.return_value = sizes
        assert sizes == tcp._ThemeConfigsProvider__sizes  # type: ignore


def test_theme_configs_provider_bitmaps_dir(bitmaps_dir, sizes, hotspots) -> None:
    with patch.object(
        ThemeConfigsProvider,
        "_ThemeConfigsProvider__bitmaps_dir",
        new_callable=PropertyMock,
    ) as mock_bitmaps_dir:
        tcp = ThemeConfigsProvider(mock_bitmaps_dir, hotspots, sizes)

        mock_bitmaps_dir.return_value = bitmaps_dir
        assert bitmaps_dir == tcp._ThemeConfigsProvider__bitmaps_dir  # type: ignore


def test_theme_configs_provider_cords(bitmaps_dir, sizes, hotspots) -> None:
    with patch.object(
        ThemeConfigsProvider,
        "_ThemeConfigsProvider__cords",
        new_callable=PropertyMock,
    ) as mock_hotspots:
        tcp = ThemeConfigsProvider(bitmaps_dir, mock_hotspots, sizes)

        mock_hotspots.return_value = HotspotsParser(hotspots)
        assert isinstance(tcp._ThemeConfigsProvider__cords, HotspotsParser)  # type: ignore


def test_theme_configs_provider_get_png_files_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__get_png_files()
        ThemeConfigsProvider.__get_png_files()  # type: ignore


def test_theme_configs_provider_list_static_png_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__list_static_png()
        ThemeConfigsProvider.__list_static_png  # type: ignore
