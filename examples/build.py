import json
from pathlib import Path

from clickgen.clickgen import create_theme
from clickgen.typing import Config, ThemeInfo, ThemeSettings

with open("./hotspots.json", "r") as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

info: ThemeInfo = ThemeInfo(theme_name="BQ", author="Kaiz Khatri")
bitmap_dir = Path("./bitmaps")
out_dir = Path("./themes")

sett: ThemeSettings = ThemeSettings(
    bitmaps_dir=bitmap_dir,
    sizes=[24, 28],
    hotspots=hotspots,
    animation_delay=60,
    out_dir=out_dir,
)
cfg: Config = Config(info, sett)

create_theme(cfg)
