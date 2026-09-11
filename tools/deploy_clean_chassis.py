#!/usr/bin/env python3
import shutil
from PIL import Image

src = "/tmp/clean_master_ivory.png"
dst = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"

im = Image.open(src).convert("RGBA")
# Ensure tail loop pixels are set to the shadow tone (31, 26, 58, 70)
im.putpixel((97, 51), (31, 26, 58, 70))
im.putpixel((98, 51), (31, 26, 58, 70))
im.putpixel((98, 52), (31, 26, 58, 70))
im.putpixel((92, 61), (31, 26, 58, 15))
im.save(dst)
print("✓ Saved clean paint_ivory_stock.png")

# Now rebuild paint_bamboo_bronze.png using the clean formula
import sys
sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.build_macaque_bronze_chassis import create_macaque_paint_bamboo_bronze

bronze_dst = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png"
create_macaque_paint_bamboo_bronze(dst, bronze_dst)
print("✓ Rebuilt clean paint_bamboo_bronze.png")
