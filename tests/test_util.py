#!/usr/bin/env python
# -*- coding: utf-8 -*-


from os import getcwd, symlink
from pathlib import Path
from clickgen import util
from clickgen.util import chdir
import tempfile


def test_chdir() -> None:
    current = getcwd()
    with chdir(tempfile.tempdir):
        assert tempfile.tempdir == getcwd()
    assert getcwd() == current


def test_remove_util() -> None:
    tmp_dir = Path(tempfile.mkdtemp())
    tmp_file = Path(tempfile.mkstemp()[1])
    tmp_link = tmp_dir / "link"
    symlink(tmp_file, tmp_link)

    util.remove_util(tmp_dir)
    assert tmp_dir.exists() is False

    util.remove_util(tmp_file)
    assert tmp_file.exists() is False

    util.remove_util(tmp_link)
    assert tmp_link.exists() is False
