#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/screenshots/proof_battle_hud_hotbar.png")
# Scan for white pixels of EnemyTag card in x: 700~1000, y: 120~260
min_x, min_y, max_x, max_y = 9999, 9999, 0, 0
for y in range(120, 260):
    for x in range(700, 1000):
        p = im.getpixel((x, y))
        r, g, b = p[0], p[1], p[2]
        if r > 240 and g > 240 and b > 230:
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)

print(f"EnemyTag card bounds on screen: x=({min_x}, {max_x}), y=({min_y}, {max_y})")
padded_crop = im.crop((min_x - 30, min_y - 20, max_x + 30, max_y + 40))
padded_crop.save("/opt/side/bravesoul-game/screenshots/proof_battle_crop_enemytag.png")
padded_crop.save("/opt/side/bravesoul-game/proofs/battle_hud_contrast/proof_battle_crop_enemytag.png")
print("Saved correctly padded crop_enemytag.")
