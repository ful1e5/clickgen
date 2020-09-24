import json
from clickgen import build_win_cursor_theme

with open('./hotspots.json', 'r') as hotspot_file:
    hotspots = json.loads(hotspot_file.read())

build_win_cursor_theme(
    name="My Cursor", image_dir="./bitmaps", cursor_sizes=[24, 28], hotspots=hotspots, out_path="./themes", delay=50)
