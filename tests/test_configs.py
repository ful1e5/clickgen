#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.configs import ThemeInfo


def test_theme_info():
    t = ThemeInfo(theme_name="foo", author="bar")
    assert isinstance(t, ThemeInfo)

    assert t.comment == None
    assert isinstance(t.theme_name, str)
    assert isinstance(t.author, str)
    assert t.url == "Unknown Source!"
