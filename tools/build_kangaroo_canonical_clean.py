#!/usr/bin/env python3
"""
build_kangaroo_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十四族 鐵拳袋鼠 (The Boxer Kangaroo, kangaroo) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/BOXER_KANGAROO_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh/mucus/gills, stamped heavy caramel bronze plates,
  creamy ivory enamel cheek & pouch shell, prize fighter crimson knuckle armor, cold-rolled tungsten
  helical spring legs, 4-segment articulated brass balance tail with cast iron counterweight,
  championship double-ring brass winding key, dual steam exhaust backpack, pneumatic piston stamping knuckles)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette for The Boxer Kangaroo:
    Primary: Stamped Heavy Caramel Bronze (#C86D20)
    Secondary: Creamy Ivory White Enamel (#FFFDF8)
    Accent: Dopamine Golden Championship Brass Key & Cog Teeth (#FFD028)
    Detail: Amber Vacuum Gauge Dial Eyes & Heart Gem Core (#FF9F1C)
    Warm Highlight: Prize Fighter Crimson Knuckle Armor & Trim (#E63946)
    Secondary Hull: Warm Orange Steam Conduit Piping (#FFA010)
    Frame: Cold-Rolled Tungsten Helical Springs & Chassis Frame (#4A5568)
    Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_9a32151a/repo"
KANGAROO_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kangaroo"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Boxer Kangaroo Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary Hull: Stamped Heavy Caramel Bronze (#C86D20)
BRONZE_BASE  = (200, 109, 32, 255)
BRONZE_LIGHT = (235, 145, 65, 255)
BRONZE_SHINE = (255, 185, 115, 255)
BRONZE_DARK  = (150, 75, 18, 255)
BRONZE_DEEP  = (105, 48, 10, 255)

# Secondary Hull / Piping: Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 80, 255)
ORANGE_SHINE = (255, 230, 155, 255)
ORANGE_DARK  = (200, 115, 8, 255)
ORANGE_DEEP  = (140, 75, 5, 255)

# Secondary: Creamy Ivory White Enamel (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (230, 224, 215, 255)
IVORY_DARK    = (195, 188, 178, 255)

# Accent: Dopamine Golden Championship Brass Key & Gears (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# Detail: Amber Vacuum Gauge Dial Eyes & Clockwork Heart Core (#FF9F1C)
AMBER_BASE  = (255, 159, 28, 255)
AMBER_LIGHT = (255, 195, 85, 255)
AMBER_SHINE = (255, 240, 175, 255)
AMBER_DARK  = (195, 110, 12, 255)
AMBER_DEEP  = (130, 70, 8, 255)

# Warm Highlight: Prize Fighter Crimson Knuckle Armor (#E63946)
CRIMSON_BASE  = (230, 57, 70, 255)
CRIMSON_LIGHT = (255, 105, 115, 255)
CRIMSON_SHINE = (255, 165, 175, 255)
CRIMSON_DARK  = (175, 30, 45, 255)
CRIMSON_DEEP  = (120, 18, 28, 255)

# Cold-Rolled Tungsten Frame & Helical Springs (#4A5568)
TUNGSTEN_LIGHT = (115, 128, 148, 255)
TUNGSTEN_BASE  = (74, 85, 104, 255)
TUNGSTEN_DARK  = (45, 55, 72, 255)
TUNGSTEN_DEEP  = (28, 35, 48, 255)
TUNGSTEN_SHINE = (175, 188, 205, 255)

# Harness Leather Straps (#8E522D)
CANVAS_BASE  = (142, 82, 45, 255)
CANVAS_LIGHT = (180, 112, 68, 255)
CANVAS_DARK  = (96, 52, 26, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL BOXER KANGAROO SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_kangaroo_champion_double_ring.png
    # Championship Double-Ring Brass Winding Key (沖壓黃銅雙環冠軍發條鑰匙)
    # Features:
    # - Socket at upper-mid spine (63, 56)
    # - Polished brass shaft angling backwards/upwards to (80, 26)
    # - Symmetrical double-ring brass handles shaped like retro championship belt buckle
    # - Central hub with interlocking twin gear cogs relief
    # - Pure transparent corners (0-ART29 compliance)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (63, 56) to (80, 26)
    for t in np.linspace(0.0, 1.0, 45):
        sx = 63.0 + t * 17.0
        sy = 56.0 - t * 30.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (63, 56)
    kd.ellipse([59, 52, 67, 60], fill=GOLD_DARK, outline=OUTLINE)
    kd.ellipse([60, 53, 66, 59], fill=GOLD_BASE)
    kd.ellipse([62, 55, 64, 57], fill=ORANGE_BASE)

    # 2. Championship Double-Ring Hub at (80, 26)
    kcx, kcy = 80.0, 26.0

    # Draw Double Rings: Left Ring centered at (72, 22), Right Ring centered at (88, 22)
    # Outer rings
    for rcx, rcy in [(72.0, 22.0), (88.0, 22.0)]:
        r_outer = 8.5
        r_inner = 4.2
        for y in range(int(rcy - r_outer - 1), int(rcy + r_outer + 2)):
            for x in range(int(rcx - r_outer - 1), int(rcx + r_outer + 2)):
                dist = ((x - rcx)**2 + (y - rcy)**2)**0.5
                if r_inner <= dist <= r_outer:
                    # Metallic cylindrical highlight
                    angle = np.arctan2(y - rcy, x - rcx)
                    spec = max(0.0, np.cos(angle - 0.75 * np.pi))
                    r_r = int(np.clip(255 * (0.75 + 0.25 * spec), 0, 255))
                    g_r = int(np.clip(208 * (0.75 + 0.25 * spec), 0, 255))
                    b_r = int(np.clip(40 * (0.75 + 0.5 * spec) + 60 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_r, g_r, b_r, 255))

    # Center Hub Plate: Connecting the two rings at (80, 24)
    kd.rounded_rectangle([74, 18, 86, 30], radius=4, fill=GOLD_BASE, outline=GOLD_DARK)
    # Embossed interlocking cogs in center hub
    kd.ellipse([77, 21, 83, 27], fill=GOLD_LIGHT, outline=GOLD_DEEP)
    kd.ellipse([79, 23, 81, 25], fill=ORANGE_BASE)
    # White highlight dots on ring tops
    kd.point((72, 14), fill=WHITE_SHINE)
    kd.point((88, 14), fill=WHITE_SHINE)
    kd.point((80, 19), fill=WHITE_SHINE)

    apply_clean_outline(key_img)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_kangaroo_steam_exhaust_backpack.png
    # Twin Micro Steam Exhaust Backpack (雙聯微型高壓蒸氣散熱背包)
    # Features:
    # - Mounts on upper back / left shoulder (44..56, 50..66)
    # - Twin tilted brass smokestacks with relief valves
    # - Soft semi-transparent sweet steam puffs venting upwards into the air (32..46, 26..46)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Backpack Tank Body on back (44..54, 52..66)
    for y in range(54, 66):
        t_y = (y - 54) / 12.0
        w_tank = 5.0 + t_y * 1.5
        cx_tank = 49.0
        for x in range(int(cx_tank - w_tank), int(cx_tank + w_tank + 1)):
            dx = x - cx_tank
            spec = max(0.0, 1.0 - abs(dx) / w_tank)
            r_c = int(np.clip(200 * (0.8 + 0.25 * spec), 0, 255))
            g_c = int(np.clip(109 * (0.8 + 0.25 * spec), 0, 255))
            b_c = int(np.clip(32 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
            curio_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Pressure gauge dial on backpack tank (49, 60)
    cd.ellipse([46, 57, 52, 63], fill=IVORY_PRIMARY, outline=GOLD_DARK)
    cd.line([(49, 60), (51, 58)], fill=CRIMSON_BASE, width=1)  # needle

    # 2. Twin Tilted Smokestacks extending up-left
    # Stack 1: base at (46, 54), top at (40, 42)
    for t in np.linspace(0.0, 1.0, 25):
        px = 46.0 - t * 6.0
        py = 54.0 - t * 12.0
        for w in [-1.5, -0.5, 0.5, 1.5]:
            nx = px + w * 0.9
            ny = py - w * 0.4
            curio_img.putpixel((int(nx), int(ny)), GOLD_BASE)
    # Rim top stack 1
    cd.ellipse([38, 40, 42, 44], fill=GOLD_LIGHT, outline=GOLD_DEEP)

    # Stack 2: base at (52, 53), top at (47, 39)
    for t in np.linspace(0.0, 1.0, 25):
        px = 52.0 - t * 5.0
        py = 53.0 - t * 14.0
        for w in [-1.5, -0.5, 0.5, 1.5]:
            nx = px + w * 0.9
            ny = py - w * 0.4
            curio_img.putpixel((int(nx), int(ny)), BRONZE_LIGHT)
    # Rim top stack 2
    cd.ellipse([45, 37, 49, 41], fill=GOLD_LIGHT, outline=GOLD_DEEP)

    # 3. Soft Steam Puffs venting upwards
    steam_puffs = [
        (39, 36, 4.5, 160),
        (34, 30, 6.0, 140),
        (43, 28, 5.0, 120),
        (36, 20, 7.0, 90),
        (42, 16, 5.5, 70),
    ]
    for spx, spy, rad, alpha_base in steam_puffs:
        for y in range(int(spy - rad - 1), int(spy + rad + 2)):
            for x in range(int(spx - rad - 1), int(spx + rad + 2)):
                dist = ((x - spx)**2 + (y - spy)**2)**0.5
                if dist <= rad:
                    falloff = max(0.0, 1.0 - dist / rad)**1.5
                    alpha = int(alpha_base * falloff)
                    if alpha > 0:
                        cur_p = curio_img.getpixel((x, y))
                        new_r = int(np.clip(255 * 0.95, 0, 255))
                        new_g = int(np.clip(250 * 0.95, 0, 255))
                        new_b = int(np.clip(240 * 0.95, 0, 255))
                        if cur_p[3] == 0:
                            curio_img.putpixel((x, y), (new_r, new_g, new_b, alpha))
                        else:
                            # blend
                            blend_a = min(255, cur_p[3] + alpha)
                            curio_img.putpixel((x, y), (new_r, new_g, new_b, blend_a))

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Core Mechanical Body)
    # File: chassis/chassis_kangaroo_caramel_bronze_default.png
    # Features:
    # - 2.2 Head-to-body chibi pear-shaped boxer metal chassis
    # - Torso & pelvis with stamped heavy caramel bronze plates (#C86D20)
    # - Dual helical cold-rolled tungsten spring legs (#4A5568)
    # - Tungsten diamond-plate tread feet (接地軟陰影 y: 120, x: 64)
    # - 4-segment articulated brass counterweight pendulum tail to the left
    # - Left arm defensively guarding chest with clenched bronze fist
    # - Right arm raised forward in boxer stance (socket at x=88, y=72)
    # - STRICTLY 0 pixels in outer weapon zone (x:94..128) -> 0-ART9/0-ART11 compliant!
    # - Head neck/jaw structure with open eye cavities
    # - Soft ground contact shadow (48x16px ellipse at y=120)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft Ground Contact Shadow (centered at x=64, y=120, radius 26x8)
    shadow_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_img)
    shd.ellipse([38, 115, 90, 125], fill=(31, 26, 58, 110))
    # Tail contact shadow
    shd.ellipse([10, 116, 24, 122], fill=(31, 26, 58, 80))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(2.0))
    chassis_img.alpha_composite(shadow_img)

    # 2. 4-Segment Articulated Brass Counterweight Pendulum Tail
    # Origin: (48, 92) -> Segment 1: (38, 98) -> Segment 2: (28, 106) -> Segment 3: (20, 114) -> Segment 4 & Weight: (14, 116)
    tail_pts = [(48.0, 92.0), (38.0, 98.0), (28.0, 106.0), (20.0, 114.0), (14.0, 116.0)]
    for i in range(len(tail_pts) - 1):
        p0 = tail_pts[i]
        p1 = tail_pts[i+1]
        t_rad = 3.8 - i * 0.6
        for t in np.linspace(0.0, 1.0, 30):
            tx = p0[0] + t * (p1[0] - p0[0])
            ty = p0[1] + t * (p1[1] - p0[1])
            for d in np.linspace(-t_rad, t_rad, int(t_rad * 4 + 1)):
                # Normal vector
                dx = p1[0] - p0[0]
                dy = p1[1] - p0[1]
                length = (dx**2 + dy**2)**0.5
                nx = -dy / length
                ny = dx / length
                px = int(tx + d * nx)
                py = int(ty + d * ny)
                spec = max(0.0, 1.0 - abs(d) / t_rad)
                r_t = int(np.clip(255 * (0.75 + 0.25 * spec), 0, 255))
                g_t = int(np.clip(208 * (0.75 + 0.25 * spec), 0, 255))
                b_t = int(np.clip(40 * (0.75 + 0.4 * spec) + 40 * spec, 0, 255))
                chassis_img.putpixel((px, py), (r_t, g_t, b_t, 255))
        # Hinge joint rings
        chd.ellipse([int(p1[0] - 2), int(p1[1] - 2), int(p1[0] + 2), int(p1[1] + 2)], fill=GOLD_DARK)

    # Heavy Cylindrical Cast Iron Counterweight at Tail Tip (10..18, 112..118)
    for y in range(112, 119):
        for x in range(10, 19):
            dx = x - 14.5
            spec = max(0.0, 1.0 - abs(dx) / 4.5)
            r_w = int(np.clip(74 * (0.8 + 0.3 * spec), 0, 255))
            g_w = int(np.clip(85 * (0.8 + 0.3 * spec), 0, 255))
            b_w = int(np.clip(104 * (0.8 + 0.3 * spec), 0, 255))
            chassis_img.putpixel((x, y), (r_w, g_w, b_w, 255))
    chd.rectangle([10, 112, 18, 118], outline=OUTLINE)

    # 3. Feet: Tungsten Diamond-Plate Tread Feet
    # Left foot: (42..54, 116..120)
    for y in range(116, 121):
        for x in range(42, 55):
            spec = max(0.0, 1.0 - abs(x - 48) / 6.0)
            chassis_img.putpixel((x, y), (int(74 + 40 * spec), int(85 + 40 * spec), int(104 + 40 * spec), 255))
    # Right foot: (66..78, 116..120)
    for y in range(116, 121):
        for x in range(66, 79):
            spec = max(0.0, 1.0 - abs(x - 72) / 6.0)
            chassis_img.putpixel((x, y), (int(74 + 40 * spec), int(85 + 40 * spec), int(104 + 40 * spec), 255))

    # 4. Dual Helical Cold-Rolled Tungsten Spring Legs
    # Left leg spring: from (48, 96) down to (48, 116)
    # Right leg spring: from (72, 96) down to (72, 116)
    for leg_cx in [48.0, 72.0]:
        num_coils = 5
        for t in np.linspace(0.0, num_coils * 2.0 * np.pi, 200):
            progress = t / (num_coils * 2.0 * np.pi)
            sy = 96.0 + progress * 20.0
            sx = leg_cx + np.sin(t) * 4.5
            wire_r = 1.6
            for d in range(-1, 2):
                spec = max(0.0, np.cos(t))
                r_wire = int(np.clip(74 + 60 * spec, 0, 255))
                g_wire = int(np.clip(85 + 60 * spec, 0, 255))
                b_wire = int(np.clip(104 + 70 * spec, 0, 255))
                chassis_img.putpixel((int(sx + d), int(sy)), (r_wire, g_wire, b_wire, 255))
                chassis_img.putpixel((int(sx), int(sy + d)), (r_wire, g_wire, b_wire, 255))

    # 5. Pelvis & Lower Torso Chassis (48..78, 86..98)
    for y in range(86, 99):
        w_pelvis = 12.0 - abs(y - 92) * 0.7
        for x in range(int(63 - w_pelvis), int(63 + w_pelvis + 1)):
            dx = x - 63.0
            spec = max(0.0, 1.0 - abs(dx) / w_pelvis)
            r_p = int(np.clip(200 * (0.75 + 0.3 * spec), 0, 255))
            g_p = int(np.clip(109 * (0.75 + 0.3 * spec), 0, 255))
            b_p = int(np.clip(32 * (0.75 + 0.4 * spec) + 40 * spec, 0, 255))
            chassis_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    # 6. Upper Torso Chassis (50..78, 58..88)
    # Shaded caramel bronze with multi-tone depth (0-ART18 compliance)
    for y in range(58, 88):
        t_y = (y - 58) / 30.0
        # Pear shape: narrower at top (w ~ 9), wider at bottom (w ~ 14)
        w_torso = 9.0 + t_y * 5.0
        cx = 63.0
        for x in range(int(cx - w_torso), int(cx + w_torso + 1)):
            dx = x - cx
            dist_norm = abs(dx) / w_torso
            # Multi-tone surface with highlight on upper left
            spec = max(0.0, 1.0 - ((dx + 3.0)**2 + (y - 68.0)**2)**0.5 / 14.0)
            r_b = int(np.clip(200 * (0.7 + 0.35 * spec) + 55 * (spec**2), 0, 255))
            g_b = int(np.clip(109 * (0.7 + 0.35 * spec) + 45 * (spec**2), 0, 255))
            b_b = int(np.clip(32 * (0.7 + 0.4 * spec) + 30 * spec, 0, 255))
            chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Exposed brass bolts along torso side seams
    for by in [64, 72, 80]:
        chd.ellipse([52, by - 1, 54, by + 1], fill=GOLD_LIGHT)
        chd.ellipse([72, by - 1, 74, by + 1], fill=GOLD_LIGHT)

    # 7. Head Base Structure & Neck (y: 34..58, x: 50..76)
    # Neck column
    for y in range(54, 59):
        for x in range(58, 69):
            chassis_img.putpixel((x, y), TUNGSTEN_BASE)

    # Cranial bronze base (y: 34..56, x: 50..76)
    for y in range(34, 56):
        t_h = (y - 34) / 22.0
        w_head = 10.0 + np.sin(t_h * np.pi) * 3.0
        cx = 63.0
        for x in range(int(cx - w_head), int(cx + w_head + 1)):
            dx = x - cx
            spec = max(0.0, 1.0 - ((dx + 2.0)**2 + (y - 42.0)**2)**0.5 / 11.0)
            r_h = int(np.clip(200 * (0.75 + 0.3 * spec) + 45 * (spec**2), 0, 255))
            g_h = int(np.clip(109 * (0.75 + 0.3 * spec) + 35 * (spec**2), 0, 255))
            b_h = int(np.clip(32 * (0.75 + 0.4 * spec) + 25 * spec, 0, 255))
            chassis_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Open Eye Cavities on chassis (so eyes are not baked into chassis)
    # Left eye cavity at (55, 42), Right eye cavity at (69, 42)
    for y in range(38, 47):
        for x in range(51, 60):
            if ((x - 55)**2 + (y - 42)**2) <= 16:
                chassis_img.putpixel((x, y), TUNGSTEN_DEEP)
    for y in range(38, 47):
        for x in range(65, 74):
            if ((x - 69)**2 + (y - 42)**2) <= 16:
                chassis_img.putpixel((x, y), TUNGSTEN_DEEP)

    # 8. Left Arm (Defensive Guarding Stance)
    # Shoulder at (54, 62) -> Elbow at (40, 74) -> Clenched Fist at (50, 72)
    # Upper arm
    for t in np.linspace(0.0, 1.0, 25):
        ax = 54.0 - t * 14.0
        ay = 62.0 + t * 12.0
        for w in [-2, -1, 0, 1, 2]:
            chassis_img.putpixel((int(ax + w*0.7), int(ay + w*0.7)), BRONZE_BASE)
    # Forearm to clenched fist
    for t in np.linspace(0.0, 1.0, 25):
        ax = 40.0 + t * 10.0
        ay = 74.0 - t * 2.0
        for w in [-2, -1, 0, 1, 2]:
            chassis_img.putpixel((int(ax + w*0.2), int(ay + w)), BRONZE_LIGHT)
    # Clenched left boxing fist
    chd.rounded_rectangle([47, 68, 54, 76], radius=3, fill=BRONZE_LIGHT, outline=OUTLINE)
    chd.line([(49, 71), (52, 71)], fill=GOLD_BASE, width=1)

    # 9. Right Arm (Forward Boxer Stance)
    # Shoulder at (72, 62) -> Elbow at (80, 68) -> Wrist Socket at (88, 72)
    for t in np.linspace(0.0, 1.0, 25):
        ax = 72.0 + t * 8.0
        ay = 62.0 + t * 6.0
        for w in [-2, -1, 0, 1, 2]:
            chassis_img.putpixel((int(ax + w*0.6), int(ay + w*0.8)), BRONZE_BASE)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 80.0 + t * 8.0
        ay = 68.0 + t * 4.0
        for w in [-2, -1, 0, 1, 2]:
            chassis_img.putpixel((int(ax + w*0.4), int(ay + w)), BRONZE_LIGHT)
    # Clean wrist coupling socket (stops at x=89, y=72)
    chd.ellipse([86, 69, 90, 75], fill=TUNGSTEN_BASE, outline=OUTLINE)
    # STRICT ASSERTION: ensure NO chassis pixels beyond x=92
    for y in range(H):
        for x in range(93, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Cranial Armor & Long Ears)
    # File: head_unit/head_kangaroo_steampunk_boxer_visor.png
    # Features:
    # - Boxer Visor Helmet with heavy tungsten guard plate (#4A5568 / #FFD028)
    # - Twin tall streamlined brass ears with steam vents on outer curve
    #   - Left ear: base (50, 32) -> apex (42, 10)
    #   - Right ear: base (68, 32) -> apex (76, 8)
    # - Creamy ivory enamel cheekplates (#FFFDF8) and snout
    # - Rounded nose with brass rivet button at (72, 48)
    # - 100% HOLLOW eye sockets centered at (55, 42) and (69, 42) with alpha = 0 (0-ART27 compliance)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Twin Tall Streamlined Brass Ears
    # Left Ear: base at (50, 33), apex at (42, 10)
    for t in np.linspace(0.0, 1.0, 60):
        ex = 50.0 - t * 8.0
        ey = 33.0 - t * 23.0
        # Ear width: narrow at base, wider in middle (w ~ 4.5), pointed at apex
        w_ear = np.sin(t * np.pi) * 4.2 + (1.0 - t) * 1.5
        for d in np.linspace(-w_ear, w_ear, int(w_ear * 4 + 1)):
            px = int(ex + d)
            py = int(ey)
            spec = max(0.0, 1.0 - abs(d) / (w_ear + 0.1))
            if d < 0:
                # Inner ear cavity (warm orange shading)
                r_e = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))
                g_e = int(np.clip(160 * (0.8 + 0.2 * spec), 0, 255))
                b_e = int(np.clip(16 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
            else:
                # Outer ear shell (caramel bronze / brass)
                r_e = int(np.clip(200 * (0.75 + 0.3 * spec), 0, 255))
                g_e = int(np.clip(109 * (0.75 + 0.3 * spec), 0, 255))
                b_e = int(np.clip(32 * (0.75 + 0.4 * spec), 0, 255))
            head_img.putpixel((px, py), (r_e, g_e, b_e, 255))
    # Steam vent slits on left ear outer edge
    for vy in [18, 22, 26]:
        hd.line([(int(47 - (33 - vy)*0.3), vy), (int(49 - (33 - vy)*0.3), vy)], fill=GOLD_LIGHT, width=1)

    # Right Ear: base at (68, 33), apex at (76, 8)
    for t in np.linspace(0.0, 1.0, 60):
        ex = 68.0 + t * 8.0
        ey = 33.0 - t * 25.0
        w_ear = np.sin(t * np.pi) * 4.2 + (1.0 - t) * 1.5
        for d in np.linspace(-w_ear, w_ear, int(w_ear * 4 + 1)):
            px = int(ex + d)
            py = int(ey)
            spec = max(0.0, 1.0 - abs(d) / (w_ear + 0.1))
            if d > 0:
                # Outer ear shell
                r_e = int(np.clip(200 * (0.75 + 0.3 * spec), 0, 255))
                g_e = int(np.clip(109 * (0.75 + 0.3 * spec), 0, 255))
                b_e = int(np.clip(32 * (0.75 + 0.4 * spec), 0, 255))
            else:
                # Inner ear cavity
                r_e = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))
                g_e = int(np.clip(160 * (0.8 + 0.2 * spec), 0, 255))
                b_e = int(np.clip(16 * (0.8 + 0.4 * spec) + 30 * spec, 0, 255))
            head_img.putpixel((px, py), (r_e, g_e, b_e, 255))
    # Steam vent slits on right ear outer edge
    for vy in [16, 20, 24]:
        hd.line([(int(72 + (33 - vy)*0.3), vy), (int(74 + (33 - vy)*0.3), vy)], fill=GOLD_LIGHT, width=1)

    # 2. Boxer Visor Cranial Helmet (y: 30..42, x: 48..78)
    for y in range(30, 40):
        w_helm = 11.5 - abs(y - 35) * 0.4
        for x in range(int(63 - w_helm), int(63 + w_helm + 1)):
            dx = x - 63.0
            spec = max(0.0, 1.0 - abs(dx) / w_helm)
            head_img.putpixel((x, y), (int(255 * (0.75 + 0.25 * spec)), int(208 * (0.75 + 0.25 * spec)), int(40 * (0.75 + 0.5 * spec) + 40 * spec), 255))

    # Brow Band: Tungsten Guard Plate across forehead (y: 34..38, x: 49..77)
    for y in range(34, 38):
        for x in range(50, 77):
            dx = x - 63.0
            spec = max(0.0, 1.0 - abs(dx) / 13.0)
            head_img.putpixel((x, y), (int(74 + 50 * spec), int(85 + 50 * spec), int(104 + 60 * spec), 255))
    # Rivet studs on brow band
    for rx in [53, 63, 73]:
        hd.ellipse([rx - 1, 35, rx + 1, 37], fill=GOLD_LIGHT, outline=GOLD_DEEP)

    # 3. Creamy Ivory Enamel Cheekplates & Snout (y: 44..55, x: 50..75)
    for y in range(44, 56):
        t_c = (y - 44) / 12.0
        w_cheek = 11.0 - t_c * 2.5
        for x in range(int(63 - w_cheek), int(63 + w_cheek + 1)):
            dx = x - 63.0
            spec = max(0.0, 1.0 - abs(dx) / (w_cheek + 0.1))
            r_iv = int(np.clip(255 * (0.92 + 0.08 * spec), 0, 255))
            g_iv = int(np.clip(253 * (0.92 + 0.08 * spec), 0, 255))
            b_iv = int(np.clip(248 * (0.92 + 0.08 * spec), 0, 255))
            head_img.putpixel((x, y), (r_iv, g_iv, b_iv, 255))

    # Snout Nose Rivet Button at (71, 48)
    hd.ellipse([69, 46, 73, 50], fill=GOLD_LIGHT, outline=OUTLINE)
    hd.point((70, 47), fill=WHITE_SHINE)

    # Cheekplate fixing bolts
    hd.ellipse([51, 49, 53, 51], fill=GOLD_BASE)
    hd.ellipse([73, 49, 75, 51], fill=GOLD_BASE)

    # 4. HOLLOW EYE SOCKETS (0-ART27 Compliance!)
    # Clear eye sockets centered at (55, 42) and (69, 42) to alpha = 0
    for y in range(37, 48):
        for x in range(50, 61):
            if ((x - 55.0)**2 + (y - 42.0)**2) <= 20.0:
                head_img.putpixel((x, y), (0, 0, 0, 0))
    for y in range(37, 48):
        for x in range(64, 75):
            if ((x - 69.0)**2 + (y - 42.0)**2) <= 20.0:
                head_img.putpixel((x, y), (0, 0, 0, 0))

    # Rim edges around eye sockets in brass
    for angle in np.linspace(0, 2 * np.pi, 24):
        bx = int(55.0 + np.cos(angle) * 4.8)
        by = int(42.0 + np.sin(angle) * 4.8)
        if head_img.getpixel((bx, by))[3] > 0:
            head_img.putpixel((bx, by), GOLD_DARK)
        bx2 = int(69.0 + np.cos(angle) * 4.8)
        by2 = int(42.0 + np.sin(angle) * 4.8)
        if head_img.getpixel((bx2, by2))[3] > 0:
            head_img.putpixel((bx2, by2), GOLD_DARK)

    apply_clean_outline(head_img)

    # Re-verify eye sockets are 100% hollow after outline pass
    for cy, cx in [(42, 55), (41, 55), (43, 55), (42, 54), (42, 56),
                   (42, 69), (41, 69), (43, 69), (42, 68), (42, 70)]:
        head_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Harness & Stamped Gear Pouch)
    # File: costume/costume_kangaroo_champion_belt_harness.png
    # Features:
    # - Cog City artisan prize fighter reinforced harness & stamped front pouch
    # - Semi-circular creamy ivory enamel stamped gear pouch (#FFFDF8) on belly (x: 52..74, y: 70..90)
    # - Polished golden brass clasp & cog teeth emblem at pouch top
    # - Chestnut harness leather straps with prize fighter crimson edging (#E63946)
    # - Micro steam pressure gauge at chest (54, 64)
    # - Gem aperture hole of 14px centered at (63, 67) so optic_core heart shines through
    # - Fully decoupled (0-ART26b compliance: no lower legs/tail baked in!)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Leather Harness Straps crossing shoulders and chest
    # Shoulder strap left: (54, 58) to (63, 76)
    for t in np.linspace(0.0, 1.0, 30):
        sx = 54.0 + t * 9.0
        sy = 58.0 + t * 18.0
        for w in [-1.5, -0.5, 0.5, 1.5]:
            costume_img.putpixel((int(sx + w*0.8), int(sy - w*0.4)), CANVAS_BASE)
            # Crimson edge
            if abs(w) > 1.0:
                costume_img.putpixel((int(sx + w*0.8), int(sy - w*0.4)), CRIMSON_BASE)

    # Shoulder strap right: (72, 58) to (63, 76)
    for t in np.linspace(0.0, 1.0, 30):
        sx = 72.0 - t * 9.0
        sy = 58.0 + t * 18.0
        for w in [-1.5, -0.5, 0.5, 1.5]:
            costume_img.putpixel((int(sx + w*0.8), int(sy + w*0.4)), CANVAS_BASE)
            if abs(w) > 1.0:
                costume_img.putpixel((int(sx + w*0.8), int(sy + w*0.4)), CRIMSON_BASE)

    # Waist Belt Band (52..74, 88..92)
    for y in range(88, 93):
        for x in range(52, 75):
            costume_img.putpixel((x, y), CANVAS_DARK)
            if y in [88, 92]:
                costume_img.putpixel((x, y), CRIMSON_BASE)

    # 2. Semi-Circular Creamy Ivory Enamel Gear Pouch (x: 52..74, y: 70..89)
    pcx, pcy = 63.0, 72.0
    for y in range(71, 90):
        # Pouch drops down from top rim
        dy = y - 71.0
        w_pouch = np.sin((dy / 19.0) * np.pi * 0.75 + 0.25) * 10.5
        for x in range(int(pcx - w_pouch), int(pcx + w_pouch + 1)):
            dx = x - pcx
            spec = max(0.0, 1.0 - abs(dx) / (w_pouch + 0.1))
            shade_y = max(0.0, (y - 71.0) / 19.0)
            r_iv = int(np.clip(255 * (0.95 - 0.1 * shade_y + 0.1 * spec), 0, 255))
            g_iv = int(np.clip(253 * (0.95 - 0.1 * shade_y + 0.1 * spec), 0, 255))
            b_iv = int(np.clip(248 * (0.95 - 0.12 * shade_y + 0.1 * spec), 0, 255))
            costume_img.putpixel((x, y), (r_iv, g_iv, b_iv, 255))

    # Golden Pouch Rim & Clasp (x: 52..74, y: 70..72)
    for x in range(53, 74):
        costume_img.putpixel((x, 71), GOLD_BASE)
        costume_img.putpixel((x, 72), GOLD_DARK)
    # Stamped Cog Clasp in center (61..65, 70..74)
    cosd.ellipse([60, 70, 66, 75], fill=GOLD_LIGHT, outline=GOLD_DEEP)
    cosd.ellipse([62, 72, 64, 74], fill=ORANGE_BASE)

    # Miniature Brass Oil Can / Pin tucked in pouch corner (54, 73..78)
    cosd.rectangle([53, 73, 56, 78], fill=GOLD_BASE, outline=GOLD_DEEP)

    # 3. Micro Steam Pressure Gauge on Left Chest (54, 63)
    cosd.ellipse([51, 60, 57, 66], fill=IVORY_PRIMARY, outline=GOLD_DARK)
    cosd.line([(54, 63), (56, 61)], fill=CRIMSON_BASE, width=1)

    # 4. GEM APERTURE HOLE (14px diameter) centered at (63, 67)
    for y in range(60, 75):
        for x in range(56, 71):
            if ((x - 63.0)**2 + (y - 67.0)**2) <= 49.0:  # radius 7px -> diameter 14px
                costume_img.putpixel((x, y), (0, 0, 0, 0))

    # Brass Bezel Ring around the gem aperture hole
    for angle in np.linspace(0, 2 * np.pi, 36):
        gx = int(63.0 + np.cos(angle) * 7.5)
        gy = int(67.0 + np.sin(angle) * 7.5)
        if 0 <= gx < W and 0 <= gy < H and costume_img.getpixel((gx, gy))[3] > 0:
            costume_img.putpixel((gx, gy), GOLD_BASE)

    apply_clean_outline(costume_img)

    # Re-verify gem aperture is hollow
    for y in range(62, 73):
        for x in range(58, 69):
            if ((x - 63.0)**2 + (y - 67.0)**2) <= 36.0:
                costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30, Dial Eyes & Heart Core)
    # File: optic_core/optic_kangaroo_amber_dial_core.png
    # Features:
    # - Eye Lenses: Twin 8px amber vacuum gauge dial optical lenses (#FF9F1C)
    #   - Left eye center at (55, 42)
    #   - Right eye center at (69, 42)
    #   - Concentric dial tick ring & crosshair calibration markings
    #   - Brilliant white specular glint in top-left
    # - Clockwork Heart Core:
    #   - Centered at (63, 67), diamond-faceted amber crystal (#FF9F1C / #FFD028)
    #   - High-specular glint at apex, copper radiator ring
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crd = ImageDraw.Draw(core_img)

    # 1. Twin Amber Vacuum Gauge Dial Eyes
    for ecx, ecy in [(55.0, 42.0), (69.0, 42.0)]:
        r_eye = 4.2
        for y in range(int(ecy - r_eye - 1), int(ecy + r_eye + 2)):
            for x in range(int(ecx - r_eye - 1), int(ecx + r_eye + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_eye:
                    spec = max(0.0, 1.0 - dist / r_eye)
                    # Amber glass gradient
                    r_a = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_a = int(np.clip(159 * (0.8 + 0.25 * spec), 0, 255))
                    b_a = int(np.clip(28 * (0.8 + 0.4 * spec) + 50 * spec, 0, 255))
                    core_img.putpixel((x, y), (r_a, g_a, b_a, 255))

        # Dial markings: concentric tick ring
        crd.ellipse([int(ecx - 3), int(ecy - 3), int(ecx + 3), int(ecy + 3)], outline=AMBER_DARK, width=1)
        # Crosshair ticks
        crd.point((int(ecx), int(ecy - 3)), fill=AMBER_DEEP)
        crd.point((int(ecx), int(ecy + 3)), fill=AMBER_DEEP)
        crd.point((int(ecx - 3), int(ecy)), fill=AMBER_DEEP)
        crd.point((int(ecx + 3), int(ecy)), fill=AMBER_DEEP)
        # Center calibration needle pivot
        crd.point((int(ecx), int(ecy)), fill=AMBER_DEEP)
        # Brilliant specular glint in top-left
        crd.point((int(ecx - 1), int(ecy - 1)), fill=WHITE_SHINE)
        crd.point((int(ecx - 2), int(ecy - 1)), fill=WHITE_SHINE)

    # 2. Clockwork Heart Diamond Core at (63, 67)
    hcx, hcy = 63.0, 67.0
    r_gem = 5.2
    for y in range(int(hcy - r_gem - 2), int(hcy + r_gem + 3)):
        for x in range(int(hcx - r_gem - 2), int(hcx + r_gem + 3)):
            manhattan = abs(x - hcx) + abs(y - hcy)
            if manhattan <= r_gem:
                dx = x - hcx
                dy = y - hcy
                if dx <= 0 and dy <= 0:
                    # Top-left facet: high specular shine
                    spec = 1.0
                    r_k, g_k, b_k = 255, 250, 185
                elif dx > 0 and dy <= 0:
                    # Top-right facet: bright gold
                    spec = 0.8
                    r_k, g_k, b_k = 255, 208, 40
                elif dx <= 0 and dy > 0:
                    # Bottom-left facet: warm amber
                    spec = 0.6
                    r_k, g_k, b_k = 255, 159, 28
                else:
                    # Bottom-right facet: deep shade
                    spec = 0.4
                    r_k, g_k, b_k = 195, 110, 12
                core_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Copper radiator collar around diamond
    crd.ellipse([int(hcx - 6), int(hcy - 6), int(hcx + 6), int(hcy + 6)], outline=BRONZE_LIGHT, width=1)
    # Apex white glint
    crd.point((int(hcx - 1), int(hcy - 1)), fill=WHITE_SHINE)
    crd.point((int(hcx), int(hcy - 1)), fill=WHITE_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Forefront Single-Held Knuckle)
    # File: weapon/weapon_kangaroo_piston_brass_knuckle.png
    # Features:
    # - Pneumatic Piston Brass Stamping Knuckle (氣壓活塞衝壓黃銅拳套)
    # - Right hand single-held heavy boxing weapon (0-MKT7 compliant: 1 weapon only!)
    # - Mounts on right fist from (82, 62) to (114, 84)
    # - Prize fighter crimson stamped steel shell (#E63946)
    # - Twin sliding cold-rolled tungsten punch pistons (#4A5568 / TUNGSTEN_LIGHT) protruding from fist
    # - Miniature brass air pressure reservoir cylinder and steam exhaust pipe along wrist
    # - Polished brass knuckle plates and high-impact rivet studs (#FFD028)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Wrist Air Reservoir Cylinder & Steam Pipe (82..94, 62..70)
    for y in range(63, 71):
        for x in range(83, 95):
            dy = y - 67.0
            spec = max(0.0, 1.0 - abs(dy) / 4.0)
            r_w = int(np.clip(255 * (0.75 + 0.25 * spec), 0, 255))
            g_w = int(np.clip(208 * (0.75 + 0.25 * spec), 0, 255))
            b_w = int(np.clip(40 * (0.75 + 0.5 * spec) + 50 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_w, g_w, b_w, 255))
    # Brass cylinder bands
    wd.line([(86, 63), (86, 70)], fill=GOLD_DEEP, width=1)
    wd.line([(92, 63), (92, 70)], fill=GOLD_DEEP, width=1)

    # 2. Main Boxing Knuckle Casing in Prize Fighter Crimson (#E63946) (x: 88..106, y: 64..84)
    kcx, kcy = 96.0, 74.0
    for y in range(64, 85):
        w_knuckle = 8.5 - abs(y - 74) * 0.4
        for x in range(int(kcx - w_knuckle), int(kcx + w_knuckle + 1)):
            dx = x - kcx
            spec = max(0.0, 1.0 - ((dx + 2.0)**2 + (y - 72.0)**2)**0.5 / 10.0)
            r_k = int(np.clip(230 * (0.75 + 0.3 * spec) + 50 * (spec**2), 0, 255))
            g_k = int(np.clip(57 * (0.75 + 0.3 * spec) + 40 * (spec**2), 0, 255))
            b_k = int(np.clip(70 * (0.75 + 0.3 * spec) + 40 * (spec**2), 0, 255))
            weapon_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # 3. Polished Brass Stamping Knuckle Guard & Rivet Studs (x: 98..105, y: 66..82)
    for y in range(66, 83):
        for x in range(99, 106):
            dx = x - 102.5
            spec = max(0.0, 1.0 - abs(dx) / 3.5)
            weapon_img.putpixel((x, y), (int(255 * (0.8 + 0.2 * spec)), int(208 * (0.8 + 0.2 * spec)), int(40 * (0.8 + 0.5 * spec) + 50 * spec), 255))
    # 4 Brass Knuckle Rivet Studs
    for ry in [68, 72, 76, 80]:
        wd.ellipse([102, ry - 1, 105, ry + 1], fill=WHITE_SHINE, outline=GOLD_DEEP)

    # 4. Twin Sliding Cold-Rolled Tungsten Punch Pistons protruding from front (x: 104..114)
    # Upper Piston: y: 69..73
    for y in range(69, 74):
        for x in range(104, 114):
            dy = y - 71.0
            spec = max(0.0, 1.0 - abs(dy) / 2.5)
            weapon_img.putpixel((x, y), (int(74 + 70 * spec), int(85 + 70 * spec), int(104 + 80 * spec), 255))
    wd.rectangle([112, 69, 114, 73], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    wd.point((113, 70), fill=WHITE_SHINE)

    # Lower Piston: y: 76..80
    for y in range(76, 81):
        for x in range(104, 114):
            dy = y - 78.0
            spec = max(0.0, 1.0 - abs(dy) / 2.5)
            weapon_img.putpixel((x, y), (int(74 + 70 * spec), int(85 + 70 * spec), int(104 + 80 * spec), 255))
    wd.rectangle([112, 76, 114, 80], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    wd.point((113, 77), fill=WHITE_SHINE)

    # Steam Exhaust Vent on bottom of knuckle
    wd.line([(92, 82), (96, 85)], fill=ORANGE_BASE, width=2)
    wd.point((96, 85), fill=GOLD_LIGHT)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ASSETS (128x128 and 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_kangaroo_champion_double_ring", key_img),
        ("back_curio", "curio_kangaroo_steam_exhaust_backpack", curio_img),
        ("chassis", "chassis_kangaroo_caramel_bronze_default", chassis_img),
        ("head_unit", "head_kangaroo_steampunk_boxer_visor", head_img),
        ("optic_core", "optic_kangaroo_amber_dial_core", core_img),
        ("costume", "costume_kangaroo_champion_belt_harness", costume_img),
        ("weapon", "weapon_kangaroo_piston_brass_knuckle", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{KANGAROO_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)

        # 128x128
        dst_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(dst_128)

        # 512x512 LANCZOS
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{slot_dir}/{item_id}_512.png"
        img_512.save(dst_512)
        print(f"  ✓ Saved {slot}: {item_id}.png (128x128 & 512x512 LANCZOS)")

    # Universal Key & Weapon copies
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_kangaroo_champion_double_ring.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_kangaroo_piston_brass_knuckle.png")
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
    comp_exact = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_img in [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]:
        comp_exact.alpha_composite(s_img)

    comp_path = f"{KANGAROO_PD_DIR}/proof_paperdoll_kangaroo_composite.png"
    comp_exact.save(comp_path)
    print("  ✓ Composite saved:", comp_path)

    # Magenta proof (proof_paperdoll_kangaroo_magenta.png)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(comp_exact)
    mag_path = f"{KANGAROO_PD_DIR}/proof_paperdoll_kangaroo_magenta.png"
    magenta_bg.save(mag_path)
    print("  ✓ Magenta proof saved:", mag_path)

    # 7 slices proof (proof_kangaroo_all_7_slices.png)
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
        ("COMPOSITE", comp_exact)
    ]
    for idx, (lbl, s_im) in enumerate(slice_list):
        px = idx * W
        strip.alpha_composite(s_im, (px, 0))

    strip_path = f"{KANGAROO_PD_DIR}/proof_kangaroo_all_7_slices.png"
    strip.save(strip_path)
    print("  ✓ 7 Slices Proof saved:", strip_path)

    # SHOWCASE HD (game/assets/sprites/player/showcase/kangaroo_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/kangaroo_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
