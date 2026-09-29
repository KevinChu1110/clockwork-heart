#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/walrus"
PARTY_IDLE = f"{REPO_ROOT}/game/assets/sprites/player/party/walrus_idle.png"

print("=== INSPECT WALRUS ASSETS ===")

if os.path.exists(PARTY_IDLE):
    im = Image.open(PARTY_IDLE).convert("RGBA")
    arr = np.array(im)
    counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Walrus party idle shadow counts (118..127): {counts}")
    bbox = im.getbbox()
    print(f"Walrus party idle bbox: {bbox}")
    if bbox:
        print(f"Margins: L={bbox[0]}, T={bbox[1]}, R={128-bbox[2]}, B={128-bbox[3]}")
else:
    print("Warning: Party idle not found!")

slots = ["chassis", "head_unit", "costume", "optic_core", "back_curio", "winding_key", "weapon"]
for slot in slots:
    slot_dir = f"{BASE_DIR}/{slot}"
    if not os.path.exists(slot_dir):
        print(f"Slot dir missing: {slot_dir}")
        continue
    files = [f for f in os.listdir(slot_dir) if f.endswith(".png") and not f.endswith("_512.png")]
    for f in files:
        p = f"{slot_dir}/{f}"
        img = Image.open(p).convert("RGBA")
        bbox = img.getbbox()
        arr = np.array(img)[:, :, 3]
        ys, xs = np.where(arr > 20)
        com = (float(np.mean(xs)), float(np.mean(ys))) if len(xs) > 0 else None
        print(f"[{slot:12s}] {f:48s} | bbox={bbox} | com={com}")
