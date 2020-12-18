import json
from pathlib import Path

from clickgen import clickgen
from clickgen.typing.core import Config, ThemeInfo, ThemeSettings, JsonData

with open("./hotspots.json", "r") as hotspot_file:
    hotspots: JsonData = json.loads(hotspot_file.read())

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

clickgen.create_theme(cfg)
