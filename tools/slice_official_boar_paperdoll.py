#!/usr/bin/env python3
"""
tools/slice_official_boar_paperdoll.py
Slices the flawless official master web/media/hero/char_boar.png (928x1160)
into 7 modular MapleStory Character.wz paperdoll parts in 512 coordinate space.
"""

import os
import json
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from collections import deque

REPO_ROOT = "/opt/side/bravesoul-game"
HERO_BOAR = f"{REPO_ROOT}/web/media/hero/char_boar.png"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"
PARTS_DIR = f"{BOAR_DIR}/maple_parts"
JSON_PATH = f"{REPO_ROOT}/game/data/tables/maple_paperdoll_boar.json"

for sub in ["body", "head_unit", "eyes", "costume", "weapon", "winding_key", "back_curio"]:
    os.makedirs(f"{PARTS_DIR}/{sub}", exist_ok=True)

# 1. 泛洪去背
raw_im = Image.open(HERO_BOAR).convert("RGBA")
arr = np.array(raw_im)
h, w, _ = arr.shape

visited = np.zeros((h, w), dtype=bool)
bg_mask = np.zeros((h, w), dtype=bool)

def is_bg(r, g, b):
    if r > 215 and g > 210 and b > 195:
        if abs(int(r) - int(g)) < 22 and abs(int(g) - int(b)) < 22:
            return True
    if r > 235 and g > 235 and b > 235:
        return True
    return False

queue = deque()
for x in range(w):
    for y in [0, 1, 2, 3, h-1, h-2, h-3]:
        r, g, b, a = arr[y, x]
        if is_bg(r, g, b):
            queue.append((x, y))
            visited[y, x] = True

for y in range(h):
    for x in [0, 1, 2, 3, w-1, w-2, w-3]:
        if not visited[y, x]:
            r, g, b, a = arr[y, x]
            if is_bg(r, g, b):
                queue.append((x, y))
                visited[y, x] = True

while queue:
    cx, cy = queue.popleft()
    bg_mask[cy, cx] = True
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
            visited[ny, nx] = True
            r, g, b, a = arr[ny, nx]
            if is_bg(r, g, b):
                queue.append((nx, ny))

arr[bg_mask, 3] = 0
master = Image.fromarray(arr, mode="RGBA")

# 縮放到 512 畫布基準
# 928x1160 縮小約 0.44 倍 -> 408 x 510，置中於 (256, 480) 腳底對齊
SCALE = 500.0 / 1160.0 # 0.4310
new_w = int(w * SCALE) # 400
new_h = int(h * SCALE) # 500

scaled_master = master.resize((new_w, new_h), Image.Resampling.LANCZOS)
canvas_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
OFFSET_X = (512 - new_w) // 2 # 56
OFFSET_Y = 512 - new_h - 4   # 8
canvas_512.alpha_composite(scaled_master, (OFFSET_X, OFFSET_Y))
canvas_512.save("/tmp/clean_master_512.png")
print("Saved /tmp/clean_master_512.png, bbox:", canvas_512.getbbox())

# -----------------------------------------------------------------------------
# 2. 裁切 7 大模組化切片
# -----------------------------------------------------------------------------
c_arr = np.array(canvas_512)

# 1. WINDING KEY (背部鑰匙)
# 在 512 中大約位於 x: 335..455, y: 55..180
key_layer = np.zeros_like(c_arr)
for y in range(50, 185):
    for x in range(330, 460):
        r, g, b, a = c_arr[y, x]
        if a > 20:
            # 判斷金色發條鑰匙
            if (int(r) > 130 and int(g) > 85 and int(b) < 80) or (int(r) > 180 and int(g) > 140):
                if x > 335 and y < 165:
                    key_layer[y, x] = [r, g, b, a]

im_key = Image.fromarray(key_layer, mode="RGBA")
k_bbox = im_key.getbbox()
if not k_bbox:
    k_bbox = (335, 55, 455, 175)
