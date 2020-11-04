#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from os import path
from tests.conftest import sizes
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


# __get_png_files()
def test_theme_configs_provider_get_png_files_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__get_png_files()
        ThemeConfigsProvider.__get_png_files()  # type: ignore


# __list_static_png()
def test_theme_configs_provider_list_static_png_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__list_static_png()
        ThemeConfigsProvider.__list_static_png  # type: ignore


# __list_animated_png()
def test_theme_configs_provider_list_animated_png_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__list_animated_png()
        ThemeConfigsProvider.__list_animated_png()  # type: ignore


# __resize_cursor()
def test_theme_configs_provider_resize_cursor_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider, hotspots, sizes
) -> None:
    with pytest.raises(AttributeError):
        tcp.__resize_cursor(hotspots[0], sizes[0])
        ThemeConfigsProvider.__resize_cursor(hotspots[0], sizes[0])  # type: ignore


# __write_cfg_file()
def test_theme_configs_provider_write_cfg_file_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider, hotspots, lines
) -> None:
    with pytest.raises(AttributeError):
        tcp.__write_cfg_file(hotspots[0], lines)
        ThemeConfigsProvider.__write_cfg_file(hotspots[0], lines)  # type: ignore


# __generate_cursor()
def test_theme_configs_provider_generate_cursor_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider, hotspots
) -> None:
    with pytest.raises(AttributeError):
        tcp.__generate_cursor(hotspots[0])
        ThemeConfigsProvider.__generate_cursor(hotspots[0])  # type: ignore


# __generate_static_cfg
def test_theme_configs_provider_generate_static_cfgs_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__generate_static_cfgs()
        ThemeConfigsProvider.__generate_static_cfgs()  # type: ignore


# __generate_animated_cfg
def test_theme_configs_provider_generate_animated_cfgs_raise_attribute_error_exception(
    tcp: ThemeConfigsProvider,
) -> None:
    with pytest.raises(AttributeError):
        tcp.__generate_animated_cfgs(50)
        ThemeConfigsProvider.__generate_animated_cfgs(50)  # type: ignore


# generate()
def test_theme_configs_provider_generate(tcp: ThemeConfigsProvider) -> None:
    a = tcp.generate(50)
    assert a == tcp.config_dir


def test_theme_configs_provider_generate_dir_is_not_empty(
    tcp: ThemeConfigsProvider,
) -> None:
    a = tcp.generate(50)
    assert len(os.listdir(a)) > 0


def test_theme_configs_provider_generate_configs_dir_files(
    tcp: ThemeConfigsProvider,
) -> None:
    a = tcp.generate(50)
    assert sorted(os.listdir(a)) == sorted(["b.in", "a.in", "c.in", "2x2", "1x1"])


def test_theme_configs_provider_generate_configs_dir_image_files(
    tcp: ThemeConfigsProvider, sizes
) -> None:
    a = tcp.generate(50)
    expected = ["a.png", "b.png", "c-01.png", "c-02.png"]

    for s in sizes:
        d = path.join(a, f"{s}x{s}")
        assert sorted(os.listdir(d)) == sorted(expected)
