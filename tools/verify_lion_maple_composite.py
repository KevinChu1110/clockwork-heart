#!/usr/bin/env python3
"""
tools/verify_lion_maple_composite.py
Composites Lion MapleStory slices in anchor hierarchy and compares with legacy composition.
"""

import numpy as np
from PIL import Image

OUT_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/game/assets/sprites/player/paperdoll/lion/maple_parts"

# Skeleton Anchors in 512 canvas:
# root = (256, 480)
# body is at (0, 0)
# back_key = (342, 296)
# navel = (256, 348)
# hand = (144, 320)
# neck = (250, 274)
# brow_rel_neck = (-22, -101) -> brow = (228, 173)

anchors = {
    "root": (0, 0),
    "neck": (250, 274),
    "navel": (256, 348),
    "hand": (144, 320),
    "back_key": (342, 296),
    "brow": (228, 173),
    "tail": (360, 380)
}

layers = [
    # (slot, file, anchor, origin, z)
    ("winding_key", f"{OUT_DIR}/winding_key/key_classic_brass.png", "back_key", (20, 113), 5),
    ("back_curio", f"{OUT_DIR}/back_curio/curio_lion_fan_tail.png", "tail", (9, 16), 8),
    ("body", f"{OUT_DIR}/body/paint_brass_gold.png", "root", (0, 0), 10),
    ("head_unit", f"{OUT_DIR}/head_unit/ear_lion_gilded_mane_brass.png", "neck", (119, 223), 20),
    ("costume", f"{OUT_DIR}/costume/costume_nutcracker_guard.png", "navel", (126, 118), 25),
    ("eyes", f"{OUT_DIR}/eyes/eyes_cyan_emerald.png", "brow", (60, 30), 30),
    ("weapon", f"{OUT_DIR}/weapon/wpn_knight_lance.png", "hand", (69, 293), 40),
]

# Sort by Z
layers.sort(key=lambda x: x[4])

comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

for slot, p, anc_name, origin, z in layers:
    im = Image.open(p).convert("RGBA")
    anc = anchors[anc_name]
    # dest = anc - origin
    dest = (anc[0] - origin[0], anc[1] - origin[1])
    print(f"Layer {slot:12s} (Z:{z:2d}): anc={anc}, origin={origin} -> dest={dest}, size={im.size}")
    comp.alpha_composite(im, dest)

comp_out = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/lion_maple_test_comp.png"
comp.save(comp_out)
print(f"✓ Saved composite: {comp_out}, bbox={comp.getbbox()}")

# Magenta background
mag = Image.new("RGBA", (512, 512), (255, 0, 255, 255))
mag.alpha_composite(comp)
mag_out = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a/tools/lion_maple_test_magenta.png"
mag.save(mag_out)
print(f"✓ Saved magenta: {mag_out}")
