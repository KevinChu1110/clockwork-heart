#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = im.size

# Let's inspect the arms too!
# Character right arm (image left): x: 27..42, y: 50..95
crop_arm_l = im.crop((25, 45, 45, 95))
crop_arm_l.save("/tmp/macaque_arm_l.png")

# Character left arm (image right): x: 75..100, y: 50..95
crop_arm_r = im.crop((75, 45, 100, 95))
crop_arm_r.save("/tmp/macaque_arm_r.png")

print("Saved arm crops")
