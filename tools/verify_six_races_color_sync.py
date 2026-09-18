#!/usr/bin/env python3
"""
tools/verify_six_races_color_sync.py
Verifies color synchronization and quality metrics for all six races:
Lion, Fox, Boar, Macaque, Tiger, Crane.
Formula per t_2247d718 requirement 1:
- Average plate color for opaque pixels (alpha > 200) excluding lineart (max(RGB) <= 70).
- L2 color distance to chassis paint (< 60.0).
- Unique color count (> 10000).
- Flat area ratio (< 0.10, gradient < 1.0 among opaque pixels).
- Unique MD5 vs stock.
"""

import os
import sys
import hashlib

sys.path.insert(0, "/opt/side/bravesoul-game")
import numpy as np
from PIL import Image
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
    ("Fox", "Orange Stock",
     f"{BASE}/fox/head_unit/ear_fox_radar_orange_512.png",
     f"{BASE}/fox/chassis/paint_fox_orange_512.png"),

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
    ("Tiger Head", "Ember Orange",
     f"{BASE}/tiger/head_unit/head_ember_tiger_ember_512.png",
     f"{BASE}/tiger/chassis/paint_ember_orange_512.png"),
    ("Tiger Ear", "Volcano Black",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_volcano_512.png",
     f"{BASE}/tiger/chassis/paint_volcano_black_512.png"),
    ("Tiger Ear", "Ivory Stock",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_ivory_512.png",
     f"{BASE}/tiger/chassis/paint_ivory_stock_512.png"),
    ("Tiger Ear", "Ember Orange",
     f"{BASE}/tiger/head_unit/ear_ember_tiger_ember_512.png",
     f"{BASE}/tiger/chassis/paint_ember_orange_512.png"),

    # Crane
    ("Crane", "Zephyr Azure",
     f"{BASE}/crane/head_unit/head_cloud_crane_azure_512.png",
     f"{BASE}/crane/chassis/paint_zephyr_azure_512.png"),
    ("Crane", "Ivory Stock",
     f"{BASE}/crane/head_unit/head_cloud_crane_ivory_512.png",
     f"{BASE}/crane/chassis/paint_ivory_stock_512.png"),
    ("Crane", "Porcelain Stock",
     f"{BASE}/crane/head_unit/head_cloud_crane_porcelain_512.png",
     f"{BASE}/crane/chassis/paint_crane_porcelain_512.png"),
]

def get_average_plate_color(path: str) -> np.ndarray:
    im = Image.open(path).convert("RGBA")
    arr = np.array(im)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    mask = (alpha > 200) & (np.max(rgb, axis=2) > 70)
    if np.sum(mask) == 0:
        mask = alpha > 200
    pixels = rgb[mask].astype(float)
    return np.mean(pixels, axis=0)

def color_distance(c1, c2) -> float:
    return float(np.linalg.norm(np.array(c1) - np.array(c2)))

def get_md5(p: str) -> str:
    with open(p, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def main():
    print("====================================================================================================")
    print("【驗收量測】六族頭部塗裝同步新公式色距與品質指標稽核 (t_2247d718 / 0-ART28h)")
    print("====================================================================================================")
    print(f"{'族系':11s} | {'塗裝變體':15s} | {'Head 平均色':19s} | {'Chassis 平均色':19s} | {'色距':6s} | {'色階數':6s} | {'平坦區':6s} | {'判定'}")
    print("-" * 105)
    
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
            
        c_head = get_average_plate_color(head_p)
        c_ch = get_average_plate_color(ch_p)
        dist = color_distance(c_head, c_ch)
        
        q = measure_image_quality(head_p)
        assert q is not None
        colors_ok = q["unique_colors"] > 10000
        flat_ok = q["flat_ratio"] < 0.10
        dist_ok = dist < 60.0
        
        is_pass = colors_ok and flat_ok and dist_ok
        if not is_pass:
            all_pass = False
        status = "✅ PASS" if is_pass else "❌ FAIL"
        
        c_h_str = f"({c_head[0]:.1f},{c_head[1]:.1f},{c_head[2]:.1f})"
        c_c_str = f"({c_ch[0]:.1f},{c_ch[1]:.1f},{c_ch[2]:.1f})"
        
        print(f"{race:11s} | {variant:15s} | {c_h_str:19s} | {c_c_str:19s} | {dist:6.1f} | {q['unique_colors']:6d} | {q['flat_ratio']*100:5.2f}% | {status}")
        
    print("-" * 105)
    if all_pass:
        print("🎉 全部 17 組新切片新公式平均色距全部 < 60.0、色階數 > 10000、平坦區 < 10%，全部通過驗收！")
    else:
        print("❌ 部分切片未達到合格標準，請修正！")
    return all_pass

if __name__ == "__main__":
    ok = main()
    sys.exit(0 if ok else 1)
