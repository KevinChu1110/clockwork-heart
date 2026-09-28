#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/seal"

comp = Image.open(f"{BASE_DIR}/proof_paperdoll_seal_composite.png").convert("RGBA")
print(f"Composite bbox: {comp.getbbox()}")

slices = {
    "chassis": "chassis/chassis_seal_marine_titanium_default.png",
    "optic_core": "optic_core/face_seal_cyan_quartz_convex_lens.png",
    "costume": "costume/costume_seal_deepsea_diver_harness.png",
    "head_unit": "head_unit/head_seal_streamline_cowl_sonar.png",
    "back_curio": "back_curio/curio_seal_hydro_ducted_tail_flukes.png",
    "winding_key": "winding_key/key_seal_marine_propeller_brass.png",
    "weapon": "weapon/weapon_seal_clapper_gauntlets.png"
}

for slot, rel in slices.items():
    p = f"{BASE_DIR}/{rel}"
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    if bbox:
        cx = (bbox[0] + bbox[2]) / 2.0
        cy = (bbox[1] + bbox[3]) / 2.0
        print(f"[{slot:12s}] bbox={bbox} center=({cx:.1f}, {cy:.1f})")
    else:
        print(f"[{slot:12s}] EMPTY!")

arr = np.array(comp)
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"\nGround shadow row counts (118..127): {shadow_counts}")
for y in range(118, 128):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"  y={y}: min_x={xs[0]}, max_x={xs[-1]}, count={len(xs)}")
    else:
        print(f"  y={y}: count=0")
