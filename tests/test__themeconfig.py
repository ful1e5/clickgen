#!/usr/bin/env python
# -*- coding: utf-8 -*-

from typing import List, Tuple

import pytest

from clickgen.providers.themeconfig import _clean_cur_name

testdata: List[Tuple[str, str]] = [
    ("/foo/bar-01", "/foo/bar"),
    ("/foo/b-000000001", "/foo/b"),
    ("/foo/b", "/foo/b"),
    ("/foo/bsd-gg", "/foo/bsd"),
    ("/foo/rr.ds=ds-rf", "/foo/brr.ds=ds"),
]


@pytest.mark.parametrize("arg, result", testdata)
def test_clean_cur_name(arg, result) -> None:
    assert _clean_cur_name(arg) == result
