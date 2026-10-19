#!/usr/bin/env python3
from PIL import Image
import numpy as np

w = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/maple_parts/weapon/wpn_anvil_greathammer.png").convert("RGBA")
# 裁出底部 (0, 200, 176, 252)
crop = w.crop((0, 200, 176, 252))
crop.save("/tmp/hammer_bottom_check.png")
print("Saved /tmp/hammer_bottom_check.png")
