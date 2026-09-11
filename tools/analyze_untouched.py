#!/usr/bin/env python3
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
tunic_alt_pts = set(pt for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))

not_in_tunic = [pt for pt in dark_pts if 59 <= pt[1] <= 83 and pt not in tunic_alt_pts]
print(f"Dark points in 59..83 NOT altered by tunic: {len(not_in_tunic)}")
for y_min, y_max in [(59, 64), (65, 70), (71, 75), (76, 80), (81, 83)]:
    pts = [p for p in not_in_tunic if y_min <= p[1] <= y_max]
    print(f"y={y_min:2d}..{y_max:2d}: count={len(pts):3d}, x list: {sorted(set(p[0] for p in pts))}")
