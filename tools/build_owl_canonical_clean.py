#!/usr/bin/env python3
"""
build_owl_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Chrono Owl (靈鐘鴞 / The Chrono Owl) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/CHRONO_OWL_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero feathers, zero bird flesh, stamped brass lamellae wings, clockface lens domes, ratchet swivel neck ring, sun-moon astrolabe key)
- references/art_direction.md (Dopamine high-saturation palette: Ivory #FFFDF8, Sky Blue #38A0FF, Brass Gold #FFD028, Mint Green #4ED86A, Warm Orange #FFA010, Outline #1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r
- Benchmarked directly against Orbit Hound, Emerald Fawn, and Xuanji Tortoise standards.
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
OWL_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/owl"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Chrono Owl Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Ivory White Enamel (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (225, 222, 215, 255)
IVORY_DEEP    = (185, 180, 172, 255)

# Midnight Blue Alloy Shell (#1F1A3A & deep metallic blue)
MIDNIGHT_BLUE  = (38, 48, 86, 255)
MIDNIGHT_LIGHT = (58, 72, 122, 255)
MIDNIGHT_SHINE = (95, 115, 175, 255)
MIDNIGHT_DARK  = (24, 30, 56, 255)

# Secondary: Sky Blue (#38A0FF)
SKY_BLUE_BASE  = (56, 160, 255, 255)
SKY_BLUE_LIGHT = (120, 195, 255, 255)
SKY_BLUE_SHINE = (180, 225, 255, 255)
SKY_BLUE_DARK  = (30, 115, 210, 255)
SKY_BLUE_DEEP  = (18, 70, 145, 255)

# Accent: Sun-Moon Astrolabe Brass & Gold (#FFD028 / #D4A017)
BRASS_GOLD    = (212, 160, 23, 255)
BRASS_LIGHT   = (255, 225, 95, 255)
BRASS_SHINE   = (255, 250, 175, 255)
BRASS_DARK    = (150, 105, 12, 255)
BRASS_DEEP    = (90, 60, 8, 255)

GOLD_PRIMARY  = (255, 208, 40, 255)
GOLD_LIGHT    = (255, 235, 115, 255)
GOLD_SHINE    = (255, 250, 185, 255)
GOLD_DARK     = (195, 145, 18, 255)

# Detail: Mint Aurora Green (#4ED86A)
MINT_GREEN    = (78, 216, 106, 255)
MINT_LIGHT    = (140, 240, 165, 255)
MINT_SHINE    = (200, 255, 215, 255)
MINT_DARK     = (36, 140, 62, 255)
MINT_DEEP     = (18, 78, 35, 255)

# Warm Highlight: Warm Orange (#FFA010)
ORANGE_BASE    = (255, 160, 16, 255)
ORANGE_LIGHT   = (255, 195, 80, 255)
ORANGE_DARK    = (195, 110, 10, 255)

# Translucent Quartz Viewport (#7EC8E3)
QUARTZ_CYAN    = (126, 200, 227, 255)
QUARTZ_LIGHT   = (190, 240, 255, 255)
QUARTZ_DARK    = (60, 140, 175, 255)

# Tungsten Talons & Dark Mechanism (#26262B)
TUNGSTEN_BASE   = (38, 38, 45, 255)
TUNGSTEN_LIGHT  = (68, 68, 80, 255)
TUNGSTEN_DARK   = (20, 20, 25, 255)

# Chrome Springs & Steel Rods
STEEL_LIGHT   = (195, 205, 220, 255)
STEEL_MID     = (130, 142, 160, 255)
STEEL_DARK    = (70, 78, 92, 255)

WHITE_SHINE   = (255, 255, 255, 255)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL CHRONO OWL SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_owl_sun_moon_astrolabe_gold.png
    # Sun-Moon Astrolabe Wind-up Key (三環日月星象黃銅發條鑰匙)
    # Socket at upper spine (64, 64)
    # Key shaft extends up and right to astrolabe center at (88, 34)
    # Three concentric astrolabe brass rings with sun/moon symbols and Differential gear arms
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Key shaft entering spine socket at (64, 64) up to (88, 34)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 64.0 + t * 24.0
        sy = 64.0 - t * 30.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(212 + 35 * spec, 0, 255))
                    g_s = int(np.clip(160 + 30 * spec, 0, 255))
                    b_s = int(np.clip(23 + 45 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 64)
    kd.ellipse([60, 60, 68, 68], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([61, 61, 67, 67], fill=BRASS_GOLD)

    # Key Head: Three-Ring Sun-Moon Astrolabe centered at (88, 34)
    kcx, kcy = 88.0, 34.0
    r_outer = 15.0
    r_mid = 10.5
    r_inner = 6.0
    r_hub = 3.0

    # Draw the concentric astrolabe rings
    for y in range(int(kcy - r_outer - 3), int(kcy + r_outer + 4)):
        for x in range(int(kcx - r_outer - 3), int(kcx + r_outer + 4)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5

            # Outer ring: dist between 13.0 and 15.5
            is_ring1 = (dist >= 12.8 and dist <= 15.2)
            # Mid ring: dist between 8.8 and 11.2
            is_ring2 = (dist >= 8.8 and dist <= 11.2)
            # Inner ring: dist between 4.8 and 6.8
            is_ring3 = (dist >= 4.8 and dist <= 6.8)
            # Center hub: dist <= 3.2
            is_hub = (dist <= 3.2)
            # 4 diagonal astrolabe spokes connecting rings (at 45, 135, 225, 315 deg)
            spoke_dist = abs(abs(dx) - abs(dy)) / 1.414
            is_spoke = (spoke_dist <= 1.2 and dist <= 14.5)

            if is_ring1 or is_ring2 or is_ring3 or is_hub or is_spoke:
                spec = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 14.0)
                shine = max(0.0, 1.0 - ((x - (kcx - 5))**2 + (y - (kcy - 5))**2)**0.5 / 5.0)**2

                # Sun crescent accent on outer ring (top right)
                if is_ring1 and dx > 0 and dy < 0:
                    r_k = int(np.clip(255 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    g_k = int(np.clip(208 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                    b_k = int(np.clip(40 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                # Moon crescent accent on mid ring (bottom left)
                elif is_ring2 and dx < 0 and dy > 0:
                    r_k = int(np.clip(180 * (0.85 + 0.25 * spec) + 50 * shine, 0, 255))
                    g_k = int(np.clip(210 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                    b_k = int(np.clip(255 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                else:
                    r_k = int(np.clip(212 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_k = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    b_k = int(np.clip(23 * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Astrolabe outlines
    kd.ellipse([int(kcx - r_outer), int(kcy - r_outer), int(kcx + r_outer), int(kcy + r_outer)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - r_mid), int(kcy - r_mid), int(kcx + r_mid), int(kcy + r_mid)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - r_inner), int(kcy - r_inner), int(kcx + r_inner), int(kcy + r_inner)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - r_hub), int(kcy - r_hub), int(kcx + r_hub), int(kcy + r_hub)], fill=GOLD_PRIMARY, outline=OUTLINE)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    # 4 small gold planet beads at 0, 90, 180, 270 deg on outer ring
    for deg in [0, 90, 180, 270]:
        rad = np.radians(deg)
        bx = int(round(kcx + 14.0 * np.cos(rad)))
        by = int(round(kcy + 14.0 * np.sin(rad)))
        kd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=GOLD_SHINE, outline=OUTLINE)

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Floating Side Satellite)
    # File: back_curio/curio_owl_floating_micro_orrery.png
    # Floating Micro-Orrery (懸浮微型太陽系天體儀)
    # Centered at (104, 60), clean & self-contained
    # Central golden sun sphere + 2 brass orbital rings with enamel planet beads (Sky Blue & Coral Red)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    ocx, ocy = 104.0, 60.0

    # 1. Outer Brass Orbital Ring (ellipse tilted at 20 deg)
    for y in range(int(ocy - 16), int(ocy + 17)):
        for x in range(int(ocx - 18), int(ocx + 19)):
            dx = x - ocx
            dy = y - ocy
            # Rotate by -20 deg
            rad = np.radians(-20)
            rx = dx * np.cos(rad) - dy * np.sin(rad)
            ry = dx * np.sin(rad) + dy * np.cos(rad)
            # Ellipse formula
            d_ring = (rx / 14.0)**2 + (ry / 7.0)**2
            if abs(d_ring - 1.0) <= 0.22:
                spec = max(0.0, 1.0 - abs(rx) / 14.0)
                curio_img.putpixel((x, y), (int(212 + 35 * spec), int(160 + 30 * spec), int(23 + 45 * spec), 255))

    # Inner Orbital Ring (tilted at 45 deg)
    for y in range(int(ocy - 12), int(ocy + 13)):
        for x in range(int(ocx - 14), int(ocx + 15)):
            dx = x - ocx
            dy = y - ocy
            rad = np.radians(45)
            rx = dx * np.cos(rad) - dy * np.sin(rad)
            ry = dx * np.sin(rad) + dy * np.cos(rad)
            d_ring = (rx / 9.5)**2 + (ry / 4.8)**2
            if abs(d_ring - 1.0) <= 0.25:
                spec = max(0.0, 1.0 - abs(rx) / 9.5)
                curio_img.putpixel((x, y), (int(180 + 30 * spec), int(140 + 25 * spec), int(30 + 40 * spec), 255))

    # Central Sun Sphere (radius 4.5)
    for y in range(int(ocy - 6), int(ocy + 7)):
        for x in range(int(ocx - 6), int(ocx + 7)):
            dx = x - ocx
            dy = y - ocy
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.5:
                spec = max(0.0, 1.0 - ((x - (ocx - 1.5))**2 + (y - (ocy - 1.5))**2)**0.5 / 5.0)
                shine = max(0.0, 1.0 - ((x - (ocx - 1.5))**2 + (y - (ocy - 1.5))**2)**0.5 / 2.0)**2
                r_sun = int(np.clip(255 * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
                g_sun = int(np.clip(208 * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
                b_sun = int(np.clip(40 * (0.6 + 0.4 * spec) + 80 * shine, 0, 255))
                curio_img.putpixel((x, y), (r_sun, g_sun, b_sun, 255))

    cd.ellipse([int(ocx - 4.5), int(ocy - 4.5), int(ocx + 4.5), int(ocy + 4.5)], outline=OUTLINE, width=1)
    cd.point((int(ocx - 1), int(ocy - 1)), fill=WHITE_SHINE)

    # Planet 1: Sky Blue Enamel Planet bead on outer ring at (116, 55)
    p1x, p1y = 116, 55
    cd.ellipse([p1x - 3, p1y - 3, p1x + 3, p1y + 3], fill=SKY_BLUE_BASE, outline=OUTLINE)
    cd.point((p1x - 1, p1y - 1), fill=SKY_BLUE_SHINE)

    # Planet 2: Mint Green Planet bead on inner ring at (97, 65)
    p2x, p2y = 97, 65
    cd.ellipse([p2x - 2, p2y - 2, p2x + 2, p2y + 2], fill=MINT_GREEN, outline=OUTLINE)
    cd.point((p2x, p2y), fill=MINT_SHINE)

    # Tiny trailing starlight sparks around curio
    for sx, sy in [(92, 52), (112, 70), (106, 44)]:
        cd.point((sx, sy), fill=GOLD_SHINE)

    # Clean thick outline on orbital elements (using immutable snapshot to prevent accidental flood-fill)
    curio_snap = np.array(curio_img)[:, :, 3] > 80
    for y in range(int(ocy - 17), int(ocy + 18)):
        for x in range(int(ocx - 19), int(ocx + 20)):
            if not curio_snap[y, x]:
                if curio_snap[y-1, x] or curio_snap[y+1, x] or curio_snap[y, x-1] or curio_snap[y, x+1]:
                    curio_img.putpixel((x, y), OUTLINE)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Core Body & Lamellae Wings)
    # File: chassis/chassis_owl_brass_lamellae_default.png
    # Features:
    # - Stamped Brass Lamellae Wings (沖壓黃銅疊片羽翼板件, 12 plates)
    # - Midnight blue alloy outer wing cover (#1F1A3A / #263056)
    # - Ivory White enamel belly plate (#FFFDF8) (x: 44..84, y: 56..96)
    # - 0-ART18: Full multi-tone shading & depth across belly
    # - Chest Tourbillon Quartz Window (x: 56..72, y: 64..78) with twin escapement balance wheels & mint hairspring
    # - Tungsten Talons (3-claw grasping perches, ground at y: 114)
    # - Strictly ZERO weapon baked in (0-ART9, 0-ART11 compliant: x >= 95 is strictly 0)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Tungsten Perch Talons (雙足三爪鎢鋼機械抓握爪)
    # Left foot at (52, 113), Right foot at (76, 113)
    for fx in [52.0, 76.0]:
        # 3 claws per foot
        for c_angle in [-0.5, 0.0, 0.5]:
            for t in np.linspace(0.0, 1.0, 12):
                cx = fx + np.sin(c_angle) * (t * 8.0)
                cy = 110.0 + t * 4.0
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if dx**2 + dy**2 <= 2:
                            spec = max(0.0, 1.0 - t * 0.7)
                            r_t = int(np.clip(38 + 30 * spec, 0, 255))
                            g_t = int(np.clip(38 + 30 * spec, 0, 255))
                            b_t = int(np.clip(45 + 35 * spec, 0, 255))
                            chassis_img.putpixel((int(cx + dx), int(cy + dy)), (r_t, g_t, b_t, 255))
        # Talon joint boss
        ch_d.ellipse([int(fx - 4), 108, int(fx + 4), 112], fill=BRASS_DARK, outline=OUTLINE)
        ch_d.ellipse([int(fx - 2), 109, int(fx + 2), 111], fill=BRASS_GOLD)

    # 3. Stamped Brass Lamellae Wings (folded at sides)
    # Left wing (x: 28..48, y: 56..96) - Midnight blue shell with brass stepped lamellae
    for plate in range(6):
        py_top = 58 + plate * 6
        py_bot = py_top + 10
        px_left = 30 + plate * 2
        px_right = 48
        # Wing plate polygon
        pts = [(px_left, py_top), (px_right, py_top), (px_right, py_bot), (px_left + 4, py_bot + 2)]
        ch_d.polygon(pts, fill=MIDNIGHT_BLUE, outline=OUTLINE)
        # Stamped brass edge on feather tips
        ch_d.line([(px_left, py_top), (px_left + 4, py_bot + 2)], fill=BRASS_GOLD, width=2)
        # Copper rivet on plate hinge
        ch_d.ellipse([px_right - 4, py_top + 2, px_right - 1, py_top + 5], fill=BRASS_SHINE, outline=OUTLINE)

    # Right wing base (x: 78..94, y: 58..92) - kept strictly x < 95 for 0-ART9/11 compliance!
    for plate in range(5):
        py_top = 60 + plate * 6
        py_bot = py_top + 9
        px_left = 78
        px_right = 92 - plate * 2
        pts = [(px_left, py_top), (px_right, py_top), (px_right - 2, py_bot + 1), (px_left, py_bot)]
        ch_d.polygon(pts, fill=MIDNIGHT_BLUE, outline=OUTLINE)
        ch_d.line([(px_right, py_top), (px_right - 2, py_bot + 1)], fill=BRASS_GOLD, width=2)
        ch_d.ellipse([px_left + 1, py_top + 2, px_left + 4, py_top + 5], fill=BRASS_SHINE, outline=OUTLINE)

    # 4. Torso: Ivory Enamel Belly Plate & Alloy Core (x: 42..86, y: 54..98)
    cx_t, cy_t = 64.0, 76.0
    for y in range(54, 99):
        for x in range(42, 87):
            dx = (x - cx_t) / 21.0
            dy = (y - cy_t) / 20.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 6))**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 6))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Ivory enamel belly with gradient warmth
                r_p = int(np.clip(255 * (1.0 - 0.16 * edge_shade) + 20 * shine, 0, 255))
                g_p = int(np.clip(253 * (1.0 - 0.15 * edge_shade) + 20 * shine, 0, 255))
                b_p = int(np.clip(248 * (1.0 - 0.12 * edge_shade) + 20 * shine, 0, 255))
                chassis_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    ch_d.ellipse([42, 54, 86, 98], outline=OUTLINE, width=1)

    # 5. Tourbillon Escapement Quartz Viewport (x: 56..72, y: 64..78)
    # Centered at (64, 71), radius ~7.0
    tcx, tcy = 64.0, 71.0
    for y in range(63, 79):
        for x in range(56, 73):
            dx = (x - tcx) / 8.0
            dy = (y - tcy) / 7.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                dist = dist_sq**0.5
                # Internal brass escapement balance wheel and mint hairspring
                is_balance_spoke = (abs(x - tcx) <= 1.5 or abs(y - tcy) <= 1.5)
                is_hairspring = ((x + y * 2) % 4 == 0 and dist > 0.3 and dist < 0.8)
                if is_balance_spoke:
                    r_v = int(np.clip(212 * (1.0 - 0.2 * dist), 0, 255))
                    g_v = int(np.clip(160 * (1.0 - 0.2 * dist), 0, 255))
                    b_v = int(np.clip(23 * (1.0 - 0.2 * dist), 0, 255))
                elif is_hairspring:
                    r_v = int(np.clip(78 + 40 * (1.0 - dist), 0, 255))
                    g_v = int(np.clip(216 + 30 * (1.0 - dist), 0, 255))
                    b_v = int(np.clip(106 + 50 * (1.0 - dist), 0, 255))
                else:
                    # High-transparency quartz blue glass
                    spec = max(0.0, 1.0 - ((x - (tcx - 2))**2 + (y - (tcy - 2))**2)**0.5 / 6.0)
                    r_v = int(np.clip(126 * (0.8 + 0.3 * spec), 0, 255))
                    g_v = int(np.clip(200 * (0.8 + 0.3 * spec), 0, 255))
                    b_v = int(np.clip(227 * (0.8 + 0.3 * spec) + 20, 0, 255))
                chassis_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    ch_d.ellipse([56, 63, 72, 79], outline=OUTLINE, width=1)
    ch_d.ellipse([57, 64, 71, 78], outline=BRASS_GOLD, width=1)
    ch_d.point((int(tcx - 2), int(tcy - 2)), fill=WHITE_SHINE)

    # 6. Strict check: Ensure weapon zone x >= 95 is completely empty (0-ART9/11)
    for y in range(H):
        for x in range(95, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_owl_brass_plume_antennas.png
    # Features:
    # - Stamped Brass Cranium Shell & 360-degree Ratchet Swivel Neck Ring
    # - Stamped Bronze Plume Antennas (一對青銅翎管微波天線羽, left 36..46, right 82..92)
    # - Golden triangular beak at center (64, 46)
    # - 0-ART27 COMPLIANT: Recessed hollow clockface eye sockets at (52, 38) and (76, 38)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # Dual Bronze Plume Antennas (翎管微波天線羽)
    # Left Plume Antenna: (36..46, 12..30), pivot at (44, 28)
    for y in range(12, 31):
        for x in range(35, 48):
            prog = (y - 12) / 18.0
            pw = 5.0 * np.sin(prog * np.pi)
            if abs(x - (40.0 + prog * 4.0)) <= pw:
                spec = max(0.0, 1.0 - abs(x - 42.0) / 4.0)
                r_e = int(np.clip(212 + 35 * spec, 0, 255))
                g_e = int(np.clip(160 + 30 * spec, 0, 255))
                b_e = int(np.clip(23 + 45 * spec, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))
    hd.ellipse([36, 12, 46, 30], outline=OUTLINE, width=1)
    # Stepped feather notches on left antenna
    for y in range(16, 28, 3):
        hd.line([(38, y), (44, y - 1)], fill=BRASS_SHINE, width=1)
    hd.ellipse([42, 27, 46, 31], fill=GOLD_PRIMARY, outline=OUTLINE)

    # Right Plume Antenna: (82..92, 12..30), pivot at (84, 28)
    for y in range(12, 31):
        for x in range(80, 93):
            prog = (y - 12) / 18.0
            pw = 5.0 * np.sin(prog * np.pi)
            if abs(x - (88.0 - prog * 4.0)) <= pw:
                spec = max(0.0, 1.0 - abs(x - 86.0) / 4.0)
                r_e = int(np.clip(212 + 35 * spec, 0, 255))
                g_e = int(np.clip(160 + 30 * spec, 0, 255))
                b_e = int(np.clip(23 + 45 * spec, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))
    hd.ellipse([82, 12, 92, 30], outline=OUTLINE, width=1)
    # Stepped feather notches on right antenna
    for y in range(16, 28, 3):
        hd.line([(84, y - 1), (90, y)], fill=BRASS_SHINE, width=1)
    hd.ellipse([82, 27, 86, 31], fill=GOLD_PRIMARY, outline=OUTLINE)

    # Ratchet Swivel Neck Ring at base (y: 52..56, x: 50..78)
    hd.ellipse([50, 52, 78, 56], fill=BRASS_DARK, outline=OUTLINE)
    for rx in range(54, 76, 4):
        hd.line([(rx, 52), (rx, 56)], fill=BRASS_SHINE, width=1)

    # Head Cranial Shell (Ivory enamel dome with Midnight blue brow cap)
    hcx, hcy = 64.0, 38.0
    for y in range(22, 54):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - hcy) / 15.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Midnight blue forehead cap (y: 22..29)
                is_cap = (y <= 29 and dist_sq <= 0.85)
                if is_cap:
                    r_h = int(np.clip(38 * (0.85 + 0.3 * spec) + 50 * shine, 0, 255))
                    g_h = int(np.clip(48 * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                    b_h = int(np.clip(86 * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                else:
                    r_h = int(np.clip(255 * (1.0 - 0.15 * edge_shade) + 20 * shine, 0, 255))
                    g_h = int(np.clip(253 * (1.0 - 0.14 * edge_shade) + 20 * shine, 0, 255))
                    b_h = int(np.clip(248 * (1.0 - 0.10 * edge_shade) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    hd.ellipse([42, 22, 86, 53], outline=OUTLINE, width=1)

    # Golden Pyramid Triangle Beak at center (64, 46)
    beak_pts = [(64, 43), (67, 49), (61, 49)]
    hd.polygon(beak_pts, fill=GOLD_PRIMARY, outline=OUTLINE)
    hd.point((64, 45), fill=WHITE_SHINE)

    # 0-ART27 Hollow Clockface Eye Sockets
    # Recessed hollow sockets at (52, 38) and (76, 38), radius 5.5
    eye_centers = [(52.0, 38.0), (76.0, 38.0)]
    r_eye_socket = 5.5
    for ecx, ecy in eye_centers:
        for y in range(int(ecy - r_eye_socket - 2), int(ecy + r_eye_socket + 3)):
            for x in range(int(ecx - r_eye_socket - 2), int(ecx + r_eye_socket + 3)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_eye_socket:
                    head_img.putpixel((x, y), (0, 0, 0, 0))
        # Concentric brass bezel around hollow sockets
        hd.ellipse([int(ecx - r_eye_socket), int(ecy - r_eye_socket),
                    int(ecx + r_eye_socket), int(ecy + r_eye_socket)], outline=OUTLINE, width=1)
        hd.ellipse([int(ecx - r_eye_socket - 1), int(ecy - r_eye_socket - 1),
                    int(ecx + r_eye_socket + 1), int(ecy + r_eye_socket + 1)], outline=BRASS_GOLD, width=1)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 22)
    # File: optic_core/face_owl_clockface_lens_dusk_gold.png
    # Features:
    # - Concentric Clockface Lenses (雙聯同心圓刻度石英鐘面目鏡)
    # - Centered exactly at (52, 38) and (76, 38)
    # - 12-hour micro dial numerals & orange ticking second hand (#FFA010)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ecx, ecy in eye_centers:
        r_lens = 5.0
        for y in range(int(ecy - r_lens - 1), int(ecy + r_lens + 2)):
            for x in range(int(ecx - r_lens - 1), int(ecx + r_lens + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    norm_dist = dist / r_lens
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.5))**2 + (y - (ecy - 1.5))**2)**0.5 / 4.0)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.5))**2 + (y - (ecy - 1.5))**2)**0.5 / 2.0)**2
                    rim = max(0.0, (norm_dist - 0.6) / 0.4)

                    # Gold/amber luminous clockface
                    r_o = int(np.clip(255 * (0.85 + 0.15 * spec) + 30 * shine - 30 * rim, 0, 255))
                    g_o = int(np.clip(208 * (0.85 + 0.15 * spec) + 40 * shine - 40 * rim, 0, 255))
                    b_o = int(np.clip(40 * (0.7 + 0.3 * spec) + 80 * shine + 20 * rim, 0, 255))
                    core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

        c_d.ellipse([int(ecx - r_lens), int(ecy - r_lens), int(ecx + r_lens), int(ecy + r_lens)], outline=OUTLINE, width=1)

        # 12 clockface dial ticks (at 12, 3, 6, 9 o'clock)
        for deg in [0, 90, 180, 270]:
            rad = np.radians(deg)
            tx = int(round(ecx + 3.8 * np.cos(rad)))
            ty = int(round(ecy + 3.8 * np.sin(rad)))
            core_img.putpixel((tx, ty), OUTLINE)

        # Orange ticking second hand (#FFA010) pointing at 10 o'clock on left, 2 o'clock on right
        target_deg = 300 if ecx < 64 else 60
        rad_hand = np.radians(target_deg)
        hx = int(round(ecx + 3.5 * np.cos(rad_hand)))
        hy = int(round(ecy + 3.5 * np.sin(rad_hand)))
        c_d.line([(int(ecx), int(ecy)), (hx, hy)], fill=ORANGE_BASE, width=1)
        core_img.putpixel((hx, hy), ORANGE_LIGHT)

        # Center jewel pivot
        c_d.ellipse([int(ecx - 1), int(ecy - 1), int(ecx + 1), int(ecy + 1)], fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_owl_dawn_astronomer_robe.png
    # Features:
    # - Dawn Astronomer Robe & Collar Capelet (晨曦觀星學者短披肩斗篷)
    # - Deep Sky Blue & Midnight Blue velvet capelet over shoulders (y: 52..70, x: 38..90)
    # - Gold star embroidery and brass brooches at collar
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ct_d = ImageDraw.Draw(costume_img)

    for y in range(52, 72):
        for x in range(38, 90):
            prog = (y - 52) / 19.0
            cw = 20.0 + 4.5 * np.sin(prog * np.pi)
            dx = abs(x - 64.0)
            if dx <= cw:
                spec = max(0.0, 1.0 - ((x - 56.0)**2 + (y - 56.0)**2)**0.5 / 15.0)
                # Royal Astronomer Sky Blue with deep midnight folds
                is_collar_lapel = (dx <= 8.0 and y <= 62)
                if is_collar_lapel:
                    r_c = int(np.clip(212 * (0.8 + 0.25 * spec), 0, 255))
                    g_c = int(np.clip(160 * (0.8 + 0.25 * spec), 0, 255))
                    b_c = int(np.clip(23 * (0.8 + 0.25 * spec), 0, 255))
                else:
                    r_c = int(np.clip(56 * (0.8 + 0.3 * spec) + 10 * np.sin(x * 0.4), 0, 255))
                    g_c = int(np.clip(160 * (0.8 + 0.3 * spec) + 15 * np.sin(y * 0.4), 0, 255))
                    b_c = int(np.clip(255 * (0.8 + 0.3 * spec) + 10 * np.sin(x * 0.3 + y * 0.3), 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    ct_d.ellipse([38, 52, 89, 71], outline=OUTLINE, width=1)

    # Gold Brooches at collar closure (64, 58)
    ct_d.ellipse([61, 55, 67, 61], fill=BRASS_GOLD, outline=OUTLINE)
    ct_d.ellipse([62, 56, 66, 60], fill=GOLD_PRIMARY)
    ct_d.point((63, 57), fill=WHITE_SHINE)

    # Embroidered gold star accents on shoulders
    for sx, sy in [(48, 62), (80, 62)]:
        ct_d.line([(sx - 2, sy), (sx + 2, sy)], fill=GOLD_PRIMARY, width=1)
        ct_d.line([(sx, sy - 2), (sx, sy + 2)], fill=GOLD_PRIMARY, width=1)
        ct_d.point((sx, sy), fill=WHITE_SHINE)

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 30, Top Layer)
    # File: weapon/weapon_owl_armillary_escapement_scepter.png
    # Features:
    # - Armillary Escapement Scepter / Celestial Orrery Wand (渾天星儀擒縱法杖 / 天文星曆權杖)
    # - Mage Magic class (`magic`)
    # - SINGLE-WIELD (0-MKT7): Left hand grips wand shaft at (28, 72)
    # - Wand head: Rotating Brass Armillary Rings at (12, 42) with central Mint Green Quartz Core (#4ED86A)
    # - Wand shaft extends from (46, 88) through grip (28, 72) up to armillary head (12, 42)
    # - STRICT ZERO pixels crossing body or reaching weapon zone x >= 95
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Wand Shaft: Straight brass rod from (46, 88) through (28, 72) to (12, 42)
    for t in np.linspace(0.0, 1.0, 75):
        lx = 46.0 - t * 34.0
        ly = 88.0 - t * 46.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    dist = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist / 1.5)
                    # Fluted brass shaft with midnight blue grips
                    is_grip = (t > 0.35 and t < 0.60)
                    if is_grip:
                        r_w = int(np.clip(38 * (0.8 + 0.3 * spec), 0, 255))
                        g_w = int(np.clip(48 * (0.8 + 0.3 * spec), 0, 255))
                        b_w = int(np.clip(86 * (0.8 + 0.3 * spec), 0, 255))
                    else:
                        r_w = int(np.clip(212 + 35 * spec, 0, 255))
                        g_w = int(np.clip(160 + 30 * spec, 0, 255))
                        b_w = int(np.clip(23 + 45 * spec, 0, 255))
                    weapon_img.putpixel((int(lx + dx), int(ly + dy)), (r_w, g_w, b_w, 255))

    wd.line([(47, 89), (11, 41)], fill=OUTLINE, width=1)

    # Rear Pommel Counterweight at (46, 88)
    wd.ellipse([44, 86, 48, 90], fill=BRASS_GOLD, outline=OUTLINE)
    wd.point((46, 88), fill=GOLD_SHINE)

    # Armillary Head centered at (12, 40)
    acx, acy = 12.0, 40.0
    # Outer armillary ring (radius 8.5)
    wd.ellipse([int(acx - 8.5), int(acy - 8.5), int(acx + 8.5), int(acy + 8.5)], outline=OUTLINE, width=1)
    wd.ellipse([int(acx - 7.5), int(acy - 7.5), int(acx + 7.5), int(acy + 7.5)], outline=BRASS_GOLD, width=1)

    # Tilted inner ring (radius 6.0, tilted)
    wd.ellipse([int(acx - 6.0), int(acy - 3.5), int(acx + 6.0), int(acy + 3.5)], outline=GOLD_PRIMARY, width=1)

    # Central Mint Green Escapement Crystal Core (#4ED86A)
    for y in range(int(acy - 4), int(acy + 5)):
        for x in range(int(acx - 4), int(acx + 5)):
            dist = ((x - acx)**2 + (y - acy)**2)**0.5
            if dist <= 3.5:
                spec = max(0.0, 1.0 - ((x - (acx - 1))**2 + (y - (acy - 1))**2)**0.5 / 3.0)
                r_c = int(np.clip(78 + 60 * spec, 0, 255))
                g_c = int(np.clip(216 + 35 * spec, 0, 255))
                b_c = int(np.clip(106 + 50 * spec, 0, 255))
                weapon_img.putpixel((x, y), (r_c, g_c, b_c, 255))
    wd.ellipse([int(acx - 3.5), int(acy - 3.5), int(acx + 3.5), int(acy + 3.5)], outline=OUTLINE, width=1)
    wd.point((int(acx - 1), int(acy - 1)), fill=WHITE_SHINE)

    # Wand Hand Grip: Left brass mechanical bird claw grasping shaft at (26..32, 70..76)
    wd.ellipse([26, 70, 32, 76], fill=BRASS_GOLD, outline=OUTLINE)
    wd.ellipse([28, 71, 31, 75], fill=GOLD_PRIMARY)
    wd.point((29, 72), fill=BRASS_SHINE)

    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE SLICES (128x128 & 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "chassis_owl_brass_lamellae_default", chassis_img),
        ("head_unit", "head_owl_brass_plume_antennas", head_img),
        ("winding_key", "key_owl_sun_moon_astrolabe_gold", key_img),
        ("costume", "costume_owl_dawn_astronomer_robe", costume_img),
        ("optic_core", "face_owl_clockface_lens_dusk_gold", core_img),
        ("weapon", "weapon_owl_armillary_escapement_scepter", weapon_img),
        ("back_curio", "curio_owl_floating_micro_orrery", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{OWL_PD_DIR}/{slot}"
        os.makedirs(out_dir, exist_ok=True)
        dst_128 = f"{out_dir}/{item_id}.png"
        img.save(dst_128)

        # 512x512 with LANCZOS
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{out_dir}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copyfile(f"{OWL_PD_DIR}/winding_key/key_owl_sun_moon_astrolabe_gold.png",
                    f"{KEY_DIR}/key_owl_sun_moon_astrolabe_gold.png")
    shutil.copyfile(f"{OWL_PD_DIR}/weapon/weapon_owl_armillary_escapement_scepter.png",
                    f"{WEAPON_DIR}/weapon_owl_armillary_escapement_scepter.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{OWL_PD_DIR}/proof_paperdoll_owl_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{OWL_PD_DIR}/proof_paperdoll_owl_magenta.png"
    magenta_bg.save(proof_mag)

    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Optic", "Costume", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, core_img, costume_img, weapon_img]

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        sd.rectangle([px, py, px + W, py + H], fill=(42, 36, 62, 255), outline=OUTLINE)
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255))

    strip_path = f"{OWL_PD_DIR}/proof_owl_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")


if __name__ == "__main__":
    build_all()
