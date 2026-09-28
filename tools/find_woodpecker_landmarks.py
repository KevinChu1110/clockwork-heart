#!/usr/bin/env python3
"""
Find detailed landmark candidates for woodpecker.
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"

chassis = Image.open(f"{PD_DIR}/chassis/chassis_woodpecker_tinplate_brass_default.png").convert("RGBA")
head = Image.open(f"{PD_DIR}/head_unit/head_woodpecker_scarlet_crest_cowl.png").convert("RGBA")
optic = Image.open(f"{PD_DIR}/optic_core/face_woodpecker_precision_gauge_monocle.png").convert("RGBA")
costume = Image.open(f"{PD_DIR}/costume/costume_woodpecker_skyspire_inspector_harness.png").convert("RGBA")
curio = Image.open(f"{PD_DIR}/back_curio/curio_woodpecker_riveted_tinplate_prop_tail.png").convert("RGBA")
weapon = Image.open(f"{PD_DIR}/weapon/weapon_woodpecker_resonance_pneumatic_heavy_gun.png").convert("RGBA")
key = Image.open(f"{PD_DIR}/winding_key/key_woodpecker_high_frequency_percussion_key.png").convert("RGBA")

print("Head bbox:   ", head.getbbox())
print("Optic bbox:  ", optic.getbbox())
print("Costume bbox:", costume.getbbox())
print("Curio bbox:  ", curio.getbbox())
print("Chassis bbox:", chassis.getbbox())
print("Weapon bbox: ", weapon.getbbox())
print("Key bbox:    ", key.getbbox())

ch_arr = np.array(chassis)
print("\nChassis foot rows y=105..120:")
for y in range(105, 120):
    xs = np.where(ch_arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y}: min_x={xs[0]}, max_x={xs[-1]}, count={len(xs)}, center={np.mean(xs):.1f}")

hd_arr = np.array(head)
print("\nHead features:")
print("Crest top:", np.min(np.where(hd_arr[:, :, 3] > 20)[0]))
ys, xs = np.where(hd_arr[:, :, 3] > 20)
print(f"Head center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

op_arr = np.array(optic)
ys, xs = np.where(op_arr[:, :, 3] > 20)
print(f"Optic center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

wp_arr = np.array(weapon)
ys, xs = np.where(wp_arr[:, :, 3] > 20)
print(f"Weapon center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

ky_arr = np.array(key)
ys, xs = np.where(ky_arr[:, :, 3] > 20)
print(f"Key center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")

cu_arr = np.array(curio)
ys, xs = np.where(cu_arr[:, :, 3] > 20)
print(f"Curio center: ({np.mean(xs):.1f}, {np.mean(ys):.1f})")
