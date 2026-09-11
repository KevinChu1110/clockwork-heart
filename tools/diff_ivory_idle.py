#!/usr/bin/env python3
from PIL import Image

idle_x3 = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_idle_x3.png").convert("RGBA")
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

# Let's inspect where ivory differs from idle_x3
w, h = 128, 128
diff_count = 0
for y in range(h):
    for x in range(w):
        pi = ivory.getpixel((x, y))
        px = idle_x3.getpixel((x, y))
        if pi[3] > 0 and px[3] > 0:
            if pi != px:
                diff_count += 1

print(f"Total overlapping pixels: 4720, differing pixels: {diff_count}")
