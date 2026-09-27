#!/usr/bin/env python3
"""
build_viper_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十七族 竹影青蛇 (The Bamboo Viper, viper) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/BAMBOO_VIPER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, carved bamboo lacquer plates,
  ivory enamel faceplate/belly, three-leaf bamboo leaf winding key clearly protruding from back silhouette,
  streamlined carved bamboo crest & conical hood, 7-segment articulated bamboo tail,
  gale bamboo shadow dagger weapon)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Bamboo Emerald Green (#4ED86A)
    2. Secondary Trim: Warm Deep Bamboo (#2E8B57)
    3. Faceplate Enamel: Ivory White (#FFFDF8)
    4. Accent & Key: Dopamine Gold Brass (#FFD028)
    5. Optic Core & Energy: Emerald Glass Jewel (#34D399)
    6. Tungsten Frame & Joints: Ink Stone Slate Gray (#3A4454)
    7. Costume Straps & Buckles: Coral Pink (#FF5E8A)
    8. Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
VIPER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/viper"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Bamboo Viper Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Bamboo Emerald Green (#4ED86A)
BAMBOO_BASE  = (78, 216, 106, 255)
BAMBOO_LIGHT = (118, 235, 142, 255)
BAMBOO_SHINE = (175, 250, 190, 255)
BAMBOO_DARK  = (52, 168, 76, 255)
BAMBOO_DEEP  = (32, 120, 52, 255)

# 2. Secondary Trim: Warm Deep Bamboo (#2E8B57)
TRIM_BASE  = (46, 139, 87, 255)
TRIM_LIGHT = (72, 175, 118, 255)
TRIM_SHINE = (120, 215, 160, 255)
TRIM_DARK  = (30, 98, 60, 255)
TRIM_DEEP  = (18, 65, 38, 255)

# 3. Faceplate & Chest Enamel: Ivory White (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (228, 222, 212, 255)
IVORY_DARK    = (192, 185, 174, 255)

# 4. Accent: Dopamine Golden Brass & Winding Key (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 5. Detail: Emerald Glass Jewel Optic & Energy Blade (#34D399)
EMERALD_BASE  = (52, 211, 153, 255)
EMERALD_LIGHT = (95, 235, 185, 255)
EMERALD_SHINE = (170, 255, 225, 255)
EMERALD_DARK  = (32, 158, 110, 255)
EMERALD_DEEP  = (18, 105, 72, 255)

# 6. Ink Stone Slate Gray Frame & Joints (#3A4454)
SLATE_BASE  = (58, 68, 84, 255)
SLATE_LIGHT = (92, 106, 128, 255)
SLATE_SHINE = (145, 160, 185, 255)
SLATE_DARK  = (38, 45, 58, 255)
SLATE_DEEP  = (24, 28, 36, 255)

# 7. Highlight: Coral Pink High-Pressure Seals & Buckles (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

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
    points_to_outline = set()

    for y in range(h):
        for x in range(w):
            p = px_snap[x, y]
            if isinstance(p, tuple) and len(p) >= 4 and p[3] >= min_alpha:
                for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if 0 <= nx < w and 0 <= ny < h:
                        np_px = px_snap[nx, ny]
                        if isinstance(np_px, tuple) and len(np_px) >= 4 and np_px[3] == 0:
                            if ignore_regions:
                                in_ignored = False
                                for ig_x, ig_y, ig_r in ignore_regions:
                                    if (nx - ig_x)**2 + (ny - ig_y)**2 <= ig_r**2:
                                        in_ignored = True
                                        break
                                if in_ignored:
                                    continue
                            points_to_outline.add((nx, ny))

    for px, py in points_to_outline:
        img.putpixel((px, py), outline_color)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL BAMBOO VIPER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_viper_bamboo_leaf_fan.png
    # Three-Leaf Bamboo Leaf Fan Key (三葉竹葉發條鑰匙)
    # Socket boss at upper spine (64, 58), shaft extends diagonally up-right to (96, 22)
    # This ensures the key wing PROTRUDES CLEARLY beyond the character's head silhouette (x: 90..116)!
    # Features:
    # - Polished brass shaft with bevel shading
    # - Three sculpted bamboo leaves radiating up and right
    # - Central taiji pivot hub (#FFD028 / #34D399)
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
    kd.ellipse([63, 57, 65, 59], fill=EMERALD_BASE)

    # 2. Key Hub at (96, 22) with Three Bamboo Leaf Blades
    kcx, kcy = 96.0, 22.0

    # Three sculpted bamboo leaf petals radiating from center: Up, Up-Right, Right-Down
    leaf_angles = [-1.70, -0.75, 0.15]
    for ang in leaf_angles:
        tip_len = 16.0
        tx = kcx + np.cos(ang) * tip_len
        ty = kcy + np.sin(ang) * tip_len
        perp = ang + 1.5708

        # Draw smooth shaded leaf petal
        for t in np.linspace(0.0, 1.0, 35):
            cx = kcx + t * (tx - kcx)
            cy = kcy + t * (ty - kcy)
            w_factor = np.sin(t * np.pi) * 4.5
            for s in np.linspace(-1.0, 1.0, 15):
                lx = cx + s * np.cos(perp) * w_factor
                ly = cy + s * np.sin(perp) * w_factor
                spec = max(0.0, 1.0 - abs(s))
                shine = max(0.0, (1.0 - abs(s)))**2 if t > 0.3 else 0.0

                # Gradient between golden brass and bamboo green
                r_l = int(np.clip(255 * (0.85 + 0.15 * spec) * (1 - 0.3*t) + 78 * 0.3 * t + 30 * shine, 0, 255))
                g_l = int(np.clip(208 * (0.85 + 0.15 * spec) * (1 - 0.2*t) + 216 * 0.2 * t + 35 * shine, 0, 255))
                b_l = int(np.clip(40 * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((int(lx), int(ly)), (r_l, g_l, b_l, 255))

        # Leaf center vein line
        for t in np.linspace(0.1, 0.9, 25):
            vx = int(kcx + t * (tx - kcx))
            vy = int(kcy + t * (ty - kcy))
            key_img.putpixel((vx, vy), GOLD_LIGHT)

    # Central Taiji Brass Hub & Glass Jewel at (96, 22)
    kd.ellipse([int(kcx - 6), int(kcy - 6), int(kcx + 6), int(kcy + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=EMERALD_BASE)
    kd.ellipse([int(kcx - 1), int(kcy - 1), int(kcx + 1), int(kcy + 1)], fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline to guarantee 0-ART29 compliance
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_viper_articulated_bamboo_tail.png
    # 7-Segment Articulated Bamboo Tail (七節同軸鉸接木簧蛇尾)
    # Originates at sacrum (52, 88), sweeps in an elegant S-curve down-left to touch ground at (14, 112):
    # Segments: (52, 88) -> (44, 93) -> (36, 98) -> (28, 102) -> (22, 105) -> (18, 108) -> (14, 112)
    # Features:
    # - 7 articulated cylindrical bamboo tube segments (#4ED86A / #2E8B57)
    # - Brass bevel rings (#FFD028) & internal spring pivot rivets at segment junctions
    # - Polished lacquer sheen & dark green reinforcing dorsal spine strips
    # - Rounded protective bamboo tip at ground level for stable tripod support
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    tail_segments = [
        (52.0, 88.0, 6.5, 4.5),    # Seg 1: Sacral base
        (44.0, 93.0, 6.0, 4.2),    # Seg 2: Descending curve
        (36.0, 98.0, 5.5, 3.8),    # Seg 3: Mid curve
        (28.0, 102.0, 5.0, 3.5),   # Seg 4: Transition segment
        (22.0, 105.0, 4.5, 3.2),   # Seg 5: Lower curve
        (18.0, 108.0, 4.0, 3.0),   # Seg 6: Near tip
        (14.0, 112.0, 3.5, 2.6),   # Seg 7: Ground contact tip
    ]

    # Draw transmission spine between segments
    for i in range(len(tail_segments) - 1):
        (x0, y0, _, _), (x1, y1, _, _) = tail_segments[i], tail_segments[i+1]
        for t in np.linspace(0.0, 1.0, 20):
            bx = x0 + t * (x1 - x0)
            by = y0 + t * (y1 - y0)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx**2 + dy**2 <= 4:
                        curio_img.putpixel((int(bx + dx), int(by + dy)), TRIM_BASE)

    # Draw each segment plate
    for seg_idx, (scx, scy, srx, sry) in enumerate(tail_segments):
        for y in range(int(scy - sry - 2), int(scy + sry + 3)):
            for x in range(int(scx - srx - 2), int(scx + srx + 3)):
                dx = (x - scx) / srx
                dy = (y - scy) / sry
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (scx - 1.5))**2 + (y - (scy - 1.5))**2)**0.5 / (srx * 1.2))
                    shine = max(0.0, 1.0 - ((x - (scx - 1.5))**2 + (y - (scy - 1.5))**2)**0.5 / (srx * 0.5))**2
                    edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                    # Outer gold / trim ring at joints
                    is_rim = dist_sq >= 0.75
                    if is_rim:
                        r_t = int(np.clip(255 * (0.8 + 0.2 * spec) - 20 * edge_shade, 0, 255))
                        g_t = int(np.clip(208 * (0.8 + 0.2 * spec) - 20 * edge_shade, 0, 255))
                        b_t = int(np.clip(40 * (0.8 + 0.4 * spec) + 30 * shine, 0, 255))
                    else:
                        # Bamboo emerald green lacquer
                        r_t = int(np.clip(78 * (0.75 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                        g_t = int(np.clip(216 * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                        b_t = int(np.clip(106 * (0.75 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))

                    curio_img.putpixel((x, y), (r_t, g_t, b_t, 255))

        # Pivot brass rivet in segment center
        cd.ellipse([int(scx - 1), int(scy - 1), int(scx + 1), int(scy + 1)], fill=GOLD_BASE, outline=OUTLINE)
        cd.point((int(scx), int(scy)), fill=WHITE_SHINE)

    # Segment 7 Tip: Polished Bamboo Round Cap at (14, 112)
    cd.ellipse([11, 110, 16, 114], fill=GOLD_BASE, outline=OUTLINE)
    cd.point((13, 111), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_viper_bamboo_lacquer_default.png
    # Features:
    # - 2.2 Chibi streamlined zen ninja bamboo toy chassis
    # - Soft ground contact shadow at (64, 116)
    # - Agile bamboo foot pads / landing blocks at (48, 112) and (72, 112)
    # - Slender articulated limbs with brass ball joints (#FFD028)
    # - Solid neck collar at (x: 54..74, y: 48..58) for seamless head seating
    # - Bamboo Emerald Green hull (#4ED86A) with warm deep bamboo trim (#2E8B57)
    # - Ivory White (#FFFDF8) enamel chest & belly plate with taiji cog accent
    # - Left hand clenched at (38, 80)
    # - Right arm tucked at ribs with weapon grip joint at (82, 74)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 30, 116 - 4, 64 + 30, 116 + 5], fill=(31, 26, 58, 120))
    ch_d.ellipse([64 - 20, 116 - 3, 64 + 20, 116 + 4], fill=(31, 26, 58, 160))

    # 2. Foot pads & Leg struts
    # Left foot: (48, 112), Right foot: (70, 112)
    for fx, fy in [(48, 112), (70, 112)]:
        # Brass ankle joint
        ch_d.ellipse([fx - 3, fy - 6, fx + 3, fy - 2], fill=GOLD_BASE, outline=OUTLINE)
        # Foot pad (bamboo crawler sole)
        for y in range(fy - 3, fy + 4):
            for x in range(fx - 6, fx + 7):
                dx = (x - fx) / 6.0
                dy = (y - fy) / 3.0
                if dx**2 + dy**2 <= 1.0:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                    r_f = int(np.clip(46 * (0.8 + 0.4 * spec), 0, 255))
                    g_f = int(np.clip(139 * (0.8 + 0.4 * spec), 0, 255))
                    b_f = int(np.clip(87 * (0.8 + 0.4 * spec), 0, 255))
                    chassis_img.putpixel((x, y), (r_f, g_f, b_f, 255))

    # Leg pillars connecting pelvis to feet
    # Left leg: (54, 94) -> (48, 108)
    for t in np.linspace(0.0, 1.0, 20):
        lx = int(54 * (1 - t) + 48 * t)
        ly = int(94 * (1 - t) + 108 * t)
        for dx in range(-3, 4):
            chassis_img.putpixel((lx + dx, ly), BAMBOO_DARK)
    # Right leg: (68, 94) -> (70, 108)
    for t in np.linspace(0.0, 1.0, 20):
        rx = int(68 * (1 - t) + 70 * t)
        ry = int(94 * (1 - t) + 108 * t)
        for dx in range(-3, 4):
            chassis_img.putpixel((rx + dx, ry), BAMBOO_DARK)

    # 3. Main Torso Hull (Bamboo Emerald Green + Ivory Enamel Belly)
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

                # Ivory Enamel Belly Shield in center (x: 52..72, y: 64..88)
                is_belly = (52 <= x <= 72) and (64 <= y <= 88) and (((x - 62)/10.0)**2 + ((y - 76)/12.0)**2 <= 1.0)
                if is_belly:
                    # Multi-tone ivory shading to satisfy 0-ART18 (>= 20 unique colors in 60:84, 48:72)
                    b_spec = max(0.0, 1.0 - ((x - 60)**2 + (y - 72)**2)**0.5 / 10.0)
                    r_b = int(np.clip(255 * (0.88 + 0.12 * b_spec) - 20 * edge_shade, 0, 255))
                    g_b = int(np.clip(253 * (0.88 + 0.12 * b_spec) - 20 * edge_shade, 0, 255))
                    b_b = int(np.clip(248 * (0.85 + 0.15 * b_spec) - 25 * edge_shade + 10 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))
                else:
                    # Bamboo Emerald Green Hull
                    r_m = int(np.clip(78 * (0.75 + 0.45 * spec) + 55 * shine - 25 * edge_shade, 0, 255))
                    g_m = int(np.clip(216 * (0.75 + 0.45 * spec) + 35 * shine - 25 * edge_shade, 0, 255))
                    b_m = int(np.clip(106 * (0.75 + 0.45 * spec) + 50 * shine - 25 * edge_shade, 0, 255))
                    chassis_img.putpixel((x, y), (r_m, g_m, b_m, 255))

    # Taiji Cog Medallion on Chest at (62, 70)
    ch_d.ellipse([58, 66, 66, 74], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.ellipse([60, 68, 64, 72], fill=EMERALD_BASE)
    ch_d.point((61, 69), fill=WHITE_SHINE)

    # 4. Solid Neck Collar at (x: 54..72, y: 48..56)
    for y in range(48, 57):
        for x in range(54, 72):
            chassis_img.putpixel((x, y), BAMBOO_DARK)
    ch_d.rectangle([56, 52, 70, 56], fill=BAMBOO_BASE, outline=OUTLINE)

    # 5. Left Arm: Tucked naturally on left side (38, 78)
    for t in np.linspace(0.0, 1.0, 20):
        ax = int(48 * (1 - t) + 38 * t)
        ay = int(66 * (1 - t) + 78 * t)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    chassis_img.putpixel((ax + dx, ay + dy), BAMBOO_BASE)
    # Left hand wooden sphere / ball at (38, 78)
    ch_d.ellipse([34, 75, 41, 82], fill=BAMBOO_LIGHT, outline=OUTLINE)
    ch_d.ellipse([36, 77, 39, 80], fill=GOLD_BASE)

    # 6. Right Arm: Tucked at ribs with weapon grip joint at (82, 74)
    # STRICT: Never exceed x = 93! x >= 94 must be 0 (0-ART9/11)
    for t in np.linspace(0.0, 1.0, 20):
        ax = int(74 * (1 - t) + 82 * t)
        ay = int(66 * (1 - t) + 74 * t)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4 and (ax + dx) < 94:
                    chassis_img.putpixel((ax + dx, ay + dy), BAMBOO_BASE)
    # Right hand ball socket at (82, 74)
    ch_d.ellipse([79, 71, 85, 77], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.point((81, 73), fill=WHITE_SHINE)

    # Apply outline safely
    apply_clean_outline(chassis_img)

    # Hard clamp to satisfy 0-ART9 / 0-ART11
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr, "RGBA")

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: COSTUME (Z: 25, Over Chassis / Under Head)
    # File: costume/costume_viper_zen_dojo_shinobi_wrap.png
    # Zen Dojo Shinobi Wrap (道場竹影夜行忍裝)
    # Features:
    # - Slate gray (#3A4454) ninja wrap with emerald trim (#4ED86A)
    # - Cross-chest shinobi harness & bamboo shoulder guards at (44, 62) and (78, 62)
    # - Dopamine gold braided waist sash (#FFD028) at y: 80..86
    # - Coral pink (#FF5E8A) shinobi buckle and oil flask clip
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Shoulder Pauldrons / Bamboo Guards
    # Left shoulder: (44, 62), Right shoulder: (78, 62)
    for sx, sy in [(44, 62), (78, 62)]:
        cos_d.ellipse([sx - 5, sy - 4, sx + 5, sy + 4], fill=SLATE_BASE, outline=OUTLINE)
        cos_d.ellipse([sx - 3, sy - 2, sx + 3, sy + 2], fill=BAMBOO_BASE)
        cos_d.point((sx, sy), fill=GOLD_BASE)

    # 2. Chest Vest / Ninja Wrap (x: 50..74, y: 60..78)
    for y in range(60, 78):
        for x in range(50, 74):
            dx = (x - 62) / 11.0
            dy = (y - 68) / 8.0
            if dx**2 + dy**2 <= 1.0:
                # Open V-neck revealing ivory chest medallion in center
                is_v_neck = (58 <= x <= 66) and (60 <= y <= 72) and (abs(x - 62) < (y - 59) * 0.6)
                if not is_v_neck:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                    r_c = int(np.clip(58 * (0.8 + 0.4 * spec), 0, 255))
                    g_c = int(np.clip(68 * (0.8 + 0.4 * spec), 0, 255))
                    b_c = int(np.clip(84 * (0.8 + 0.4 * spec), 0, 255))
                    costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Emerald trim on lapels
    cos_d.line([(57, 60), (62, 73)], fill=BAMBOO_LIGHT, width=1)
    cos_d.line([(67, 60), (62, 73)], fill=BAMBOO_LIGHT, width=1)

    # 3. Braided Gold Sash & Belt at y: 80..86
    for y in range(80, 87):
        for x in range(48, 76):
            if ((x - 62)/13.0)**2 + ((y - 83)/3.0)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(y - 83) / 3.0)
                r_s = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                g_s = int(np.clip(208 * (0.85 + 0.2 * spec), 0, 255))
                b_s = int(np.clip(40 * (0.85 + 0.3 * spec), 0, 255))
                costume_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    # Coral Pink Ninja Buckle at (62, 83)
    cos_d.ellipse([59, 81, 65, 85], fill=CORAL_BASE, outline=OUTLINE)
    cos_d.point((62, 83), fill=WHITE_SHINE)

    # Miniature bamboo lubricant flask on hip at (50, 86)
    cos_d.rectangle([48, 84, 52, 90], fill=BAMBOO_BASE, outline=OUTLINE)
    cos_d.point((50, 84), fill=GOLD_BASE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 4 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: HEAD UNIT (Z: 20, Over Chassis & Winding Key)
    # File: head_unit/head_viper_carved_bamboo_crest_hood.png
    # Streamlined Carved Bamboo Crest & Conical Hood (多節竹雕蛇冠斗笠)
    # Distinctive Features:
    # - Sculpted Bamboo Conical Hood (竹笠斗笠) spanning (x: 34..94, y: 16..32) with dark bamboo brim (#2E8B57)
    # - Bamboo Emerald Green cranial snake-crest plates (#4ED86A) with streamlined snake snout contour
    # - Crown conical finial & gold apex gem at (64, 14)
    # - Lateral brass acoustic listening ear-pivots at (40, 42) and (88, 42)
    # - Lower ivory white jaw armor at y: 46..58
    # - 0-ART27 MANDATORY: Eye socket zones (52, 40) and (76, 40) MUST BE HOLLOW (alpha=0)!
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0
    hrx, hry = 23.0, 18.0

    # 1. Main Head Cranial Dome
    for y in range(24, 60):
        for x in range(38, 90):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / (hrx * 1.1))
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / (hrx * 0.4))**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Lower jaw / cheek ivory plate (y >= 46, abs(x - 64) <= 16)
                is_jaw = (y >= 46) and (abs(x - hcx) <= 16)
                if is_jaw:
                    r_h = int(np.clip(255 * (0.85 + 0.15 * spec) - 15 * edge_shade, 0, 255))
                    g_h = int(np.clip(253 * (0.85 + 0.15 * spec) - 15 * edge_shade, 0, 255))
                    b_h = int(np.clip(248 * (0.85 + 0.15 * spec) - 20 * edge_shade, 0, 255))
                else:
                    # Bamboo Emerald Green cranial plate
                    r_h = int(np.clip(78 * (0.75 + 0.45 * spec) + 55 * shine - 25 * edge_shade, 0, 255))
                    g_h = int(np.clip(216 * (0.75 + 0.45 * spec) + 35 * shine - 25 * edge_shade, 0, 255))
                    b_h = int(np.clip(106 * (0.75 + 0.45 * spec) + 50 * shine - 25 * edge_shade, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 2. Conical Bamboo Hood & Wide Brim (竹雕斗笠帽簷)
    # The conical hat spans x: 34..94, y: 14..32, giving instant silhouette readability!
    # Apex at (64, 15), left edge at (34, 30), right edge at (94, 30)
    for y in range(16, 32):
        progress = (y - 15.0) / 16.0  # 0.0 at top to 1.0 at brim
        half_w = progress * 30.0
        for x in range(int(hcx - half_w), int(hcx + half_w + 1)):
            if 0 <= x < W:
                spec = max(0.0, 1.0 - abs(x - hcx) / (half_w + 1.0))
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - 20)**2)**0.5 / 10.0)**2

                # Brim rim at bottom (y >= 29) has warm deep bamboo & gold trim
                if y >= 29:
                    r_cap = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))
                    g_cap = int(np.clip(208 * (0.8 + 0.2 * spec), 0, 255))
                    b_cap = int(np.clip(40 * (0.8 + 0.4 * spec) + 20 * shine, 0, 255))
                else:
                    # Conical bamboo woven slats
                    r_cap = int(np.clip(46 * (0.8 + 0.4 * spec) + 35 * shine, 0, 255))
                    g_cap = int(np.clip(139 * (0.8 + 0.4 * spec) + 35 * shine, 0, 255))
                    b_cap = int(np.clip(87 * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))

                head_img.putpixel((x, y), (r_cap, g_cap, b_cap, 255))

    # Bamboo woven radiating lines on conical hat
    for ang in np.linspace(-0.8, 0.8, 7):
        for t in np.linspace(0.2, 0.95, 20):
            lx = int(hcx + np.sin(ang) * (t * 30.0))
            ly = int(16 + t * 15.0)
            if 0 <= lx < W and 0 <= ly < H:
                head_img.putpixel((lx, ly), TRIM_LIGHT)

    # Conical Apex Finial: Golden spire at (64, 14)
    hd.ellipse([62, 12, 66, 16], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 13), fill=WHITE_SHINE)

    # 3. Lateral Brass Ear-Pivots at (40, 42) and (88, 42)
    for ex, ey in [(40, 42), (88, 42)]:
        hd.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=GOLD_BASE, outline=OUTLINE)
        hd.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=TRIM_BASE)
        hd.point((ex, ey), fill=WHITE_SHINE)

    # 4. Forehead ridge & Brow plate
    hd.line([(50, 35), (64, 33), (78, 35)], fill=BAMBOO_LIGHT, width=2)

    # Clean outline pass BEFORE hollowing eye sockets
    apply_clean_outline(head_img, ignore_regions=[(52, 40, 6), (76, 40, 6)])

    # 5. STRICT 0-ART27 COMPLIANCE: HOLLOW EYE SOCKETS
    # Left eye socket at (52, 40), Right eye socket at (76, 40)
    # Ensure radius 4 around (52, 40) and (76, 40) is strictly 0 alpha!
    h_arr = np.array(head_img)
    for ey, ex in [(40, 52), (40, 76)]:
        for y in range(ey - 5, ey + 6):
            for x in range(ex - 5, ex + 6):
                if (x - ex)**2 + (y - ey)**2 <= 18:
                    h_arr[y, x, :] = 0
    head_img = Image.fromarray(h_arr, "RGBA")

    print("  ✓ Slice 5 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, Face Jewels & Features)
    # File: optic_core/face_viper_emerald_glass_optic.png
    # Features:
    # - Warm Emerald Glass Optics (#34D399) centered exactly at (52, 40) and (76, 40)
    # - Rich multi-tone depth (satisfies 0-QA31 >= 15 unique colors in optic zone)
    # - Inner concentric taiji gear reticle & crystalline highlight
    # - Miniature triangular bamboo nose plate at (64, 47)
    # - Discrete smiling mouth slit at y: 51..53
    # - 0-ART27 MANDATORY: Eye centers (52, 40) and (76, 40) MUST HAVE alpha > 200!
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    core_d = ImageDraw.Draw(core_img)

    # 1. Dual Emerald Optic Lenses at (52, 40) and (76, 40)
    eye_centers = [(52.0, 40.0), (76.0, 40.0)]
    for ecx, ecy in eye_centers:
        for y in range(int(ecy - 6), int(ecy + 7)):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= 4.8:
                    norm = dist / 4.8
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 4.0)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 1.8)**2

                    # Lens bevel & internal depth
                    if norm >= 0.85:
                        # Gold retaining bezel ring
                        r_e = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                        g_e = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                        b_e = int(np.clip(40 * (0.8 + 0.5 * spec), 0, 255))
                    else:
                        # Emerald glass crystal
                        r_e = int(np.clip(52 * (0.7 + 0.6 * spec) + 120 * shine, 0, 255))
                        g_e = int(np.clip(211 * (0.7 + 0.5 * spec) + 40 * shine, 0, 255))
                        b_e = int(np.clip(153 * (0.7 + 0.6 * spec) + 80 * shine, 0, 255))

                    core_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        # Distinct high-contrast reflection highlights
        core_d.point((int(ecx - 1), int(ecy - 1)), fill=WHITE_SHINE)
        core_d.point((int(ecx - 2), int(ecy - 1)), fill=WHITE_SHINE)
        core_d.point((int(ecx + 1), int(ecy + 1)), fill=EMERALD_LIGHT)

    # 2. Triangular Inset Bamboo Nose at (64, 47)
    core_d.polygon([(62, 46), (66, 46), (64, 49)], fill=TRIM_BASE, outline=OUTLINE)
    core_d.point((64, 47), fill=BAMBOO_LIGHT)

    # 3. Smiling Mechanical Mouth Slit at y: 52..54
    core_d.line([(59, 52), (62, 54), (64, 54), (66, 54), (69, 52)], fill=OUTLINE, width=1)
    core_d.point((64, 53), fill=TRIM_LIGHT)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Forefront Handheld Weapon)
    # File: weapon/weapon_viper_gale_bamboo_dagger.png
    # Gale Bamboo Shadow Dagger (疾風竹影短匕)
    # Held in right hand at (82, 74)
    # Scaled to distinct Dagger / Wakizashi proportions (~24px blade):
    # - Grip handle at (82, 74) extending up-back to brass ring pommel at (78, 69)
    # - Taiji disc guard (#FFD028) at (84, 76)
    # - Forward-thrusting bamboo shadow dagger blade (#2E8B57 / #4ED86A) to (102, 92)
    # - Razor-sharp emerald energy cutting edge (#34D399) with gold serrated teeth
    # - Micro wind-cut particles at blade tip
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Handle & Pommel Ring
    # Pommel ring at (77, 68)
    wd.ellipse([74, 65, 80, 71], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([76, 67, 78, 69], fill=(0, 0, 0, 0))

    # Grip wrapped in slate-gray silk wrap from (78, 69) to (84, 75)
    for t in np.linspace(0.0, 1.0, 20):
        hx = int(78 * (1 - t) + 84 * t)
        hy = int(69 * (1 - t) + 75 * t)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    weapon_img.putpixel((hx + dx, hy + dy), SLATE_BASE)
        # Gold wrap diamond accent
        if int(t * 10) % 3 == 0:
            weapon_img.putpixel((hx, hy), GOLD_LIGHT)

    # 2. Disc Guard (Tsuba) at (84, 76)
    wd.ellipse([80, 72, 88, 80], fill=GOLD_DARK, outline=OUTLINE)
    wd.ellipse([81, 73, 87, 79], fill=GOLD_BASE)
    wd.ellipse([83, 75, 85, 77], fill=EMERALD_BASE)

    # 3. Dagger Blade from (85, 77) to (102, 92)
    # Blade length ~ 22px, clearly dagger / wakizashi scaled
    blade_start = np.array([85.0, 77.0])
    blade_tip   = np.array([102.0, 92.0])
    blade_dir   = blade_tip - blade_start
    blade_len   = np.linalg.norm(blade_dir)
    blade_unit  = blade_dir / blade_len
    blade_perp  = np.array([-blade_unit[1], blade_unit[0]])

    for t in np.linspace(0.0, 1.0, 50):
        pos = blade_start + t * blade_dir
        width = (1.0 - t * 0.88) * 3.2  # Tapers towards tip
        for s in np.linspace(-1.0, 1.0, 15):
            px = pos + s * blade_perp * width
            ix, iy = int(round(px[0])), int(round(px[1]))
            if 0 <= ix < W and 0 <= iy < H:
                spec = max(0.0, 1.0 - abs(s))
                shine = max(0.0, (1.0 - abs(s)))**2

                # Spine side (s < 0): Carbonized dark bamboo
                # Cutting edge side (s > 0): Glowing emerald energy blade
                if s < 0:
                    r_w = int(np.clip(46 * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                    g_w = int(np.clip(139 * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                    b_w = int(np.clip(87 * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                else:
                    r_w = int(np.clip(52 * (0.7 + 0.6 * spec) + 80 * shine, 0, 255))
                    g_w = int(np.clip(211 * (0.7 + 0.5 * spec) + 40 * shine, 0, 255))
                    b_w = int(np.clip(153 * (0.7 + 0.6 * spec) + 90 * shine, 0, 255))

                weapon_img.putpixel((ix, iy), (r_w, g_w, b_w, 255))

        # Central fuller groove with gold inlay teeth
        if 0.15 <= t <= 0.75 and int(t * 30) % 4 == 0:
            c_pos = pos
            cx, cy = int(round(c_pos[0])), int(round(c_pos[1]))
            weapon_img.putpixel((cx, cy), GOLD_BASE)

    # Sharp white tip
    wd.point((102, 92), fill=WHITE_SHINE)
    wd.point((101, 91), fill=EMERALD_LIGHT)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_viper_bamboo_leaf_fan", key_img),
        ("back_curio", "curio_viper_articulated_bamboo_tail", curio_img),
        ("chassis", "chassis_viper_bamboo_lacquer_default", chassis_img),
        ("costume", "costume_viper_zen_dojo_shinobi_wrap", costume_img),
        ("head_unit", "head_viper_carved_bamboo_crest_hood", head_img),
        ("optic_core", "face_viper_emerald_glass_optic", core_img),
        ("weapon", "weapon_viper_gale_bamboo_dagger", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{VIPER_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{VIPER_PD_DIR}/winding_key/key_viper_bamboo_leaf_fan.png",
                    f"{KEY_DIR}/key_viper_bamboo_leaf_fan.png")
    shutil.copyfile(f"{VIPER_PD_DIR}/weapon/weapon_viper_gale_bamboo_dagger.png",
                    f"{WEAPON_DIR}/weapon_viper_gale_bamboo_dagger.png")
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

    proof_comp = f"{VIPER_PD_DIR}/proof_paperdoll_viper_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{VIPER_PD_DIR}/proof_paperdoll_viper_magenta.png"
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

    strip_path = f"{VIPER_PD_DIR}/proof_viper_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/viper_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/viper_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
