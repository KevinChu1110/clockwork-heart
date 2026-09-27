#!/usr/bin/env python3
"""
build_raccoon_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 星巡浣熊 (The Orbit Raccoon, raccoon) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/ORBIT_RACCOON_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero raccoon flesh, high-impact aerospace engineering polymer plates,
  ivory enamel cheek/decompression plates, parabolic radar dish ears, vulcanized magnetic silicone boots,
  quad solar sail wind-up key, 5-segment coaxial ring antenna discharge tail, anti-gravity pulse blaster gun)
- references/art_direction.md (Dopamine palette: Electric Orbit Aqua #00C2CB, Ivory White #FFFDF8,
  Solar Gold #FFD028, Phosphor Mint Green #4ED86A, Coral Pink #FF5E8A, Deep Outline #1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
RACCOON_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/raccoon"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Orbit Raccoon Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Electric Orbit Aqua (#00C2CB) High-Impact Engineering Polymer Shell
AQUA_BASE  = (0, 194, 203, 255)
AQUA_LIGHT = (70, 225, 235, 255)
AQUA_SHINE = (175, 245, 250, 255)
AQUA_DARK  = (0, 135, 145, 255)
AQUA_DEEP  = (0, 85, 95, 255)

# Secondary: Ivory White Enamel Decompression & Shock Shell (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (225, 220, 212, 255)
IVORY_DARK    = (185, 180, 172, 255)

# Accent: Solar Photon Sail Gold & Brass (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# Detail: Phosphor Mint Green HUD Optics & Targeting Reticles (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (140, 240, 165, 255)
MINT_SHINE = (210, 255, 225, 255)
MINT_DARK  = (36, 140, 62, 255)

# Warm Highlight: Coral Pink High-Pressure Silicone Seals & Dampers (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

# Deep Space Webbing Harness (Navy-Charcoal)
NAVY_HARNESS = (32, 45, 68, 255)
NAVY_LIGHT   = (60, 80, 115, 255)
NAVY_DARK    = (20, 28, 44, 255)

# Vulcanized Industrial Black Silicone Boots (#202026)
SILICONE_BASE  = (32, 32, 38, 255)
SILICONE_LIGHT = (65, 65, 78, 255)

# Stainless Steel Guideway Rails / Pins / Wire
STEEL_LIGHT = (195, 205, 220, 255)
STEEL_MID   = (130, 142, 160, 255)
STEEL_DARK  = (70, 78, 92, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL ORBIT RACCOON SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_raccoon_quad_solar_sail.png
    # Quad Solar Sail Wind-up Key (四葉光子太陽能翼板發條鑰匙)
    # Socket at upper spine (64, 62)
    # Key shaft extends up and right to hub at (86, 32)
    # 4 gold photon solar-sail vanes with micro photovoltaic grid lines & gear hub
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
    kd.ellipse([60, 58, 68, 66], fill=GOLD_DARK, outline=OUTLINE)
    kd.ellipse([61, 59, 67, 65], fill=GOLD_BASE)
    kd.ellipse([63, 61, 65, 63], fill=CORAL_BASE)

    # 2. Quad Solar Sail Vanes centered at (86, 32)
    kcx, kcy = 86.0, 32.0

    # 4 Solar photon sail vanes radiating outward symmetrically
    angles = [np.pi * 0.25, np.pi * 0.75, np.pi * 1.25, np.pi * 1.75]
    sail_length = 16.5
    sail_width = 8.5

    for angle in angles:
        # Sail center line
        cos_a = np.cos(angle)
        sin_a = np.sin(angle)
        norm_cos = -sin_a
        norm_sin = cos_a

        for dist in np.linspace(5.0, sail_length, 25):
            w_factor = 2.0 + (dist / sail_length) * (sail_width - 2.0)
            for w_off in np.linspace(-w_factor / 2.0, w_factor / 2.0, 15):
                px = kcx + dist * cos_a + w_off * norm_cos
                py = kcy + dist * sin_a + w_off * norm_sin
                ix, iy = int(px), int(py)
                if 0 <= ix < W and 0 <= iy < H:
                    norm_dist = abs(w_off) / (w_factor / 2.0)
                    is_border = (norm_dist >= 0.75 or dist >= sail_length - 1.2)
                    is_grid_line = (int(dist) % 4 == 0 or abs(w_off) < 0.6)

                    if is_border:
                        key_img.putpixel((ix, iy), GOLD_BASE)
                    elif is_grid_line:
                        key_img.putpixel((ix, iy), GOLD_DARK)
                    else:
                        # Deep photovoltaic blue-cyan cell with gold shine
                        spec = max(0.0, 1.0 - norm_dist)
                        r_v = int(np.clip(20 * (1 - spec) + 240 * spec, 0, 255))
                        g_v = int(np.clip(140 * (1 - spec) + 220 * spec, 0, 255))
                        b_v = int(np.clip(200 * (1 - spec) + 80 * spec, 0, 255))
                        key_img.putpixel((ix, iy), (r_v, g_v, b_v, 255))

    # 3. Central Gear Hub Boss at (86, 32)
    r_hub = 6.0
    for y in range(int(kcy - r_hub - 2), int(kcy + r_hub + 3)):
        for x in range(int(kcx - r_hub - 2), int(kcx + r_hub + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if dist <= r_hub:
                spec = max(0.0, 1.0 - dist / r_hub)
                shine = max(0.0, 1.0 - ((x - (kcx - 1.5))**2 + (y - (kcy - 1.5))**2)**0.5 / 3.0)**2
                r_h = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                g_h = int(np.clip(208 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                b_h = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                key_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Hub gear teeth
    for g_angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        gtx = int(kcx + (r_hub + 1.5) * np.cos(g_angle))
        gty = int(kcy + (r_hub + 1.5) * np.sin(g_angle))
        if 0 <= gtx < W and 0 <= gty < H:
            key_img.putpixel((gtx, gty), GOLD_LIGHT)

    # Core gemstone / solar battery eye
    kd.ellipse([int(kcx - 2.5), int(kcy - 2.5), int(kcx + 2.5), int(kcy + 2.5)], fill=CORAL_BASE, outline=OUTLINE)
    kd.point((int(kcx - 0.5), int(kcy - 0.5)), fill=WHITE_SHINE)

    apply_clean_outline(key_img)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Tail Layer)
    # File: back_curio/curio_raccoon_coaxial_ring_antenna_tail.png
    # Five-Segment Coaxial High-Voltage Discharge Ring Antenna Tail (五節同軸高壓放電環形天線長尾)
    # Extends from pelvis (52, 82) down-left to (28, 84), then curving up-left to tip at (20, 72)
    # 5 coaxial ring segments alternating conducting brass/gold rings and luminescent aqua/mint polymer insulators
    # Tip features spherical discharge terminal with micro antenna probe
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

    curve_pts = bezier_curve((52.0, 82.0), (38.0, 86.0), (24.0, 86.0), (20.0, 72.0), num_pts=60)

    # Core stainless steel spine wire
    for i in range(len(curve_pts) - 1):
        x0, y0 = curve_pts[i]
        x1, y1 = curve_pts[i+1]
        cd.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=STEEL_LIGHT, width=3)
        cd.line([(int(x0)-1, int(y0)), (int(x1)-1, int(y1))], fill=OUTLINE, width=1)
        cd.line([(int(x0)+1, int(y0)), (int(x1)+1, int(y1))], fill=OUTLINE, width=1)

    # 5 articulated coaxial cylindrical ring segments
    t_scales = np.linspace(0.12, 0.88, 5)
    scale_indices = [int(t * (len(curve_pts) - 1)) for t in t_scales]

    for i, idx in enumerate(scale_indices):
        rx_c, ry_c = curve_pts[idx]
        progress = i / 4.0
        # Tapering from base to tip
        r_scale_w = 7.5 - 1.8 * progress
        r_scale_h = 5.2 - 1.2 * progress

        p_prev = curve_pts[max(0, idx - 2)]
        p_next = curve_pts[min(len(curve_pts) - 1, idx + 2)]
        tangent_angle = np.arctan2(p_next[1] - p_prev[1], p_next[0] - p_prev[0])
        normal_angle = tangent_angle + np.pi / 2.0

        is_gold_ring = (i % 2 == 0)

        for y_off in np.linspace(-r_scale_h, r_scale_h, 13):
            for x_off in np.linspace(-r_scale_w, r_scale_w, 15):
                if (x_off / r_scale_w)**2 + (y_off / r_scale_h)**2 <= 1.0:
                    px = rx_c + x_off * np.cos(normal_angle) + y_off * np.cos(tangent_angle)
                    py = ry_c + x_off * np.sin(normal_angle) + y_off * np.sin(tangent_angle)
                    ix, iy = int(px), int(py)
                    if 0 <= ix < W and 0 <= iy < H:
                        spec = max(0.0, 1.0 - ((x_off**2 + y_off**2)**0.5) / r_scale_w)
                        shine = max(0.0, 1.0 - (x_off**2 + (y_off - 1)**2)**0.5 / 2.5)**2

                        if is_gold_ring:
                            # Conducting Brass / Gold Ring Segment
                            r_sc = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                            g_sc = int(np.clip(208 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                            b_sc = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                        else:
                            # Luminescent Electric Aqua / Mint Polymer Insulator Ring
                            r_sc = int(np.clip(0 * (1 - spec) + 70 * spec + 30 * shine, 0, 255))
                            g_sc = int(np.clip(194 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                            b_sc = int(np.clip(203 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))

                        curio_img.putpixel((ix, iy), (r_sc, g_sc, b_sc, 255))

        # Brass hinge pivot rivet
        cd.ellipse([int(rx_c - 1.5), int(ry_c - 1.5), int(rx_c + 1.5), int(ry_c + 1.5)], fill=GOLD_BASE, outline=OUTLINE)
        cd.point((int(rx_c), int(ry_c)), fill=WHITE_SHINE)

    # Spherical discharge terminal electrode at tail tip (20, 72)
    tip_x, tip_y = 20.0, 72.0
    cd.ellipse([int(tip_x - 3.5), int(tip_y - 3.5), int(tip_x + 3.5), int(tip_y + 3.5)], fill=GOLD_BASE, outline=OUTLINE)
    cd.ellipse([int(tip_x - 1.5), int(tip_y - 1.5), int(tip_x + 1.5), int(tip_y + 1.5)], fill=MINT_BASE)
    cd.point((int(tip_x - 0.5), int(tip_y - 0.5)), fill=WHITE_SHINE)

    # Micro antenna needle probe at tip
    cd.line([(int(tip_x), int(tip_y)), (int(tip_x - 3), int(tip_y - 6))], fill=STEEL_LIGHT, width=2)
    cd.ellipse([int(tip_x - 4), int(tip_y - 8), int(tip_x - 2), int(tip_y - 6)], fill=CORAL_BASE, outline=OUTLINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_raccoon_orbit_aqua_default.png
    # Features:
    # - 2.0~2.2 Chibi aerospace zero-G stance
    # - Soft ground contact shadow at (64, 116)
    # - Heavy-duty vulcanized black silicone boots (#202026) with magnetic suction treads
    # - Articulated legs with electric aqua polymer plates & coral pink dampeners
    # - Electric Orbit Aqua (#00C2CB) body hull with multi-tone depth
    # - Ivory White (#FFFDF8) enamel chest & belly shock-absorbing plate
    # - Left hand forward/raised balancing palm at (38, 86)
    # - Right hand tucked at ribs at (83, 75)
    # - STRICT ZERO pixels in outer weapon zone (x >= 94) for 0-ART9 / 0-ART11
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Vulcanized Silicone Magnetic Boots
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
                r_l = int(np.clip(0 * (0.8 + 0.35 * spec) + 50 * spec, 0, 255))
                g_l = int(np.clip(194 * (0.8 + 0.35 * spec) + 35 * spec, 0, 255))
                b_l = int(np.clip(203 * (0.8 + 0.35 * spec) + 45 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 2, mid_x + 3, mid_y + 2], fill=CORAL_BASE, outline=OUTLINE)
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

                # Ivory enamel shock-absorbing chest & belly plate
                is_chest_plate = ((x - 63.0)**2 / 10.5**2 + (y - 75.0)**2 / 11.0**2 <= 1.0)
                if is_chest_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    # Electric Orbit Aqua High-Impact Polymer Hull
                    r_t = int(np.clip(0 * (0.75 + 0.45 * spec) + 50 * spec - 15 * edge_shade + 60 * shine, 0, 255))
                    g_t = int(np.clip(194 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_t = int(np.clip(203 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center mini energy solar gauge at (63, 75)
    ch_d.ellipse([60, 72, 66, 78], fill=OUTLINE)
    ch_d.ellipse([61, 73, 65, 77], fill=MINT_BASE)
    ch_d.point((62, 74), fill=MINT_SHINE)

    # Silicone pressure damper seam across mid-torso
    ch_d.arc([46, 68, 80, 88], start=20, end=160, fill=CORAL_BASE, width=1)

    # 5. Left Arm & Raised Balancing Palm
    ch_d.line([(48, 73), (38, 86)], fill=AQUA_LIGHT, width=4)
    ch_d.ellipse([34, 84, 41, 91], fill=AQUA_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 86, 39, 89], fill=GOLD_BASE)

    # 6. Right Arm & Grip Hub (tucked at ribs)
    ch_d.line([(74, 72), (83, 75)], fill=AQUA_LIGHT, width=4)
    ch_d.ellipse([80, 73, 86, 79], fill=AQUA_BASE, outline=OUTLINE)
    ch_d.point((83, 76), fill=GOLD_BASE)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_raccoon_parabolic_radar_dish.png
    # Features:
    # - Spherical Electric Aqua Polymer Helmet Dome at (64, 44), rx=18.5, ry=15.5
    # - Ivory White (#FFFDF8) enamel muzzle and cheek plates
    # - Forehead miniature brass venting plate at (64, 32)
    # - Pair of 360-degree parabolic radar dish ears with brass rings at (44, 26) and (84, 26)
    # - 6 micro stainless steel signal sensor whiskers (左右各三根)
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Electric Aqua & Ivory Muzzle)
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
                    r_h = int(np.clip(0 * (0.75 + 0.45 * spec) + 50 * spec - 15 * edge_shade + 60 * shine, 0, 255))
                    g_h = int(np.clip(194 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_h = int(np.clip(203 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Threaded snout and mouth seam
    hd.polygon([(62, 47), (66, 47), (64, 49)], fill=OUTLINE)
    hd.line([(64, 49), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([60, 50, 64, 54], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 50, 68, 54], start=0, end=180, fill=OUTLINE, width=1)

    # Forehead Vent / Sensor Plate at (64, 32)
    hd.ellipse([61, 30, 67, 34], fill=GOLD_BASE, outline=OUTLINE)
    hd.ellipse([62, 31, 66, 33], fill=CORAL_BASE)
    hd.point((64, 32), fill=WHITE_SHINE)

    # 2. Dual Parabolic Radar Dish Ears at (44, 26) and (84, 26)
    ear_positions = [(44, 26), (84, 26)]
    for ex, ey in ear_positions:
        # Outer parabolic dish
        hd.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=GOLD_BASE, outline=OUTLINE)
        hd.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=AQUA_DEEP)
        # Center feed-horn antenna pin
        hd.ellipse([ex - 1.5, ey - 1.5, ex + 1.5, ey + 1.5], fill=CORAL_BASE)
        hd.point((ex, ey), fill=WHITE_SHINE)

    # 3. 6 Micro Stainless Steel Signal Sensor Whiskers
    whisker_lines = [
        ([(47, 46), (32, 44)], [(46, 48), (30, 48)], [(47, 50), (33, 53)]),
        ([(81, 46), (96, 44)], [(82, 48), (98, 48)], [(81, 50), (95, 53)])
    ]
    for w_group in whisker_lines:
        for w_pts in w_group:
            hd.line(w_pts, fill=STEEL_LIGHT, width=1)

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
    # File: optic_core/face_raccoon_hud_polarizer_visor.png
    # Features:
    # - Deep Space Polycarbonate Visor across eye zone
    # - Dual 22px-scale Phosphor-Green Targeting Reticles at (52, 40) and (76, 40)
    # - Glowing mint core (#4ED86A) with alpha == 255 at center (0-ART27 compliant)
    # - White specular glints
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    # Polycarbonate dark visor shield across eye region
    for y in range(35, 46):
        for x in range(45, 84):
            dx = (x - 64.0) / 18.0
            dy = (y - 40.0) / 5.5
            if dx**2 + dy**2 <= 1.0:
                core_img.putpixel((x, y), (21, 27, 46, 210))

    # Dual glowing mint targeting reticles
    for ecx, ecy in eye_centers:
        r_lens = 4.2
        for y in range(int(ecy - r_lens - 2), int(ecy + r_lens + 3)):
            for x in range(int(ecx - r_lens - 2), int(ecx + r_lens + 3)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    spec = max(0.0, 1.0 - dist / r_lens)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.5))**2 + (y - (ecy - 1.5))**2)**0.5 / 2.0)**2
                    # Targeting concentric circle reticle
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
    # File: costume/costume_raccoon_space_explorer_harness.png
    # Features:
    # - Space Explorer Harness (星穹宇航探險工裝背帶)
    # - Navy webbing straps with brass buckles & coral pink pads
    # - Center pressure release valve
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
                    r_v = int(np.clip(32 * (0.8 + 0.4 * spec), 0, 255))
                    g_v = int(np.clip(45 * (0.8 + 0.4 * spec), 0, 255))
                    b_v = int(np.clip(68 * (0.8 + 0.4 * spec), 0, 255))
                    costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Center brass buckle
    cos_d.ellipse([60, 71, 66, 77], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([62, 73, 64, 75], fill=CORAL_BASE)

    # Rivets on belt
    for rx in [52, 57, 69, 74]:
        cos_d.ellipse([rx - 1, 81, rx + 1, 83], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.point((rx, 82), fill=WHITE_SHINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_raccoon_anti_gravity_pulse_blaster.png
    # Features:
    # - Anti-Gravity Pulse Blaster (反重力脈衝光銃)
    # - Right-hand single held (0-MKT7 compliant) at (84, 75)
    # - Electric Aqua Polymer Receiver & Coil Barrel
    # - Induction coil rings (x=98, 105, 112)
    # - Coral pink muzzle aperture ring at (118, 75) with mint optical emitter
    # - Top sighting heat sink rail
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Grip Socket at (84, 75)
    wd.ellipse([81, 72, 87, 78], fill=AQUA_BASE, outline=OUTLINE)
    wd.ellipse([82, 73, 86, 77], fill=AQUA_LIGHT)
    wd.point((84, 75), fill=GOLD_BASE)

    # 2. Main Receiver Body (x: 84..95, y: 71..80)
    for y in range(71, 81):
        for x in range(84, 96):
            spec = max(0.0, 1.0 - ((x - 88)**2 + (y - 74)**2)**0.5 / 6.0)
            r_w = int(np.clip(0 * (0.8 + 0.3 * spec) + 50 * spec, 0, 255))
            g_w = int(np.clip(194 * (0.8 + 0.3 * spec) + 35 * spec, 0, 255))
            b_w = int(np.clip(203 * (0.8 + 0.3 * spec) + 45 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Power cell indicator window on receiver
    wd.ellipse([88, 73, 92, 77], fill=OUTLINE)
    wd.ellipse([89, 74, 91, 76], fill=MINT_BASE)

    # 3. Horizontal Pulse Barrel (x: 95..118, y: 73..77)
    for y in range(73, 78):
        for x in range(95, 119):
            spec = max(0.0, 1.0 - abs(y - 75) / 2.5)
            r_b = int(np.clip(195 * (0.8 + 0.3 * spec), 0, 255))
            g_b = int(np.clip(205 * (0.8 + 0.3 * spec), 0, 255))
            b_b = int(np.clip(220 * (0.8 + 0.3 * spec), 0, 255))
            weapon_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # 4. Magnetic Induction Coil Rings around barrel
    for coil_x in [98, 105, 112]:
        wd.ellipse([coil_x - 1, 71, coil_x + 1, 79], fill=GOLD_BASE, outline=OUTLINE)
        wd.point((coil_x, 72), fill=WHITE_SHINE)

    # 5. Top Sighting Rail / Heat Sink Fin
    wd.line([(87, 70), (114, 70)], fill=STEEL_LIGHT, width=2)
    wd.point((114, 69), fill=MINT_BASE)

    # 6. Muzzle Aperture Vent Ring at (118, 75)
    wd.ellipse([117, 72, 120, 78], fill=CORAL_BASE, outline=OUTLINE)
    wd.ellipse([118, 73, 119, 77], fill=MINT_BASE)
    wd.point((119, 75), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 AND 512x512 LANCZOS SLICES
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_raccoon_quad_solar_sail", key_img),
        ("back_curio", "curio_raccoon_coaxial_ring_antenna_tail", curio_img),
        ("chassis", "chassis_raccoon_orbit_aqua_default", chassis_img),
        ("head_unit", "head_raccoon_parabolic_radar_dish", head_img),
        ("optic_core", "face_raccoon_hud_polarizer_visor", core_img),
        ("costume", "costume_raccoon_space_explorer_harness", costume_img),
        ("weapon", "weapon_raccoon_anti_gravity_pulse_blaster", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{RACCOON_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{RACCOON_PD_DIR}/winding_key/key_raccoon_quad_solar_sail.png",
                    f"{KEY_DIR}/key_raccoon_quad_solar_sail.png")
    shutil.copyfile(f"{RACCOON_PD_DIR}/weapon/weapon_raccoon_anti_gravity_pulse_blaster.png",
                    f"{WEAPON_DIR}/weapon_raccoon_anti_gravity_pulse_blaster.png")
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

    proof_comp = f"{RACCOON_PD_DIR}/proof_paperdoll_raccoon_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{RACCOON_PD_DIR}/proof_paperdoll_raccoon_magenta.png"
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

    strip_path = f"{RACCOON_PD_DIR}/proof_raccoon_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/raccoon_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/raccoon_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
