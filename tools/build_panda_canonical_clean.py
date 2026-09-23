#!/usr/bin/env python3
"""
build_panda_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Porcelain Panda (瓷韻熊貓 / The Porcelain Panda) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/PORCELAIN_PANDA_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh, zero cloth/plush, zero slime, all high-fired porcelain/lacquer/brass, brass key)
- references/art_direction.md (Dopamine high-saturation palette, clean enamel/brass, deep outline)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r
- Benchmarked directly against Xuanji Tortoise (玄機龜), Colossus Elephant (鋼岳象), and Spring-Leg Frog (碧簧蛙).
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
PANDA_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/panda"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Dawson Day 258 Series & Porcelain Panda Proposal)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Mutton-fat White Jade Crackled Porcelain (#FFFDF8)
PORCELAIN_WHITE = (255, 253, 248, 255) # Pure Mutton-Fat White Porcelain
PORCELAIN_LIGHT = (255, 255, 255, 255) # Pure specular highlight
PORCELAIN_SHADE = (222, 225, 232, 255) # Soft cel shadow
PORCELAIN_DEEP  = (182, 188, 200, 255) # Seam & ambient occlusion

# Secondary: Obsidian Navy-Black Gloss Lacquer (#1F1A3A)
LACQUER_BASE    = (31, 26, 58, 255)    # #1F1A3A Deep glossy lacquer
LACQUER_DARK    = (18, 14, 36, 255)    # Core shadow
LACQUER_SHINE   = (115, 105, 155, 255) # High specular reflection curve
LACQUER_RIM     = (72, 64, 108, 255)   # Subsurface edge highlight

# Accent: Tianyuan Stamped Gold / Amber Crystal (#FFD028)
GOLD_PRIMARY    = (255, 208, 40, 255)  # #FFD028 Stamped Gold
GOLD_LIGHT      = (255, 235, 115, 255)
GOLD_SHINE      = (255, 250, 185, 255)
GOLD_DARK       = (195, 145, 18, 255)
GOLD_DEEP       = (125, 85, 10, 255)

# Detail: Mint Bamboo Green Enamel (#4ED86A)
MINT_GREEN      = (78, 216, 106, 255)  # #4ED86A Mint Bamboo Green
MINT_LIGHT      = (135, 240, 160, 255)
MINT_DARK       = (36, 140, 62, 255)
MINT_DEEP       = (18, 78, 35, 255)

# Warm Highlight: High-torque Warm Orange (#FFA010)
ORANGE_ACCENT   = (255, 160, 16, 255)  # #FFA010
ORANGE_LIGHT    = (255, 205, 80, 255)
ORANGE_DARK     = (190, 95, 10, 255)

# Metal: Polished Tianyuan Brass & Antique Bronze (#D4A017)
BRASS_GOLD      = (212, 160, 23, 255)
BRASS_LIGHT     = (255, 225, 95, 255)
BRASS_SHINE     = (255, 250, 175, 255)
BRASS_DARK      = (150, 105, 12, 255)
BRASS_DEEP      = (90, 60, 8, 255)

BRONZE_BASE     = (165, 120, 55, 255)
BRONZE_LIGHT    = (215, 175, 95, 255)
BRONZE_DARK     = (105, 75, 30, 255)

# Polished Mechanical Steel
STEEL_LIGHT     = (200, 210, 225, 255)
STEEL_MID       = (130, 140, 155, 255)
STEEL_DARK      = (70, 78, 90, 255)

WHITE_SHINE     = (255, 255, 255, 255)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL PORCELAIN PANDA SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back)
    # File: winding_key/key_panda_taiji_ruyi_brass.png
    # Brass Taiji Ruyi Wind-up Key (青銅太極如意發條鑰匙)
    # Symmetrical Taiji yin-yang dual-fish & Ruyi cloud wings mounted on upper back
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Key shaft/stem entering spine socket at (40, 48) from key head (28, 28)
    for y in range(28, 50):
        for x in range(26, 42):
            t_s = (y - 28) / 22.0
            sx = 28.0 + t_s * 12.0
            dist = abs(x - sx)
            if dist <= 2.2:
                edge_t = dist / 2.2
                r_s = int(np.clip(212 * (1 - 0.3 * edge_t) - 25 * t_s, 0, 255))
                g_s = int(np.clip(160 * (1 - 0.4 * edge_t) - 35 * t_s, 0, 255))
                b_s = int(np.clip(23 * (1 - 0.6 * edge_t) + 40 * (1 - t_s), 0, 255))
                key_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    # Center socket boss at (40, 48)
    kd.ellipse([37, 45, 43, 51], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([38, 46, 42, 50], fill=BRASS_GOLD)

    # Key Head: Taiji Ruyi Wings (center (28, 28), outer radius 13.5, hub radius 4.5)
    kcx, kcy = 28.0, 28.0
    r_hub = 4.5
    r_wing = 13.5

    for y in range(int(kcy - r_wing - 2), int(kcy + r_wing + 3)):
        for x in range(int(kcx - r_wing - 2), int(kcx + r_wing + 3)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5

            if dist <= r_wing:
                angle = np.arctan2(dy, dx)
                d_eye1 = ((x - (kcx + 5.2))**2 + (y - (kcy - 4.5))**2)**0.5
                d_eye2 = ((x - (kcx - 5.2))**2 + (y - (kcy + 4.5))**2)**0.5
                waist = 1.0 - 0.28 * abs(np.sin(angle + 0.6))

                if dist <= r_wing * waist and d_eye1 > 2.2 and d_eye2 > 2.2:
                    if dist <= r_hub:
                        spec = max(0.0, 1.0 - ((x - (kcx - 1.2))**2 + (y - (kcy - 1.2))**2)**0.5 / 3.5)
                        r_v = int(np.clip(212 + 43 * spec, 0, 255))
                        g_v = int(np.clip(160 + 80 * spec, 0, 255))
                        b_v = int(np.clip(23 + 180 * spec, 0, 255))
                        key_img.putpixel((x, y), (r_v, g_v, b_v, 255))
                    else:
                        spec = max(0.0, 1.0 - ((x - (kcx - 5))**2 + (y - (kcy - 5))**2)**0.5 / 9.0)
                        shine = max(0.0, np.cos(angle - 2.2))
                        r_v = int(np.clip(175 + 75 * spec + 45 * shine - 10 * (dist / r_wing), 0, 255))
                        g_v = int(np.clip(135 + 85 * spec + 38 * shine - 15 * (dist / r_wing), 0, 255))
                        b_v = int(np.clip(18 + 160 * spec + 30 * shine, 0, 255))
                        key_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    kd.ellipse([int(kcx - r_wing + 1), int(kcy - r_wing + 1), int(kcx + r_wing - 1), int(kcy + r_wing - 1)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - r_hub), int(kcy - r_hub), int(kcx + r_hub), int(kcy + r_hub)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx + 5.2 - 2.2), int(kcy - 4.5 - 2.2), int(kcx + 5.2 + 2.2), int(kcy - 4.5 + 2.2)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - 5.2 - 2.2), int(kcy + 4.5 - 2.2), int(kcx - 5.2 + 2.2), int(kcy + 4.5 + 2.2)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - 1.8), int(kcy - 1.8), int(kcx + 1.8), int(kcy + 1.8)], fill=ORANGE_ACCENT)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Back)
    # File: back_curio/curio_panda_floating_taiji_box.png
    # Micro clockwork floating Taiji music box (微型發條懸浮太極八音盒)
    # Floating at left flank (center (24, 46), radius 9) with golden notes
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    bcx, bcy, br = 24.0, 46.0, 9.5

    # Floating Taiji Box Body (Octagonal Obsidian Lacquer with Brass Corner Mounts)
    for y in range(int(bcy - br - 1), int(bcy + br + 2)):
        for x in range(int(bcx - br - 1), int(bcx + br + 2)):
            dx = x - bcx
            dy = y - bcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= br and abs(dx) + abs(dy) <= br * 1.34:
                spec = max(0.0, 1.0 - ((x - (bcx - 2.5))**2 + (y - (bcy - 2.5))**2)**0.5 / 6.0)
                shine = max(0.0, 1.0 - ((x - (bcx - 2.5))**2 + (y - (bcy - 2.5))**2)**0.5 / 2.5)**2

                if dist <= br - 2.4:
                    # Inner lid: Taiji yin-yang dial
                    angle = np.arctan2(dy, dx)
                    s_val = np.sin(angle + 0.3)
                    if s_val >= 0:
                        # White porcelain half with cel shine
                        r_c = int(np.clip(240 + 15 * spec + 10 * shine, 0, 255))
                        g_c = int(np.clip(238 + 17 * spec + 10 * shine, 0, 255))
                        b_c = int(np.clip(235 + 20 * spec + 10 * shine, 0, 255))
                    else:
                        # Black lacquer half with violet specular
                        r_c = int(np.clip(28 + 70 * spec + 30 * shine, 0, 255))
                        g_c = int(np.clip(24 + 65 * spec + 30 * shine, 0, 255))
                        b_c = int(np.clip(54 + 95 * spec + 40 * shine, 0, 255))
                    curio_img.putpixel((x, y), (r_c, g_c, b_c, 255))
                else:
                    # Outer Brass Frame with directional reflection
                    r_c = int(np.clip(180 + 70 * spec + 25 * shine, 0, 255))
                    g_c = int(np.clip(135 + 75 * spec + 25 * shine, 0, 255))
                    b_c = int(np.clip(20 + 150 * spec, 0, 255))
                    curio_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cd.ellipse([int(bcx - br), int(bcy - br), int(bcx + br), int(bcy + br)], outline=OUTLINE, width=1)
    cd.ellipse([int(bcx - br + 2.4), int(bcy - br + 2.4), int(bcx + br - 2.4), int(bcy + br - 2.4)], outline=OUTLINE, width=1)
    # Center Amber Jewel
    cd.ellipse([int(bcx - 1.8), int(bcy - 1.8), int(bcx + 1.8), int(bcy + 1.8)], fill=GOLD_PRIMARY, outline=OUTLINE)
    cd.point((int(bcx - 1), int(bcy - 1)), fill=WHITE_SHINE)

    # Top mini winding cog & suspension ring
    cd.rectangle([int(bcx - 2), int(bcy - br - 3), int(bcx + 2), int(bcy - br)], fill=BRASS_GOLD, outline=OUTLINE)
    cd.ellipse([int(bcx - 2.5), int(bcy - br - 5), int(bcx + 2.5), int(bcy - br - 2)], outline=BRASS_LIGHT, width=1)

    # Sparkle / Music resonance particles
    cd.point((int(bcx - 6), int(bcy - br - 3)), fill=GOLD_SHINE)
    cd.point((int(bcx + 7), int(bcy - br - 1)), fill=GOLD_LIGHT)
    cd.point((int(bcx + 8), int(bcy + br - 2)), fill=MINT_LIGHT)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Base)
    # File: chassis/paint_panda_porcelain.png
    # Complete headless automaton panda chassis:
    # - Low-gravity Taiji stance (太極抱元沉步架式)
    # - Soft contact ground shadow at (64, 116)
    # - Black lacquer feet & legs with antique bronze sole plates
    # - Thick mutton-fat white porcelain chest & belly (#FFFDF8) with ice crackles
    # - Circular viewport for Taiji Gyroscope at (64, 76)
    # - Left arm extending in defensive palm posture (x: 26..46, y: 64..84)
    # - Right arm leading to cupped wrist socket at (88, 76)
    # - Strictly ZERO weapon baked in (0-ART9, 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 34, 116 - 4, 64 + 34, 116 + 5], fill=(31, 26, 58, 125))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Lower Limbs & Feet
    for fcx in [44.0, 84.0]:
        for y in range(106, 118):
            for x in range(int(fcx - 8), int(fcx + 9)):
                dx = (x - fcx) / 8.0
                dy = (y - 112) / 4.5
                if dx**2 + dy**2 <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (fcx - 2))**2 + (y - 109)**2)**0.5 / 5.0)
                    shine = max(0.0, 1.0 - ((x - (fcx - 2))**2 + (y - 109)**2)**0.5 / 2.0)**2
                    if y >= 113:
                        # Bronze sole plate
                        r_f = int(np.clip(165 + 40 * spec, 0, 255))
                        g_f = int(np.clip(120 + 35 * spec, 0, 255))
                        b_f = int(np.clip(55 + 30 * spec, 0, 255))
                    else:
                        # Obsidian lacquer boot
                        r_f = int(np.clip(31 + 75 * spec + 30 * shine, 0, 255))
                        g_f = int(np.clip(26 + 70 * spec + 30 * shine, 0, 255))
                        b_f = int(np.clip(58 + 105 * spec + 40 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_f, g_f, b_f, 255))

        ch_d.ellipse([int(fcx - 8), 106, int(fcx + 8), 116], outline=OUTLINE, width=1)
        ch_d.point((int(fcx - 3), 114), fill=BRASS_GOLD)
        ch_d.point((int(fcx + 2), 114), fill=BRASS_GOLD)

    # Legs
    for lcx in [44.0, 84.0]:
        for y in range(90, 108):
            for x in range(int(lcx - 7), int(lcx + 8)):
                dx = (x - lcx) / 7.0
                dy = (y - 99) / 9.0
                if dx**2 + dy**2 <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (lcx - 2))**2 + (y - 95)**2)**0.5 / 6.0)
                    shine = max(0.0, 1.0 - ((x - (lcx - 2))**2 + (y - 95)**2)**0.5 / 2.5)**2
                    r_l = int(np.clip(31 + 70 * spec + 30 * shine, 0, 255))
                    g_l = int(np.clip(26 + 65 * spec + 30 * shine, 0, 255))
                    b_l = int(np.clip(58 + 100 * spec + 40 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_l, g_l, b_l, 255))
        ch_d.ellipse([int(lcx - 7), 90, int(lcx + 7), 108], outline=OUTLINE, width=1)

    # Tail Counterweight Block
    for y in range(88, 97):
        for x in range(28, 37):
            if ((x - 32)**2 + (y - 92)**2)**0.5 <= 4.2:
                spec = max(0.0, 1.0 - ((x - 30)**2 + (y - 90)**2)**0.5 / 3.0)
                r_t = int(np.clip(165 + 45 * spec, 0, 255))
                g_t = int(np.clip(120 + 40 * spec, 0, 255))
                b_t = int(np.clip(55 + 30 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))
    ch_d.ellipse([28, 88, 36, 96], outline=OUTLINE, width=1)

    # 3. Torso: Mutton-Fat White Porcelain Breastplate & Belly Plate (x: 43..85, y: 52..98)
    for y in range(52, 98):
        for x in range(43, 85):
            prog = (y - 52) / 44.0
            cur_hw = 15.0 + 4.5 * np.sin(prog * np.pi)
            dx = (x - 64.0) / cur_hw
            dy = (y - 75.0) / 22.0
            dist_sq = dx**2 + dy**2

            if dist_sq <= 1.0:
                d_light = ((x - 56.0)**2 + (y - 62.0)**2)**0.5
                spec = max(0.0, 1.0 - d_light / 18.0)
                shine = max(0.0, 1.0 - d_light / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.35) / 0.65)

                r_p = int(np.clip(255 * (1.0 - 0.18 * edge_shade) + 20 * shine - 5 * (y / 98.0), 0, 255))
                g_p = int(np.clip(253 * (1.0 - 0.16 * edge_shade) + 20 * shine - 8 * (y / 98.0), 0, 255))
                b_p = int(np.clip(248 * (1.0 - 0.12 * edge_shade) + 20 * shine - 10 * (y / 98.0), 0, 255))

                crackle_noise = (np.sin(x * 1.35 + y * 0.72) * np.cos(y * 1.48 - x * 0.42))
                if crackle_noise > 0.86 and dist_sq < 0.85:
                    r_p = int(np.clip(r_p * 0.84, 0, 255))
                    g_p = int(np.clip(g_p * 0.86, 0, 255))
                    b_p = int(np.clip(b_p * 0.90, 0, 255))

                chassis_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    # Flanks
    for y in range(64, 92):
        for x in range(39, 46):
            if ((x - 44)**2 + (y - 78)**2)**0.5 < 12:
                spec = max(0.0, 1.0 - ((x - 41)**2 + (y - 74)**2)**0.5 / 6.0)
                chassis_img.putpixel((x, y), (int(31 + 40 * spec), int(26 + 35 * spec), int(58 + 60 * spec), 255))
        for x in range(83, 90):
            if ((x - 84)**2 + (y - 78)**2)**0.5 < 12:
                spec = max(0.0, 1.0 - ((x - 85)**2 + (y - 74)**2)**0.5 / 6.0)
                chassis_img.putpixel((x, y), (int(31 + 40 * spec), int(26 + 35 * spec), int(58 + 60 * spec), 255))

    ch_d.ellipse([43, 52, 85, 96], outline=OUTLINE, width=1)

    # 4. Taiji Gyroscope Viewport Aperture (center (64, 76), outer radius 8.0, inner 5.8)
    for y in range(68, 85):
        for x in range(56, 73):
            dist = ((x - 64.0)**2 + (y - 76.0)**2)**0.5
            if dist <= 8.0:
                if dist >= 5.8:
                    spec = max(0.0, 1.0 - ((x - 61)**2 + (y - 73)**2)**0.5 / 4.0)
                    shine = max(0.0, 1.0 - ((x - 61)**2 + (y - 73)**2)**0.5 / 2.0)**2
                    r_b = int(np.clip(212 + 43 * spec + 25 * shine, 0, 255))
                    g_b = int(np.clip(160 + 80 * spec + 25 * shine, 0, 255))
                    b_b = int(np.clip(23 + 180 * spec, 0, 255))
                    chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))
                else:
                    angle = np.arctan2(y - 76.0, x - 64.0)
                    spec = max(0.0, 1.0 - dist / 5.0)
                    if np.sin(angle) >= 0:
                        chassis_img.putpixel((x, y), (int(18 + 20 * spec), int(14 + 20 * spec), int(34 + 30 * spec), 255))
                    else:
                        chassis_img.putpixel((x, y), (int(55 + 40 * spec), int(65 + 40 * spec), int(80 + 40 * spec), 255))

    ch_d.ellipse([56, 68, 72, 84], outline=OUTLINE, width=1)
    ch_d.ellipse([58, 70, 70, 82], outline=BRASS_DEEP, width=1)
    ch_d.point((64, 69), fill=GOLD_SHINE)
    ch_d.point((64, 83), fill=GOLD_SHINE)
    ch_d.point((57, 76), fill=GOLD_SHINE)
    ch_d.point((71, 76), fill=GOLD_SHINE)

    # 5. Neck Collar Mounting Socket
    ch_d.rounded_rectangle([50, 47, 78, 54], radius=3, fill=BRASS_GOLD, outline=OUTLINE, width=1)
    ch_d.ellipse([54, 48, 74, 53], fill=BRASS_DARK)
    for nx in [53, 60, 68, 75]:
        ch_d.point((nx, 51), fill=BRASS_LIGHT)

    # 6. Left Arm (Defensive Taiji Palm Gesture): extending outward & forward (x: 22..44, y: 60..86)
    ch_d.ellipse([34, 60, 42, 68], fill=LACQUER_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 62, 40, 66], fill=LACQUER_SHINE)

    for y in range(66, 80):
        for x in range(26, 39):
            dx = (x - 32) / 6.0
            dy = (y - 73) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 29)**2 + (y - 70)**2)**0.5 / 5.0)
                shine = max(0.0, 1.0 - ((x - 29)**2 + (y - 70)**2)**0.5 / 2.0)**2
                r_a = int(np.clip(31 + 65 * spec + 30 * shine, 0, 255))
                g_a = int(np.clip(26 + 60 * spec + 30 * shine, 0, 255))
                b_a = int(np.clip(58 + 90 * spec + 40 * shine, 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    ch_d.ellipse([26, 66, 38, 80], outline=OUTLINE, width=1)

    # Left Wrist & Open Palm: White porcelain palm gesturing in Taiji ward-off
    ch_d.rectangle([25, 76, 29, 80], fill=BRASS_GOLD, outline=OUTLINE)
    for y in range(78, 86):
        for x in range(22, 31):
            if ((x - 26)**2 + (y - 82)**2)**0.5 <= 4.0:
                spec = max(0.0, 1.0 - ((x - 24)**2 + (y - 80)**2)**0.5 / 3.0)
                r_p = int(np.clip(245 + 10 * spec, 0, 255))
                g_p = int(np.clip(242 + 13 * spec, 0, 255))
                b_p = int(np.clip(238 + 17 * spec, 0, 255))
                chassis_img.putpixel((x, y), (r_p, g_p, b_p, 255))
    ch_d.ellipse([22, 78, 30, 86], outline=OUTLINE, width=1)
    ch_d.line([(24, 80), (24, 84)], fill=OUTLINE, width=1)

    # 7. Right Arm & Cupped Wrist Socket (Ready for weapon gauntlet, x: 82..94, y: 62..78)
    ch_d.ellipse([86, 60, 94, 68], fill=LACQUER_BASE, outline=OUTLINE)
    ch_d.ellipse([88, 62, 92, 66], fill=LACQUER_SHINE)

    for y in range(66, 78):
        for x in range(82, 94):
            dx = (x - 88) / 5.5
            dy = (y - 72) / 6.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 86)**2 + (y - 70)**2)**0.5 / 4.0)
                shine = max(0.0, 1.0 - ((x - 86)**2 + (y - 70)**2)**0.5 / 1.8)**2
                r_ra = int(np.clip(31 + 60 * spec + 30 * shine, 0, 255))
                g_ra = int(np.clip(26 + 55 * spec + 30 * shine, 0, 255))
                b_ra = int(np.clip(58 + 85 * spec + 40 * shine, 0, 255))
                chassis_img.putpixel((x, y), (r_ra, g_ra, b_ra, 255))
    ch_d.ellipse([82, 66, 93, 77], outline=OUTLINE, width=1)

    ch_d.rectangle([85, 74, 91, 78], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.point((88, 76), fill=BRASS_DARK)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Cranial Dome & Ears)
    # File: head_unit/head_panda_brass_socket_ears.png
    # - Mutton-fat white porcelain cranial dome (x: 38..90, y: 18..56)
    # - Tilted obsidian lacquer panda eye surround patches (x: 42..58 and x: 70..86)
    # - Clean HOLLOW eye sockets at left (49, 34) and right (79, 34) for 0-ART27!
    # - Dual spherical brass ball-and-socket ear caps (雙聯青古銅球窩半球耳罩) at top corners (42, 20) and (86, 20)
    # - Horizontal metal cooling mesh mouth (y: 48..51, x: 55..73)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 38.0
    hrx, hry = 25.5, 17.5

    # 1. High-fired White Porcelain Cranial Dome
    for y in range(int(hcy - hry - 2), int(hcy + hry + 3)):
        for x in range(int(hcx - hrx - 2), int(hcx + hrx + 3)):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                z_sphere = np.sqrt(max(0.0, 1.0 - dist_sq))
                d_light = ((x - 54.0)**2 + (y - 28.0)**2)**0.5
                spec = max(0.0, 1.0 - d_light / 16.0)
                shine = max(0.0, 1.0 - d_light / 5.5)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_h = int(np.clip(205 + 45 * z_sphere - 20 * edge_shade + 20 * shine - 5 * (y / 56.0), 0, 255))
                g_h = int(np.clip(203 + 45 * z_sphere - 20 * edge_shade + 20 * shine - 6 * (y / 56.0), 0, 255))
                b_h = int(np.clip(198 + 45 * z_sphere - 16 * edge_shade + 20 * shine - 8 * (y / 56.0), 0, 255))

                crackle_noise = (np.sin(x * 1.4 + y * 0.8) * np.cos(y * 1.6 - x * 0.5))
                if crackle_noise > 0.86 and dist_sq < 0.8:
                    r_h = int(np.clip(r_h * 0.82, 0, 255))
                    g_h = int(np.clip(g_h * 0.85, 0, 255))
                    b_h = int(np.clip(b_h * 0.90, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    hd.ellipse([int(hcx - hrx), int(hcy - hry), int(hcx + hrx), int(hcy + hry)], outline=OUTLINE, width=1)

    # 2. Obsidian Black Lacquer Eye Surround Patches
    for side, pcx, pcy, tilt in [("left", 50.0, 34.0, 0.25), ("right", 78.0, 34.0, -0.25)]:
        for y in range(int(pcy - 9), int(pcy + 10)):
            for x in range(int(pcx - 10), int(pcx + 11)):
                dx = x - pcx
                dy = y - pcy
                rx = dx * np.cos(tilt) - dy * np.sin(tilt)
                ry = dx * np.sin(tilt) + dy * np.cos(tilt)
                if (rx / 8.5)**2 + (ry / 7.0)**2 <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (pcx - 2))**2 + (y - (pcy - 2))**2)**0.5 / 5.0)
                    shine = max(0.0, 1.0 - ((x - (pcx - 2))**2 + (y - (pcy - 2))**2)**0.5 / 2.0)**2
                    r_lp = int(np.clip(31 + 65 * spec + 30 * shine, 0, 255))
                    g_lp = int(np.clip(26 + 60 * spec + 30 * shine, 0, 255))
                    b_lp = int(np.clip(58 + 95 * spec + 40 * shine, 0, 255))
                    head_img.putpixel((x, y), (r_lp, g_lp, b_lp, 255))

    # Eye patch outlines & brass bezel rings
    for side, pcx, pcy in [("left", 49.0, 34.0), ("right", 79.0, 34.0)]:
        for y in range(int(pcy - 8), int(pcy + 9)):
            for x in range(int(pcx - 8), int(pcx + 9)):
                dist = ((x - pcx)**2 + (y - pcy)**2)**0.5
                if dist <= 7.2 and dist >= 5.0:
                    spec = max(0.0, 1.0 - ((x - (pcx - 2))**2 + (y - (pcy - 2))**2)**0.5 / 3.5)
                    shine = max(0.0, 1.0 - ((x - (pcx - 2))**2 + (y - (pcy - 2))**2)**0.5 / 1.5)**2
                    r_bz = int(np.clip(212 + 43 * spec + 25 * shine, 0, 255))
                    g_bz = int(np.clip(160 + 80 * spec + 25 * shine, 0, 255))
                    b_bz = int(np.clip(23 + 180 * spec, 0, 255))
                    head_img.putpixel((x, y), (r_bz, g_bz, b_bz, 255))

        hd.ellipse([int(pcx - 7.0), int(pcy - 7.0), int(pcx + 7.0), int(pcy + 7.0)], outline=OUTLINE, width=1)
        hd.ellipse([int(pcx - 5.0), int(pcy - 5.0), int(pcx + 5.0), int(pcy + 5.0)], outline=OUTLINE, width=1)

        # 0-ART27 HOLLOW EYE SOCKET ASSERTION: Clear inner pixels to alpha=0!
        for y in range(int(pcy - 5), int(pcy + 6)):
            for x in range(int(pcx - 5), int(pcx + 6)):
                if ((x - pcx)**2 + (y - pcy)**2)**0.5 < 4.8:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    # 3. Dual Spherical Brass Ball-and-Socket Ear Caps (雙聯青古銅球窩半球耳罩)
    for ecx in [42.0, 86.0]:
        for y in range(int(20 - 9), int(20 + 10)):
            for x in range(int(ecx - 9), int(ecx + 10)):
                dx = x - ecx
                dy = y - 20.0
                dist = (dx**2 + dy**2)**0.5
                if dist <= 7.5:
                    spec = max(0.0, 1.0 - ((x - (ecx - 2))**2 + (y - 17)**2)**0.5 / 4.5)
                    shine = max(0.0, 1.0 - ((x - (ecx - 2))**2 + (y - 17)**2)**0.5 / 2.0)**2
                    r_e = int(np.clip(212 + 43 * spec + 30 * shine, 0, 255))
                    g_e = int(np.clip(160 + 80 * spec + 30 * shine, 0, 255))
                    b_e = int(np.clip(23 + 180 * spec, 0, 255))
                    head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        hd.ellipse([int(ecx - 7.5), int(20 - 7.5), int(ecx + 7.5), int(20 + 7.5)], outline=OUTLINE, width=1)
        hd.ellipse([int(ecx - 3.5), int(20 - 3.5), int(ecx + 3.5), int(20 + 3.5)], fill=BRASS_DARK, outline=OUTLINE)
        hd.line([(int(ecx - 2), 20), (int(ecx + 2), 20)], fill=OUTLINE, width=1)
        hd.point((int(ecx - 1), 19), fill=WHITE_SHINE)

    # 4. Nose and Cooling Mesh Mouth
    hd.polygon([(62, 42), (66, 42), (64, 45)], fill=LACQUER_BASE, outline=OUTLINE)
    hd.point((63, 42), fill=LACQUER_SHINE)

    hd.rounded_rectangle([56, 48, 72, 51], radius=1, fill=BRASS_DARK, outline=OUTLINE, width=1)
    for mx in range(58, 71, 3):
        hd.line([(mx, 49), (mx, 50)], fill=OUTLINE, width=1)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Chest & Waist Armor)
    # File: costume/costume_panda_zen_apprentice_robe.png
    # Tianyuan Dojo Stamped Apprentice Robe/Tunic (天元道場生漆沖壓練功甲)
    # - Diagonal overlap collar (斜襟) with brass frog-buttons (盤扣)
    # - Mint bamboo green trim (#4ED86A)
    # - Gold-inlaid shoulder pauldrons
    # - Hollow central aperture (center (64, 76), radius 6.5) for Taiji Gyroscope / Core!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(56, 93):
        for x in range(44, 85):
            prog = (y - 56) / 36.0
            cur_hw = 16.0 + 3.5 * np.sin(prog * np.pi)
            dx = (x - 64.0) / cur_hw
            dy = (y - 74.0) / 18.0
            dist_sq = dx**2 + dy**2

            if dist_sq <= 1.0:
                seam_x = 52.0 + prog * 24.0
                z_curv = np.sqrt(max(0.0, 1.0 - dist_sq))
                spec = max(0.0, 1.0 - ((x - 56)**2 + (y - 64)**2)**0.5 / 10.0)
                shine = max(0.0, 1.0 - ((x - 56)**2 + (y - 64)**2)**0.5 / 3.0)**2

                if x <= seam_x:
                    # Obsidian navy-blue lacquer flap
                    r_c = int(np.clip(26 + 15 * z_curv + 60 * spec + 30 * shine, 0, 255))
                    g_c = int(np.clip(22 + 15 * z_curv + 55 * spec + 30 * shine, 0, 255))
                    b_c = int(np.clip(50 + 20 * z_curv + 85 * spec + 40 * shine, 0, 255))
                else:
                    # White porcelain under-flap with cel shadow
                    r_c = int(np.clip(210 + 25 * z_curv + 25 * spec + 15 * shine - 10 * prog, 0, 255))
                    g_c = int(np.clip(210 + 23 * z_curv + 23 * spec + 15 * shine - 12 * prog, 0, 255))
                    b_c = int(np.clip(205 + 23 * z_curv + 20 * spec + 15 * shine - 15 * prog, 0, 255))

                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    cos_d.ellipse([44, 56, 84, 92], outline=OUTLINE, width=1)

    # Diagonal Collar Seam & Mint Green Silk Trim
    for y in range(56, 86):
        prog = (y - 56) / 30.0
        sx = int(52.0 + prog * 24.0)
        spec = max(0.0, 1.0 - abs(y - 68) / 18.0)
        r_m = int(np.clip(78 + 60 * spec, 0, 255))
        g_m = int(np.clip(216 + 30 * spec, 0, 255))
        b_m = int(np.clip(106 + 60 * spec, 0, 255))
        cos_d.point((sx, y), fill=(r_m, g_m, b_m, 255))
        cos_d.point((sx - 1, y), fill=MINT_LIGHT)
        cos_d.point((sx + 1, y), fill=OUTLINE)

    # Brass Frog-Buttons (盤扣) at (55, 62), (61, 70), (69, 78)
    for bx, by in [(55, 62), (61, 70), (69, 78)]:
        cos_d.rectangle([bx - 2, by - 1, bx + 2, by + 1], fill=BRASS_GOLD, outline=OUTLINE)
        cos_d.point((bx, by), fill=BRASS_SHINE)

    # Shoulder Pauldrons (x: 40..50, y: 58..68 and x: 78..88, y: 58..68)
    for px, py in [(40, 58), (78, 58)]:
        for y in range(py, py + 11):
            for x in range(px, px + 11):
                if ((x - (px + 5))**2 + (y - (py + 5))**2)**0.5 <= 5.0:
                    spec = max(0.0, 1.0 - ((x - (px + 3))**2 + (y - (py + 3))**2)**0.5 / 4.0)
                    r_p = int(np.clip(31 + 65 * spec, 0, 255))
                    g_p = int(np.clip(26 + 60 * spec, 0, 255))
                    b_p = int(np.clip(58 + 95 * spec, 0, 255))
                    costume_img.putpixel((x, y), (r_p, g_p, b_p, 255))
        cos_d.rounded_rectangle([px, py, px + 10, py + 10], radius=3, outline=OUTLINE, width=1)
        cos_d.ellipse([px + 2, py + 2, px + 8, py + 8], outline=GOLD_PRIMARY, width=1)
        cos_d.point((px + 5, py + 5), fill=GOLD_SHINE)

    # Waist Belt and Stamped Buckle
    for y in range(86, 92):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(y - 88) / 3.0)
            costume_img.putpixel((x, y), (int(25 + 30 * spec), int(20 + 30 * spec), int(45 + 40 * spec), 255))
    cos_d.rectangle([46, 86, 82, 91], outline=OUTLINE, width=1)
    cos_d.rectangle([60, 85, 68, 92], fill=BRASS_GOLD, outline=OUTLINE)
    cos_d.ellipse([62, 87, 66, 90], fill=MINT_GREEN, outline=OUTLINE)
    cos_d.point((64, 88), fill=WHITE_SHINE)

    # CRITICAL: Hollow center hole for Taiji Gyroscope / Core (center (64, 76), radius 6.5)
    for y in range(69, 84):
        for x in range(57, 72):
            if ((x - 64.0)**2 + (y - 76.0)**2)**0.5 <= 6.5:
                costume_img.putpixel((x, y), (0, 0, 0, 0))

    cos_d.ellipse([57, 69, 71, 83], outline=BRASS_GOLD, width=1)
    cos_d.ellipse([56, 68, 72, 84], outline=OUTLINE, width=1)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, Eyes & Chest Core)
    # File: optic_core/core_obsidian_amber_quartz.png
    # - Two Obsidian & Amber Quartz Convex Optical Lens Eyes at (49, 34) and (79, 34)
    # - Central Taiji Clockwork Heart Balance Gyro Gem at (64, 76)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    core_d = ImageDraw.Draw(core_img)

    for ecx in [49.0, 79.0]:
        for y in range(int(34 - 5), int(34 + 6)):
            for x in range(int(ecx - 5), int(ecx + 6)):
                dist = ((x - ecx)**2 + (y - 34.0)**2)**0.5
                if dist <= 4.7:
                    t = dist / 4.7
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - 32.5)**2)**0.5 / 2.5)
                    r_e = int(np.clip(255 * (1 - 0.2 * t) + 20 * spec, 0, 255))
                    g_e = int(np.clip(208 * (1 - 0.3 * t) + 40 * spec, 0, 255))
                    b_e = int(np.clip(40 * (1 - 0.5 * t) + 180 * spec, 0, 255))
                    core_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        core_d.ellipse([int(ecx - 4.5), int(34 - 4.5), int(ecx + 4.5), int(34 + 4.5)], outline=OUTLINE, width=1)
        core_d.ellipse([int(ecx - 2.2), int(34 - 2.2), int(ecx + 2.2), int(34 + 2.2)], outline=GOLD_DEEP, width=1)
        core_d.point((int(ecx - 1), 32), fill=WHITE_SHINE)
        core_d.point((int(ecx - 2), 33), fill=WHITE_SHINE)

    # Chest Taiji Gyro Core Gem (center (64, 76), radius 5.5)
    for y in range(70, 83):
        for x in range(58, 71):
            dx = x - 64.0
            dy = y - 76.0
            dist = (dx**2 + dy**2)**0.5
            if dist <= 5.5:
                angle = np.arctan2(dy, dx)
                spec = max(0.0, 1.0 - ((x - 62.0)**2 + (y - 74.0)**2)**0.5 / 3.0)
                if np.sin(angle) >= 0:
                    r_g = int(np.clip(255 * 0.9 + 50 * spec, 0, 255))
                    g_g = int(np.clip(208 * 0.9 + 50 * spec, 0, 255))
                    b_g = int(np.clip(40 * 0.9 + 180 * spec, 0, 255))
                else:
                    r_g = int(np.clip(78 * 0.9 + 100 * spec, 0, 255))
                    g_g = int(np.clip(216 * 0.9 + 40 * spec, 0, 255))
                    b_g = int(np.clip(106 * 0.9 + 100 * spec, 0, 255))
                core_img.putpixel((x, y), (r_g, g_g, b_g, 255))

    core_d.ellipse([58, 70, 70, 82], outline=OUTLINE, width=1)
    core_d.point((63, 74), fill=WHITE_SHINE)
    core_d.point((64, 74), fill=WHITE_SHINE)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Handheld Weapon)
    # File: weapon/wpn_panda_taiji_cestus.png
    # Zen Taiji Cog-Gauntlets / Cestus (乾坤太極機關拳套 / 破勢寸勁生漆拳環)
    # Heavy mechanical gauntlet mounted on right hand at (88, 76)
    # High-pressure miniature pneumatic cylinder, brass piston rods, cog gearing,
    # bamboo-joint knuckle plates, embossed Taiji emblem
    # Single weapon, strictly 0-MKT7 compliant!
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Arm Bracket Cuff (x: 80..88, y: 70..82)
    for y in range(70, 83):
        for x in range(80, 89):
            spec = max(0.0, 1.0 - ((x - 82)**2 + (y - 73)**2)**0.5 / 5.0)
            shine = max(0.0, 1.0 - ((x - 82)**2 + (y - 73)**2)**0.5 / 2.0)**2
            r_c = int(np.clip(31 + 65 * spec + 30 * shine, 0, 255))
            g_c = int(np.clip(26 + 60 * spec + 30 * shine, 0, 255))
            b_c = int(np.clip(58 + 95 * spec + 40 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    wd.rectangle([80, 70, 88, 82], outline=OUTLINE, width=1)
    wd.line([(80, 74), (88, 74)], fill=BRASS_GOLD, width=1)
    wd.line([(80, 78), (88, 78)], fill=BRASS_GOLD, width=1)

    # 2. High-Pressure Miniature Pneumatic Cylinder & Piston (x: 84..100, y: 64..72)
    for y in range(65, 72):
        for x in range(84, 99):
            spec = max(0.0, 1.0 - abs(y - 67) / 3.0)
            shine = max(0.0, 1.0 - abs(y - 67) / 1.5)**2
            r_s = int(np.clip(130 + 70 * spec + 40 * shine, 0, 255))
            g_s = int(np.clip(140 + 70 * spec + 40 * shine, 0, 255))
            b_s = int(np.clip(155 + 70 * spec + 40 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    wd.rounded_rectangle([84, 65, 98, 71], radius=2, outline=OUTLINE, width=1)
    wd.arc([88, 62, 96, 68], start=180, end=360, fill=BRASS_GOLD, width=1)
    wd.rectangle([82, 67, 84, 69], fill=BRASS_DARK, outline=OUTLINE)

    # 3. Heavy Stamped Brass Fist Box / Cestus Head (x: 86..106, y: 71..87)
    for y in range(71, 88):
        for x in range(86, 107):
            dx = (x - 96.0) / 10.0
            dy = (y - 79.0) / 8.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 92)**2 + (y - 75)**2)**0.5 / 6.0)
                shine = max(0.0, 1.0 - ((x - 92)**2 + (y - 75)**2)**0.5 / 2.2)**2
                r_w = int(np.clip(212 + 43 * spec + 30 * shine, 0, 255))
                g_w = int(np.clip(160 + 80 * spec + 30 * shine, 0, 255))
                b_w = int(np.clip(23 + 180 * spec, 0, 255))
                weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    wd.rounded_rectangle([86, 71, 106, 87], radius=3, outline=OUTLINE, width=1)

    # 4. Knuckle Bamboo-Joint Segments (天元破勢竹節紋)
    for ky in [74, 78, 82]:
        for y in range(ky, ky + 4):
            for x in range(103, 108):
                spec = max(0.0, 1.0 - abs(y - (ky + 1.5)) / 2.0)
                r_k = int(np.clip(220 + 35 * spec, 0, 255))
                g_k = int(np.clip(180 + 45 * spec, 0, 255))
                b_k = int(np.clip(80 + 100 * spec, 0, 255))
                weapon_img.putpixel((x, y), (r_k, g_k, b_k, 255))
        wd.rounded_rectangle([103, ky, 107, ky + 3], radius=1, outline=OUTLINE)
        wd.point((105, ky + 1), fill=WHITE_SHINE)

    # 5. Embossed Taiji Cog Emblem on Hand Backplate (center (96, 79), radius 5.0)
    for y in range(74, 85):
        for x in range(91, 102):
            dist = ((x - 96.0)**2 + (y - 79.0)**2)**0.5
            if dist <= 5.0:
                angle = np.arctan2(y - 79.0, x - 96.0)
                spec = max(0.0, 1.0 - dist / 5.0)
                if np.sin(angle) >= 0:
                    weapon_img.putpixel((x, y), (int(31 + 45 * spec), int(26 + 40 * spec), int(58 + 65 * spec), 255))
                else:
                    weapon_img.putpixel((x, y), (int(245 + 10 * spec), int(242 + 13 * spec), int(238 + 17 * spec), 255))

    wd.ellipse([91, 74, 101, 84], outline=OUTLINE, width=1)
    wd.ellipse([93, 76, 99, 82], outline=BRASS_GOLD, width=1)
    wd.ellipse([94, 77, 97, 80], fill=GOLD_PRIMARY, outline=OUTLINE)
    wd.point((95, 78), fill=WHITE_SHINE)

    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE SLICES (128x128 & 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "paint_panda_porcelain", chassis_img),
        ("head_unit", "head_panda_brass_socket_ears", head_img),
        ("winding_key", "key_panda_taiji_ruyi_brass", key_img),
        ("costume", "costume_panda_zen_apprentice_robe", costume_img),
        ("optic_core", "core_obsidian_amber_quartz", core_img),
        ("weapon", "wpn_panda_taiji_cestus", weapon_img),
        ("back_curio", "curio_panda_floating_taiji_box", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{PANDA_PD_DIR}/{slot}"
        os.makedirs(out_dir, exist_ok=True)
        dst_128 = f"{out_dir}/{item_id}.png"
        img.save(dst_128)

        # 512x512 with LANCZOS
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{out_dir}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    shutil.copyfile(f"{PANDA_PD_DIR}/winding_key/key_panda_taiji_ruyi_brass.png", f"{KEY_DIR}/key_panda_taiji_ruyi_brass.png")
    shutil.copyfile(f"{PANDA_PD_DIR}/weapon/wpn_panda_taiji_cestus.png", f"{WEAPON_DIR}/wpn_panda_taiji_cestus.png")
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

    proof_comp = f"{PANDA_PD_DIR}/proof_paperdoll_panda_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{PANDA_PD_DIR}/proof_paperdoll_panda_magenta.png"
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

    proof_7 = f"{PANDA_PD_DIR}/proof_panda_all_7_slices.png"
    strip_img.save(proof_7)
    print("  ✓ Proof images generated successfully")


if __name__ == "__main__":
    build_all()
