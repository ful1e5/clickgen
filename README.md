# Clickgen

[![ci](https://github.com/ful1e5/clickgen/actions/workflows/ci.yml/badge.svg)](https://github.com/ful1e5/clickgen/actions/workflows/ci.yml)
[![code coverage](https://codecov.io/gh/ful1e5/clickgen/branch/main/graph/badge.svg)](https://codecov.io/gh/ful1e5/clickgen)

**Clickgen** is cross-platform python library for building **X11** and **Windows** Cursors.
Clickgen's core functionality is heavily inspired by **[quantum5/win2xcur](https://github.com/quantum5/win2xcur)**
from `clickgen v2.0.0` and onwards.

##### Become Sponsor

This library is funded by the community. I appreciate all these wonderful people who patronize and sponsoring me.

Visit the [GitHub Sponsor](https://github.com/sponsors/ful1e5) page to become a partner.
DM me on [Twitter](https://twitter.com/ful1e5) if your company would like to sponsor this library,
I will gladly look into it and embed your logo in the README.

##### Sponsors

<!-- Add your name and avatar here with the Pull Request in case I missed it. -->

Be you first.

## Notices

- **2022-06-15:** Docker Image support deprecated due to cross-platform compatibility.
- **2022-07-09:** :warning: All the **functionality and modules are removed from older versions in `v2.0.0`**.
  I will be restricting any updates to the `>=v1.2.0` versions to security updates and hotfixes.
  Check updated documentations for [building cursors from API](#api-examples) and [CLIs](#clis) usage.

## Requirements

- Python version 3.7 or higher
- [Pillow](https://pypi.org/project/Pillow) >= 8.1.1
- [toml](https://pypi.org/project/toml) >= 0.10.2
- [numpy](https://pypi.org/project/numpy) >= 1.21.6

## Install

```bash
pip3 install clickgen
```

> **Note**
> Distributions' packages are not affiliated with clickgen developers.
> If you encounter any issues with the incorrect installation, you should contact the package maintainer first.

### Arch Linux

- [AUR](https://aur.archlinux.org/packages/python-clickgen)

## Usage

### `clickgen` CLI

#### Linux Format (XCursor)

For example, if you have to build [ponter.png](https://github.com/ful1e5/clickgen/blob/main/samples/pngs/pointer.png)
file to Linux Format:

```
clickgen samples/pngs/pointer.png -x 10 -y 10 -s 22 24 32 -p x11
```

You also **build animated Xcursor** by providing multiple png files to argument and animation delay with `-d`:

```
clickgen samples/pngs/wait-001.png samples/pngs/wait-001.png -d 3 -x 10 -y 10 -s 22 24 32 -p x11
```

#### Windows Formats (.cur and .ani)

To build [ponter.png](https://github.com/ful1e5/clickgen/blob/main/samples/pngs/pointer.png)
file to Windows Format (`.cur`):

> **Warning: Windows Cursor only support single size.**

```
clickgen samples/pngs/pointer.png -x 10 -y 10 -s 32 -p windows
```

For **animated Windows Cursor** (`.ani`):

```
clickgen samples/pngs/wait-001.png samples/pngs/wait-001.png -d 3 -x 10 -y 10 -s 32 -p windows
```

For more information, run `clickgen --help`.

### `ctgen` CLI

This CLI allow you to generate Windows and Linux Cursor themes from config (.toml) file.

```
ctgen theme.toml
```

You also provide multiple theme configuration file once as following:

```
ctgen theme1.toml theme2.toml
```

Override theme's `name` of theme with `-n` option:

```
ctgen theme1.toml -n "New Theme"
```

You can run `ctgen --help` to view all available options and you also check
[samples](https://github.com/ful1e5/clickgen/blob/main/samples) directory for more information.

### API Examples

### Static `XCursor`

```python
from clickgen.parser import open_blob
from clickgen.writer import to_x11

with open("samples/pngs/pointer.png", "rb") as p:
    cur = open_blob([p.read()], hotspot=(50, 50))

    # save X11 static cursor
    xresult = to_x11(cur.frames)
    with open("xtest", "wb") as o:
        o.write(xresult)
```

### Animated `XCursor`

```python
from glob import glob

from clickgen.parser import open_blob
from clickgen.writer import to_x11

# Get .png files from directory
fnames = glob("samples/pngs/wait-*.png")
pngs: List[bytes] = []

# Reading as bytes
for f in sorted(fnames):
    with open(f, "rb") as p:
        pngs.append(p.read())

cur = open_blob(pngs, hotspot=(100, 100))

# save X11 animated cursor
result = to_x11(cur.frames)
with open("animated-xtest", "wb") as o:
    o.write(result)
```

### Static `Windows Cursor` (.cur)

```python
from clickgen.parser import open_blob
from clickgen.writer import to_win

with open("samples/pngs/pointer.png", "rb") as p:
    cur = open_blob([p.read()], hotspot=(50, 50))

    # save Windows static cursor
    ext, result = to_win(cur.frames)
    with open(f"test{ext}", "wb") as o:
        o.write(result)
```

### Animated `Windows Cursor` (.ani)

```python
from glob import glob

from clickgen.parser import open_blob
from clickgen.writer import to_win

# Get .png files from directory
fnames = glob("samples/pngs/wait-*.png")
pngs: List[bytes] = []

# Reading as bytes
for f in sorted(fnames):
    with open(f, "rb") as p:
        pngs.append(p.read())

cur = open_blob(pngs, hotspot=(100, 100))

# save Windows animated cursor
ext, result = to_win(cur.frames)
with open(f"test-ani{ext}", "wb") as o:
    o.write(aresult)
```

### Documentation

Check [wiki](https://github.com/ful1e5/clickgen/wiki) for documentation.
