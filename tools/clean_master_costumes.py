#!/usr/bin/env python3
"""
tools/clean_master_costumes.py
Cleans and refines all 3 official costume slices for Lion according to 0-ART50 standards:
1. Cleans stray noise, dirty clipping lines, and edge artifacts.
2. Ensures circular core port-hole at (106, 70) with golden rim so the glowing heart core shines through.
3. Produces high-resolution, perfectly aligned costume sprites matching navel anchor (256, 348), origin=[126, 118].
"""

import math
import numpy as np
from PIL import Image, ImageDraw

WS_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_dd5fc16a"
MASTER_P = f"{WS_ROOT}/tools/lion_master_512.png"
RAW_NUT_512 = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion/costume/costume_nutcracker_guard_512.png"
RAW_ART_512 = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion/costume/costume_steam_artisan_512.png"
OUT_DIR = f"{WS_ROOT}/game/assets/sprites/player/paperdoll/lion/maple_parts"

def run():
    master = Image.open(MASTER_P).convert("RGBA")
    m_arr = np.array(master)

    # -------------------------------------------------------------
    # 1. COSTUME ROYAL GUARD (from master)
    # -------------------------------------------------------------
    print("--- 1. Refining Costume Royal Guard ---")
    cos_rg_arr = np.zeros_like(m_arr)
    for y in range(230, 443):
        for x in range(130, 371):
            is_key = (x > 330 and y < 320)
            is_lance = (x < 152 and y < 330)
            if m_arr[y, x, 3] > 0 and not is_key and not is_lance:
                # Include breastplate and skirt
                if y >= 270:
                    cos_rg_arr[y, x] = m_arr[y, x]

    cos_rg = Image.fromarray(cos_rg_arr, mode="RGBA").crop((130, 230, 370, 442))
    # Ensure core port-hole at (106, 70) is transparent so the body's cyan heart core shines through!
    rg_arr = np.array(cos_rg)
    for cy in range(len(rg_arr)):
        for cx in range(len(rg_arr[0])):
            d = math.hypot(cx - 106, cy - 70)
            if d < 15:
                rg_arr[cy, cx, 3] = 0

    cos_rg = Image.fromarray(rg_arr, mode="RGBA")
    # Gold bezel around core opening
    rg_draw = ImageDraw.Draw(cos_rg)
    rg_draw.ellipse([106 - 16, 70 - 16, 106 + 16, 70 + 16], outline=(245, 205, 55, 255), width=2)
    cos_rg.save(f"{OUT_DIR}/costume/costume_royal_guard.png")
    print("  ✓ costume_royal_guard.png refined (Ivory Cuirass + Navy Pteruges Skirt)")

    # -------------------------------------------------------------
    # 2. COSTUME NUTCRACKER GUARD (clean 512 raw asset)
    # -------------------------------------------------------------
    print("--- 2. Refining Costume Nutcracker Guard ---")
    nut_raw = Image.open(RAW_NUT_512).convert("RGBA")
    n_arr = np.array(nut_raw)

    # Clean stray noise: remove isolated pixels where alpha < 80 or outside bounds
    for y in range(512):
        for x in range(512):
            if n_arr[y, x, 3] < 90:
                n_arr[y, x] = 0
            # Remove dirty top/side margin noise (y < 225 or x < 130 or x > 370 or y > 442)
            if y < 225 or x < 125 or x > 375 or y > 445:
                n_arr[y, x] = 0

    nut_clean = Image.fromarray(n_arr, mode="RGBA").crop((130, 230, 370, 442))
    # Cut circular core port-hole at (106, 70)
    nut_arr = np.array(nut_clean)
    for cy in range(len(nut_arr)):
        for cx in range(len(nut_arr[0])):
            d = math.hypot(cx - 106, cy - 70)
            if d < 15:
                nut_arr[cy, cx, 3] = 0

    nut_final = Image.fromarray(nut_arr, mode="RGBA")
    ndraw = ImageDraw.Draw(nut_final)
    # Polished golden bezel around core opening
    ndraw.ellipse([106 - 16, 70 - 16, 106 + 16, 70 + 16], outline=(245, 215, 60, 255), width=2)
    nut_final.save(f"{OUT_DIR}/costume/costume_nutcracker_guard.png")
    print("  ✓ costume_nutcracker_guard.png refined (Scarlet Uniform + Cleaned Edges + Core Port)")

    # -------------------------------------------------------------
    # 3. COSTUME STEAM ARTISAN (clean 512 raw asset)
    # -------------------------------------------------------------
    print("--- 3. Refining Costume Steam Artisan ---")
    art_raw = Image.open(RAW_ART_512).convert("RGBA")
    a_arr = np.array(art_raw)

    # Clean stray noise and dirty alignment lines
    for y in range(512):
        for x in range(512):
            if a_arr[y, x, 3] < 90:
                a_arr[y, x] = 0
            if y < 225 or x < 125 or x > 375 or y > 445:
                a_arr[y, x] = 0

    art_clean = Image.fromarray(a_arr, mode="RGBA").crop((130, 230, 370, 442))
    art_arr = np.array(art_clean)
    # Cut circular core port-hole at (106, 70)
    for cy in range(len(art_arr)):
        for cx in range(len(art_arr[0])):
            d = math.hypot(cx - 106, cy - 70)
            if d < 15:
                art_arr[cy, cx, 3] = 0

    art_final = Image.fromarray(art_arr, mode="RGBA")
    adraw = ImageDraw.Draw(art_final)
    # Polished brass bezel around core opening
    adraw.ellipse([106 - 16, 70 - 16, 106 + 16, 70 + 16], outline=(215, 165, 45, 255), width=2)
    art_final.save(f"{OUT_DIR}/costume/costume_steam_artisan.png")
    print("  ✓ costume_steam_artisan.png refined (Slate-Steel Overall + Studded Belt + Core Port)")

    # -------------------------------------------------------------
    # 4. BARE CHASSIS (BODY)
    # In master body, we have the complete arms, legs, and bare torso
    # Underneath the costumes, the bare chassis has the golden brass gear pelvis
    # -------------------------------------------------------------
    print("--- 4. Refining Bare Chassis (Body) ---")
    body_arr = np.zeros_like(m_arr)
    for y in range(260, 512):
        for x in range(120, 420):
            is_key = (x > 330 and y < 330)
            if m_arr[y, x, 3] > 0 and not is_key:
                body_arr[y, x] = m_arr[y, x]

    # For bare chassis: in the waist/pelvis region (y: 350..425),
    # replace the blue cloth with solid golden brass mechanical linkages and gears
    for y in range(350, 425):
        for x in range(185, 325):
            p = body_arr[y, x]
            if p[3] > 60 and (int(p[2]) > int(p[0]) + 10):
                lum = (int(p[0]) + int(p[1]) + int(p[2])) / 3.0 / 255.0
                r = int(np.clip(180 * lum + 40, 0, 255))
                g = int(np.clip(135 * lum + 25, 0, 255))
                b = int(np.clip(65 * lum + 15, 0, 255))
                body_arr[y, x] = [r, g, b, p[3]]

    bare_body = Image.fromarray(body_arr, mode="RGBA")
    bare_body.save(f"{OUT_DIR}/body/paint_brass_gold.png")

    b_iv = np.array(bare_body)
    gold_m = (b_iv[:, :, 3] > 100) & (b_iv[:, :, 0] > 140) & (b_iv[:, :, 1] > 100) & (b_iv[:, :, 2] < 100)
    b_iv[gold_m, 0] = np.clip(b_iv[gold_m, 0] * 0.95 + 20, 0, 255)
    b_iv[gold_m, 1] = np.clip(b_iv[gold_m, 1] * 0.95 + 20, 0, 255)
    b_iv[gold_m, 2] = np.clip(b_iv[gold_m, 2] * 0.5 + 110, 0, 255)
    Image.fromarray(b_iv, mode="RGBA").save(f"{OUT_DIR}/body/paint_ivory_stock.png")

    b_nv = np.array(bare_body)
    b_nv[gold_m, 0] = np.clip(b_nv[gold_m, 0] * 0.2 + 20, 0, 255)
    b_nv[gold_m, 1] = np.clip(b_nv[gold_m, 1] * 0.3 + 40, 0, 255)
    b_nv[gold_m, 2] = np.clip(b_nv[gold_m, 2] * 0.4 + 90, 0, 255)
    Image.fromarray(b_nv, mode="RGBA").save(f"{OUT_DIR}/body/paint_midnight_navy.png")
    print("  ✓ Body paints refined (Brass Gold, Ivory Stock, Midnight Navy)")

    print("🎉 ALL REFINEMENTS COMPLETE!")

if __name__ == "__main__":
    run()
