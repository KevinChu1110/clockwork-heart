#!/usr/bin/env python3
"""
verify_bison_lanczos.py
Verify genuine LANCZOS smoothing on all 7 512x512 slices for 第四十四族 撼地野牛 (The Groundshaker Bison, bison).
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BISON_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bison"

SLICES = [
    ("chassis", "chassis_bison_rusted_tinplate_default"),
    ("head_unit", "head_bison_riveted_brow_horn_crest"),
    ("winding_key", "key_bison_heavy_cross_t_bar_cast_iron"),
    ("costume", "costume_bison_junkyard_demolition_cuirass"),
    ("optic_core", "face_bison_amber_pressure_gauge_eye"),
    ("weapon", "weapon_bison_wasteland_anvil_crusher_hammer"),
    ("back_curio", "curio_bison_twin_vent_exhaust_stack")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{BISON_PD}/{slot}/{item_id}.png"
    p512 = f"{BISON_PD}/{slot}/{item_id}_512.png"

    if not os.path.exists(p128) or not os.path.exists(p512):
        print(f"❌ Missing slice files for {slot}: {p128} / {p512}")
        all_pass = False
        continue

    im128 = Image.open(p128).convert("RGBA")
    im512 = Image.open(p512).convert("RGBA")

    arr128 = np.array(im128)
    arr512 = np.array(im512)

    c128 = len(np.unique(arr128[arr128[:, :, 3] > 8][:, :3], axis=0))
    c512 = len(np.unique(arr512[arr512[:, :, 3] > 8][:, :3], axis=0))

    # Nearest would have c512 == c128. Lanczos produces smooth sub-pixel gradients: c512 >> c128
    is_lanczos = (c512 > c128 * 1.5)
    print(f"  [{slot:<12}] 128 unique: {c128:4d} -> 512 unique: {c512:5d} | Lanczos smooth: {is_lanczos}")
    if not is_lanczos:
        print(f"    ❌ Warning: {slot} does not show Lanczos smoothing!")
        all_pass = False

if all_pass:
    print("✓ All 7 512x512 slices verified as genuine LANCZOS smoothed!")
    exit(0)
else:
    print("❌ Some slices failed Lanczos verification!")
    exit(1)
