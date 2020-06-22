#!/usr/bin/env python
# encoding: utf-8

import json
import subprocess
from setuptools import setup, find_namespace_packages
from distutils.command.install import install as _install

try:
    # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError:
    # for pip <= 9.0.3
    from pip.req import parse_requirements


# third-party dependencies
def load_requirements(fname):
    reqs = parse_requirements(fname, session='clickgen_session')
    return [str(ir.requirement) for ir in reqs]


class install(_install):
    def run(self):
        subprocess.call(['make', 'clean', '-C', 'xcursorgen'])
        subprocess.call(['make', '-C', 'xcursorgen'])
        _install.run(self)


# readme.md as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

with open('clickgen/pkginfo.json') as fp:
    _info = json.load(fp)

setup(name=_info['name'],
      version=_info['version'],
      author=_info['author'],
      author_email=_info['author_email'],
      description=_info['description'],
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/KaizIqbal/clickgen',
      classifiers=[
          _info['status_classifier'], 'Topic :: System :: Operating System',
          'Programming Language :: Python :: 3', 'Programming Language :: C',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent', 'Typing :: Typed'
      ],
      cmdclass={
          'install': install,
      },
      python_requires='>=3.6',
      scripts=['scripts/clickgen'],
      install_requires=load_requirements('requirements.txt'),
      packages=find_namespace_packages(include=['clickgen', 'clickgen.*']),
      include_package_data=True,
      zip_safe=True)
