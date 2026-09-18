#!/usr/bin/env python3
"""
tools/measure_costume_final_metrics.py
Measures exact bounding boxes and dimensions for:
- Lion: Bare chassis, Original nutcracker, Fixed nutcracker, Artisan ref
- Penguin: Bare chassis, Original navigator, Fixed navigator, Abyssal ref
"""

from PIL import Image
import numpy as np

REPO = "/opt/side/bravesoul-game"

def get_nz_bbox(path):
    im = Image.open(path)
    a = np.array(im.split()[-1])
    nz = np.nonzero(a > 10)
    if len(nz[0]) == 0:
        return None
    ymin, ymax = int(nz[0].min()), int(nz[0].max())
    xmin, xmax = int(nz[1].min()), int(nz[1].max())
    w = xmax - xmin + 1
    h = ymax - ymin + 1
    return (xmin, ymin, xmax, ymax), (w, h)

# 1. Lion
p_lion_ch = f"{REPO}/game/assets/sprites/player/paperdoll/lion/chassis/paint_brass_gold_512.png"
p_lion_fixed = f"{REPO}/game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard_512.png"
p_lion_artisan = f"{REPO}/game/assets/sprites/player/paperdoll/lion/costume/costume_steam_artisan_512.png"

# 2. Penguin
p_pen_ch = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/chassis/paint_penguin_navy_512.png"
p_pen_fixed = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/costume/costume_navigator_harness_512.png"
p_pen_abyssal = f"{REPO}/game/assets/sprites/player/paperdoll/penguin/costume/costume_abyssal_diver_cuirass_512.png"

print("=== LION ASSETS ===")
print("Bare Chassis :", get_nz_bbox(p_lion_ch))
print("Fixed Costume:", get_nz_bbox(p_lion_fixed))
print("Artisan Ref  :", get_nz_bbox(p_lion_artisan))

print("\n=== PENGUIN ASSETS ===")
print("Bare Chassis :", get_nz_bbox(p_pen_ch))
print("Fixed Costume:", get_nz_bbox(p_pen_fixed))
print("Abyssal Ref  :", get_nz_bbox(p_pen_abyssal))

# Specific width comparison at different Y levels for Penguin
im_ch = Image.open(p_pen_ch)
im_c = Image.open(p_pen_fixed)
a_ch = np.array(im_ch.split()[-1]) > 10
a_c = np.array(im_c.split()[-1]) > 10

print("\n=== PENGUIN WIDTH COMPARISON PER ROW ===")
for y in [175, 185, 200, 228, 260, 300, 350, 380, 400, 412]:
    row_ch = np.nonzero(a_ch[y, :])[0]
    row_c = np.nonzero(a_c[y, :])[0]
    w_ch = (row_ch.max() - row_ch.min() + 1) if len(row_ch) else 0
    w_c = (row_c.max() - row_c.min() + 1) if len(row_c) else 0
    x_ch_str = f"[{row_ch.min()},{row_ch.max()}]" if len(row_ch) else "none"
    x_c_str = f"[{row_c.min()},{row_c.max()}]" if len(row_c) else "none"
    print(f"y={y:3d} | Bare Chassis: w={w_ch:3d} {x_ch_str:12s} | Fixed Greatcoat: w={w_c:3d} {x_c_str:12s} | Delta W={w_c - w_ch:+3d}")
