#!/usr/bin/env python3
"""
build_seahorse_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十三族 琉璃海馬 (The Crystal Seahorse, seahorse) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/CRYSTAL_SEAHORSE_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero fish scales/mucus/gills, stamped pressure-proof titanium hull plates,
  ivory white porcelain cheek/chest plates, trident crown cog visor, coiled manganese spring tail,
  trident coral brass winding key, dual propeller fins, abyssal prism astrolabe floating focus)
- references/art_direction.md & references/brand_assets.md:
  Dawson Day 258 Dopamine palette:
    Primary: High-Pressure Abyssal Cyan Enamel (#38A0FF)
    Secondary: Ivory White Porcelain Enamel (#FFFDF8)
    Accent: Dopamine Golden Trident Coral Brass Key & Cog Teeth (#FFD028)
    Detail: Deep-Sea Sapphire Twin Optical Core Lenses (#1C54B2)
    Fluorescent: Mint Turquoise Resonator Fins & Seal Rings (#2EC4B6)
    Highlight: Coral Pink Micro Pressure Valves & Terminals (#FF5E8A)
    Frame: Matte Titanium Pressure-Proof Frame (#7A8B99)
    Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
SEAHORSE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/seahorse"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Crystal Seahorse Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: High-Pressure Abyssal Cyan Enamel (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

# Secondary: Ivory White Porcelain Enamel Cheek & Chest Plates (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (225, 220, 212, 255)
IVORY_DARK    = (185, 180, 170, 255)

# Accent: Dopamine Golden Trident Coral Brass Key & Cog Teeth (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# Detail: Deep-Sea Sapphire Optical Core & Focus Crystal (#1C54B2)
SAPPHIRE_BASE  = (28, 84, 178, 255)
SAPPHIRE_LIGHT = (55, 130, 240, 255)
SAPPHIRE_SHINE = (160, 205, 255, 255)
SAPPHIRE_DARK  = (15, 45, 110, 255)

# Secondary Hull: Mint Turquoise Resonator Fins & Seal Rings (#2EC4B6)
MINT_BASE  = (46, 196, 182, 255)
MINT_LIGHT = (110, 230, 220, 255)
MINT_SHINE = (190, 255, 245, 255)
MINT_DARK  = (20, 145, 135, 255)
MINT_DEEP  = (10, 95, 88, 255)

# Warm Highlight: Coral Pink Micro Pressure Valves & Terminals (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

# Structure: Matte Titanium Pressure-Proof Frame (#7A8B99)
TITANIUM_LIGHT = (155, 172, 188, 255)
TITANIUM_BASE  = (122, 139, 153, 255)
TITANIUM_DARK  = (80, 95, 108, 255)
TITANIUM_DEEP  = (50, 60, 70, 255)

# Harness Leather / Canvas Straps (#8E522D)
CANVAS_BASE  = (142, 82, 45, 255)
CANVAS_LIGHT = (180, 112, 68, 255)
CANVAS_DARK  = (96, 52, 26, 255)

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
                                for rx, ry, r_rad in ignore_regions:
                                    if (nx - rx)**2 + (ny - ry)**2 <= r_rad**2:
                                        in_ignored = True
                                        break
                                if in_ignored:
                                    continue
                            points_to_outline.add((nx, ny))

    for px, py in points_to_outline:
        img.putpixel((px, py), outline_color)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL CRYSTAL SEAHORSE SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_seahorse_trident_coral_spire.png
    # Trident Coral-Crystal Brass Winding Key (三叉戟珊瑚晶簇黃銅發條鑰匙)
    # Features:
    # - Socket at upper-mid spine (63, 58)
    # - Polished brass shaft extending diagonally up-right to trident hub at (84, 26)
    # - Baroque trident handle stamped in dopamine gold (#FFD028)
    # - Center trident cavity holds deep-sea sapphire crystal (#1C54B2 / #38A0FF)
    # - Flanked by clockwork coral cog teeth branches
    # - Central coral pink pivot jewel (#FF5E8A) with brilliant specular glint
    # - STRICTLY transparent corners (0-ART29 compliance)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (63, 58) to (84, 26)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 63.0 + t * 21.0
        sy = 58.0 - t * 32.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (63, 58)
    kd.ellipse([59, 54, 67, 62], fill=GOLD_DARK, outline=OUTLINE)
    kd.ellipse([60, 55, 66, 61], fill=GOLD_BASE)
    kd.ellipse([62, 57, 64, 59], fill=CORAL_BASE)

    # 2. Trident Coral Hub & Handle at (84, 26)
    kcx, kcy = 84.0, 26.0

    # Trident central spire extending upwards to (84, 12)
    for ty in range(12, int(kcy) + 1):
        t_prog = (ty - 12) / (kcy - 12)
        half_w = 1.0 + t_prog * 2.5
        for x in range(int(kcx - half_w), int(kcx + half_w + 1)):
            dist_x = abs(x - kcx)
            spec = max(0.0, 1.0 - dist_x / half_w)
            r_sp = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
            g_sp = int(np.clip(208 * (0.85 + 0.2 * spec), 0, 255))
            b_sp = int(np.clip(40 * (0.85 + 0.5 * spec) + 50 * spec, 0, 255))
            key_img.putpixel((x, ty), (r_sp, g_sp, b_sp, 255))
    kd.point((int(kcx), 12), fill=WHITE_SHINE)

    # Trident Left Fork: curves from (76, 28) up to (73, 16)
    left_fork_pts = [(82, 30), (76, 26), (73, 20), (74, 16)]
    for i in range(len(left_fork_pts) - 1):
        p0 = left_fork_pts[i]
        p1 = left_fork_pts[i+1]
        for t in np.linspace(0.0, 1.0, 15):
            fx = p0[0] + t * (p1[0] - p0[0])
            fy = p0[1] + t * (p1[1] - p0[1])
            for d in [-1, 0, 1]:
                key_img.putpixel((int(fx + d), int(fy)), GOLD_BASE)
                key_img.putpixel((int(fx), int(fy + d)), GOLD_LIGHT)
    kd.point((74, 16), fill=WHITE_SHINE)

    # Trident Right Fork: curves from (86, 30) up to (95, 16)
    right_fork_pts = [(86, 30), (92, 26), (95, 20), (94, 16)]
    for i in range(len(right_fork_pts) - 1):
        p0 = right_fork_pts[i]
        p1 = right_fork_pts[i+1]
        for t in np.linspace(0.0, 1.0, 15):
            fx = p0[0] + t * (p1[0] - p0[0])
            fy = p0[1] + t * (p1[1] - p0[1])
            for d in [-1, 0, 1]:
                key_img.putpixel((int(fx + d), int(fy)), GOLD_BASE)
                key_img.putpixel((int(fx), int(fy + d)), GOLD_LIGHT)
    kd.point((94, 16), fill=WHITE_SHINE)

    # Clockwork coral branch teeth on outer forks
    coral_branches = [
        (72, 22, GOLD_LIGHT), (70, 24, CORAL_BASE),
        (96, 22, GOLD_LIGHT), (98, 24, CORAL_BASE),
        (80, 16, GOLD_BASE),  (88, 16, GOLD_BASE)
    ]
    for cbx, cby, c_col in coral_branches:
        kd.ellipse([cbx - 1, cby - 1, cbx + 1, cby + 1], fill=c_col)

    # Center oval bezel & sapphire crystal jewel at (84, 26)
    r_jewel = 4.8
    for y in range(int(kcy - r_jewel - 1), int(kcy + r_jewel + 2)):
        for x in range(int(kcx - r_jewel - 1), int(kcx + r_jewel + 2)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if dist <= r_jewel:
                spec = max(0.0, 1.0 - dist / r_jewel)
                shine = max(0.0, 1.0 - ((x - (kcx - 1.2))**2 + (y - (kcy - 1.2))**2)**0.5 / 2.0)**2
                r_j = int(np.clip(28 * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                g_j = int(np.clip(84 * (0.8 + 0.3 * spec) + 120 * shine, 0, 255))
                b_j = int(np.clip(178 * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                key_img.putpixel((x, y), (r_j, g_j, b_j, 255))

    kd.ellipse([int(kcx - r_jewel), int(kcy - r_jewel), int(kcx + r_jewel), int(kcy + r_jewel)],
               outline=GOLD_DARK, width=1)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    apply_clean_outline(key_img)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_seahorse_twin_propeller_fins.png
    # Twin Clockwork Propeller Fins (雙聯微型發條螺旋推進晶鰭)
    # Features:
    # - Originates along dorsal spine (50..54, 56..74)
    # - Dual-layer high-toughness mint turquoise silicone / crystal fins (#2EC4B6)
    # - Hydrofoil radiating fin ribs with brass hinges and micro exhaust nozzles (#FF5E8A)
    # - Micro bubbles / fluid exhaust particles venting behind
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Upper Dorsal Propeller Fin: sweeps from spine (52, 58) back to (32, 46)
    upper_fin_poly = [
        (52, 58),  # Hinge base
        (46, 52),
        (38, 48),
        (32, 46),  # Fin tip
        (34, 54),
        (40, 58),
        (48, 62),
        (52, 63)   # Lower base
    ]
    # Draw translucent textured mint fin body
    cd.polygon(upper_fin_poly, fill=MINT_BASE)
    # Highlight & gradient shading on upper fin
    for py in range(46, 64):
        for px in range(32, 53):
            if curio_img.getpixel((px, py))[3] > 0:
                dist_tip = ((px - 32)**2 + (py - 46)**2)**0.5
                spec = max(0.0, 1.0 - dist_tip / 24.0)
                r_f = int(np.clip(46 * (0.8 + 0.35 * spec), 0, 255))
                g_f = int(np.clip(196 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                b_f = int(np.clip(182 * (0.8 + 0.35 * spec) + 50 * spec, 0, 255))
                curio_img.putpixel((px, py), (r_f, g_f, b_f, 255))

    # Radiating hydrofoil ribs on upper fin
    for end_pt in [(33, 47), (35, 52), (39, 56)]:
        cd.line([(52, 60), end_pt], fill=MINT_SHINE, width=1)

    # 2. Lower Dorsal Propeller Fin: sweeps from spine (50, 66) back to (34, 66)
    lower_fin_poly = [
        (50, 66),  # Hinge base
        (44, 64),
        (36, 65),
        (34, 68),  # Tip
        (36, 73),
        (42, 75),
        (48, 74),
        (50, 72)
    ]
    cd.polygon(lower_fin_poly, fill=MINT_DARK)
    for py in range(64, 76):
        for px in range(34, 51):
            if curio_img.getpixel((px, py))[3] > 0:
                dist_tip = ((px - 34)**2 + (py - 68)**2)**0.5
                spec = max(0.0, 1.0 - dist_tip / 18.0)
                r_f = int(np.clip(20 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                g_f = int(np.clip(145 * (0.8 + 0.35 * spec) + 50 * spec, 0, 255))
                b_f = int(np.clip(135 * (0.8 + 0.35 * spec) + 60 * spec, 0, 255))
                curio_img.putpixel((px, py), (r_f, g_f, b_f, 255))

    # Ribs on lower fin
    for end_pt in [(35, 68), (38, 72)]:
        cd.line([(50, 70), end_pt], fill=MINT_LIGHT, width=1)

    # 3. Brass Hinges & Micro Hydraulic Nozzles at Spine attachment
    cd.ellipse([50, 58, 54, 62], fill=GOLD_BASE, outline=OUTLINE)
    cd.point((52, 60), fill=WHITE_SHINE)
    cd.ellipse([48, 67, 52, 71], fill=GOLD_BASE, outline=OUTLINE)
    cd.point((50, 69), fill=WHITE_SHINE)

    # Micro Coral Pink pressure valves
    cd.ellipse([49, 62, 53, 65], fill=CORAL_BASE)
    cd.ellipse([47, 71, 51, 74], fill=CORAL_BASE)

    # 4. Micro Stream / Air Bubble Droplets drifting behind fins
    bubble_coords = [
        (28, 48, 1.8), (24, 53, 1.4), (29, 60, 2.0),
        (26, 68, 1.5), (30, 72, 1.2)
    ]
    for bx, by, br in bubble_coords:
        cd.ellipse([int(bx - br), int(by - br), int(bx + br), int(by + br)],
                   fill=CYAN_LIGHT, outline=OUTLINE)
        cd.point((int(bx - 0.5), int(by - 0.5)), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_seahorse_abyssal_cyan_default.png
    # Features:
    # - 2.2 Chibi vertical S-curve seahorse toy posture
    # - Soft ground contact shadow centered at (64, 120), 48x16px
    # - Five-segment coiled manganese-steel spiral spring tail (下半身螺旋板簧尾)
    #   anchoring to ground with three micro hydraulic damping fin pads
    # - High-gloss Dopamine Cyan Enamel (#38A0FF) body hull with multi-tone depth
    # - Ivory White (#FFFDF8) enamel shock-absorbing belly plate & titanium anti-pressure ribs
    # - Ball-and-socket articulated titanium mechanical spine joints (#7A8B99)
    # - Left arm: gracefully curved forward fluid-guiding palm at (40, 76)
    # - Right arm: tucked grip hub ready to channel astrolabe at (78, 72)
    # - STRICT ZERO pixels in outer weapon zone (x >= 94) for 0-ART9 / 0-ART11
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow (48x16 ellipse at (64, 120))
    ch_d.ellipse([64 - 24, 120 - 7, 64 + 24, 120 + 7], fill=(31, 26, 58, 110))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.5))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Lower Grounding Hydraulic Fin Pads at base (y: 115..118)
    ground_pads = [
        (54, 116, 5.0, 2.5),  # Left pad
        (64, 117, 6.0, 2.8),  # Center pad
        (74, 116, 5.0, 2.5)   # Right pad
    ]
    for px, py, pw, ph in ground_pads:
        ch_d.ellipse([int(px - pw), int(py - ph), int(px + pw), int(py + ph)],
                     fill=TITANIUM_BASE, outline=OUTLINE)
        ch_d.ellipse([int(px - pw + 1), int(py - ph + 1), int(px + pw - 1), int(py + ph - 1)],
                     fill=TITANIUM_LIGHT)
        ch_d.point((int(px), int(py)), fill=WHITE_SHINE)

    # 3. Five-Segment Coiled Manganese-Steel Spiral Spring Tail
    # Elegant S-curve / spiral tail curling from pelvis (62, 88) down to base (64, 116)
    # Node centers along spiral:
    tail_spiral_nodes = [
        (62.0, 88.0, 9.0),   # Segment 1 (Pelvis base)
        (58.0, 96.0, 8.2),   # Segment 2 (Upper curve)
        (56.0, 104.0, 7.5),  # Segment 3 (Mid spiral)
        (60.0, 111.0, 6.8),  # Segment 4 (Lower curl)
        (65.0, 115.0, 6.0)   # Segment 5 (Terminal anchor)
    ]

    for idx, (tx, ty, trad) in enumerate(tail_spiral_nodes):
        for y in range(int(ty - trad - 2), int(ty + trad + 3)):
            for x in range(int(tx - trad - 2), int(tx + trad + 3)):
                dist = ((x - tx)**2 + (y - ty)**2)**0.5
                if dist <= trad:
                    spec = max(0.0, 1.0 - ((x - (tx - 2))**2 + (y - (ty - 2))**2)**0.5 / trad)
                    shine = max(0.0, 1.0 - ((x - (tx - 2))**2 + (y - (ty - 2))**2)**0.5 / 2.5)**2
                    edge_shade = max(0.0, (dist / trad - 0.5) / 0.5)

                    # High-gloss Cyan enamel with ivory belly rim
                    if x >= tx + trad * 0.3:
                        # Inner ventral curve has ivory white enamel
                        r_t = int(np.clip(255 * (0.85 + 0.2 * spec) - 30 * edge_shade + 20 * shine, 0, 255))
                        g_t = int(np.clip(253 * (0.85 + 0.2 * spec) - 30 * edge_shade + 20 * shine, 0, 255))
                        b_t = int(np.clip(248 * (0.85 + 0.2 * spec) - 30 * edge_shade + 20 * shine, 0, 255))
                    else:
                        r_t = int(np.clip(56 * (0.8 + 0.35 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                        g_t = int(np.clip(160 * (0.8 + 0.35 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                        b_t = int(np.clip(255 * (0.8 + 0.35 * spec) - 10 * edge_shade + 40 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

        # Ball joint & silicone damping ring between segments
        if idx < len(tail_spiral_nodes) - 1:
            nxt_x, nxt_y, _ = tail_spiral_nodes[idx + 1]
            mid_x = int(0.5 * (tx + nxt_x))
            mid_y = int(0.5 * (ty + nxt_y))
            ch_d.ellipse([mid_x - 3, mid_y - 2, mid_x + 3, mid_y + 2], fill=CORAL_BASE, outline=OUTLINE)
            ch_d.point((mid_x, mid_y), fill=CORAL_LIGHT)

    # 4. Torso Body Shell (x: 48..78, y: 56..90)
    cx_t, cy_t = 63.0, 72.0
    for y in range(56, 91):
        for x in range(48, 79):
            dx = (x - cx_t) / 14.5
            dy = (y - cy_t) / 17.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Ivory porcelain enamel shock-absorbing chest & belly center
                is_belly_plate = ((x - 63.0)**2 / 8.5**2 + (y - 73.0)**2 / 12.0**2 <= 1.0)
                if is_belly_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 25 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 25 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 25 * shine, 0, 255))
                else:
                    # Abyssal Cyan Enamel
                    r_t = int(np.clip(56 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_t = int(np.clip(160 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_t = int(np.clip(255 * (0.75 + 0.45 * spec) - 10 * edge_shade + 40 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Titanium horizontal anti-pressure ribs across belly (0-ART18 rich detailing)
    for ry in [66, 72, 78, 84]:
        for rx in range(56, 71):
            if chassis_img.getpixel((rx, ry))[3] > 0:
                chassis_img.putpixel((rx, ry), TITANIUM_BASE)
        ch_d.point((63, ry), fill=GOLD_BASE)

    # 5. Left Arm: graceful fluid-guiding palm at (40, 76)
    ch_d.line([(50, 68), (40, 76)], fill=CYAN_LIGHT, width=4)
    ch_d.ellipse([36, 73, 43, 80], fill=CYAN_BASE, outline=OUTLINE)
    ch_d.ellipse([38, 75, 41, 78], fill=IVORY_PRIMARY)
    ch_d.point((39, 76), fill=WHITE_SHINE)

    # 6. Right Arm & Grip Hub tucked at ribs at (78, 72)
    ch_d.line([(72, 68), (78, 72)], fill=CYAN_LIGHT, width=4)
    ch_d.ellipse([75, 70, 81, 76], fill=CYAN_BASE, outline=OUTLINE)
    ch_d.point((78, 73), fill=GOLD_BASE)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11 compliance)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_seahorse_crown_visor.png
    # Features:
    # - Stamped Quartz Crown Visor (沖壓高透石英水晶冠冕頂盔)
    # - Helmet Dome at (64, 42), rx=18.5, ry=15.5
    # - Cyan enamel dome with ivory porcelain cheek plates (#FFFDF8)
    # - Three-Crest Trident Crown Gear Crest (三叉王冠狀齒輪晶冠) at y: 14..28
    # - Stamped tubular suction nozzle snout (套筒式金屬吸水長吻) with brass adjustment rings
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Abyssal Cyan & Ivory Cheek Plates)
    for y in range(int(hcy - hry - 2), int(hcy + hry + 3)):
        for x in range(int(hcx - hrx - 2), int(hcx + hrx + 3)):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Ivory porcelain cheek plates at lower face
                is_cheek = (y >= 41 and abs(x - hcx) <= 15.0 and ((x - hcx)/14.0)**2 + ((y - 46)/9.0)**2 <= 1.0)
                if is_cheek:
                    r_h = int(np.clip(255 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    g_h = int(np.clip(253 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    b_h = int(np.clip(248 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                else:
                    r_h = int(np.clip(56 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_h = int(np.clip(160 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_h = int(np.clip(255 * (0.75 + 0.45 * spec) - 10 * edge_shade + 40 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Titanium Cheek Screws at (48, 46) and (80, 46)
    for sx, sy in [(48, 46), (80, 46)]:
        hd.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=TITANIUM_LIGHT, outline=OUTLINE)
        hd.point((sx, sy), fill=WHITE_SHINE)

    # 2. Tubular Suction Nozzle Snout at (64, 48..56)
    snout_poly = [
        (61, 47), (67, 47), (66, 55), (62, 55)
    ]
    hd.polygon(snout_poly, fill=TITANIUM_BASE, outline=OUTLINE)
    # Brass calibrated rings on snout
    hd.line([(61, 50), (67, 50)], fill=GOLD_BASE, width=1)
    hd.line([(62, 53), (66, 53)], fill=GOLD_BASE, width=1)
    # Suction tip port
    hd.ellipse([62, 54, 66, 57], fill=GOLD_DARK, outline=OUTLINE)
    hd.point((64, 55), fill=CORAL_BASE)

    # 3. Three-Crest Trident Crown Gear Crest (三叉王冠狀齒輪晶冠) at y: 14..28
    # Center crown spire at x=64, y: 14..27
    center_crown_pts = [(64, 14), (67, 24), (61, 24)]
    hd.polygon(center_crown_pts, fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 15), fill=WHITE_SHINE)

    # Left crown crest at (54, 20)
    left_crest_pts = [(53, 19), (57, 26), (50, 26)]
    hd.polygon(left_crest_pts, fill=GOLD_BASE, outline=OUTLINE)
    hd.point((53, 20), fill=WHITE_SHINE)

    # Right crown crest at (74, 20)
    right_crest_pts = [(75, 19), (78, 26), (71, 26)]
    hd.polygon(right_crest_pts, fill=GOLD_BASE, outline=OUTLINE)
    hd.point((75, 20), fill=WHITE_SHINE)

    # Crown headband across forehead at y: 26..29
    hd.rectangle([48, 26, 80, 29], fill=GOLD_BASE, outline=OUTLINE)
    for gx in [52, 58, 64, 70, 76]:
        hd.point((gx, 28), fill=CYAN_BASE)
        hd.point((gx, 27), fill=WHITE_SHINE)

    # 4. HOLLOW EYE SOCKETS (0-ART27 compliance)
    for ecx, ecy in eye_centers:
        hd.ellipse([ecx - 6, ecy - 6, ecx + 6, ecy + 6], outline=GOLD_BASE, width=1)
        hd.ellipse([ecx - 5, ecy - 5, ecx + 5, ecy + 5], outline=OUTLINE, width=1)
        for y in range(ecy - 4, ecy + 5):
            for x in range(ecx - 4, ecx + 5):
                if (x - ecx)**2 + (y - ecy)**2 <= 3.5**2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    ignore_eyes = [(ecx, ecy, 3.8) for ecx, ecy in eye_centers]
    apply_clean_outline(head_img, ignore_regions=ignore_eyes)

    # Re-verify eye centers strictly alpha = 0
    for ecx, ecy in eye_centers:
        for y in range(ecy - 3, ecy + 4):
            for x in range(ecx - 3, ecx + 4):
                if (x - ecx)**2 + (y - ecy)**2 <= 3.2**2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 30)
    # File: optic_core/optic_seahorse_ocean_sapphire.png
    # Features:
    # - Deep-Sea Sapphire Twin Optical Core Lenses (#1C54B2 / #38A0FF)
    # - Left Eye at (52, 40) & Right Eye at (76, 40)
    # - Concentric rangefinder reticle rings & crosshairs
    # - Fully opaque lens centers (alpha == 255, 0-ART27 compliant)
    # - Central Clockwork Heart Core Crystal at chest (64, 71)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in eye_centers:
        r_lens = 4.6
        # Brass clamp bezel
        c_d.ellipse([int(ex - r_lens - 1), int(ey - r_lens - 1), int(ex + r_lens + 1), int(ey + r_lens + 1)],
                    fill=GOLD_DARK, outline=OUTLINE)

        for y in range(int(ey - r_lens - 1), int(ey + r_lens + 2)):
            for x in range(int(ex - r_lens - 1), int(ex + r_lens + 2)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= r_lens:
                    spec = max(0.0, 1.0 - dist / r_lens)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.5))**2 + (y - (ey - 1.5))**2)**0.5 / 2.0)**2
                    # Concentric reticle ring
                    is_reticle = (abs(dist - 2.5) <= 0.4)
                    if is_reticle:
                        r_c, g_c, b_c = 195, 235, 255
                    else:
                        r_c = int(np.clip(28 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        g_c = int(np.clip(84 * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                        b_c = int(np.clip(178 * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        c_d.ellipse([int(ex - r_lens), int(ey - r_lens), int(ex + r_lens), int(ey + r_lens)],
                    outline=GOLD_BASE, width=1)
        # Reticle crosshair
        c_d.line([(int(ex - 1.5), int(ey)), (int(ex + 1.5), int(ey))], fill=CYAN_LIGHT, width=1)
        c_d.line([(int(ex), int(ey - 1.5)), (int(ex), int(ey + 1.5))], fill=CYAN_LIGHT, width=1)
        c_d.point((int(ex - 1), int(ey - 1)), fill=WHITE_SHINE)

    # Clockwork Heart Crystal Core at center chest (64, 71)
    hr_c = 4.5
    for y in range(int(71 - hr_c - 1), int(71 + hr_c + 2)):
        for x in range(int(64 - hr_c - 1), int(64 + hr_c + 2)):
            # Diamond facet shape: abs(x - 64) + abs(y - 71) <= 4.8
            manhattan = abs(x - 64) + abs(y - 71)
            if manhattan <= 4.8:
                spec = max(0.0, 1.0 - manhattan / 4.8)
                shine = max(0.0, 1.0 - ((x - 63)**2 + (y - 70)**2)**0.5 / 2.0)**2
                r_cr = int(np.clip(56 * (0.85 + 0.3 * spec) + 80 * shine, 0, 255))
                g_cr = int(np.clip(160 * (0.85 + 0.3 * spec) + 70 * shine, 0, 255))
                b_cr = int(np.clip(255 * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                core_img.putpixel((x, y), (r_cr, g_cr, b_cr, 255))

    # Brass retention claws holding the crystal
    c_d.polygon([(64, 65), (63, 67), (65, 67)], fill=GOLD_BASE)
    c_d.polygon([(64, 77), (63, 75), (65, 75)], fill=GOLD_BASE)
    c_d.polygon([(58, 71), (60, 70), (60, 72)], fill=GOLD_BASE)
    c_d.polygon([(70, 71), (68, 70), (68, 72)], fill=GOLD_BASE)
    c_d.point((63, 70), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_seahorse_abyssal_scholar_harness.png
    # Features:
    # - Abyssal Scholar Harness (海淵天宮星象學者輕甲工裝)
    # - Does NOT bake chassis underneath (0-ART26b compliant, y >= 92 is 0)
    # - Glazed Ivory White porcelain breastplate (#FFFDF8) with cyan titanium pauldrons (#38A0FF)
    # - Scholar leather/canvas harness straps (#8E522D)
    # - Clean aperture window at chest (64, 71) revealing Clockwork Heart crystal
    # - Waist utility belt with miniature brass pressure/depth gauge at (64, 82)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(58, 89):
        for x in range(48, 79):
            dx = (x - 63.0) / 14.5
            dy = (y - 73.0) / 14.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 59)**2 + (y - 68)**2)**0.5 / 14.0)

                # Center chest crystal aperture (keep hollow for optic_core crystal)
                is_core_aperture = (abs(x - 64) + abs(y - 71) <= 5.8)
                if is_core_aperture:
                    continue

                # Breastplate / Pauldron body
                is_pauldron = (abs(x - 63.0) >= 9.5 and y <= 68)
                if is_pauldron:
                    # Cyan titanium pauldron
                    r_a = int(np.clip(56 * (0.8 + 0.35 * spec), 0, 255))
                    g_a = int(np.clip(160 * (0.8 + 0.35 * spec), 0, 255))
                    b_a = int(np.clip(255 * (0.8 + 0.35 * spec), 0, 255))
                else:
                    # Ivory white glazed scholar breastplate
                    r_a = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                    g_a = int(np.clip(253 * (0.85 + 0.25 * spec), 0, 255))
                    b_a = int(np.clip(248 * (0.85 + 0.25 * spec), 0, 255))

                costume_img.putpixel((x, y), (r_a, g_a, b_a, 255))

    # Canvas shoulder harness straps with brass buckles
    strap_pts = [(52, 60), (54, 65), (74, 60), (72, 65)]
    for sx, sy in strap_pts:
        cos_d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=CANVAS_BASE)
        cos_d.point((sx, sy), fill=GOLD_BASE)

    # Gold rim around the chest crystal aperture
    cos_d.ellipse([64 - 6, 71 - 6, 64 + 6, 71 + 6], outline=GOLD_BASE, width=1)

    # Waist utility belt with miniature brass depth gauge at (64, 82)
    cos_d.rectangle([50, 80, 76, 84], fill=CANVAS_DARK, outline=OUTLINE)
    # Depth gauge dial
    cos_d.ellipse([60, 78, 68, 86], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([61, 79, 67, 85], fill=IVORY_PRIMARY)
    # Coral needle & center pivot
    cos_d.line([(64, 82), (66, 80)], fill=CORAL_BASE, width=1)
    cos_d.point((64, 82), fill=OUTLINE)
    cos_d.point((62, 80), fill=WHITE_SHINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Top Layer)
    # File: weapon/weapon_seahorse_abyssal_prism_astrolabe.png
    # Features:
    # - Abyssal Prism Astrolabe (【深海靈晶浮空星盤 / 琉璃棱鏡核心】)
    # - Right-hand single wielded floating focus (0-MKT7 compliant)
    # - Levitated astrolabe centered at (98, 66)
    # - Three concentric calibrated titanium & brass gimbal rings
    # - Central octahedral high-refractive sapphire crystal (#1C54B2 / #38A0FF)
    # - Light channeling rays / mana energy motes orbiting the gimbal rings
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    acx, acy = 98.0, 66.0

    # 1. Outer Gimbal Ring: Brass with Astrological Scale Ticks (radius 14.5)
    r_out = 14.5
    for y in range(int(acy - r_out - 2), int(acy + r_out + 3)):
        for x in range(int(acx - r_out - 2), int(acx + r_out + 3)):
            dist = ((x - acx)**2 + (y - acy)**2)**0.5
            if r_out - 1.8 <= dist <= r_out + 0.8:
                angle = np.arctan2(y - acy, x - acx)
                spec = max(0.0, 1.0 - ((x - (acx - 4))**2 + (y - (acy - 4))**2)**0.5 / 16.0)
                shine = max(0.0, np.cos(angle - 2.35))**2
                r_w = int(np.clip(255 * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                g_w = int(np.clip(208 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Outer Astrological scale ticks
    for deg in range(0, 360, 30):
        rad = np.radians(deg)
        tx0 = int(acx + (r_out - 1.5) * np.cos(rad))
        ty0 = int(acy + (r_out - 1.5) * np.sin(rad))
        tx1 = int(acx + (r_out + 1.2) * np.cos(rad))
        ty1 = int(acy + (r_out + 1.2) * np.sin(rad))
        wd.line([(tx0, ty0), (tx1, ty1)], fill=GOLD_LIGHT, width=1)

    # 2. Middle Gimbal Ring: Titanium Steel Inclined Ring (radius 10.0)
    # Elliptical projection representing tilted ring
    for deg in range(0, 360, 4):
        rad = np.radians(deg)
        rx = acx + 10.0 * np.cos(rad)
        ry = acy + 6.5 * np.sin(rad)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            weapon_img.putpixel((int(rx + dx), int(ry + dy)), TITANIUM_BASE)
        weapon_img.putpixel((int(rx), int(ry)), TITANIUM_LIGHT)

    # 3. Inner Gimbal Ring: Cyan Enamel Counter-Tilted Ring (radius 6.5)
    for deg in range(0, 360, 5):
        rad = np.radians(deg)
        rx = acx + 4.5 * np.cos(rad)
        ry = acy + 6.5 * np.sin(rad)
        weapon_img.putpixel((int(rx), int(ry)), CYAN_LIGHT)

    # 4. Central Octahedral High-Refractive Sapphire Crystal
    # Diamond / octahedron shape
    r_crystal = 4.8
    for y in range(int(acy - r_crystal - 2), int(acy + r_crystal + 3)):
        for x in range(int(acx - r_crystal - 2), int(acx + r_crystal + 3)):
            manhattan = abs(x - acx) + abs(y - acy)
            if manhattan <= r_crystal:
                # Facet shading
                dx = x - acx
                dy = y - acy
                if dx <= 0 and dy <= 0:
                    # Top-left facet: high specular shine
                    spec = 1.0
                    r_k, g_k, b_k = 195, 235, 255
                elif dx > 0 and dy <= 0:
                    # Top-right facet: cyan light
                    spec = 0.7
                    r_k, g_k, b_k = 56, 160, 255
                elif dx <= 0 and dy > 0:
                    # Bottom-left facet: deep sapphire
                    spec = 0.5
                    r_k, g_k, b_k = 28, 84, 178
                else:
                    # Bottom-right facet: deep shade
                    spec = 0.3
                    r_k, g_k, b_k = 15, 45, 110
                weapon_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Crisp white glint on crystal apex
    wd.point((int(acx - 1), int(acy - 1)), fill=WHITE_SHINE)
    wd.point((int(acx), int(acy - 1)), fill=WHITE_SHINE)

    # 5. Energy Channeling Conduit from Hand (80, 72) to Astrolabe (98, 66)
    for t in np.linspace(0.0, 1.0, 20):
        lx = 80.0 + t * 18.0
        ly = 72.0 - t * 6.0 + np.sin(t * np.pi) * 2.0
        if 0 <= int(lx) < W and 0 <= int(ly) < H:
            weapon_img.putpixel((int(lx), int(ly)), CYAN_LIGHT)
    # Stardust energy motes around astrolabe
    star_motes = [(98, 48), (114, 66), (98, 84), (84, 66), (108, 54), (88, 76)]
    for mx, my in star_motes:
        wd.point((mx, my), fill=CYAN_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ASSETS (128x128 and 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_seahorse_trident_coral_spire", key_img),
        ("back_curio", "curio_seahorse_twin_propeller_fins", curio_img),
        ("chassis", "chassis_seahorse_abyssal_cyan_default", chassis_img),
        ("head_unit", "head_seahorse_crown_visor", head_img),
        ("optic_core", "optic_seahorse_ocean_sapphire", core_img),
        ("costume", "costume_seahorse_abyssal_scholar_harness", costume_img),
        ("weapon", "weapon_seahorse_abyssal_prism_astrolabe", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{SEAHORSE_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)

        # 128x128
        dst_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(dst_128)

        # 512x512 LANCZOS
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{slot_dir}/{item_id}_512.png"
        img_512.save(dst_512)
        print(f"  ✓ Saved {slot}: {item_id}.png (128x128 & 512x512 LANCZOS)")

    # Universal Key & Weapon copies
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_seahorse_trident_coral_spire.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_seahorse_abyssal_prism_astrolabe.png")
    print("  ✓ Saved universal key & weapon copies")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOF IMAGES
    # Layers Z order:
    # 1. winding_key (Z: 5)
    # 2. back_curio  (Z: 8)
    # 3. chassis     (Z: 10)
    # 4. head_unit   (Z: 20)
    # 5. costume     (Z: 25)
    # 6. optic_core  (Z: 30)
    # 7. weapon      (Z: 40)
    # ─────────────────────────────────────────────────────────────
    comp_exact = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_img in [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]:
        comp_exact.alpha_composite(s_img)

    comp_path = f"{SEAHORSE_PD_DIR}/proof_paperdoll_seahorse_composite.png"
    comp_exact.save(comp_path)
    print("  ✓ Composite saved:", comp_path)

    # Magenta proof (proof_paperdoll_seahorse_magenta.png)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(comp_exact)
    mag_path = f"{SEAHORSE_PD_DIR}/proof_paperdoll_seahorse_magenta.png"
    magenta_bg.save(mag_path)
    print("  ✓ Magenta proof saved:", mag_path)

    # 7 slices proof (proof_seahorse_all_7_slices.png)
    strip_w = W * 8
    strip = Image.new("RGBA", (strip_w, H), (240, 240, 245, 255))
    slice_list = [
        ("KEY", key_img),
        ("CURIO", curio_img),
        ("CHASSIS", chassis_img),
        ("HEAD", head_img),
        ("COSTUME", costume_img),
        ("OPTIC", core_img),
        ("WEAPON", weapon_img),
        ("COMP", comp_exact)
    ]
    for idx, (label_txt, sl_img) in enumerate(slice_list):
        px = idx * W
        s_draw = ImageDraw.Draw(strip)
        s_draw.rectangle([px, 0, px + W - 1, H - 1], outline=(200, 200, 210, 255))
        s_draw.text((px + 4, 4), label_txt, fill=(60, 60, 80, 255))
        strip.alpha_composite(sl_img, (px, 0))

    strip_path = f"{SEAHORSE_PD_DIR}/proof_seahorse_all_7_slices.png"
    strip.save(strip_path)
    print("  ✓ 7 Slices Proof saved:", strip_path)

    # SHOWCASE HD (game/assets/sprites/player/showcase/seahorse_idle_hd.png)
    showcase_dir = f"{REPO_ROOT}/game/assets/sprites/player/showcase"
    os.makedirs(showcase_dir, exist_ok=True)
    comp_512 = comp_exact.resize((512, 512), Image.Resampling.LANCZOS)
    c_bbox = comp_512.getbbox()
    if c_bbox:
        char_crop = comp_512.crop(c_bbox)
        target_h = int(1200 * 0.76)
        scale_sc = target_h / char_crop.height
        sc_w = int(char_crop.width * scale_sc)
        sc_h = target_h
        scaled_showcase = char_crop.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

        showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_paste_x = (800 - sc_w) // 2
        sc_paste_y = (1200 - sc_h) // 2 - 20

        # Ground shadow in showcase
        sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_sh_draw = ImageDraw.Draw(sc_shadow)
        sc_sh_draw.ellipse([sc_paste_x + sc_w//2 - 140, sc_paste_y + sc_h - 20,
                            sc_paste_x + sc_w//2 + 140, sc_paste_y + sc_h + 30], fill=(31, 26, 58, 90))
        sc_shadow = sc_shadow.filter(ImageFilter.GaussianBlur(8.0))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))
        showcase_dst = f"{showcase_dir}/seahorse_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
