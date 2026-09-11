#!/usr/bin/env python3
from PIL import Image

rab = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png").convert("RGBA")

# Count suspicious pixels on rabbit:
suspicious = 0
w, h = rab.size
for y in range(1, h-1):
    for x in range(1, w-1):
        r, g, b, a = rab.getpixel((x, y))
        if a < 128: continue
        val = (r + g + b) // 3
        if val < 120:
            nbrs = []
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    nr, ng, nb, na = rab.getpixel((x+dx, y+dy))
                    if na > 128:
                        nbrs.append((nr+ng+nb)//3)
            if nbrs and (sum(nbrs)//len(nbrs)) > 180:
                suspicious += 1

print(f"Rabbit suspicious dark specks in light area: {suspicious}")
