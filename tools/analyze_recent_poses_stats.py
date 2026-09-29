#!/usr/bin/env python3
import os
import sys
from PIL import Image
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses"
recent_races = ["firefly", "marmot", "swan", "takin", "lemur"]
poses = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

print(f"Analyzing recent 5 races in {POSES_DIR}: {recent_races}")

for race in recent_races:
    print(f"\n=== Race: {race} ===")
    r_colors_128 = []
    r_alphas_128 = []
    r_colors_512 = []
    r_alphas_512 = []
    for p in poses:
        p128 = f"{POSES_DIR}/{race}/{p}.png"
        p512 = f"{POSES_DIR}/{race}/{p}_512.png"
        if os.path.exists(p128):
            im128 = Image.open(p128).convert("RGBA")
            arr128 = np.array(im128)
            c128 = len(np.unique(arr128.reshape(-1, 4), axis=0))
            a128 = len(np.unique(arr128[:, :, 3]))
            r_colors_128.append(c128)
            r_alphas_128.append(a128)
            print(f"  {p:10s} 128: colors={c128:4d}, alphas={a128:3d}", end="")
        if os.path.exists(p512):
            im512 = Image.open(p512).convert("RGBA")
            arr512 = np.array(im512)
            c512 = len(np.unique(arr512.reshape(-1, 4), axis=0))
            a512 = len(np.unique(arr512[:, :, 3]))
            r_colors_512.append(c512)
            r_alphas_512.append(a512)
            print(f" | 512: colors={c512:5d}, alphas={a512:3d}")
        else:
            print()
    if r_colors_128:
        print(f"  --> 128 range: colors [{min(r_colors_128)}, {max(r_colors_128)}], alphas [{min(r_alphas_128)}, {max(r_alphas_128)}]")
    if r_colors_512:
        print(f"  --> 512 range: colors [{min(r_colors_512)}, {max(r_colors_512)}], alphas [{min(r_alphas_512)}, {max(r_alphas_512)}]")