crop_k = im_key.crop(k_bbox)
crop_k.save(f"{PARTS_DIR}/winding_key/key_classic_brass.png")
# back_key 錨點: (360, 140) -> Origin: (360 - k_bbox[0], 140 - k_bbox[1])
k_origin = [360 - k_bbox[0], 140 - k_bbox[1]]
print("Winding key:", crop_k.size, "Origin:", k_origin)

# 2. HEAD UNIT (頭部：面具、獠牙、耳朵、角盔，Y <= 176)
head_layer = np.zeros_like(c_arr)
for y in range(20, 177):
    for x in range(120, 400):
        r, g, b, a = c_arr[y, x]
        if a > 20 and key_layer[y, x, 3] == 0:
            head_layer[y, x] = [r, g, b, a]

im_head = Image.fromarray(head_layer, mode="RGBA")
h_bbox = im_head.getbbox()
if not h_bbox:
    h_bbox = (120, 20, 400, 177)
crop_h = im_head.crop(h_bbox)

# 去眼窩發光像素
arr_h = np.array(crop_h)
for y in range(len(arr_h)):
    for x in range(len(arr_h[0])):
        r, g, b, a = arr_h[y, x]
        # 眼睛在 crop_h 中的位置
        if (int(g) > int(r) + 15 and int(g) > 90) or (int(g) > 115 and int(b) > 115 and int(r) < 135):
            arr_h[y, x] = [28, 24, 34, 255]

clean_head_brass = Image.fromarray(arr_h, mode="RGBA")
clean_head_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl_brass.png")
clean_head_brass.save(f"{PARTS_DIR}/head_unit/ear_boar_rivet_cowl.png")

# 生成象牙與赤焰變體
arr_hb = np.array(clean_head_brass)
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

# Neck: (250, 176) -> Origin: (250 - h_bbox[0], 176 - h_bbox[1])
h_origin = [250 - h_bbox[0], 176 - h_bbox[1]]
print("Head unit:", clean_head_brass.size, "Origin:", h_origin)

# 3. WEAPON (戰錘)
weapon_layer = np.zeros_like(c_arr)
for y in range(250, 512):
    for x in range(50, 240):
        r, g, b, a = c_arr[y, x]
        if a > 20:
            # 戰錘石頭與木柄
            is_hammer_head = (y >= 320 and x <= 180)
            is_shaft = (y >= 250 and y < 340 and x >= 150 and x <= 220)
            is_ground_shadow = (y >= 480 and x <= 220)
            if is_hammer_head or is_shaft or is_ground_shadow:
                weapon_layer[y, x] = [r, g, b, a]

im_w = Image.fromarray(weapon_layer, mode="RGBA")
w_bbox = im_w.getbbox()
if not w_bbox:
    w_bbox = (50, 250, 240, 512)
crop_w = im_w.crop(w_bbox)
crop_w.save(f"{PARTS_DIR}/weapon/wpn_anvil_greathammer.png")
# Hand: (180, 340) -> Origin: (180 - w_bbox[0], 340 - w_bbox[1])
w_origin = [180 - w_bbox[0], 340 - w_bbox[1]]
print("Weapon:", crop_w.size, "Origin:", w_origin)

# 4. EYES (獨立光學義眼)
w_e, h_e = 90, 60
cx, cy = 45, 30
eye_cyan = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
dc = ImageDraw.Draw(eye_cyan)
dc.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(20, 18, 25, 255), outline=(130, 105, 50, 255), width=2)
dc.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(12, 85, 95, 255))
dc.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(25, 175, 185, 255))
dc.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(55, 240, 230, 255))
dc.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(10, 38, 42, 255))
dc.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
dc.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(210, 255, 255, 220))
eye_cyan.save(f"{PARTS_DIR}/eyes/eyes_cyan_emerald.png")

