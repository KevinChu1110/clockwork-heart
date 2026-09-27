#!/usr/bin/env python3
"""
build_hedgehog_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十一族 棘輪刺蝟 (The Ratchet Hedgehog, hedgehog) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/RATCHET_HEDGEHOG_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological quills, zero flesh, stamped polished brass plates,
  ivory enamel cheek/chest plates, semicircular tuning fork ears, vulcanized silicone artisan boots,
  single-direction ratchet & pawl winding key, spring steel needle-quill pack, ratchet needle-dart weapon)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette:
    Primary: Warm Amber Orange Polished Brass (#FF8C42)
    Secondary: Ivory White Enamel (#FFFDF8)
    Accent: Dopamine Golden Ratchet Key & Clock Gears (#FFD028)
    Detail: Phosphor Mint Green Watchmaker Precision Loupe (#4ED86A)
    Warm Highlight: Coral Pink High-Pressure Silicone Seals & Thread Terminals (#FF5E8A)
    Quill Steel: Quenched Spring Steel Needles (#5A5666)
    Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
HEDGEHOG_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hedgehog"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Ratchet Hedgehog Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Warm Amber Orange Polished Brass (#FF8C42)
AMBER_BASE  = (255, 140, 66, 255)
AMBER_LIGHT = (255, 180, 115, 255)
AMBER_SHINE = (255, 220, 175, 255)
AMBER_DARK  = (205, 95, 25, 255)
AMBER_DEEP  = (145, 55, 10, 255)

# Secondary: Ivory White Enamel Cheek & Chest Plates (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (230, 224, 215, 255)
IVORY_DARK    = (195, 188, 178, 255)

# Accent: Dopamine Golden Ratchet & Pawl Winding Key & Clock Gears (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# Detail: Phosphor Mint Green Watchmaker Precision Loupe & Optics (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (140, 240, 165, 255)
MINT_SHINE = (210, 255, 225, 255)
MINT_DARK  = (36, 140, 62, 255)

# Warm Highlight: Coral Pink High-Pressure Silicone Seals & Thread Terminals (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

# Quill Steel: Quenched Spring Steel Needles (#5A5666)
STEEL_BASE  = (90, 86, 102, 255)
STEEL_LIGHT = (140, 136, 155, 255)
STEEL_SHINE = (195, 192, 210, 255)
STEEL_DARK  = (55, 52, 65, 255)

# Artisan Tailor Vest / Horologist Leather
VEST_BASE  = (142, 82, 45, 255)
VEST_LIGHT = (180, 112, 68, 255)
VEST_DARK  = (96, 52, 26, 255)

# Vulcanized Industrial Black Silicone Boots (#202026)
SILICONE_BASE  = (32, 32, 38, 255)
SILICONE_LIGHT = (65, 65, 78, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL RATCHET HEDGEHOG SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_hedgehog_ratchet_and_pawl_cross.png
    # Single-Direction Ratchet & Pawl Winding Key (單向棘爪棘輪發條鑰匙)
    # Socket at upper spine (64, 60), shaft extends diagonally up-right to (86, 30)
    # Features:
    # - Polished brass shaft with bevel shading
    # - Center toothed ratchet wheel with visible spring steel pawl
    # - Dual-ring baroque / cross-style winding key handle in dopamine gold (#FFD028)
    # - Central coral pink pivot gem / bearing
    # - STRICTLY transparent corners (0-ART29)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 60) to (86, 30)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 22.0
        sy = 60.0 - t * 30.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 60)
    kd.ellipse([60, 56, 68, 64], fill=GOLD_DARK, outline=OUTLINE)
    kd.ellipse([61, 57, 67, 63], fill=GOLD_BASE)
    kd.ellipse([63, 59, 65, 61], fill=CORAL_BASE)

    # 2. Key Hub & Ratchet Mechanism at (86, 30)
    kcx, kcy = 86.0, 30.0

    # Dual-Ring Baroque Cross Winding Wings
    # Left ring centered at (74, 25), Right ring centered at (98, 25)
    wing_centers = [(74.0, 25.0), (98.0, 25.0)]
    for wcx, wcy in wing_centers:
        r_outer = 11.0
        r_inner = 5.5
        for y in range(int(wcy - r_outer - 2), int(wcy + r_outer + 3)):
            for x in range(int(wcx - r_outer - 2), int(wcx + r_outer + 3)):
                dist = ((x - wcx)**2 + (y - wcy)**2)**0.5
                if r_inner <= dist <= r_outer:
                    # Circular torus shading with gold sheen
                    norm_r = (dist - r_inner) / (r_outer - r_inner)
                    spec = max(0.0, np.sin(norm_r * np.pi))
                    shine = max(0.0, 1.0 - ((x - (wcx - 3))**2 + (y - (wcy - 3))**2)**0.5 / 6.0)**2
                    r_w = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_w = int(np.clip(208 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                    b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Cross crest / top crown ornament at (86, 17)
    kd.ellipse([83, 14, 89, 20], fill=GOLD_BASE, outline=OUTLINE)
    kd.ellipse([84, 15, 88, 19], fill=GOLD_LIGHT)
    kd.point((86, 16), fill=WHITE_SHINE)

    # Central Ratchet Wheel with Sawtooth Teeth at (86, 30)
    r_ratchet = 7.0
    for y in range(int(kcy - r_ratchet - 2), int(kcy + r_ratchet + 3)):
        for x in range(int(kcx - r_ratchet - 2), int(kcx + r_ratchet + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if dist <= r_ratchet:
                angle = np.arctan2(y - kcy, x - kcx)
                # 8 sawteeth pattern
                saw = ((angle % (np.pi / 4)) / (np.pi / 4))
                spec = max(0.0, 1.0 - dist / r_ratchet)
                r_r = int(np.clip(255 * (0.75 + 0.3 * spec) - 20 * saw, 0, 255))
                g_r = int(np.clip(208 * (0.75 + 0.3 * spec) - 20 * saw, 0, 255))
                b_r = int(np.clip(40 * (0.75 + 0.5 * spec) + 30 * spec, 0, 255))
                key_img.putpixel((x, y), (r_r, g_r, b_r, 255))

    # Visible Ratchet Teeth Points around circumference
    for i in range(8):
        t_angle = i * (np.pi / 4)
        tx = int(kcx + (r_ratchet + 1.2) * np.cos(t_angle))
        ty = int(kcy + (r_ratchet + 1.2) * np.sin(t_angle))
        if 0 <= tx < W and 0 <= ty < H:
            key_img.putpixel((tx, ty), GOLD_LIGHT)

    # Spring-Steel Pawl (棘爪) engaging the ratchet wheel from top-left (77, 23) to (83, 26)
    kd.line([(76, 22), (83, 26)], fill=STEEL_LIGHT, width=2)
    kd.ellipse([75, 21, 78, 24], fill=STEEL_DARK, outline=OUTLINE)  # Pivot pin
    kd.point((76, 22), fill=WHITE_SHINE)
    # Little spring wire loop
    kd.arc([74, 20, 80, 26], start=180, end=340, fill=STEEL_SHINE, width=1)

    # Center jewel / hub bearing at (86, 30)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=CORAL_BASE, outline=OUTLINE)
    kd.ellipse([int(kcx - 1.5), int(kcy - 1.5), int(kcx + 1.5), int(kcy + 1.5)], fill=CORAL_LIGHT)
    kd.point((int(kcx - 0.5), int(kcy - 0.5)), fill=WHITE_SHINE)

    apply_clean_outline(key_img)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_hedgehog_spring_steel_quill_pack.png
    # Three-Tier Spring-Steel Quill Pack (三聯放射狀淬火彈簧鋼棘發射槽)
    # Features:
    # - Arched brass slide track rail mounted along hedgehog's curved back (36..56, 44..84)
    # - Array of radiating quenched spring steel quills (#5A5666)
    # - Faceted rhombic chisel-ground needle tips with brilliant specular highlights
    # - Guide thread weaving through miniature brass eyelets at needle bases
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Arched Brass Guide Track / Chassis Mount Spine
    track_pts = [
        (56.0, 44.0), (48.0, 48.0), (42.0, 56.0),
        (38.0, 66.0), (38.0, 76.0), (42.0, 84.0), (48.0, 90.0)
    ]
    for i in range(len(track_pts) - 1):
        x0, y0 = track_pts[i]
        x1, y1 = track_pts[i+1]
        for t in np.linspace(0.0, 1.0, 20):
            mx = x0 + t * (x1 - x0)
            my = y0 + t * (y1 - y0)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx**2 + dy**2 <= 4:
                        spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                        r_tr = int(np.clip(255 * (0.75 + 0.35 * spec), 0, 255))
                        g_tr = int(np.clip(140 * (0.75 + 0.35 * spec), 0, 255))
                        b_tr = int(np.clip(66 * (0.75 + 0.5 * spec) + 30 * spec, 0, 255))
                        curio_img.putpixel((int(mx + dx), int(my + dy)), (r_tr, g_tr, b_tr, 255))

    # 2. Radiating Quenched Spring Steel Quills
    # Needles originate along the track and project backwards/radially
    quill_definitions = [
        # (base_x, base_y, length, angle_deg)
        (56.0, 44.0, 17.0, 125.0),
        (52.0, 46.0, 19.0, 135.0),
        (48.0, 50.0, 21.0, 145.0),
        (44.0, 55.0, 22.0, 155.0),
        (40.0, 61.0, 23.0, 165.0),
        (38.0, 68.0, 24.0, 175.0),
        (37.0, 75.0, 23.0, 185.0),
        (39.0, 82.0, 21.0, 195.0),
        (43.0, 88.0, 18.0, 205.0),
        (48.0, 92.0, 15.0, 215.0),
        # Inner secondary layer (interleaved shorter needles for density)
        (53.0, 49.0, 14.0, 130.0),
        (49.0, 54.0, 15.0, 140.0),
        (45.0, 60.0, 16.0, 150.0),
        (42.0, 66.0, 17.0, 160.0),
        (40.0, 73.0, 17.0, 170.0),
        (41.0, 80.0, 15.0, 180.0),
        (44.0, 86.0, 13.0, 190.0),
    ]

    for bx, by, qlen, qang_deg in quill_definitions:
        qrad = np.radians(qang_deg)
        cos_q = np.cos(qrad)
        sin_q = np.sin(qrad)
        norm_cos = -sin_q
        norm_sin = cos_q

        # Draw needle from base to tip
        for d in np.linspace(0.0, qlen, int(qlen * 2)):
            # Width tapers from 2.5px at base to 0.4px at tip
            w_d = 2.5 * (1.0 - d / qlen) + 0.4
            for w_off in np.linspace(-w_d / 2.0, w_d / 2.0, 7):
                px = bx + d * cos_q + w_off * norm_cos
                py = by + d * sin_q + w_off * norm_sin
                ix, iy = int(px), int(py)
                if 0 <= ix < W and 0 <= iy < H:
                    # Faceted steel shading: ridge along center line (w_off ~ 0)
                    norm_w = abs(w_off) / (w_d / 2.0 + 1e-5)
                    ridge_spec = max(0.0, 1.0 - norm_w)**2
                    tip_shine = max(0.0, (d / qlen) - 0.6) / 0.4

                    r_q = int(np.clip(90 * (0.8 + 0.4 * ridge_spec) + 90 * tip_shine, 0, 255))
                    g_q = int(np.clip(86 * (0.8 + 0.4 * ridge_spec) + 90 * tip_shine, 0, 255))
                    b_q = int(np.clip(102 * (0.8 + 0.4 * ridge_spec) + 110 * tip_shine, 0, 255))
                    curio_img.putpixel((ix, iy), (r_q, g_q, b_q, 255))

        # Base sleeve collar & brass eyelet
        cd.ellipse([int(bx - 1.8), int(by - 1.8), int(bx + 1.8), int(by + 1.8)], fill=GOLD_BASE, outline=OUTLINE)
        cd.point((int(bx), int(by)), fill=GOLD_LIGHT)

    # 3. Spun Cotton Guide Thread weaving along the needle eyelets
    for i in range(len(quill_definitions) - 1):
        if i >= 10: break
        bx0, by0 = quill_definitions[i][0], quill_definitions[i][1]
        bx1, by1 = quill_definitions[i+1][0], quill_definitions[i+1][1]
        cd.line([(int(bx0), int(by0)), (int(bx1), int(by1))], fill=IVORY_LIGHT, width=1)

    # Thread tension terminal at (48, 92)
    cd.ellipse([46, 90, 50, 94], fill=CORAL_BASE, outline=OUTLINE)
    cd.point((48, 92), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_hedgehog_amber_brass_default.png
    # Features:
    # - 2.0 ~ 2.2 Chibi artisan guard stance
    # - Soft ground contact shadow at (64, 116)
    # - Heavy-duty vulcanized black silicone boots (#202026) with brass toe caps
    # - Articulated legs with amber brass armor and coral pink dampeners
    # - Warm Amber Orange (#FF8C42) polished brass body hull with multi-tone depth
    # - Ivory White (#FFFDF8) enamel chest & belly shock-absorbing plate
    # - Left hand forward/raised balancing palm at (38, 84)
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

    # 2. Vulcanized Silicone Boots with Polished Brass Caps
    boot_pos = [(48.0, 113.0), (70.0, 113.0)]
    for bx, by in boot_pos:
        # Sole base
        ch_d.ellipse([int(bx - 7), int(by - 2), int(bx + 7), int(by + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(bx - 5), int(by - 1), int(bx + 5), int(by + 2)], fill=SILICONE_LIGHT)
        # Polished Brass toe cap & rim
        ch_d.ellipse([int(bx - 4), int(by), int(bx + 4), int(by + 3)], fill=AMBER_BASE)
        ch_d.line([(int(bx - 3), int(by + 2)), (int(bx + 3), int(by + 2))], fill=GOLD_BASE, width=1)
        ch_d.point((int(bx), int(by + 1)), fill=WHITE_SHINE)

    # 3. Articulated Legs with Amber Brass Armor
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
                r_l = int(np.clip(255 * (0.8 + 0.35 * spec), 0, 255))
                g_l = int(np.clip(140 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                b_l = int(np.clip(66 * (0.8 + 0.35 * spec) + 40 * spec, 0, 255))
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
                    # Warm Amber Orange Polished Brass Shell
                    r_t = int(np.clip(255 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_t = int(np.clip(140 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_t = int(np.clip(66 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center mini clockwork escapement / regulator window at (63, 75)
    ch_d.ellipse([60, 72, 66, 78], fill=OUTLINE)
    ch_d.ellipse([61, 73, 65, 77], fill=GOLD_BASE)
    ch_d.point((63, 75), fill=CORAL_BASE)
    ch_d.point((62, 74), fill=WHITE_SHINE)

    # Precision silicone pressure damper seam across mid-torso
    ch_d.arc([46, 68, 80, 88], start=20, end=160, fill=CORAL_BASE, width=1)

    # 5. Left Arm & Raised Balancing Palm (ready for thread guide)
    ch_d.line([(48, 73), (38, 84)], fill=AMBER_LIGHT, width=4)
    ch_d.ellipse([34, 82, 41, 89], fill=AMBER_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 84, 39, 87], fill=GOLD_BASE)

    # 6. Right Arm & Grip Hub (tucked at ribs)
    ch_d.line([(74, 72), (83, 75)], fill=AMBER_LIGHT, width=4)
    ch_d.ellipse([80, 73, 86, 79], fill=AMBER_BASE, outline=OUTLINE)
    ch_d.point((83, 76), fill=GOLD_BASE)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_hedgehog_brass_tuning_fork_ears.png
    # Features:
    # - Spherical Amber Polished Brass Helmet Dome at (64, 44), rx=18.5, ry=15.5
    # - Ivory White (#FFFDF8) enamel cheek and muzzle plates
    # - Knurled micrometer adjustment knob snout with golden clock hand whiskers
    # - Pair of semicircular polished brass tuning fork ears at (44, 26) and (84, 26)
    # - Forehead miniature escapement bridge plate at (64, 32)
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Amber Brass & Ivory Enamel Cheek)
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
                    r_h = int(np.clip(255 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_h = int(np.clip(140 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_h = int(np.clip(66 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Knurled Snout / Micrometer Knob & Smiling Mouth Seam
    hd.ellipse([62, 46, 66, 49], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 47), fill=WHITE_SHINE)
    hd.line([(64, 49), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([60, 50, 64, 54], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 50, 68, 54], start=0, end=180, fill=OUTLINE, width=1)

    # Forehead Escapement Bridge / Sensor Plate at (64, 32)
    hd.ellipse([61, 30, 67, 34], fill=GOLD_BASE, outline=OUTLINE)
    hd.ellipse([62, 31, 66, 33], fill=CORAL_BASE)
    hd.point((64, 32), fill=WHITE_SHINE)

    # 2. Semicircular Polished Brass Tuning Fork Ears at (44, 26) and (84, 26)
    ear_positions = [(44, 26), (84, 26)]
    for ex, ey in ear_positions:
        # Tuning fork outer curve
        hd.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=AMBER_BASE, outline=OUTLINE)
        hd.ellipse([ex - 4, ey - 4, ex + 4, ey + 4], fill=GOLD_BASE)
        # Inner resonance slot
        hd.ellipse([ex - 2, ey - 3, ex + 2, ey + 3], fill=AMBER_DEEP)
        hd.point((ex, ey - 1), fill=CORAL_BASE)
        hd.point((ex, ey - 4), fill=WHITE_SHINE)

    # 3. Golden Clock Hand Whiskers (走時指針鬍鬚 - 左右各一對)
    whisker_lines = [
        ([(47, 47), (32, 45)], [(46, 49), (31, 51)]),
        ([(81, 47), (96, 45)], [(82, 49), (97, 51)])
    ]
    for w_group in whisker_lines:
        for w_pts in w_group:
            hd.line(w_pts, fill=GOLD_BASE, width=2)
            # Arrow/diamond tip for clock hand
            tx, ty = w_pts[1]
            hd.point((tx, ty), fill=WHITE_SHINE)

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
    # File: optic_core/face_hedgehog_watchmaker_precision_loupe.png
    # Features:
    # - Left Eye at (52, 40): Obsidian gem jewel eye, brilliant white glint
    # - Right Eye at (76, 40): Watchmaker Precision Loupe (#4ED86A)
    #   - Brass mounting clamp ring (#FFD028 / #1F1A3A)
    #   - Phosphor mint green lens with concentric reticle and crosshair
    #   - Fully opaque lens center (alpha == 255, 0-ART27 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    # Left Eye: Deep Obsidian Jewel Eye at (52, 40)
    lex, ley = 52.0, 40.0
    r_eye = 4.2
    for y in range(int(ley - r_eye - 2), int(ley + r_eye + 3)):
        for x in range(int(lex - r_eye - 2), int(lex + r_eye + 3)):
            dist = ((x - lex)**2 + (y - ley)**2)**0.5
            if dist <= r_eye:
                spec = max(0.0, 1.0 - dist / r_eye)
                r_e = int(np.clip(25 * (0.8 + 0.3 * spec), 0, 255))
                g_e = int(np.clip(28 * (0.8 + 0.3 * spec), 0, 255))
                b_e = int(np.clip(45 * (0.8 + 0.3 * spec) + 20 * spec, 0, 255))
                core_img.putpixel((x, y), (r_e, g_e, b_e, 255))
    c_d.ellipse([int(lex - r_eye), int(ley - r_eye), int(lex + r_eye), int(ley + r_eye)], outline=OUTLINE, width=1)
    c_d.point((int(lex - 1), int(ley - 1)), fill=WHITE_SHINE)
    c_d.point((int(lex - 2), int(ley - 2)), fill=WHITE_SHINE)

    # Right Eye: Watchmaker Precision Loupe at (76, 40)
    rex, rey = 76.0, 40.0
    r_loupe = 4.8
    # Brass clamp ring
    c_d.ellipse([int(rex - r_loupe - 1), int(rey - r_loupe - 1), int(rex + r_loupe + 1), int(rey + r_loupe + 1)],
                fill=GOLD_DARK, outline=OUTLINE)
    # Mounting arm bracket
    c_d.line([(int(rex + r_loupe), int(rey)), (int(rex + r_loupe + 3), int(rey + 2))], fill=GOLD_BASE, width=2)

    for y in range(int(rey - r_loupe - 1), int(rey + r_loupe + 2)):
        for x in range(int(rex - r_loupe - 1), int(rex + r_loupe + 2)):
            dist = ((x - rex)**2 + (y - rey)**2)**0.5
            if dist <= r_loupe:
                spec = max(0.0, 1.0 - dist / r_loupe)
                shine = max(0.0, 1.0 - ((x - (rex - 1.5))**2 + (y - (rey - 1.5))**2)**0.5 / 2.0)**2
                # Concentric reticle ring
                is_reticle = (abs(dist - 2.6) <= 0.4)
                if is_reticle:
                    r_c, g_c, b_c = 210, 255, 225
                else:
                    r_c = int(np.clip(78 * (0.8 + 0.3 * spec) + 55 * shine, 0, 255))
                    g_c = int(np.clip(216 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    b_c = int(np.clip(106 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    c_d.ellipse([int(rex - r_loupe), int(rey - r_loupe), int(rex + r_loupe), int(rey + r_loupe)],
                outline=GOLD_BASE, width=1)
    # Crosshair tick marks
    c_d.line([(int(rex - 1.5), int(rey)), (int(rex + 1.5), int(rey))], fill=MINT_SHINE, width=1)
    c_d.line([(int(rex), int(rey - 1.5)), (int(rex), int(rey + 1.5))], fill=MINT_SHINE, width=1)
    c_d.point((int(rex - 1), int(rey - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_hedgehog_marionette_tailor_vest.png
    # Features:
    # - Marionette Tailor Vest (晨曦提線裁縫工匠馬甲)
    # - Rich horologist leather with fine spun cotton thread stitches
    # - Chest pocket holding miniature screwdriver & tweezers
    # - Coral pink bowtie / neck ribbon at (64, 58)
    # - Polished brass buckles and buttons
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
                is_vest = (abs(x - 63.0) >= 3.0 or y >= 68)
                if is_vest:
                    r_v = int(np.clip(142 * (0.8 + 0.35 * spec), 0, 255))
                    g_v = int(np.clip(82 * (0.8 + 0.35 * spec), 0, 255))
                    b_v = int(np.clip(45 * (0.8 + 0.35 * spec), 0, 255))
                    costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Fine spun cotton thread stitches along lapel
    stitch_pts = [(52, 62), (54, 66), (56, 70), (58, 74), (74, 62), (72, 66), (70, 70), (68, 74)]
    for sx, sy in stitch_pts:
        cos_d.point((sx, sy), fill=IVORY_LIGHT)

    # Coral Pink Bowtie / Collar Ribbon at (64, 58)
    cos_d.ellipse([62, 57, 66, 61], fill=CORAL_BASE, outline=OUTLINE)
    cos_d.polygon([(58, 56), (62, 59), (58, 62)], fill=CORAL_LIGHT, outline=OUTLINE)
    cos_d.polygon([(70, 56), (66, 59), (70, 62)], fill=CORAL_LIGHT, outline=OUTLINE)
    cos_d.point((64, 59), fill=WHITE_SHINE)

    # Chest Pocket with Screwdriver & Tweezers at (52, 72)
    cos_d.rectangle([51, 71, 56, 76], fill=VEST_DARK, outline=OUTLINE)
    # Screwdriver handle protruding
    cos_d.line([(52, 68), (52, 71)], fill=AMBER_LIGHT, width=2)
    cos_d.point((52, 67), fill=GOLD_BASE)
    # Tweezers tip protruding
    cos_d.line([(55, 67), (55, 71)], fill=STEEL_LIGHT, width=1)

    # Waist Belt & Brass Buckle
    cos_d.line([(50, 81), (76, 81)], fill=VEST_DARK, width=2)
    cos_d.rectangle([61, 79, 65, 83], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.point((63, 81), fill=WHITE_SHINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_hedgehog_ratchet_needle_dart.png
    # Features:
    # - Ratchet Needle-Dart / Shadow Quills (棘輪穿針機關鏢 / 巡影飛棘)
    # - Right-hand single held (0-MKT7 compliant) at (84, 75)
    # - Grip hub with knurled brass handle
    # - Amber brass rear rewind spool housing with coral thread terminal
    # - Ratchet locking collar disc
    # - Four-ridged quenched steel needle dart blade tapering to piercing tip at (118, 75)
    # - Phosphor mint green guidance line channel
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Grip Socket at (84, 75)
    wd.ellipse([81, 72, 87, 78], fill=AMBER_BASE, outline=OUTLINE)
    wd.ellipse([82, 73, 86, 77], fill=AMBER_LIGHT)
    wd.point((84, 75), fill=GOLD_BASE)

    # 2. Main Rewind Spool Housing (x: 85..95, y: 71..80)
    for y in range(71, 81):
        for x in range(85, 96):
            spec = max(0.0, 1.0 - ((x - 90)**2 + (y - 75)**2)**0.5 / 6.0)
            r_w = int(np.clip(255 * (0.8 + 0.3 * spec), 0, 255))
            g_w = int(np.clip(140 * (0.8 + 0.3 * spec) + 30 * spec, 0, 255))
            b_w = int(np.clip(66 * (0.8 + 0.3 * spec) + 40 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Thread Spool Eyelet & Coral Pink Terminal on Spool Housing
    wd.ellipse([87, 73, 91, 77], fill=GOLD_DARK, outline=OUTLINE)
    wd.ellipse([88, 74, 90, 76], fill=CORAL_BASE)
    wd.point((89, 75), fill=WHITE_SHINE)

    # 3. Ratchet Collar Disc (x: 95..98, y: 70..80)
    for y in range(70, 81):
        for x in range(95, 99):
            is_notch = (y % 2 == 0)
            c_col = GOLD_LIGHT if is_notch else GOLD_DARK
            weapon_img.putpixel((x, y), c_col)

    # 4. Quenched Steel Four-Ridged Needle Blade (x: 98..118, y: 73..77)
    tip_x, tip_y = 118.0, 75.0
    for x in range(98, int(tip_x) + 1):
        # Tapering half-height
        h_t = 3.5 * (1.0 - (x - 98) / (tip_x - 98)) + 0.4
        for y in range(int(tip_y - h_t - 1), int(tip_y + h_t + 2)):
            if abs(y - tip_y) <= h_t:
                spec = max(0.0, 1.0 - abs(y - tip_y) / (h_t + 1e-5))**2
                shine = max(0.0, (x - 98) / (tip_x - 98))

                # Center mint green energy / groove line
                is_groove = (abs(y - tip_y) <= 0.6 and x <= 112)
                if is_groove:
                    weapon_img.putpixel((x, y), MINT_BASE)
                else:
                    r_b = int(np.clip(90 * (0.8 + 0.35 * spec) + 80 * shine, 0, 255))
                    g_b = int(np.clip(86 * (0.8 + 0.35 * spec) + 80 * shine, 0, 255))
                    b_b = int(np.clip(102 * (0.8 + 0.35 * spec) + 100 * shine, 0, 255))
                    weapon_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Needle Razor Point at (118, 75)
    wd.point((118, 75), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 AND 512x512 LANCZOS SLICES
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_hedgehog_ratchet_and_pawl_cross", key_img),
        ("back_curio", "curio_hedgehog_spring_steel_quill_pack", curio_img),
        ("chassis", "chassis_hedgehog_amber_brass_default", chassis_img),
        ("head_unit", "head_hedgehog_brass_tuning_fork_ears", head_img),
        ("optic_core", "face_hedgehog_watchmaker_precision_loupe", core_img),
        ("costume", "costume_hedgehog_marionette_tailor_vest", costume_img),
        ("weapon", "weapon_hedgehog_ratchet_needle_dart", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{HEDGEHOG_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)

        # 128x128
        dst_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(dst_128)

        # 512x512 LANCZOS
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{slot_dir}/{item_id}_512.png"
        img_512.save(dst_512)

        print(f"  ✓ Saved {slot:<12}: 128 -> {dst_128}, 512 -> {dst_512}")

    # Universal copies for cross-race equipment indexing
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_hedgehog_ratchet_and_pawl_cross.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_hedgehog_ratchet_needle_dart.png")
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
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ordered_slices = [key_img, curio_img, chassis_img, head_unit_composite(head_img, core_img), costume_img, weapon_img]

    # Let's do exact canonical order
    comp_exact = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_img in [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]:
        comp_exact.alpha_composite(s_img)

    comp_path = f"{HEDGEHOG_PD_DIR}/proof_paperdoll_hedgehog_composite.png"
    comp_exact.save(comp_path)
    print("  ✓ Composite saved:", comp_path)

    # Magenta proof (proof_paperdoll_hedgehog_magenta.png)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(comp_exact)
    mag_path = f"{HEDGEHOG_PD_DIR}/proof_paperdoll_hedgehog_magenta.png"
    magenta_bg.save(mag_path)
    print("  ✓ Magenta proof saved:", mag_path)

    # 7 slices proof (proof_hedgehog_all_7_slices.png)
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
        # Grid box
        s_draw = ImageDraw.Draw(strip)
        s_draw.rectangle([px, 0, px + W - 1, H - 1], outline=(200, 200, 210, 255))
        s_draw.text((px + 4, 4), label_txt, fill=(60, 60, 80, 255))
        strip.alpha_composite(sl_img, (px, 0))

    strip_path = f"{HEDGEHOG_PD_DIR}/proof_hedgehog_all_7_slices.png"
    strip.save(strip_path)
    print("  ✓ 7 Slices Proof saved:", strip_path)

    # SHOWCASE HD (game/assets/sprites/player/showcase/hedgehog_idle_hd.png)
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
        sc_draw = ImageDraw.Draw(showcase_hd)
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
        showcase_dst = f"{showcase_dir}/hedgehog_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


def head_unit_composite(head, core):
    out = head.copy()
    out.alpha_composite(core)
    return out


if __name__ == "__main__":
    build_all()
