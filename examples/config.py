import json
from clickgen import configsgen

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

configsgen.generate_configs(
    imgs_dir="./bitmaps", cursor_sizes=[24, 28], out_dir="./configs", delay=45)
