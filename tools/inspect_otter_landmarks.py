#!/usr/bin/env python3
import numpy as np
from PIL import Image

comp_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/proof_paperdoll_otter_composite.png"
im = Image.open(comp_path).convert("RGBA")
arr = np.array(im)
print("Composite size:", im.size, "bbox:", im.getbbox())

slices = {
    "key": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/winding_key/key_otter_nautical_rudder_helm.png",
    "curio": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/back_curio/curio_otter_articulated_rudder_tail.png",
    "chassis": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/chassis/chassis_otter_abyssal_cyan_default.png",
    "head": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/head_unit/head_otter_diver_bell_visor.png",
    "costume": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/costume/costume_otter_deepsea_salvage_harness.png",
    "optic": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/optic_core/face_otter_phosphor_green_gauges.png",
    "weapon": "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/otter/weapon/weapon_otter_abyssal_anchor_cleaver.png",
}

for name, p in slices.items():
    s_im = Image.open(p).convert("RGBA")
    s_arr = np.array(s_im)
    alpha = s_arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    cy = np.mean(ys)
    cx = np.mean(xs)
    print(f"{name:8s}: center=({cx:.1f}, {cy:.1f}), min_x={xs.min()}, max_x={xs.max()}, min_y={ys.min()}, max_y={ys.max()}")

print("\nGround shadow rows (118..127):")
shadow_counts = []
for y in range(118, 128):
    count = int(np.sum(arr[y, :, 3] > 20))
    shadow_counts.append(count)
    print(f"y={y}: count={count}")
print("EXPECTED_SHADOW =", shadow_counts)
