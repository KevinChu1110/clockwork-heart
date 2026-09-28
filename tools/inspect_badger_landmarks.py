#!/usr/bin/env python3
"""
Inspect badger slice landmarks, bboxes, centers, and baseline shadow.
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_80f63a7e"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/badger"

slices = [
    ("chassis", "chassis_badger_polymer_space_default.png"),
    ("head_unit", "head_badger_flathead_ballistic_visor.png"),
    ("winding_key", "key_badger_four_vane_antenna_gold.png"),
    ("costume", "costume_badger_eva_heavy_harness.png"),
    ("optic_core", "face_badger_amber_led_matrix_visor.png"),
    ("weapon", "weapon_badger_starbreaker_ripper_claw.png"),
    ("back_curio", "curio_badger_dual_coldgas_reaction_thruster.png")
]

print("=== BADGER SLICES INSPECTION ===")
for slot, fname in slices:
    p = os.path.join(BASE_DIR, slot, fname)
    if not os.path.exists(p):
        print(f"MISSING: {p}")
        continue
    im = Image.open(p).convert("RGBA")
    bbox = im.getbbox()
    arr = np.array(im)
    alpha = arr[:, :, 3]
    ys, xs = np.where(alpha > 10)
    if len(xs) > 0:
        cx, cy = float(np.mean(xs)), float(np.mean(ys))
        print(f"{slot:12s}: bbox={bbox}, center=({cx:.1f}, {cy:.1f}), pixels={len(xs)}")
    else:
        print(f"{slot:12s}: EMPTY")

comp_path = f"{BASE_DIR}/proof_paperdoll_badger_composite.png"
if os.path.exists(comp_path):
    cim = Image.open(comp_path).convert("RGBA")
    c_arr = np.array(cim)
    print("\nComposite bbox:", cim.getbbox())
    shadow_counts = [int(np.sum(c_arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Shadow counts (118..127): {shadow_counts}")
    # Also check chassis shadow
    ch_im = Image.open(os.path.join(BASE_DIR, "chassis", "chassis_badger_polymer_space_default.png")).convert("RGBA")
    ch_arr = np.array(ch_im)
    ch_shadow = [int(np.sum(ch_arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Chassis shadow counts (118..127): {ch_shadow}")