eye_amber = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
da = ImageDraw.Draw(eye_amber)
da.ellipse([cx - 15, cy - 14, cx + 15, cy + 14], fill=(26, 15, 10, 255), outline=(165, 90, 25, 255), width=2)
da.ellipse([cx - 13, cy - 12, cx + 13, cy + 12], fill=(125, 40, 10, 255))
da.ellipse([cx - 11, cy - 10, cx + 11, cy + 10], fill=(220, 110, 18, 255))
da.ellipse([cx - 8, cy - 7, cx + 8, cy + 7], fill=(255, 190, 40, 255))
da.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(48, 18, 8, 255))
da.ellipse([cx + 2, cy - 5, cx + 6, cy - 1], fill=(255, 255, 255, 255))
da.ellipse([cx - 4, cy + 1, cx - 2, cy + 3], fill=(255, 230, 170, 220))
eye_amber.save(f"{PARTS_DIR}/eyes/eyes_amber_gold.png")

eye_blink = Image.new("RGBA", (w_e, h_e), (0, 0, 0, 0))
db = ImageDraw.Draw(eye_blink)
db.arc([cx - 15, cy - 11, cx + 15, cy + 11], start=10, end=170, fill=(35, 25, 45, 255), width=4)
db.line([(cx - 14, cy), (cx + 14, cy)], fill=(25, 20, 35, 255), width=3)
db.line([(cx - 11, cy - 1), (cx + 11, cy - 1)], fill=(245, 205, 55, 240), width=1)
eye_blink.save(f"{PARTS_DIR}/eyes/eyes_blink.png")
eye_origin = [45, 30]

# 5. COSTUMES (Harness & Ironclad)
# 束帶：在 512 中大約位於 x: 180..340, y: 250..420
cos_layer = np.zeros_like(c_arr)
for y in range(250, 420):
    for x in range(180, 340):
        r, g, b, a = c_arr[y, x]
        if a > 20 and weapon_layer[y, x, 3] == 0:
            # 扣除核心中央，留下金邊束帶
            d = math.hypot(x - 230, y - 306)
            if d < 22: continue
            cos_layer[y, x] = [r, g, b, a]

im_cos = Image.fromarray(cos_layer, mode="RGBA")
cos_bbox = im_cos.getbbox()
if not cos_bbox:
    cos_bbox = (180, 250, 340, 420)
crop_cos_harn = im_cos.crop(cos_bbox)
crop_cos_harn.save(f"{PARTS_DIR}/costume/costume_viking_harness.png")

# Ironclad
crop_cos_iron = crop_cos_harn.copy()
draw_ir = ImageDraw.Draw(crop_cos_iron)
draw_ir.rounded_rectangle([15, 18, crop_cos_iron.width - 15, crop_cos_iron.height - 18], radius=16, fill=(45, 58, 80, 245), outline=(22, 28, 40, 255), width=3)
# 挖出核心
mask_i = Image.new("L", crop_cos_iron.size, 0)
dw = ImageDraw.Draw(mask_i)
# 核心在 crop 內的相對位置: (230 - cos_bbox[0], 306 - cos_bbox[1])
core_rel_x = 230 - cos_bbox[0]
core_rel_y = 306 - cos_bbox[1]
dw.ellipse([core_rel_x - 22, core_rel_y - 22, core_rel_x + 22, core_rel_y + 22], fill=255)
arr_ir = np.array(crop_cos_iron)
arr_ir[np.array(mask_i) > 0, 3] = 0
crop_cos_iron = Image.fromarray(arr_ir, mode="RGBA")
draw_ir = ImageDraw.Draw(crop_cos_iron)
draw_ir.ellipse([core_rel_x - 23, core_rel_y - 23, core_rel_x + 23, core_rel_y + 23], outline=(245, 205, 55, 255), width=3)
crop_cos_iron.save(f"{PARTS_DIR}/costume/costume_viking_ironclad.png")

