#!/usr/bin/env python3
from PIL import Image
from typing import cast

BASE = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
comp = Image.open(f"{BASE}/proof_paperdoll_tortoise_composite.png").convert("RGBA")
c_px = comp.load()

for y in range(116, 128):
    alphas = [cast(tuple[int, int, int, int], c_px[x, y])[3] for x in range(128)]
    non_zero = sum(1 for a in alphas if a > 20)
    print(f"y={y:3d}: non_zero(a>20)={non_zero}")
