#!/usr/bin/env python3
from PIL import Image
import numpy as np

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
slices_512 = [
    f"{pd_dir}/winding_key/key_tai_chi_dual_fish_512.png",
    f"{pd_dir}/back_curio/curio_bagua_armillary_rings_512.png",
    f"{pd_dir}/chassis/paint_tortoise_jade_512.png",
    f"{pd_dir}/head_unit/head_xuanji_tortoise_stock_512.png",
    f"{pd_dir}/costume/costume_zen_dojo_harness_512.png",
    f"{pd_dir}/optic_core/core_amber_quartz_512.png",
    f"{pd_dir}/weapon/wpn_bagua_astrolabe_512.png",
]
comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
for p in slices_512:
    comp512.alpha_composite(Image.open(p).convert("RGBA"))

arr = np.array(comp512)
for y in range(50, 480, 30):
    xs = np.where(arr[y, :, 3] > 10)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: x=[{xs.min():3d}..{xs.max():3d}] width={xs.max()-xs.min()+1:3d}")
