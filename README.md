<!-- Branding -->
<p align="center">
  <img src="https://imgur.com/L2IZ2MH.png" width="120" alt="clickgen" />
  <br />
  <img src="https://i.imgur.com/TeItlMh.png" width="200" />
</p>

<p align="center">
  X11 & Windows Cursor Building API 👷
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

# Install

```bash
pip3 install clickgen
```

# Examples

## Generating Cursor config(.in) files

```python
import json
from clickgen import configsgen

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

configsgen.generate_configs(
    imgs_dir="./bitmaps", cursor_sizes=[24, 28], out_dir="./configs", delay=45)
```
