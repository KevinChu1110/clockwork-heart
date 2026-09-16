#!/usr/bin/env python3
"""
tools/build_repaired_tiger_chassis.py
High-fidelity visual restoration of the 3 Tiger chassis variants.
"""

from typing import cast
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
CHASSIS_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tiger/chassis"

OUTLINE = (31, 26, 58, 255) # Standard crisp dark outline #1F1A3A

def repair_ember_orange(src_path: str, dst_path: str):
    img = Image.open(src_path).convert("RGBA")
    arr = np.array(img)

    # 1. Clean shadow axis / crosshair pixels at (64, 116) and (64, 124)
    arr[116, 64] = [0, 0, 0, 0]
    arr[124, 64] = [0, 0, 0, 0]

    # 2. Upper chest neck collar 3D metallic restoration (Y=48..53, X=57..71)
    collar_palette = {
        48: {
            57: OUTLINE, 58: (95, 48, 30, 255), 59: (140, 75, 38, 255),
            60: (185, 110, 50, 255), 61: (220, 150, 75, 255), 62: (245, 190, 105, 255),
            63: (252, 215, 135, 255), 64: (255, 225, 150, 255), 65: (252, 215, 135, 255),
            66: (240, 185, 100, 255), 67: (215, 140, 70, 255), 68: (175, 100, 48, 255),
            69: (135, 70, 36, 255), 70: (90, 45, 28, 255), 71: OUTLINE
        },
        49: {
            57: OUTLINE, 58: (75, 38, 32, 255), 59: (120, 62, 35, 255),
            60: (170, 95, 45, 255), 61: (215, 140, 68, 255), 62: (242, 180, 95, 255),
            63: (250, 205, 125, 255), 64: (252, 215, 140, 255), 65: (250, 205, 125, 255),
            66: (235, 170, 90, 255), 67: (200, 130, 62, 255), 68: (155, 88, 42, 255),
            69: (110, 56, 32, 255), 70: (70, 35, 30, 255), 71: OUTLINE
        },
        50: {
            57: OUTLINE, 58: (65, 32, 34, 255), 59: (105, 52, 32, 255),
            60: (150, 80, 40, 255), 61: (195, 120, 58, 255), 62: (228, 155, 80, 255),
            63: (240, 180, 105, 255), 64: (245, 190, 115, 255), 65: (240, 180, 105, 255),
            66: (220, 148, 75, 255), 67: (185, 112, 54, 255), 68: (140, 75, 38, 255),
            69: (98, 48, 30, 255), 70: (62, 30, 32, 255), 71: OUTLINE
        },
        51: {
            57: OUTLINE, 58: (58, 28, 36, 255), 59: (92, 45, 30, 255),
            60: (135, 70, 36, 255), 61: (175, 102, 50, 255), 62: (208, 132, 68, 255),
            63: (222, 150, 85, 255), 64: (228, 160, 95, 255), 65: (222, 150, 85, 255),
            66: (200, 128, 65, 255), 67: (165, 96, 48, 255), 68: (125, 65, 35, 255),
            69: (85, 42, 28, 255), 70: (55, 26, 34, 255), 71: OUTLINE
        },
        52: {
            57: OUTLINE, 58: (48, 22, 38, 255), 59: (78, 36, 32, 255),
            60: (115, 58, 34, 255), 61: (148, 80, 42, 255), 62: (175, 105, 55, 255),
            63: (190, 120, 68, 255), 64: (195, 128, 75, 255), 65: (190, 120, 68, 255),
            66: (170, 100, 52, 255), 67: (140, 75, 40, 255), 68: (105, 52, 32, 255),
            69: (72, 32, 30, 255), 70: (45, 22, 36, 255), 71: OUTLINE
        },
        53: {
            57: OUTLINE, 58: OUTLINE, 59: (50, 24, 38, 255),
            60: (75, 35, 35, 255), 61: (98, 48, 35, 255), 62: (125, 65, 38, 255),
            63: (145, 82, 48, 255), 64: (152, 90, 55, 255), 65: (145, 82, 48, 255),
            66: (120, 62, 38, 255), 67: (92, 45, 35, 255), 68: (70, 32, 35, 255),
            69: (48, 22, 38, 255), 70: OUTLINE, 71: OUTLINE
        }
    }

    for y, row in collar_palette.items():
        for x, col in row.items():
            arr[y, x] = col

    # 3. Left hand & forearm restoration (Y=65..85, X=85..95)
    for y in range(77, 86):
        for x in range(92, 96):
            arr[y, x] = [0, 0, 0, 0]

    for y in range(65, 68):
        arr[y, 93] = [0, 0, 0, 0]
        arr[y, 92] = OUTLINE
        if arr[y, 91, 3] > 0:
            arr[y, 91] = (165, 52, 22, 255)

    for y in range(68, 76):
        arr[y, 93] = OUTLINE
        if y in (68, 69):
            arr[y, 92] = (125, 45, 35, 255)
        elif y in (70, 71, 72):
            arr[y, 92] = (185, 62, 18, 255)
        else:
            arr[y, 92] = (150, 48, 22, 255)

    arr[76, 92] = OUTLINE
    arr[76, 93] = [0, 0, 0, 0]
    arr[77, 92] = OUTLINE
    arr[77, 91] = (120, 45, 30, 255)
    arr[78, 91] = OUTLINE
    arr[78, 90] = (165, 65, 30, 255)

    fist_palette = {
        78: {
            86: (124, 70, 55, 255), 87: (80, 55, 47, 255), 88: OUTLINE,
            89: (226, 85, 38, 255), 90: (170, 60, 25, 255), 91: OUTLINE
        },
        79: {
            86: (220, 95, 35, 255), 87: (185, 75, 30, 255), 88: (95, 38, 30, 255),
            89: (235, 160, 55, 255), 90: (175, 105, 35, 255), 91: OUTLINE
        },
        80: {
            86: (150, 68, 38, 255), 87: (230, 165, 55, 255), 88: (252, 205, 80, 255),
            89: (225, 150, 45, 255), 90: OUTLINE
        },
        81: {
            86: (185, 80, 30, 255), 87: (240, 175, 60, 255), 88: (160, 95, 35, 255),
            89: (210, 135, 40, 255), 90: OUTLINE
        },
        82: {
            86: (200, 95, 38, 255), 87: (175, 90, 32, 255), 88: (130, 62, 30, 255),
            89: OUTLINE
        },
        83: {
            86: OUTLINE, 87: (130, 60, 30, 255), 88: OUTLINE
        },
        84: {
            87: OUTLINE
        }
    }

    arr[84, 88] = [0, 0, 0, 0]

    for y, row in fist_palette.items():
        for x, col in row.items():
            arr[y, x] = col

    repaired = Image.fromarray(arr)
    repaired.save(dst_path)
    print(f"✓ Saved repaired ember orange -> {dst_path}")
    return repaired

from build_tiger_ivory_chassis import create_tiger_paint_ivory_stock
from build_tiger_volcano_chassis import create_tiger_paint_volcano_black

def main():
    ember_file = f"{CHASSIS_DIR}/paint_ember_orange.png"
    ivory_file = f"{CHASSIS_DIR}/paint_ivory_stock.png"
    black_file = f"{CHASSIS_DIR}/paint_volcano_black.png"

    repair_ember_orange(ember_file, ember_file)
    create_tiger_paint_ivory_stock(ember_file, ivory_file)
    create_tiger_paint_volcano_black(ember_file, black_file)

if __name__ == "__main__":
    main()
