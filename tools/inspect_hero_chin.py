#!/usr/bin/env python3
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
HERO_BOAR = f"{REPO_ROOT}/web/media/hero/char_boar.png"

im = Image.open(HERO_BOAR).convert("RGBA")
# 在 928x1160 中，野豬的嘴部下顎大約在 (380, 390, 560, 540)
chin = im.crop((380, 390, 560, 540))
chin.save("/tmp/hero_chin.png")
print("Saved /tmp/hero_chin.png")
