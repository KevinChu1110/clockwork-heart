#!/usr/bin/env python3
"""
build_bison_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十四族 撼地野牛 (The Groundshaker Bison, bison) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/GROUNDSHAKER_BISON_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped matte cast iron plates,
  cold-rolled tungsten steel framework, high-pressure steam pneumatic actuators, antique brass and copper conduits)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Base: Ivory White (#FFFDF8)
    2. Primary: Junkyard Orange (#FFA010)
    3. Secondary: Brass Warm Orange (#E6A15C)
    4. Accent: Dopamine Gold (#FFD028)
    5. Ochre Brown: Weathered Cast Iron (#D49B4B / #3A2E2A)
    6. Functional Sky Blue: Pressure Gauge & Indicators (#38A0FF)
    7. Accent Mint Green: Safety Scale (#4ED86A)
    8. Blush Coral Pink: Vent Valve Ports (#FF5E8A)
    9. Outline: Deep Blue-Purple (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BISON_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bison"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Groundshaker Bison Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Weathered Cast Iron & Rust Tinplate (#3A2E2A & #584642)
IRON_BASE  = (68, 54, 48, 255)
IRON_LIGHT = (105, 86, 78, 255)
IRON_SHINE = (150, 128, 118, 255)
IRON_DARK  = (42, 34, 30, 255)
IRON_DEEP  = (28, 22, 20, 255)

# 2. Junkyard Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (190, 105, 8, 255)
ORANGE_DEEP  = (130, 68, 5, 255)

# 3. Warm Gold Brass (#FFD028 & #E6A15C)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

BRASS_BASE  = (230, 161, 92, 255)
BRASS_LIGHT = (248, 196, 142, 255)
BRASS_DARK  = (175, 110, 50, 255)

# 4. Ochre Brown (#D49B4B)
OCHRE_BASE  = (212, 155, 75, 255)
OCHRE_LIGHT = (235, 185, 115, 255)
OCHRE_DARK  = (160, 105, 45, 255)

# 5. Sky Blue Gauge Quartz (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)
SKY_DEEP  = (14, 60, 130, 255)

# 6. Safety Mint Green (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_DARK  = (42, 160, 68, 255)

# 7. Blush Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (195, 45, 85, 255)

# 8. Ivory Enamel White (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (228, 222, 212, 255)
IVORY_DARK  = (195, 188, 175, 255)

# 9. Steel & Rivet Gray
STEEL_BASE  = (85, 95, 110, 255)
STEEL_LIGHT = (130, 145, 165, 255)
STEEL_SHINE = (190, 205, 225, 255)
STEEL_DARK  = (50, 58, 70, 255)

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
                for (rx0, ry0, rx1, ry1) in ignore_regions:
                    if rx0 <= x <= rx1 and ry0 <= y <= ry1:
                        skip = True
                        break
                if skip:
                    continue

            # If pixel is empty/semi-transparent, check if any 4-neighbor is opaque
            if px_snap[x, y][3] < min_alpha:
                has_solid_neighbor = False
                for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h:
                        if px_snap[nx, ny][3] >= min_alpha:
                            has_solid_neighbor = True
                            break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL GROUNDSHAKER BISON SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_bison_heavy_cross_t_bar_cast_iron.png
    # Heavy Cross T-Bar Cast-Iron Winding Key (重工十字T柄生鐵發條鑰匙)
    # Socket boss at spine (64, 58), shaft extends diagonally up-right to (88, 22)
    # Protrudes clearly beyond head/shoulder silhouette (x: 72..104, y: 10..36)
    # Complies with 0-ART29 & 0-QA16: dark < 260px, max_run < 13px
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 58) to (88, 22)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 24.0
        sy = 58.0 - t * 36.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Base socket collar at spine (64, 58)
    kd.ellipse([64 - 5, 58 - 5, 64 + 5, 58 + 5], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 58 - 3, 64 + 3, 58 + 3], fill=GOLD_BASE)
    kd.ellipse([64 - 1, 58 - 1, 64 + 1, 58 + 1], fill=SKY_BASE)

    # 2. Heavy Cross T-Bar Hub at (88, 22)
    kcx, kcy = 88.0, 22.0

    # Draw Heavy Cross T-Bar handle arms (T-Bar across angle 45 deg or horizontal/vertical)
    # Main horizontal T-bar: length 26px, thickness 6px
    for x in range(int(kcx - 13), int(kcx + 14)):
        for y in range(int(kcy - 3), int(kcy + 4)):
            dx = (x - kcx) / 13.0
            dy = (y - kcy) / 3.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(dy))
                shine = max(0.0, 1.0 - abs(dx)) * spec
                r_v = int(np.clip(255 * (0.82 + 0.25 * spec) + 30 * shine, 0, 255))
                g_v = int(np.clip(208 * (0.82 + 0.25 * spec) + 30 * shine, 0, 255))
                b_v = int(np.clip(40 * (0.82 + 0.4 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Vertical crossbar stem: length 16px, thickness 5px
    for y in range(int(kcy - 8), int(kcy + 9)):
        for x in range(int(kcx - 2), int(kcx + 3)):
            spec = max(0.0, 1.0 - abs(x - kcx) / 2.5)
            r_v = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
            g_v = int(np.clip(208 * (0.85 + 0.2 * spec), 0, 255))
            b_v = int(np.clip(40 * (0.85 + 0.35 * spec), 0, 255))
            key_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Spherical Cast-Iron Knobs at ends of T-bar
    knob_positions = [(kcx - 13.0, kcy), (kcx + 13.0, kcy), (kcx, kcy - 8.0)]
    for kx, ky in knob_positions:
        kd.ellipse([int(kx - 3), int(ky - 3), int(kx + 3), int(ky + 3)], fill=ORANGE_BASE, outline=OUTLINE_KEY)
        kd.ellipse([int(kx - 1.5), int(ky - 1.5), int(kx + 1.5), int(ky + 1.5)], fill=GOLD_LIGHT)
        kd.point((int(kx), int(ky)), fill=WHITE_SHINE)

    # Central Ratchet Locking Collar
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=IRON_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 1), int(kcy - 1), int(kcx + 1), int(kcy + 1)], fill=SKY_BASE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_bison_twin_vent_exhaust_stack.png
    # Twin-Vent Exhaust Heat-Sink Stack (雙聯排氣散熱煙囪)
    # Features:
    # - Two heavy stamped exhaust pipes angled slightly outwards:
    #   Left pipe: from (46, 56) to (42, 28)
    #   Right pipe: from (78, 56) to (82, 28)
    # - Weighted flapper caps at top angled at 20 degrees
    # - Copper cooling rings and rivet details
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    pipe_defs = [
        ((46.0, 56.0), (42.0, 28.0), -1),  # Left stack
        ((78.0, 56.0), (82.0, 28.0), 1)    # Right stack
    ]

    for (x0, y0), (x1, y1), side in pipe_defs:
        for t in np.linspace(0.0, 1.0, 40):
            px = x0 + t * (x1 - x0)
            py = y0 + t * (y1 - y0)
            for dx in range(-4, 5):
                spec = max(0.0, 1.0 - abs(dx) / 4.0)
                # Stamped cast iron pipe with copper heat fins
                is_fin = int(py) % 5 == 0
                if is_fin:
                    r_p = int(np.clip(212 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                    g_p = int(np.clip(155 * (0.8 + 0.3 * spec) + 25 * spec, 0, 255))
                    b_p = int(np.clip(75 * (0.8 + 0.4 * spec) + 20 * spec, 0, 255))
                else:
                    r_p = int(np.clip(68 * (0.8 + 0.4 * spec) + 35 * spec, 0, 255))
                    g_p = int(np.clip(54 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
                    b_p = int(np.clip(48 * (0.8 + 0.4 * spec) + 25 * spec, 0, 255))
                curio_img.putpixel((int(px + dx), int(py)), (r_p, g_p, b_p, 255))

        # Flapper Cap at top of each stack
        top_x, top_y = int(x1), int(y1)
        cd.ellipse([top_x - 5, top_y - 2, top_x + 5, top_y + 2], fill=IRON_DARK, outline=OUTLINE)
        cd.ellipse([top_x - 4, top_y - 1, top_x + 4, top_y + 1], fill=GOLD_BASE)

        # Angled hinged flapper lid
        flapper_x1 = top_x + side * 6
        flapper_y1 = top_y - 4
        cd.line([(top_x - side * 4, top_y - 1), (flapper_x1, flapper_y1)], fill=ORANGE_BASE, width=2)
        cd.ellipse([flapper_x1 - 1, flapper_y1 - 1, flapper_x1 + 1, flapper_y1 + 1], fill=GOLD_LIGHT)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_bison_rusted_tinplate_default.png
    # Groundshaker Bison Rusted Tinplate Chassis (撼地野牛生鏽耐磨馬口鐵重裝素體)
    # Features:
    # - 2.2 Chibi heavy low-center-of-gravity cast iron & tinplate chassis
    # - Ground contact shadow at (64, 116)
    # - Articulated twin-flange cast iron hooves at (44, 113) and (72, 113)
    # - Thick shock-absorbing legs with compression springs
    # - Solid neck collar at (x: 52..76, y: 44..56) for seamless head seating (zero holes)
    # - High-torque spring hump chassis on shoulders (x: 44..84, y: 50..66)
    # - Torso: stamped tinplate with junkyard orange (#FFA010) coating & rivets
    # - Left hand clenched at (42, 76)
    # - Right arm tucked at (84, 72)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 36, 116 - 6, 64 + 36, 116 + 6], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Articulated Twin-Flange Cast-Iron Hooves at (44, 113) and (72, 113)
    hoof_pos = [(44.0, 113.0), (72.0, 113.0)]
    for hx, hy in hoof_pos:
        # Sole damping plate
        ch_d.ellipse([int(hx - 9), int(hy - 3), int(hx + 9), int(hy + 3)], fill=IRON_DEEP, outline=OUTLINE)
        # Twin-flange hoof caps (two halves: left dx -7..-1, right dx 1..7)
        ch_d.ellipse([int(hx - 8), int(hy - 2), int(hx - 1), int(hy + 2)], fill=IRON_BASE)
        ch_d.ellipse([int(hx + 1), int(hy - 2), int(hx + 8), int(hy + 2)], fill=IRON_BASE)
        ch_d.line([(int(hx - 6), int(hy)), (int(hx - 2), int(hy))], fill=GOLD_BASE, width=1)
        ch_d.line([(int(hx + 2), int(hy)), (int(hx + 6), int(hy))], fill=GOLD_BASE, width=1)

    # 3. Thick Articulated Legs with Compression Springs
    leg_paths = [
        ((44.0, 112.0), (52.0, 88.0)),
        ((72.0, 112.0), (68.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-6, 7):
                spec = max(0.0, 1.0 - abs(dx) / 6.0)
                r_l = int(np.clip(68 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                g_l = int(np.clip(54 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                b_l = int(np.clip(48 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 4, mid_y - 2, mid_x + 4, mid_y + 2], fill=ORANGE_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 50..78, y: 44..58)
    for ny in range(44, 59):
        for nx in range(50, 79):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 14.0)
            r_n = int(np.clip(68 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
            g_n = int(np.clip(54 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            b_n = int(np.clip(48 * (0.8 + 0.45 * spec) + 25 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 5. Hump Shoulder Chassis & Torso Shell (x: 40..88, y: 54..98)
    cx_t, cy_t = 64.0, 76.0
    for y in range(54, 99):
        for x in range(40, 89):
            dx = (x - cx_t) / 23.0
            dy = (y - cy_t) / 21.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 23.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Ivory white central pressure dial plate
                is_dial_plate = ((x - 64.0)**2 / 12.0**2 + (y - 74.0)**2 / 12.0**2 <= 1.0)
                if is_dial_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    # Junkyard bright orange (#FFA010) tinplate coating with gold brass trim
                    is_rim = dist_sq >= 0.75
                    if is_rim:
                        r_t = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        g_t = int(np.clip(208 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        b_t = int(np.clip(40 * (0.8 + 0.4 * spec) + 35 * shine - 10 * edge_shade, 0, 255))
                    else:
                        r_t = int(np.clip(255 * (0.8 + 0.3 * spec) + 25 * shine - 15 * edge_shade, 0, 255))
                        g_t = int(np.clip(160 * (0.8 + 0.3 * spec) + 20 * shine - 15 * edge_shade, 0, 255))
                        b_t = int(np.clip(16 * (0.8 + 0.4 * spec) + 15 * shine - 10 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # High-Torque Pressure Indicator in center of chest (64, 74)
    ch_d.ellipse([64 - 5, 74 - 5, 64 + 5, 74 + 5], fill=IRON_DARK, outline=OUTLINE)
    ch_d.ellipse([64 - 4, 74 - 4, 64 + 4, 74 + 4], fill=SKY_BASE)
    ch_d.ellipse([64 - 2, 74 - 2, 64 + 2, 74 + 2], fill=SKY_LIGHT)
    # Dial indicator needle
    ch_d.line([(64, 74), (66, 71)], fill=GOLD_BASE, width=1)

    # 6. Clenched Left Hand at (42, 76)
    ch_d.ellipse([42 - 5, 76 - 5, 42 + 5, 76 + 5], fill=IRON_DARK, outline=OUTLINE)
    ch_d.ellipse([42 - 4, 76 - 4, 42 + 4, 76 + 4], fill=IRON_BASE)
    ch_d.ellipse([42 - 2, 76 - 2, 42 + 2, 76 + 2], fill=IRON_LIGHT)
    ch_d.line([(42 - 3, 76), (42 + 3, 76)], fill=GOLD_BASE, width=1)

    # 7. Right Arm Grip Shoulder Joint at (84, 72)
    ch_d.ellipse([84 - 5, 72 - 5, 84 + 5, 72 + 5], fill=IRON_DARK, outline=OUTLINE)
    ch_d.ellipse([84 - 4, 72 - 4, 84 + 4, 72 + 4], fill=ORANGE_BASE)
    ch_d.ellipse([84 - 2, 72 - 2, 84 + 2, 72 + 2], fill=GOLD_BASE)

    # Strictly clear any stray pixels in weapon zone (x >= 94) for 0-ART9/11
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # Re-enforce zero pixels at x >= 94 after outline pass
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_bison_riveted_brow_horn_crest.png
    # Riveted I-Beam Brow Horn Crest (鉚接工字鋼曲角重盔)
    # Features:
    # - Stamped spherical cast iron skull helmet centered at (64, 46), radius 22px
    # - Two massive curved forged I-beam mechanical horns:
    #   Left horn: curves up-left to (22, 22), with yellow-black hazard stripes
    #   Right horn: curves up-right to (106, 22), with yellow-black hazard stripes
    # - Triple checkerplate sunshade visor over brow (x: 48..80, y: 32..38)
    # - Sturdy snout with dual coral pink steam vent relief ports at (57, 52) and (71, 52)
    # - STRICT 0-ART27: Eye sockets centered at (54, 42) and (74, 42) must be hollow (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Stamped cast iron helmet sphere centered at (64, 46)
    hcx, hcy = 64.0, 46.0
    for y in range(24, 62):
        for x in range(42, 87):
            dx = (x - hcx) / 22.0
            dy = (y - hcy) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 22.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                r_h = int(np.clip(68 * (0.8 + 0.45 * spec) + 40 * shine - 20 * edge_shade, 0, 255))
                g_h = int(np.clip(54 * (0.8 + 0.45 * spec) + 35 * shine - 20 * edge_shade, 0, 255))
                b_h = int(np.clip(48 * (0.8 + 0.45 * spec) + 30 * shine - 15 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 2. Dual Forged I-Beam Horns
    # Left Horn: from (46, 38) curving to (22, 22)
    for t in np.linspace(0.0, 1.0, 40):
        hx = 46.0 - t * 24.0
        # Curve upwards
        hy = 38.0 - np.sin(t * np.pi * 0.5) * 16.0
        thick = 4.5 * (1.0 - 0.4 * t)
        for dx in range(int(-thick), int(thick + 1)):
            for dy in range(int(-thick), int(thick + 1)):
                if dx**2 + dy**2 <= thick**2:
                    # Hazard stripe pattern: alternating black and gold
                    is_stripe = int((hx + hy) / 4.0) % 2 == 0
                    if is_stripe:
                        r_hn, g_hn, b_hn = GOLD_BASE[:3]
                    else:
                        r_hn, g_hn, b_hn = IRON_DARK[:3]
                    head_img.putpixel((int(hx + dx), int(hy + dy)), (r_hn, g_hn, b_hn, 255))

    # Right Horn: from (82, 38) curving to (106, 22)
    for t in np.linspace(0.0, 1.0, 40):
        hx = 82.0 + t * 24.0
        hy = 38.0 - np.sin(t * np.pi * 0.5) * 16.0
        thick = 4.5 * (1.0 - 0.4 * t)
        for dx in range(int(-thick), int(thick + 1)):
            for dy in range(int(-thick), int(thick + 1)):
                if dx**2 + dy**2 <= thick**2:
                    is_stripe = int((hx - hy) / 4.0) % 2 == 0
                    if is_stripe:
                        r_hn, g_hn, b_hn = GOLD_BASE[:3]
                    else:
                        r_hn, g_hn, b_hn = IRON_DARK[:3]
                    head_img.putpixel((int(hx + dx), int(hy + dy)), (r_hn, g_hn, b_hn, 255))

    # Horn tip golden caps
    hd.ellipse([22 - 3, 22 - 3, 22 + 3, 22 + 3], fill=GOLD_BASE, outline=OUTLINE)
    hd.ellipse([106 - 3, 22 - 3, 106 + 3, 22 + 3], fill=GOLD_BASE, outline=OUTLINE)

    # 3. Triple Checkerplate Brow Sunshade Visor (x: 48..80, y: 32..38)
    for vy in range(32, 39):
        for vx in range(48, 81):
            spec = max(0.0, 1.0 - abs(vx - 64.0) / 16.0)
            hd.point((vx, vy), fill=ORANGE_BASE)
    hd.line([(48, 34), (80, 34)], fill=GOLD_BASE, width=1)
    hd.line([(50, 37), (78, 37)], fill=GOLD_LIGHT, width=1)

    # 4. Sturdy Cast Iron Snout Plate (x: 52..76, y: 46..58)
    for sy in range(46, 59):
        for sx in range(52, 77):
            dx = (sx - 64.0) / 12.0
            dy = (sy - 52.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r_s = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                g_s = int(np.clip(160 * (0.85 + 0.2 * spec), 0, 255))
                b_s = int(np.clip(16 * (0.85 + 0.3 * spec), 0, 255))
                head_img.putpixel((sx, sy), (r_s, g_s, b_s, 255))

    # Snout Rim Outline
    hd.ellipse([52, 46, 76, 58], outline=OUTLINE)

    # Dual Coral Pink Vent Valve Ports at (57, 52) and (71, 52)
    hd.ellipse([57 - 2, 52 - 2, 57 + 2, 52 + 2], fill=CORAL_BASE, outline=OUTLINE)
    hd.point((57, 52), fill=CORAL_LIGHT)
    hd.ellipse([71 - 2, 52 - 2, 71 + 2, 52 + 2], fill=CORAL_BASE, outline=OUTLINE)
    hd.point((71, 52), fill=CORAL_LIGHT)

    # 5. Hollow Eye Sockets for 0-ART27:
    # Clear eye sockets centered at (54, 42) and (74, 42), radius 4px
    h_px = head_img.load()
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    # Outline pass ignoring eye sockets
    ignore_eyes = [(50, 38, 58, 46), (70, 38, 78, 46)]
    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=100, ignore_regions=ignore_eyes)

    # Re-enforce strictly hollow eye sockets after outline pass
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_bison_junkyard_demolition_cuirass.png
    # Junkyard Demolition Cuirass & Tassets (舊庫拆解工兵重胸甲與防刮裙甲)
    # Features:
    # - Heavy stamped boiler demolition cuirass covering chest (x: 44..84, y: 60..84)
    # - Gold brass harness clasps on shoulders (48..54, 58..68) and (74..80, 58..68)
    # - 4 heavy scrap metal tassets hanging down to y: 94
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Cuirass Front Plate (x: 46..82, y: 62..84)
    for y in range(62, 85):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            # Stamped heavy cast-iron armor plate
            r_c = int(np.clip(68 * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
            g_c = int(np.clip(54 * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
            b_c = int(np.clip(48 * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
            costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Center vertical steel reinforcement beam
    for y in range(62, 85):
        for x in range(62, 67):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 2.5)
            r_c = int(np.clip(255 * (0.8 + 0.3 * spec), 0, 255))
            g_c = int(np.clip(208 * (0.8 + 0.3 * spec), 0, 255))
            b_c = int(np.clip(40 * (0.8 + 0.4 * spec), 0, 255))
            costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Shoulder Harness Straps & Heavy Gold Buckles
    strap_cols = [(48, 54), (74, 80)]
    for sx0, sx1 in strap_cols:
        for y in range(58, 70):
            for x in range(sx0, sx1 + 1):
                costume_img.putpixel((x, y), OCHRE_BASE)
        # Heavy gold brass buckle at (sx0+3, 64)
        bx = (sx0 + sx1) // 2
        cos_d.ellipse([bx - 3, 64 - 3, bx + 3, 64 + 3], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.ellipse([bx - 1, 64 - 1, bx + 1, 64 + 1], fill=WHITE_SHINE)

    # 2. Lower Tassets (4 hanging armored plates between y: 84 and 94)
    # 4 tasset plates: plate 1: 46..53, plate 2: 55..62, plate 3: 66..73, plate 4: 75..82
    tasset_x_spans = [(46, 53), (55, 62), (66, 73), (75, 82)]
    for tx0, tx1 in tasset_x_spans:
        for y in range(84, 95):  # strictly ends at 94, y >= 96 is completely zero!
            for x in range(tx0, tx1 + 1):
                spec = max(0.0, 1.0 - abs(x - (tx0 + tx1)/2.0) / 4.0)
                r_tas = int(np.clip(255 * (0.75 + 0.35 * spec), 0, 255))
                g_tas = int(np.clip(160 * (0.75 + 0.35 * spec), 0, 255))
                b_tas = int(np.clip(16 * (0.75 + 0.4 * spec), 0, 255))
                costume_img.putpixel((x, y), (r_tas, g_tas, b_tas, 255))
        # Tasset bottom rivet
        mid_tx = (tx0 + tx1) // 2
        cos_d.ellipse([mid_tx - 1, 92 - 1, mid_tx + 1, 92 + 1], fill=GOLD_BASE)

    # Clean outline pass
    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # Strictly enforce 0-ART26b: clear y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_bison_amber_pressure_gauge_eye.png
    # Amber Dual-Needle Pressure Gauge Eye (琥珀雙針耐震壓力表目鏡)
    # Features:
    # - Two thick quartz convex lens eyes centered at (54, 42) and (74, 42)
    # - Convex lenses with sky blue quartz glass (#38A0FF) & specular shines
    # - Dial cursor needles with safety mint green (#4ED86A) limit line
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:
        # Outer Brass Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Quartz Glass)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r_q = int(np.clip(56 * (0.8 + 0.3 * spec) + 120 * shine, 0, 255))
                    g_q = int(np.clip(160 * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    b_q = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    core_img.putpixel((x, y), (r_q, g_q, b_q, 255))

        # Miniature Green Safety Limit Arc
        c_d.arc([int(ex - 2), int(ey - 2), int(ex + 2), int(ey + 2)], start=210, end=330, fill=MINT_BASE, width=1)

        # Gauge Needles (Coral & Gold pointers)
        c_d.line([(int(ex), int(ey)), (int(ex + 2), int(ey - 1))], fill=CORAL_BASE, width=1)
        c_d.line([(int(ex), int(ey)), (int(ex - 1), int(ey + 2))], fill=GOLD_LIGHT, width=1)

        # Specular High-Reflectivity Spark
        core_img.putpixel((int(ex - 1), int(ey - 1)), WHITE_SHINE)

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_bison_wasteland_anvil_crusher_hammer.png
    # Wasteland Anvil Scrap-Crusher Sledgehammer (廢土重砧碎鐵巨鎚)
    # Features:
    # - Single-hand grip in right hand (84, 72)
    # - Heavy forged I-beam shaft extending diagonally down-forward to (98, 104)
    # - Massive four-square cast iron anvil crusher hammerhead (x: 88..120, y: 84..108)
    # - Honeycomb anti-skid impact face and gold reinforced bands
    # - Single-wield compliant (0-MKT7)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wp_d = ImageDraw.Draw(weapon_img)

    # 1. Heavy Forged I-Beam Hammer Shaft: from (84, 68) to (98, 104)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 84.0 + t * 14.0
        sy = 68.0 + t * 36.0
        for dx in range(-2, 3):
            spec = max(0.0, 1.0 - abs(dx) / 2.0)
            # Wrapped with textured canvas grip
            is_grip = (sy < 80.0)
            if is_grip:
                r_s = int(np.clip(212 * (0.8 + 0.3 * spec), 0, 255))
                g_s = int(np.clip(155 * (0.8 + 0.3 * spec), 0, 255))
                b_s = int(np.clip(75 * (0.8 + 0.35 * spec), 0, 255))
            else:
                r_s = int(np.clip(68 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
                g_s = int(np.clip(54 * (0.8 + 0.4 * spec) + 25 * spec, 0, 255))
                b_s = int(np.clip(48 * (0.8 + 0.4 * spec) + 20 * spec, 0, 255))
            weapon_img.putpixel((int(sx + dx), int(sy)), (r_s, g_s, b_s, 255))

    # Shaft end pommel knob at (84, 66)
    wp_d.ellipse([84 - 3, 66 - 3, 84 + 3, 66 + 3], fill=GOLD_BASE, outline=OUTLINE)
    wp_d.ellipse([84 - 1, 66 - 1, 84 + 1, 66 + 1], fill=GOLD_LIGHT)

    # 2. Massive Four-Square Cast Iron Anvil Crusher Head (x: 88..122, y: 84..108)
    # Anvil Head Center (105, 96)
    for y in range(86, 107):
        for x in range(90, 122):
            dx = (x - 105.0) / 15.0
            dy = (y - 96.0) / 10.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 100.0)**2 + (y - 92.0)**2)**0.5 / 15.0)
                shine = max(0.0, 1.0 - ((x - 100.0)**2 + (y - 92.0)**2)**0.5 / 5.0)**2

                # Anvil front impact face band (gold reinforcement)
                is_band = (103 <= x <= 107) or (x >= 118)
                if is_band:
                    r_h = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    g_h = int(np.clip(208 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    b_h = int(np.clip(40 * (0.8 + 0.4 * spec) + 30 * shine, 0, 255))
                else:
                    r_h = int(np.clip(68 * (0.85 + 0.4 * spec) + 40 * shine, 0, 255))
                    g_h = int(np.clip(54 * (0.85 + 0.4 * spec) + 35 * shine, 0, 255))
                    b_h = int(np.clip(48 * (0.85 + 0.4 * spec) + 30 * shine, 0, 255))

                weapon_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Anvil Horn / Nose extending forward at (122..126, 94..98)
    for y in range(94, 99):
        for x in range(120, 126):
            wp_d.point((x, y), fill=IRON_BASE)

    # Honeycomb Anti-Skid Impact Face (front edge x: 120, y: 88..104)
    for y in range(88, 105, 3):
        wp_d.ellipse([118, y - 1, 121, y + 1], fill=GOLD_LIGHT, outline=OUTLINE)

    # Central Shaft Mounting Collar & Rivets
    wp_d.ellipse([98 - 4, 96 - 4, 98 + 4, 96 + 4], fill=GOLD_BASE, outline=OUTLINE)
    wp_d.ellipse([98 - 2, 96 - 2, 98 + 2, 96 + 2], fill=ORANGE_BASE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_bison_heavy_cross_t_bar_cast_iron", key_img),
        ("back_curio", "curio_bison_twin_vent_exhaust_stack", curio_img),
        ("chassis", "chassis_bison_rusted_tinplate_default", chassis_img),
        ("head_unit", "head_bison_riveted_brow_horn_crest", head_img),
        ("costume", "costume_bison_junkyard_demolition_cuirass", costume_img),
        ("optic_core", "face_bison_amber_pressure_gauge_eye", core_img),
        ("weapon", "weapon_bison_wasteland_anvil_crusher_hammer", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{BISON_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{BISON_PD_DIR}/winding_key/key_bison_heavy_cross_t_bar_cast_iron.png", f"{KEY_DIR}/key_bison_heavy_cross_t_bar_cast_iron.png")
    shutil.copyfile(f"{BISON_PD_DIR}/weapon/weapon_bison_wasteland_anvil_crusher_hammer.png", f"{WEAPON_DIR}/weapon_bison_wasteland_anvil_crusher_hammer.png")
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

    proof_comp = f"{BISON_PD_DIR}/proof_paperdoll_bison_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{BISON_PD_DIR}/proof_paperdoll_bison_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 36
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
        sd.text((px + 4, py + H + 8), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{BISON_PD_DIR}/proof_bison_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/bison_idle_hd.png)
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
        sc_sdraw.ellipse((400 - 220, 1120 - 22, 400 + 220, 1120 + 22), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{showcase_dir}/bison_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    # ─────────────────────────────────────────────────────────────
    # BASE SPRITES (idle, idle_x3, party, web)
    # ─────────────────────────────────────────────────────────────
    # 1. bison_idle.png (64x64)
    idle_64 = composite.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(f"{REPO_ROOT}/game/assets/sprites/player/bison_idle.png")

    # 2. bison_idle_x3.png (128x128)
    composite.save(f"{REPO_ROOT}/game/assets/sprites/player/bison_idle_x3.png")

    # 3. party/bison_idle.png (128x128)
    os.makedirs(f"{REPO_ROOT}/game/assets/sprites/player/party", exist_ok=True)
    composite.save(f"{REPO_ROOT}/game/assets/sprites/player/party/bison_idle.png")

    # 4. web/media/hero/bison_idle.png (128x128)
    os.makedirs(f"{REPO_ROOT}/web/media/hero", exist_ok=True)
    composite.save(f"{REPO_ROOT}/web/media/hero/bison_idle.png")
    print("  ✓ Base idle sprites generated successfully")

    print("🎉 ALL GROUNDSHAKER BISON CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
