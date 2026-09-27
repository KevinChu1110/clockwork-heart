#!/usr/bin/env python3
"""
build_otter_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 浪花海獺 (The Tidal Otter, otter) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/TIDAL_OTTER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero otter flesh, pressure-proof titanium hull plates,
  ivory enamel cheek/decompression plates, bronze acoustic valves, vulcanized silicone diving boots,
  dual-helm nautical rudder key, 5-segment articulated keel-rudder tail with micro contra-propeller,
  abyssal anchor cleaver heavy axe)
- references/art_direction.md (Dopamine high-saturation palette: Sky Blue #38A0FF, Ivory #FFFDF8,
  Brass Gold #FFD028, Phosphor Mint Green #4ED86A, Coral Pink #FF5E8A, Thick Outline #1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
OTTER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/otter"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Tidal Otter Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Dopamine Sky Blue High-Pressure Titanium Hull (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

# Secondary: Ivory White Enamel Decompression Shell (#FFFDF8)
IVORY_PRIMARY  = (255, 253, 248, 255)
IVORY_LIGHT    = (255, 255, 255, 255)
IVORY_SHADE    = (222, 218, 210, 255)
IVORY_DARK     = (185, 180, 172, 255)

# Accent: Nautical Rudder Helm Gold & Brass Bushings (#FFD028 / #D4A017)
BRASS_GOLD     = (255, 208, 40, 255)
BRASS_LIGHT    = (255, 235, 115, 255)
BRASS_SHINE    = (255, 250, 185, 255)
BRASS_DARK     = (195, 145, 18, 255)
BRASS_DEEP     = (130, 90, 10, 255)

# Detail: Phosphor Mint Green Depth-Gauge Optics (#4ED86A)
MINT_GREEN     = (78, 216, 106, 255)
MINT_LIGHT     = (140, 240, 165, 255)
MINT_SHINE     = (210, 255, 225, 255)
MINT_DARK      = (36, 140, 62, 255)

# Warm Highlight: Coral Pink High-Pressure Silicone Seals & Dampers (#FF5E8A)
CORAL_PINK     = (255, 94, 138, 255)
CORAL_LIGHT    = (255, 150, 180, 255)
CORAL_DARK     = (190, 45, 85, 255)

# Heavy Antique Bronze for Abyssal Anchor Cleaver (#CD7F32 / #B8860B)
BRONZE_BASE    = (185, 120, 50, 255)
BRONZE_LIGHT   = (225, 165, 90, 255)
BRONZE_SHINE   = (255, 215, 140, 255)
BRONZE_DARK    = (125, 75, 25, 255)
BRONZE_DEEP    = (80, 45, 15, 255)

# Deep Navy Salvage Canvas Harness
NAVY_HARNESS   = (30, 50, 80, 255)
NAVY_LIGHT     = (55, 85, 130, 255)
NAVY_DARK      = (18, 30, 52, 255)

# Vulcanized Industrial Black Silicone Diving Boots (#202026)
SILICONE_BASE  = (32, 32, 38, 255)
SILICONE_LIGHT = (65, 65, 78, 255)

# High-Pressure Stainless Steel Wire / Cables / Rivets
STEEL_LIGHT    = (195, 205, 220, 255)
STEEL_MID      = (130, 142, 160, 255)
STEEL_DARK     = (70, 78, 92, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL TIDAL OTTER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_otter_nautical_rudder_helm.png
    # Dual-Helm Nautical Rudder Key (雙舵輪金黃航海發條鑰匙)
    # Socket at upper spine (64, 62)
    # Key shaft extends up and right to helm hub at (86, 32)
    # Dual concentric helm wheels with 8 marine spokes and rim knobs
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 62) to (86, 32)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 22.0
        sy = 62.0 - t * 30.0
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

    # 2. Dual Concentric Helm Rings (雙舵輪輪圈) centered at (86, 32)
    kcx, kcy = 86.0, 32.0
    r_outer = 14.5
    r_inner = 8.0

    # Draw 8 helm spokes with rounded grips
    for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        for dist in np.linspace(3.0, 17.5, 30):
            px = int(kcx + dist * np.cos(angle))
            py = int(kcy + dist * np.sin(angle))
            if 0 <= px < W and 0 <= py < H:
                key_img.putpixel((px, py), BRASS_GOLD)
                if dist >= 15.0:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if 0 <= px + dx < W and 0 <= py + dy < H:
                            key_img.putpixel((px + dx, py + dy), BRASS_LIGHT)

    # Outer & Inner Rings
    for y in range(int(kcy - r_outer - 4), int(kcy + r_outer + 5)):
        for x in range(int(kcx - r_outer - 4), int(kcx + r_outer + 5)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            is_outer_ring = (dist <= r_outer + 1.2 and dist >= r_outer - 1.5)
            is_inner_ring = (dist <= r_inner + 1.1 and dist >= r_inner - 1.3)
            if is_outer_ring or is_inner_ring:
                spec = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 4.0)**2
                r_k = int(np.clip(255 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                g_k = int(np.clip(208 * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                b_k = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Center Hub Boss
    r_hub = 4.5
    for y in range(int(kcy - r_hub - 1), int(kcy + r_hub + 2)):
        for x in range(int(kcx - r_hub - 1), int(kcx + r_hub + 2)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if dist <= r_hub:
                spec = max(0.0, 1.0 - dist / r_hub)
                r_h = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                g_h = int(np.clip(160 * (0.85 + 0.2 * spec), 0, 255))
                b_h = int(np.clip(20 + 50 * spec, 0, 255))
                key_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=CORAL_PINK, outline=OUTLINE)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    apply_clean_outline(key_img)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Tail Layer)
    # File: back_curio/curio_otter_articulated_rudder_tail.png
    # Five-Segment Articulated Keel-Rudder Tail with Contra-Rotating Propeller
    # Extends from pelvis (52, 82) down and left to tip at (20, 94)
    # 5 hydrodynamic titanium hull plates + brass contra-rotating micro-propeller
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    def bezier_curve(p0, p1, p2, p3, num_pts=60):
        pts = []
        for t in np.linspace(0.0, 1.0, num_pts):
            x = (1-t)**3 * p0[0] + 3*(1-t)**2 * t * p1[0] + 3*(1-t) * t**2 * p2[0] + t**3 * p3[0]
            y = (1-t)**3 * p0[1] + 3*(1-t)**2 * t * p1[1] + 3*(1-t) * t**2 * p2[1] + t**3 * p3[1]
            pts.append((x, y))
        return pts

    curve_pts = bezier_curve((52.0, 82.0), (42.0, 85.0), (32.0, 90.0), (20.0, 94.0), num_pts=60)

    # Core stainless steel spine wire
    for i in range(len(curve_pts) - 1):
        x0, y0 = curve_pts[i]
        x1, y1 = curve_pts[i+1]
        cd.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=STEEL_LIGHT, width=3)
        cd.line([(int(x0)-1, int(y0)), (int(x1)-1, int(y1))], fill=OUTLINE, width=1)
        cd.line([(int(x0)+1, int(y0)), (int(x1)+1, int(y1))], fill=OUTLINE, width=1)

    # 5 articulated hydrofoil rudder plates
    t_scales = np.linspace(0.1, 0.9, 5)
    scale_indices = [int(t * (len(curve_pts) - 1)) for t in t_scales]

    for i, idx in enumerate(scale_indices):
        rx_c, ry_c = curve_pts[idx]
        progress = i / 4.0
        r_scale_w = 6.2 - 1.5 * progress
        r_scale_h = 4.8 - 1.0 * progress

        p_prev = curve_pts[max(0, idx - 2)]
        p_next = curve_pts[min(len(curve_pts) - 1, idx + 2)]
        tangent_angle = np.arctan2(p_next[1] - p_prev[1], p_next[0] - p_prev[0])
        normal_angle = tangent_angle + np.pi / 2.0

        for y_off in np.linspace(-r_scale_h, r_scale_h, 11):
            for x_off in np.linspace(-r_scale_w, r_scale_w, 13):
                if (x_off / r_scale_w)**2 + (y_off / r_scale_h)**2 <= 1.0:
                    px = rx_c + x_off * np.cos(normal_angle) + y_off * np.cos(tangent_angle)
                    py = ry_c + x_off * np.sin(normal_angle) + y_off * np.sin(tangent_angle)
                    ix, iy = int(px), int(py)
                    if 0 <= ix < W and 0 <= iy < H:
                        spec = max(0.0, 1.0 - ((x_off**2 + y_off**2)**0.5) / r_scale_w)
                        shine = max(0.0, 1.0 - (x_off**2 + (y_off - 1)**2)**0.5 / 2.5)**2
                        edge_dist = 1.0 - ((x_off / r_scale_w)**2 + (y_off / r_scale_h)**2)
                        
                        # Titanium sky blue with ivory trailing edge
                        if y_off > r_scale_h * 0.4:
                            r_sc = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                            g_sc = int(np.clip(253 * (0.85 + 0.2 * spec), 0, 255))
                            b_sc = int(np.clip(248 * (0.85 + 0.2 * spec), 0, 255))
                        else:
                            r_sc = int(np.clip(56 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                            g_sc = int(np.clip(160 * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                            b_sc = int(np.clip(255 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                        curio_img.putpixel((ix, iy), (r_sc, g_sc, b_sc, 255))

        # Brass hinge pivot rivet
        cd.ellipse([int(rx_c - 1.5), int(ry_c - 1.5), int(rx_c + 1.5), int(ry_c + 1.5)], fill=BRASS_GOLD, outline=OUTLINE)
        cd.point((int(rx_c), int(ry_c)), fill=WHITE_SHINE)

    # Micro contra-rotating twin propeller at tail tip (20, 94)
    tip_x, tip_y = 20.0, 94.0
    cd.ellipse([int(tip_x - 3), int(tip_y - 3), int(tip_x + 3), int(tip_y + 3)], fill=BRASS_GOLD, outline=OUTLINE)
    cd.ellipse([int(tip_x - 1), int(tip_y - 1), int(tip_x + 1), int(tip_y + 1)], fill=CORAL_PINK)

    # Propeller blades
    for p_angle in [np.pi * 0.25, np.pi * 0.75, np.pi * 1.25, np.pi * 1.75]:
        b_end_x = int(tip_x + 6.0 * np.cos(p_angle))
        b_end_y = int(tip_y + 6.0 * np.sin(p_angle))
        cd.line([(int(tip_x), int(tip_y)), (b_end_x, b_end_y)], fill=BRASS_LIGHT, width=2)
        cd.point((b_end_x, b_end_y), fill=OUTLINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_otter_abyssal_cyan_default.png
    # Features:
    # - 2.0~2.2 Chibi hydrodynamic pressure-proof diving posture
    # - Soft ground contact shadow at (64, 116)
    # - Heavy-duty vulcanized black silicone diving boots (#202026) with steel toe guards
    # - Articulated legs with sky blue titanium plates & coral pink pressure dampeners
    # - Titanium Sky Blue (#38A0FF) body hull with multi-tone depth
    # - Ivory White (#FFFDF8) enamel chest & belly decompression plate
    # - Left hand forward/downward fluid-balancing palm at (38, 88)
    # - Right hand tucked at ribs at (82, 75)
    # - STRICT ZERO pixels in outer weapon zone (x >= 94) for 0-ART9 / 0-ART11
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Vulcanized Silicone Diving Boots
    boot_pos = [(48.0, 113.0), (70.0, 113.0)]
    for bx, by in boot_pos:
        # Sole base
        ch_d.ellipse([int(bx - 7), int(by - 2), int(bx + 7), int(by + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(bx - 5), int(by - 1), int(bx + 5), int(by + 2)], fill=SILICONE_LIGHT)
        # Steel toe cap & plate
        ch_d.line([(int(bx - 4), int(by + 2)), (int(bx + 4), int(by + 2))], fill=STEEL_LIGHT, width=2)
        ch_d.point((int(bx), int(by + 1)), fill=WHITE_SHINE)

    # 3. Articulated Legs
    leg_paths = [
        ((48.0, 112.0), (52.0, 88.0)),
        ((70.0, 112.0), (68.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-4, 5):
                spec = max(0.0, 1.0 - abs(dx) / 4.0)
                r_l = int(np.clip(56 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                g_l = int(np.clip(160 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                b_l = int(np.clip(255 * (0.8 + 0.35 * spec) + 40 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 2, mid_x + 3, mid_y + 2], fill=CORAL_PINK, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Torso Body Shell (x: 44..84, y: 56..96)
    cx_t, cy_t = 63.0, 76.0
    for y in range(56, 97):
        for x in range(44, 85):
            dx = (x - cx_t) / 19.5
            dy = (y - cy_t) / 19.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 19.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Ivory enamel decompression chest & belly plate
                is_chest_plate = ((x - 63.0)**2 / 10.5**2 + (y - 75.0)**2 / 11.0**2 <= 1.0)
                if is_chest_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    r_t = int(np.clip(56 * (0.75 + 0.45 * spec) - 25 * edge_shade + 55 * shine, 0, 255))
                    g_t = int(np.clip(160 * (0.75 + 0.45 * spec) - 25 * edge_shade + 50 * shine, 0, 255))
                    b_t = int(np.clip(255 * (0.75 + 0.45 * spec) - 20 * edge_shade + 65 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center mini optical pressure gauge at (63, 75)
    ch_d.ellipse([60, 72, 66, 78], fill=OUTLINE)
    ch_d.ellipse([61, 73, 65, 77], fill=MINT_GREEN)
    ch_d.point((62, 74), fill=MINT_SHINE)

    # Silicone pressure damper seam across mid-torso
    ch_d.arc([46, 68, 80, 88], start=20, end=160, fill=CORAL_PINK, width=1)

    # 5. Left Arm & Streamlined Balancing Palm
    ch_d.line([(48, 73), (38, 86)], fill=CYAN_LIGHT, width=4)
    ch_d.ellipse([34, 84, 41, 91], fill=CYAN_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 86, 39, 89], fill=BRASS_GOLD)

    # 6. Right Arm & Grip Hub (tucked at ribs)
    ch_d.line([(74, 72), (83, 75)], fill=CYAN_LIGHT, width=4)
    ch_d.ellipse([80, 73, 86, 79], fill=CYAN_BASE, outline=OUTLINE)
    ch_d.point((83, 76), fill=BRASS_GOLD)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_otter_diver_bell_visor.png
    # Features:
    # - Spherical Titanium Sky Blue Diving Helmet at (64, 44), rx=18.5, ry=15.5
    # - Ivory White (#FFFDF8) enamel muzzle and cheek plates
    # - Forehead miniature brass water-pressure balancing valve at (64, 32)
    # - Pair of bronze acoustic ear valves with brass rings at (44, 27) and (84, 27)
    # - 6 micro stainless steel fluid velocity needle whiskers (左右各三根)
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Titanium Cyan & Ivory Muzzle)
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
                    r_h = int(np.clip(56 * (0.75 + 0.45 * spec) - 25 * edge_shade + 55 * shine, 0, 255))
                    g_h = int(np.clip(160 * (0.75 + 0.45 * spec) - 25 * edge_shade + 50 * shine, 0, 255))
                    b_h = int(np.clip(255 * (0.75 + 0.45 * spec) - 20 * edge_shade + 65 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Nose & Mouth Seam
    hd.polygon([(62, 47), (66, 47), (64, 49)], fill=OUTLINE)
    hd.line([(64, 49), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([60, 50, 64, 54], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 50, 68, 54], start=0, end=180, fill=OUTLINE, width=1)

    # Forehead Pressure Valve at (64, 32)
    hd.ellipse([61, 30, 67, 34], fill=BRASS_GOLD, outline=OUTLINE)
    hd.ellipse([62, 31, 66, 33], fill=CORAL_PINK)
    hd.point((64, 32), fill=WHITE_SHINE)

    # 2. Bronze Watertight Acoustic Ear Valves at (44, 27) and (84, 27)
    ear_positions = [(44, 27), (84, 27)]
    for ex, ey in ear_positions:
        hd.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], fill=BRASS_GOLD, outline=OUTLINE)
        hd.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=BRONZE_DARK)
        hd.ellipse([ex - 1, ey - 1, ex + 1, ey + 1], fill=CORAL_PINK)

    # 3. 6 Micro Stainless Steel Fluid Velocity Sensor Needles (Whiskers)
    whisker_lines = [
        ([(47, 46), (32, 44)], [(46, 48), (30, 48)], [(47, 50), (33, 53)]),
        ([(81, 46), (96, 44)], [(82, 48), (98, 48)], [(81, 50), (95, 53)])
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
    # File: optic_core/face_otter_phosphor_green_gauges.png
    # Features:
    # - Dual 24px-scale Phosphor-Green Quartz Dome Optical Lenses at (52, 40) and (76, 40)
    # - Concentric depth meter cursor rings with glowing mint core (#4ED86A)
    # - White specular quartz glint at top-left
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
                    # Depth meter concentric circle ring
                    is_ring = (abs(dist - 2.5) <= 0.4)
                    if is_ring:
                        r_c, g_c, b_c = 210, 255, 225
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
    # File: costume/costume_otter_deepsea_salvage_harness.png
    # Features:
    # - Deepsea Salvage Diver Harness (海淵打撈工匠耐壓雙肩吊帶工裝)
    # - Deep Navy (#1E3250) reinforced canvas straps with brass buckles
    # - Coral pink pressure dampers & front placket valve
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
                is_strap = (abs((x - 63.0) - (y - 73.0) * 0.7) <= 2.2 or abs((x - 63.0) + (y - 73.0) * 0.7) <= 2.2)
                is_belt = (abs(y - 82) <= 2.0)
                if is_strap or is_belt:
                    r_v = int(np.clip(30 * (0.8 + 0.4 * spec), 0, 255))
                    g_v = int(np.clip(50 * (0.8 + 0.4 * spec), 0, 255))
                    b_v = int(np.clip(80 * (0.8 + 0.4 * spec), 0, 255))
                    costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Center brass buckle
    cos_d.ellipse([60, 71, 66, 77], fill=BRASS_GOLD, outline=OUTLINE)
    cos_d.ellipse([62, 73, 64, 75], fill=CORAL_PINK)

    # Rivets on belt
    for rx in [52, 57, 69, 74]:
        cos_d.ellipse([rx - 1, 81, rx + 1, 83], fill=BRASS_GOLD, outline=OUTLINE)
        cos_d.point((rx, 82), fill=WHITE_SHINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_otter_abyssal_anchor_cleaver.png
    # Features:
    # - Abyssal Anchor Cleaver (海錨防禦重斧 / 琉璃破障重斧)
    # - Right-hand single held (0-MKT7 compliant) at (84, 75)
    # - Heavy antique bronze shank extending from top shackle (86, 50) to crown (92, 88)
    # - Single-side flukes expanded into massive crescent cleaving axe blade (x: 88..114, y: 60..96)
    # - Steel cable coils wrapped around shank
    # - Polished bronze and steel cutting bevel
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Top Shackle Ring at (86, 50)
    wd.ellipse([82, 46, 90, 54], outline=BRASS_GOLD, width=2)
    wd.ellipse([84, 48, 88, 52], fill=(0, 0, 0, 0))

    # 2. Main Bronze Anchor Shank (86, 52) to (92, 88)
    for t in np.linspace(0.0, 1.0, 40):
        sx = 86.0 + t * 6.0
        sy = 52.0 + t * 36.0
        for w_s in range(-3, 4):
            px = int(sx + w_s)
            py = int(sy)
            if 0 <= px < W and 0 <= py < H:
                spec = max(0.0, 1.0 - abs(w_s) / 3.0)
                r_w = int(np.clip(185 * (0.8 + 0.3 * spec), 0, 255))
                g_w = int(np.clip(120 * (0.8 + 0.3 * spec), 0, 255))
                b_w = int(np.clip(50 * (0.8 + 0.3 * spec), 0, 255))
                weapon_img.putpixel((px, py), (r_w, g_w, b_w, 255))

    # Steel cable coils wrapped around shank
    for cy_coil in [58, 63, 68]:
        wd.line([(83, cy_coil), (89, cy_coil - 2)], fill=STEEL_LIGHT, width=2)

    # 3. Grip Hand Socket at (84, 75)
    wd.ellipse([81, 72, 87, 78], fill=CYAN_BASE, outline=OUTLINE)
    wd.ellipse([82, 73, 86, 77], fill=CYAN_LIGHT)
    wd.point((84, 75), fill=BRASS_GOLD)

    # 4. Massive Crescent Axe Blade (x: 88..114, y: 60..96)
    for y in range(60, 97):
        for x in range(88, 115):
            # Curved crescent geometry
            # Outer boundary circle center at (82, 78), r=32
            # Inner hollow cutout circle center at (74, 78), r=24
            d_outer = ((x - 82)**2 + (y - 78)**2)**0.5
            d_inner = ((x - 74)**2 + (y - 78)**2)**0.5
            if d_outer <= 31.0 and d_inner >= 17.0 and x >= 88:
                spec = max(0.0, 1.0 - abs(d_outer - 24.0) / 7.0)
                shine = max(0.0, 1.0 - ((x - 105)**2 + (y - 76)**2)**0.5 / 6.0)**2
                is_edge = (d_outer >= 28.5)
                if is_edge:
                    # Razor steel cutting edge
                    r_b = int(np.clip(220 * (0.85 + 0.25 * spec) + 35 * shine, 0, 255))
                    g_b = int(np.clip(230 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    b_b = int(np.clip(245 * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                else:
                    # Antique heavy bronze axe body
                    r_b = int(np.clip(185 * (0.8 + 0.35 * spec) + 50 * shine, 0, 255))
                    g_b = int(np.clip(120 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                    b_b = int(np.clip(50 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Fluke anchor crown spike at bottom (92, 94)
    wd.polygon([(89, 90), (95, 90), (92, 96)], fill=BRONZE_LIGHT, outline=OUTLINE)

    # High pressure indicator valve on axe back
    wd.ellipse([90, 74, 94, 78], fill=OUTLINE)
    wd.ellipse([91, 75, 93, 77], fill=MINT_GREEN)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 AND 512x512 LANCZOS SLICES
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_otter_nautical_rudder_helm", key_img),
        ("back_curio", "curio_otter_articulated_rudder_tail", curio_img),
        ("chassis", "chassis_otter_abyssal_cyan_default", chassis_img),
        ("head_unit", "head_otter_diver_bell_visor", head_img),
        ("optic_core", "face_otter_phosphor_green_gauges", core_img),
        ("costume", "costume_otter_deepsea_salvage_harness", costume_img),
        ("weapon", "weapon_otter_abyssal_anchor_cleaver", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{OTTER_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{OTTER_PD_DIR}/winding_key/key_otter_nautical_rudder_helm.png",
                    f"{KEY_DIR}/key_otter_nautical_rudder_helm.png")
    shutil.copyfile(f"{OTTER_PD_DIR}/weapon/weapon_otter_abyssal_anchor_cleaver.png",
                    f"{WEAPON_DIR}/weapon_otter_abyssal_anchor_cleaver.png")
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

    proof_comp = f"{OTTER_PD_DIR}/proof_paperdoll_otter_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{OTTER_PD_DIR}/proof_paperdoll_otter_magenta.png"
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

    strip_path = f"{OTTER_PD_DIR}/proof_otter_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/otter_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/otter_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
