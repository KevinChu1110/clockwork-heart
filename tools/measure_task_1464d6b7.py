import os
import glob
import hashlib
import numpy as np
from PIL import Image

print("=== 1. 0-QA17 走動角色區 Crop 重複欄量測 (NN baseline ~50% vs 實機 512 合成) ===")

def compute_repeat_rates(img_path):
    im = Image.open(img_path).convert("RGBA")
    arr = np.array(im)
    h, w, _ = arr.shape
    
    col_repeats = 0
    for c in range(w - 1):
        if np.array_equal(arr[:, c], arr[:, c + 1]):
            col_repeats += 1
            
    row_repeats = 0
    for r in range(h - 1):
        if np.array_equal(arr[r, :], arr[r + 1, :]):
            row_repeats += 1
            
    h_pix_repeats = np.sum(np.all(arr[:, :-1] == arr[:, 1:], axis=2))
    total_pairs = h * (w - 1)
    pix_repeat_rate = h_pix_repeats / total_pairs
    
    return col_repeats / (w - 1), row_repeats / (h - 1), pix_repeat_rate, im.size

crops = [
    "screenshots/proof_explore_fox_walk_crop.png",
    "screenshots/proof_explore_lion_walk_crop.png",
    "screenshots/proof_compare_idle_vs_walk_crop.png"
]

all_crops_ok = True
for cp in crops:
    if os.path.exists(cp):
        col, row, pix, sz = compute_repeat_rates(cp)
        print(f"File: {cp} (size={sz})")
        print(f"  - 相鄰整欄完全相同比例: {col*100:.2f}% (NN baseline ~50%)")
        print(f"  - 相鄰整列完全相同比例: {row*100:.2f}%")
        print(f"  - 相鄰像素水平重複比例: {pix*100:.2f}%")
        is_ok = col < 0.25 # 遠低於 NN 的 50%
        if not is_ok:
            all_crops_ok = False
        print(f"  => 0-QA17 判定: {'PASS (非 NN 放大，為平滑真實渲染)' if is_ok else 'FAIL'}\n")
    else:
        print(f"File not found: {cp}")
        all_crops_ok = False

print("\n=== 2. 合成圖長邊 ≥ 512 量測 ===")
proof_files = [
    "screenshots/proof_explore_fox_walk_512.png",
    "screenshots/proof_explore_lion_walk_512.png",
    "screenshots/proof_compare_idle_vs_walk_512.png"
]

all_sizes_ok = True
for pf in proof_files:
    if os.path.exists(pf):
        im = Image.open(pf)
        w, h = im.size
        max_edge = max(w, h)
        is_ok = max_edge >= 512
        if not is_ok:
            all_sizes_ok = False
        print(f"File: {pf} -> 尺寸: {w}x{h}, 長邊: {max_edge} >= 512: {'PASS' if is_ok else 'FAIL'}")
    else:
        print(f"File not found: {pf}")
        all_sizes_ok = False

print("\n=== 3. 截圖 MD5 重複性檢查 ===")
md5s = set()
all_md5_unique = True
for pf in proof_files:
    if os.path.exists(pf):
        with open(pf, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()
        print(f"{pf}: {h}")
        if h in md5s:
            all_md5_unique = False
            print(f"  [ERROR] 重複 MD5: {h}")
        md5s.add(h)

print(f"\n量測結果總結: 0-QA17={all_crops_ok}, 尺寸512={all_sizes_ok}, MD5唯一={all_md5_unique}")
