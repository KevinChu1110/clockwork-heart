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

# Let's see: what if striker is restricted to y <= 84?
striker_cropped = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
for y in range(59, 85):
    for x in range(128):
        # Also let's lower the collar in center (x: 45..68):
        # if x is in center and y < 60, don't copy
        if 48 <= x <= 65 and y < 60:
            continue
        col = cast(tuple[int,int,int,int], striker.getpixel((x, y)))
        striker_cropped.putpixel((x, y), col)

comp_tunic = Image.alpha_composite(bare, tunic)
comp_cropped = Image.alpha_composite(bare, striker_cropped)

tunic_alt = sum(1 for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))
crop_alt = sum(1 for pt in dark_pts if comp_cropped.getpixel(pt) != bare.getpixel(pt))

print(f"Tunic altered: {tunic_alt}")
print(f"Striker cropped altered: {crop_alt}")
