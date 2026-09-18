#!/usr/bin/env python3
"""
tools/verify_six_races_color_sync.py
Verifies color synchronization and quality metrics for all six races:
Lion, Fox, Boar, Macaque, Tiger, Crane.
Checks:
- Dominant color distance between head_unit and chassis paint (< 60.0).
- Unique color count (> 10000).
- Flat area ratio (< 0.10).
"""

import os
import sys
import numpy as np
from PIL import Image
from tools.verify_bear_penguin_color_sync import check_dominant_opaque_color, color_distance
from tools.audit_head_quality import measure_image_quality

REPO = "/opt/side/bravesoul-game"
BASE = f"{REPO}/game/assets/sprites/player/paperdoll"

TEST_PAIRS = [
    # Lion
    ("Lion", "Midnight Navy",
     f"{BASE}/lion/head_unit/ear_lion_gilded_mane_midnight_512.png",
     f"{BASE}/lion/chassis/paint_midnight_navy_512.png"),
    ("Lion", "Ivory Stock",
     f"{BASE}/lion/head_unit/ear_lion_gilded_mane_ivory_512.png",
     f"{BASE}/lion/chassis/paint_ivory_stock_512.png"),
     
    # Fox
    ("Fox", "Emerald Glaze",
     f"{BASE}/fox/head_unit/ear_fox_radar_emerald_512.png",
     f"{BASE}/fox/chassis/paint_emerald_glaze_512.png"),
    ("Fox", "Ivory Stock",
     f"{BASE}/fox/head_unit/ear_fox_radar_ivory_512.png",
     f"{BASE}/fox/chassis/paint_ivory_stock_512.png"),

    # Boar
    ("Boar", "Molten Crimson",
     f"{BASE}/boar/head_unit/ear_boar_rivet_cowl_crimson_512.png",
     f"{BASE}/boar/chassis/paint_molten_crimson_512.png"),
    ("Boar", "Brass Gold",
     f"{BASE}/boar/head_unit/ear_boar_rivet_cowl_brass_512.png",
     f"{BASE}/boar/chassis/paint_brass_gold_512.png"),

    # Macaque
    ("Macaque", "Bamboo Bronze",
     f"{BASE}/macaque/head_unit/ear_macaque_coaxial_bronze_512.png",
     f"{BASE}/macaque/chassis/paint_bamboo_bronze_512.png"),

    # Tiger
    ("Tiger Head", "Volcano Black",
     f"{BASE}/tiger/head_unit/head_ember_tiger_volcano_512.png",
     f"{BASE}/tiger/chassis/paint_volcano_black_512.png"),
    ("Tiger Head", "Ivory Stock",
     f"{BASE}/tiger/head_unit/head_ember_tiger_ivory_512.png",
     f"{BASE}/tiger/chassis/paint_ivory_stock_512.png"),
    ("Tiger Ear", "Volcano Black",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_volcano_512.png",
     f"{BASE}/tiger/chassis/paint_volcano_black_512.png"),
    ("Tiger Ear", "Ivory Stock",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_ivory_512.png",
     f"{BASE}/tiger/chassis/paint_ivory_stock_512.png"),

    # Crane
    ("Crane", "Zephyr Azure",
     f"{BASE}/crane/head_unit/head_cloud_crane_azure_512.png",
     f"{BASE}/crane/chassis/paint_zephyr_azure_512.png"),
    ("Crane", "Ivory Stock",
     f"{BASE}/crane/head_unit/head_cloud_crane_ivory_512.png",
     f"{BASE}/crane/chassis/paint_ivory_stock_512.png"),
]

def main():
    print("====================================================================================================")
    print("【驗收量測】六族頭部塗裝同步色距與品質指標稽核 (0-ART28h)")
    print("====================================================================================================")
    print(f"{'族系':11s} | {'塗裝變體':14s} | {'Head 主色':17s} | {'Chassis 主色':17s} | {'色距':6s} | {'色階數':6s} | {'平坦區':6s} | {'判定'}")
    print("-" * 100)
    
    all_pass = True
    for race, variant, head_p, ch_p in TEST_PAIRS:
        if not os.path.exists(head_p):
            print(f"Missing head file: {head_p}")
            all_pass = False
            continue
        if not os.path.exists(ch_p):
            print(f"Missing chassis file: {ch_p}")
            all_pass = False
            continue
            
        c_head = check_dominant_opaque_color(head_p, is_chassis=False)
        c_ch = check_dominant_opaque_color(ch_p, is_chassis=True)
        dist = color_distance(c_head, c_ch)
        
        q = measure_image_quality(head_p)
        colors_ok = q["unique_colors"] > 10000
        flat_ok = q["flat_ratio"] < 0.10
        dist_ok = dist < 60.0
        
        is_pass = colors_ok and flat_ok and dist_ok
        if not is_pass:
            all_pass = False
        status = "✅ PASS" if is_pass else "❌ FAIL"
        
        print(f"{race:11s} | {variant:14s} | {str(c_head):17s} | {str(c_ch):17s} | {dist:6.1f} | {q['unique_colors']:6d} | {q['flat_ratio']*100:5.2f}% | {status}")
        
    print("-" * 100)
    if all_pass:
        print("🎉 全部六族新切片色距 < 60.0、色階數 > 10000、平坦區 < 10%，全部通過驗收！")
    else:
        print("❌ 部分切片未達到合格標準，請修正！")
    return all_pass

if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
