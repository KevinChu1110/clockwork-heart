#!/usr/bin/env python3
"""
build_ram_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十九族 星盤靈羊 (The Astral Ram, ram) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/ASTRAL_RAM_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, ivory polymer armor plates,
  concentric scalloped enamel lamellae, dual phosphor-bronze balance spring horns,
  astrolabe tri-star winding key clearly protruding from silhouette,
  floating gravitational orbit rings, starlight starlight amber optic, astral resonance staff)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Ivory Polymer White (#FFFDF8)
    2. Secondary Trim: Astral Orbit Blue (#38A0FF)
    3. Accent & Seals: Coral Pink (#FF5E8A)
    4. Optic Core & LEDs: Amber Starlight (#FFD028)
    5. Balance Spring Horns: Superconducting Phosphor-Bronze (#C88A4A)
    6. Frame & Struts: Ink Stone Slate Titanium (#4A5568)
    7. Energy Aura & Crystals: Mint Nebula Glow (#4ED86A)
    8. Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
RAM_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/ram"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Astral Ram Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Ivory Polymer White (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (228, 222, 212, 255)
IVORY_DARK  = (195, 188, 175, 255)
IVORY_DEEP  = (160, 152, 140, 255)

# 2. Secondary Trim: Astral Orbit Blue (#38A0FF)
BLUE_BASE  = (56, 160, 255, 255)
BLUE_LIGHT = (112, 192, 255, 255)
BLUE_SHINE = (175, 225, 255, 255)
BLUE_DARK  = (28, 112, 204, 255)
BLUE_DEEP  = (16, 68, 140, 255)

# 3. Accent: Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 200, 220, 255)
CORAL_DARK  = (200, 50, 95, 255)
CORAL_DEEP  = (140, 25, 60, 255)

# 4. Optic Core & LEDs: Amber Starlight (#FFD028 / #FFA010)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (205, 148, 18, 255)
GOLD_DEEP  = (145, 95, 10, 255)

# 5. Balance Spring Horns: Superconducting Phosphor-Bronze (#C88A4A)
BRONZE_BASE  = (200, 138, 74, 255)
BRONZE_LIGHT = (235, 175, 105, 255)
BRONZE_SHINE = (255, 215, 155, 255)
BRONZE_DARK  = (150, 95, 42, 255)
BRONZE_DEEP  = (105, 60, 22, 255)

# 6. Frame & Struts: Ink Stone Slate Titanium (#4A5568)
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (108, 122, 145, 255)
STEEL_SHINE = (155, 170, 195, 255)
STEEL_DARK  = (48, 56, 70, 255)
STEEL_DEEP  = (30, 36, 46, 255)

# 7. Energy Aura & Crystals: Mint Nebula Glow (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)

WHITE_SHINE = (255, 255, 255, 255)


def apply_clean_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=80, ignore_regions=None) -> None:
    """Safe, non-recursive, snapshot-based 1px outline pass.
    Prevents flood-fill / propagation bugs that create rectangular black artifact blocks (0-ART29).
    """
    snapshot = img.copy()
    px_snap = snapshot.load()
    if px_snap is None:
        return

    w, h = img.size
    px_dest = img.load()
    if px_dest is None:
        return

    for y in range(h):
        for x in range(w):
            if ignore_regions:
                skip = False
                for (rx1, ry1, rx2, ry2) in ignore_regions:
                    if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                        skip = True
                        break
                if skip:
                    continue

            # If pixel is currently transparent
            if px_snap[x, y][3] < min_alpha:
                # Check 8 neighbors in snapshot
                has_solid_neighbor = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            if px_snap[nx, ny][3] >= min_alpha:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break

                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL ASTRAL RAM SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_ram_astrolabe_tri_star.png
    # Astrolabe Tri-Star Winding Key (星盤三叉星芒發條鑰匙)
    # Socket boss at spine (64, 58), shaft extends diagonally up-right to (96, 22)
    # Protrudes clearly beyond head silhouette (x: 90..116)
    # Features:
    # - Polished golden brass shaft with radial bevel shading
    # - Astrolabe Tri-Star Wings: three sculpted star-wing leaves radiating from (96, 22)
    # - Central gyroscope pivot with sapphire / ivory jewel
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 58) to (96, 22)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 32.0
        sy = 58.0 - t * 36.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 58)
    kd.ellipse([60, 54, 68, 62], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([61, 55, 67, 61], fill=GOLD_BASE)
    kd.ellipse([63, 57, 65, 59], fill=BLUE_BASE)

    # 2. Astrolabe Tri-Star Head at (96, 22)
    kcx, kcy = 96.0, 22.0

    # Three astrolabe star blades: pointing Up (-1.65), Up-Right (-0.75), Right-Down (0.15)
    star_angles = [-1.65, -0.75, 0.15]
    for ang in star_angles:
        tip_len = 16.0
        tx = kcx + np.cos(ang) * tip_len
        ty = kcy + np.sin(ang) * tip_len
        perp = ang + 1.5708

        for t in np.linspace(0.0, 1.0, 35):
            cx = kcx + t * (tx - kcx)
            cy = kcy + t * (ty - kcy)
            w_factor = np.sin(t * np.pi) * 4.6
            for s in np.linspace(-1.0, 1.0, 15):
                lx = cx + s * np.cos(perp) * w_factor
                ly = cy + s * np.sin(perp) * w_factor
                spec = max(0.0, 1.0 - abs(s))
                shine = max(0.0, (1.0 - abs(s)))**2 if t > 0.3 else 0.0

                # Shading: golden brass with subtle astral blue resonance tint
                r_l = int(np.clip(255 * (0.85 + 0.15 * spec) * (1 - 0.2*t) + 56 * 0.2 * t + 30 * shine, 0, 255))
                g_l = int(np.clip(208 * (0.85 + 0.15 * spec) * (1 - 0.2*t) + 160 * 0.2 * t + 35 * shine, 0, 255))
                b_l = int(np.clip(40 * (0.85 + 0.2 * spec) + 50 * shine + 40 * t, 0, 255))
                key_img.putpixel((int(lx), int(ly)), (r_l, g_l, b_l, 255))

        # Star tip bright tooth
        for t in np.linspace(0.1, 0.95, 25):
            vx = int(kcx + t * (tx - kcx))
            vy = int(kcy + t * (ty - kcy))
            key_img.putpixel((vx, vy), GOLD_LIGHT)

    # 3. Outer Astrolabe Calibrated Dial Ring (radius 10px from 96, 22)
    for theta in np.linspace(0, 2 * np.pi, 60):
        rx = kcx + np.cos(theta) * 10.0
        ry = kcy + np.sin(theta) * 10.0
        key_img.putpixel((int(round(rx)), int(round(ry))), GOLD_LIGHT)

    # Central Gyroscope Sapphire Jewel at (96, 22)
    kd.ellipse([int(kcx - 6), int(kcy - 6), int(kcx + 6), int(kcy + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=BLUE_BASE)
    kd.ellipse([int(kcx - 1), int(kcy - 1), int(kcx + 1), int(kcy + 1)], fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline to guarantee 0-ART29 compliance
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_ram_gravity_orbit_rings.png
    # Floating Gravitational Orbit Rings (懸浮反重力星環儀)
    # Three concentric / intersecting ultra-thin dopamine glowing orbital rings
    # Originating around (64, 60)
    # Features:
    # - Ring 1 (Astral Blue): tilted ellipse rx=34, ry=14
    # - Ring 2 (Coral Pink): reverse tilted ellipse rx=28, ry=18
    # - Ring 3 (Mint Glow): outer celestial arc with orbital micro-crystals
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Ring 1: Astral Blue Main Orbit (tilt: -0.35 rad)
    cx, cy = 64.0, 60.0
    tilt1 = -0.35
    cos1, sin1 = np.cos(tilt1), np.sin(tilt1)
    for theta in np.linspace(0, 2 * np.pi, 240):
        ex = 34.0 * np.cos(theta)
        ey = 13.5 * np.sin(theta)
        rx = cx + (ex * cos1 - ey * sin1)
        ry = cy + (ex * sin1 + ey * cos1)
        # Width 2.2px
        spec = 0.5 + 0.5 * np.sin(theta)
        r_c = int(np.clip(56 * (0.8 + 0.3 * spec) + 50 * spec, 0, 255))
        g_c = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * spec, 0, 255))
        b_c = int(np.clip(255, 0, 255))
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 1:
                    curio_img.putpixel((int(round(rx + dx)), int(round(ry + dy))), (r_c, g_c, b_c, 255))

    # Ring 2: Coral Pink Intersecting Orbit (tilt: 0.45 rad)
    tilt2 = 0.45
    cos2, sin2 = np.cos(tilt2), np.sin(tilt2)
    for theta in np.linspace(0, 2 * np.pi, 200):
        ex = 28.0 * np.cos(theta)
        ey = 16.0 * np.sin(theta)
        rx = cx + (ex * cos2 - ey * sin2)
        ry = cy + (ex * sin2 + ey * cos2)
        spec = 0.5 + 0.5 * np.cos(theta)
        r_c = int(np.clip(255, 0, 255))
        g_c = int(np.clip(94 * (0.8 + 0.3 * spec), 0, 255))
        b_c = int(np.clip(138 * (0.8 + 0.4 * spec), 0, 255))
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 1:
                    curio_img.putpixel((int(round(rx + dx)), int(round(ry + dy))), (r_c, g_c, b_c, 255))

    # Orbital Micro-Crystals (nodes along orbits)
    nodes = [
        (cx + 34.0 * cos1, cy + 34.0 * sin1, GOLD_BASE),
        (cx - 34.0 * cos1, cy - 34.0 * sin1, MINT_BASE),
        (cx + 28.0 * cos2, cy + 28.0 * sin2, BLUE_LIGHT),
        (cx - 28.0 * cos2, cy - 28.0 * sin2, CORAL_LIGHT),
    ]
    for nx, ny, color in nodes:
        cd.ellipse([int(nx - 2), int(ny - 2), int(nx + 2), int(ny + 2)], fill=color, outline=OUTLINE)
        cd.point((int(nx), int(ny)), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_ram_astral_polymer_default.png
    # Features:
    # - 2.2 Chibi high-gloss ivory polymer ram chassis (#FFFDF8)
    # - Soft ground contact shadow at (64, 116)
    # - Gold brass hooves & ankle ball joints at (48, 112) and (70, 112)
    # - Concentric scalloped enamel lamellae chest/belly plate (60:84, 48:72)
    #   yielding >= 20 unique colors (0-ART18 compliant)
    # - Right arm tucked with staff grip socket at (82, 74)
    # - Left arm balanced at (38, 78)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    ch_d.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 160))

    # 2. Hooves & Leg Struts
    # Left hoof: (48, 112), Right hoof: (70, 112)
    for fx, fy in [(48, 112), (70, 112)]:
        # Brass ankle joint
        ch_d.ellipse([fx - 3, fy - 6, fx + 3, fy - 2], fill=GOLD_BASE, outline=OUTLINE)
        # Gold-plated hoof shoe & anti-static pad
        for y in range(fy - 3, fy + 4):
            for x in range(fx - 5, fx + 6):
                dx = (x - fx) / 5.0
                dy = (y - fy) / 3.0
                if dx**2 + dy**2 <= 1.0:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                    r_f = int(np.clip(200 * (0.8 + 0.3 * spec) + 55 * spec, 0, 255))
                    g_f = int(np.clip(138 * (0.8 + 0.3 * spec) + 70 * spec, 0, 255))
                    b_f = int(np.clip(74 * (0.8 + 0.4 * spec) + 80 * spec, 0, 255))
                    chassis_img.putpixel((x, y), (r_f, g_f, b_f, 255))

    # Leg pillars connecting pelvis to hooves
    # Left leg: (54, 94) -> (48, 108)
    for t in np.linspace(0.0, 1.0, 20):
        lx = int(54 * (1 - t) + 48 * t)
        ly = int(94 * (1 - t) + 108 * t)
        for dx in range(-3, 4):
            chassis_img.putpixel((lx + dx, ly), STEEL_BASE)
    # Right leg: (68, 94) -> (70, 108)
    for t in np.linspace(0.0, 1.0, 20):
        rx = int(68 * (1 - t) + 70 * t)
        ry = int(94 * (1 - t) + 108 * t)
        for dx in range(-3, 4):
            chassis_img.putpixel((rx + dx, ry), STEEL_BASE)

    # 3. Main Torso Hull (Ivory White Polymer + Concentric Scalloped Lamellae)
    tcx, tcy = 62.0, 74.0
    trx, try_ = 18.0, 20.0

    for y in range(54, 96):
        for x in range(44, 82):
            dx = (x - tcx) / trx
            dy = (y - tcy) / try_
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 1.1))
                shine = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 0.4))**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                # Scalloped Lamellae Belly Shield (x: 52..72, y: 64..88)
                is_belly = (52 <= x <= 72) and (64 <= y <= 88) and (((x - 62)/10.0)**2 + ((y - 76)/12.0)**2 <= 1.0)
                if is_belly:
                    # Multi-tone ivory shading to satisfy 0-ART18 (>= 20 unique colors in 60:84, 48:72)
                    b_spec = max(0.0, 1.0 - ((x - 60)**2 + (y - 72)**2)**0.5 / 10.0)
                    r_b = int(np.clip(255 * (0.88 + 0.12 * b_spec) - 20 * edge_shade, 0, 255))
                    g_b = int(np.clip(253 * (0.88 + 0.12 * b_spec) - 20 * edge_shade, 0, 255))
                    b_b = int(np.clip(248 * (0.85 + 0.15 * b_spec) - 25 * edge_shade + 10 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))
                else:
                    # Primary Ivory Polymer Plate
                    r_m = int(np.clip(255 * (0.82 + 0.18 * spec) + 20 * shine - 30 * edge_shade, 0, 255))
                    g_m = int(np.clip(253 * (0.82 + 0.18 * spec) + 20 * shine - 30 * edge_shade, 0, 255))
                    b_m = int(np.clip(248 * (0.80 + 0.20 * spec) + 15 * shine - 35 * edge_shade, 0, 255))
                    chassis_img.putpixel((x, y), (r_m, g_m, b_m, 255))

    # Concentric Astrolabe Dial Lines on Chest
    for r_dial in [5, 8]:
        for ang in np.linspace(0, 2 * np.pi, 30):
            px = int(tcx + r_dial * np.cos(ang))
            py = int(tcy + r_dial * np.sin(ang))
            chassis_img.putpixel((px, py), GOLD_BASE)

    # 4. Arms & Hands
    # Left Arm & Shoulder: balanced at (38, 78)
    for y in range(48, 62):
        for x in range(38, 50):
            if ((x - 44.0)/6.0)**2 + ((y - 55.0)/7.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), IVORY_SHADE)
    for t in np.linspace(0.0, 1.0, 20):
        ax = int(50 * (1 - t) + 38 * t)
        ay = int(66 * (1 - t) + 78 * t)
        for d in range(-2, 3):
            chassis_img.putpixel((ax + d, ay), STEEL_LIGHT)
    ch_d.ellipse([34, 75, 42, 83], fill=IVORY_BASE, outline=OUTLINE)
    ch_d.point((38, 79), fill=GOLD_BASE)

    # Right Arm & Shoulder: tucked at ribs with weapon grip at (82, 74)
    # Strictly stop before x=94 to comply with 0-ART9/11
    for y in range(58, 72):
        for x in range(74, 86):
            if ((x - 80.0)/6.0)**2 + ((y - 65.0)/7.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), IVORY_SHADE)
    for t in np.linspace(0.0, 1.0, 20):
        ax = int(72 * (1 - t) + 82 * t)
        ay = int(66 * (1 - t) + 74 * t)
        if ax < 94:
            for d in range(-2, 3):
                if ax + d < 94:
                    chassis_img.putpixel((ax + d, ay), STEEL_LIGHT)
    ch_d.ellipse([78, 70, 86, 78], fill=IVORY_BASE, outline=OUTLINE)
    ch_d.ellipse([80, 72, 84, 76], fill=GOLD_BASE)

    # 5. Neck Collar & Upper Shoulder Foundation (44..84, 46..58)
    for y in range(46, 58):
        for x in range(44, 85):
            if ((x - 64.0)/20.0)**2 + ((y - 54.0)/10.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), IVORY_SHADE)

    # Zero out strictly at x >= 94 (0-ART9/11)
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr).copy()

    apply_clean_outline(chassis_img)
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_ram_spiral_balance_horns.png
    # Features:
    # - Sculpted ivory polymer ram faceplate & hood (x: 44..84, y: 22..52)
    # - Cute ear protectors / acoustic baffle caps at (36, 36) and (92, 36)
    # - Dual Phosphor-Bronze Balance Spring Spiral Horns:
    #   Left horn spirals outward from (46, 32) to (20, 24) and loops back to (28, 42)
    #   Right horn spirals outward from (82, 32) to (108, 24) and loops back to (100, 42)
    # - STRICT HOLLOW EYE SOCKETS AT (52, 40) AND (76, 40) (0-ART27 compliant)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Sculpted Ivory Faceplate
    hcx, hcy = 64.0, 40.0
    hrx, hry = 22.0, 18.0

    for y in range(22, 59):
        for x in range(40, 89):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / (hrx * 1.1))
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / (hrx * 0.4))**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                r_h = int(np.clip(255 * (0.85 + 0.15 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                g_h = int(np.clip(253 * (0.85 + 0.15 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                b_h = int(np.clip(248 * (0.82 + 0.18 * spec) + 15 * shine - 30 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Forehead Mold Seam & Gold Star Stud
    for y in range(24, 32):
        head_img.putpixel((64, y), BLUE_BASE)
    hd.ellipse([62, 25, 66, 29], fill=GOLD_BASE, outline=OUTLINE)

    # 2. Side Ear Protectors (36, 36) and (92, 36)
    for ex, ey in [(36, 36), (92, 36)]:
        hd.ellipse([ex - 4, ey - 5, ex + 4, ey + 5], fill=IVORY_BASE, outline=OUTLINE)
        hd.ellipse([ex - 2, ey - 3, ex + 2, ey + 3], fill=BLUE_BASE)
        hd.point((ex, ey), fill=WHITE_SHINE)

    # 3. Dual Phosphor-Bronze Balance Spring Spiral Horns
    # Left Horn: Spiral from (46, 32) -> curve up-left to (22, 24) -> loop down-in to (28, 42)
    left_horn_pts = [
        np.array([46.0, 32.0]),
        np.array([40.0, 27.0]),
        np.array([32.0, 23.0]),
        np.array([23.0, 23.0]),
        np.array([19.0, 28.0]),
        np.array([19.0, 34.0]),
        np.array([23.0, 40.0]),
        np.array([29.0, 42.0])
    ]
    # Right Horn: Spiral from (82, 32) -> curve up-right to (106, 24) -> loop down-in to (100, 42)
    right_horn_pts = [
        np.array([82.0, 32.0]),
        np.array([88.0, 27.0]),
        np.array([96.0, 23.0]),
        np.array([105.0, 23.0]),
        np.array([109.0, 28.0]),
        np.array([109.0, 34.0]),
        np.array([105.0, 40.0]),
        np.array([99.0, 42.0])
    ]

    for horn in [left_horn_pts, right_horn_pts]:
        # Collect dense centerline points
        dense_pts = []
        for i in range(len(horn) - 1):
            p0, p1 = horn[i], horn[i+1]
            for t in np.linspace(0.0, 1.0, 20):
                dense_pts.append(p0 + t * (p1 - p0))

        total_pts = len(dense_pts)
        for idx, pt in enumerate(dense_pts):
            t_ratio = idx / float(total_pts)
            hr = 5.2 * (1.0 - 0.45 * t_ratio)
            # Tangent & normal
            if idx < total_pts - 1:
                tangent = dense_pts[idx+1] - pt
            else:
                tangent = pt - dense_pts[idx-1]
            t_norm = np.linalg.norm(tangent)
            if t_norm > 1e-4:
                normal = np.array([-tangent[1], tangent[0]]) / t_norm
            else:
                normal = np.array([0.0, 1.0])

            # Draw smooth metallic cross-slice
            for s in np.linspace(-1.0, 1.0, int(hr * 4 + 1)):
                pos = pt + s * normal * hr
                ix, iy = int(round(pos[0])), int(round(pos[1]))
                if 0 <= ix < W and 0 <= iy < H:
                    spec = max(0.0, 1.0 - abs(s))
                    shine = max(0.0, 1.0 - abs(s + 0.3))**2

                    # Spiral Balance Spring coils (alternating micro-ribs)
                    coil_phase = (idx % 4)
                    if coil_phase == 0 or coil_phase == 1:
                        # Bright polished bronze spring ribbon
                        r_b = int(np.clip(235 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        g_b = int(np.clip(175 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        b_b = int(np.clip(105 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    else:
                        # Spring gap shade
                        r_b = int(np.clip(150 * (0.8 + 0.2 * spec), 0, 255))
                        g_b = int(np.clip(95 * (0.8 + 0.2 * spec), 0, 255))
                        b_b = int(np.clip(42 * (0.8 + 0.3 * spec), 0, 255))

                    # Outer edge lightguide line
                    if s > 0.65:
                        r_b = int(np.clip(56 * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
                        g_b = int(np.clip(160 * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
                        b_b = int(np.clip(255 * (0.85 + 0.15 * spec), 0, 255))

                    head_img.putpixel((ix, iy), (r_b, g_b, b_b, 255))

        # Horn Tip: Astral Blue Pulse Jewel with Brass Ring
        tip_pt = horn[-1]
        hd.ellipse([int(tip_pt[0] - 3), int(tip_pt[1] - 3), int(tip_pt[0] + 3), int(tip_pt[1] + 3)], fill=GOLD_BASE, outline=OUTLINE)
        hd.ellipse([int(tip_pt[0] - 2), int(tip_pt[1] - 2), int(tip_pt[0] + 2), int(tip_pt[1] + 2)], fill=BLUE_BASE)
        hd.point((int(tip_pt[0]), int(tip_pt[1])), fill=WHITE_SHINE)

    # Clean outline pass BEFORE hollowing eye sockets
    apply_clean_outline(head_img, ignore_regions=[(47, 35, 57, 45), (71, 35, 81, 45)])

    # 4. Strict Hollow Eye Sockets for 0-ART27 (alpha == 0 at eye zones)
    # Left eye socket at (52, 40), Right eye socket at (76, 40)
    # Ensure radius ~4.2 around (52, 40) and (76, 40) is strictly 0 alpha!
    h_arr = np.array(head_img)
    for ey, ex in [(40, 52), (40, 76)]:
        for y in range(ey - 5, ey + 6):
            for x in range(ex - 5, ex + 6):
                if (x - ex)**2 + (y - ey)**2 <= 18:
                    h_arr[y, x, :] = 0
    head_img = Image.fromarray(h_arr, "RGBA").copy()

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_ram_gravity_starlight_robe.png
    # Features:
    # - Starlight Gravity Mage Robe (星軌漫步者引力法袍)
    # - Astral Blue (#38A0FF) anti-static polymer mantle
    # - Coral Pink (#FF5E8A) piped edges and gold brass buckles
    # - Multi-tier scalloped enamel chest plate (x: 52..72, y: 62..82)
    # - 0-ART26b compliant: strictly ZERO pixels at y >= 96 (no lower legs/feet baked)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # Mantle Body (x: 44..80, y: 56..88)
    for y in range(56, 89):
        for x in range(44, 81):
            dx = (x - 62.0) / 18.0
            dy = (y - 70.0) / 16.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 66)**2)**0.5 / 16.0)
                edge = max(0.0, (dx**2 + dy**2 - 0.4) / 0.6)
                r_c = int(np.clip(56 * (0.8 + 0.35 * spec) - 20 * edge, 0, 255))
                g_c = int(np.clip(160 * (0.8 + 0.35 * spec) - 20 * edge, 0, 255))
                b_c = int(np.clip(255 * (0.85 + 0.15 * spec) + 15 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Coral Pink Collar Trim & Hem (y: 56..60 and y: 84..88)
    for x in range(48, 77):
        costume_img.putpixel((x, 56), CORAL_BASE)
        costume_img.putpixel((x, 57), CORAL_LIGHT)
        if 46 <= x <= 78:
            costume_img.putpixel((x, 86), CORAL_BASE)
            costume_img.putpixel((x, 87), CORAL_DARK)

    # Gold Astrolabe Buckle & Observation Window at (62, 68)
    cos_d.ellipse([58, 64, 66, 72], fill=GOLD_DARK, outline=OUTLINE)
    cos_d.ellipse([59, 65, 65, 71], fill=GOLD_BASE)
    cos_d.ellipse([61, 67, 63, 69], fill=MINT_BASE)
    cos_d.point((62, 68), fill=WHITE_SHINE)

    # Shoulder Epaulets at (44, 58) and (80, 58)
    for sx in [44, 80]:
        cos_d.ellipse([sx - 3, 58 - 3, sx + 3, 58 + 3], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.point((sx, 58), fill=WHITE_SHINE)

    # Strict check: 0-ART26b compliance (no pixels at y >= 96)
    cos_arr = np.array(costume_img)
    cos_arr[96:, :, :] = 0
    costume_img = Image.fromarray(cos_arr).copy()

    apply_clean_outline(costume_img)
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_ram_starlight_amber_optic.png
    # Features:
    # - Starlight Amber LED Matrix Optic (#FFD028 / #FFA010)
    # - Centers precisely aligned with head sockets: Left (52, 40), Right (76, 40)
    # - Solid lens center (alpha=255) with star reticle (0-ART27 compliant)
    # - Cheerful blush LED matrix indicator dots at (44, 46) and (84, 46)
    # - Cute small digital mouth line at (64, 47)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(core_img)

    for ecx, ecy in [(52.0, 40.0), (76.0, 40.0)]:
        # Solid circular lens housing & retaining bezel
        for y in range(int(ecy - 6), int(ecy + 7)):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= 4.8:
                    norm = dist / 4.8
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 4.0)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 1.8)**2

                    if norm >= 0.85:
                        # Gold retaining bezel ring
                        r_o = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                        g_o = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                        b_o = int(np.clip(40 * (0.8 + 0.5 * spec), 0, 255))
                    else:
                        # Starlight Amber LED Crystal
                        r_o = int(np.clip(255, 0, 255))
                        g_o = int(np.clip(208 * (0.75 + 0.35 * spec) + 30 * shine, 0, 255))
                        b_o = int(np.clip(40 * (0.7 + 0.6 * spec) + 80 * shine, 0, 255))

                    core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

        # Star reticle & white highlight
        core_img.putpixel((int(ecx), int(ecy)), WHITE_SHINE)
        core_img.putpixel((int(ecx - 1), int(ecy)), GOLD_LIGHT)
        core_img.putpixel((int(ecx + 1), int(ecy)), GOLD_LIGHT)
        core_img.putpixel((int(ecx), int(ecy - 1)), GOLD_LIGHT)
        core_img.putpixel((int(ecx), int(ecy + 1)), GOLD_LIGHT)

    # Coral Pink LED Blush Dots
    for bx in [44, 84]:
        cod.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=CORAL_BASE)
        cod.point((bx, 46), fill=CORAL_LIGHT)

    # Digital Mouth Indicator
    cod.line([(62, 47), (64, 48), (66, 47)], fill=OUTLINE, width=1)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_ram_astral_spiral_staff.png
    # Features:
    # - Astral Spiral Resonance Staff (星軌游絲共鳴杖)
    # - Held in right hand at (82, 74) (0-MKT7 single-wield compliant)
    # - Titanium & bronze shaft extending up to (100, 32)
    # - Astrolabe celestial sphere & anti-gravity mint crystal at (100, 32)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Staff Shaft from (80, 80) to (100, 34)
    p_base = np.array([78.0, 82.0])
    p_head = np.array([100.0, 34.0])
    staff_vec = p_head - p_base
    staff_len = float(np.linalg.norm(staff_vec))
    staff_dir = staff_vec / staff_len
    staff_perp = np.array([-staff_dir[1], staff_dir[0]])

    for t in np.linspace(0.0, 1.0, 60):
        pos = p_base + t * staff_vec
        for s in np.linspace(-1.5, 1.5, 7):
            pp = pos + s * staff_perp
            ix, iy = int(round(pp[0])), int(round(pp[1]))
            if 0 <= ix < W and 0 <= iy < H:
                spec = max(0.0, 1.0 - abs(s) / 1.5)
                # Bronze / titanium alternating winding ribs
                is_rib = int(t * 24) % 2 == 0
                if is_rib:
                    r_w = int(np.clip(200 * (0.8 + 0.3 * spec) + 50 * spec, 0, 255))
                    g_w = int(np.clip(138 * (0.8 + 0.3 * spec) + 50 * spec, 0, 255))
                    b_w = int(np.clip(74 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
                else:
                    r_w = int(np.clip(74 * (0.8 + 0.4 * spec), 0, 255))
                    g_w = int(np.clip(85 * (0.8 + 0.4 * spec), 0, 255))
                    b_w = int(np.clip(104 * (0.8 + 0.4 * spec), 0, 255))
                weapon_img.putpixel((ix, iy), (r_w, g_w, b_w, 255))

    # Base Counterweight Finial at (78, 82)
    wd.ellipse([76, 80, 80, 84], fill=GOLD_BASE, outline=OUTLINE)

    # 2. Astrolabe Sphere & Crystal at (100, 32)
    scx, scy = 100.0, 32.0
    # Outer armillary ring
    for ang in np.linspace(0, 2 * np.pi, 50):
        rx = scx + 8.0 * np.cos(ang)
        ry = scy + 8.0 * np.sin(ang)
        weapon_img.putpixel((int(round(rx)), int(round(ry))), GOLD_LIGHT)

    # Diagonal celestial ring
    for ang in np.linspace(0, 2 * np.pi, 50):
        rx = scx + 8.0 * np.cos(ang) * 0.7 - 8.0 * np.sin(ang) * 0.7
        ry = scy + 8.0 * np.cos(ang) * 0.4 + 8.0 * np.sin(ang) * 0.4
        weapon_img.putpixel((int(round(rx)), int(round(ry))), BLUE_LIGHT)

    # Core Anti-Gravity Mint Crystal at (100, 32)
    wd.ellipse([int(scx - 4), int(scy - 4), int(scx + 4), int(scy + 4)], fill=MINT_BASE, outline=OUTLINE)
    wd.ellipse([int(scx - 2), int(scy - 2), int(scx + 2), int(scy + 2)], fill=MINT_LIGHT)
    wd.point((int(scx), int(scy)), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_ram_astrolabe_tri_star", key_img),
        ("back_curio", "curio_ram_gravity_orbit_rings", curio_img),
        ("chassis", "chassis_ram_astral_polymer_default", chassis_img),
        ("costume", "costume_ram_gravity_starlight_robe", costume_img),
        ("head_unit", "head_ram_spiral_balance_horns", head_img),
        ("optic_core", "face_ram_starlight_amber_optic", core_img),
        ("weapon", "weapon_ram_astral_spiral_staff", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{RAM_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{RAM_PD_DIR}/winding_key/key_ram_astrolabe_tri_star.png",
                    f"{KEY_DIR}/key_ram_astrolabe_tri_star.png")
    shutil.copyfile(f"{RAM_PD_DIR}/weapon/weapon_ram_astral_spiral_staff.png",
                    f"{WEAPON_DIR}/weapon_ram_astral_spiral_staff.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order by layer_z_index:
    # z=5: winding_key
    # z=8: back_curio
    # z=10: chassis
    # z=20: head_unit
    # z=25: costume
    # z=30: optic_core
    # z=40: weapon
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{RAM_PD_DIR}/proof_paperdoll_ram_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{RAM_PD_DIR}/proof_paperdoll_ram_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Optic", "Costume", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, core_img, costume_img, weapon_img]

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255))

    strip_path = f"{RAM_PD_DIR}/proof_ram_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/ram_idle_hd.png)
    # ─────────────────────────────────────────────────────────────
    showcase_dir = f"{REPO_ROOT}/game/assets/sprites/player/showcase"
    os.makedirs(showcase_dir, exist_ok=True)
    comp_512 = composite.resize((512, 512), Image.Resampling.LANCZOS)
    cbox = comp_512.getbbox()
    if cbox:
        char_crop = comp_512.crop(cbox)
        sh_scale = 1000.0 / char_crop.height
        sc_w = int(round(char_crop.width * sh_scale))
        sc_h = int(round(char_crop.height * sh_scale))
        scaled_showcase = char_crop.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

        showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_paste_x = (800 - sc_w) // 2
        sc_paste_y = 1120 - sc_h

        sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_sdraw = ImageDraw.Draw(sc_shadow)
        sc_sdraw.ellipse((400 - 180, 1120 - 18, 400 + 180, 1120 + 18), fill=(31, 26, 58, 110))
        sc_shadow = sc_shadow.filter(ImageFilter.GaussianBlur(radius=10))

        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))
        showcase_dst = f"{showcase_dir}/ram_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
