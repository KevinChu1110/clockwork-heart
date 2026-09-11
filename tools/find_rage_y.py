#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_hud_hotbar.png")
# Let's crop x: 20 to 200, y: 70 to 200
crop = im.crop((20, 70, 200, 200))
crop.save("/tmp/find_rage_y.png")
print("Saved /tmp/find_rage_y.png")
