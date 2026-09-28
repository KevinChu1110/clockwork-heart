#!/usr/bin/env python3
"""
verify_gecko_lanczos.py
Verify genuine LANCZOS smoothing on all 7 512x512 slices for 第四十五族 巡管守宮 (The Conduit Gecko).
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GECKO_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/gecko"

SLICES = [
    ("chassis", "chassis_gecko_brass_patina_default"),
    ("head_unit", "head_gecko_conduit_scout_crest_cowl"),
    ("winding_key", "key_gecko_dual_ring_relief_valve_brass"),
    ("costume", "costume_gecko_highpressure_stealth_harness"),
    ("optic_core", "face_gecko_dual_slit_aperture_quartz_lens"),
    ("weapon", "weapon_gecko_conduit_ratchet_dart"),
    ("back_curio", "curio_gecko_segmented_gear_balance_tail")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{GECKO_PD}/{slot}/{item_id}.png"
    p512 = f"{GECKO_PD}/{slot}/{item_id}_512.png"

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
