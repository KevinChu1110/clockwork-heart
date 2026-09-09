#!/usr/bin/env python3
from typing import cast
from PIL import Image

gold = Image.open("game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold.png").convert("RGBA")
key = Image.open("game/assets/sprites/player/paperdoll/lion/winding_key/key_classic_brass.png").convert("RGBA")

print("Key pixels around 85..105, 50..75:")
for y in range(48, 78):
    row_k = ""
    row_g = ""
    for x in range(85, 108):
        kp = cast(tuple[int, int, int, int], key.getpixel((x, y)))
        gp = cast(tuple[int, int, int, int], gold.getpixel((x, y)))
        row_k += "." if kp[3] == 0 else "#"
        row_g += "." if gp[3] == 0 else ("x" if gp[0] > 230 and gp[1] > 220 else "#")
    if "#" in row_k or "#" in row_g or "x" in row_g:
        print(f"Y={y:2d} K: {row_k}  G: {row_g}")
