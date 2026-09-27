#!/usr/bin/env python3
"""
build_cat_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Umbral Cat (幽影貓 / The Umbral Cat) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/UMBRAL_CAT_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero cat flesh, cold-rolled obsidian steel chassis, stamped brass acoustic ears, silicone pads, tungsten spring whiskers, crescent twin-ring gold key, segmented gyro-tail)
- references/art_direction.md (Dopamine high-saturation palette: Obsidian #2B2630, Ivory #FFFDF8, Brass Gold #FFD028, Mint Green #4ED86A, Warm Orange #FFA010, Outline #1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
CAT_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/cat"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Umbral Cat Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Cold-rolled Obsidian Steel (#2B2630)
OBSIDIAN_BASE  = (43, 38, 48, 255)
OBSIDIAN_LIGHT = (76, 68, 86, 255)
OBSIDIAN_SHINE = (112, 102, 128, 255)
OBSIDIAN_DARK  = (24, 21, 29, 255)
OBSIDIAN_DEEP  = (16, 14, 20, 255)

# Secondary: Ivory White Enamel (#FFFDF8)
IVORY_PRIMARY  = (255, 253, 248, 255)
IVORY_LIGHT    = (255, 255, 255, 255)
IVORY_SHADE    = (222, 218, 210, 255)
IVORY_DARK     = (185, 180, 172, 255)

# Accent: Crescent Key & Acoustic Brass Gold (#FFD028 / #D4A017)
BRASS_GOLD     = (255, 208, 40, 255)
BRASS_LIGHT    = (255, 235, 115, 255)
BRASS_SHINE    = (255, 250, 185, 255)
BRASS_DARK     = (195, 145, 18, 255)
BRASS_DEEP     = (130, 90, 10, 255)

# Detail: Mint Aurora Night-Vision Green (#4ED86A)
MINT_GREEN     = (78, 216, 106, 255)
MINT_LIGHT     = (140, 240, 165, 255)
MINT_SHINE     = (210, 255, 225, 255)
MINT_DARK      = (36, 140, 62, 255)

# Warm Highlight: Warm Orange Rivets & Accents (#FFA010)
ORANGE_BASE    = (255, 160, 16, 255)
ORANGE_LIGHT   = (255, 195, 80, 255)
ORANGE_DARK    = (195, 110, 10, 255)

# Tungsten Whiskers, Springs & Steel Wire
STEEL_LIGHT    = (195, 205, 220, 255)
STEEL_MID      = (130, 142, 160, 255)
STEEL_DARK     = (70, 78, 92, 255)

# Engineering Silicone Pads (#202026)
SILICONE_BASE  = (32, 32, 38, 255)
SILICONE_LIGHT = (55, 55, 65, 255)

WHITE_SHINE    = (255, 255, 255, 255)


def apply_clean_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=80, ignore_regions=None) -> None:
    """Safe, non-recursive, snapshot-based 1px outline pass.
    Prevents flood-fill / propagation bugs that create rectangular black artifact blocks.
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
    print("=== BUILDING 100% MODULAR CANONICAL UMBRAL CAT SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_cat_crescent_twin_ring_gold.png
    # Crescent Twin-Ring Brass Wind-up Key (新月夜行雙環黃銅發條鑰匙)
    # Socket at upper spine (64, 64)
    # Key shaft extends up and right to crescent center at (88, 34)
    # Outer crescent blade with inner counter-rotating differential gear
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 64) to (88, 34)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 64.0 + t * 24.0
        sy = 64.0 - t * 30.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 64)
    kd.ellipse([60, 60, 68, 68], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([61, 61, 67, 67], fill=BRASS_GOLD)

    # 2. Crescent Twin-Ring Head at (88, 34)
    kcx, kcy = 88.0, 34.0
    r_outer = 14.5
    r_inner_cut = 11.2
    cut_offset_x = 3.2
    cut_offset_y = 3.0

    # Draw Crescent Outer Blade
    for y in range(int(kcy - r_outer - 4), int(kcy + r_outer + 5)):
        for x in range(int(kcx - r_outer - 4), int(kcx + r_outer + 5)):
            dx = x - kcx
            dy = y - kcy
            dist_sq = dx**2 + dy**2
            if dist_sq <= r_outer**2:
                # Cutout inner circle shifted to create crescent moon shape
                dx_cut = x - (kcx + cut_offset_x)
                dy_cut = y - (kcy + cut_offset_y)
                dist_cut_sq = dx_cut**2 + dy_cut**2
                if dist_cut_sq > r_inner_cut**2:
                    spec = max(0.0, 1.0 - ((x - (kcx - 5))**2 + (y - (kcy - 5))**2)**0.5 / 15.0)
                    shine = max(0.0, 1.0 - ((x - (kcx - 6))**2 + (y - (kcy - 6))**2)**0.5 / 5.0)**2
                    r_k = int(np.clip(255 * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                    g_k = int(np.clip(208 * (0.85 + 0.2 * spec) + 45 * shine, 0, 255))
                    b_k = int(np.clip(40 * (0.85 + 0.2 * spec) + 70 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Inner Differential Gear (Twin Ring) at (88, 34)
    r_gear = 7.5
    for y in range(int(kcy - r_gear - 3), int(kcy + r_gear + 4)):
        for x in range(int(kcx - r_gear - 3), int(kcx + r_gear + 4)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= r_gear:
                angle = np.arctan2(dy, dx)
                cogs = np.cos(6.0 * angle)
                cog_bound = r_gear - 1.5 + 1.5 * max(0.0, cogs)
                if dist <= cog_bound and dist >= 2.5:
                    spec = max(0.0, 1.0 - dist / r_gear)
                    r_g = int(np.clip(212 + 40 * spec, 0, 255))
                    g_g = int(np.clip(160 + 40 * spec, 0, 255))
                    b_g = int(np.clip(23 + 60 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_g, g_g, b_g, 255))

    # Central Hub Rivet with Orange Accent
    kd.ellipse([int(kcx - 2.5), int(kcy - 2.5), int(kcx + 2.5), int(kcy + 2.5)], fill=ORANGE_BASE, outline=OUTLINE)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    # Safe Outline Pass
    apply_clean_outline(key_img)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Tail Layer)
    # File: back_curio/curio_cat_segmented_gyro_tail.png
    # Nine-Segment Coaxial Balancing Gyro-Tail (九節同軸平衡發條鋼索尾)
    # Extends from spine base (50, 84) upward-left in elegant S-curve to (28, 46)
    # 9 brass rotors strung along flexible tungsten spring wire
    # Tip features precision dual-cone brass Gyro Balance Bob with orange belt
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Flexible Tungsten Steel Core Wire (S-curve spline)
    def bezier_curve(p0, p1, p2, p3, num_pts=60):
        pts = []
        for t in np.linspace(0.0, 1.0, num_pts):
            x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
            pts.append((x, y))
        return pts

    curve_pts = bezier_curve((50.0, 84.0), (36.0, 78.0), (26.0, 62.0), (28.0, 46.0), num_pts=80)

    # Draw core steel wire
    for i in range(len(curve_pts) - 1):
        x0, y0 = curve_pts[i]
        x1, y1 = curve_pts[i+1]
        cd.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=STEEL_LIGHT, width=2)
        cd.line([(int(x0)-1, int(y0)), (int(x1)-1, int(y1))], fill=OUTLINE, width=1)
        cd.line([(int(x0)+1, int(y0)), (int(x1)+1, int(y1))], fill=OUTLINE, width=1)

    # 2. 9 Coaxial Stamped Brass Rotors along tail curve
    t_rotors = np.linspace(0.1, 0.88, 9)
    rotor_indices = [int(t * (len(curve_pts) - 1)) for t in t_rotors]

    for idx in rotor_indices:
        rx_c, ry_c = curve_pts[idx]
        progress = idx / (len(curve_pts) - 1)
        r_rot = 4.0 - 1.2 * progress
        p_prev = curve_pts[max(0, idx - 2)]
        p_next = curve_pts[min(len(curve_pts) - 1, idx + 2)]
        tangent_angle = np.arctan2(p_next[1] - p_prev[1], p_next[0] - p_prev[0])
        normal_angle = tangent_angle + np.pi / 2.0

        for r_step in np.linspace(-r_rot, r_rot, 7):
            px = rx_c + r_step * np.cos(normal_angle)
            py = ry_c + r_step * np.sin(normal_angle)
            spec = max(0.0, 1.0 - abs(r_step) / r_rot)
            r_c = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
            g_c = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
            b_c = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
            cd.ellipse([int(px - 1), int(py - 1), int(px + 1), int(py + 1)], fill=(r_c, g_c, b_c, 255))

        cd.ellipse([int(rx_c - r_rot - 0.5), int(ry_c - r_rot - 0.5),
                    int(rx_c + r_rot + 0.5), int(ry_c + r_rot + 0.5)], outline=OUTLINE, width=1)

    # 3. Tip: Gyro Balance Bob at (28, 46)
    tbx, tby = 28.0, 46.0
    r_bob = 6.0
    for y in range(int(tby - r_bob - 2), int(tby + r_bob + 3)):
        for x in range(int(tbx - r_bob - 2), int(tbx + r_bob + 3)):
            dx = x - tbx
            dy = y - tby
            dist_profile = abs(dx) * 1.1 + abs(dy) * 0.95
            if dist_profile <= r_bob:
                spec = max(0.0, 1.0 - ((x - (tbx - 2))**2 + (y - (tby - 2))**2)**0.5 / (r_bob * 1.2))
                shine = max(0.0, 1.0 - ((x - (tbx - 2))**2 + (y - (tby - 2))**2)**0.5 / 2.5)**2
                if abs(dy) <= 1:
                    r_b = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    g_b = int(np.clip(160 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    b_b = int(np.clip(16 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                else:
                    r_b = int(np.clip(255 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                    g_b = int(np.clip(208 * (0.85 + 0.25 * spec) + 45 * shine, 0, 255))
                    b_b = int(np.clip(40 * (0.85 + 0.25 * spec) + 70 * shine, 0, 255))
                curio_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    cd.polygon([(int(tbx), int(tby - r_bob)), (int(tbx + r_bob * 0.9), int(tby)),
                (int(tbx), int(tby + r_bob)), (int(tbx - r_bob * 0.9), int(tby))], outline=OUTLINE)
    cd.line([(int(tbx), int(tby + r_bob)), (int(tbx), int(tby + r_bob + 3))], fill=STEEL_LIGHT, width=1)
    cd.point((int(tbx), int(tby + r_bob + 3)), fill=OUTLINE)
    cd.point((int(tbx - 1), int(tby - 2)), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_cat_obsidian_steel_default.png
    # Features:
    # - Agile Prowling Cat Chibi posture
    # - Soft ground contact shadow at (64, 116)
    # - 4 articulated mechanical limbs with silicone foot pads (#202026) & tungsten claws
    # - Cold-rolled Obsidian Steel (#2B2630) plates with rich metallic highlights
    # - Ivory White (#FFFDF8) enamel chest plate with micro core mint glow
    # - Left hand touch ground balance at (38, 92)
    # - Right hand tucked at side ribs at (82, 74)
    # - STRICTLY ZERO weapon baked in (0-ART9/0-ART11: x >= 95 is STRICTLY 0)
    # - Multi-tone depth with unique colors >= 20 (0-ART18)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 30, 116 - 4, 64 + 30, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Silicone Foot Pads & Tungsten Claws
    feet_pos = [(44.0, 113.0), (58.0, 113.0), (72.0, 113.0), (84.0, 113.0)]
    for fcx, fcy in feet_pos:
        ch_d.ellipse([int(fcx - 5), int(fcy - 1), int(fcx + 5), int(fcy + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(fcx - 3), int(fcy), int(fcx + 3), int(fcy + 2)], fill=SILICONE_LIGHT)
        for c_dx in [-3, 0, 3]:
            ch_d.line([(int(fcx + c_dx), int(fcy + 2)), (int(fcx + c_dx), int(fcy + 4))], fill=STEEL_LIGHT, width=1)
            ch_d.point((int(fcx + c_dx), int(fcy + 4)), fill=OUTLINE)

    # 3. Articulated Legs
    leg_paths = [
        ((44.0, 113.0), (48.0, 86.0)),
        ((58.0, 113.0), (60.0, 86.0)),
        ((72.0, 113.0), (70.0, 86.0)),
        ((84.0, 113.0), (78.0, 86.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 28):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-3, 4):
                if abs(dx) <= 3:
                    spec = max(0.0, 1.0 - abs(dx) / 3.0)
                    r_l = int(np.clip(43 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
                    g_l = int(np.clip(38 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
                    b_l = int(np.clip(48 * (0.8 + 0.4 * spec) + 40 * spec, 0, 255))
                    chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 2, mid_y - 2, mid_x + 2, mid_y + 2], fill=ORANGE_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=BRASS_SHINE)

    # 4. Torso Body Shell (x: 42..86, y: 56..96)
    cx_t, cy_t = 63.0, 76.0
    for y in range(56, 97):
        for x in range(42, 87):
            dx = (x - cx_t) / 21.0
            dy = (y - cy_t) / 19.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 19.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                is_chest_plate = ((x - 62.0)**2 / 9.0**2 + (y - 74.0)**2 / 9.5**2 <= 1.0)
                if is_chest_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    r_t = int(np.clip(43 * (0.75 + 0.5 * spec) - 20 * edge_shade + 55 * shine, 0, 255))
                    g_t = int(np.clip(38 * (0.75 + 0.5 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    b_t = int(np.clip(48 * (0.75 + 0.5 * spec) - 20 * edge_shade + 65 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    ch_d.arc([44, 58, 82, 94], start=30, end=150, fill=OBSIDIAN_DEEP, width=1)
    ch_d.line([(52, 70), (52, 80)], fill=OUTLINE, width=1)
    ch_d.line([(72, 70), (72, 80)], fill=OUTLINE, width=1)
    ch_d.ellipse([60, 71, 66, 77], fill=MINT_DARK, outline=OUTLINE)
    ch_d.ellipse([61, 72, 65, 76], fill=MINT_GREEN)
    ch_d.point((62, 73), fill=MINT_SHINE)

    # 5. Left Arm & Claw
    ch_d.line([(48, 74), (40, 88)], fill=OBSIDIAN_LIGHT, width=3)
    ch_d.ellipse([37, 86, 43, 92], fill=OBSIDIAN_BASE, outline=OUTLINE)
    ch_d.point((40, 89), fill=BRASS_GOLD)

    # 6. Right Arm & Claw (tucked at ribs)
    ch_d.line([(74, 72), (83, 75)], fill=OBSIDIAN_LIGHT, width=3)
    ch_d.ellipse([80, 73, 86, 79], fill=OBSIDIAN_BASE, outline=OUTLINE)
    ch_d.point((83, 76), fill=ORANGE_BASE)

    # Safe Outline Pass for chassis
    apply_clean_outline(chassis_img)

    # Ensure strictly zero pixels at x >= 95
    for y in range(H):
        for x in range(95, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_cat_brass_acoustic_ears.png
    # Features:
    # - Spherical Cold-rolled Obsidian Steel skull centered at (64, 44), rx=18, ry=15
    # - Ivory White (#FFFDF8) enamel muzzle and cheek plates with fine panel seams
    # - Stamped Brass Folding Acoustic Ears (立耳!) at (42..54, 14..32) and (74..86, 14..32)
    # - 6 micro tungsten spring whiskers extending from cheeks
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # - Brass ocular rings with deep socket shading around eye perimeters
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Obsidian Steel & Ivory Muzzle)
    for y in range(int(hcy - hry - 2), int(hcy + hry + 3)):
        for x in range(int(hcx - hrx - 2), int(hcx + hrx + 3)):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 5.5)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                is_muzzle = (y >= 43 and abs(x - hcx) <= 15.0 and ((x - hcx)/14.0)**2 + ((y - 48)/10.0)**2 <= 1.0)
                if is_muzzle:
                    r_h = int(np.clip(255 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    g_h = int(np.clip(253 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    b_h = int(np.clip(248 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                else:
                    r_h = int(np.clip(43 * (0.75 + 0.5 * spec) - 20 * edge_shade + 55 * shine, 0, 255))
                    g_h = int(np.clip(38 * (0.75 + 0.5 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    b_h = int(np.clip(48 * (0.75 + 0.5 * spec) - 20 * edge_shade + 65 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Metallic black nose & mouth seam
    hd.polygon([(62, 47), (66, 47), (64, 49)], fill=OUTLINE)
    hd.line([(64, 49), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([60, 50, 64, 54], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 50, 68, 54], start=0, end=180, fill=OUTLINE, width=1)

    # 2. Stamped Brass Acoustic Folding Ears (Upright cat ears!)
    ear_triangles = [
        ([(48, 33), (41, 14), (56, 31)], True),
        ([(72, 31), (87, 14), (80, 33)], False)
    ]
    for ear_pts, is_left in ear_triangles:
        hd.polygon(ear_pts, fill=BRASS_GOLD, outline=OUTLINE)
        if is_left:
            hd.polygon([(47, 30), (43, 17), (53, 29)], fill=BRASS_DARK, outline=OUTLINE)
            hd.ellipse([48, 30, 52, 34], fill=ORANGE_BASE, outline=OUTLINE)
            hd.point((50, 32), fill=BRASS_SHINE)
        else:
            hd.polygon([(81, 30), (85, 17), (75, 29)], fill=BRASS_DARK, outline=OUTLINE)
            hd.ellipse([76, 30, 80, 34], fill=ORANGE_BASE, outline=OUTLINE)
            hd.point((78, 32), fill=BRASS_SHINE)

    # 3. 6 Micro Tungsten Spring Whiskers
    whisker_lines = [
        ([(47, 46), (32, 43)], [(46, 48), (30, 48)], [(47, 50), (33, 53)]),
        ([(81, 46), (96, 43)], [(82, 48), (98, 48)], [(81, 50), (95, 53)])
    ]
    for w_group in whisker_lines:
        for w_pts in w_group:
            hd.line(w_pts, fill=STEEL_LIGHT, width=1)

    # 4. HOLLOW EYE SOCKETS (0-ART27 compliance)
    for ecx, ecy in eye_centers:
        hd.ellipse([ecx - 6, ecy - 6, ecx + 6, ecy + 6], outline=BRASS_GOLD, width=1)
        hd.ellipse([ecx - 5, ecy - 5, ecx + 5, ecy + 5], outline=OUTLINE, width=1)
        for y in range(ecy - 4, ecy + 5):
            for x in range(ecx - 4, ecx + 5):
                if (x - ecx)**2 + (y - ecy)**2 <= 3.5**2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    # Safe Outline Pass for head unit (ignore hollow eye socket centers)
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
    # File: optic_core/face_cat_slit_optic_emerald.png
    # Features:
    # - Dual Emerald Quartz Night-Vision Lenses at (52, 40) and (76, 40)
    # - Mint Green (#4ED86A) glowing annular rings with rich depth
    # - Vertical Night-Prowl Slit Pupils (black slit)
    # - White specular quartz glint at top-left of each lens
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ecx, ecy in eye_centers:
        r_lens = 4.2
        for y in range(int(ecy - r_lens - 2), int(ecy + r_lens + 3)):
            for x in range(int(ecx - r_lens - 2), int(ecx + r_lens + 3)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    spec = max(0.0, 1.0 - dist / r_lens)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.5))**2 + (y - (ecy - 1.5))**2)**0.5 / 2.0)**2
                    is_slit = (abs(x - ecx) <= 0.8 and abs(y - ecy) <= 3.2)
                    if is_slit:
                        r_c, g_c, b_c = 18, 14, 25
                    else:
                        r_c = int(np.clip(78 * (0.8 + 0.3 * spec) + 55 * shine, 0, 255))
                        g_c = int(np.clip(216 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        b_c = int(np.clip(106 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        c_d.ellipse([int(ecx - r_lens), int(ecy - r_lens), int(ecx + r_lens), int(ecy + r_lens)],
                    outline=OUTLINE, width=1)
        c_d.point((int(ecx - 1), int(ecy - 1)), fill=WHITE_SHINE)
        c_d.point((int(ecx), int(ecy - 2)), fill=MINT_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_cat_skyspire_prowler_vest.png
    # Features:
    # - Skyspire Prowler Tight Work Vest (天街巡夜緊身工裝背心)
    # - Dark Navy/Charcoal micro-weave canvas (x: 48..78, y: 58..88)
    # - Dual crossed leather harness straps with brass gear buckles (#FFD028)
    # - Warm Orange (#FFA010) pressure release studs along front placket
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
                is_strap = (abs((x - 63.0) - (y - 73.0)) <= 2.2 or abs((x - 63.0) + (y - 73.0)) <= 2.2)
                if is_strap:
                    r_v = int(np.clip(65 * (0.8 + 0.3 * spec), 0, 255))
                    g_v = int(np.clip(52 * (0.8 + 0.3 * spec), 0, 255))
                    b_v = int(np.clip(42 * (0.8 + 0.3 * spec), 0, 255))
                else:
                    r_v = int(np.clip(36 * (0.8 + 0.4 * spec), 0, 255))
                    g_v = int(np.clip(45 * (0.8 + 0.4 * spec), 0, 255))
                    b_v = int(np.clip(61 * (0.8 + 0.4 * spec), 0, 255))
                costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    cos_d.ellipse([61, 71, 65, 75], fill=BRASS_GOLD, outline=OUTLINE)
    cos_d.point((63, 73), fill=ORANGE_BASE)

    for rx in [52, 57, 69, 74]:
        cos_d.ellipse([rx - 1, 84, rx + 1, 86], fill=ORANGE_BASE, outline=OUTLINE)
        cos_d.point((rx, 85), fill=BRASS_SHINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_cat_shadowspring_stiletto.png
    # Features:
    # - Shadowspring Sleeve-Blade / Nightprowl Arc Stiletto (暗影發條袖刃 / 匿夜弧光短匕)
    # - Reverse grip held in right mechanical hand at (84, 72)
    # - Spring-loaded brass socket casing over forearm
    # - Curved obsidian stiletto blade extending backward & downward (x: 82..106, y: 64..96)
    # - Mint Green quenched night-vision razor edge (#4ED86A)
    # - Differential micro gear swivel at pommel
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Sleeve Socket Box on Forearm (x: 80..88, y: 67..76)
    for y in range(67, 77):
        for x in range(80, 89):
            spec = max(0.0, 1.0 - ((x - 84)**2 + (y - 71)**2)**0.5 / 6.0)
            shine = max(0.0, 1.0 - ((x - 83)**2 + (y - 70)**2)**0.5 / 2.5)**2
            r_w = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
            g_w = int(np.clip(208 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
            b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    wd.rectangle([80, 67, 88, 76], outline=OUTLINE, width=1)
    wd.ellipse([82, 70, 86, 74], fill=ORANGE_BASE, outline=OUTLINE)
    wd.point((84, 72), fill=BRASS_SHINE)

    # 2. Hand Grip (82..87, 71..77)
    for y in range(71, 78):
        for x in range(82, 88):
            spec = max(0.0, 1.0 - ((x - 85)**2 + (y - 74)**2)**0.5 / 4.0)
            r_g = int(np.clip(76 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
            g_g = int(np.clip(68 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
            b_g = int(np.clip(86 * (0.8 + 0.4 * spec) + 40 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_g, g_g, b_g, 255))
    wd.ellipse([82, 71, 87, 77], outline=OUTLINE, width=1)

    # 3. Curved Obsidian Stiletto Blade
    blade_pts = []
    for t in np.linspace(0.0, 1.0, 50):
        bx = (1-t)**2 * 84.0 + 2*(1-t)*t * 94.0 + t**2 * 104.0
        by = (1-t)**2 * 74.0 + 2*(1-t)*t * 83.0 + t**2 * 94.0
        blade_pts.append((bx, by))

    for i in range(len(blade_pts) - 1):
        x0, y0 = blade_pts[i]
        x1, y1 = blade_pts[i+1]
        t_prog = i / (len(blade_pts) - 1)
        w_b = max(1.0, 4.0 - 3.0 * t_prog)

        dx_b = x1 - x0
        dy_b = y1 - y0
        norm_len = (dx_b**2 + dy_b**2)**0.5
        if norm_len > 0:
            nx_b = -dy_b / norm_len
            ny_b = dx_b / norm_len
        else:
            nx_b, ny_b = 0.0, 1.0

        for w_step in np.linspace(-w_b, w_b, int(w_b * 3 + 2)):
            px = int(x0 + w_step * nx_b)
            py = int(y0 + w_step * ny_b)
            if 0 <= px < W and 0 <= py < H:
                spec = max(0.0, 1.0 - abs(w_step) / w_b)
                shine = max(0.0, 1.0 - abs(w_step - 0.5) / 1.5)**2
                if w_step > w_b * 0.4:
                    r_c = int(np.clip(78 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    g_c = int(np.clip(216 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                    b_c = int(np.clip(106 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                else:
                    r_c = int(np.clip(43 * (0.8 + 0.6 * spec) + 65 * shine, 0, 255))
                    g_c = int(np.clip(38 * (0.8 + 0.6 * spec) + 60 * shine, 0, 255))
                    b_c = int(np.clip(48 * (0.8 + 0.6 * spec) + 75 * shine, 0, 255))
                weapon_img.putpixel((px, py), (r_c, g_c, b_c, 255))

    weapon_img.putpixel((104, 94), WHITE_SHINE)
    weapon_img.putpixel((103, 93), MINT_SHINE)

    # 4. Pommel Counter-Weight & Differential Micro Gear at (82, 65)
    for y in range(63, 68):
        for x in range(80, 85):
            spec = max(0.0, 1.0 - ((x - 82)**2 + (y - 65)**2)**0.5 / 2.5)
            r_p = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
            g_p = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
            b_p = int(np.clip(40 * (0.85 + 0.5 * spec) + 40 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_p, g_p, b_p, 255))
    wd.ellipse([80, 63, 84, 67], outline=OUTLINE, width=1)
    wd.point((82, 65), fill=MINT_GREEN)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE SLICES (128x128 & 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "chassis_cat_obsidian_steel_default", chassis_img),
        ("head_unit", "head_cat_brass_acoustic_ears", head_img),
        ("winding_key", "key_cat_crescent_twin_ring_gold", key_img),
        ("costume", "costume_cat_skyspire_prowler_vest", costume_img),
        ("optic_core", "face_cat_slit_optic_emerald", core_img),
        ("weapon", "weapon_cat_shadowspring_stiletto", weapon_img),
        ("back_curio", "curio_cat_segmented_gyro_tail", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{CAT_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{CAT_PD_DIR}/winding_key/key_cat_crescent_twin_ring_gold.png",
                    f"{KEY_DIR}/key_cat_crescent_twin_ring_gold.png")
    shutil.copyfile(f"{CAT_PD_DIR}/weapon/weapon_cat_shadowspring_stiletto.png",
                    f"{WEAPON_DIR}/weapon_cat_shadowspring_stiletto.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{CAT_PD_DIR}/proof_paperdoll_cat_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{CAT_PD_DIR}/proof_paperdoll_cat_magenta.png"
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
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255))

    strip_path = f"{CAT_PD_DIR}/proof_cat_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")


if __name__ == "__main__":
    build_all()
