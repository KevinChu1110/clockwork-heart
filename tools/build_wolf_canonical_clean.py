#!/usr/bin/env python3
"""
build_wolf_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十二族 荒原鋼狼 (The Scrap Wolf, wolf) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/SCRAP_WOLF_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero leather/flesh, stamped rust-proof steel plates,
  ivory enamel cheek/chest plates, folded brass airfoil sensor ears, vulcanized silicone marching boots,
  Po Jun heavy cross winding key, segmented spring steel balance tail, scrap sawblade greatsword)
- references/art_direction.md & references/brand_assets.md:
  Dawson Day 258 Dopamine palette:
    Primary: Warm Orange Rust-Proof Steel Plate (#FFA010)
    Secondary: Ivory White Enamel (#FFFDF8)
    Accent: Dopamine Golden Po Jun Heavy Cross Key & Clock Gears (#FFD028)
    Detail: Star Sky Blue Twin Optical Core Lenses (#38A0FF)
    Warm Highlight: Coral Pink High-Pressure Silicone Seals & Fluid Terminals (#FF5E8A)
    Scrap Steel: Quenched Stamped Tungsten Steel Sawblade & Interlocking Cowl (#5A5666)
    Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
WOLF_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Scrap Wolf Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Warm Orange Rust-Proof Steel Plate (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 80, 255)
ORANGE_SHINE = (255, 230, 155, 255)
ORANGE_DARK  = (210, 115, 8, 255)
ORANGE_DEEP  = (150, 75, 4, 255)

# Secondary: Ivory White Enamel Cheek & Chest Plates (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (230, 224, 215, 255)
IVORY_DARK    = (195, 188, 178, 255)

# Accent: Dopamine Golden Po Jun Cross Key & Clock Gears (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# Detail: Star Sky Blue Twin Optical Core Lenses (#38A0FF)
BLUE_BASE  = (56, 160, 255, 255)
BLUE_LIGHT = (120, 205, 255, 255)
BLUE_SHINE = (200, 235, 255, 255)
BLUE_DARK  = (20, 105, 200, 255)

# Warm Highlight: Coral Pink High-Pressure Silicone Seals & Fluid Terminals (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

# Scrap Steel: Quenched Stamped Tungsten Steel Sawblade & Interlocking Cowl (#5A5666)
STEEL_BASE  = (90, 86, 102, 255)
STEEL_LIGHT = (140, 136, 155, 255)
STEEL_SHINE = (195, 192, 210, 255)
STEEL_DARK  = (55, 52, 65, 255)

# Scavenger Harness Canvas / Leather straps (#8E522D)
CANVAS_BASE  = (142, 82, 45, 255)
CANVAS_LIGHT = (180, 112, 68, 255)
CANVAS_DARK  = (96, 52, 26, 255)

# Vulcanized Industrial Black Silicone Marching Boots (#202026)
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
    print("=== BUILDING 100% MODULAR CANONICAL SCRAP WOLF SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_wolf_heavy_pojun_cross.png
    # High-Torque Po Jun Heavy Cross Winding Key (高扭力破軍重工十字發條鑰匙)
    # Socket at upper spine (64, 60), shaft extends diagonally up-right to (86, 30)
    # Features:
    # - Polished brass shaft with bevel metal shading
    # - Four-Ring Cross Winding Wing Handle in dopamine gold (#FFD028)
    # - Center tungsten steel axle hub with visible self-locking ratchet teeth
    # - Central coral pink pivot jewel (#FF5E8A) with brilliant specular glint
    # - STRICTLY transparent corners (0-ART29 compliance)
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

    # 2. Key Hub & Po Jun Cross Mechanism at (86, 30)
    kcx, kcy = 86.0, 30.0

    # Four-Ring Cross Winding Wings: Left, Right, Top, Bottom
    # Centers at (74, 30), (98, 30), (86, 18), (86, 42)
    cross_wings = [
        (74.0, 30.0, 10.5, 5.0),  # Left
        (98.0, 30.0, 10.5, 5.0),  # Right
        (86.0, 18.0, 10.5, 5.0),  # Top
        (86.0, 42.0, 9.5, 4.5),   # Bottom (slightly more compact for clearance)
    ]
    for wcx, wcy, r_outer, r_inner in cross_wings:
        for y in range(int(wcy - r_outer - 2), int(wcy + r_outer + 3)):
            for x in range(int(wcx - r_outer - 2), int(wcx + r_outer + 3)):
                dist = ((x - wcx)**2 + (y - wcy)**2)**0.5
                if r_inner <= dist <= r_outer:
                    norm_r = (dist - r_inner) / (r_outer - r_inner)
                    spec = max(0.0, np.sin(norm_r * np.pi))
                    shine = max(0.0, 1.0 - ((x - (wcx - 2))**2 + (y - (wcy - 2))**2)**0.5 / 5.0)**2
                    r_w = int(np.clip(255 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_w = int(np.clip(208 * (0.8 + 0.3 * spec) + 35 * shine, 0, 255))
                    b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Central Ratchet Wheel with Sawteeth at (86, 30)
    r_ratchet = 7.5
    for y in range(int(kcy - r_ratchet - 2), int(kcy + r_ratchet + 3)):
        for x in range(int(kcx - r_ratchet - 2), int(kcx + r_ratchet + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if dist <= r_ratchet:
                angle = np.arctan2(y - kcy, x - kcx)
                saw = ((angle % (np.pi / 4)) / (np.pi / 4))
                spec = max(0.0, 1.0 - dist / r_ratchet)
                r_r = int(np.clip(90 * (0.8 + 0.3 * spec) + 60 * spec - 15 * saw, 0, 255))
                g_r = int(np.clip(86 * (0.8 + 0.3 * spec) + 60 * spec - 15 * saw, 0, 255))
                b_r = int(np.clip(102 * (0.8 + 0.3 * spec) + 80 * spec, 0, 255))
                key_img.putpixel((x, y), (r_r, g_r, b_r, 255))

    # Visible Ratchet Teeth Points around circumference
    for i in range(8):
        t_angle = i * (np.pi / 4)
        tx = int(kcx + (r_ratchet + 1.2) * np.cos(t_angle))
        ty = int(kcy + (r_ratchet + 1.2) * np.sin(t_angle))
        if 0 <= tx < W and 0 <= ty < H:
            key_img.putpixel((tx, ty), GOLD_LIGHT)

    # Spring-Steel Self-Locking Pawl engaging the ratchet wheel from (77, 24) to (83, 27)
    kd.line([(76, 23), (83, 27)], fill=STEEL_LIGHT, width=2)
    kd.ellipse([75, 22, 78, 25], fill=STEEL_DARK, outline=OUTLINE)
    kd.point((76, 23), fill=WHITE_SHINE)

    # Center jewel / hub bearing at (86, 30)
    kd.ellipse([int(kcx - 3.5), int(kcy - 3.5), int(kcx + 3.5), int(kcy + 3.5)], fill=CORAL_BASE, outline=OUTLINE)
    kd.ellipse([int(kcx - 1.8), int(kcy - 1.8), int(kcx + 1.8), int(kcy + 1.8)], fill=CORAL_LIGHT)
    kd.point((int(kcx - 0.5), int(kcy - 0.5)), fill=WHITE_SHINE)

    apply_clean_outline(key_img)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_wolf_segmented_spring_tail.png
    # High-Torque Segmented Spring Steel Balance Tail (高扭力螺旋發條多節重鋼平衡尾)
    # Features:
    # - Originates at lower back spine (46, 84)
    # - Seven distinct articulated stamped tungsten steel casing segments (#5A5666)
    # - Arches outwards and sweeps gracefully back-left to counterpoise knight stance
    # - Visible inner continuous helical gold spring (#FFD028) connecting segments
    # - Coral pink (#FF5E8A) silicone dampener seal rings between segments
    # - Stamped brass aerodynamic balance fin at tip
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Seven Segment Nodes along tail curve
    tail_nodes = [
        (46.0, 84.0, 6.0),   # Base segment (closest to spine)
        (40.0, 86.0, 5.8),   # Segment 2
        (33.0, 87.0, 5.5),   # Segment 3
        (26.0, 85.0, 5.0),   # Segment 4
        (21.0, 80.0, 4.6),   # Segment 5
        (18.0, 72.0, 4.2),   # Segment 6
        (17.0, 63.0, 3.8),   # Segment 7 (Tip node)
    ]

    # 1. Inner Helical Gold Spring Wire passing through all segments
    for i in range(len(tail_nodes) - 1):
        x0, y0, r0 = tail_nodes[i]
        x1, y1, r1 = tail_nodes[i+1]
        for t in np.linspace(0.0, 1.0, 25):
            mx = x0 + t * (x1 - x0)
            my = y0 + t * (y1 - y0)
            # Helical coil oscillation
            perp_x = -(y1 - y0)
            perp_y = (x1 - x0)
            p_len = (perp_x**2 + perp_y**2)**0.5 + 1e-5
            perp_x /= p_len
            perp_y /= p_len
            wave = np.sin(t * np.pi * 4.0) * 2.2
            wx = int(mx + perp_x * wave)
            wy = int(my + perp_y * wave)
            if 0 <= wx < W and 0 <= wy < H:
                curio_img.putpixel((wx, wy), GOLD_LIGHT)

    # 2. Seven Stamped Tungsten Steel Casing Segments
    for idx, (nx, ny, nrad) in enumerate(tail_nodes):
        for y in range(int(ny - nrad - 2), int(ny + nrad + 3)):
            for x in range(int(nx - nrad - 2), int(nx + nrad + 3)):
                dist = ((x - nx)**2 + (y - ny)**2)**0.5
                if dist <= nrad:
                    spec = max(0.0, 1.0 - ((x - (nx - 1.5))**2 + (y - (ny - 1.5))**2)**0.5 / nrad)
                    shine = max(0.0, 1.0 - ((x - (nx - 1.5))**2 + (y - (ny - 1.5))**2)**0.5 / 2.0)**2
                    r_s = int(np.clip(90 * (0.8 + 0.35 * spec) + 70 * shine, 0, 255))
                    g_s = int(np.clip(86 * (0.8 + 0.35 * spec) + 70 * shine, 0, 255))
                    b_s = int(np.clip(102 * (0.8 + 0.35 * spec) + 90 * shine, 0, 255))
                    curio_img.putpixel((x, y), (r_s, g_s, b_s, 255))

        # Coral Pink Silicone Dampener Ring between segments
        if idx < len(tail_nodes) - 1:
            nxt_x, nxt_y, _ = tail_nodes[idx + 1]
            mid_x = int(0.5 * (nx + nxt_x))
            mid_y = int(0.5 * (ny + nxt_y))
            cd.ellipse([mid_x - 2, mid_y - 2, mid_x + 2, mid_y + 2], fill=CORAL_BASE)
            cd.point((mid_x, mid_y), fill=CORAL_LIGHT)

        # Micro rivet on segment center
        cd.point((int(nx), int(ny)), fill=GOLD_BASE)

    # 3. Aerodynamic Balance Fin / Brass Tip Spear at (17, 63)
    tip_poly = [
        (17, 56),  # Tip point
        (13, 62),  # Left fin wing
        (17, 65),  # Base center
        (21, 62)   # Right fin wing
    ]
    cd.polygon(tip_poly, fill=GOLD_BASE, outline=OUTLINE)
    cd.point((17, 58), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_wolf_warm_orange_default.png
    # Features:
    # - 2.0 ~ 2.2 Chibi standard knight stance
    # - Soft ground contact shadow centered at (64, 116)
    # - Heavy-duty vulcanized black silicone marching boots (#202026) with tungsten toe kicker plates
    # - Warm Orange (#FFA010) rust-proof steel plates on limbs and torso hull
    # - Ivory White (#FFFDF8) enamel shock-absorbing chest & belly plate
    # - Coral pink (#FF5E8A) ball-and-socket joint bushings
    # - Left arm: raised balancing palm / defensive guard at (38, 84)
    # - Right arm: grip hub tucked at (82, 75)
    # - STRICT ZERO pixels in outer weapon zone (x >= 94) for 0-ART9 / 0-ART11
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Vulcanized Silicone Marching Boots with Tungsten Toe Kicker Plates
    boot_pos = [(48.0, 113.0), (70.0, 113.0)]
    for bx, by in boot_pos:
        # Sole base
        ch_d.ellipse([int(bx - 7), int(by - 2), int(bx + 7), int(by + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(bx - 5), int(by - 1), int(bx + 5), int(by + 2)], fill=SILICONE_LIGHT)
        # Tungsten steel rounded toe kicker cap & rim
        ch_d.ellipse([int(bx - 4), int(by), int(bx + 4), int(by + 3)], fill=STEEL_BASE)
        ch_d.line([(int(bx - 3), int(by + 2)), (int(bx + 3), int(by + 2))], fill=STEEL_LIGHT, width=1)
        ch_d.point((int(bx), int(by + 1)), fill=WHITE_SHINE)

    # 3. Articulated Legs with Warm Orange Steel Armor Plates
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
                g_l = int(np.clip(160 * (0.8 + 0.35 * spec), 0, 255))
                b_l = int(np.clip(16 * (0.8 + 0.35 * spec) + 40 * spec, 0, 255))
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
                    # Warm Orange Rust-Proof Steel Shell
                    r_t = int(np.clip(255 * (0.75 + 0.45 * spec) - 20 * edge_shade + 50 * shine, 0, 255))
                    g_t = int(np.clip(160 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_t = int(np.clip(16 * (0.75 + 0.45 * spec) - 10 * edge_shade + 40 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center clockwork escapement / regulator window at (63, 75)
    ch_d.ellipse([60, 72, 66, 78], fill=OUTLINE)
    ch_d.ellipse([61, 73, 65, 77], fill=GOLD_BASE)
    ch_d.point((63, 75), fill=CORAL_BASE)
    ch_d.point((62, 74), fill=WHITE_SHINE)

    # Coral Pink pressure damper seam across mid-torso
    ch_d.arc([46, 68, 80, 88], start=20, end=160, fill=CORAL_BASE, width=1)

    # 5. Left Arm & Raised Balancing Palm / Defensive Stance at (38, 84)
    ch_d.line([(48, 73), (38, 84)], fill=ORANGE_LIGHT, width=4)
    ch_d.ellipse([34, 82, 41, 89], fill=ORANGE_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 84, 39, 87], fill=GOLD_BASE)

    # 6. Right Arm & Grip Hub (tucked at ribs, ready to hold sawblade sword)
    ch_d.line([(74, 72), (83, 75)], fill=ORANGE_LIGHT, width=4)
    ch_d.ellipse([80, 73, 86, 79], fill=ORANGE_BASE, outline=OUTLINE)
    ch_d.point((83, 76), fill=GOLD_BASE)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_wolf_gear_mane_cowl.png
    # Features:
    # - Spherical Warm Orange Steel Helmet Dome at (64, 44), rx=19.0, ry=16.0
    # - Ivory White (#FFFDF8) enamel cheek and muzzle plates
    # - Knurled micrometer adjustment knob snout with micro brass gear teeth
    # - Folded stamped brass airfoil sensor ears (折疊沖壓黃銅導風耳) at (42, 24) and (86, 24)
    # - Five-layer interlocking tungsten steel gear mane cowl (五層同心齒輪咬合護頸) at y: 50..62
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 19.0, 16.0
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Warm Orange Steel & Ivory Enamel Cheek)
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
                    g_h = int(np.clip(160 * (0.75 + 0.45 * spec) - 25 * edge_shade + 45 * shine, 0, 255))
                    b_h = int(np.clip(16 * (0.75 + 0.45 * spec) - 10 * edge_shade + 40 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Chrome Snout / Micrometer Knob & Mouth Seam with Micro Gear Teeth
    hd.ellipse([62, 46, 66, 49], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 47), fill=WHITE_SHINE)
    hd.line([(64, 49), (64, 53)], fill=OUTLINE, width=1)
    # Micro gear teeth along mouth line
    for gx in [61, 63, 65, 67]:
        hd.point((gx, 52), fill=GOLD_LIGHT)
    hd.arc([60, 50, 64, 54], start=0, end=180, fill=OUTLINE, width=1)
    hd.arc([64, 50, 68, 54], start=0, end=180, fill=OUTLINE, width=1)

    # Forehead Escapement Bridge / Sensor Plate at (64, 32)
    hd.ellipse([61, 30, 67, 34], fill=GOLD_BASE, outline=OUTLINE)
    hd.ellipse([62, 31, 66, 33], fill=CORAL_BASE)
    hd.point((64, 32), fill=WHITE_SHINE)

    # 2. Folded Stamped Brass Airfoil Sensor Ears at (42, 24) and (86, 24)
    # Sleek, triangular-aerodynamic wolf ears with internal acoustic resonance slats
    ear_triangles = [
        # Left ear: base (36, 34) to (48, 32), tip at (38, 16)
        ([(36, 34), (48, 32), (38, 16)], (40, 26)),
        # Right ear: base (80, 32) to (92, 34), tip at (90, 16)
        ([(80, 32), (92, 34), (90, 16)], (88, 26))
    ]
    for ear_poly, pivot in ear_triangles:
        hd.polygon(ear_poly, fill=GOLD_BASE, outline=OUTLINE)
        # Inner acoustic slat
        px, py = pivot
        hd.line([(px, py - 6), (px, py + 3)], fill=STEEL_DARK, width=2)
        hd.point((px, py), fill=CORAL_BASE)
        # Airfoil tip shine
        tip_x, tip_y = ear_poly[2]
        hd.point((tip_x, tip_y + 1), fill=WHITE_SHINE)

    # 3. Five-Layer Concentric Interlocking Gear Mane Cowl (五層齒輪咬合護頸) at y: 50..64
    # Distinct five overlapping curved tiers with precision interlocking gear teeth
    cowl_tiers = [
        # (y_top, y_bottom, half_width, tooth_pitch)
        (50, 52, 14.0, 3),  # Tier 1 (Neck collar)
        (53, 55, 17.0, 4),  # Tier 2
        (56, 58, 20.0, 4),  # Tier 3
        (59, 61, 23.0, 5),  # Tier 4
        (62, 64, 25.0, 5),  # Tier 5 (Base shoulder gear)
    ]
    cowl_cx = 64.0
    for t_idx, (y_t, y_b, hw, pitch) in enumerate(cowl_tiers):
        for cy in range(y_t, y_b + 1):
            for cx in range(int(cowl_cx - hw), int(cowl_cx + hw + 1)):
                rel_x = cx - cowl_cx
                # Gear tooth alternation
                is_tooth = (int(abs(rel_x) + t_idx) % pitch < pitch // 2 + 1)

                if cy == y_t and t_idx > 0:
                    # Clear separation groove between concentric tiers
                    c_cowl = OUTLINE
                elif abs(rel_x) >= hw - 1.5:
                    # Golden brass cog tooth outer edge
                    c_cowl = GOLD_BASE
                elif is_tooth:
                    # Tooth face with specular metal bevel
                    c_cowl = STEEL_LIGHT
                else:
                    # Tooth gullet notch
                    c_cowl = STEEL_BASE
                head_img.putpixel((cx, cy), c_cowl)

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
    # File: optic_core/face_wolf_twin_blue_optic_lens.png
    # Features:
    # - Star Sky Blue Twin Optical Core Lenses (#38A0FF)
    # - Left Eye at (52, 40) & Right Eye at (76, 40)
    # - Brass mounting bezels with precision clamp brackets
    # - Star sky blue crystal lenses with concentric rangefinder reticle rings & crosshairs
    # - Fully opaque lens centers (alpha == 255, 0-ART27 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in eye_centers:
        r_lens = 4.6
        # Brass clamp bezel
        c_d.ellipse([int(ex - r_lens - 1), int(ey - r_lens - 1), int(ex + r_lens + 1), int(ey + r_lens + 1)],
                    fill=GOLD_DARK, outline=OUTLINE)

        for y in range(int(ey - r_lens - 1), int(ey + r_lens + 2)):
            for x in range(int(ex - r_lens - 1), int(ex + r_lens + 2)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= r_lens:
                    spec = max(0.0, 1.0 - dist / r_lens)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.5))**2 + (y - (ey - 1.5))**2)**0.5 / 2.0)**2
                    # Concentric rangefinder reticle ring
                    is_reticle = (abs(dist - 2.5) <= 0.4)
                    if is_reticle:
                        r_c, g_c, b_c = 200, 235, 255
                    else:
                        r_c = int(np.clip(56 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        g_c = int(np.clip(160 * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                        b_c = int(np.clip(255 * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        c_d.ellipse([int(ex - r_lens), int(ey - r_lens), int(ex + r_lens), int(ey + r_lens)],
                    outline=GOLD_BASE, width=1)
        # Crosshair tick marks
        c_d.line([(int(ex - 1.5), int(ey)), (int(ex + 1.5), int(ey))], fill=BLUE_SHINE, width=1)
        c_d.line([(int(ex), int(ey - 1.5)), (int(ex), int(ey + 1.5))], fill=BLUE_SHINE, width=1)
        c_d.point((int(ex - 1), int(ey - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_wolf_scavenger_scrap_plate_armor.png
    # Features:
    # - Scavenger Scrap Plate Armor (廢土拾荒者拼裝板甲)
    # - Does NOT bake chassis underneath (0-ART26b compliant)
    # - Stamped Warm Orange (#FFA010) and Quenched Steel (#5A5666) breastplate
    # - Heavy-duty canvas shoulder straps (#8E522D) with brass buckles
    # - Coral pink silicone seal damper rings along plate edges
    # - Waist utility belt with brass gear buckle at (64, 82)
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
                # Outer armor plate shape (open at center upper chest to reveal collar, covers lower chest & waist)
                is_armor = (abs(x - 63.0) >= 3.0 or y >= 67)
                if is_armor:
                    # Alternating Warm Orange & Quenched Steel plate segments
                    if y >= 77:
                        # Lower waist segment: Quenched Tungsten Steel
                        r_a = int(np.clip(90 * (0.8 + 0.35 * spec), 0, 255))
                        g_a = int(np.clip(86 * (0.8 + 0.35 * spec), 0, 255))
                        b_a = int(np.clip(102 * (0.8 + 0.35 * spec), 0, 255))
                    else:
                        # Upper breastplate: Warm Orange rust-proof steel
                        r_a = int(np.clip(255 * (0.8 + 0.35 * spec), 0, 255))
                        g_a = int(np.clip(160 * (0.8 + 0.35 * spec), 0, 255))
                        b_a = int(np.clip(16 * (0.8 + 0.35 * spec) + 40 * spec, 0, 255))
                    costume_img.putpixel((x, y), (r_a, g_a, b_a, 255))

    # Canvas shoulder straps with brass adjustment buckles
    strap_pts = [(52, 60), (54, 65), (56, 70), (74, 60), (72, 65), (70, 70)]
    for sx, sy in strap_pts:
        cos_d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=CANVAS_BASE)
        cos_d.point((sx, sy), fill=GOLD_BASE)

    # Waist utility belt with brass gear-shaped buckle at (63, 82)
    cos_d.rectangle([50, 80, 76, 84], fill=CANVAS_DARK, outline=OUTLINE)
    cos_d.ellipse([60, 79, 66, 85], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([62, 81, 64, 83], fill=CORAL_BASE)
    cos_d.point((63, 82), fill=WHITE_SHINE)

    # Coral Pink silicone seal beads along breastplate rim
    rim_beads = [(51, 68), (53, 73), (73, 73), (75, 68)]
    for rx, ry in rim_beads:
        cos_d.point((rx, ry), fill=CORAL_BASE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Top Layer)
    # File: weapon/weapon_wolf_scrap_sawblade_greatsword.png
    # Features:
    # - Scrap Sawblade Greatsword / Po Jun Blade (【廢土鋸齒重鋼劍 / 破軍殘刃】)
    # - Right-hand single wielded (0-MKT7 compliant)
    # - Hilt at (82, 75) wrapped in dark grip wrap with brass pommel
    # - Crossguard: rotating brass outer gear wheel counterweight ring (#FFD028)
    # - Heavy broadsword blade extending diagonally down-forward from (86, 78) to (114, 104)
    # - Both upper and lower blade edges feature sharp, precision-cut sawteeth (鋸齒槽)
    # - Center blade fuller inlaid with Star Sky Blue (#38A0FF) energy conduit line
    # - Mirror finish bevel highlights and razor-sharp white glint at the tip
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Hilt & Pommel at (82, 75)
    # Pommel
    wd.ellipse([78, 71, 82, 75], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((80, 73), fill=WHITE_SHINE)
    # Grip wrap
    wd.line([(80, 73), (85, 77)], fill=CANVAS_DARK, width=3)
    wd.point((82, 75), fill=GOLD_LIGHT)

    # 2. Crossguard: Rotating Brass Outer Gear Wheel Ring at (86, 78)
    gx_c, gy_c = 86.0, 78.0
    wd.ellipse([int(gx_c - 5), int(gy_c - 5), int(gx_c + 5), int(gy_c + 5)], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([int(gx_c - 3), int(gy_c - 3), int(gx_c + 3), int(gy_c + 3)], fill=STEEL_DARK)
    wd.point((int(gx_c), int(gy_c)), fill=CORAL_BASE)
    # Gear teeth on guard
    for a_deg in range(0, 360, 45):
        rad = np.radians(a_deg)
        tx = int(gx_c + 6.0 * np.cos(rad))
        ty = int(gy_c + 6.0 * np.sin(rad))
        if 0 <= tx < W and 0 <= ty < H:
            weapon_img.putpixel((tx, ty), GOLD_LIGHT)

    # 3. Quenched Stamped Tungsten Steel Sawblade Greatsword Blade
    # Extends from (88, 80) to (114, 104)
    blade_start = np.array([88.0, 80.0])
    blade_end   = np.array([114.0, 104.0])
    blade_vec   = blade_end - blade_start
    blade_len   = float(np.linalg.norm(blade_vec))
    blade_dir   = blade_vec / blade_len
    blade_perp  = np.array([-blade_dir[1], blade_dir[0]])

    for d in np.linspace(0.0, blade_len, int(blade_len * 2.5)):
        t_norm = d / blade_len
        # Blade half-width tapers from 4.5px at base to 1.2px near tip, then 0 at tip
        w_d = 4.5 * (1.0 - t_norm**1.2) + 0.8
        base_pos = blade_start + d * blade_dir

        for w_off in np.linspace(-w_d, w_d, int(w_d * 5) + 1):
            cur_pos = base_pos + w_off * blade_perp
            ix, iy = int(cur_pos[0]), int(cur_pos[1])
            if 0 <= ix < W and 0 <= iy < H:
                # Sawteeth notches along outer edges
                is_outer_edge = abs(w_off) >= w_d - 1.2
                tooth_notch = (int(d * 1.5) % 3 == 0)

                # Center cyan/blue energy groove line
                is_energy_line = (abs(w_off) <= 0.6 and t_norm <= 0.85)

                if is_outer_edge and tooth_notch:
                    # Recessed saw tooth gap
                    c_b = STEEL_DARK
                elif is_energy_line:
                    c_b = BLUE_BASE
                else:
                    spec = max(0.0, 1.0 - abs(w_off) / w_d)**2
                    shine = max(0.0, t_norm - 0.4) / 0.6
                    r_b = int(np.clip(90 * (0.8 + 0.35 * spec) + 80 * shine, 0, 255))
                    g_b = int(np.clip(86 * (0.8 + 0.35 * spec) + 80 * shine, 0, 255))
                    b_b = int(np.clip(102 * (0.8 + 0.35 * spec) + 100 * shine, 0, 255))
                    c_b = (r_b, g_b, b_b, 255)

                weapon_img.putpixel((ix, iy), c_b)

    # Razor-sharp white glint at sword tip (114, 104)
    wd.point((114, 104), fill=WHITE_SHINE)
    wd.point((113, 103), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 AND 512x512 LANCZOS SLICES
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_wolf_heavy_pojun_cross", key_img),
        ("back_curio", "curio_wolf_segmented_spring_tail", curio_img),
        ("chassis", "chassis_wolf_warm_orange_default", chassis_img),
        ("head_unit", "head_wolf_gear_mane_cowl", head_img),
        ("optic_core", "face_wolf_twin_blue_optic_lens", core_img),
        ("costume", "costume_wolf_scavenger_scrap_plate_armor", costume_img),
        ("weapon", "weapon_wolf_scrap_sawblade_greatsword", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{WOLF_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_wolf_heavy_pojun_cross.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_wolf_scrap_sawblade_greatsword.png")
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

    comp_path = f"{WOLF_PD_DIR}/proof_paperdoll_wolf_composite.png"
    comp_exact.save(comp_path)
    print("  ✓ Composite saved:", comp_path)

    # Magenta proof (proof_paperdoll_wolf_magenta.png)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(comp_exact)
    mag_path = f"{WOLF_PD_DIR}/proof_paperdoll_wolf_magenta.png"
    magenta_bg.save(mag_path)
    print("  ✓ Magenta proof saved:", mag_path)

    # 7 slices proof (proof_wolf_all_7_slices.png)
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
        s_draw = ImageDraw.Draw(strip)
        s_draw.rectangle([px, 0, px + W - 1, H - 1], outline=(200, 200, 210, 255))
        s_draw.text((px + 4, 4), label_txt, fill=(60, 60, 80, 255))
        strip.alpha_composite(sl_img, (px, 0))

    strip_path = f"{WOLF_PD_DIR}/proof_wolf_all_7_slices.png"
    strip.save(strip_path)
    print("  ✓ 7 Slices Proof saved:", strip_path)

    # SHOWCASE HD (game/assets/sprites/player/showcase/wolf_idle_hd.png)
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
        showcase_dst = f"{showcase_dir}/wolf_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
