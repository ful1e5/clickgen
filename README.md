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

## Build Dependencies

- gcc

## External Libraries

- libxcursor-dev
- libx11-dev
- libpng-dev (<=1.6)

#### Install Dependencies

##### macOS

```bash
brew install --cask xquartz
brew install libpng gcc
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

Check [**examples**](https://github.com/ful1e5/clickgen/tree/main/examples) directory for building entire theme from `.png` files.

### create a static `XCursor`

```python
from pathlib import Path
from clickgen.builders import XCursor
from clickgen.core import CursorAlias

with CursorAlias.from_bitmap(png="all-scroll.png", hotspot=(5, 2)) as alias:
    x_cfg = alias.create(sizes=[(22, 22),(24, 24)])
    XCursor.create(alias_file=x_cfg, out_dir=Path("."))

```

### create an animated `XCursor`

```python
from pathlib import Path
from clickgen.builders import XCursor
from clickgen.core import CursorAlias

with CursorAlias.from_bitmap(png=["all-scroll-01.png", "all-scroll-02.png"], hotspot=(5, 2)) as alias:
    x_cfg = alias.create(sizes=[(22, 22),(24, 24)])
    XCursor.create(alias_file=x_cfg, out_dir=Path("."))

```


### create a static `Windows Cursor` (.cur)

```python
from pathlib import Path
from clickgen.builders import WindowsCursor
from clickgen.core import CursorAlias

with CursorAlias.from_bitmap(png="all-scroll.png", hotspot=(5, 2)) as alias:
    win_cfg = alias.create(sizes=(24, 24))
    WindowsCursor.create(alias_file=win_cfg, out_dir=Path("."))

```

### create an animated `Windows Cursor` (.ani)

```python
from pathlib import Path
from clickgen.builders import WindowsCursor
from clickgen.core import CursorAlias

with CursorAlias.from_bitmap(png=["all-scroll-01.png", "all-scroll-02.png"], hotspot=(5, 2)) as alias:
    win_cfg = alias.create(sizes=(24, 24))
    WindowsCursor.create(alias_file=win_cfg, out_dir=Path("."))

```