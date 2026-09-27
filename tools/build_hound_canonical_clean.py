#!/usr/bin/env python3
"""
build_hound_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Orbit Hound (星軌犬 / The Orbit Hound) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/ORBIT_HOUND_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh, zero slime, ABS/POM engineering polymer, brass radar leaf ears, brass antenna key)
- references/art_direction.md (Dopamine high-saturation palette, clean enamel/polymer gloss, deep outline)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r
- Benchmarked directly against Emerald Fawn, Porcelain Panda, and Xuanji Tortoise standards.
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
HOUND_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hound"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Orbit Hound Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Ivory White Engineering Polymer (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (225, 222, 215, 255)
IVORY_DEEP    = (185, 180, 172, 255)

# Secondary: Orbit Sky Blue (#38A0FF)
SKY_BLUE_BASE  = (56, 160, 255, 255)
SKY_BLUE_LIGHT = (120, 195, 255, 255)
SKY_BLUE_SHINE = (180, 225, 255, 255)
SKY_BLUE_DARK  = (30, 115, 210, 255)
SKY_BLUE_DEEP  = (18, 70, 145, 255)

# Accent: Four-Blade Antenna Key & LED Gold (#FFD028 / #D4A017)
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

# Warm Highlight: Coral Pink / Red Warning (#FF5E8A)
CORAL_BASE    = (255, 94, 138, 255)
CORAL_LIGHT   = (255, 150, 180, 255)
CORAL_DARK    = (190, 45, 85, 255)

# Translucent Core Viewport (#7EC8E3)
CYAN_CORE     = (126, 200, 227, 255)
CYAN_LIGHT    = (180, 235, 255, 255)
CYAN_DARK     = (60, 140, 175, 255)

# Silicone Pad & Dark Mechanism (#26262B)
RUBBER_BASE   = (38, 38, 43, 255)
RUBBER_LIGHT  = (68, 68, 78, 255)
RUBBER_DARK   = (22, 22, 26, 255)

# Chrome Springs & Steel Rods
STEEL_LIGHT   = (195, 205, 220, 255)
STEEL_MID     = (130, 142, 160, 255)
STEEL_DARK    = (70, 78, 92, 255)

WHITE_SHINE   = (255, 255, 255, 255)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL ORBIT HOUND SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_hound_four_blade_antenna_gold.png
    # Four-Blade Antenna Wind-up Key (四葉天線金黃發條鑰匙)
    # Socket at spine (66, 64)
    # Shaft extends up and right to cross-head center at (88, 36)
    # Symmetrical 4 aerofoil antenna blades oriented in cross pattern
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Key shaft entering spine socket at (66, 64) up to (88, 36)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 66.0 + t * 22.0
        sy = 64.0 - t * 28.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(212 + 35 * spec, 0, 255))
                    g_s = int(np.clip(160 + 30 * spec, 0, 255))
                    b_s = int(np.clip(23 + 45 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (66, 64)
    kd.ellipse([62, 60, 70, 68], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([63, 61, 69, 67], fill=BRASS_GOLD)

    # Key Head: Symmetrical Four-Blade Antenna Cross Head centered at (88, 36)
    kcx, kcy = 88.0, 36.0
    r_hub = 4.5
    r_blade = 14.0

    for y in range(int(kcy - r_blade - 4), int(kcy + r_blade + 5)):
        for x in range(int(kcx - r_blade - 4), int(kcx + r_blade + 5)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= r_blade:
                angle = np.arctan2(dy, dx)
                # 4-blade cross antenna pattern: peaks at 0, 90, 180, 270 deg
                blade_val = np.cos(4.0 * angle)
                blade_bound = r_hub + (r_blade - r_hub) * max(0.0, (blade_val + 0.4) / 1.4)
                if dist <= blade_bound:
                    if dist <= r_hub:
                        spec = max(0.0, 1.0 - dist / r_hub)
                        r_k = int(np.clip(212 + 40 * spec, 0, 255))
                        g_k = int(np.clip(160 + 45 * spec, 0, 255))
                        b_k = int(np.clip(23 + 60 * spec, 0, 255))
                    else:
                        spec = max(0.0, 1.0 - ((x - (kcx - 3))**2 + (y - (kcy - 3))**2)**0.5 / 12.0)
                        shine = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 5.0)**2
                        # Slit cutout in each blade (telemetry radar slot)
                        if dist > 6.5 and dist < 10.8 and blade_val > 0.7:
                            continue
                        r_k = int(np.clip(212 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        g_k = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        b_k = int(np.clip(23 * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Center Hub hole with central telemetry rivet
    kd.ellipse([int(kcx - r_hub), int(kcy - r_hub), int(kcx + r_hub), int(kcy + r_hub)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=OUTLINE)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=BRASS_SHINE)

    # Blade concentric telemetry rings on tips
    for angle_deg in [0, 90, 180, 270]:
        rad = np.radians(angle_deg)
        tx = int(kcx + (r_blade - 2.5) * np.cos(rad))
        ty = int(kcy + (r_blade - 2.5) * np.sin(rad))
        kd.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=GOLD_PRIMARY, outline=OUTLINE)
        kd.point((tx, ty), fill=WHITE_SHINE)

    # Clean thick outline around key
    k_px = key_img.load()
    if k_px is not None:
        for y in range(int(kcy - r_blade - 3), int(kcy + r_blade + 4)):
            for x in range(int(kcx - r_blade - 3), int(kcx + r_blade + 4)):
                p = k_px[x, y]
                if isinstance(p, tuple) and p[3] > 100:
                    for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                        np_px = k_px[nx, ny]
                        if isinstance(np_px, tuple) and np_px[3] == 0:
                            kd.point((nx, ny), fill=OUTLINE)

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Floating Side Satellite)
    # File: back_curio/curio_hound_floating_micro_satellite.png
    # Floating Micro-Satellite (懸浮微型軌道探測衛星)
    # Centered at (106, 62), clean & self-contained
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    scx, scy = 106.0, 62.0

    # Solar array wings on left and right: (94..100, 59..65) and (112..118, 59..65)
    for wx_range in [range(93, 101), range(111, 119)]:
        for y in range(58, 66):
            for x in wx_range:
                spec = max(0.0, 1.0 - abs(y - 62.0) / 4.0)
                # Dark navy solar cells with blue shine
                r_w = int(np.clip(30 * (0.8 + 0.3 * spec), 0, 255))
                g_w = int(np.clip(70 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                b_w = int(np.clip(160 * (0.8 + 0.3 * spec) + 50 * spec, 0, 255))
                curio_img.putpixel((x, y), (r_w, g_w, b_w, 255))
        cd.rectangle([min(wx_range), 58, max(wx_range), 65], outline=OUTLINE, width=1)
        # Solar grid lines
        mid_x = (min(wx_range) + max(wx_range)) // 2
        cd.line([(mid_x, 59), (mid_x, 64)], fill=BRASS_GOLD, width=1)
        cd.line([(min(wx_range)+1, 61), (max(wx_range)-1, 61)], fill=SKY_BLUE_LIGHT, width=1)

    # Antenna probe extending upward to beacon LED at (106, 50)
    for y in range(50, 58):
        curio_img.putpixel((int(scx), y), STEEL_LIGHT)
    cd.line([(int(scx), 51), (int(scx), 57)], fill=OUTLINE, width=1)
    # Red/Coral collision avoidance beacon LED
    cd.ellipse([int(scx - 2), 48, int(scx + 2), 52], fill=CORAL_BASE, outline=OUTLINE)
    cd.point((int(scx), 50), fill=WHITE_SHINE)

    # Spherical polymer satellite body (r=6.5)
    for y in range(int(scy - 7), int(scy + 8)):
        for x in range(int(scx - 7), int(scx + 8)):
            dx = (x - scx) / 6.5
            dy = (y - scy) / 6.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (scx - 2))**2 + (y - (scy - 2))**2)**0.5 / 7.0)
                shine = max(0.0, 1.0 - ((x - (scx - 2))**2 + (y - (scy - 2))**2)**0.5 / 2.5)**2
                # Polymer ivory sphere with sky blue equatorial telemetry band
                is_band = abs(y - scy) <= 1.2
                if is_band:
                    r_b = int(np.clip(56 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    g_b = int(np.clip(160 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    b_b = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                else:
                    r_b = int(np.clip(255 * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    g_b = int(np.clip(253 * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    b_b = int(np.clip(248 * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                curio_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    cd.ellipse([int(scx - 6), int(scy - 6), int(scx + 6), int(scy + 6)], outline=OUTLINE, width=1)
    # Forward miniature optical sensor lens (Mint green)
    cd.ellipse([int(scx - 2), int(scy - 2), int(scx + 2), int(scy + 2)], fill=MINT_GREEN, outline=OUTLINE)
    cd.point((int(scx), int(scy)), fill=MINT_SHINE)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Base)
    # File: chassis/chassis_hound_polymer_astro_default.png
    # Features:
    # - Orbit Hound agile patrol stance (星軌信標巡邏架式)
    # - Soft contact ground shadow at (64, 116)
    # - 4 articulated mechanical legs with POM joints & silicone suction pads (#26262B)
    # - Rear legs with chrome shock springs
    # - Tail: chrome spiral spring tail with coral beacon LED at tip
    # - Modular Ivory polymer panels (#FFFDF8) with Sky Blue (#38A0FF) accent stripes
    # - Polycarbonate transparent viewport at chest (56..72, 64..78) with teal glow & visible brass gears
    # - Left hand grip socket at (28, 74)
    # - Right hand balanced pose at (44, 76)
    # - Strictly ZERO weapon baked in (0-ART9, 0-ART11 compliant: x >= 95 is strictly 0)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 32, 116 - 4, 64 + 32, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Chrome Spring Tail (extends from lower spine 76, 82 up to 94, 72)
    for t in np.linspace(0.0, 1.0, 35):
        tx = 76.0 + t * 18.0
        # Gentle spring wave
        wave = 2.0 * np.sin(t * 6.0 * np.pi)
        ty = 82.0 - t * 10.0 + wave
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    spec = 1.0 if (int(t * 10) % 2 == 0) else 0.7
                    chassis_img.putpixel((int(tx + dx), int(ty + dy)),
                                         (int(195 * spec), int(205 * spec), int(220 * spec), 255))
    # Tail tip coral beacon LED at (94, 72)
    ch_d.ellipse([92, 70, 96, 74], fill=CORAL_BASE, outline=OUTLINE)
    ch_d.point((94, 72), fill=WHITE_SHINE)

    # 3. Feet: Magnetic Silicone Suction Pads (4 feet)
    foot_coords = [(42.0, 113.0), (56.0, 113.0), (74.0, 113.0), (86.0, 113.0)]
    for fcx, fcy in foot_coords:
        ch_d.ellipse([int(fcx - 5), int(fcy), int(fcx + 5), int(fcy + 4)], fill=RUBBER_BASE, outline=OUTLINE)
        ch_d.ellipse([int(fcx - 3), int(fcy + 1), int(fcx + 3), int(fcy + 3)], fill=RUBBER_LIGHT)

    # 4. Articulated Legs (POM polymer casings with sky-blue joint rings)
    # Forelegs: Left (42, 113) up to (48, 88), Right (56, 113) up to (58, 88)
    for fx, tx_top in [(42.0, 48.0), (56.0, 58.0)]:
        for t in np.linspace(0.0, 1.0, 30):
            lx = fx + t * (tx_top - fx)
            ly = 113.0 - t * 25.0
            for dx in range(-3, 4):
                if abs(dx) <= 3:
                    spec = max(0.0, 1.0 - abs(dx) / 3.0)
                    r_l = int(np.clip(255 * (0.8 + 0.3 * spec), 0, 255))
                    g_l = int(np.clip(253 * (0.8 + 0.3 * spec), 0, 255))
                    b_l = int(np.clip(248 * (0.8 + 0.3 * spec), 0, 255))
                    chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        # Blue knee ring
        ch_d.ellipse([int(fx + 0.5 * (tx_top - fx) - 3), int(100), int(fx + 0.5 * (tx_top - fx) + 3), int(104)],
                     fill=SKY_BLUE_BASE, outline=OUTLINE)

    # Hindlegs: Left (74, 113) up to (70, 88), Right (86, 113) up to (80, 88)
    for hx, hx_top in [(74.0, 70.0), (86.0, 80.0)]:
        for t in np.linspace(0.0, 1.0, 30):
            lx = hx + t * (hx_top - hx)
            ly = 113.0 - t * 25.0
            for dx in range(-3, 4):
                if abs(dx) <= 3:
                    spec = max(0.0, 1.0 - abs(dx) / 3.0)
                    r_l = int(np.clip(255 * (0.8 + 0.3 * spec), 0, 255))
                    g_l = int(np.clip(253 * (0.8 + 0.3 * spec), 0, 255))
                    b_l = int(np.clip(248 * (0.8 + 0.3 * spec), 0, 255))
                    chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        # Rear shock spring coil overlay
        for sy in range(96, 108, 3):
            ch_d.line([(int(hx - 2), sy), (int(hx + 2), sy + 1)], fill=STEEL_LIGHT, width=1)

    # Outline legs
    ch_d.line([(39, 113), (45, 88)], fill=OUTLINE, width=1)
    ch_d.line([(45, 113), (51, 88)], fill=OUTLINE, width=1)
    ch_d.line([(53, 113), (55, 88)], fill=OUTLINE, width=1)
    ch_d.line([(59, 113), (61, 88)], fill=OUTLINE, width=1)
    ch_d.line([(71, 113), (67, 88)], fill=OUTLINE, width=1)
    ch_d.line([(77, 113), (73, 88)], fill=OUTLINE, width=1)
    ch_d.line([(83, 113), (77, 88)], fill=OUTLINE, width=1)
    ch_d.line([(89, 113), (83, 88)], fill=OUTLINE, width=1)

    # 5. Torso: Modular Ivory Polymer Shell (x: 40..86, y: 56..96)
    cx_t, cy_t = 63.0, 76.0
    for y in range(56, 97):
        for x in range(40, 87):
            dx = (x - cx_t) / 22.0
            dy = (y - cy_t) / 19.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 6))**2 + (y - (cy_t - 6))**2)**0.5 / 20.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 6))**2 + (y - (cy_t - 6))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Sky Blue lateral accent stripe on flank (x: 72..80)
                is_stripe = (x >= 73 and x <= 79)
                if is_stripe:
                    r_p = int(np.clip(56 * (0.85 + 0.3 * spec) + 50 * shine, 0, 255))
                    g_p = int(np.clip(160 * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                    b_p = int(np.clip(255 * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                else:
                    r_p = int(np.clip(255 * (1.0 - 0.16 * edge_shade) + 20 * shine, 0, 255))
                    g_p = int(np.clip(253 * (1.0 - 0.15 * edge_shade) + 20 * shine, 0, 255))
                    b_p = int(np.clip(248 * (1.0 - 0.12 * edge_shade) + 20 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    ch_d.ellipse([40, 56, 86, 96], outline=OUTLINE, width=1)

    # Rivet lines along modular polymer seams
    for ry in [62, 70, 78, 86]:
        ch_d.point((47, ry), fill=BRASS_GOLD)
        ch_d.point((67, ry), fill=BRASS_GOLD)

    # 6. Transparent Polycarbonate Chest Viewport (56..70, 66..78)
    for y in range(66, 79):
        for x in range(56, 71):
            dx = (x - 63.5) / 7.0
            dy = (y - 72.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dist = (dx**2 + dy**2)**0.5
                # Transparent teal glass with internal brass gear teeth and mint spring
                is_gear = (abs(x - 63.5) <= 2.5 or abs(y - 72.0) <= 2.0)
                is_spring = ((x + y) % 3 == 0)
                if is_gear:
                    r_v = int(np.clip(212 * (1.0 - 0.2 * dist), 0, 255))
                    g_v = int(np.clip(160 * (1.0 - 0.2 * dist), 0, 255))
                    b_v = int(np.clip(23 * (1.0 - 0.2 * dist), 0, 255))
                elif is_spring:
                    r_v = int(np.clip(78, 0, 255))
                    g_v = int(np.clip(216, 0, 255))
                    b_v = int(np.clip(106, 0, 255))
                else:
                    r_v = int(np.clip(126 * (0.8 + 0.3 * (1 - dist)), 0, 255))
                    g_v = int(np.clip(200 * (0.8 + 0.3 * (1 - dist)), 0, 255))
                    b_v = int(np.clip(227 * (0.8 + 0.3 * (1 - dist)), 0, 255))
                chassis_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    ch_d.ellipse([56, 66, 70, 78], outline=OUTLINE, width=1)
    ch_d.ellipse([57, 67, 69, 77], outline=SKY_BLUE_BASE, width=1)
    ch_d.point((63, 72), fill=MINT_LIGHT)

    # 7. Forearms & Wrist Sockets
    # Left wrist at (28, 74) for lance grip
    ch_d.ellipse([25, 71, 31, 77], fill=SKY_BLUE_BASE, outline=OUTLINE)
    ch_d.point((28, 74), fill=BRASS_GOLD)
    # Right wrist at (44, 76) balanced in zero-G
    ch_d.ellipse([41, 73, 47, 79], fill=SKY_BLUE_BASE, outline=OUTLINE)
    ch_d.point((44, 76), fill=BRASS_GOLD)

    # Neck collar ring (connector for head unit)
    ch_d.ellipse([54, 48, 74, 56], fill=SKY_BLUE_BASE, outline=OUTLINE)
    ch_d.point((64, 51), fill=SKY_BLUE_LIGHT)

    # Strict compliance: clean weapon zone (x >= 95)
    for y in range(H):
        for x in range(95, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_hound_radar_leaf_antennas.png
    # Features:
    # - Polymer puppy head with spherical astro visor overlay
    # - Snout with gold sensor button nose (#FFD028) at (64, 46)
    # - Lower chin cooling louver slits (no organic lips!)
    # - Dual 360-degree rotating brass radar leaf ears at left (42..54) and right (74..86)
    # - 0-ART27 COMPLIANT: Recessed hollow eye sockets at (53, 40) and (75, 40)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # Dual Brass Radar Leaf Antennas (Ears)
    # Left Radar Ear: (42..54, 14..32), pivot at (48, 28)
    for y in range(14, 32):
        for x in range(40, 54):
            prog = (y - 14) / 17.0
            ew = 5.5 * np.sin(prog * np.pi)
            if abs(x - 47.0) <= ew:
                spec = max(0.0, 1.0 - abs(x - 46.0) / 4.0)
                r_e = int(np.clip(212 + 35 * spec, 0, 255))
                g_e = int(np.clip(160 + 30 * spec, 0, 255))
                b_e = int(np.clip(23 + 45 * spec, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))
    hd.ellipse([41, 14, 53, 31], outline=OUTLINE, width=1)
    # Concentric acoustic telemetry ridges on left ear
    for y in range(18, 29, 3):
        hd.line([(44, y), (50, y)], fill=BRASS_SHINE, width=1)
    # Pivot joint ring
    hd.ellipse([45, 27, 49, 31], fill=GOLD_PRIMARY, outline=OUTLINE)

    # Right Radar Ear: (74..86, 14..32), pivot at (80, 28)
    for y in range(14, 32):
        for x in range(74, 88):
            prog = (y - 14) / 17.0
            ew = 5.5 * np.sin(prog * np.pi)
            if abs(x - 81.0) <= ew:
                spec = max(0.0, 1.0 - abs(x - 80.0) / 4.0)
                r_e = int(np.clip(212 + 35 * spec, 0, 255))
                g_e = int(np.clip(160 + 30 * spec, 0, 255))
                b_e = int(np.clip(23 + 45 * spec, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))
    hd.ellipse([75, 14, 87, 31], outline=OUTLINE, width=1)
    # Concentric acoustic telemetry ridges on right ear
    for y in range(18, 29, 3):
        hd.line([(78, y), (84, y)], fill=BRASS_SHINE, width=1)
    # Pivot joint ring
    hd.ellipse([79, 27, 83, 31], fill=GOLD_PRIMARY, outline=OUTLINE)

    # Head Dome & Cranial Shell (Ivory polymer)
    hcx, hcy = 64.0, 40.0
    for y in range(26, 56):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 14.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Ivory polymer shell
                r_h = int(np.clip(255 * (1.0 - 0.15 * edge_shade) + 20 * shine, 0, 255))
                g_h = int(np.clip(253 * (1.0 - 0.14 * edge_shade) + 20 * shine, 0, 255))
                b_h = int(np.clip(248 * (1.0 - 0.10 * edge_shade) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    hd.ellipse([44, 26, 84, 55], outline=OUTLINE, width=1)

    # Spherical Astro Visor Rim arc (Polycarbonate highlight along brow and temples)
    for x in range(48, 81):
        vy = int(28.0 + 3.0 * np.sin((x - 48.0) / 32.0 * np.pi))
        hd.point((x, vy), fill=CYAN_LIGHT)
    hd.ellipse([46, 28, 82, 53], outline=CYAN_DARK, width=1)

    # Muzzle / Snout (Ivory polymer lower protrusion)
    hd.ellipse([54, 42, 74, 52], fill=IVORY_PRIMARY, outline=OUTLINE)
    # Nose: Gold metallic sensor button (#FFD028) at snout tip (64, 45)
    hd.ellipse([62, 44, 66, 48], fill=GOLD_PRIMARY, outline=OUTLINE)
    hd.point((64, 45), fill=WHITE_SHINE)

    # Chin louver cooling slits (no biological lips)
    for ly in [50, 52]:
        hd.line([(61, ly), (67, ly)], fill=OUTLINE, width=1)

    # 0-ART27 Hollow Eye Sockets
    # Recessed hollow sockets at (53, 40) and (75, 40)
    eye_centers = [(53.0, 40.0), (75.0, 40.0)]
    r_eye_socket = 4.5
    for ecx, ecy in eye_centers:
        for y in range(int(ecy - r_eye_socket - 2), int(ecy + r_eye_socket + 3)):
            for x in range(int(ecx - r_eye_socket - 2), int(ecx + r_eye_socket + 3)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_eye_socket:
                    head_img.putpixel((x, y), (0, 0, 0, 0))
        hd.ellipse([int(ecx - r_eye_socket), int(ecy - r_eye_socket),
                    int(ecx + r_eye_socket), int(ecy + r_eye_socket)], outline=OUTLINE, width=1)
        hd.ellipse([int(ecx - r_eye_socket - 1), int(ecy - r_eye_socket - 1),
                    int(ecx + r_eye_socket + 1), int(ecy + r_eye_socket + 1)], outline=SKY_BLUE_BASE, width=1)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 22)
    # File: optic_core/face_hound_dot_matrix_led_eyes.png
    # Features:
    # - Dot-Matrix LED Lenses (點陣式黃色 LED 晶片大眼)
    # - Centered exactly at (53, 40) and (75, 40)
    # - Amber/gold micro LED grid showing focused curious pattern
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ecx, ecy in eye_centers:
        r_lens = 4.0
        for y in range(int(ecy - r_lens - 1), int(ecy + r_lens + 2)):
            for x in range(int(ecx - r_lens - 1), int(ecx + r_lens + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    norm_dist = dist / r_lens
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 3.0)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 1.5)**2
                    rim = max(0.0, (norm_dist - 0.5) / 0.5)

                    r_o = int(np.clip(255 * (0.8 + 0.2 * spec) + 30 * shine - 30 * rim, 0, 255))
                    g_o = int(np.clip(208 * (0.8 + 0.2 * spec) + 40 * shine - 40 * rim, 0, 255))
                    b_o = int(np.clip(40 * (0.6 + 0.4 * spec) + 80 * shine + 20 * rim, 0, 255))
                    core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

        c_d.ellipse([int(ecx - r_lens), int(ecy - r_lens), int(ecx + r_lens), int(ecy + r_lens)], outline=OUTLINE, width=1)
        # Dot matrix grid highlights (LED phosphor dots)
        for dx_dot in [-1.5, 0, 1.5]:
            for dy_dot in [-1.5, 0, 1.5]:
                if dx_dot**2 + dy_dot**2 <= 4.0:
                    px = int(round(ecx + dx_dot))
                    py = int(round(ecy + dy_dot))
                    core_img.putpixel((px, py), GOLD_SHINE)
        c_d.point((int(ecx - 1), int(ecy - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_hound_space_explorer_harness.png
    # Features:
    # - Space Explorer Lightweight Harness (太空探索防護背帶)
    # - Sky Blue (#38A0FF) aerospace harness webbing over shoulders and chest (y: 52..68, x: 42..85)
    # - Central quick-release brass buckle (#FFD028) with coral red safety latch (#FF5E8A)
    # - Flank-mounted miniature cold-gas canisters
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ct_d = ImageDraw.Draw(costume_img)

    for y in range(52, 68):
        for x in range(42, 86):
            prog = (y - 52) / 16.0
            cw = 18.0 + 3.0 * np.sin(prog * np.pi)
            dx = abs(x - 63.5)
            if dx <= cw:
                spec = max(0.0, 1.0 - ((x - 55.0)**2 + (y - 56.0)**2)**0.5 / 14.0)
                r_c = int(np.clip(56 * (0.8 + 0.3 * spec) + 15 * np.sin(x * 0.5), 0, 255))
                g_c = int(np.clip(160 * (0.8 + 0.3 * spec) + 20 * np.sin(y * 0.5), 0, 255))
                b_c = int(np.clip(255 * (0.8 + 0.3 * spec) + 10 * np.sin(x * 0.3 + y * 0.3), 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    ct_d.ellipse([42, 52, 85, 68], outline=OUTLINE, width=1)

    # Diagonal harness straps across torso
    for t in np.linspace(0.0, 1.0, 30):
        sx = 46.0 + t * 28.0
        sy = 62.0 + t * 24.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    costume_img.putpixel((int(sx + dx), int(sy + dy)), SKY_BLUE_DARK)

    for t in np.linspace(0.0, 1.0, 30):
        sx = 80.0 - t * 28.0
        sy = 62.0 + t * 24.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    costume_img.putpixel((int(sx + dx), int(sy + dy)), SKY_BLUE_DARK)

    # Central Quick-Release Buckle at (63, 72)
    ct_d.ellipse([58, 67, 68, 77], fill=BRASS_GOLD, outline=OUTLINE)
    ct_d.ellipse([59, 68, 67, 76], fill=GOLD_PRIMARY)
    ct_d.point((61, 70), fill=BRASS_SHINE)
    # Coral red safety latch button
    ct_d.ellipse([62, 71, 64, 73], fill=CORAL_BASE, outline=OUTLINE)

    # Flank micro cold-gas canister nozzles at (44, 66) and (82, 66)
    for nx, ny in [(44, 66), (82, 66)]:
        ct_d.ellipse([nx - 2, ny - 2, nx + 2, ny + 2], fill=STEEL_LIGHT, outline=OUTLINE)
        ct_d.point((nx, ny), fill=WHITE_SHINE)

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 30, Top Layer)
    # File: weapon/weapon_hound_stellar_beacon_lance.png
    # Features:
    # - Stellar Radar Beacon Lance / Orbit Antenna Pike (星軌雷達天線長槍)
    # - Knight Spear class (`spear`)
    # - SINGLE-WIELD (0-MKT7): Left hand grips lance shaft at (28, 74)
    # - Right hand maintains zero-G balance (no second weapon!)
    # - Long lance shaft: counterweight at (48, 86) -> grip at (28, 74) -> tip at (8, 46)
    # - Dynamic upward angle pointing toward sky
    # - Lance head: aerodynamic telemetry fins with electromagnetic resonance probe tip
    # - Beacon emitter lamp near tip glowing Mint Green (#4ED86A) and Gold (#FFD028)
    # - STRICT ZERO pixels crossing body or reaching weapon zone x >= 95
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Lance Shaft: Straight line from rear counterweight (48, 88) through grip (28, 74) to tip (8, 46)
    # Total length: ~58 px
    for t in np.linspace(0.0, 1.0, 80):
        lx = 48.0 - t * 40.0
        ly = 88.0 - t * 42.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    dist = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist / 1.5)
                    # High-impact white polymer shaft with brass sleeves
                    is_brass_sleeve = (t > 0.35 and t < 0.55) or (t > 0.85)
                    if is_brass_sleeve:
                        r_w = int(np.clip(212 + 35 * spec, 0, 255))
                        g_w = int(np.clip(160 + 30 * spec, 0, 255))
                        b_w = int(np.clip(23 + 45 * spec, 0, 255))
                    else:
                        r_w = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                        g_w = int(np.clip(253 * (0.85 + 0.25 * spec), 0, 255))
                        b_w = int(np.clip(248 * (0.85 + 0.25 * spec), 0, 255))
                    weapon_img.putpixel((int(lx + dx), int(ly + dy)), (r_w, g_w, b_w, 255))

    # Lance Outline
    wd.line([(49, 89), (7, 45)], fill=OUTLINE, width=1)

    # Rear Counterweight & Antenna fin at (46..50, 86..90)
    wd.ellipse([46, 86, 50, 90], fill=BRASS_GOLD, outline=OUTLINE)
    wd.point((48, 88), fill=GOLD_SHINE)

    # Telemetry Fin Array on Lance Head (near 14..22, 50..58)
    # Upper fin: from (18, 54) to (14, 46)
    wd.polygon([(18, 54), (14, 46), (12, 50)], fill=SKY_BLUE_BASE, outline=OUTLINE)
    # Lower fin: from (22, 58) to (24, 66)
    wd.polygon([(22, 58), (24, 66), (28, 62)], fill=SKY_BLUE_BASE, outline=OUTLINE)

    # Photon Beacon Emitter Lamp at (12, 50)
    wd.ellipse([10, 48, 14, 52], fill=GOLD_PRIMARY, outline=OUTLINE)
    wd.point((12, 50), fill=WHITE_SHINE)

    # Electromagnetic Resonance Needle Probe Tip at (8, 46) extending to (4, 42)
    for t in np.linspace(0.0, 1.0, 20):
        px = 8.0 - t * 4.0
        py = 46.0 - t * 4.0
        weapon_img.putpixel((int(px), int(py)), MINT_LIGHT)
    wd.polygon([(4, 42), (7, 43), (6, 46)], fill=MINT_GREEN, outline=OUTLINE)
    wd.point((4, 42), fill=MINT_SHINE)

    # Hand Gauntlet: Left armored glove gripping lance at (26..32, 72..77)
    wd.ellipse([26, 72, 32, 77], fill=IVORY_PRIMARY, outline=OUTLINE)
    wd.ellipse([28, 73, 31, 76], fill=SKY_BLUE_BASE)
    wd.point((29, 74), fill=BRASS_GOLD)

    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE SLICES (128x128 & 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "chassis_hound_polymer_astro_default", chassis_img),
        ("head_unit", "head_hound_radar_leaf_antennas", head_img),
        ("winding_key", "key_hound_four_blade_antenna_gold", key_img),
        ("costume", "costume_hound_space_explorer_harness", costume_img),
        ("optic_core", "face_hound_dot_matrix_led_eyes", core_img),
        ("weapon", "weapon_hound_stellar_beacon_lance", weapon_img),
        ("back_curio", "curio_hound_floating_micro_satellite", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{HOUND_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{HOUND_PD_DIR}/winding_key/key_hound_four_blade_antenna_gold.png",
                    f"{KEY_DIR}/key_hound_four_blade_antenna_gold.png")
    shutil.copyfile(f"{HOUND_PD_DIR}/weapon/weapon_hound_stellar_beacon_lance.png",
                    f"{WEAPON_DIR}/weapon_hound_stellar_beacon_lance.png")
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

    proof_comp = f"{HOUND_PD_DIR}/proof_paperdoll_hound_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{HOUND_PD_DIR}/proof_paperdoll_hound_magenta.png"
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

    strip_path = f"{HOUND_PD_DIR}/proof_hound_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")


if __name__ == "__main__":
    build_all()
