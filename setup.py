import subprocess
from setuptools import setup
from distutils.command.install import install as _install


class install(_install):
    def run(self):
        subprocess.call(['make', 'clean', '-C', 'src'])
        subprocess.call(['make', '-C', 'src'])
        _install.run(self)


# third-party dependencies
with open('./requirements.txt') as f:
    required = f.read().splitlines()

setup(
    author='Kaiz Khatri',
    cmdclass={
        'install': install,
    },
    install_requires=required,
    name='clickgen',
    package_data={'clickgen': ['xcursorgen.so']},
    packages=['clickgen'],
    version='1.0.0',
)
