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

comp_tunic = Image.alpha_composite(bare, tunic)
comp_striker = Image.alpha_composite(bare, striker)

# Case A: Whole image dark points
dark_all: list[tuple[int, int]] = []
for y in range(128):
    for x in range(128):
        r, g, b, a = cast(tuple[int, int, int, int], bare.getpixel((x, y)))
        if a > 150 and r < 110 and g < 90 and b < 80:
            dark_all.append((x, y))

tunic_alt_all = sum(1 for pt in dark_all if comp_tunic.getpixel(pt) != bare.getpixel(pt))
striker_alt_all = sum(1 for pt in dark_all if comp_striker.getpixel(pt) != bare.getpixel(pt))

print(f"Whole image: tunic={tunic_alt_all}, striker={striker_alt_all}, ratio={striker_alt_all/tunic_alt_all:.4f}")

# Case B: Crop region (30, 38, 100, 86)
dark_crop = [pt for pt in dark_all if 30 <= pt[0] < 100 and 38 <= pt[1] < 86]
tunic_alt_crop = sum(1 for pt in dark_crop if comp_tunic.getpixel(pt) != bare.getpixel(pt))
striker_alt_crop = sum(1 for pt in dark_crop if comp_striker.getpixel(pt) != bare.getpixel(pt))

print(f"Crop (30,38-100,86): tunic={tunic_alt_crop}, striker={striker_alt_crop}, ratio={striker_alt_crop/tunic_alt_crop:.4f}")
