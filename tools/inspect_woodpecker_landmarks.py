#!/usr/bin/env python3
"""
Inspect woodpecker slice landmarks, bboxes, centers, and baseline shadow.
"""
import os
from PIL import Image
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"

slices = [
    ("chassis", "chassis_woodpecker_tinplate_brass_default.png"),
    ("head_unit", "head_woodpecker_scarlet_crest_cowl.png"),
    ("winding_key", "key_woodpecker_high_frequency_percussion_key.png"),
    ("costume", "costume_woodpecker_skyspire_inspector_harness.png"),
    ("optic_core", "face_woodpecker_precision_gauge_monocle.png"),
    ("weapon", "weapon_woodpecker_resonance_pneumatic_heavy_gun.png"),
    ("back_curio", "curio_woodpecker_riveted_tinplate_prop_tail.png")
]

print("=== WOODPECKER SLICES INSPECTION ===")
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

comp_path = f"{BASE_DIR}/proof_paperdoll_woodpecker_composite.png"
if os.path.exists(comp_path):
    cim = Image.open(comp_path).convert("RGBA")
    c_arr = np.array(cim)
    print("\nComposite bbox:", cim.getbbox())
    shadow_counts = [int(np.sum(c_arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Composite shadow counts (118..127): {shadow_counts}")
    ch_im = Image.open(os.path.join(BASE_DIR, "chassis", "chassis_woodpecker_tinplate_brass_default.png")).convert("RGBA")
    ch_arr = np.array(ch_im)
    ch_shadow = [int(np.sum(ch_arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Chassis shadow counts (118..127):   {ch_shadow}")
    # idle sprite
    idle_path = f"{REPO_ROOT}/game/assets/sprites/player/woodpecker_idle.png"
    if os.path.exists(idle_path):
        i_im = Image.open(idle_path).convert("RGBA")
        i_arr = np.array(i_im)
        i_shadow = [int(np.sum(i_arr[y, :, 3] > 20)) for y in range(118, 128)]
        print(f"woodpecker_idle shadow counts (118..127): {i_shadow}")
        print(f"woodpecker_idle bbox: {i_im.getbbox()}")
