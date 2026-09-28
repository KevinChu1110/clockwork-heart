#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/sailfish"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"

idle_128 = Image.open(f"{POSES_DIR}/idle.png")
idle_512 = Image.open(f"{POSES_DIR}/idle_512.png")
attack_128 = Image.open(f"{POSES_DIR}/attack.png")
attack_512 = Image.open(f"{POSES_DIR}/attack_512.png")

print(f"idle_128: size={idle_128.size}, bbox={idle_128.getbbox()}")
print(f"idle_512: size={idle_512.size}, bbox={idle_512.getbbox()}")
print(f"attack_128: size={attack_128.size}, bbox={attack_128.getbbox()}")
print(f"attack_512: size={attack_512.size}, bbox={attack_512.getbbox()}")

arr = np.array(idle_128)
shadow_rows = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print("Shadow rows 118..127 count:", shadow_rows)

# Check all slices in paperdoll
slots = ["chassis", "head_unit", "winding_key", "costume", "optic_core", "weapon", "back_curio"]
for s in slots:
    sdir = f"{PD_DIR}/{s}"
    files = [f for f in os.listdir(sdir) if f.endswith(".png")]
    for f in sorted(files):
        p = f"{sdir}/{f}"
        im = Image.open(p)
        print(f"Slice {s}/{f}: size={im.size}, bbox={im.getbbox()}")
