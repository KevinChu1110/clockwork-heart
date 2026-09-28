#!/usr/bin/env python3
"""
build_beaver_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十八族 劈木河狸 (The Woodchopper Beaver, beaver) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/WOODCHOPPER_BEAVER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped enamel plates,
  cold-rolled steel framework, stamped brass chisel teeth, perforated heavy brass paddle tail, sawtooth cog key)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Deepwood Forest Enamel (#4A7C59)
    2. Secondary Hull / Trim: Dawn Warm Orange (#FFA010)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Amber / Sapphire: Amber Gold (#FFA010) & Sapphire (#38A0FF)
    6. Cute Coral Pink: Coral Pink (#FF5E8A)
    7. Cold Stamped Tungsten Steel: Tungsten Gray (#3A3644)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BEAVER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/beaver"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Woodchopper Beaver Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Deepwood Forest Enamel (#4A7C59)
FOREST_BASE  = (74, 124, 89, 255)
FOREST_LIGHT = (108, 168, 125, 255)
FOREST_SHINE = (152, 212, 168, 255)
FOREST_DARK  = (52, 92, 64, 255)
FOREST_DEEP  = (35, 64, 44, 255)

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

# 5. Amber Gold Optic Lens (#FFA010) & Sapphire Indicator (#38A0FF)
AMBER_BASE  = (255, 160, 16, 255)
AMBER_LIGHT = (255, 200, 70, 255)
AMBER_SHINE = (255, 240, 165, 255)
AMBER_DARK  = (195, 110, 8, 255)
AMBER_DEEP  = (135, 70, 5, 255)

SAPPHIRE_BASE  = (56, 160, 255, 255)
SAPPHIRE_LIGHT = (120, 205, 255, 255)
SAPPHIRE_SHINE = (195, 235, 255, 255)
SAPPHIRE_DARK  = (24, 105, 195, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL WOODCHOPPER BEAVER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_beaver_sawtooth_cog_brass.png
    # Sawtooth Cog Brass Winding Key (鋸齒環輪雙孔黃銅發條鑰匙)
    # Features:
    # - Socket boss at upper back (64, 58)
    # - Heavy polished brass key shaft extends up-right to saw cog hub at (92, 22)
    # - 16-tooth circular saw wheel outer rim, center dual concentric holes, warm brass
    # - Center sapphire gem bearing at (92, 22)
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

    # 2. Sawtooth Cog Wheel: Center (92, 22), outer radius ~ 15
    kcx, kcy = 92.0, 22.0
    # Outer saw disc ring: r from 8 to 15
    for dy in range(-18, 19):
        for dx in range(-18, 19):
            dist = (dx**2 + dy**2)**0.5
            angle = np.arctan2(dy, dx)
            # 16 saw teeth modulation
            tooth = 2.8 * np.sin(16 * angle)
            max_r = 14.5 + tooth
            if 6.5 <= dist <= max_r:
                spec = max(0.0, 1.0 - abs(dist - 11.0) / 4.5)
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

    # Dual Circular Cutout Holes in Key (classic wind-up key holes): at (83, 22) and (101, 22)
    for hole_x in [kcx - 9.0, kcx + 9.0]:
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 9:  # radius 3 hole
                    key_img.putpixel((int(hole_x + dx), int(kcy + dy)), (0, 0, 0, 0))

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
    # File: back_curio/curio_beaver_perforated_paddle_tail.png
    # Stamped Perforated Heavy Brass Paddle Tail (沖壓穿孔重型黃銅壓板扁尾)
    # Features:
    # - Originates from pelvis at (46, 84..88)
    # - Sweeps down-left to (16..38, 92..118)
    # - Stamped heavy brass paddle shape (width 20..26, height 26..30)
    # - 18 micro hexagonal / round weight-reducing perforations
    # - Heavy dual torsion spring damping hinge at root (46, 86)
    # - Ground rubber contact pad along bottom edge (y: 116..120)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Hinge Socket at base (46, 86)
    cd.ellipse([46 - 4, 86 - 4, 46 + 4, 86 + 4], fill=TUNGSTEN_LIGHT, outline=OUTLINE)
    cd.ellipse([46 - 2, 86 - 2, 46 + 2, 86 + 2], fill=GOLD_BASE)
    cd.point((46, 86), fill=WHITE_SHINE)

    # 2. Main Paddle Body
    # Center of paddle at (28, 104), radius x ~ 14, radius y ~ 12, rotated ~ 25 degrees
    # We define the paddle polygon / ellipse oriented diagonally
    paddle_pts = [
        (44, 86),   # root top
        (38, 88),   # upper neck
        (30, 92),   # mid upper
        (22, 98),   # left curve
        (16, 106),  # far left edge
        (16, 112),  # bottom left corner
        (22, 117),  # bottom edge left
        (32, 118),  # bottom edge mid
        (40, 114),  # bottom right edge
        (44, 106),  # right curve
        (46, 96),   # mid right
        (48, 88)    # root bottom
    ]
    # Draw filled paddle body with radial shading
    cd.polygon(paddle_pts, fill=GOLD_BASE, outline=OUTLINE)

    # Interior gradient & bevel on paddle
    for y in range(86, 119):
        for x in range(16, 48):
            if curio_img.getpixel((x, y))[3] > 100:
                dist = ((x - 28)**2 + (y - 104)**2)**0.5
                spec = max(0.0, 1.0 - dist / 15.0)
                sh_x = (x - 16.0) / 32.0
                r_p = int(np.clip(255 * (0.82 + 0.25 * spec), 0, 255))
                g_p = int(np.clip(208 * (0.82 + 0.25 * spec), 0, 255))
                b_p = int(np.clip(40 * (0.82 + 0.45 * spec) + 30 * spec, 0, 255))
                curio_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    # Perforated honeycomb holes (3 columns x 4 rows = 12 main holes + 4 boundary holes = 16 holes)
    hole_centers = [
        (23, 100), (29, 99), (35, 98),
        (21, 105), (27, 104), (33, 103), (39, 102),
        (22, 110), (28, 109), (34, 108), (40, 107),
        (25, 114), (31, 114), (37, 113)
    ]
    for hx, hy in hole_centers:
        cd.ellipse([hx - 1, hy - 1, hx + 1, hy + 1], fill=(0, 0, 0, 0))
        # Bevel highlight on hole upper rim
        curio_img.putpixel((hx, hy - 1), GOLD_LIGHT)

    # Reinforcing stamped ribs along paddle midline
    cd.line([(44, 88), (28, 116)], fill=GOLD_SHINE, width=1)

    # Ground non-slip rubber contact pad along bottom edge (y: 117..120)
    for px in range(18, 40):
        if curio_img.getpixel((px, 117))[3] > 0:
            curio_img.putpixel((px, 117), TUNGSTEN_DARK)
        if curio_img.getpixel((px, 118))[3] > 0:
            curio_img.putpixel((px, 118), (28, 25, 34, 255))

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Core Body Layer)
    # File: chassis_beaver_brass_timber_default.png
    # Deepwood Forest Enamel & Brass Stamped Alloy Chassis (劈木河狸墨綠耐磨漆與黃銅沖壓素體)
    # Features:
    # - 2.2 head-tall chubby barrel-torso chibi toy beaver frame
    # - Deepwood Forest Enamel (#4A7C59) plates with rich multi-tone depth (>=20 unique colors in torso)
    # - Heavy articulated ball-and-socket knees and elbows
    # - Flat metal footplates with non-slip grooved rubber soles at base (y: 114..120)
    # - Short rounded metal ears, coral pink blush roundels (#FF5E8A)
    # - Left hand curves in front of torso (holding grip/balancing)
    # - Right arm held at side, clamp hand strictly x <= 92 (ZERO pixels at x >= 94!)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Legs and Footplates
    # Left leg: Thigh (46..54, 84..96), Knee (48, 97), Shin (46..52, 98..114), Foot (42..54, 114..120)
    # Right leg: Thigh (74..82, 84..96), Knee (78, 97), Shin (76..82, 98..114), Foot (74..86, 114..120)
    for leg_cx, leg_name in [(48.0, "left"), (78.0, "right")]:
        # Thigh (forest green enamel)
        for y in range(84, 98):
            for x in range(int(leg_cx - 6), int(leg_cx + 7)):
                spec = max(0.0, 1.0 - abs(x - leg_cx) / 6.0)
                sh = max(0.0, (y - 84) / 14.0)
                r_c = int(np.clip(74 * (0.95 - 0.2 * sh + 0.25 * spec), 0, 255))
                g_c = int(np.clip(124 * (0.95 - 0.2 * sh + 0.25 * spec), 0, 255))
                b_c = int(np.clip(89 * (0.95 - 0.2 * sh + 0.25 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        # Knee Ball-Joint (brass)
        chd.ellipse([int(leg_cx - 5), 94, int(leg_cx + 5), 102], fill=GOLD_BASE, outline=OUTLINE)
        chd.ellipse([int(leg_cx - 3), 96, int(leg_cx + 3), 100], fill=GOLD_LIGHT)
        chd.point((int(leg_cx), 98), fill=WHITE_SHINE)

        # Shin (forest green enamel with brass vertical reinforcement groove)
        for y in range(100, 115):
            for x in range(int(leg_cx - 5), int(leg_cx + 6)):
                spec = max(0.0, 1.0 - abs(x - leg_cx) / 5.0)
                sh = max(0.0, (y - 100) / 15.0)
                r_c = int(np.clip(74 * (0.95 - 0.18 * sh + 0.25 * spec), 0, 255))
                g_c = int(np.clip(124 * (0.95 - 0.18 * sh + 0.25 * spec), 0, 255))
                b_c = int(np.clip(89 * (0.95 - 0.18 * sh + 0.25 * spec), 0, 255))
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

    # 2. Main Torso / Barrel Body (x: 42..86, y: 58..94)
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
                r_e = int(np.clip(74 * (0.96 - 0.25 * sh_y + 0.28 * spec), 0, 255))
                g_e = int(np.clip(124 * (0.96 - 0.25 * sh_y + 0.28 * spec), 0, 255))
                b_e = int(np.clip(89 * (0.96 - 0.25 * sh_y + 0.28 * spec), 0, 255))
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
    chd.ellipse([60, 68, 68, 76], fill=FOREST_DARK)
    chd.ellipse([62, 70, 66, 74], fill=GOLD_SHINE)

    # 3. Arms / Forelimbs
    # Left Arm: Shoulder (44, 64), Elbow (38, 72), Hand (40, 78) holding balancing grip
    for y in range(64, 80):
        for x in range(36, 46):
            if ((x - 41) / 4.5)**2 + ((y - 71) / 7.5)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 41) / 4.5)
                r_a = int(np.clip(74 * (0.92 + 0.25 * spec), 0, 255))
                g_a = int(np.clip(124 * (0.92 + 0.25 * spec), 0, 255))
                b_a = int(np.clip(89 * (0.92 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    chd.ellipse([38, 75, 43, 80], fill=GOLD_BASE, outline=OUTLINE)  # Brass toy hand clamp

    # Right Arm: Shoulder (84, 64), Elbow (88, 70), Hand (89, 74)
    # STRICT 0-ART9/11 RULE: strictly x <= 92 (no pixels at x >= 94)
    for y in range(64, 76):
        for x in range(83, 93):  # strictly up to 92
            if ((x - 87) / 5.0)**2 + ((y - 69) / 6.0)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 87) / 5.0)
                r_a = int(np.clip(74 * (0.92 + 0.25 * spec), 0, 255))
                g_a = int(np.clip(124 * (0.92 + 0.25 * spec), 0, 255))
                b_a = int(np.clip(89 * (0.92 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_a, g_a, b_a, 255))
    chd.ellipse([87, 71, 92, 76], fill=GOLD_BASE, outline=OUTLINE)  # Brass toy weapon clamp (x <= 92)

    # 4. Neck & Cranial Shell (Head)
    # Neck (58..70, 50..60)
    for y in range(50, 61):
        for x in range(58, 71):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 6.0)
            r_n = int(np.clip(74 * (0.88 + 0.25 * spec), 0, 255))
            g_n = int(np.clip(124 * (0.88 + 0.25 * spec), 0, 255))
            b_n = int(np.clip(89 * (0.88 + 0.25 * spec), 0, 255))
            chassis_img.putpixel((x, y), (r_n, g_n, b_n, 255))
    chd.line([(58, 54), (70, 54)], fill=GOLD_BASE, width=1)
    chd.line([(58, 58), (70, 58)], fill=GOLD_BASE, width=1)

    # Head Cranial Shell: Center (64, 36), radius x: 21.5, radius y: 18
    hcx, hcy = 64.0, 36.0
    for y in range(18, 52):
        for x in range(43, 86):
            dx = (x - hcx) / 21.5
            dy = (y - hcy) / 17.5
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 16.0)
                sh_y = (y - 18.0) / 33.0
                r_h = int(np.clip(74 * (0.96 - 0.22 * sh_y + 0.28 * spec), 0, 255))
                g_h = int(np.clip(124 * (0.96 - 0.22 * sh_y + 0.28 * spec), 0, 255))
                b_h = int(np.clip(89 * (0.96 - 0.22 * sh_y + 0.28 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Muzzle / Snout: Center (64, 48), width x: 54..74, height y: 44..56
    for y in range(44, 57):
        for x in range(54, 75):
            dx = (x - 64.0) / 10.0
            dy = (y - 50.0) / 6.0
            if dx**2 + dy**2 <= 1.05:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 10.0)
                r_m = int(np.clip(74 * (0.92 + 0.25 * spec), 0, 255))
                g_m = int(np.clip(124 * (0.92 + 0.25 * spec), 0, 255))
                b_m = int(np.clip(89 * (0.92 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r_m, g_m, b_m, 255))

    # Snout nostrils plate (stamped brass plate with two tiny mechanical nostrils)
    chd.rounded_rectangle([58, 51, 70, 55], radius=2, fill=FOREST_DARK, outline=OUTLINE)
    chd.rectangle([60, 52, 62, 54], fill=GOLD_BASE, outline=OUTLINE)
    chd.rectangle([66, 52, 68, 54], fill=GOLD_BASE, outline=OUTLINE)

    # Cheek Blush Roundels in Coral Pink (#FF5E8A)
    for bx, by in [(46, 45), (82, 45)]:
        chd.ellipse([bx - 3, by - 2, bx + 3, by + 2], fill=CORAL_BASE)
        chd.point((bx, by), fill=CORAL_LIGHT)

    # Eye Socket Under-rings (deepened socket shadow ready for optic_core)
    for ex in [52, 76]:
        chd.ellipse([ex - 5, 40 - 5, ex + 5, 40 + 5], fill=FOREST_DARK, outline=OUTLINE)

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
    # SLICE 4: HEAD UNIT (Z: 20, Head & Teeth Layer)
    # File: head_unit/head_beaver_chisel_teeth_lumber_cap.png
    # Stamped Brass Chisel Teeth & Sapper Hardcap (沖壓雙聯黃銅鑿齒護下頜與拓荒伐木工硬帽)
    # Features:
    # 1. Sapper Hardcap: Domed forest green enamel helmet with outward flanged rim (y: 12..30, x: 44..84)
    #    and central miniature brass gear crest badge at (64, 16)
    # 2. Short rounded metal ears: left (38..46, 16..26), right (82..90, 16..26)
    # 3. Stamped Brass Chisel Teeth (沖壓雙聯黃銅鑿齒): pair of sturdy flat stamped brass chisel teeth
    #    at (60..63, 54..62) and (65..68, 54..62), with 45-degree chip-clearing bevel cutting edges
    # 4. STRICT 0-ART27 COMPLIANCE: Eye sockets at (52, 40) and (76, 40) MUST BE 100% HOLLOW!
    #    (alpha == 0 in boxes [38..42, 50..54] and [38..42, 74..78])
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Short Rounded Metal Ears
    for ex_base, ear_side in [(42, "left"), (86, "right")]:
        hd.ellipse([ex_base - 5, 16, ex_base + 5, 26], fill=GOLD_BASE, outline=OUTLINE)
        hd.ellipse([ex_base - 3, 18, ex_base + 3, 24], fill=CORAL_BASE)
        hd.point((ex_base, 20), fill=CORAL_LIGHT)

    # 2. Sapper Hardcap Dome (y: 12..30, x: 45..83)
    for y in range(12, 31):
        for x in range(45, 84):
            dx = (x - 64.0) / 19.0
            dy = (y - 25.0) / 13.0
            if dx**2 + dy**2 <= 1.05 and y <= 27:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 18.0)**2)**0.5 / 14.0)
                sh_y = (y - 12.0) / 15.0
                r_h = int(np.clip(74 * (0.95 - 0.2 * sh_y + 0.3 * spec), 0, 255))
                g_h = int(np.clip(124 * (0.95 - 0.2 * sh_y + 0.3 * spec), 0, 255))
                b_h = int(np.clip(89 * (0.95 - 0.2 * sh_y + 0.3 * spec), 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Hardcap Brim (outward-flanged protective rim along y: 26..30, x: 43..85)
    hd.rounded_rectangle([43, 26, 85, 30], radius=2, fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(45, 28), (83, 28)], fill=GOLD_LIGHT, width=1)
    # Brim rivets
    for rx in [46, 54, 74, 82]:
        hd.point((rx, 28), fill=WHITE_SHINE)

    # Central Miniature Brass Gear Crest Badge at (64, 18)
    hd.ellipse([64 - 4, 18 - 4, 64 + 4, 18 + 4], fill=GOLD_BASE, outline=OUTLINE)
    hd.ellipse([64 - 2, 18 - 2, 64 + 2, 18 + 2], fill=SAPPHIRE_BASE)
    hd.point((64, 18), fill=WHITE_SHINE)

    # 3. Stamped Dual Brass Chisel Teeth (沖壓雙聯黃銅鑿齒)
    # Left tooth: (60..63, 54..62), Right tooth: (65..68, 54..62)
    for tx_start in [60, 65]:
        for y in range(54, 63):
            for x in range(tx_start, tx_start + 4):
                spec = max(0.0, 1.0 - abs(x - (tx_start + 1.5)) / 2.0)
                if y >= 61:  # 45-degree cutting bevel edge
                    r_t = int(np.clip(255 * (0.92 + 0.18 * spec), 0, 255))
                    g_t = int(np.clip(235 * (0.92 + 0.18 * spec), 0, 255))
                    b_t = int(np.clip(160 * (0.92 + 0.18 * spec), 0, 255))
                else:
                    r_t = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_t = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_t = int(np.clip(40 * (0.8 + 0.5 * spec) + 40 * spec, 0, 255))
                head_img.putpixel((x, y), (r_t, g_t, b_t, 255))
        # Bevel highlight line
        hd.line([(tx_start, 62), (tx_start + 3, 62)], fill=WHITE_SHINE, width=1)
        # Vertical milling groove
        hd.line([(tx_start + 1, 55), (tx_start + 1, 60)], fill=GOLD_SHINE, width=1)

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
    # SLICE 5: COSTUME (Z: 25, Chest & Armor Layer)
    # File: costume/costume_beaver_deepwood_sapper_harness.png
    # Deepwood Sapper Harness (深林開拓工兵抗磨胸甲與工具背帶)
    # Features:
    # - Fits over torso (x: 44..84, y: 60..94)
    # - Cold-rolled steel breastplate with Dawn Warm Orange (#FFA010) borders
    # - Crossed heavy leather utility suspenders with Fresh Mint Green (#4ED86A) buckles
    # - Sturdy sapper utility belt at waist with brass buckle at (64, 88)
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
                r_c = int(np.clip(58 * (0.85 + 0.4 * spec), 0, 255))
                g_c = int(np.clip(54 * (0.85 + 0.4 * spec), 0, 255))
                b_c = int(np.clip(68 * (0.85 + 0.4 * spec), 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 2. Dawn Warm Orange Scalloped Trim & Shoulder Straps
    # Pauldrons / Strap Pads: Left (42..48, 63..73), Right (80..86, 63..73)
    for px, py_base in [(45, 68), (83, 68)]:
        cosd.ellipse([px - 4, py_base - 5, px + 4, py_base + 5], fill=ORANGE_BASE, outline=OUTLINE)
        cosd.ellipse([px - 2, py_base - 3, px + 2, py_base + 3], fill=ORANGE_LIGHT)
        cosd.point((px, py_base), fill=GOLD_BASE)

    # Diagonal Crossed Utility Suspenders (x: 48..80, y: 64..86)
    # Left strap from (48, 64) to (68, 86)
    for t in np.linspace(0.0, 1.0, 30):
        sx = int(round(48 * (1 - t) + 68 * t))
        sy = int(round(64 * (1 - t) + 86 * t))
        for dx in (-1, 0, 1):
            costume_img.putpixel((sx + dx, sy), ORANGE_BASE)

    # Right strap from (80, 64) to (60, 86)
    for t in np.linspace(0.0, 1.0, 30):
        sx = int(round(80 * (1 - t) + 60 * t))
        sy = int(round(64 * (1 - t) + 86 * t))
        for dx in (-1, 0, 1):
            costume_img.putpixel((sx + dx, sy), ORANGE_BASE)

    # Mint Green (#4ED86A) Tool Clip Buckles at suspender junctions: (56, 72) and (72, 72)
    for bx in [55, 73]:
        cosd.rounded_rectangle([bx - 3, 71, bx + 3, 77], radius=1, fill=MINT_BASE, outline=OUTLINE)
        cosd.point((bx, 74), fill=MINT_SHINE)

    # Central Sapper Badge / Compass Medallion at (64, 74)
    cosd.ellipse([64 - 5, 74 - 5, 64 + 5, 74 + 5], fill=GOLD_BASE, outline=OUTLINE)
    cosd.ellipse([64 - 3, 74 - 3, 64 + 3, 74 + 3], fill=ORANGE_BASE)
    cosd.polygon([(64, 71), (66, 74), (64, 77), (62, 74)], fill=WHITE_SHINE)

    # 3. Waist Heavy Sapper Tool Belt & Brass Buckle at (64, 88)
    cosd.rectangle([48, 87, 80, 92], fill=ORANGE_DARK, outline=OUTLINE)
    cosd.rectangle([60, 86, 68, 93], fill=GOLD_BASE, outline=OUTLINE)
    cosd.ellipse([62, 88, 66, 91], fill=TUNGSTEN_DARK)
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
    # File: optic_core/face_beaver_amber_surveyor_lens.png
    # Amber Surveyor Optic Lens (琥珀金同心圓測量目鏡)
    # Features:
    # - Left eye centered at (52, 40), Right eye centered at (76, 40)
    # - High opacity at centers (alpha == 255 > 200, 0-ART27 compliant)
    # - Deep amber quartz outer ring, bright warm orange iris, crosshair tick marks
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
                        col = AMBER_SHINE
                    elif ratio <= 0.65:
                        col = AMBER_LIGHT
                    elif ratio <= 0.88:
                        col = AMBER_BASE
                    else:
                        col = AMBER_DEEP
                    core_img.putpixel((x, y), col)

        # Concentric Surveyor Scale & Crosshair markings
        cored.ellipse([ex - 5, ey - 5, ex + 5, ey + 5], outline=AMBER_DARK)
        cored.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], outline=AMBER_LIGHT)
        # Crosshair lines
        cored.line([(ex - 4, ey), (ex - 2, ey)], fill=SAPPHIRE_BASE)
        cored.line([(ex + 2, ey), (ex + 4, ey)], fill=SAPPHIRE_BASE)
        cored.line([(ex, ey - 4), (ex, ey - 2)], fill=SAPPHIRE_BASE)
        cored.line([(ex, ey + 2), (ex, ey + 4)], fill=SAPPHIRE_BASE)
        # White specular glints
        core_img.putpixel((ex - 2, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 1, ey - 2), WHITE_SHINE)
        core_img.putpixel((ex - 2, ey - 1), WHITE_SHINE)
        core_img.putpixel((ex + 1, ey + 1), AMBER_SHINE)

    apply_clean_outline(core_img)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Weapon Layer)
    # File: weapon/weapon_beaver_log_greataxe.png
    # Deepwood Log-Splitting Greataxe (深林拓荒劈木巨斧)
    # Features:
    # - Held in right hand: handgrip at (88..92, 68..74)
    # - Shaft extends from counterweight pommel at (85, 82) through grip up to (96, 42)
    # - Heavy double-crescent log-splitting axe head at top (y: 30..56, x: 92..122)
    # - Broad curved primary axe blade sweeping forward (104..122, 32..54) with razor-sharp white edge
    # - Heavy brass counterweight hammer/spike on back (88..96, 38..48)
    # - Sapphire cooling line along blade spine
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Shaft / Handle
    # Shaft points: (85, 84) -> (89, 72) -> (93, 56) -> (97, 40)
    for t in np.linspace(0.0, 1.0, 60):
        sx = 85.0 * (1 - t) + 97.0 * t
        sy = 84.0 * (1 - t) + 40.0 * t
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx**2 + dy**2 <= 1:
                    weapon_img.putpixel((int(round(sx + dx)), int(round(sy + dy))), TUNGSTEN_LIGHT)

    # Pommel at (85, 84)
    wd.ellipse([83, 82, 87, 86], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((85, 84), fill=WHITE_SHINE)

    # Leather wrapped grip at (88..91, 68..74)
    for y in range(68, 75):
        for x in range(88, 92):
            if (y + x) % 2 == 0:
                weapon_img.putpixel((x, y), ORANGE_BASE)
            else:
                weapon_img.putpixel((x, y), TUNGSTEN_DARK)

    # 2. Back Counterweight Hammer / Spike at (86..94, 39..47)
    wd.rectangle([87, 40, 94, 46], fill=GOLD_BASE, outline=OUTLINE)
    wd.polygon([(87, 40), (84, 43), (87, 46)], fill=GOLD_LIGHT, outline=OUTLINE)
    wd.point((85, 43), fill=WHITE_SHINE)

    # 3. Axe Eye / Collar at (94..99, 38..48)
    wd.ellipse([93, 38, 100, 48], fill=TUNGSTEN_DARK, outline=OUTLINE)
    wd.ellipse([94, 39, 99, 47], fill=GOLD_BASE)
    wd.ellipse([95, 41, 98, 45], fill=SAPPHIRE_BASE)

    # 4. Heavy Crescent Log-Splitting Axe Blade (x: 98..124, y: 30..58)
    # Blade polygon:
    # Top flare: (100, 38) -> (108, 30) -> (118, 32)
    # Outer cutting crescent: (118, 32) -> (122, 38) -> (123, 44) -> (122, 50) -> (117, 56)
    # Bottom beard: (117, 56) -> (108, 56) -> (100, 48)
    blade_poly = [
        (98, 40),
        (106, 31),
        (116, 32),
        (121, 38),
        (123, 44),
        (121, 50),
        (116, 56),
        (106, 56),
        (98, 47)
    ]
    wd.polygon(blade_poly, fill=TUNGSTEN_LIGHT, outline=OUTLINE)

    # Shading across the axe blade
    for y in range(30, 58):
        for x in range(98, 124):
            if weapon_img.getpixel((x, y))[3] > 100:
                dist_edge = max(0.0, 1.0 - abs(x - 122.0) / 24.0)
                sh_y = (y - 30.0) / 28.0
                r_b = int(np.clip(74 * (0.85 + 0.35 * dist_edge), 0, 255))
                g_b = int(np.clip(124 * (0.85 + 0.35 * dist_edge), 0, 255))
                b_b = int(np.clip(89 * (0.85 + 0.35 * dist_edge), 0, 255))
                weapon_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Gold Inlaid Timber Sawtooth Pattern on Blade Cheek
    wd.polygon([(102, 42), (107, 36), (112, 42), (107, 46)], fill=GOLD_BASE, outline=OUTLINE)
    wd.polygon([(107, 42), (112, 36), (117, 42), (112, 46)], fill=GOLD_SHINE)

    # Sapphire hydraulic cooling line along blade spine
    wd.line([(100, 43), (114, 43)], fill=SAPPHIRE_SHINE, width=1)

    # Razor-sharp white cutting crescent edge (outer curve)
    crescent_edge = [
        (116, 32), (118, 34), (120, 36), (121, 38), (122, 41),
        (123, 44), (122, 47), (121, 50), (119, 53), (117, 55), (115, 56)
    ]
    for ex, ey in crescent_edge:
        weapon_img.putpixel((ex, ey), WHITE_SHINE)
        weapon_img.putpixel((ex - 1, ey), GOLD_LIGHT)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_beaver_sawtooth_cog_brass", key_img),
        ("back_curio", "curio_beaver_perforated_paddle_tail", curio_img),
        ("chassis", "chassis_beaver_brass_timber_default", chassis_img),
        ("head_unit", "head_beaver_chisel_teeth_lumber_cap", head_img),
        ("costume", "costume_beaver_deepwood_sapper_harness", costume_img),
        ("optic_core", "face_beaver_amber_surveyor_lens", core_img),
        ("weapon", "weapon_beaver_log_greataxe", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{BEAVER_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{BEAVER_PD_DIR}/winding_key/key_beaver_sawtooth_cog_brass.png", f"{KEY_DIR}/key_beaver_sawtooth_cog_brass.png")
    shutil.copyfile(f"{BEAVER_PD_DIR}/weapon/weapon_beaver_log_greataxe.png", f"{WEAPON_DIR}/weapon_beaver_log_greataxe.png")
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

    proof_comp = f"{BEAVER_PD_DIR}/proof_paperdoll_beaver_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{BEAVER_PD_DIR}/proof_paperdoll_beaver_magenta.png"
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

    strip_path = f"{BEAVER_PD_DIR}/proof_beaver_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/beaver_idle_hd.png)
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

        showcase_out = f"{showcase_dir}/beaver_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL WOODCHOPPER BEAVER CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
