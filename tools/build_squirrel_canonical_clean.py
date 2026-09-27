#!/usr/bin/env python3
"""
build_squirrel_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十五族 巡林松鼠 (The Timber Squirrel, squirrel) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/TIMBER_SQUIRREL_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped polished copper plates,
  ivory enamel cheek/chest plates, folding thin brass wind-vane ears, vulcanized silicone boots with claw grips,
  three-ring acorn filigree winding key, 9-segment articulated cogwheel gyro-tail, emerald clockwork foil weapon)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette:
    Primary Hull: Chestnut Bronze Stamped Copper (#8B5A2B)
    Secondary Hull: Almond Gold Orange (#D27D2D)
    Chest & Faceplate Enamel: Ivory White Enamel (#FFFDF8)
    Ranger Costume & Beret: Forest Emerald Green (#2D8A4E)
    Accent & Key: Dopamine Gold (#FFD028)
    Detail & Optics: Phosphor Mint Green (#4ED86A)
    Tungsten Frame & Blade: Cold-Rolled Tungsten Steel (#4A5568)
    Highlight & Bushings: Coral Pink High-Pressure Seals (#FF5E8A)
    Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
SQUIRREL_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/squirrel"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Timber Squirrel Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (96, 62, 24, 255)        # Deep warm bronze for key filigree (complies with 0-ART29 dark limit)

# Primary Hull: Chestnut Bronze Stamped Copper (#8B5A2B)
CHESTNUT_BASE  = (139, 90, 43, 255)
CHESTNUT_LIGHT = (175, 118, 62, 255)
CHESTNUT_SHINE = (215, 155, 95, 255)
CHESTNUT_DARK  = (102, 62, 26, 255)
CHESTNUT_DEEP  = (68, 38, 14, 255)

# Secondary Hull: Almond Gold Orange (#D27D2D)
ALMOND_BASE  = (210, 125, 45, 255)
ALMOND_LIGHT = (238, 158, 78, 255)
ALMOND_SHINE = (255, 195, 125, 255)
ALMOND_DARK  = (165, 92, 28, 255)

# Faceplate & Chest Enamel: Ivory White (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (230, 224, 215, 255)
IVORY_DARK    = (195, 188, 178, 255)

# Accent: Dopamine Golden Brass & Winding Key (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# Detail: Forest Emerald Green (#2D8A4E)
EMERALD_BASE  = (45, 138, 78, 255)
EMERALD_LIGHT = (68, 178, 105, 255)
EMERALD_SHINE = (115, 218, 148, 255)
EMERALD_DARK  = (28, 95, 52, 255)
EMERALD_DEEP  = (16, 60, 32, 255)

# Detail: Phosphor Mint Green Optics & Crystals (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (140, 240, 165, 255)
MINT_SHINE = (210, 255, 225, 255)
MINT_DARK  = (36, 140, 62, 255)

# Highlight: Coral Pink High-Pressure Seals & Bearings (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

# Tungsten Frame: Cold-Rolled Tungsten Steel (#4A5568)
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (118, 132, 155, 255)
STEEL_SHINE = (175, 188, 210, 255)
STEEL_DARK  = (48, 56, 70, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL TIMBER SQUIRREL SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_squirrel_acorn_filigree.png
    # Three-Ring Acorn Filigree Brass Winding Key (三環橡果鏤空黃銅發條鑰匙)
    # Socket boss at upper spine (64, 60), shaft extends diagonally up-right to (86, 28)
    # Features:
    # - Polished brass shaft with bevel shading
    # - Three interlocking baroque filigree rings in dopamine gold (#FFD028)
    # - Central micro-carved wind-up acorn with gear teeth on cap
    # - Central coral pink pivot gem / bearing
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 60) to (86, 28)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 22.0
        sy = 60.0 - t * 32.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 60)
    kd.ellipse([60, 56, 68, 64], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([61, 57, 67, 63], fill=GOLD_BASE)
    kd.ellipse([63, 59, 65, 61], fill=CORAL_BASE)

    # 2. Key Hub at (86, 28) with Three Interlocking Filigree Rings
    kcx, kcy = 86.0, 28.0

    # Three rings: Top ring at (86, 17), Left ring at (75, 27), Right ring at (97, 27)
    ring_centers = [(86.0, 17.0), (75.0, 27.0), (97.0, 27.0)]
    for rcx, rcy in ring_centers:
        r_outer = 9.5
        r_inner = 5.2
        for y in range(int(rcy - r_outer - 2), int(rcy + r_outer + 3)):
            for x in range(int(rcx - r_outer - 2), int(rcx + r_outer + 3)):
                dist = ((x - rcx)**2 + (y - rcy)**2)**0.5
                if r_inner <= dist <= r_outer:
                    norm_r = (dist - r_inner) / (r_outer - r_inner)
                    spec = max(0.0, np.sin(norm_r * np.pi))
                    shine = max(0.0, 1.0 - ((x - (rcx - 2.5))**2 + (y - (rcy - 2.5))**2)**0.5 / 5.0)**2
                    r_w = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_w = int(np.clip(208 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                    b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Decorative crest finial at top ring peak (86, 7)
    kd.ellipse([84, 5, 88, 9], fill=GOLD_BASE, outline=OUTLINE_KEY)
    kd.point((86, 6), fill=WHITE_SHINE)

    # 3. Central Carved Wind-up Acorn at (86, 28)
    for y in range(27, 36):
        for x in range(81, 92):
            dx = (x - 86.0) / 4.5
            dy = (y - 30.5) / 5.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 84.5)**2 + (y - 29.0)**2)**0.5 / 5.0)
                shine = max(0.0, 1.0 - ((x - 84.5)**2 + (y - 29.0)**2)**0.5 / 2.5)**2
                r_a = int(np.clip(175 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                g_a = int(np.clip(118 * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                b_a = int(np.clip(62 * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                key_img.putpixel((x, y), (r_a, g_a, b_a, 255))

    # Acorn gear-cap (upper half): golden cog teeth cap
    kd.arc([81, 23, 91, 29], start=180, end=360, fill=GOLD_BASE, width=3)
    for cx in range(82, 91, 2):
        kd.point((cx, 24), fill=GOLD_LIGHT)
        kd.point((cx, 23), fill=WHITE_SHINE)

    # Acorn stem / top tip
    kd.line([(86, 23), (86, 20)], fill=GOLD_DARK, width=2)
    kd.point((86, 20), fill=GOLD_LIGHT)

    # Central coral jewel at acorn core (86, 31)
    kd.ellipse([85, 30, 87, 32], fill=CORAL_BASE, outline=OUTLINE_KEY)
    kd.point((86, 30), fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline to guarantee 0-ART29 compliance
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_squirrel_articulated_cog_gyro_tail.png
    # 9-Segment Articulated Cogwheel Gyro-Tail (九節鉸鏈同軸沖壓鏤空黃銅齒輪陀螺大尾巴)
    # Originates at sacrum (48, 92), sweeps in a glorious upward/backward squirrel curve:
    # (48, 92) -> (40, 86) -> (28, 76) -> (20, 62) -> (22, 46) -> (30, 34) -> (44, 24) -> (52, 28)
    # Features:
    # - 9 articulated gear nodes with radial cross-spokes and central hubs
    # - Pierced gear rings with teeth and concentric relief
    # - Central flexible steel transmission cable linking all 9 segment hubs
    # - Miniature gyro balance rotor / brass acorn finial at tip
    # - Rich chestnut bronze (#8B5A2B), almond orange (#D27D2D), dopamine gold (#FFD028)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Segment definitions: (cx, cy, outer_radius, inner_radius, num_teeth, is_gold)
    tail_segments = [
        (48.0, 92.0,  5.5, 2.5,  6, False),  # Seg 1: Root hinge at spine
        (40.0, 86.0,  7.0, 3.2,  8, False),  # Seg 2: Ascending curve
        (30.0, 78.0,  9.0, 4.2, 10, True),   # Seg 3: Expanding lower swell
        (22.0, 66.0, 11.0, 5.0, 12, True),   # Seg 4: Main bushy belly
        (19.0, 52.0, 12.0, 5.5, 12, True),   # Seg 5: Widest crown of tail
        (23.0, 39.0, 11.0, 5.0, 10, True),   # Seg 6: Upper curve
        (32.0, 29.0,  9.0, 4.0,  8, True),   # Seg 7: Arching forward
        (43.0, 24.0,  7.5, 3.2,  8, False),  # Seg 8: Inward curl
        (51.0, 28.0,  5.5, 2.2,  6, False),  # Seg 9: Gyro finial tip
    ]

    # 1. Central flexible steel transmission spine cable linking all hubs
    for i in range(len(tail_segments) - 1):
        x0, y0 = tail_segments[i][0], tail_segments[i][1]
        x1, y1 = tail_segments[i+1][0], tail_segments[i+1][1]
        for t in np.linspace(0.0, 1.0, 25):
            sx = x0 + t * (x1 - x0)
            sy = y0 + t * (y1 - y0)
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    curio_img.putpixel((int(sx + dx), int(sy + dy)), STEEL_LIGHT)

    # 2. Draw 9 Articulated Pierced Cogwheel Segments with Cross-Spokes
    for i, (scx, scy, r_out, r_in, teeth, is_gold) in enumerate(tail_segments):
        # Ring body with multi-tone gradient
        for y in range(int(scy - r_out - 2), int(scy + r_out + 3)):
            for x in range(int(scx - r_out - 2), int(scx + r_out + 3)):
                dist = ((x - scx)**2 + (y - scy)**2)**0.5
                if dist <= r_out:
                    angle = np.arctan2(y - scy, x - scx)
                    # Cog tooth modulation
                    tooth_phase = (angle * teeth / (2.0 * np.pi)) % 1.0
                    is_tooth = (dist >= r_out - 1.5) and (tooth_phase < 0.5)

                    # 4 radial gear spokes connecting rim to axle hub
                    is_spoke = (dist < r_in) and (abs(np.sin(angle * 2.0)) <= 0.35)

                    if dist >= r_in or is_spoke or dist <= 2.5:
                        norm_r = (dist - r_in) / (r_out - r_in) if dist >= r_in else 0.5
                        spec = max(0.0, np.sin(norm_r * np.pi))
                        shine = max(0.0, 1.0 - ((x - (scx - 2.5))**2 + (y - (scy - 2.5))**2)**0.5 / (r_out * 0.7))**2

                        if is_gold:
                            r_g = int(np.clip(255 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                            g_g = int(np.clip(208 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                            b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * shine, 0, 255))
                        else:
                            r_g = int(np.clip(210 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                            g_g = int(np.clip(125 * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                            b_g = int(np.clip(45 * (0.8 + 0.35 * spec) + 45 * shine, 0, 255))

                        curio_img.putpixel((x, y), (r_g, g_g, b_g, 255))

        # Distinct cog teeth tips around perimeter
        for ti in range(teeth):
            tang = ti * (2.0 * np.pi / teeth)
            tx = int(scx + (r_out + 1.2) * np.cos(tang))
            ty = int(scy + (r_out + 1.2) * np.sin(tang))
            if 0 <= tx < W and 0 <= ty < H:
                curio_img.putpixel((tx, ty), GOLD_LIGHT if is_gold else ALMOND_LIGHT)

        # Central axle hub & bearing
        cd.ellipse([int(scx - 2.5), int(scy - 2.5), int(scx + 2.5), int(scy + 2.5)], fill=STEEL_DARK, outline=OUTLINE)
        cd.ellipse([int(scx - 1.5), int(scy - 1.5), int(scx + 1.5), int(scy + 1.5)], fill=GOLD_BASE)
        cd.point((int(scx), int(scy)), fill=CORAL_BASE if (i % 2 == 1) else WHITE_SHINE)

    # 3. Micro Gyro Flywheel Finial at Tip (51, 28)
    cd.ellipse([49, 26, 53, 30], fill=GOLD_LIGHT, outline=OUTLINE)
    cd.point((51, 28), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_squirrel_chestnut_bronze_default.png
    # Features:
    # - 2.2 Chibi agile fencer posture
    # - Soft ground contact shadow at (64, 116)
    # - High-traction rubber boots with 3 claw teeth and tungsten joints (#4A5568 / #202026)
    # - Articulated legs with chestnut bronze armor (#8B5A2B) & coral pink damper rings (#FF5E8A)
    # - Solid chestnut bronze neck collar at (x: 54..74, y: 48..58) for seamless head seating
    # - Chestnut bronze stamped copper torso (#8B5A2B) with almond orange beveling (#D27D2D)
    # - Ivory White (#FFFDF8) enamel chest & belly shock-absorbing plate
    # - Three non-slip maintenance / heat dissipation slots on belly
    # - Left hand curved forward/raised in balancing stance at (38, 84)
    # - Right arm tucked at ribs at (83, 75) ready to thrust
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. High-Traction Vulcanized Boots with Front Claw Teeth
    boot_pos = [(48.0, 113.0), (70.0, 113.0)]
    for bx, by in boot_pos:
        ch_d.ellipse([int(bx - 7), int(by - 2), int(bx + 7), int(by + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(bx - 5), int(by - 1), int(bx + 5), int(by + 2)], fill=SILICONE_LIGHT)
        ch_d.ellipse([int(bx - 4), int(by), int(bx + 4), int(by + 3)], fill=CHESTNUT_BASE)
        for cdx in [-3, 0, 3]:
            ch_d.line([(int(bx + cdx), int(by + 2)), (int(bx + cdx), int(by + 4))], fill=STEEL_LIGHT, width=1)
        ch_d.point((int(bx), int(by + 1)), fill=WHITE_SHINE)

    # 3. Articulated Legs with Chestnut Bronze Armor
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
                r_l = int(np.clip(139 * (0.8 + 0.35 * spec), 0, 255))
                g_l = int(np.clip(90 * (0.8 + 0.35 * spec) + 25 * spec, 0, 255))
                b_l = int(np.clip(43 * (0.8 + 0.35 * spec) + 30 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 2, mid_x + 3, mid_y + 2], fill=CORAL_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 54..74, y: 48..58)
    for ny in range(48, 59):
        for nx in range(54, 75):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 10.0)
            r_n = int(np.clip(139 * (0.8 + 0.35 * spec), 0, 255))
            g_n = int(np.clip(90 * (0.8 + 0.35 * spec) + 20 * spec, 0, 255))
            b_n = int(np.clip(43 * (0.8 + 0.35 * spec) + 20 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 5. Torso Body Shell (x: 44..84, y: 56..96)
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
                    # Warm Chestnut Bronze Polished Copper Shell
                    r_t = int(np.clip(139 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_t = int(np.clip(90 * (0.75 + 0.45 * spec) - 15 * edge_shade + 45 * shine, 0, 255))
                    b_t = int(np.clip(43 * (0.75 + 0.45 * spec) - 10 * edge_shade + 45 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center mini clockwork regulator window at (63, 75)
    ch_d.ellipse([60, 72, 66, 78], fill=OUTLINE)
    ch_d.ellipse([61, 73, 65, 77], fill=GOLD_BASE)
    ch_d.point((63, 75), fill=CORAL_BASE)
    ch_d.point((62, 74), fill=WHITE_SHINE)

    # Three ventilation / inspection slots on belly plate
    for sy in [81, 84, 87]:
        ch_d.line([(59, sy), (67, sy)], fill=CHESTNUT_DARK, width=1)
        ch_d.line([(60, sy), (66, sy)], fill=OUTLINE, width=1)

    # 6. Left Arm & Raised Balancing Palm
    ch_d.line([(48, 73), (38, 84)], fill=CHESTNUT_LIGHT, width=4)
    ch_d.ellipse([34, 82, 41, 89], fill=CHESTNUT_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 84, 39, 87], fill=GOLD_BASE)

    # 7. Right Arm & Grip Hub (tucked at ribs)
    ch_d.line([(74, 72), (83, 75)], fill=CHESTNUT_LIGHT, width=4)
    ch_d.ellipse([80, 73, 86, 79], fill=CHESTNUT_BASE, outline=OUTLINE)
    ch_d.point((83, 76), fill=GOLD_BASE)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_squirrel_timber_fencer_beret.png
    # Features:
    # - Spherical Chestnut Bronze skull dome at (64, 44), rx=18.5, ry=15.5
    # - Ivory White (#FFFDF8) enamel cheek & muzzle plates with micro screws
    # - Knurled brass snout & smiling fencer mouth seam
    # - Twin folding thin brass wind-vane ears at (38, 20) and (86, 22)
    # - Emerald green fencer beret (#2D8A4E) tilted elegantly on head
    # - Dopamine golden wind-up feather / quill ornament (#FFD028) on right side of beret
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 18.5, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Chestnut Bronze & Ivory Enamel Cheek)
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
                    r_h = int(np.clip(139 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_h = int(np.clip(90 * (0.75 + 0.45 * spec) - 15 * edge_shade + 45 * shine, 0, 255))
                    b_h = int(np.clip(43 * (0.75 + 0.45 * spec) - 10 * edge_shade + 45 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Knurled Snout / Copper Knob & Smiling Mouth Seam
    hd.ellipse([62, 46, 66, 49], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 47), fill=WHITE_SHINE)
    hd.line([(64, 49), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([60, 50, 64, 54], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 50, 68, 54], start=0, end=180, fill=OUTLINE, width=1)

    # Cheek Screws
    hd.ellipse([46, 46, 48, 48], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((47, 47), fill=WHITE_SHINE)
    hd.ellipse([80, 46, 82, 48], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((81, 47), fill=WHITE_SHINE)

    # 2. Twin Folding Thin Brass Wind-Vane Ears at (38, 20) and (86, 22)
    # Left Ear
    hd.polygon([(46, 32), (36, 17), (43, 14), (50, 28)], fill=CHESTNUT_BASE, outline=OUTLINE)
    hd.polygon([(45, 30), (38, 18), (43, 16), (48, 27)], fill=ALMOND_BASE)
    hd.line([(44, 28), (40, 18)], fill=GOLD_BASE, width=1)
    hd.ellipse([46, 30, 50, 34], fill=GOLD_DARK, outline=OUTLINE)
    hd.point((48, 32), fill=CORAL_BASE)

    # Right Ear
    hd.polygon([(82, 33), (85, 16), (92, 18), (85, 33)], fill=CHESTNUT_BASE, outline=OUTLINE)
    hd.polygon([(83, 31), (86, 18), (90, 19), (86, 31)], fill=ALMOND_BASE)
    hd.line([(85, 30), (88, 19)], fill=GOLD_BASE, width=1)
    hd.ellipse([80, 31, 84, 35], fill=GOLD_DARK, outline=OUTLINE)
    hd.point((82, 33), fill=CORAL_BASE)

    # 3. Emerald Green Fencer Beret (#2D8A4E) tilted elegantly over top of head
    for y in range(24, 36):
        for x in range(48, 76):
            dx = (x - 62.0) / 13.5
            dy = (y - 30.0) / 5.5
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 28)**2)**0.5 / 12.0)
                shine = max(0.0, 1.0 - ((x - 58)**2 + (y - 28)**2)**0.5 / 4.0)**2
                r_b = int(np.clip(45 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                g_b = int(np.clip(138 * (0.8 + 0.35 * spec) + 50 * shine, 0, 255))
                b_b = int(np.clip(78 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                head_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    hd.arc([48, 27, 75, 36], start=0, end=180, fill=EMERALD_DARK, width=2)
    hd.point((62, 27), fill=EMERALD_SHINE)

    # Dopamine Gold Wind-up Feather / Quill (#FFD028)
    hd.line([(70, 29), (79, 19)], fill=GOLD_BASE, width=2)
    hd.polygon([(74, 24), (79, 19), (78, 25)], fill=GOLD_LIGHT, outline=OUTLINE)
    hd.point((79, 19), fill=WHITE_SHINE)
    hd.ellipse([69, 28, 72, 31], fill=CORAL_BASE, outline=OUTLINE)

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
    # File: optic_core/face_squirrel_mint_crosshair_lens.png
    # Features:
    # - Twin Phosphor Mint Green Optical Crystal Lenses at (52, 40) and (76, 40)
    # - Brass mounting bezel rings (#FFD028 / #1F1A3A)
    # - Phosphor mint green crystal lens with concentric reticle and crosshairs
    # - Brilliant white glints (confidence fencer expression)
    # - Fully opaque lens center (alpha == 255, min_alpha > 200, 0-ART27 & 0-QA31 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in eye_centers:
        r_lens = 4.5
        c_d.ellipse([int(ex - r_lens - 1), int(ey - r_lens - 1), int(ex + r_lens + 1), int(ey + r_lens + 1)],
                    fill=GOLD_DARK, outline=OUTLINE)

        for y in range(int(ey - r_lens - 1), int(ey + r_lens + 2)):
            for x in range(int(ex - r_lens - 1), int(ex + r_lens + 2)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= r_lens:
                    spec = max(0.0, 1.0 - dist / r_lens)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.2))**2 + (y - (ey - 1.2))**2)**0.5 / 2.0)**2
                    is_reticle = (abs(dist - 2.5) <= 0.4)
                    if is_reticle:
                        r_c, g_c, b_c = 210, 255, 225
                    else:
                        r_c = int(np.clip(78 * (0.8 + 0.3 * spec) + 55 * shine, 0, 255))
                        g_c = int(np.clip(216 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        b_c = int(np.clip(106 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        c_d.ellipse([int(ex - r_lens), int(ey - r_lens), int(ex + r_lens), int(ey + r_lens)],
                    outline=GOLD_BASE, width=1)
        c_d.line([(int(ex - 1.5), int(ey)), (int(ex + 1.5), int(ey))], fill=MINT_SHINE, width=1)
        c_d.line([(int(ex), int(ey - 1.5)), (int(ex), int(ey + 1.5))], fill=MINT_SHINE, width=1)
        c_d.point((int(ex - 1), int(ey - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_squirrel_canopy_courier_harness.png
    # Features:
    # - Canopy Courier Harness (林冠信差遊俠短披風與擊劍皮扣裝甲)
    # - Deep Forest Emerald Green (#2D8A4E) ranger half-cape with rich folds
    # - Diagonal chestnut leather chest harness with golden gear buckle (#FFD028)
    # - Stamped brass vine medallion / heart mirror (#FFD028)
    # - Miniature courier pouch with brass clasp at left hip (47, 80)
    # - Fine spun ivory / gold stitch detailing
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
                shine = max(0.0, 1.0 - ((x - 59)**2 + (y - 68)**2)**0.5 / 4.0)**2
                is_vest = (abs(x - 63.0) >= 3.0 or y >= 68)
                if is_vest:
                    r_v = int(np.clip(45 * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    g_v = int(np.clip(138 * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                    b_v = int(np.clip(78 * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Diagonal Leather Harness Belt (from right shoulder 70, 60 down to left hip 54, 82)
    for t in np.linspace(0.0, 1.0, 30):
        bx = 70.0 - t * 16.0
        by = 60.0 + t * 22.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                costume_img.putpixel((int(bx + dx), int(by + dy)), CHESTNUT_DARK)

    # Stamped Brass Gear Buckle / Medallion at chest center (63, 69)
    cos_d.ellipse([60, 66, 66, 72], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([61, 67, 65, 71], fill=GOLD_LIGHT)
    cos_d.point((63, 69), fill=CORAL_BASE)
    cos_d.point((62, 68), fill=WHITE_SHINE)

    # Courier Pouch / Parts Box at Left Hip (50, 78)
    cos_d.rectangle([48, 77, 54, 83], fill=CHESTNUT_BASE, outline=OUTLINE)
    cos_d.rectangle([49, 78, 53, 80], fill=ALMOND_BASE)
    cos_d.ellipse([50, 79, 52, 81], fill=GOLD_BASE, outline=OUTLINE)

    # Fine gold / ivory stitch points along collar & hem
    stitch_pts = [(53, 62), (55, 66), (57, 70), (73, 62), (71, 66), (69, 70)]
    for sx, sy in stitch_pts:
        cos_d.point((sx, sy), fill=GOLD_LIGHT)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_squirrel_emerald_clockwork_foil.png
    # Features:
    # - Emerald Clockwork Foil / Timber Needler Rapier (翡翠發條細劍)
    # - Right-hand single held (0-MKT7 compliant) at (84, 75)
    # - Spiral knurled brass grip with emerald core pommel at (80, 75)
    # - Circular pierced gear-wheel guard (鏤空齒輪圓盤護手, #FFD028)
    # - Flexible cold-rolled tungsten steel needle blade tapering to needle point at (118, 75)
    # - Micro calibration marks and brilliant tip glint
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Pommel with Mint Crystal Gem at (80, 75)
    wd.ellipse([78, 73, 81, 77], fill=GOLD_DARK, outline=OUTLINE)
    wd.ellipse([79, 74, 80, 76], fill=MINT_BASE)
    wd.point((79, 74), fill=WHITE_SHINE)

    # 2. Spiral Brass Grip (x: 81..86, y: 74..76)
    for x in range(81, 87):
        for y in range(74, 77):
            spec = max(0.0, 1.0 - abs(y - 75.0) / 1.5)
            r_g = int(np.clip(255 * (0.8 + 0.3 * spec), 0, 255))
            g_g = int(np.clip(208 * (0.8 + 0.3 * spec), 0, 255))
            b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_g, g_g, b_g, 255))

    # 3. Pierced Gear-Wheel Guard (鏤空齒輪圓盤護手) at (87, 75)
    for y in range(68, 83):
        for x in range(85, 91):
            dx = (x - 87.5) / 3.0
            dy = (y - 75.0) / 7.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                is_rim = (dist_sq >= 0.5)
                spec = max(0.0, 1.0 - abs(y - 75.0) / 7.0)
                if is_rim:
                    r_w = int(np.clip(255 * (0.8 + 0.35 * spec), 0, 255))
                    g_w = int(np.clip(208 * (0.8 + 0.35 * spec), 0, 255))
                    b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * spec, 0, 255))
                else:
                    is_spoke = (y % 3 == 0)
                    r_w = 255 if is_spoke else 195
                    g_w = 208 if is_spoke else 145
                    b_w = 40 if is_spoke else 18
                weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    for ty in [68, 71, 75, 79, 82]:
        wd.point((88, ty), fill=GOLD_LIGHT)

    # 4. Needle-Foil Blade tapering from (90, 75) to piercing tip at (118, 75)
    blade_x0 = 90.0
    blade_x1 = 118.0
    for x in range(int(blade_x0), int(blade_x1) + 1):
        t = (x - blade_x0) / (blade_x1 - blade_x0)
        half_w = 1.8 * (1.0 - t) + 0.4
        for y_off in np.linspace(-half_w, half_w, 5):
            iy = int(round(75.0 + y_off))
            dist_center = abs(y_off) / half_w
            spec = max(0.0, 1.0 - dist_center)
            shine = max(0.0, 1.0 - t)**2

            r_b = int(np.clip(74 * (0.8 + 0.4 * spec) + 140 * spec + 60 * shine, 0, 255))
            g_b = int(np.clip(85 * (0.8 + 0.4 * spec) + 140 * spec + 60 * shine, 0, 255))
            b_b = int(np.clip(104 * (0.8 + 0.4 * spec) + 150 * spec + 60 * shine, 0, 255))
            weapon_img.putpixel((x, iy), (r_b, g_b, b_b, 255))

    for mx in [95, 100, 105, 110]:
        wd.point((mx, 74), fill=MINT_LIGHT)

    wd.point((118, 75), fill=WHITE_SHINE)
    wd.point((117, 75), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_squirrel_acorn_filigree", key_img),
        ("back_curio", "curio_squirrel_articulated_cog_gyro_tail", curio_img),
        ("chassis", "chassis_squirrel_chestnut_bronze_default", chassis_img),
        ("head_unit", "head_squirrel_timber_fencer_beret", head_img),
        ("optic_core", "face_squirrel_mint_crosshair_lens", core_img),
        ("costume", "costume_squirrel_canopy_courier_harness", costume_img),
        ("weapon", "weapon_squirrel_emerald_clockwork_foil", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{SQUIRREL_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{SQUIRREL_PD_DIR}/winding_key/key_squirrel_acorn_filigree.png",
                    f"{KEY_DIR}/key_squirrel_acorn_filigree.png")
    shutil.copyfile(f"{SQUIRREL_PD_DIR}/weapon/weapon_squirrel_emerald_clockwork_foil.png",
                    f"{WEAPON_DIR}/weapon_squirrel_emerald_clockwork_foil.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order by layer_z_index:
    # z=5: winding_key
    # z=8: back_curio
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

    proof_comp = f"{SQUIRREL_PD_DIR}/proof_paperdoll_squirrel_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SQUIRREL_PD_DIR}/proof_paperdoll_squirrel_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
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

    strip_path = f"{SQUIRREL_PD_DIR}/proof_squirrel_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/squirrel_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/squirrel_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
