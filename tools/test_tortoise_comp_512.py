#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"

slices_512 = [
    ("key", f"{pd_dir}/winding_key/key_tai_chi_dual_fish_512.png"),
    ("curio", f"{pd_dir}/back_curio/curio_bagua_armillary_rings_512.png"),
    ("chassis", f"{pd_dir}/chassis/paint_tortoise_jade_512.png"),
    ("head", f"{pd_dir}/head_unit/head_xuanji_tortoise_stock_512.png"),
    ("costume", f"{pd_dir}/costume/costume_zen_dojo_harness_512.png"),
    ("core", f"{pd_dir}/optic_core/core_amber_quartz_512.png"),
    ("weapon", f"{pd_dir}/weapon/wpn_bagua_astrolabe_512.png"),
]

comp_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for name, p in slices_512:
    im = Image.open(p).convert("RGBA")
    comp_512.alpha_composite(im)

print("Composite 512 size:", comp_512.size, "bbox:", comp_512.getbbox())
comp_512.save("/tmp/tortoise_comp_512.png")
