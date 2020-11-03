#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from typing import List, Tuple
from clickgen.providers.themeconfig import _clean_cur_name

testdata: List[Tuple[str, str]] = [
    ("/foo/bar-01", "/foo/bar"),
    ("/foo/b-000000001", "/foo/b"),
    ("/foo/b", "/foo/b"),
]


@pytest.mark.parametrize("arg, result", testdata)
def test_clean_cur_name(arg, result) -> None:
    assert _clean_cur_name(arg) == result
