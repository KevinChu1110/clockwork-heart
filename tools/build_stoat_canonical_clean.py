#!/usr/bin/env python3
"""
build_stoat_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十九族 旋刃伶鼬 (The Whirling Stoat, stoat) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/WHIRLING_STOAT_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, ivory tinplate plates,
  cold-rolled steel framework, stamped aerodynamic hood & brass acoustic ears,
  segmented spring balance tungsten black-tip tail, whirlwind tri-ring pawl key)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Ivory Tinplate Enamel (#FFFDF8)
    2. Secondary Hull / Trim: Scrap Warm Orange (#FFA010)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Sapphire: Dynamic Crosshair Sapphire Quartz (#38A0FF)
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
STOAT_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/stoat"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Whirling Stoat Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Ivory Tinplate Enamel (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHINE  = (255, 255, 255, 255)
IVORY_SHADOW = (235, 226, 210, 255)
IVORY_DARK   = (210, 198, 178, 255)
IVORY_DEEP   = (180, 168, 148, 255)

# 2. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Scrap Warm Orange (#FFA010)
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

# 5. Sapphire Dynamic Crosshair Optic Lens (#38A0FF)
SAPPHIRE_BASE  = (56, 160, 255, 255)
SAPPHIRE_LIGHT = (120, 205, 255, 255)
SAPPHIRE_SHINE = (195, 235, 255, 255)
SAPPHIRE_DARK  = (24, 105, 195, 255)
SAPPHIRE_DEEP  = (12, 60, 140, 255)

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
                has_solid_neighbor = False
                for nx, ny in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
                    if 0 <= nx < w and 0 <= ny < h:
                        if px_snap[nx, ny][3] >= min_alpha:
                            has_solid_neighbor = True
                            break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL WHIRLING STOAT SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_stoat_whirlwind_tri_ring_brass.png
    # Whirlwind Tri-Ring Pawl Key (三環旋風棘爪黃銅發條鑰匙)
    # Features:
    # - Socket boss at upper back (64, 58)
    # - Polished brass key shaft extends up-right from (64, 58) to (92, 22)
    # - 3 Whirlwind aerodynamic curved tri-ring blades (120-deg rotational symmetry)
    # - Tri-circular weight-reduction cutout holes
    # - Central sapphire gem bearing at (92, 22)
    # - Warm golden bronze outline (OUTLINE_KEY)
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

    # 2. Three Whirlwind Tri-Ring Blades: Center (92, 22), outer radius ~ 15
    kcx, kcy = 92.0, 22.0
    for dy in range(-18, 19):
        for dx in range(-18, 19):
            dist = (dx**2 + dy**2)**0.5
            angle = np.arctan2(dy, dx)
            # 3 whirlwind curved blades modulation
            # Modulate blade thickness and flare
            blade_wave = np.cos(3 * angle - 0.4 * dist)
            max_r = 14.5 + 2.5 * blade_wave
            if 6.0 <= dist <= max_r and blade_wave > -0.3:
                spec = max(0.0, 1.0 - abs(dist - 10.5) / 4.5)
                shine = max(0.0, 1.0 - ((dx + 2)**2 + (dy + 2)**2)**0.5 / 8.0)
                r_g = int(np.clip(255 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                g_g = int(np.clip(208 * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                b_g = int(np.clip(40 * (0.8 + 0.5 * spec) + 45 * shine, 0, 255))
                key_img.putpixel((int(kcx + dx), int(kcy + dy)), (r_g, g_g, b_g, 255))

    # Center Hub disc at (92, 22), r <= 6.5
    for dx in range(-7, 8):
        for dy in range(-7, 8):
            d = (dx**2 + dy**2)**0.5
            if d <= 6.5:
                spec = max(0.0, 1.0 - d / 6.5)
                r_g = int(np.clip(255 * (0.85 + 0.2 * spec), 0, 255))
                g_g = int(np.clip(208 * (0.85 + 0.2 * spec), 0, 255))
                b_g = int(np.clip(40 * (0.85 + 0.4 * spec), 0, 255))
                key_img.putpixel((int(kcx + dx), int(kcy + dy)), (r_g, g_g, b_g, 255))

    # 3 Circular Cutout Holes in the 3 Blades (120 deg apart at radius 10)
    for rot in [0.0, 2.094, 4.188]:
        hx = kcx + 9.5 * np.cos(rot + 0.5)
        hy = kcy + 9.5 * np.sin(rot + 0.5)
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                if dx**2 + dy**2 <= 5:  # radius ~2.2 hole
                    key_img.putpixel((int(round(hx + dx)), int(round(hy + dy))), (0, 0, 0, 0))

    # Center sapphire gem bearing at (92, 22)
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

    # Clean outline pass with warm bronze outline (OUTLINE_KEY) to avoid dark limit violations
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict 0-ART29 transparent corners
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_stoat_flexible_segmented_tail.png
    # Segmented Spring Balance Tungsten Black-Tip Tail (多節同軸彈簧平衡鎢鋼黑尖尾)
    # Features:
    # - Originates from pelvis at (46, 84..88)
    # - 7-segment polished ivory-tinplate rings & gold torsion coils curling up-left:
    #   (46, 86) -> (40, 80) -> (33, 72) -> (26, 62) -> (22, 50) -> (21, 38) -> (25, 26)
    # - Segment 7 tipped with solid Tungsten Steel Black Cone (#3A3644) with bevel highlights
    # - Inter-segment brass damping hinge springs
    # - Dynamic acrobatic balance stabilizer
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Hinge Socket at base (46, 86)
    cd.ellipse([46 - 4, 86 - 4, 46 + 4, 86 + 4], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    cd.ellipse([46 - 2, 86 - 2, 46 + 2, 86 + 2], fill=GOLD_BASE)
    cd.point((46, 86), fill=WHITE_SHINE)

    # 2. 7 Coaxial Segmented Spring Rings
    # Segment centers:
    seg_centers = [
        (43.0, 83.0, 5.2, "ivory"),
        (38.0, 76.0, 5.0, "ivory"),
        (32.0, 68.0, 4.8, "ivory"),
        (26.0, 58.0, 4.5, "ivory"),
        (22.0, 47.0, 4.2, "ivory"),
        (22.0, 36.0, 4.0, "tungsten_mid"),
        (25.0, 26.0, 3.8, "tungsten_tip"),
    ]

    # Inter-segment brass torsion coils
    for i in range(len(seg_centers) - 1):
        x1, y1, r1, _ = seg_centers[i]
        x2, y2, r2, _ = seg_centers[i + 1]
        for t in np.linspace(0.0, 1.0, 15):
            cx = x1 * (1 - t) + x2 * t
            cy = y1 * (1 - t) + y2 * t
            coil_off = 1.8 * np.sin(t * 12.0)
            px = int(round(cx + coil_off))
            py = int(round(cy))
            curio_img.putpixel((px, py), GOLD_BASE)
            curio_img.putpixel((px + 1, py), GOLD_SHINE)

    # Draw segments
    for idx, (scx, scy, s_rad, s_type) in enumerate(seg_centers):
        irad = int(np.ceil(s_rad))
        for dy in range(-irad - 1, irad + 2):
            for dx in range(-irad - 1, irad + 2):
                dist = (dx**2 + dy**2)**0.5
                if dist <= s_rad:
                    spec = max(0.0, 1.0 - dist / s_rad)
                    shine = max(0.0, 1.0 - ((dx + 1)**2 + (dy + 1)**2)**0.5 / (s_rad * 0.8))
                    if s_type == "ivory":
                        # Ivory tinplate ring
                        r_col = int(np.clip(255 * (0.92 + 0.08 * shine), 0, 255))
                        g_col = int(np.clip(253 * (0.92 + 0.08 * shine) - 20 * (1 - spec), 0, 255))
                        b_col = int(np.clip(248 * (0.92 + 0.08 * shine) - 40 * (1 - spec), 0, 255))
                    elif s_type == "tungsten_mid":
                        # Transition to Tungsten
                        r_col = int(np.clip(58 * (0.85 + 0.35 * shine) + 20 * spec, 0, 255))
                        g_col = int(np.clip(54 * (0.85 + 0.35 * shine) + 20 * spec, 0, 255))
                        b_col = int(np.clip(68 * (0.85 + 0.35 * shine) + 25 * spec, 0, 255))
                    else:
                        # Solid Tungsten Black-Tip Cone
                        r_col = int(np.clip(45 * (0.8 + 0.4 * shine) + 30 * spec, 0, 255))
                        g_col = int(np.clip(42 * (0.8 + 0.4 * shine) + 30 * spec, 0, 255))
                        b_col = int(np.clip(55 * (0.8 + 0.4 * shine) + 40 * spec, 0, 255))
                    curio_img.putpixel((int(round(scx + dx)), int(round(scy + dy))), (r_col, g_col, b_col, 255))

        # Gold decorative collar ring on each segment
        if s_type == "ivory":
            cd.ellipse([int(scx - s_rad * 0.6), int(scy - s_rad * 0.6), int(scx + s_rad * 0.6), int(scy + s_rad * 0.6)], outline=GOLD_BASE)
        elif s_type == "tungsten_tip":
            # Sharp tip conical apex at (26, 21)
            cd.polygon([(scx - 2, scy), (scx + 2, scy), (26, 21)], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
            curio_img.putpixel((26, 21), WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Core Body Layer)
    # File: chassis/chassis_stoat_ivory_tinplate_default.png
    # Ivory Tinplate & Brass Stamped Alloy Chassis (旋刃伶鼬象牙白馬口鐵防砂素體)
    # Features:
    # - 2.2 head-tall agile cylindrical streamline chibi toy stoat frame
    # - Ivory Tinplate Enamel (#FFFDF8) plates with rich multi-tone depth (>=20 unique colors in torso)
    # - Ball-and-socket mechanical knee and elbow joints
    # - Flat metal footplates with non-slip grooved rubber soles at base (y: 114..120)
    # - Left hand held forward for balance / acrobatics (40, 78)
    # - Right arm held at side, clamp hand strictly x <= 92 (ZERO pixels at x >= 94!)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Legs and Footplates
    # Left leg: Thigh (46..54, 84..96), Knee (48, 97), Shin (46..52, 98..114), Foot (42..54, 114..120)
    # Right leg: Thigh (74..82, 84..96), Knee (78, 97), Shin (76..82, 98..114), Foot (74..86, 114..120)
    for leg_cx, leg_name in [(48.0, "left"), (78.0, "right")]:
        # Thigh (ivory tinplate)
        for y in range(84, 98):
            for x in range(int(leg_cx - 6), int(leg_cx + 7)):
                spec = max(0.0, 1.0 - abs(x - leg_cx) / 6.0)
                sh = max(0.0, (y - 84) / 14.0)
                r_c = int(np.clip(255 * (0.96 - 0.15 * sh + 0.08 * spec), 0, 255))
                g_c = int(np.clip(253 * (0.96 - 0.18 * sh + 0.08 * spec), 0, 255))
                b_c = int(np.clip(248 * (0.95 - 0.22 * sh + 0.08 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        # Knee Ball-Joint (brass)
        chd.ellipse([int(leg_cx - 5), 94, int(leg_cx + 5), 102], fill=GOLD_BASE, outline=OUTLINE)
        chd.ellipse([int(leg_cx - 3), 96, int(leg_cx + 3), 100], fill=GOLD_LIGHT)
        chd.point((int(leg_cx), 98), fill=WHITE_SHINE)

        # Shin (ivory tinplate with vertical brass rivet groove)
        for y in range(100, 115):
            for x in range(int(leg_cx - 5), int(leg_cx + 6)):
                spec = max(0.0, 1.0 - abs(x - leg_cx) / 5.0)
                sh = max(0.0, (y - 100) / 15.0)
                r_c = int(np.clip(255 * (0.95 - 0.15 * sh + 0.08 * spec), 0, 255))
                g_c = int(np.clip(253 * (0.95 - 0.18 * sh + 0.08 * spec), 0, 255))
                b_c = int(np.clip(248 * (0.95 - 0.22 * sh + 0.08 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        # Footplate (Stamped Tungsten Steel with brass rim & textured rubber sole)
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
                    # Bottom non-slip grooved rubber pad
                    chassis_img.putpixel((x, y), (28, 25, 34, 255))
        chd.line([(int(leg_cx - 5), 116), (int(leg_cx + 5), 116)], fill=TUNGSTEN_SHINE, width=1)

    # 2. Main Torso / Cylindrical Slender Body (x: 42..86, y: 58..94)
    # Rich multi-tone shading to guarantee 0-ART18 (>=20 unique colors in [58:94, 44:84])
    tcx, tcy = 64.0, 75.0
    for y in range(58, 95):
        for x in range(42, 87):
            dx = (x - tcx) / 21.5
            dy = (y - tcy) / 18.0
            if dx**2 + dy**2 <= 1.05:
                dist = (dx**2 + dy**2)**0.5
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 68.0)**2)**0.5 / 18.0)
                sh_y = (y - 58.0) / 36.0
                # Ivory porcelain / enamel gradient
                r_e = int(np.clip(255 * (0.98 - 0.22 * sh_y + 0.15 * spec), 0, 255))
                g_e = int(np.clip(253 * (0.98 - 0.25 * sh_y + 0.12 * spec), 0, 255))
                b_e = int(np.clip(248 * (0.97 - 0.32 * sh_y + 0.08 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_e, g_e, b_e, 255))

    # Torso Brass Seams, Screws & Central Clockwork Core
    chd.arc([47, 62, 81, 90], start=10, end=170, fill=GOLD_BASE, width=1)
    chd.line([(52, 78), (76, 78)], fill=GOLD_BASE, width=1)
    # Corner brass rivets
    for rx, ry in [(48, 64), (80, 64), (48, 86), (80, 86)]:
        chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
        chd.point((rx, ry), fill=WHITE_SHINE)

    # Central Core Socket Ring at (64, 72)
    chd.ellipse([58, 66, 70, 78], fill=GOLD_BASE, outline=OUTLINE)
    chd.ellipse([60, 68, 68, 76], fill=SAPPHIRE_DARK)
    chd.ellipse([62, 70, 66, 74], fill=GOLD_SHINE)

    # 3. Arms / Forelimbs
    # Left Arm: Shoulder (44, 64), Elbow (38, 72), Hand (40, 78) holding balancing grip
    for y in range(64, 80):
        for x in range(36, 46):
            if ((x - 41) / 4.5)**2 + ((y - 71) / 7.5)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 41) / 4.5)
                r_a = int(np.clip(255 * (0.92 + 0.08 * spec), 0, 255))
                g_a = int(np.clip(253 * (0.92 + 0.08 * spec) - 20 * (1 - spec), 0, 255))
                b_a = int(np.clip(248 * (0.92 + 0.08 * spec) - 35 * (1 - spec), 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    chd.ellipse([38, 75, 43, 80], fill=GOLD_BASE, outline=OUTLINE)  # Brass toy hand clamp

    # Right Arm: Shoulder (84, 64), Elbow (88, 70), Hand (89, 74)
    # STRICT 0-ART9/11 RULE: strictly x <= 92 (no pixels at x >= 94)
    for y in range(64, 76):
        for x in range(83, 93):  # strictly up to 92
            if ((x - 87) / 5.0)**2 + ((y - 69) / 6.0)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 87) / 5.0)
                r_a = int(np.clip(255 * (0.92 + 0.08 * spec), 0, 255))
                g_a = int(np.clip(253 * (0.92 + 0.08 * spec) - 20 * (1 - spec), 0, 255))
                b_a = int(np.clip(248 * (0.92 + 0.08 * spec) - 35 * (1 - spec), 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    chd.ellipse([87, 71, 92, 76], fill=GOLD_BASE, outline=OUTLINE)  # Brass toy weapon clamp (x <= 92)

    # 4. Neck & Cranial Shell (Head Base)
    # Neck (58..70, 50..60)
    for y in range(50, 61):
        for x in range(58, 71):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 6.0)
            r_n = int(np.clip(255 * (0.88 + 0.12 * spec), 0, 255))
            g_n = int(np.clip(253 * (0.88 + 0.12 * spec) - 25 * (1 - spec), 0, 255))
            b_n = int(np.clip(248 * (0.88 + 0.12 * spec) - 45 * (1 - spec), 0, 255))
            chassis_img.putpixel((x, y), (r_n, g_n, b_n, 255))

    # Head Cranial Shell (x: 44..84, y: 22..52)
    for y in range(22, 53):
        for x in range(44, 85):
            dx = (x - 64.0) / 19.5
            dy = (y - 37.0) / 14.5
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 16.0)
                sh_y = (y - 22.0) / 30.0
                r_h = int(np.clip(255 * (0.98 - 0.2 * sh_y + 0.15 * spec), 0, 255))
                g_h = int(np.clip(253 * (0.98 - 0.22 * sh_y + 0.12 * spec), 0, 255))
                b_h = int(np.clip(248 * (0.97 - 0.28 * sh_y + 0.08 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Snout / Chin plate (stamped ivory plate with brass nose bolt)
    chd.rounded_rectangle([58, 48, 70, 54], radius=2, fill=IVORY_SHADOW, outline=OUTLINE)
    chd.rectangle([62, 50, 66, 52], fill=GOLD_BASE, outline=OUTLINE)

    # Cheek Blush Roundels in Coral Pink (#FF5E8A)
    for bx, by in [(46, 45), (82, 45)]:
        chd.ellipse([bx - 3, by - 2, bx + 3, by + 2], fill=CORAL_BASE)
        chd.point((bx, by), fill=CORAL_LIGHT)

    # Eye Socket Under-rings (deepened socket shadow ready for optic_core)
    for ex in [52, 76]:
        chd.ellipse([ex - 5, 40 - 5, ex + 5, 40 + 5], fill=IVORY_DARK, outline=OUTLINE)

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
    # SLICE 4: HEAD UNIT (Z: 20, Head & Ears Layer)
    # File: head_unit/head_stoat_aerodynamic_hood_ears.png
    # Aerodynamic Hood & Brass Acoustic Ears (沖壓防沙流線兜帽與雙聯薄黃銅拾音立耳)
    # Features:
    # 1. Aerodynamic Sand-Proof Hood: Domed ivory enamel hood with brass aerodynamic ridge (y: 12..30, x: 44..84)
    # 2. Semi-circular thin brass acoustic ears: left (40..48, 14..26), right (80..88, 14..26), micro torsion springs
    # 3. Flanged forehead rim with reinforcement hex bolts
    # 4. STRICT 0-ART27 COMPLIANCE: Eye sockets at (52, 40) and (76, 40) MUST BE 100% HOLLOW!
    #    (alpha == 0 in boxes [38..42, 50..54] and [38..42, 74..78])
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Semi-Circular Brass Acoustic Ears with internal spring coils
    for ex_base, ear_side in [(44, "left"), (84, "right")]:
        hd.ellipse([ex_base - 5, 14, ex_base + 5, 26], fill=GOLD_BASE, outline=OUTLINE)
        hd.ellipse([ex_base - 3, 16, ex_base + 3, 24], fill=GOLD_LIGHT)
        # Internal miniature torsion coil
        hd.arc([ex_base - 2, 17, ex_base + 2, 23], start=0, end=270, fill=SAPPHIRE_BASE, width=1)
        hd.point((ex_base, 19), fill=WHITE_SHINE)

    # 2. Aerodynamic Hood Dome (y: 12..30, x: 45..83)
    for y in range(12, 31):
        for x in range(45, 84):
            dx = (x - 64.0) / 19.0
            dy = (y - 25.0) / 13.0
            if dx**2 + dy**2 <= 1.05 and y <= 27:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 18.0)**2)**0.5 / 14.0)
                sh_y = (y - 12.0) / 15.0
                r_h = int(np.clip(255 * (0.96 - 0.15 * sh_y + 0.12 * spec), 0, 255))
                g_h = int(np.clip(253 * (0.96 - 0.18 * sh_y + 0.10 * spec), 0, 255))
                b_h = int(np.clip(248 * (0.95 - 0.24 * sh_y + 0.08 * spec), 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Central Aerodynamic Brass Ridge / Crest at (64, 14..24)
    hd.polygon([(63, 13), (65, 13), (66, 25), (62, 25)], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(64, 14), (64, 24)], fill=WHITE_SHINE, width=1)

    # Hood Visor Rim (protective flanged rim along y: 26..30, x: 43..85)
    hd.rounded_rectangle([43, 26, 85, 30], radius=2, fill=ORANGE_BASE, outline=OUTLINE)
    hd.line([(45, 28), (83, 28)], fill=ORANGE_LIGHT, width=1)
    # Rim hex rivets
    for rx in [46, 54, 74, 82]:
        hd.point((rx, 28), fill=WHITE_SHINE)

    # Clean outline pass with strict ignore_regions for eye sockets to guarantee 0-ART27 compliance!
    eye_ignore = [(48, 36, 56, 44), (72, 36, 80, 44)]
    apply_clean_outline(head_img, ignore_regions=eye_ignore)

    # 4. Enforce STRICT 0-ART27 HOLLOW EYE SOCKETS
    for ex in [52, 76]:
        for ey in range(37, 44):
            for exx in range(ex - 3, ex + 4):
                head_img.putpixel((exx, ey), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25, Chest & Cape Layer)
    # File: costume/costume_stoat_scavenger_wind_cape.png
    # Scavenger Wind Cape & Utility Rig (廢土拾荒輕量防風斗篷與工具束帶)
    # Features:
    # - Fits over torso (x: 44..84, y: 58..92)
    # - Scrap Warm Orange (#FFA010) fabric with dopamine shading
    # - Mint Green (#4ED86A) enamel clasp & utility pouch fasteners
    # - Cross-chest leather rig & brass utility buckle
    # - STRICT 0-ART26b RULE: strictly zero pixels at y >= 96 (no lower chassis baking!)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Cape Shoulders & Mantle (y: 58..78, x: 44..84)
    for y in range(58, 79):
        for x in range(44, 85):
            dx = (x - 64.0) / 20.0
            dy = (y - 68.0) / 11.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 20.0)
                sh_y = (y - 58.0) / 21.0
                r_o = int(np.clip(255 * (0.95 - 0.2 * sh_y + 0.15 * spec), 0, 255))
                g_o = int(np.clip(160 * (0.95 - 0.2 * sh_y + 0.2 * spec), 0, 255))
                b_o = int(np.clip(16 * (0.95 - 0.2 * sh_y) + 40 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_o, g_o, b_o, 255))

    # 2. Chest Harness & Cross-Belt (y: 72..92, x: 48..80)
    for y in range(78, 93):  # strictly <= 92
        for x in range(48, 81):
            dx = (x - 64.0) / 16.0
            dy = (y - 85.0) / 8.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 16.0)
                sh_y = (y - 78.0) / 15.0
                r_o = int(np.clip(255 * (0.9 - 0.25 * sh_y + 0.15 * spec), 0, 255))
                g_o = int(np.clip(160 * (0.9 - 0.25 * sh_y + 0.15 * spec), 0, 255))
                b_o = int(np.clip(16 * (0.9 - 0.25 * sh_y) + 30 * spec, 0, 255))
                costume_img.putpixel((x, y), (r_o, g_o, b_o, 255))

    # Diagonal utility strap across chest (52, 62) to (76, 86)
    cosd.line([(52, 62), (76, 86)], fill=TUNGSTEN_LIGHT, width=3)
    cosd.line([(52, 62), (76, 86)], fill=GOLD_BASE, width=1)

    # Mint Green Utility Buckle at center (64, 74)
    cosd.rounded_rectangle([61, 71, 67, 77], radius=2, fill=MINT_BASE, outline=OUTLINE)
    cosd.ellipse([62, 72, 66, 76], fill=MINT_SHINE)
    cosd.point((64, 74), fill=WHITE_SHINE)

    # Scavenger Tools Pouch on Belt (y: 86..91, x: 50..60)
    cosd.rounded_rectangle([50, 86, 60, 92], radius=1, fill=GOLD_DARK, outline=OUTLINE)
    cosd.line([(50, 88), (60, 88)], fill=GOLD_LIGHT, width=1)
    cosd.point((55, 90), fill=WHITE_SHINE)

    # Cape hem fringe & reinforcement stitch line
    cosd.line([(46, 78), (82, 78)], fill=ORANGE_SHINE, width=1)

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
    # File: optic_core/face_stoat_sapphire_crosshair_lens.png
    # Sapphire Dynamic Crosshair Optic Lens (天青藍高頻動態追蹤目鏡)
    # Features:
    # - Left eye centered at (52, 40), Right eye centered at (76, 40)
    # - High opacity at centers (alpha == 255 > 200, 0-ART27 compliant)
    # - Dynamic tracking crosshairs and concentric angle markings (MINT/SAPPHIRE)
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
                        col = SAPPHIRE_SHINE
                    elif ratio <= 0.65:
                        col = SAPPHIRE_LIGHT
                    elif ratio <= 0.88:
                        col = SAPPHIRE_BASE
                    else:
                        col = SAPPHIRE_DEEP
                    core_img.putpixel((x, y), col)

        # Concentric Tracker Scale & Crosshair markings
        cored.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], outline=SAPPHIRE_DARK)
        cored.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], outline=SAPPHIRE_LIGHT)
        # Crosshair lines in Mint Green (#4ED86A)
        cored.line([(ex - 4, ey), (ex - 2, ey)], fill=MINT_BASE)
        cored.line([(ex + 2, ey), (ex + 4, ey)], fill=MINT_BASE)
        cored.line([(ex, ey - 4), (ex, ey - 2)], fill=MINT_BASE)
        cored.line([(ex, ey + 2), (ex, ey + 4)], fill=MINT_BASE)
        # White specular glints
        core_img.putpixel((ex - 2, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 1, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 2, ey - 1), WHITE_SHINE)
        core_img.putpixel((ex + 1, ey + 1), SAPPHIRE_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Weapon Layer)
    # File: weapon/weapon_stoat_crescent_dagger.png
    # Scrap Whirling Crescent Dagger (廢土旋刃弧光短匕)
    # Features:
    # - Held in right hand: handgrip at (88..92, 68..75)
    # - Single-wield (0-MKT7), reverse-grip shinobi dagger
    # - Crescent-curved high-carbon spring steel blade sweeping up-right (94..122, 38..68)
    # - Polished brass counterweight pommel at (87, 78)
    # - Sapphire cooling line along blade spine
    # - Razor-sharp white cutting crescent edge
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Hilt & Grip (Reverse-grip angle)
    # Grip from pommel (86, 78) to guard (92, 66)
    for t in np.linspace(0.0, 1.0, 40):
        sx = 86.0 * (1 - t) + 92.0 * t
        sy = 78.0 * (1 - t) + 66.0 * t
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx**2 + dy**2 <= 1:
                    weapon_img.putpixel((int(round(sx + dx)), int(round(sy + dy))), TUNGSTEN_LIGHT)

    # Pommel at (86, 78)
    wd.ellipse([84, 76, 88, 80], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((86, 78), fill=WHITE_SHINE)

    # Wrapped grip segments at (88..91, 68..75)
    for y in range(68, 76):
        for x in range(88, 92):
            if (y + x) % 2 == 0:
                weapon_img.putpixel((x, y), ORANGE_BASE)
            else:
                weapon_img.putpixel((x, y), TUNGSTEN_DARK)

    # 2. Guard / Collar at (92..96, 64..68)
    wd.ellipse([91, 63, 97, 69], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([92, 64, 96, 68], fill=SAPPHIRE_BASE)

    # 3. Crescent Blade (x: 94..122, y: 38..66)
    # Crescent polygon sweeping upwards to a deadly point at (118, 38)
    blade_poly = [
        (94, 65),
        (100, 58),
        (108, 48),
        (118, 38),   # Tip
        (115, 46),
        (110, 54),
        (104, 62),
        (96, 68)
    ]
    wd.polygon(blade_poly, fill=TUNGSTEN_LIGHT, outline=OUTLINE)

    # Shading across the crescent dagger blade
    for y in range(38, 68):
        for x in range(94, 122):
            if weapon_img.getpixel((x, y))[3] > 100:
                dist_tip = max(0.0, 1.0 - ((x - 118.0)**2 + (y - 38.0)**2)**0.5 / 35.0)
                r_b = int(np.clip(58 * (0.85 + 0.35 * dist_tip), 0, 255))
                g_b = int(np.clip(54 * (0.85 + 0.35 * dist_tip), 0, 255))
                b_b = int(np.clip(68 * (0.85 + 0.35 * dist_tip), 0, 255))
                weapon_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Sapphire energy cooling groove along blade spine
    wd.line([(96, 64), (103, 56), (111, 46)], fill=SAPPHIRE_SHINE, width=1)
    wd.line([(97, 65), (104, 57), (112, 47)], fill=SAPPHIRE_BASE, width=1)

    # Razor-sharp white cutting crescent edge
    crescent_edge = [
        (94, 65), (98, 60), (102, 54), (107, 48), (112, 42), (118, 38)
    ]
    for ex, ey in crescent_edge:
        weapon_img.putpixel((ex, ey), WHITE_SHINE)
        weapon_img.putpixel((ex + 1, ey), GOLD_LIGHT)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_stoat_whirlwind_tri_ring_brass", key_img),
        ("back_curio", "curio_stoat_flexible_segmented_tail", curio_img),
        ("chassis", "chassis_stoat_ivory_tinplate_default", chassis_img),
        ("head_unit", "head_stoat_aerodynamic_hood_ears", head_img),
        ("costume", "costume_stoat_scavenger_wind_cape", costume_img),
        ("optic_core", "face_stoat_sapphire_crosshair_lens", core_img),
        ("weapon", "weapon_stoat_crescent_dagger", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{STOAT_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{STOAT_PD_DIR}/winding_key/key_stoat_whirlwind_tri_ring_brass.png", f"{KEY_DIR}/key_stoat_whirlwind_tri_ring_brass.png")
    shutil.copyfile(f"{STOAT_PD_DIR}/weapon/weapon_stoat_crescent_dagger.png", f"{WEAPON_DIR}/weapon_stoat_crescent_dagger.png")
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

    proof_comp = f"{STOAT_PD_DIR}/proof_paperdoll_stoat_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{STOAT_PD_DIR}/proof_paperdoll_stoat_magenta.png"
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

    strip_path = f"{STOAT_PD_DIR}/proof_stoat_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    # Standard ground soft shadow for idle assets (y: 116..122)
    idle_base = composite.copy()
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([34, 115, 94, 123], fill=(31, 26, 58, 110))
    shd.ellipse([44, 116, 84, 122], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(idle_base)

    # 1. 128x128 game/assets/sprites/player/stoat_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/stoat_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/stoat_idle.png
    p_idle_64 = f"{PLAYER_DIR}/stoat_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/stoat_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/stoat_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/stoat_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/stoat_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/stoat_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL WHIRLING STOAT CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
