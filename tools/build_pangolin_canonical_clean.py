#!/usr/bin/env python3
"""
build_pangolin_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 沙鱗穿山甲 (The Dune Pangolin, pangolin) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/DUNE_PANGOLIN_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero pangolin flesh, articulated stamped warm orange scale-plates,
  stamped thin brass fan-shaped acoustic ears, ivory enamel cheek/breast plates, silicone pads,
  concentric coil-scale spiral gold key, 7-segment scale-plate tail, dune-drill hydraulic claw)
- references/art_direction.md (Dopamine high-saturation palette: Orange #FFA010, Ivory #FFFDF8,
  Brass Gold #FFD028, Sky Blue #38A0FF, Coral Pink #FF5E8A, Outline #1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
PANGOLIN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Dune Pangolin Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Articulated Stamped Warm Orange Scale-Plates (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 80, 255)
ORANGE_SHINE = (255, 230, 150, 255)
ORANGE_DARK  = (200, 105, 10, 255)
ORANGE_DEEP  = (145, 65, 8, 255)

# Secondary: Ivory White Enamel (#FFFDF8)
IVORY_PRIMARY  = (255, 253, 248, 255)
IVORY_LIGHT    = (255, 255, 255, 255)
IVORY_SHADE    = (225, 220, 210, 255)
IVORY_DARK     = (185, 180, 170, 255)

# Accent: Concentric Scale Spiral Key & Acoustic Brass Gold (#FFD028 / #D4A017)
BRASS_GOLD     = (255, 208, 40, 255)
BRASS_LIGHT    = (255, 235, 115, 255)
BRASS_SHINE    = (255, 250, 185, 255)
BRASS_DARK     = (195, 145, 18, 255)
BRASS_DEEP     = (130, 90, 10, 255)

# Detail: Starry Sky Blue Optical Lens Domes (#38A0FF)
SKY_BLUE       = (56, 160, 255, 255)
BLUE_LIGHT     = (125, 205, 255, 255)
BLUE_SHINE     = (205, 235, 255, 255)
BLUE_DARK      = (20, 95, 190, 255)

# Warm Highlight: Coral Pink Pressure Damper & Joint Seals (#FF5E8A)
CORAL_PINK     = (255, 94, 138, 255)
CORAL_LIGHT    = (255, 150, 180, 255)
CORAL_DARK     = (190, 45, 85, 255)

# Industrial High-Grip Silicone & Tungsten Steel
SILICONE_BASE  = (32, 32, 38, 255)
SILICONE_LIGHT = (65, 65, 78, 255)
STEEL_LIGHT    = (195, 205, 220, 255)
STEEL_DARK     = (90, 100, 115, 255)
WHITE_SHINE    = (255, 255, 255, 255)


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
    print("=== BUILDING 100% MODULAR CANONICAL DUNE PANGOLIN SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_pangolin_coil_scale_spiral_gold.png
    # Concentric Coil-Scale Spiral Gold Key (同心渦卷金鱗發條鑰匙)
    # Socket at upper spine (64, 62)
    # Key shaft extends up and right to coil center at (88, 34)
    # Twin outward curved spiral wings with concentric scale reliefs
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 62) to (88, 34)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 64.0 + t * 24.0
        sy = 62.0 - t * 28.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 62)
    kd.ellipse([60, 58, 68, 66], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([61, 59, 67, 65], fill=BRASS_GOLD)
    kd.ellipse([63, 61, 65, 63], fill=CORAL_PINK)

    # 2. Concentric Coil-Scale Spiral Wing Head at (88, 34)
    kcx, kcy = 88.0, 34.0
    r_outer = 15.0

    # Draw Spiral Wing Profiles
    for y in range(int(kcy - r_outer - 3), int(kcy + r_outer + 4)):
        for x in range(int(kcx - r_outer - 3), int(kcx + r_outer + 4)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= r_outer and dist >= 2.5:
                angle = np.arctan2(dy, dx)
                # Twin spiral lobes inspired by overlapping pangolin scales
                # Archimedean / logarithmic curve blend
                spiral_phase = (angle % np.pi) / np.pi
                r_spiral = 4.5 + 10.5 * spiral_phase
                if dist <= r_spiral + 2.0 and dist >= r_spiral - 4.5:
                    spec = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 16.0)
                    shine = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 4.0)**2
                    scale_ripple = 0.5 + 0.5 * np.sin(dist * 1.8 + angle * 2.0)

                    r_k = int(np.clip(255 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                    g_k = int(np.clip((180 + 40 * scale_ripple) * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    b_k = int(np.clip(35 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Inner Core Gear & Rivet
    r_gear = 6.0
    for y in range(int(kcy - r_gear - 2), int(kcy + r_gear + 3)):
        for x in range(int(kcx - r_gear - 2), int(kcx + r_gear + 3)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= r_gear:
                angle = np.arctan2(dy, dx)
                cogs = np.cos(6.0 * angle)
                cog_bound = r_gear - 1.2 + 1.2 * max(0.0, cogs)
                if dist <= cog_bound and dist >= 2.2:
                    spec = max(0.0, 1.0 - dist / r_gear)
                    r_g = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                    g_g = int(np.clip(160 * (0.85 + 0.2 * spec), 0, 255))
                    b_g = int(np.clip(20 + 50 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_g, g_g, b_g, 255))

    # Central Hub Rivet with Coral Pink Accent
    kd.ellipse([int(kcx - 2.5), int(kcy - 2.5), int(kcx + 2.5), int(kcy + 2.5)], fill=CORAL_PINK, outline=OUTLINE)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    # Safe Outline Pass (0-ART29 safe snapshot)
    apply_clean_outline(key_img)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Tail Layer)
    # File: back_curio/curio_pangolin_segmented_scale_tail.png
    # Seven-Segment Stamped Scale-Plate Counterweight Tail (七節沖壓厚鋼金屬覆鱗尾)
    # Extends from spine base (50, 84) down and left to ground at (22, 104)
    # 7 articulated stamped heavy scale plates overlapping on spring steel core
    # Tip features octagonal brass counterweight bob (八角黃銅配重球) with rivets
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Flexible Spring Steel Core Spine
    def bezier_curve(p0, p1, p2, p3, num_pts=60):
        pts = []
        for t in np.linspace(0.0, 1.0, num_pts):
            x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
            pts.append((x, y))
        return pts

    curve_pts = bezier_curve((50.0, 84.0), (40.0, 86.0), (30.0, 96.0), (22.0, 104.0), num_pts=70)

    # Draw core steel wire
    for i in range(len(curve_pts) - 1):
        x0, y0 = curve_pts[i]
        x1, y1 = curve_pts[i+1]
        cd.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=STEEL_LIGHT, width=3)
        cd.line([(int(x0)-1, int(y0)), (int(x1)-1, int(y1))], fill=OUTLINE, width=1)
        cd.line([(int(x0)+1, int(y0)), (int(x1)+1, int(y1))], fill=OUTLINE, width=1)

    # 2. 7 Articulated Stamped Scale Plates along tail curve
    t_scales = np.linspace(0.08, 0.88, 7)
    scale_indices = [int(t * (len(curve_pts) - 1)) for t in t_scales]

    for i, idx in enumerate(scale_indices):
        rx_c, ry_c = curve_pts[idx]
        progress = i / 6.0
        # Scale width decreases from base to tip
        r_scale_w = 6.5 - 2.2 * progress
        r_scale_h = 5.0 - 1.2 * progress

        p_prev = curve_pts[max(0, idx - 2)]
        p_next = curve_pts[min(len(curve_pts) - 1, idx + 2)]
        tangent_angle = np.arctan2(p_next[1] - p_prev[1], p_next[0] - p_prev[0])
        normal_angle = tangent_angle + np.pi / 2.0

        # Draw overlapping scale plate
        for y_off in np.linspace(-r_scale_h, r_scale_h, 11):
            for x_off in np.linspace(-r_scale_w, r_scale_w, 13):
                if (x_off / r_scale_w)**2 + (y_off / r_scale_h)**2 <= 1.0:
                    px = rx_c + x_off * np.cos(normal_angle) + y_off * np.cos(tangent_angle)
                    py = ry_c + x_off * np.sin(normal_angle) + y_off * np.sin(tangent_angle)
                    spec = max(0.0, 1.0 - (x_off**2 + y_off**2)**0.5 / r_scale_w)
                    shine = max(0.0, 1.0 - ((x_off - 1)**2 + (y_off - 1)**2)**0.5 / 2.0)**2
                    r_sc = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    g_sc = int(np.clip(160 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                    b_sc = int(np.clip(16 * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                    curio_img.putpixel((int(px), int(py)), (r_sc, g_sc, b_sc, 255))

        # Rivet stud on scale hinge
        cd.ellipse([int(rx_c - 1.5), int(ry_c - 1.5), int(rx_c + 1.5), int(ry_c + 1.5)],
                   fill=BRASS_GOLD, outline=OUTLINE)

    # 3. Tip: Octagonal Brass Counterweight Bob at (20, 106)
    tbx, tby = 20.0, 106.0
    r_bob = 5.5
    for y in range(int(tby - r_bob - 2), int(tby + r_bob + 3)):
        for x in range(int(tbx - r_bob - 2), int(tbx + r_bob + 3)):
            dx = x - tbx
            dy = y - tby
            dist_profile = max(abs(dx), abs(dy), (abs(dx) + abs(dy)) * 0.72)
            if dist_profile <= r_bob:
                spec = max(0.0, 1.0 - ((x - (tbx - 2))**2 + (y - (tby - 2))**2)**0.5 / (r_bob * 1.2))
                shine = max(0.0, 1.0 - ((x - (tbx - 1.5))**2 + (y - (tby - 1.5))**2)**0.5 / 2.0)**2
                r_b = int(np.clip(255 * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                g_b = int(np.clip(208 * (0.85 + 0.2 * spec) + 45 * shine, 0, 255))
                b_b = int(np.clip(40 * (0.85 + 0.2 * spec) + 70 * shine, 0, 255))
                curio_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    cd.polygon([(int(tbx - r_bob * 0.5), int(tby - r_bob)),
                (int(tbx + r_bob * 0.5), int(tby - r_bob)),
                (int(tbx + r_bob), int(tby - r_bob * 0.5)),
                (int(tbx + r_bob), int(tby + r_bob * 0.5)),
                (int(tbx + r_bob * 0.5), int(tby + r_bob)),
                (int(tbx - r_bob * 0.5), int(tby + r_bob)),
                (int(tbx - r_bob), int(tby + r_bob * 0.5)),
                (int(tbx - r_bob), int(tby - r_bob * 0.5))], outline=OUTLINE)
    cd.point((int(tbx), int(tby)), fill=CORAL_PINK)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_pangolin_dune_orange_default.png
    # Features:
    # - Low, grounded martial monk stance with rounded 2.2 chibi scale torso
    # - Soft ground contact shadow at (64, 116)
    # - 4 articulated mechanical limbs with silicone foot pads & stamped metal toe caps
    # - Warm Orange (#FFA010) electroplated metal scale plates with overlapping bevels
    # - Ivory White (#FFFDF8) enamel chest & belly plate with rich multi-tone depth
    # - Left hand extended forward in balance palm guard (化勁引掌) at (36, 88)
    # - Right hand tucked ready for weapon claw at (80, 76)
    # - STRICTLY ZERO weapon baked in (0-ART9/0-ART11: x >= 94 is STRICTLY 0)
    # - Multi-tone depth with unique colors >= 20 (0-ART18)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 34, 116 - 5, 64 + 34, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Silicone Foot Pads & Metal Protective Caps
    feet_pos = [(42.0, 113.0), (56.0, 113.0), (72.0, 113.0), (84.0, 113.0)]
    for fcx, fcy in feet_pos:
        ch_d.ellipse([int(fcx - 5), int(fcy - 1), int(fcx + 5), int(fcy + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(fcx - 3), int(fcy), int(fcx + 3), int(fcy + 2)], fill=SILICONE_LIGHT)
        # Metal toe caps with rivets
        for c_dx in [-3, 0, 3]:
            ch_d.line([(int(fcx + c_dx), int(fcy + 1)), (int(fcx + c_dx), int(fcy + 3))], fill=BRASS_GOLD, width=1)
            ch_d.point((int(fcx + c_dx), int(fcy + 3)), fill=OUTLINE)

    # 3. Articulated Legs with Orange Scale Plates
    leg_paths = [
        ((42.0, 113.0), (48.0, 86.0)),
        ((56.0, 113.0), (58.0, 86.0)),
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
                    r_l = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_l = int(np.clip(160 * (0.8 + 0.25 * spec), 0, 255))
                    b_l = int(np.clip(16 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                    chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 2, mid_y - 2, mid_x + 2, mid_y + 2], fill=CORAL_PINK, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=BRASS_SHINE)

    # 4. Torso Body Shell (x: 40..88, y: 56..98)
    # Chubby spherical scale-plated body
    cx_t, cy_t = 63.0, 76.0
    for y in range(56, 99):
        for x in range(40, 89):
            dx = (x - cx_t) / 22.0
            dy = (y - cy_t) / 20.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 20.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 6.5)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Ivory White enamel breast/belly plate at front center
                is_chest_plate = ((x - 62.0)**2 / 10.0**2 + (y - 75.0)**2 / 10.5**2 <= 1.0)
                if is_chest_plate:
                    # Multi-tone ivory shading with soft gradient
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    # Warm Orange electroplated scale hull with subtle horizontal scale ridges
                    ridge = 0.85 + 0.15 * np.cos((y - 56) * 0.8)
                    r_t = int(np.clip(255 * (0.75 + 0.3 * spec) * ridge - 25 * edge_shade + 40 * shine, 0, 255))
                    g_t = int(np.clip(160 * (0.75 + 0.3 * spec) * ridge - 25 * edge_shade + 35 * shine, 0, 255))
                    b_t = int(np.clip(16 * (0.75 + 0.3 * spec) * ridge - 10 * edge_shade + 50 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Scale armor seams and central gear emblem
    ch_d.arc([42, 58, 84, 96], start=30, end=150, fill=ORANGE_DEEP, width=1)
    ch_d.line([(51, 70), (51, 82)], fill=OUTLINE, width=1)
    ch_d.line([(73, 70), (73, 82)], fill=OUTLINE, width=1)
    ch_d.ellipse([60, 72, 66, 78], fill=BRASS_DARK, outline=OUTLINE)
    ch_d.ellipse([61, 73, 65, 77], fill=BRASS_GOLD)
    ch_d.point((62, 74), fill=BRASS_SHINE)

    # 5. Left Arm & Open Palm Guard (化勁引掌, x: 34..48, y: 72..90)
    ch_d.line([(46, 74), (38, 86)], fill=ORANGE_BASE, width=3)
    ch_d.ellipse([34, 84, 42, 90], fill=IVORY_PRIMARY, outline=OUTLINE)
    ch_d.point((38, 87), fill=CORAL_PINK)

    # 6. Right Arm & Wrist Mount (tucked ready at ribs, x: 74..84, y: 72..80)
    ch_d.line([(74, 73), (82, 76)], fill=ORANGE_BASE, width=3)
    ch_d.ellipse([79, 74, 85, 80], fill=ORANGE_DARK, outline=OUTLINE)
    ch_d.point((82, 77), fill=BRASS_GOLD)

    # Safe Outline Pass for chassis
    apply_clean_outline(chassis_img)

    # Ensure strictly zero pixels at x >= 94 (0-ART9/0-ART11 protection)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_pangolin_brass_acoustic_ears.png
    # Features:
    # - Spherical Warm Orange & Ivory enamel skull centered at (64, 44), rx=18.5, ry=15.5
    # - 3 curved rows of overlapping metal scale plates on skull dome
    # - Stamped Brass Fan-Shaped Acoustic Ears (立耳!) at (42..54, 16..32) and (74..86, 16..32)
    # - Rounded snout with small brass pressure valve at nose
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # - Brass ocular rings with deep socket shading around eye perimeters
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Orange Scale Armor & Ivory Cheek/Muzzle)
    for y in range(int(hcy - hry - 2), int(hcy + hry + 3)):
        for x in range(int(hcx - hrx - 2), int(hcx + hrx + 3)):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 5.5)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Ivory enamel cheeks and lower snout
                is_muzzle = (y >= 43 and abs(x - hcx) <= 15.0 and ((x - hcx)/14.0)**2 + ((y - 48)/10.0)**2 <= 1.0)
                if is_muzzle:
                    r_h = int(np.clip(255 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    g_h = int(np.clip(253 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    b_h = int(np.clip(248 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                else:
                    # Warm Orange electroplated scale helmet with 3 rows of scale ribs
                    ridge = 0.88 + 0.12 * np.cos((y - 30) * 1.2)
                    r_h = int(np.clip(255 * (0.75 + 0.3 * spec) * ridge - 20 * edge_shade + 45 * shine, 0, 255))
                    g_h = int(np.clip(160 * (0.75 + 0.3 * spec) * ridge - 20 * edge_shade + 40 * shine, 0, 255))
                    b_h = int(np.clip(16 * (0.75 + 0.3 * spec) * ridge - 10 * edge_shade + 55 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Metallic Brass Nose Valve & Mouth Seam
    hd.ellipse([62, 47, 66, 50], fill=BRASS_GOLD, outline=OUTLINE)
    hd.point((64, 48), fill=BRASS_SHINE)
    hd.line([(64, 50), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([60, 51, 64, 55], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 51, 68, 55], start=0, end=180, fill=OUTLINE, width=1)

    # 2. Stamped Thin Brass Fan-Shaped Acoustic Ears (扇形拾音耳, 立耳!)
    # Left ear: (42..54, 16..32), Right ear: (74..86, 16..32)
    ear_sectors = [
        (47.0, 24.0, True),
        (81.0, 24.0, False)
    ]
    for ex, ey, is_left in ear_sectors:
        # Fan shape
        r_ear = 9.0
        for y in range(int(ey - r_ear - 2), int(ey + r_ear + 3)):
            for x in range(int(ex - r_ear - 2), int(ex + r_ear + 3)):
                dx = x - ex
                dy = y - ey
                dist = (dx**2 + dy**2)**0.5
                if dist <= r_ear and y <= ey + 4:
                    angle = np.arctan2(dy, dx)
                    # Fan sector: angle range
                    valid_angle = (-2.5 <= angle <= -0.5) if is_left else (-2.6 <= angle <= -0.6)
                    if valid_angle or dist <= 4.0:
                        spec = max(0.0, 1.0 - dist / r_ear)
                        shine = max(0.0, 1.0 - ((x - (ex - 2))**2 + (y - (ey - 2))**2)**0.5 / 3.0)**2
                        # Inner acoustic mesh grid
                        mesh = (int(x + y) % 2 == 0) and (dist > 3.5)
                        if mesh:
                            r_e = int(np.clip(195 * (0.8 + 0.25 * spec), 0, 255))
                            g_e = int(np.clip(145 * (0.8 + 0.25 * spec), 0, 255))
                            b_e = int(np.clip(18 * (0.8 + 0.25 * spec), 0, 255))
                        else:
                            r_e = int(np.clip(255 * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                            g_e = int(np.clip(208 * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                            b_e = int(np.clip(40 * (0.85 + 0.2 * spec) + 60 * shine, 0, 255))
                        head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        # Ear hinge base with coral pink ring
        hd.ellipse([int(ex - 2.5), int(ey + 3), int(ex + 2.5), int(ey + 7)], fill=CORAL_PINK, outline=OUTLINE)
        hd.point((int(ex), int(ey + 5)), fill=BRASS_GOLD)

    # 3. HOLLOW EYE SOCKETS (0-ART27 compliance)
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
    # File: optic_core/face_pangolin_sky_blue_optic_domes.png
    # Features:
    # - Dual Starry Sky Blue Optical Lens Domes at (52, 40) and (76, 40)
    # - Sky Blue (#38A0FF) glowing quartz lenses with concentric rangefinder reticle
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
                    # Concentric rangefinder ring
                    is_reticle = (abs(dist - 2.4) <= 0.4) or (abs(x - ecx) <= 0.4 and dist <= 3.2)
                    if is_reticle:
                        r_c, g_c, b_c = 210, 240, 255
                    else:
                        r_c = int(np.clip(56 * (0.8 + 0.3 * spec) + 55 * shine, 0, 255))
                        g_c = int(np.clip(160 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        b_c = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        c_d.ellipse([int(ecx - r_lens), int(ecy - r_lens), int(ecx + r_lens), int(ecy + r_lens)],
                    outline=OUTLINE, width=1)
        c_d.point((int(ecx - 1), int(ecy - 1)), fill=WHITE_SHINE)
        c_d.point((int(ecx), int(ecy - 2)), fill=BLUE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_pangolin_scavenger_tinker_vest.png
    # Features:
    # - Scavenger Tinker Work Vest (齒輪營地拾荒工匠工裝背心)
    # - Sturdy khaki/sand-olive canvas vest (x: 48..78, y: 58..88)
    # - Diagonal leather tool belt strap across chest with brass buckle (#FFD028)
    # - Miniature screwdriver/tinker tool handle in pocket
    # - Coral pink (#FF5E8A) & brass rivet studs along hem
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
                # Diagonal cross-body tool strap
                is_strap = (abs((x - 63.0) - (y - 73.0) * 0.8) <= 2.2)
                if is_strap:
                    r_v = int(np.clip(115 * (0.8 + 0.3 * spec), 0, 255))
                    g_v = int(np.clip(75 * (0.8 + 0.3 * spec), 0, 255))
                    b_v = int(np.clip(45 * (0.8 + 0.3 * spec), 0, 255))
                else:
                    # Canvas vest texture (sand khaki)
                    r_v = int(np.clip(140 * (0.8 + 0.35 * spec), 0, 255))
                    g_v = int(np.clip(120 * (0.8 + 0.35 * spec), 0, 255))
                    b_v = int(np.clip(85 * (0.8 + 0.35 * spec), 0, 255))
                costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Brass Buckle on Tool Strap
    cos_d.ellipse([61, 71, 66, 76], fill=BRASS_GOLD, outline=OUTLINE)
    cos_d.point((63, 73), fill=BRASS_SHINE)

    # Tool Handle in pocket (54, 76..82)
    cos_d.line([(54, 74), (54, 80)], fill=STEEL_LIGHT, width=2)
    cos_d.ellipse([52, 72, 56, 75], fill=CORAL_PINK, outline=OUTLINE)

    # Rivet studs along hem
    for rx in [52, 58, 68, 74]:
        cos_d.ellipse([rx - 1, 84, rx + 1, 86], fill=ORANGE_BASE, outline=OUTLINE)
        cos_d.point((rx, 85), fill=BRASS_SHINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_pangolin_dune_drill_claw.png
    # Features:
    # - Dune-Drill Hydraulic Claw / Sandstorm Breaker Claw (渦輪掘進破甲機關爪)
    # - Mounted on right arm/hand (x: 80..112, y: 64..96)
    # - Stamped Tungsten Steel Breaker Claw with 3 heavy curved blades
    # - Turbo rotor housing with brass rotor (#FFD028) & coral pink damper ring (#FF5E8A)
    # - Sky Blue (#38A0FF) energy exhaust slits
    # - SINGLE WIELD (0-MKT7 compliant: only on right hand, left hand empty)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Hydraulic Forearm Casing & Turbo Housing (x: 78..88, y: 67..78)
    for y in range(67, 79):
        for x in range(78, 89):
            spec = max(0.0, 1.0 - ((x - 83)**2 + (y - 73)**2)**0.5 / 6.5)
            shine = max(0.0, 1.0 - ((x - 82)**2 + (y - 71)**2)**0.5 / 2.5)**2
            r_w = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
            g_w = int(np.clip(160 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
            b_w = int(np.clip(16 * (0.8 + 0.5 * spec) + 50 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    wd.rectangle([78, 67, 88, 78], outline=OUTLINE, width=1)
    # Brass Turbine Rotor
    wd.ellipse([80, 69, 86, 75], fill=BRASS_GOLD, outline=OUTLINE)
    wd.point((83, 72), fill=CORAL_PINK)

    # 2. Hand Grip & Hydraulic Cylinder (81..87, 73..79)
    for y in range(73, 80):
        for x in range(81, 88):
            spec = max(0.0, 1.0 - ((x - 84)**2 + (y - 76)**2)**0.5 / 4.0)
            r_g = int(np.clip(195 * (0.8 + 0.3 * spec), 0, 255))
            g_g = int(np.clip(205 * (0.8 + 0.3 * spec), 0, 255))
            b_g = int(np.clip(220 * (0.8 + 0.3 * spec), 0, 255))
            weapon_img.putpixel((x, y), (r_g, g_g, b_g, 255))
    wd.ellipse([81, 73, 87, 79], outline=OUTLINE, width=1)

    # 3. Three Curved Tungsten Breaker Claw Blades
    # Claw 1 (top): (84, 71) -> (104, 76)
    # Claw 2 (middle): (85, 75) -> (108, 85)
    # Claw 3 (bottom): (84, 78) -> (102, 94)
    claw_configs = [
        ((84.0, 71.0), (95.0, 72.0), (105.0, 77.0), 3.2),
        ((85.0, 75.0), (98.0, 78.0), (110.0, 86.0), 4.0),
        ((84.0, 78.0), (95.0, 85.0), (103.0, 95.0), 3.4),
    ]

    for p0, p1, p2, claw_max_w in claw_configs:
        blade_pts = []
        for t in np.linspace(0.0, 1.0, 45):
            bx = (1-t)**2 * p0[0] + 2*(1-t)*t * p1[0] + t**2 * p2[0]
            by = (1-t)**2 * p0[1] + 2*(1-t)*t * p1[1] + t**2 * p2[1]
            blade_pts.append((bx, by))

        for i in range(len(blade_pts) - 1):
            x0, y0 = blade_pts[i]
            x1, y1 = blade_pts[i+1]
            t_prog = i / (len(blade_pts) - 1)
            w_b = max(1.0, claw_max_w - (claw_max_w - 0.8) * t_prog)

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
                    shine = max(0.0, 1.0 - abs(w_step - 0.4) / 1.4)**2
                    # Energy vent highlight in middle of claw blade
                    if abs(w_step) <= 0.6 and t_prog < 0.65:
                        r_c = int(np.clip(56 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        g_c = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        b_c = int(np.clip(255 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    else:
                        # Polished tungsten steel blade
                        r_c = int(np.clip(195 * (0.8 + 0.25 * spec) + 55 * shine, 0, 255))
                        g_c = int(np.clip(205 * (0.8 + 0.25 * spec) + 50 * shine, 0, 255))
                        b_c = int(np.clip(220 * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    weapon_img.putpixel((px, py), (r_c, g_c, b_c, 255))

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 AND 512x512 LANCZOS SLICES
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_pangolin_coil_scale_spiral_gold", key_img),
        ("back_curio", "curio_pangolin_segmented_scale_tail", curio_img),
        ("chassis", "chassis_pangolin_dune_orange_default", chassis_img),
        ("head_unit", "head_pangolin_brass_acoustic_ears", head_img),
        ("optic_core", "face_pangolin_sky_blue_optic_domes", core_img),
        ("costume", "costume_pangolin_scavenger_tinker_vest", costume_img),
        ("weapon", "weapon_pangolin_dune_drill_claw", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{PANGOLIN_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{PANGOLIN_PD_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold.png",
                    f"{KEY_DIR}/key_pangolin_coil_scale_spiral_gold.png")
    shutil.copyfile(f"{PANGOLIN_PD_DIR}/weapon/weapon_pangolin_dune_drill_claw.png",
                    f"{WEAPON_DIR}/weapon_pangolin_dune_drill_claw.png")
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

    proof_comp = f"{PANGOLIN_PD_DIR}/proof_paperdoll_pangolin_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{PANGOLIN_PD_DIR}/proof_paperdoll_pangolin_magenta.png"
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

    strip_path = f"{PANGOLIN_PD_DIR}/proof_pangolin_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")


if __name__ == "__main__":
    build_all()
