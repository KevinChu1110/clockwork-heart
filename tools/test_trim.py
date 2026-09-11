#!/usr/bin/env python3
import sys
sys.path.insert(0, "/opt/side/bravesoul-game/tools")
from typing import cast
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

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
tunic_alt = sum(1 for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))
print(f"Target: tunic_alt = {tunic_alt}")

# Test with cand cropped to x in 39..68 and y in 59..83
from test_new_striker import create_candidate
cand = create_candidate()

cand_trimmed = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for y in range(128):
    for x in range(128):
        if x > 68:
            continue
        col = cast(tuple[int,int,int,int], cand.getpixel((x, y)))
        if col[3] > 0:
            cand_trimmed.putpixel((x, y), col)

comp_trim = Image.alpha_composite(bare, cand_trimmed)
trim_alt = sum(1 for pt in dark_pts if comp_trim.getpixel(pt) != bare.getpixel(pt))
print(f"Trimmed (x <= 68): altered = {trim_alt}")
