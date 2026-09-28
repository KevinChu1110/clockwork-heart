#!/usr/bin/env python3
"""
build_courser_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十七族 鐵蹄駿駒 (The Ironhoof Courser, courser) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/IRONHOOF_COURSER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped ivory enamel plates,
  cold-rolled tungsten steel framework, gilded brass gear-wave mane, baroque trefoil filigree winding key)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Polished Cream White Enamel (#FFFDF8)
    2. Secondary Hull / Trim: Dawn Warm Orange (#FFA010)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Sky Sapphire: Sky Sapphire Blue (#38A0FF)
    6. Cute Coral Pink: Coral Pink (#FF5E8A)
    7. Cold Stamped Tungsten Steel: Tungsten Gray (#3A3644)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
COURSER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/courser"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Ironhoof Courser Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Polished Cream White Enamel (#FFFDF8)
CREAM_BASE  = (255, 253, 248, 255)
CREAM_LIGHT = (255, 255, 255, 255)
CREAM_SHADE = (235, 228, 218, 255)
CREAM_DARK  = (205, 196, 182, 255)
CREAM_DEEP  = (168, 158, 144, 255)

# 2. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Dawn Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (195, 110, 8, 255)
ORANGE_DEEP  = (135, 70, 5, 255)

# 4. Fresh Mint Green (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 5. Sky Sapphire Optic Lens & Indicator Jewels (#38A0FF)
SAPPHIRE_BASE  = (56, 160, 255, 255)
SAPPHIRE_LIGHT = (120, 205, 255, 255)
SAPPHIRE_SHINE = (195, 235, 255, 255)
SAPPHIRE_DARK  = (24, 105, 195, 255)
SAPPHIRE_DEEP  = (14, 60, 130, 255)

# 6. Cute Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_DARK  = (195, 55, 95, 255)

# 7. Cold Stamped Tungsten Steel (#3A3644)
TUNGSTEN_BASE  = (58, 54, 68, 255)
TUNGSTEN_LIGHT = (96, 92, 110, 255)
TUNGSTEN_SHINE = (135, 130, 150, 255)
TUNGSTEN_DARK  = (38, 35, 46, 255)
TUNGSTEN_DEEP  = (24, 22, 30, 255)

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
                # Check 8 neighbors in snapshot
                has_solid_neighbor = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            if px_snap[nx, ny][3] >= min_alpha:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL IRONHOOF COURSER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_courser_baroque_trefoil_gold.png
    # Baroque Trefoil Filigree Winding Key (巴洛克雙聯三葉草金飾發條鑰匙)
    # Features:
    # - Socket boss at upper back (64, 58)
    # - Heavy polished brass key shaft extends up-right to trefoil hub at (92, 22)
    # - Double trefoil openwork wings: left trefoil at (80, 18), right trefoil at (104, 18)
    # - Center sapphire gem bearing at (92, 22)
    # - Finial crown at (92, 10)
    # - Warm golden bronze outline (OUTLINE_KEY = (140, 110, 25, 255))
    # - STRICTLY transparent corners & 0-ART29 dark limit (dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from socket (64, 58) to hub (92, 22)
    for t in np.linspace(0.0, 1.0, 60):
        sx = 64.0 + t * 28.0
        sy = 58.0 - t * 36.0
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
    kd.ellipse([64 - 1, 58 - 1, 64 + 1, 58 + 1], fill=SAPPHIRE_BASE)

    # 2. Central Hub at (92, 22)
    kcx, kcy = 92.0, 22.0
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            d = (dx**2 + dy**2)**0.5
            if d <= 7.0:
                spec = max(0.0, 1.0 - d / 7.0)
                shine = max(0.0, 1.0 - ((dx + 2)**2 + (dy + 2)**2)**0.5 / 5.0)
                r_g = int(np.clip(255 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                g_g = int(np.clip(208 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 45 * shine, 0, 255))
                key_img.putpixel((int(kcx + dx), int(kcy + dy)), (r_g, g_g, b_g, 255))

    # Center sapphire gem bearing
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

    # 3. Baroque Double Trefoil Wings
    # Left wing center ~ (80, 20): 3 lobes at angles: up (80, 13), left (73, 20), down (80, 27)
    left_lobes = [(80, 13), (73, 20), (80, 27)]
    for lx, ly in left_lobes:
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                d = (dx**2 + dy**2)**0.5
                if 2.0 <= d <= 5.2:
                    spec = max(0.0, 1.0 - abs(d - 3.5) / 1.8)
                    shine = max(0.0, 1.0 - ((dx + 1)**2 + (dy + 1)**2)**0.5 / 4.0)
                    r_g = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    g_g = int(np.clip(208 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * shine, 0, 255))
                    key_img.putpixel((lx + dx, ly + dy), (r_g, g_g, b_g, 255))

    # Left bridge from hub to lobes
    for t in np.linspace(0.0, 1.0, 25):
        bx = int(round(kcx * (1 - t) + 80.0 * t))
        by = int(round(kcy * (1 - t) + 20.0 * t))
        for dy in (-1, 0, 1):
            key_img.putpixel((bx, by + dy), GOLD_LIGHT)

    # Right wing center ~ (104, 20): 3 lobes at angles: up (104, 13), right (111, 20), down (104, 27)
    right_lobes = [(104, 13), (111, 20), (104, 27)]
    for rx, ry in right_lobes:
        for dx in range(-5, 6):
            for dy in range(-5, 6):
                d = (dx**2 + dy**2)**0.5
                if 2.0 <= d <= 5.2:
                    spec = max(0.0, 1.0 - abs(d - 3.5) / 1.8)
                    shine = max(0.0, 1.0 - ((dx - 1)**2 + (dy + 1)**2)**0.5 / 4.0)
                    r_g = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    g_g = int(np.clip(208 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * shine, 0, 255))
                    key_img.putpixel((rx + dx, ry + dy), (r_g, g_g, b_g, 255))

    # Right bridge from hub to lobes
    for t in np.linspace(0.0, 1.0, 25):
        bx = int(round(kcx * (1 - t) + 104.0 * t))
        by = int(round(kcy * (1 - t) + 20.0 * t))
        for dy in (-1, 0, 1):
            key_img.putpixel((bx, by + dy), GOLD_LIGHT)

    # 4. Top Crown Finial at (92, 10)
    kd.polygon([(int(kcx), 6), (int(kcx - 4), 13), (int(kcx + 4), 13)], fill=GOLD_LIGHT, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 2), 6, int(kcx + 2), 10], fill=GOLD_SHINE)

    # Clean outline pass with warm bronze outline (OUTLINE_KEY) to avoid dark limit violations
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict 0-ART29 transparent corners
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_courser_articulated_spring_tail.png
    # Articulated Spring-Coil Tail (鉸接多節彈簧金屬流線甩尾)
    # Features:
    # - Originates from pelvis/rump at (44, 82)
    # - 5 tapering articulated polished brass cone segments connected by spring coils
    #   sweeping back and down to (20, 110)
    # - Clockwork dangling gear bell at tip (20, 112)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Nodes along tail spline
    tail_nodes = [
        (44.0, 82.0, 5.0),   # Base segment 1
        (38.0, 87.0, 4.5),   # Segment 2
        (32.0, 93.0, 4.0),   # Segment 3
        (26.0, 100.0, 3.5),  # Segment 4
        (22.0, 107.0, 3.0),  # Segment 5
    ]

    # Draw spring coils between nodes
    for i in range(len(tail_nodes) - 1):
        x1, y1, r1 = tail_nodes[i]
        x2, y2, r2 = tail_nodes[i + 1]
        for t in np.linspace(0.0, 1.0, 30):
            tx = x1 * (1 - t) + x2 * t
            ty = y1 * (1 - t) + y2 * t
            rad = r1 * (1 - t) + r2 * t
            # Draw brass cone sleeve
            for dx in np.linspace(-rad, rad, int(rad * 2) + 2):
                for dy in np.linspace(-rad, rad, int(rad * 2) + 2):
                    if dx**2 + dy**2 <= rad**2:
                        spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / rad)
                        shine = max(0.0, 1.0 - abs(dy + 0.5 * dx) / rad)
                        r_b = int(np.clip(255 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                        g_b = int(np.clip(208 * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                        b_b = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * shine, 0, 255))
                        curio_img.putpixel((int(round(tx + dx)), int(round(ty + dy))), (r_b, g_b, b_b, 255))

        # Spring coil joint between segments
        jx = int(round((x1 + x2) * 0.5))
        jy = int(round((y1 + y2) * 0.5))
        cd.ellipse([jx - 2, jy - 2, jx + 2, jy + 2], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
        cd.point((jx, jy), fill=WHITE_SHINE)

    # Dangling Brass Gear Bell at tip (20, 112)
    bx, by = 20, 112
    cd.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=GOLD_BASE, outline=OUTLINE)
    cd.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=GOLD_LIGHT)
    cd.point((bx, by), fill=WHITE_SHINE)
    # Bell clapper / gear teeth
    for ang in np.linspace(0, 2 * np.pi, 6, endpoint=False):
        gx = int(round(bx + 4.5 * np.cos(ang)))
        gy = int(round(by + 4.5 * np.sin(ang)))
        curio_img.putpixel((gx, gy), GOLD_LIGHT)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Core Body Layer)
    # File: chassis_courser_cream_gold_default.png
    # Cream Gold Default Alloy Chassis (鐵蹄駿駒奶油金黃合金素體)
    # Features:
    # - 2.2 head-tall chibi toy horse frame
    # - Cream White Enamel plates with rich multi-tone depth (>=20 unique colors in torso)
    # - Horse head cranium & muzzle with plate seams, brass nostrils rivets, coral pink cheek blush
    # - Articulated ball-and-socket limbs
    # - Tungsten steel horseshoe footplates at base (y: 114..120)
    # - STRICT 0-ART9/11 COMPLIANCE: strictly 0 pixels at x >= 94
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Legs and Hoofplates
    # Left leg: Thigh (46..54, 84..96), Knee (48, 97), Shin (46..52, 98..114), Hoof (42..54, 114..120)
    # Right leg: Thigh (74..82, 84..96), Knee (78, 97), Shin (76..82, 98..114), Hoof (74..86, 114..120)
    for leg_cx, leg_name in [(48.0, "left"), (78.0, "right")]:
        # Thigh (cream enamel)
        for y in range(84, 98):
            for x in range(int(leg_cx - 6), int(leg_cx + 7)):
                spec = max(0.0, 1.0 - abs(x - leg_cx) / 6.0)
                sh = max(0.0, (y - 84) / 14.0)
                r_c = int(np.clip(255 * (0.95 - 0.2 * sh + 0.15 * spec), 0, 255))
                g_c = int(np.clip(253 * (0.95 - 0.2 * sh + 0.15 * spec), 0, 255))
                b_c = int(np.clip(248 * (0.95 - 0.25 * sh + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        # Knee Ball-Joint (brass)
        chd.ellipse([int(leg_cx - 5), 94, int(leg_cx + 5), 102], fill=GOLD_BASE, outline=OUTLINE)
        chd.ellipse([int(leg_cx - 3), 96, int(leg_cx + 3), 100], fill=GOLD_LIGHT)
        chd.point((int(leg_cx), 98), fill=WHITE_SHINE)

        # Shin (cream enamel with suspension groove)
        for y in range(100, 115):
            for x in range(int(leg_cx - 5), int(leg_cx + 6)):
                spec = max(0.0, 1.0 - abs(x - leg_cx) / 5.0)
                sh = max(0.0, (y - 100) / 15.0)
                r_c = int(np.clip(255 * (0.95 - 0.18 * sh + 0.15 * spec), 0, 255))
                g_c = int(np.clip(253 * (0.95 - 0.18 * sh + 0.15 * spec), 0, 255))
                b_c = int(np.clip(248 * (0.95 - 0.22 * sh + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        # Horseshoe Footplate (Stamped Tungsten Steel with brass trim & ground rubber pad)
        for y in range(114, 121):
            for x in range(int(leg_cx - 7), int(leg_cx + 8)):
                t_spec = max(0.0, 1.0 - abs(x - leg_cx) / 7.0)
                if y == 114:
                    chassis_img.putpixel((x, y), GOLD_BASE)
                elif y < 119:
                    r_t = int(np.clip(58 * (0.85 + 0.4 * t_spec), 0, 255))
                    g_t = int(np.clip(54 * (0.85 + 0.4 * t_spec), 0, 255))
                    b_t = int(np.clip(68 * (0.85 + 0.4 * t_spec), 0, 255))
                    chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))
                else:
                    # Bottom non-slip pad
                    chassis_img.putpixel((x, y), (28, 25, 34, 255))
        chd.line([(int(leg_cx - 5), 116), (int(leg_cx + 5), 116)], fill=TUNGSTEN_SHINE, width=1)

    # 2. Main Torso / Pelvis (x: 44..84, y: 58..94)
    # Rich multi-tone shading to guarantee 0-ART18 (>=20 unique colors in [58:94, 44:84])
    tcx, tcy = 64.0, 75.0
    for y in range(58, 95):
        for x in range(44, 85):
            dx = (x - tcx) / 19.0
            dy = (y - tcy) / 17.0
            if dx**2 + dy**2 <= 1.05:
                # Radial spherical lighting + vertical gravity gradient
                dist = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 68.0)**2)**0.5 / 18.0)
                sh_y = (y - 58.0) / 36.0
                r_e = int(np.clip(255 * (0.96 - 0.22 * sh_y + 0.16 * spec), 0, 255))
                g_e = int(np.clip(253 * (0.96 - 0.24 * sh_y + 0.16 * spec), 0, 255))
                b_e = int(np.clip(248 * (0.96 - 0.30 * sh_y + 0.16 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    # Torso Brass Panel Seams, Screws & Clockwork Heart Socket
    chd.arc([47, 62, 81, 90], start=10, end=170, fill=GOLD_BASE, width=1)
    chd.line([(52, 78), (76, 78)], fill=GOLD_BASE, width=1)
    # Corner brass rivets
    for rx, ry in [(48, 64), (80, 64), (48, 86), (80, 86)]:
        chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
        chd.point((rx, ry), fill=WHITE_SHINE)

    # Central Core Socket Ring at (64, 72)
    chd.ellipse([58, 66, 70, 78], fill=GOLD_BASE, outline=OUTLINE)
    chd.ellipse([60, 68, 68, 76], fill=CREAM_DARK)
    chd.ellipse([62, 70, 66, 74], fill=GOLD_SHINE)

    # 3. Arms / Forelimbs
    # Left Arm (viewer's left): Shoulder (44, 64), Elbow (38, 72), Hand (40, 78) holding rein strap
    for y in range(64, 80):
        for x in range(36, 46):
            if ((x - 41) / 4.5)**2 + ((y - 71) / 7.5)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 41) / 4.5)
                r_a = int(np.clip(255 * (0.92 + 0.15 * spec), 0, 255))
                g_a = int(np.clip(253 * (0.92 + 0.15 * spec), 0, 255))
                b_a = int(np.clip(248 * (0.92 + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    chd.ellipse([38, 75, 43, 80], fill=GOLD_BASE, outline=OUTLINE)  # Brass toy hand clamp

    # Right Arm (viewer's right): Shoulder (84, 64), Elbow (88, 70), Hand (89, 74)
    # STRICT 0-ART9/11 RULE: strictly x <= 92 (no pixels at x >= 94)
    for y in range(64, 76):
        for x in range(83, 93):  # strictly up to 92
            if ((x - 87) / 5.0)**2 + ((y - 69) / 6.0)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 87) / 5.0)
                r_a = int(np.clip(255 * (0.92 + 0.15 * spec), 0, 255))
                g_a = int(np.clip(253 * (0.92 + 0.15 * spec), 0, 255))
                b_a = int(np.clip(248 * (0.92 + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    chd.ellipse([87, 71, 92, 76], fill=GOLD_BASE, outline=OUTLINE)  # Brass toy weapon clamp (x <= 92)

    # 4. Neck & Cranial Shell (Head)
    # Neck (58..70, 50..60)
    for y in range(50, 61):
        for x in range(58, 71):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 6.0)
            r_n = int(np.clip(255 * (0.88 + 0.2 * spec), 0, 255))
            g_n = int(np.clip(253 * (0.88 + 0.2 * spec), 0, 255))
            b_n = int(np.clip(248 * (0.88 + 0.2 * spec), 0, 255))
            chassis_img.putpixel((x, y), (r_n, g_n, b_n, 255))
    chd.line([(58, 54), (70, 54)], fill=GOLD_BASE, width=1)
    chd.line([(58, 58), (70, 58)], fill=GOLD_BASE, width=1)

    # Head Cranial Shell: Center (64, 36), radius x: 21, radius y: 18
    hcx, hcy = 64.0, 36.0
    for y in range(18, 52):
        for x in range(43, 86):
            dx = (x - hcx) / 21.0
            dy = (y - hcy) / 17.5
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 16.0)
                sh_y = (y - 18.0) / 33.0
                r_h = int(np.clip(255 * (0.96 - 0.18 * sh_y + 0.18 * spec), 0, 255))
                g_h = int(np.clip(253 * (0.96 - 0.20 * sh_y + 0.18 * spec), 0, 255))
                b_h = int(np.clip(248 * (0.96 - 0.26 * sh_y + 0.18 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Muzzle / Snout: Center (64, 48), width x: 54..74, height y: 44..56
    for y in range(44, 57):
        for x in range(54, 75):
            dx = (x - 64.0) / 10.0
            dy = (y - 50.0) / 6.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 10.0)
                r_m = int(np.clip(255 * (0.92 + 0.15 * spec), 0, 255))
                g_m = int(np.clip(253 * (0.92 + 0.15 * spec), 0, 255))
                b_m = int(np.clip(248 * (0.92 + 0.15 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_m, g_m, b_m, 255))

    # Snout nostrils plate (stamped brass plate with two tiny mechanical nostrils)
    chd.rounded_rectangle([58, 51, 70, 55], radius=2, fill=CREAM_DARK, outline=OUTLINE)
    # Dual nostrils (stamped brass slots)
    chd.rectangle([60, 52, 62, 54], fill=GOLD_BASE, outline=OUTLINE)
    chd.rectangle([66, 52, 68, 54], fill=GOLD_BASE, outline=OUTLINE)

    # Cheek Blush Roundels in Coral Pink (#FF5E8A)
    for bx, by in [(46, 45), (82, 45)]:
        chd.ellipse([bx - 3, by - 2, bx + 3, by + 2], fill=CORAL_BASE)
        chd.point((bx, by), fill=CORAL_LIGHT)

    # Eye Socket Under-rings (deepened socket shadow ready for optic_core)
    for ex in [52, 76]:
        chd.ellipse([ex - 5, 40 - 5, ex + 5, 40 + 5], fill=CREAM_DARK, outline=OUTLINE)

    # Clean outline pass
    apply_clean_outline(chassis_img)

    # Strict check: 0-ART9/11 compliance - verify zero pixels at x >= 94
    ch_arr = np.array(chassis_img)
    if np.any(ch_arr[:, 94:, 3] > 0):
        print("  ⚠️ Trimming chassis pixels at x >= 94 for 0-ART9/11 compliance...")
        for y in range(H):
            for x in range(94, W):
                chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20, Head & Mane Layer)
    # File: head_unit/head_courser_brass_chanfron_mane.png
    # Baroque Stamped Brass Chanfron & Gear-Wave Mane (巴洛克沖壓黃銅護面額甲與波浪齒輪鬃甲)
    # Features:
    # 1. Stamped Gilded Gear-Wave Crest Mane (7 stepped gear cogs along crest midline y: 8..34, x: 58..70)
    # 2. Upright rigid metal ears: left (40..48, 10..26), right (80..88, 10..26)
    # 3. Baroque Stamped Brass Chanfron running down forehead (60..68, 24..48)
    # 4. STRICT 0-ART27 COMPLIANCE: Eye sockets at (52, 40) and (76, 40) MUST BE 100% HOLLOW!
    #    (alpha == 0 in boxes [38..42, 50..54] and [38..42, 74..78])
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Upright Rigid Metal Ears
    # Left Ear: tip at (42, 10), base at (46, 26)
    ear_l = [(42, 10), (48, 18), (49, 26), (43, 26), (39, 18)]
    hd.polygon(ear_l, fill=GOLD_BASE, outline=OUTLINE)
    # Left ear inner acoustic channel (coral pink / brass highlight)
    hd.polygon([(42, 13), (46, 18), (47, 24), (43, 24), (40, 18)], fill=CORAL_BASE)
    hd.point((43, 16), fill=CORAL_LIGHT)

    # Right Ear: tip at (86, 10), base at (82, 26)
    ear_r = [(86, 10), (89, 18), (85, 26), (79, 26), (80, 18)]
    hd.polygon(ear_r, fill=GOLD_BASE, outline=OUTLINE)
    # Right ear inner acoustic channel
    hd.polygon([(86, 13), (88, 18), (85, 24), (81, 24), (82, 18)], fill=CORAL_BASE)
    hd.point((85, 16), fill=CORAL_LIGHT)

    # 2. Stamped Gilded Gear-Wave Crest Mane (7 stepped gear teeth along crest y: 8..34, x: 58..70)
    # Gear teeth wave profile
    mane_teeth = [
        (64.0, 9.0, 6.0, 3.0),
        (64.0, 13.0, 7.0, 3.0),
        (64.0, 17.0, 7.5, 3.0),
        (64.0, 21.0, 8.0, 3.0),
        (64.0, 25.0, 8.0, 3.0),
        (64.0, 29.0, 7.5, 3.0),
        (64.0, 33.0, 7.0, 3.0),
    ]
    for mx, my, mrx, mry in mane_teeth:
        for y in range(int(my - mry), int(my + mry + 1)):
            for x in range(int(mx - mrx), int(mx + mrx + 1)):
                if ((x - mx) / mrx)**2 + ((y - my) / mry)**2 <= 1.0:
                    spec = max(0.0, 1.0 - abs(x - mx) / mrx)
                    r_m = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                    g_m = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
                    b_m = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
                    head_img.putpixel((x, y), (r_m, g_m, b_m, 255))
        # Central crest ridge highlight
        hd.line([(int(mx), int(my - mry + 1)), (int(mx), int(my + mry - 1))], fill=GOLD_SHINE, width=1)

    # 3. Baroque Stamped Brass Chanfron (護面額甲)
    # Extends down forehead midline: x: 60..68, y: 24..48 (leaving x: 50..55 and x: 73..78 completely clear)
    for y in range(24, 49):
        # Tapering chanfron shape
        w_half = 3.5 if y < 32 else (4.0 if y < 42 else 3.0)
        for x in range(int(64.0 - w_half), int(64.0 + w_half + 1)):
            spec = max(0.0, 1.0 - abs(x - 64.0) / w_half)
            r_c = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
            g_c = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
            b_c = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
            head_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Baroque Filigree Trefoil Emblem on Chanfron at (64, 28)
    hd.ellipse([61, 26, 67, 32], fill=GOLD_DARK, outline=OUTLINE)
    hd.ellipse([62, 27, 66, 31], fill=SAPPHIRE_BASE)
    hd.point((64, 29), fill=WHITE_SHINE)

    # Rivets along chanfron nose bridge
    for ry in [36, 42, 47]:
        hd.ellipse([63, ry - 1, 65, ry + 1], fill=GOLD_SHINE, outline=OUTLINE)

    # Clean outline pass with strict ignore_regions for eye sockets to guarantee 0-ART27 compliance!
    # Left eye socket zone: [37..43, 49..55], Right eye socket zone: [37..43, 73..79]
    eye_ignore = [(48, 36, 56, 44), (72, 36, 80, 44)]
    apply_clean_outline(head_img, ignore_regions=eye_ignore)

    # 4. Enforce STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye regions must have alpha == 0
    for ex in [52, 76]:
        for ey in range(37, 44):
            for exx in range(ex - 3, ex + 4):
                head_img.putpixel((exx, ey), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Chest & Armor Layer)
    # File: costume/costume_courser_dawn_patrol_cuirass.png
    # Dawn Patrol Cuirass (晨曦巡防騎士拋光輕胸甲)
    # Features:
    # - Fits over torso (x: 44..84, y: 60..94)
    # - Polished light breastplate in cream enamel with Dawn Warm Orange (#FFA010) borders
    # - Shoulder pauldrons with gold rivets at (40..48, 62..72) and (80..88, 62..72)
    # - Central chest medallion in Fresh Mint Green (#4ED86A) with gold clover star
    # - Waist saddle girth strap with brass buckle at (64, 88)
    # - STRICT 0-ART26b COMPLIANCE: strictly 0 pixels at y >= 96!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Breastplate Main Shell (x: 46..82, y: 62..93)
    for y in range(62, 94):
        for x in range(46, 83):
            dx = (x - 64.0) / 18.0
            dy = (y - 77.0) / 15.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 16.0)
                sh_y = (y - 62.0) / 32.0
                r_c = int(np.clip(255 * (0.95 - 0.18 * sh_y + 0.16 * spec), 0, 255))
                g_c = int(np.clip(253 * (0.95 - 0.20 * sh_y + 0.16 * spec), 0, 255))
                b_c = int(np.clip(248 * (0.95 - 0.26 * sh_y + 0.16 * spec), 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 2. Dawn Warm Orange Scalloped Trim & Shoulder Guards
    # Pauldrons: Left (40..48, 63..73), Right (80..88, 63..73)
    for px, py_base in [(44, 68), (84, 68)]:
        cosd.ellipse([px - 5, py_base - 5, px + 5, py_base + 5], fill=ORANGE_BASE, outline=OUTLINE)
        cosd.ellipse([px - 3, py_base - 3, px + 3, py_base + 3], fill=ORANGE_LIGHT)
        cosd.point((px, py_base), fill=GOLD_BASE)

    # Orange Trim along Cuirass Collar and Lower Hem
    cosd.arc([47, 62, 81, 72], start=180, end=360, fill=ORANGE_BASE, width=2)
    cosd.arc([48, 80, 80, 92], start=10, end=170, fill=ORANGE_BASE, width=2)

    # 3. Central Mint Green (#4ED86A) Medallion with Gold Clover Star at (64, 73)
    cosd.ellipse([58, 67, 70, 79], fill=GOLD_DARK, outline=OUTLINE)
    cosd.ellipse([59, 68, 69, 78], fill=MINT_BASE, outline=OUTLINE)
    cosd.ellipse([61, 70, 67, 76], fill=MINT_LIGHT)
    # Gold clover star center
    cosd.polygon([(64, 70), (66, 73), (64, 76), (62, 73)], fill=GOLD_SHINE)

    # 4. Waist Saddle Girth Strap & Brass Buckle at (64, 88)
    cosd.rectangle([50, 87, 78, 91], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    cosd.rectangle([61, 86, 67, 92], fill=GOLD_BASE, outline=OUTLINE)
    cosd.point((64, 89), fill=WHITE_SHINE)

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
    # File: optic_core/face_courser_sapphire_optic_lens.png
    # Sky Sapphire Optic Lens (天藍石英同心圓光學目鏡)
    # Features:
    # - Left eye centered at (52, 40), Right eye centered at (76, 40)
    # - High opacity at centers (alpha == 255 > 200, 0-ART27 compliant)
    # - Deep sapphire blue outer ring, bright sky cyan iris, white specular glint
    # - Internal escapement dial tick marks for clockwork personality
    # - Rich color depth to pass 0-QA31 (>=15 unique colors in optic zone)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    for ex in [52, 76]:
        ey = 40
        er = 6.0
        # Multi-tone concentric gradient lens
        for y in range(int(ey - er - 1), int(ey + er + 2)):
            for x in range(int(ex - er - 1), int(ex + er + 2)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= er:
                    ratio = dist / er
                    if ratio <= 0.35:
                        # Inner glowing pupil
                        col = SAPPHIRE_SHINE
                    elif ratio <= 0.65:
                        # Cyan iris ring
                        col = SAPPHIRE_LIGHT
                    elif ratio <= 0.88:
                        # Sapphire midtone
                        col = SAPPHIRE_BASE
                    else:
                        # Deep outer bevel
                        col = SAPPHIRE_DEEP
                    core_img.putpixel((x, y), col)

        # Concentric Escapement Tick Marks & Bevel Ring
        cored.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], outline=SAPPHIRE_DARK)
        cored.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], outline=SAPPHIRE_LIGHT)
        # White specular glints
        core_img.putpixel((ex - 2, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 1, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 2, ey - 1), WHITE_SHINE)
        core_img.putpixel((ex + 1, ey + 1), SAPPHIRE_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Weapon Layer)
    # File: weapon/weapon_courser_cavalry_saber.png
    # Dawn Clockwork Cavalry Saber (晨曦齒輪騎兵劍)
    # Features:
    # - Held in right hand: handgrip at (88..92, 68..74)
    # - Gold brass external gear handguard disk at (90, 68) with 8 teeth
    # - Counterweight pommel with balance spring at (86, 76)
    # - Curved spring-steel single-edged cavalry blade sweeping up and forward:
    #   from (92, 64) -> (98, 48) -> (104, 34) -> tip at (108, 22)
    # - Tempered steel core, polished white cutting edge, gold fuller back-ridge
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Counterweight Balance Pommel & Handgrip
    # Pommel at (86, 76)
    wd.ellipse([84, 74, 88, 78], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((86, 76), fill=WHITE_SHINE)

    # Handgrip: Leather wrapped grip with brass wire winding (88..91, 68..74)
    for y in range(68, 75):
        for x in range(88, 92):
            if (y + x) % 2 == 0:
                weapon_img.putpixel((x, y), GOLD_BASE)
            else:
                weapon_img.putpixel((x, y), TUNGSTEN_DARK)

    # 2. External Gear Handguard Disk at (90, 67)
    hgx, hgy = 90.0, 67.0
    for dy in range(-7, 8):
        for dx in range(-7, 8):
            d = (dx**2 + dy**2)**0.5
            if d <= 6.5:
                spec = max(0.0, 1.0 - d / 6.5)
                shine = max(0.0, 1.0 - ((dx + 1.5)**2 + (dy + 1.5)**2)**0.5 / 4.0)
                r_h = int(np.clip(255 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                g_h = int(np.clip(208 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                b_h = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * shine, 0, 255))
                weapon_img.putpixel((int(hgx + dx), int(hgy + dy)), (r_h, g_h, b_h, 255))
    # Center screw
    wd.ellipse([int(hgx - 2), int(hgy - 2), int(hgx + 2), int(hgy + 2)], fill=GOLD_DARK)
    wd.point((int(hgx), int(hgy)), fill=WHITE_SHINE)

    # 8 Gear Teeth around guard disk
    for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
        tx = int(round(hgx + 6.8 * np.cos(ang)))
        ty = int(round(hgy + 6.8 * np.sin(ang)))
        if 0 <= tx < W and 0 <= ty < H:
            weapon_img.putpixel((tx, ty), GOLD_LIGHT)

    # 3. Curved Cavalry Saber Blade
    # Spline: (92, 64) -> (94, 57) -> (97, 50) -> (100, 43) -> (103, 36) -> (105.5, 29) -> (108, 22)
    blade_pts = [
        (92.0, 64.0),
        (94.0, 57.0),
        (97.0, 50.0),
        (100.0, 43.0),
        (103.0, 36.0),
        (105.5, 29.0),
        (108.0, 22.0)
    ]
    for i in range(len(blade_pts) - 1):
        x1, y1 = blade_pts[i]
        x2, y2 = blade_pts[i + 1]
        for t in np.linspace(0.0, 1.0, 35):
            bx = x1 * (1 - t) + x2 * t
            by = y1 * (1 - t) + y2 * t
            t_len = (i + t) / float(len(blade_pts) - 1)
            # Blade cross section: spine (left/inner) in gold/dark, core in steel, edge (right/outer) in white shine
            for w_off in range(-2, 3):
                px = int(round(bx + w_off * 0.9))
                py = int(round(by - w_off * 0.4))
                if 0 <= px < W and 0 <= py < H:
                    if w_off == -2:
                        # Gold fuller on back spine with gradient
                        r_w = int(np.clip(255 * (0.82 + 0.18 * t_len), 0, 255))
                        g_w = int(np.clip(208 * (0.82 + 0.18 * t_len), 0, 255))
                        b_w = int(np.clip(40 * (0.82 + 0.35 * t_len) + 30 * t_len, 0, 255))
                        weapon_img.putpixel((px, py), (r_w, g_w, b_w, 255))
                    elif w_off == -1:
                        # Tempered steel dark core
                        r_w = int(np.clip(58 * (0.8 + 0.35 * t_len), 0, 255))
                        g_w = int(np.clip(54 * (0.8 + 0.35 * t_len), 0, 255))
                        b_w = int(np.clip(68 * (0.8 + 0.35 * t_len), 0, 255))
                        weapon_img.putpixel((px, py), (r_w, g_w, b_w, 255))
                    elif w_off == 0:
                        # Polished steel spine highlight
                        r_w = int(np.clip(100 * (0.85 + 0.35 * t_len), 0, 255))
                        g_w = int(np.clip(105 * (0.85 + 0.35 * t_len), 0, 255))
                        b_w = int(np.clip(125 * (0.85 + 0.35 * t_len), 0, 255))
                        weapon_img.putpixel((px, py), (r_w, g_w, b_w, 255))
                    elif w_off == 1:
                        # Sharp cutting bevel
                        r_w = int(np.clip(230 * (0.88 + 0.12 * t_len), 0, 255))
                        g_w = int(np.clip(235 * (0.88 + 0.12 * t_len), 0, 255))
                        b_w = int(np.clip(245 * (0.88 + 0.12 * t_len), 0, 255))
                        weapon_img.putpixel((px, py), (r_w, g_w, b_w, 255))
                    else:
                        # Razor white cutting edge
                        weapon_img.putpixel((px, py), WHITE_SHINE)

    # Piercing Saber Tip at (108, 22)
    wd.polygon([(108, 20), (105, 24), (110, 24)], fill=WHITE_SHINE, outline=OUTLINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_courser_baroque_trefoil_gold", key_img),
        ("back_curio", "curio_courser_articulated_spring_tail", curio_img),
        ("chassis", "chassis_courser_cream_gold_default", chassis_img),
        ("head_unit", "head_courser_brass_chanfron_mane", head_img),
        ("costume", "costume_courser_dawn_patrol_cuirass", costume_img),
        ("optic_core", "face_courser_sapphire_optic_lens", core_img),
        ("weapon", "weapon_courser_cavalry_saber", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{COURSER_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{COURSER_PD_DIR}/winding_key/key_courser_baroque_trefoil_gold.png", f"{KEY_DIR}/key_courser_baroque_trefoil_gold.png")
    shutil.copyfile(f"{COURSER_PD_DIR}/weapon/weapon_courser_cavalry_saber.png", f"{WEAPON_DIR}/weapon_courser_cavalry_saber.png")
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

    proof_comp = f"{COURSER_PD_DIR}/proof_paperdoll_courser_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{COURSER_PD_DIR}/proof_paperdoll_courser_magenta.png"
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

    strip_path = f"{COURSER_PD_DIR}/proof_courser_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/courser_idle_hd.png)
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
        sc_sdraw.ellipse((400 - 220, 1120 - 22, 400 + 220, 1120 + 22), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{showcase_dir}/courser_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL IRONHOOF COURSER CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
