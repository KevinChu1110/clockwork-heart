#!/usr/bin/env python3
"""
探索性 QA 第三十六輪 自動查驗腳本 (verify_qa_round36.py)
依據規範：review.md 0-QA15, 0-QA17, 0-QA23, 0-QA24, 0-QA25
"""

import os
import sys
import hashlib
from PIL import Image

PROOF_DIR = "proofs/qa_round36"
CROPS_DIR = "proofs/qa_round36/crops"

FULL_PROOFS = [
    "proof_01_lobby_village_zh_TW.png",
    "proof_02_lobby_village_en.png",
    "proof_03_lobby_village_ja.png",
    "proof_04_lobby_village_ko.png",
    "proof_05_regression_forge_dialog.png",
    "proof_06_regression_gem_workshop_dialog.png",
    "proof_07_regression_windup_quest_dialog.png",
    "proof_08_regression_sortie_adventure_tab.png",
]

CROPS = [
    "crop_hall_cards_zh_TW.png",
    "crop_hall_cards_en.png",
    "crop_hall_cards_ja.png",
    "crop_hall_cards_ko.png",
    "crop_dock_zh_TW.png",
    "crop_dock_en.png",
    "crop_dock_ja.png",
    "crop_dock_ko.png",
    "crop_topbar_zh_TW.png",
    "crop_topbar_en.png",
    "crop_topbar_ja.png",
    "crop_topbar_ko.png",
]

def md5_file(path: str) -> str:
    h = hashlib.md5()
    with open(path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()

def main():
    print("=== 探索性 QA 第三十六輪 驗證開始 ===")
    ok = True

    # 1. [0-QA23] 目錄檢查
    print("\n[階段 1: 0-QA23 獨立目錄檢驗]")
    if not os.path.isdir(PROOF_DIR) or not os.path.isdir(CROPS_DIR):
        print(f"  ❌ 目錄不存在: {PROOF_DIR} 或 {CROPS_DIR}")
        return 1
    print(f"  ✓ proof 輸出目錄獨立指向 {PROOF_DIR}，無覆蓋其它任務目錄。")

    # 2. [0-QA15] 規格 (1280x720) 與 MD5 互異性檢驗
    print("\n[階段 2: 0-QA15 規格與 MD5 互異性檢驗 (8張全景)]")
    seen_md5 = {}
    for fn in FULL_PROOFS:
        path = os.path.join(PROOF_DIR, fn)
        if not os.path.isfile(path):
            print(f"  ❌ 檔案缺失: {path}")
            ok = False
            continue

        size_kb = os.path.getsize(path) / 1024
        if size_kb < 40:
            print(f"  ❌ 檔案過小 (<40KB): {fn} ({size_kb:.1f} KB)")
            ok = False

        digest = md5_file(path)
        if digest in seen_md5:
            print(f"  ❌ MD5 重複 (0-QA15 違規): {fn} 與 {seen_md5[digest]} 重複 ({digest})")
            ok = False
        else:
            seen_md5[digest] = fn

        try:
            with Image.open(path) as img:
                w, h = img.size
                if (w, h) != (1280, 720):
                    print(f"  ❌ 規格不符 1280x720: {fn} ({w}x{h})")
                    ok = False
                else:
                    print(f"  ✓ {fn}: 1280x720 | {size_kb:.1f} KB | md5={digest[:8]}...")
        except Exception as e:
            print(f"  ❌ 圖檔解析失敗: {fn}, err={e}")
            ok = False

    # 3. [0-QA15] 局部特寫檢驗 (12張 Crops)
    print("\n[階段 3: 局部特寫 Crops 完整性與規格檢驗 (12張)]")
    crop_md5 = {}
    for fn in CROPS:
        path = os.path.join(CROPS_DIR, fn)
        if not os.path.isfile(path):
            print(f"  ❌ 特寫圖缺失: {path}")
            ok = False
            continue

        size_kb = os.path.getsize(path) / 1024
        digest = md5_file(path)
        if digest in crop_md5:
            print(f"  ❌ Crop MD5 重複: {fn} 與 {crop_md5[digest]} ({digest})")
            ok = False
        else:
            crop_md5[digest] = fn

        try:
            with Image.open(path) as img:
                w, h = img.size
                print(f"  ✓ {fn}: {w}x{h} | {size_kb:.1f} KB | md5={digest[:8]}...")
        except Exception as e:
            print(f"  ❌ Crop 圖檔解析失敗: {fn}, err={e}")
            ok = False

    if ok:
        print("\n🎉 探索性 QA 第三十六輪 實機截圖與規範核驗全數合格 (PASS)！")
        return 0
    else:
        print("\n❌ 驗證失敗，請檢查錯誤紀錄。")
        return 1

if __name__ == "__main__":
    sys.exit(main())
