#!/usr/bin/env python3
"""
tools/heal_all_boar_seams.py
Heals all clipping seams and transparent holes:
1. Slices Head with full chin/snout extension down to Y=210 so mouth/jaw is 100% complete with 0 holes.
2. Ensures Body has a 100% solid, fully painted torso and arm background behind the hammer (no vertical slits).
3. Smoothly anchors Head at Neck (250, 176) and Weapon at Hand (180, 340).
"""

import json
import math
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

# 載入原始未破壞的 512 身體原圖
# 在 raw_chassis_512 中，野豬的整個身軀是完整連續的！
ch_raw = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold_512.png").convert("RGBA")
head_raw = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png").convert("RGBA")
weapon_raw = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")

# -----------------------------------------------------------------------------
# 1. HEAD UNIT: 完整下巴與下顎 (Y 從 35 到 215)
# -----------------------------------------------------------------------------
print("--- 1. Healing Head Unit (Full Chin & Jaw) ---")
# 寬度 130..400 (270 px), 高度 35..215 (180 px)
# Neck 錨點: (250, 176) -> Origin: (250 - 130, 176 - 35) = (120, 141)
crop_head_box = (130, 35, 400, 215)
h_origin = [250 - 130, 176 - 35]

variants = [
    ("ear_boar_rivet_cowl_brass", "ear_boar_rivet_cowl_brass_512.png"),
    ("ear_boar_rivet_cowl_ivory", "ear_boar_rivet_cowl_ivory_512.png"),
    ("ear_boar_rivet_cowl_crimson", "ear_boar_rivet_cowl_crimson_512.png"),
    ("ear_boar_rivet_cowl", "ear_boar_rivet_cowl_512.png")
]

for out_name, src_file in variants:
    p = f"{BOAR_DIR}/head_unit/{src_file}"
    im = Image.open(p).convert("RGBA")
    arr = np.array(im)
    
    # 平滑去眼窩發光像素 (226..252, 145..172)
    for y in range(145, 173):
        for x in range(226, 253):
            r, g, b, a = arr[y, x]
            if (int(g) > int(r) + 15 and int(g) > 90) or (int(g) > 115 and int(b) > 115 and int(r) < 135):
                arr[y, x] = [28, 24, 34, 255]

    clean_h = Image.fromarray(arr, mode="RGBA").crop(crop_head_box)
    clean_h.save(f"{PARTS_DIR}/head_unit/{out_name}.png")
    print(f"  ✓ Saved {out_name}.png: size={clean_h.size}, origin={h_origin}")

# -----------------------------------------------------------------------------
# 2. BODY CHASSIS: 100% 飽滿無縫金屬底盤，無任何垂直穿透縫隙
# -----------------------------------------------------------------------------
print("--- 2. Healing Pure Bodies (Solid Seamless Chassis) ---")
gem_cyan = Image.open("/tmp/pure_gem.png").convert("RGBA")
gw, gh = gem_cyan.size

arr_c = np.array(gem_cyan)
arr_a = arr_c.copy()
for y in range(gh):
    for x in range(gw):
        r, g, b, a = arr_c[y, x]
        if a > 0:
            lum = (int(r) + int(g) + int(b)) / 3.0
            arr_a[y, x] = [
                min(255, int(lum * 1.35 + 35)),
                min(255, int(lum * 0.70 + 10)),
                min(255, int(lum * 0.15)),
                a
            ]
gem_crimson = Image.fromarray(arr_a, mode="RGBA")
gem_pos = (209, 288)

paints = [
    ("paint_brass_gold", gem_cyan, (140, 105, 45)),
    ("paint_ivory_stock", gem_cyan, (90, 85, 95)),
    ("paint_molten_crimson", gem_crimson, (140, 60, 40))
]

for p_name, gem_img, bg_col in paints:
    ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
    arr = np.array(ch)
    
    # 清理胸前核心區域
    for y in range(265, 345):
        for x in range(180, 270):
            d = math.hypot(x - 230, y - 306)
            if d < 28:
                arr[y, x] = [bg_col[0] // 3, bg_col[1] // 3, bg_col[2] // 3, 255]

    # 填補下巴下顎與頸部交接處 (x: 180..270, y: 170..215)，確保 100% 實心無透明空洞
    for y in range(170, 215):
        for x in range(180, 275):
            if arr[y, x, 3] == 0:
                arr[y, x] = [bg_col[0] // 2, bg_col[1] // 2, bg_col[2] // 2, 255]

    # 填補戰錘後方手臂軀幹 (x: 150..225, y: 300..450)，確保 100% 實心無垂直穿透縫
    for y in range(300, 450):
        for x in range(150, 225):
            if arr[y, x, 3] < 50:
                arr[y, x] = [bg_col[0] // 2, bg_col[1] // 2, bg_col[2] // 2, 255]

    cleaned_ch = Image.fromarray(arr, mode="RGBA")
    draw = ImageDraw.Draw(cleaned_ch)
    draw.ellipse([204, 282, 256, 330], fill=(20, 18, 16, 255), outline=bg_col, width=2)
    cleaned_ch.alpha_composite(gem_img, gem_pos)
    
    cleaned_ch.save(f"{PARTS_DIR}/body/{p_name}.png")
    print(f"  ✓ Saved {p_name}.png")

# -----------------------------------------------------------------------------
# 3. WEAPON: 裁切寬度向右延伸到 235，完美包含整個握柄與手部
# -----------------------------------------------------------------------------
print("--- 3. Healing Weapon Slices ---")
# 原本只裁到 215，現在完整裁切到 235: (63, 270, 235, 502) -> 尺寸 (172, 232)
# Hand: (180, 340) -> Origin: (180 - 63, 340 - 270) = (117, 70)
arr_w = np.array(weapon_raw)
for y in range(len(arr_w)):
    for x in range(len(arr_w[0])):
        if y > 495 and x > 195:
            arr_w[y, x] = [0, 0, 0, 0]

clean_w = Image.fromarray(arr_w, mode="RGBA").crop((63, 270, 235, 502))
clean_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
w_origin = [117, 70]
print(f"  ✓ Saved wpn_anvil_greathammer.png: size={clean_w.size}, origin={w_origin}")

# -----------------------------------------------------------------------------
# 4. JSON SPEC UPDATE
# -----------------------------------------------------------------------------
with open(JSON_PATH, "r", encoding="utf-8") as f:
    spec = json.load(f)

# 更新 head 與 weapon 的規格尺寸與 origin
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_brass"]["width"] = clean_h.width
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_brass"]["height"] = clean_h.height
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_brass"]["origin"] = h_origin

spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_ivory"]["width"] = clean_h.width
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_ivory"]["height"] = clean_h.height
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_ivory"]["origin"] = h_origin

spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_crimson"]["width"] = clean_h.width
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_crimson"]["height"] = clean_h.height
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl_crimson"]["origin"] = h_origin

spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl"]["width"] = clean_h.width
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl"]["height"] = clean_h.height
spec["parts"]["head_unit"]["items"]["ear_boar_rivet_cowl"]["origin"] = h_origin

spec["parts"]["weapon"]["items"]["wpn_anvil_greathammer"]["width"] = clean_w.width
spec["parts"]["weapon"]["items"]["wpn_anvil_greathammer"]["height"] = clean_w.height
spec["parts"]["weapon"]["items"]["wpn_anvil_greathammer"]["origin"] = w_origin

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)
print("✓ JSON updated")