# Navel: (256, 340) -> Origin: (256 - cos_bbox[0], 340 - cos_bbox[1])
cos_origin = [256 - cos_bbox[0], 340 - cos_bbox[1]]
print("Costume:", crop_cos_harn.size, "Origin:", cos_origin)

# 6. TAIL
raw_tail = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
tail_512 = raw_tail.resize((512, 512), Image.Resampling.NEAREST)
c_tail = tail_512.crop((340, 320, 436, 408))
c_tail.save(f"{PARTS_DIR}/back_curio/curio_spring_tail.png")
tail_origin = [10, 15]

# 7. BODY CHASSIS (純淨金屬底盤，在 512 畫布中 (0, 0))
# 直接使用去除頭部、武器、鑰匙後的完整身軀底盤，確保 100% 0 洞口、0 穿模！
body_layer = c_arr.copy()
# 扣除頭部與鑰匙
body_layer[head_layer[:, :, 3] > 0] = [0, 0, 0, 0]
body_layer[key_layer[:, :, 3] > 0] = [0, 0, 0, 0]

body_brass = Image.fromarray(body_layer, mode="RGBA")
body_brass.save(f"{PARTS_DIR}/body/paint_brass_gold.png")

# Ivory
arr_bb = np.array(body_brass)
arr_bi = arr_bb.copy()
for y in range(512):
    for x in range(512):
        if arr_bi[y, x, 3] > 0 and math.hypot(x - 230, y - 306) > 24:
            r, g, b = arr_bi[y, x, :3]
            lum = int(0.299 * r + 0.587 * g + 0.114 * b)
            arr_bi[y, x, :3] = [min(255, lum + 15), min(255, lum + 15), min(255, lum + 20)]
Image.fromarray(arr_bi, mode="RGBA").save(f"{PARTS_DIR}/body/paint_ivory_stock.png")

# Crimson
arr_bc = arr_bb.copy()
for y in range(512):
    for x in range(512):
        if arr_bc[y, x, 3] > 0:
            r, g, b = arr_bc[y, x, :3]
            if math.hypot(x - 230, y - 306) <= 24:
                lum = (int(r) + int(g) + int(b)) / 3.0
                arr_bc[y, x, :3] = [min(255, int(lum * 1.35 + 35)), min(255, int(lum * 0.70 + 10)), min(255, int(lum * 0.15))]
            else:
                arr_bc[y, x, :3] = [min(255, int(r * 1.25 + 20)), int(g * 0.70), int(b * 0.70)]
Image.fromarray(arr_bc, mode="RGBA").save(f"{PARTS_DIR}/body/paint_molten_crimson.png")
print("Body:", body_brass.size, "Origin: [0, 0]")

# 8. UPDATE JSON SPEC
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
                    "width": clean_head_brass.width,
                    "height": clean_head_brass.height,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl_ivory": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_ivory.png",
                    "width": clean_head_brass.width,
                    "height": clean_head_brass.height,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl_crimson": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl_crimson.png",
                    "width": clean_head_brass.width,
                    "height": clean_head_brass.height,
                    "origin": h_origin
                },
                "ear_boar_rivet_cowl": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/head_unit/ear_boar_rivet_cowl.png",
                    "width": clean_head_brass.width,
                    "height": clean_head_brass.height,
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
                    "width": crop_cos_harn.width,
                    "height": crop_cos_harn.height,
                    "origin": cos_origin
                },
                "costume_viking_ironclad": {
                    "path": "res://assets/sprites/player/paperdoll/boar/maple_parts/costume/costume_viking_ironclad.png",
                    "width": crop_cos_iron.width,
                    "height": crop_cos_iron.height,
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
                    "width": crop_w.width,
                    "height": crop_w.height,
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
                    "width": crop_k.width,
                    "height": crop_k.height,
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
print("✓ Saved JSON spec")
print("🎉 Official ultra-HD Boar sliced successfully!")
