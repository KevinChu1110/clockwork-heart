#!/usr/bin/env python3
"""
tools/patch_hammer_shadow_and_reimport.py
1. Fills the ground shadow gap under the hammer in body chassis (y: 480..502, x: 180..240).
2. Deletes stale .godot import cache for maple_parts so Godot loads the pristine new PNGs.
"""

import os
import shutil
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

# 1. 填補 body 底部陰影 (在 x: 170..245, y: 480..504 鋪滿自然地面投影色 (170, 150, 100, 180))
for p_name in ["paint_brass_gold", "paint_ivory_stock", "paint_molten_crimson"]:
    body_p = f"{PARTS_DIR}/body/{p_name}.png"
    im = Image.open(body_p).convert("RGBA")
    arr = np.array(im)
    
    for y in range(480, 505):
        for x in range(170, 245):
            if arr[y, x, 3] < 100:
                # 填充自然地面沙地投影色
                arr[y, x] = [165, 145, 95, 160]

    Image.fromarray(arr, mode="RGBA").save(body_p)
    print(f"  ✓ Patched shadow for {p_name}")

# 2. 清理 stale .godot/imported/ 關於 maple_parts 的快取
godot_imported = f"{REPO_ROOT}/game/.godot/imported"
if os.path.exists(godot_imported):
    for f in os.listdir(godot_imported):
        if "maple_parts" in f or "proof_maple_boar" in f:
            full_p = os.path.join(godot_imported, f)
            try:
                os.remove(full_p)
                print(f"  Removed stale cache: {f}")
            except Exception as e:
                pass

print("🎉 Shadow patched and stale cache cleared!")
