#!/usr/bin/env python3
"""
tools/audit_marmot_poses.py
驗收輪廓差 audit:
- battle vs idle 要有明顯差異 (>= 4000 px)
- battle vs attack 相同屬正常 (review.md 4b-8-1)
"""
import os
import sys
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/marmot"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"

print("=================================================================")
print("=== 第六十五族碎石旱獺 (marmot) 戰鬥姿態輪廓差 Audit ===")
print("=================================================================")

idle_img = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
attack_img = Image.open(f"{POSES_DIR}/attack.png").convert("RGBA")
battle_img = Image.open(f"{PLAYER_DIR}/marmot_battle.png").convert("RGBA")

# 1. battle vs idle
diff_bi = ImageChops.difference(battle_img, idle_img)
arr_bi = np.array(diff_bi)
body_diff_bi = int(np.sum(np.any(arr_bi[:118, :, :] > 0, axis=-1)))
total_diff_bi = int(np.sum(np.any(arr_bi > 0, axis=-1)))

print(f"\n[1] Battle vs Idle 輪廓差檢驗:")
print(f"    - 身體區 (y < 118) 差異像素: {body_diff_bi} px")
print(f"    - 全圖差異像素: {total_diff_bi} px ({total_diff_bi / (128*128) * 100:.1f}%)")
if body_diff_bi >= 4000:
    print(f"    ✓ PASS: battle vs idle 具備極顯著姿態與輪廓差異 ({body_diff_bi} px >= 4000 px)")
else:
    print(f"    ❌ FAIL: battle vs idle 差異不足 ({body_diff_bi} px < 4000 px)")
    sys.exit(1)

# 2. battle vs attack
diff_ba = ImageChops.difference(battle_img, attack_img)
arr_ba = np.array(diff_ba)
diff_ba_count = int(np.sum(np.any(arr_ba > 0, axis=-1)))

print(f"\n[2] Battle vs Attack 慣例對齊檢驗 (review.md 4b-8-1):")
print(f"    - 差異像素: {diff_ba_count} px")
if diff_ba_count == 0:
    print(f"    ✓ PASS: battle == attack 完全一致 (符合 review.md 4b-8-1 全域慣例，非違規)")
else:
    print(f"    ❌ FAIL: battle 與 attack 不一致 ({diff_ba_count} px)")
    sys.exit(1)

print("\n=================================================================")
print("=== MARMOT_POSES_SILHOUETTE_AUDIT_OK ===")
print("=================================================================")
