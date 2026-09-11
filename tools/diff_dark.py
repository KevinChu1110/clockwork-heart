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

tunic_alt_pts = set(pt for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))
striker_alt_pts = set(pt for pt in dark_pts if comp_striker.getpixel(pt) != bare.getpixel(pt))

striker_extra = striker_alt_pts - tunic_alt_pts

print(f"Total tunic altered: {len(tunic_alt_pts)}")
print(f"Total striker altered: {len(striker_alt_pts)}")
print(f"Striker extra altered: {len(striker_extra)}")

# Breakdown of striker_extra by region:
print("\nStriker extra points by Y:")
for y_min, y_max in [(50, 58), (59, 65), (66, 75), (76, 84), (85, 120)]:
    pts = [pt for pt in striker_extra if y_min <= pt[1] <= y_max]
    print(f"  Y {y_min:2d}..{y_max:2d}: count={len(pts):3d}, X range: {min(p[0] for p in pts) if pts else '-'}..{max(p[0] for p in pts) if pts else '-'}")
