#!/usr/bin/env python3
from PIL import Image
import sys
sys.path.insert(0, "/opt/side/bravesoul-game")
from tools.build_macaque_bronze_chassis import create_macaque_paint_bamboo_bronze

ivory_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
im = Image.open(ivory_path).convert("RGBA")
im.putpixel((97, 51), (31, 26, 58, 70))
im.putpixel((98, 51), (31, 26, 58, 70))
im.putpixel((98, 52), (31, 26, 58, 70))
im.putpixel((92, 61), (31, 26, 58, 15))
im.save(ivory_path)
print("✓ Restored tail ring shadow in ivory")

bronze_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png"
create_macaque_paint_bamboo_bronze(ivory_path, bronze_path)
print("✓ Rebuilt bronze chassis")
