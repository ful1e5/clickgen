#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.command.install import install as _install
import json
import subprocess

from setuptools import find_namespace_packages, setup


class install(_install):
    def run(self):
        subprocess.call(["make", "clean", "-C", "xcursorgen"])
        subprocess.call(["make", "-C", "xcursorgen"])
        _install.run(self)


# readme.md as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

with open("clickgen/pkginfo.json") as fp:
    _info = json.load(fp)

setup(
    name=_info["name"],
    version=_info["version"],
    author=_info["author"],
    author_email=_info["author_email"],
    description=_info["description"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ful1e5/clickgen",
    classifiers=[
        _info["status_classifier"],
        "Topic :: System :: Operating System",
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    cmdclass={"install": install},
    python_requires=">=3.6",
    scripts=["scripts/clickgen"],
    keywords=["cursor", "xcursor", "windows", "linux", "anicursorgen", "xcursorgen"],
    install_requires=["Pillow>=7.2.0"],
    packages=find_namespace_packages(include=["clickgen", "clickgen.*"]),
    include_package_data=True,
    zip_safe=True,
)
