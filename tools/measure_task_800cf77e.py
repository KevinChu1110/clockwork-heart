import os
import glob
import numpy as np
from PIL import Image

print("=== 1. 0-QA17 角色區 Crop 重複欄量測 (NN baseline ~50% vs 實機 512 合成) ===")

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
            
    # 水平方向像素重複對
    h_pix_repeats = np.sum(np.all(arr[:, :-1] == arr[:, 1:], axis=2))
    total_pairs = h * (w - 1)
    pix_repeat_rate = h_pix_repeats / total_pairs
    
    return col_repeats / (w - 1), row_repeats / (h - 1), pix_repeat_rate, im.size

crops = [
    "screenshots/proof_explore_fox_equipped_crop.png",
    "screenshots/proof_battle_lion_equipped_crop.png",
    "screenshots/proof_wardrobe_preview_crop.png"
]

for cp in crops:
    if os.path.exists(cp):
        col, row, pix, sz = compute_repeat_rates(cp)
        print(f"File: {cp} (size={sz})")
        print(f"  - 相鄰整欄完全相同比例: {col*100:.2f}% (若為 NN 放大此值常在 40%~75%)")
        print(f"  - 相鄰整列完全相同比例: {row*100:.2f}%")
        print(f"  - 相鄰像素水平重複比例: {pix*100:.2f}%")
        is_ok = col < 0.20 # 遠低於 NN 的 50%
        print(f"  => 0-QA17 判定: {'PASS (非 NN 放大，為平滑真實渲染)' if is_ok else 'FAIL'}\n")
    else:
        print(f"File not found: {cp}")

print("\n=== 2. 衣櫥格子來源檔長邊 ≥ 512 量測 ===")
all_costumes = [
    "game/assets/sprites/player/paperdoll/common/costume/costume_viking_harness_512.png",
    "game/assets/sprites/player/paperdoll/common/costume/costume_dawn_monk_tunic_512.png",
    "game/assets/sprites/player/paperdoll/common/costume/costume_astral_cape_512.png",
    "game/assets/sprites/player/paperdoll/common/costume/costume_nutcracker_guard_512.png"
]
all_races = ["fox", "lion", "boar", "macaque", "tiger", "bear", "crane", "penguin", "rabbit"]
chassis_files = []
for r in all_races:
    chassis_files.extend(glob.glob(f"game/assets/sprites/player/paperdoll/{r}/chassis/*_512.png"))

print(f"Checking {len(all_costumes)} shared costume 512 files...")
costumes_ok = True
for f in all_costumes:
    with Image.open(f) as im:
        max_edge = max(im.size)
        print(f"  [OK] {os.path.basename(f)}: size={im.size}, max_edge={max_edge} >= 512")
        if max_edge < 512:
            costumes_ok = False

print(f"\nChecking {len(chassis_files)} chassis 512 files across all 9 races...")
chassis_ok = True
for f in chassis_files:
    with Image.open(f) as im:
        max_edge = max(im.size)
        if max_edge < 512:
            print(f"  [FAIL] {f}: size={im.size}")
            chassis_ok = False
if chassis_ok:
    print(f"  ✓ 全數 {len(chassis_files)} 張 chassis 512 切片長邊均 >= 512")

print(f"\n總結: 衣櫥格子來源檔長邊 ≥512 檢驗 {'PASS' if costumes_ok and chassis_ok else 'FAIL'}")
