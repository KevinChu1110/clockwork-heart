#!/usr/bin/env python3
"""
build_tortoise_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Xuanji Tortoise (玄機龜) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/XUANJI_TORTOISE_DESIGN_PROPOSAL.md
- docs/world/CANON.md
- art_direction.md 15-item checklist
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART27, 0-ART28, 0-ART28r
- Benchmarked directly against Clockwork Bear (玄軸熊) and Steam Penguin (蒸氣企鵝) standards.
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
TORTOISE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Dawson Day 258 Series)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
JADE_PRIMARY = (45, 106, 79, 255)      # #2D6A4F Jade Bronze Primary
JADE_DARK = (28, 68, 50, 255)
JADE_DEEP = (18, 45, 34, 255)
JADE_LIGHT = (72, 160, 120, 255)
JADE_SHINE = (120, 220, 170, 255)

WHITE_PLATE = (255, 253, 248, 255)     # #FFFDF8 Marble cream white
WHITE_SHINE = (255, 255, 255, 255)
WHITE_SHADOW = (215, 210, 200, 255)
WHITE_DARK = (175, 170, 160, 255)

BRASS_GOLD = (255, 208, 40, 255)       # #FFD028 Tianyuan Brass Gold
BRASS_DARK = (180, 130, 20, 255)
BRASS_DEEP = (110, 75, 15, 255)
BRASS_LIGHT = (255, 235, 120, 255)

AMBER_CORE = (255, 160, 16, 255)       # #FFA010 Amber Quartz Lens
AMBER_LIGHT = (255, 220, 90, 255)
AMBER_DARK = (180, 95, 10, 255)
AMBER_DEEP = (120, 55, 5, 255)

EMERALD_MINT = (78, 216, 106, 255)     # #4ED86A Mint Emerald Core
EMERALD_LIGHT = (160, 250, 180, 255)
EMERALD_DARK = (30, 135, 60, 255)
EMERALD_DEEP = (15, 80, 35, 255)

STEEL_DARK = (55, 62, 75, 255)
STEEL_MID = (100, 112, 130, 255)
STEEL_LIGHT = (170, 185, 205, 255)

def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL XUANJI TORTOISE SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back)
    # File: winding_key/key_tai_chi_dual_fish.png
    # Completely independent brass winding key anchored at upper back
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)
    
    # Stem entering back socket at (38, 46) from key center (28, 28)
    for y in range(35, 48):
        for x in range(30, 42):
            t_s = (y - 35) / 12.0
            sx = 34 + t_s * 4.0
            dist = abs(x - sx)
            if dist <= 2.2:
                edge_t = dist / 2.2
                r_s = int(np.clip(255 * (1 - 0.4 * edge_t) - 40 * t_s, 0, 255))
                g_s = int(np.clip(208 * (1 - 0.5 * edge_t) - 60 * t_s, 0, 255))
                b_s = int(np.clip(40 * (1 - 0.7 * edge_t), 0, 255))
                key_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    # Tai Chi Dual Fish medallion (center (28, 28), radius 12)
    cx, cy, r_k = 28.0, 28.0, 12.0
    for y in range(int(cy - r_k - 3), int(cy + r_k + 4)):
        for x in range(int(cx - r_k - 3), int(cx + r_k + 4)):
            dx = x - cx
            dy = y - cy
            dist = (dx**2 + dy**2)**0.5
            if dist <= r_k:
                angle = np.arctan2(dy, dx)
                if dist >= 7.8:
                    # Outer brass ring with smooth specular reflection
                    spec = max(0.0, 1.0 - ((x - (cx - 5))**2 + (y - (cy - 5))**2)**0.5 / 6.0)
                    shine = max(0.0, np.cos(angle - 2.35))
                    r_k_val = int(np.clip(180 + 75 * spec + 60 * shine, 0, 255))
                    g_k_val = int(np.clip(120 + 90 * spec + 50 * shine, 0, 255))
                    b_k_val = int(np.clip(15 + 180 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_k_val, g_k_val, b_k_val, 255))
                else:
                    # Inner Tai Chi Yin-Yang field
                    t_y = dist / 7.8
                    is_light_half = (dx >= 0) if dy < 0 else (dx > 0 and dy >= 0)
                    base_b = 215 if is_light_half else 65
                    spec_in = max(0.0, 1.0 - ((x - (cx - 2))**2 + (y - (cy - 2))**2)**0.5 / 4.0)
                    r_k_val = int(np.clip(base_b + 40 * spec_in - 20 * t_y, 0, 255))
                    g_k_val = int(np.clip(base_b * 0.75 + 40 * spec_in - 20 * t_y, 0, 255))
                    b_k_val = int(np.clip(base_b * 0.2 + 80 * spec_in, 0, 255))
                    key_img.putpixel((x, y), (r_k_val, g_k_val, b_k_val, 255))

    kd.ellipse([int(cx - r_k), int(cy - r_k), int(cx + r_k), int(cy + r_k)], outline=OUTLINE, width=1)
    kd.ellipse([int(cx - 7.8), int(cy - 7.8), int(cx + 7.8), int(cy + 7.8)], outline=OUTLINE, width=1)
    kd.ellipse([int(cx - 1), int(cy - 4), int(cx + 1), int(cy - 2)], fill=BRASS_DEEP)
    kd.ellipse([int(cx - 1), int(cy + 2), int(cx + 1), int(cy + 4)], fill=WHITE_SHINE)

    # Dual Fish side tail wings
    for fx, fy in [(15, 23), (14, 25), (13, 27), (16, 28), (40, 23), (41, 25), (42, 27), (39, 28)]:
        key_img.putpixel((fx, fy), BRASS_GOLD)
    kd.polygon([(17, 24), (12, 19), (14, 29)], outline=OUTLINE)
    kd.polygon([(39, 24), (44, 19), (42, 29)], outline=OUTLINE)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Back)
    # File: back_curio/curio_bagua_armillary_rings.png
    # Floating mini armillary sphere with emerald gem at (18, 54)
    # + grounded tail rudder at (28, 107)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)
    
    # 1. Hovering armillary astrolabe sphere (center (18, 54), radius 8)
    acx, acy, ar = 18.0, 54.0, 8.5
    for y in range(int(acy - ar - 2), int(acy + ar + 3)):
        for x in range(int(acx - ar - 2), int(acx + ar + 3)):
            dx = x - acx
            dy = y - acy
            dist = (dx**2 + dy**2)**0.5
            if abs(dist - 7.0) <= 1.5:
                spec = max(0.0, 1.0 - ((x - (acx - 4))**2 + (y - (acy - 4))**2)**0.5 / 4.0)
                r_c = int(np.clip(180 + 75 * spec, 0, 255))
                g_c = int(np.clip(120 + 90 * spec, 0, 255))
                b_c = int(np.clip(20 + 150 * spec, 0, 255))
                curio_img.putpixel((x, y), (r_c, g_c, b_c, 255))
            elif dist <= 4.0:
                t_e = dist / 4.0
                spec_e = max(0.0, 1.0 - ((x - (acx - 1.5))**2 + (y - (acy - 1.5))**2)**0.5 / 2.0)
                r_e = int(np.clip(30 + 200 * spec_e, 0, 255))
                g_e = int(np.clip(160 + 95 * spec_e - 40 * t_e, 0, 255))
                b_e = int(np.clip(70 + 170 * spec_e, 0, 255))
                curio_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    cd.ellipse([int(acx - ar), int(acy - ar), int(acx + ar), int(acy + ar)], outline=OUTLINE, width=1)
    cd.point((int(acx - 1), int(acy - 1)), fill=WHITE_SHINE)
        
    # 2. Grounded tail rudder on chassis spine
    for y in range(103, 112):
        for x in range(25, 34):
            dx = x - 29.5
            dy = y - 107.5
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.2:
                spec_t = max(0.0, 1.0 - abs(dx) / 4.0)
                r_t = int(np.clip(160 + 90 * spec_t, 0, 255))
                g_t = int(np.clip(110 + 90 * spec_t, 0, 255))
                b_t = int(np.clip(15 + 100 * spec_t, 0, 255))
                curio_img.putpixel((x, y), (r_t, g_t, b_t, 255))
                
    cd.rounded_rectangle([25, 103, 33, 111], radius=2, outline=OUTLINE, width=1)
    cd.point((29, 106), fill=WHITE_SHINE)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Base)
    # File: chassis/paint_tortoise_jade.png
    # The complete headless automaton tortoise chassis:
    # - Heavy jade-green bronze carapace back & belly base
    # - Raised collar rim for head_unit insertion (hiding neck seam)
    # - 4 sturdy hydraulic leg pillars with blunt metal claws
    # - Clenched mechanical right forearm & palm (open for weapon holding)
    # - Soft contact ground shadow under feet (centered at (64, 114))
    # - Strictly ZERO weapon baked in (0-ART9, 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow (centered at (64, 114), radius 34x5)
    ch_d.ellipse([64 - 34, 114 - 4, 64 + 34, 114 + 4], fill=(31, 26, 58, 125))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Main Carapace & Torso Body (x: 28..88, y: 48..106)
    # Shell Back (Left dome)
    for y in range(48, 106):
        for x in range(28, 88):
            # Carapace ellipsoid equation
            dx = (x - 56) / 28.0
            dy = (y - 78) / 26.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 46)**2 + (y - 64)**2)**0.5 / 16.0)
                r_b = int(np.clip(28 + 60 * (1 - t) + 80 * spec, 0, 255))
                g_b = int(np.clip(68 + 70 * (1 - t) + 120 * spec, 0, 255))
                b_b = int(np.clip(50 + 50 * (1 - t) + 90 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Carapace outer thick rim
    ch_d.ellipse([28, 50, 84, 104], outline=OUTLINE, width=1)
    ch_d.arc([30, 52, 82, 102], start=90, end=270, fill=JADE_LIGHT, width=1)
    
    # Back Carapace Bagua chamfer ridges & rivets
    ch_d.arc([34, 58, 62, 94], start=120, end=240, fill=BRASS_GOLD, width=1)
    ch_d.ellipse([34, 74, 36, 76], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.ellipse([42, 60, 44, 62], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.ellipse([42, 90, 44, 92], fill=BRASS_GOLD, outline=OUTLINE)

    # Raised Neck Collar Ring (for head_unit to socket into smoothly)
    ch_d.rounded_rectangle([52, 46, 74, 56], radius=4, fill=BRASS_GOLD, outline=OUTLINE, width=1)
    ch_d.line([(54, 48), (72, 48)], fill=BRASS_LIGHT, width=1)
    ch_d.line([(54, 54), (72, 54)], fill=BRASS_DEEP, width=1)

    # Chest hollow cavity for core (x: 58..68, y: 65..75)
    ch_d.polygon([(63, 64), (68, 70), (63, 76), (58, 70)], fill=OUTLINE)

    # 3. Four Hydraulic Leg Pillars & Foot Claws
    # Hind-Left Foot (x: 26..38, y: 98..109)
    ch_d.rounded_rectangle([26, 98, 38, 105], radius=3, fill=JADE_DARK, outline=OUTLINE, width=1)
    ch_d.line([(28, 100), (36, 100)], fill=JADE_LIGHT, width=1)
    ch_d.polygon([(25, 109), (28, 104), (31, 109)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(32, 109), (35, 104), (38, 109)], fill=STEEL_MID, outline=OUTLINE)

    # Hind-Right Foot (x: 82..94, y: 98..109)
    ch_d.rounded_rectangle([82, 98, 94, 105], radius=3, fill=JADE_DARK, outline=OUTLINE, width=1)
    ch_d.line([(84, 100), (92, 100)], fill=JADE_LIGHT, width=1)
    ch_d.polygon([(82, 109), (85, 104), (87, 109)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(88, 109), (91, 104), (94, 109)], fill=STEEL_MID, outline=OUTLINE)

    # Fore-Left Leg & Footpad (x: 40..54, y: 96..115)
    # Leg cylinder
    ch_d.rounded_rectangle([42, 94, 52, 104], radius=3, fill=JADE_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(44, 96), (50, 96)], fill=JADE_SHINE, width=1)
    # Brass shock collar
    ch_d.rounded_rectangle([41, 103, 53, 107], radius=1, fill=BRASS_GOLD, outline=BRASS_DEEP, width=1)
    # Footplate & 3 blunt metal claws (firmly resting on shadow at y=114)
    ch_d.polygon([(39, 114), (42, 107), (44, 114)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(44, 115), (47, 107), (50, 115)], fill=STEEL_LIGHT, outline=OUTLINE)
    ch_d.polygon([(50, 114), (53, 107), (55, 114)], fill=STEEL_DARK, outline=OUTLINE)

    # Fore-Right Leg & Footpad (x: 66..80, y: 96..115)
    # Leg cylinder
    ch_d.rounded_rectangle([68, 94, 78, 104], radius=3, fill=JADE_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(70, 96), (76, 96)], fill=JADE_SHINE, width=1)
    # Brass shock collar
    ch_d.rounded_rectangle([67, 103, 79, 107], radius=1, fill=BRASS_GOLD, outline=BRASS_DEEP, width=1)
    # Footplate & 3 blunt metal claws (firmly resting on shadow at y=114)
    ch_d.polygon([(65, 114), (68, 107), (70, 114)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(70, 115), (73, 107), (76, 115)], fill=STEEL_LIGHT, outline=OUTLINE)
    ch_d.polygon([(76, 114), (79, 107), (81, 114)], fill=STEEL_DARK, outline=OUTLINE)

    # 4. Right Arm & Open Gripping Palm (x: 70..82, y: 72..86)
    # Upper arm & elbow joint
    ch_d.rounded_rectangle([68, 72, 78, 82], radius=4, fill=JADE_PRIMARY, outline=OUTLINE, width=1)
    ch_d.ellipse([70, 74, 76, 80], fill=BRASS_GOLD, outline=OUTLINE)
    # Forearm
    ch_d.rounded_rectangle([74, 74, 82, 82], radius=3, fill=JADE_DARK, outline=OUTLINE, width=1)
    # Brass wrist ring
    ch_d.rounded_rectangle([78, 75, 82, 81], radius=1, fill=BRASS_GOLD, outline=BRASS_DEEP)
    # Metallic clenched hand ready for weapon (x: 82..87, y: 76..82)
    ch_d.polygon([(82, 76), (86, 75), (88, 79), (86, 83), (82, 82)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.line([(84, 77), (86, 80)], fill=BRASS_LIGHT, width=1)
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Head)
    # File: head_unit/head_xuanji_tortoise_stock.png
    # Cranial helmet shell, brass hydraulic neck, jaws (x: 44..86, y: 22..58)
    # Eyes hollowed out for optic_core to fill in cleanly
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Hydraulic Neck Sleeves (x: 54..72, y: 44..56)
    for y in range(44, 56):
        for x in range(54, 72):
            dx = (x - 63) / 8.5
            if abs(dx) <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 60) / 4.0)
                r_n = int(np.clip(160 + 80 * spec, 0, 255))
                g_n = int(np.clip(110 + 90 * spec, 0, 255))
                b_n = int(np.clip(15 + 100 * spec, 0, 255))
                head_img.putpixel((x, y), (r_n, g_n, b_n, 255))

    hd.line([(55, 48), (71, 48)], fill=OUTLINE, width=1)
    hd.line([(55, 52), (71, 52)], fill=OUTLINE, width=1)

    # 2. Cranial Dome Helmet (center (64, 38), radius 16x13)
    for y in range(23, 49):
        for x in range(46, 82):
            dx = (x - 64.0) / 16.0
            dy = (y - 38.0) / 13.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 30)**2)**0.5 / 8.0)
                r_h = int(np.clip(35 + 50 * (1 - t) + 90 * spec, 0, 255))
                g_h = int(np.clip(85 + 60 * (1 - t) + 120 * spec, 0, 255))
                b_h = int(np.clip(60 + 50 * (1 - t) + 90 * spec, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Helmet outlines & ridges
    hd.ellipse([48, 25, 80, 49], outline=OUTLINE, width=1)
    hd.arc([50, 27, 78, 47], start=180, end=360, fill=JADE_LIGHT, width=1)
    # Crown crest
    hd.line([(64, 25), (64, 33)], fill=BRASS_GOLD, width=2)
    hd.point((64, 26), fill=WHITE_SHINE)

    # Golden Jaw plates
    hd.rounded_rectangle([52, 44, 76, 51], radius=3, fill=BRASS_GOLD, outline=OUTLINE, width=1)
    hd.line([(54, 46), (74, 46)], fill=BRASS_LIGHT, width=1)
    hd.line([(54, 49), (74, 49)], fill=BRASS_DARK, width=1)

    # Hollow eye sockets (hollowed out with deep dark recessed socket ring)
    # Left eye socket at (55, 39)
    hd.ellipse([50, 35, 60, 45], fill=OUTLINE)
    hd.ellipse([51, 36, 59, 44], fill=JADE_DEEP)
    # Right eye socket at (69, 39)
    hd.ellipse([64, 35, 74, 45], fill=OUTLINE)
    hd.ellipse([65, 36, 73, 44], fill=JADE_DEEP)
    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Overlay)
    # File: costume/costume_zen_dojo_harness.png
    # Zen Dojo Harness: Marble cream-white chestplate, pauldrons,
    # brass belt buckle, central core opening
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Marble White Plastron Chestplate (x: 48..78, y: 56..92)
    for y in range(56, 92):
        for x in range(48, 78):
            dx = (x - 63.0) / 14.0
            dy = (y - 74.0) / 16.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 66)**2)**0.5 / 7.0)
                r_p = int(np.clip(220 + 35 * (1 - t) + 20 * spec, 0, 255))
                g_p = int(np.clip(215 + 38 * (1 - t) + 20 * spec, 0, 255))
                b_p = int(np.clip(205 + 43 * (1 - t) + 20 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    # Chestplate border & rivets
    cos_d.ellipse([49, 58, 77, 90], outline=OUTLINE, width=1)
    cos_d.arc([51, 60, 75, 88], start=0, end=180, fill=WHITE_SHADOW, width=1)
    cos_d.ellipse([53, 62, 55, 64], fill=BRASS_GOLD, outline=OUTLINE)
    cos_d.ellipse([71, 62, 73, 64], fill=BRASS_GOLD, outline=OUTLINE)

    # Left & Right Shoulder Pauldron clasps
    cos_d.polygon([(44, 60), (52, 56), (50, 68), (42, 66)], fill=JADE_PRIMARY, outline=OUTLINE)
    cos_d.line([(45, 62), (49, 59)], fill=BRASS_GOLD, width=1)
    cos_d.polygon([(74, 56), (82, 60), (84, 66), (76, 68)], fill=JADE_PRIMARY, outline=OUTLINE)
    cos_d.line([(77, 59), (81, 62)], fill=BRASS_GOLD, width=1)

    # Central Core Rhombic Opening (hollowed out so optic_core shines through)
    cos_d.polygon([(63, 63), (69, 70), (63, 77), (57, 70)], fill=(0, 0, 0, 0), outline=OUTLINE)
    cos_d.polygon([(63, 64), (68, 70), (63, 76), (58, 70)], outline=BRASS_GOLD)

    # Zen Dojo Waist Harness & Gold Buckle (x: 50..76, y: 78..86)
    cos_d.rectangle([50, 80, 76, 85], fill=JADE_DARK, outline=OUTLINE)
    cos_d.rounded_rectangle([58, 78, 68, 87], radius=2, fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cos_d.rectangle([60, 80, 66, 85], fill=BRASS_DARK)
    cos_d.point((61, 81), fill=WHITE_SHINE)
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, FX/Optics)
    # File: optic_core/core_amber_quartz.png
    # Two glowing amber quartz eye lenses + chest mint emerald heart
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cord = ImageDraw.Draw(core_img)

    # 1. Left amber quartz lens (center (55, 40), radius 4.5)
    for y in range(35, 46):
        for x in range(50, 61):
            dx = x - 55.0
            dy = y - 40.0
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.2:
                t = dist / 4.2
                spec = max(0.0, 1.0 - ((x - 53.5)**2 + (y - 38.5)**2)**0.5 / 2.0)
                r_c = int(np.clip(180 + 75 * spec - 40 * t, 0, 255))
                g_c = int(np.clip(100 + 130 * spec - 30 * t, 0, 255))
                b_c = int(np.clip(10 + 200 * spec, 0, 255))
                core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cord.ellipse([51, 36, 59, 44], outline=BRASS_GOLD, width=1)
    cord.point((53, 38), fill=WHITE_SHINE)
    cord.point((54, 38), fill=WHITE_SHINE)

    # 2. Right amber quartz lens (center (69, 40), radius 4.5)
    for y in range(35, 46):
        for x in range(64, 75):
            dx = x - 69.0
            dy = y - 40.0
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.2:
                t = dist / 4.2
                spec = max(0.0, 1.0 - ((x - 67.5)**2 + (y - 38.5)**2)**0.5 / 2.0)
                r_c = int(np.clip(180 + 75 * spec - 40 * t, 0, 255))
                g_c = int(np.clip(100 + 130 * spec - 30 * t, 0, 255))
                b_c = int(np.clip(10 + 200 * spec, 0, 255))
                core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cord.ellipse([65, 36, 73, 44], outline=BRASS_GOLD, width=1)
    cord.point((67, 38), fill=WHITE_SHINE)
    cord.point((68, 38), fill=WHITE_SHINE)

    # 3. Chest Mint Emerald Heart Gem (faceted crystal at (63, 70))
    for y in range(65, 76):
        for x in range(58, 69):
            dx = abs(x - 63.0) / 4.5
            dy = abs(y - 70.0) / 5.0
            if dx + dy <= 1.0:
                t = dx + dy
                spec = max(0.0, 1.0 - ((x - 62)**2 + (y - 68)**2)**0.5 / 2.0)
                r_c = int(np.clip(35 + 180 * spec, 0, 255))
                g_c = int(np.clip(180 + 75 * spec + 30 * (1 - t), 0, 255))
                b_c = int(np.clip(75 + 140 * spec, 0, 255))
                core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cord.polygon([(63, 65), (67, 70), (63, 75), (59, 70)], outline=OUTLINE)
    cord.polygon([(63, 66), (66, 70), (63, 74), (60, 70)], outline=EMERALD_LIGHT)
    cord.line([(63, 66), (63, 74)], fill=WHITE_SHINE, width=1)
    cord.point((62, 68), fill=WHITE_SHINE)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Front)
    # File: weapon/wpn_bagua_astrolabe.png
    # Completely independent Xuanji Bagua Astrolabe / Bulwark Float-Crystal
    # Centered at (96, 62), hovering above right hand
    # Concentric rotating brass rings + central glowing emerald crystal
    # Zero body or arm slice baked into weapon!
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wx, wy = 96.0, 62.0
    # Outer brass astrolabe ring (radius 16)
    for rad in range(16, 13, -1):
        t_w = (rad - 14) / 2.0
        w_col = BRASS_GOLD if rad == 15 else (BRASS_DARK if rad == 16 else BRASS_LIGHT)
        wd.ellipse([int(wx - rad), int(wy - rad), int(wx + rad), int(wy + rad)], outline=w_col, width=1)
    wd.ellipse([int(wx - 16), int(wy - 16), int(wx + 16), int(wy + 16)], outline=OUTLINE, width=1)

    # Inner rotating ring (tilted ellipse)
    wd.arc([int(wx - 12), int(wy - 6), int(wx + 12), int(wy + 6)], start=0, end=360, fill=BRASS_LIGHT, width=1)
    wd.arc([int(wx - 6), int(wy - 12), int(wx + 6), int(wy + 12)], start=0, end=360, fill=BRASS_DEEP, width=1)

    # Four Bagua Astrolabe pointer beads at 0, 90, 180, 270 degrees
    for ang in [0, np.pi/2, np.pi, 3*np.pi/2]:
        bx = int(wx + 15 * np.cos(ang))
        by = int(wy + 15 * np.sin(ang))
        wd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=BRASS_LIGHT, outline=OUTLINE)

    # Central Floating Hexagonal Emerald Crystal (radius 6.5)
    for y in range(int(wy - 8), int(wy + 9)):
        for x in range(int(wx - 8), int(wx + 9)):
            dx = abs(x - wx)
            dy = abs(y - wy)
            if dx <= 6.0 and (dx * 0.5 + dy * 0.866) <= 6.0:
                dist = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - ((x - (wx - 2))**2 + (y - (wy - 2))**2)**0.5 / 2.5)
                r_cr = int(np.clip(25 + 200 * spec, 0, 255))
                g_cr = int(np.clip(170 + 85 * spec + 20 * (1 - dist/6.0), 0, 255))
                b_cr = int(np.clip(80 + 150 * spec, 0, 255))
                weapon_img.putpixel((x, y), (r_cr, g_cr, b_cr, 255))

    # Facet lines & outline
    hex_poly = [
        (int(wx), int(wy - 7)), (int(wx + 6), int(wy - 3)),
        (int(wx + 6), int(wy + 3)), (int(wx), int(wy + 7)),
        (int(wx - 6), int(wy + 3)), (int(wx - 6), int(wy - 3))
    ]
    wd.polygon(hex_poly, outline=OUTLINE)
    wd.line([(int(wx), int(wy - 7)), (int(wx), int(wy + 7))], fill=WHITE_SHINE, width=1)
    wd.line([(int(wx - 6), int(wy)), (int(wx + 6), int(wy))], fill=EMERALD_LIGHT, width=1)
    wd.point((int(wx - 1), int(wy - 2)), fill=WHITE_SHINE)
    wd.point((int(wx), int(wy - 2)), fill=WHITE_SHINE)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 and 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "paint_tortoise_jade", chassis_img),
        ("head_unit", "head_xuanji_tortoise_stock", head_img),
        ("winding_key", "key_tai_chi_dual_fish", key_img),
        ("costume", "costume_zen_dojo_harness", costume_img),
        ("optic_core", "core_amber_quartz", core_img),
        ("weapon", "wpn_bagua_astrolabe", weapon_img),
        ("back_curio", "curio_bagua_armillary_rings", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{TORTOISE_PD_DIR}/{slot}"
        os.makedirs(out_dir, exist_ok=True)
        dst_128 = f"{out_dir}/{item_id}.png"
        img.save(dst_128)
        
        # 512x512 with LANCZOS
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{out_dir}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    shutil.copyfile(f"{TORTOISE_PD_DIR}/winding_key/key_tai_chi_dual_fish.png", f"{KEY_DIR}/key_tai_chi_dual_fish.png")
    shutil.copyfile(f"{TORTOISE_PD_DIR}/weapon/wpn_bagua_astrolabe.png", f"{WEAPON_DIR}/wpn_bagua_astrolabe.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{TORTOISE_PD_DIR}/proof_paperdoll_tortoise_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{TORTOISE_PD_DIR}/proof_paperdoll_tortoise_magenta.png"
    magenta_bg.save(proof_mag)

    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    titles = ["Key (Z:5)", "Curio (Z:8)", "Chassis (Z:10)", "Head (Z:20)", "Costume (Z:25)", "Core (Z:30)", "Weapon (Z:40)"]
    imgs = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    for i, (t, simg) in enumerate(zip(titles, imgs)):
        sx = 8 + i * (W + 8)
        sy = 16
        cb = Image.new("RGBA", (W, H), (45, 40, 60, 255))
        cb_d = ImageDraw.Draw(cb)
        for cy in range(0, H, 16):
            for cx in range(0, W, 16):
                if (cx // 16 + cy // 16) % 2 == 1:
                    cb_d.rectangle([cx, cy, cx + 15, cy + 15], fill=(55, 50, 75, 255))
        cb.alpha_composite(simg)
        strip_img.paste(cb, (sx, sy))
        sd.text((sx + 4, 2), t, fill=(255, 208, 40, 255))

    proof_7 = f"{TORTOISE_PD_DIR}/proof_tortoise_all_7_slices.png"
    strip_img.save(proof_7)
    print("  ✓ Proof images generated successfully")

if __name__ == "__main__":
    build_all()
