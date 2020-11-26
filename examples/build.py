# from clickgen.configs import Config, ThemeInfo, ThemeSettings
# import json
# from clickgen.clickgen import create_theme

# with open("./hotspots.json", "r") as hotspot_file:
#     hotspots = json.loads(hotspot_file.read())

# info: ThemeInfo = ThemeInfo(
#     theme_name="BQ", author="Kaiz Khatri", comment=None, url=None
# )

# sett: ThemeSettings = ThemeSettings(
#     bitmaps_dir="./bitmaps",
#     sizes=[24, 28],
#     hotspots=hotspots,
#     animation_delay=60,
#     out_dir="./themes",
# )
# cfg: Config = Config(info, sett)
# create_theme(cfg)

from os import path
from clickgen.providers.bitmaps import Bitmaps


b = Bitmaps(path.abspath("./bitmaps"))