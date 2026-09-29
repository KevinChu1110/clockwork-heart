#!/usr/bin/env python3
"""
verify_camel_lanczos.py
Verify genuine LANCZOS smoothing on all 7 512x512 slices for 第五十四族 日晷駱駝 (The Sundial Camel, camel).
"""
import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMEL_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/camel"

SLICES = [
    ("chassis", "chassis_camel_sanded_tinplate_default"),
    ("head_unit", "head_camel_sundial_gnomon_cowl"),
    ("winding_key", "key_camel_armillary_dial_brass"),
    ("costume", "costume_camel_scavenger_astronomer_robe"),
    ("optic_core", "face_camel_dual_spectroscope_quartz_lens"),
    ("weapon", "weapon_camel_sundial_refraction_rod"),
    ("back_curio", "curio_camel_twin_condenser_humps")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{CAMEL_PD}/{slot}/{item_id}.png"
    p512 = f"{CAMEL_PD}/{slot}/{item_id}_512.png"

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
    sys.exit(0)
else:
    print("❌ Some slices failed Lanczos verification!")
    sys.exit(1)
