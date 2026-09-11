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
tunic_alt = sum(1 for pt in dark_pts if comp_tunic.getpixel(pt) != bare.getpixel(pt))
print(f"Target (tunic altered): {tunic_alt}")

for max_y in [80, 81, 82, 83, 84, 85]:
    for min_y in [59, 60]:
        test_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        for y in range(min_y, max_y + 1):
            for x in range(128):
                # Don't cover chin/jaw in center:
                if 46 <= x <= 65 and y < 60:
                    continue
                col = cast(tuple[int,int,int,int], striker.getpixel((x, y)))
                if col[3] > 0:
                    test_img.putpixel((x, y), col)
        comp = Image.alpha_composite(bare, test_img)
        alt = sum(1 for pt in dark_pts if comp.getpixel(pt) != bare.getpixel(pt))
        print(f"min_y={min_y}, max_y={max_y}: altered={alt}")
