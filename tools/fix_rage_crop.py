#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_hud_hotbar.png")
# Scan for white pixels of the rage card in x: 20~200, y: 70~250
# Cream white is #FFFDF8 -> (255, 253, 248)
min_x, min_y, max_x, max_y = 9999, 9999, 0, 0
for y in range(70, 250):
    for x in range(20, 200):
        p = im.getpixel((x, y))
        r, g, b = p[0], p[1], p[2]
        if r > 240 and g > 240 and b > 230:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

print(f"Rage card bounds on screen: x=({min_x}, {max_x}), y=({min_y}, {max_y})")
# Let's crop with 20px padding around it
padded_crop = im.crop((min_x - 15, min_y - 15, max_x + 15, max_y + 15))
padded_crop.save("/opt/side/bravesoul-game/screenshots/proof_battle_crop_rage.png")
padded_crop.save("/opt/side/bravesoul-game/proofs/battle_hud_contrast/proof_battle_crop_rage.png")
print("Saved correctly padded crop_rage.")
