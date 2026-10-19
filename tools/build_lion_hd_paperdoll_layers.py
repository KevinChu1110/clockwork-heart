#!/usr/bin/env python3
"""
tools/build_lion_hd_paperdoll_layers.py
Creates complete, pristine, non-clipping, high-definition modular paperdoll layers for Lion.
"""

import os
import numpy as np
from PIL import Image, ImageDraw

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a"
MASTER_P = f"{WS_ROOT}/tools/lion_master_512.png"
OUT_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts"

def build_all():
    master = Image.open(MASTER_P).convert("RGBA")
    m_arr = np.array(master)

    # -------------------------------------------------------------
    # 1. BARE CHASSIS (BODY)
    # The mechanical chassis: golden brass joints, chest core, hips and legs
    # In master, the blue skirt is y: 350..425, x: 190..325
    # For bare chassis, under the blue skirt we render golden brass mechanical joint pelvis
    # -------------------------------------------------------------
    print("--- 1. Building Chassis (Bare Body) ---")
    chassis_arr = np.zeros_like(m_arr)
    for y in range(260, 512):
        for x in range(120, 420):
            # exclude lance and key
            is_lance = (x < 155 and y < 380)
            is_key = (x > 330 and y < 330)
            if m_arr[y, x, 3] > 0 and not is_lance and not is_key:
                chassis_arr[y, x] = m_arr[y, x]

    # Convert blue skirt area (y: 355..425, x: 200..320) on bare chassis into brass/bronze mechanical joints
    for y in range(355, 425):
        for x in range(200, 320):
            p = chassis_arr[y, x]
            if p[3] > 100:
                # If it's the blue skirt
                if int(p[2]) > int(p[0]) + 15 and int(p[2]) > 60:
                    # Replace with warm brass/bronze mechanics [180, 135, 65]
                    lum = (int(p[0]) + int(p[1]) + int(p[2])) / 3.0 / 255.0
                    r = int(np.clip(185 * lum + 45, 0, 255))
                    g = int(np.clip(135 * lum + 30, 0, 255))
                    b = int(np.clip(65 * lum + 15, 0, 255))
                    chassis_arr[y, x] = [r, g, b, p[3]]

    chassis_brass = Image.fromarray(chassis_arr, mode="RGBA")
    chassis_brass.save(f"{OUT_DIR}/body/paint_brass_gold.png")

    # Ivory Chassis variant
    ch_ivory = np.array(chassis_brass)
    gold_mask = (ch_ivory[:, :, 3] > 100) & (ch_ivory[:, :, 0] > 150) & (ch_ivory[:, :, 1] > 110) & (ch_ivory[:, :, 2] < 110)
    ch_ivory[gold_mask, 0] = np.clip(ch_ivory[gold_mask, 0] * 0.95 + 20, 0, 255)
    ch_ivory[gold_mask, 1] = np.clip(ch_ivory[gold_mask, 1] * 0.95 + 20, 0, 255)
    ch_ivory[gold_mask, 2] = np.clip(ch_ivory[gold_mask, 2] * 0.5 + 110, 0, 255)
    Image.fromarray(ch_ivory, mode="RGBA").save(f"{OUT_DIR}/body/paint_ivory_stock.png")

    # Midnight Navy Chassis variant
    ch_navy = np.array(chassis_brass)
    ch_navy[gold_mask, 0] = np.clip(ch_navy[gold_mask, 0] * 0.2 + 20, 0, 255)
    ch_navy[gold_mask, 1] = np.clip(ch_navy[gold_mask, 1] * 0.3 + 40, 0, 255)
    ch_navy[gold_mask, 2] = np.clip(ch_navy[gold_mask, 2] * 0.4 + 90, 0, 255)
    Image.fromarray(ch_navy, mode="RGBA").save(f"{OUT_DIR}/body/paint_midnight_navy.png")
    print("  ✓ Body paints saved: brass_gold, ivory_stock, midnight_navy")

    # -------------------------------------------------------------
    # 2. COSTUMES
    # Variant 1: costume_royal_guard (Ivory cuirass + Navy/Gold pteruges skirt + belt)
    # Variant 2: costume_steam_artisan (Leather brown & brass artisan apron/suspenders)
    # Variant 3: costume_nutcracker_guard (Scarlet red & gold nutcracker guard uniform)
    # -------------------------------------------------------------
    print("--- 2. Building Costumes ---")
    # Base Royal Guard costume directly from master (y: 230..442, x: 130..370)
    # In master, the blue skirt is y: 350..425, and belt is y: 345..355
    cos_royal_arr = np.zeros_like(m_arr)
    for y in range(230, 443):
        for x in range(130, 371):
            is_key = (x > 330 and y < 320)
            if m_arr[y, x, 3] > 0 and not is_key:
                cos_royal_arr[y, x] = m_arr[y, x]

    cos_royal = Image.fromarray(cos_royal_arr, mode="RGBA").crop((130, 230, 370, 442))
    cos_royal.save(f"{OUT_DIR}/costume/costume_royal_guard.png")
    print("  ✓ costume_royal_guard.png saved")

    # Variant 2: Steam Artisan (warm leather brown #7A4B28 & brass buckled suspenders)
    cos_art_arr = np.array(cos_royal)
    for cy in range(len(cos_art_arr)):
        for cx in range(len(cos_art_arr[0])):
            p = cos_art_arr[cy, cx]
            if p[3] > 80:
                if cy >= 115 and (int(p[2]) > int(p[0]) + 10):
                    lum = (int(p[0]) + int(p[1]) + int(p[2])) / 3.0 / 255.0
                    r = int(np.clip(135 * lum + 40, 0, 255))
                    g = int(np.clip(85 * lum + 20, 0, 255))
                    b = int(np.clip(45 * lum + 10, 0, 255))
                    cos_art_arr[cy, cx] = [r, g, b, p[3]]

    cos_art = Image.fromarray(cos_art_arr, mode="RGBA")
    adraw = ImageDraw.Draw(cos_art)
    strap_color = (130, 80, 40, 240)
    strap_edge = (50, 30, 15, 255)
    buckle_gold = (255, 210, 50, 255)
    adraw.line([(88, 55), (88, 120)], fill=strap_edge, width=6)
    adraw.line([(88, 55), (88, 120)], fill=strap_color, width=4)
    adraw.rectangle([85, 95, 91, 102], outline=buckle_gold, width=2)
    adraw.line([(155, 55), (155, 120)], fill=strap_edge, width=6)
    adraw.line([(155, 55), (155, 120)], fill=strap_color, width=4)
    adraw.rectangle([152, 95, 158, 102], outline=buckle_gold, width=2)

    cos_art.save(f"{OUT_DIR}/costume/costume_steam_artisan.png")
    print("  ✓ costume_steam_artisan.png saved")

    # Variant 3: Nutcracker Guard (Scarlet red #C82828 skirt & golden braids)
    cos_nut_arr = np.array(cos_royal)
    for cy in range(len(cos_nut_arr)):
        for cx in range(len(cos_nut_arr[0])):
            p = cos_nut_arr[cy, cx]
            if p[3] > 80 and cy >= 115 and (int(p[2]) > int(p[0]) + 10):
                lum = (int(p[0]) + int(p[1]) + int(p[2])) / 3.0 / 255.0
                r = int(np.clip(200 * lum + 40, 0, 255))
                g = int(np.clip(45 * lum + 10, 0, 255))
                b = int(np.clip(45 * lum + 10, 0, 255))
                cos_nut_arr[cy, cx] = [r, g, b, p[3]]

    cos_nut = Image.fromarray(cos_nut_arr, mode="RGBA")
    cos_nut.save(f"{OUT_DIR}/costume/costume_nutcracker_guard.png")
    print("  ✓ costume_nutcracker_guard.png saved")

if __name__ == "__main__":
    build_all()
