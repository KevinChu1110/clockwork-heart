#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

print("=== Left face: x: 30..50, y: 20..45 ===")
for y in range(20, 45):
    row = []
    for x in range(30, 50):
        r, g, b, a = im.getpixel((x, y))
        val = (r + g + b) // 3
        if a == 0:
            row.append("  .  ")
        elif val < 115:
            row.append(f"##{val:02d}")
        elif val < 180:
            row.append(f"=={val:02d}")
        else:
            row.append(f"  {val:02d}")
    print(f"y={y:02d}: " + " ".join(row))
