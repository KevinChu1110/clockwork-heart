#!/usr/bin/env python3
import sys
sys.path.insert(0, "/opt/side/bravesoul-game")

from PIL import Image
from tools.build_macaque_bronze_chassis import create_macaque_paint_bamboo_bronze

# 1. Update ivory chassis
ivory = Image.open("/tmp/clean_master_ivory.png").convert("RGBA")
# Remove floating pixels:
ivory.putpixel((97, 51), (0, 0, 0, 0))
ivory.putpixel((98, 51), (0, 0, 0, 0))
ivory.putpixel((98, 52), (0, 0, 0, 0))
ivory.putpixel((92, 61), (0, 0, 0, 0))
ivory_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
ivory.save(ivory_path)
print(f"✓ Saved {ivory_path}")

# 2. Build bronze chassis from ivory
bronze_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png"
create_macaque_paint_bamboo_bronze(ivory_path, bronze_path)
print(f"✓ Saved {bronze_path}")
