#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

print("=== Forehead region above left eye (x: 60..75, y: 20..32) ===")
for y in range(20, 33):
    row = []
    for x in range(60, 75):
        r, g, b, a = im.getpixel((x, y))
        val = (r + g + b) // 3
        if a == 0:
            row.append("  .  ")
        elif val < 100:
            row.append(f"##{val:02d}")
        elif val < 180:
            row.append(f"=={val:02d}")
        else:
            row.append(f"  {val:02d}")
    print(f"y={y:02d}: " + " ".join(row))
