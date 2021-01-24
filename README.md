[![CI](https://github.com/ful1e5/clickgen/workflows/CI/badge.svg)](https://github.com/ful1e5/clickgen/actions)
[![PyPI - Wheel](https://img.shields.io/pypi/wheel/pytype)](https://pypi.org/project/clickgen/#files)
[![Code Coverage](https://codecov.io/gh/ful1e5/clickgen/branch/main/graph/badge.svg)](https://codecov.io/gh/ful1e5/clickgen)
[![CodeFactor](https://www.codefactor.io/repository/github/ful1e5/clickgen/badge/main)](https://www.codefactor.io/repository/github/ful1e5/clickgen/overview/main)

# Clickgen

The hustle free cursor building toolbox 🧰

**clickgen** is _API_ for building **X11** and **Windows** Cursors from `.png` files. clickgen is using `anicursorgen` and `xcursorgen` _under the hood_.

## Install

### using pip

```bash
pip3 install clickgen
```

### ArchLinux

```bash
yay -S python-clickgen
```

### Manjaro

```bash
pamac build python-clickgen
```

## CLI

```
clickgen -h
```

## PyPi Dependencies

- Pillow/python-pillow

## Runtime Dependencies

- libxcursor-dev
- libx11-dev
- libpng-dev (<=1.6)

#### Install Runtime Dependencies

##### macOS

```bash
brew cask install xquartz libpng
```

##### Debain/ubuntu

```bash
sudo apt install libx11-dev libxcursor-dev libpng-dev
```

##### ArchLinux/Manjaro

```bash
sudo pacman -S libx11 libxcursor libpng
```

##### Fedora/Fedora Silverblue/CentOS/RHEL

```bash
sudo dnf install libx11-devel libxcursor-devel libpng-devel
```

## Examples

Check [**examples**](./examples/) directory.