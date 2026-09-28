#!/usr/bin/env python3
"""
build_raven_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十一族 星儀渡鴉 (The Armillary Raven, raven) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/ARMILLARY_RAVEN_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological feathers, zero bird flesh, obsidian tinplate,
  astronomer hood & dual-flap brass beak, armillary dual-ring brass winding key,
  horologist scholar robe with gear pin & star chart cylinder, astrolabe monocle & celestial cyan core,
  armillary clockwork wand, articulated steampunk wings)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Obsidian Tinplate / Tungsten Steel (#3A3644) & Sunny Cream Ivory White (#FFFDF8)
    2. Secondary Hull / Robe: Warm Orange (#FFA010)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Quartz: Celestial Cyan Quartz (#38A0FF)
    6. Cute Coral Pink: Coral Pink (#FF5E8A)
    7. Cold Stamped Tungsten Steel: Tungsten Gray (#3A3644)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAVEN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/raven"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Armillary Raven Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Obsidian Tinplate / Cold Stamped Tungsten Steel (#3A3644)
OBS_BASE   = (58, 54, 68, 255)
OBS_LIGHT  = (96, 92, 110, 255)
OBS_SHINE  = (135, 130, 150, 255)
OBS_DARK   = (38, 35, 46, 255)
OBS_DEEP   = (26, 24, 32, 255)

# 2. Chest & Underbelly: Sunny Cream Ivory White (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (235, 226, 210, 255)
IVORY_DARK   = (210, 198, 178, 255)
IVORY_DEEP   = (180, 168, 148, 255)

# 3. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Scholar Robe Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (195, 110, 8, 255)
ORANGE_DEEP  = (135, 70, 5, 255)

# 5. Fresh Mint Green Trim & Sensor (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 6. Coral Pink Damping Pads (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 7. Celestial Cyan Quartz Core (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

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
            p_curr = px_snap[x, y]
            a_curr = p_curr[3] if isinstance(p_curr, (tuple, list)) else 0
            if a_curr < min_alpha:
                has_solid_neighbor = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            p_nb = px_snap[nx, ny]
                            a_nb = p_nb[3] if isinstance(p_nb, (tuple, list)) else 0
                            if a_nb >= min_alpha:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL ARMILLARY RAVEN SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_raven_armillary_sphere_brass.png
    # Features:
    # - 渾天雙環天球儀黃銅發條鑰匙 (Armillary Sphere Dual-Ring Brass Key)
    # - Centered at (72, 22), shaft extends down-left to spine socket boss (64, 56)
    # - Dual interlocking rings: Outer celestial equator ring, inner meridian ring at 45 deg
    # - Polished brass gradient (#FFD028, #FFA010, #FFFDF8)
    # - Complies strictly with 0-ART29 dark limit (< 260 px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft from spine (64, 56) to sphere base (72, 34)
    for t in np.linspace(0.0, 1.0, 28):
        sx = 64.0 + (72.0 - 64.0) * t
        sy = 56.0 + (34.0 - 56.0) * t
        for offset in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.3))
            shade = 1.0 - abs(offset) / 2.5
            r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * shade), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * shade), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine Socket Boss (61..67, 54..60)
    for y in range(54, 61):
        for x in range(61, 68):
            d = ((x - 64.0)**2 + (y - 57.0)**2)**0.5
            if d <= 3.5:
                key_img.putpixel((x, y), GOLD_LIGHT if d < 1.8 else GOLD_DARK)

    # 2. Armillary Sphere Rings at center (72, 22)
    k_cx, k_cy = 72.0, 22.0
    r_outer = 11.5
    r_inner = 7.5

    # Outer Celestial Equator Ring
    for y in range(8, 36):
        for x in range(58, 86):
            d = ((x - k_cx)**2 + (y - k_cy)**2)**0.5
            if abs(d - r_outer) <= 1.8:
                spec = max(0.0, 1.0 - abs(x - 70.0) / 10.0)
                shine = max(0.0, 1.0 - ((x - 68.0)**2 + (y - 15.0)**2)**0.5 / 5.0)
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((x, y), (r, g, b, 255))

    # Inner Meridian Ring (elliptical inclined ring)
    for y in range(12, 32):
        for x in range(62, 82):
            dx = (x - k_cx)
            dy = (y - k_cy)
            # 45-degree rotation
            u = (dx + dy) / 1.414
            v = (-dx + dy) / 1.414
            d_ell = (u**2 + (v / 0.55)**2)**0.5
            if abs(d_ell - r_inner) <= 1.5:
                spec = max(0.0, 1.0 - abs(x - 74.0) / 8.0)
                r = int(np.clip(GOLD_LIGHT[0] * (0.85 + 0.2 * spec), 0, 255))
                g = int(np.clip(GOLD_LIGHT[1] * (0.85 + 0.2 * spec), 0, 255))
                b = int(np.clip(GOLD_LIGHT[2] * (0.85 + 0.2 * spec), 0, 255))
                key_img.putpixel((x, y), (r, g, b, 255))

    # Central Sphere Pivot & Gnomon Axis Pin
    for y in range(19, 26):
        for x in range(69, 76):
            d = ((x - k_cx)**2 + (y - k_cy)**2)**0.5
            if d <= 3.2:
                key_img.putpixel((x, y), GOLD_SHINE if d <= 1.5 else GOLD_DARK)

    # Dial axis pin extensions (north-south)
    kd.line([(int(k_cx), int(k_cy - r_outer - 2)), (int(k_cx), int(k_cy + r_outer + 2))], fill=GOLD_SHINE, width=1)
    kd.point((int(k_cx), int(k_cy - r_outer - 2)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8)
    # File: back_curio/curio_raven_articulated_steampunk_wings.png
    # Features:
    # - 多節沖壓冷軋鎢鋼聯動機械羽翼 (Articulated Steampunk Wings)
    # - Left wing folds back-left (x: 22..52, y: 52..96)
    # - Right wing base folds back-right (x: 76..93, y: 54..92) strictly x < 94!
    # - Overlapping metallic lamellae with rivet pins and brass hinges (#FFD028)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Left Wing Articulated Blades (7 overlapping lamellae)
    blade_defs_left = [
        # (tip_x, tip_y, base_x, base_y, width)
        (23, 76, 44, 60, 4.0),
        (25, 83, 46, 64, 4.2),
        (29, 89, 48, 68, 4.0),
        (34, 94, 50, 72, 3.8),
        (40, 97, 52, 75, 3.5),
        (46, 95, 54, 78, 3.2),
        (50, 91, 56, 80, 3.0),
    ]

    for bx, by, rx, ry, bw in blade_defs_left:
        dx = by - ry
        dy = -(bx - rx)
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            nx = dx / length * bw
            ny = dy / length * bw
            poly = [(rx - nx, ry - ny), (rx + nx, ry + ny), (bx + nx * 0.3, by + ny * 0.3), (bx, by), (bx - nx * 0.3, by - ny * 0.3)]
            cd.polygon(poly, fill=OBS_BASE, outline=OUTLINE)

    # Shading pass over Left Wing to give multi-tone cold steel depth
    for y in range(54, 100):
        for x in range(21, 60):
            p = curio_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 100:
                dist_root = ((x - 50.0)**2 + (y - 70.0)**2)**0.5
                spec = max(0.0, 1.0 - abs(x - 36.0) / 18.0)
                shine = max(0.0, 1.0 - ((x - 32.0)**2 + (y - 82.0)**2)**0.5 / 12.0)**2
                shade = max(0.0, (dist_root - 10.0) / 25.0)

                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine - 15 * shade, 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine - 15 * shade, 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine - 15 * shade, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    for bx, by, rx, ry, bw in blade_defs_left:
        # Ridge line & Rivets
        cd.line([(rx, ry), (bx, by)], fill=OBS_LIGHT, width=1)
        cd.point((int(rx), int(ry)), fill=GOLD_BASE)

    # Wing Hinge Arm & Damper Tube
    cd.line([(44, 60), (56, 76)], fill=GOLD_BASE, width=2)
    cd.line([(45, 61), (57, 77)], fill=GOLD_LIGHT, width=1)
    cd.ellipse([42, 58, 46, 62], fill=GOLD_SHINE, outline=OUTLINE)
    cd.ellipse([54, 74, 58, 78], fill=GOLD_SHINE, outline=OUTLINE)

    # 2. Right Wing Base Blades (x strictly < 94)
    blade_defs_right = [
        (88, 62, 76, 58, 3.5),
        (91, 68, 77, 62, 3.8),
        (92, 75, 78, 66, 3.8),
        (90, 82, 78, 71, 3.6),
        (86, 88, 77, 76, 3.2),
    ]

    for bx, by, rx, ry, bw in blade_defs_right:
        dx = by - ry
        dy = -(bx - rx)
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            nx = dx / length * bw
            ny = dy / length * bw
            poly = [(rx - nx, ry - ny), (rx + nx, ry + ny), (bx + nx * 0.3, by + ny * 0.3), (bx, by), (bx - nx * 0.3, by - ny * 0.3)]
            cd.polygon(poly, fill=OBS_BASE, outline=OUTLINE)

    # Shading pass over Right Wing
    for y in range(56, 92):
        for x in range(74, 94):
            p = curio_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 100:
                spec = max(0.0, 1.0 - abs(x - 84.0) / 10.0)
                shine = max(0.0, 1.0 - ((x - 86.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    for bx, by, rx, ry, bw in blade_defs_right:
        cd.line([(rx, ry), (bx, by)], fill=OBS_LIGHT, width=1)
        cd.point((int(rx), int(ry)), fill=GOLD_BASE)

    # Right Wing Pivot Hinge
    cd.line([(76, 58), (82, 74)], fill=GOLD_BASE, width=2)
    cd.ellipse([74, 56, 78, 60], fill=GOLD_SHINE, outline=OUTLINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10)
    # File: chassis/chassis_raven_obsidian_brass_default.png
    # Features:
    # - 2.2 Head-to-Body Q-version mechanical bird automaton chassis
    # - Bare chassis torso (x: 44..84, y: 56..94) with multi-tone depth (0-ART18: >= 20 colors)
    # - Obsidian tungsten steel plates with Sunny Cream Ivory White belly panel
    # - 3-toed brass grasping claws with coral silicone damper pads at bottom (y: 96..112)
    # - Left wing/arm guarding pose at x: 34..48, y: 64..84
    # - Right arm at x: 80..93, y: 62..82
    # - STRICT 0-ART9/11: weapon zone x >= 94 MUST BE ZERO PIXELS!
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Main Torso Ellipsoid Hull (x: 44..84, y: 56..94)
    cx_t, cy_t = 64.0, 75.0
    rx_t, ry_t = 19.0, 18.0

    for y in range(56, 95):
        for x in range(44, 85):
            dx = (x - cx_t) / rx_t
            dy = (y - cy_t) / ry_t
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Underbelly vs flank plates
                is_belly = (abs(x - 64.0) <= 9.0 and y >= 64)
                if is_belly:
                    # Sunny Cream Ivory White
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.2 * spec) + 15 * shine - 25 * edge_shade, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.2 * spec) + 15 * shine - 25 * edge_shade, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.2 * spec) + 15 * shine - 25 * edge_shade, 0, 255))
                else:
                    # Obsidian Tungsten Plate
                    r = int(np.clip(OBS_BASE[0] * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                    g = int(np.clip(OBS_BASE[1] * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                    b = int(np.clip(OBS_BASE[2] * (0.75 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))

    # Torso Gold Brass Trim Band (y: 72..74)
    for bx in range(48, 81):
        if ((bx - cx_t)/rx_t)**2 + ((73.0 - cy_t)/ry_t)**2 <= 0.95:
            chassis_img.putpixel((bx, 73), GOLD_BASE)
            chassis_img.putpixel((bx, 74), GOLD_LIGHT)

    # Rivets on Torso Plate Flanks
    for rx, ry in [(49, 66), (48, 80), (79, 66), (80, 80)]:
        chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)

    # 2. Left Forearm/Wing Tip in Guarding Position (x: 34..48, y: 64..84)
    for y in range(64, 85):
        for x in range(34, 49):
            dx = (x - 41.0) / 6.0
            dy = (y - 74.0) / 9.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 39.0) / 6.0)
                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))
    # Brass wrist cuff & claw tips
    chd.line([(36, 79), (44, 79)], fill=GOLD_BASE, width=1)
    chd.polygon([(36, 81), (34, 86), (37, 84)], fill=GOLD_LIGHT, outline=OUTLINE)
    chd.polygon([(40, 82), (40, 87), (42, 84)], fill=GOLD_LIGHT, outline=OUTLINE)
    chd.polygon([(44, 81), (46, 86), (45, 83)], fill=GOLD_LIGHT, outline=OUTLINE)

    # 3. Right Upper Arm Base (x: 80..93, y: 62..82) - strictly x < 94!
    for y in range(64, 82):
        for x in range(80, 94):
            dx = (x - 86.0) / 6.0
            dy = (y - 72.0) / 8.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 85.0) / 6.0)
                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))
    chd.ellipse([88, 70, 92, 74], fill=GOLD_BASE, outline=OUTLINE)

    # 4. Brass Grasping Talons at bottom (y: 92..112)
    # Left Talon: x: 46..58, y: 92..112
    # Right Talon: x: 70..82, y: 92..112
    for t_cx in [52.0, 76.0]:
        # Ankle joint
        chd.ellipse([int(t_cx - 4), 92, int(t_cx + 4), 98], fill=GOLD_DARK, outline=OUTLINE)
        chd.ellipse([int(t_cx - 2), 94, int(t_cx + 2), 96], fill=CORAL_BASE)
        # 3 Forward Talons
        for toe_off, toe_len in [(-4, 10), (0, 13), (4, 10)]:
            start_x = int(t_cx + toe_off * 0.6)
            start_y = 96
            end_x = int(t_cx + toe_off * 1.5)
            end_y = 96 + toe_len
            chd.line([(start_x, start_y), (end_x, end_y)], fill=GOLD_BASE, width=2)
            chd.line([(start_x, start_y), (end_x, end_y)], fill=GOLD_LIGHT, width=1)
            # Talon tip point
            chd.point((end_x, end_y), fill=WHITE_SHINE)
            # Coral damping silicone pad under heel
            chd.point((int(t_cx), 98), fill=CORAL_BASE)

    # STRICT 0-ART9/11 enforcement: ensure zero pixels in x >= 94
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)

    # Re-enforce zero pixels at x >= 94 after outline pass
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_raven_astronomer_hood_beak.png
    # Features:
    # - 天文占星金屬風帽與黃銅機械喙 (Astronomer Hood & Brass Beak)
    # - Waterdrop streamline obsidian steel hood (x: 40..88, y: 16..54)
    # - Dual-flap high-carbon brass mechanical beak (x: 58..70, y: 44..54)
    # - Delicate brass directional antenna on crown (x: 63..65, y: 6..18)
    # - Eye socket outer brass bezel rings at (52, 40) and (76, 40)
    # - STRICT 0-ART27: Inner eye socket centers MUST be completely hollow (alpha == 0)
    #   at (39..41, 51..53) and (39..41, 75..77)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Crown Antenna (x: 63..65, y: 6..18)
    hd.line([(64, 8), (64, 20)], fill=GOLD_BASE, width=2)
    hd.line([(64, 8), (64, 20)], fill=GOLD_LIGHT, width=1)
    hd.ellipse([62, 5, 66, 9], fill=GOLD_SHINE, outline=OUTLINE)
    hd.point((64, 6), fill=MINT_BASE)

    # 2. Main Helmet Dome (x: 40..88, y: 18..54)
    cx_h, cy_h = 64.0, 36.0
    for y in range(18, 54):
        for x in range(40, 89):
            dx = (x - cx_h) / 22.0
            dy = (y - cy_h) / 16.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 3. Brow Vernier Graduation Ring & Mint Guide Line (y: 28..31, x: 44..84)
    for bx in range(44, 85):
        if ((bx - cx_h)/22.0)**2 + ((29.0 - cy_h)/16.0)**2 <= 0.98:
            head_img.putpixel((bx, 29), GOLD_BASE)
            head_img.putpixel((bx, 30), MINT_BASE)
            if bx % 4 == 0:
                head_img.putpixel((bx, 28), GOLD_LIGHT)

    # 4. Brass Mechanical Beak (Dual-Flap Brass Beak, x: 58..70, y: 44..55)
    beak_pts = [(58, 45), (70, 45), (66, 54), (64, 55), (62, 54)]
    hd.polygon(beak_pts, fill=GOLD_BASE, outline=OUTLINE)
    # Beak central dividing slit (dual-flap opening mechanism)
    hd.line([(59, 49), (69, 49)], fill=OUTLINE, width=1)
    hd.line([(60, 48), (68, 48)], fill=GOLD_LIGHT, width=1)
    hd.point((64, 52), fill=GOLD_SHINE)

    # 5. Golden Brass Bezel Rings surrounding Eye Sockets
    for ecx in [52.0, 76.0]:
        for y in range(34, 47):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - 40.0)**2)**0.5
                if 2.5 <= dist <= 5.8:
                    spec = max(0.0, 1.0 - abs(x - (ecx - 1.0)) / 5.0)
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec), 0, 255))
                    head_img.putpixel((x, y), (r, g, b, 255))

    # 6. STRICT 0-ART27 HOLLOW EYE SOCKETS
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
    # SLICE 5: OPTIC CORE (Z: 30)
    # File: optic_core/face_raven_astrolabe_monocle_lens.png
    # Features:
    # - 單片多重游標石英目鏡與天藍星核 (Astrolabe Monocle & Cyan Quartz Lens)
    # - Right eye (76, 40): Multi-lens brass monocle with vernier reticle
    # - Left eye (52, 40): Clear celestial cyan quartz spherical lens
    # - Aligns with 0-ART27: Center pixels at (52, 40) and (76, 40) have alpha > 200
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crd = ImageDraw.Draw(core_img)

    # 1. Left Eye (52, 40): Celestial Cyan Quartz Sphere
    ecx_l, ecy_l = 52.0, 40.0
    r_core = 5.2
    for y in range(35, 46):
        for x in range(47, 58):
            dist = ((x - ecx_l)**2 + (y - ecy_l)**2)**0.5
            if dist <= r_core:
                spec = max(0.0, 1.0 - ((x - 50.0)**2 + (y - 38.0)**2)**0.5 / 4.0)
                shine = max(0.0, 1.0 - ((x - 50.0)**2 + (y - 38.0)**2)**0.5 / 2.0)**2
                r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))
    crd.ellipse([int(ecx_l - r_core), int(ecy_l - r_core), int(ecx_l + r_core), int(ecy_l + r_core)], outline=OUTLINE, width=1)
    core_img.putpixel((50, 38), WHITE_SHINE)
    core_img.putpixel((51, 38), CYAN_SHINE)

    # 2. Right Eye (76, 40): Brass Monocle Frame & Triple-Layer Vernier Lens
    ecx_r, ecy_r = 76.0, 40.0
    r_mono = 5.8
    for y in range(34, 47):
        for x in range(70, 83):
            dist = ((x - ecx_r)**2 + (y - ecy_r)**2)**0.5
            if dist <= r_mono:
                spec = max(0.0, 1.0 - ((x - 74.0)**2 + (y - 38.0)**2)**0.5 / 4.5)
                shine = max(0.0, 1.0 - ((x - 74.0)**2 + (y - 38.0)**2)**0.5 / 2.0)**2
                # Monocle inner lens cyan quartz
                r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.2 * spec) + 25 * shine, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))

    # Brass outer ring and vernier tick marks
    crd.ellipse([int(ecx_r - r_mono), int(ecy_r - r_mono), int(ecx_r + r_mono), int(ecy_r + r_mono)], outline=GOLD_BASE, width=1)
    crd.ellipse([int(ecx_r - r_mono - 1), int(ecy_r - r_mono - 1), int(ecx_r + r_mono + 1), int(ecy_r + r_mono + 1)], outline=OUTLINE, width=1)

    # Vernier crosshair lines
    crd.line([(int(ecx_r - 3), int(ecy_r)), (int(ecx_r + 3), int(ecy_r))], fill=GOLD_LIGHT, width=1)
    crd.line([(int(ecx_r), int(ecy_r - 3)), (int(ecx_r), int(ecy_r + 3))], fill=GOLD_LIGHT, width=1)
    # Monocle bracket arm extending to helmet rim
    crd.line([(int(ecx_r + r_mono), int(ecy_r)), (int(ecx_r + r_mono + 3), int(ecy_r - 2))], fill=GOLD_BASE, width=1)

    core_img.putpixel((75, 39), WHITE_SHINE)
    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_raven_horologist_scholar_robe.png
    # Features:
    # - 鐘錶學者齒輪短披肩與星圖筒 (Horologist Scholar Robe & Star Chart Cylinder)
    # - Warm Orange (#FFA010) heavy canvas short robe over chest and shoulders (y: 54..92, x: 42..86)
    # - Fresh Mint Green (#4ED86A) edge piping
    # - Golden brass hexagonal gear pin at collar (64, 58)
    # - Slanted brass star chart cylinder at left waist (47..55, 76..88)
    # - STRICT 0-ART26b: lower zone y >= 96 MUST BE STRICTLY 0 PIXELS!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ctd = ImageDraw.Draw(costume_img)

    for y in range(54, 93):
        for x in range(42, 87):
            dx = (x - 64.0) / 19.0
            dy = (y - 70.0) / 17.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 66.0)**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 66.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dx**2 + dy**2 - 0.5) / 0.5)

                r = int(np.clip(ORANGE_BASE[0] * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                costume_img.putpixel((x, y), (r, g, b, 255))

    # Mint Green Edge Piping (Outer hem contour)
    for x in range(46, 83):
        y_bot = int(round(70.0 + 17.0 * (max(0.0, 1.0 - ((x - 64.0)/19.0)**2))**0.5))
        if y_bot <= 92:
            costume_img.putpixel((x, y_bot), MINT_BASE)
            costume_img.putpixel((x, y_bot - 1), MINT_LIGHT)

    # Collar Gear Pin at (64, 58)
    ctd.ellipse([61, 55, 67, 61], fill=GOLD_BASE, outline=OUTLINE)
    for ga in [0, 60, 120, 180, 240, 300]:
        grad = np.radians(ga)
        gx = int(round(64.0 + 3.5 * np.cos(grad)))
        gy = int(round(58.0 + 3.5 * np.sin(grad)))
        costume_img.putpixel((gx, gy), GOLD_LIGHT)
    ctd.point((64, 58), fill=WHITE_SHINE)

    # Slanted Brass Star Chart Cylinder at left waist (x: 47..55, y: 76..88)
    for t in np.linspace(0.0, 1.0, 18):
        cx_c = 54.0 - 5.0 * t
        cy_c = 76.0 + 11.0 * t
        for o in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(cx_c + o * 0.9))
            py = int(round(cy_c + o * 0.4))
            if px < W and py < 95:
                costume_img.putpixel((px, py), GOLD_BASE if abs(o) <= 1.0 else GOLD_DARK)
    # Mint green strap across chest
    ctd.line([(62, 59), (51, 78)], fill=MINT_BASE, width=2)
    ctd.line([(63, 60), (52, 79)], fill=MINT_LIGHT, width=1)

    # STRICT 0-ART26b enforcement: zero pixels at y >= 96
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(costume_img)

    # Re-enforce zero pixels at y >= 96 after outline pass
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_raven_armillary_wand.png
    # Features:
    # - 渾天星儀發條短杖 (Armillary Clockwork Wand)
    # - Right-hand single held (0-MKT7 compliant)
    # - Polished brass shaft extending from grip (88, 76) up to armillary head at (104, 38)
    # - Three concentric rotating brass rings with celestial cyan quartz core (#38A0FF)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Wand Shaft from (88, 78) to (104, 38)
    w_start = (88.0, 78.0)
    w_end = (104.0, 38.0)
    for t in np.linspace(0.0, 1.0, 48):
        sx = w_start[0] + (w_end[0] - w_start[0]) * t
        sy = w_start[1] + (w_end[1] - w_start[1]) * t
        for off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(sx + off * 0.9))
            py = int(round(sy - off * 0.35))
            if 0 <= px < W and 0 <= py < H:
                weapon_img.putpixel((px, py), GOLD_BASE if abs(off) <= 1.0 else GOLD_LIGHT)

    # Shaft vernier tick marks
    for t in [0.25, 0.45, 0.65, 0.85]:
        tx = int(round(w_start[0] + (w_end[0] - w_start[0]) * t))
        ty = int(round(w_start[1] + (w_end[1] - w_start[1]) * t))
        weapon_img.putpixel((tx - 1, ty), MINT_BASE)
        weapon_img.putpixel((tx + 1, ty), GOLD_LIGHT)

    # Grip at (88, 76)
    wd.ellipse([85, 73, 91, 79], fill=GOLD_DARK, outline=OUTLINE)
    wd.ellipse([86, 74, 90, 78], fill=ORANGE_BASE)

    # 2. Armillary Head at (104, 36)
    ah_cx, ah_cy = 104.0, 36.0
    r_head_outer = 11.0
    r_head_mid = 7.5

    # Outer Equator Ring
    for y in range(24, 49):
        for x in range(92, 117):
            d = ((x - ah_cx)**2 + (y - ah_cy)**2)**0.5
            if abs(d - r_head_outer) <= 1.6:
                spec = max(0.0, 1.0 - abs(x - 100.0) / 10.0)
                shine = max(0.0, 1.0 - ((x - 98.0)**2 + (y - 30.0)**2)**0.5 / 5.0)
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Middle Inclined Ring
    for y in range(26, 47):
        for x in range(94, 115):
            dx = x - ah_cx
            dy = y - ah_cy
            u = (dx + dy) / 1.414
            v = (-dx + dy) / 1.414
            d_mid = (u**2 + (v / 0.55)**2)**0.5
            if abs(d_mid - r_head_mid) <= 1.4:
                spec = max(0.0, 1.0 - abs(x - 106.0) / 8.0)
                weapon_img.putpixel((x, y), GOLD_LIGHT if spec > 0.5 else GOLD_BASE)

    # Central Celestial Cyan Quartz Core
    for y in range(32, 41):
        for x in range(100, 109):
            d = ((x - ah_cx)**2 + (y - ah_cy)**2)**0.5
            if d <= 3.8:
                spec = max(0.0, 1.0 - ((x - 102.0)**2 + (y - 34.0)**2)**0.5 / 3.0)
                shine = max(0.0, 1.0 - ((x - 102.0)**2 + (y - 34.0)**2)**0.5 / 1.5)**2
                r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    weapon_img.putpixel((103, 35), WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_raven_armillary_sphere_brass", key_img),
        ("back_curio", "curio_raven_articulated_steampunk_wings", curio_img),
        ("chassis", "chassis_raven_obsidian_brass_default", chassis_img),
        ("head_unit", "head_raven_astronomer_hood_beak", head_img),
        ("costume", "costume_raven_horologist_scholar_robe", costume_img),
        ("optic_core", "face_raven_astrolabe_monocle_lens", core_img),
        ("weapon", "weapon_raven_armillary_wand", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{RAVEN_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{RAVEN_PD_DIR}/winding_key/key_raven_armillary_sphere_brass.png", f"{KEY_DIR}/key_raven_armillary_sphere_brass.png")
    shutil.copyfile(f"{RAVEN_PD_DIR}/weapon/weapon_raven_armillary_wand.png", f"{WEAPON_DIR}/weapon_raven_armillary_wand.png")
    print("  ✓ Synced key & weapon to universal folders")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order by layer_z_index:
    # z=5:  winding_key
    # z=8:  back_curio
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

    proof_comp = f"{RAVEN_PD_DIR}/proof_paperdoll_raven_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{RAVEN_PD_DIR}/proof_paperdoll_raven_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 28
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Costume", "Optic", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 14)
    except Exception:
        font = ImageFont.load_default()

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 8), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{RAVEN_PD_DIR}/proof_raven_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([34, 108, 94, 120], fill=(31, 26, 58, 110))
    shd.ellipse([44, 110, 84, 118], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/raven_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/raven_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/raven_idle.png
    p_idle_64 = f"{PLAYER_DIR}/raven_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/raven_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/raven_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/raven_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/raven_idle.png"
    idle_with_shadow.save(p_web_idle)
    print("  ✓ Official Idle assets (64, 128, party, web) generated successfully")

    # 5. Showcase HD (800x1200 RGBA, 4-corner alpha=0)
    os.makedirs(SHOWCASE_DIR, exist_ok=True)
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
        sc_sdraw.ellipse((400 - 220, 1120 - 22, 400 + 220, 1120 + 22), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{SHOWCASE_DIR}/raven_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL ARMILLARY RAVEN CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
