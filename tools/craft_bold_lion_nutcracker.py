#!/usr/bin/env python3
"""
tools/craft_bold_lion_nutcracker.py
Bold, high-readability Nutcracker Guard uniform for Lion (512x512):
- Bold red double-breasted chest bib across X: 206..294 (width ~88px).
- 6 large, prominent 3D golden buttons (radius 7px) with braided frogging cords.
- Rich royal navy uniform coat flanks (X: 168..212 on left, X: 288..332 on right).
- Prominent golden crescent epaulets with fringe on both shoulders.
- High-visibility golden officer's belt with rectangular buckle.
- Direct composite and visual inspection.
"""

import math
import subprocess
import numpy as np
from PIL import Image, ImageDraw

REPO_ROOT = "/opt/side/bravesoul-game"
LION_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion"
WORK_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_84698e86"

# Load fresh HEAD image
out = subprocess.check_output(["git", "show", "HEAD:game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard_512.png"], cwd=REPO_ROOT)
with open("/tmp/fresh_head_lion2.png", "wb") as f:
    f.write(out)

base_im = Image.open("/tmp/fresh_head_lion2.png").convert("RGBA")
base_arr = np.array(base_im, dtype=np.float32)

canvas = base_arr.copy()

def clamp(v, low=0.0, high=255.0):
    return float(max(low, min(high, v)))

def put_px(x, y, rgb, alpha=1.0):
    if 0 <= x < 512 and 0 <= y < 512 and alpha > 0.0:
        c = np.array(rgb, dtype=np.float32)
        cur_a = canvas[y, x, 3] / 255.0
        new_a = alpha + cur_a * (1.0 - alpha)
        if new_a > 0:
            canvas[y, x, :3] = (c[:3] * alpha + canvas[y, x, :3] * cur_a * (1.0 - alpha)) / new_a
            canvas[y, x, 3] = new_a * 255.0

OUTLINE = np.array([31, 26, 58, 255], dtype=np.float32)

# High-contrast Nutcracker colors
C_NAVY_DARK = np.array([20.0, 30.0, 56.0])
C_NAVY_MID = np.array([35.0, 52.0, 96.0])
C_NAVY_LIGHT = np.array([55.0, 80.0, 142.0])

C_RED_DARK = np.array([125.0, 18.0, 28.0])
C_RED_MID = np.array([192.0, 32.0, 46.0])
C_RED_LIGHT = np.array([238.0, 60.0, 76.0])

C_GOLD_DARK = np.array([125.0, 78.0, 16.0])
C_GOLD_MID = np.array([232.0, 175.0, 34.0])
C_GOLD_LIGHT = np.array([255.0, 225.0, 60.0])
C_GOLD_SPEC = np.array([255.0, 255.0, 200.0])

C_WHITE = np.array([250.0, 248.0, 255.0])

# 1. Fill Torso Navy Uniform & Red Double-Breasted Bib (Y: 272..366)
for y in range(272, 366):
    t_y = (y - 272) / 94.0
    x_min = int(172 - 8.0 * math.sin(t_y * math.pi))
    x_max = int(328 + 6.0 * math.sin(t_y * math.pi))
    
    # Neckline curve: Y=288 at center X=250, curving up to Y=272 at X=190 and X=310
    dx_neck = (x_min + x_max) / 2.0
    
    for x in range(x_min, x_max + 1):
        dx = (x - 250.0) / 60.0
        neck_y = 288.0 - 18.0 * min(1.0, dx * dx)
        if y < neck_y:
            continue
            
        is_edge = (x == x_min or x == x_max or abs(y - neck_y) <= 1.5)
        if is_edge:
            put_px(x, y, OUTLINE[:3])
            continue
            
        # Red plastron bounds: X: 210..290
        bib_left = int(212 - 4.0 * t_y)
        bib_right = int(288 + 4.0 * t_y)
        
        if bib_left <= x <= bib_right:
            # White piping braid on left and right
            if x in (bib_left, bib_left + 1, bib_right - 1, bib_right) or abs(y - neck_y) <= 2.5:
                put_px(x, y, C_WHITE)
            else:
                # Saturated Nutcracker scarlet red
                dist_center = abs(x - 250) / 40.0
                dot = 1.0 - dist_center * 0.35
                c = C_RED_MID * dot + C_RED_LIGHT * (1.0 - dot)
                if abs(x - 250) <= 6:
                    c = C_RED_LIGHT
                put_px(x, y, c)
        else:
            # Royal navy uniform fabric
            dist_center = abs(x - 250) / 75.0
            c = C_NAVY_MID if x < 250 else C_NAVY_DARK
            if abs(x - x_min) <= 4:
                c = C_NAVY_LIGHT
            put_px(x, y, c)

