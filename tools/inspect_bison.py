#!/usr/bin/env python3
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
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

print("=== BISON SLICE BBOXES & LANDMARKS ===")
for slot, item_id in SLICES:
    p = f"{BISON_PD}/{slot}/{item_id}.png"
    im = Image.open(p)
    bbox = im.getbbox()
    print(f"{slot:15s} bbox={bbox}")

comp = Image.open(f"{BISON_PD}/proof_paperdoll_bison_composite.png")
print(f"composite bbox={comp.getbbox()}")

arr = np.array(comp)
print("Composite ground shadow row counts (118..127):")
shadow_counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
print(shadow_counts)

for y in range(120, 128):
    print(f"y={y}: max_alpha={arr[y, :, 3].max()} counts_gt_0={int(np.sum(arr[y, :, 3] > 0))} counts_gt_20={int(np.sum(arr[y, :, 3] > 20))}")
