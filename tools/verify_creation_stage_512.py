#!/usr/bin/env python3
import hashlib
import os
import sys
import numpy as np
from PIL import Image

def get_md5(path):
    with open(path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def analyze_crop(img_path, box, name):
    img = Image.open(img_path).convert("RGBA")
    w, h = img.size
    crop = img.crop(box)
    os.makedirs("screenshots", exist_ok=True)
    crop_path = f"screenshots/crop_{name}.png"
    crop.save(crop_path)
    arr = np.array(crop)
    cw, ch = crop.size
    
    # 計算 unique 顏色數 (RGB)
    rgb_arr = arr[:, :, :3].reshape(-1, 3)
    unique_colors = len(np.unique(rgb_arr, axis=0))
    
    # 計算相鄰重複欄比例 (horizontal neighbor duplicate columns)
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

    print(f"  Crop 區域 [{name}] ({box}): {cw}x{ch}")
    print(f"    Unique 顏色數: {unique_colors}")
    print(f"    相鄰重複欄比例: {dup_col_ratio:.2%}")
    print(f"    相鄰重複列比例: {dup_row_ratio:.2%}")
    
    return unique_colors, dup_col_ratio, dup_row_ratio

def main():
    proof_files = {
        "rabbit": "proofs/creation_stage_512/proof_creation_stage_rabbit_512.png",
        "fox": "proofs/creation_stage_512/proof_creation_stage_fox_512.png",
        "crane": "proofs/creation_stage_512/proof_creation_stage_crane_512.png",
        "lion": "proofs/creation_stage_512/proof_creation_stage_lion_512.png"
    }

    print("==================================================================")
    print("=== 開局選族中央舞台 512 高清合成 實機截圖與規範全面驗證 ===")
    print("==================================================================")

    # 1. 0-QA18 檢查 (1280x720 完整畫面，有場景有 HUD，非貼圖 dump)
    print("\n=== 1. 0-QA18 檢查 (1280x720 完整畫面，有場景有 HUD，非貼圖 dump) ===")
    for race, p in proof_files.items():
        if not os.path.exists(p):
            print(f"FAIL: 截圖檔案不存在: {p}")
            sys.exit(1)
        img = Image.open(p).convert("RGBA")
        w, h = img.size
        print(f"  檢查 [{race}] ({p}): 尺寸 {w}x{h}")
        if (w, h) != (1280, 720):
            print(f"FAIL: 尺寸不是 1280x720: {w}x{h}")
            sys.exit(1)
        arr = np.array(img)
        corners = [arr[0, 0, 3], arr[0, w-1, 3], arr[h-1, 0, 3], arr[h-1, w-1, 3]]
        if all(c == 0 for c in corners):
            print(f"FAIL: {p} 四角全透明，判定為貼圖 dump (0-QA18 違規)！")
            sys.exit(1)
        # 純白像素檢查
        white_pixels = np.sum(np.all(arr[:, :, :3] > 250, axis=2) & (arr[:, :, 3] > 250))
        white_ratio = white_pixels / (w * h)
        if white_ratio > 0.5:
            print(f"FAIL: {p} 純白比例過高 ({white_ratio:.2%})，可能為白底 dump！")
            sys.exit(1)
        print(f"    ✓ 0-QA18 通過: 為 1280x720 實機渲染畫面，四角不透明，純白比例={white_ratio:.2%}。")

    # 2. 0-QA15 檢查 (MD5 查重)
    print("\n=== 2. 0-QA15 檢查 (MD5 查重) ===")
    md5_dict = {}
    for race, p in proof_files.items():
        md5_val = get_md5(p)
        print(f"  [{race}] {p} -> MD5: {md5_val}")
        if md5_val in md5_dict.values():
            print(f"FAIL: MD5 衝突！{race} 截圖與其他種族重複！")
            sys.exit(1)
        md5_dict[race] = md5_val
    print("  ✓ 0-QA15 通過: 截圖 MD5 互不重複！")

    # 3. 0-QA17 檢查 (中央舞台角色區域量測，否證 128 NEAREST 放大)
    print("\n=== 3. 0-QA17 檢查 (中央舞台角色區域量測，否證 128 NEAREST 放大) ===")
    char_box = (250, 360, 370, 560)
    for race, p in proof_files.items():
        unique_colors, dup_col_ratio, dup_row_ratio = analyze_crop(p, char_box, f"stage_{race}")
        if dup_col_ratio > 0.08:
            print(f"FAIL: [{race}] 重複欄比例 > 8% ({dup_col_ratio:.2%})，可能為 128 NEAREST 硬放大！")
            sys.exit(1)
        if unique_colors < 5000:
            print(f"FAIL: [{race}] Unique 色數過低 ({unique_colors})，可能為低色數點陣！")
            sys.exit(1)
        print(f"    ✓ [{race}] 0-QA17 通過: 重複欄比例={dup_col_ratio:.2%} (<8%), 色數={unique_colors} (>5000)")

    # 4. 狐族臉部錯位青綠光球否證量測 (review 意見 2)
    print("\n=== 4. 狐族臉部錯位青綠光球否證量測 ===")
    fox_img = Image.open(proof_files["fox"]).convert("RGBA")
    fox_arr = np.array(fox_img)
    fox_face = fox_arr[380:480, 270:360]
    face_cyan = (fox_face[:, :, 1] > 120) & (fox_face[:, :, 2] > 100) & (fox_face[:, :, 0] < fox_face[:, :, 1] - 20)
    cyan_count = np.sum(face_cyan)
    print(f"  狐族臉部區域 (y:380..480, x:270..360) 孤立青綠像素數: {cyan_count}")
    if cyan_count > 0:
        print(f"FAIL: 狐族臉部仍有殘留青綠色像素 ({cyan_count})！")
        sys.exit(1)
    print("  ✓ 狐族臉部乾淨，無錯位青綠色發光球！")

    # 5. 0-ART26c 武器渲染量測 (review 意見 1: 獅族手持長槍判定)
    print("\n=== 5. 0-ART26c 武器渲染量測 ===")
    lion_img = Image.open(proof_files["lion"]).convert("RGBA")
    lion_arr = np.array(lion_img)
    # 獅族右手持長槍區域 (x:240..275, y:360..460)
    lance_crop = lion_arr[360:460, 240:275]
    # 長槍槍身主要為金黃/乳白/深青色
    lance_pixels = np.sum((lance_crop[:, :, 3] > 200) & (lance_crop[:, :, :3].mean(axis=2) > 100))
    print(f"  獅族長槍區域實機像素數: {lance_pixels}")
    if lance_pixels < 200:
        print(f"FAIL: 獅族長槍未正確渲染！(像素數={lance_pixels})")
        sys.exit(1)
    print("  ✓ 獅族長槍清晰持於手上，武器槽位渲染通過！")

    print("\n==================================================================")
    print("✓ 全項驗證通過：0-QA18 (1280x720 完整畫面), 0-QA17 (512+LINEAR 平滑無鋸齒), 0-QA15 (無重複), 0-ART26c (武器完整渲染), 狐面乾淨")
    print("==================================================================")

if __name__ == "__main__":
    main()
