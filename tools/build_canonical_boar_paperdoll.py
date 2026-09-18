#!/usr/bin/env python3
import os, hashlib
from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"
BOAR = f"{REPO}/game/assets/sprites/player/paperdoll/boar"
CHASSIS_DIR = f"{BOAR}/chassis"
HEAD_DIR = f"{BOAR}/head_unit"

# Load aligned HD master (512x512)
hd = Image.open(f"{REPO}/proofs/debug_hd_in_512.png").convert("RGBA")
arr_hd = np.array(hd)

# 1. Base Head Unit: Y <= 176, exclude winding key at x > 360, y < 110
head_mask = (arr_hd[:, :, 3] > 30) & (np.arange(512)[:, None] <= 176) & \
            ~((np.arange(512)[:, None] < 110) & (np.arange(512)[None, :] > 360))

head_base = np.zeros_like(arr_hd)
head_base[head_mask] = arr_hd[head_mask]

# Smooth feathering along bottom Y=176
for x in range(512):
    if head_base[176, x, 3] > 0:
        head_base[176, x, 3] = int(round(head_base[176, x, 3] * 0.80))

# 2. Base Chassis: Y >= 170, clear tusk at x < 137 for y in [165..275]
ch_mask = (arr_hd[:, :, 3] > 10) & (np.arange(512)[:, None] >= 170)
tusk_mask = (np.arange(512)[:, None] >= 165) & (np.arange(512)[:, None] <= 275) & (np.arange(512)[None, :] < 137)
ch_mask = ch_mask & (~tusk_mask)

chassis_base = np.zeros_like(arr_hd)
chassis_base[ch_mask] = arr_hd[ch_mask]

# Smooth tusk boundary along x=137 for Y in [175..265]
for y in range(175, 266):
    if chassis_base[y, 137, 3] > 0 and chassis_base[y, 136, 3] == 0:
        chassis_base[y, 137, 3] = int(round(chassis_base[y, 137, 3] * 0.70))
    if chassis_base[y, 138, 3] > 0 and chassis_base[y, 137, 3] < 100:
        chassis_base[y, 138, 3] = int(round(chassis_base[y, 138, 3] * 0.85))

# Target variants and their palette mappings
VARIANTS = {
    "brass": {
        "head_name": "ear_boar_rivet_cowl_brass",
        "chassis_name": "paint_brass_gold",
        "h_tint": (1.0, 0.95, 0.80),
        "c_tint": (1.0, 0.95, 0.80),
    },
    "crimson": {
        "head_name": "ear_boar_rivet_cowl_crimson",
        "chassis_name": "paint_molten_crimson",
        "h_tint": (1.10, 0.65, 0.52),
        "c_tint": (1.10, 0.65, 0.52),
    },
    "ivory": {
        "head_name": "ear_boar_rivet_cowl_ivory",
        "chassis_name": "paint_ivory_stock",
        "h_tint": (1.20, 1.15, 1.10),
        "c_tint": (1.20, 1.15, 1.10),
    },
}

def apply_tint(arr, tint, is_ivory=False):
    out = arr.copy()
    valid = out[:, :, 3] > 20
    px = out[valid, :3].astype(float)
    if is_ivory:
        # Desaturate slightly and brighten
        lum = 0.299 * px[:, 0] + 0.587 * px[:, 1] + 0.114 * px[:, 2]
        for c in range(3):
            px[:, c] = np.clip(lum * 0.6 + px[:, c] * 0.4, 0, 255)
            px[:, c] = np.clip(px[:, c] * tint[c], 0, 215) # cap at 215 so zero pure white
    else:
        for c in range(3):
            px[:, c] = np.clip(px[:, c] * tint[c], 0, 255)
    out[valid, :3] = px.astype(np.uint8)
    return out

def build_assets():
    print("=== Building Canonical Boar Paperdoll Assets ===")
    
    # 1. Base stock head
    h_stock_512 = Image.fromarray(head_base, "RGBA")
    h_stock_512.save(f"{HEAD_DIR}/ear_boar_rivet_cowl_512.png")
    h_stock_128 = h_stock_512.resize((128, 128), Image.Resampling.LANCZOS)
    arr_h128 = np.array(h_stock_128)
    arr_h128[0, 0] = [0, 0, 0, 0]
    arr_h128[0, 127] = [0, 0, 0, 0]
    arr_h128[127, 0] = [0, 0, 0, 0]
    arr_h128[127, 127] = [0, 0, 0, 0]
    Image.fromarray(arr_h128, "RGBA").save(f"{HEAD_DIR}/ear_boar_rivet_cowl.png")
    print("✓ Saved base ear_boar_rivet_cowl 512 and 128")

    for key, v in VARIANTS.items():
        is_iv = (key == "ivory")
        
        # Head
        h_arr = apply_tint(head_base, v["h_tint"], is_iv)
        im_h_512 = Image.fromarray(h_arr, "RGBA")
        im_h_512.save(f"{HEAD_DIR}/{v['head_name']}_512.png")
        
        im_h_128 = im_h_512.resize((128, 128), Image.Resampling.LANCZOS)
        arr_128 = np.array(im_h_128)
        arr_128[0, 0] = [0, 0, 0, 0]
        arr_128[0, 127] = [0, 0, 0, 0]
        arr_128[127, 0] = [0, 0, 0, 0]
        arr_128[127, 127] = [0, 0, 0, 0]
        Image.fromarray(arr_128, "RGBA").save(f"{HEAD_DIR}/{v['head_name']}.png")
        
        # Chassis
        c_arr = apply_tint(chassis_base, v["c_tint"], is_iv)
        im_c_512 = Image.fromarray(c_arr, "RGBA")
        im_c_512.save(f"{CHASSIS_DIR}/{v['chassis_name']}_512.png")
        
        im_c_128 = im_c_512.resize((128, 128), Image.Resampling.LANCZOS)
        arr_c128 = np.array(im_c_128)
        arr_c128[0, 0] = [0, 0, 0, 0]
        arr_c128[0, 127] = [0, 0, 0, 0]
        arr_c128[127, 0] = [0, 0, 0, 0]
        arr_c128[127, 127] = [0, 0, 0, 0]
        Image.fromarray(arr_c128, "RGBA").save(f"{CHASSIS_DIR}/{v['chassis_name']}.png")
        
        print(f"✓ Saved {key}: {v['head_name']} & {v['chassis_name']} (512 & 128)")

if __name__ == "__main__":
    build_assets()
