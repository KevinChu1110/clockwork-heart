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

for y in range(58, 76):
    row = ""
    for x in range(40, 75):
        t_a = cast(tuple[int,int,int,int], tunic.getpixel((x, y)))[3]
        b_r, b_g, b_b, b_a = cast(tuple[int,int,int,int], bare.getpixel((x, y)))
        is_dark = (b_a > 150 and b_r < 110 and b_g < 90 and b_b < 80)
        if t_a > 30 and is_dark:
            row += "X" # altered dark
        elif t_a > 30:
            row += "T" # tunic only
        elif is_dark:
            row += "#" # bare dark
        else:
            row += "."
    print(f"y={y:2d}: {row}")
