import json
import os

from .__main__ import main

with open(os.path.join(os.path.dirname(__file__), 'pkginfo.json')) as fp:
    _info = json.load(fp)

__version__ = _info['version']
info = _info
