#!/usr/bin/env python3
"""
build_elephant_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Colossus Elephant (鋼岳象) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/COLOSSUS_ELEPHANT_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh, all metal/enamel/hydraulic, brass key)
- docs/ART_DAILY_CONSTITUTION.md (Dopamine high-saturation palette, clean enamel/brass, deep outline)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
ELEPHANT_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Dawson Day 258 Series & Elephant Proposal)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Brass Primary (#D4A017 ~ #B8860B)
BRASS_PRIMARY = (212, 160, 23, 255)    # #D4A017 Quenched Brass Gold
BRASS_LIGHT = (255, 220, 85, 255)      # Specular highlight
BRASS_SHINE = (255, 245, 170, 255)     # Intense specular shine
BRASS_DARK = (155, 110, 15, 255)       # Shaded brass
BRASS_DEEP = (95, 65, 10, 255)         # Deep seam shadow

# Ivory Alloy Secondary (#FFFDF8 ~ #FFF8E7)
IVORY_WHITE = (255, 253, 248, 255)     # #FFFDF8 Ivory-white alloy
IVORY_SHINE = (255, 255, 255, 255)
IVORY_SHADOW = (220, 215, 205, 255)
IVORY_DARK = (180, 175, 165, 255)

# Steam Warm Orange Accent (#FFA010 ~ #FF5E8A)
ORANGE_STEAM = (255, 160, 16, 255)     # #FFA010 High pressure steam orange
ORANGE_LIGHT = (255, 210, 80, 255)
ORANGE_DARK = (190, 95, 10, 255)
ORANGE_DEEP = (120, 50, 5, 255)

# Sky Blue Quartz (#38A0FF)
SKY_BLUE = (56, 160, 255, 255)         # #38A0FF Sky blue optical lens
SKY_LIGHT = (160, 220, 255, 255)
SKY_DARK = (20, 100, 190, 255)
SKY_DEEP = (10, 50, 120, 255)

# Mint Green Core (#4ED86A)
MINT_GREEN = (78, 216, 106, 255)       # #4ED86A Clockwork heart gem
MINT_LIGHT = (170, 250, 185, 255)
MINT_DARK = (30, 140, 60, 255)
MINT_DEEP = (15, 80, 35, 255)

# Mechanical Steel / Hydraulic Pistons
STEEL_LIGHT = (175, 190, 210, 255)     # Polished chromium-molybdenum rod
STEEL_MID = (105, 118, 135, 255)
STEEL_DARK = (58, 65, 78, 255)
STEEL_DEEP = (35, 40, 50, 255)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL COLOSSUS ELEPHANT SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back)
    # File: winding_key/key_heavy_cross_wheel.png
    # Heavy industrial cross-wheel brass key (4-ring cross concentric geometry)
    # Anchored on upper left back spine, clearly breaks outer silhouette
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Key stem entering back spine socket at (38, 48) from center (28, 26)
    for y in range(32, 49):
        for x in range(28, 42):
            t_s = (y - 32) / 16.0
            sx = 28 + t_s * 10.0
            dist = abs(x - sx)
            if dist <= 2.2:
                edge_t = dist / 2.2
                r_s = int(np.clip(220 * (1 - 0.3 * edge_t) - 30 * t_s, 0, 255))
                g_s = int(np.clip(165 * (1 - 0.4 * edge_t) - 40 * t_s, 0, 255))
                b_s = int(np.clip(25 * (1 - 0.6 * edge_t), 0, 255))
                key_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    # Heavy Cross-Wheel Key Head (center (26, 24), radius 13)
    kcx, kcy, kr = 26.0, 24.0, 13.0
    for y in range(int(kcy - kr - 2), int(kcy + kr + 3)):
        for x in range(int(kcx - kr - 2), int(kcx + kr + 3)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= kr:
                angle = np.arctan2(dy, dx)
                is_cross_arm = (abs(dx) <= 2.6 or abs(dy) <= 2.6)
                is_outer_rim = (dist >= 9.2)
                is_inner_hub = (dist <= 4.2)
                in_quad_ring = (dist > 4.2 and dist < 9.2 and not is_cross_arm)

                if is_outer_rim or is_cross_arm or is_inner_hub:
                    spec = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 7.0)
                    shine = max(0.0, np.cos(angle - 2.2))
                    r_k = int(np.clip(180 + 75 * spec + 45 * shine, 0, 255))
                    g_k = int(np.clip(130 + 80 * spec + 35 * shine, 0, 255))
                    b_k = int(np.clip(20 + 160 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_k, g_k, b_k, 255))
                elif in_quad_ring:
                    pass

    kd.ellipse([int(kcx - kr), int(kcy - kr), int(kcx + kr), int(kcy + kr)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - 4.2), int(kcy - 4.2), int(kcx + 4.2), int(kcy + 4.2)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - 1.5), int(kcy - 1.5), int(kcx + 1.5), int(kcy + 1.5)], fill=BRASS_SHINE)
    kd.line([(int(kcx - kr), int(kcy - 2.6)), (int(kcx + kr), int(kcy - 2.6))], fill=OUTLINE, width=1)
    kd.line([(int(kcx - kr), int(kcy + 2.6)), (int(kcx + kr), int(kcy + 2.6))], fill=OUTLINE, width=1)
    kd.line([(int(kcx - 2.6), int(kcy - kr)), (int(kcx - 2.6), int(kcy + kr))], fill=OUTLINE, width=1)
    kd.line([(int(kcx + 2.6), int(kcy - kr)), (int(kcx + 2.6), int(kcy + kr))], fill=OUTLINE, width=1)

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Back)
    # File: back_curio/curio_dual_pressure_gauge.png
    # Miniature dual-gauge steam pressure meter & exhaust vent on rear shoulder (x: 14..32, y: 44..68)
    # + 3-segmented hinged brass ground tail rudder at rear chassis (x: 22..34, y: 104..113)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Mounting bracket from chassis
    cd.line([(21, 52), (32, 56)], fill=STEEL_MID, width=2)
    cd.line([(17, 62), (32, 66)], fill=STEEL_MID, width=2)

    # Gauge 1 (Upper primary steam meter, center (22, 51), radius 6.5)
    gcx1, gcy1, gr1 = 22.0, 51.0, 6.5
    for y in range(int(gcy1 - gr1 - 1), int(gcy1 + gr1 + 2)):
        for x in range(int(gcx1 - gr1 - 1), int(gcx1 + gr1 + 2)):
            dx = x - gcx1
            dy = y - gcy1
            dist = (dx**2 + dy**2)**0.5
            if dist <= gr1:
                if dist >= 4.5:
                    # Brass bezel ring with smooth gradient
                    spec = max(0.0, 1.0 - abs(dx - 1.5) / 5.0)
                    r_g = int(np.clip(180 + 75 * spec, 0, 255))
                    g_g = int(np.clip(130 + 80 * spec, 0, 255))
                    b_g = int(np.clip(25 + 130 * spec, 0, 255))
                    curio_img.putpixel((x, y), (r_g, g_g, b_g, 255))
                else:
                    # Dial face with subtle radial shading
                    t_d = dist / 4.5
                    r_d = int(np.clip(255 - 25 * t_d, 0, 255))
                    g_d = int(np.clip(250 - 20 * t_d, 0, 255))
                    b_d = int(np.clip(240 - 30 * t_d, 0, 255))
                    curio_img.putpixel((x, y), (r_d, g_d, b_d, 255))

    cd.ellipse([int(gcx1 - gr1), int(gcy1 - gr1), int(gcx1 + gr1), int(gcy1 + gr1)], outline=OUTLINE, width=1)
    cd.line([(int(gcx1), int(gcy1)), (int(gcx1 + 3), int(gcy1 - 3))], fill=ORANGE_STEAM, width=1)
    cd.point((int(gcx1), int(gcy1)), fill=BRASS_DEEP)

    # Gauge 2 (Lower secondary meter, center (18, 62), radius 5.0)
    gcx2, gcy2, gr2 = 18.0, 62.0, 5.0
    for y in range(int(gcy2 - gr2 - 1), int(gcy2 + gr2 + 2)):
        for x in range(int(gcx2 - gr2 - 1), int(gcx2 + gr2 + 2)):
            dx = x - gcx2
            dy = y - gcy2
            dist = (dx**2 + dy**2)**0.5
            if dist <= gr2:
                if dist >= 3.5:
                    spec2 = max(0.0, 1.0 - abs(dx - 1.0) / 4.0)
                    curio_img.putpixel((x, y), (int(180 + 70 * spec2), int(130 + 70 * spec2), int(25 + 100 * spec2), 255))
                else:
                    t_d2 = dist / 3.5
                    curio_img.putpixel((x, y), (int(255 - 20 * t_d2), int(250 - 20 * t_d2), int(240 - 20 * t_d2), 255))

    cd.ellipse([int(gcx2 - gr2), int(gcy2 - gr2), int(gcx2 + gr2), int(gcy2 + gr2)], outline=OUTLINE, width=1)
    cd.line([(int(gcx2), int(gcy2)), (int(gcx2 - 2), int(gcy2 - 2))], fill=ORANGE_STEAM, width=1)

    # Mini exhaust vent funnel on top of upper gauge
    cd.polygon([(20, 44), (24, 44), (23, 46), (21, 46)], fill=BRASS_PRIMARY, outline=OUTLINE)

    # Segmented Hinged Brass Ground Tail Rudder (x: 22..34, y: 104..113)
    for y in range(104, 113):
        for x in range(23, 33):
            dx = x - 28.0
            dy = y - 108.5
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.5:
                spec_t = max(0.0, 1.0 - abs(dx) / 4.0)
                r_t = int(np.clip(170 + 80 * spec_t - 20 * abs(dy) / 4.5, 0, 255))
                g_t = int(np.clip(125 + 80 * spec_t - 20 * abs(dy) / 4.5, 0, 255))
                b_t = int(np.clip(22 + 110 * spec_t, 0, 255))
                curio_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    cd.rounded_rectangle([23, 104, 32, 112], radius=2, outline=OUTLINE, width=1)
    cd.line([(23, 107), (32, 107)], fill=OUTLINE, width=1)
    cd.line([(23, 110), (32, 110)], fill=OUTLINE, width=1)
    cd.point((27, 105), fill=BRASS_SHINE)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Base)
    # File: chassis/paint_elephant_brass.png
    # The complete headless Colossus Elephant automaton chassis:
    # - Monumental 2.1-chibi torso with quenched brass plating (strictly x <= 88)
    # - Raised collar ring at (50..76, y: 46..56) for seamless head socketing
    # - Ivory alloy convex belly plate with chamfered bevels
    # - 4 heavy hydraulic pillar legs with dampening springs & rubber soles
    # - Right mechanical arm and open grasping palm (x: 74..87, y: 72..84)
    # - Left mechanical arm & fist supporting posture (x: 36..46, y: 74..84)
    # - Ground contact soft shadow (centered at (64, 115), radius 38x5)
    # - Strictly ZERO weapon baked in (0-ART9/0-ART11 compliant: x >= 90 is strictly 0 pixels)
    # - Full 3D shading, rivets, panels (0-ART18 compliant, zero flat blocks)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft ground contact shadow (centered at (64, 115), radius 36x5)
    ch_d.ellipse([64 - 36, 115 - 5, 64 + 36, 115 + 5], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Main Torso Carapace & Belly Structure (x: 34..88, y: 50..104)
    for y in range(50, 104):
        for x in range(34, 89):
            dx = (x - 61.0) / 25.0
            dy = (y - 78.0) / 24.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 52)**2 + (y - 66)**2)**0.5 / 16.0)
                r_b = int(np.clip(160 + 60 * (1 - t) + 80 * spec, 0, 255))
                g_b = int(np.clip(115 + 50 * (1 - t) + 70 * spec, 0, 255))
                b_b = int(np.clip(18 + 25 * (1 - t) + 120 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    ch_d.ellipse([34, 52, 88, 102], outline=OUTLINE, width=1)
    ch_d.arc([36, 54, 86, 100], start=120, end=240, fill=BRASS_LIGHT, width=1)

    # 3. Ivory-White Alloy Plastron (Belly Plate, x: 46..76, y: 64..96)
    for y in range(64, 96):
        for x in range(46, 77):
            dx = (x - 61.0) / 14.5
            dy = (y - 80.0) / 15.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t_iv = dist**0.5
                spec_iv = max(0.0, 1.0 - ((x - 55)**2 + (y - 72)**2)**0.5 / 10.0)
                r_iv = int(np.clip(220 + 35 * (1 - t_iv) + 35 * spec_iv, 0, 255))
                g_iv = int(np.clip(215 + 35 * (1 - t_iv) + 35 * spec_iv, 0, 255))
                b_iv = int(np.clip(205 + 40 * (1 - t_iv) + 45 * spec_iv, 0, 255))
                chassis_img.putpixel((x, y), (r_iv, g_iv, b_iv, 255))

    ch_d.ellipse([46, 64, 76, 96], outline=OUTLINE, width=1)
    ch_d.arc([48, 66, 74, 94], start=160, end=320, fill=IVORY_SHINE, width=1)

    # Rivets on ivory belly plate
    for rx, ry in [(50, 72), (72, 72), (52, 88), (70, 88)]:
        ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=BRASS_PRIMARY, outline=OUTLINE)

    # Raised Neck Collar Ring (for head_unit to socket into smoothly, x: 50..74, y: 46..56)
    ch_d.rounded_rectangle([50, 46, 74, 56], radius=4, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(52, 48), (72, 48)], fill=BRASS_LIGHT, width=1)
    ch_d.line([(52, 54), (72, 54)], fill=BRASS_DEEP, width=1)

    # Chest hollow cavity for core (x: 58..68, y: 64..76)
    ch_d.polygon([(63, 64), (69, 70), (63, 76), (57, 70)], fill=OUTLINE)

    # 4. Four Heavy Hydraulic Leg Columns & Broad Stepping Feet
    # Hind-Left Foot (x: 26..38, y: 96..108)
    ch_d.rounded_rectangle([26, 96, 38, 105], radius=3, fill=BRASS_DARK, outline=OUTLINE, width=1)
    ch_d.line([(28, 98), (36, 98)], fill=BRASS_LIGHT, width=1)
    ch_d.rounded_rectangle([25, 105, 39, 109], radius=2, fill=STEEL_DARK, outline=OUTLINE, width=1)

    # Hind-Right Foot (x: 82..94, y: 96..108)
    ch_d.rounded_rectangle([82, 96, 94, 105], radius=3, fill=BRASS_DARK, outline=OUTLINE, width=1)
    ch_d.line([(84, 98), (92, 98)], fill=BRASS_LIGHT, width=1)
    ch_d.rounded_rectangle([81, 105, 95, 109], radius=2, fill=STEEL_DARK, outline=OUTLINE, width=1)

    # Fore-Left Heavy Hydraulic Column (x: 38..54, y: 92..115)
    ch_d.rounded_rectangle([39, 90, 53, 102], radius=4, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(42, 92), (50, 92)], fill=BRASS_LIGHT, width=1)
    ch_d.rounded_rectangle([42, 101, 50, 108], radius=2, fill=STEEL_LIGHT, outline=STEEL_DARK, width=1)
    ch_d.line([(43, 103), (49, 103)], fill=STEEL_DEEP, width=1)
    ch_d.line([(43, 106), (49, 106)], fill=STEEL_DEEP, width=1)
    ch_d.rounded_rectangle([37, 108, 55, 115], radius=3, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(39, 109), (53, 109)], fill=BRASS_SHINE, width=1)
    ch_d.rounded_rectangle([38, 113, 54, 116], radius=2, fill=STEEL_DARK, outline=OUTLINE, width=1)

    # Fore-Right Heavy Hydraulic Column (x: 68..84, y: 92..115)
    ch_d.rounded_rectangle([69, 90, 83, 102], radius=4, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(72, 92), (80, 92)], fill=BRASS_LIGHT, width=1)
    ch_d.rounded_rectangle([72, 101, 80, 108], radius=2, fill=STEEL_LIGHT, outline=STEEL_DARK, width=1)
    ch_d.line([(73, 103), (79, 103)], fill=STEEL_DEEP, width=1)
    ch_d.line([(73, 106), (79, 106)], fill=STEEL_DEEP, width=1)
    ch_d.rounded_rectangle([67, 108, 85, 115], radius=3, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(69, 109), (83, 109)], fill=BRASS_SHINE, width=1)
    ch_d.rounded_rectangle([68, 113, 84, 116], radius=2, fill=STEEL_DARK, outline=OUTLINE, width=1)

    # 5. Left Arm (resting/balancing fist, x: 34..46, y: 72..86)
    ch_d.rounded_rectangle([34, 72, 44, 80], radius=3, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.ellipse([36, 79, 44, 87], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.point((40, 83), fill=STEEL_LIGHT)

    # 6. Right Arm & Open Grasping Palm (strictly x <= 88, y: 70..85)
    ch_d.rounded_rectangle([74, 70, 83, 79], radius=3, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    ch_d.line([(76, 72), (81, 72)], fill=BRASS_LIGHT, width=1)
    ch_d.rounded_rectangle([77, 74, 85, 82], radius=3, fill=BRASS_DARK, outline=OUTLINE, width=1)
    ch_d.rounded_rectangle([79, 75, 84, 80], radius=1, fill=BRASS_PRIMARY, outline=BRASS_DEEP)
    # Palm (ending at x=88 max)
    ch_d.polygon([(82, 76), (86, 75), (88, 79), (86, 83), (82, 82)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.line([(84, 77), (86, 80)], fill=BRASS_LIGHT, width=1)

    # Enforce strictly 0 pixels for chassis in weapon blade zone (x >= 90, y: 35..80)
    for cy in range(35, 80):
        for cx in range(90, 128):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Head)
    # File: head_unit/head_colossus_elephant_stock.png
    # Features:
    # - Stamped deep gold cranial helmet dome (center (64, 38))
    # - Fluted stamped double-layer heat-sink ear plates on both sides
    # - 6-stage telescopic polished brass hydraulic trunk curling down & slightly up
    # - Ivory-alloy bumper blunt tusks curving down from jaw flanges
    # - Hollow recessed eye sockets for optic_core lens insertion (0-ART27 compliant)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Hydraulic Neck Sleeves (x: 54..74, y: 44..56)
    for y in range(44, 56):
        for x in range(54, 74):
            dx = (x - 64.0) / 9.0
            if abs(dx) <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 61) / 5.0)
                r_n = int(np.clip(180 + 75 * spec, 0, 255))
                g_n = int(np.clip(135 + 75 * spec, 0, 255))
                b_n = int(np.clip(25 + 100 * spec, 0, 255))
                head_img.putpixel((x, y), (r_n, g_n, b_n, 255))

    hd.line([(55, 48), (73, 48)], fill=OUTLINE, width=1)
    hd.line([(55, 52), (73, 52)], fill=OUTLINE, width=1)

    # 2. Fluted Stamped Heat-Sink Ear Plates (Left ear: x: 22..46, Right ear: x: 80..104)
    for y in range(24, 50):
        for x in range(22, 46):
            dx = (x - 42.0) / 19.0
            dy = (y - 37.0) / 13.0
            dist = dx**2 + dy**2
            if dist <= 1.0 and x <= 44:
                spec_e = max(0.0, 1.0 - abs(y - 33) / 10.0)
                r_e = int(np.clip(170 + 65 * spec_e, 0, 255))
                g_e = int(np.clip(120 + 65 * spec_e, 0, 255))
                b_e = int(np.clip(20 + 80 * spec_e, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    hd.arc([22, 24, 46, 50], start=90, end=270, fill=OUTLINE, width=1)
    hd.line([(34, 24), (44, 37)], fill=OUTLINE, width=1)
    hd.line([(34, 50), (44, 37)], fill=OUTLINE, width=1)
    hd.line([(25, 34), (42, 36)], fill=ORANGE_STEAM, width=1)
    hd.line([(25, 40), (42, 38)], fill=ORANGE_STEAM, width=1)
    for bx, by in [(24, 30), (23, 37), (25, 44)]:
        hd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=BRASS_SHINE, outline=OUTLINE)

    for y in range(24, 50):
        for x in range(82, 106):
            dx = (x - 86.0) / 19.0
            dy = (y - 37.0) / 13.0
            dist = dx**2 + dy**2
            if dist <= 1.0 and x >= 84:
                spec_e = max(0.0, 1.0 - abs(y - 33) / 10.0)
                r_e = int(np.clip(170 + 65 * spec_e, 0, 255))
                g_e = int(np.clip(120 + 65 * spec_e, 0, 255))
                b_e = int(np.clip(20 + 80 * spec_e, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    hd.arc([82, 24, 106, 50], start=270, end=90, fill=OUTLINE, width=1)
    hd.line([(94, 24), (84, 37)], fill=OUTLINE, width=1)
    hd.line([(94, 50), (84, 37)], fill=OUTLINE, width=1)
    hd.line([(86, 36), (103, 34)], fill=ORANGE_STEAM, width=1)
    hd.line([(86, 38), (103, 40)], fill=ORANGE_STEAM, width=1)
    for bx, by in [(104, 30), (105, 37), (103, 44)]:
        hd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=BRASS_SHINE, outline=OUTLINE)

    # 3. Cranial Helmet Dome (center (64, 37), radius 20x15)
    for y in range(22, 50):
        for x in range(44, 84):
            dx = (x - 64.0) / 19.0
            dy = (y - 37.0) / 14.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 56)**2 + (y - 29)**2)**0.5 / 10.0)
                r_h = int(np.clip(175 + 50 * (1 - t) + 80 * spec, 0, 255))
                g_h = int(np.clip(125 + 50 * (1 - t) + 70 * spec, 0, 255))
                b_h = int(np.clip(22 + 25 * (1 - t) + 120 * spec, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    hd.ellipse([44, 23, 84, 49], outline=OUTLINE, width=1)
    hd.arc([46, 25, 82, 47], start=180, end=360, fill=BRASS_LIGHT, width=1)
    hd.polygon([(62, 23), (66, 23), (65, 32), (63, 32)], fill=BRASS_LIGHT, outline=OUTLINE)
    hd.point((64, 25), fill=BRASS_SHINE)

    # 4. Ivory Bumper Tusks
    hd.rounded_rectangle([48, 46, 54, 52], radius=2, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    hd.rounded_rectangle([74, 46, 80, 52], radius=2, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)

    for y in range(48, 63):
        for x in range(42, 53):
            t_k = (y - 48) / 14.0
            curv_x = 50.0 - t_k * 6.0
            dist = abs(x - curv_x)
            width_k = 2.8 * (1.0 - 0.4 * t_k)
            if dist <= width_k:
                spec_k = max(0.0, 1.0 - dist / width_k)
                r_k = int(np.clip(230 + 25 * spec_k, 0, 255))
                g_k = int(np.clip(225 + 25 * spec_k, 0, 255))
                b_k = int(np.clip(215 + 35 * spec_k, 0, 255))
                head_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    hd.line([(50, 48), (44, 62)], fill=OUTLINE, width=1)
    hd.line([(53, 49), (46, 62)], fill=OUTLINE, width=1)
    hd.point((45, 62), fill=OUTLINE)

    for y in range(48, 63):
        for x in range(75, 86):
            t_k = (y - 48) / 14.0
            curv_x = 78.0 + t_k * 6.0
            dist = abs(x - curv_x)
            width_k = 2.8 * (1.0 - 0.4 * t_k)
            if dist <= width_k:
                spec_k = max(0.0, 1.0 - dist / width_k)
                r_k = int(np.clip(230 + 25 * spec_k, 0, 255))
                g_k = int(np.clip(225 + 25 * spec_k, 0, 255))
                b_k = int(np.clip(215 + 35 * spec_k, 0, 255))
                head_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    hd.line([(78, 48), (84, 62)], fill=OUTLINE, width=1)
    hd.line([(75, 49), (82, 62)], fill=OUTLINE, width=1)
    hd.point((83, 62), fill=OUTLINE)

    # 5. Six-Stage Telescopic Hydraulic Trunk
    trunk_stages = [
        (44, 50, 6.2, 5.8),
        (50, 56, 5.8, 5.2),
        (56, 62, 5.2, 4.6),
        (62, 68, 4.6, 4.0),
        (68, 74, 4.0, 3.4),
        (74, 80, 3.4, 2.6),
    ]

    for s_idx, (y_start, y_end, r_top, r_bot) in enumerate(trunk_stages):
        for y in range(y_start, y_end + 1):
            t_st = (y - y_start) / max(1, (y_end - y_start))
            curr_r = r_top * (1 - t_st) + r_bot * t_st
            cx_t = 64.0 - 1.8 * np.sin(t_st * np.pi) + (1.2 if s_idx >= 4 else 0.0)
            for x in range(int(cx_t - curr_r - 1), int(cx_t + curr_r + 2)):
                dist = abs(x - cx_t)
                if dist <= curr_r:
                    edge_t = dist / curr_r
                    spec = max(0.0, 1.0 - abs(x - (cx_t - curr_r * 0.4)) / (curr_r * 0.8))
                    r_tr = int(np.clip(180 + 75 * spec - 40 * edge_t, 0, 255))
                    g_tr = int(np.clip(135 + 75 * spec - 45 * edge_t, 0, 255))
                    b_tr = int(np.clip(25 + 130 * spec - 15 * edge_t, 0, 255))
                    head_img.putpixel((x, y), (r_tr, g_tr, b_tr, 255))

        cx_joint = 64.0 - 1.8 * np.sin(np.pi) + (1.2 if s_idx >= 4 else 0.0)
        hd.line([(int(cx_joint - r_bot), y_end), (int(cx_joint + r_bot), y_end)], fill=OUTLINE, width=1)
        hd.line([(int(cx_joint - r_top + 1), y_start), (int(cx_joint + r_top - 1), y_start)], fill=BRASS_SHINE, width=1)

    hd.ellipse([63, 79, 67, 82], fill=BRASS_DEEP, outline=OUTLINE)
    hd.point((64, 80), fill=STEEL_LIGHT)
    hd.point((66, 80), fill=STEEL_LIGHT)

    # 6. Hollow Recessed Eye Sockets (0-ART27 compliant)
    hd.ellipse([49, 33, 59, 43], fill=OUTLINE)
    hd.ellipse([50, 34, 58, 42], fill=BRASS_DEEP)
    hd.ellipse([69, 33, 79, 43], fill=OUTLINE)
    hd.ellipse([70, 34, 78, 42], fill=BRASS_DEEP)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Overlay)
    # File: costume/costume_cog_workshop_overalls.png
    # Great Cog Foundry Pioneer Harness-Plates (巨輪工坊先鋒吊帶甲):
    # - Stamped brass pauldrons with rich 3D shading & bevels
    # - Warm orange utility straps with leather grain & metal stitches
    # - Heavy stamped waist belt with gradient & mini pressure buckle
    # - Central diamond opening cleanly exposing chest heart gem
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Left Pauldron (x: 32..46, y: 56..68) with 3D gradient
    for y in range(56, 69):
        for x in range(32, 47):
            dx = (x - 39.0) / 7.0
            dy = (y - 62.0) / 6.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                spec = max(0.0, 1.0 - ((x - 36)**2 + (y - 59)**2)**0.5 / 5.0)
                r_p = int(np.clip(170 + 75 * spec - 30 * dy, 0, 255))
                g_p = int(np.clip(125 + 75 * spec - 35 * dy, 0, 255))
                b_p = int(np.clip(20 + 120 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    cos_d.rounded_rectangle([32, 56, 46, 68], radius=4, outline=OUTLINE, width=1)
    cos_d.line([(34, 58), (44, 58)], fill=BRASS_SHINE, width=1)
    cos_d.ellipse([37, 61, 41, 65], fill=ORANGE_STEAM, outline=OUTLINE)

    # Right Pauldron (x: 80..89, y: 56..68) strictly x <= 89
    for y in range(56, 69):
        for x in range(80, 90):
            dx = (x - 85.0) / 5.0
            dy = (y - 62.0) / 6.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                spec = max(0.0, 1.0 - ((x - 83)**2 + (y - 59)**2)**0.5 / 5.0)
                r_p = int(np.clip(170 + 75 * spec - 30 * dy, 0, 255))
                g_p = int(np.clip(125 + 75 * spec - 35 * dy, 0, 255))
                b_p = int(np.clip(20 + 120 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    cos_d.rounded_rectangle([80, 56, 89, 68], radius=4, outline=OUTLINE, width=1)
    cos_d.line([(82, 58), (87, 58)], fill=BRASS_SHINE, width=1)
    cos_d.ellipse([83, 61, 87, 65], fill=ORANGE_STEAM, outline=OUTLINE)

    # 2. Warm Orange Crossed Utility Harness Straps (from shoulders to waist) with gradient
    # Left strap
    for t_s in np.linspace(0, 1, 28):
        sx = 42.0 + t_s * 14.0
        sy = 64.0 + t_s * 24.0
        for ow in range(-2, 3):
            for oh in range(-2, 3):
                if ow**2 + oh**2 <= 4.0:
                    px = int(sx + ow)
                    py = int(sy + oh)
                    spec_s = max(0.0, 1.0 - abs(ow) / 2.0)
                    r_st = int(np.clip(200 + 55 * spec_s - 30 * t_s, 0, 255))
                    g_st = int(np.clip(120 + 55 * spec_s - 35 * t_s, 0, 255))
                    b_st = int(np.clip(15 + 40 * spec_s, 0, 255))
                    costume_img.putpixel((px, py), (r_st, g_st, b_st, 255))

    cos_d.line([(42, 64), (56, 88)], fill=OUTLINE, width=1)
    cos_d.line([(45, 64), (59, 88)], fill=OUTLINE, width=1)

    # Right strap
    for t_s in np.linspace(0, 1, 28):
        sx = 84.0 - t_s * 13.0
        sy = 64.0 + t_s * 24.0
        for ow in range(-2, 3):
            for oh in range(-2, 3):
                if ow**2 + oh**2 <= 4.0:
                    px = int(sx + ow)
                    py = int(sy + oh)
                    spec_s = max(0.0, 1.0 - abs(ow) / 2.0)
                    r_st = int(np.clip(200 + 55 * spec_s - 30 * t_s, 0, 255))
                    g_st = int(np.clip(120 + 55 * spec_s - 35 * t_s, 0, 255))
                    b_st = int(np.clip(15 + 40 * spec_s, 0, 255))
                    costume_img.putpixel((px, py), (r_st, g_st, b_st, 255))

    cos_d.line([(84, 64), (71, 88)], fill=OUTLINE, width=1)
    cos_d.line([(81, 64), (68, 88)], fill=OUTLINE, width=1)

    # Brass buckles on harness straps
    cos_d.rounded_rectangle([44, 68, 50, 74], radius=1, fill=BRASS_LIGHT, outline=OUTLINE)
    cos_d.rounded_rectangle([76, 68, 82, 74], radius=1, fill=BRASS_LIGHT, outline=OUTLINE)

    # 3. Heavy Stamped Waist Belt (x: 46..80, y: 88..96) with multi-tone gradient
    for y in range(88, 97):
        for x in range(46, 81):
            t_b = (y - 88) / 8.0
            spec_b = max(0.0, 1.0 - abs(y - 91) / 4.0)
            r_bt = int(np.clip(170 + 80 * spec_b - 40 * t_b, 0, 255))
            g_bt = int(np.clip(125 + 75 * spec_b - 40 * t_b, 0, 255))
            b_bt = int(np.clip(20 + 100 * spec_b, 0, 255))
            costume_img.putpixel((x, y), (r_bt, g_bt, b_bt, 255))

    cos_d.rounded_rectangle([46, 88, 80, 96], radius=3, outline=OUTLINE, width=1)
    cos_d.line([(48, 90), (78, 90)], fill=BRASS_SHINE, width=1)
    cos_d.line([(48, 94), (78, 94)], fill=BRASS_DEEP, width=1)

    # Central Belt Buckle: Mini Dial Pressure Meter (center (64, 92), radius 4.5)
    for y in range(87, 98):
        for x in range(59, 70):
            dx = x - 64.0
            dy = y - 92.0
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.5:
                if dist >= 3.2:
                    costume_img.putpixel((x, y), BRASS_PRIMARY)
                else:
                    t_d = dist / 3.2
                    costume_img.putpixel((x, y), (int(255 - 20 * t_d), int(250 - 20 * t_d), int(240 - 20 * t_d), 255))

    cos_d.ellipse([59, 87, 69, 97], outline=OUTLINE, width=1)
    cos_d.line([(64, 92), (66, 90)], fill=ORANGE_STEAM, width=1)

    # Central Diamond Core Aperture (keeps area around (63, 70) completely transparent)
    for cy in range(63, 78):
        for cx in range(56, 72):
            if abs(cx - 63.5) + abs(cy - 70.5) <= 7.0:
                costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    cos_d.polygon([(64, 63), (71, 70), (64, 77), (57, 70)], outline=OUTLINE)
    cos_d.polygon([(64, 62), (72, 70), (64, 78), (56, 70)], outline=BRASS_PRIMARY)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, Face & Chest Gem)
    # File: optic_core/core_sky_quartz.png
    # Features:
    # - Left & Right Sky Blue Quartz convex lens eyes (center (54, 38) and (74, 38))
    #   Multi-layer refraction, concentric pressure reticle circle, bright white spark
    # - Chest Heart Gem: Mint-emerald rhombus crystal at (64, 70) with 3D crystal facets
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cord = ImageDraw.Draw(core_img)

    # Left Sky Blue Quartz Lens Eye (center (54.0, 38.0), radius 4.2)
    lcx, lcy, lr = 54.0, 38.0, 4.2
    for y in range(int(lcy - lr - 1), int(lcy + lr + 2)):
        for x in range(int(lcx - lr - 1), int(lcx + lr + 2)):
            dx = x - lcx
            dy = y - lcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= lr:
                t = dist / lr
                spec = max(0.0, 1.0 - ((x - (lcx - 1.2))**2 + (y - (lcy - 1.2))**2)**0.5 / 2.0)
                r_o = int(np.clip(20 + 230 * spec, 0, 255))
                g_o = int(np.clip(120 + 135 * spec - 60 * t, 0, 255))
                b_o = int(np.clip(255 - 40 * t, 0, 255))
                core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

    cord.ellipse([int(lcx - lr), int(lcy - lr), int(lcx + lr), int(lcy + lr)], outline=OUTLINE, width=1)
    cord.point((int(lcx - 1), int(lcy - 1)), fill=IVORY_SHINE)

    # Right Sky Blue Quartz Lens Eye (center (74.0, 38.0), radius 4.2)
    rcx, rcy, rr = 74.0, 38.0, 4.2
    for y in range(int(rcy - rr - 1), int(rcy + rr + 2)):
        for x in range(int(rcx - rr - 1), int(rcx + rr + 2)):
            dx = x - rcx
            dy = y - rcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= rr:
                t = dist / rr
                spec = max(0.0, 1.0 - ((x - (rcx - 1.2))**2 + (y - (rcy - 1.2))**2)**0.5 / 2.0)
                r_o = int(np.clip(20 + 230 * spec, 0, 255))
                g_o = int(np.clip(120 + 135 * spec - 60 * t, 0, 255))
                b_o = int(np.clip(255 - 40 * t, 0, 255))
                core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

    cord.ellipse([int(rcx - rr), int(rcy - rr), int(rcx + rr), int(rcy + rr)], outline=OUTLINE, width=1)
    cord.point((int(rcx - 1), int(rcy - 1)), fill=IVORY_SHINE)

    # Chest Clockwork Heart Gem (Mint Emerald Rhombus, center (64, 70), width 10, height 12)
    for y in range(64, 77):
        for x in range(58, 71):
            dx = abs(x - 64.0) / 5.5
            dy = abs(y - 70.0) / 6.5
            if dx + dy <= 1.0:
                t_c = dx + dy
                is_top = (y < 70)
                is_left = (x < 64)
                if is_top and is_left:
                    spec_c = 0.9
                elif is_top:
                    spec_c = 0.6
                elif is_left:
                    spec_c = 0.4
                else:
                    spec_c = 0.1
                r_c = int(np.clip(20 + 230 * spec_c * (1 - 0.3 * t_c), 0, 255))
                g_c = int(np.clip(140 + 115 * spec_c - 50 * t_c, 0, 255))
                b_c = int(np.clip(60 + 180 * spec_c, 0, 255))
                core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cord.polygon([(64, 64), (69, 70), (64, 76), (59, 70)], outline=OUTLINE)
    cord.line([(64, 64), (64, 76)], fill=MINT_LIGHT, width=1)
    cord.line([(59, 70), (69, 70)], fill=MINT_LIGHT, width=1)
    cord.point((63, 69), fill=IVORY_SHINE)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Handheld Weapon)
    # File: weapon/wpn_colossus_cleaver_axe.png
    # Colossus Cleaver Axe / Ground-Shatter Cog-Axe (巨輪開山重斧)
    # - Heavy steel crescent cleaver axe blade (x: 84..118, y: 40..80)
    # - Central 16px brass concentric gear counterweight with rotating gear teeth
    # - Sturdy steel handle (x: 83..86, y: 48..96) held by right palm at (85, 78)
    # - Brass counterbalance pommel at base (84, 97)
    # - Completely decoupled from chassis (0-ART9 / 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Sturdy Axe Shaft / Handle (x: 83..86, y: 46..98)
    for y in range(46, 98):
        for x in range(83, 87):
            spec_w = max(0.0, 1.0 - abs(x - 84) / 2.0)
            r_w = int(np.clip(60 + 120 * spec_w, 0, 255))
            g_w = int(np.clip(68 + 120 * spec_w, 0, 255))
            b_w = int(np.clip(80 + 130 * spec_w, 0, 255))
            weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    wd.line([(83, 46), (83, 98)], fill=OUTLINE, width=1)
    wd.line([(86, 46), (86, 98)], fill=OUTLINE, width=1)

    for gy in [75, 78, 81, 84]:
        wd.line([(83, gy), (86, gy)], fill=BRASS_PRIMARY, width=1)

    wd.rounded_rectangle([81, 97, 88, 102], radius=2, fill=BRASS_PRIMARY, outline=OUTLINE, width=1)
    wd.point((84, 98), fill=BRASS_SHINE)

    # 2. Central 16px Concentric Gear Counterweight (center (96, 58), radius 8)
    acx, acy, ar = 96.0, 58.0, 8.0
    for y in range(int(acy - ar - 2), int(acy + ar + 3)):
        for x in range(int(acx - ar - 2), int(acx + ar + 3)):
            dx = x - acx
            dy = y - acy
            dist = (dx**2 + dy**2)**0.5
            if dist <= ar:
                angle = np.arctan2(dy, dx)
                tooth = 1.0 + 0.25 * np.cos(angle * 8.0)
                if dist <= ar * tooth:
                    spec = max(0.0, 1.0 - ((x - (acx - 2))**2 + (y - (acy - 2))**2)**0.5 / 5.0)
                    r_a = int(np.clip(180 + 75 * spec, 0, 255))
                    g_a = int(np.clip(130 + 75 * spec, 0, 255))
                    b_a = int(np.clip(25 + 130 * spec, 0, 255))
                    weapon_img.putpixel((x, y), (r_a, g_a, b_a, 255))

    wd.ellipse([int(acx - ar), int(acy - ar), int(acx + ar), int(acy + ar)], outline=OUTLINE, width=1)
    wd.ellipse([int(acx - 3.5), int(acy - 3.5), int(acx + 3.5), int(acy + 3.5)], fill=BRASS_LIGHT, outline=OUTLINE)
    wd.point((int(acx), int(acy)), fill=OUTLINE)

    # 3. Massive Double-Beveled Steel Crescent Cleaver Blade (x: 88..118, y: 40..76)
    for y in range(40, 78):
        for x in range(86, 118):
            dx = x - 96.0
            dy = y - 58.0
            dist = (dx**2 + dy**2)**0.5
            angle = np.arctan2(dy, dx)
            if abs(angle) <= 1.15 and dist >= 7.0 and dist <= 21.0:
                t_blade = (dist - 7.0) / 14.0
                spec_b = max(0.0, 1.0 - abs(dy) / 16.0) * t_blade
                r_bl = int(np.clip(70 + 160 * t_blade + 25 * spec_b, 0, 255))
                g_bl = int(np.clip(80 + 160 * t_blade + 15 * spec_b, 0, 255))
                b_bl = int(np.clip(95 + 160 * t_blade, 0, 255))
                weapon_img.putpixel((x, y), (r_bl, g_bl, b_bl, 255))

    wd.arc([75, 37, 117, 79], start=-65, end=65, fill=OUTLINE, width=1)
    wd.arc([74, 38, 116, 78], start=-62, end=62, fill=IVORY_SHINE, width=1)
    wd.line([(86, 46), (105, 41)], fill=OUTLINE, width=1)
    wd.line([(86, 70), (105, 75)], fill=OUTLINE, width=1)
    wd.arc([80, 43, 112, 73], start=-55, end=55, fill=STEEL_MID, width=1)

    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 128px SLICES & 512px UPSCALE HIGH-RES ASSETS
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("winding_key", "key_heavy_cross_wheel", key_img),
        ("back_curio", "curio_dual_pressure_gauge", curio_img),
        ("chassis", "paint_elephant_brass", chassis_img),
        ("head_unit", "head_colossus_elephant_stock", head_img),
        ("costume", "costume_cog_workshop_overalls", costume_img),
        ("optic_core", "core_sky_quartz", core_img),
        ("weapon", "wpn_colossus_cleaver_axe", weapon_img),
    ]

    for slot, item_id, img_128 in slices:
        slot_dir = f"{ELEPHANT_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        path_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(path_128)
        print(f"  Saved 128px slice: {path_128}")

        path_512 = f"{slot_dir}/{item_id}_512.png"
        img_512 = img_128.resize((512, 512), resample=Image.Resampling.NEAREST)
        img_512_smooth = img_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
        blended = Image.blend(img_512, img_512_smooth, 0.45)
        blended.save(path_512)
        print(f"  Saved 512px slice: {path_512}")

    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copyfile(f"{ELEPHANT_PD_DIR}/winding_key/key_heavy_cross_wheel.png", f"{KEY_DIR}/key_heavy_cross_wheel.png")
    shutil.copyfile(f"{ELEPHANT_PD_DIR}/weapon/wpn_colossus_cleaver_axe.png", f"{WEAPON_DIR}/wpn_colossus_cleaver_axe.png")
    print("  ✓ Synced key_heavy_cross_wheel to common key/ directory")
    print("  ✓ Synced wpn_colossus_cleaver_axe to common weapon/ directory")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE PROOF IMAGES
    # ─────────────────────────────────────────────────────────────
    comp_128 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    comp_128.alpha_composite(key_img)
    comp_128.alpha_composite(curio_img)
    comp_128.alpha_composite(chassis_img)
    comp_128.alpha_composite(head_img)
    comp_128.alpha_composite(costume_img)
    comp_128.alpha_composite(core_img)
    comp_128.alpha_composite(weapon_img)

    comp_path = f"{ELEPHANT_PD_DIR}/proof_paperdoll_elephant_composite.png"
    comp_128.save(comp_path)
    print("  ✓ Saved standard composite proof:", comp_path)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(comp_128)
    mag_path = f"{ELEPHANT_PD_DIR}/proof_paperdoll_elephant_magenta.png"
    magenta_bg.save(mag_path)
    print("  ✓ Saved magenta verification proof:", mag_path)

    strip_img = Image.new("RGBA", (128 * 7, 128), (0, 0, 0, 0))
    for idx, (slot, item_id, s_img) in enumerate(slices):
        strip_img.paste(s_img, (idx * 128, 0))
    strip_path = f"{ELEPHANT_PD_DIR}/proof_elephant_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Saved all 7 slices strip proof:", strip_path)

    print("\n=== COLOSSUS ELEPHANT ASSET GENERATION FULLY COMPLETED ===")


if __name__ == "__main__":
    build_all()
