#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import shutil
import tempfile
from os import getcwd, symlink
from pathlib import Path
from contextlib import redirect_stdout

import pytest
from clickgen.util import PNGProvider, chdir, debug, timer, remove_util

from tests.utils import create_test_image


def test_chdir() -> None:
    current = getcwd()
    with chdir(tempfile.tempdir):
        assert tempfile.tempdir == getcwd()
    assert getcwd() == current


def test_remove_util() -> None:
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_file = tempfile.mkstemp()[1]
    tmp_link = tmp_dir / "link"
    symlink(tmp_file, tmp_link)

    remove_util(tmp_dir)
    assert tmp_dir.exists() is False

    remove_util(tmp_file)
    assert os.path.exists(tmp_file) is False

    remove_util(tmp_link)
    assert tmp_link.exists() is False


def test_PNGProvider_exception(tmpdir_factory: pytest.TempdirFactory) -> None:
    directory = Path(tmpdir_factory.mktemp("tt"))
    with pytest.raises(FileNotFoundError) as excinfo:
        PNGProvider(directory)
    assert str(excinfo.value) == f"'*.png' files not found in '{directory.absolute()}'"
    shutil.rmtree(directory)


def test_PNGProvider(image_dir) -> None:
    create_test_image(image_dir, 3)
    p = PNGProvider(image_dir)
    p_str = PNGProvider(str(image_dir))
    assert p.bitmaps_dir == p_str.bitmaps_dir


def test_PNGProvider_get(tmpdir_factory: pytest.TempdirFactory) -> None:
    d = tmpdir_factory.mktemp("ffff")
    directory = Path(d)

    # static
    images = create_test_image(directory, 1, key="static")
    p = PNGProvider(directory)
    assert p.get("static") == images[0]

    # animated
    images1 = create_test_image(directory, 4, key="animated")
    p1 = PNGProvider(directory)
    assert sorted(p1.get("animated")) == sorted(images1)

    shutil.rmtree(d)


# Only for Developer testing
def test_timer_wrapper_func() -> None:
    @timer
    def pp() -> None:
        print("time ?")

    f = io.StringIO()
    with redirect_stdout(f):
        pp()

    assert "time ?" in f.getvalue()
    assert "Finished 'pp' in" in f.getvalue()


def test_debug_wrapper_func() -> None:
    @debug
    def pp(a: int) -> int:
        return a - 1

    f = io.StringIO()
    with redirect_stdout(f):
        pp(2)

    assert f.getvalue() == "Calling pp(2)\n'pp' returned 1\n"
