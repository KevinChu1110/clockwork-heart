#!/usr/bin/env python3
import os
import glob
import numpy as np
from PIL import Image

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfb84d21"
RACES = ["takin", "lemur", "marmot", "firefly", "manta"]
SLOTS = ["chassis", "head_unit", "costume", "weapon", "back_curio", "optic_core", "winding_key"]

print(f"{'Race':<10} {'Slot':<12} {'128 Px':<8} {'128 Colors':<12} {'c100%':<8} {'512 Colors':<12} {'512 Alphas':<12}")
print("-" * 75)

for race in RACES:
    pdir = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/{race}"
    for slot in SLOTS:
        files_128 = glob.glob(f"{pdir}/{slot}/*.png")
        files_128 = [f for f in files_128 if not f.endswith("_512.png") and not f.endswith(".import")]
        if not files_128:
            continue
        f128 = files_128[0]
        base = os.path.splitext(f128)[0]
        f512 = f"{base}_512.png"

        im128 = Image.open(f128).convert("RGBA")
        arr128 = np.array(im128)
        mask128 = arr128[:, :, 3] > 8
        px128 = int(np.sum(mask128))
        colors128 = len(np.unique(arr128[mask128][:, :3], axis=0))
        c100 = (colors128 / px128) * 100.0 if px128 > 0 else 0

        if os.path.exists(f512):
            im512 = Image.open(f512).convert("RGBA")
            arr512 = np.array(im512)
            mask512 = arr512[:, :, 3] > 8
            colors512 = len(np.unique(arr512[mask512][:, :3], axis=0))
            alphas512 = len(np.unique(arr512[:, :, 3]))
        else:
            colors512 = 0
            alphas512 = 0

        print(f"{race:<10} {slot:<12} {px128:<8} {colors128:<12} {c100:<8.2f} {colors512:<12} {alphas512:<12}")
