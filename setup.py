#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import find_namespace_packages
from distutils.core import Extension, setup

xcursorgen_module = Extension(
    "xcursorgen",
    define_macros=[("MAJOR_VERSION", "1"), ("MINOR_VERSION", "0")],
    include_dirs=["/usr/local/include"],
    runtime_library_dirs=["X11", "Xcursor", "png", "z"],
    library_dirs=["/usr/local/lib"],
    sources=["xcursorgen/xcursorgen.c", "xcursorgen/xcursorgen.h"],
)

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
    ext_modules=[xcursorgen_module],
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
    zip_safe=True,
)
