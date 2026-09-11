#!/usr/bin/env python3
from PIL import Image

ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")

# Look at isolated dark pixels in the belly:
for y in range(65, 95):
    for x in range(40, 75):
        r, g, b, a = ivory.getpixel((x, y))
        val = (r + g + b) // 3
        # if val < 100, let's see its neighbors
        if val < 120 and a > 200:
            nbrs = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nr, ng, nb, na = ivory.getpixel((x+dx, y+dy))
                    nbrs.append((nr+ng+nb)//3)
            avg_nbr = sum(nbrs) // len(nbrs)
            if avg_nbr > 180:
                print(f"Belly speck at ({x}, {y}): val={val}, avg_nbr={avg_nbr}")
