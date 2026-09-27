#!/usr/bin/env python3
"""
build_chameleon_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十族 幻彩變色龍 (The Mirage Chameleon, chameleon) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/MIRAGE_CHAMELEON_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, ivory titanium armor plates,
  dopamine optical interference lamellae, independent 360° turret rangefinder lenses,
  coaxial torsion spiral tail, prismatic tri-vane winding key clearly protruding from silhouette,
  mirage compound bow)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Ivory Titanium White (#FFFDF8)
    2. Secondary Trim: Wasteland Dopamine Bright Orange (#FFA010)
    3. Optic Core & LEDs: Amber Starlight (#FFD028)
    4. Optical Interference: Mint Nebula Glow (#4ED86A)
    5. Sky Cyan: Astral Orbit Blue (#38A0FF)
    6. Accent & Seals: Coral Pink (#FF5E8A)
    7. Frame & Struts: Mottled Brass Ochre (#D49B4B)
    8. Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
CHAMELEON_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/chameleon"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Mirage Chameleon Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Ivory Titanium White (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (228, 222, 212, 255)
IVORY_DARK  = (195, 188, 175, 255)
IVORY_DEEP  = (160, 152, 140, 255)

# 2. Secondary Trim: Wasteland Dopamine Bright Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 192, 64, 255)
ORANGE_SHINE = (255, 224, 128, 255)
ORANGE_DARK  = (210, 115, 8, 255)
ORANGE_DEEP  = (150, 75, 4, 255)

# 3. Optic Core & LEDs: Amber Starlight (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (205, 148, 18, 255)
GOLD_DEEP  = (145, 95, 10, 255)

# 4. Optical Interference: Mint Nebula Glow (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 5. Sky Cyan: Astral Orbit Blue (#38A0FF)
BLUE_BASE  = (56, 160, 255, 255)
BLUE_LIGHT = (112, 192, 255, 255)
BLUE_SHINE = (175, 225, 255, 255)
BLUE_DARK  = (28, 112, 204, 255)
BLUE_DEEP  = (16, 68, 140, 255)

# 6. Accent & Seals: Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 200, 220, 255)
CORAL_DARK  = (200, 50, 95, 255)
CORAL_DEEP  = (140, 25, 60, 255)

# 7. Frame & Struts: Mottled Brass Ochre (#D49B4B)
BRASS_BASE  = (212, 155, 75, 255)
BRASS_LIGHT = (235, 185, 115, 255)
BRASS_SHINE = (255, 215, 155, 255)
BRASS_DARK  = (165, 110, 42, 255)
BRASS_DEEP  = (115, 72, 24, 255)

# Structural Steels & Slate
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (108, 122, 145, 255)
STEEL_SHINE = (155, 170, 195, 255)
STEEL_DARK  = (48, 56, 70, 255)
STEEL_DEEP  = (30, 36, 46, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL MIRAGE CHAMELEON SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_chameleon_prismatic_trivane.png
    # Prismatic Tri-Vane Winding Key (三稜透鏡發條鑰匙)
    # Socket boss at spine (64, 58), shaft extends diagonally up-right to (96, 22)
    # Protrudes clearly beyond head silhouette (x: 90..116)
    # Features:
    # - Polished golden brass shaft with radial bevel shading
    # - Three triangular prismatic vane wings radiating from hub (96, 22)
    # - Prismatic interference facets (Cyan, Mint, Amber, Coral highlights)
    # - Central faceted quartz crystal hub at (96, 22)
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

    # Base socket collar at (64, 58)
    kd.ellipse([64 - 5, 58 - 5, 64 + 5, 58 + 5], fill=BRASS_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 58 - 3, 64 + 3, 58 + 3], fill=GOLD_BASE)

    # 2. Three Triangular Prismatic Wings radiating from (96, 22)
    # Vane angles: -2.3 rad (up-left), -0.7 rad (up-right), 1.8 rad (down-right)
    kcx, kcy = 96.0, 22.0
    vane_angles = [-2.35, -0.75, 1.65]
    vane_colors = [
        (BLUE_BASE, BLUE_LIGHT, BLUE_SHINE),    # Cyan wing
        (MINT_BASE, MINT_LIGHT, MINT_SHINE),    # Mint wing
        (ORANGE_BASE, ORANGE_LIGHT, ORANGE_SHINE) # Orange wing
    ]

    for angle, (c_base, c_light, c_shine) in zip(vane_angles, vane_colors):
        # Build triangular vane: root at kcx, kcy; two outer tip vertices
        tip_dist = 18.0
        tip_cx = kcx + tip_dist * np.cos(angle)
        tip_cy = kcy + tip_dist * np.sin(angle)
        perp_angle = angle + np.pi / 2.0
        w_spread = 8.5
        v1 = (tip_cx + w_spread * np.cos(perp_angle), tip_cy + w_spread * np.sin(perp_angle))
        v2 = (tip_cx - w_spread * np.cos(perp_angle), tip_cy - w_spread * np.sin(perp_angle))

        # Fill triangle with bevel & prismatic interference gradient
        poly = [(kcx, kcy), v1, v2]
        kd.polygon(poly, fill=c_base, outline=OUTLINE_KEY)

        # Inner facet 1 (shine)
        kd.polygon([(kcx, kcy), v1, ((kcx + tip_cx)/2.0, (kcy + tip_cy)/2.0)], fill=c_light)
        # Inner facet 2 (core highlight)
        kd.polygon([((kcx + tip_cx)/2.0, (kcy + tip_cy)/2.0), v1, (tip_cx, tip_cy)], fill=c_shine)

        # Tip jewel dot
        kd.ellipse([int(tip_cx - 2), int(tip_cy - 2), int(tip_cx + 2), int(tip_cy + 2)], fill=GOLD_LIGHT, outline=OUTLINE_KEY)

    # 3. Central Faceted Quartz Crystal Hub at (96, 22)
    kd.ellipse([int(kcx - 7), int(kcy - 7), int(kcx + 7), int(kcy + 7)], fill=BRASS_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=MINT_BASE)
    kd.ellipse([int(kcx - 1), int(kcy - 1), int(kcx + 1), int(kcy + 1)], fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline to guarantee 0-ART29 compliance
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_chameleon_spiral_torsion_tail.png
    # Coaxial Torsion Spiral Tail (多節同軸發條扭簧平衡卷尾)
    # Originates at rump (46, 88).
    # Curves down and coils into a classic mechanical chameleon curled tail.
    # Features:
    # - 5 segmented articulated titanium/brass rings
    # - Inner coaxial coiled torsion spring spiral with steel ribbon
    # - Optical interference mint (#4ED86A) and cyan (#38A0FF) plate highlights
    # - Golden brass rivet hinges along segment joints
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Path of coiled tail:
    # 1. Rump exit: (46, 86) -> (36, 92) -> (28, 100) -> (24, 110)
    # 2. Curl base: (24, 110) -> (28, 116) -> (36, 117) -> (42, 112)
    # 3. Inner coil: (42, 112) -> (44, 104) -> (38, 99) -> (32, 102) -> (32, 107) -> (36, 107)
    tail_ctrl_pts = [
        np.array([46.0, 86.0]),
        np.array([40.0, 90.0]),
        np.array([32.0, 96.0]),
        np.array([26.0, 104.0]),
        np.array([24.0, 112.0]),
        np.array([28.0, 118.0]),
        np.array([36.0, 118.0]),
        np.array([42.0, 114.0]),
        np.array([45.0, 106.0]),
        np.array([41.0, 99.0]),
        np.array([34.0, 100.0]),
        np.array([31.0, 105.0]),
        np.array([35.0, 109.0]),
        np.array([38.0, 106.0])
    ]

    # Generate dense centerline
    dense_pts = []
    for i in range(len(tail_ctrl_pts) - 1):
        p0, p1 = tail_ctrl_pts[i], tail_ctrl_pts[i+1]
        for t in np.linspace(0.0, 1.0, 20):
            dense_pts.append(p0 + t * (p1 - p0))

    total_dense = len(dense_pts)

    # Draw tail segments along centerline with tapering radius
    for idx, pt in enumerate(dense_pts):
        t_ratio = idx / float(total_dense)
        # Radius tapers from 5.5px at rump to 1.8px at tip
        r = 5.5 * (1.0 - 0.65 * t_ratio)

        # Tangent & normal
        if idx < total_dense - 1:
            tangent = dense_pts[idx+1] - pt
        else:
            tangent = pt - dense_pts[idx-1]
        t_norm = np.linalg.norm(tangent)
        if t_norm > 1e-4:
            normal = np.array([-tangent[1], tangent[0]]) / t_norm
        else:
            normal = np.array([0.0, 1.0])

        # Cross section
        for s in np.linspace(-1.0, 1.0, int(r * 4 + 1)):
            pos = pt + s * normal * r
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            if 0 <= ix < W and 0 <= iy < H:
                spec = max(0.0, 1.0 - abs(s))
                shine = max(0.0, 1.0 - abs(s + 0.25))**2

                # Segment alternating patterns
                seg_id = int(t_ratio * 7)
                is_gap = (int(idx) % 18) in (0, 1)

                if is_gap:
                    # Brass hinge spacer
                    r_c = int(np.clip(212 * (0.8 + 0.3 * spec), 0, 255))
                    g_c = int(np.clip(155 * (0.8 + 0.3 * spec), 0, 255))
                    b_c = int(np.clip(75 * (0.8 + 0.4 * spec), 0, 255))
                else:
                    # Titanium outer hull with optical interference gradient
                    if seg_id % 2 == 0:
                        # Mint glow interference
                        r_c = int(np.clip(78 * (0.8 + 0.2 * spec) + 80 * shine, 0, 255))
                        g_c = int(np.clip(216 * (0.85 + 0.15 * spec) + 30 * shine, 0, 255))
                        b_c = int(np.clip(106 * (0.8 + 0.2 * spec) + 50 * shine, 0, 255))
                    else:
                        # Ivory titanium with cyan highlight
                        r_c = int(np.clip(255 * (0.82 + 0.18 * spec) - 20 * abs(s), 0, 255))
                        g_c = int(np.clip(253 * (0.82 + 0.18 * spec) - 20 * abs(s), 0, 255))
                        b_c = int(np.clip(248 * (0.80 + 0.20 * spec) + 20 * shine, 0, 255))

                curio_img.putpixel((ix, iy), (r_c, g_c, b_c, 255))

    # Center Spiral Hub Jewel at (36, 106)
    cd.ellipse([34, 104, 38, 108], fill=GOLD_BASE, outline=OUTLINE)
    cd.point((36, 106), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_chameleon_mirage_titanium_default.png
    # Features:
    # - 2.2 Chibi high-gloss ivory titanium chameleon chassis (#FFFDF8)
    # - Soft ground contact shadow at (64, 116)
    # - Chameleon zygodactylous clamp feet at (48, 112) and (70, 112)
    # - Opposing two-finger / three-finger clamp digits with coral pink pads
    # - Bare chassis torso crop (60:84, 48:72) has >= 20 unique colors (0-ART18 compliant)
    # - Right arm tucked at ribs with weapon grip socket at (82, 74)
    # - Left arm raised forward to hold bow grip at (38, 76)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    ch_d.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 160))

    # 2. Zygodactylous Clamp Feet & Leg Struts
    # Left foot: (48, 112), Right foot: (70, 112)
    for fx, fy in [(48, 112), (70, 112)]:
        # Brass ankle ball joint
        ch_d.ellipse([fx - 3, fy - 6, fx + 3, fy - 2], fill=BRASS_BASE, outline=OUTLINE)
        # Zygodactylous clamp claws (front two digits, rear two digits)
        # Outer clamp
        ch_d.ellipse([fx - 6, fy - 2, fx - 1, fy + 4], fill=IVORY_BASE, outline=OUTLINE)
        # Inner clamp
        ch_d.ellipse([fx + 1, fy - 2, fx + 6, fy + 4], fill=IVORY_BASE, outline=OUTLINE)
        # Coral pink silicone grip pad
        ch_d.point((fx - 3, fy + 2), fill=CORAL_BASE)
        ch_d.point((fx + 3, fy + 2), fill=CORAL_BASE)

    # Leg pillars connecting pelvis to ankles
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

    # 3. Main Torso Hull (Ivory Titanium White + Prismatic Interference Lamellae)
    tcx, tcy = 62.0, 74.0
    trx, try_ = 18.0, 20.0

    # Solid Pelvis & Hip Plate (48..76, 88..96) connecting torso to legs
    for y in range(88, 96):
        for x in range(48, 76):
            if ((x - 62.0)/14.0)**2 + ((y - 92.0)/4.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), STEEL_BASE)

    for y in range(54, 96):
        for x in range(44, 82):
            dx = (x - tcx) / trx
            dy = (y - tcy) / try_
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 1.1))
                shine = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 0.4))**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                # Prismatic interference belly plate (x: 52..72, y: 64..88)
                is_belly = (52 <= x <= 72) and (64 <= y <= 88) and (((x - 62)/10.0)**2 + ((y - 76)/12.0)**2 <= 1.0)
                if is_belly:
                    # Multi-tone ivory & subtle interference shading to satisfy 0-ART18 (>= 20 unique colors in 60:84, 48:72)
                    b_spec = max(0.0, 1.0 - ((x - 60)**2 + (y - 72)**2)**0.5 / 10.0)
                    r_b = int(np.clip(255 * (0.88 + 0.12 * b_spec) - 20 * edge_shade, 0, 255))
                    g_b = int(np.clip(253 * (0.88 + 0.12 * b_spec) - 18 * edge_shade, 0, 255))
                    b_b = int(np.clip(248 * (0.85 + 0.15 * b_spec) - 22 * edge_shade + 12 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))
                else:
                    # Primary Ivory Titanium Plate
                    r_m = int(np.clip(255 * (0.82 + 0.18 * spec) + 20 * shine - 30 * edge_shade, 0, 255))
                    g_m = int(np.clip(253 * (0.82 + 0.18 * spec) + 20 * shine - 30 * edge_shade, 0, 255))
                    b_m = int(np.clip(248 * (0.80 + 0.20 * spec) + 15 * shine - 35 * edge_shade, 0, 255))
                    chassis_img.putpixel((x, y), (r_m, g_m, b_m, 255))

    # Optical Interference Flank Lamellae Lines (thin mint/cyan grooves)
    for gy in [66, 72, 78, 84]:
        for gx in range(50, 74):
            if ((gx - tcx)/trx)**2 + ((gy - tcy)/try_)**2 <= 0.8:
                if (gx + gy) % 4 == 0:
                    chassis_img.putpixel((gx, gy), MINT_LIGHT)
                elif (gx + gy) % 4 == 2:
                    chassis_img.putpixel((gx, gy), BLUE_LIGHT)

    # 4. Arms & Hands
    # Left Arm: extended forward to bow grip at (38, 76) with solid shoulder & arm filling
    for y in range(52, 68):
        for x in range(38, 52):
            if ((x - 45.0)/7.0)**2 + ((y - 60.0)/8.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), IVORY_SHADE)
    for t in np.linspace(0.0, 1.0, 30):
        ax = int(48 * (1 - t) + 38 * t)
        ay = int(62 * (1 - t) + 76 * t)
        for d in range(-3, 4):
            for dy in range(-2, 3):
                if d**2 + dy**2 <= 9:
                    chassis_img.putpixel((ax + d, ay + dy), STEEL_LIGHT)
    ch_d.ellipse([34, 72, 44, 80], fill=IVORY_BASE, outline=OUTLINE)
    ch_d.point((38, 76), fill=CORAL_BASE)

    # Right Arm: tucked at ribs with weapon grip at (82, 74)
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
    ch_d.ellipse([80, 72, 84, 76], fill=BRASS_BASE)

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
    # File: head_unit/head_chameleon_crested_visor_cowl.png
    # Features:
    # - Sculpted ivory titanium chameleon faceplate (x: 42..86, y: 22..54)
    # - Crested Visor Cowl: high-rising triangular titanium aerodynamic crest
    #   rising up from (64, 22) to (64, 12) with orange (#FFA010) & gold (#FFD028) chevrons
    # - Turret eye housings encircling the eye sockets:
    #   Left turret socket at (52, 40), Right turret socket at (76, 40)
    # - STRICT HOLLOW EYE SOCKETS AT (52, 40) AND (76, 40) (0-ART27 compliant)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Main Sculpted Faceplate & Cranium
    hcx, hcy = 64.0, 40.0
    hrx, hry = 22.0, 18.0

    for y in range(22, 58):
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

    # 2. Crested Visor Cowl (Aerodynamic Triangular Crest)
    # Tip at (64, 12), base flaring down to (52, 26) and (76, 26)
    crest_poly = [(64, 12), (76, 26), (52, 26)]
    hd.polygon(crest_poly, fill=ORANGE_BASE, outline=OUTLINE)
    # Inner gold chevron accent
    hd.polygon([(64, 15), (73, 25), (55, 25)], fill=GOLD_BASE)
    hd.polygon([(64, 18), (70, 24), (58, 24)], fill=WHITE_SHINE)

    # Crest dorsal ridge rivets
    for ry in [14, 18, 22]:
        hd.ellipse([63, ry - 1, 65, ry + 1], fill=BRASS_DARK)

    # 3. Turret Collar Rings encircling eye sockets at (52, 40) and (76, 40)
    for ex, ey in [(52, 40), (76, 40)]:
        # Brass gear tooth turret base ring (radius 8..11)
        for ang in np.linspace(0, 2 * np.pi, 24):
            gx = int(ex + 8.5 * np.cos(ang))
            gy = int(ey + 8.5 * np.sin(ang))
            head_img.putpixel((gx, gy), BRASS_BASE)
        hd.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], outline=OUTLINE, width=1)

    # Forehead brow visor arch
    for bx in range(48, 81):
        by = int(32 - 3.0 * np.cos((bx - 64)/16.0 * np.pi))
        head_img.putpixel((bx, by), ORANGE_BASE)
        head_img.putpixel((bx, by + 1), ORANGE_DARK)

    # Clean outline pass BEFORE hollowing eye sockets
    apply_clean_outline(head_img, ignore_regions=[(47, 35, 57, 45), (71, 35, 81, 45)])

    # 4. Strict Hollow Eye Sockets for 0-ART27 (alpha == 0 at eye zones)
    # Left eye socket at (52, 40), Right eye socket at (76, 40)
    h_arr = np.array(head_img)
    for ey, ex in [(40, 52), (40, 76)]:
        for y in range(ey - 5, ey + 6):
            for x in range(ex - 5, ex + 6):
                if (x - ex)**2 + (y - ey)**2 <= 20:
                    h_arr[y, x, :] = 0
    head_img = Image.fromarray(h_arr, "RGBA").copy()

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_chameleon_wasteland_scout_rig.png
    # Features:
    # - Wasteland Scout Rig (荒原斥候防沙迷彩背心裝甲)
    # - Warm orange (#FFA010) rugged waterproof canvas vest with ivory & mint green trims
    # - Chest plate (x: 48..76, y: 58..86) with dopamine tactical ammo pouches
    # - Gold brass buckles and emergency lube valve at (62, 68)
    # - 0-ART26b compliant: strictly ZERO pixels at y >= 96 (no lower legs/feet baked)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # Vest Body (x: 44..80, y: 58..88)
    for y in range(58, 89):
        for x in range(44, 81):
            dx = (x - 62.0) / 18.0
            dy = (y - 72.0) / 15.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 68)**2)**0.5 / 16.0)
                edge = max(0.0, (dx**2 + dy**2 - 0.4) / 0.6)
                r_c = int(np.clip(255 * (0.8 + 0.3 * spec) - 20 * edge, 0, 255))
                g_c = int(np.clip(160 * (0.8 + 0.3 * spec) - 20 * edge, 0, 255))
                b_c = int(np.clip(16 * (0.8 + 0.5 * spec) + 20 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Mint Green (#4ED86A) and Ivory Trims
    for x in range(48, 77):
        costume_img.putpixel((x, 58), MINT_BASE)
        costume_img.putpixel((x, 59), MINT_LIGHT)
        if 46 <= x <= 78:
            costume_img.putpixel((x, 86), MINT_BASE)
            costume_img.putpixel((x, 87), MINT_DARK)

    # Scout Chest Plate & Emergency Valve at (62, 68)
    cos_d.ellipse([58, 64, 66, 72], fill=STEEL_DARK, outline=OUTLINE)
    cos_d.ellipse([59, 65, 65, 71], fill=BRASS_BASE)
    cos_d.ellipse([61, 67, 63, 69], fill=GOLD_BASE)
    cos_d.point((62, 68), fill=WHITE_SHINE)

    # 3 Ammo Pouches / Slots on lower vest (52, 78), (62, 78), (72, 78)
    for px in [52, 62, 72]:
        cos_d.rectangle([px - 3, 76, px + 3, 82], fill=IVORY_BASE, outline=OUTLINE)
        cos_d.line([(px - 3, 79), (px + 3, 79)], fill=ORANGE_DARK)

    # Shoulder Straps at (44, 60) and (80, 60)
    for sx in [44, 80]:
        cos_d.ellipse([sx - 3, 60 - 3, sx + 3, 60 + 3], fill=BRASS_BASE, outline=OUTLINE)
        cos_d.point((sx, 60), fill=WHITE_SHINE)

    # Strict check: 0-ART26b compliance (no pixels at y >= 96)
    cos_arr = np.array(costume_img)
    cos_arr[96:, :, :] = 0
    costume_img = Image.fromarray(cos_arr).copy()

    apply_clean_outline(costume_img)
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_chameleon_turret_rangefinder_lens.png
    # Features:
    # - Turret Rangefinder Lenses (雙向砲塔測距雙目光學透鏡)
    # - Centers precisely aligned with head sockets: Left (52, 40), Right (76, 40)
    # - Solid lens centers (alpha=255) with amber starlight LEDs (0-ART27 compliant)
    # - Concentric rangefinder reticles and laser crosshair highlights
    # - Cheerful coral pink blush LEDs at (44, 46) and (84, 46)
    # - Cute small digital mouth at (64, 48)
    # - Color richness >= 15 unique colors (0-QA31 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(core_img)

    for ecx, ecy in [(52.0, 40.0), (76.0, 40.0)]:
        # Solid circular convex quartz lens housing
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
                        # Amber Starlight LED Convex Quartz Lens
                        r_o = int(np.clip(255, 0, 255))
                        g_o = int(np.clip(208 * (0.75 + 0.35 * spec) + 30 * shine, 0, 255))
                        b_o = int(np.clip(40 * (0.7 + 0.6 * spec) + 80 * shine, 0, 255))

                    core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

        # Rangefinder crosshair reticle
        core_img.putpixel((int(ecx), int(ecy)), WHITE_SHINE)
        core_img.putpixel((int(ecx - 1), int(ecy)), GOLD_LIGHT)
        core_img.putpixel((int(ecx + 1), int(ecy)), GOLD_LIGHT)
        core_img.putpixel((int(ecx), int(ecy - 1)), GOLD_LIGHT)
        core_img.putpixel((int(ecx), int(ecy + 1)), GOLD_LIGHT)
        # Outer ring marks at 3px
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
            core_img.putpixel((int(ecx + dx), int(ecy + dy)), ORANGE_BASE)

    # Coral Pink LED Blush Dots
    for bx in [44, 84]:
        cod.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=CORAL_BASE)
        cod.point((bx, 46), fill=CORAL_LIGHT)

    # Digital Mouth Indicator
    cod.line([(62, 48), (64, 49), (66, 48)], fill=OUTLINE, width=1)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_chameleon_mirage_compound_bow.png
    # Features:
    # - Mirage Prismatic Compound Bow (幻彩棱鏡複合機關弓)
    # - Held in left hand at (38, 76) (0-MKT7 single-wield compliant)
    # - Titanium spring-steel riser with ivory grip at (38, 76)
    # - Upper limb arching up-forward to upper eccentric cam pulley at (32, 40)
    # - Lower limb arching down-forward to lower eccentric cam pulley at (32, 104)
    # - High-tensile bowstring running between cams
    # - Optical interference prism attached to riser at (36, 68)
    # - Nocked mint glow energy arrow resting on arrow rest
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Bow Handle / Riser at (38, 76)
    for y in range(70, 83):
        for x in range(36, 41):
            weapon_img.putpixel((x, y), IVORY_BASE)
    # Handle grip wraps
    for y in [72, 75, 78, 81]:
        wd.line([(36, y), (40, y)], fill=ORANGE_BASE)

    # 2. Upper Bow Limb: from (38, 70) curving to (32, 40)
    upper_limb_pts = [
        np.array([38.0, 70.0]),
        np.array([35.0, 60.0]),
        np.array([31.0, 50.0]),
        np.array([32.0, 40.0])
    ]
    for i in range(len(upper_limb_pts) - 1):
        p0, p1 = upper_limb_pts[i], upper_limb_pts[i+1]
        for t in np.linspace(0.0, 1.0, 30):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-1, 2):
                weapon_img.putpixel((ix + d, iy), STEEL_LIGHT)
                weapon_img.putpixel((ix, iy), MINT_LIGHT)

    # 3. Lower Bow Limb: from (38, 82) curving to (32, 104)
    lower_limb_pts = [
        np.array([38.0, 82.0]),
        np.array([35.0, 92.0]),
        np.array([31.0, 98.0]),
        np.array([32.0, 104.0])
    ]
    for i in range(len(lower_limb_pts) - 1):
        p0, p1 = lower_limb_pts[i], lower_limb_pts[i+1]
        for t in np.linspace(0.0, 1.0, 30):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-1, 2):
                weapon_img.putpixel((ix + d, iy), STEEL_LIGHT)
                weapon_img.putpixel((ix, iy), MINT_LIGHT)

    # 4. Eccentric Cam Pulleys at (32, 40) and (32, 104)
    for cy in [40, 104]:
        wd.ellipse([32 - 4, cy - 4, 32 + 4, cy + 4], fill=BRASS_BASE, outline=OUTLINE)
        wd.ellipse([32 - 2, cy - 2, 32 + 2, cy + 2], fill=GOLD_BASE)
        wd.point((32, cy), fill=WHITE_SHINE)

    # 5. Bowstring running from (34, 40) -> (42, 76) -> (34, 104)
    for t in np.linspace(0.0, 1.0, 40):
        sx1 = int(34 * (1 - t) + 42 * t)
        sy1 = int(40 * (1 - t) + 76 * t)
        weapon_img.putpixel((sx1, sy1), STEEL_SHINE)

        sx2 = int(42 * (1 - t) + 34 * t)
        sy2 = int(76 * (1 - t) + 104 * t)
        weapon_img.putpixel((sx2, sy2), STEEL_SHINE)

    # 6. Optical Prism Sight on Riser at (36, 68)
    wd.polygon([(36, 65), (40, 68), (36, 71)], fill=BLUE_BASE, outline=OUTLINE)
    wd.point((37, 68), fill=MINT_LIGHT)

    # 7. Nocked Mint Glow Energy Arrow pointing left/forward from (42, 76) to (18, 76)
    for ax in range(18, 43):
        weapon_img.putpixel((ax, 76), MINT_LIGHT)
        if ax % 2 == 0:
            weapon_img.putpixel((ax, 75), MINT_BASE)
    # Arrow tip arrowhead at (18, 76)
    wd.polygon([(18, 76), (22, 74), (22, 78)], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((19, 76), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_chameleon_prismatic_trivane", key_img),
        ("back_curio", "curio_chameleon_spiral_torsion_tail", curio_img),
        ("chassis", "chassis_chameleon_mirage_titanium_default", chassis_img),
        ("costume", "costume_chameleon_wasteland_scout_rig", costume_img),
        ("head_unit", "head_chameleon_crested_visor_cowl", head_img),
        ("optic_core", "face_chameleon_turret_rangefinder_lens", core_img),
        ("weapon", "weapon_chameleon_mirage_compound_bow", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{CHAMELEON_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{CHAMELEON_PD_DIR}/winding_key/key_chameleon_prismatic_trivane.png",
                    f"{KEY_DIR}/key_chameleon_prismatic_trivane.png")
    shutil.copyfile(f"{CHAMELEON_PD_DIR}/weapon/weapon_chameleon_mirage_compound_bow.png",
                    f"{WEAPON_DIR}/weapon_chameleon_mirage_compound_bow.png")
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

    proof_comp = f"{CHAMELEON_PD_DIR}/proof_paperdoll_chameleon_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{CHAMELEON_PD_DIR}/proof_paperdoll_chameleon_magenta.png"
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

    strip_path = f"{CHAMELEON_PD_DIR}/proof_chameleon_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/chameleon_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/chameleon_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
