#!/usr/bin/env python
# encoding: utf-8

import json
import os

from .__main__ import main as build

from .x11 import main as x11_gen

from .win import main as win_gen

from .linker.__main__ import link_cursors
from .linker import linker

from .template.__main__ import create_x11_template
from .template import template

from .configsgen.__main__ import generate_animated_cursor, generate_static_cursor
from .configsgen import configsgen

from .build import build_cursor_theme, build_win_curosr_theme, build_x11_curosr_theme

with open(os.path.join(os.path.dirname(__file__), 'pkginfo.json')) as fp:
    _info = json.load(fp)

__version__ = _info['version']
info = _info
