#!/usr/bin/env python3
from PIL import Image

b = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png").convert("RGBA")
# 裁出底部陰影 (60, 460, 440, 512)
crop = b.crop((60, 460, 440, 512))
crop.save("/tmp/body_shadow_check.png")
print("Saved /tmp/body_shadow_check.png, bbox:", crop.getbbox())
