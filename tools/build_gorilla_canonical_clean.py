#!/usr/bin/env python3
"""
build_gorilla_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十四族 鋼臂巨猩 (The Steelarm Gorilla, gorilla) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/STEELARM_GORILLA_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped matte cast iron plates,
  cold-rolled tungsten steel framework, high-pressure steam pneumatic actuators, antique brass and copper conduits)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Stamped Matte Cast Iron Black (#2B2836)
    2. Secondary Hull / Trim: Industrial Gold Brass (#FFD028)
    3. Steam Orange: Steam Gauge Orange (#FFA010)
    4. Forging Crimson: Forging Nutcracker Crimson (#E63946)
    5. Gauge Mint Green: Pressure Safe Mint Green (#4ED86A)
    6. Vent Sky Blue: Steam Vent Sky Cyan (#38A0FF)
    7. Boiler Ivory White Enamel: Boiler Ivory White (#FFFDF8)
    8. Dark Outline: Deep Warm Bronze/Brown Outline (#2E1F18 / #1F1A3A)
    Plus: Cold-Rolled Tungsten Steel (#4A5568 / #718096) & Copper Conduits (#B45309 / #D97706)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GORILLA_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/gorilla"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Steelarm Gorilla Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Stamped Matte Cast Iron Black (#2B2836)
IRON_BASE  = (43, 40, 54, 255)
IRON_LIGHT = (72, 68, 88, 255)
IRON_SHINE = (110, 105, 130, 255)
IRON_DARK  = (28, 26, 36, 255)
IRON_DEEP  = (18, 16, 24, 255)

# 2. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Steam Gauge Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (190, 105, 8, 255)
ORANGE_DEEP  = (130, 68, 5, 255)

# 4. Forging Nutcracker Crimson (#E63946)
CRIMSON_BASE  = (230, 57, 70, 255)
CRIMSON_LIGHT = (255, 105, 118, 255)
CRIMSON_SHINE = (255, 175, 185, 255)
CRIMSON_DARK  = (175, 30, 45, 255)
CRIMSON_DEEP  = (115, 15, 28, 255)

# 5. Pressure Safe Mint Green (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 6. Steam Vent Sky Cyan (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)
SKY_DEEP  = (14, 60, 130, 255)

# 7. Boiler Ivory White Enamel (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (228, 222, 212, 255)
IVORY_DARK  = (195, 188, 175, 255)

# 8. Cold-Rolled Tungsten Steel (#4A5568 / #718096)
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (113, 128, 150, 255)
STEEL_SHINE = (160, 174, 192, 255)
STEEL_DARK  = (45, 55, 72, 255)
STEEL_DEEP  = (26, 32, 44, 255)

# 9. Copper & Conduit Bronze (#D97706 / #B45309)
COPPER_BASE  = (217, 119, 6, 255)
COPPER_LIGHT = (245, 158, 11, 255)
COPPER_SHINE = (251, 191, 36, 255)
COPPER_DARK  = (180, 83, 9, 255)
COPPER_DEEP  = (120, 53, 15, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL STEELARM GORILLA SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_gorilla_heavy_t_forged_key.png
    # Metropolis Heavy T-Forged Winding Key (巨輪鍛工重型 T 字鍛鐵發條鑰匙)
    # Features:
    # - Socket boss at upper spine (64, 52)
    # - Heavy forged iron shaft extends up-right to T-hub at (84, 20)
    # - Heavy T-bar handle (width ~26px) from (72, 14) to (96, 26)
    # - Pure brass cylindrical counterweight heads at both ends
    # - Diamond knurled central grip with warm golden bronze finish
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from socket (64, 52) to T-hub (84, 20)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 64.0 + t * 20.0
        sy = 52.0 - t * 32.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Base socket collar at spine (64, 52)
    kd.ellipse([64 - 5, 52 - 5, 64 + 5, 52 + 5], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 52 - 3, 64 + 3, 52 + 3], fill=GOLD_BASE)
    kd.ellipse([64 - 1, 52 - 1, 64 + 1, 52 + 1], fill=ORANGE_BASE)

    # 2. T-Crossbar Handle: from (72, 14) to (96, 26)
    t_p1 = (72.0, 14.0)
    t_p2 = (96.0, 26.0)
    for t in np.linspace(0.0, 1.0, 50):
        tx = t_p1[0] + t * (t_p2[0] - t_p1[0])
        ty = t_p1[1] + t * (t_p2[1] - t_p1[1])
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    # Knurling pattern in center portion
                    is_knurl = (0.25 <= t <= 0.75) and ((int(tx + ty)) % 2 == 0)
                    if is_knurl:
                        r_t = int(np.clip(217 * (0.85 + 0.25 * spec), 0, 255))
                        g_t = int(np.clip(119 * (0.85 + 0.25 * spec), 0, 255))
                        b_t = int(np.clip(6 * (0.85 + 0.25 * spec) + 30 * spec, 0, 255))
                    else:
                        r_t = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                        g_t = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
                        b_t = int(np.clip(40 * (0.85 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(tx + dx), int(ty + dy)), (r_t, g_t, b_t, 255))

    # 3. Dual Brass / Copper Cylindrical Counterweights at ends: (72, 14) and (96, 26)
    for cwx, cwy in [t_p1, t_p2]:
        for y in range(int(cwy - 4), int(cwy + 5)):
            for x in range(int(cwx - 4), int(cwx + 5)):
                dist = ((x - cwx)**2 + (y - cwy)**2)**0.5
                if dist <= 4.0:
                    spec = max(0.0, 1.0 - dist / 4.0)
                    r_c = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                    g_c = int(np.clip(160 * (0.85 + 0.25 * spec), 0, 255))
                    b_c = int(np.clip(16 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_c, g_c, b_c, 255))
        kd.ellipse([int(cwx - 2), int(cwy - 2), int(cwx + 2), int(cwy + 2)], fill=GOLD_LIGHT, outline=OUTLINE_KEY)
        kd.point((int(cwx - 1), int(cwy - 1)), fill=WHITE_SHINE)

    # 4. Central Hub Knuckle at (84, 20)
    kd.ellipse([84 - 4, 20 - 4, 84 + 4, 20 + 4], fill=GOLD_BASE, outline=OUTLINE_KEY)
    kd.ellipse([84 - 2, 20 - 2, 84 + 2, 20 + 2], fill=ORANGE_BASE)
    kd.point((83, 19), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_gorilla_twin_turbo_exhaust_chimney.png
    # Twin Turbo Exhaust Chimneys (背部雙渦輪過熱洩壓排氣煙囪組件)
    # Features:
    # - Left Chimney: x=50..58, y=26..54 (rising from shoulder)
    # - Right Chimney: x=70..78, y=26..54 (rising from shoulder)
    # - Flared top rims with hinged circular rain flaps
    # - Warm copper manifold connecting both chimneys at (48..80, 48..60)
    # - High-pressure white steam clouds escaping from pipe tops
    # - Pressure relief safety bands with warm orange (#FFA010) highlights
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Back Boiler / Manifold Block (x: 48..80, y: 48..62)
    for my in range(48, 63):
        for mx in range(48, 81):
            spec = max(0.0, 1.0 - ((mx - 64.0)**2 / 16.0**2 + (my - 55.0)**2 / 8.0**2))
            if spec > 0:
                r_m = int(np.clip(217 * (0.8 + 0.3 * spec), 0, 255))
                g_m = int(np.clip(119 * (0.8 + 0.3 * spec), 0, 255))
                b_m = int(np.clip(6 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                curio_img.putpixel((mx, my), (r_m, g_m, b_m, 255))

    # Manifold rivets
    for rx in [52, 64, 76]:
        for ry in [51, 59]:
            cd.point((rx, ry), fill=GOLD_LIGHT)

    # 2. Left and Right Vertical Turbo Exhaust Pipes
    pipe_defs = [
        (54, 52, 28, 7, "left"),
        (74, 52, 28, 7, "right")
    ]
    for px, py_bottom, py_top, pw, name in pipe_defs:
        half_w = pw // 2
        for py in range(py_top, py_bottom + 1):
            for x_off in range(-half_w, half_w + 1):
                cur_x = px + x_off
                norm_w = abs(x_off) / float(half_w)
                spec = max(0.0, 1.0 - norm_w)
                shine = max(0.0, 1.0 - abs(x_off - (-1)) / 2.0)**2

                # Brass cylinder shading with heat indicator bands
                is_band = (py in range(py_top + 4, py_top + 7)) or (py in range(py_bottom - 6, py_bottom - 3))
                if is_band:
                    r_p = int(np.clip(255 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                    g_p = int(np.clip(160 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                    b_p = int(np.clip(16 * (0.85 + 0.4 * spec) + 50 * shine, 0, 255))
                else:
                    r_p = int(np.clip(255 * (0.8 + 0.3 * spec) + 45 * shine, 0, 255))
                    g_p = int(np.clip(208 * (0.8 + 0.3 * spec) + 45 * shine, 0, 255))
                    b_p = int(np.clip(40 * (0.8 + 0.4 * spec) + 60 * shine, 0, 255))

                curio_img.putpixel((cur_x, py), (r_p, g_p, b_p, 255))

        # Flared Top Rim at pipe mouth
        cd.ellipse([px - half_w - 1, py_top - 2, px + half_w + 1, py_top + 2], fill=GOLD_LIGHT, outline=OUTLINE)
        cd.ellipse([px - half_w, py_top - 1, px + half_w, py_top + 1], fill=IRON_DEEP)

        # Hinged Rain Cap Flap tilted back/outward
        flap_x_off = -2 if name == "left" else 2
        cd.line([(px - half_w + flap_x_off, py_top - 3), (px + half_w + flap_x_off, py_top - 5)], fill=STEEL_SHINE, width=2)
        cd.point((px + flap_x_off, py_top - 4), fill=GOLD_BASE)

    # 3. Soft Puffy Steam Clouds Escaping from Chimney Mouths
    steam_clouds = [
        (52.0, 20.0, 6.0, 5.0),
        (50.0, 12.0, 7.5, 6.0),
        (76.0, 20.0, 6.0, 5.0),
        (78.0, 12.0, 7.5, 6.0),
    ]
    for scx, scy, srx, sry in steam_clouds:
        for y in range(int(scy - sry - 1), int(scy + sry + 2)):
            for x in range(int(scx - srx - 1), int(scx + srx + 2)):
                dx = (x - scx) / srx
                dy = (y - scy) / sry
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (scx - 1.5))**2 + (y - (scy - 1.5))**2)**0.5 / (srx * 1.2))
                    # Soft white/ivory puff with pale sky cyan shadow
                    r_sm = int(np.clip(255 * (0.92 + 0.08 * spec), 0, 255))
                    g_sm = int(np.clip(253 * (0.92 + 0.08 * spec), 0, 255))
                    b_sm = int(np.clip(248 * (0.88 + 0.2 * spec) + 40 * (1.0 - spec), 0, 255))
                    a_sm = int(np.clip(235 * (1.0 - 0.45 * dist_sq), 0, 255))
                    curio_img.putpixel((x, y), (r_sm, g_sm, b_sm, a_sm))

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_gorilla_brass_heavy_default.png
    # Heavy Stamped Brass & Cast Iron Gorilla Chassis (鋼臂巨猩重型沖壓黃銅素體)
    # Features:
    # - 2.2 Chibi low-center-of-gravity cast iron gorilla chassis
    # - Soft ground contact shadow at (64, 116)
    # - Heavy wide stamping boots with diamond grip soles at (46, 113) and (82, 113)
    # - Short stout legs with knee ball-and-socket joints
    # - Massive barrel torso (x: 36..92, y: 54..96) with stamped iron plates (#2B2836) and brass bevels
    # - Wide arched shoulder cowls (left 30..48, right 80..92)
    # - Left Arm: Massive heavy forearm and clenched knuckle fist resting at (26..42, 80..96)
    # - Right Arm: Forearm positioned for gauntlet mount, wrist joint at (86..92, 70..78)
    # - Solid neck collar / jaw support at (52..76, 44..54) ensuring zero gap
    # - Rounded gorilla skull dome at (44..84, 22..48) with mechanical side rivets
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 38, 116 - 5, 64 + 38, 116 + 6], fill=(31, 26, 58, 135))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Heavy Stamping Boots with Diamond Grip Soles
    boot_positions = [(46.0, 113.0), (82.0, 113.0)]
    for bx, by in boot_positions:
        # Sole plate (cold-rolled steel / graphite)
        ch_d.ellipse([int(bx - 10), int(by - 3), int(bx + 10), int(by + 3)], fill=STEEL_DEEP, outline=OUTLINE)
        # Upper boot cap (cast iron)
        ch_d.ellipse([int(bx - 8), int(by - 2), int(bx + 8), int(by + 2)], fill=IRON_BASE)
        ch_d.ellipse([int(bx - 6), int(by - 1), int(bx + 6), int(by + 2)], fill=IRON_LIGHT)
        # Brass toe cap reinforcement
        ch_d.line([(int(bx - 6), int(by + 1)), (int(bx + 6), int(by + 1))], fill=GOLD_BASE, width=1)
        ch_d.point((int(bx), int(by)), fill=WHITE_SHINE)

    # 3. Short Stout Legs with Ball-and-Socket Knees
    leg_paths = [
        ((46.0, 112.0), (52.0, 92.0)),
        ((82.0, 112.0), (76.0, 92.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 24):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-6, 7):
                spec = max(0.0, 1.0 - abs(dx) / 6.0)
                r_l = int(np.clip(43 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                g_l = int(np.clip(40 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                b_l = int(np.clip(54 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 5, mid_y - 3, mid_x + 5, mid_y + 3], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 50..78, y: 44..56)
    for ny in range(44, 57):
        for nx in range(50, 79):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 14.0)
            r_n = int(np.clip(43 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            g_n = int(np.clip(40 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            b_n = int(np.clip(54 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 5. Gorilla Skull & Face Base (x: 44..84, y: 22..48)
    cx_h, cy_h = 64.0, 35.0
    for y in range(22, 49):
        for x in range(44, 85):
            dx = (x - cx_h) / 20.0
            dy = (y - cy_h) / 13.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_hd = int(np.clip(43 * (0.82 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                g_hd = int(np.clip(40 * (0.82 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                b_hd = int(np.clip(54 * (0.82 + 0.45 * spec) + 45 * shine - 15 * edge_shade, 0, 255))
                chassis_img.putpixel((x, y), (r_hd, g_hd, b_hd, 255))

    # Faceplate muzzle / jaw block (x: 52..76, y: 38..48)
    for my in range(38, 49):
        for mx in range(52, 77):
            spec = max(0.0, 1.0 - abs(mx - 64.0) / 12.0)
            is_rim = (my == 38 or my == 48 or mx == 52 or mx == 76)
            if is_rim:
                chassis_img.putpixel((mx, my), GOLD_BASE)
            else:
                r_m = int(np.clip(74 * (0.85 + 0.3 * spec), 0, 255))
                g_m = int(np.clip(85 * (0.85 + 0.3 * spec), 0, 255))
                b_m = int(np.clip(104 * (0.85 + 0.3 * spec), 0, 255))
                chassis_img.putpixel((mx, my), (r_m, g_m, b_m, 255))

    # 6. Bulky Barrel Torso (x: 36..92, y: 54..98)
    cx_t, cy_t = 64.0, 76.0
    for y in range(54, 99):
        for x in range(36, 93):
            # Clamp right edge to <= 92 so x >= 94 is strictly 0!
            if x >= 94:
                continue
            dx = (x - cx_t) / 26.0
            dy = (y - cy_t) / 22.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 6))**2 + (y - (cy_t - 6))**2)**0.5 / 24.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 6))**2 + (y - (cy_t - 6))**2)**0.5 / 8.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Outer cast iron hull with warm gold / brass edge rivets
                is_rim = dist_sq >= 0.78
                if is_rim:
                    r_t = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                    g_t = int(np.clip(208 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                    b_t = int(np.clip(40 * (0.8 + 0.4 * spec) + 35 * shine - 10 * edge_shade, 0, 255))
                else:
                    r_t = int(np.clip(43 * (0.8 + 0.45 * spec) + 45 * shine - 15 * edge_shade, 0, 255))
                    g_t = int(np.clip(40 * (0.8 + 0.45 * spec) + 45 * shine - 15 * edge_shade, 0, 255))
                    b_t = int(np.clip(54 * (0.8 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Torso Rivets for mechanical toy flavor
    torso_rivets = [(42, 64), (42, 82), (50, 94), (78, 94), (88, 64), (88, 82)]
    for rx, ry in torso_rivets:
        if rx < 94:
            ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
            ch_d.point((rx, ry), fill=WHITE_SHINE)

    # 7. Left Arm: Heavy Forearm & Clenched Fist (x: 26..44, y: 70..98)
    left_arm_pts = [
        ((44.0, 68.0), (34.0, 80.0)),
        ((34.0, 80.0), (32.0, 94.0))
    ]
    for (ax0, ay0), (ax1, ay1) in left_arm_pts:
        for t in np.linspace(0.0, 1.0, 22):
            ax = ax0 + t * (ax1 - ax0)
            ay = ay0 + t * (ay1 - ay0)
            for dx in range(-6, 7):
                for dy in range(-4, 5):
                    if dx**2 / 36.0 + dy**2 / 16.0 <= 1.0:
                        spec = max(0.0, 1.0 - abs(dx) / 6.0)
                        r_a = int(np.clip(43 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                        g_a = int(np.clip(40 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                        b_a = int(np.clip(54 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                        chassis_img.putpixel((int(ax + dx), int(ay + dy)), (r_a, g_a, b_a, 255))

    # Left Knuckle Fist (x: 28..38, y: 88..98) with Tungsten Knuckle Caps
    ch_d.ellipse([27, 88, 39, 98], fill=STEEL_BASE, outline=OUTLINE)
    ch_d.ellipse([29, 90, 37, 96], fill=STEEL_LIGHT)
    for kx in [30, 33, 36]:
        ch_d.ellipse([kx - 1, 93, kx + 1, 96], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((kx, 94), fill=WHITE_SHINE)

    # 8. Right Arm: Tucked to torso, wrist connection joint at (84..92, 70..78)
    right_arm_pts = [
        ((82.0, 66.0), (88.0, 74.0))
    ]
    for (rx0, ry0), (rx1, ry1) in right_arm_pts:
        for t in np.linspace(0.0, 1.0, 18):
            rx = rx0 + t * (rx1 - rx0)
            ry = ry0 + t * (ry1 - ry0)
            for dx in range(-4, 5):
                for dy in range(-4, 5):
                    if dx**2 + dy**2 <= 16:
                        cur_x = int(rx + dx)
                        if cur_x < 94:  # STRICT ZERO AT x >= 94
                            spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 4.0)
                            r_r = int(np.clip(43 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                            g_r = int(np.clip(40 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                            b_r = int(np.clip(54 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                            chassis_img.putpixel((cur_x, int(ry + dy)), (r_r, g_r, b_r, 255))

    # Wrist Mount Coupling Ring (x: 87..92, y: 72..76)
    for wy in range(72, 77):
        for wx in range(87, 93):
            if wx < 94:
                chassis_img.putpixel((wx, wy), GOLD_BASE)

    # 9. Shoulder Armor Cowls (Left: 32..46, 56..68; Right: 82..92, 56..68)
    for sx, sy in [(38.0, 62.0), (86.0, 62.0)]:
        for y in range(int(sy - 7), int(sy + 8)):
            for x in range(int(sx - 7), int(sx + 8)):
                if x < 94 and ((x - sx)**2 + (y - sy)**2)**0.5 <= 7.0:
                    spec = max(0.0, 1.0 - ((x - (sx - 2))**2 + (y - (sy - 2))**2)**0.5 / 7.0)
                    r_s = int(np.clip(255 * (0.8 + 0.3 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.3 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.4 * spec) + 40 * spec, 0, 255))
                    chassis_img.putpixel((x, y), (r_s, g_s, b_s, 255))
        if sx < 94:
            ch_d.ellipse([int(sx - 3), int(sy - 3), int(sx + 3), int(sy + 3)], fill=STEEL_BASE, outline=OUTLINE)
            ch_d.point((int(sx), int(sy)), fill=WHITE_SHINE)

    # STRICT 0-ART9/11: zero pixels at x >= 94!
    for cy in range(H):
        for cx in range(94, W):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    apply_clean_outline(chassis_img, ignore_regions=[(94, 0, 127, 127)])

    # Re-enforce zero pixels at x >= 94 after outline pass
    for cy in range(H):
        for cx in range(94, W):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_gorilla_riveted_brow_crest.png
    # Riveted Brow Crest & Mesh Ears (沖壓黃銅防撞重額甲與圓形散熱耳網)
    # Features:
    # - Heavy stamped arched brass brow crest (x: 46..82, y: 26..38)
    # - 5 cold-pressed steel rivets across brow crest
    # - Dual circular brass mesh ears on left (36..46, 32..42) and right (82..92, 32..42)
    # - Crown reinforcement ridge along skull top (x: 54..74, y: 20..28)
    # - STRICT 0-ART27:
    #   Left eye socket at (54, 38) MUST BE HOLLOW (alpha=0 at x in [53..55], y in [37..39])
    #   Right eye socket at (74, 38) MUST BE HOLLOW (alpha=0 at x in [73..75], y in [37..39])
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Circular Brass Mesh Ears
    ear_positions = [(40.0, 36.0, "left"), (88.0, 36.0, "right")]
    for ecx, ecy, side in ear_positions:
        r_ear = 6.5
        for y in range(int(ecy - r_ear - 1), int(ecy + r_ear + 2)):
            for x in range(int(ecx - r_ear - 1), int(ecx + r_ear + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_ear:
                    spec = max(0.0, 1.0 - dist / r_ear)
                    # Outer rim is beveled brass
                    is_rim = (dist >= 4.8)
                    if is_rim:
                        r_e = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                        g_e = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
                        b_e = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
                    else:
                        # Inner acoustic mesh grid
                        is_mesh = ((x + y) % 2 == 0)
                        if is_mesh:
                            r_e = int(np.clip(217 * (0.8 + 0.3 * spec), 0, 255))
                            g_e = int(np.clip(119 * (0.8 + 0.3 * spec), 0, 255))
                            b_e = int(np.clip(6 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                        else:
                            r_e = int(np.clip(43 * (0.8 + 0.35 * spec), 0, 255))
                            g_e = int(np.clip(40 * (0.8 + 0.35 * spec), 0, 255))
                            b_e = int(np.clip(54 * (0.8 + 0.35 * spec), 0, 255))
                    head_img.putpixel((x, y), (r_e, g_e, b_e, 255))
        hd.ellipse([int(ecx - 2), int(ecy - 2), int(ecx + 2), int(ecy + 2)], fill=GOLD_BASE, outline=OUTLINE)
        hd.point((int(ecx), int(ecy)), fill=WHITE_SHINE)

    # 2. Crown Plate / Ventilation Ridge on skull top (x: 54..74, y: 20..27)
    for ry in range(20, 28):
        for rx in range(54, 75):
            spec = max(0.0, 1.0 - abs(rx - 64.0) / 10.0)
            r_r = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
            g_r = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
            b_r = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
            head_img.putpixel((rx, ry), (r_r, g_r, b_r, 255))

    # Ridge rivets
    for rx in [56, 64, 72]:
        hd.point((rx, 22), fill=STEEL_SHINE)

    # 3. Heavy Stamped Brass Brow Crest (x: 46..82, y: 26..38)
    for y in range(26, 39):
        for x in range(46, 83):
            # Arched brow formula
            arch_dy = (x - 64.0)**2 / 45.0
            if y >= 26 + arch_dy * 0.4 and y <= 38 + arch_dy * 0.4:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
                shine = max(0.0, 1.0 - abs(y - 30) / 4.0)**2
                r_b = int(np.clip(255 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                g_b = int(np.clip(208 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                b_b = int(np.clip(40 * (0.85 + 0.4 * spec) + 50 * shine, 0, 255))
                head_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # 5 Cold-Pressed Rivets along Brow Crest
    brow_rivets = [(50, 31), (57, 29), (64, 28), (71, 29), (78, 31)]
    for rx, ry in brow_rivets:
        hd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=STEEL_BASE, outline=OUTLINE)
        hd.point((rx, ry), fill=WHITE_SHINE)

    # 4. Golden Bezel Rings Surrounding Eye Sockets
    for ecx in [54.0, 74.0]:
        ecy = 38.0
        for y in range(32, 45):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if 2.4 <= dist <= 5.5:
                    head_img.putpixel((x, y), GOLD_BASE)

    # 5. STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye socket centers MUST be completely transparent (alpha = 0)
    for y in range(36, 41):
        for x in range(52, 57):
            if ((x - 54.0)**2 + (y - 38.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(72, 77):
            if ((x - 74.0)**2 + (y - 38.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(head_img, ignore_regions=[(50, 34, 58, 42), (70, 34, 78, 42)])

    # Re-enforce 0-ART27 hollow eye socket centers
    for y in range(37, 40):
        for x in range(53, 56):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(73, 76):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_gorilla_steam_forge_boiler_harness.png
    # Steam Boiler Forging Harness (巨輪城高壓鍛工背帶與耐熱鍋爐胸甲)
    # Features:
    # - Creamy Ivory Enamel (#FFFDF8) boiler chestplate (x: 52..76, y: 60..82)
    # - Two heavy leather rivet harness straps crossing from shoulders
    # - Abdominal dual horizontal pneumatic cylinders (x: 54..74, y: 84..92) with copper sleeves
    # - Metropolis gear emblem and copper steam fittings
    # - STRICT 0-ART26b: Lower leg zone y >= 96 strictly ZERO pixels!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Heavy Leather Work Harness Straps from shoulders down to waist
    straps = [
        ((46.0, 56.0), (54.0, 84.0)),
        ((82.0, 56.0), (74.0, 84.0))
    ]
    for (sx0, sy0), (sx1, sy1) in straps:
        for t in np.linspace(0.0, 1.0, 30):
            sx = sx0 + t * (sx1 - sx0)
            sy = sy0 + t * (sy1 - sy0)
            for dx in range(-2, 3):
                costume_img.putpixel((int(sx + dx), int(sy)), (46, 31, 24, 255))
        # Brass Buckles
        bx = int(0.4 * sx0 + 0.6 * sx1)
        by = int(0.4 * sy0 + 0.6 * sy1)
        cos_d.rectangle([bx - 3, by - 2, bx + 3, by + 2], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.point((bx, by), fill=WHITE_SHINE)

    # 2. Rounded Ivory Enamel Boiler Chestplate (x: 52..76, y: 60..82)
    cx_cp, cy_cp = 64.0, 71.0
    for y in range(60, 83):
        for x in range(52, 77):
            dx = (x - cx_cp) / 11.5
            dy = (y - cy_cp) / 10.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_cp - 3))**2 + (y - (cy_cp - 3))**2)**0.5 / 12.0)
                shine = max(0.0, 1.0 - ((x - (cx_cp - 3))**2 + (y - (cy_cp - 3))**2)**0.5 / 4.0)**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                # Ivory porcelain boiler face
                r_iv = int(np.clip(255 * (0.92 + 0.15 * spec) - 35 * edge_shade + 30 * shine, 0, 255))
                g_iv = int(np.clip(253 * (0.92 + 0.15 * spec) - 35 * edge_shade + 30 * shine, 0, 255))
                b_iv = int(np.clip(248 * (0.92 + 0.15 * spec) - 35 * edge_shade + 30 * shine, 0, 255))
                costume_img.putpixel((x, y), (r_iv, g_iv, b_iv, 255))

    # Brass Beveled Border around Boiler Plate
    for y in range(59, 84):
        for x in range(51, 78):
            dx = (x - cx_cp) / 12.5
            dy = (y - cy_cp) / 11.5
            dist_sq = dx**2 + dy**2
            if 0.85 <= dist_sq <= 1.05:
                costume_img.putpixel((x, y), GOLD_BASE)

    # Central Forging Gear Emblem / Pressure Inspection Window
    cos_d.ellipse([64 - 5, 71 - 5, 64 + 5, 71 + 5], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([64 - 3, 71 - 3, 64 + 3, 71 + 3], fill=ORANGE_BASE)
    cos_d.ellipse([64 - 1, 71 - 1, 64 + 1, 71 + 1], fill=SKY_BASE)
    cos_d.point((63, 70), fill=WHITE_SHINE)

    # 3. Abdominal Dual Horizontal Pneumatic Cylinders (x: 54..74, y: 84..92)
    for py in [85, 89]:
        # Copper cylinder sleeve
        for px in range(54, 75):
            costume_img.putpixel((px, py), COPPER_BASE)
            costume_img.putpixel((px, py + 1), COPPER_DARK)
        # Shiny steel piston rods in center
        for px in range(61, 68):
            costume_img.putpixel((px, py), STEEL_SHINE)
            costume_img.putpixel((px, py + 1), STEEL_LIGHT)
        # Brass end caps
        cos_d.rectangle([53, py - 1, 55, py + 2], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.rectangle([73, py - 1, 75, py + 2], fill=GOLD_BASE, outline=OUTLINE)

    # STRICT 0-ART26b: Lower leg zone y >= 96 strictly ZERO pixels!
    for cy in range(96, H):
        for cx in range(W):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    apply_clean_outline(costume_img, ignore_regions=[(0, 96, 127, 127)])

    # Re-enforce y >= 96 zero pixels after outline
    for cy in range(96, H):
        for cx in range(W):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_gorilla_dual_gauge_optic_lens.png
    # Dual Steam Gauge Quartz Optics (雙聯黃銅蒸氣壓力表石英目鏡)
    # Features:
    # - Left lens centered at (54, 38)
    # - Right lens centered at (74, 38)
    # - Precision convex lens shading in industrial gold brass (#FFD028) dial
    # - Warm orange pressure needle (#FFA010) pointing up-right
    # - Safe pressure mint green arc (#4ED86A)
    # - High-reflection quartz glass glints (#FFFDF8)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(core_img)

    for ecx in [54.0, 74.0]:
        ecy = 38.0
        r_lens = 4.0
        for y in range(int(ecy - r_lens - 1), int(ecy + r_lens + 2)):
            for x in range(int(ecx - r_lens - 1), int(ecx + r_lens + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    norm_d = dist / r_lens
                    spec = max(0.0, 1.0 - norm_d)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 2.2)**2

                    # Golden dial face
                    r_e = int(np.clip(255 * (0.85 + 0.15 * spec) + 50 * shine, 0, 255))
                    g_e = int(np.clip(208 * (0.85 + 0.15 * spec) + 50 * shine, 0, 255))
                    b_e = int(np.clip(40 * (0.85 + 0.4 * spec) + 60 * shine, 0, 255))

                    core_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        # Mint green safe pressure arc on upper-left quadrant
        for ang in np.linspace(np.pi * 0.7, np.pi * 1.3, 12):
            ax = int(round(ecx + 2.8 * np.cos(ang)))
            ay = int(round(ecy - 2.8 * np.sin(ang)))
            core_img.putpixel((ax, ay), MINT_BASE)

        # Orange pressure indicator needle from center pointing up-right
        for t in np.linspace(0.0, 1.0, 6):
            nx = int(round(ecx + t * 2.5))
            ny = int(round(ecy - t * 2.0))
            core_img.putpixel((nx, ny), ORANGE_BASE)

        # Central needle pin
        core_img.putpixel((int(ecx), int(ecy)), IRON_DEEP)

        # Specular white reflection glint at upper-left
        core_img.putpixel((int(ecx - 1), int(ecy - 1)), WHITE_SHINE)
        core_img.putpixel((int(ecx), int(ecy - 2)), WHITE_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_gorilla_steam_forging_fist.png
    # High-Pressure Steam Forging Gauntlet (高壓蒸氣鍛打拳套)
    # Features:
    # - Single-wield right hand heavy gauntlet (0-MKT7 compliant)
    # - Stamped nutcracker crimson (#E63946) heavy shell (x: 84..116, y: 58..92)
    # - Sliding cold-rolled tungsten steel forging punch heads (#718096 / #4A5568)
    # - Copper steam accumulator tube on gauntlet spine
    # - Sky cyan (#38A0FF) pressure relief nozzle with soft steam puff
    # - Industrial brass reinforcement ribs (#FFD028)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Wrist Cuff & Forearm Bracer Sleeve (x: 84..94, y: 64..84)
    for wy in range(65, 84):
        for wx in range(84, 94):
            spec = max(0.0, 1.0 - abs(wy - 74.0) / 10.0)
            r_c = int(np.clip(43 * (0.85 + 0.35 * spec), 0, 255))
            g_c = int(np.clip(40 * (0.85 + 0.35 * spec), 0, 255))
            b_c = int(np.clip(54 * (0.85 + 0.35 * spec), 0, 255))
            weapon_img.putpixel((wx, wy), (r_c, g_c, b_c, 255))
    # Beveled brass wrist bands with steel rivets
    for wy in [66, 74, 82]:
        for wx in range(84, 94):
            weapon_img.putpixel((wx, wy), GOLD_BASE)
        wd.point((88, wy), fill=WHITE_SHINE)

    # 2. Main Armored Hand Gauntlet Box (x: 93..108, y: 64..84) - Heavy Crimson Enamel
    for y in range(64, 85):
        for x in range(93, 109):
            dx = (x - 100.0) / 8.0
            dy = (y - 74.0) / 10.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - ((x - 97.0)**2 + (y - 71.0)**2)**0.5 / 10.0)
                shine = max(0.0, 1.0 - ((x - 97.0)**2 + (y - 71.0)**2)**0.5 / 3.5)**2
                r_w = int(np.clip(230 * (0.85 + 0.25 * spec) + 35 * shine, 0, 255))
                g_w = int(np.clip(57 * (0.85 + 0.25 * spec) + 35 * shine, 0, 255))
                b_w = int(np.clip(70 * (0.85 + 0.25 * spec) + 35 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Gauntlet Central Gold Gear / Cross Reinforcement
    wd.ellipse([97, 71, 103, 77], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((100, 74), fill=WHITE_SHINE)

    # 3. Four Articulated Clenched Finger Knuckles (Striking Face at x: 108..118)
    knuckles = [
        (111.0, 66.0, 4.0, 2.5),  # Index
        (113.0, 71.5, 4.5, 2.5),  # Middle (protruding furthest)
        (113.0, 77.0, 4.5, 2.5),  # Ring
        (111.0, 82.5, 4.0, 2.5),  # Pinky
    ]
    for kcx, kcy, krx, kry in knuckles:
        for y in range(int(kcy - kry - 1), int(kcy + kry + 2)):
            for x in range(int(kcx - krx - 1), int(kcx + krx + 2)):
                if ((x - kcx) / krx)**2 + ((y - kcy) / kry)**2 <= 1.0:
                    spec = max(0.0, 1.0 - (x - (kcx - 1.0)) / (krx * 1.5))
                    r_k = int(np.clip(113 * (0.85 + 0.3 * spec), 0, 255))
                    g_k = int(np.clip(128 * (0.85 + 0.3 * spec), 0, 255))
                    b_k = int(np.clip(150 * (0.85 + 0.3 * spec), 0, 255))
                    weapon_img.putpixel((x, y), (r_k, g_k, b_k, 255))
        # Punching piston head cap & rivet
        wd.line([(int(kcx + krx - 1), int(kcy - 1)), (int(kcx + krx - 1), int(kcy + 1))], fill=STEEL_SHINE, width=1)
        wd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    # 4. Folded Armored Thumb Plate across lower front (x: 98..107, y: 79..85)
    wd.rounded_rectangle([98, 79, 107, 85], radius=2, fill=STEEL_BASE, outline=OUTLINE)
    wd.point((102, 82), fill=GOLD_BASE)

    # 5. Horizontal Pneumatic Steam Piston Actuator mounted on forearm top (x: 86..102, y: 60..64)
    for py in range(60, 65):
        for px in range(86, 103):
            spec = max(0.0, 1.0 - abs(py - 62.0) / 2.0)
            r_p = int(np.clip(217 * (0.85 + 0.3 * spec), 0, 255))
            g_p = int(np.clip(119 * (0.85 + 0.3 * spec), 0, 255))
            b_p = int(np.clip(6 * (0.85 + 0.3 * spec) + 30 * spec, 0, 255))
            weapon_img.putpixel((px, py), (r_p, g_p, b_p, 255))
    # Actuator front nozzle and cyan pressure valve
    wd.rectangle([101, 61, 105, 63], fill=SKY_BASE, outline=OUTLINE)
    wd.point((103, 62), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_gorilla_heavy_t_forged_key", key_img),
        ("back_curio", "curio_gorilla_twin_turbo_exhaust_chimney", curio_img),
        ("chassis", "chassis_gorilla_brass_heavy_default", chassis_img),
        ("head_unit", "head_gorilla_riveted_brow_crest", head_img),
        ("costume", "costume_gorilla_steam_forge_boiler_harness", costume_img),
        ("optic_core", "face_gorilla_dual_gauge_optic_lens", core_img),
        ("weapon", "weapon_gorilla_steam_forging_fist", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{GORILLA_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{GORILLA_PD_DIR}/winding_key/key_gorilla_heavy_t_forged_key.png", f"{KEY_DIR}/key_gorilla_heavy_t_forged_key.png")
    shutil.copyfile(f"{GORILLA_PD_DIR}/weapon/weapon_gorilla_steam_forging_fist.png", f"{WEAPON_DIR}/weapon_gorilla_steam_forging_fist.png")
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

    proof_comp = f"{GORILLA_PD_DIR}/proof_paperdoll_gorilla_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{GORILLA_PD_DIR}/proof_paperdoll_gorilla_magenta.png"
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

    strip_path = f"{GORILLA_PD_DIR}/proof_gorilla_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/gorilla_idle_hd.png)
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

        showcase_out = f"{showcase_dir}/gorilla_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL STEELARM GORILLA CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
