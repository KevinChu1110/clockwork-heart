#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

for fn in ["paint_ivory_stock_512.png", "paint_bamboo_bronze_512.png"]:
    p = f"{MACAQUE_DIR}/chassis/{fn}"
    im = Image.open(p).convert("RGBA")
    pixel = im.getpixel((230, 140))
    print(f"{fn} at (230, 140): {pixel}")
