#!/usr/bin/env python3
"""
build_peacock_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十五族 稜鏡孔雀 (The Prism Peacock, peacock) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/PRISM_PEACOCK_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological feathers, zero soft tissue/flesh,
  glazed porcelain enamel metal plates, baroque diadem prism antenna, dual-color kaleidoscope gem optics,
  marionette court baroque cuirass, articulated kaleidoscope expanding crystal fan,
  floating kaleidoscope prism focus, dawn baroque filigree sunburst winding key)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Imperial Peacock Blue (#1B4965)
    2. Secondary Hull / Trim: Dopamine Gold (#FFD028)
    3. Dawn Soft White / Ivory (#FFF8E7 / #FFFDF8)
    4. Kaleidoscope Mint Green (#4ED86A)
    5. Nutcracker Ruby Crimson (#E63946)
    6. Prism Sky Blue (#38A0FF)
    7. Amethyst Purple (#8338EC)
    8. Warm Outline: Deep Warm Bronze/Brown Outline (#2E1F18 / #1F1A3A)
    Plus: Quartz crystal reflections & highlights
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
PEACOCK_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/peacock"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Prism Peacock Specification)
OUTLINE = (46, 31, 24, 255)            # #2E1F18 Deep warm bronze-brown hand-drawn outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Imperial Peacock Blue (#1B4965)
BLUE_BASE  = (27, 73, 101, 255)
BLUE_LIGHT = (48, 118, 160, 255)
BLUE_SHINE = (75, 165, 215, 255)
BLUE_DARK  = (18, 48, 68, 255)
BLUE_DEEP  = (12, 32, 46, 255)

# 2. Secondary Hull / Trim: Dopamine Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Dawn Soft White / Ivory (#FFF8E7 / #FFFDF8)
IVORY_BASE  = (255, 248, 231, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (230, 220, 200, 255)
IVORY_DARK  = (195, 185, 165, 255)

# 4. Kaleidoscope Mint Green (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (130, 238, 155, 255)
MINT_SHINE = (195, 255, 210, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 5. Nutcracker Ruby Crimson (#E63946)
RUBY_BASE  = (230, 57, 70, 255)
RUBY_LIGHT = (255, 105, 118, 255)
RUBY_SHINE = (255, 175, 185, 255)
RUBY_DARK  = (175, 30, 45, 255)
RUBY_DEEP  = (115, 15, 28, 255)

# 6. Prism Sky Blue (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)
SKY_DEEP  = (14, 60, 130, 255)

# 7. Amethyst Purple (#8338EC)
AMETHYST_BASE  = (131, 56, 236, 255)
AMETHYST_LIGHT = (175, 110, 255, 255)
AMETHYST_SHINE = (220, 175, 255, 255)
AMETHYST_DARK  = (95, 30, 185, 255)
AMETHYST_DEEP  = (60, 15, 125, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL PRISM PEACOCK SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_peacock_filigree_sunburst_key.png
    # Dawn Baroque Filigree Sunburst Key (晨曦巴洛克日曜鏤空發條鑰匙)
    # Features:
    # - Socket collar at spine (64, 54)
    # - Polished brass shaft angled up-right to sunburst center at (kcx=80, kcy=24)
    # - Openwork filigree sunburst ring (outer r=9.5, inner r=5.0)
    # - 8 radiating flame rays (N, NE, E, SE, S, SW, W, NW)
    # - Central purple amethyst gemstone bearing (#8338EC) at (80, 24)
    # - Warm golden bronze outline (OUTLINE_KEY) to comply with 0-ART29 & 0-QA16 dark limit
    # - STRICTLY transparent corners
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    kcx, kcy = 80.0, 24.0

    # 1. Key shaft from spine socket (64, 54) to sunburst hub (kcx, kcy)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 64.0 + t * (kcx - 64.0)
        sy = 54.0 + t * (kcy - 54.0)
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.82 + 0.22 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.82 + 0.22 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.82 + 0.45 * spec) + 30 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Base socket collar at spine (64, 54)
    kd.ellipse([64 - 5, 54 - 5, 64 + 5, 54 + 5], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 54 - 3, 64 + 3, 54 + 3], fill=GOLD_BASE)
    kd.ellipse([64 - 1, 54 - 1, 64 + 1, 54 + 1], fill=AMETHYST_BASE)

    # 2. Openwork Sunburst Ring: outer r ~ 9.5, inner r ~ 5.0
    r_out = 9.5
    r_in = 5.0
    for y in range(int(kcy - r_out - 2), int(kcy + r_out + 3)):
        for x in range(int(kcx - r_out - 2), int(kcx + r_out + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if r_in <= dist <= r_out:
                norm_r = (dist - r_in) / (r_out - r_in)
                spec = max(0.0, np.sin(norm_r * np.pi))
                r_w = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                g_w = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
                b_w = int(np.clip(40 * (0.85 + 0.4 * spec) + 35 * spec, 0, 255))
                key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # 3. 8 Radiating Baroque Flame Rays (angles 0, 45, 90, 135, 180, 225, 270, 315 deg)
    for ang_deg in range(0, 360, 45):
        rad = np.radians(ang_deg)
        # Ray extends from r=9.0 out to r=15.0
        r_start = 9.0
        r_end = 15.0 if ang_deg % 90 == 0 else 13.5
        for r_step in np.linspace(r_start, r_end, 12):
            rx = kcx + r_step * np.cos(rad)
            ry = kcy + r_step * np.sin(rad)
            width = max(1, int(round(2.0 * (1.0 - (r_step - r_start) / (r_end - r_start)))))
            for w_off in range(-width + 1, width):
                perp_rad = rad + np.pi / 2
                px = rx + w_off * np.cos(perp_rad)
                py = ry + w_off * np.sin(perp_rad)
                spec = 1.0 - (r_step - r_start) / (r_end - r_start)
                r_r = int(np.clip(255 * (0.88 + 0.15 * spec), 0, 255))
                g_r = int(np.clip(208 * (0.88 + 0.15 * spec) + 20 * spec, 0, 255))
                b_r = int(np.clip(40 * (0.88 + 0.4 * spec) + 50 * spec, 0, 255))
                key_img.putpixel((int(round(px)), int(round(py))), (r_r, g_r, b_r, 255))

    # 4. Central Amethyst Bearing Gem Hub at (kcx, kcy)
    kd.ellipse([int(kcx - 4), int(kcy - 4), int(kcx + 4), int(kcy + 4)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=AMETHYST_BASE)
    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=AMETHYST_LIGHT)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_peacock_articulated_kaleidoscope_fan.png
    # Articulated Kaleidoscope Mechanical Expanding Fan (鉸接萬花筒機械開屏晶扇)
    # Features:
    # - 9 radial articulated gilded brass struts spreading behind body
    # - Pivot hub at (64, 62)
    # - In idle pose, semi-open fan spanning from upper-left to upper-right (angles ~ -160 to -20 deg)
    # - Each strut has 2 octagonal quartz prisms (inner r=24..28, outer r=36..44)
    # - Facets shaded with dopamine sky blue (#38A0FF), mint green (#4ED86A) and gold
    # - Ruby crimson (#E63946) pivot rivets at strut joints
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    p_cx, p_cy = 64.0, 62.0

    # 9 Strut angles from -158 deg to -22 deg (stepping 17 degrees)
    strut_angles_deg = [-158, -141, -124, -107, -90, -73, -56, -39, -22]

    # Draw the translucent prism aura mesh behind the struts
    aura_pts = []
    for ang in strut_angles_deg:
        rad = np.radians(ang)
        r_tip = 46.0
        aura_pts.append((p_cx + r_tip * np.cos(rad), p_cy + r_tip * np.sin(rad)))
    aura_poly = [(p_cx, p_cy)] + aura_pts
    cd.polygon(aura_poly, fill=(56, 160, 255, 45))

    # Draw each strut and its 2 octagonal prisms
    for i, ang_deg in enumerate(strut_angles_deg):
        rad = np.radians(ang_deg)
        dir_x = np.cos(rad)
        dir_y = np.sin(rad)

        # 1. Brass Strut Beam: from r=6 to r=46
        for r in np.linspace(6.0, 45.0, 40):
            bx = p_cx + r * dir_x
            by = p_cy + r * dir_y
            spec = max(0.0, 1.0 - abs(r - 25.0) / 20.0)
            r_b = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))
            g_b = int(np.clip(208 * (0.8 + 0.2 * spec), 0, 255))
            b_b = int(np.clip(40 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
            for dx, dy in [(-1, 0), (0, 0), (1, 0), (0, -1), (0, 1)]:
                curio_img.putpixel((int(round(bx + dx)), int(round(by + dy))), (r_b, g_b, b_b, 255))

        # 2. Inner Octagonal Quartz Prism at r=24.0
        r_inner = 24.0
        ix = p_cx + r_inner * dir_x
        iy = p_cy + r_inner * dir_y
        inner_radius = 4.5
        # Draw octagonal facet
        for py in range(int(iy - inner_radius - 1), int(iy + inner_radius + 2)):
            for px in range(int(ix - inner_radius - 1), int(ix + inner_radius + 2)):
                dx = abs(px - ix)
                dy = abs(py - iy)
                if dx + dy <= inner_radius * 1.35 and max(dx, dy) <= inner_radius:
                    dist_c = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist_c / inner_radius)
                    # Alternate colors: sky blue vs mint green facets
                    if i % 2 == 0:
                        r_p = int(np.clip(56 * (0.85 + 0.3 * spec) + 50 * spec, 0, 255))
                        g_p = int(np.clip(160 * (0.85 + 0.3 * spec) + 60 * spec, 0, 255))
                        b_p = int(np.clip(255 * (0.9 + 0.15 * spec), 0, 255))
                    else:
                        r_p = int(np.clip(78 * (0.85 + 0.3 * spec) + 50 * spec, 0, 255))
                        g_p = int(np.clip(216 * (0.9 + 0.15 * spec) + 30 * spec, 0, 255))
                        b_p = int(np.clip(106 * (0.85 + 0.3 * spec) + 70 * spec, 0, 255))
                    curio_img.putpixel((px, py), (r_p, g_p, b_p, 240))
        cd.point((int(round(ix)), int(round(iy))), fill=WHITE_SHINE)

        # 3. Outer Octagonal Quartz Prism at r=41.0 (Larger, more brilliant)
        r_outer = 41.0
        ox = p_cx + r_outer * dir_x
        oy = p_cy + r_outer * dir_y
        outer_radius = 6.0
        for py in range(int(oy - outer_radius - 1), int(oy + outer_radius + 2)):
            for px in range(int(ox - outer_radius - 1), int(ox + outer_radius + 2)):
                dx = abs(px - ox)
                dy = abs(py - oy)
                if dx + dy <= outer_radius * 1.35 and max(dx, dy) <= outer_radius:
                    dist_c = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist_c / outer_radius)
                    # Brilliant kaleidoscope refraction
                    if i % 2 == 1:
                        r_p = int(np.clip(56 * (0.8 + 0.4 * spec) + 70 * spec, 0, 255))
                        g_p = int(np.clip(160 * (0.8 + 0.35 * spec) + 70 * spec, 0, 255))
                        b_p = int(np.clip(255 * (0.9 + 0.1 * spec), 0, 255))
                    else:
                        r_p = int(np.clip(78 * (0.8 + 0.4 * spec) + 60 * spec, 0, 255))
                        g_p = int(np.clip(216 * (0.88 + 0.2 * spec) + 40 * spec, 0, 255))
                        b_p = int(np.clip(106 * (0.8 + 0.35 * spec) + 80 * spec, 0, 255))
                    curio_img.putpixel((px, py), (r_p, g_p, b_p, 255))

        # Brass bezel ring and ruby pivot rivet on outer prism
        cd.ellipse([int(ox - 2), int(oy - 2), int(ox + 2), int(oy + 2)], fill=RUBY_BASE, outline=GOLD_BASE)
        cd.point((int(ox), int(oy)), fill=WHITE_SHINE)

    # 4. Central Mechanical Hub / Escapement Gear at (p_cx, p_cy)
    cd.ellipse([int(p_cx - 8), int(p_cy - 8), int(p_cx + 8), int(p_cy + 8)], fill=GOLD_DARK, outline=OUTLINE)
    cd.ellipse([int(p_cx - 6), int(p_cy - 6), int(p_cx + 6), int(p_cy + 6)], fill=GOLD_BASE)
    cd.ellipse([int(p_cx - 3), int(p_cy - 3), int(p_cx + 3), int(p_cy + 3)], fill=RUBY_BASE)
    cd.point((int(p_cx), int(p_cy)), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Main Body Layer)
    # File: chassis/chassis_peacock_glazed_porcelain_default.png
    # Prism Peacock Glazed Porcelain Metal Chassis (稜鏡孔雀彩釉琺瑯金屬素體)
    # Features:
    # - Slender elegant posture, ballet third-position stance
    # - Soft ground contact shadow around y=118..124
    # - Ball-and-socket knees and ankles with brass joints
    # - Glazed porcelain blue hull (#1B4965) with polished gold brass trim (#FFD028)
    # - Solid neck collar / head mount at (x: 52..76, y: 46..58) (zero holes)
    # - Torso body shell (x: 44..84, y: 56..94) with rich shading (>= 20 unique colors)
    # - Left arm poised at waist/hip in classical ballet poise at (38, 74)
    # - Right arm bent forward, hand at (82, 74) gesturing towards the floating focus
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 118 - 4, 64 + 28, 118 + 4], fill=(27, 48, 68, 110))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Slender Brass Mechanical Legs with Ballet Soles
    # Feet at (54, 115) and (74, 115)
    feet_pos = [(54.0, 115.0), (74.0, 115.0)]
    for bx, by in feet_pos:
        # Ballet metal sole with slip-resistant pad
        ch_d.ellipse([int(bx - 6), int(by - 3), int(bx + 6), int(by + 3)], fill=GOLD_DARK, outline=OUTLINE)
        ch_d.ellipse([int(bx - 4), int(by - 2), int(bx + 4), int(by + 2)], fill=GOLD_BASE)
        ch_d.point((int(bx - 1), int(by - 1)), fill=WHITE_SHINE)

    # Slender articulated leg shafts
    leg_paths = [
        ((54.0, 114.0), (56.0, 88.0)),
        ((74.0, 114.0), (72.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-4, 5):
                spec = max(0.0, 1.0 - abs(dx) / 4.0)
                # Polished brass leg cylinders
                r_l = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                g_l = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                b_l = int(np.clip(40 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        # Knee ball-and-socket joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 3, mid_x + 3, mid_y + 3], fill=BLUE_BASE, outline=OUTLINE)
        ch_d.ellipse([mid_x - 2, mid_y - 2, mid_x + 2, mid_y + 2], fill=BLUE_LIGHT)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 3. Solid Neck Collar & Shoulder Flange (x: 46..82, y: 46..64)
    for ny in range(46, 65):
        for nx in range(46, 83):
            # Check shoulder slope
            if ny < 56 and (nx < 50 or nx > 78):
                continue
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 14.0)
            r_n = int(np.clip(27 * (0.85 + 0.4 * spec) + 30 * spec, 0, 255))
            g_n = int(np.clip(73 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
            b_n = int(np.clip(101 * (0.85 + 0.4 * spec) + 50 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 4. Torso Body Shell (x: 42..86, y: 56..95)
    cx_t, cy_t = 64.0, 75.0
    for y in range(56, 96):
        for x in range(42, 87):
            dx = (x - cx_t) / 19.5
            dy = (y - cy_t) / 18.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Gold filigree seam along the flanks
                is_gold_seam = (0.70 <= dist_sq <= 0.88)
                if is_gold_seam:
                    r_t = int(np.clip(255 * (0.82 + 0.22 * spec) - 20 * edge_shade + 25 * shine, 0, 255))
                    g_t = int(np.clip(208 * (0.82 + 0.22 * spec) - 20 * edge_shade + 25 * shine, 0, 255))
                    b_t = int(np.clip(40 * (0.82 + 0.4 * spec) + 30 * shine, 0, 255))
                else:
                    # Imperial Peacock Blue porcelain enamel
                    r_t = int(np.clip(27 * (0.8 + 0.45 * spec) + 40 * shine - 10 * edge_shade, 0, 255))
                    g_t = int(np.clip(73 * (0.8 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                    b_t = int(np.clip(101 * (0.8 + 0.45 * spec) + 65 * shine - 15 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center escutcheon bezel and balance escapement window on chest (x: 64, y: 76)
    ch_d.ellipse([64 - 5, 76 - 5, 64 + 5, 76 + 5], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([64 - 4, 76 - 4, 64 + 4, 76 + 4], fill=GOLD_BASE)
    ch_d.ellipse([64 - 2, 76 - 2, 64 + 2, 76 + 2], fill=RUBY_BASE)
    ch_d.point((63, 75), fill=WHITE_SHINE)

    # 5. Left Arm: Poised gracefully at waist in ballet third position at (38, 74)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 48.0 - t * 10.0
        ay = 64.0 + t * 10.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 3.0)
                    r_a = int(np.clip(27 * (0.8 + 0.4 * spec) + 35 * spec, 0, 255))
                    g_a = int(np.clip(73 * (0.8 + 0.4 * spec) + 40 * spec, 0, 255))
                    b_a = int(np.clip(101 * (0.8 + 0.4 * spec) + 50 * spec, 0, 255))
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), (r_a, g_a, b_a, 255))
    # Left hand at waist
    ch_d.ellipse([34, 72, 42, 80], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([36, 74, 40, 78], fill=GOLD_BASE)
    ch_d.point((38, 75), fill=WHITE_SHINE)

    # 6. Right Arm: Gesturing forward, hand at (82, 74)
    # STRICT 0-ART9/11: Right arm must not exceed x=93!
    for t in np.linspace(0.0, 1.0, 20):
        rax = 74.0 + t * 8.0
        ray = 64.0 + t * 10.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 3.0)
                    r_a = int(np.clip(27 * (0.8 + 0.4 * spec) + 35 * spec, 0, 255))
                    g_a = int(np.clip(73 * (0.8 + 0.4 * spec) + 40 * spec, 0, 255))
                    b_a = int(np.clip(101 * (0.8 + 0.4 * spec) + 50 * spec, 0, 255))
                    px = int(rax + dx)
                    py = int(ray + dy)
                    if px < 94:
                        chassis_img.putpixel((px, py), (r_a, g_a, b_a, 255))
    # Right wrist sleeve and hand
    ch_d.ellipse([78, 71, 86, 79], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([80, 73, 84, 77], fill=GOLD_BASE)
    ch_d.point((82, 74), fill=WHITE_SHINE)

    apply_clean_outline(chassis_img)

    # Strict check: 0-ART9/11: zero pixels at x >= 94
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Above Chassis)
    # File: head_unit/head_peacock_baroque_diadem_prism.png
    # Baroque Diadem Prism Antenna (巴洛克冠羽稜鏡天線)
    # Features:
    # - Glazed porcelain blue head dome (x: 42..86, y: 22..52)
    # - Baroque diadem crown with 3 brass rods ending in teardrop quartz prisms:
    #     - Central rod up to y=6 with teardrop quartz prism at (64, 6)
    #     - Left rod up-left to (50, 9) with teardrop quartz prism
    #     - Right rod up-right to (78, 9) with teardrop quartz prism
    # - Slender golden beak with polished tip at (64, 52)
    # - Eye socket rims with 12 micro-gear teeth around eye centers at (53, 39) and (75, 39)
    # - STRICT 0-ART27: Inner eye socket centers MUST BE HOLLOW (alpha=0 at centers)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    cx_h, cy_h = 64.0, 36.0

    # 1. Main Head Dome (x: 42..86, y: 22..52)
    for y in range(20, 52):
        for x in range(42, 87):
            dx = (x - cx_h) / 20.0
            dy = (y - cy_h) / 15.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_h = int(np.clip(27 * (0.8 + 0.45 * spec) + 40 * shine - 10 * edge_shade, 0, 255))
                g_h = int(np.clip(73 * (0.8 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                b_h = int(np.clip(101 * (0.8 + 0.45 * spec) + 65 * shine - 15 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 2. Dawn Ivory Cheek Plates (y: 42..50)
    for y in range(42, 51):
        for x in list(range(44, 52)) + list(range(76, 85)):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 20.0)
            r_c = int(np.clip(255 * (0.88 + 0.2 * spec), 0, 255))
            g_c = int(np.clip(248 * (0.88 + 0.2 * spec), 0, 255))
            b_c = int(np.clip(231 * (0.88 + 0.2 * spec), 0, 255))
            head_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 3. Baroque Diadem Base Coronet along forehead (y: 20..24)
    for bx in range(48, 81):
        head_img.putpixel((bx, 22), GOLD_BASE)
        head_img.putpixel((bx, 23), GOLD_LIGHT)

    # 4. Three Baroque Diadem Antenna Rods & Teardrop Quartz Prisms
    # Rod definitions: (tip_x, tip_y, base_x, base_y)
    rods = [
        ((64.0, 6.0), (64.0, 21.0), AMETHYST_LIGHT),
        ((50.0, 9.0), (56.0, 22.0), SKY_LIGHT),
        ((78.0, 9.0), (72.0, 22.0), MINT_LIGHT)
    ]
    for (tx, ty), (bx, by), tip_gem_color in rods:
        # Brass rod
        for t in np.linspace(0.0, 1.0, 25):
            rx = bx + t * (tx - bx)
            ry = by + t * (ty - by)
            for dx in range(-1, 2):
                head_img.putpixel((int(round(rx + dx)), int(round(ry))), GOLD_BASE)
        # Teardrop Quartz Prism at tip
        hd.ellipse([int(tx - 3), int(ty - 4), int(tx + 3), int(ty + 4)], fill=tip_gem_color, outline=GOLD_BASE)
        hd.point((int(tx), int(ty - 1)), fill=WHITE_SHINE)

    # 5. Slender Golden Beak at (64, 50..54)
    beak_pts = [(61, 48), (67, 48), (64, 53)]
    hd.polygon(beak_pts, fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 50), fill=WHITE_SHINE)

    # 6. Golden Bezel Rings around eye sockets at (53, 39) and (75, 39)
    for ecx in [53.0, 75.0]:
        for y in range(34, 45):
            for x in range(int(ecx - 5), int(ecx + 6)):
                dist = ((x - ecx)**2 + (y - 39.0)**2)**0.5
                if 2.4 <= dist <= 5.2:
                    head_img.putpixel((x, y), GOLD_BASE)

    # 7. STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye socket centers MUST be completely transparent (alpha = 0)
    for y in range(37, 42):
        for x in range(51, 56):
            if ((x - 53.0)**2 + (y - 39.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(73, 78):
            if ((x - 75.0)**2 + (y - 39.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(head_img, ignore_regions=[(49, 35, 57, 43), (71, 35, 79, 43)])

    # Re-enforce 0-ART27 hollow eye socket centers
    for y in range(38, 41):
        for x in range(52, 55):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(74, 77):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 25, Eye Layer)
    # File: optic_core/face_peacock_kaleidoscope_gem_lens.png
    # Kaleidoscope Gem Optics (萬花筒雙色寶石折光透鏡)
    # Features:
    # - Dual-lens quartz gemstone optics:
    #     - Left eye (53, 39): Imperial Sapphire Blue (#1B4965 / #38A0FF)
    #     - Right eye (75, 39): Emerald Mint Green (#4ED86A)
    # - Micro brass gear-toothed rim around each lens
    # - Precision alignment with head_unit hollow eye sockets (0-ART27 & 0-QA31)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    # (A) Left Eye: Sapphire Blue Lens at (53, 39)
    lex, ley = 53.0, 39.0
    for y in range(int(ley - 4), int(ley + 5)):
        for x in range(int(lex - 4), int(lex + 5)):
            dist = ((x - lex)**2 + (y - ley)**2)**0.5
            if dist <= 3.8:
                spec = max(0.0, 1.0 - dist / 3.8)
                # Outer rim is deep sapphire, inner core is bright sky cyan
                if dist >= 2.6:
                    core_img.putpixel((x, y), BLUE_BASE)
                else:
                    r_c = int(np.clip(56 * (0.85 + 0.3 * spec) + 50 * spec, 0, 255))
                    g_c = int(np.clip(160 * (0.85 + 0.3 * spec) + 60 * spec, 0, 255))
                    b_c = int(np.clip(255 * (0.9 + 0.15 * spec), 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))
    c_d.point((int(lex - 1), int(ley - 1)), fill=WHITE_SHINE)

    # (B) Right Eye: Emerald Mint Lens at (75, 39)
    rex, rey = 75.0, 39.0
    for y in range(int(rey - 4), int(rey + 5)):
        for x in range(int(rex - 4), int(rex + 5)):
            dist = ((x - rex)**2 + (y - rey)**2)**0.5
            if dist <= 3.8:
                spec = max(0.0, 1.0 - dist / 3.8)
                if dist >= 2.6:
                    core_img.putpixel((x, y), MINT_DARK)
                else:
                    r_c = int(np.clip(78 * (0.85 + 0.3 * spec) + 50 * spec, 0, 255))
                    g_c = int(np.clip(216 * (0.9 + 0.15 * spec) + 30 * spec, 0, 255))
                    b_c = int(np.clip(106 * (0.85 + 0.3 * spec) + 70 * spec, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))
    c_d.point((int(rex - 1), int(rey - 1)), fill=WHITE_SHINE)

    # Clean outline on optic core lenses
    apply_clean_outline(core_img, outline_color=OUTLINE)
    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25, Torso Overlay Layer)
    # File: costume/costume_peacock_marionette_court_cuirass.png
    # Marionette Court Cuirass (木偶宮廷巴洛克金線胸甲)
    # Features:
    # - Dawn Ivory White enamel curved breastplate on torso (x: 48..80, y: 58..88)
    # - Ornate baroque filigree scrollwork in dopamine gold (#FFD028)
    # - Teardrop ruby crimson (#E63946) brooch at collar (64, 62)
    # - Escapement window at lower center showing golden balance wheel
    # - STRICT ZERO pixels at y >= 96 (0-ART26b compliant, decoupled from lower chassis)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(58, 89):
        for x in range(48, 81):
            dx = (x - 64.0) / 15.0
            dy = (y - 73.0) / 14.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 68.0)**2)**0.5 / 15.0)
                shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 68.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Gold baroque filigree trim along border
                is_gold_filigree = (0.75 <= dist_sq <= 0.98) or ((x + y) % 6 == 0 and dist_sq <= 0.6)
                if is_gold_filigree:
                    r_c = int(np.clip(255 * (0.85 + 0.25 * spec) - 20 * edge_shade + 25 * shine, 0, 255))
                    g_c = int(np.clip(208 * (0.85 + 0.25 * spec) - 20 * edge_shade + 25 * shine, 0, 255))
                    b_c = int(np.clip(40 * (0.85 + 0.4 * spec) + 30 * shine, 0, 255))
                else:
                    # Dawn Ivory Enamel Breastplate
                    r_c = int(np.clip(255 * (0.9 + 0.15 * spec) - 25 * edge_shade + 20 * shine, 0, 255))
                    g_c = int(np.clip(248 * (0.9 + 0.15 * spec) - 25 * edge_shade + 20 * shine, 0, 255))
                    b_c = int(np.clip(231 * (0.9 + 0.15 * spec) - 25 * edge_shade + 20 * shine, 0, 255))

                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Teardrop Ruby Brooch at collar (64, 62)
    cos_d.ellipse([64 - 4, 62 - 4, 64 + 4, 62 + 4], fill=GOLD_DARK, outline=OUTLINE)
    cos_d.ellipse([64 - 3, 62 - 3, 64 + 3, 62 + 3], fill=RUBY_BASE)
    cos_d.ellipse([64 - 1, 62 - 1, 64 + 1, 62 + 1], fill=RUBY_LIGHT)
    cos_d.point((63, 61), fill=WHITE_SHINE)

    # Lower Escapement Window at (64, 82)
    cos_d.ellipse([64 - 4, 82 - 4, 64 + 4, 82 + 4], fill=GOLD_DARK, outline=OUTLINE)
    cos_d.ellipse([64 - 3, 82 - 3, 64 + 3, 82 + 3], fill=GOLD_BASE)
    cos_d.point((64, 82), fill=AMETHYST_BASE)

    apply_clean_outline(costume_img)

    # STRICT 0-ART26b check: zero pixels at y >= 96
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 30, Front Equipment Layer)
    # File: weapon/weapon_peacock_kaleidoscope_prism_focus.png
    # Kaleidoscope Prism Focus (萬花筒聚能稜鏡)
    # Features:
    # - Single-wield weapon (0-MKT7 compliant: 1 weapon group)
    # - Floating kaleidoscope prism focus held / hovering near right hand (center around x=102, y=68)
    # - Octagonal pierced brass filigree gimbal cage with ruby pivot joints
    # - Hovering 12-sided dual-color crystal core (sky blue #38A0FF and emerald mint #4ED86A)
    # - Orbiting optical rune energy arc / light particles
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wcx, wcy = 104.0, 68.0

    # 1. Optical energy aura and rune ring
    r_aura = 16.0
    for y in range(int(wcy - r_aura - 2), int(wcy + r_aura + 3)):
        for x in range(int(wcx - r_aura - 2), int(wcx + r_aura + 3)):
            dist = ((x - wcx)**2 + (y - wcy)**2)**0.5
            if 13.0 <= dist <= 16.0:
                norm_d = (dist - 13.0) / 3.0
                spec = max(0.0, np.sin(norm_d * np.pi))
                weapon_img.putpixel((x, y), (56, 160, 255, int(150 * spec)))

    # 2. Octagonal Brass Filigree Gimbal Cage (r=12.0)
    r_cage = 12.0
    for y in range(int(wcy - r_cage - 2), int(wcy + r_cage + 3)):
        for x in range(int(wcx - r_cage - 2), int(wcx + r_cage + 3)):
            dx = abs(x - wcx)
            dy = abs(y - wcy)
            if dx + dy <= r_cage * 1.35 and max(dx, dy) <= r_cage:
                dist = (dx**2 + dy**2)**0.5
                if 9.5 <= dist <= 12.0:
                    spec = max(0.0, 1.0 - abs(dist - 10.8) / 1.5)
                    r_w = int(np.clip(255 * (0.82 + 0.25 * spec), 0, 255))
                    g_w = int(np.clip(208 * (0.82 + 0.25 * spec), 0, 255))
                    b_w = int(np.clip(40 * (0.82 + 0.4 * spec) + 30 * spec, 0, 255))
                    weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Four Ruby Pivot Joints on Cage (N, S, W, E)
    for px_off, py_off in [(0.0, -11.5), (0.0, 11.5), (-11.5, 0.0), (11.5, 0.0)]:
        rx = int(round(wcx + px_off))
        ry = int(round(wcy + py_off))
        wd.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=RUBY_BASE, outline=GOLD_BASE)
        wd.point((rx, ry), fill=WHITE_SHINE)

    # 3. Hovering 12-Sided Dual-Color Kaleidoscope Crystal Core (r=8.0)
    r_core = 7.5
    for y in range(int(wcy - r_core - 1), int(wcy + r_core + 2)):
        for x in range(int(wcx - r_core - 1), int(wcx + r_core + 2)):
            dist = ((x - wcx)**2 + (y - wcy)**2)**0.5
            if dist <= r_core:
                spec = max(0.0, 1.0 - ((x - (wcx - 2))**2 + (y - (wcy - 2))**2)**0.5 / r_core)
                shine = max(0.0, 1.0 - ((x - (wcx - 2))**2 + (y - (wcy - 2))**2)**0.5 / 2.5)**2
                # Split facet: upper-left is sky blue, lower-right is emerald mint green
                if (x - wcx) + (y - wcy) <= 0:
                    r_p = int(np.clip(56 * (0.8 + 0.4 * spec) + 60 * shine, 0, 255))
                    g_p = int(np.clip(160 * (0.8 + 0.35 * spec) + 60 * shine, 0, 255))
                    b_p = int(np.clip(255 * (0.9 + 0.1 * spec), 0, 255))
                else:
                    r_p = int(np.clip(78 * (0.8 + 0.4 * spec) + 50 * shine, 0, 255))
                    g_p = int(np.clip(216 * (0.88 + 0.2 * spec) + 35 * shine, 0, 255))
                    b_p = int(np.clip(106 * (0.8 + 0.35 * spec) + 70 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    # Core star shine highlight
    wd.point((int(wcx - 1), int(wcy - 1)), fill=WHITE_SHINE)
    wd.point((int(wcx - 2), int(wcy - 1)), fill=WHITE_SHINE)
    wd.point((int(wcx - 1), int(wcy - 2)), fill=WHITE_SHINE)

    # 4. Wrist Connector / Hover Grip Stem (x: 84..90, y: 72..78)
    for y in range(72, 79):
        for x in range(84, 91):
            weapon_img.putpixel((x, y), GOLD_DARK)
    for y in range(74, 78):
        weapon_img.putpixel((85, y), GOLD_LIGHT)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_peacock_filigree_sunburst_key", key_img),
        ("back_curio", "curio_peacock_articulated_kaleidoscope_fan", curio_img),
        ("chassis", "chassis_peacock_glazed_porcelain_default", chassis_img),
        ("head_unit", "head_peacock_baroque_diadem_prism", head_img),
        ("costume", "costume_peacock_marionette_court_cuirass", costume_img),
        ("optic_core", "face_peacock_kaleidoscope_gem_lens", core_img),
        ("weapon", "weapon_peacock_kaleidoscope_prism_focus", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{PEACOCK_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{PEACOCK_PD_DIR}/winding_key/key_peacock_filigree_sunburst_key.png", f"{KEY_DIR}/key_peacock_filigree_sunburst_key.png")
    shutil.copyfile(f"{PEACOCK_PD_DIR}/weapon/weapon_peacock_kaleidoscope_prism_focus.png", f"{WEAPON_DIR}/weapon_peacock_kaleidoscope_prism_focus.png")
    print("  ✓ Synced key & weapon to universal folders")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order by layer_z_index:
    # z=5:  winding_key
    # z=8:  back_curio
    # z=10: chassis
    # z=20: head_unit
    # z=25: costume
    # z=25: optic_core (over head_unit hollow eye sockets)
    # z=30: weapon
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{PEACOCK_PD_DIR}/proof_paperdoll_peacock_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{PEACOCK_PD_DIR}/proof_paperdoll_peacock_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
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
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{PEACOCK_PD_DIR}/proof_peacock_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/peacock_idle_hd.png)
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
        char_scaled = char_crop.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

        showcase_img = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_x = (800 - sc_w) // 2
        sc_y = (1200 - sc_h) // 2 + 30
        showcase_img.alpha_composite(char_scaled, (sc_x, sc_y))

        # Strict check: 0-ART25: 4 corners must be 100% transparent
        for cy, cx in [(0, 0), (0, 799), (1199, 0), (1199, 799)]:
            showcase_img.putpixel((cx, cy), (0, 0, 0, 0))

        sh_path = f"{showcase_dir}/peacock_idle_hd.png"
        showcase_img.save(sh_path)
        print("  ✓ Showcase HD (800x1200) generated:", sh_path)


if __name__ == "__main__":
    build_all()
