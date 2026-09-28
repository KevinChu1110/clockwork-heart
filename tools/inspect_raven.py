#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

p = "/opt/side/bravesoul-game/game/assets/sprites/player"
idle = Image.open(f"{p}/party/raven_idle.png")
arr = np.array(idle)
print("idle size:", idle.size)
print("idle bbox:", idle.getbbox())
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("shadow counts (118..127):", shadow_counts)

comp = Image.open(f"{p}/paperdoll/raven/proof_paperdoll_raven_composite.png")
print("comp bbox:", comp.getbbox())

slices = [
    "winding_key/key_raven_armillary_sphere_brass.png",
    "back_curio/curio_raven_articulated_steampunk_wings.png",
    "chassis/chassis_raven_obsidian_brass_default.png",
    "head_unit/head_raven_astronomer_hood_beak.png",
    "costume/costume_raven_horologist_scholar_robe.png",
    "optic_core/face_raven_astrolabe_monocle_lens.png",
    "weapon/weapon_raven_armillary_wand.png"
]
for s in slices:
    im = Image.open(f"{p}/paperdoll/raven/{s}")
    print(f"{s}: bbox={im.getbbox()}")
