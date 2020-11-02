#!/usr/bin/env python
# -*- coding: utf-8 -*-

from contextlib import contextmanager
from glob import glob
import itertools
from os import chdir, getcwd, listdir, path, remove, rename, symlink, unlink
from os.path import islink
import sys
from typing import Callable, List, Optional

from .db import CursorDB


@contextmanager
def _cd(dir_path: str):
    """ Temporary change directory context manager. """

    CWD = getcwd()
    chdir(dir_path)
    try:
        yield
    except:
        print(f"Exception caught: {sys.exc_info()[0]}", file=sys.stderr)
    finally:
        chdir(CWD)


class WinCursorsFixer(CursorDB):
    """ Rename Windows cursors accordinf to local database. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def run(self) -> List[str]:
        """ Run fixer. """
        for ext in ("*.ani", "*.cur"):
            self.__files.extend(glob(path.join(super().dir, ext)))

        if len(self.__files) == 0:
            print(
                f"'Windows' cursors not found in '{super().dir}'",
                file=sys.stderr,
            )

        # Renaming cursors according to master DB
        super().rename(self.__files)

        # Renaming cursors according to Win DB
        curs = listdir(super().dir)
        for cur, key in itertools.product(curs, super().win_db):
            ext: str = path.splitext(cur)[1]
            func: Callable[[str], str] = lambda x: f"{x}{ext}"
            l: List[str] = list(map(func, super().win_db[key]))

            if cur in l:
                src: str = path.join(super().dir, cur)
                dst: str = path.join(super().dir, key)

                print(f"Renaming '{cur}' to '{key}'")
                rename(src, dst)

        # Removing other cursors, That's not in Win DB
        rm_list: List[str] = list(listdir(super().dir) - super().win_db.keys())
        for e in rm_list:
            print(f"Deleting '{path.basename(e)}'")
            remove(path.join(super().dir, e))

        return listdir(super().dir)


class XCursorLinker(CursorDB):
    """ Create symlinks of missing `XCursors`. """

    __files: List[str] = []

    def __init__(self, dir: str) -> None:
        super().__init__(dir)

    def _find_relative_cursors(self, cur: str) -> Optional[List[str]]:
        """ Find relative cursors from local DB. """
        result: Optional[List[str]] = []

        for l in super().db:
            if cur in l:
                l.remove(cur)
                result.extend(l)

        if len(result) >= 0:
            return result
        else:
            return None

    def _clean_old_symlinks(self) -> None:
        for cur in listdir(super().dir):
            if islink(cur):
                unlink(cur)

    def _link(self, target: str, links: List[str]) -> None:
        """ Generate symlinks for @target. """
        for l in links:
            symlink(target, l)
            print(f"'{l}' symlink generated from '{target}'")

    def run(self) -> List[str]:
        """ Run linker. """
        func: Callable[[str], bool] = lambda x: x.split(".")[0] == x
        self.__files.extend(list(filter(func, glob(path.join(super().dir, "*")))))

        if len(self.__files) == 0:
            print(
                f"'XCursors' not found in '{super().dir}'",
                file=sys.stderr,
            )

        # Renaming cursors according to master DB
        super().rename(self.__files)

        # Create symlinks for missing cursors
        with _cd(super().dir):
            self._clean_old_symlinks()
            for cur in listdir(super().dir):
                rel_curs: Optional[List[str]] = self._find_relative_cursors(cur)
                if rel_curs:
                    self._link(cur, rel_curs)
                else:
                    continue

        return listdir(super().dir)
