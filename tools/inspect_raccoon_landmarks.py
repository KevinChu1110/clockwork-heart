#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

base = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/raccoon"
comp = Image.open(f"{base}/proof_paperdoll_raccoon_composite.png")
print("Composite size:", comp.size, "bbox:", comp.getbbox())

slices = [
    "chassis/chassis_raccoon_orbit_aqua_default.png",
    "head_unit/head_raccoon_parabolic_radar_dish.png",
    "winding_key/key_raccoon_quad_solar_sail.png",
    "back_curio/curio_raccoon_coaxial_ring_antenna_tail.png",
    "costume/costume_raccoon_space_explorer_harness.png",
    "optic_core/face_raccoon_hud_polarizer_visor.png",
    "weapon/weapon_raccoon_anti_gravity_pulse_blaster.png"
]

for s in slices:
    path = os.path.join(base, s)
    im = Image.open(path)
    print(f"{s:55s} size={im.size} bbox={im.getbbox()}")

arr = np.array(comp)
shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Ground shadow counts (118..127):", shadow)

# Also check 512 composite if any, or 512 slices
for s in slices:
    p512 = os.path.join(base, s.replace(".png", "_512.png"))
    if os.path.exists(p512):
        im512 = Image.open(p512)
        print(f"512: {s:50s} size={im512.size} bbox={im512.getbbox()}")
