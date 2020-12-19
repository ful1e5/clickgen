#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pathlib import Path
import pytest

from . import __path__ as root


@pytest.fixture(scope="module")
def bitmaps_dir() -> str:
    return Path(root[0]) / "assets" / "test_bitmaps"
