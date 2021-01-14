#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import tempfile
from pathlib import Path

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
        == "CursorDB(aa=[], bb=['cc'], cc=['bb'], ddddd=['ffffff'], ffffff=['ddddd'])"
    )


def test_CursorDB_repr(data) -> None:
    db = CursorDB(data)
    assert (
        db.__repr__()
        == "{'aa': [], 'bb': ['cc'], 'cc': ['bb'], 'ddddd': ['ffffff'], 'ffffff': ['ddddd']}"
    )


def test_CursorDB_search_symlinks_without_find_similar(data) -> None:
    db = CursorDB(data)
    value = db.search_symlinks("a")
    assert value is None

    value = db.search_symlinks("aa")
    assert value == []

    value = db.search_symlinks("bb")
    assert value == ["cc"]


def test_CursorDB_search_symlinks_with_find_similar(data) -> None:
    db = CursorDB(data)
    value = db.search_symlinks("a", find_similar=True)
    assert value == []

    value = db.search_symlinks("fffaf", find_similar=True)
    assert value == ["ddddd"]

    value = db.search_symlinks("bb", find_similar=True)
    assert value == ["cc"]


def test_CursorDB_rename_file_is_not_file_exception(data) -> None:
    db = CursorDB(data)
    test_p = Path(tempfile.tempdir) / "fffaf"
    with pytest.raises(FileNotFoundError) as excinfo:
        db.rename_file(test_p)
    assert str(excinfo.value) == f"'{test_p}' is not file"
    test_p.unlink(missing_ok=True)

    test_p1 = Path(tempfile.mkdtemp())
    with pytest.raises(FileNotFoundError) as excinfo:
        db.rename_file(test_p1)
    assert str(excinfo.value) == f"'{test_p1}' is not file"
    os.rmdir(test_p1)


def test_CursorDB_rename_file(data) -> None:
    db = CursorDB(data)

    test_p = Path(tempfile.tempdir) / "fffaf"
    test_p.write_text("test")

    return_p = db.rename_file(test_p)
    assert str(return_p) == str(Path(tempfile.tempdir) / "ffffff")

    test_p.unlink(missing_ok=True)

    test_p1 = Path(tempfile.tempdir) / "aa"
    test_p1.write_text("test")

    return_p = db.rename_file(test_p1)
    assert return_p is None

    test_p1.unlink(missing_ok=True)
