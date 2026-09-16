#!/usr/bin/env python3
"""
tools/apply_crane_paperdoll_fix.py
Fixes Cloud Crane (雲嵐鶴) paperdoll assets:
1. Removes artificial white glove and residual bow pixels from chassis (paint_crane_porcelain.png & paint_zephyr_azure.png).
2. Restores complete, unbroken mechanical compound bow (wpn_zephyr_wing_bow.png) with continuous riser/joint and natural grip.
3. Re-exports all Cloud Crane composites and proof images.
Conforms to review.md 0-ART9, 0-ART11, 0-ART12, and CANON.md.
"""

import os
from PIL import Image, ImageDraw
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"
UNIV_WEAPON = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon/wpn_zephyr_wing_bow.png"
master = Image.open("/tmp/crane_center_128.png").convert("RGBA")
W, H = 128, 128

def apply_fix():
    print("=== 1. APPLYING FIX TO WEAPON wpn_zephyr_wing_bow.png ===")
    weapon_clean = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    for y in range(48, 102):
        for x in range(78, 107):
            p = master.getpixel((x, y))
            if p[3] < 20:
                continue
            
            # Upper wing blade & tip
            is_bow_upper = (y <= 78 and x >= 94)
            is_bow_tip = (y <= 62 and x >= 90)
            
            # Mechanical joint/bearing connecting upper wing to riser (x: 91..98, y: 76..85)
            is_joint = (76 <= y <= 85 and 91 <= x <= 98)
            
            # Lower limb and lower pulley
            is_lower = (y >= 84 and 80 <= x <= 93)
            
            # Bow riser / grip / handle & fingers (x: 81..91, y: 80..85)
            is_grip = (80 <= y <= 85 and 81 <= x <= 91)
            
            if is_bow_upper or is_bow_tip or is_joint or is_lower or is_grip:
                weapon_clean.putpixel((x, y), p)

    # Draw crisp pulley cams & bowstring
    wd = ImageDraw.Draw(weapon_clean)
    # Upper pulley cam at (99, 54)
    wd.ellipse([97, 52, 103, 58], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255))
    # Lower pulley cam at (82, 94)
    wd.ellipse([80, 92, 86, 98], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255))
    # High-tension tungsten wire bowstring
    wd.line([(98, 56), (82, 94)], fill=(220, 230, 245, 220), width=1)

    target_wpn1 = f"{CRANE_DIR}/weapon/wpn_zephyr_wing_bow.png"
    weapon_clean.save(target_wpn1)
    weapon_clean.save(UNIV_WEAPON)
    print(f"  ✓ Saved clean weapon: {target_wpn1} (bbox: {weapon_clean.getbbox()})")
    print(f"  ✓ Saved clean weapon: {UNIV_WEAPON}")

    print("\n=== 2. APPLYING FIX TO CHASSIS paint_crane_porcelain.png ===")
    ch_src = Image.open(f"{CRANE_DIR}/chassis/paint_crane_porcelain.png").convert("RGBA")
    ch_clean = ch_src.copy()

    # A. Clear fake white glove at y: 71..79, x: 80..88, restore natural arm/sleeve:
    for y in range(71, 79):
        for x in range(80, 88):
            mp = master.getpixel((x, y))
            ch_clean.putpixel((x, y), mp)

    # B. Remove bow pixels from chassis:
    for y in range(79, 105):
        for x in range(85, 100):
            ch_clean.putpixel((x, y), (0, 0, 0, 0))
    for y in range(85, 100):
        for x in range(80, 86):
            ch_clean.putpixel((x, y), (0, 0, 0, 0))

    # C. Natural articulated fist at y: 80..85, x: 80..85:
    for y in range(80, 85):
        for x in range(80, 85):
            mp = master.getpixel((x, y))
            if mp[3] > 20:
                ch_clean.putpixel((x, y), mp)

    # Outline fist bottom and right edge
    ch_draw = ImageDraw.Draw(ch_clean)
    ch_draw.line([(80, 84), (83, 84)], fill=(31, 26, 58, 255))
    ch_draw.line([(84, 81), (84, 83)], fill=(31, 26, 58, 255))

    target_ch1 = f"{CRANE_DIR}/chassis/paint_crane_porcelain.png"
    ch_clean.save(target_ch1)
    print(f"  ✓ Saved clean porcelain chassis: {target_ch1} (bbox: {ch_clean.getbbox()})")

    print("\n=== 3. REGENERATING paint_zephyr_azure.png ===")
    from build_crane_azure_chassis import create_crane_paint_zephyr_azure
    target_azure = f"{CRANE_DIR}/chassis/paint_zephyr_azure.png"
    create_crane_paint_zephyr_azure(src_path=target_ch1, out_path=target_azure)
    print(f"  ✓ Saved regenerated azure chassis: {target_azure}")

    print("\n=== 4. REGENERATING ALL CRANE PROOFS & COMPOSITES ===")
    from produce_clean_crane_slices import main as produce_crane_slices
    produce_crane_slices()

    import subprocess
    subprocess.run(["python3", f"{REPO_ROOT}/tools/generate_crane_proofs.py"], check=True)
    print("  ✓ All crane proofs re-exported successfully!")

if __name__ == "__main__":
    apply_fix()
