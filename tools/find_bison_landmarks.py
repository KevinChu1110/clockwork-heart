#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BISON_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bison"

chassis = Image.open(f"{BISON_PD}/chassis/chassis_bison_rusted_tinplate_default.png").convert("RGBA")
head = Image.open(f"{BISON_PD}/head_unit/head_bison_riveted_brow_horn_crest.png").convert("RGBA")
key = Image.open(f"{BISON_PD}/winding_key/key_bison_heavy_cross_t_bar_cast_iron.png").convert("RGBA")
costume = Image.open(f"{BISON_PD}/costume/costume_bison_junkyard_demolition_cuirass.png").convert("RGBA")
optic = Image.open(f"{BISON_PD}/optic_core/face_bison_amber_pressure_gauge_eye.png").convert("RGBA")
weapon = Image.open(f"{BISON_PD}/weapon/weapon_bison_wasteland_anvil_crusher_hammer.png").convert("RGBA")
curio = Image.open(f"{BISON_PD}/back_curio/curio_bison_twin_vent_exhaust_stack.png").convert("RGBA")

def find_center_and_bounds(name, img):
    arr = np.array(img)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 20)
    if len(xs) == 0:
        print(f"{name}: empty")
        return
    cx, cy = np.mean(xs), np.mean(ys)
    print(f"{name:15s}: center=({cx:.1f}, {cy:.1f}) min_x={xs.min()} max_x={xs.max()} min_y={ys.min()} max_y={ys.max()}")

find_center_and_bounds("chassis", chassis)
find_center_and_bounds("head", head)
find_center_and_bounds("key", key)
find_center_and_bounds("costume", costume)
find_center_and_bounds("optic", optic)
find_center_and_bounds("weapon", weapon)
find_center_and_bounds("curio", curio)

# Look at optic eye positions
arr_optic = np.array(optic)
ys, xs = np.where(arr_optic[:, :, 3] > 100)
print(f"optic eye pixels: x=[{xs.min()}..{xs.max()}], y=[{ys.min()}..{ys.max()}] center=({xs.mean():.1f}, {ys.mean():.1f})")

# Look at curio twin vents
arr_curio = np.array(curio)
ys, xs = np.where(arr_curio[:, :, 3] > 100)
print(f"curio pixels: x=[{xs.min()}..{xs.max()}], y=[{ys.min()}..{ys.max()}] center=({xs.mean():.1f}, {ys.mean():.1f})")

# Look at weapon hammer head vs handle
arr_wpn = np.array(weapon)
ys, xs = np.where(arr_wpn[:, :, 3] > 100)
print(f"weapon pixels: x=[{xs.min()}..{xs.max()}], y=[{ys.min()}..{ys.max()}] center=({xs.mean():.1f}, {ys.mean():.1f})")
