#!/usr/bin/env python3
from PIL import Image

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")
comp = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png").convert("RGBA")
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

# Let's check the face area in idle_x3 vs ivory:
print("Face in idle_x3 around the eye crack (y: 32..44, x: 65..75):")
for y in range(32, 45):
    row = []
    for x in range(65, 75):
        r, g, b, a = idle_x3.getpixel((x, y))
        val = (r + g + b) // 3
        row.append(f"{val:03d}")
    print(f"y={y:02d}: " + " ".join(row))
