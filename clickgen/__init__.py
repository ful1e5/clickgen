#!/usr/bin/env python
# encoding: utf-8

import json
import os

from .__main__ import main as build, x11_gen, win_gen, link_cursors, create_x11_template
from .linker import linker
from .template import template

with open(os.path.join(os.path.dirname(__file__), 'pkginfo.json')) as fp:
    _info = json.load(fp)

__version__ = _info['version']
info = _info
