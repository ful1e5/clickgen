<!-- Branding -->
<p align="center">
  <img src="https://imgur.com/L2IZ2MH.png" width="120" alt="clickgen" />
  <br />
  <img src="https://i.imgur.com/TeItlMh.png" width="200" />
</p>

<p align="center">
  X11 & Windows cursor building API 👷
</p>

<!-- Badges -->
<p align="center">
  <a href="https://github.com/ful1ie5/clickgen/actions?query=workflow%3Abuild">
    <img alt="GitHub Action Build" src="https://github.com/ful1e5/clickgen/workflows/build/badge.svg" />
  </a>

  <a href="https://badge.fury.io/py/clickgen">
    <img src="https://badge.fury.io/py/clickgen.svg" alt="PyPI version" height="20">
  </a>

  <a href="https://www.codefactor.io/repository/github/ful1e5/clickgen">
    <img src="https://www.codefactor.io/repository/github/ful1e5/clickgen/badge" alt="CodeFactor" />
  </a>
</p>

---

# Clickgen

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

🔥 Check **examples** [here](./examples/)

> **Recommended**: Design Cursor `bitmaps` images(.png) in 200x200 pixel for **HiDPI** size support.
> **Note**: Provide cursor's hotspot respect to `bitmaps`, Clickgen's `Linker` automatically generate hotspots for each `cursor_sizes`.
> Check [hotspots.json](./examples/hotspots.json) file for more info.

### Generate Cursor's config files (.in)

```python
import json
from clickgen import configsgen

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

configsgen.generate_configs(
    imgs_dir="./bitmaps", cursor_sizes=[24, 28], out_dir="./configs", delay=50)
```

### Build Cursor Theme

```python
import json
from clickgen import build_cursor_theme

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

build_cursor_theme(
    name="My Cursor", image_dir="./bitmaps", cursor_sizes=[24, 28], hotspots=hotspots, out_path="./themes", delay=50)

```

### Build only `x11` cursor theme

```python
import json
from clickgen import build_x11_cursor_theme

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

build_x11_cursor_theme(
    name="My Cursor", image_dir="./bitmaps", cursor_sizes=[24, 28], hotspots=hotspots, out_path="./themes", delay=50)
```

### Build only `Windows` cursor theme

```python
import json
from clickgen import build_win_cursor_theme

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

build_win_cursor_theme(
    name="My Cursor", image_dir="./bitmaps", cursor_sizes=[24, 28], hotspots=hotspots, out_path="./themes", delay=50)
```
