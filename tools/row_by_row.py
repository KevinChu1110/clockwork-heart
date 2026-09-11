#!/usr/bin/env python3
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")
striker = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker.png").convert("RGBA")

bare = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
bare = Image.alpha_composite(bare, chassis)
bare = Image.alpha_composite(bare, head)

dark_pts: list[tuple[int, int]] = []
for y in range(128):
    for x in range(128):
        px = cast(tuple[int, int, int, int], bare.getpixel((x, y)))
        r, g, b, a = px
        if a > 150 and r < 110 and g < 90 and b < 80:
            dark_pts.append((x, y))

comp_tunic = Image.alpha_composite(bare, tunic)
comp_striker = Image.alpha_composite(bare, striker)

print("Comparison of altered dark points row by row (y=59..83):")
print(" y | tunic | striker | diff | bare darks in row")
for y in range(58, 85):
    b_darks = [p for p in dark_pts if p[1] == y]
    t_alts = [p for p in b_darks if comp_tunic.getpixel(p) != bare.getpixel(p)]
    s_alts = [p for p in b_darks if comp_striker.getpixel(p) != bare.getpixel(p)]
    print(f"{y:2d} | {len(t_alts):5d} | {len(s_alts):7d} | {len(s_alts)-len(t_alts):+4d} | total {len(b_darks)}")
