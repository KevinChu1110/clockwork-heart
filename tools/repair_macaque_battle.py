#!/usr/bin/env python3
from PIL import Image

mb = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png").convert("RGBA")
w, h = mb.size

# 1. Clean forehead crack in macaque_battle (x: 59..72, y: 32..43)
for y in range(32, 44):
    for x in range(59, 72):
        r, g, b, a = mb.getpixel((x, y))
        val = (r + g + b) // 3
        if val < 130 and a > 200:
            # find clean left & right light neighbors
            l_col = None
            for lx in range(x - 1, max(30, x - 6), -1):
                lr, lg, lb, la = mb.getpixel((lx, y))
                if la > 200 and (lr + lg + lb) // 3 > 170:
                    l_col = (lr, lg, lb)
                    break
            r_col = None
            for rx in range(x + 1, min(w, x + 6)):
                rr, rg, rb, ra = mb.getpixel((rx, y))
                if ra > 200 and (rr + rg + rb) // 3 > 170:
                    r_col = (rr, rg, rb)
                    break
            if l_col and r_col:
                mb.putpixel((x, y), ((l_col[0]+r_col[0])//2, (l_col[1]+r_col[1])//2, (l_col[2]+r_col[2])//2, 255))
            elif l_col:
                mb.putpixel((x, y), (*l_col, 255))
            elif r_col:
                mb.putpixel((x, y), (*r_col, 255))

# 2. Clean belly scratch in macaque_battle (x: 48..56, y: 73..78)
for y in range(73, 79):
    for x in range(48, 56):
        r, g, b, a = mb.getpixel((x, y))
        val = (r + g + b) // 3
        if val < 120 and a > 200:
            light_nbrs = []
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        nr, ng, nb, na = mb.getpixel((nx, ny))
                        if na > 200 and (nr + ng + nb) // 3 > 165:
                            light_nbrs.append((nr, ng, nb))
            if light_nbrs:
                ar = sum(c[0] for c in light_nbrs) // len(light_nbrs)
                ag = sum(c[1] for c in light_nbrs) // len(light_nbrs)
                ab = sum(c[2] for c in light_nbrs) // len(light_nbrs)
                mb.putpixel((x, y), (ar, ag, ab, 255))

mb.save("/opt/side/bravesoul-game/game/assets/sprites/player/macaque_battle.png")
print("✓ Repaired macaque_battle.png")
