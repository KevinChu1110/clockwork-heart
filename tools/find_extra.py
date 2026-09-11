#!/usr/bin/env python3
import sys
sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from typing import cast
from PIL import Image
from test_new_striker import create_candidate

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

cand = create_candidate()
chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png").convert("RGBA")
head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial.png").convert("RGBA")
tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic.png").convert("RGBA")

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
comp_cand = Image.alpha_composite(bare, cand)

tunic_alt = set(pt for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))
cand_alt = set(pt for pt in dark_pts if comp_cand.getpixel(pt) != bare.getpixel(pt))

extra = cand_alt - tunic_alt
print(f"Cand total: {len(cand_alt)}, Tunic total: {len(tunic_alt)}, Extra: {len(extra)}")

for y in range(58, 85):
    pts = [p for p in extra if p[1] == y]
    if pts:
        print(f"y={y:2d}: count={len(pts):2d}, x coords: {sorted(p[0] for p in pts)}")
