#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

for fn in ["ear_macaque_coaxial_512.png", "ear_macaque_coaxial_bronze_512.png", "ear_macaque_coaxial_ivory_512.png"]:
    p = f"{MACAQUE_DIR}/head_unit/{fn}"
    im = Image.open(p).convert("RGBA")
    # 檢查眼窩中心 (230, 140)
    pixel = im.getpixel((230, 140))
    print(f"{fn} at (230, 140): {pixel}")
