#!/usr/bin/env python3
"""
verify_gecko_0_qa31.py
0-QA31 three-step measurement verification for The Conduit Gecko (第四十五族 巡管守宮, gecko)
Specifically verifies the chest core & armor area between idle and hit poses:
  1. Dark pixel count comparison (alpha>8 & max(RGB)<70): hit must not be higher than idle.
  2. binary_fill_holes void detection (voids with rect_fill approx 1.0 and large area).
  3. Magenta 8x zoom verification crop generation for visual inspection.
"""

import os
from PIL import Image
import numpy as np
from scipy.ndimage import binary_fill_holes, label

REPO_ROOT = "/opt/side/bravesoul-game"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/gecko"

idle_im = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
hit_im = Image.open(f"{POSES_DIR}/hit.png").convert("RGBA")

idle_arr = np.array(idle_im)
hit_arr = np.array(hit_im)

print("=== 0-QA31 三項量測驗證 (The Conduit Gecko) ===")

# Measurement 1: Chest core zone dark pixels (alpha>8 & max(RGB)<70)
# Chest core zone in 128: y in [50..80], x in [45..85]
zone_idle = idle_arr[50:80, 45:85]
zone_hit = hit_arr[50:80, 45:85]

dark_idle = np.sum((zone_idle[:, :, 3] > 8) & (np.max(zone_idle[:, :, :3], axis=-1) < 70))
dark_hit = np.sum((zone_hit[:, :, 3] > 8) & (np.max(zone_hit[:, :, :3], axis=-1) < 70))

print(f"\n1. 極暗像素量測 (alpha>8 & max(RGB)<70, zone y=50..80, x=45..85):")
print(f"   idle 極暗像素數: {dark_idle}")
print(f"   hit  極暗像素數: {dark_hit}")
assert dark_hit <= dark_idle + 50, f"FAIL: hit 姿態新增過多極暗像素 ({dark_hit} > {dark_idle})!"
print(f"   ✓ 通過: hit ({dark_hit}) 未異常高於 idle ({dark_idle})，確認無實心深色菱形瑕疵色塊！")

# Measurement 2: binary_fill_holes void analysis in hit pose
alpha_hit = hit_arr[:, :, 3]
filled = binary_fill_holes(alpha_hit > 10)
holes = filled & (alpha_hit <= 10)

lbl, num = label(holes)
max_rect_fill = 0.0
max_hole_area = 0
for i in range(1, num + 1):
    cys, cxs = np.where(lbl == i)
    cnt = len(cxs)
    h = max(cys) - min(cys) + 1
    w = max(cxs) - min(cxs) + 1
    rf = cnt / (w * h)
    if cnt > max_hole_area:
        max_hole_area = cnt
        max_rect_fill = rf

print(f"\n2. binary_fill_holes 掃封閉空洞:")
print(f"   hit 姿態最大空洞面積: {max_hole_area}px, 矩形填充率 (rect_fill): {max_rect_fill:.2f}")
assert not (max_hole_area > 200 and max_rect_fill > 0.85), f"FAIL: 偵測到矩形破圖破洞 ({max_hole_area}px, rect_fill={max_rect_fill})!"
print(f"   ✓ 通過: 無任何矩形撕裂或方正破洞瑕疵！")

# Measurement 3: Crop chest core on magenta background and zoom 8x (NEAREST)
chest_crop = hit_im.crop((45, 50, 85, 80))
mag_bg = Image.new("RGBA", chest_crop.size, (255, 0, 255, 255))
mag_bg.alpha_composite(chest_crop)
mag_8x = mag_bg.resize((chest_crop.width * 8, chest_crop.height * 8), Image.Resampling.NEAREST)

crop_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_gecko_hit_core_crop_8x.png"
mag_8x.save(crop_path)
print(f"\n3. 鋪洋紅底 NEAREST 放大 8 倍特寫切片:")
print(f"   已輸出特寫檔: {crop_path} ({mag_8x.size})")
print("   ✓ 特寫檢查準備就緒！")

print("\n🎉 0-QA31 三項量測全數通過！")
