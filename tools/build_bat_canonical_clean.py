#!/usr/bin/env python3
"""
build_bat_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十三族 星翼蝙蝠 (The Starwing Bat, bat) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/STARWING_BAT_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological tissue, aerospace engineering polymers,
  dual parabolic sonar radar ears, dual amber quartz night optics,
  six-segment folding luminescent starwing mantle, zero-g orbital stealth flight harness,
  orbital dual-ring pulsar winding key, superconducting pulse astral shuriken)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Matte Aurora Purple-Black (#1F1A3A)
    2. Secondary Hull: Obsidian Engineering Plastic (#2B2836)
    3. Neon Mint: Radar Circuits & LEDs (#4ED86A)
    4. Electric Sky: Luminescent Starwing Coolant Membrane (#38A0FF)
    5. Coral Pulse: Mag-Grip Silicone Paws & Seals (#FF5E8A)
    6. Solar Amber: Dual Quartz Night Optics & Shuriken Tips (#FFD028 / #FFA010)
    7. Enamel Ivory: Ceramic Chest Anvil & Cheek Armor (#FFFDF8)
    8. Warm Outline: Deep Hand-drawn Brown-Black (#2E1F18)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
BAT_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bat"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Starwing Bat Specification)
OUTLINE = (46, 31, 24, 255)            # #2E1F18 Deep warm brown hand-drawn thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Matte Aurora Deep Purple-Black (#1F1A3A)
POLY_BASE  = (31, 26, 58, 255)
POLY_LIGHT = (55, 48, 88, 255)
POLY_SHINE = (85, 75, 125, 255)
POLY_DARK  = (22, 18, 42, 255)
POLY_DEEP  = (15, 12, 28, 255)

# 2. Secondary Hull: Obsidian Engineering Plastic (#2B2836)
OBS_BASE  = (43, 40, 54, 255)
OBS_LIGHT = (68, 64, 82, 255)
OBS_SHINE = (98, 92, 115, 255)
OBS_DARK  = (28, 26, 36, 255)
OBS_DEEP  = (18, 16, 24, 255)

# 3. Neon Mint: Radar Circuits & LEDs (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (130, 235, 150, 255)
MINT_SHINE = (195, 250, 205, 255)
MINT_DARK  = (45, 165, 70, 255)

# 4. Electric Sky: Luminescent Starwing Coolant Membrane (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 195, 255, 255)
SKY_SHINE = (185, 228, 255, 255)
SKY_DARK  = (25, 115, 205, 255)

# 5. Coral Pulse: Mag-Grip Silicone Paws & Seals (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 200, 220, 255)
CORAL_DARK  = (200, 50, 95, 255)

# 6. Solar Amber & Gold (#FFD028 / #FFA010)
AMBER_BASE  = (255, 208, 40, 255)
AMBER_LIGHT = (255, 235, 115, 255)
AMBER_SHINE = (255, 250, 185, 255)
AMBER_DARK  = (210, 145, 15, 255)
AMBER_DEEP  = (140, 90, 8, 255)

ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_DARK  = (190, 105, 8, 255)

# 7. Enamel Ivory: Ceramic Chest Anvil & Cheek Armor (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (220, 215, 205, 255)
IVORY_DARK  = (185, 180, 170, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL STARWING BAT SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_bat_orbital_pulsar_key.png
    # Orbital Dual-Ring Pulsar Winding Key (星穹雙環脈衝發條鑰匙)
    # Socket boss at spine (64, 58), shaft extends diagonally up-right to (88, 24)
    # Protrudes clearly beyond head silhouette (x: 74..104, y: 10..38)
    # Features:
    # - Aerospace polished brass & electric sky fluorescent composite dual-ring gyroscope
    # - Outer ring (r=9.5), inner concentric ring (r=5.5)
    # - Central 4-pointed pulsar star insignia (#FFD028 & #FFFDF8)
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from socket (64, 58) to gyroscope hub (88, 24)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 24.0
        sy = 58.0 - t * 34.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Base socket collar at spine (64, 58)
    kd.ellipse([64 - 5, 58 - 5, 64 + 5, 58 + 5], fill=AMBER_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 58 - 3, 64 + 3, 58 + 3], fill=AMBER_BASE)
    kd.ellipse([64 - 1, 58 - 1, 64 + 1, 58 + 1], fill=SKY_BASE)

    # 2. Concentric Dual-Ring Gyroscope at (88, 24)
    kcx, kcy = 88.0, 24.0

    # (A) Outer Gyro Ring: r_inner=7.5, r_outer=10.5
    r_out_max = 10.5
    r_out_min = 7.5
    for y in range(int(kcy - r_out_max - 2), int(kcy + r_out_max + 3)):
        for x in range(int(kcx - r_out_max - 2), int(kcx + r_out_max + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if r_out_min <= dist <= r_out_max:
                norm_r = (dist - r_out_min) / (r_out_max - r_out_min)
                spec = max(0.0, np.sin(norm_r * np.pi))
                shine = max(0.0, 1.0 - ((x - (kcx - 2.5))**2 + (y - (kcy - 2.5))**2)**0.5 / 5.0)**2
                # Golden brass with electric sky fluorescent rim
                is_sky_edge = (dist >= 9.8)
                if is_sky_edge:
                    r_w = int(np.clip(56 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_w = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    b_w = int(np.clip(255 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                else:
                    r_w = int(np.clip(255 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    g_w = int(np.clip(208 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    b_w = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # (B) Inner Gyro Ring: r_in_min=4.2, r_in_max=6.2
    r_in_max = 6.2
    r_in_min = 4.2
    for y in range(int(kcy - r_in_max - 1), int(kcy + r_in_max + 2)):
        for x in range(int(kcx - r_in_max - 1), int(kcx + r_in_max + 2)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if r_in_min <= dist <= r_in_max:
                norm_r = (dist - r_in_min) / (r_in_max - r_in_min)
                spec = max(0.0, np.sin(norm_r * np.pi))
                r_w = int(np.clip(56 * (0.85 + 0.3 * spec), 0, 255))
                g_w = int(np.clip(160 * (0.85 + 0.3 * spec), 0, 255))
                b_w = int(np.clip(255 * (0.85 + 0.3 * spec), 0, 255))
                key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # (C) Four Outer Micro-Pulsar Pins (N, S, W, E) with Coral Pink damping dots
    pin_defs = [
        (0.0, -11.5), (0.0, 11.5), (-11.5, 0.0), (11.5, 0.0)
    ]
    for px_off, py_off in pin_defs:
        tx = int(round(kcx + px_off))
        ty = int(round(kcy + py_off))
        kd.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=CORAL_BASE, outline=OUTLINE_KEY)
        kd.point((tx, ty), fill=WHITE_SHINE)

    # (D) Central 4-pointed Pulsar Star Insignia & Optical Bearing Hub
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=POLY_BASE, outline=OUTLINE_KEY)
    # 4-pointed diamond star
    star_poly = [
        (kcx, kcy - 4.5), (kcx + 1.5, kcy), (kcx, kcy + 4.5), (kcx - 1.5, kcy)
    ]
    kd.polygon(star_poly, fill=AMBER_LIGHT)
    star_poly_h = [
        (kcx - 4.5, kcy), (kcx, kcy + 1.5), (kcx + 4.5, kcy), (kcx, kcy - 1.5)
    ]
    kd.polygon(star_poly_h, fill=AMBER_BASE)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_bat_articulated_starwing_mantle.png
    # Six-Segment Folding Luminescent Starwing Mantle (六聯折疊螢光星翼披風)
    # Features:
    # - Left Wing (3 segments) spreading from spine (60, 56) out to (18, 48), (14, 66), (24, 82)
    # - Right Wing (3 segments) spreading from spine (68, 56) out to (82, 50), (86, 64), (78, 78)
    #   (tucked nicely on right side to avoid clipping weapon grip)
    # - High-tensile POM ribs (POLY_BASE & OBS_BASE)
    # - Luminescent Electric Sky (#38A0FF) coolant membrane with soft transparency & highlights
    # - Neon Mint (#4ED86A) aerodynamic trailing edge wiring
    # - Central spinal micro-thruster housing (54..74, 58..72)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Luminescent Electric Sky Coolant Membrane (Drawn first under ribs)
    # Left wing membrane triangles:
    left_wing_poly = [
        (60, 56), (42, 44), (20, 48), (14, 62), (22, 74), (34, 84), (54, 76), (62, 64)
    ]
    # Right wing membrane triangles (folded tighter):
    right_wing_poly = [
        (66, 56), (78, 46), (88, 52), (86, 66), (78, 78), (68, 72)
    ]

    for poly in [left_wing_poly, right_wing_poly]:
        # Draw translucent gradient membrane
        cd.polygon(poly, fill=SKY_BASE)

    # Shade the membrane surfaces with rich gradient and coolant flow lines
    for y in range(40, 88):
        for x in range(12, 92):
            if curio_img.getpixel((x, y))[3] > 0:
                dist_cx = abs(x - 64.0)
                norm_d = dist_cx / 45.0
                spec = max(0.0, 1.0 - abs(y - 62.0) / 24.0)
                shine = max(0.0, 1.0 - ((x - 30.0)**2 + (y - 56.0)**2)**0.5 / 18.0)

                # Electric sky with glowing neon cyan-mint gradients
                r_m = int(np.clip(56 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                g_m = int(np.clip(160 * (0.8 + 0.35 * spec) + 60 * shine, 0, 255))
                b_m = int(np.clip(255 * (0.85 + 0.15 * spec) + 30 * shine, 0, 255))
                curio_img.putpixel((x, y), (r_m, g_m, b_m, 230))

    # 2. Articulated POM Wing Ribs (Three on Left, Three on Right)
    left_ribs = [
        ((60.0, 56.0), (42.0, 44.0), (20.0, 48.0)),
        ((60.0, 58.0), (36.0, 58.0), (14.0, 62.0)),
        ((60.0, 62.0), (40.0, 72.0), (22.0, 74.0)),
        ((60.0, 64.0), (46.0, 80.0), (34.0, 84.0))
    ]
    for seg in left_ribs:
        for i in range(len(seg) - 1):
            (x0, y0), (x1, y1) = seg[i], seg[i+1]
            for t in np.linspace(0.0, 1.0, 20):
                rx = x0 + t * (x1 - x0)
                ry = y0 + t * (y1 - y0)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        curio_img.putpixel((int(rx + dx), int(ry + dy)), POLY_BASE)
        # Rib joint bulb
        for (jx, jy) in seg:
            cd.ellipse([jx - 2, jy - 2, jx + 2, jy + 2], fill=OBS_BASE, outline=OUTLINE)
            cd.point((int(jx), int(jy)), fill=MINT_LIGHT)

    right_ribs = [
        ((66.0, 56.0), (76.0, 48.0), (88.0, 52.0)),
        ((66.0, 60.0), (80.0, 62.0), (86.0, 66.0)),
        ((66.0, 64.0), (76.0, 74.0), (78.0, 78.0))
    ]
    for seg in right_ribs:
        for i in range(len(seg) - 1):
            (x0, y0), (x1, y1) = seg[i], seg[i+1]
            for t in np.linspace(0.0, 1.0, 20):
                rx = x0 + t * (x1 - x0)
                ry = y0 + t * (y1 - y0)
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        curio_img.putpixel((int(rx + dx), int(ry + dy)), POLY_BASE)
        for (jx, jy) in seg:
            cd.ellipse([jx - 2, jy - 2, jx + 2, jy + 2], fill=OBS_BASE, outline=OUTLINE)
            cd.point((int(jx), int(jy)), fill=MINT_LIGHT)

    # 3. Aerodynamic Trailing Edge Neon Mint Sensor Strips
    trailing_pts_left = [(20, 48), (14, 62), (22, 74), (34, 84)]
    for i in range(len(trailing_pts_left) - 1):
        cd.line([trailing_pts_left[i], trailing_pts_left[i+1]], fill=MINT_BASE, width=1)

    trailing_pts_right = [(88, 52), (86, 66), (78, 78)]
    for i in range(len(trailing_pts_right) - 1):
        cd.line([trailing_pts_right[i], trailing_pts_right[i+1]], fill=MINT_BASE, width=1)

    # 4. Central Spinal Micro-Thruster & Attitude Control Housing (54..74, 58..74)
    for y in range(58, 75):
        for x in range(54, 75):
            dx = (x - 64.0) / 9.0
            dy = (y - 66.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 9.0)
                r_h = int(np.clip(31 * (0.85 + 0.3 * spec), 0, 255))
                g_h = int(np.clip(26 * (0.85 + 0.3 * spec), 0, 255))
                b_h = int(np.clip(58 * (0.85 + 0.3 * spec), 0, 255))
                curio_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Dual Micro-Nozzle Vents with Sky Blue Glow
    cd.ellipse([57, 68, 62, 73], fill=OBS_DEEP, outline=OUTLINE)
    cd.ellipse([58, 69, 61, 72], fill=SKY_BASE)
    cd.point((59, 70), fill=WHITE_SHINE)

    cd.ellipse([66, 68, 71, 73], fill=OBS_DEEP, outline=OUTLINE)
    cd.ellipse([67, 69, 70, 72], fill=SKY_BASE)
    cd.point((68, 70), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_bat_astral_polymer_default.png
    # Starwing Bat Astral Polymer Chassis (星翼蝙蝠極光紫黑航太聚合物素體)
    # Features:
    # - 2.2 Chibi low-gravity aerodynamic chassis
    # - Soft ground contact shadow at (64, 116)
    # - Dual inverted mag-grip paws with coral pink silicone suction pads at (46, 113) and (72, 113)
    # - Solid neck collar at (x: 52..76, y: 46..58) for seamless head seating (zero holes)
    # - Matte aurora purple-black hull (#1F1A3A) with obsidian ball-and-socket limb joints
    # - Ivory enamel cheek/torso mount base with glowing sky blue / mint battery indicator
    # - Left hand poised in balanced radar frequency tuning stance at (38, 76)
    # - Right arm tucked at ribs with weapon grip joint at (80, 72)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 32, 116 - 5, 64 + 32, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Inverted Mag-Grip Mechanical Paws with Coral Pink Silicone Pads
    paw_pos = [(46.0, 113.0), (72.0, 113.0)]
    for bx, by in paw_pos:
        # Magnetic claw base (aerospace titanium POM)
        ch_d.ellipse([int(bx - 8), int(by - 3), int(bx + 8), int(by + 3)], fill=OBS_BASE, outline=OUTLINE)
        # Coral Pink Magnetic Silicone Suction Cushion
        ch_d.ellipse([int(bx - 6), int(by - 2), int(bx + 6), int(by + 2)], fill=CORAL_BASE)
        ch_d.ellipse([int(bx - 4), int(by - 1), int(bx + 4), int(by + 1)], fill=CORAL_LIGHT)
        # Miniature toe claw clips (4 fingers)
        for cdx in [-6, -2, 2, 6]:
            ch_d.point((int(bx + cdx), int(by + 2)), fill=AMBER_BASE)
        ch_d.point((int(bx), int(by)), fill=WHITE_SHINE)

    # 3. Slender Articulated Legs with Neon Mint Gasket Rings
    leg_paths = [
        ((46.0, 112.0), (52.0, 88.0)),
        ((72.0, 112.0), (66.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-5, 6):
                spec = max(0.0, 1.0 - abs(dx) / 5.0)
                r_l = int(np.clip(31 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                g_l = int(np.clip(26 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                b_l = int(np.clip(58 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 2, mid_x + 3, mid_y + 2], fill=MINT_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 52..76, y: 46..58)
    for ny in range(46, 59):
        for nx in range(52, 77):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 12.0)
            r_n = int(np.clip(31 * (0.85 + 0.4 * spec) + 30 * spec, 0, 255))
            g_n = int(np.clip(26 * (0.85 + 0.4 * spec) + 30 * spec, 0, 255))
            b_n = int(np.clip(58 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 5. Torso Body Shell (x: 42..86, y: 56..96)
    cx_t, cy_t = 64.0, 77.0
    for y in range(56, 97):
        for x in range(42, 87):
            dx = (x - cx_t) / 20.0
            dy = (y - cy_t) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 20.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Ivory enamel backing mount plate on chest
                is_chest_mount = ((x - 64.0)**2 / 11.0**2 + (y - 75.0)**2 / 12.0**2 <= 1.0)
                if is_chest_mount:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 35 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 35 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 35 * edge_shade + 20 * shine, 0, 255))
                else:
                    # Outer matte aurora purple-black hull with neon cyan seam trim
                    is_rim = dist_sq >= 0.75
                    if is_rim:
                        r_t = int(np.clip(56 * (0.8 + 0.3 * spec) + 30 * shine - 15 * edge_shade, 0, 255))
                        g_t = int(np.clip(160 * (0.8 + 0.3 * spec) + 30 * shine - 15 * edge_shade, 0, 255))
                        b_t = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine - 10 * edge_shade, 0, 255))
                    else:
                        r_t = int(np.clip(31 * (0.8 + 0.45 * spec) + 40 * shine - 12 * edge_shade, 0, 255))
                        g_t = int(np.clip(26 * (0.8 + 0.45 * spec) + 40 * shine - 12 * edge_shade, 0, 255))
                        b_t = int(np.clip(58 * (0.8 + 0.45 * spec) + 50 * shine - 12 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Glowing Pulsar Energy Core on chest (x: 64, y: 75)
    ch_d.ellipse([64 - 5, 75 - 5, 64 + 5, 75 + 5], fill=POLY_DEEP, outline=OUTLINE)
    ch_d.ellipse([64 - 4, 75 - 4, 64 + 4, 75 + 4], fill=SKY_BASE)
    ch_d.ellipse([64 - 2, 75 - 2, 64 + 2, 75 + 2], fill=MINT_LIGHT)
    ch_d.point((63, 74), fill=WHITE_SHINE)

    # 6. Left Arm: Poised at waist, radar frequency tuning gesture at (38, 76)
    left_arm_pts = [
        ((46.0, 66.0), (38.0, 76.0))
    ]
    for (ax0, ay0), (ax1, ay1) in left_arm_pts:
        for t in np.linspace(0.0, 1.0, 20):
            ax = ax0 + t * (ax1 - ax0)
            ay = ay0 + t * (ay1 - ay0)
            for dx in range(-4, 5):
                for dy in range(-4, 5):
                    if dx**2 + dy**2 <= 16:
                        spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 4.0)
                        r_a = int(np.clip(31 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        g_a = int(np.clip(26 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        b_a = int(np.clip(58 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                        chassis_img.putpixel((int(ax + dx), int(ay + dy)), (r_a, g_a, b_a, 255))
    ch_d.ellipse([34, 72, 42, 80], fill=OBS_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 74, 40, 78], fill=MINT_BASE)
    ch_d.point((38, 76), fill=WHITE_SHINE)

    # 7. Right Arm: Tucked at ribs, ending at (80, 72)
    # STRICT 0-ART9/11: Right arm must not exceed x=93!
    for t in np.linspace(0.0, 1.0, 20):
        rax = 76.0 + t * 4.0
        ray = 66.0 + t * 6.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    px = int(rax + dx)
                    py = int(ray + dy)
                    if px < 94:
                        spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 4.0)
                        r_a = int(np.clip(31 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        g_a = int(np.clip(26 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        b_a = int(np.clip(58 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                        chassis_img.putpixel((px, py), (r_a, g_a, b_a, 255))

    # Right wrist ball joint at (80, 72)
    ch_d.ellipse([77, 69, 83, 75], fill=SKY_BASE, outline=OUTLINE)
    ch_d.point((80, 72), fill=WHITE_SHINE)

    # Strict clamp to x < 94 to ensure 0-ART9/11 compliance
    for cy in range(H):
        for cx in range(94, W):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)

    # Ensure zero pixels at x >= 94 again after outline
    for cy in range(H):
        for cx in range(94, W):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_bat_sonar_parabolic_crest.png
    # Features:
    # - Sonar Parabolic Crest / Dual Radar Ears (雙聯拋物面聲納雷達集音耳)
    # - Aurora purple-black aerodynamic helmet (40..88, 18..54)
    # - Ivory enamel cheek armor panels (44..52, 44..54) and (76..84, 44..54)
    # - Huge parabolic sonar radar ears:
    #   - Left Ear: base at (46, 24), expands to (28..56, 4..24)
    #   - Right Ear: base at (82, 24), expands to (72..100, 4..24)
    #   - Neon Mint (#4ED86A) frequency printed circuit strips along rim
    #   - Brass acoustic micromesh grid inside ear dish
    # - STRICT 0-ART27:
    #   Left eye socket at (52, 40) MUST BE HOLLOW (alpha=0 at x in [51, 53], y in [39, 41])
    #   Right eye socket at (76, 40) MUST BE HOLLOW (alpha=0 at x in [75, 77], y in [39, 41])
    #   Enclosing bronze bezel ring!
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. DUAL PARABOLIC SONAR RADAR EARS (Drawn on upper head sides)
    # Left Parabolic Radar Ear (center around 42, 14)
    for y in range(4, 26):
        for x in range(28, 56):
            # Parabolic dish equation
            dx = (x - 42.0) / 12.0
            dy = (y - 14.0) / 10.0
            if dx**2 + dy**2 <= 1.0:
                dist = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - dist)
                # Outer rim is neon mint printed circuit
                is_circuit_rim = (0.75 <= dist <= 1.0)
                if is_circuit_rim:
                    r_e = int(np.clip(78 * (0.85 + 0.25 * spec), 0, 255))
                    g_e = int(np.clip(216 * (0.85 + 0.25 * spec), 0, 255))
                    b_e = int(np.clip(106 * (0.85 + 0.25 * spec), 0, 255))
                else:
                    # Inner dish: semi-translucent purple polycarbonate with brass microring
                    is_brass_mesh = ((x + y) % 3 == 0 and dist <= 0.6)
                    if is_brass_mesh:
                        r_e = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))
                        g_e = int(np.clip(208 * (0.8 + 0.2 * spec), 0, 255))
                        b_e = int(np.clip(40 * (0.8 + 0.2 * spec), 0, 255))
                    else:
                        r_e = int(np.clip(31 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        g_e = int(np.clip(26 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        b_e = int(np.clip(58 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    # Left ear acoustic probe tip at (38, 5)
    hd.ellipse([37, 4, 39, 6], fill=AMBER_LIGHT, outline=OUTLINE)
    hd.point((38, 5), fill=WHITE_SHINE)

    # Right Parabolic Radar Ear (center around 86, 14)
    for y in range(4, 26):
        for x in range(72, 100):
            dx = (x - 86.0) / 12.0
            dy = (y - 14.0) / 10.0
            if dx**2 + dy**2 <= 1.0:
                dist = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - dist)
                is_circuit_rim = (0.75 <= dist <= 1.0)
                if is_circuit_rim:
                    r_e = int(np.clip(78 * (0.85 + 0.25 * spec), 0, 255))
                    g_e = int(np.clip(216 * (0.85 + 0.25 * spec), 0, 255))
                    b_e = int(np.clip(106 * (0.85 + 0.25 * spec), 0, 255))
                else:
                    is_brass_mesh = ((x - y) % 3 == 0 and dist <= 0.6)
                    if is_brass_mesh:
                        r_e = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))
                        g_e = int(np.clip(208 * (0.8 + 0.2 * spec), 0, 255))
                        b_e = int(np.clip(40 * (0.8 + 0.2 * spec), 0, 255))
                    else:
                        r_e = int(np.clip(31 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        g_e = int(np.clip(26 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        b_e = int(np.clip(58 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    # Right ear acoustic probe tip at (90, 5)
    hd.ellipse([89, 4, 91, 6], fill=AMBER_LIGHT, outline=OUTLINE)
    hd.point((90, 5), fill=WHITE_SHINE)

    # 2. Main Helmet Dome (x: 40..88, y: 18..54)
    cx_h, cy_h = 64.0, 36.0
    for y in range(18, 52):
        for x in range(40, 89):
            dx = (x - cx_h) / 22.0
            dy = (y - cy_h) / 16.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 20.0)
                shine = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_h = int(np.clip(31 * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                g_h = int(np.clip(26 * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                b_h = int(np.clip(58 * (0.8 + 0.45 * spec) + 45 * shine - 15 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 3. Cheek Armor Plates (Enamel Ivory Ceramic, y: 44..54)
    for y in range(44, 55):
        for x in list(range(44, 52)) + list(range(76, 85)):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 20.0)
            head_img.putpixel((x, y), IVORY_BASE)

    # 4. Brow Sensor Band & Neon Mint Frequency Guide (y: 28..31)
    for bx in range(46, 83):
        head_img.putpixel((bx, 29), MINT_BASE)
        head_img.putpixel((bx, 30), SKY_BASE)

    # 5. Golden Brass Bezel Rings surrounding Eye Sockets
    for ecx in [52.0, 76.0]:
        for y in range(35, 46):
            for x in range(int(ecx - 5), int(ecx + 6)):
                dist = ((x - ecx)**2 + (y - 40.0)**2)**0.5
                if 2.5 <= dist <= 5.5:
                    head_img.putpixel((x, y), AMBER_BASE)

    # 6. Snout / Nose Acoustic Sensor Bridge at (58..70, 46..54)
    for y in range(46, 54):
        for x in range(58, 71):
            dx = (x - 64.0) / 6.0
            dy = (y - 50.0) / 4.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 6.0)
                r_sn = int(np.clip(43 * (0.85 + 0.3 * spec), 0, 255))
                g_sn = int(np.clip(40 * (0.85 + 0.3 * spec), 0, 255))
                b_sn = int(np.clip(54 * (0.85 + 0.3 * spec), 0, 255))
                head_img.putpixel((x, y), (r_sn, g_sn, b_sn, 255))

    # Ultrasonic Emitter Vent Slots at nose bridge
    hd.line([(62, 51), (66, 51)], fill=MINT_BASE, width=1)
    hd.point((64, 49), fill=WHITE_SHINE)

    # 7. STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye socket centers MUST be completely transparent (alpha = 0)
    for y in range(38, 43):
        for x in range(50, 55):
            if ((x - 52.0)**2 + (y - 40.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(74, 79):
            if ((x - 76.0)**2 + (y - 40.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(head_img, ignore_regions=[(48, 36, 56, 44), (72, 36, 80, 44)])

    # Re-enforce 0-ART27 hollow eye socket centers
    for y in range(39, 42):
        for x in range(51, 54):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(75, 78):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_bat_orbital_stealth_harness.png
    # Features:
    # - Orbital Stealth Harness & Flight Suit (星穹失重匿蹤飛行胸甲與抗真空防護服)
    # - Sleek aerodynamic breastplate covering (46..82, 56..92)
    # - Central Enamel Ivory (#FFFDF8) ceramic chest plate with electric sky status LED
    # - Dual aerodynamic shoulder pauldrons at left (38..46, 56..66) and right (82..90, 56..66)
    # - Coral Pink (#FF5E8A) energy coupling latch & micro-pressure relief seals
    # - STRICT 0-ART26b: Lower leg zone y >= 96 strictly ZERO pixels!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # 1. Breastplate Curved Hull (x: 46..82, y: 56..92)
    for y in range(56, 93):
        for x in range(46, 83):
            dx = (x - 64.0) / 18.0
            dy = (y - 74.0) / 17.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_c = int(np.clip(31 * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                g_c = int(np.clip(26 * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                b_c = int(np.clip(58 * (0.75 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))

                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 2. Central Enamel Ivory Shield Plate on Breast (54..74, 64..82)
    for y in range(64, 83):
        for x in range(54, 75):
            dx = (x - 64.0) / 10.0
            dy = (y - 73.0) / 9.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 61.0)**2 + (y - 70.0)**2)**0.5 / 10.0)
                shine = max(0.0, 1.0 - ((x - 61.0)**2 + (y - 70.0)**2)**0.5 / 3.0)**2
                r_iv = int(np.clip(255 * (0.88 + 0.15 * spec) + 20 * shine, 0, 255))
                g_iv = int(np.clip(253 * (0.88 + 0.15 * spec) + 20 * shine, 0, 255))
                b_iv = int(np.clip(248 * (0.88 + 0.15 * spec) + 20 * shine, 0, 255))
                costume_img.putpixel((x, y), (r_iv, g_iv, b_iv, 255))

    # Central Electric Sky Coolant Status Indicator
    cd.rectangle([62, 70, 66, 76], fill=SKY_BASE, outline=OUTLINE)
    cd.point((64, 73), fill=WHITE_SHINE)

    # 3. Waist Harness Belt with Coral Pink Power Latch (y: 84..90)
    for x in range(48, 81):
        costume_img.putpixel((x, 85), OBS_BASE)
        costume_img.putpixel((x, 86), OBS_LIGHT)
        costume_img.putpixel((x, 87), OBS_BASE)

    # Coral Pink Power Latch in center
    cd.ellipse([61, 84, 67, 88], fill=CORAL_BASE, outline=OUTLINE)
    cd.point((64, 86), fill=CORAL_LIGHT)

    # 4. Shoulder Pauldrons (Left: 38..46, 56..66; Right: 82..90, 56..66)
    pauldrons = [(42.0, 61.0), (86.0, 61.0)]
    for px, py in pauldrons:
        cd.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=POLY_LIGHT, outline=OUTLINE)
        cd.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=IVORY_BASE)
        cd.ellipse([int(px - 2), int(py - 2), int(px + 2), int(py + 2)], fill=MINT_BASE)
        cd.point((int(px), int(py)), fill=WHITE_SHINE)

    # Collar Neck Guard Flange at (56..72, 54..58)
    cd.rounded_rectangle([56, 54, 72, 58], radius=2, fill=OBS_LIGHT, outline=OUTLINE)
    cd.line([(58, 56), (70, 56)], fill=MINT_BASE, width=1)

    # STRICT 0-ART26b: Lower leg zone y >= 96 strictly ZERO pixels!
    for cy in range(96, H):
        for cx in range(W):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    apply_clean_outline(costume_img)

    # Re-enforce y >= 96 zero pixels after outline
    for cy in range(96, H):
        for cx in range(W):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_bat_dual_amber_optic_lens.png
    # Features:
    # - Dual Amber Quartz Night Optics (雙聯琥珀夜視石英目鏡)
    # - Left lens centered at (52, 40)
    # - Right lens centered at (76, 40)
    # - Precision convex lens shading in solar amber quartz (#FFD028 / #FFA010)
    # - Reticle crosshair dots & LED targeting matrix
    # - Coral pink blush sensor dots at (44, 46) and (84, 46)
    # - Digital acoustic sensor vent at (62..66, 49)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(core_img)

    for ecx in [52.0, 76.0]:
        ecy = 40.0
        r_lens = 3.8
        for y in range(int(ecy - r_lens - 1), int(ecy + r_lens + 2)):
            for x in range(int(ecx - r_lens - 1), int(ecx + r_lens + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    norm_d = dist / r_lens
                    spec = max(0.0, 1.0 - norm_d)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.0))**2 + (y - (ecy - 1.0))**2)**0.5 / 2.0)**2

                    r_e = int(np.clip(255 * (0.85 + 0.15 * spec) + 50 * shine, 0, 255))
                    g_e = int(np.clip(208 * (0.85 + 0.15 * spec) + 50 * shine, 0, 255))
                    b_e = int(np.clip(40 * (0.85 + 0.5 * spec) + 60 * shine, 0, 255))

                    core_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        # Precision Specular White Glint
        core_img.putpixel((int(ecx - 1), int(ecy - 1)), WHITE_SHINE)
        core_img.putpixel((int(ecx), int(ecy - 1)), WHITE_SHINE)

        # Concentric reticle crosshair indicator
        core_img.putpixel((int(ecx), int(ecy)), AMBER_DEEP)

        # Neon Mint Status LED at upper-outer corner
        led_x = int(ecx - 2 if ecx < 64 else ecx + 2)
        core_img.putpixel((led_x, int(ecy - 2)), MINT_LIGHT)

    # Coral Pink Blush Sensor Dots
    for bx in [44, 84]:
        cod.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=CORAL_BASE)
        cod.point((bx, 46), fill=CORAL_LIGHT)

    # Digital Mouth / Sensor Indicator
    cod.line([(62, 49), (64, 50), (66, 49)], fill=OUTLINE, width=1)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_bat_superconducting_pulse_dart.png
    # Features:
    # - Superconducting Pulse Astral Shuriken (超導脈衝星紋鏢)
    # - Single-wield compliant (0-MKT7): held in right armored gauntlet at (86..92, 68..74)
    # - 32px diameter circular 6-bladed shuriken centered at (96, 68)
    # - Six high-precision curved superconducting electromagnetic blades
    #   sweeping from hub out to cutting edge arc (#FFD028 tips & #38A0FF edges)
    # - Central pulsing gyroscopic core with neon mint and solar gold reticle
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wcx, wcy = 96.0, 68.0

    # 1. Six-Bladed Superconducting Electromagnetic Shuriken
    # Radius of shuriken outer tips: 15.0 px
    r_shuriken = 15.0
    r_core = 5.0

    for angle_deg in np.linspace(0.0, 360.0, 360, endpoint=False):
        rad = np.radians(angle_deg)
        # 6-fold symmetry
        blade_mod = (angle_deg % 60.0) / 60.0
        # Blade profile: curved forward tooth
        blade_reach = r_core + (r_shuriken - r_core) * (blade_mod**0.7)
        for r in np.linspace(r_core, blade_reach, 40):
            bx = int(round(wcx + r * np.cos(rad)))
            by = int(round(wcy + r * np.sin(rad)))
            if 0 <= bx < W and 0 <= by < H:
                norm_r = (r - r_core) / (r_shuriken - r_core)
                spec = max(0.0, blade_mod)

                # Outer blade edge is annealed gold with electric sky superconductor plasma
                if norm_r >= 0.75:
                    r_w = int(np.clip(255 * (0.85 + 0.15 * spec), 0, 255))
                    g_w = int(np.clip(208 * (0.85 + 0.15 * spec), 0, 255))
                    b_w = int(np.clip(40 * (0.85 + 0.5 * spec) + 50 * spec, 0, 255))
                elif norm_r >= 0.5:
                    r_w = int(np.clip(56 * (0.85 + 0.25 * spec), 0, 255))
                    g_w = int(np.clip(160 * (0.85 + 0.25 * spec), 0, 255))
                    b_w = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                else:
                    # Titanium obsidian dark blade body
                    r_w = int(np.clip(43 * (0.8 + 0.4 * norm_r), 0, 255))
                    g_w = int(np.clip(40 * (0.8 + 0.4 * norm_r), 0, 255))
                    b_w = int(np.clip(54 * (0.8 + 0.4 * norm_r), 0, 255))

                weapon_img.putpixel((bx, by), (r_w, g_w, b_w, 255))

    # 2. Central Pulsing Gyroscopic Core (r=5.0)
    for y in range(int(wcy - r_core - 1), int(wcy + r_core + 2)):
        for x in range(int(wcx - r_core - 1), int(wcx + r_core + 2)):
            dist = ((x - wcx)**2 + (y - wcy)**2)**0.5
            if dist <= r_core:
                spec = max(0.0, 1.0 - dist / r_core)
                r_c = int(np.clip(255 * (0.85 + 0.15 * spec), 0, 255))
                g_c = int(np.clip(208 * (0.85 + 0.15 * spec), 0, 255))
                b_c = int(np.clip(40 * (0.85 + 0.5 * spec) + 40 * spec, 0, 255))
                weapon_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    wd.ellipse([wcx - 3, wcy - 3, wcx + 3, wcy + 3], fill=MINT_BASE, outline=OUTLINE)
    wd.ellipse([wcx - 1, wcy - 1, wcx + 1, wcy + 1], fill=WHITE_SHINE)

    # 3. Right Armored Gauntlet Gripping Dart at (86..92, 68..74)
    wd.ellipse([84, 66, 92, 74], fill=POLY_LIGHT, outline=OUTLINE)
    wd.ellipse([85, 67, 91, 73], fill=AMBER_BASE)
    wd.point((88, 70), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_bat_orbital_pulsar_key", key_img),
        ("back_curio", "curio_bat_articulated_starwing_mantle", curio_img),
        ("chassis", "chassis_bat_astral_polymer_default", chassis_img),
        ("head_unit", "head_bat_sonar_parabolic_crest", head_img),
        ("costume", "costume_bat_orbital_stealth_harness", costume_img),
        ("optic_core", "face_bat_dual_amber_optic_lens", core_img),
        ("weapon", "weapon_bat_superconducting_pulse_dart", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{BAT_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)

        # 128x128 Save
        p_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(p_128)

        # 512x512 Genuine LANCZOS Resampling Save
        p_512 = f"{slot_dir}/{item_id}_512.png"
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(p_512)
        print(f"  ✓ Saved [{slot:<12}] 128 & 512 LANCZOS: {item_id}")

    # Copy universal key and weapon to universal paperdoll directory
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copyfile(f"{BAT_PD_DIR}/winding_key/key_bat_orbital_pulsar_key.png", f"{KEY_DIR}/key_bat_orbital_pulsar_key.png")
    shutil.copyfile(f"{BAT_PD_DIR}/weapon/weapon_bat_superconducting_pulse_dart.png", f"{WEAPON_DIR}/weapon_bat_superconducting_pulse_dart.png")
    print("  ✓ Synced key & weapon to universal folders")

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

    proof_comp = f"{BAT_PD_DIR}/proof_paperdoll_bat_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{BAT_PD_DIR}/proof_paperdoll_bat_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Optic", "Costume", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, core_img, costume_img, weapon_img]

    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 14)
    except Exception:
        font = ImageFont.load_default()

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{BAT_PD_DIR}/proof_bat_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/bat_idle_hd.png)
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
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{showcase_dir}/bat_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL STARWING BAT CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
