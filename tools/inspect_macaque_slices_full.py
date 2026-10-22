#!/usr/bin/env python3
import os
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
MACAQUE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/macaque"

# 檢查 128x128 槽位切片
print("=== 128x128 Slots ===")
for sub in ["chassis", "head_unit", "costume", "optic_core", "weapon", "winding_key", "back_curio"]:
    sub_dir = f"{MACAQUE_DIR}/{sub}"
    if os.path.exists(sub_dir):
        for f in sorted(os.listdir(sub_dir)):
            if f.endswith(".png") and not f.endswith("_512.png"):
                im = Image.open(f"{sub_dir}/{f}")
                print(f"  {sub}/{f}: size={im.size}, bbox={im.getbbox()}")

print("\n=== 512x512 Slots ===")
for sub in ["chassis", "head_unit", "costume", "optic_core", "weapon", "winding_key", "back_curio"]:
    sub_dir = f"{MACAQUE_DIR}/{sub}"
    if os.path.exists(sub_dir):
        for f in sorted(os.listdir(sub_dir)):
            if f.endswith("_512.png") or f == "curio_spring_tail.png":
                im = Image.open(f"{sub_dir}/{f}")
                print(f"  {sub}/{f}: size={im.size}, bbox={im.getbbox()}")
