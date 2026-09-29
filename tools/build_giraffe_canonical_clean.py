#!/usr/bin/env python3
"""
build_giraffe_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十五族 鐘塔長頸鹿 (The Belfry Giraffe, giraffe) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/design/BELFRY_GIRAFFE_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  stamped ivory tinplate plates #FFFDF8, polished walnut wood mosaic patches #FFA010,
  three-segment telescoping brass periscope neck tubes #FFD028,
  dual brass ossicone radar knobs with mint-green quartz prisms #4ED86A,
  dawn herald woolen cape #FFA010, dual periscope quartz convex lenses #4ED86A,
  belfry celestial-string composite mechanical bow #FFA010/#FFD028,
  three-ring openwork carillon brass key #FFD028,
  miniature pendulum bob linkage tail #FFD028)
- references/art_direction.md & references/brand_assets.md:
  Dopamine + European Clockwork Marionette palette:
    1. Base: Ivory Canvas & Stamped Tinplate (#FFFDF8, #E8ECF2)
    2. Primary: Dopamine Dawn Warm Orange / Walnut (#FFA010, #FFB84D)
    3. Secondary: Celestial Mint Green Quartz (#4ED86A, #85FFA0)
    4. Metal: Dopamine Gold & Brass (#FFD028, #E6A15C)
    5. Sanded Tinplate: (#5A4E46, #7A6C62, #3A322D, #8A7A70)
    6. Accent: Coral Pink (#FF5E8A) for seals, rivets and cape brooch
    7. Dark Outline: Deep Blue-Purple (#1F1A3A)
    8. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GIRAFFE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/giraffe"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Belfry Giraffe Specification)
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

# 3. Dawn Dopamine Warm Orange / Walnut (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 4. Sanded Tinplate Plates (#5A4E46, #7A6C62, #3A322D)
TIN_SHINE = (156, 142, 134, 255)
TIN_LIGHT = (122, 108, 98, 255)
TIN_BASE  = (90, 78, 70, 255)
TIN_DARK  = (58, 50, 45, 255)
TIN_DEEP  = (38, 32, 28, 255)

# 5. Dopamine Coral Pink (#FF5E8A) for seals & brooch
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 195, 215, 255)
CORAL_DARK  = (210, 45, 95, 255)

# 6. Mint Green Optic Quartz (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (133, 255, 160, 255)
MINT_SHINE = (200, 255, 215, 255)
MINT_DARK  = (40, 160, 68, 255)

# 7. Sky Blue & Steel String (#38A0FF)
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
    print("=== BUILDING 第五十五族 鐘塔長頸鹿 (THE BELFRY GIRAFFE) CANONICAL ASSETS ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Under Chassis / Back Layer)
    # File: winding_key/key_giraffe_three_ring_carillon_brass.png
    # Features:
    # - 三環鏤空八音音筒發條鑰匙 (Three-Ring Carillon Brass Key)
    # - Standing upright on back, central brass spindle from (64, 42) up to (64, 20)
    # - Three interlocking openwork rings:
    #     Top ring at (64.0, 13.0), radius 7.5
    #     Left ring at (53.0, 22.0), radius 7.5
    #     Right ring at (75.0, 22.0), radius 7.5
    # - Center openwork holes with carillon comb gear teeth
    # - Central coral pink axle washer (#FF5E8A) at (64, 22)
    # - Complies with 0-ART29: warm golden bronze outline OUTLINE_KEY, 0 dark artifacts
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Vertical Key Spindle Shaft (x: 62..66, y: 22..42)
    for sy in range(22, 43):
        for sx in range(62, 67):
            shade = 1.0 - abs(sx - 64.0) / 2.5
            shine = max(0.0, 1.0 - abs(sx - 63.0) / 1.5)**2
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * shade) + 30 * shine, 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * shade) + 25 * shine, 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade) + 15 * shine, 0, 255))
            key_img.putpixel((sx, sy), (r, g, b, 255))

    # Base mounting flange & collar rings
    kd.rectangle([60, 38, 68, 42], fill=GOLD_BASE, outline=OUTLINE_KEY)
    kd.rectangle([59, 41, 69, 44], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.line([(60, 39), (68, 39)], fill=GOLD_LIGHT, width=1)

    # 2. Three Interlocking Openwork Carillon Rings
    ring_centers = [
        (64.0, 13.0),   # Top ring
        (53.0, 22.0),   # Left ring
        (75.0, 22.0)    # Right ring
    ]
    outer_rad = 7.5
    outer_thick = 2.2
    inner_rad = 4.8

    for rx, ry in ring_centers:
        for dy in range(int(-outer_rad - 3), int(outer_rad + 4)):
            for dx in range(int(-outer_rad - 3), int(outer_rad + 4)):
                d = (dx**2 + dy**2)**0.5
                px = int(round(rx + dx))
                py = int(round(ry + dy))
                if 0 <= px < W and 0 <= py < H:
                    in_ring = (inner_rad <= d <= outer_rad)
                    if in_ring:
                        spec = max(0.0, 1.0 - abs(d - 0.5 * (inner_rad + outer_rad)) / (outer_thick / 2.0))
                        shine = max(0.0, 1.0 - ((dx - 1.5)**2 + (dy + 2.0)**2)**0.5 / 4.0)**2
                        r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                        key_img.putpixel((px, py), (r, g, b, 255))

        # Carillon comb teeth along outer rim (8 micro gear teeth per ring)
        for i in range(8):
            theta = i * (2.0 * np.pi / 8.0)
            tx = int(round(rx + np.cos(theta) * (outer_rad + 0.8)))
            ty = int(round(ry + np.sin(theta) * (outer_rad + 0.8)))
            if 0 <= tx < W and 0 <= ty < H:
                key_img.putpixel((tx, ty), GOLD_LIGHT if i % 2 == 0 else GOLD_DARK)

    # 3. Central Escapement Hub with Coral Pink Rivet (#FF5E8A) at (64, 22)
    kd.ellipse([60, 18, 68, 26], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([61, 19, 67, 25], fill=CORAL_BASE)
    kd.ellipse([62, 20, 66, 24], fill=IVORY_BASE, outline=GOLD_BASE)
    kd.point((64, 21), fill=WHITE_SHINE)
    kd.point((64, 22), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_giraffe_pendulum_bob_link_tail.png
    # Features:
    # - 微型黃銅鐘擺重錘連桿短尾 (Miniature Pendulum Bob Linkage Tail)
    # - Pivot escapement bracket at hip (64, 82..86)
    # - Slender brass pendulum rod extending down-left to (42, 104)
    # - Symmetrical circular brass pendulum bob weight at (42, 104), radius 7.5
    # - Concentric engraved ring, dopamine coral pink (#FF5E8A) center jewel
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Pivot bracket at hip (62..66, 82..86)
    cd.ellipse([61, 81, 67, 87], fill=GOLD_DARK, outline=OUTLINE)
    cd.ellipse([62, 82, 66, 86], fill=GOLD_BASE)
    cd.point((64, 83), fill=GOLD_LIGHT)

    # 2. Slender brass pendulum rod from (64, 84) to (42, 104)
    p0 = np.array([64.0, 84.0])
    p1 = np.array([42.0, 104.0])
    for t in np.linspace(0.0, 1.0, 28):
        pt = p0 + t * (p1 - p0)
        for offset in [-1.0, 0.0, 1.0]:
            normal = np.array([-(p1[1] - p0[1]), (p1[0] - p0[0])])
            normal = normal / (np.linalg.norm(normal) + 1e-6)
            px = int(round(pt[0] + offset * normal[0]))
            py = int(round(pt[1] + offset * normal[1]))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(offset) / 1.5
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * shade), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * shade), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                curio_img.putpixel((px, py), (r, g, b, 255))

    # 3. Circular Brass Pendulum Bob at (42, 104)
    bob_cx, bob_cy = 42.0, 104.0
    bob_rad = 7.5
    for dy in range(-9, 10):
        for dx in range(-9, 10):
            d = (dx**2 + dy**2)**0.5
            if d <= bob_rad:
                px = int(round(bob_cx + dx))
                py = int(round(bob_cy + dy))
                spec = max(0.0, 1.0 - d / bob_rad)
                shine = max(0.0, 1.0 - ((dx + 2)**2 + (dy + 2)**2)**0.5 / 3.0)**2
                # Concentric ring groove at d ~= 4.5
                is_groove = abs(d - 4.5) < 0.8
                if is_groove:
                    r = int(np.clip(GOLD_DARK[0] * 0.9, 0, 255))
                    g = int(np.clip(GOLD_DARK[1] * 0.9, 0, 255))
                    b = int(np.clip(GOLD_DARK[2] * 0.9, 0, 255))
                else:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                curio_img.putpixel((px, py), (r, g, b, 255))

    # Center coral pink rivet on bob
    cd.ellipse([int(bob_cx - 2), int(bob_cy - 2), int(bob_cx + 2), int(bob_cy + 2)], fill=CORAL_BASE, outline=OUTLINE)
    cd.point((int(bob_cx), int(bob_cy)), fill=WHITE_SHINE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_giraffe_sanded_tinplate_default.png
    # Features:
    # - 沖壓馬口鐵胡桃拼花矮萌底盤 (Stamped Tinplate Walnut Giraffe Chassis)
    # - 2.2 chibi ratio, stout low-center-of-gravity stance
    # - Soft ground contact shadow under hooves (x: 26..102, y: 112..120)
    # - Stepped brass mechanical hooves at (44, 114) and (76, 114)
    # - Sanded tinplate & brass ball-joint knees at (46, 96) and (74, 96)
    # - Torso: Stamped thin ivory tinplate plates (#FFFDF8) with walnut mosaic patches (#FFA010)
    # - Upper chest & neck base flange at (x: 48..80, y: 44..59)
    # - Left arm at (37..47, 68..78), right arm at (79..89, 68..78) (strictly x < 94)
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
        # Stepped brass plate on hoof
        ch_d.polygon([
            (int(fx - 4), int(fy + 1)),
            (int(fx), int(fy + 4)),
            (int(fx + 4), int(fy + 1))
        ], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((int(fx - 2), int(fy - 1)), fill=GOLD_LIGHT)
        ch_d.point((int(fx + 2), int(fy - 1)), fill=WHITE_SHINE)

    # 3. Mechanical Stepper Legs (44..52, 88..113) & (68..76, 88..113)
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
                r = int(np.clip(TIN_SHINE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(TIN_SHINE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(TIN_SHINE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Brass knee ball-joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 5, mid_y - 4, mid_x + 5, mid_y + 4], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Upper Chest Flange & Curved Neck Base Hinge (x: 48..80, y: 44..59)
    for ny in range(44, 60):
        for nx in range(48, 81):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 16.0)
            shine = max(0.0, 1.0 - abs(nx - 60.0) / 6.0)**2
            r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.2 * spec) + 15 * shine, 0, 255))
            g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.2 * spec) + 15 * shine, 0, 255))
            b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.2 * spec) + 10 * shine, 0, 255))
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

                # Walnut wood mosaic patches (#FFA010) on flank sides
                is_walnut_patch = ((44 <= tx <= 54 or 72 <= tx <= 82) and (62 <= ty <= 74 or 78 <= ty <= 88))
                is_belly_enamel = (54 <= tx <= 74 and 64 <= ty <= 90)

                if is_walnut_patch:
                    r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
                elif is_belly_enamel:
                    r = int(np.clip(IVORY_BASE[0] * (0.88 + 0.2 * spec) + 15 * shine, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.88 + 0.2 * spec) + 15 * shine, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.88 + 0.2 * spec) + 10 * shine, 0, 245))
                else:
                    r = int(np.clip(TIN_SHINE[0] * (0.85 + 0.35 * spec) + 40 * shine, 0, 255))
                    g = int(np.clip(TIN_SHINE[1] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
                    b = int(np.clip(TIN_SHINE[2] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Brass decorative rivets at panel seams
    for ry in [66, 74, 82]:
        for rx in [53, 75]:
            ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
            ch_d.point((rx, ry - 1), fill=GOLD_LIGHT)

    # 6. Arms: Left arm at (37..47, 68..78); Right arm at (79..89, 68..78) (strictly x < 94)
    ch_d.ellipse([37, 68, 47, 78], fill=IVORY_BASE, outline=OUTLINE)
    ch_d.ellipse([39, 70, 45, 76], fill=GOLD_BASE)
    ch_d.point((42, 72), fill=GOLD_LIGHT)

    ch_d.ellipse([79, 68, 89, 78], fill=IVORY_BASE, outline=OUTLINE)
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
    # File: head_unit/head_giraffe_telescoping_periscope_cowl.png
    # Features:
    # - 三節黃銅伸縮潛望觀測兜帽 (Telescoping Periscope Cowl & Neck)
    # - Ivory tinplate faceplate (#FFFDF8) over head (y: 34..57, x: 42..86)
    # - Three-segment brass telescoping neck tubes with gear rack sliders (y: 46..58)
    # - Dual rounded brass ossicone radar knobs at (52, 20) and (76, 20)
    # - Mint-green glowing quartz prisms on ossicone tips (#4ED86A)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Three-segment telescoping neck tubes with gear rack sliders (x: 48..80, y: 46..58)
    for ny in range(46, 59):
        # 3 distinct concentric tube segments: 46..49, 50..53, 54..58
        segment_id = (ny - 46) // 4
        sw = 14.0 + segment_id * 1.5
        for nx in range(int(hcx - sw), int(hcx + sw + 1)):
            spec = max(0.0, 1.0 - abs(nx - hcx) / (sw + 0.1))
            shine = max(0.0, 1.0 - abs(nx - (hcx - 3.0)) / 5.0)**2
            is_rack = (abs(nx - (hcx - 8)) < 1.0 or abs(nx - (hcx + 8)) < 1.0) and (ny % 2 == 0)
            if is_rack:
                r = int(np.clip(GOLD_LIGHT[0], 0, 255))
                g = int(np.clip(GOLD_LIGHT[1], 0, 255))
                b = int(np.clip(GOLD_LIGHT[2], 0, 255))
            else:
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            head_img.putpixel((nx, ny), (r, g, b, 255))

    # Segment divider lines
    hd.line([(int(hcx - 14), 49), (int(hcx + 14), 49)], fill=GOLD_DARK, width=1)
    hd.line([(int(hcx - 15), 53), (int(hcx + 15), 53)], fill=GOLD_DARK, width=1)

    # 2. Main Faceplate & Cowl Shell (x: 42..86, y: 34..50)
    for y in range(34, 51):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - 42.0) / 10.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 21.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 7.0)**2
                # Walnut mosaic patches on temple sides
                is_side_walnut = (x < 48 or x > 80) and (36 <= y <= 46)
                if is_side_walnut:
                    r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
                else:
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.2 * spec) + 15 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 3. Dual Ossicone Radar Knobs at (52, 20) and (76, 20)
    for ox, oy in [(52.0, 20.0), (76.0, 20.0)]:
        # Vertical stalk from head up to knob
        hd.rectangle([int(ox - 2), int(oy + 2), int(ox + 2), 34], fill=GOLD_BASE, outline=OUTLINE)
        hd.line([(int(ox), int(oy + 2)), (int(ox), 33)], fill=GOLD_LIGHT, width=1)
        # Spherical radar knob
        hd.ellipse([int(ox - 5), int(oy - 5), int(ox + 5), int(oy + 5)], fill=GOLD_BASE, outline=OUTLINE)
        hd.ellipse([int(ox - 3), int(oy - 3), int(ox + 3), int(oy + 3)], fill=GOLD_LIGHT)
        # Glowing mint-green quartz prism tip (#4ED86A)
        hd.polygon([
            (int(ox - 3), int(oy - 5)),
            (int(ox), int(oy - 10)),
            (int(ox + 3), int(oy - 5))
        ], fill=MINT_BASE, outline=OUTLINE)
        hd.point((int(ox), int(oy - 8)), fill=MINT_LIGHT)
        hd.point((int(ox), int(oy - 7)), fill=WHITE_SHINE)

    # Forehead crest plate
    hd.polygon([(56, 34), (64, 28), (72, 34)], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 31), fill=GOLD_LIGHT)

    # 4. Hollow Eye Sockets for 0-ART27 (Strictly alpha == 0)
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
    # File: costume/costume_giraffe_dawn_herald_woolen_cape.png
    # Features:
    # - 晨曦禮賓防風呢絨斗篷披肩 (Dawn Herald Woolen Cape)
    # - Dawn warm orange (#FFA010) woolen cape with ivory (#FFFDF8) trim
    # - Coral pink (#FF5E8A) round brooch fastener at (64, 63)
    # - Dual rows of polished brass button studs (#FFD028)
    # - Stitched hemlines
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(60, 88):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2

            # Ivory lining along lapel / inner border
            is_ivory_trim = (abs(x - 64.0) < 3.0 and y >= 65) or (y >= 84)

            if is_ivory_trim:
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.2 * spec) + 15 * shine, 0, 255))
            else:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Dual rows of brass button studs (#FFD028)
    for by in [68, 74, 80]:
        for bx in [58, 70]:
            cos_d.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=GOLD_BASE, outline=OUTLINE)
            cos_d.point((bx, by - 1), fill=GOLD_LIGHT)

    # Coral Pink round brooch fastener at (64, 63)
    cos_d.ellipse([61, 60, 67, 66], fill=GOLD_DARK, outline=OUTLINE)
    cos_d.ellipse([62, 61, 66, 65], fill=CORAL_BASE)
    cos_d.point((64, 62), fill=CORAL_LIGHT)
    cos_d.point((64, 63), fill=WHITE_SHINE)

    # Epaulet fringe accents at shoulders (44, 62) and (84, 62)
    for px, py in [(44.0, 62.0), (84.0, 62.0)]:
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=GOLD_DARK, outline=OUTLINE)
        cos_d.ellipse([int(px - 2), int(py - 1), int(px + 2), int(py + 1)], fill=GOLD_BASE)
        cos_d.point((int(px), int(py)), fill=GOLD_LIGHT)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART26b enforcement: Zero pixels at y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_giraffe_dual_periscope_quartz_lens.png
    # Features:
    # - 雙聯潛望測距石英凸透鏡 (Dual Periscope Rangefinder Quartz Lens)
    # - Left eye at (54, 42): Mint green glowing quartz convex lens (#4ED86A)
    # - Right eye at (74, 42): Mint green glowing quartz convex lens (#4ED86A)
    # - Concentric reticle rings & crosshair markings (#FFD028 / #85FFA0)
    # - Polished brass screw bezels
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    eyes_config = [
        (54.0, 42.0),   # Left Eye
        (74.0, 42.0)    # Right Eye
    ]

    for ex, ey in eyes_config:
        # Brass screw bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Quartz convex lens gradient
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

        # Concentric reticle ring & crosshairs
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), MINT_LIGHT)
        core_img.putpixel((int(ex + 1), int(ey)), MINT_LIGHT)
        core_img.putpixel((int(ex), int(ey - 1)), MINT_LIGHT)
        core_img.putpixel((int(ex), int(ey + 1)), MINT_DARK)

    # Vernier dial tick marks on bezel
    c_d.point((49, 41), fill=GOLD_LIGHT)
    c_d.point((79, 41), fill=GOLD_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    # Guarantee center alignment alpha
    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_giraffe_belfry_celestial_bow.png
    # Features:
    # - 鐘樓天弦複合機關弓 (Belfry Celestial-String Composite Bow)
    # - Single-weapon held in right hand (grip at 88, 74)
    # - Layered spring-steel limbs with warm orange enamel (#FFA010) and brass accents (#FFD028)
    # - Upper limb curving up to upper eccentric pulley at (92, 40)
    # - Lower limb curving down to lower eccentric pulley at (92, 106)
    # - Dual eccentric brass pulley wheels with spokes
    # - High-tension royal spun steel-gold bowstring strung between pulleys
    # - Central clockwork guide rail and mint quartz aiming crystal (#4ED86A)
    # - Complies strictly with review.md 0-MKT7 single-weapon standard
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Bow Grip and Central Riser (x: 86..91, y: 70..78)
    wd.rectangle([86, 70, 91, 78], fill=ORANGE_BASE, outline=OUTLINE)
    wd.line([(87, 72), (87, 76)], fill=ORANGE_LIGHT, width=1)
    wd.rectangle([87, 73, 90, 75], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((88, 74), fill=GOLD_LIGHT)

    # Aiming Quartz Crystal at center of riser (#4ED86A)
    wd.polygon([(84, 74), (86, 72), (88, 74), (86, 76)], fill=MINT_BASE, outline=OUTLINE)
    wd.point((86, 74), fill=WHITE_SHINE)

    # 2. Upper Bow Limb: from (88, 70) curving forward and up to (92, 40)
    p_up_start = np.array([88.0, 70.0])
    p_up_ctrl = np.array([96.0, 55.0])
    p_up_end = np.array([92.0, 40.0])

    for t in np.linspace(0.0, 1.0, 36):
        # Quadratic bezier
        pt = (1 - t)**2 * p_up_start + 2 * (1 - t) * t * p_up_ctrl + t**2 * p_up_end
        for offset in [-1.5, -0.5, 0.5, 1.5]:
            tangent = 2 * (1 - t) * (p_up_ctrl - p_up_start) + 2 * t * (p_up_end - p_up_ctrl)
            normal = np.array([-tangent[1], tangent[0]])
            normal = normal / (np.linalg.norm(normal) + 1e-6)
            px = int(round(pt[0] + offset * normal[0]))
            py = int(round(pt[1] + offset * normal[1]))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(offset) / 2.0
                is_gold_trim = (abs(t - 0.5) < 0.2)
                if is_gold_trim:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                else:
                    r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # 3. Lower Bow Limb: from (88, 78) curving forward and down to (92, 106)
    p_dn_start = np.array([88.0, 78.0])
    p_dn_ctrl = np.array([96.0, 93.0])
    p_dn_end = np.array([92.0, 106.0])

    for t in np.linspace(0.0, 1.0, 36):
        pt = (1 - t)**2 * p_dn_start + 2 * (1 - t) * t * p_dn_ctrl + t**2 * p_dn_end
        for offset in [-1.5, -0.5, 0.5, 1.5]:
            tangent = 2 * (1 - t) * (p_dn_ctrl - p_dn_start) + 2 * t * (p_dn_end - p_dn_ctrl)
            normal = np.array([-tangent[1], tangent[0]])
            normal = normal / (np.linalg.norm(normal) + 1e-6)
            px = int(round(pt[0] + offset * normal[0]))
            py = int(round(pt[1] + offset * normal[1]))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(offset) / 2.0
                is_gold_trim = (abs(t - 0.5) < 0.2)
                if is_gold_trim:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                else:
                    r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # 4. Eccentric Pulley Wheels at (92, 40) and (92, 106)
    for pw_x, pw_y in [(92.0, 40.0), (92.0, 106.0)]:
        wd.ellipse([int(pw_x - 5), int(pw_y - 5), int(pw_x + 5), int(pw_y + 5)], fill=GOLD_DARK, outline=OUTLINE)
        wd.ellipse([int(pw_x - 4), int(pw_y - 4), int(pw_x + 4), int(pw_y + 4)], fill=GOLD_BASE)
        wd.ellipse([int(pw_x - 2), int(pw_y - 2), int(pw_x + 2), int(pw_y + 2)], fill=CORAL_BASE, outline=OUTLINE)
        wd.point((int(pw_x), int(pw_y)), fill=WHITE_SHINE)

    # 5. Royal Spun Steel Bowstring from (92, 40) to (86, 74) to (92, 106)
    for p_from, p_to in [((92.0, 40.0), (86.0, 74.0)), ((86.0, 74.0), (92.0, 106.0))]:
        for t in np.linspace(0.0, 1.0, 36):
            sx = int(round(p_from[0] + t * (p_to[0] - p_from[0])))
            sy = int(round(p_from[1] + t * (p_to[1] - p_from[1])))
            if 0 <= sx < W and 0 <= sy < H:
                weapon_img.putpixel((sx, sy), SKY_LIGHT if t > 0.4 and t < 0.6 else WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_giraffe_three_ring_carillon_brass", key_img),
        ("back_curio", "curio_giraffe_pendulum_bob_link_tail", curio_img),
        ("chassis", "chassis_giraffe_sanded_tinplate_default", chassis_img),
        ("head_unit", "head_giraffe_telescoping_periscope_cowl", head_img),
        ("costume", "costume_giraffe_dawn_herald_woolen_cape", costume_img),
        ("optic_core", "face_giraffe_dual_periscope_quartz_lens", core_img),
        ("weapon", "weapon_giraffe_belfry_celestial_bow", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{GIRAFFE_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{GIRAFFE_PD_DIR}/winding_key/key_giraffe_three_ring_carillon_brass.png",
                 f"{KEY_DIR}/key_giraffe_three_ring_carillon_brass.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{GIRAFFE_PD_DIR}/weapon/weapon_giraffe_belfry_celestial_bow.png",
                 f"{WEAPON_DIR}/weapon_giraffe_belfry_celestial_bow.png")

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

    proof_comp = f"{GIRAFFE_PD_DIR}/proof_paperdoll_giraffe_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{GIRAFFE_PD_DIR}/proof_paperdoll_giraffe_magenta.png"
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

    strip_path = f"{GIRAFFE_PD_DIR}/proof_giraffe_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/giraffe_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/giraffe_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/giraffe_idle.png
    p_idle_64 = f"{PLAYER_DIR}/giraffe_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/giraffe_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/giraffe_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/giraffe_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/giraffe_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/giraffe_idle_hd.png)
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

        showcase_out = f"{SHOWCASE_DIR}/giraffe_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL BELFRY GIRAFFE CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
