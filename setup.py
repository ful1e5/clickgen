import subprocess
from setuptools import setup, find_namespace_packages
from distutils.command.install import install as _install


class install(_install):
    def run(self):
        subprocess.call(['make', 'clean', '-C', 'src'])
        subprocess.call(['make', '-C', 'src'])
        _install.run(self)


# third-party dependencies
with open('./requirements.txt') as f:
    required = f.read().splitlines()

setup(author='Kaiz Khatri',
      cmdclass={
          'install': install,
      },
      install_requires=required,
      name='clickgen',
      package_data={'clickgen': ['xcursorgen.so']},
      packages=find_namespace_packages(include=['clickgen.*']),
      include_package_data=True,
      version='1.0.0',
      zip_safe=True)
