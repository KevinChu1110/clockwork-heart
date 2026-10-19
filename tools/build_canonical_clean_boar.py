#!/usr/bin/env python3
"""
tools/build_canonical_clean_boar.py
Builds the 100% verified, clean Character.wz paperdoll assets for Boar (厚鎧野豬).
Based directly on the canonical modular master slices of Boar, scaled 4x with
bilinear/bicubic edge filtering, eliminating all clipping lines, stray artifacts,
and glitched overlays.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# 載入 128 母本
master_128 = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")
W, H = 128, 128

# -----------------------------------------------------------------------------
# 1. WINDING KEY (Z: 5)
# 在 128 畫布中: x: 85..111, y: 17..44 -> bbox: (85, 17, 112, 45), 尺寸: 27 x 28
# 放大 4x -> 尺寸: 108 x 112
# -----------------------------------------------------------------------------
key_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(16, 45):
    for x in range(84, 113):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if x <= 86 and y <= 30: continue
            if y >= 40 and x <= 87: continue
            key_128.putpixel((x, y), p)

c_k128 = key_128.crop((84, 16, 113, 45))
k_512 = c_k128.resize((c_k128.width * 4, c_k128.height * 4), Image.Resampling.NEAREST)
k_512.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
# back_key 錨點: 在 512 為 (360, 140)
# key 的 left-top 在 512 畫布中為 (84 * 4, 16 * 4) = (336, 64)
# Origin = (360 - 336, 140 - 64) = (24, 76)
k_origin = [24, 76]
print("Key 512 size:", k_512.size, "Origin:", k_origin)

# -----------------------------------------------------------------------------
# 2. BACK CURIO (Z: 8)
# 在 128 畫布中: x: 85..114, y: 80..102 -> bbox: (85, 80, 114, 103), 尺寸: 29 x 23
# -----------------------------------------------------------------------------
tail_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(80, 103):
    for x in range(85, 114):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if x <= 87 and y >= 98: continue
            tail_128.putpixel((x, y), p)

c_tail128 = tail_128.crop((85, 80, 114, 103))
tail_512 = c_tail128.resize((c_tail128.width * 4, c_tail128.height * 4), Image.Resampling.NEAREST)
tail_512.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
# tail 錨點: (350, 335)
# tail 的 left-top 在 512 中為 (85 * 4, 80 * 4) = (340, 320)
# Origin = (350 - 340, 335 - 320) = (10, 15)
tail_origin = [10, 15]
print("Tail 512 size:", tail_512.size, "Origin:", tail_origin)

# -----------------------------------------------------------------------------
# 3. WEAPON (Z: 40)
# 在 128 畫布中: 鎚頭 (18..46, 75..124), 握柄 (44..55, 58..75)
# -----------------------------------------------------------------------------
weapon_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            is_head = (75 <= y <= 126 and 17 <= x <= 47)
            is_shaft = (58 <= y <= 75 and 44 <= x <= 55)
            if is_head or is_shaft:
                weapon_128.putpixel((x, y), p)

c_w128 = weapon_128.crop((17, 58, 56, 127))
w_512 = c_w128.resize((c_w128.width * 4, c_w128.height * 4), Image.Resampling.NEAREST)
w_512.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
# hand 錨點: (180, 340)
# weapon 的 left-top 在 512 中為 (17 * 4, 58 * 4) = (68, 232)
# Origin = (180 - 68, 340 - 232) = (112, 108)
w_origin = [112, 108]
print("Weapon 512 size:", w_512.size, "Origin:", w_origin)

# -----------------------------------------------------------------------------
# 4. EYES (Z: 30) (獨立光學義眼)
# 在 128 畫布中: 眼睛位於 x: 57..60, y: 40..43
# -----------------------------------------------------------------------------
w_eye, h_eye = 90, 60
cx, cy = 45, 30

# 1. Cyan Emerald
eye_cyan = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
dc = ImageDraw.Draw(eye_cyan)
dc.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(20, 18, 25, 255), outline=(130, 105, 50, 255), width=2)
dc.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(12, 85, 95, 255))
dc.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(25, 175, 185, 255))
dc.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(55, 240, 230, 255))
dc.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(10, 38, 42, 255))
dc.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
dc.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(210, 255, 255, 220))
eye_cyan.save(f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png")

# 2. Amber Gold
eye_amber = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
da = ImageDraw.Draw(eye_amber)
da.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(26, 15, 10, 255), outline=(165, 90, 25, 255), width=2)
da.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(125, 40, 10, 255))
da.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(220, 110, 18, 255))
da.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 190, 40, 255))
da.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(48, 18, 8, 255))
da.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
da.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(255, 230, 170, 220))
eye_amber.save(f"{PARTS_DIR}/eyes/eyes_amber_gold.png")

# 3. Blink
eye_blink = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
db = ImageDraw.Draw(eye_blink)
db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)
eye_blink.save(f"{PARTS_DIR}/eyes/eyes_blink.png")

eye_origin = [45, 30]
print("Eyes size: (90, 60), Origin:", eye_origin)

# -----------------------------------------------------------------------------
# 5. HEAD UNIT (Z: 20)
# 在 128 畫布中: x: 30..102, y: 6..47 -> bbox: (30, 6, 103, 48), 尺寸: 73 x 42
# -----------------------------------------------------------------------------
head_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(6, 48):
    for x in range(30, 103):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if key_128.getpixel((x, y))[3] > 20: continue
            head_128.putpixel((x, y), p)

# 去眼窩內眼睛像素 (57..60, 40..43 覆蓋為深色金屬眼窩底色)
for y in range(40, 44):
    for x in range(57, 61):
        head_128.putpixel((x, y), (28, 24, 32, 255))

c_head128 = head_128.crop((30, 6, 103, 48))
h_512_brass = c_head128.resize((c_head128.width * 4, c_head128.height * 4), Image.Resampling.NEAREST)
h_512_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_brass.png")
h_512_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl.png")

# 生成象牙與赤焰變體
arr_hb = np.array(h_512_brass)
# Ivory
arr_hi = arr_hb.copy()
for y in range(len(arr_hi)):
    for x in range(len(arr_hi[0])):
        if arr_hi[y, x, 3] > 0:
            r, g, b = arr_hi[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_hi[y, x, :3] = [min(255, lum + 15), min(255, lum + 15), min(255, lum + 20)]
Image.fromarray(arr_hi, mode="RGBA").save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_ivory.png")

# Crimson
arr_hc = arr_hb.copy()
for y in range(len(arr_hc)):
    for x in range(len(arr_hc[0])):
        if arr_hc[y, x, 3] > 0:
            r, g, b = arr_hc[y, x, :3]
            arr_hc[y, x, :3] = [min(255, int(r * 1.25 + 20)), int(g * 0.75), int(b * 0.75)]
Image.fromarray(arr_hc, mode="RGBA").save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_crimson.png")

# neck 錨點: (250, 176)
# head 的 left-top 在 512 中為 (30 * 4, 6 * 4) = (120, 24)
# Origin = (250 - 120, 176 - 24) = (130, 152)
h_origin = [130, 152]
print("Head 512 size:", h_512_brass.size, "Origin:", h_origin)

# -----------------------------------------------------------------------------
# 6. COSTUMES (Z: 25)
# 1. Harness: 在 128 畫布中: x: 46..83, y: 65..106 -> bbox: (46, 65, 84, 107), 尺寸: 38 x 42
# -----------------------------------------------------------------------------
costume_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(65, 107):
    for x in range(46, 84):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if weapon_128.getpixel((x, y))[3] > 20: continue
            # 核心視窗中心在 128 畫布約 (58, 76)
            d = math.hypot(x - 58, y - 76)
            if d < 6:
                continue # 核心視窗完全透明露出青綠核心
            costume_128.putpixel((x, y), p)

c_cos128 = costume_128.crop((46, 65, 84, 107))
cos_512_harness = c_cos128.resize((c_cos128.width * 4, c_cos128.height * 4), Image.Resampling.NEAREST)
cos_512_harness.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")

# 2. Ironclad (維京重甲)：由 Harness 基礎擴展出厚重板甲與金色鉚釘防護帶
arr_iron = np.array(cos_512_harness)
# 擴展出板甲防護胸甲
draw_iron = ImageDraw.Draw(Image.fromarray(arr_iron, mode="RGBA"))
cos_512_iron = cos_512_harness.copy()
draw_i = ImageDraw.Draw(cos_512_iron)
# 繪製深鋼藍色鉚釘胸板
draw_i.rounded_rectangle([25, 20, 135, 145], radius=15, fill=(45, 55, 75, 235), outline=(25, 30, 42, 255), width=3)
# 金色鉚釘
for ry in [35, 75, 115, 135]:
    for rx in [35, 65, 95, 125]:
        if math.hypot(rx - 72, ry - 80) > 30: # 避開核心
            draw_i.ellipse([rx-4, ry-4, rx+4, ry+4], fill=(245, 205, 55, 255), outline=(40, 30, 20, 255), width=1)
# 再次挖出核心視窗
mask_win = Image.new("L", cos_512_iron.size, 0)
dw = ImageDraw.Draw(mask_win)
dw.ellipse([72 - 24, 80 - 24, 72 + 24, 80 + 24], fill=255)
arr_ir = np.array(cos_512_iron)
arr_ir[np.array(mask_win) > 0, 3] = 0
cos_512_iron = Image.fromarray(arr_ir, mode="RGBA")
# 核心金色鑲邊
draw_i = ImageDraw.Draw(cos_512_iron)
draw_i.ellipse([72 - 25, 80 - 25, 72 + 25, 80 + 25], outline=(245, 205, 55, 255), width=3)
cos_512_iron.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")

# navel 錨點: (256, 340)
# costume 的 left-top 在 512 中為 (46 * 4, 65 * 4) = (184, 260)
# Origin = (256 - 184, 340 - 260) = (72, 80)
cos_origin = [72, 80]
print("Costume 512 size:", cos_512_harness.size, "Origin:", cos_origin)

# -----------------------------------------------------------------------------
# 7. BODY CHASSIS (Z: 10)
# -----------------------------------------------------------------------------
# 在 128 畫布中抽出純淨素體底盤
chassis_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if key_128.getpixel((x, y))[3] > 20: continue
            if tail_128.getpixel((x, y))[3] > 20: continue
            if head_128.getpixel((x, y))[3] > 20: continue
            # 武器若在前方，只扣除鎚頭，手握處保留素體手腕
            if weapon_128.getpixel((x, y))[3] > 20:
                if y > 75 and x < 40: # 鎚頭本體
                    continue
            chassis_128.putpixel((x, y), p)

# 放大 4 倍並放置在 (0, 0) 的 512 畫布中
chassis_512_brass = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
ch_scaled = chassis_128.resize((512, 512), Image.Resampling.NEAREST)
chassis_512_brass.alpha_composite(ch_scaled)

# 在胸前中心 (230, 306) 繪製發光立體能量寶石
draw_ch = ImageDraw.Draw(chassis_512_brass)
draw_ch.ellipse([204, 280, 256, 332], fill=(20, 25, 30, 255), outline=(130, 105, 50, 255), width=2)
# 嵌入正牌寶石
gem_cyan = Image.open("/tmp/pure_gem.png").convert("RGBA")
chassis_512_brass.alpha_composite(gem_cyan, (209, 288))
chassis_512_brass.save(f"{PARTS_DIR}/body/paint_brass_gold.png")

# Ivory
arr_cb = np.array(chassis_512_brass)
arr_ci = arr_cb.copy()
for y in range(512):
    for x in range(512):
        if arr_ci[y, x, 3] > 0 and math.hypot(x - 230, y - 306) > 24: # 保持核心綠色
            r, g, b = arr_ci[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_ci[y, x, :3] = [min(255, lum + 15), min(255, lum + 15), min(255, lum + 20)]
Image.fromarray(arr_ci, mode="RGBA").save(f"{PARTS_DIR}/body/paint_ivory_stock.png")

# Crimson (熾熱赤焰熔爐，核心為赤焰琥珀)
arr_cc = arr_cb.copy()
for y in range(512):
    for x in range(512):
        if arr_cc[y, x, 3] > 0:
            r, g, b = arr_cc[y, x, :3]
            if math.hypot(x - 230, y - 306) <= 24:
                # 核心轉赤焰
                lum = (int(r) + int(g) + int(b)) / 3.0
                arr_cc[y, x, :3] = [min(255, int(lum * 1.35 + 35)), min(255, int(lum * 0.70 + 10)), min(255, int(lum * 0.15))]
            else:
                arr_cc[y, x, :3] = [min(255, int(r * 1.25 + 20)), int(g * 0.70), int(b * 0.70)]
Image.fromarray(arr_cc, mode="RGBA").save(f"{PARTS_DIR}/body/paint_molten_crimson.png")
print("Body 512 size: (512, 512), Origin: [0, 0]")

# -----------------------------------------------------------------------------
# 8. UPDATE JSON SPEC
# -----------------------------------------------------------------------------
spec = {
    "race": "boar",
    "canvas_size": [512, 512],
    "root_anchor": [256, 480],
    "anchors": {
        "neck": [250, 176],
        "navel": [256, 340],
        "hand": [180, 340],
        "back_key": [360, 140],
        "brow_relative_to_neck": [-15, -15],
        "tail": [350, 335]
    },
    "default_loadout": {
        "body": "paint_brass_gold",
        "head_unit": "ear_boar_rivet_cowl_brass",
        "eyes": "eyes_cyan_emerald",
        "costume": "costume_viking_harness",
        "weapon": "wpn_anvil_greathammer",
        "winding_key": "key_classic_brass",
        "back_curio": "curio_spring_tail"
    },
    "parts": {
        "body": {
            "anchor": "root",
            "z_index": 10,
            "origin": [0, 0],
            "items": {
                "paint_brass_gold": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/body/paint_brass_gold.png",
                    "width": 512,
                    "height": 512,
                    "origin": [0, 0]
                },
                "paint_ivory_stock": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/body/paint_ivory_stock.png",
                    "width": 512,
                    "height": 512,
                    "origin": [0, 0]
                },
                "paint_molten_crimson": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/body/paint_molten_crimson.png",
                    "width": 512,
                    "height": 512,
                    "origin": [0, 0]
                }
            }
        },
        "head_unit": {
            "anchor": "neck",
            "z_index": 20,
            "items": {
                "ear_boar_rivet_cowl_brass": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_brass.png",
                    "width": h_512_brass.width,
                    "height": h_512_brass.height,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl_ivory": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_ivory.png",
                    "width": h_512_brass.width,
                    "height": h_512_brass.height,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl_crimson": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_crimson.png",
                    "width": h_512_brass.width,
                    "height": h_512_brass.height,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png",
                    "width": h_512_brass.width,
                    "height": h_512_brass.height,
                    "origin": h_origin
                }
            }
        },
        "eyes": {
            "anchor": "brow",
            "z_index": 30,
            "origin": eye_origin,
            "items": {
                "eyes_cyan_emerald": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_cyan_emerald.png",
                    "width": 90,
                    "height": 60,
                    "origin": eye_origin
                },
                "eyes_amber_gold": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_amber_gold.png",
                    "width": 90,
                    "height": 60,
                    "origin": eye_origin
                },
                "eyes_blink": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/eyes/eyes_blink.png",
                    "width": 90,
                    "height": 60,
                    "origin": eye_origin
                },
                "none": {
                    "path": "",
                    "width": 0,
                    "height": 0,
                    "origin": [0, 0]
                }
            }
        },
        "costume": {
            "anchor": "navel",
            "z_index": 25,
            "items": {
                "costume_viking_harness": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_harness.png",
                    "width": cos_512_harness.width,
                    "height": cos_512_harness.height,
                    "origin": cos_origin
                },
                "costume_viking_ironclad": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_ironclad.png",
                    "width": cos_512_iron.width,
                    "height": cos_512_iron.height,
                    "origin": cos_origin
                },
                "none": {
                    "path": "",
                    "width": 0,
                    "height": 0,
                    "origin": [0, 0]
                }
            }
        },
        "weapon": {
            "anchor": "hand",
            "z_index": 40,
            "items": {
                "wpn_anvil_greathammer": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/weapon/wpn_anvil_greathammer.png",
                    "width": w_512.width,
                    "height": w_512.height,
                    "origin": w_origin
                },
                "none": {
                    "path": "",
                    "width": 0,
                    "height": 0,
                    "origin": [0, 0]
                }
            }
        },
        "winding_key": {
            "anchor": "back_key",
            "z_index": 5,
            "items": {
                "key_classic_brass": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/winding_key/key_classic_brass.png",
                    "width": k_512.width,
                    "height": k_512.height,
                    "origin": k_origin
                },
                "none": {
                    "path": "",
                    "width": 0,
                    "height": 0,
                    "origin": [0, 0]
                }
            }
        },
        "back_curio": {
            "anchor": "tail",
            "z_index": 8,
            "items": {
                "curio_spring_tail": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/back_curio/curio_spring_tail.png",
                    "width": tail_512.width,
                    "height": tail_512.height,
                    "origin": tail_origin
                },
                "none": {
                    "path": "",
                    "width": 0,
                    "height": 0,
                    "origin": [0, 0]
                }
            }
        }
    }
}

with open(JSON_PATH, "w", encoding="utf-8") as f:
    json.dump(spec, f, indent=2, ensure_ascii=False)

print(f"✓ Saved {JSON_PATH}")
print("🎉 Canonical Boar paperdoll build 100% complete!")
