#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

print("=== Pixel map around eye (y: 32..45, x: 65..78) ===")
for y in range(32, 45):
    row = []
    for x in range(65, 78):
        r, g, b, a = im.getpixel((x, y))
        if a == 0:
            row.append("  .  ")
        else:
            # brightness
            val = (r + g + b) // 3
            if val < 80:
                row.append(f"##{val:02d}")
            elif val < 160:
                row.append(f"=={val:02d}")
            else:
                row.append(f"  {val:02d}")
    print(f"y={y:02d}: " + " ".join(row))
