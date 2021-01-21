# Installation

## Warnings

!!! warning
    clickgen CI & Building is tested on Linux platform only. Check [GitHub Action](https://github.com/ful1e5/clickgen/actions) for more detail.

## Python Support

clickgen supports these Python versions.

| **Python**          | **3.9** | **3.8** | **3.7** | **3.6** | **3.5** | **3.4** | **3.3** | **3.2** | **2.7** | **2.6** | **2.5** | **2.4** |
| ------------------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- | ------- |
| clickgen 1.1.7      | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.6      | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.5beta  | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.4beta  | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.3alpha | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.2alpha | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.1alpha | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |
| clickgen 1.1.0alpha | Yes     | Yes     | Yes     | Yes     |         |         |         |         |         |         |         |         |

## Basic Installation

!!! warning
    The following instructions will install clickgen library only. See [External Libraries](#external-libraries) for a full list of external libraries required by clickgen.

Install clickgen with **pip**:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade clickgen
```

## Building From Source

Download and extract the [compressed archive from PyPI](https://pypi.org/project/clickgen/).

### External Libraries

!!! note
    clickgen is using xcursorgen CLI internally for making xcursors.

xcursorgen require external libraries:

- **libpng** provides PNG functionality.
  - Starting with clickgen 1.1.0, libpng is required by default.
- **zlib** provides access to compressed PNGs.
  - Starting with clickgen 1.1.0, zlib is required by default.
- **libXcursor** X Window System Cursor management library.
  - Starting with clickgen 1.1.0, libXcursor is required by default.
- **libX11** Core X11 protocol client library.
  - Starting with clickgen 1.1.0, libX11 is required by default.

### Building on macOS

The easiest way to install external libraries is via [Homebrew](https://brew.sh/). After you install Homebrew, run:

```bash
brew install gcc libpng
brew install --cask xquartz
```

Now install clickgen with:

```bash
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade clickgen
```

or from within the uncompressed source directory:

```bash
python3 setup.py install
```

### Building on Linux

If you didn’t build Python from source, make sure you have Python’s development libraries installed.

In Debian or Ubuntu:

```bash
sudo apt-get install python3-dev python3-setuptools
```

In Fedora, the command is:

```bash
sudo dnf install python3-devel redhat-rpm-config
```

!!! note
    `redhat-rpm-config` is required on Fedora 23, but not earlier versions.

Prerequisites for **Ubuntu 16.04 LTS - 20.04 LTS** are installed with:

```bash
sudo apt install libx11-dev libxcursor-dev libpng-dev
```

Prerequisites are installed on **Arch Linux, Manjaro** with:

```bash
sudo pacman -S libx11 libxcursor libpng
```

Prerequisites are installed on recent **Red Hat, CentOS** or **Fedora** with:

```bash
sudo dnf install libx11-devel libxcursor-devel libpng-devel
```

Note that the package manager may be yum or DNF, depending on the exact distribution.

## Platform Support

Current platform support for clickgen. Binary distributions are contributed for each release on a volunteer basis, but the source should compile and run everywhere platform support is listed. In general, we aim to support all current versions of Linux and macOS.

### Continuous Integration Targets

These platforms are built and tested for every change.

| Operating system                | Tested Python versions | Tested architecture |
| ------------------------------- | ---------------------- | ------------------- |
| Ubuntu Linux 18.04 LTS (Bionic) | 3.8, 3.9               | x86-64              |

## Old Versions

You can download old distributions from the [release history at PyPI](https://pypi.org/project/clickgen/#history) and by direct URL access eg. [https://pypi.org/project/clickgen/1.1.0/](https://pypi.org/project/clickgen/1.1.0/).
