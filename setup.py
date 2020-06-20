#!/usr/bin/env python
# encoding: utf-8

from pkginfo import *

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
        subprocess.call(['make', 'clean', '-C', 'src'])
        subprocess.call(['make', '-C', 'src'])
        _install.run(self)


# readme.md as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name=package_name,
      version=package_version,
      author=package_author,
      author_email=package_author_email,
      description=package_description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/KaizIqbal/clickgen',
      classifiers=[
          package_status_classifier, 'Topic :: System :: Operating System',
          'Programming Language :: Python :: 3', 'Programming Language :: C',
          'Natural Language :: English',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent', 'Typing :: Typed'
      ],
      python_requires='>=3.6',
      cmdclass={
          'install': install,
      },
      install_requires=load_requirements('requirements.txt'),
      packages=find_namespace_packages(include=['clickgen', 'clickgen.*']),
      include_package_data=True,
      zip_safe=True)
