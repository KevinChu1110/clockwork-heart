#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
HERO_BOAR = f"{REPO_ROOT}/web/media/hero/char_boar.png"

im = Image.open(HERO_BOAR).convert("RGBA")
# 戰錘在原圖的 (40, 500, 500, 1150)
hammer = im.crop((40, 500, 500, 1150))
hammer.save("/tmp/hero_hammer_full.png")
print("Saved /tmp/hero_hammer_full.png")
