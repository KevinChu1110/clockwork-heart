#!/usr/bin/env python3
"""
build_swan_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十三族 旋音天鵝 (The Melodic Swan, swan) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/MELODIC_SWAN_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological feathers, zero bird flesh, silver enamel tinplate,
  tiara visor with brass beak, octave dual-loop brass winding key,
  theatre herald cuirass & ballet tassets, prismatic crystal monocle & cyan core,
  octave spiral piercing lance, spring steel ballet wings)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (Melodic Swan canonical colors):
    1. Primary Hull: Silver Enamel Tinplate (#E8EFF5) & Sunny Cream Ivory White (#FFFDF8)
    2. Secondary Hull / Trim: Dawn Rose Gold (#E8A598)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028, #FFA010)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Quartz: Celestial Cyan Quartz (#38A0FF)
    6. Cute Coral Pink: Coral Pink (#FF5E8A)
    7. Cold Stamped Tungsten Steel: Tungsten Steel (#7A8A9E, #5C6A7B)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SWAN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/swan"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Melodic Swan Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Silver Enamel Tinplate (#E8EFF5)
SILVER_BASE   = (232, 239, 245, 255)
SILVER_LIGHT  = (246, 250, 253, 255)
SILVER_SHINE  = (255, 255, 255, 255)
SILVER_SHADOW = (205, 215, 226, 255)
SILVER_DARK   = (175, 188, 202, 255)
SILVER_DEEP   = (140, 155, 172, 255)

# 2. Chest & Underbelly: Sunny Cream Ivory White (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (238, 230, 215, 255)
IVORY_DARK   = (215, 202, 182, 255)
IVORY_DEEP   = (185, 172, 152, 255)

# 3. Dawn Rose Gold Trim (#E8A598)
ROSE_BASE  = (232, 165, 152, 255)
ROSE_LIGHT = (248, 198, 188, 255)
ROSE_SHINE = (255, 224, 218, 255)
ROSE_DARK  = (198, 128, 115, 255)
ROSE_DEEP  = (155, 92, 80, 255)

# 4. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 5. Cold Stamped Spring Steel (#7A8A9E)
STEEL_BASE  = (122, 138, 158, 255)
STEEL_LIGHT = (165, 180, 198, 255)
STEEL_SHINE = (210, 222, 235, 255)
STEEL_DARK  = (92, 106, 123, 255)
STEEL_DEEP  = (61, 72, 86, 255)

# 6. Fresh Mint Green Trim & Belt (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 7. Coral Pink Damping & Cooling Ports (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 8. Celestial Cyan Quartz Core & Monocle Lens (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL MELODIC SWAN SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_swan_octave_dual_loop_brass.png
    # Features:
    # - 雙環八音八度黃銅發條鑰匙 (Octave Dual-Ring Brass Key)
    # - Centered at (70, 22), shaft extends down-left to spine socket boss (64, 56)
    # - Dual musical note interlocking loops (lower octave & higher octave rings)
    # - Polished brass gradient (#FFD028, #FFA010, #FFFDF8)
    # - Complies strictly with 0-ART29 dark limit (< 260 px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft from spine (64, 56) to dual loop base (70, 32)
    for t in np.linspace(0.0, 1.0, 28):
        sx = 64.0 + (70.0 - 64.0) * t
        sy = 56.0 + (32.0 - 56.0) * t
        for offset in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.25))
            shade = 1.0 - abs(offset) / 2.5
            r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * shade), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * shade), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine Socket Boss (61..67, 54..60)
    for y in range(54, 61):
        for x in range(61, 68):
            d = ((x - 64.0)**2 + (y - 57.0)**2)**0.5
            if d <= 3.5:
                key_img.putpixel((x, y), GOLD_LIGHT if d < 1.8 else GOLD_DARK)

    # 2. Dual Octave Loops at (62, 20) and (76, 17)
    # Loop 1 (Left loop, lower octave)
    k1_cx, k1_cy = 62.0, 21.0
    r1_out, r1_in = 8.5, 5.0
    for y in range(11, 31):
        for x in range(52, 72):
            d = ((x - k1_cx)**2 + (y - k1_cy)**2)**0.5
            if r1_in <= d <= r1_out:
                spec = max(0.0, 1.0 - abs(x - 60.0) / 7.0)
                shine = max(0.0, 1.0 - ((x - 59.0)**2 + (y - 16.0)**2)**0.5 / 4.0)
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((x, y), (r, g, b, 255))

    # Loop 2 (Right loop, higher octave)
    k2_cx, k2_cy = 76.0, 18.0
    r2_out, r2_in = 9.5, 6.0
    for y in range(8, 29):
        for x in range(66, 87):
            d = ((x - k2_cx)**2 + (y - k2_cy)**2)**0.5
            if r2_in <= d <= r2_out:
                spec = max(0.0, 1.0 - abs(x - 74.0) / 8.0)
                shine = max(0.0, 1.0 - ((x - 73.0)**2 + (y - 13.0)**2)**0.5 / 4.5)
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec) + 40 * shine, 0, 255))
                key_img.putpixel((x, y), (r, g, b, 255))

    # Octave Music Note Cross-Bridge between loops
    for y in range(16, 24):
        for x in range(63, 75):
            d_mid = abs(y - (19.0 + (x - 68.0) * 0.2))
            if d_mid <= 2.2:
                key_img.putpixel((x, y), GOLD_SHINE if d_mid <= 1.0 else GOLD_DARK)

    # Music cylinder comb pin ticks on bridge
    kd.point((66, 17), fill=WHITE_SHINE)
    kd.point((70, 18), fill=WHITE_SHINE)
    kd.point((74, 19), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8)
    # File: back_curio/curio_swan_spring_steel_ballet_wings.png
    # Features:
    # - 多節同軸冷軋彈簧鋼滑翔護羽 (Spring Steel Ballet Wings)
    # - Left wing folds back-left (x: 20..52, y: 48..96)
    # - Right wing base folds back-right (x: 76..93, y: 50..92) strictly x < 94!
    # - Central spring-loaded damping pivot & comb rudder tail at bottom (x: 58..70, y: 88..98)
    # - Polished mirror spring steel (#E8EFF5, #CBD5E1, #94A3B8) with rose gold trim
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Left Wing Ballet Feather Blades (6 stepped cold-rolled steel blades)
    blade_defs_left = [
        # (tip_x, tip_y, base_x, base_y, width)
        (20, 68, 44, 58, 4.2),
        (22, 75, 46, 62, 4.4),
        (26, 82, 48, 66, 4.2),
        (32, 88, 50, 70, 4.0),
        (38, 93, 52, 74, 3.6),
        (46, 95, 54, 78, 3.2),
    ]

    for bx, by, rx, ry, bw in blade_defs_left:
        dx = by - ry
        dy = -(bx - rx)
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            nx = dx / length * bw
            ny = dy / length * bw
            poly = [(rx - nx, ry - ny), (rx + nx, ry + ny), (bx + nx * 0.3, by + ny * 0.3), (bx, by), (bx - nx * 0.3, by - ny * 0.3)]
            cd.polygon(poly, fill=SILVER_SHADOW, outline=OUTLINE)

    # Shading pass over Left Wing to give brilliant silver enamel / spring steel sheen
    for y in range(50, 98):
        for x in range(18, 58):
            p = curio_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 100:
                dist_root = ((x - 50.0)**2 + (y - 68.0)**2)**0.5
                spec = max(0.0, 1.0 - abs(x - 34.0) / 16.0)
                shine = max(0.0, 1.0 - ((x - 30.0)**2 + (y - 76.0)**2)**0.5 / 12.0)**2
                shade = max(0.0, (dist_root - 10.0) / 25.0)

                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine - 15 * shade, 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine - 15 * shade, 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine - 15 * shade, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    for bx, by, rx, ry, bw in blade_defs_left:
        # Rose gold ridge line & golden pivot rivets
        cd.line([(rx, ry), (bx, by)], fill=ROSE_LIGHT, width=1)
        cd.point((int(rx), int(ry)), fill=GOLD_BASE)

    # Left Wing Hinge Joint
    cd.line([(44, 58), (54, 74)], fill=GOLD_BASE, width=2)
    cd.ellipse([42, 56, 46, 60], fill=GOLD_SHINE, outline=OUTLINE)
    cd.ellipse([52, 72, 56, 76], fill=GOLD_SHINE, outline=OUTLINE)

    # 2. Right Wing Base Blades (x strictly < 94)
    blade_defs_right = [
        (88, 56, 76, 56, 3.8),
        (92, 64, 77, 60, 4.0),
        (93, 72, 78, 65, 3.8),
        (91, 80, 78, 70, 3.6),
        (86, 86, 77, 75, 3.2),
    ]

    for bx, by, rx, ry, bw in blade_defs_right:
        dx = by - ry
        dy = -(bx - rx)
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            nx = dx / length * bw
            ny = dy / length * bw
            poly = [(rx - nx, ry - ny), (rx + nx, ry + ny), (bx + nx * 0.3, by + ny * 0.3), (bx, by), (bx - nx * 0.3, by - ny * 0.3)]
            cd.polygon(poly, fill=SILVER_SHADOW, outline=OUTLINE)

    # Shading pass over Right Wing
    for y in range(52, 90):
        for x in range(74, 94):
            p = curio_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 100:
                spec = max(0.0, 1.0 - abs(x - 85.0) / 9.0)
                shine = max(0.0, 1.0 - ((x - 86.0)**2 + (y - 68.0)**2)**0.5 / 10.0)**2
                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    for bx, by, rx, ry, bw in blade_defs_right:
        cd.line([(rx, ry), (bx, by)], fill=ROSE_LIGHT, width=1)
        cd.point((int(rx), int(ry)), fill=GOLD_BASE)

    # Right Wing Pivot Hinge
    cd.line([(76, 56), (82, 72)], fill=GOLD_BASE, width=2)
    cd.ellipse([74, 54, 78, 58], fill=GOLD_SHINE, outline=OUTLINE)

    # 3. Comb Rudder Tail at bottom center (x: 58..70, y: 88..98)
    tail_pts = [(64, 88), (58, 97), (64, 95), (70, 97)]
    cd.polygon(tail_pts, fill=SILVER_LIGHT, outline=OUTLINE)
    cd.line([(64, 88), (64, 95)], fill=ROSE_BASE, width=1)
    for tx in [61, 64, 67]:
        cd.point((tx, 94), fill=GOLD_SHINE)

    # STRICT 0-ART9/11 enforcement: ensure zero pixels in x >= 94
    for y in range(H):
        for x in range(94, W):
            curio_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(curio_img)

    # Re-enforce zero pixels at x >= 94 after outline pass
    for y in range(H):
        for x in range(94, W):
            curio_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10)
    # File: chassis/chassis_swan_silver_enamel_default.png
    # Features:
    # - 2.2 Head-to-Body Q-version mechanical swan automaton chassis
    # - Bare chassis torso (x: 44..84, y: 56..94) with multi-tone depth (0-ART18: >= 20 colors)
    # - Silver Enamel (#E8EFF5) with Sunny Cream Ivory White (#FFFDF8) belly panel
    # - Circular translucent quartz music box window at center chest (64, 72)
    # - Graceful ballet metal webbed feet with brass ankle pivot joints (y: 92..112)
    # - Left wing/arm poised in graceful ballet dancer curve at x: 34..48, y: 64..84
    # - Right arm base at x: 80..93, y: 62..82
    # - STRICT 0-ART9/11: weapon zone x >= 94 MUST BE ZERO PIXELS!
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Main Torso Ellipsoid Hull (x: 44..84, y: 54..94)
    cx_t, cy_t = 64.0, 75.0
    rx_t, ry_t = 19.0, 19.0

    for y in range(54, 95):
        for x in range(44, 85):
            dx = (x - cx_t) / rx_t
            dy = (y - cy_t) / ry_t
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Underbelly vs flank plates
                is_belly = (abs(x - 64.0) <= 9.0 and y >= 64)
                if is_belly:
                    # Sunny Cream Ivory White
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.2 * spec) + 15 * shine - 25 * edge_shade, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.2 * spec) + 15 * shine - 25 * edge_shade, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.2 * spec) + 15 * shine - 25 * edge_shade, 0, 255))
                else:
                    # Silver Enamel Tinplate
                    r = int(np.clip(SILVER_BASE[0] * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                    g = int(np.clip(SILVER_BASE[1] * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                    b = int(np.clip(SILVER_BASE[2] * (0.75 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))

    # Torso Rose Gold Trim Band & Brass Rivets (y: 72..74)
    for bx in range(48, 81):
        if ((bx - cx_t)/rx_t)**2 + ((73.0 - cy_t)/ry_t)**2 <= 0.95:
            chassis_img.putpixel((bx, 73), ROSE_BASE)
            chassis_img.putpixel((bx, 74), ROSE_LIGHT)

    # Circular Music Box Window at (64, 72)
    for y in range(67, 78):
        for x in range(59, 70):
            d_win = ((x - 64.0)**2 + (y - 72.0)**2)**0.5
            if d_win <= 4.8:
                if d_win >= 4.0:
                    chassis_img.putpixel((x, y), GOLD_BASE)
                elif d_win <= 3.2:
                    # Quartz window glass with cyan glow & music cylinder pins
                    is_pin = (x in [62, 64, 66] and y in [70, 72, 74])
                    if is_pin:
                        chassis_img.putpixel((x, y), GOLD_SHINE)
                    else:
                        chassis_img.putpixel((x, y), CYAN_LIGHT if d_win <= 1.5 else CYAN_BASE)

    # Rivets on Torso Plate Flanks
    for rx, ry in [(49, 66), (48, 80), (79, 66), (80, 80)]:
        chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)

    # 2. Left Forearm/Wing poised in Graceful Ballet Pose (x: 34..48, y: 64..84)
    for y in range(64, 85):
        for x in range(34, 49):
            dx = (x - 41.0) / 6.0
            dy = (y - 74.0) / 9.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 39.0) / 6.0)
                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))
    # Rose gold wrist cuff & silver wing tip
    chd.line([(36, 79), (44, 79)], fill=ROSE_BASE, width=1)
    chd.polygon([(36, 81), (34, 86), (37, 84)], fill=SILVER_LIGHT, outline=OUTLINE)
    chd.polygon([(40, 82), (40, 87), (42, 84)], fill=SILVER_LIGHT, outline=OUTLINE)
    chd.polygon([(44, 81), (46, 86), (45, 83)], fill=SILVER_LIGHT, outline=OUTLINE)

    # 3. Right Upper Arm Base (x: 80..93, y: 62..82) - strictly x < 94!
    for y in range(64, 82):
        for x in range(80, 94):
            dx = (x - 86.0) / 6.0
            dy = (y - 72.0) / 8.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 85.0) / 6.0)
                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))
    chd.ellipse([88, 70, 92, 74], fill=GOLD_BASE, outline=OUTLINE)

    # 4. Ballet Metal Webbed Feet at bottom (y: 92..112)
    # Left Foot: cx = 52.0; Right Foot: cx = 76.0
    for t_cx in [52.0, 76.0]:
        # Ankle ball joint
        chd.ellipse([int(t_cx - 4), 92, int(t_cx + 4), 98], fill=GOLD_DARK, outline=OUTLINE)
        chd.ellipse([int(t_cx - 2), 94, int(t_cx + 2), 96], fill=ROSE_BASE)
        # Webbed ballet feet plate
        foot_pts = [
            (int(t_cx - 3), 96),
            (int(t_cx - 7), 108),
            (int(t_cx - 2), 107),
            (int(t_cx), 110),
            (int(t_cx + 2), 107),
            (int(t_cx + 7), 108),
            (int(t_cx + 3), 96)
        ]
        chd.polygon(foot_pts, fill=SILVER_LIGHT, outline=OUTLINE)
        chd.line([(int(t_cx), 96), (int(t_cx), 110)], fill=ROSE_BASE, width=1)
        chd.point((int(t_cx), 96), fill=GOLD_SHINE)

    # STRICT 0-ART9/11 enforcement: ensure zero pixels in x >= 94
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)

    # Re-enforce zero pixels at x >= 94 after outline pass
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_swan_tiara_beak_visor.png
    # Features:
    # - 八音皇冠護額長喙 (Music Tiara Visor & Brass Beak)
    # - Streamline silver enamel helmet dome (x: 40..88, y: 16..52)
    # - Forehead 5-pointed music tiara crown (x: 54..74, y: 8..20) with gold bead tips
    # - Continuous solid articulated swan neck and throat (x: 56..74, y: 46..62)
    # - Polished brass mechanical beak (x: 57..71, y: 44..55)
    # - Cheek coral pink round cooling ports at (45, 42) and (83, 42)
    # - Eye socket outer golden brass bezel rings at (52, 40) and (76, 40)
    # - STRICT 0-ART27: Inner eye socket centers MUST be completely hollow (alpha == 0)
    #   at (39..41, 51..53) and (39..41, 75..77)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Continuous Articulated Swan Neck & Collar (x: 56..74, y: 46..62)
    for y in range(46, 62):
        for x in range(56, 75):
            # Curved cylinder neck connecting head to torso without any gap
            dx = (x - 65.0) / 8.5
            dy = (y - 54.0) / 8.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - abs(x - 63.0) / 7.0)
                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Articulated brass ball-joint collars across neck
    for ny in [50, 55, 60]:
        hd.line([(58, ny), (72, ny)], fill=GOLD_BASE, width=1)
        hd.point((65, ny), fill=GOLD_SHINE)

    # 2. Main Helmet Dome (x: 40..88, y: 18..52)
    cx_h, cy_h = 64.0, 35.0
    for y in range(18, 53):
        for x in range(40, 89):
            dx = (x - cx_h) / 22.0
            dy = (y - cy_h) / 16.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 28.0)**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 28.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 3. Brow Rose Gold Band & Mint Accent (y: 28..31, x: 44..84)
    for bx in range(44, 85):
        if ((bx - cx_h)/22.0)**2 + ((29.0 - cy_h)/16.0)**2 <= 0.98:
            head_img.putpixel((bx, 29), ROSE_BASE)
            head_img.putpixel((bx, 30), MINT_BASE)
            if bx % 4 == 0:
                head_img.putpixel((bx, 28), GOLD_LIGHT)

    # 4. Music Tiara Crown on Forehead (x: 54..74, y: 8..20)
    tiara_pts = [
        (54, 20), (55, 14), (58, 17), (61, 10), (64, 16),
        (67, 10), (70, 17), (73, 14), (74, 20)
    ]
    hd.polygon(tiara_pts, fill=GOLD_BASE, outline=OUTLINE)
    # Crown finial beads
    for fx, fy in [(55, 13), (61, 9), (67, 9), (73, 13)]:
        hd.ellipse([fx - 1, fy - 1, fx + 1, fy + 1], fill=GOLD_SHINE)
    # Central mint gem on crown
    hd.ellipse([63, 17, 65, 19], fill=MINT_BASE)

    # 5. Cheek Coral Pink Cooling Ports at (45, 42) and (83, 42)
    hd.ellipse([43, 40, 47, 44], fill=CORAL_BASE, outline=OUTLINE)
    hd.ellipse([81, 40, 85, 44], fill=CORAL_BASE, outline=OUTLINE)
    head_img.putpixel((45, 42), CORAL_LIGHT)
    head_img.putpixel((83, 42), CORAL_LIGHT)

    # 6. Polished Brass Mechanical Beak (x: 57..71, y: 44..55)
    beak_pts = [(57, 45), (71, 45), (67, 54), (64, 55), (61, 54)]
    hd.polygon(beak_pts, fill=GOLD_BASE, outline=OUTLINE)
    # Beak central dividing slit (dual-flap opening mechanism)
    hd.line([(58, 49), (70, 49)], fill=OUTLINE, width=1)
    hd.line([(59, 48), (69, 48)], fill=GOLD_LIGHT, width=1)
    hd.point((64, 52), fill=GOLD_SHINE)

    # 7. Golden Brass Bezel Rings surrounding Eye Sockets
    for ecx in [52.0, 76.0]:
        for y in range(34, 47):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - 40.0)**2)**0.5
                if 2.5 <= dist <= 5.8:
                    spec = max(0.0, 1.0 - abs(x - (ecx - 1.0)) / 5.0)
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec), 0, 255))
                    head_img.putpixel((x, y), (r, g, b, 255))

    # 8. STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye socket centers MUST be completely transparent (alpha = 0)
    for y in range(38, 43):
        for x in range(50, 55):
            if ((x - 52.0)**2 + (y - 40.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(74, 79):
            if ((x - 76.0)**2 + (y - 40.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(head_img, ignore_regions=[(48, 36, 56, 44), (72, 36, 80, 44)])

    # Re-enforce 0-ART27 hollow eye socket centers
    for y in range(39, 42):
        for x in range(51, 54):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(75, 78):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 30)
    # File: optic_core/face_swan_prismatic_crystal_monocle.png
    # Features:
    # - 單片棱鏡聚焦水晶目鏡 (Prismatic Crystal Monocle & Optic Lens)
    # - Right eye (76, 40): Multi-lens prismatic crystal monocle with brass vernier gear rim
    # - Left eye (52, 40): Spherical cyan quartz optic lens with refraction glint
    # - Aligns with 0-ART27: Center pixels at (52, 40) and (76, 40) have alpha > 200
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crd = ImageDraw.Draw(core_img)

    # 1. Left Eye (52, 40): Celestial Cyan Quartz Sphere
    ecx_l, ecy_l = 52.0, 40.0
    r_core = 5.2
    for y in range(35, 46):
        for x in range(47, 58):
            dist = ((x - ecx_l)**2 + (y - ecy_l)**2)**0.5
            if dist <= r_core:
                spec = max(0.0, 1.0 - ((x - 50.0)**2 + (y - 38.0)**2)**0.5 / 4.0)
                shine = max(0.0, 1.0 - ((x - 50.0)**2 + (y - 38.0)**2)**0.5 / 2.0)**2
                r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))
    crd.ellipse([int(ecx_l - r_core), int(ecy_l - r_core), int(ecx_l + r_core), int(ecy_l + r_core)], outline=OUTLINE, width=1)
    core_img.putpixel((50, 38), WHITE_SHINE)
    core_img.putpixel((51, 38), CYAN_SHINE)

    # 2. Right Eye (76, 40): Prismatic Crystal Monocle with Gear-toothed Brass Rim
    ecx_r, ecy_r = 76.0, 40.0
    r_mono = 5.8
    for y in range(34, 47):
        for x in range(70, 83):
            dist = ((x - ecx_r)**2 + (y - ecy_r)**2)**0.5
            if dist <= r_mono:
                spec = max(0.0, 1.0 - ((x - 74.0)**2 + (y - 38.0)**2)**0.5 / 4.5)
                shine = max(0.0, 1.0 - ((x - 74.0)**2 + (y - 38.0)**2)**0.5 / 2.0)**2
                # Monocle inner prismatic cyan quartz
                r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.2 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.2 * spec) + 25 * shine, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))

    # Brass outer gear rim & vernier crosshairs
    crd.ellipse([int(ecx_r - r_mono), int(ecy_r - r_mono), int(ecx_r + r_mono), int(ecy_r + r_mono)], outline=GOLD_BASE, width=1)
    crd.ellipse([int(ecx_r - r_mono - 1), int(ecy_r - r_mono - 1), int(ecx_r + r_mono + 1), int(ecy_r + r_mono + 1)], outline=OUTLINE, width=1)

    # Prismatic crosshair reticle
    crd.line([(int(ecx_r - 3), int(ecy_r)), (int(ecx_r + 3), int(ecy_r))], fill=GOLD_LIGHT, width=1)
    crd.line([(int(ecx_r), int(ecy_r - 3)), (int(ecx_r), int(ecy_r + 3))], fill=GOLD_LIGHT, width=1)
    # Monocle bracket arm extending to helmet rim
    crd.line([(int(ecx_r + r_mono), int(ecy_r)), (int(ecx_r + r_mono + 3), int(ecy_r - 2))], fill=GOLD_BASE, width=1)

    core_img.putpixel((75, 39), WHITE_SHINE)
    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_swan_theatre_herald_cuirass.png
    # Features:
    # - 大劇院儀仗近衛胸甲與游標裙甲 (Theatre Herald Cuirass & Tassets)
    # - Solid Gorget Collar bridging neck to chest (x: 54..74, y: 52..58)
    # - Stamped silver steel cuirass over chest (x: 42..86, y: 55..84)
    # - Dawn Rose Gold (#E8A598) trim & beveled borders
    # - Fresh Mint Green (#4ED86A) vernier scale belt at waist (y: 80..84)
    # - 4 curved ballet tasset plates flared outward over hips (y: 83..94, x: 44..84)
    # - STRICT 0-ART26b: lower zone y >= 96 MUST BE STRICTLY 0 PIXELS!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ctd = ImageDraw.Draw(costume_img)

    # 1. Gorget Collar bridging neck to chest (y: 52..58, x: 54..74)
    for y in range(52, 59):
        for x in range(55, 74):
            dx = (x - 64.5) / 9.0
            dy = (y - 55.0) / 3.5
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 63.0) / 8.0)
                r = int(np.clip(ROSE_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                g = int(np.clip(ROSE_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                b = int(np.clip(ROSE_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                costume_img.putpixel((x, y), (r, g, b, 255))

    for y in range(55, 85):
        for x in range(42, 87):
            dx = (x - 64.0) / 19.0
            dy = (y - 68.0) / 15.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 64.0)**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 64.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dx**2 + dy**2 - 0.5) / 0.5)

                r = int(np.clip(SILVER_BASE[0] * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                costume_img.putpixel((x, y), (r, g, b, 255))

    # Rose Gold Piping & Gorget Trim (y: 56..60)
    for bx in range(48, 81):
        if ((bx - 64.0)/19.0)**2 + ((58.0 - 68.0)/15.0)**2 <= 0.95:
            costume_img.putpixel((bx, 58), ROSE_BASE)
            costume_img.putpixel((bx, 59), ROSE_LIGHT)

    # Heraldic Rose Gold Center Ridge on Breastplate
    ctd.line([(64, 60), (64, 79)], fill=ROSE_BASE, width=2)
    ctd.line([(64, 60), (64, 79)], fill=ROSE_LIGHT, width=1)
    ctd.ellipse([62, 66, 66, 70], fill=GOLD_BASE, outline=OUTLINE)
    ctd.point((64, 68), fill=MINT_BASE)

    # Fresh Mint Green Vernier Scale Belt (y: 80..83, x: 44..84)
    for bx in range(44, 85):
        if ((bx - 64.0)/19.0)**2 + ((81.0 - 68.0)/15.0)**2 <= 1.05:
            costume_img.putpixel((bx, 81), MINT_BASE)
            costume_img.putpixel((bx, 82), MINT_DARK)
            if bx % 3 == 0:
                costume_img.putpixel((bx, 80), GOLD_LIGHT)
    # Belt Center Buckle
    ctd.ellipse([61, 79, 67, 84], fill=GOLD_SHINE, outline=OUTLINE)

    # Ballet Tasset Plates Flared Outward (y: 83..94, x: 44..84)
    # 4 distinct metal skirt plates
    tasset_rects = [
        [(44, 83), (52, 83), (50, 93), (42, 91)], # Leftmost
        [(52, 83), (62, 83), (61, 94), (51, 93)], # Mid-left
        [(66, 83), (76, 83), (77, 93), (67, 94)], # Mid-right
        [(76, 83), (84, 83), (86, 91), (78, 93)], # Rightmost
    ]
    for poly in tasset_rects:
        ctd.polygon(poly, fill=SILVER_LIGHT, outline=OUTLINE)
        # Rose gold border on tasset hem
        ctd.line([poly[3], poly[2]], fill=ROSE_BASE, width=1)

    # STRICT 0-ART26b enforcement: zero pixels at y >= 96
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(costume_img)

    # Re-enforce zero pixels at y >= 96 after outline pass
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_swan_octave_spiral_lance.png
    # Features:
    # - 八音螺旋穿刺長槍 (Octave Spiral Piercing Lance)
    # - Right-hand single held (0-MKT7 compliant)
    # - Grip at (88, 76) with brass pommel and knurled handle
    # - Seamless silver-plated steel shaft extending up-right to (106, 36)
    # - Spiral conical golden lance tip from (106, 36) to (114, 18)
    # - Miniature octave sound cylinder and comb teeth on lance housing
    # - Vibrant multi-tone color richness (0-ART5 compliant >= 20 colors)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Lance Shaft from pommel (86, 92) through grip (88, 76) to lance base (106, 36)
    w_start = (86.0, 92.0)
    w_mid   = (88.0, 76.0)
    w_base  = (106.0, 36.0)

    # Pommel & Lower Shaft (86, 92) -> (88, 76)
    wd.ellipse([83, 90, 89, 96], fill=GOLD_SHINE, outline=OUTLINE)
    for t in np.linspace(0.0, 1.0, 24):
        sx = w_start[0] + (w_mid[0] - w_start[0]) * t
        sy = w_start[1] + (w_mid[1] - w_start[1]) * t
        for off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(sx + off * 0.9))
            py = int(round(sy - off * 0.2))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(off) / 2.0
                r = int(np.clip(SILVER_BASE[0] * (0.75 + 0.3 * shade), 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.75 + 0.3 * shade), 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.75 + 0.3 * shade), 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # Grip & Handguard at (88, 76)
    wd.ellipse([84, 73, 92, 79], fill=GOLD_BASE, outline=OUTLINE)
    for gy in range(74, 79):
        for gx in range(85, 92):
            d_grp = ((gx - 88.0)**2 + (gy - 76.0)**2)**0.5
            if d_grp <= 3.0:
                spec = max(0.0, 1.0 - d_grp / 3.0)
                r = int(np.clip(ROSE_BASE[0] * (0.8 + 0.35 * spec), 0, 255))
                g = int(np.clip(ROSE_BASE[1] * (0.8 + 0.35 * spec), 0, 255))
                b = int(np.clip(ROSE_BASE[2] * (0.8 + 0.35 * spec), 0, 255))
                weapon_img.putpixel((gx, gy), (r, g, b, 255))

    # Main Shaft from (88, 76) to (106, 36) with rich metallic gradient
    for t in np.linspace(0.0, 1.0, 56):
        sx = w_mid[0] + (w_base[0] - w_mid[0]) * t
        sy = w_mid[1] + (w_base[1] - w_mid[1]) * t
        for off in [-1.8, -0.8, 0.2, 1.2, 2.2]:
            px = int(round(sx + off * 0.9))
            py = int(round(sy - off * 0.4))
            if 0 <= px < W and 0 <= py < H:
                dist_edge = abs(off) / 2.5
                spec = max(0.0, 1.0 - dist_edge)
                shine = max(0.0, 1.0 - abs(t - 0.5) / 0.5)**2
                r = int(np.clip(SILVER_BASE[0] * (0.7 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(SILVER_BASE[1] * (0.7 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(SILVER_BASE[2] * (0.7 + 0.35 * spec) + 35 * shine, 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # Miniature Octave Music Cylinder Housing on Lance (around t=0.55..0.75, x: 95..105, y: 45..59)
    for y in range(45, 59):
        for x in range(95, 106):
            d_cyl = abs((x - 100.0) + (y - 52.0)*0.4)
            if d_cyl <= 4.2:
                spec = max(0.0, 1.0 - d_cyl / 4.2)
                shine = max(0.0, 1.0 - ((x - 98.0)**2 + (y - 50.0)**2)**0.5 / 5.0)
                r = int(np.clip(GOLD_BASE[0] * (0.75 + 0.35 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.75 + 0.35 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.75 + 0.35 * spec) + 35 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Music cylinder steel comb teeth pins & mint graduation ticks
    for cy in [47, 50, 53, 56]:
        weapon_img.putpixel((98, cy), STEEL_SHINE)
        weapon_img.putpixel((99, cy), STEEL_LIGHT)
        weapon_img.putpixel((101, cy), MINT_BASE)
        weapon_img.putpixel((102, cy), MINT_LIGHT)

    # 2. Spiral Conical Lance Tip from (106, 36) to tip (114, 18) with multi-tone gradient
    tip_pt = (114.0, 18.0)
    for t in np.linspace(0.0, 1.0, 40):
        cur_x = w_base[0] + (tip_pt[0] - w_base[0]) * t
        cur_y = w_base[1] + (tip_pt[1] - w_base[1]) * t
        cone_radius = 5.2 * (1.0 - t)
        for off in np.linspace(-cone_radius, cone_radius, int(cone_radius * 4 + 1)):
            px = int(round(cur_x + off * 0.7))
            py = int(round(cur_y - off * 0.4))
            if 0 <= px < W and 0 <= py < H:
                # Golden spiral fluting with rich color variation
                is_spiral = int(t * 8.0 + off) % 2 == 0
                spec = max(0.0, 1.0 - abs(off) / (cone_radius + 0.1))
                shine = max(0.0, 1.0 - abs(t - 0.7) / 0.3)**2
                base_c = GOLD_SHINE if is_spiral else GOLD_DARK
                r = int(np.clip(base_c[0] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(base_c[1] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(base_c[2] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    wd.point((114, 18), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_swan_octave_dual_loop_brass", key_img),
        ("back_curio", "curio_swan_spring_steel_ballet_wings", curio_img),
        ("chassis", "chassis_swan_silver_enamel_default", chassis_img),
        ("head_unit", "head_swan_tiara_beak_visor", head_img),
        ("costume", "costume_swan_theatre_herald_cuirass", costume_img),
        ("optic_core", "face_swan_prismatic_crystal_monocle", core_img),
        ("weapon", "weapon_swan_octave_spiral_lance", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{SWAN_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{SWAN_PD_DIR}/winding_key/key_swan_octave_dual_loop_brass.png", f"{KEY_DIR}/key_swan_octave_dual_loop_brass.png")
    shutil.copyfile(f"{SWAN_PD_DIR}/weapon/weapon_swan_octave_spiral_lance.png", f"{WEAPON_DIR}/weapon_swan_octave_spiral_lance.png")
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

    proof_comp = f"{SWAN_PD_DIR}/proof_paperdoll_swan_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SWAN_PD_DIR}/proof_paperdoll_swan_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 28
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

    strip_path = f"{SWAN_PD_DIR}/proof_swan_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/swan_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/swan_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/swan_idle.png
    p_idle_64 = f"{PLAYER_DIR}/swan_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/swan_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/swan_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/swan_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/swan_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/swan_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL MELODIC SWAN CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
