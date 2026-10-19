#!/usr/bin/env python3
"""
tools/apply_flawless_fixes.py
Applies the final flawless polish:
1. Embeds the authentic 3D glowing Cyan/Crimson energy gem into pure bodies.
2. 100% cleans key_classic_brass to eradicate any off-white / grey rectangular halos.
3. Smoothly eliminates the vertical straight line on the warhammer shadow.
4. Perfectly aligns costume windows so the cyan gem shines through flawlessly.
"""

import math
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"

# 1. 取得真實立體發光翡翠綠寶石
gem_cyan = Image.open("/tmp/pure_gem.png").convert("RGBA")
gw, gh = gem_cyan.size # 42, 37

# 製作赤焰熔爐寶石
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

# 2. 嵌入素體 (center at (230, 306) -> pos: (230 - 21, 306 - 18) = (209, 288))
gem_pos = (209, 288)

paints = [
    ("paint_brass_gold", gem_cyan, (140, 105, 45)),
    ("paint_ivory_stock", gem_cyan, (90, 85, 95)),
    ("paint_molten_crimson", gem_crimson, (140, 60, 40))
]

for p_name, gem_img, bg_col in paints:
    ch = Image.open(f"{BOAR_DIR}/chassis/{p_name}_512.png").convert("RGBA")
    arr = np.array(ch)
    
    # 清理胸前 (200..260, 275..337)
    for y in range(265, 345):
        for x in range(180, 270):
            d = math.hypot(x - 230, y - 306)
            if d < 28:
                arr[y, x] = [bg_col[0] // 3, bg_col[1] // 3, bg_col[2] // 3, 255]

    cleaned_ch = Image.fromarray(arr, mode="RGBA")
    draw = ImageDraw.Draw(cleaned_ch)
    # 底座金屬環
    draw.ellipse([204, 283, 256, 329], fill=(22, 18, 16, 255), outline=(bg_col[0], bg_col[1], bg_col[2], 255), width=2)
    cleaned_ch.alpha_composite(gem_img, gem_pos)
    
    cleaned_ch.save(f"{PARTS_DIR}/body/{p_name}.png")
    print(f"  ✓ Flawless body saved: {p_name}")

# 3. 外裝 Costume (確保視窗完美露出寶石，無黑底)
# Harness (origin=[72, 80], pos=(184, 260) -> 核心中心在 costume 內為 (230-184, 306-260) = (46, 46))
raw_h = Image.open(f"{BOAR_DIR}/costume/costume_viking_harness_512.png").convert("RGBA")
arr_h = np.array(raw_h)
for y in range(len(arr_h)):
    for x in range(len(arr_h[0])):
        r, g, b, a = arr_h[y, x]
        if (int(r) > 130 and int(g) < 150 and int(b) < 90 and 170 <= x <= 245 and 240 <= y <= 330):
            arr_h[y, x] = [0, 0, 0, 0]
            continue
        d = math.hypot(x - 230, y - 306)
        if d < 24:
            arr_h[y, x] = [0, 0, 0, 0] # 完全透明以露出底盤能量寶石！

clean_h = Image.fromarray(arr_h, mode="RGBA").crop((184, 260, 332, 424))
clean_h.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")
print("  ✓ Flawless costume harness saved")

# Ironclad
raw_i = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png").convert("RGBA")
arr_i = np.array(raw_i)
for y in range(len(arr_i)):
    for x in range(len(arr_i[0])):
        if x > 335 and y < 215:
            d_sh = math.hypot(x - 330, y - 215)
            if d_sh > 46:
                arr_i[y, x] = [0, 0, 0, 0]
                continue
        d = math.hypot(x - 230, y - 306)
        if d < 24:
            arr_i[y, x] = [0, 0, 0, 0] # 核心視窗露出寶石

clean_i = Image.fromarray(arr_i, mode="RGBA").crop((192, 180, 372, 384))
clean_i.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
print("  ✓ Flawless costume ironclad saved")

# 4. 戰錘：徹底清除右下角垂直切線
raw_w = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png").convert("RGBA")
arr_w = np.array(raw_w)
for y in range(460, 512):
    for x in range(60, 236):
        if arr_w[y, x, 3] > 0:
            if x < 85 and y > 495:
                arr_w[y, x, 3] = 0
            elif x < 95 and y > 500:
                arr_w[y, x, 3] = int(arr_w[y, x, 3] * 0.4)
            # 右側地面陰影：在 x > 195 處以自然圓弧半徑衰減到 0，絕對無垂直切線！
            if x > 190 and y > 465:
                dist = math.hypot(x - 190, y - 485)
                fade = max(0.0, 1.0 - dist / 22.0)
                arr_w[y, x, 3] = int(arr_w[y, x, 3] * fade)

cleaned_w = Image.fromarray(arr_w, mode="RGBA").crop((60, 260, 236, 512))
cleaned_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
print("  ✓ Flawless warhammer saved")

# 5. 發條鑰匙：徹底消除任何白色/灰白色暈邊
raw_k = Image.open(f"{PARTS_DIR}/winding_key/key_classic_brass.png").convert("RGBA")
arr_k = np.array(raw_k)
for y in range(len(arr_k)):
    for x in range(len(arr_k[0])):
        r, g, b, a = arr_k[y, x]
        if a > 0:
            # 任何接近純白、米白或灰色 (R>180, G>180, B>175) 均為去背殘留，直接清除
            if r > 180 and g > 180 and b > 170:
                arr_k[y, x] = [0, 0, 0, 0]
            elif a < 40:
                arr_k[y, x] = [0, 0, 0, 0]

cleaned_k = Image.fromarray(arr_k, mode="RGBA")
cleaned_k.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
print("  ✓ Flawless winding key saved")

print("🎉 All flawless fixes applied successfully!")
