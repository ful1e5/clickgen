#!/usr/bin/env python
# -*- coding: utf-8 -*-

from clickgen.builders.x11builder import X11CursorsBuilder


def test_x11builder(config_dir, out_dir) -> None:
    X11CursorsBuilder(config_dir, out_dir)
