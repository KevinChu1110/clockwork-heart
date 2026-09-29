#!/usr/bin/env python3
"""
verify_caterpillar_lanczos.py
Verify genuine LANCZOS smoothing on all 7 512x512 slices for 第五十族 風箱毛蟲 (The Bellows Caterpillar, caterpillar).
"""
import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_75f26312"
CATERPILLAR_PD = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/caterpillar"

SLICES = [
    ("chassis", "chassis_caterpillar_brass_bellows_default"),
    ("head_unit", "head_caterpillar_sensor_bellows_cowl"),
    ("winding_key", "key_caterpillar_dual_ring_bellows_key"),
    ("costume", "costume_caterpillar_deepwood_sapper_cuirass"),
    ("optic_core", "face_caterpillar_amber_condenser_lens"),
    ("weapon", "weapon_caterpillar_vine_valley_compression_hammer"),
    ("back_curio", "curio_caterpillar_segmented_pressure_pack")
]

print("=== VERIFYING LANCZOS 512x512 RESCALING (NON-NEAREST) ===")
all_pass = True
for slot, item_id in SLICES:
    p128 = f"{CATERPILLAR_PD}/{slot}/{item_id}.png"
    p512 = f"{CATERPILLAR_PD}/{slot}/{item_id}_512.png"

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
