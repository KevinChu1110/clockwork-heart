#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/hedgehog"
comp = Image.open(f"{BASE_DIR}/proof_paperdoll_hedgehog_composite.png").convert("RGBA")
head = Image.open(f"{BASE_DIR}/head_unit/head_hedgehog_brass_tuning_fork_ears.png").convert("RGBA")
optic = Image.open(f"{BASE_DIR}/optic_core/face_hedgehog_watchmaker_precision_loupe.png").convert("RGBA")
chassis = Image.open(f"{BASE_DIR}/chassis/chassis_hedgehog_amber_brass_default.png").convert("RGBA")
curio = Image.open(f"{BASE_DIR}/back_curio/curio_hedgehog_spring_steel_quill_pack.png").convert("RGBA")
wpn = Image.open(f"{BASE_DIR}/weapon/weapon_hedgehog_ratchet_needle_dart.png").convert("RGBA")
key = Image.open(f"{BASE_DIR}/winding_key/key_hedgehog_ratchet_and_pawl_cross.png").convert("RGBA")

print("Head bbox:", head.getbbox())
print("Optic bbox:", optic.getbbox())
print("Chassis bbox:", chassis.getbbox())
print("Curio bbox:", curio.getbbox())
print("Weapon bbox:", wpn.getbbox())
print("Key bbox:", key.getbbox())

# Let's inspect where eyes, ears, feet are
c_arr = np.array(chassis)
feet_y = []
for y in range(100, 126):
    if np.sum(c_arr[y, :, 3] > 50) > 0:
        feet_y.append(y)
print("Feet y span:", min(feet_y), max(feet_y))

# Optic center
o_arr = np.array(optic)
oy, ox = np.where(o_arr[:, :, 3] > 50)
print(f"Optic core center: x={int(np.mean(ox))}, y={int(np.mean(oy))}, range x=({min(ox)}, {max(ox)}), y=({min(oy)}, {max(oy)})")

# Weapon center
w_arr = np.array(wpn)
wy, wx = np.where(w_arr[:, :, 3] > 50)
print(f"Weapon center: x={int(np.mean(wx))}, y={int(np.mean(wy))}, range x=({min(wx)}, {max(wx)}), y=({min(wy)}, {max(wy)})")

# Key center
k_arr = np.array(key)
ky, kx = np.where(k_arr[:, :, 3] > 50)
print(f"Key center: x={int(np.mean(kx))}, y={int(np.mean(ky))}, range x=({min(kx)}, {max(kx)}), y=({min(ky)}, {max(ky)})")

# Curio center
cu_arr = np.array(curio)
cuy, cux = np.where(cu_arr[:, :, 3] > 50)
print(f"Curio center: x={int(np.mean(cux))}, y={int(np.mean(cuy))}, range x=({min(cux)}, {max(cux)}), y=({min(cuy)}, {max(cuy)})")
