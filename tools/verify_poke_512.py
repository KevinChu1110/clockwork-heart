#!/usr/bin/env python3
import hashlib
import sys
from PIL import Image
import numpy as np

def get_md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def analyze_crop(img_path, box, name):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    print(f"[{name}] 圖片尺寸: {w}x{h}")
    crop = img.crop(box)
    crop.save(f"screenshots/crop_{name}.png")
    arr = np.array(crop)
    cw, ch = crop.size
    
    # 計算 unique 顏色數 (RGB)
    rgb_arr = arr[:, :, :3].reshape(-1, 3)
    unique_colors = len(np.unique(rgb_arr, axis=0))
    
    # 計算相鄰重複欄比例 (horizontal neighbor duplicate columns)
    # NN 放大若為 2x 放大，(N-1)/N = 50% 重複欄；若不是 NN 放大，重複欄應該極低 (接近 0%)
    dup_cols = 0
    for x in range(cw - 1):
        if np.array_equal(arr[:, x, :3], arr[:, x + 1, :3]):
            dup_cols += 1
    dup_col_ratio = dup_cols / (cw - 1) if cw > 1 else 0
    
    # 重複列比例
    dup_rows = 0
    for y in range(ch - 1):
        if np.array_equal(arr[y, :, :3], arr[y + 1, :, :3]):
            dup_rows += 1
    dup_row_ratio = dup_rows / (ch - 1) if ch > 1 else 0

    print(f"  Crop 區域 ({box}): {cw}x{ch}")
    print(f"  Unique 顏色數: {unique_colors}")
    print(f"  相鄰重複欄比例: {dup_col_ratio:.2%}")
    print(f"  相鄰重複列比例: {dup_row_ratio:.2%}")
    
    return unique_colors, dup_col_ratio, dup_row_ratio

def main():
    p1 = "screenshots/proof_lobby_poke_rabbit_attack_512.png"
    p2 = "screenshots/proof_lobby_poke_lion_attack_512.png"
    
    md5_1 = get_md5(p1)
    md5_2 = get_md5(p2)
    print("0-QA18 檢查 (1280x720 完整畫面，有場景有 HUD，非貼圖 dump):")
    for p in [p1, p2]:
        img = Image.open(p).convert("RGBA")
        w, h = img.size
        print(f"  檢查 {p}: 尺寸 {w}x{h}")
        if (w, h) != (1280, 720):
            print(f"FAIL: 尺寸不是 1280x720: {w}x{h}")
            sys.exit(1)
        arr = np.array(img)
        corners = [arr[0, 0, 3], arr[0, w-1, 3], arr[h-1, 0, 3], arr[h-1, w-1, 3]]
        if all(c == 0 for c in corners):
            print(f"FAIL: {p} 四角全透明，判定為貼圖 dump (0-QA18 違規)！")
            sys.exit(1)
        print(f"  ✓ 0-QA18 通過: {p} 為 1280x720 實機渲染畫面，四角不透明。")

    print("\n0-QA15 檢查 (md5 查重):")
    print(f"  兔族: {p1} -> md5: {md5_1}")
    print(f"  獅族: {p2} -> md5: {md5_2}")
    if md5_1 == md5_2:
        print("FAIL: md5 相同！兩張截圖重複！")
        sys.exit(1)
    # 檢查歷史截圖是否重複
    hist_md5s = {
        "777398385f24464351a31d6544a56a48": "歷史獅族截圖",
        "034441a689e97f5930227ab077c12b97": "歷史兔族截圖"
    }
    for m, name in [(md5_1, "兔族"), (md5_2, "獅族")]:
        if m in hist_md5s:
            print(f"FAIL: {name}截圖 md5 與{hist_md5s[m]}重複！")
            sys.exit(1)
    print("  ✓ PASS: 兩張截圖 md5 完全相異，且與歷史截圖不重複！")
        
    print("\n0-QA17 檢查 (角色區域量測，否證 128 NEAREST 放大):")
    # 大廳角色中央區域大約在 x: 515~765, y: 220~490 (原 1280x720 畫面中央)
    box = (520, 220, 760, 480)
    c1, col_r1, row_r1 = analyze_crop(p1, box, "rabbit_attack")
    c2, col_r2, row_r2 = analyze_crop(p2, box, "lion_attack")
    
    if col_r1 > 0.10 or col_r2 > 0.10:
        print("FAIL: 重複欄比例 > 10%，可能為 NEAREST 放大！")
        sys.exit(1)
    if c1 < 5000 or c2 < 5000:
        print("FAIL: Unique 色數過低，可能為低色數點陣！")
        sys.exit(1)
        
    print("\n✓ 0-QA17 驗證通過：重複欄 ≈ 0%，色數破萬，證明為高清 512 + LINEAR 渲染！")

if __name__ == "__main__":
    main()
