#!/usr/bin/env python3
from PIL import Image

im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
w, h = im.size

# Let's inspect where dark pixels exist in light areas:
# Light areas: pixels where nearby pixels are mostly light (> 180)
# If a pixel is < 120 and most of its 8-neighbors or 5x5 neighbors are > 180, it is a speck, scratch, or crack!

suspicious = []
for y in range(1, h - 1):
    for x in range(1, w - 1):
        r, g, b, a = im.getpixel((x, y))
        if a < 128:
            continue
        val = (r + g + b) // 3
        if val < 130:
            # check neighbors
            light_nbrs = 0
            total_nbrs = 0
            for dy in [-2, -1, 0, 1, 2]:
                for dx in [-2, -1, 0, 1, 2]:
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        nr, ng, nb, na = im.getpixel((nx, ny))
                        if na > 128:
                            total_nbrs += 1
                            nval = (nr + ng + nb) // 3
                            if nval > 180:
                                light_nbrs += 1
            if total_nbrs >= 10 and light_nbrs >= 8:
                suspicious.append((x, y, val, light_nbrs, total_nbrs))

print(f"Total suspicious dark pixels in light areas: {len(suspicious)}")
# Group by region
head = [p for p in suspicious if p[1] < 55]
torso = [p for p in suspicious if 55 <= p[1] < 100]
lower = [p for p in suspicious if p[1] >= 100]
print(f"  Head: {len(head)}")
print(f"  Torso: {len(torso)}")
print(f"  Lower: {len(lower)}")

print("\nHead suspicious pixels:")
for p in head:
    print(f"  ({p[0]}, {p[1]}): val={p[2]}, light_nbrs={p[3]}/{p[4]}")

print("\nTorso suspicious pixels:")
for p in torso:
    print(f"  ({p[0]}, {p[1]}): val={p[2]}, light_nbrs={p[3]}/{p[4]}")
