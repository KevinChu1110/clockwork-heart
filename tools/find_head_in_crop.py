#!/usr/bin/env python3
from PIL import Image

crop = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_macaque_crop_zen_striker.png")
print("size:", crop.size)

# The character head is near the top of the crop
# Let's crop y: 0..150, x: 0..250
head_crop = crop.crop((20, 10, 220, 160))
head_crop.save("/tmp/real_head_in_crop.png")
print("Saved /tmp/real_head_in_crop.png")
