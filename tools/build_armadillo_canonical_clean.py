#!/usr/bin/env python3
"""
build_armadillo_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十九族 熔鎧犰狳 (The Crucible Armadillo, armadillo) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CRUCIBLE_ARMADILLO_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  quenched cast-iron ball-joint chassis with exposed brass bolts, ivory ceramic thermal shield,
  quenched visor cowl helmet, four-leaf foundry cooling winding key,
  foundry anvil heavy cuirass, amber refractory quartz optic lenses,
  black iron heavy greatsword, segmented stamped cast-iron carapace & heat-sink tail)
- references/art_direction.md & references/brand_assets.md:
  Dopamine + Molten Foundry palette:
    1. Base: Ivory Ceramic Glaze / Polished Nickel Alloy (#FFFDF8, #E8ECF2, #CCD4E0)
    2. Primary: Dopamine Foundry Brass Gold (#FFD028, #D4A520, #FFF59D)
    3. Secondary: Dawn Dopamine Warm Orange (#FFA010, #FFB84D)
    4. Accent: Dopamine Coral Pink (#FF5E8A, #FF2A6D, #FFA8C5)
    5. Cast Iron / Refractory Metal: (#2B2630, #3A4454, #4E5A6E)
    6. Dark Outline: Deep Blue-Purple (#1F1A3A)
    7. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
ARMADILLO_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/armadillo"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Crucible Armadillo Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory Ceramic / Heat Insulation (#FFFDF8, #E8ECF2)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (232, 236, 242, 255)
IVORY_DARK   = (204, 212, 224, 255)

# 2. Dopamine Foundry Brass Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Dawn Dopamine Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 4. Dopamine Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 195, 215, 255)
CORAL_DARK  = (210, 45, 95, 255)

# 5. Cold-Rolled Cast Iron / Refractory Black (#2B2630, #3A4454, #4E5A6E)
IRON_LIGHT = (110, 125, 148, 255)
IRON_MID   = (78, 90, 110, 255)
IRON_BASE  = (58, 68, 84, 255)
IRON_DARK  = (43, 38, 48, 255)
IRON_DEEP  = (31, 26, 38, 255)

# 6. Amber Optic Crystal (#FFB020)
AMBER_BASE  = (255, 176, 32, 255)
AMBER_LIGHT = (255, 215, 90, 255)
AMBER_SHINE = (255, 245, 180, 255)
AMBER_DARK  = (215, 120, 10, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL CRUCIBLE ARMADILLO SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_armadillo_crucible_four_leaf_key.png
    # Features:
    # - 四葉散熱鍛造發條鑰匙 (Four-Leaf Foundry Cooling Winding Key)
    # - Robust forged brass shaft extending from spine socket (64, 56) to central hub at (64, 25)
    # - 4 symmetrical cloverleaf cooling vanes radiating at 0°, 90°, 180°, 270°
    # - Each leaf features an inner ventilation perforation
    # - Central escapement gear hub with warm amber / coral jewel pivot
    # - Warm golden bronze outline (OUTLINE_KEY) compliant with 0-ART29 (< 260px dark, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    hub_x, hub_y = 64.0, 25.0

    # 1. Key Shaft with Machined Thermal Flanges from (64, 56) to (64, 25)
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

    # 2. Four Cooling Cloverleaf Wings (Angles: 0°, 90°, 180°, 270°)
    angles = [0.0, np.pi / 2.0, np.pi, 3.0 * np.pi / 2.0]
    leaf_dist = 11.5
    leaf_radius = 6.0

    for ang in angles:
        cx = hub_x + np.cos(ang) * leaf_dist
        cy = hub_y + np.sin(ang) * leaf_dist
        # Outer leaf disc
        for dy in range(int(-leaf_radius - 1), int(leaf_radius + 2)):
            for dx in range(int(-leaf_radius - 1), int(leaf_radius + 2)):
                d = (dx**2 + dy**2)**0.5
                if d <= leaf_radius:
                    px = int(round(cx + dx))
                    py = int(round(cy + dy))
                    if 0 <= px < W and 0 <= py < H:
                        spec = max(0.0, 1.0 - d / leaf_radius)
                        r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * (spec**2), 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * (spec**2), 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 15 * (spec**2), 0, 255))
                        key_img.putpixel((px, py), (r, g, b, 255))

    # Inner ventilation perforations (hollow circles in each leaf)
    k_px = key_img.load()
    inner_rad = 2.4
    for ang in angles:
        cx = hub_x + np.cos(ang) * leaf_dist
        cy = hub_y + np.sin(ang) * leaf_dist
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if (dx**2 + dy**2)**0.5 <= inner_rad:
                    px = int(round(cx + dx))
                    py = int(round(cy + dy))
                    if 0 <= px < W and 0 <= py < H:
                        k_px[px, py] = (0, 0, 0, 0)

    # Connecting web bridges between leaves
    diag_angles = [np.pi / 4.0, 3.0 * np.pi / 4.0, 5.0 * np.pi / 4.0, 7.0 * np.pi / 4.0]
    for dang in diag_angles:
        for r_step in np.linspace(4.0, 8.5, 10):
            bx = int(round(hub_x + np.cos(dang) * r_step))
            by = int(round(hub_y + np.sin(dang) * r_step))
            if 0 <= bx < W and 0 <= by < H:
                key_img.putpixel((bx, by), GOLD_DARK)

    # 3. Central Escapement Hub & Jewel Boss
    kd.ellipse([int(hub_x - 6), int(hub_y - 6), int(hub_x + 6), int(hub_y + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 4), int(hub_y - 4), int(hub_x + 4), int(hub_y + 4)], fill=GOLD_BASE)
    # Core amber jewel
    kd.ellipse([int(hub_x - 2), int(hub_y - 2), int(hub_x + 2), int(hub_y + 2)], fill=ORANGE_BASE)
    kd.point((int(hub_x), int(hub_y - 1)), fill=GOLD_LIGHT)
    kd.point((int(hub_x), int(hub_y)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_armadillo_segmented_cast_iron_carapace.png
    # Features:
    # - 多節沖壓鑄鐵散熱背甲與四節散熱重尾 (Segmented Cast-Iron Carapace & Tail)
    # - 5-tier concentric stamped cast-iron shell plates (#2B2630 / #3A4454)
    # - Brass expansion hinges (#FFD028) & orange heat vent seams (#FFA010)
    # - Segmented heat-sink tail extending from pelvis (62, 88) down to ground at (36, 114)
    # - Clear central wind-up key port around (64, 40..58)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Broad Segmented Carapace Shell Plates (x: 40..88, y: 50..86)
    # Concentric curved plates arched across the back
    shell_cx, shell_cy = 64.0, 68.0
    for y in range(50, 88):
        for x in range(38, 90):
            # Elliptical distance from shell center
            dx = (x - shell_cx) / 22.0
            dy = (y - shell_cy) / 18.0
            d_sq = dx**2 + dy**2
            if d_sq <= 1.0:
                # Segment lines (5 tiers of overlapping cast iron plates)
                tier_idx = int((y - 50) / 7.5)
                is_seam = ((y - 50) % 7.5 < 1.0)
                spec = max(0.0, 1.0 - d_sq**0.5)
                shine = max(0.0, 1.0 - ((x - (shell_cx - 4))**2 + (y - (shell_cy - 4))**2)**0.5 / 12.0)**2

                if is_seam:
                    # Heat vent orange seam with brass glow
                    r = int(np.clip(ORANGE_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                    g = int(np.clip(ORANGE_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                    b = int(np.clip(ORANGE_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                else:
                    # Tough dark cast iron plate
                    base_c = IRON_BASE if tier_idx % 2 == 0 else IRON_MID
                    r = int(np.clip(base_c[0] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(base_c[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(base_c[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    # Brass rivets on plate edges
    for ry in [56, 64, 72, 80]:
        for rx in [44, 52, 76, 84]:
            cd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
            cd.point((rx, ry - 1), fill=GOLD_LIGHT)

    # 2. Four-Stage Telescopic Cast-Iron Heat-Sink Tail from (62, 88) to (36, 114)
    for seg_idx, (t0, t1, rad0, rad1) in enumerate([
        (0.0, 0.28, 5.0, 4.2),
        (0.25, 0.55, 4.5, 3.6),
        (0.52, 0.80, 3.8, 3.0),
        (0.78, 1.00, 3.2, 2.5)
    ]):
        for t in np.linspace(t0, t1, 16):
            cur_rad = rad0 + (rad1 - rad0) * ((t - t0) / (t1 - t0 + 0.001))
            tx = 62.0 + (36.0 - 62.0) * t
            ty = 88.0 + (114.0 - 88.0) * t
            for offset in np.linspace(-cur_rad, cur_rad, int(cur_rad * 2 + 1)):
                px = int(round(tx + offset * 0.7))
                py = int(round(ty - offset * 0.7))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - abs(offset) / (cur_rad + 0.1))
                    shine = max(0.0, 1.0 - abs(offset - 1.0) / 1.5)**2
                    r = int(np.clip(IRON_BASE[0] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(IRON_BASE[1] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(IRON_BASE[2] * (0.85 + 0.35 * spec) + 15 * shine, 0, 255))
                    curio_img.putpixel((px, py), (r, g, b, 255))

        # Brass coupling collar at joint
        cx = 62.0 + (36.0 - 62.0) * t1
        cy = 88.0 + (114.0 - 88.0) * t1
        cd.ellipse([int(cx - rad1 - 1), int(cy - 2), int(cx + rad1 + 1), int(cy + 2)], fill=GOLD_BASE, outline=OUTLINE)

    # Blunt spherical anti-recoil bumper weight at tail tip (36, 114)
    cd.ellipse([31, 110, 41, 118], fill=IRON_DARK, outline=OUTLINE)
    cd.ellipse([33, 112, 39, 116], fill=IRON_MID)
    cd.point((35, 113), fill=IRON_LIGHT)
    cd.point((36, 114), fill=WHITE_SHINE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_armadillo_crucible_iron_default.png
    # Features:
    # - 耐火鑄鐵球鉸素體底盤 (Crucible Cast-Iron Ball-Joint Chassis)
    # - 2.2 chibi ratio, stout low-center-of-gravity fortress stance
    # - Feet: Heavy steel anti-slip three-point treads at (44, 114) and (76, 114)
    # - Legs: Cast-iron and brass heavy ball-joint knees at (46, 96) and (74, 96)
    # - Torso: Quenched cast iron frame (#2B2630) with ivory ceramic belly plate (#FFFDF8)
    # - Left arm forward in shielding stance at (36..46, 68..78)
    # - Right arm at (80..92, 68..76) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow under feet and tail
    ch_d.ellipse([64 - 40, 116 - 6, 64 + 40, 116 + 6], fill=(31, 26, 58, 140))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Heavy Anti-Slip Steel Tread Feet at (44, 114) and (76, 114)
    feet_pos = [(44.0, 114.0), (76.0, 114.0)]
    for fx, fy in feet_pos:
        # Foot base plate
        ch_d.ellipse([int(fx - 9), int(fy - 4), int(fx + 9), int(fy + 4)], fill=IRON_DEEP, outline=OUTLINE)
        ch_d.ellipse([int(fx - 7), int(fy - 3), int(fx + 7), int(fy + 3)], fill=IRON_BASE)
        # Three anti-slip front tread cleats
        for t_off in [-5, 0, 5]:
            ch_d.polygon([
                (int(fx + t_off - 2), int(fy + 1)),
                (int(fx + t_off), int(fy + 4)),
                (int(fx + t_off + 2), int(fy + 1))
            ], fill=GOLD_BASE, outline=OUTLINE)
        # Highlight
        ch_d.point((int(fx - 2), int(fy - 1)), fill=GOLD_LIGHT)
        ch_d.point((int(fx + 2), int(fy - 1)), fill=WHITE_SHINE)

    # 3. Heavy Cast-Iron & Brass Shins/Thighs
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
                r = int(np.clip(IRON_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(IRON_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(IRON_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Brass knee ball-joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 5, mid_y - 4, mid_x + 5, mid_y + 4], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Upper Chest Flange & Neck Hinge (x: 46..82, y: 44..59)
    for ny in range(44, 60):
        for nx in range(46, 83):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 18.0)
            r = int(np.clip(IRON_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(IRON_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(IRON_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Stout Torso (x: 42..86, y: 58..95)
    # Cast-iron frame with ivory ceramic thermal shield on belly
    for ty in range(58, 95):
        for tx in range(42, 87):
            dx = (tx - 64.0) / 20.0
            dy = (ty - 76.0) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 68.0)**2)**0.5 / 12.0)**2
                is_belly_ceramic = (52 <= tx <= 76 and 64 <= ty <= 88)
                if is_belly_ceramic:
                    # Ivory ceramic thermal insulation tile (#FFFDF8) with soft tones
                    r = int(np.clip(236 * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
                    g = int(np.clip(232 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                    b = int(np.clip(224 * (0.85 + 0.25 * spec) + 20 * shine, 0, 242))
                else:
                    # Outer cast-iron heavy frame
                    r = int(np.clip(IRON_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(IRON_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(IRON_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Gear reduction inspection dial on belly at (64, 76)
    ch_d.ellipse([58, 70, 70, 82], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([59, 71, 69, 81], fill=IRON_DEEP)
    ch_d.ellipse([61, 73, 67, 79], fill=GOLD_BASE)
    ch_d.point((64, 76), fill=ORANGE_BASE)
    ch_d.point((63, 75), fill=WHITE_SHINE)

    # 6. Left Arm forward in guarding shield stance at (36..48, 68..80)
    for t in np.linspace(0.0, 1.0, 18):
        ax = 52.0 - t * 12.0
        ay = 66.0 + t * 8.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), IRON_BASE)
    ch_d.ellipse([36, 72, 46, 80], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.ellipse([38, 74, 44, 78], fill=IRON_LIGHT)
    ch_d.point((41, 76), fill=GOLD_LIGHT)

    # 7. Right Arm positioned at (80..92, 68..76) (strictly x < 94)
    for t in np.linspace(0.0, 1.0, 16):
        ax = 78.0 + t * 9.0  # max ax = 87
        ay = 66.0 + t * 6.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px = int(ax + dx)
                py = int(ay + dy)
                if px < 94 and dx**2 + dy**2 <= 9:
                    chassis_img.putpixel((px, py), IRON_BASE)
    # Right brass wrist / ball joint
    ch_d.ellipse([84, 71, 91, 78], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.point((87, 74), fill=GOLD_LIGHT)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART9/11 enforcement: Zero pixels at x >= 94
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_armadillo_quenched_visor_cowl.png
    # Features:
    # - 黑曜淬火面甲頭盔 (Quenched Visor Cowl Helmet)
    # - Cast-iron aerodynamic arched faceplate (#2B2630 / #3A4454)
    # - Golden stamped anti-splash brow visor at y: 26..34, x: 44..84 (#FFD028)
    # - Dual short folded brass ear fins at (38..46, 30..42) and (82..90, 30..42)
    # - Micro coral pink ventilation exhaust ports (#FF5E8A)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Base Arched Helmet Shell & Faceplate (x: 42..86, y: 34..57)
    for y in range(34, 58):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - 45.0) / 11.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 21.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 7.0)**2
                # Cast-iron plate tone
                r = int(np.clip(IRON_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(IRON_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(IRON_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Dual Coral Pink Cheek Vent Ports at (44, 50) and (84, 50)
    for cx in (44, 84):
        hd.ellipse([cx - 2, 50 - 2, cx + 2, 50 + 2], fill=CORAL_BASE, outline=OUTLINE)
        hd.point((cx, 50), fill=GOLD_LIGHT)

    # 2. Folded Brass Mechanical Ear Fins at (38..46, 32..44) and (82..90, 32..44)
    # Left Ear Fin
    hd.polygon([(38, 42), (36, 32), (44, 34), (46, 42)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(38, 36), (44, 38)], fill=GOLD_LIGHT, width=1)
    # Right Ear Fin
    hd.polygon([(90, 42), (92, 32), (84, 34), (82, 42)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(90, 36), (84, 38)], fill=GOLD_LIGHT, width=1)

    # 3. Stamped Golden Anti-Splash Brow Visor (x: 44..84, y: 26..36)
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

    # 4. Hollow Eye Sockets for 0-ART27:
    # Clear eye sockets centered at (54, 42) and (74, 42), radius 3.5px
    h_px = head_img.load()
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    # Outline pass ignoring eye sockets
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
    # File: costume/costume_armadillo_foundry_anvil_cuirass.png
    # Features:
    # - 熔爐鐵砧重裝板甲 (Foundry Anvil Heavy Cuirass)
    # - Heavy double cast-iron chestplate (#3A4454 / #2B2630)
    # - Warm gold brass protective corner guards (#FFD028)
    # - Molten orange hazard / heat warning accents (#FFA010)
    # - Miniature forged anvil crest in center chest at (64, 72)
    # - Flange skirting and belt ending strictly at y: 92
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Chest Cuirass (x: 46..82, y: 60..86)
    for y in range(60, 87):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            # Orange hazard chevron striping on chestplate trim
            is_orange_chevron = (64 <= y <= 66 and (x + y) % 6 < 3)
            if is_orange_chevron:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(IRON_MID[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(IRON_MID[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(IRON_MID[2] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Center Embossed Brass Anvil Totem at (64, 72)
    # Anvil horn, face, and base
    cos_d.polygon([(59, 70), (69, 70), (68, 72), (66, 73), (67, 75), (61, 75), (62, 73), (60, 72)], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.point((64, 71), fill=GOLD_LIGHT)

    # 2. Heavy Double-Stamped Curved Pauldrons at (42, 60) and (86, 60)
    for px, py in [(42.0, 60.0), (86.0, 60.0)]:
        cos_d.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=IRON_MID)
        cos_d.point((int(px), int(py)), fill=GOLD_LIGHT)

    # 3. Waist Heavy Plate Belt & Buckle hanging from y: 86 down to y: 92
    waist_spans = [(48, 55), (57, 63), (65, 71), (73, 80)]
    for x0, x1 in waist_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=IRON_BASE, outline=OUTLINE)
        cos_d.line([(x0 + 1, 88), (x1 - 1, 88)], fill=GOLD_BASE, width=1)
        cos_d.point((int(0.5 * (x0 + x1)), 90), fill=GOLD_LIGHT)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART26b enforcement: Zero pixels at y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_armadillo_amber_refractory_lens.png
    # Features:
    # - 琥珀耐熱石英目鏡 (Amber Refractory Quartz Optic Lens)
    # - Annealed convex quartz crystal lenses centered at (54, 42) and (74, 42)
    # - Brass retention bezels with vernier gear teeth
    # - Dopamine warm orange (#FFA010) & amber glow with concentric range reticles
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:
        # Outer Brass Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Amber Refractory Quartz)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r = int(np.clip(AMBER_BASE[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(AMBER_BASE[1] * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    b = int(np.clip(AMBER_BASE[2] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Concentric dial crosshair & focus highlight
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), AMBER_SHINE)
        core_img.putpixel((int(ex + 1), int(ey)), AMBER_LIGHT)
        core_img.putpixel((int(ex), int(ey - 1)), AMBER_LIGHT)
        core_img.putpixel((int(ex), int(ey + 1)), AMBER_DARK)

    # Vernier micro gear teeth on bezel
    c_d.point((49, 41), fill=GOLD_LIGHT)
    c_d.point((79, 41), fill=GOLD_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    # 0-ART27 verification: Ensure center pixels at (54, 42) and (74, 42) are completely opaque
    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_armadillo_black_iron_heavy_sword.png
    # Features:
    # - 玄鐵重破大劍 (Black Iron Heavy Greatsword)
    # - Quenched black iron forged blade standing upright at x: 84..90, y: 22..72
    # - Thick brass crossguard at y: 72..75, x: 78..96
    # - Two-handed hilt wrapped in fireproof grip tape at y: 76..88
    # - Spherical brass counterweight pommel at (87, 90)
    # - Glowing heat vent groove etched along blade center
    # - Complies strictly with review.md 0-MKT7 single-weapon standard
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Main Black Iron Blade (x: 84..90, y: 22..72)
    # Tapered tip at y: 18..24
    blade_poly = [
        (87, 18), (91, 24), (91, 72), (83, 72), (83, 24)
    ]
    wd.polygon(blade_poly, fill=IRON_DARK, outline=OUTLINE)

    # Blade bevel shading
    for y in range(24, 72):
        for x in range(84, 91):
            spec = max(0.0, 1.0 - abs(x - 87.0) / 3.5)
            shine = max(0.0, 1.0 - abs(x - 86.0) / 1.5)**2
            is_center_vent = (x == 87 and y >= 28 and y <= 68)
            if is_center_vent:
                # Orange thermal heat dissipation groove
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(IRON_BASE[0] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(IRON_BASE[1] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(IRON_BASE[2] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r, g, b, 255))

    # Blade cutting tip highlight
    wd.point((87, 19), fill=WHITE_SHINE)

    # 2. Thick Brass Crossguard at y: 72..75, x: 76..98
    wd.rectangle([76, 72, 98, 75], fill=GOLD_BASE, outline=OUTLINE)
    wd.line([(78, 73), (96, 73)], fill=GOLD_LIGHT, width=1)
    # Crossguard end caps
    wd.ellipse([75, 71, 79, 76], fill=GOLD_DARK, outline=OUTLINE)
    wd.ellipse([95, 71, 99, 76], fill=GOLD_DARK, outline=OUTLINE)

    # 3. Two-Handed Fireproof Grip Hilt (x: 85..89, y: 76..88)
    for y in range(76, 89):
        is_wrap = (y % 3 == 0)
        c = GOLD_BASE if is_wrap else (140, 94, 40, 255)
        for x in range(85, 90):
            weapon_img.putpixel((x, y), c)
    wd.rectangle([85, 76, 89, 88], outline=OUTLINE)

    # 4. Spherical Brass Counterweight Pommel at (87, 91)
    wd.ellipse([84, 89, 90, 95], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([85, 90, 89, 94], fill=GOLD_LIGHT)
    wd.point((87, 91), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_armadillo_crucible_four_leaf_key", key_img),
        ("back_curio", "curio_armadillo_segmented_cast_iron_carapace", curio_img),
        ("chassis", "chassis_armadillo_crucible_iron_default", chassis_img),
        ("head_unit", "head_armadillo_quenched_visor_cowl", head_img),
        ("costume", "costume_armadillo_foundry_anvil_cuirass", costume_img),
        ("optic_core", "face_armadillo_amber_refractory_lens", core_img),
        ("weapon", "weapon_armadillo_black_iron_heavy_sword", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{ARMADILLO_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{ARMADILLO_PD_DIR}/winding_key/key_armadillo_crucible_four_leaf_key.png",
                 f"{KEY_DIR}/key_armadillo_crucible_four_leaf_key.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{ARMADILLO_PD_DIR}/weapon/weapon_armadillo_black_iron_heavy_sword.png",
                 f"{WEAPON_DIR}/weapon_armadillo_black_iron_heavy_sword.png")

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

    proof_comp = f"{ARMADILLO_PD_DIR}/proof_paperdoll_armadillo_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{ARMADILLO_PD_DIR}/proof_paperdoll_armadillo_magenta.png"
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

    strip_path = f"{ARMADILLO_PD_DIR}/proof_armadillo_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/armadillo_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/armadillo_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/armadillo_idle.png
    p_idle_64 = f"{PLAYER_DIR}/armadillo_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/armadillo_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/armadillo_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/armadillo_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/armadillo_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/armadillo_idle_hd.png)
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

        showcase_out = f"{SHOWCASE_DIR}/armadillo_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL CRUCIBLE ARMADILLO CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
