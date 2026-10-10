#!/usr/bin/env python3
"""
驗證 t_58e87148 / t_d9a6aa7e 實機回歸截圖存證：
- 存在性與檔案大小 (> 20KB)
- 尺寸 (1280x720)
- SHA256 唯一性
- 零空白/零黑屏檢測
"""
import hashlib
import os
import sys
from PIL import Image

BASE_DIR = "/opt/side/bravesoul-game/proofs/t_58e87148"

FILES = [
    "proof_01_bag_weapon_selected_zh_TW.png",
    "proof_02_bag_consumable_selected_hidden.png",
    "proof_03_bag_weapon_selected_en.png",
    "proof_04_forge_dialog_transitioned.png",
]

def main():
    print(f"=== 驗證 {BASE_DIR} 實機截圖存證 ===")
    hashes = {}
    errors = []

    for full_name in FILES:
        full_path = os.path.join(BASE_DIR, full_name)

        if not os.path.exists(full_path):
            errors.append(f"截圖不存在: {full_path}")
            continue

        f_size = os.path.getsize(full_path)
        if f_size < 20000:
            errors.append(f"截圖過小 ({f_size} bytes): {full_name}")

        with open(full_path, "rb") as f:
            h = hashlib.sha256(f.read()).hexdigest()
        if h in hashes:
            errors.append(f"SHA256 重複: {full_name} 與 {hashes[h]} 相同 ({h})")
        else:
            hashes[h] = full_name

        try:
            with Image.open(full_path) as im:
                if im.size != (1280, 720):
                    errors.append(f"截圖尺寸非 1280x720: {full_name} 為 {im.size}")
                stat = im.convert("L").getextrema()
                if stat[0] == stat[1]:
                    errors.append(f"截圖為純色圖: {full_name}")
                print(f"  ✓ {full_name} ({f_size}B, 1280x720, SHA256={h[:16]}..., min={stat[0]}, max={stat[1]})")
        except Exception as e:
            errors.append(f"PIL 讀取失敗 {full_name}: {e}")

    if errors:
        print("\n[FAIL] 發現以下錯誤:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print("\n[OK] 全部 4 張實機截圖校驗完全合格！")

if __name__ == "__main__":
    main()
