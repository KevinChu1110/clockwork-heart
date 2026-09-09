#!/usr/bin/env python3
import os
import sys
from typing import cast
from PIL import Image, ImageChops

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
from generate_lion_proofs import build_composite

c_bare = build_composite("paint_brass_gold.png", None)
c_nut = build_composite("paint_brass_gold.png", "costume_nutcracker_guard.png")
c_art = build_composite("paint_brass_gold.png", "costume_steam_artisan.png")

diff_bare_nut = ImageChops.difference(c_bare, c_nut)
diff_bare_art = ImageChops.difference(c_bare, c_art)

bbox_bn = diff_bare_nut.getbbox()
bbox_ba = diff_bare_art.getbbox()

print("Diff bare vs nut bbox:", bbox_bn)
print("Diff bare vs art bbox:", bbox_ba)

diff_px_bn = 0
diff_px_ba = 0
for y in range(128):
    for x in range(128):
        p_bn = cast(tuple[int, int, int, int], diff_bare_nut.getpixel((x, y)))
        p_ba = cast(tuple[int, int, int, int], diff_bare_art.getpixel((x, y)))
        if max(p_bn) > 0:
            diff_px_bn += 1
        if max(p_ba) > 0:
            diff_px_ba += 1

print(f"Diff bare vs nut pixels: {diff_px_bn}")
print(f"Diff bare vs art pixels: {diff_px_ba}")
