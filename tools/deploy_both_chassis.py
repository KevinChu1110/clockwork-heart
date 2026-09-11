#!/usr/bin/env python3
import shutil
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

# 1. Save clean paint_ivory_stock.png
ivory = Image.open("/tmp/clean_master_ivory.png").convert("RGBA")
# Ensure tail loop pixels are set to the shadow tone (31, 26, 58, 70)
ivory.putpixel((97, 51), (31, 26, 58, 70))
ivory.putpixel((98, 51), (31, 26, 58, 70))
ivory.putpixel((98, 52), (31, 26, 58, 70))
ivory.putpixel((92, 61), (31, 26, 58, 15))
ivory_path = f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png"
ivory.save(ivory_path)
print(f"✓ Saved {ivory_path}")

# 2. Save clean paint_bamboo_bronze.png
bronze = Image.open("/tmp/test_pure_bronze.png").convert("RGBA")
bronze_path = f"{MACAQUE_DIR}/chassis/paint_bamboo_bronze.png"
bronze.save(bronze_path)
print(f"✓ Saved {bronze_path}")
