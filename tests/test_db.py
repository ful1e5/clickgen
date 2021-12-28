#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
.. moduleauthor:: Kaiz Khatri <kaizmandhu@gmail.com>
"""

import os
import tempfile
from pathlib import Path

import pytest

from clickgen.db import CursorDB


def test_CursorDB_exceptions() -> None:
    """Testing CursorDB ``TypeError`` exceptions."""
    with pytest.raises(TypeError) as excinfo:
        CursorDB("aa") # type: ignore
    assert str(excinfo.value) == "'data' is not type of 'List'"

    with pytest.raises(TypeError) as excinfo:
        CursorDB(["aa"]) # type: ignore
    assert str(excinfo.value) == "Item 'aa' is not type of 'Set'"


def test_CursorDB(data) -> None:
    """Testing CursorDB class members value."""
    db = CursorDB(data)
    assert db.data == {
        "aa": [],
        "bb": ["cc"],
        "cc": ["bb"],
        "ddddd": ["ffffff"],
        "ffffff": ["ddddd"],
    }


def test_CursorDB_str(data) -> None:
    """Testing CursorDB ``__str__`` datamethod."""
    db = CursorDB(data)
    assert (
        db.__str__()
        == "CursorDB(aa=[], bb=['cc'], cc=['bb'], ddddd=['ffffff'], ffffff=['ddddd'])"
    )


def test_CursorDB_repr(data) -> None:
    """Testing CursorDB ``__repr__`` datamethod."""
    db = CursorDB(data)
    assert (
        db.__repr__()
        == "{'aa': [], 'bb': ['cc'], 'cc': ['bb'], 'ddddd': ['ffffff'], 'ffffff': ['ddddd']}"
    )


def test_CursorDB_search_symlinks_without_find_similar(data) -> None:
    """Testing CursorDB search_symlinks method without ``find_similar`` argument."""
    db = CursorDB(data)
    value = db.search_symlinks("a")
    assert value is None

    value = db.search_symlinks("aa")
    assert value == []

    value = db.search_symlinks("bb")
    assert value == ["cc"]


def test_CursorDB_search_symlinks_with_find_similar(data) -> None:
    """Testing CursorDB search_symlinks method with ``find_similar`` argument."""
    db = CursorDB(data)
    value = db.search_symlinks("a", find_similar=True)
    assert value == []

    value = db.search_symlinks("fffaf", find_similar=True)
    assert value == ["ddddd"]

    value = db.search_symlinks("bb", find_similar=True)
    assert value == ["cc"]


def test_CursorDB_rename_file_is_not_file_exception(data) -> None:
    """Testing CursorDB rename_file method ``FileNotFoundError`` exception. """
    db = CursorDB(data)
    test_p = Path(str(tempfile.tempdir)) / "fffaf"
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
    """Testing CursorDB rename_file method."""
    db = CursorDB(data)

    test_p = Path(str(tempfile.tempdir)) / "fffaf"
    test_p.write_text("test")

    return_p = db.rename_file(test_p)
    assert str(return_p) == str(Path(str(tempfile.tempdir)) / "ffffff")

    test_p.unlink(missing_ok=True)

    test_p1 = Path(str(tempfile.tempdir)) / "aa"
    test_p1.write_text("test")

    return_p = db.rename_file(test_p1)
    assert return_p is None

    test_p1.unlink(missing_ok=True)
