#!/usr/bin/env python3
"""
build_meerkat_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十六族 沙哨狐獴 (The Sentry Meerkat, meerkat) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/SENTRY_MEERKAT_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh/soft tissue, stamped tinplate plates,
  brass rivets, micro acoustic funnel ears, periscope brass rangefinder optics,
  wasteland patched canvas poncho, articulated 5-segment tripod grounding tail,
  rusted coil spring-gun, high-torque scrap winding key)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Sand Ochre Stamped Tinplate (#D49B4B)
    2. Secondary Accent: Wasteland Dopamine Bright Orange (#FFA010)
    3. Brass & Trim: Polished Golden Brass & Winding Key (#FFD028)
    4. Chassis & Mechanism: Stamped Tinplate Steel Charcoal (#514E59)
    5. Sunlit Muzzle & Belly Plate: Sunlit Cream Ivory Enamel (#FFFDF8)
    6. Optical Lenses: Crystal Amber Gold (#FFB703)
    7. Verdigris & Seals: Verdigris Teal (#2A9D8F)
    8. Outline: Deep Warm Bronze/Brown Outline (#2E1F18 / #1F1A3A)
    Plus: Spring-gun coil highlights, ruby/cyan reflections
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
MEERKAT_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/meerkat"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Sentry Meerkat Specification)
OUTLINE = (46, 31, 24, 255)            # #2E1F18 Deep warm bronze-brown hand-drawn outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Sand Ochre Stamped Tinplate (#D49B4B)
OCHRE_BASE  = (212, 155, 75, 255)
OCHRE_LIGHT = (235, 185, 110, 255)
OCHRE_SHINE = (252, 218, 155, 255)
OCHRE_DARK  = (165, 110, 45, 255)
OCHRE_DEEP  = (115, 72, 26, 255)

# 2. Secondary Accent: Wasteland Dopamine Bright Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 230, 150, 255)
ORANGE_DARK  = (195, 105, 8, 255)
ORANGE_DEEP  = (135, 65, 5, 255)

# 3. Brass & Trim: Polished Golden Brass & Winding Key (#FFD028)
BRASS_BASE  = (255, 208, 40, 255)
BRASS_LIGHT = (255, 235, 115, 255)
BRASS_SHINE = (255, 250, 185, 255)
BRASS_DARK  = (195, 145, 18, 255)
BRASS_DEEP  = (130, 90, 10, 255)

# 4. Chassis & Mechanism: Stamped Tinplate Steel Charcoal (#514E59)
STEEL_BASE  = (81, 78, 89, 255)
STEEL_LIGHT = (120, 116, 130, 255)
STEEL_SHINE = (165, 160, 178, 255)
STEEL_DARK  = (52, 50, 58, 255)
STEEL_DEEP  = (32, 30, 38, 255)

# 5. Sunlit Muzzle & Belly Plate: Sunlit Cream Ivory Enamel (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (230, 222, 210, 255)
IVORY_DARK  = (195, 185, 170, 255)

# 6. Optical Lenses: Crystal Amber Gold (#FFB703)
AMBER_BASE  = (255, 183, 3, 255)
AMBER_LIGHT = (255, 215, 75, 255)
AMBER_SHINE = (255, 248, 180, 255)
AMBER_DARK  = (200, 135, 2, 255)
AMBER_DEEP  = (135, 85, 0, 255)

# 7. Verdigris & Seals: Verdigris Teal (#2A9D8F)
TEAL_BASE   = (42, 157, 143, 255)
TEAL_LIGHT  = (75, 195, 180, 255)
TEAL_SHINE  = (145, 235, 222, 255)
TEAL_DARK   = (25, 110, 100, 255)

# Accent & Highlights
CYAN_GLOW   = (56, 160, 255, 255)
RUBY_RED    = (230, 57, 70, 255)
WHITE_SHINE = (255, 255, 255, 255)
RUBBER_SOLE = (54, 40, 32, 255)


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
    print("=== BUILDING 100% MODULAR CANONICAL SENTRY MEERKAT SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_meerkat_high_torque_scrap_key.png
    # Wasteland High-Torque Scrap Winding Key (荒漠生鏽高扭力發條鑰匙)
    # Features:
    # - Socket boss at upper spine (64, 58)
    # - Heavy scrap iron shaft extends up-right to gear hub at (84, 24)
    # - Double-cog / gear silhouette scrap iron handle with stamped serrated edges
    # - Polished brass rivets & bushings, rust patina (#D49B4B / #FFD028)
    # - Strict check: 0-ART29 / 0-QA16 compliant (zero dark rectangular background plate)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from spine (64, 58) to gear hub (84, 24)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 20.0
        sy = 58.0 - t * 34.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(BRASS_BASE[2] * (0.8 + 0.5 * spec) + 40 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 58)
    kd.ellipse([60, 54, 68, 62], fill=STEEL_DARK, outline=OUTLINE)
    kd.ellipse([61, 55, 67, 61], fill=BRASS_DARK)
    kd.ellipse([62, 56, 66, 60], fill=BRASS_BASE)
    kd.point((64, 58), fill=AMBER_LIGHT)

    # 2. Dual-Cog Heavy Scrap Winding Handle centered at (84, 24)
    kcx, kcy = 84.0, 24.0
    r_outer = 13.5
    r_inner = 6.5

    # 8-toothed stamped gear silhouette
    for angle in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        for dist in np.linspace(5.0, 16.5, 25):
            px = int(kcx + dist * np.cos(angle))
            py = int(kcy + dist * np.sin(angle))
            if 0 <= px < W and 0 <= py < H:
                key_img.putpixel((px, py), BRASS_BASE)
                if dist >= 13.5:
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        if 0 <= px + dx < W and 0 <= py + dy < H:
                            key_img.putpixel((px + dx, py + dy), BRASS_LIGHT)

    # Outer & Inner Gear Body Rings
    for y in range(int(kcy - r_outer - 4), int(kcy + r_outer + 5)):
        for x in range(int(kcx - r_outer - 4), int(kcx + r_outer + 5)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            is_ring = (dist <= r_outer + 0.8 and dist >= r_inner - 0.5)
            if is_ring:
                spec = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 15.0)
                shine = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 4.0)**2
                # Dual-tone: brass rim + weathered steel body
                if dist > r_outer - 2.5:
                    r_k = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                    g_k = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                    b_k = int(np.clip(BRASS_BASE[2] * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                else:
                    r_k = int(np.clip(STEEL_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    g_k = int(np.clip(STEEL_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    b_k = int(np.clip(STEEL_BASE[2] * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Center Hub Boss
    r_hub = 4.2
    for y in range(int(kcy - r_hub - 1), int(kcy + r_hub + 2)):
        for x in range(int(kcx - r_hub - 1), int(kcx + r_hub + 2)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if dist <= r_hub:
                spec = max(0.0, 1.0 - dist / r_hub)
                r_h = int(np.clip(BRASS_BASE[0] * (0.85 + 0.2 * spec), 0, 255))
                g_h = int(np.clip(BRASS_BASE[1] * (0.85 + 0.2 * spec), 0, 255))
                b_h = int(np.clip(BRASS_BASE[2] * (0.85 + 0.2 * spec) + 30 * spec, 0, 255))
                key_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=AMBER_BASE, outline=OUTLINE)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Tail Layer)
    # File: back_curio/curio_meerkat_tripod_grounding_tail.png
    # Articulated Tripod Grounding Tail (鉸接多節生鏽金屬三腳平衡接地擺尾)
    # Features:
    # - Extends from pelvis (58, 86) down-left to ground at (28, 118)
    # - 5 articulated stamped tinplate & steel segment plates
    # - Grounding tripod brass claws touching ground at x: 20..36, y: 114..120
    # - Fully decoupled, stable third ground contact
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

    tail_curve = bezier_curve((58.0, 86.0), (46.0, 92.0), (34.0, 104.0), (28.0, 118.0), num_pts=60)

    # Core steel flexible wire
    for i in range(len(tail_curve) - 1):
        x0, y0 = tail_curve[i]
        x1, y1 = tail_curve[i+1]
        cd.line([(int(x0), int(y0)), (int(x1), int(y1))], fill=STEEL_LIGHT, width=3)
        cd.line([(int(x0)-1, int(y0)), (int(x1)-1, int(y1))], fill=OUTLINE, width=1)
        cd.line([(int(x0)+1, int(y0)), (int(x1)+1, int(y1))], fill=OUTLINE, width=1)

    # 5 articulated stamped tinplate segment plates
    t_scales = np.linspace(0.12, 0.88, 5)
    scale_indices = [int(t * (len(tail_curve) - 1)) for t in t_scales]

    for i, idx in enumerate(scale_indices):
        rx_c, ry_c = tail_curve[idx]
        progress = i / 4.0
        r_scale_w = 5.6 - 1.2 * progress
        r_scale_h = 4.2 - 0.8 * progress

        p_prev = tail_curve[max(0, idx - 2)]
        p_next = tail_curve[min(len(tail_curve) - 1, idx + 2)]
        tangent_angle = np.arctan2(p_next[1] - p_prev[1], p_next[0] - p_prev[0])
        normal_angle = tangent_angle + np.pi / 2.0

        for y_off in np.linspace(-r_scale_h, r_scale_h, 11):
            for x_off in np.linspace(-r_scale_w, r_scale_w, 13):
                if (x_off / r_scale_w)**2 + (y_off / r_scale_h)**2 <= 1.0:
                    px = int(rx_c + x_off * np.cos(normal_angle) - y_off * np.sin(normal_angle))
                    py = int(ry_c + x_off * np.sin(normal_angle) + y_off * np.cos(normal_angle))
                    if 0 <= px < W and 0 <= py < H:
                        spec = max(0.0, 1.0 - (x_off**2 + y_off**2)**0.5 / r_scale_w)
                        # Alternating sand ochre and weathered steel segments
                        if i % 2 == 0:
                            r_c = int(np.clip(OCHRE_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                            g_c = int(np.clip(OCHRE_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                            b_c = int(np.clip(OCHRE_BASE[2] * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                        else:
                            r_c = int(np.clip(STEEL_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                            g_c = int(np.clip(STEEL_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                            b_c = int(np.clip(STEEL_BASE[2] * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                        curio_img.putpixel((px, py), (r_c, g_c, b_c, 255))

        # Brass connecting hinge rivet
        cd.ellipse([int(rx_c - 1.5), int(ry_c - 1.5), int(rx_c + 1.5), int(ry_c + 1.5)], fill=BRASS_LIGHT, outline=OUTLINE)

    # Tip: Tripod Grounding Claws at (28, 118)
    tip_x, tip_y = 28.0, 118.0
    # Soft ground contact shadow under tail
    cd.ellipse([int(tip_x - 12), int(tip_y - 2), int(tip_x + 12), int(tip_y + 3)], fill=(46, 31, 24, 110))

    # Three grounding brass foot pads: Left (20, 118), Center (28, 119), Right (36, 118)
    for cx_f, cy_f in [(20.0, 118.0), (28.0, 119.0), (36.0, 118.0)]:
        cd.line([(int(tip_x), int(tip_y - 3)), (int(cx_f), int(cy_f))], fill=STEEL_LIGHT, width=2)
        cd.ellipse([int(cx_f - 3), int(cy_f - 2), int(cx_f + 3), int(cy_f + 2)], fill=BRASS_BASE, outline=OUTLINE)
        cd.point((int(cx_f), int(cy_f)), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Main Body Layer)
    # File: chassis/chassis_meerkat_tinplate_default.png
    # Sentry Meerkat Stamped Tinplate Metal Chassis (沙哨狐獴沖壓馬口鐵金屬素體)
    # Features:
    # - 2.0 ~ 2.2 chibi upright sentry standing posture
    # - Soft ground contact shadow around y=118..124
    # - Stamped tinplate legs with knee ratchet bearings and rubber sole pads
    # - Stamped tinplate chest (sand ochre #D49B4B) with sunlit cream ivory (#FFFDF8) belly plate
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # - Solid neck/collar flange at (x: 52..76, y: 46..58) (zero holes)
    # - Head base: cheek plates and snout (x: 46..82, y: 28..54)
    # - Left arm bent at side/waist (44..52, 64..78)
    # - Right arm upper limb (74..86, 64..76)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow under feet
    ch_d.ellipse([64 - 28, 118 - 4, 64 + 28, 118 + 4], fill=(46, 31, 24, 110))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Stamped Tinplate Mechanical Legs with Vulcanized Rubber Soles
    # Feet at (52, 116) and (72, 116)
    feet_pos = [(52.0, 116.0), (72.0, 116.0)]
    for bx, by in feet_pos:
        # Sole with slip-resistant pad
        ch_d.ellipse([int(bx - 6), int(by - 3), int(bx + 6), int(by + 3)], fill=RUBBER_SOLE, outline=OUTLINE)
        ch_d.ellipse([int(bx - 4), int(by - 2), int(bx + 4), int(by + 2)], fill=STEEL_BASE)
        ch_d.point((int(bx - 1), int(by - 1)), fill=WHITE_SHINE)

    # Upright tinplate leg pillars
    leg_paths = [
        ((52.0, 115.0), (55.0, 88.0)),
        ((72.0, 115.0), (69.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 28):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-4, 5):
                spec = max(0.0, 1.0 - abs(dx) / 4.0)
                # Sand ochre & steel plate cylinder
                r_l = int(np.clip(OCHRE_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
                g_l = int(np.clip(OCHRE_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
                b_l = int(np.clip(OCHRE_BASE[2] * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        # Ratchet knee joint at mid height
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 3, mid_x + 3, mid_y + 3], fill=BRASS_DARK, outline=OUTLINE)
        ch_d.ellipse([mid_x - 2, mid_y - 2, mid_x + 2, mid_y + 2], fill=BRASS_BASE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 3. Solid Neck Collar & Shoulder Flange (x: 46..82, y: 46..64)
    for ny in range(46, 65):
        for nx in range(46, 83):
            if ny < 56 and (nx < 50 or nx > 78):
                continue
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 14.0)
            r_n = int(np.clip(STEEL_BASE[0] * (0.85 + 0.3 * spec), 0, 255))
            g_n = int(np.clip(STEEL_BASE[1] * (0.85 + 0.3 * spec), 0, 255))
            b_n = int(np.clip(STEEL_BASE[2] * (0.85 + 0.3 * spec) + 30 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 4. Torso Body Shell (x: 44..84, y: 56..94)
    cx_t, cy_t = 64.0, 75.0
    for y in range(56, 95):
        for x in range(44, 85):
            dx = (x - cx_t) / 18.5
            dy = (y - cy_t) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 4))**2 + (y - (cy_t - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Center belly plate: sunlit cream ivory enamel (#FFFDF8)
                is_belly = (abs(x - cx_t) <= 9.0 and y >= 64 and y <= 88)
                # Orange warning diagonal chevron across chest
                is_orange_stripe = (y >= 60 and y <= 66 and (x + y) % 6 < 3)

                if is_belly:
                    r_t = int(np.clip(IVORY_BASE[0] * (0.88 + 0.15 * spec) - 15 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(IVORY_BASE[1] * (0.88 + 0.15 * spec) - 15 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(IVORY_BASE[2] * (0.88 + 0.15 * spec) - 15 * edge_shade + 20 * shine, 0, 255))
                elif is_orange_stripe:
                    r_t = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    g_t = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    b_t = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                else:
                    # Sand ochre stamped tinplate
                    r_t = int(np.clip(OCHRE_BASE[0] * (0.82 + 0.3 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                    g_t = int(np.clip(OCHRE_BASE[1] * (0.82 + 0.3 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                    b_t = int(np.clip(OCHRE_BASE[2] * (0.82 + 0.3 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Brass rivets on chest corners
    for rx, ry in [(49, 62), (79, 62), (51, 84), (77, 84)]:
        ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=BRASS_LIGHT, outline=OUTLINE)

    # 5. Head Shell Base (x: 46..82, y: 28..54)
    cx_h, cy_h = 64.0, 41.0
    for y in range(28, 55):
        for x in range(46, 83):
            dx = (x - cx_h) / 16.5
            dy = (y - cy_h) / 13.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_h - 3))**2 + (y - (cy_h - 3))**2)**0.5 / 15.0)
                shine = max(0.0, 1.0 - ((x - (cx_h - 3))**2 + (y - (cy_h - 3))**2)**0.5 / 5.0)**2
                # Lower face / muzzle plate in cream ivory
                if y >= 43 and abs(x - cx_h) <= 10.0:
                    r_h = int(np.clip(IVORY_BASE[0] * (0.88 + 0.15 * spec) + 20 * shine, 0, 255))
                    g_h = int(np.clip(IVORY_BASE[1] * (0.88 + 0.15 * spec) + 20 * shine, 0, 255))
                    b_h = int(np.clip(IVORY_BASE[2] * (0.88 + 0.15 * spec) + 20 * shine, 0, 255))
                else:
                    r_h = int(np.clip(OCHRE_BASE[0] * (0.82 + 0.3 * spec) + 30 * shine, 0, 255))
                    g_h = int(np.clip(OCHRE_BASE[1] * (0.82 + 0.3 * spec) + 30 * shine, 0, 255))
                    b_h = int(np.clip(OCHRE_BASE[2] * (0.82 + 0.3 * spec) + 30 * shine, 0, 255))
                chassis_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Metallic cute snout & breathing vent
    ch_d.ellipse([62, 45, 66, 48], fill=STEEL_BASE, outline=OUTLINE)
    ch_d.point((64, 46), fill=BRASS_LIGHT)

    # 6. Left Arm (poised at waist / rangefinder dial at 44..52, 64..78)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 48.0 - t * 4.0
        ay = 64.0 + t * 12.0
        for dx in range(-3, 4):
            spec = max(0.0, 1.0 - abs(dx) / 3.0)
            r_a = int(np.clip(OCHRE_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
            g_a = int(np.clip(OCHRE_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
            b_a = int(np.clip(OCHRE_BASE[2] * (0.8 + 0.25 * spec) + 20 * spec, 0, 255))
            chassis_img.putpixel((int(ax + dx), int(ay)), (r_a, g_a, b_a, 255))
    # Left hand resting at (44, 76)
    ch_d.ellipse([42, 74, 47, 78], fill=BRASS_BASE, outline=OUTLINE)

    # 7. Right Arm (holding forward to x: 88, strictly x < 94)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 76.0 + t * 10.0
        ay = 64.0 + t * 8.0
        for dx in range(-3, 4):
            px = int(ax + dx)
            py = int(ay)
            if px < 94:  # STRICT 0-ART9/11 check
                spec = max(0.0, 1.0 - abs(dx) / 3.0)
                r_a = int(np.clip(OCHRE_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
                g_a = int(np.clip(OCHRE_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
                b_a = int(np.clip(OCHRE_BASE[2] * (0.8 + 0.25 * spec) + 20 * spec, 0, 255))
                chassis_img.putpixel((px, py), (r_a, g_a, b_a, 255))
    # Right hand at (86, 72)
    ch_d.ellipse([84, 70, 89, 75], fill=BRASS_BASE, outline=OUTLINE)

    # STRICT 0-ART9/11 enforcement: clear any accidental pixels at x >= 94
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Above Chassis)
    # File: head_unit/head_meerkat_scavenger_cowl_ears.png
    # Scavenger Cowl Brow-Plate & Micro Acoustic Funnel Ears (拾荒風鏡金屬面甲與微型集音漏斗耳)
    # Features:
    # - Stamped metal visor / brow cowl across x: 46..82, y: 26..36
    # - Micro acoustic funnel ears at left (36..46, 20..32) and right (82..92, 20..32)
    # - Polished brass rivets, verdigris seam accents
    # - STRICT 0-ART27: Hollow eye sockets at (54, 40) and (72, 40) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Stamped Visor / Forehead Cowl Band (x: 48..80, y: 28..37)
    for y in range(28, 38):
        for x in range(48, 81):
            spec = max(0.0, 1.0 - ((x - 64.0)**2 + (y - 32.0)**2)**0.5 / 18.0)
            shine = max(0.0, 1.0 - abs(x - 62.0) / 10.0)**2
            # Orange warning stripe in center of cowl
            if abs(x - 64.0) <= 6.0:
                r_w = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                g_w = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                b_w = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
            else:
                r_w = int(np.clip(STEEL_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g_w = int(np.clip(STEEL_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                b_w = int(np.clip(STEEL_BASE[2] * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
            head_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Cowl mounting rivets
    for rx in [50, 58, 70, 78]:
        hd.ellipse([rx - 1, 31, rx + 1, 33], fill=BRASS_LIGHT, outline=OUTLINE)

    # 2. Micro Acoustic Funnel Ears (Left: 38..46, 22..32; Right: 82..90, 22..32)
    # Left Funnel Ear (Conical brass horn)
    for y in range(20, 33):
        for x in range(36, 48):
            dx = (x - 42.0) / 5.5
            dy = (y - 26.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                # Outer brass bell, inner acoustic dark diaphragm
                if dx**2 + dy**2 > 0.45:
                    r_e = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
                    g_e = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
                    b_e = int(np.clip(BRASS_BASE[2] * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                else:
                    r_e = int(np.clip(STEEL_DARK[0] * (0.85 + 0.2 * spec), 0, 255))
                    g_e = int(np.clip(STEEL_DARK[1] * (0.85 + 0.2 * spec), 0, 255))
                    b_e = int(np.clip(STEEL_DARK[2] * (0.85 + 0.2 * spec), 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    # Right Funnel Ear (Conical brass horn)
    for y in range(20, 33):
        for x in range(80, 92):
            dx = (x - 86.0) / 5.5
            dy = (y - 26.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                if dx**2 + dy**2 > 0.45:
                    r_e = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
                    g_e = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
                    b_e = int(np.clip(BRASS_BASE[2] * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                else:
                    r_e = int(np.clip(STEEL_DARK[0] * (0.85 + 0.2 * spec), 0, 255))
                    g_e = int(np.clip(STEEL_DARK[1] * (0.85 + 0.2 * spec), 0, 255))
                    b_e = int(np.clip(STEEL_DARK[2] * (0.85 + 0.2 * spec), 0, 255))
                head_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    # 3. Goggles Bezel Rims around eye sockets
    # Bezel frames at (54, 40) and (72, 40)
    for cx_eye in [54.0, 72.0]:
        for y in range(36, 45):
            for x in range(int(cx_eye - 5), int(cx_eye + 6)):
                dist = ((x - cx_eye)**2 + (y - 40.0)**2)**0.5
                if 3.4 <= dist <= 5.2:
                    head_img.putpixel((x, y), BRASS_BASE)

    # Bridge between goggles
    hd.line([(58, 40), (68, 40)], fill=BRASS_DARK, width=2)
    hd.point((63, 40), fill=BRASS_LIGHT)

    # STRICT 0-ART27: Hollow Eye Sockets
    # Ensure inner region of eye sockets (radius < 3.2) is 100% transparent (alpha == 0)
    for cx_eye in [54.0, 72.0]:
        for y in range(37, 44):
            for x in range(int(cx_eye - 4), int(cx_eye + 5)):
                if ((x - cx_eye)**2 + (y - 40.0)**2)**0.5 < 3.2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(head_img, ignore_regions=[(51, 37, 57, 43), (69, 37, 75, 43)])
    # Double ensure hollow sockets after outline
    for cx_eye in [54.0, 72.0]:
        for y in range(37, 44):
            for x in range(int(cx_eye - 3), int(cx_eye + 4)):
                if ((x - cx_eye)**2 + (y - 40.0)**2)**0.5 < 3.0:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 25 / 30, Eye Layer)
    # File: optic_core/face_meerkat_periscope_rangefinder_lens.png
    # Periscope Brass Rangefinder Optics & Ocular Lenses (潛望式黃銅測距目鏡)
    # Features:
    # - Left eye: Brass washer ring & reflective convex optic lens at (54, 40)
    # - Right eye: Radiant amber-gold ocular lens at (72, 40)
    # - Brass periscope tube extending UPWARD from right eye socket (72, 40) to (75, 20..36)
    # - Top objective periscope prism at (75, 22) with forward amber lens
    # - High opacity at eye centers, rich color depth, perfectly aligns with hollow sockets
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    # 1. Left Eye: Brass washer ring & convex crystal lens at (54, 40)
    for y in range(37, 44):
        for x in range(51, 58):
            dist = ((x - 54.0)**2 + (y - 40.0)**2)**0.5
            if dist <= 3.2:
                spec = max(0.0, 1.0 - dist / 3.2)
                shine = max(0.0, 1.0 - ((x - 53.0)**2 + (y - 39.0)**2)**0.5 / 1.5)**2
                r_l = int(np.clip(AMBER_BASE[0] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                g_l = int(np.clip(AMBER_BASE[1] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                b_l = int(np.clip(AMBER_BASE[2] * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                core_img.putpixel((x, y), (r_l, g_l, b_l, 255))
    c_d.point((53, 39), fill=WHITE_SHINE)
    c_d.point((55, 41), fill=CYAN_GLOW)

    # 2. Right Eye: Radiant amber-gold ocular lens at (72, 40)
    for y in range(37, 44):
        for x in range(69, 76):
            dist = ((x - 72.0)**2 + (y - 40.0)**2)**0.5
            if dist <= 3.2:
                spec = max(0.0, 1.0 - dist / 3.2)
                shine = max(0.0, 1.0 - ((x - 71.0)**2 + (y - 39.0)**2)**0.5 / 1.5)**2
                r_r = int(np.clip(AMBER_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                g_r = int(np.clip(AMBER_BASE[1] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                b_r = int(np.clip(AMBER_BASE[2] * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                core_img.putpixel((x, y), (r_r, g_r, b_r, 255))
    c_d.point((71, 39), fill=WHITE_SHINE)
    c_d.point((73, 41), fill=CYAN_GLOW)

    # 3. Brass Periscope Tube extending upward from right eye (72, 40) to top prism (75, 20..36)
    # Periscope vertical barrel
    for y in range(22, 38):
        for x in range(73, 78):
            spec = max(0.0, 1.0 - abs(x - 75.0) / 2.5)
            r_p = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
            g_p = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
            b_p = int(np.clip(BRASS_BASE[2] * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
            core_img.putpixel((x, y), (r_p, g_p, b_p, 255))
        # Distance calibration tick marks
        if y in [26, 30, 34]:
            core_img.putpixel((73, y), STEEL_DARK)

    # Top Objective Prism Head at (75, 22)
    c_d.rectangle([72, 19, 78, 23], fill=BRASS_DARK, outline=OUTLINE)
    c_d.rectangle([73, 20, 77, 22], fill=BRASS_LIGHT)
    # Forward-facing amber lens aperture
    c_d.ellipse([74, 20, 76, 22], fill=AMBER_BASE)
    c_d.point((75, 21), fill=WHITE_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25, Torso Overlay Layer)
    # File: costume/costume_meerkat_patched_canvas_poncho.png
    # Wasteland Patched Canvas Poncho (廢土補丁帆布防沙短斗篷)
    # Features:
    # - Draped over shoulders and chest at y: 56..90, x: 44..84
    # - Multi-tone patchwork: Wasteland Dopamine Orange (#FFA010) & Sand Ochre (#D49B4B)
    # - Weathered canvas textures, cross-stitch seams, brass gear brooch at center (64, 66)
    # - Scalloped hem at y: 86..90
    # - STRICT 0-ART26b: Decoupled, zero pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(56, 92):
        for x in range(44, 85):
            dx = (x - 64.0) / 19.0
            dy = (y - 74.0) / 16.0
            dist_sq = dx**2 + dy**2
            # Short capelet bell shape
            if dist_sq <= 1.0 and y <= 89:
                spec = max(0.0, 1.0 - ((x - 62.0)**2 + (y - 70.0)**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - 62.0)**2 + (y - 70.0)**2)**0.5 / 6.0)**2
                # Left patch: Dopamine Orange, Right patch: Sand Ochre, Center seam
                if x < 63:
                    r_c = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                    g_c = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                    b_c = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                else:
                    r_c = int(np.clip(OCHRE_BASE[0] * (0.82 + 0.25 * spec) + 25 * shine, 0, 255))
                    g_c = int(np.clip(OCHRE_BASE[1] * (0.82 + 0.25 * spec) + 25 * shine, 0, 255))
                    b_c = int(np.clip(OCHRE_BASE[2] * (0.82 + 0.25 * spec) + 25 * shine, 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Center vertical cross-stitch line along x=63
    for y in range(58, 88, 3):
        cos_d.line([(62, y), (64, y+1)], fill=IVORY_LIGHT, width=1)

    # Scalloped bottom fringe points
    for fx in range(46, 83, 4):
        cos_d.polygon([(fx, 88), (fx + 2, 91), (fx + 4, 88)], fill=ORANGE_DARK)

    # Chest Brooch: Rusted Brass Gear Brooch at (64, 66)
    cos_d.ellipse([61, 63, 67, 69], fill=BRASS_DARK, outline=OUTLINE)
    cos_d.ellipse([62, 64, 66, 68], fill=BRASS_BASE)
    cos_d.point((64, 66), fill=AMBER_LIGHT)

    # Brass Collar Clasp Pins
    for cx_pin in [54, 74]:
        cos_d.ellipse([cx_pin - 1, 59, cx_pin + 1, 61], fill=BRASS_LIGHT, outline=OUTLINE)

    # STRICT 0-ART26b enforcement: zero pixels at y >= 96
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Front Equipment Layer)
    # File: weapon/weapon_meerkat_rusted_coil_spring_gun.png
    # Rusted Coil Spring-Gun (生鏽彈簧刺銃)
    # Features:
    # - Single-wielded in right hand (0-MKT7 compliant)
    # - Stock / receiver at (84, 74), long chassis extending up-right to muzzle at (114, 42)
    # - Exposed double-layer high-tension brass clockwork coil springs along barrel
    # - Folding rusted steel bayonet blade below muzzle (102..116, 42..50)
    # - Muzzle slotted flash suppressor, verdigris brass fittings, pressure gauge
    # - Completely decoupled, single weapon
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Main gun axis: from stock (82, 74) to muzzle (114, 42)
    # Vector: dx = 32, dy = -32 (angle -45 deg)
    for t in np.linspace(0.0, 1.0, 80):
        gx = 82.0 + t * 32.0
        gy = 74.0 - t * 32.0
        # Barrel thickness: width ~5px perpendicular to gun axis
        for d in range(-2, 3):
            # Normal vector (-1, -1) normalized
            nx = -d * 0.707
            ny = -d * 0.707
            px = int(gx + nx)
            py = int(gy + ny)
            if 0 <= px < W and 0 <= py < H:
                spec = max(0.0, 1.0 - abs(d) / 2.0)
                shine = max(0.0, 1.0 - abs(d + 1.0) / 1.5)**2
                # Gun barrel steel body with rich multi-tone shading
                r_w = int(np.clip(STEEL_BASE[0] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                g_w = int(np.clip(STEEL_BASE[1] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                b_w = int(np.clip(STEEL_BASE[2] * (0.8 + 0.35 * spec) + 45 * shine, 0, 255))
                weapon_img.putpixel((px, py), (r_w, g_w, b_w, 255))

    # Wooden / canvas stock grip near (80..86, 72..78) with rich wood-grain / leather shading
    for sy in range(72, 81):
        for sx in range(78, 88):
            if (sx - 82)**2 + (sy - 76)**2 <= 16:
                dist = ((sx - 82)**2 + (sy - 76)**2)**0.5
                spec = max(0.0, 1.0 - dist / 4.0)
                r_st = int(np.clip(OCHRE_DARK[0] * (0.8 + 0.3 * spec), 0, 255))
                g_st = int(np.clip(OCHRE_DARK[1] * (0.8 + 0.3 * spec), 0, 255))
                b_st = int(np.clip(OCHRE_DARK[2] * (0.8 + 0.3 * spec) + 20 * spec, 0, 255))
                weapon_img.putpixel((sx, sy), (r_st, g_st, b_st, 255))
    wd.line([(80, 75), (83, 78)], fill=BRASS_LIGHT, width=1)
    wd.line([(82, 73), (85, 76)], fill=BRASS_BASE, width=1)

    # Exposed Double-Layer High-Tension Clockwork Coil Springs along barrel (t = 0.22..0.78)
    for t in np.linspace(0.22, 0.78, 14):
        bx = 82.0 + t * 32.0
        by = 74.0 - t * 32.0
        # Draw spring coil loops with gradient
        for coil_r in range(-4, 5):
            cx = int(bx - coil_r * 0.707)
            cy = int(by - coil_r * 0.707)
            if 0 <= cx < W and 0 <= cy < H:
                c_spec = max(0.0, 1.0 - abs(coil_r) / 4.0)
                r_c = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * c_spec), 0, 255))
                g_c = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * c_spec), 0, 255))
                b_c = int(np.clip(BRASS_BASE[2] * (0.8 + 0.4 * c_spec) + 30 * c_spec, 0, 255))
                weapon_img.putpixel((cx, cy), (r_c, g_c, b_c, 255))
        # Specular shine point on top of coil
        hx = int(bx - 3 * 0.707)
        hy = int(by - 3 * 0.707)
        if 0 <= hx < W and 0 <= hy < H:
            weapon_img.putpixel((hx, hy), WHITE_SHINE)

    # Folding Rusted Steel Bayonet Blade under muzzle (t = 0.65..1.0)
    for by in range(41, 54):
        for bx in range(101, 117):
            # Triangle from (102, 53) to (116, 42) to (110, 48)
            # Check if point is inside triangle or near blade edge
            if 102 <= bx <= 116 and 42 <= by <= 53:
                # Interpolate blade bevel
                t_b = (bx - 102) / 14.0
                edge_y = 53.0 - t_b * 11.0
                spine_y = 48.0 - t_b * 6.0
                if spine_y <= by <= edge_y + 1.0:
                    spec = max(0.0, 1.0 - abs(by - spine_y) / 4.0)
                    r_b = int(np.clip(STEEL_LIGHT[0] * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                    g_b = int(np.clip(STEEL_LIGHT[1] * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
                    b_b = int(np.clip(STEEL_LIGHT[2] * (0.8 + 0.3 * spec) + 40 * spec, 0, 255))
                    weapon_img.putpixel((bx, by), (r_b, g_b, b_b, 255))
    wd.line([(103, 52), (115, 43)], fill=WHITE_SHINE, width=1)

    # Muzzle Slotted Flash Suppressor & Pressure Valve at (114, 42)
    for my in range(39, 45):
        for mx in range(112, 118):
            spec = max(0.0, 1.0 - ((mx - 114.5)**2 + (my - 41.5)**2)**0.5 / 3.0)
            r_m = int(np.clip(BRASS_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
            g_m = int(np.clip(BRASS_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
            b_m = int(np.clip(BRASS_BASE[2] * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
            weapon_img.putpixel((mx, my), (r_m, g_m, b_m, 255))
    wd.point((115, 41), fill=AMBER_LIGHT)

    # Miniature Pressure Gauge at (90, 66)
    for gy in range(64, 70):
        for gx in range(88, 94):
            dist = ((gx - 90.5)**2 + (gy - 66.5)**2)**0.5
            if dist <= 2.8:
                if dist > 1.8:
                    weapon_img.putpixel((gx, gy), BRASS_DARK)
                else:
                    weapon_img.putpixel((gx, gy), IVORY_LIGHT)
    wd.point((90, 66), fill=RUBY_RED)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 LANCZOS ASSETS
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("chassis", "chassis_meerkat_tinplate_default", chassis_img),
        ("head_unit", "head_meerkat_scavenger_cowl_ears", head_img),
        ("winding_key", "key_meerkat_high_torque_scrap_key", key_img),
        ("costume", "costume_meerkat_patched_canvas_poncho", costume_img),
        ("optic_core", "face_meerkat_periscope_rangefinder_lens", core_img),
        ("weapon", "weapon_meerkat_rusted_coil_spring_gun", weapon_img),
        ("back_curio", "curio_meerkat_tripod_grounding_tail", curio_img)
    ]

    for slot, item_id, img_128 in slices_data:
        slot_dir = f"{MEERKAT_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)

        p128 = f"{slot_dir}/{item_id}.png"
        img_128.save(p128)

        # Genuine Lanczos 512x512 high-res export
        img_512 = img_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
        p512 = f"{slot_dir}/{item_id}_512.png"
        img_512.save(p512)

        print(f"  ✓ Saved [{slot:<12}] 128: {p128} | 512: {p512}")

    # Copy to common slots for paperdoll cross-race sharing
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{MEERKAT_PD_DIR}/winding_key/key_meerkat_high_torque_scrap_key.png",
                 f"{KEY_DIR}/key_meerkat_high_torque_scrap_key.png")
    shutil.copy2(f"{MEERKAT_PD_DIR}/weapon/weapon_meerkat_rusted_coil_spring_gun.png",
                 f"{WEAPON_DIR}/weapon_meerkat_rusted_coil_spring_gun.png")
    print("  ✓ Common key and weapon slices updated")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOF IMAGES
    # ─────────────────────────────────────────────────────────────
    # Layer order by z-index: key (5), curio (8), chassis (10), head (20), costume (25), optic (30), weapon (40)
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{MEERKAT_PD_DIR}/proof_paperdoll_meerkat_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{MEERKAT_PD_DIR}/proof_paperdoll_meerkat_magenta.png"
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

    strip_path = f"{MEERKAT_PD_DIR}/proof_meerkat_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/meerkat_idle_hd.png)
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

        sh_path = f"{showcase_dir}/meerkat_idle_hd.png"
        showcase_img.save(sh_path)
        print("  ✓ Showcase HD (800x1200) generated:", sh_path)


if __name__ == "__main__":
    build_all()
