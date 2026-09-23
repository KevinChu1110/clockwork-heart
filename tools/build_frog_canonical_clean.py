#!/usr/bin/env python3
"""
build_frog_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Spring-Leg Frog (碧簧蛙 / 碧簧蛙) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/SPRING_FROG_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh, zero slime, all metal/enamel/springs, brass key)
- references/art_direction.md (Dopamine high-saturation palette, clean enamel/brass, deep outline)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r
- Benchmarked directly against Xuanji Tortoise (玄機龜) and Colossus Elephant (鋼岳象) standards.
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
FROG_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/frog"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Dawson Day 258 Series & Spring Frog Proposal)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Emerald Enamel (#4ED86A)
EMERALD_PRIMARY = (78, 216, 106, 255)  # Mint Emerald Green Enamel
EMERALD_LIGHT = (135, 240, 160, 255)   # Specular highlight
EMERALD_SHINE = (195, 255, 210, 255)   # Hot highlight
EMERALD_DARK = (36, 140, 62, 255)      # Cel shadow
EMERALD_DEEP = (18, 78, 35, 255)       # Deep seam shadow

# Secondary: Stamped Lemon Yellow (#FFD028)
YELLOW_PRIMARY = (255, 208, 40, 255)   # Stamped Lemon Yellow
YELLOW_LIGHT = (255, 235, 115, 255)
YELLOW_SHINE = (255, 250, 185, 255)
YELLOW_DARK = (195, 145, 18, 255)
YELLOW_DEEP = (125, 85, 10, 255)

# Accent: High-torque Warm Orange (#FFA010)
ORANGE_ACCENT = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 205, 80, 255)
ORANGE_DARK = (190, 95, 10, 255)
ORANGE_DEEP = (120, 50, 5, 255)

# Detail: Sky Blue Quartz (#38A0FF)
SKY_BLUE = (56, 160, 255, 255)
SKY_LIGHT = (155, 215, 255, 255)
SKY_DARK = (20, 100, 190, 255)
SKY_DEEP = (10, 50, 120, 255)

# Metal: Polished Tianyuan Brass Gold (#D4A017)
BRASS_GOLD = (212, 160, 23, 255)
BRASS_LIGHT = (255, 225, 95, 255)
BRASS_SHINE = (255, 250, 175, 255)
BRASS_DARK = (150, 105, 12, 255)
BRASS_DEEP = (90, 60, 8, 255)

# Manganese Spring Steel / Hydraulic Rods (#708090)
STEEL_LIGHT = (180, 195, 215, 255)
STEEL_MID = (110, 122, 140, 255)
STEEL_DARK = (60, 68, 80, 255)
STEEL_DEEP = (36, 42, 52, 255)

WHITE_SHINE = (255, 255, 255, 255)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL SPRING FROG SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back)
    # File: winding_key/key_twin_wing_concentric.png
    # Double butterfly-wing concentric stamped brass key on upper back
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Key shaft/stem entering spine socket at (38, 48) from center (28, 26)
    for y in range(32, 50):
        for x in range(26, 42):
            t_s = (y - 32) / 18.0
            sx = 28 + t_s * 10.0
            dist = abs(x - sx)
            if dist <= 2.2:
                edge_t = dist / 2.2
                r_s = int(np.clip(212 * (1 - 0.3 * edge_t) - 30 * t_s, 0, 255))
                g_s = int(np.clip(160 * (1 - 0.4 * edge_t) - 40 * t_s, 0, 255))
                b_s = int(np.clip(23 * (1 - 0.6 * edge_t), 0, 255))
                key_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    # Center socket boss at (38, 48)
    kd.ellipse([35, 45, 41, 51], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([36, 46, 40, 50], fill=BRASS_GOLD)

    # Twin-Wing Concentric Head (center (26, 25))
    kcx, kcy = 26.0, 25.0
    r_hub = 5.0
    r_wing = 14.0

    # Draw left and right concentric butterfly wings
    for y in range(int(kcy - r_wing - 2), int(kcy + r_wing + 3)):
        for x in range(int(kcx - r_wing - 2), int(kcx + r_wing + 3)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5

            if dist <= r_wing:
                # Shape butterfly wing lobes: left lobe (dx < 0), right lobe (dx > 0)
                # Cutout slot top and bottom for butterfly silhouette
                angle = np.arctan2(dy, dx)
                is_vertical_cutout = (abs(dx) < 2.2 and abs(dy) > r_hub)
                is_concentric_hole = (dist > 7.5 and dist < 11.2 and abs(dx) > 4.5)

                if dist <= r_hub:
                    # Central Brass Hub
                    spec = max(0.0, 1.0 - ((x - (kcx - 1.5))**2 + (y - (kcy - 1.5))**2)**0.5 / 3.5)
                    r_v = int(np.clip(212 + 43 * spec, 0, 255))
                    g_v = int(np.clip(160 + 80 * spec, 0, 255))
                    b_v = int(np.clip(23 + 180 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_v, g_v, b_v, 255))
                elif not is_vertical_cutout and not is_concentric_hole:
                    # Outer brass plate with specular highlight
                    spec = max(0.0, 1.0 - ((x - (kcx - 5))**2 + (y - (kcy - 5))**2)**0.5 / 9.0)
                    shine = max(0.0, np.cos(angle - 2.3))
                    r_v = int(np.clip(180 + 75 * spec + 40 * shine, 0, 255))
                    g_v = int(np.clip(135 + 85 * spec + 35 * shine, 0, 255))
                    b_v = int(np.clip(18 + 160 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Outlines for key
    kd.ellipse([int(kcx - r_wing), int(kcy - r_wing), int(kcx + r_wing), int(kcy + r_wing)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - r_hub), int(kcy - r_hub), int(kcx + r_hub), int(kcy + r_hub)], outline=OUTLINE, width=1)
    # Left concentric hole outline
    kd.ellipse([int(kcx - 11), int(kcy - 4.5), int(kcx - 7.5), int(kcy + 4.5)], outline=OUTLINE, width=1)
    # Right concentric hole outline
    kd.ellipse([int(kcx + 7.5), int(kcy - 4.5), int(kcx + 11), int(kcy + 4.5)], outline=OUTLINE, width=1)
    # Center orange accent pin
    kd.ellipse([int(kcx - 1.5), int(kcy - 1.5), int(kcx + 1.5), int(kcy + 1.5)], fill=ORANGE_ACCENT)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Back)
    # File: back_curio/curio_lotus_leaf_parasol.png
    # Micro clockwork lotus leaf parasol floating / mounted behind left back
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Parasol canopy center at (18, 48), radius 11
    pcx, pcy, pr = 18.0, 48.0, 11.0

    # 1. Slender polished brass shaft/stem running from canopy center (18, 48) down to back bracket (27, 82)
    for y in range(48, 83):
        t_p = (y - 48) / 34.0
        px = 18.0 + t_p * 9.0
        for x in range(int(px - 1), int(px + 2)):
            cd.point((x, y), fill=BRASS_GOLD if abs(x - px) < 0.6 else OUTLINE)

    # 2. Back bracket clamp at (27, 82)
    cd.rectangle([25, 79, 29, 85], fill=BRASS_DARK, outline=OUTLINE)
    cd.point((26, 81), fill=BRASS_SHINE)

    # 3. Lotus Leaf Parasol Canopy (scalloped emerald enamel plate)
    for y in range(int(pcy - pr - 2), int(pcy + pr + 3)):
        for x in range(int(pcx - pr - 2), int(pcx + pr + 3)):
            dx = x - pcx
            dy = (y - pcy) * 1.25  # Perspective squish
            dist = (dx**2 + dy**2)**0.5
            if dist <= pr:
                angle = np.arctan2(dy, dx)
                # 6 scalloped petal waves
                scallop = 1.0 + 0.12 * np.cos(6 * angle)
                if dist <= pr * scallop:
                    spec = max(0.0, 1.0 - ((x - (pcx - 3))**2 + (y - (pcy - 3))**2)**0.5 / 6.0)
                    shine = max(0.0, np.cos(angle - 2.4))
                    r_c = int(np.clip(78 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    g_c = int(np.clip(216 * (0.8 + 0.3 * spec) + 39 * shine, 0, 255))
                    b_c = int(np.clip(106 * (0.8 + 0.3 * spec) + 80 * spec, 0, 255))
                    curio_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Radial brass vein ribs (6 lines radiating from center)
    for i in range(6):
        rad_ang = i * (np.pi / 3.0) + 0.2
        ex = int(pcx + (pr - 1) * np.cos(rad_ang))
        ey = int(pcy + (pr - 1) * np.sin(rad_ang) * 0.8)
        cd.line([(int(pcx), int(pcy)), (ex, ey)], fill=BRASS_GOLD, width=1)

    # Canopy rim outline
    cd.ellipse([int(pcx - pr), int(pcy - pr * 0.8), int(pcx + pr), int(pcy + pr * 0.8)], outline=OUTLINE, width=1)

    # Central golden finial spike & dewdrop jewel
    cd.ellipse([int(pcx - 3), int(pcy - 3), int(pcx + 3), int(pcy + 3)], fill=BRASS_GOLD, outline=OUTLINE)
    cd.ellipse([int(pcx - 1.5), int(pcy - 1.5), int(pcx + 1.5), int(pcy + 1.5)], fill=SKY_BLUE)
    cd.point((int(pcx - 1), int(pcy - 1)), fill=WHITE_SHINE)
    cd.line([(int(pcx), int(pcy - 3)), (int(pcx), int(pcy - 6))], fill=BRASS_GOLD, width=1)
    cd.point((int(pcx), int(pcy - 7)), fill=WHITE_SHINE)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Base)
    # File: chassis/paint_frog_emerald.png
    # Complete headless automaton frog chassis:
    # - Low-gravity crouched stance with dual manganese spring legs
    # - Three-pronged stamped brass webbed suction feet resting firmly on ground
    # - Stamped lemon yellow chest/belly base (#FFD028)
    # - Mint emerald enamel flank armor and thigh casings (#4ED86A)
    # - Neck collar mounting socket (y=48..56, x=48..78) with brass rivets
    # - Extended left arm for balance; right cupped mechanical wrist ready to hold weapon
    # - Soft contact ground shadow at (64, 116)
    # - Strictly ZERO weapon baked in (0-ART9, 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow (centered at (64, 116), radius 34x5)
    ch_d.ellipse([64 - 34, 116 - 4, 64 + 34, 116 + 5], fill=(31, 26, 58, 125))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Hind Limbs: Folded High-Tension Manganese Spring Legs
    # Left Thigh & Spring Plate (x: 26..46, y: 74..104)
    for y in range(74, 105):
        for x in range(26, 48):
            dx = (x - 36) / 10.0
            dy = (y - 88) / 14.0
            if dx**2 + dy**2 <= 1.0:
                t = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - ((x - 32)**2 + (y - 82)**2)**0.5 / 7.0)
                r_th = int(np.clip(78 * (0.8 + 0.3 * spec) - 20 * t, 0, 255))
                g_th = int(np.clip(216 * (0.8 + 0.3 * spec) - 20 * t, 0, 255))
                b_th = int(np.clip(106 * (0.8 + 0.3 * spec) + 80 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_th, g_th, b_th, 255))

    # Right Thigh & Spring Plate (x: 78..98, y: 74..104)
    for y in range(74, 105):
        for x in range(78, 100):
            dx = (x - 88) / 10.0
            dy = (y - 88) / 14.0
            if dx**2 + dy**2 <= 1.0:
                t = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - ((x - 84)**2 + (y - 82)**2)**0.5 / 7.0)
                r_th = int(np.clip(78 * (0.8 + 0.3 * spec) - 20 * t, 0, 255))
                g_th = int(np.clip(216 * (0.8 + 0.3 * spec) - 20 * t, 0, 255))
                b_th = int(np.clip(106 * (0.8 + 0.3 * spec) + 80 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_th, g_th, b_th, 255))

    # Manganese Arc Leaf Springs (Steel arcs running along thighs)
    for y in range(80, 102):
        for x in range(28, 44):
            # Curved leaf spring line
            dist_curve = abs((x - 34) - 0.05 * (y - 90)**2)
            if dist_curve <= 1.8:
                chassis_img.putpixel((x, y), STEEL_LIGHT if dist_curve < 0.9 else STEEL_MID)
        for x in range(82, 98):
            dist_curve = abs((x - 90) + 0.05 * (y - 90)**2)
            if dist_curve <= 1.8:
                chassis_img.putpixel((x, y), STEEL_LIGHT if dist_curve < 0.9 else STEEL_MID)

    # Knee Joint Brass Pivot Caps
    ch_d.ellipse([32, 85, 38, 91], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.ellipse([34, 87, 36, 89], fill=BRASS_SHINE)
    ch_d.ellipse([88, 85, 94, 91], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.ellipse([90, 87, 92, 89], fill=BRASS_SHINE)

    # Outlines for thighs
    ch_d.ellipse([26, 74, 46, 104], outline=OUTLINE, width=1)
    ch_d.ellipse([78, 74, 98, 104], outline=OUTLINE, width=1)

    # 3. Three-Pronged Stamped Brass Webbed Feet (y: 104..116)
    # Left foot: center (34, 112)
    l_foot_poly = [(22, 114), (26, 108), (34, 107), (42, 108), (46, 114), (38, 116), (30, 116)]
    ch_d.polygon(l_foot_poly, fill=BRASS_GOLD, outline=OUTLINE)
    # Left 3 toes suction pads
    ch_d.ellipse([21, 112, 25, 116], fill=BRASS_LIGHT, outline=OUTLINE)
    ch_d.ellipse([32, 113, 36, 117], fill=BRASS_LIGHT, outline=OUTLINE)
    ch_d.ellipse([43, 112, 47, 116], fill=BRASS_LIGHT, outline=OUTLINE)

    # Right foot: center (88, 112)
    r_foot_poly = [(76, 114), (80, 108), (88, 107), (96, 108), (100, 114), (92, 116), (84, 116)]
    ch_d.polygon(r_foot_poly, fill=BRASS_GOLD, outline=OUTLINE)
    # Right 3 toes suction pads
    ch_d.ellipse([75, 112, 79, 116], fill=BRASS_LIGHT, outline=OUTLINE)
    ch_d.ellipse([86, 113, 90, 117], fill=BRASS_LIGHT, outline=OUTLINE)
    ch_d.ellipse([97, 112, 101, 116], fill=BRASS_LIGHT, outline=OUTLINE)

    # 4. Main Torso & Belly Body (x: 40..86, y: 52..104)
    # Outer emerald flank body
    for y in range(54, 104):
        for x in range(38, 90):
            dx = (x - 63.5) / 22.0
            dy = (y - 78.0) / 24.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 55)**2 + (y - 68)**2)**0.5 / 14.0)
                r_b = int(np.clip(78 * (0.85 + 0.35 * spec) - 25 * t, 0, 255))
                g_b = int(np.clip(216 * (0.85 + 0.35 * spec) - 25 * t, 0, 255))
                b_b = int(np.clip(106 * (0.85 + 0.35 * spec) + 80 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    ch_d.ellipse([41, 54, 86, 103], outline=OUTLINE, width=1)

    # Central Lemon Yellow Stamped Belly Plate (#FFD028) (x: 48..79, y: 62..100)
    for y in range(62, 101):
        for x in range(48, 80):
            dx = (x - 63.5) / 14.0
            dy = (y - 81.0) / 18.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 74)**2)**0.5 / 10.0)
                t = (dx**2 + dy**2)**0.5
                r_y = int(np.clip(255 * (0.9 + 0.2 * spec) - 30 * t, 0, 255))
                g_y = int(np.clip(208 * (0.9 + 0.2 * spec) - 35 * t, 0, 255))
                b_y = int(np.clip(40 * (0.9 + 0.2 * spec) + 120 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_y, g_y, b_y, 255))

    ch_d.ellipse([48, 62, 79, 100], outline=OUTLINE, width=1)
    # Belly stamping grooves / rivets
    ch_d.line([(54, 76), (73, 76)], fill=YELLOW_DARK, width=1)
    ch_d.line([(52, 86), (75, 86)], fill=YELLOW_DARK, width=1)
    ch_d.ellipse([53, 75, 55, 77], fill=BRASS_DEEP)
    ch_d.ellipse([72, 75, 74, 77], fill=BRASS_DEEP)
    ch_d.ellipse([51, 85, 53, 87], fill=BRASS_DEEP)
    ch_d.ellipse([74, 85, 76, 87], fill=BRASS_DEEP)

    # 5. Raised Collar Socket Rim (y: 48..56, x: 46..81)
    # Stamped brass collar band with mounting rivets for seamless head insertion
    collar_poly = [(46, 54), (52, 49), (64, 48), (76, 49), (81, 54), (77, 57), (64, 56), (50, 57)]
    ch_d.polygon(collar_poly, fill=BRASS_GOLD, outline=OUTLINE)
    # Collar rivets
    for rx in [52, 60, 68, 75]:
        ch_d.ellipse([rx - 1, 52, rx + 1, 54], fill=BRASS_SHINE)

    # 6. Forelimbs & Hands (0-ART9 compliant: pure hands, zero weapon)
    # Left Arm: extended outward for balance (x: 30..44, y: 64..78)
    l_arm_poly = [(42, 64), (32, 68), (30, 75), (36, 78), (44, 72)]
    ch_d.polygon(l_arm_poly, fill=EMERALD_PRIMARY, outline=OUTLINE)
    ch_d.ellipse([27, 72, 33, 78], fill=BRASS_GOLD, outline=OUTLINE)  # Wrist ball
    # Left 3 webbed fingers open in balance pose
    ch_d.line([(28, 74), (22, 72)], fill=BRASS_GOLD, width=1)
    ch_d.line([(27, 75), (21, 76)], fill=BRASS_GOLD, width=1)
    ch_d.line([(28, 77), (23, 80)], fill=BRASS_GOLD, width=1)

    # Right Arm: bent forward to hold weapon (x: 80..94, y: 64..76)
    r_arm_poly = [(82, 64), (90, 66), (93, 72), (88, 77), (80, 72)]
    ch_d.polygon(r_arm_poly, fill=EMERALD_PRIMARY, outline=OUTLINE)
    ch_d.ellipse([90, 69, 96, 75], fill=BRASS_GOLD, outline=OUTLINE)  # Wrist ball
    # Clenched mechanical brass fingers waiting for dart (x: 91..96, y: 70..76)
    # Strictly zero weapon pixels! Hand bounds end at x=96, y=76.
    ch_d.arc([91, 69, 96, 74], start=0, end=360, fill=BRASS_LIGHT, width=1)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Head)
    # File: head_unit/head_spring_frog_stock.png
    # Stamped Emerald Green Enamel Frog Head Casing (#4ED86A):
    # - Broad curved head shell with brass trim
    # - Two prominent stamped brass circular convex eye bezels at (48, 32) and (78, 32)
    # - CRITICAL 0-ART27 COMPLIANCE: Eye centers are HOLLOW (alpha=0) so optic_core shows through!
    # - Horizontal dart launch slot / mouth seam (y: 44..48, x: 44..82)
    # - Temple adjustment brass knobs on sides (ears replacement)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Main Broad Frog Head Shell (x: 36..91, y: 22..55)
    hcx, hcy = 63.5, 38.0
    for y in range(22, 55):
        for x in range(36, 92):
            dx = (x - hcx) / 26.0
            dy = (y - hcy) / 15.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - (hcx - 8))**2 + (y - (hcy - 6))**2)**0.5 / 12.0)
                shine = max(0.0, np.cos(np.arctan2(dy, dx) - 2.4))
                r_h = int(np.clip(78 * (0.85 + 0.35 * spec) + 40 * shine - 25 * t, 0, 255))
                g_h = int(np.clip(216 * (0.85 + 0.35 * spec) + 30 * shine - 25 * t, 0, 255))
                b_h = int(np.clip(106 * (0.85 + 0.35 * spec) + 80 * spec, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    hd.ellipse([36, 22, 91, 54], outline=OUTLINE, width=1)

    # 2. Side Temple Brass Adjustment Knobs (Mechanical ear replacements)
    # Left knob at (34, 38)
    hd.rectangle([32, 35, 36, 42], fill=BRASS_GOLD, outline=OUTLINE)
    hd.line([(34, 35), (34, 42)], fill=OUTLINE, width=1)
    # Right knob at (91, 38)
    hd.rectangle([91, 35, 95, 42], fill=BRASS_GOLD, outline=OUTLINE)
    hd.line([(93, 35), (93, 42)], fill=OUTLINE, width=1)

    # 3. Two Prominent Stamped Brass Eye Bezels (Frames)
    # Left eye bezel: center (49, 29), outer radius 8.5, inner radius 5.5
    # Right eye bezel: center (77, 29), outer radius 8.5, inner radius 5.5
    for ecx in [49.0, 77.0]:
        for y in range(int(29 - 9), int(29 + 10)):
            for x in range(int(ecx - 9), int(ecx + 10)):
                dist = ((x - ecx)**2 + (y - 29.0)**2)**0.5
                if dist <= 9.0 and dist >= 5.5:
                    # Brass bezel ring with shine
                    spec = max(0.0, 1.0 - ((x - (ecx - 3))**2 + (y - 26)**2)**0.5 / 4.0)
                    r_bz = int(np.clip(212 + 43 * spec, 0, 255))
                    g_bz = int(np.clip(160 + 80 * spec, 0, 255))
                    b_bz = int(np.clip(23 + 180 * spec, 0, 255))
                    head_img.putpixel((x, y), (r_bz, g_bz, b_bz, 255))

        hd.ellipse([int(ecx - 9), int(29 - 9), int(ecx + 9), int(29 + 9)], outline=OUTLINE, width=1)
        hd.ellipse([int(ecx - 5.5), int(29 - 5.5), int(ecx + 5.5), int(29 + 5.5)], outline=OUTLINE, width=1)

        # 0-ART27 HOLLOW EYE SOCKET ASSERTION: Clear inner pixels to alpha=0!
        for y in range(int(29 - 5), int(29 + 6)):
            for x in range(int(ecx - 5), int(ecx + 6)):
                if ((x - ecx)**2 + (y - 29.0)**2)**0.5 < 5.2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    # 4. Horizontal Stamped Coin-Slot Dart Ejection Mouth (y: 44..48, x: 45..82)
    hd.rounded_rectangle([45, 44, 82, 48], radius=2, fill=BRASS_DARK, outline=OUTLINE, width=1)
    hd.line([(47, 46), (80, 46)], fill=OUTLINE, width=1)
    # Cooling louvers / gear teeth underneath mouth
    for lx in range(50, 78, 4):
        hd.line([(lx, 49), (lx, 51)], fill=OUTLINE, width=1)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Chest & Waist Armor)
    # File: costume/costume_spring_forest_courier.png
    # Spring forest courier vest / harness:
    # - Lemon yellow stamped breastplate (#FFD028)
    # - Dual crossed harness straps with brass rivets and buckles
    # - Hollow central aperture (y: 66..76, x: 59..69) for optic_core chest gem
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # Main Harness Vest body (x: 46..81, y: 56..88)
    for y in range(56, 89):
        for x in range(46, 82):
            dx = (x - 63.5) / 16.0
            dy = (y - 71.0) / 15.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                spec = max(0.0, 1.0 - ((x - 56)**2 + (y - 64)**2)**0.5 / 10.0)
                t = dist**0.5
                r_c = int(np.clip(255 * (0.85 + 0.3 * spec) - 20 * t, 0, 255))
                g_c = int(np.clip(208 * (0.85 + 0.3 * spec) - 25 * t, 0, 255))
                b_c = int(np.clip(40 * (0.85 + 0.3 * spec) + 120 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cos_d.ellipse([46, 56, 81, 88], outline=OUTLINE, width=1)

    # Leatherette / Manganese shoulder straps
    cos_d.line([(48, 56), (56, 72)], fill=STEEL_DARK, width=2)
    cos_d.line([(79, 56), (71, 72)], fill=STEEL_DARK, width=2)
    cos_d.line([(48, 56), (56, 72)], fill=STEEL_MID, width=1)
    cos_d.line([(79, 56), (71, 72)], fill=STEEL_MID, width=1)

    # Brass Buckles on straps
    cos_d.rectangle([51, 62, 55, 66], fill=BRASS_GOLD, outline=OUTLINE)
    cos_d.rectangle([72, 62, 76, 66], fill=BRASS_GOLD, outline=OUTLINE)

    # Waist Belt and Dart Ammo Pouch
    cos_d.rectangle([48, 80, 79, 85], fill=STEEL_DARK, outline=OUTLINE)
    cos_d.rectangle([60, 79, 67, 86], fill=BRASS_GOLD, outline=OUTLINE)  # Center belt buckle
    cos_d.point((63, 82), fill=BRASS_SHINE)

    # Mini Dart Ammo Pouch on left waist (x: 44..49, y: 78..86)
    cos_d.rounded_rectangle([43, 78, 48, 86], radius=1, fill=ORANGE_DARK, outline=OUTLINE)
    cos_d.line([(43, 81), (48, 81)], fill=BRASS_GOLD, width=1)

    # CRITICAL: Hollow center hole for Clockwork Heart Gem (center (63.5, 71), radius 5.5)
    for y in range(65, 77):
        for x in range(58, 70):
            if ((x - 63.5)**2 + (y - 71.0)**2)**0.5 <= 5.5:
                costume_img.putpixel((x, y), (0, 0, 0, 0))

    cos_d.ellipse([58, 65, 69, 76], outline=BRASS_GOLD, width=1)
    cos_d.ellipse([57, 64, 70, 77], outline=OUTLINE, width=1)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, Face & Chest Core)
    # File: optic_core/core_azure_aperture.png
    # - Two Sky Blue Quartz Convex Optical Lens Eyes at (49, 29) and (77, 29)
    # - Central Clockwork Heart Emerald/Sky Blue Gemstone at (63.5, 71)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    core_d = ImageDraw.Draw(core_img)

    # 1. Two Sky Blue Optical Convex Eyes
    for ecx in [49.0, 77.0]:
        for y in range(int(29 - 6), int(29 + 7)):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - 29.0)**2)**0.5
                if dist <= 5.2:
                    t = dist / 5.2
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.5))**2 + (y - 27.5)**2)**0.5 / 2.8)
                    r_e = int(np.clip(20 * (1 - 0.5 * t) + 235 * spec, 0, 255))
                    g_e = int(np.clip(100 * (1 - 0.4 * t) + 155 * spec, 0, 255))
                    b_e = int(np.clip(255 * (1 - 0.3 * t) + 40 * spec, 0, 255))
                    core_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        # Optical aperture crosshair / mechanical ring
        core_d.ellipse([int(ecx - 5.0), int(29 - 5.0), int(ecx + 5.0), int(29 + 5.0)], outline=OUTLINE, width=1)
        core_d.ellipse([int(ecx - 2.5), int(29 - 2.5), int(ecx + 2.5), int(29 + 2.5)], outline=SKY_DEEP, width=1)
        # Specular glint
        core_d.point((int(ecx - 1), int(27)), fill=WHITE_SHINE)
        core_d.point((int(ecx - 2), int(28)), fill=WHITE_SHINE)

    # 2. Chest Clockwork Heart Core Gem (center (63.5, 71), radius 5.0)
    for y in range(66, 77):
        for x in range(58, 70):
            dist = ((x - 63.5)**2 + (y - 71.0)**2)**0.5
            if dist <= 5.0:
                t = dist / 5.0
                spec = max(0.0, 1.0 - ((x - 62)**2 + (y - 69.5)**2)**0.5 / 2.5)
                # Radiant Sky Blue / Emerald gem depth
                r_g = int(np.clip(35 + 220 * spec, 0, 255))
                g_g = int(np.clip(180 + 75 * spec - 30 * t, 0, 255))
                b_g = int(np.clip(240 + 15 * spec - 40 * t, 0, 255))
                core_img.putpixel((x, y), (r_g, g_g, b_g, 255))

    core_d.ellipse([58, 66, 68, 76], outline=OUTLINE, width=1)
    # Rhombus crystal facets
    core_d.line([(63, 67), (67, 71)], fill=SKY_LIGHT, width=1)
    core_d.line([(67, 71), (63, 75)], fill=SKY_DEEP, width=1)
    core_d.line([(63, 75), (59, 71)], fill=SKY_DEEP, width=1)
    core_d.line([(59, 71), (63, 67)], fill=WHITE_SHINE, width=1)
    core_d.point((62, 70), fill=WHITE_SHINE)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Handheld Weapon)
    # File: weapon/wpn_lotus_cog_dart.png
    # Single handheld / hovering Lotus Cog-Dart (碧葉旋刃機關鏢)
    # - Center at right hand (x: 94, y: 64)
    # - 6-point aerodynamic curved blade gear teeth (#4ED86A & polished steel edge)
    # - Orange / brass concentric inertia weight ring (#FFA010 & #FFD028)
    # - High precision brass ball bearing center hub with reflection
    # - Strictly ZERO double weapons (0-MKT7 compliant)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wx, wy = 94.0, 64.0
    r_outer = 16.0
    r_ring = 10.0
    r_hub_w = 4.5

    # 1. Six-Blade Lotus Cog Dart Body
    for y in range(int(wy - r_outer - 2), int(wy + r_outer + 3)):
        for x in range(int(wx - r_outer - 2), int(wx + r_outer + 3)):
            dx = x - wx
            dy = y - wy
            dist = (dx**2 + dy**2)**0.5
            angle = np.arctan2(dy, dx)

            # 6 sharp curved turbine teeth
            blade_mod = np.cos(6.0 * angle)
            blade_r = r_ring + (r_outer - r_ring) * max(0.0, blade_mod)**1.8

            if dist <= blade_r:
                spec = max(0.0, 1.0 - ((x - (wx - 4))**2 + (y - (wy - 4))**2)**0.5 / 10.0)
                shine = max(0.0, np.cos(angle - 2.4))

                if dist > r_ring:
                    # Outer aerodynamic blade teeth in emerald enamel with polished cutting edge
                    is_cutting_edge = (blade_mod > 0.6 and dist > r_outer - 3.0)
                    if is_cutting_edge:
                        r_w = int(np.clip(220 + 35 * spec, 0, 255))
                        g_w = int(np.clip(235 + 20 * spec, 0, 255))
                        b_w = int(np.clip(245 + 10 * spec, 0, 255))
                    else:
                        r_w = int(np.clip(78 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        g_w = int(np.clip(216 * (0.8 + 0.3 * spec) + 39 * shine, 0, 255))
                        b_w = int(np.clip(106 * (0.8 + 0.3 * spec) + 80 * spec, 0, 255))
                    weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))
                elif dist > r_hub_w:
                    # Middle orange & brass weight ring
                    if dist >= 7.5:
                        # Brass gold outer ring
                        r_w = int(np.clip(212 + 43 * spec + 30 * shine, 0, 255))
                        g_w = int(np.clip(160 + 80 * spec + 25 * shine, 0, 255))
                        b_w = int(np.clip(23 + 180 * spec, 0, 255))
                    else:
                        # Warm orange inner ring
                        r_w = int(np.clip(255 * (0.85 + 0.3 * spec) - 20, 0, 255))
                        g_w = int(np.clip(160 * (0.85 + 0.3 * spec) - 25, 0, 255))
                        b_w = int(np.clip(16 * (0.85 + 0.3 * spec) + 100 * spec, 0, 255))
                    weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))
                else:
                    # Center steel ball bearing hub
                    r_w = int(np.clip(180 + 75 * spec, 0, 255))
                    g_w = int(np.clip(195 + 60 * spec, 0, 255))
                    b_w = int(np.clip(215 + 40 * spec, 0, 255))
                    weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Ring outlines
    wd.ellipse([int(wx - r_ring), int(wy - r_ring), int(wx + r_ring), int(wy + r_ring)], outline=OUTLINE, width=1)
    wd.ellipse([int(wx - 7.5), int(wy - 7.5), int(wx + 7.5), int(wy + 7.5)], outline=OUTLINE, width=1)
    wd.ellipse([int(wx - r_hub_w), int(wy - r_hub_w), int(wx + r_hub_w), int(wy + r_hub_w)], outline=OUTLINE, width=1)

    # Outer 6 blade outlines & radial lines
    for i in range(6):
        blade_angle = i * (np.pi / 3.0)
        bx = int(wx + r_outer * np.cos(blade_angle))
        by = int(wy + r_outer * np.sin(blade_angle))
        wd.line([(int(wx + r_ring * np.cos(blade_angle)), int(wy + r_ring * np.sin(blade_angle))), (bx, by)], fill=OUTLINE, width=1)

    # Center glint
    wd.ellipse([int(wx - 1.5), int(wy - 1.5), int(wx + 1.5), int(wy + 1.5)], fill=BRASS_GOLD)
    wd.point((int(wx - 1), int(wy - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 and 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "paint_frog_emerald", chassis_img),
        ("head_unit", "head_spring_frog_stock", head_img),
        ("winding_key", "key_twin_wing_concentric", key_img),
        ("costume", "costume_spring_forest_courier", costume_img),
        ("optic_core", "core_azure_aperture", core_img),
        ("weapon", "wpn_lotus_cog_dart", weapon_img),
        ("back_curio", "curio_lotus_leaf_parasol", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{FROG_PD_DIR}/{slot}"
        os.makedirs(out_dir, exist_ok=True)
        dst_128 = f"{out_dir}/{item_id}.png"
        img.save(dst_128)

        # 512x512 with LANCZOS
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{out_dir}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    shutil.copyfile(f"{FROG_PD_DIR}/winding_key/key_twin_wing_concentric.png", f"{KEY_DIR}/key_twin_wing_concentric.png")
    shutil.copyfile(f"{FROG_PD_DIR}/weapon/wpn_lotus_cog_dart.png", f"{WEAPON_DIR}/wpn_lotus_cog_dart.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE PROOFS
    # ─────────────────────────────────────────────────────────────
    # Composite order strictly matches PaperdollRenderer Z-index:
    # 1. winding_key (Z: 5)
    # 2. back_curio (Z: 8)
    # 3. chassis (Z: 10)
    # 4. head_unit (Z: 20)
    # 5. costume (Z: 25)
    # 6. optic_core (Z: 30)
    # 7. weapon (Z: 40)
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{FROG_PD_DIR}/proof_paperdoll_frog_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{FROG_PD_DIR}/proof_paperdoll_frog_magenta.png"
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

    proof_7 = f"{FROG_PD_DIR}/proof_frog_all_7_slices.png"
    strip_img.save(proof_7)
    print("  ✓ Proof images generated successfully")


if __name__ == "__main__":
    build_all()
