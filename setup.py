#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
from setuptools import setup, find_namespace_packages
from distutils.command.install import install as _install


class install(_install):
    def run(self):
        subprocess.call(["make", "clean", "-C", "xcursorgen"])
        subprocess.call(["make", "-C", "xcursorgen"])
        _install.run(self)


# readme.md as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="clickgen",
    version="1.1.7",
    author="Kaiz Khatri",
    author_email="kaizmandhu@gmail.com",
    description="X11 & Windows cursor building API 👷",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ful1e5/clickgen",
    cmdclass={"install": install},
    scripts=["scripts/clickgen"],
    keywords=["cursor", "xcursor", "windows", "linux", "anicursorgen", "xcursorgen"],
    install_requires=["Pillow>=7.2.0"],
    package_dir={"clickgen": "src"},
    packages=find_namespace_packages(include=["src", "src.*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "status_classifier",
        "Topic :: System :: Operating System",
        "Programming Language :: Python :: 3",
        "Programming Language :: C",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=True,
)
