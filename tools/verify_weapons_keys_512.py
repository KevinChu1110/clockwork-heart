#!/usr/bin/env python3
import os
from PIL import Image

BASE = "game/assets/sprites/player/paperdoll"

checks = [
    # 8 weapons
    ("lion", "weapon", "wpn_knight_lance_512.png"),
    ("boar", "weapon", "wpn_anvil_greathammer_512.png"),
    ("fox", "weapon", "wpn_astral_staff_512.png"),
    ("macaque", "weapon", "wpn_spring_claws_512.png"),
    ("tiger", "weapon", "wpn_twin_ember_sabers_512.png"),
    ("crane", "weapon", "wpn_zephyr_wing_bow_512.png"),
    ("bear", "weapon", "wpn_eccentric_gyro_sledge_512.png"),
    ("penguin", "weapon", "wpn_twin_harpoon_gun_512.png"),
    # rabbit weapon
    ("rabbit", "weapon", "wpn_dawn_blade_512.png"),
    # 4 unique keys
    ("bear", "winding_key", "key_cross_pendulum_512.png"),
    ("crane", "winding_key", "key_tri_wing_zephyr_512.png"),
    ("penguin", "winding_key", "key_twin_ring_helm_512.png"),
    ("tiger", "winding_key", "key_turbine_flame_512.png"),
    # rabbit key
    ("rabbit", "winding_key", "key_classic_brass_512.png"),
]

all_ok = True
for race, slot, filename in checks:
    path = os.path.join(BASE, race, slot, filename)
    if not os.path.exists(path):
        print(f"FAIL: Missing {path}")
        all_ok = False
        continue
    im = Image.open(path)
    if im.size != (512, 512) or im.mode != "RGBA":
        print(f"FAIL: {path} has size={im.size}, mode={im.mode}")
        all_ok = False
        continue
    max_edge = max(im.size)
    if max_edge != 512:
        print(f"FAIL: {path} max_edge={max_edge} != 512")
        all_ok = False
        continue
    print(f"OK: {path} (512x512 RGBA)")

if all_ok:
    print("ALL WEAPONS AND KEYS 512 CHECKS PASSED!")
else:
    print("SOME CHECKS FAILED!")
    exit(1)
