import subprocess
from setuptools import setup
from distutils.command.install import install as _install


class install(_install):
    def run(self):
        subprocess.call(['make', 'clean', '-C', 'src'])
        subprocess.call(['make', '-C', 'src'])
        _install.run(self)


setup(
    name='clickgen',
    version='1.0.0',
    author='Kaiz Khatri',
    packages=['clickgen'],
    package_data={'clickgen': ['xcursorgen.so']},
    cmdclass={'install': install},
)
