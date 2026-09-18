#!/usr/bin/env python3
"""
tools/verify_bear_penguin_color_sync.py
Verifies color synchronization between head_unit variants and chassis paints for Bear and Penguin.
Criteria: Color distance between head dominant color and chassis dominant color must be < 60.0 for new paint variants.
"""

import os
import numpy as np
from PIL import Image

REPO = "/opt/side/bravesoul-game"

def check_dominant_opaque_color(path, is_chassis=False):
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    opaque = arr[arr[:, :, 3] > 200][:, :3]
    if is_chassis:
        # 排除接縫與深色邊框 (max channel > 70)
        filtered = opaque[np.max(opaque, axis=1) > 70]
    else:
        # 排除深色描邊
        filtered = opaque[~((opaque[:, 0] < 50) & (opaque[:, 1] < 50) & (opaque[:, 2] < 50))]
    colors, counts = np.unique(filtered, axis=0, return_counts=True)
    top_color = tuple(int(x) for x in colors[np.argmax(counts)])
    return top_color

def color_distance(c1, c2):
    return float(np.linalg.norm(np.array(c1) - np.array(c2)))

def main():
    print("================================================================================")
    print("【驗收量測】玄軸熊與蒸氣企鵝頭部塗裝同步色距稽核 (0-ART28h)")
    print("================================================================================")
    
    # 依任務指示：熊族 amber/quarry 與企鵝族 ivory/polar 為本單補齊塗裝，色距需 < 60.0。
    # stock 保持原圖基準。
    pairs = [
        # Bear Variants
        ("Bear", "Amber (新增)", 
         f"{REPO}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_amber_512.png",
         f"{REPO}/game/assets/sprites/player/paperdoll/bear/chassis/paint_bear_amber_512.png", True),
        ("Bear", "Quarry (新增)", 
         f"{REPO}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_quarry_512.png",
         f"{REPO}/game/assets/sprites/player/paperdoll/bear/chassis/paint_iron_quarry_512.png", True),
        ("Bear", "Ivory Stock (原圖)", 
         f"{REPO}/game/assets/sprites/player/paperdoll/bear/head_unit/head_iron_bear_stock_512.png",
         f"{REPO}/game/assets/sprites/player/paperdoll/bear/chassis/paint_ivory_stock_512.png", False),
        
        # Penguin Variants
        ("Penguin", "Ivory (新增)", 
         f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_ivory_512.png",
         f"{REPO}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_ivory_stock_512.png", True),
        ("Penguin", "Polar Frost (新增)", 
         f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_polar_512.png",
         f"{REPO}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_polar_frost_512.png", True),
        ("Penguin", "Navy Stock (原圖)", 
         f"{REPO}/game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock_512.png",
         f"{REPO}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_penguin_navy_512.png", False),
    ]

    all_pass = True
    print(f"{'族系':8s} | {'塗裝':16s} | {'Head 主色 (RGB)':20s} | {'Chassis 主色 (RGB)':20s} | {'色距':6s} | {'判定'}")
    print("-" * 92)

    for race, variant, head_p, ch_p, is_variant in pairs:
        assert os.path.exists(head_p), f"缺少頭部切片: {head_p}"
        assert os.path.exists(ch_p), f"缺少身體切片: {ch_p}"

        c_head = check_dominant_opaque_color(head_p, is_chassis=False)
        c_ch = check_dominant_opaque_color(ch_p, is_chassis=True)
        dist = color_distance(c_head, c_ch)
        
        if is_variant:
            status = "✅ PASS" if dist < 60.0 else "❌ FAIL"
            if dist >= 60.0:
                all_pass = False
        else:
            status = f"ℹ️ 原圖基準 ({'PASS' if dist < 60.0 else '未改動'})"
            
        print(f"{race:8s} | {variant:16s} | {str(c_head):20s} | {str(c_ch):20s} | {dist:6.1f} | {status}")

    print("-" * 92)
    if all_pass:
        print("🎉 全部補齊變體頭部與身體主色色距均遠優於 60.0 標準，驗收通過！")
    else:
        print("❌ 有變體未達標（色距 >= 60.0）！")
    return all_pass

if __name__ == "__main__":
    import sys
    ok = main()
    sys.exit(0 if ok else 1)