# 2. 6 Bold Spherical 3D Golden Buttons (X: 228 and X: 272, Y: 304, 324, 344)
def draw_bold_button(bx, by, rad=7.0):
    for dy in range(-int(rad) - 1, int(rad) + 2):
        for dx in range(-int(rad) - 1, int(rad) + 2):
            d = math.sqrt(dx * dx + dy * dy)
            if d <= rad:
                nx, ny = dx / rad, dy / rad
                dot = -(nx * -0.65 + ny * -0.65)
                if math.sqrt((dx + 2.0)**2 + (dy + 2.0)**2) <= 2.5:
                    c = C_GOLD_SPEC
                elif dot > 0.2:
                    c = C_GOLD_LIGHT
                elif dot > -0.3:
                    c = C_GOLD_MID
                else:
                    c = C_GOLD_DARK
                put_px(bx + dx, by + dy, c)
            elif d <= rad + 1.2:
                put_px(bx + dx, by + dy, OUTLINE[:3], 0.8)

for y_btn in [304, 324, 344]:
    # Braided gold horizontal cord
    for x in range(212, 238):
        put_px(x, y_btn - 1, C_GOLD_LIGHT)
        put_px(x, y_btn, C_GOLD_MID)
        put_px(x, y_btn + 1, C_GOLD_DARK)
    for x in range(262, 288):
        put_px(x, y_btn - 1, C_GOLD_LIGHT)
        put_px(x, y_btn, C_GOLD_MID)
        put_px(x, y_btn + 1, C_GOLD_DARK)
    draw_bold_button(228, y_btn, rad=7.0)
    draw_bold_button(272, y_btn, rad=7.0)

# 3. Bold Gold Epaulets on Shoulders
# Left Shoulder: X: 130..190, Y: 248..285
for y in range(248, 280):
    for x in range(130, 192):
        dx = (x - 160.0) / 28.0
        dy = (y - 263.0) / 14.0
        dist = dx*dx + dy*dy
        if dist <= 1.0:
            if dist >= 0.84 or y == 248:
                put_px(x, y, OUTLINE[:3])
            else:
                dot = -(dx * -0.65 + dy * -0.7)
                c = C_GOLD_SPEC if dot > 0.5 else (C_GOLD_LIGHT if dot > 0.0 else C_GOLD_MID)
                put_px(x, y, c)
# Left tassels
for tx in range(134, 190, 5):
    for fy in range(276, 298):
        if fy == 297:
            put_px(tx, fy, OUTLINE[:3], 0.8)
        else:
            put_px(tx, fy, C_GOLD_MID if fy > 288 else C_GOLD_LIGHT)
            put_px(tx + 1, fy, C_GOLD_DARK)

# Right Shoulder: X: 308..368, Y: 248..285
for y in range(248, 280):
    for x in range(308, 370):
        dx = (x - 340.0) / 28.0
        dy = (y - 263.0) / 14.0
        dist = dx*dx + dy*dy
        if dist <= 1.0:
            if dist >= 0.84 or y == 248:
                put_px(x, y, OUTLINE[:3])
            else:
                dot = -(dx * -0.65 + dy * -0.7)
                c = C_GOLD_SPEC if dot > 0.5 else (C_GOLD_LIGHT if dot > 0.0 else C_GOLD_MID)
                put_px(x, y, c)
# Right tassels
for tx in range(312, 368, 5):
    for fy in range(276, 298):
        if fy == 297:
            put_px(tx, fy, OUTLINE[:3], 0.8)
        else:
            put_px(tx, fy, C_GOLD_MID if fy > 288 else C_GOLD_LIGHT)
            put_px(tx + 1, fy, C_GOLD_DARK)

# 4. Bold Gold Officer's Belt (Y: 356..368, X: 190..318)
for y in range(356, 369):
    for x in range(190, 319):
        if y in (356, 368) or x in (190, 318):
            put_px(x, y, OUTLINE[:3])
        elif y in (357, 358):
            put_px(x, y, C_GOLD_LIGHT)
        elif y in (366, 367):
            put_px(x, y, C_GOLD_DARK)
        else:
            put_px(x, y, C_GOLD_MID)

# Belt buckle (X: 234..266, Y: 352..372)
for y in range(352, 373):
    for x in range(234, 267):
        is_border = (x in (234, 235, 265, 266) or y in (352, 353, 371, 372))
        if is_border:
            put_px(x, y, OUTLINE[:3])
        elif x in (236, 237, 263, 264) or y in (354, 355, 369, 370):
            put_px(x, y, C_GOLD_SPEC if y <= 355 else C_GOLD_MID)
        else:
            put_px(x, y, C_NAVY_DARK)

dst_path = f"{LION_DIR}/costume/costume_nutcracker_guard_512.png"
res = Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))
res.save(dst_path)
print("✓ Saved bold lion nutcracker to:", dst_path)
print("  Bbox:", res.getbbox())
