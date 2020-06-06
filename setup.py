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

# readme.md as long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(version='1.0.1',
      author='Kaiz Khatri',
      author_email='kaizmandhu@gmail.com',
      description='X11 & Windows Cursor API 👷',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
          "Programming Language :: Python :: 3",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      python_requires='>=3.6',
      cmdclass={
          'install': install,
      },
      install_requires=required,
      name='clickgen',
      packages=find_namespace_packages(include=['clickgen', 'clickgen.*']),
      include_package_data=True,
      zip_safe=True)
