#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"

SLICES = [
    ("chassis", "chassis_rhino_molten_iron_default"),
    ("head_unit", "head_rhino_crucible_battering_crest"),
    ("winding_key", "key_rhino_crucible_crosshair_key"),
    ("costume", "costume_rhino_crucible_smith_plate"),
    ("optic_core", "face_rhino_dual_amber_pyro_optic"),
    ("weapon", "weapon_rhino_crucible_breaker_axe"),
    ("back_curio", "curio_rhino_steam_furnace_exhaust")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{RHINO_PD}/{slot}/{item_id}.png"
    p512 = f"{RHINO_PD}/{slot}/{item_id}_512.png"

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
