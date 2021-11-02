#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from distutils.command.install import install as _install
from shutil import which

from setuptools import setup


def make_path() -> str:
    path = which("make")
    if not path:
        raise Exception("'make' command not found")
    return path


class install(_install):
    def run(self):
        subprocess.call([make_path(), "-C", "xcursorgen"])
        _install.run(self)


setup(cmdclass={"install": install})
