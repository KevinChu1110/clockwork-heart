#!/usr/bin/env python3
"""
tools/build_true_modular_boar.py
Builds the 100% clean, modular Character.wz paperdoll slices for Boar:
1. Slices master_128 into 7 modular parts: key, tail, chassis, head, costume, eyes, weapon.
2. Removes selection marching ants from head.
3. Scales them 4x into pristine 512 coordinate space with exact origins.
4. Generates 3 body paints, 4 head variants, 3 eyes, 2 costumes, weapon, key, and tail.
5. Updates maple_paperdoll_boar.json.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

master_128 = Image.open(f"{BOAR_DIR}/proof_paperdoll_boar_composite.png").convert("RGBA")
W, H = 128, 128

# 1. WINDING KEY (Z: 5)
key_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(16, 45):
    for x in range(84, 113):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if x <= 86 and y <= 30: continue
            if y >= 40 and x <= 87: continue
            key_128.putpixel((x, y), p)

# 2. BACK CURIO (Z: 8)
tail_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(80, 103):
    for x in range(85, 114):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if x <= 87 and y >= 98: continue
            tail_128.putpixel((x, y), p)

# 3. WEAPON (Z: 40)
weapon_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            is_head = (75 <= y <= 126 and 17 <= x <= 47)
            is_shaft = (58 <= y <= 75 and 44 <= x <= 55)
            if is_head or is_shaft:
                weapon_128.putpixel((x, y), p)

# 4. HEAD UNIT (Z: 20)
head_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(6, 48):
    for x in range(30, 103):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if key_128.getpixel((x, y))[3] > 20: continue
            head_128.putpixel((x, y), p)

# 修復頭部上的螞蟻線噪點 (將白點黑點替換為金屬底色)
arr_h128 = np.array(head_128)
for y in range(H):
    for x in range(W):
        r, g, b, a = arr_h128[y, x]
        if a > 50:
            # 判斷是否為黑白交替的螞蟻線點 (非常亮或非常暗的孤立噪點)
            if (r > 210 and g > 210 and b > 210) or (r < 25 and g < 25 and b < 25 and 30 <= x <= 80 and 8 <= y <= 35):
                # 替換為相鄰深藍金屬色
                arr_h128[y, x] = [45, 58, 80, 255]

head_128 = Image.fromarray(arr_h128, mode="RGBA")
# 去眼窩內眼睛 (57..60, 40..43)
for y in range(40, 44):
    for x in range(57, 61):
        head_128.putpixel((x, y), (28, 24, 32, 255))

# 5. COSTUME (Z: 25)
costume_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(65, 107):
    for x in range(46, 84):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if weapon_128.getpixel((x, y))[3] > 20: continue
            d = math.hypot(x - 58, y - 76)
            if d < 6:
                continue # 核心視窗
            costume_128.putpixel((x, y), p)

# 6. CHASSIS (Z: 10) (真正的純淨金屬底盤，扣除所有外裝、武器、鑰匙！)
chassis_128 = Image.new('RGBA', (W, H), (0, 0, 0, 0))
for y in range(H):
    for x in range(W):
        p = master_128.getpixel((x, y))
        if p[3] > 20:
            if key_128.getpixel((x, y))[3] > 20: continue
            if tail_128.getpixel((x, y))[3] > 20: continue
            if head_128.getpixel((x, y))[3] > 20: continue
            if weapon_128.getpixel((x, y))[3] > 20: continue
            if costume_128.getpixel((x, y))[3] > 20: continue
            chassis_128.putpixel((x, y), p)

# 補齊素體在 costume 與 weapon 背後的底盤金屬 (避免裸機時空洞)
for y in range(65, 107):
    for x in range(44, 84):
        p = master_128.getpixel((x, y))
        if p[3] > 20 and chassis_128.getpixel((x, y))[3] == 0:
            # 填補金屬底盤色
            chassis_128.putpixel((x, y), (55, 65, 82, 255))

# 在素體胸口中央 (58, 76) 繪製發光青綠能量寶石
draw_ch128 = ImageDraw.Draw(chassis_128)
draw_ch128.ellipse([54, 72, 62, 80], fill=(20, 180, 190, 255), outline=(140, 105, 50, 255), width=1)
draw_ch128.ellipse([56, 74, 60, 78], fill=(60, 245, 235, 255))
draw_ch128.point((57, 74), fill=(255, 255, 255, 255))

# -----------------------------------------------------------------------------
# 產生 512 緊湊切片
# -----------------------------------------------------------------------------
# 1. Key
c_k128 = key_128.crop((84, 16, 113, 45))
k_512 = c_k128.resize((c_k128.width * 4, c_k128.height * 4), Image.Resampling.NEAREST)
k_512.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
k_origin = [24, 76]

# 2. Tail
c_tail128 = tail_128.crop((85, 80, 114, 103))
tail_512 = c_tail128.resize((c_tail128.width * 4, c_tail128.height * 4), Image.Resampling.NEAREST)
tail_512.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
tail_origin = [10, 15]

# 3. Weapon
c_w128 = weapon_128.crop((17, 58, 56, 127))
w_512 = c_w128.resize((c_w128.width * 4, c_w128.height * 4), Image.Resampling.NEAREST)
w_512.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
w_origin = [112, 108]

# 4. Eyes
w_eye, h_eye = 90, 60
cx, cy = 45, 30
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

eye_blink = Image.new("RGBA", (w_eye, h_eye), (0, 0, 0, 0))
db = ImageDraw.Draw(eye_blink)
db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)
eye_blink.save(f"{PARTS_DIR}/eyes/eyes_blink.png")
eye_origin = [45, 30]

# 5. Head Unit
c_head128 = head_128.crop((30, 6, 103, 48))
h_512_brass = c_head128.resize((c_head128.width * 4, c_head128.height * 4), Image.Resampling.NEAREST)
h_512_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_brass.png")
h_512_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl.png")

arr_hb = np.array(h_512_brass)
arr_hi = arr_hb.copy()
for y in range(len(arr_hi)):
    for x in range(len(arr_hi[0])):
        if arr_hi[y, x, 3] > 0:
            r, g, b = arr_hi[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_hi[y, x, :3] = [min(255, lum + 15), min(255, lum + 15), min(255, lum + 20)]
Image.fromarray(arr_hi, mode="RGBA").save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_ivory.png")

arr_hc = arr_hb.copy()
for y in range(len(arr_hc)):
    for x in range(len(arr_hc[0])):
        if arr_hc[y, x, 3] > 0:
            r, g, b = arr_hc[y, x, :3]
            arr_hc[y, x, :3] = [min(255, int(r * 1.25 + 20)), int(g * 0.75), int(b * 0.75)]
Image.fromarray(arr_hc, mode="RGBA").save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_crimson.png")
h_origin = [130, 152]

# 6. Costumes
c_cos128 = costume_128.crop((46, 65, 84, 107))
cos_512_harness = c_cos128.resize((c_cos128.width * 4, c_cos128.height * 4), Image.Resampling.NEAREST)
# 金邊
draw_cos_h = ImageDraw.Draw(cos_512_harness)
draw_cos_h.ellipse([46 - 22, 46 - 22, 46 + 22, 46 + 22], outline=(245, 205, 55, 255), width=2)
cos_512_harness.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")

# Ironclad
cos_512_iron = cos_512_harness.copy()
draw_i = ImageDraw.Draw(cos_512_iron)
draw_i.rounded_rectangle([15, 18, 137, 150], radius=15, fill=(45, 55, 75, 245), outline=(22, 28, 40, 255), width=3)
for ry in [34, 110, 140]:
    for rx in [30, 60, 90, 120]:
        if math.hypot(rx - 48, ry - 46) > 26:
            draw_i.ellipse([rx-3, ry-3, rx+3, ry+3], fill=(245, 205, 55, 255), outline=(30, 24, 15, 255), width=1)
# 挖空核心視窗
mask_i = Image.new("L", cos_512_iron.size, 0)
dw = ImageDraw.Draw(mask_i)
dw.ellipse([48 - 22, 46 - 22, 48 + 22, 46 + 22], fill=255)
arr_ir = np.array(cos_512_iron)
arr_ir[np.array(mask_i) > 0, 3] = 0
cos_512_iron = Image.fromarray(arr_ir, mode="RGBA")
draw_i = ImageDraw.Draw(cos_512_iron)
draw_i.ellipse([48 - 23, 46 - 23, 48 + 23, 46 + 23], outline=(245, 205, 55, 255), width=3)
cos_512_iron.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")
cos_origin = [72, 80]

# 7. Body Chassis (純淨金屬底盤，無任何武器與外裝，0-ART18 合規)
chassis_512 = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
ch_scaled = chassis_128.resize((512, 512), Image.Resampling.NEAREST)
chassis_512.alpha_composite(ch_scaled)
chassis_512.save(f"{PARTS_DIR}/body/paint_brass_gold.png")

# Ivory
arr_cb = np.array(chassis_512)
arr_ci = arr_cb.copy()
for y in range(512):
    for x in range(512):
        if arr_ci[y, x, 3] > 0 and math.hypot(x - 232, y - 304) > 24:
            r, g, b = arr_ci[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_ci[y, x, :3] = [min(255, lum + 15), min(255, lum + 15), min(255, lum + 20)]
Image.fromarray(arr_ci, mode="RGBA").save(f"{PARTS_DIR}/body/paint_ivory_stock.png")

# Crimson
arr_cc = arr_cb.copy()
for y in range(512):
    for x in range(512):
        if arr_cc[y, x, 3] > 0:
            r, g, b = arr_cc[y, x, :3]
            if math.hypot(x - 232, y - 304) <= 24:
                lum = (int(r) + int(g) + int(b)) / 3.0
                arr_cc[y, x, :3] = [min(255, int(lum * 1.35 + 35)), min(255, int(lum * 0.70 + 10)), min(255, int(lum * 0.15))]
            else:
                arr_cc[y, x, :3] = [min(255, int(r * 1.25 + 20)), int(g * 0.70), int(b * 0.70)]
Image.fromarray(arr_cc, mode="RGBA").save(f"{PARTS_DIR}/body/paint_molten_crimson.png")

# 8. SPEC JSON
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
print("🎉 True modular Boar system successfully built!")
