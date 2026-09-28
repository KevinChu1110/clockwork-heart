#!/usr/bin/env python3
"""
verify_badger_lanczos.py
Verify genuine LANCZOS smoothing on all 7 512x512 slices for 第四十六族 破星蜜獾 (The Starbreaker Honey Badger, badger).
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BADGER_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/badger"

SLICES = [
    ("chassis", "chassis_badger_polymer_space_default"),
    ("head_unit", "head_badger_flathead_ballistic_visor"),
    ("winding_key", "key_badger_four_vane_antenna_gold"),
    ("costume", "costume_badger_eva_heavy_harness"),
    ("optic_core", "face_badger_amber_led_matrix_visor"),
    ("weapon", "weapon_badger_starbreaker_ripper_claw"),
    ("back_curio", "curio_badger_dual_coldgas_reaction_thruster")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{BADGER_PD}/{slot}/{item_id}.png"
    p512 = f"{BADGER_PD}/{slot}/{item_id}_512.png"

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
