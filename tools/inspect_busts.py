#!/usr/bin/env python3
from PIL import Image

for name in ["ember_tiger", "cloud_crane", "iron_bear", "rabbit", "fox_mage"]:
    p = f"/opt/side/bravesoul-game/game/assets/sprites/portraits/{name}.png"
    im = Image.open(p)
    print(f"[{name:12s}] size={im.size} mode={im.mode} bbox={im.getbbox()}")
