#!/usr/bin/env python3
"""
build_hippo_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十六族 重閥河馬 (The Steamvalve Hippo, hippo) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/design/STEAMVALVE_HIPPO_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological tissue, stamped heavy brass plates #FFA010/#FFFDF8,
  cold-rolled tungsten steel framework, rotating safety relief valve ears #FF5E8A,
  manometer pressure gauge optic core #4ED86A, dual steam exhaust ballast tail #FFA010/#FFD028,
  steamvalve piston heavy lance #FFD028/#4ED86A, dual valve handwheel brass key #FFD028)
- references/art_direction.md & references/brand_assets.md
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIPPO_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hippo"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Steamvalve Hippo Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory Canvas & Stamped Tinplate (#FFFDF8, #E8ECF2)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (232, 236, 242, 255)
IVORY_DARK   = (204, 212, 224, 255)

# 2. Dopamine Gold & Brass (#FFD028, #E6A15C)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

BRASS_BASE  = (230, 161, 92, 255)
BRASS_LIGHT = (248, 196, 142, 255)
BRASS_DARK  = (175, 110, 50, 255)

# 3. Primary: Dopamine Warm Orange / Thick Cast Brass (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 4. Cold-Rolled Tungsten & Sanded Tinplate Plates (#5A4E46, #7A6C62, #3A322D)
TIN_SHINE = (156, 142, 134, 255)
TIN_LIGHT = (122, 108, 98, 255)
TIN_BASE  = (90, 78, 70, 255)
TIN_DARK  = (58, 50, 45, 255)
TIN_DEEP  = (38, 32, 28, 255)

# 5. Accent: Coral Pink (#FF5E8A) for safety relief valve warning rings & pull valves
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 195, 215, 255)
CORAL_DARK  = (210, 45, 95, 255)

# 6. Secondary: Mint Green Optic Quartz Manometer (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (133, 255, 160, 255)
MINT_SHINE = (200, 255, 215, 255)
MINT_DARK  = (40, 160, 68, 255)

# 7. Sky Blue & Steam Vapor (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)

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
            if px_snap[x, y][3] > min_alpha:
                continue

            if ignore_regions:
                in_ignored = False
                for rx0, ry0, rx1, ry1 in ignore_regions:
                    if rx0 <= x <= rx1 and ry0 <= y <= ry1:
                        in_ignored = True
                        break
                if in_ignored:
                    continue

            # Check 4-connectivity
            has_opaque_neighbor = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    if px_snap[nx, ny][3] >= min_alpha:
                        has_opaque_neighbor = True
                        break

            if has_opaque_neighbor:
                px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 第五十六族 重閥河馬 (THE STEAMVALVE HIPPO) CANONICAL ASSETS ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Under Chassis / Back Layer)
    # File: winding_key/key_hippo_dual_valve_handwheel_brass.png
    # Features:
    # - 雙聯閥門輪轂黃銅發條鑰匙 (Dual Valve Handwheel Brass Key)
    # - Standing upright on back, central brass spindle from (64, 44) up to (64, 22)
    # - Classical industrial steam pipe handwheel design at (64.0, 18.0)
    # - Outer handwheel rim (radius 13.5, inner radius 9.5) with non-slip knurled grip notches
    # - Inner concentric valve hub ring (radius 4.5) with central coral pink lock washer (#FF5E8A)
    # - Four cross/diagonal reinforcing steel spokes connecting hub to outer rim
    # - Complies with 0-ART29: warm golden bronze outline OUTLINE_KEY, 0 dark artifacts
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Vertical Key Spindle Shaft (x: 62..66, y: 22..44)
    for sy in range(22, 45):
        for sx in range(62, 67):
            shade = 1.0 - abs(sx - 64.0) / 2.5
            shine = max(0.0, 1.0 - abs(sx - 63.0) / 1.5)**2
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * shade) + 30 * shine, 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * shade) + 25 * shine, 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade) + 15 * shine, 0, 255))
            key_img.putpixel((sx, sy), (r, g, b, 255))

    # Mounting flange collar
    kd.rectangle([59, 39, 69, 44], fill=GOLD_BASE, outline=OUTLINE_KEY)
    kd.rectangle([58, 42, 70, 46], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.line([(59, 40), (69, 40)], fill=GOLD_LIGHT, width=1)

    # 2. Outer Handwheel Valve Rim centered at (64.0, 18.0)
    hx, hy = 64.0, 18.0
    r_outer = 13.5
    r_inner = 9.5
    for dy in range(int(-r_outer - 3), int(r_outer + 4)):
        for dx in range(int(-r_outer - 3), int(r_outer + 4)):
            d = (dx**2 + dy**2)**0.5
            px = int(round(hx + dx))
            py = int(round(hy + dy))
            if 0 <= px < W and 0 <= py < H:
                if r_inner <= d <= r_outer:
                    spec = max(0.0, 1.0 - abs(d - 0.5 * (r_inner + r_outer)) / 2.0)
                    shine = max(0.0, 1.0 - ((dx - 2.0)**2 + (dy + 2.0)**2)**0.5 / 5.0)**2
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    # Knurled grip ridges on outer rim (12 notches)
    for i in range(12):
        theta = i * (2.0 * np.pi / 12.0)
        nx = int(round(hx + np.cos(theta) * (r_outer + 0.8)))
        ny = int(round(hy + np.sin(theta) * (r_outer + 0.8)))
        if 0 <= nx < W and 0 <= ny < H:
            key_img.putpixel((nx, ny), GOLD_LIGHT if i % 2 == 0 else GOLD_DARK)

    # 3. Four Handwheel Spokes (Cross / Diagonal spokes connecting hub to rim)
    spoke_angles = [0.0, np.pi * 0.5, np.pi, np.pi * 1.5]
    for ang in spoke_angles:
        cos_a = np.cos(ang)
        sin_a = np.sin(ang)
        for dist in np.linspace(4.0, 10.5, 14):
            sx = int(round(hx + dist * cos_a))
            sy = int(round(hy + dist * sin_a))
            for off in [-1, 0, 1]:
                px = int(round(sx - off * sin_a))
                py = int(round(sy + off * cos_a))
                if 0 <= px < W and 0 <= py < H:
                    shade = 1.0 - abs(off) / 1.5
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    # 4. Central Valve Hub (radius 4.5) with Coral Pink Center Washer (#FF5E8A)
    for dy in range(-5, 6):
        for dx in range(-5, 6):
            d = (dx**2 + dy**2)**0.5
            if d <= 4.5:
                px = int(round(hx + dx))
                py = int(round(hy + dy))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - d / 4.5)
                    r = int(np.clip(GOLD_DARK[0] * (0.85 + 0.3 * spec), 0, 255))
                    g = int(np.clip(GOLD_DARK[1] * (0.85 + 0.3 * spec), 0, 255))
                    b = int(np.clip(GOLD_DARK[2] * (0.85 + 0.25 * spec), 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    kd.ellipse([int(hx - 2), int(hy - 2), int(hx + 2), int(hy + 2)], fill=CORAL_BASE, outline=GOLD_BASE)
    kd.point((int(hx), int(hy)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_hippo_dual_steam_exhaust_ballast_tail.png
    # Features:
    # - 雙聯蒸氣排氣壓載水箱短尾 (Dual Steam Exhaust Ballast Tail)
    # - Heavy ballast tank mounted low at hip rear (x: 36..52, y: 78..102)
    # - Cylindrical brass ballast pressure chamber with reinforced copper bands
    # - Miniature condensation drain petcock valve at (40, 100)
    # - Exhaust venting nozzle with subtle glowing steam bubble at (36, 82)
    # - Coral pink safety ring (#FF5E8A) on tank pressure flange
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Main Cylindrical Ballast Tank (x: 38..52, y: 80..98)
    for ty in range(80, 99):
        for tx in range(38, 53):
            # Cylinder horizontal shading
            spec = max(0.0, 1.0 - abs(tx - 44.0) / 7.0)
            shine = max(0.0, 1.0 - abs(tx - 42.0) / 3.0)**2
            is_copper_band = (abs(ty - 84) <= 1) or (abs(ty - 94) <= 1)
            if is_copper_band:
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            curio_img.putpixel((tx, ty), (r, g, b, 255))

    # Top & bottom rounded caps
    cd.ellipse([38, 77, 52, 83], fill=ORANGE_LIGHT, outline=OUTLINE)
    cd.ellipse([38, 95, 52, 100], fill=ORANGE_DARK, outline=OUTLINE)

    # 2. Coral Pink Safety Indicator Ring at y: 88..90
    for y in range(88, 91):
        for x in range(38, 53):
            curio_img.putpixel((x, y), CORAL_BASE if abs(x - 44) < 5 else CORAL_DARK)

    # 3. Bottom Condensation Drain Petcock (Valve Cone) at (45, 99..104)
    cd.polygon([(43, 99), (47, 99), (45, 104)], fill=GOLD_BASE, outline=OUTLINE)
    cd.ellipse([43, 103, 47, 106], fill=TIN_DARK, outline=OUTLINE)
    cd.point((45, 104), fill=GOLD_LIGHT)

    # 4. Angled Steam Vent Exhaust Nozzle at top-left (35..38, 79..83)
    cd.polygon([(38, 80), (34, 82), (35, 86), (39, 83)], fill=TIN_SHINE, outline=OUTLINE)
    cd.ellipse([33, 81, 36, 85], fill=TIN_DEEP, outline=OUTLINE)

    # Subtle steam highlight at vent tip
    cd.ellipse([31, 79, 34, 82], fill=(232, 246, 255, 180))
    cd.point((32, 80), fill=WHITE_SHINE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_hippo_thick_cast_brass_default.png
    # Features:
    # - 沖壓厚鑄黃銅鎢鋼矮萌底盤 (Thick Cast Brass & Tungsten Hippo Chassis)
    # - 2.2 chibi ratio, extremely solid, low center of gravity stout stance
    # - Soft ground contact shadow under hooves (x: 22..106, y: 112..122)
    # - Four chunky hydraulic suspension legs with stepped heavy brass hooves at (40, 114) and (72, 114)
    # - Tungsten steel articulated knees at (42, 96) and (70, 96)
    # - Torso: Stamped thick-cast brass plates (#FFA010 / #FFFDF8) with exposed heavy rivets (#1F1A3A / #FFD028)
    # - Left arm at (34..46, 68..80), right arm at (76..88, 68..80) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow under hooves (x: 22..106, y: 112..122)
    ch_d.ellipse([64 - 42, 116 - 6, 64 + 42, 116 + 6], fill=(31, 26, 58, 140))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Chunky Heavy Brass Hooves at (40, 114) and (72, 114)
    feet_pos = [(40.0, 114.0), (72.0, 114.0)]
    for fx, fy in feet_pos:
        ch_d.ellipse([int(fx - 10), int(fy - 5), int(fx + 10), int(fy + 5)], fill=TIN_DEEP, outline=OUTLINE)
        ch_d.ellipse([int(fx - 8), int(fy - 4), int(fx + 8), int(fy + 4)], fill=TIN_BASE)
        # Stamped brass protective hoof guard
        ch_d.polygon([
            (int(fx - 6), int(fy)),
            (int(fx), int(fy + 4)),
            (int(fx + 6), int(fy)),
            (int(fx), int(fy - 3))
        ], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((int(fx - 2), int(fy)), fill=GOLD_LIGHT)
        ch_d.point((int(fx + 2), int(fy)), fill=WHITE_SHINE)

    # 3. Chunky Piston Suspension Legs (x: 32..48, y: 88..113) & (x: 64..80, y: 88..113)
    leg_coords = [
        ((40.0, 113.0), (46.0, 88.0)),
        ((72.0, 113.0), (66.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_coords:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-8, 9):
                spec = max(0.0, 1.0 - abs(dx) / 8.0)
                shine = max(0.0, 1.0 - abs(dx - 1.0) / 4.0)**2
                r = int(np.clip(TIN_SHINE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(TIN_SHINE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(TIN_SHINE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Heavy tungsten knee ball joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 6, mid_y - 5, mid_x + 6, mid_y + 5], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Upper Chest Flange & Thick Neck Hinge (x: 44..84, y: 44..59)
    for ny in range(44, 60):
        for nx in range(44, 85):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 20.0)
            shine = max(0.0, 1.0 - abs(nx - 60.0) / 8.0)**2
            r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
            g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Stout Torso (x: 38..88, y: 58..95)
    # Chunky rounded brass tummy with rich gradient for 0-ART18
    for ty in range(58, 95):
        for tx in range(38, 89):
            dx = (tx - 64.0) / 24.0
            dy = (ty - 77.0) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - (dist_sq)**0.5)
                # Volumetric spherical highlight shifted toward top-left (58, 70)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 70.0)**2)**0.5 / 12.0)**2
                # Lower belly ivory plate patch
                is_belly_plate = (abs(tx - 64.0) < 14.0) and (ty > 72)
                if is_belly_plate:
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
                else:
                    r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                    g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Rivets along flank plate seams
    rivet_spots = [(44, 68), (42, 78), (44, 88), (84, 68), (86, 78), (84, 88)]
    for rx, ry in rivet_spots:
        ch_d.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((rx, ry), fill=WHITE_SHINE)

    # 6. Arms: Left arm at (34..46, 68..80), Right arm at (76..88, 68..80) (strictly x < 94)
    # Left Arm (Shield side / braced)
    for ay in range(68, 81):
        for ax in range(34, 46):
            if (ax - 40)**2 + (ay - 74)**2 <= 30:
                spec = max(0.0, 1.0 - ((ax - 40)**2 + (ay - 74)**2)**0.5 / 5.5)
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec), 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec), 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((ax, ay), (r, g, b, 255))
    ch_d.ellipse([34, 76, 44, 84], fill=TIN_BASE, outline=OUTLINE)
    ch_d.point((39, 80), fill=GOLD_LIGHT)

    # Right Arm (Weapon grip side, strictly x < 94!)
    for ay in range(68, 82):
        for ax in range(78, 91):  # Strictly stops at 90, well clear of 94!
            if (ax - 84)**2 + (ay - 75)**2 <= 30:
                spec = max(0.0, 1.0 - ((ax - 84)**2 + (ay - 75)**2)**0.5 / 5.5)
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec), 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec), 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((ax, ay), (r, g, b, 255))
    ch_d.ellipse([80, 78, 89, 86], fill=TIN_BASE, outline=OUTLINE)
    ch_d.point((84, 82), fill=GOLD_LIGHT)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART9/11: zero pixels at x >= 94
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_hippo_ballast_safety_valve_cowl.png
    # Features:
    # - 沖壓金屬面甲活動大頜兜帽 (Ballast Safety-Valve Cowl & Articulated Jaw)
    # - Sturdy wide hippo tinplate head casing (x: 36..92, y: 22..58)
    # - Upper cranial dome in ivory enamel #FFFDF8 / #FFA010
    # - Dual rotating miniature safety relief valve ears at (36, 26) and (92, 26)
    #   with coral pink warning ring (#FF5E8A)
    # - Articulated wide metal snout & lower jaw at (x: 44..84, y: 44..58)
    # - Brass radiator cooling intake grille lines on snout
    # - STRICT 0-ART27: Hollow eye sockets at (54, 42) & (74, 42) (inner max alpha = 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Main Cranial Shell Dome (x: 40..88, y: 22..46)
    hcx, hcy = 64.0, 36.0
    for y in range(22, 47):
        for x in range(40, 89):
            dx = (x - hcx) / 23.0
            dy = (y - hcy) / 13.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 4))**2)**0.5 / 8.0)**2
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 2. Forehead Stamped Brass Plate (x: 48..80, y: 24..34)
    for y in range(24, 35):
        for x in range(48, 81):
            if abs(x - 64.0) < 14.0 - (y - 24) * 0.4:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 14.0)
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 20, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 20, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec) + 15, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 3. Dual Rotating Safety Relief Valve Ears at (36, 26) and (92, 26)
    ear_centers = [(36.0, 26.0), (92.0, 26.0)]
    for ex, ey in ear_centers:
        hd.ellipse([int(ex - 6), int(ey - 6), int(ex + 6), int(ey + 6)], fill=GOLD_DARK, outline=OUTLINE)
        hd.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_BASE)
        # Coral pink safety warning ring (#FF5E8A)
        hd.ellipse([int(ex - 3), int(ey - 3), int(ex + 3), int(ey + 3)], fill=CORAL_BASE, outline=GOLD_BASE)
        # Center valve spindle pin
        hd.point((int(ex), int(ey)), fill=WHITE_SHINE)
        # Cross notches
        hd.point((int(ex - 4), int(ey)), fill=GOLD_LIGHT)
        hd.point((int(ex + 4), int(ey)), fill=GOLD_LIGHT)
        hd.point((int(ex), int(ey - 4)), fill=GOLD_LIGHT)
        hd.point((int(ex), int(ey + 4)), fill=GOLD_LIGHT)

    # 4. Wide Stamped Metal Hippo Snout & Lower Jaw at (x: 44..84, y: 44..58)
    for y in range(44, 59):
        for x in range(44, 85):
            dx = (x - 64.0) / 19.0
            dy = (y - 51.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 48.0)**2)**0.5 / 6.0)**2
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Radiator cooling intake grille lines on snout (horizontal brass slots)
    for gy in [48, 51, 54]:
        hd.line([(52, gy), (76, gy)], fill=GOLD_DARK, width=1)
        hd.line([(54, gy), (74, gy)], fill=GOLD_BASE, width=1)

    # Nostril steam port rivets
    hd.ellipse([54, 46, 58, 49], fill=TIN_DEEP, outline=OUTLINE)
    hd.ellipse([70, 46, 74, 49], fill=TIN_DEEP, outline=OUTLINE)
    hd.point((56, 47), fill=GOLD_LIGHT)
    hd.point((72, 47), fill=GOLD_LIGHT)

    # 5. Hollow Eye Sockets for 0-ART27 at (54, 42) & (74, 42)
    h_px = head_img.load()
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    ignore_eyes = [(50, 38, 58, 46), (70, 38, 78, 46)]
    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=100, ignore_regions=ignore_eyes)

    # Re-enforce strictly hollow eye sockets after outline pass (0-ART27)
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_hippo_greatcog_high_pressure_cuirass.png
    # Features:
    # - 巨輪城重裝抗震高壓鉚釘胸甲 (Greatcog High-Pressure Cuirass)
    # - Heavy riveted brass armor plates covering chest (x: 44..84, y: 60..92)
    # - Stamped overlapping armor plates with ivory enamel inlay (#FFFDF8)
    # - Cold-rolled steel buckles across center sternum
    # - Diagonal copper steam tube from left shoulder down to right waist
    # - Coral pink manual emergency pull valve ring (#FF5E8A) at chest (56, 72)
    # - Curved heavy pauldron shoulder guards at (36..46, 62..72) and (82..92, 62..72)
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(60, 88):
        for x in range(44, 85):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 20.0)
            shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            is_center_inlay = abs(x - 64.0) < 9.0
            if is_center_inlay:
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Heavy Pauldrons (Shoulder Guards) at (36..46, 62..72) and (82..92, 62..72)
    for px, py in [(41.0, 66.0), (87.0, 66.0)]:
        cos_d.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=GOLD_LIGHT)
        cos_d.point((int(px), int(py)), fill=WHITE_SHINE)

    # Diagonal Copper Steam Tube from (46, 66) to (76, 84)
    p_tube0 = np.array([46.0, 66.0])
    p_tube1 = np.array([76.0, 84.0])
    for t in np.linspace(0.0, 1.0, 24):
        pt = p_tube0 + t * (p_tube1 - p_tube0)
        for off in [-1, 0, 1]:
            px = int(round(pt[0] - off * 0.5))
            py = int(round(pt[1] + off * 0.8))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(off) / 1.5
                costume_img.putpixel((px, py), (
                    int(GOLD_BASE[0] * (0.85 + 0.25 * shade)),
                    int(GOLD_BASE[1] * (0.85 + 0.25 * shade)),
                    int(GOLD_BASE[2] * (0.85 + 0.25 * shade)),
                    255
                ))

    # Coral Pink Emergency Pull Valve Ring (#FF5E8A) at chest (56, 73)
    cos_d.ellipse([53, 70, 59, 76], fill=CORAL_BASE, outline=OUTLINE)
    cos_d.ellipse([54, 71, 58, 75], fill=CORAL_LIGHT)
    cos_d.point((56, 73), fill=WHITE_SHINE)

    # Stamped High-Pressure Belt Buckle at y: 86..92
    cos_d.rectangle([54, 86, 74, 92], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.rectangle([56, 88, 72, 90], fill=TIN_DEEP)
    cos_d.point((64, 89), fill=WHITE_SHINE)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART26b enforcement: Zero pixels at y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_hippo_dual_pressure_gauge_quartz_lens.png
    # Features:
    # - 雙聯同軸高壓石英壓力表目鏡 (Dual Pressure Gauge Quartz Lens)
    # - Left eye at (54, 42), Right eye at (74, 42)
    # - Polished brass bezels with vernier gear teeth
    # - Mint green luminous manometer gauge dial face (#4ED86A, #85FFA0)
    # - Concentric gauge scale rings and black indicator needle pointing upward
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    eyes_config = [
        (54.0, 42.0),   # Left Eye: Pressure Gauge
        (74.0, 42.0)    # Right Eye: Pressure Gauge
    ]

    for ex, ey in eyes_config:
        # Brass outer bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Mint green pressure gauge luminous dial
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r = int(np.clip(MINT_BASE[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    b = int(np.clip(MINT_BASE[2] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Thin black pressure indicator needle pointing up-left (alert status)
        core_img.putpixel((int(ex), int(ey)), (31, 26, 58, 255))
        core_img.putpixel((int(ex - 1), int(ey - 1)), (31, 26, 58, 255))
        core_img.putpixel((int(ex - 2), int(ey - 2)), (31, 26, 58, 255))

        # Quartz highlight gleam
        core_img.putpixel((int(ex + 1), int(ey - 1)), WHITE_SHINE)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    # Ensure centers meet min_alpha >= 200 for 0-ART27
    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_hippo_steamvalve_piston_heavy_lance.png
    # Features:
    # - 重閥活塞衝刺長槍 (Steamvalve Piston Heavy Lance)
    # - Massive steampunk heavy lance held firmly in right hand
    # - Main shaft extends from grip (84, 88) up to lance tip (102, 38)
    # - Heavy conical armor-piercing steel spearhead at (102, 38) with fluted grooves
    # - Mid-shaft high-pressure steam piston cylinder with transparent quartz tube
    #   and luminous mint-green conduit fluid (#4ED86A)
    # - Wide tungsten handguard buckler disc at (85, 84)
    # - Spherical brass counterweight pommel at (83, 92)
    # - Complies strictly with review.md 0-MKT7 single-weapon standard
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    lance_p0 = np.array([84.0, 90.0])
    lance_p1 = np.array([102.0, 40.0])

    # 1. Main Lance Shaft (p0 to p1)
    for t in np.linspace(0.0, 1.0, 48):
        pt = lance_p0 + t * (lance_p1 - lance_p0)
        # Mid-shaft piston chamber zone (t: 0.45..0.75) is thicker
        is_piston_chamber = (0.42 <= t <= 0.76)
        half_w = 3.2 if is_piston_chamber else 1.8

        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            normal = np.array([-(lance_p1[1] - lance_p0[1]), (lance_p1[0] - lance_p0[0])])
            normal = normal / (np.linalg.norm(normal) + 1e-6)
            px = int(round(pt[0] + offset * normal[0]))
            py = int(round(pt[1] + offset * normal[1]))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(offset) / (half_w + 0.5)
                if is_piston_chamber:
                    # Luminous mint core inside quartz cylinder
                    is_core = abs(offset) < 1.4
                    if is_core:
                        r = int(np.clip(MINT_BASE[0] * (0.85 + 0.3 * shade) + 40, 0, 255))
                        g = int(np.clip(MINT_BASE[1] * (0.85 + 0.3 * shade) + 35, 0, 255))
                        b = int(np.clip(MINT_BASE[2] * (0.85 + 0.3 * shade) + 25, 0, 255))
                    else:
                        r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                else:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # 2. Conical Armor-Piercing Spearhead at (102, 40) extending to (106, 28)
    tip_pts = [(98, 42), (105, 40), (107, 28), (101, 32)]
    wd.polygon(tip_pts, fill=GOLD_LIGHT, outline=OUTLINE)
    wd.line([(101, 32), (107, 28)], fill=WHITE_SHINE, width=1)
    wd.point((107, 28), fill=WHITE_SHINE)

    # 3. Fluted Reinforced Lance Rings along shaft
    for ring_t in [0.42, 0.76]:
        rpt = lance_p0 + ring_t * (lance_p1 - lance_p0)
        wd.ellipse([int(rpt[0] - 4), int(rpt[1] - 4), int(rpt[0] + 4), int(rpt[1] + 4)], fill=GOLD_DARK, outline=OUTLINE)
        wd.point((int(rpt[0]), int(rpt[1])), fill=GOLD_LIGHT)

    # 4. Wide Tungsten Handguard Buckler at (85, 84)
    wd.ellipse([80, 80, 90, 88], fill=TIN_BASE, outline=OUTLINE)
    wd.ellipse([82, 82, 88, 86], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((85, 84), fill=WHITE_SHINE)

    # 5. Counterweight Pommel at (83, 92)
    wd.ellipse([80, 90, 86, 96], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((83, 93), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_hippo_dual_valve_handwheel_brass", key_img),
        ("back_curio", "curio_hippo_dual_steam_exhaust_ballast_tail", curio_img),
        ("chassis", "chassis_hippo_thick_cast_brass_default", chassis_img),
        ("head_unit", "head_hippo_ballast_safety_valve_cowl", head_img),
        ("costume", "costume_hippo_greatcog_high_pressure_cuirass", costume_img),
        ("optic_core", "face_hippo_dual_pressure_gauge_quartz_lens", core_img),
        ("weapon", "weapon_hippo_steamvalve_piston_heavy_lance", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{HIPPO_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{HIPPO_PD_DIR}/winding_key/key_hippo_dual_valve_handwheel_brass.png",
                 f"{KEY_DIR}/key_hippo_dual_valve_handwheel_brass.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{HIPPO_PD_DIR}/weapon/weapon_hippo_steamvalve_piston_heavy_lance.png",
                 f"{WEAPON_DIR}/weapon_hippo_steamvalve_piston_heavy_lance.png")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE CHARACTER & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # Ordering: winding_key -> back_curio -> chassis -> head_unit -> costume -> optic_core -> weapon
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{HIPPO_PD_DIR}/proof_paperdoll_hippo_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{HIPPO_PD_DIR}/proof_paperdoll_hippo_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 40
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Costume", "Optic", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 14)
    except Exception:
        font = ImageFont.load_default()

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 4), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{HIPPO_PD_DIR}/proof_hippo_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([26, 110, 102, 122], fill=(31, 26, 58, 110))
    shd.ellipse([36, 112, 92, 120], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/hippo_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/hippo_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/hippo_idle.png
    p_idle_64 = f"{PLAYER_DIR}/hippo_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/hippo_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/hippo_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/hippo_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/hippo_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/hippo_idle_hd.png)
    os.makedirs(SHOWCASE_DIR, exist_ok=True)
    comp_bbox = composite.getbbox()
    if comp_bbox:
        char_crop = idle_with_shadow.crop(comp_bbox)
        target_h = 920
        aspect = char_crop.width / char_crop.height
        sc_w = int(target_h * aspect)
        sc_h = target_h
        scaled_showcase = char_crop.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

        showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_paste_x = (800 - sc_w) // 2
        sc_paste_y = 1120 - sc_h

        sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_sdraw = ImageDraw.Draw(sc_shadow)
        sc_sdraw.ellipse((400 - 240, 1120 - 24, 400 + 240, 1120 + 24), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{SHOWCASE_DIR}/hippo_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THE STEAMVALVE HIPPO CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
