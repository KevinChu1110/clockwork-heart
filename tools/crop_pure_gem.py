#!/usr/bin/env python3
from PIL import Image

im = Image.open("/tmp/lion_orb_chest.png").convert("RGBA")
bbox = im.getbbox()
print("Chest orb bbox inside (185..270, 260..320):", bbox)
# 裁出剛好是這顆寶石
gem = im.crop(bbox)
gem.save("/tmp/pure_gem.png")
print("Pure gem size:", gem.size)
