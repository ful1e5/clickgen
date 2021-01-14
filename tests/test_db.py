#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from clickgen.db import CursorDB


def test_CursorDB_exceptions() -> None:
    data = "aa"
    with pytest.raises(TypeError) as excinfo:
        CursorDB(data)
    assert str(excinfo.value) == "'data' is not type of 'List'"

    data = ["aa"]
    with pytest.raises(TypeError) as excinfo:
        CursorDB(data)
    assert str(excinfo.value) == "Item 'aa' is not type of 'Set'"


def test_CursorDB(data) -> None:
    db = CursorDB(data)
    assert db.data == {
        "aa": [],
        "bb": ["cc"],
        "cc": ["bb"],
        "ddddd": ["ffffff"],
        "ffffff": ["ddddd"],
    }


def test_CursorDB_str(data) -> None:
    db = CursorDB(data)
    assert (
        db.__str__()
        == "CursorDB(aa=[], cc=['bb'], bb=['cc'], ffffff=['ddddd'], ddddd=['ffffff'])"
    )


def test_CursorDB_repr(data) -> None:
    db = CursorDB(data)
    assert (
        db.__repr__()
        == "{'aa': [], 'cc': ['bb'], 'bb': ['cc'], 'ffffff': ['ddddd'], 'ddddd': ['ffffff']}"
    )
