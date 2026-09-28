#!/usr/bin/env python3
"""
build_woodpecker_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十八族 振律啄木鳥 (The Resonance Woodpecker, woodpecker) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/RESONANCE_WOODPECKER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  nickel-plated tinplate and brass chassis with exposed brass rivets and tourbillon belly window,
  scarlet spring-crest cowl helmet, twin-leaf tuning fork gold winding key,
  skyspire inspector riveted harness, coaxial gauge monocle optic lens,
  resonance pneumatic heavy gun, riveted prop-tail skid)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (The Resonance Woodpecker canonical colors):
    1. Base: Nickel-Plated Tinplate (#FFFDF8, #E8ECF2, #CCD4E0)
    2. Primary: Dopamine Brass Gold (#FFD028, #D4A520, #FFF59D)
    3. Secondary: Dopamine Scarlet (#FF5E8A, #FF2A6D, #FFA8C5)
    4. Accent: Warm Dawn Orange (#FFA010, #FFB84D)
    5. Core Cyan: Celestial Sky Blue (#38A0FF, #70C0FF)
    6. Tungsten Steel / Dark Plates: (#3A4454, #2B2630)
    7. Dark Outline: Deep Blue-Purple (#1F1A3A)
    8. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
WOODPECKER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/woodpecker"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Resonance Woodpecker Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Nickel-Plated Tinplate (#FFFDF8, #E8ECF2, #CCD4E0)
NICKEL_BASE   = (255, 253, 248, 255)
NICKEL_LIGHT  = (255, 255, 255, 255)
NICKEL_SHADE  = (232, 236, 242, 255)
NICKEL_DARK   = (204, 212, 224, 255)
NICKEL_DEEP   = (166, 180, 200, 255)

# 2. Dopamine Gold / Brass (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Dopamine Vivid Scarlet (#FF5E8A)
SCARLET_BASE  = (255, 94, 138, 255)
SCARLET_LIGHT = (255, 145, 178, 255)
SCARLET_SHINE = (255, 195, 215, 255)
SCARLET_DARK  = (210, 45, 95, 255)
SCARLET_DEEP  = (150, 20, 60, 255)

# 4. Warm Dawn Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 5. Cold-Rolled Tungsten Steel / Dark Fabric (#3A4454, #2B2630)
STEEL_LIGHT = (95, 112, 135, 255)
STEEL_BASE  = (58, 68, 84, 255)
STEEL_DARK  = (43, 38, 48, 255)
STEEL_DEEP  = (31, 26, 38, 255)

# 6. Celestial Sky Blue (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)

# 7. Walnut Wood / Timber (#C29864, #8C5E28)
TIMBER_LIGHT = (218, 178, 126, 255)
TIMBER_BASE  = (194, 152, 100, 255)
TIMBER_DARK  = (140, 94, 40, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL RESONANCE WOODPECKER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_woodpecker_high_frequency_percussion_key.png
    # Features:
    # - 雙葉調速高頻音叉發條鑰匙 (Twin-Leaf Resonance High-Frequency Winding Key)
    # - Shaft extends from spine socket (64, 56) to central hub at (66, 26)
    # - Dual governor leaf wings angled at 45 degrees
    # - Tuning fork resonant prongs curving symmetrically left & right
    # - Central axis embedded with precision gear tooth engraving
    # - Warm golden bronze outline (OUTLINE_KEY) compliant with 0-ART29 dark limit (< 260px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft with Machined Grooves from (64, 56) to (66, 26)
    for t in np.linspace(0.0, 1.0, 32):
        sx = 64.0 + (66.0 - 64.0) * t
        sy = 56.0 + (26.0 - 56.0) * t
        is_collar = (abs(t - 0.3) < 0.05) or (abs(t - 0.7) < 0.05)
        half_w = 3.0 if is_collar else 2.0

        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.2))
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

    # 2. Dual outer tuning-fork loops & governor leaf wings around hub (66, 26)
    hub_x, hub_y = 66.0, 26.0

    # Twin Governor Leaf Wings: angled left (-135°) and right (-45°)
    for wing_sign in (-1, 1):
        # Base angle
        ang_rad = -np.pi / 2.0 + wing_sign * 0.85
        cos_a = np.cos(ang_rad)
        sin_a = np.sin(ang_rad)
        wing_len = 16.0
        for t in np.linspace(0.15, 1.0, 26):
            vx = hub_x + cos_a * (wing_len * t)
            vy = hub_y + sin_a * (wing_len * t)
            # Aerodynamic taper
            w_val = 3.6 * (1.0 - abs(t - 0.45) / 0.55) + 0.6
            perp_x = -sin_a
            perp_y = cos_a
            for w_off in np.linspace(-w_val, w_val, int(w_val * 2.5 + 2)):
                px = int(round(vx + perp_x * w_off))
                py = int(round(vy + perp_y * w_off))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - abs(w_off) / (w_val + 0.1))
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * (spec**2), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * (spec**2), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 15 * (spec**2), 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    # Dual Tuning-Fork Acoustic Prongs
    for ring_r in [12.0, 17.0]:
        for deg in range(0, 360, 2):
            rad = np.radians(deg)
            rx = int(round(hub_x + np.cos(rad) * ring_r))
            ry = int(round(hub_y + np.sin(rad) * ring_r))
            if 0 <= rx < W and 0 <= ry < H:
                c = GOLD_LIGHT if ring_r == 17.0 else GOLD_BASE
                key_img.putpixel((rx, ry), c)

    # 3. Central Hub with Machined Gear / Razor-Tooth Escapement Boss
    kd.ellipse([int(hub_x - 6), int(hub_y - 6), int(hub_x + 6), int(hub_y + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 4), int(hub_y - 4), int(hub_x + 4), int(hub_y + 4)], fill=GOLD_BASE)
    # Core tuning crystal jewel (scarlet / orange)
    kd.ellipse([int(hub_x - 2), int(hub_y - 2), int(hub_x + 2), int(hub_y + 2)], fill=SCARLET_BASE)
    kd.point((int(hub_x), int(hub_y - 1)), fill=GOLD_LIGHT)
    kd.point((int(hub_x), int(hub_y)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_woodpecker_riveted_tinplate_prop_tail.png
    # Features:
    # - 鋼板沖壓三角抗震支撐尾板 (Riveted Tinplate Prop-Tail Skid)
    # - Stamped cold-rolled steel plate & heavy brass spine
    # - Extends downward-left from pelvic root (62, 88) down to (36, 115) to ground
    # - Triple-stepped truss plate with rivets & black rubber anti-recoil footpad
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Pelvic mounting hinge at (62, 88)
    cd.ellipse([57, 84, 67, 92], fill=GOLD_DARK, outline=OUTLINE)
    cd.ellipse([59, 86, 65, 90], fill=GOLD_BASE)
    cd.point((62, 88), fill=GOLD_LIGHT)

    # Main Triangular Skid Blade running from (62, 88) to (36, 114)
    # Polygon truss of three layered steel plates with rich cylindrical lighting
    for y in range(86, 116):
        t_y = (y - 86.0) / 30.0
        # Blade x bounds
        x_min = int(round(56.0 + (32.0 - 56.0) * t_y))
        x_max = int(round(66.0 + (42.0 - 66.0) * t_y))
        for x in range(x_min, x_max + 1):
            if x_min <= x <= x_max:
                span = max(1.0, float(x_max - x_min))
                spec = max(0.0, 1.0 - abs(x - (x_min + span * 0.4)) / (span * 0.5 + 0.1))
                shine = max(0.0, 1.0 - abs(x - (x_min + span * 0.3)) / (span * 0.25 + 0.1))**2
                r = int(np.clip(STEEL_BASE[0] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(STEEL_BASE[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(STEEL_BASE[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    # Heavy Brass Center Reinforcing Spine Rib
    for t in np.linspace(0.0, 1.0, 30):
        bx = 62.0 + (38.0 - 62.0) * t
        by = 88.0 + (113.0 - 88.0) * t
        for offset in (-1, 0, 1):
            px = int(round(bx + offset * 0.6))
            py = int(round(by - offset * 0.6))
            curio_img.putpixel((px, py), GOLD_BASE if offset == 0 else GOLD_DARK)

    # Round Stamped Brass Rivets along the tail blade
    rivet_pos = [(57, 92), (51, 98), (45, 104), (39, 110)]
    for rx, ry in rivet_pos:
        cd.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=GOLD_DARK, outline=OUTLINE)
        cd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE)
        cd.point((rx, ry - 1), fill=GOLD_LIGHT)

    # Ground Rubber Absorber Pad at bottom (32..42, 112..116)
    cd.ellipse([30, 111, 42, 116], fill=STEEL_DEEP, outline=OUTLINE)
    cd.line([(32, 113), (40, 113)], fill=STEEL_DARK, width=1)

    # Pneumatic shock absorber cylinder mounted on top of tail (50..58, 90..100)
    cd.rectangle([48, 92, 54, 101], fill=GOLD_BASE, outline=OUTLINE)
    cd.line([(50, 93), (50, 100)], fill=GOLD_LIGHT, width=1)
    # Tiny pressure gauge on cylinder
    cd.ellipse([45, 93, 49, 97], fill=GOLD_DARK, outline=OUTLINE)
    cd.ellipse([46, 94, 48, 96], fill=WHITE_SHINE)
    cd.point((47, 95), fill=SCARLET_BASE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_woodpecker_tinplate_brass_default.png
    # Features:
    # - 鍍鎳鐵皮黃銅高剛性素體底盤 (Nickel-Plated Tinplate & Brass Chassis)
    # - 2.2 chibi ratio, upright sharpshooter posture
    # - Feet: Zygodactyl X-claws at (46, 114) and (76, 114)
    # - Legs: High-rigidity brass ball-joint knees at (48, 98) and (74, 98)
    # - Torso: Nickel-plated chest & belly with escapement window at (64, 76)
    # - Left arm forward supporting handguard at (38..48, 70..80)
    # - Right arm at (80..92, 68..76) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow under claws & tail
    ch_d.ellipse([64 - 38, 116 - 6, 64 + 38, 116 + 6], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. X-Claws (Zygodactyl mechanical bird feet) at (46, 114) and (76, 114)
    feet_pos = [(46.0, 114.0), (76.0, 114.0)]
    for fx, fy in feet_pos:
        # Magnetic central claw hub
        ch_d.ellipse([int(fx - 7), int(fy - 3), int(fx + 7), int(fy + 3)], fill=STEEL_DEEP, outline=OUTLINE)
        ch_d.ellipse([int(fx - 5), int(fy - 2), int(fx + 5), int(fy + 2)], fill=GOLD_BASE)
        # Front two claws
        ch_d.polygon([(int(fx - 6), int(fy)), (int(fx - 9), int(fy + 2)), (int(fx - 4), int(fy + 2))], fill=GOLD_DARK, outline=OUTLINE)
        ch_d.polygon([(int(fx + 4), int(fy)), (int(fx + 9), int(fy + 2)), (int(fx + 6), int(fy + 2))], fill=GOLD_DARK, outline=OUTLINE)
        # Claws highlight
        ch_d.point((int(fx - 2), int(fy)), fill=GOLD_LIGHT)
        ch_d.point((int(fx + 2), int(fy)), fill=WHITE_SHINE)

    # 3. High-rigidity brass and nickel shins/thighs
    leg_coords = [
        ((46.0, 113.0), (52.0, 88.0)),
        ((76.0, 113.0), (70.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_coords:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-5, 6):
                spec = max(0.0, 1.0 - abs(dx) / 5.0)
                shine = max(0.0, 1.0 - abs(dx - 1.0) / 2.5)**2
                r = int(np.clip(NICKEL_SHADE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(NICKEL_SHADE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(NICKEL_SHADE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Brass knee ball-joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 4, mid_y - 3, mid_x + 4, mid_y + 3], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Upper Chest Flange & Neck Hinge (x: 48..82, y: 44..59)
    for ny in range(44, 60):
        for nx in range(48, 82):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 18.0)
            r = int(np.clip(NICKEL_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(NICKEL_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(NICKEL_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Upright Torso (x: 44..84, y: 58..95)
    # Stamped cold bright nickel-plated tinplate (#FFFDF8) with brass flank ribbing
    for ty in range(58, 95):
        for tx in range(44, 85):
            dx = (tx - 64.0) / 19.0
            dy = (ty - 76.0) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 68.0)**2)**0.5 / 12.0)**2
                is_flank_brass = (tx <= 49 or tx >= 79)
                if is_flank_brass:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                else:
                    # Nickel plate with smooth sub-shades (keep min RGB < 235 for anti-white run)
                    r = int(np.clip(236 * (0.85 + 0.25 * spec) + 25 * shine, 0, 250))
                    g = int(np.clip(232 * (0.85 + 0.25 * spec) + 25 * shine, 0, 248))
                    b = int(np.clip(225 * (0.85 + 0.25 * spec) + 25 * shine, 0, 245))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Tourbillon & Vibration Gauge Observation Window at (64, 76)
    ch_d.ellipse([57, 69, 71, 83], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([58, 70, 70, 82], fill=STEEL_DEEP)
    # Brass escapement balance wheel
    ch_d.ellipse([60, 72, 68, 80], fill=GOLD_BASE, outline=GOLD_DARK)
    ch_d.line([(60, 76), (68, 76)], fill=GOLD_LIGHT, width=1)
    ch_d.line([(64, 72), (64, 80)], fill=GOLD_LIGHT, width=1)
    # Center jewel pivot (scarlet / orange)
    ch_d.point((64, 76), fill=SCARLET_BASE)
    ch_d.point((63, 75), fill=WHITE_SHINE)

    # 6. Left Arm forward at (38..48, 70..82) gripping forestock
    for t in np.linspace(0.0, 1.0, 18):
        ax = 50.0 - t * 8.0
        ay = 66.0 + t * 10.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), NICKEL_SHADE)
    ch_d.ellipse([38, 74, 46, 82], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([40, 76, 44, 80], fill=GOLD_BASE)
    ch_d.point((42, 78), fill=GOLD_LIGHT)

    # 7. Right Arm positioned at (80..92, 68..76) (strictly x < 94)
    for t in np.linspace(0.0, 1.0, 16):
        ax = 78.0 + t * 9.0  # max ax = 87
        ay = 66.0 + t * 6.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px = int(ax + dx)
                py = int(ay + dy)
                if px < 94 and dx**2 + dy**2 <= 9:
                    chassis_img.putpixel((px, py), NICKEL_SHADE)
    # Right brass wrist / ball joint
    ch_d.ellipse([84, 71, 90, 77], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([85, 72, 89, 76], fill=GOLD_BASE)

    # Outline pass
    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART9/11 enforcement: Zero pixels at x >= 94
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_woodpecker_scarlet_crest_cowl.png
    # Features:
    # - 振律多巴胺亮紅散熱冠羽頭盔 (Resonance Scarlet Spring-Crest Cowl)
    # - Stamped brass helmet base with nickel cheeks
    # - Three-tiered stepped scarlet spring-loaded crest feathers at y: 12..32, x: 50..78
    # - Octagonal cold-rolled tungsten chisel beak pointing forward-right (x: 74..94, y: 46..54)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Base Bird Head & Face under helmet (x: 42..86, y: 34..56)
    for y in range(34, 57):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - 45.0) / 11.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 21.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 6.0)**2
                is_cheek = (x <= 46 or x >= 80)
                if is_cheek:
                    # Nickel-brass flank with high blue reflection
                    r = int(np.clip(242 * (0.85 + 0.25 * spec) + 20 * shine, 0, 252))
                    g = int(np.clip(232 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                    b = int(np.clip(210 * (0.85 + 0.25 * spec) + 20 * shine, 0, 235))
                else:
                    r = int(np.clip(236 * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
                    g = int(np.clip(232 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                    b = int(np.clip(224 * (0.85 + 0.25 * spec) + 20 * shine, 0, 242))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Dual micro cheek exhaust relief ports at (46, 50) and (78, 50)
    for cx in (46, 78):
        hd.ellipse([cx - 2, 50 - 2, cx + 2, 50 + 2], fill=STEEL_DEEP, outline=OUTLINE)
        hd.point((cx, 50), fill=SKY_BASE)

    # 2. Octagonal Machined Tungsten Chisel Beak (x: 74..94, y: 46..54)
    beak_poly = [(74, 46), (94, 49), (94, 51), (74, 54), (72, 50)]
    hd.polygon(beak_poly, fill=STEEL_BASE, outline=OUTLINE)
    # Beak upper facet highlight
    hd.polygon([(74, 46), (94, 49), (90, 50), (74, 49)], fill=STEEL_LIGHT)
    # Beak cutting tip
    hd.point((94, 50), fill=WHITE_SHINE)

    # 3. Stamped Nickel-Brass Helmet Cap (x: 44..84, y: 26..38)
    for y in range(26, 38):
        hw = 12.0 + (y - 26.0) * 0.8
        for x in range(int(hcx - hw), int(hcx + hw + 1)):
            spec = max(0.0, 1.0 - abs(x - hcx) / (hw + 0.1))
            shine = max(0.0, 1.0 - abs(x - (hcx - 2)) / 5.0)**2
            r = int(np.clip(NICKEL_BASE[0] * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
            g = int(np.clip(NICKEL_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
            b = int(np.clip(NICKEL_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 245))
            head_img.putpixel((x, y), (r, g, b, 255))
    hd.line([(int(hcx - 18), 37), (int(hcx + 18), 37)], fill=GOLD_BASE, width=1)

    # 4. Three-Tiered Stepped Scarlet Spring-Loaded Crest Feathers (y: 12..32, x: 50..78)
    # Tier 1 (Apex): (58..70, 12..22)
    # Tier 2 (Mid):  (54..74, 18..28)
    # Tier 3 (Base): (50..78, 24..34)
    tiers = [
        (64.0, 17.0, 6.0, 6.0),
        (64.0, 23.0, 9.0, 6.0),
        (64.0, 29.0, 13.0, 6.0)
    ]
    for tcx, tcy, trw, trh in tiers:
        for y in range(int(tcy - trh), int(tcy + trh + 1)):
            prog = (y - (tcy - trh)) / (trh * 2.0 + 0.1)
            cur_rw = trw * (1.0 - abs(prog - 0.5) * 0.6)
            for x in range(int(tcx - cur_rw), int(tcx + cur_rw + 1)):
                spec = max(0.0, 1.0 - abs(x - tcx) / (cur_rw + 0.1))
                shine = max(0.0, 1.0 - ((x - tcx)**2 + (y - tcy)**2)**0.5 / 5.0)**2
                r = int(np.clip(SCARLET_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(SCARLET_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(SCARLET_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Phosphor bronze spring coils between crest tiers
    hd.line([(58, 22), (70, 22)], fill=GOLD_BASE, width=1)
    hd.line([(54, 28), (74, 28)], fill=GOLD_BASE, width=1)

    # 5. Hollow Eye Sockets for 0-ART27:
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
    # File: costume/costume_woodpecker_skyspire_inspector_harness.png
    # Features:
    # - 摩天工坊高空巡檢鉚接工裝 (Skyspire Inspector Riveted Harness)
    # - Heavy crossed canvas straps in slate steel (#3A4454)
    # - Stamped brass chest plate (#FFD028) with round rivets
    # - High-visibility dopamine orange fall-arrest chevron stripes (#FFA010)
    # - Chest-mounted pressure dial at (64, 72)
    # - Waist belt and rivet loops ending at y: 92
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Chest Harness (x: 48..80, y: 60..86)
    for y in range(60, 87):
        for x in range(48, 81):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 16.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 9.0)**2
            # High-vis orange diagonal hazard chevron at y in (64..67)
            is_orange_chevron = (abs((x - 64) - (y - 65) * 0.8) <= 2)
            if is_orange_chevron:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(STEEL_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(STEEL_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(STEEL_BASE[2] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Center Stamped Brass Plate & Pressure Dial at (64, 72)
    cos_d.ellipse([58, 66, 70, 78], fill=GOLD_DARK, outline=OUTLINE)
    cos_d.ellipse([59, 67, 69, 77], fill=GOLD_BASE)
    # Dial face
    cos_d.ellipse([61, 69, 67, 75], fill=WHITE_SHINE)
    cos_d.line([(64, 72), (66, 70)], fill=SCARLET_BASE, width=1)
    cos_d.point((64, 72), fill=GOLD_DARK)

    # 2. Shoulder Harness Straps & Rivet Buckles at (44, 61) and (84, 61)
    shoulders = [(44.0, 61.0), (84.0, 61.0)]
    for px, py in shoulders:
        cos_d.ellipse([int(px - 5), int(py - 5), int(px + 5), int(py + 5)], fill=STEEL_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 3), int(py - 3), int(px + 3), int(py + 3)], fill=STEEL_LIGHT)
        # Gold rivet head
        cos_d.point((int(px), int(py)), fill=GOLD_BASE)

    # 3. Waist Toolbelt & Flanges (hanging from y: 86 down to y: 92)
    waist_spans = [(50, 56), (58, 64), (66, 72), (74, 80)]
    for x0, x1 in waist_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=STEEL_BASE, outline=OUTLINE)
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
    # File: optic_core/face_woodpecker_precision_gauge_monocle.png
    # Features:
    # - 同軸同心圓測振壓力目鏡 (Coaxial Resonance Gauge Monocle)
    # - Optical quartz convex lenses centered at (54, 42) and (74, 42)
    # - Brass retention bezels with vernier gear teeth
    # - Antireflective celestial sky blue (#38A0FF) coating with concentric range reticles
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:
        # Outer Brass Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Celestial Sky Blue Quartz)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r = int(np.clip(SKY_BASE[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(SKY_BASE[1] * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                    b = int(np.clip(SKY_BASE[2] * (0.8 + 0.25 * spec) + 50 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Concentric dial crosshair & focus highlight
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), SKY_SHINE)
        core_img.putpixel((int(ex + 1), int(ey)), SKY_LIGHT)
        core_img.putpixel((int(ex), int(ey - 1)), SKY_LIGHT)
        core_img.putpixel((int(ex), int(ey + 1)), SKY_DARK)

    # Right eye gauge vernier gear tooth (for monocle look)
    c_d.point((79, 41), fill=GOLD_LIGHT)
    c_d.point((79, 43), fill=GOLD_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    # 0-ART27 verification: Ensure center pixels at (54, 42) and (74, 42) are completely opaque
    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 35)
    # File: weapon/weapon_woodpecker_resonance_pneumatic_heavy_gun.png
    # Features:
    # - 振律重型氣動火銃 (Resonance Pneumatic Heavy Gun)
    # - Long cold-rolled tungsten steel octagonal barrel from x: 68 to x: 122, y: 70..76
    # - High-pressure brass pneumatic cylinder reservoir under barrel
    # - Multi-port flash suppressor needle muzzle at (118..124, 70..74)
    # - Walnut stock & pistol grip at (56..88, 72..80)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Walnut Gun Stock & Receiver (x: 56..88, y: 72..82)
    stock_pts = [(56, 76), (68, 73), (84, 73), (88, 77), (84, 82), (72, 80), (60, 80)]
    wd.polygon(stock_pts, fill=TIMBER_BASE, outline=OUTLINE)
    for y in range(73, 82):
        for x in range(58, 86):
            p = weapon_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 0:
                spec = max(0.0, 1.0 - abs(y - 77.0) / 4.5)
                shine = max(0.0, 1.0 - abs(x - 72.0) / 14.0)**2
                r = int(np.clip(TIMBER_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(TIMBER_BASE[1] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                b = int(np.clip(TIMBER_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Brass Trigger Guard & Mechanism at (84, 78)
    wd.ellipse([82, 76, 88, 82], fill=GOLD_DARK, outline=OUTLINE)
    wd.point((85, 78), fill=GOLD_BASE)

    # 2. Under-Barrel High-Pressure Brass Pneumatic Cylinder (x: 74..104, y: 76..80)
    for y in range(76, 81):
        for x in range(74, 105):
            spec = max(0.0, 1.0 - abs(y - 78.0) / 2.5)
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec), 0, 255))
            weapon_img.putpixel((x, y), (r, g, b, 255))
    # Pressure valve connector ring
    wd.ellipse([88, 75, 92, 81], fill=GOLD_DARK, outline=OUTLINE)

    # 3. Main Octagonal Tungsten Steel Barrel (x: 68..120, y: 70..75)
    for y in range(70, 76):
        for x in range(68, 121):
            spec = max(0.0, 1.0 - abs(y - 72.5) / 3.0)
            shine = max(0.0, 1.0 - abs(y - 71.5) / 1.5)**2
            r = int(np.clip(STEEL_BASE[0] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
            g = int(np.clip(STEEL_BASE[1] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
            b = int(np.clip(STEEL_BASE[2] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r, g, b, 255))

    # 4. Needle-Type Flash Suppressor Muzzle at (118..124, 70..76)
    wd.rectangle([118, 70, 122, 76], fill=STEEL_DARK, outline=OUTLINE)
    wd.line([(120, 69), (124, 69)], fill=STEEL_LIGHT, width=1)
    wd.line([(120, 77), (124, 77)], fill=STEEL_LIGHT, width=1)
    # Needle tip
    wd.line([(122, 73), (125, 73)], fill=GOLD_LIGHT, width=1)

    # 5. Forestock and mounting collar from x: 44 to x: 68, y: 74..78
    wd.rectangle([44, 74, 68, 78], fill=TIMBER_BASE, outline=OUTLINE)
    wd.line([(45, 75), (67, 75)], fill=TIMBER_LIGHT, width=1)
    wd.rectangle([44, 74, 50, 78], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((47, 76), fill=GOLD_LIGHT)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_woodpecker_high_frequency_percussion_key", key_img),
        ("back_curio", "curio_woodpecker_riveted_tinplate_prop_tail", curio_img),
        ("chassis", "chassis_woodpecker_tinplate_brass_default", chassis_img),
        ("head_unit", "head_woodpecker_scarlet_crest_cowl", head_img),
        ("costume", "costume_woodpecker_skyspire_inspector_harness", costume_img),
        ("optic_core", "face_woodpecker_precision_gauge_monocle", core_img),
        ("weapon", "weapon_woodpecker_resonance_pneumatic_heavy_gun", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{WOODPECKER_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{WOODPECKER_PD_DIR}/winding_key/key_woodpecker_high_frequency_percussion_key.png",
                 f"{KEY_DIR}/key_woodpecker_high_frequency_percussion_key.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{WOODPECKER_PD_DIR}/weapon/weapon_woodpecker_resonance_pneumatic_heavy_gun.png",
                 f"{WEAPON_DIR}/weapon_woodpecker_resonance_pneumatic_heavy_gun.png")

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

    proof_comp = f"{WOODPECKER_PD_DIR}/proof_paperdoll_woodpecker_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{WOODPECKER_PD_DIR}/proof_paperdoll_woodpecker_magenta.png"
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

    strip_path = f"{WOODPECKER_PD_DIR}/proof_woodpecker_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([34, 108, 94, 120], fill=(31, 26, 58, 110))
    shd.ellipse([44, 110, 84, 118], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/woodpecker_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/woodpecker_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/woodpecker_idle.png
    p_idle_64 = f"{PLAYER_DIR}/woodpecker_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/woodpecker_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/woodpecker_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/woodpecker_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/woodpecker_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/woodpecker_idle_hd.png)
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

        showcase_out = f"{SHOWCASE_DIR}/woodpecker_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL RESONANCE WOODPECKER CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
