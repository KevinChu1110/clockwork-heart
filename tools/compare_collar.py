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

print("Tunic coverage for y in 56..65:")
for y in range(56, 66):
    row_t = [x for x in range(128) if cast(tuple[int,int,int,int], tunic.getpixel((x, y)))[3] > 10]
    row_s = [x for x in range(128) if cast(tuple[int,int,int,int], striker.getpixel((x, y)))[3] > 10]
    print(f"y={y:2d}: tunic X: {min(row_t) if row_t else '-' }..{max(row_t) if row_t else '-'} (len {len(row_t)}) | striker X: {min(row_s) if row_s else '-'}..{max(row_s) if row_s else '-'} (len {len(row_s)})")
