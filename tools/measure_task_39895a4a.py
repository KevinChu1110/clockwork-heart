#!/usr/bin/env python3
import hashlib
import os
from PIL import Image
import numpy as np

SCREENSHOTS_DIR = "screenshots"

images = [
    "proof_lion_lance_idle_512.png",
    "proof_boar_hammer_idle_512.png",
    "proof_fox_staff_idle_512.png",
]

crop_images = [
    "proof_lion_lance_weapon_crop.png",
    "proof_boar_hammer_weapon_crop.png",
    "proof_fox_staff_weapon_crop.png",
]

print("=== 1. MD5 檢查（不可重複）===")
md5s = {}
for name in images:
    p = os.path.join(SCREENSHOTS_DIR, name)
    with open(p, "rb") as f:
        digest = hashlib.md5(f.read()).hexdigest()
    print(f"  {name}: {digest}")
    if digest in md5s:
        print(f"  FAIL: MD5 重複！與 {md5s[digest]} 相同")
    md5s[digest] = name

print("\n=== 2. 0-QA17 量測（相鄰欄重複率，NN baseline ~50%）===")
for crop_name in crop_images:
    p = os.path.join(SCREENSHOTS_DIR, crop_name)
    im = Image.open(p).convert("RGB")
    arr = np.array(im)
    h, w, c = arr.shape

    # 相鄰欄完全相同的比例
    col_diff = np.abs(arr[:, 1:, :] - arr[:, :-1, :]).sum(axis=2)
    same_col_count = np.sum(np.all(col_diff == 0, axis=0))
    col_repeat_rate = (same_col_count / (w - 1)) * 100.0

    # 相鄰列完全相同的比例
    row_diff = np.abs(arr[1:, :, :] - arr[:-1, :, :]).sum(axis=2)
    same_row_count = np.sum(np.all(row_diff == 0, axis=1))
    row_repeat_rate = (same_row_count / (h - 1)) * 100.0

    # 獨特色數
    unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))

    print(f"  {crop_name} ({w}x{h}):")
    print(f"    重複欄比例: {col_repeat_rate:.2f}% (目標: 遠低於 50%)")
    print(f"    重複列比例: {row_repeat_rate:.2f}%")
    print(f"    獨特色數:   {unique_colors}")

    if col_repeat_rate >= 40.0:
        print(f"    FAIL: 重複欄過高 ({col_repeat_rate:.2f}%)，疑似 NN 放大")
    else:
        print(f"    PASS: 通過 0-QA17 檢驗（非 NN 放大）")
