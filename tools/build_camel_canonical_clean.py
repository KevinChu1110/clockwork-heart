#!/usr/bin/env python3
"""
build_camel_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十四族 日晷駱駝 (The Sundial Camel, camel) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/SUNDIAL_CAMEL_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  stamped sanded tinplate plates with brass trim, ivory canvas lining,
  sundial gnomon cowl, armillary dial brass key, scavenger astronomer robe,
  dual spectroscope quartz optic lenses, wasteland sundial refraction rod,
  twin condenser oil humps)
- references/art_direction.md & references/brand_assets.md:
  Dopamine + Desert Wasteland Astronomer palette:
    1. Base: Ivory Canvas & Enamel (#FFFDF8, #E8ECF2)
    2. Primary: Dopamine Gold (#FFD028, #E6A15C)
    3. Secondary: Dawn Dopamine Warm Orange (#FFA010, #FFB84D)
    4. Desert Ochre: Weathered Ochre Sand (#D49B4B, #B88035)
    5. Sanded Tinplate: (#5A4E46, #7A6C62, #3A322D, #8A7A70)
    6. Optic & Quartz Crystal: Mint Green (#4ED86A, #85FFA0), Sky Blue (#38A0FF)
    7. Accent: Coral Pink (#FF5E8A) for seals and washers
    8. Dark Outline: Deep Blue-Purple (#1F1A3A)
    9. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMEL_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/camel"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Sundial Camel Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory Canvas & Enamel (#FFFDF8, #E8ECF2)
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

# 3. Dawn Dopamine Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 4. Desert Ochre Sand & Harmonized Cowl Plate (#987B5E / #B89B7E)
OCHRE_BASE  = (148, 122, 92, 255)
OCHRE_LIGHT = (182, 155, 125, 255)
OCHRE_SHINE = (220, 195, 165, 255)
OCHRE_DARK  = (112, 88, 62, 255)
OCHRE_DEEP  = (78, 58, 38, 255)

# 5. Sanded Tinplate Plates (#5A4E46, #7A6C62, #3A322D)
TIN_SHINE = (156, 142, 134, 255)
TIN_LIGHT = (122, 108, 98, 255)
TIN_BASE  = (90, 78, 70, 255)
TIN_DARK  = (58, 50, 45, 255)
TIN_DEEP  = (38, 32, 28, 255)

# 6. Dopamine Coral Pink (#FF5E8A) for seals & relief valve caps
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 195, 215, 255)
CORAL_DARK  = (210, 45, 95, 255)

# 7. Mint Green Optic Quartz (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (133, 255, 160, 255)
MINT_SHINE = (200, 255, 215, 255)
MINT_DARK  = (40, 160, 68, 255)

# 8. Sky Blue Gauge Quartz (#38A0FF)
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
            if ignore_regions:
                skip = False
                for item in ignore_regions:
                    if len(item) == 4:
                        rx1, ry1, rx2, ry2 = item
                        if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                            skip = True
                            break
                    elif len(item) == 3:
                        cx, cy, rad = item
                        if (x - cx)**2 + (y - cy)**2 <= rad**2:
                            skip = True
                            break
                if skip:
                    continue

            p_curr = px_snap[x, y]
            a_curr = p_curr[3] if isinstance(p_curr, (tuple, list)) else 0
            if a_curr < min_alpha:
                has_solid_neighbor = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            p_nb = px_snap[nx, ny]
                            a_nb = p_nb[3] if isinstance(p_nb, (tuple, list)) else 0
                            if a_nb >= min_alpha:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL SUNDIAL CAMEL SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_camel_armillary_dial_brass.png
    # Features:
    # - 黃銅日晷雙環刻度發條鑰匙 (Armillary Dial Brass Winding Key)
    # - Polished brass shaft extending from spine socket (64, 56) to central pivot at (64, 25)
    # - Horizontal brass drive bar connecting to dual armillary dial wings (left at 44, 25; right at 84, 25)
    # - Dual concentric armillary dial rings visibly breaking through character outer silhouette
    # - 24 solar terms micro graduation marks along the outer rings
    # - Central jewel pivot with coral pink washer (#FF5E8A) and ivory jewel boss
    # - Warm golden bronze outline (OUTLINE_KEY) compliant with 0-ART29 (< 260px dark, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    hub_x, hub_y = 64.0, 25.0

    # 1. Key Shaft with Machined Flanges from (64, 56) to (64, 25)
    for t in np.linspace(0.0, 1.0, 32):
        sy = 56.0 + (hub_y - 56.0) * t
        is_collar = (abs(t - 0.35) < 0.06) or (abs(t - 0.75) < 0.06)
        half_w = 3.0 if is_collar else 2.0

        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            px = int(round(hub_x + offset))
            py = int(round(sy))
            shade = 1.0 - abs(offset) / (half_w + 0.5)
            if is_collar:
                r = int(np.clip(GOLD_LIGHT[0] * (0.85 + 0.25 * shade), 0, 255))
                g = int(np.clip(GOLD_LIGHT[1] * (0.85 + 0.25 * shade), 0, 255))
                b = int(np.clip(GOLD_LIGHT[2] * (0.85 + 0.25 * shade), 0, 255))
            else:
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine socket mount boss at (64, 56)
    kd.ellipse([60, 52, 68, 60], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([62, 54, 66, 58], fill=GOLD_BASE)

    # 2. Horizontal Brass Crossbar connecting Hub to Left and Right Wings (x: 35..93, y: 23..27)
    for bx in range(35, 94):
        for by in range(23, 28):
            shade = 1.0 - abs(by - 25.0) / 3.0
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
            key_img.putpixel((bx, by), (r, g, b, 255))

    # 3. Dual Armillary Dial Wings at (42, 25) and (86, 25) (Outer rad: 12.0, Inner rad: 7.0)
    wing_centers = [(42.0, 25.0), (86.0, 25.0)]
    outer_rad = 11.5
    outer_thick = 2.4
    inner_rad = 6.5
    inner_thick = 2.0

    for wx, wy in wing_centers:
        for dy in range(int(-outer_rad - 3), int(outer_rad + 4)):
            for dx in range(int(-outer_rad - 3), int(outer_rad + 4)):
                d = (dx**2 + dy**2)**0.5
                px = int(round(wx + dx))
                py = int(round(wy + dy))
                if 0 <= px < W and 0 <= py < H:
                    in_outer = abs(d - outer_rad) <= (outer_thick / 2.0)
                    in_inner = abs(d - inner_rad) <= (inner_thick / 2.0)
                    in_spoke = (abs(dy) <= 1.0 and d <= outer_rad + 0.5)

                    if in_outer or in_inner or in_spoke:
                        spec = max(0.0, 1.0 - abs(d - (outer_rad if in_outer else inner_rad)) / 2.0)
                        shine = max(0.0, 1.0 - ((dx - 2)**2 + (dy + 3)**2)**0.5 / 5.0)**2
                        r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                        key_img.putpixel((px, py), (r, g, b, 255))

        # Solar Terms Micro Tick Marks (12 on each wing = 24 total)
        for i in range(12):
            theta = i * (2.0 * np.pi / 12.0)
            nx = int(round(wx + np.cos(theta) * (outer_rad + 0.8)))
            ny = int(round(wy + np.sin(theta) * (outer_rad + 0.8)))
            if 0 <= nx < W and 0 <= ny < H:
                key_img.putpixel((nx, ny), GOLD_LIGHT if i % 3 == 0 else GOLD_DARK)

        # Center jewel in each wing
        kd.ellipse([int(wx - 3), int(wy - 3), int(wx + 3), int(wy + 3)], fill=CORAL_BASE, outline=OUTLINE_KEY)
        kd.point((int(wx), int(wy)), fill=WHITE_SHINE)

    # 4. Central Escapement Pivot Hub with Coral Pink Washer (#FF5E8A)
    kd.ellipse([int(hub_x - 6), int(hub_y - 6), int(hub_x + 6), int(hub_y + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 5), int(hub_y - 5), int(hub_x + 5), int(hub_y + 5)], fill=CORAL_BASE)
    kd.ellipse([int(hub_x - 3), int(hub_y - 3), int(hub_x + 3), int(hub_y + 3)], fill=IVORY_BASE, outline=GOLD_BASE)
    kd.point((int(hub_x), int(hub_y - 1)), fill=WHITE_SHINE)
    kd.point((int(hub_x), int(hub_y)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_camel_twin_condenser_humps.png
    # Features:
    # - 雙聯散熱油壺金屬駝峰 (Twin Condenser Oil Humps)
    # - Symmetrical pair of rounded brushed brass oil condenser tanks (#FFD028, #E6A15C)
    # - Left hump center at (44, 58), Right hump center at (84, 58)
    # - Central clearance at x: 56..72 strictly empty (alpha=0) so winding key shaft passes cleanly
    # - Concentric ribbed cooling fins encircling each tank
    # - Top knurled brass filler caps with coral pink relief valve domes (#FF5E8A)
    # - Micro steam exhaust nozzles
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    humps = [(44.0, 58.0), (84.0, 58.0)]
    hump_rx = 11.5
    hump_ry = 13.5

    for hx, hy in humps:
        for y in range(int(hy - hump_ry - 2), int(hy + hump_ry + 2)):
            for x in range(int(hx - hump_rx - 2), int(hx + hump_rx + 2)):
                dx = (x - hx) / hump_rx
                dy = (y - hy) / hump_ry
                d_sq = dx**2 + dy**2
                if d_sq <= 1.0:
                    spec = max(0.0, 1.0 - d_sq**0.5)
                    shine = max(0.0, 1.0 - ((x - (hx - 3))**2 + (y - (hy - 3))**2)**0.5 / 8.0)**2
                    # Cooling fin horizontal ribs (ribs every 4px)
                    is_rib = (abs((y - (hy - 6)) % 4.0) < 1.0)
                    if is_rib:
                        r = int(np.clip(GOLD_LIGHT[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        g = int(np.clip(GOLD_LIGHT[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                        b = int(np.clip(GOLD_LIGHT[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    else:
                        r = int(np.clip(BRASS_BASE[0] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                        g = int(np.clip(BRASS_BASE[1] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                        b = int(np.clip(BRASS_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                    curio_img.putpixel((x, y), (r, g, b, 255))

        # Top Knurled Filler Cap & Coral Pink Pressure Relief Valve (#FF5E8A)
        cap_y = int(hy - hump_ry)
        cd.rectangle([int(hx - 4), cap_y - 3, int(hx + 4), cap_y], fill=GOLD_BASE, outline=OUTLINE)
        cd.ellipse([int(hx - 3), cap_y - 6, int(hx + 3), cap_y - 2], fill=CORAL_BASE, outline=OUTLINE)
        cd.point((int(hx), cap_y - 4), fill=CORAL_LIGHT)

        # Bottom mounting flange & oil gauge glass tube
        flange_y = int(hy + hump_ry)
        cd.rectangle([int(hx - 6), flange_y - 2, int(hx + 6), flange_y + 2], fill=TIN_BASE, outline=OUTLINE)
        for gy in range(int(hy - 4), int(hy + 5)):
            curio_img.putpixel((int(hx), gy), SKY_LIGHT)
            curio_img.putpixel((int(hx + 1), gy), SKY_BASE)

    # Ensure central corridor x: 56..72 is strictly empty
    c_px = curio_img.load()
    for y in range(H):
        for x in range(56, 73):
            c_px[x, y] = (0, 0, 0, 0)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)

    # Re-enforce central corridor clear
    for y in range(H):
        for x in range(56, 73):
            c_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_camel_sanded_tinplate_default.png
    # Features:
    # - 磨砂馬口鐵雙峰矮萌素體底盤 (Sanded Tinplate Camel Chassis)
    # - 2.2 chibi ratio, cute stout low-center-of-gravity stance
    # - Feet: Molded dark brown anti-slip rubber hooves with brass shock springs at (44, 114) and (76, 114)
    # - Legs: Sanded tinplate & brass ball-joint knees at (46, 96) and (74, 96)
    # - Torso: Stamped sanded tinplate plates (#5A4E46 / #7A6C62) with ivory canvas belly lining (#FFFDF8)
    # - Neck: Gracefully arched short neck from (64, 58) up to (64, 46)
    # - Left arm at (38..46, 68..78), right arm at (78..90, 68..78) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow under hooves
    ch_d.ellipse([64 - 38, 116 - 6, 64 + 38, 116 + 6], fill=(31, 26, 58, 140))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Hooves & Stepper Springs at (44, 114) and (76, 114)
    feet_pos = [(44.0, 114.0), (76.0, 114.0)]
    for fx, fy in feet_pos:
        ch_d.ellipse([int(fx - 8), int(fy - 4), int(fx + 8), int(fy + 4)], fill=TIN_DEEP, outline=OUTLINE)
        ch_d.ellipse([int(fx - 6), int(fy - 3), int(fx + 6), int(fy + 3)], fill=TIN_BASE)
        ch_d.polygon([
            (int(fx - 3), int(fy + 1)),
            (int(fx), int(fy + 4)),
            (int(fx + 3), int(fy + 1))
        ], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((int(fx - 2), int(fy - 1)), fill=GOLD_LIGHT)
        ch_d.point((int(fx + 2), int(fy - 1)), fill=WHITE_SHINE)

    # 3. Sanded Tinplate Legs (44..52, 88..113) & (68..76, 88..113)
    leg_coords = [
        ((44.0, 113.0), (52.0, 88.0)),
        ((76.0, 113.0), (70.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_coords:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-6, 7):
                spec = max(0.0, 1.0 - abs(dx) / 6.0)
                shine = max(0.0, 1.0 - abs(dx - 1.0) / 3.0)**2
                r = int(np.clip(TIN_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(TIN_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(TIN_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Brass knee ball-joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 5, mid_y - 4, mid_x + 5, mid_y + 4], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Upper Chest Flange & Curved Neck Hinge (x: 48..80, y: 44..59)
    for ny in range(44, 60):
        for nx in range(48, 81):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 16.0)
            r = int(np.clip(TIN_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(TIN_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(TIN_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Stout Torso (x: 42..86, y: 58..95)
    for ty in range(58, 95):
        for tx in range(42, 87):
            dx = (tx - 64.0) / 20.0
            dy = (ty - 76.0) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 68.0)**2)**0.5 / 12.0)**2
                is_belly_canvas = (52 <= tx <= 76 and 64 <= ty <= 88)
                if is_belly_canvas:
                    r = int(np.clip(245 * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
                    g = int(np.clip(242 * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
                    b = int(np.clip(232 * (0.85 + 0.25 * spec) + 15 * shine, 0, 245))
                else:
                    r = int(np.clip(TIN_BASE[0] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(TIN_BASE[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(TIN_BASE[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    for ry in [66, 74, 82]:
        for rx in [52, 76]:
            ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
            ch_d.point((rx, ry - 1), fill=GOLD_LIGHT)

    # 6. Arms: Left arm cupping mana at (38..46, 68..78); Right arm at (78..90, 68..78) (strictly x < 94)
    ch_d.ellipse([37, 68, 47, 78], fill=TIN_BASE, outline=OUTLINE)
    ch_d.ellipse([39, 70, 45, 76], fill=GOLD_BASE)
    ch_d.point((42, 72), fill=GOLD_LIGHT)

    ch_d.ellipse([79, 68, 89, 78], fill=TIN_BASE, outline=OUTLINE)
    ch_d.ellipse([81, 70, 87, 76], fill=GOLD_BASE)
    ch_d.point((84, 72), fill=GOLD_LIGHT)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART9/11 enforcement: Zero pixels at x >= 94
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_camel_sundial_gnomon_cowl.png
    # Features:
    # - 日晷晷針折光觀測兜帽 (Sundial Gnomon Cowl)
    # - Desert sand canvas hood (#D49B4B / #B88035) over head (y: 32..58, x: 42..86)
    # - Forehead brass sundial crest (#FFD028) at y: 24..34 with vertical gnomon pointer needle at x=64, y=16..30
    # - Folded ear flap shields at (38..44, 34..46) and (84..90, 34..46)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Base Sand Cowl Shell (x: 42..86, y: 34..57)
    for y in range(34, 58):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - 45.0) / 11.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 21.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 7.0)**2
                r = int(np.clip(OCHRE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(OCHRE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(OCHRE_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 2. Ear-Flap Shields at (36..44, 34..46) and (84..92, 34..46)
    hd.polygon([(36, 44), (34, 34), (42, 36), (44, 44)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(36, 38), (42, 40)], fill=GOLD_LIGHT, width=1)
    hd.polygon([(92, 44), (94, 34), (86, 36), (84, 44)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(92, 38), (86, 40)], fill=GOLD_LIGHT, width=1)

    # 3. Forehead Stamped Brass Sundial Crest (x: 44..84, y: 26..36)
    for y in range(26, 37):
        hw = 12.0 + (y - 26.0) * 0.8
        for x in range(int(hcx - hw), int(hcx + hw + 1)):
            spec = max(0.0, 1.0 - abs(x - hcx) / (hw + 0.1))
            shine = max(0.0, 1.0 - abs(x - (hcx - 2)) / 5.0)**2
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
            head_img.putpixel((x, y), (r, g, b, 255))
    hd.line([(int(hcx - 18), 36), (int(hcx + 18), 36)], fill=GOLD_LIGHT, width=1)

    # 4. Vertical Sundial Gnomon Pointer Needle at x=64, y: 16..28
    hd.polygon([(62, 28), (64, 16), (66, 28)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(64, 17), (64, 27)], fill=WHITE_SHINE, width=1)
    hd.ellipse([60, 27, 68, 31], fill=GOLD_DARK, outline=OUTLINE)
    hd.ellipse([62, 28, 66, 30], fill=GOLD_LIGHT)

    # 5. Hollow Eye Sockets for 0-ART27:
    h_px = head_img.load()
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    ignore_eyes = [(50, 38, 58, 46), (70, 38, 78, 46)]
    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=100, ignore_regions=ignore_eyes)

    # Re-enforce strictly hollow eye sockets after outline pass
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_camel_scavenger_astronomer_robe.png
    # Features:
    # - 廢土觀星學者帆布補丁長袍 (Scavenger Astronomer Canvas Robe)
    # - Warm orange (#FFA010) & mustard gold (#D49B4B) patchwork scholar robe
    # - Coarse linen stitches on shoulders
    # - Brass bells necklace hanging at chest (y: 66..76)
    # - Leather utility tool belt at y: 84..90
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(60, 87):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            is_orange_side = (x - 64.0) < (y - 72.0) * 0.4
            if is_orange_side:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(OCHRE_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(OCHRE_BASE[1] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                b = int(np.clip(OCHRE_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    for y in range(62, 84, 3):
        sx = int(round(64.0 + (y - 72.0) * 0.4))
        cos_d.point((sx, y), fill=IVORY_BASE)
        cos_d.point((sx + 1, y), fill=IVORY_LIGHT)

    # Chest Brass Chime Bells Necklace at y: 66..76
    cos_d.arc([50, 64, 78, 74], start=10, end=170, fill=GOLD_DARK, width=1)
    for bx, by in [(56, 71), (64, 73), (72, 71)]:
        cos_d.ellipse([bx - 3, by - 3, bx + 3, by + 3], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=GOLD_LIGHT)
        cos_d.point((bx, by + 4), fill=GOLD_DARK)

    # Epaulets at (42, 60) and (86, 60)
    for px, py in [(42.0, 60.0), (86.0, 60.0)]:
        cos_d.ellipse([int(px - 5), int(py - 4), int(px + 5), int(py + 4)], fill=OCHRE_DARK, outline=OUTLINE)
        cos_d.ellipse([int(px - 3), int(py - 2), int(px + 3), int(py + 2)], fill=GOLD_BASE)
        cos_d.point((int(px), int(py)), fill=GOLD_LIGHT)

    # Utility Belt (y: 86..92)
    waist_spans = [(48, 55), (57, 63), (65, 71), (73, 80)]
    for x0, x1 in waist_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=OCHRE_DARK, outline=OUTLINE)
        cos_d.line([(x0 + 1, 88), (x1 - 1, 88)], fill=GOLD_BASE, width=1)
        cos_d.point((int(0.5 * (x0 + x1)), 90), fill=GOLD_LIGHT)
    cos_d.rectangle([61, 86, 67, 92], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.rectangle([63, 88, 65, 90], fill=TIN_DEEP)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART26b enforcement: Zero pixels at y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_camel_dual_spectroscope_quartz_lens.png
    # Features:
    # - 雙聯光譜分折石英目鏡 (Dual Spectroscope Quartz Lens)
    # - Left eye at (54, 42): Amber gold antireflection lens (#FFD028, #FFA010)
    # - Right eye at (74, 42): Mint green polarizing quartz lens (#4ED86A, #85FFA0)
    # - Brass screw bezels with vernier gear teeth
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    eyes_config = [
        (54.0, 42.0, GOLD_BASE, GOLD_LIGHT, GOLD_DARK),   # Left Eye: Amber Gold Lens
        (74.0, 42.0, MINT_BASE, MINT_LIGHT, MINT_DARK)    # Right Eye: Mint Green Polarizing Lens
    ]

    for ex, ey, base_c, light_c, dark_c in eyes_config:
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r = int(np.clip(base_c[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(base_c[1] * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    b = int(np.clip(base_c[2] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), light_c)
        core_img.putpixel((int(ex + 1), int(ey)), light_c)
        core_img.putpixel((int(ex), int(ey - 1)), light_c)
        core_img.putpixel((int(ex), int(ey + 1)), dark_c)

    c_d.point((49, 41), fill=GOLD_LIGHT)
    c_d.point((79, 41), fill=GOLD_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_camel_sundial_refraction_rod.png
    # Features:
    # - 廢土日晷折射短杖 (Wasteland Sundial Refraction Rod)
    # - Polished brass telescopic staff held in right hand
    # - Shaft extends from (87, 88) up to (101, 56)
    # - Sundial dial disc at (101, 52) with rotating pointer and hex-cut mint quartz crystal (#4ED86A)
    # - Hanging chime bell at (96, 58)
    # - Spherical brass counterweight pommel at (87, 91)
    # - Complies strictly with review.md 0-MKT7 single-weapon standard
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    rod_x0, rod_y0 = 87.0, 88.0
    rod_x1, rod_y1 = 101.0, 56.0

    for t in np.linspace(0.0, 1.0, 40):
        rx = rod_x0 + t * (rod_x1 - rod_x0)
        ry = rod_y0 + t * (rod_y1 - rod_y0)
        is_collar = (abs(t - 0.3) < 0.05) or (abs(t - 0.7) < 0.05)
        half_w = 2.5 if is_collar else 1.5

        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            px = int(round(rx + offset * 0.8))
            py = int(round(ry - offset * 0.4))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(offset) / (half_w + 0.5)
                if is_collar:
                    r = int(np.clip(GOLD_LIGHT[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_LIGHT[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_LIGHT[2] * (0.85 + 0.25 * shade), 0, 255))
                else:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    disc_x, disc_y = 101.0, 52.0
    for dy in range(-7, 8):
        for dx in range(-7, 8):
            d = (dx**2 + dy**2)**0.5
            if d <= 6.5:
                px = int(round(disc_x + dx))
                py = int(round(disc_y + dy))
                spec = max(0.0, 1.0 - d / 6.5)
                shine = max(0.0, 1.0 - ((dx + 2)**2 + (dy + 2)**2)**0.5 / 3.0)**2
                r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.3 * spec) + 25 * shine, 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # Hex-cut Mint Quartz Crystal Gem at center of disc (#4ED86A) with rich facet shading
    for gy in range(-4, 5):
        for gx in range(-4, 5):
            if abs(gx) + abs(gy) * 0.7 <= 3.8:
                px = int(round(disc_x + gx))
                py = int(round(disc_y + gy))
                gd = (gx**2 + gy**2)**0.5
                g_spec = max(0.0, 1.0 - gd / 4.0)
                g_shine = max(0.0, 1.0 - ((gx + 1)**2 + (gy + 1)**2)**0.5 / 2.0)**2
                gr = int(np.clip(MINT_BASE[0] * (0.8 + 0.3 * g_spec) + 60 * g_shine, 0, 255))
                gg = int(np.clip(MINT_BASE[1] * (0.8 + 0.3 * g_spec) + 50 * g_shine, 0, 255))
                gb = int(np.clip(MINT_BASE[2] * (0.8 + 0.3 * g_spec) + 40 * g_shine, 0, 255))
                weapon_img.putpixel((px, py), (gr, gg, gb, 255))
    weapon_img.putpixel((int(disc_x - 1), int(disc_y - 1)), WHITE_SHINE)

    wd.line([(int(disc_x), int(disc_y - 4)), (int(disc_x + 2), int(disc_y - 9))], fill=GOLD_LIGHT, width=2)
    wd.point((int(disc_x + 2), int(disc_y - 9)), fill=WHITE_SHINE)

    wd.line([(int(disc_x - 3), int(disc_y + 4)), (96, 58)], fill=GOLD_DARK, width=1)
    wd.ellipse([94, 57, 98, 62], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((96, 59), fill=GOLD_LIGHT)

    wd.ellipse([84, 88, 90, 94], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([85, 89, 89, 93], fill=GOLD_LIGHT)
    wd.point((87, 90), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_camel_armillary_dial_brass", key_img),
        ("back_curio", "curio_camel_twin_condenser_humps", curio_img),
        ("chassis", "chassis_camel_sanded_tinplate_default", chassis_img),
        ("head_unit", "head_camel_sundial_gnomon_cowl", head_img),
        ("costume", "costume_camel_scavenger_astronomer_robe", costume_img),
        ("optic_core", "face_camel_dual_spectroscope_quartz_lens", core_img),
        ("weapon", "weapon_camel_sundial_refraction_rod", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{CAMEL_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{CAMEL_PD_DIR}/winding_key/key_camel_armillary_dial_brass.png",
                 f"{KEY_DIR}/key_camel_armillary_dial_brass.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{CAMEL_PD_DIR}/weapon/weapon_camel_sundial_refraction_rod.png",
                 f"{WEAPON_DIR}/weapon_camel_sundial_refraction_rod.png")

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

    proof_comp = f"{CAMEL_PD_DIR}/proof_paperdoll_camel_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{CAMEL_PD_DIR}/proof_paperdoll_camel_magenta.png"
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

    strip_path = f"{CAMEL_PD_DIR}/proof_camel_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([32, 108, 96, 120], fill=(31, 26, 58, 110))
    shd.ellipse([42, 110, 86, 118], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/camel_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/camel_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/camel_idle.png
    p_idle_64 = f"{PLAYER_DIR}/camel_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/camel_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/camel_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/camel_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/camel_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/camel_idle_hd.png)
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
        sc_sdraw.ellipse((400 - 220, 1120 - 22, 400 + 220, 1120 + 22), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{SHOWCASE_DIR}/camel_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL SUNDIAL CAMEL CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
