#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BAT_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bat"

SLICES = [
    ("chassis", "chassis_bat_astral_polymer_default"),
    ("head_unit", "head_bat_sonar_parabolic_crest"),
    ("winding_key", "key_bat_orbital_pulsar_key"),
    ("costume", "costume_bat_orbital_stealth_harness"),
    ("optic_core", "face_bat_dual_amber_optic_lens"),
    ("weapon", "weapon_bat_superconducting_pulse_dart"),
    ("back_curio", "curio_bat_articulated_starwing_mantle")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{BAT_PD}/{slot}/{item_id}.png"
    p512 = f"{BAT_PD}/{slot}/{item_id}_512.png"

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
else:
    print("❌ Some slices failed Lanczos verification!")
