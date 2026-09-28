#!/usr/bin/env python3
"""
build_seal_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十族 拍浪海豹 (The Clapping Seal, seal) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/CLAPPING_SEAL_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, marine titanium tinplate plates,
  streamline cowl & acoustic sonar ears, dual-blade marine propeller winding key,
  deepsea diver harness with gold anchor buckle & coral buoy, cyan quartz convex lens,
  crystal pneumatic clapper gauntlets, hydro-ducted tail flukes)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Marine Titanium Sky Blue (#38A0FF) & Sunny Cream Ivory White (#FFFDF8)
    2. Secondary Hull / Trim: Scrap Warm Orange (#FFA010)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Quartz: Cyan Quartz Convex Lens (#38A0FF)
    6. Cute Coral Pink: Coral Pink (#FF5E8A)
    7. Cold Stamped Tungsten Steel: Tungsten Gray (#3A3644)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEAL_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/seal"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Clapping Seal Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Marine Titanium Sky Blue (#38A0FF)
SKY_BASE   = (56, 160, 255, 255)
SKY_LIGHT  = (120, 205, 255, 255)
SKY_SHINE  = (195, 235, 255, 255)
SKY_DARK   = (24, 105, 195, 255)
SKY_DEEP   = (14, 60, 130, 255)

# 2. Decompression Belly & Shell: Sunny Cream Ivory White (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (235, 226, 210, 255)
IVORY_DARK   = (210, 198, 178, 255)
IVORY_DEEP   = (180, 168, 148, 255)

# 3. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Diver Harness Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (195, 110, 8, 255)
ORANGE_DEEP  = (135, 70, 5, 255)

# 5. Fresh Mint Green Gauge & Valve (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 6. Coral Pink Buoy & Seal Dampers (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 7. Cold Stamped Tungsten Steel (#3A3644)
TUNGSTEN_BASE  = (58, 54, 68, 255)
TUNGSTEN_LIGHT = (96, 92, 110, 255)
TUNGSTEN_SHINE = (135, 130, 150, 255)
TUNGSTEN_DARK  = (38, 35, 46, 255)
TUNGSTEN_DEEP  = (24, 22, 30, 255)

# 8. Crystal Glass Blue (#60C0FF)
CRYSTAL_BASE  = (96, 192, 255, 255)
CRYSTAL_LIGHT = (160, 225, 255, 255)
CRYSTAL_SHINE = (220, 245, 255, 255)
CRYSTAL_DARK  = (40, 140, 210, 255)
CRYSTAL_DEEP  = (20, 80, 150, 255)

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
                has_solid_neighbor = False
                for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if 0 <= nx < w and 0 <= ny < h:
                        if px_snap[nx, ny][3] >= min_alpha:
                            has_solid_neighbor = True
                            break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL CLAPPING SEAL SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_seal_marine_propeller_brass.png
    # Dual-Blade Marine Propeller Winding Key (雙葉水力螺旋槳黃銅發條鑰匙)
    # Features:
    # - Socket boss at upper back (64, 58)
    # - Polished brass key shaft extending up-right from (64, 58) to (90, 24)
    # - Marine hydrodynamic dual curved propeller blades (sweeping from hub)
    # - Hydrodynamic flow cutout holes in blades
    # - Central brass hub disk at (90, 24) with central sapphire/coral jewel
    # - Warm golden bronze outline (OUTLINE_KEY) to comply with 0-ART29 / 0-QA16
    # - STRICTLY transparent corners
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from socket (64, 58) to hub (90, 24)
    for t in np.linspace(0.0, 1.0, 60):
        sx = 64.0 + t * 26.0
        sy = 58.0 - t * 34.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.82 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.82 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.82 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(round(sx + dx)), int(round(sy + dy))), (r_s, g_s, b_s, 255))

    # Base socket collar at (64, 58)
    kd.ellipse([64 - 5, 58 - 5, 64 + 5, 58 + 5], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 58 - 3, 64 + 3, 58 + 3], fill=GOLD_BASE)
    kd.ellipse([64 - 1, 58 - 1, 64 + 1, 58 + 1], fill=SKY_BASE)

    # 2. Dual Propeller Blades: Hub at (90, 24)
    kcx, kcy = 90.0, 24.0

    # Blade 1: Sweeps up-left from hub (angle around 140 deg)
    # Blade 2: Sweeps down-right from hub (angle around 320 deg)
    for dy in range(-20, 21):
        for dx in range(-20, 21):
            dist = (dx**2 + dy**2)**0.5
            angle = np.arctan2(dy, dx)
            # Two opposite marine propeller hydrofoil blades
            # Angle relative to primary axis (approx 2.4 radians)
            rel_ang = (angle - 2.4) % np.pi
            if rel_ang > np.pi / 2:
                rel_ang = np.pi - rel_ang

            # Hydrodynamic curved chord profile
            chord_width = np.sin(dist / 18.0 * np.pi) * 0.55 if 4.0 <= dist <= 18.5 else 0.0
            if 4.5 <= dist <= 18.0 and abs(rel_ang) < chord_width:
                spec = max(0.0, 1.0 - abs(rel_ang) / max(0.01, chord_width))
                shine = max(0.0, 1.0 - dist / 18.0)
                r_g = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                g_g = int(np.clip(208 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((int(kcx + dx), int(kcy + dy)), (r_g, g_g, b_g, 255))

    # Center Hub disc at (90, 24), r <= 6.5
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            d = (dx**2 + dy**2)**0.5
            if d <= 6.5:
                spec = max(0.0, 1.0 - d / 6.5)
                r_g = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                g_g = int(np.clip(208 * (0.85 + 0.2 * spec), 0, 255))
                b_g = int(np.clip(40 * (0.85 + 0.4 * spec), 0, 255))
                key_img.putpixel((int(kcx + dx), int(kcy + dy)), (r_g, g_g, b_g, 255))

    # Circular Cutout Holes in the 2 Propeller Blades
    # Blade 1 cutout at dist=11, angle=2.4
    # Blade 2 cutout at dist=11, angle=2.4 + pi
    for rot in [2.4, 2.4 + np.pi]:
        hx = kcx + 11.5 * np.cos(rot)
        hy = kcy + 11.5 * np.sin(rot)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx**2 + dy**2 <= 5:  # radius ~2.2 hole
                    key_img.putpixel((int(round(hx + dx)), int(round(hy + dy))), (0, 0, 0, 0))

    # Center jewel bearing at (90, 24)
    for dx in range(-3, 4):
        for dy in range(-3, 4):
            d = (dx**2 + dy**2)**0.5
            if d <= 3.0:
                spec = max(0.0, 1.0 - d / 3.0)
                r_s = int(np.clip(56 * (0.8 + 0.3 * spec), 0, 255))
                g_s = int(np.clip(160 * (0.8 + 0.3 * spec), 0, 255))
                b_s = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                key_img.putpixel((int(kcx + dx), int(kcy + dy)), (r_s, g_s, b_s, 255))
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline (OUTLINE_KEY)
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict 0-ART29 transparent corners
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_seal_hydro_ducted_tail_flukes.png
    # Hydro-Ducted Tail Flukes (氣動導流雙葉金屬尾鰭)
    # Features:
    # - Originates from pelvic base (x: 48..80, y: 84..108)
    # - Central hydraulic damping cylinder (x: 61..67, y: 84..96) in tungsten & brass
    # - Dual hydro-ducted curved tail flukes sweeping outward & slightly down:
    #   Left fluke: (62, 92) -> (38, 104) -> (46, 96)
    #   Right fluke: (66, 92) -> (90, 104) -> (82, 96)
    # - Segmented titanium & tungsten plates with brass leading edges
    # - Miniature coral pink relief indicator at cylinder center
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Central Damping Shock Absorber Cylinder (x: 61..67, y: 84..98)
    for y in range(84, 99):
        for x in range(60, 68):
            dx = abs(x - 63.5) / 3.5
            spec = max(0.0, 1.0 - dx)
            r_t = int(np.clip(58 * (0.8 + 0.4 * spec), 0, 255))
            g_t = int(np.clip(54 * (0.8 + 0.4 * spec), 0, 255))
            b_t = int(np.clip(68 * (0.8 + 0.4 * spec), 0, 255))
            curio_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Brass Collar Rings on Damping Cylinder
    cd.rectangle([59, 87, 68, 89], fill=GOLD_BASE, outline=OUTLINE)
    cd.rectangle([59, 93, 68, 95], fill=GOLD_BASE, outline=OUTLINE)
    # Coral Pink Pressure Indicator at (64, 91)
    cd.ellipse([62, 90, 65, 92], fill=CORAL_BASE, outline=OUTLINE)

    # 2. Left Hydrofoil Metal Fluke
    # Polygon defining the left flipper blade
    left_fluke_poly = [
        (62, 92),
        (54, 95),
        (42, 101),
        (35, 106),
        (38, 108),
        (50, 105),
        (60, 99),
        (63, 96)
    ]
    cd.polygon(left_fluke_poly, fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    # Left fluke stepped plating in Sky Blue & Titanium
    for y in range(92, 109):
        for x in range(35, 64):
            if curio_img.getpixel((x, y))[3] > 100:
                dist_edge = max(0.0, 1.0 - ((x - 35.0)**2 + (y - 106.0)**2)**0.5 / 25.0)
                r_f = int(np.clip(56 * (0.6 + 0.4 * dist_edge) + 20, 0, 255))
                g_f = int(np.clip(160 * (0.6 + 0.4 * dist_edge) + 20, 0, 255))
                b_f = int(np.clip(255 * (0.7 + 0.3 * dist_edge), 0, 255))
                curio_img.putpixel((x, y), (r_f, g_f, b_f, 255))
    # Leading edge highlight (gold/brass trim)
    cd.line([(62, 92), (54, 95), (42, 101), (35, 106)], fill=GOLD_BASE, width=1)
    cd.point((35, 106), fill=WHITE_SHINE)

    # 3. Right Hydrofoil Metal Fluke
    right_fluke_poly = [
        (65, 92),
        (74, 95),
        (86, 101),
        (93, 106),
        (90, 108),
        (78, 105),
        (68, 99),
        (65, 96)
    ]
    cd.polygon(right_fluke_poly, fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    # Right fluke stepped plating
    for y in range(92, 109):
        for x in range(65, 94):
            if curio_img.getpixel((x, y))[3] > 100:
                dist_edge = max(0.0, 1.0 - ((x - 93.0)**2 + (y - 106.0)**2)**0.5 / 25.0)
                r_f = int(np.clip(56 * (0.6 + 0.4 * dist_edge) + 20, 0, 255))
                g_f = int(np.clip(160 * (0.6 + 0.4 * dist_edge) + 20, 0, 255))
                b_f = int(np.clip(255 * (0.7 + 0.3 * dist_edge), 0, 255))
                curio_img.putpixel((x, y), (r_f, g_f, b_f, 255))
    # Leading edge highlight (gold/brass trim)
    cd.line([(65, 92), (74, 95), (86, 101), (93, 106)], fill=GOLD_BASE, width=1)
    cd.point((93, 106), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Core Body Layer)
    # File: chassis/chassis_seal_marine_titanium_default.png
    # Marine Titanium & Ivory Enamel Chassis (拍浪海豹鍍鈦流線防蝕素體)
    # Features:
    # - 2.2 head-body ratio chibi seal toy body
    # - Plump hydrodynamic streamline teardrop body
    # - Dual-tone marine coating:
    #   Sky Blue (#38A0FF) on back, shoulders, flanks
    #   Sunny Cream Ivory (#FFFDF8) on chest and belly
    # - Rich multi-tone depth (>= 20 unique colors in torso) to pass 0-ART18
    # - Streamline flippers:
    #   Left flipper resting forward/downward at (34..46, 70..88)
    #   Right flipper tucked at chest (78..92, 68..84), strictly x <= 92
    #   STRICTLY 0 PIXELS AT x >= 94 to pass 0-ART9/11!
    # - Broad grounded tail/pelvic base resting at y: 98..112, x: 44..84
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Base / Pelvic Ground Support (y: 96..112, x: 42..86)
    for y in range(96, 113):
        for x in range(42, 87):
            dx = (x - 64.0) / 21.0
            dy = (y - 104.0) / 8.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 21.0)
                sh = (y - 96.0) / 16.0
                r_c = int(np.clip(56 * (0.85 - 0.2 * sh + 0.25 * spec), 0, 255))
                g_c = int(np.clip(160 * (0.85 - 0.2 * sh + 0.25 * spec), 0, 255))
                b_c = int(np.clip(255 * (0.9 - 0.15 * sh + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 2. Main Torso & Belly Volume (y: 50..98, x: 40..88)
    # Neck / Shoulder solid bridge (y: 48..60, x: 46..82) to guarantee seamless junction
    for y in range(48, 62):
        for x in range(46, 83):
            dx = abs(x - 64.0) / 18.0
            if dx <= 1.0:
                spec = max(0.0, 1.0 - dx)
                sh_y = (y - 48.0) / 14.0
                r_s = int(np.clip(56 * (0.9 - 0.15 * sh_y + 0.2 * spec), 0, 255))
                g_s = int(np.clip(160 * (0.9 - 0.15 * sh_y + 0.2 * spec), 0, 255))
                b_s = int(np.clip(255 * (0.92 - 0.12 * sh_y + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    for y in range(50, 99):
        for x in range(40, 89):
            dx = (x - 64.0) / 22.0
            dy = (y - 75.0) / 23.0
            if dx**2 + dy**2 <= 1.04:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                # Left-right position determines Ivory Belly vs Sky Blue Flanks
                belly_factor = max(0.0, 1.0 - ((x - 62.0)**2 / 16.0**2 + (y - 78.0)**2 / 18.0**2)**0.5)
                sh_y = (y - 52.0) / 46.0

                if belly_factor > 0.35:
                    # Ivory Enamel Belly (Cream White with rich multi-tone depth)
                    b_ratio = (belly_factor - 0.35) / 0.65
                    r_b = int(np.clip(255 * (0.95 - 0.12 * sh_y + 0.08 * b_ratio), 0, 255))
                    g_b = int(np.clip(253 * (0.95 - 0.15 * sh_y + 0.08 * b_ratio), 0, 255))
                    b_b = int(np.clip(248 * (0.93 - 0.20 * sh_y + 0.07 * b_ratio), 0, 255))
                    chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))
                else:
                    # Marine Titanium Sky Blue Shell
                    r_s = int(np.clip(56 * (0.88 - 0.2 * sh_y + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(160 * (0.88 - 0.2 * sh_y + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(255 * (0.92 - 0.15 * sh_y + 0.15 * spec), 0, 255))
                    chassis_img.putpixel((x, y), (r_s, g_s, b_s, 255))

    # 3. Head Sphere Base (under head unit) (y: 22..56, x: 42..86)
    for y in range(22, 57):
        for x in range(42, 87):
            dx = (x - 64.0) / 20.0
            dy = (y - 39.0) / 16.0
            if dx**2 + dy**2 <= 1.02:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                sh_y = (y - 22.0) / 34.0
                r_h = int(np.clip(56 * (0.95 - 0.15 * sh_y + 0.2 * spec), 0, 255))
                g_h = int(np.clip(160 * (0.95 - 0.15 * sh_y + 0.2 * spec), 0, 255))
                b_h = int(np.clip(255 * (0.95 - 0.12 * sh_y + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 4. Streamline Flippers
    # Left Flipper (viewer's left: x: 32..46, y: 68..88)
    left_flipper_poly = [
        (44, 68),
        (38, 73),
        (32, 80),
        (33, 86),
        (40, 84),
        (46, 78)
    ]
    chd.polygon(left_flipper_poly, fill=SKY_LIGHT, outline=OUTLINE)
    for y in range(68, 87):
        for x in range(32, 47):
            if chassis_img.getpixel((x, y))[3] > 100:
                dist_f = max(0.0, 1.0 - ((x - 33.0)**2 + (y - 84.0)**2)**0.5 / 16.0)
                r_f = int(np.clip(56 * (0.75 + 0.35 * dist_f), 0, 255))
                g_f = int(np.clip(160 * (0.75 + 0.35 * dist_f), 0, 255))
                b_f = int(np.clip(255 * (0.8 + 0.25 * dist_f), 0, 255))
                chassis_img.putpixel((x, y), (r_f, g_f, b_f, 255))
    # Brass hinge ball at left shoulder (44, 68)
    chd.ellipse([42, 66, 46, 70], fill=GOLD_BASE, outline=OUTLINE)

    # Right Flipper (viewer's right: x: 78..92, y: 66..84)
    # STRICT 0-ART9/11 RULE: rightmost pixel <= 92!
    right_flipper_poly = [
        (82, 66),
        (88, 70),
        (92, 75),
        (92, 80),
        (86, 83),
        (80, 78)
    ]
    chd.polygon(right_flipper_poly, fill=SKY_LIGHT, outline=OUTLINE)
    for y in range(66, 84):
        for x in range(78, 93):  # strictly <= 92
            if chassis_img.getpixel((x, y))[3] > 100:
                dist_f = max(0.0, 1.0 - ((x - 90.0)**2 + (y - 78.0)**2)**0.5 / 14.0)
                r_f = int(np.clip(56 * (0.8 + 0.3 * dist_f), 0, 255))
                g_f = int(np.clip(160 * (0.8 + 0.3 * dist_f), 0, 255))
                b_f = int(np.clip(255 * (0.85 + 0.2 * dist_f), 0, 255))
                chassis_img.putpixel((x, y), (r_f, g_f, b_f, 255))
    # Brass hinge ball at right shoulder (82, 66)
    chd.ellipse([80, 64, 84, 68], fill=GOLD_BASE, outline=OUTLINE)

    # 5. Panel Seam Lines & Rivets on Chassis
    # Arc seam between belly and flanks
    chd.arc([46, 62, 78, 94], start=45, end=135, fill=SKY_DARK, width=1)
    # Rivet highlights
    for rx, ry in [(48, 70), (46, 80), (80, 70), (82, 80), (64, 98), (54, 102), (74, 102)]:
        chassis_img.putpixel((rx, ry), WHITE_SHINE)

    apply_clean_outline(chassis_img)

    # Enforce strict 0-ART9 / 0-ART11: strictly zero pixels at x >= 94
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Head & Cowl Layer)
    # File: head_unit/head_seal_streamline_cowl_sonar.png
    # Streamline Cowl & Sonar Ears (沖壓流體減阻兜帽與同軸聲納立耳)
    # Features:
    # - Stamped titanium streamline cowl fitting over head (x: 40..88, y: 16..54)
    # - Central top aerodynamic cooling fin / ridge (x: 63..65, y: 14..24) in gold brass
    # - Dual circular brass acoustic sonar ears at left (x: 36..44, y: 26..34) and right (x: 84..92, y: 26..34)
    # - Stamped black metal snout at (64, 46) with 3 pairs of fine brass whiskers
    # - STRICT 0-ART27 RULE: Hollow eye sockets at centers (52, 40) and (76, 40) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Dual Acoustic Sonar Ears
    # Left Sonar Ear (center: 40, 30, radius: 5.5)
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            d = (dx**2 + dy**2)**0.5
            if d <= 5.5:
                spec = max(0.0, 1.0 - d / 5.5)
                r_e = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                g_e = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                b_e = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * spec, 0, 255))
                head_img.putpixel((40 + dx, 30 + dy), (r_e, g_e, b_e, 255))
    hd.ellipse([36, 26, 44, 34], outline=OUTLINE)
    hd.ellipse([38, 28, 42, 32], outline=GOLD_DEEP)
    head_img.putpixel((40, 30), CORAL_BASE)  # Central sensor dot

    # Right Sonar Ear (center: 88, 30, radius: 5.5)
    for dy in range(-6, 7):
        for dx in range(-6, 7):
            d = (dx**2 + dy**2)**0.5
            if d <= 5.5:
                spec = max(0.0, 1.0 - d / 5.5)
                r_e = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                g_e = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                b_e = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * spec, 0, 255))
                head_img.putpixel((88 + dx, 30 + dy), (r_e, g_e, b_e, 255))
    hd.ellipse([84, 26, 92, 34], outline=OUTLINE)
    hd.ellipse([86, 28, 90, 32], outline=GOLD_DEEP)
    head_img.putpixel((88, 30), CORAL_BASE)

    # 2. Cowl Shell (y: 18..54, x: 42..86)
    for y in range(18, 55):
        for x in range(42, 87):
            dx = (x - 64.0) / 20.0
            dy = (y - 37.0) / 17.0
            if dx**2 + dy**2 <= 1.02:
                # Keep center hollow around snout & cheeks
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                sh_y = (y - 18.0) / 36.0
                r_c = int(np.clip(56 * (0.95 - 0.2 * sh_y + 0.2 * spec), 0, 255))
                g_c = int(np.clip(160 * (0.95 - 0.2 * sh_y + 0.2 * spec), 0, 255))
                b_c = int(np.clip(255 * (0.95 - 0.15 * sh_y + 0.15 * spec), 0, 255))
                head_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Top Central Cooling Fin / Ridge (x: 63..65, y: 14..24)
    hd.polygon([(63, 14), (65, 14), (66, 25), (62, 25)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(64, 15), (64, 24)], fill=WHITE_SHINE, width=1)

    # Front Cowl Brow Rim (y: 26..30, x: 44..84)
    hd.arc([44, 24, 84, 34], start=10, end=170, fill=GOLD_BASE, width=2)

    # Snout Muzzle (x: 56..72, y: 44..52) in Sunny Ivory White (#FFFDF8)
    for y in range(44, 53):
        for x in range(56, 73):
            dx = (x - 64.0) / 8.0
            dy = (y - 48.0) / 4.0
            if dx**2 + dy**2 <= 1.0:
                head_img.putpixel((x, y), IVORY_BASE)
    hd.ellipse([56, 44, 72, 52], outline=OUTLINE)

    # Cute Stamped Black Metal Nose at (64, 46)
    hd.ellipse([62, 45, 66, 48], fill=TUNGSTEN_DARK, outline=OUTLINE)
    head_img.putpixel((63, 46), WHITE_SHINE)

    # Whiskers (3 pairs of fine brass wire whiskers)
    # Left whiskers
    hd.line([(58, 48), (48, 46)], fill=GOLD_LIGHT, width=1)
    hd.line([(58, 49), (46, 50)], fill=GOLD_LIGHT, width=1)
    hd.line([(58, 50), (48, 54)], fill=GOLD_LIGHT, width=1)
    # Right whiskers
    hd.line([(70, 48), (80, 46)], fill=GOLD_LIGHT, width=1)
    hd.line([(70, 49), (82, 50)], fill=GOLD_LIGHT, width=1)
    hd.line([(70, 50), (80, 54)], fill=GOLD_LIGHT, width=1)

    # Apply outline with eye sockets protected from bleeding
    eye_ignore = [(48, 36, 56, 44), (72, 36, 80, 44)]
    apply_clean_outline(head_img, ignore_regions=eye_ignore)

    # Enforce STRICT 0-ART27 HOLLOW EYE SOCKETS at (52, 40) and (76, 40)
    for ex in [52, 76]:
        for ey in range(37, 44):
            for exx in range(ex - 3, ex + 4):
                head_img.putpixel((exx, ey), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Outerwear Layer)
    # File: costume/costume_seal_deepsea_diver_harness.png
    # Deepsea Diver Harness (深海武道防壓束帶與珊瑚浮標)
    # Features:
    # - High-tensile waterproof coated diver martial harness in Dopamine Warm Orange (#FFA010)
    # - Diagonal cross-body belt from shoulder (52, 58) across chest to waist (74, 84)
    # - Waist belt (y: 82..90, x: 48..80)
    # - Gilded marine anchor buckle at chest center (64, 72)
    # - Mini pressure relief gauge (mint dial, brass rim) at left waist (52..58, 83..89)
    # - Spherical coral pink (#FF5E8A) buoy ball on right hip (74..80, 83..89)
    # - STRICT 0-ART26b RULE: strictly zero pixels at y >= 96!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Diagonal Cross-Chest Belt: from (52, 58) to (76, 84)
    for t in np.linspace(0.0, 1.0, 50):
        bx = 52.0 * (1 - t) + 76.0 * t
        by = 58.0 * (1 - t) + 84.0 * t
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_o = int(np.clip(255 * (0.9 + 0.15 * spec), 0, 255))
                    g_o = int(np.clip(160 * (0.9 + 0.15 * spec), 0, 255))
                    b_o = int(np.clip(16 * (0.9 + 0.15 * spec) + 30 * spec, 0, 255))
                    costume_img.putpixel((int(round(bx + dx)), int(round(by + dy))), (r_o, g_o, b_o, 255))

    # 2. Horizontal Waist Belt (y: 82..90, x: 48..80)
    for y in range(82, 91):  # strictly <= 90, well below 96
        for x in range(48, 81):
            dx = abs(x - 64.0) / 16.0
            sh = (y - 82.0) / 8.0
            spec = max(0.0, 1.0 - dx)
            r_o = int(np.clip(255 * (0.92 - 0.2 * sh + 0.15 * spec), 0, 255))
            g_o = int(np.clip(160 * (0.92 - 0.2 * sh + 0.15 * spec), 0, 255))
            b_o = int(np.clip(16 * (0.92 - 0.2 * sh) + 25 * spec, 0, 255))
            costume_img.putpixel((x, y), (r_o, g_o, b_o, 255))

    # Belt stitch reinforcement lines
    cosd.line([(48, 83), (80, 83)], fill=ORANGE_SHINE, width=1)
    cosd.line([(48, 89), (80, 89)], fill=ORANGE_DARK, width=1)

    # 3. Gilded Brass Anchor Buckle at Solar Plexus (center: 64, 72)
    # Ring top
    cosd.ellipse([62, 68, 66, 72], fill=GOLD_BASE, outline=OUTLINE)
    cosd.point((64, 70), fill=WHITE_SHINE)
    # Anchor shank & crossbar
    cosd.line([(64, 72), (64, 78)], fill=GOLD_BASE, width=2)
    cosd.line([(61, 74), (67, 74)], fill=GOLD_LIGHT, width=1)
    # Curved bottom fluke
    cosd.arc([60, 74, 68, 80], start=30, end=150, fill=GOLD_BASE, width=2)

    # 4. Mini Pressure Relief Gauge on Left Waist (51..57, 83..89)
    cosd.ellipse([51, 83, 57, 89], fill=GOLD_BASE, outline=OUTLINE)
    cosd.ellipse([52, 84, 56, 88], fill=MINT_BASE)
    cosd.point((54, 85), fill=WHITE_SHINE)
    cosd.line([(54, 86), (55, 87)], fill=OUTLINE, width=1)  # Gauge needle

    # 5. Spherical Coral Pink Buoy Ball on Right Hip (73..79, 83..89)
    cosd.ellipse([73, 83, 79, 89], fill=CORAL_BASE, outline=OUTLINE)
    cosd.ellipse([74, 84, 78, 88], fill=CORAL_LIGHT)
    cosd.point((75, 84), fill=WHITE_SHINE)

    apply_clean_outline(costume_img)

    # Strict check: 0-ART26b compliance - verify zero pixels at y >= 96
    cos_arr = np.array(costume_img)
    if np.any(cos_arr[96:, :, 3] > 0):
        print("  ⚠️ Trimming costume pixels at y >= 96 for 0-ART26b compliance...")
        for y in range(96, H):
            for x in range(W):
                costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, Face & Eyes Layer)
    # File: optic_core/face_seal_cyan_quartz_convex_lens.png
    # Cyan Quartz Convex Lens (深海琉璃石英凸透目鏡)
    # Features:
    # - Left eye centered at (52, 40), Right eye centered at (76, 40)
    # - Convex spherical quartz lens in Sky Blue (#38A0FF) & Cyan (#60C0FF)
    # - High opacity at centers (alpha == 255 > 200, 0-ART27 compliant)
    # - Concentric depth gauge circles and reticle in Fresh Mint Green (#4ED86A)
    # - Glossy white specular reflections at top-left
    # - Rich color depth to pass 0-QA31 (>= 15 unique colors in optic zone)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    for ex in [52, 76]:
        ey = 40
        er = 6.0
        # Multi-tone concentric gradient spherical convex lens
        for y in range(int(ey - er - 1), int(ey + er + 2)):
            for x in range(int(ex - er - 1), int(ex + er + 2)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= er:
                    ratio = dist / er
                    if ratio <= 0.35:
                        col = SKY_SHINE
                    elif ratio <= 0.65:
                        col = SKY_LIGHT
                    elif ratio <= 0.88:
                        col = SKY_BASE
                    else:
                        col = SKY_DEEP
                    core_img.putpixel((x, y), col)

        # Concentric Depth Gauge Reticle
        cored.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], outline=SKY_DARK)
        cored.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], outline=MINT_BASE)
        # Reticle markings in Mint Green (#4ED86A)
        cored.line([(ex - 4, ey), (ex - 2, ey)], fill=MINT_LIGHT)
        cored.line([(ex + 2, ey), (ex + 4, ey)], fill=MINT_LIGHT)
        cored.line([(ex, ey - 4), (ex, ey - 2)], fill=MINT_LIGHT)
        cored.line([(ex, ey + 2), (ex, ey + 4)], fill=MINT_LIGHT)
        # Specular glints
        core_img.putpixel((ex - 2, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 1, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 2, ey - 1), WHITE_SHINE)
        core_img.putpixel((ex + 1, ey + 1), SKY_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Weapon Layer)
    # File: weapon/weapon_seal_clapper_gauntlets.png
    # Crystal Pneumatic Clapper Gauntlets (琉璃氣動拍浪拳套)
    # Features:
    # - Held on right hand (x: 94..124, y: 60..86)
    # - Single-wield (0-MKT7 compliant: left side has 0 weapon pixels)
    # - Heavy pneumatic tungsten cylinder sleeve at (94..102, 68..80) with brass bands
    # - Twin chrome pneumatic piston rods and brass pressure valve
    # - Faceted thick Cyan Crystal Clapper striking flipper head (104..122, 62..84)
    # - Razor-clean crystalline highlights and mint pressure relief port
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Tungsten Cylinder Sleeve & Bracket (x: 94..102, y: 68..80)
    for y in range(68, 81):
        for x in range(94, 103):
            dx = abs(x - 98.0) / 4.0
            spec = max(0.0, 1.0 - dx)
            r_t = int(np.clip(58 * (0.8 + 0.4 * spec), 0, 255))
            g_t = int(np.clip(54 * (0.8 + 0.4 * spec), 0, 255))
            b_t = int(np.clip(68 * (0.8 + 0.4 * spec), 0, 255))
            weapon_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Brass reinforcement collars
    wd.rectangle([94, 69, 97, 79], fill=GOLD_BASE, outline=OUTLINE)
    wd.rectangle([100, 70, 102, 78], fill=GOLD_BASE, outline=OUTLINE)

    # 2. Twin Chrome Piston Rods (x: 102..106, y: 71..77)
    wd.line([(102, 72), (107, 72)], fill=WHITE_SHINE, width=2)
    wd.line([(102, 76), (107, 76)], fill=WHITE_SHINE, width=2)

    # Brass pressure valve wheel at top (106..110, 62..66)
    wd.ellipse([106, 62, 110, 66], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((108, 64), fill=MINT_BASE)

    # 3. Faceted Marine Cyan Crystal Clapper Striking Head (x: 105..122, y: 64..84)
    crystal_poly = [
        (106, 68),
        (114, 64),
        (121, 68),
        (122, 75),
        (120, 81),
        (112, 84),
        (105, 80)
    ]
    wd.polygon(crystal_poly, fill=CRYSTAL_LIGHT, outline=OUTLINE)

    # Shading across the crystal clapper face
    for y in range(64, 85):
        for x in range(105, 123):
            if weapon_img.getpixel((x, y))[3] > 100:
                dist_c = max(0.0, 1.0 - ((x - 114.0)**2 + (y - 74.0)**2)**0.5 / 10.0)
                r_c = int(np.clip(96 * (0.7 + 0.45 * dist_c) + 30, 0, 255))
                g_c = int(np.clip(192 * (0.7 + 0.45 * dist_c) + 20, 0, 255))
                b_c = int(np.clip(255 * (0.8 + 0.25 * dist_c), 0, 255))
                weapon_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Facet lines & crystal bevel sparkles
    wd.line([(106, 68), (114, 74), (121, 68)], fill=CRYSTAL_SHINE, width=1)
    wd.line([(114, 74), (122, 75)], fill=CRYSTAL_SHINE, width=1)
    wd.line([(114, 74), (112, 84)], fill=CRYSTAL_DARK, width=1)
    wd.line([(105, 80), (114, 74)], fill=CRYSTAL_DARK, width=1)
    # Brightest glints on crystal facets
    wd.point((114, 65), fill=WHITE_SHINE)
    wd.point((121, 69), fill=WHITE_SHINE)
    wd.point((114, 74), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_seal_marine_propeller_brass", key_img),
        ("back_curio", "curio_seal_hydro_ducted_tail_flukes", curio_img),
        ("chassis", "chassis_seal_marine_titanium_default", chassis_img),
        ("head_unit", "head_seal_streamline_cowl_sonar", head_img),
        ("costume", "costume_seal_deepsea_diver_harness", costume_img),
        ("optic_core", "face_seal_cyan_quartz_convex_lens", core_img),
        ("weapon", "weapon_seal_clapper_gauntlets", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{SEAL_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{SEAL_PD_DIR}/winding_key/key_seal_marine_propeller_brass.png", f"{KEY_DIR}/key_seal_marine_propeller_brass.png")
    shutil.copyfile(f"{SEAL_PD_DIR}/weapon/weapon_seal_clapper_gauntlets.png", f"{WEAPON_DIR}/weapon_seal_clapper_gauntlets.png")
    print("  ✓ Synced key & weapon to universal folders")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order by layer_z_index:
    # z=5:  winding_key
    # z=8:  back_curio
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

    proof_comp = f"{SEAL_PD_DIR}/proof_paperdoll_seal_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SEAL_PD_DIR}/proof_paperdoll_seal_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 36
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
        sd.text((px + 4, py + H + 8), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{SEAL_PD_DIR}/proof_seal_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    # Standard ground soft shadow for idle assets (y: 110..122)
    idle_base = composite.copy()
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([34, 110, 94, 122], fill=(31, 26, 58, 110))
    shd.ellipse([44, 112, 84, 120], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(idle_base)

    # 1. 128x128 game/assets/sprites/player/seal_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/seal_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/seal_idle.png
    p_idle_64 = f"{PLAYER_DIR}/seal_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/seal_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/seal_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/seal_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/seal_idle.png"
    idle_with_shadow.save(p_web_idle)
    print("  ✓ Official Idle assets (64, 128, party, web) generated successfully")

    # 5. Showcase HD (800x1200 RGBA, 4-corner alpha=0)
    os.makedirs(SHOWCASE_DIR, exist_ok=True)
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
        sc_sdraw.ellipse((400 - 220, 1120 - 22, 400 + 220, 1120 + 22), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{SHOWCASE_DIR}/seal_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL CLAPPING SEAL CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
