#!/usr/bin/env python3
from PIL import Image

p = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png"
im = Image.open(p).convert("RGBA")
# 放大看戰錘握柄與身體交界處 (140, 260, 240, 420)
crop = im.crop((140, 260, 240, 420))
crop.save("/tmp/hammer_body_zoom.png")
print("Saved /tmp/hammer_body_zoom.png")
