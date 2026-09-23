#!/usr/bin/env python3
from PIL import Image

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
chassis = Image.open(f"{BASE}/chassis/paint_tortoise_jade.png").convert("RGBA")
cp = chassis.load()
for y in range(46, 122, 6):
    row_xs = [x for x in range(128) if cp[x, y][3] > 20]
    if row_xs:
        print(f"y={y:3d}: x min={min(row_xs):3d}, max={max(row_xs):3d}, count={len(row_xs)}")
