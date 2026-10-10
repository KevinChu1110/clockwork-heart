#!/usr/bin/env python3
"""
驗證 t_ccf48aae 四大背包與工坊閉環功能回歸實機截圖存證：
1. 存在性與檔案大小 (> 20KB)
2. 尺寸 (1280x720)
3. SHA256 唯一性
4. 零空白/零黑屏檢測 (min != max)
"""
import hashlib
import os
import sys
from PIL import Image

DIRS = [
    "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_ccf48aae/proofs/t_ccf48aae",
    "/opt/side/bravesoul-game/proofs/t_ccf48aae"
]

FILES = [
    "proof_01_bag_dismantle_btn_visible.png",
    "proof_02_bag_gem_detail_and_refund.png",
    "proof_03_forge_workshop_bidirectional_link.png",
    "proof_04_bag_workshop_shortcut_btn.png",
]

def main():
    print("=== 驗證 t_ccf48aae 實機回歸截圖存證 ===")
    errors = []
    
    for base_dir in DIRS:
        if not os.path.exists(base_dir):
            errors.append(f"目錄不存在: {base_dir}")
            continue
            
        print(f"\n[檢查目錄] {base_dir}")
        hashes = {}
        for name in FILES:
            full_path = os.path.join(base_dir, name)
            if not os.path.exists(full_path):
                errors.append(f"截圖不存在: {full_path}")
                continue

            f_size = os.path.getsize(full_path)
            if f_size < 20000:
                errors.append(f"截圖過小 ({f_size} bytes): {name}")

            with open(full_path, "rb") as f:
                h = hashlib.sha256(f.read()).hexdigest()
            if h in hashes:
                errors.append(f"SHA256 重複: {name} 與 {hashes[h]} 相同 ({h})")
            else:
                hashes[h] = name

            try:
                with Image.open(full_path) as im:
                    if im.size != (1280, 720):
                        errors.append(f"截圖尺寸非 1280x720: {name} 為 {im.size}")
                    stat = im.convert("L").getextrema()
                    if stat[0] == stat[1]:
                        errors.append(f"截圖為純色圖: {name}")
                    print(f"  ✓ {name} ({f_size}B, 1280x720, SHA256={h[:16]}..., min={stat[0]}, max={stat[1]})")
            except Exception as e:
                errors.append(f"PIL 讀取失敗 {name}: {e}")

    if errors:
        print("\n[FAIL] 發現以下錯誤:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)

    print("\n[OK] 全部 4 項功能獨立實機截圖存證完全合格！")

if __name__ == "__main__":
    main()
