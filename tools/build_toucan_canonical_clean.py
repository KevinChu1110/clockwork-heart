#!/usr/bin/env python3
"""
build_toucan_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十一族 彩喙巨嘴鳥 (The Prism-Bill Toucan, toucan) 7 Paperdoll Slices.
Follows:
- docs/world/PRISM_BILL_TOUCAN_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  stamped brass alloy chassis #FFD028, glazed ivory-white porcelain faceplate & bib #FFFDF8,
  multi-layered stamped openwork brass prism bill visor cowl with dopamine gradient
  #FFD028 -> #FFA010 -> #4ED86A -> #38A0FF,
  emerald quartz optic monocle #4ED86A/#38A0FF with gold crosshairs,
  vine valley scout harvest harness #4ED86A with warm sunset orange trim #FFA010,
  segmented copper rudder tail #FFD028/#38A0FF,
  tri-vane canopy rotor brass winding key #FFD028/#4ED86A/#FF5E8A,
  canopy prism pneumatic arquebus #FFD028/#2B2630/#FFA010)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
- High-depth multi-tone cel-shading (>= 3 steps per slot, metal highlights & shadow bevels)
- Subpixel anti-aliased silhouette borders (alpha levels > 2)
- chassis 128 unique colors >= 150, all 7 slots c/100px >= 3.0%
- proof composite unique colors >= 300, core holes <= 0px, head vs chassis L2 < 60.0
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
TOUCAN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/toucan"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Prism-Bill Toucan Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([140, 110, 25], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = np.array([255, 253, 248], dtype=float)
IVORY_LIGHT  = np.array([255, 255, 255], dtype=float)
IVORY_SHADOW = np.array([232, 226, 214], dtype=float)
IVORY_DARK   = np.array([205, 196, 180], dtype=float)
IVORY_DEEP   = np.array([170, 160, 142], dtype=float)

# 2. Primary / Dopamine Brass Gold (#FFD028)
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 3. Secondary / Dopamine Mint Green (#4ED86A)
MINT_SHINE  = np.array([190, 255, 205], dtype=float)
MINT_LIGHT  = np.array([130, 240, 155], dtype=float)
MINT_BASE   = np.array([78, 216, 106], dtype=float)
MINT_DARK   = np.array([42, 160, 68], dtype=float)
MINT_DEEP   = np.array([24, 110, 44], dtype=float)

# 4. Accent / Dopamine Warm Sunset Orange (#FFA010)
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 5. Detail / Celestial Sky Blue (#38A0FF)
SKY_SHINE = np.array([195, 235, 255], dtype=float)
SKY_LIGHT = np.array([120, 205, 255], dtype=float)
SKY_BASE  = np.array([56, 160, 255], dtype=float)
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([14, 60, 130], dtype=float)

# 6. Coral Pink (#FF5E8A)
CORAL_SHINE = np.array([255, 208, 228], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 7. Cold-Rolled Cast Iron / Tungsten Steel (#2B2630)
STEEL_LIGHT = np.array([92, 84, 108], dtype=float)
STEEL_BASE  = np.array([58, 52, 68], dtype=float)
STEEL_SHADOW = np.array([43, 38, 50], dtype=float)
STEEL_DARK  = np.array([28, 24, 34], dtype=float)
STEEL_DEEP  = np.array([18, 15, 22], dtype=float)

WHITE_SHINE = np.array([255, 255, 255], dtype=float)


def apply_antialiased_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=50, ignore_regions=None) -> Image.Image:
    """
    Applies a clean 1px dark outline with smooth anti-aliasing on the outer boundary.
    - Solid interior remains solid (alpha=255).
    - Outline pixels that border transparent space get anti-aliased fractional alpha (e.g. 50..225).
    - Guaranteed to produce alpha levels > 2 (anti-aliasing).
    """
    arr = np.array(img).copy()
    alpha = arr[:, :, 3]
    w, h = img.size
    opaque_mask = alpha > min_alpha

    outline_alpha = np.zeros((h, w), dtype=float)
    outline_rgb = np.zeros((h, w, 3), dtype=float)

    neighbors_4 = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors_diag = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for y in range(h):
        for x in range(w):
            if opaque_mask[y, x]:
                continue
            if ignore_regions:
                skip = False
                for r in ignore_regions:
                    if len(r) == 4:
                        rx1, ry1, rx2, ry2 = r
                        if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                            skip = True
                            break
                    elif len(r) == 3:
                        cx, cy, rad = r
                        if (x - cx)**2 + (y - cy)**2 <= rad**2:
                            skip = True
                            break
                if skip:
                    continue

            ortho_count = 0
            for dx, dy in neighbors_4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    ortho_count += 1

            diag_count = 0
            for dx, dy in neighbors_diag:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    diag_count += 1

            weight = ortho_count * 1.0 + diag_count * 0.45
            if weight > 0.4:
                a_val = min(255.0, weight * 75.0 + 35.0)
                outline_alpha[y, x] = a_val
                outline_rgb[y, x] = outline_color

    out_arr = arr.copy()
    for y in range(h):
        for x in range(w):
            if not opaque_mask[y, x] and outline_alpha[y, x] > 0:
                out_arr[y, x, :3] = outline_rgb[y, x]
                out_arr[y, x, 3] = int(outline_alpha[y, x])

    return Image.fromarray(out_arr, "RGBA")


def point_in_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def build_winding_key() -> Image.Image:
    """
    SLICE 1: WINDING KEY (z=5)
    三葉林冠旋翼黃銅發條鑰匙 (key_toucan_tri_vane_canopy_rotor_brass)
    Features:
    - Center gear shaft at (40, 30), extending backwards from upper back spine.
    - Tri-vane propeller blades (0 deg, 120 deg, 240 deg) cast from polished brass (#FFD028).
    - Mint green enamel protective rim (#4ED86A).
    - Center coral pink dust-cap rivet (#FF5E8A) with specular jewel highlight.
    - Strict 0-ART29 & 0-QA16: uses OUTLINE_KEY (warm bronze) so dark runs < 13, white runs < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    kcx, kcy = 40.0, 30.0

    # 1. Back Socket Axle & Gear Hub
    for y in range(int(kcy - 5), int(kcy + 12)):
        for x in range(int(kcx - 5), int(kcx + 6)):
            dx = (x - kcx) / 4.5
            dy = (y - (kcy + 3)) / 7.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.35:
                    col = GOLD_LIGHT
                elif dot > -0.2:
                    col = GOLD_BASE + dot * 20.0
                else:
                    col = GOLD_DARK
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Tri-vane propeller blades (angles: -90 deg (up), 30 deg (down-right), 150 deg (down-left))
    angles = [-math.pi / 2.0, math.pi / 6.0, 5.0 * math.pi / 6.0]
    blade_length = 20.0
    blade_width = 7.0

    for ang in angles:
        # Build polygon for each aerodynamic propeller vane
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        tan_x, tan_y = -sin_a, cos_a

        p_root_l = (kcx - tan_x * 3.5, kcy - tan_y * 3.5)
        p_root_r = (kcx + tan_x * 3.5, kcy + tan_y * 3.5)
        p_mid_l  = (kcx + cos_a * 11.0 - tan_x * (blade_width * 0.95), kcy + sin_a * 11.0 - tan_y * (blade_width * 0.95))
        p_mid_r  = (kcx + cos_a * 11.0 + tan_x * (blade_width * 0.95), kcy + sin_a * 11.0 + tan_y * (blade_width * 0.95))
        p_tip    = (kcx + cos_a * blade_length, kcy + sin_a * blade_length)

        poly = [p_root_l, p_mid_l, p_tip, p_mid_r, p_root_r]
        min_x = int(math.floor(min(p[0] for p in poly)))
        max_x = int(math.ceil(max(p[0] for p in poly)))
        min_y = int(math.floor(min(p[1] for p in poly)))
        max_y = int(math.ceil(max(p[1] for p in poly)))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if point_in_polygon(x, y, poly):
                    dist = math.sqrt((x - kcx)**2 + (y - kcy)**2)
                    proj = (x - kcx) * cos_a + (y - kcy) * sin_a
                    perp = (x - kcx) * tan_x + (y - kcy) * tan_y

                    dot = -0.55 * (perp / (blade_width + 1e-4)) - 0.70 * (proj / (blade_length + 1e-4))

                    # Mint green enamel rim near outer edge
                    is_rim = (dist > 16.0) or (abs(perp) > blade_width * 0.75)

                    if is_rim:
                        if dot > 0.2:
                            col = MINT_LIGHT + dot * 15.0
                        elif dot > -0.3:
                            col = MINT_BASE + dot * 20.0
                        else:
                            col = MINT_DARK
                    else:
                        if dot > 0.35:
                            col = GOLD_SHINE * 0.35 + GOLD_LIGHT * 0.65
                        elif dot > -0.15:
                            col = GOLD_BASE + dot * 25.0
                        elif dot > -0.55:
                            col = GOLD_DARK + (dot + 0.15) * 20.0
                        else:
                            col = GOLD_DEEP
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Aerodynamic cutout oval in each vane for filigree lightness
    for ang in angles:
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        cox, coy = kcx + cos_a * 10.5, kcy + sin_a * 10.5
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 4.0:
                    px, py = int(cox + dx), int(coy + dy)
                    if 0 <= px < W and 0 <= py < H:
                        key_img.putpixel((px, py), (0, 0, 0, 0))

    # Center decorative collar & coral pink rivet button around (40, 30)
    for y in range(int(kcy - 7), int(kcy + 8)):
        for x in range(int(kcx - 7), int(kcx + 8)):
            dist = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if dist <= 6.5:
                dot = -0.5 * (x - kcx) / 6.5 - 0.7 * (y - kcy) / 6.5
                if dist > 4.5:
                    col = GOLD_DEEP if dot < 0 else GOLD_DARK
                elif dist > 3.0:
                    col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                elif dist > 1.2:
                    col = CORAL_LIGHT if dot > 0.3 else (CORAL_BASE if dot > -0.2 else CORAL_DARK)
                else:
                    col = CORAL_SHINE if dot > 0 else CORAL_LIGHT
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    key_img.putpixel((int(kcx), int(kcy)), (255, 255, 255, 255))
    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    多節沖壓銅片導航尾翼 (curio_toucan_segmented_copper_rudder_tail)
    Features:
    - Folding fan multi-tier stamped copper feathers extending backwards from lower hips at (44, 86)
      to left-downward (18..36, 82..102).
    - Polished brass plates (#FFD028) with celestial sky blue decorative tips (#38A0FF).
    - Exposed brass hinges and micro ball joint.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Micro hip hinge joint at (44, 86)
    jcx, jcy = 44.0, 86.0
    for y in range(82, 91):
        for x in range(40, 49):
            dx = (x - jcx) / 4.0
            dy = (y - jcy) / 4.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                col = GOLD_LIGHT if dot > 0.35 else (GOLD_BASE if dot > -0.25 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3 Folding Fan Stamped Copper Feathers
    # Feather 1 (Upper): from (43, 85) to (20, 80)
    # Feather 2 (Mid):   from (42, 87) to (18, 91)
    # Feather 3 (Lower): from (43, 89) to (24, 100)
    feathers = [
        ([(43, 84), (32, 79), (20, 80), (28, 86), (42, 87)], (20, 80)),
        ([(42, 86), (30, 86), (17, 91), (28, 96), (41, 89)], (17, 91)),
        ([(43, 88), (34, 94), (23, 100), (33, 101), (43, 91)], (23, 100))
    ]

    for poly, tip_pt in feathers:
        min_x = int(min(p[0] for p in poly))
        max_x = int(max(p[0] for p in poly))
        min_y = int(min(p[1] for p in poly))
        max_y = int(max(p[1] for p in poly))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if point_in_polygon(x, y, poly):
                    dist_to_tip = math.sqrt((x - tip_pt[0])**2 + (y - tip_pt[1])**2)
                    dot = -0.55 * (x - 30.0) / 15.0 - 0.70 * (y - 90.0) / 10.0

                    # Sky blue tip enamel decoration within 7px of tip
                    if dist_to_tip < 7.0:
                        if dot > 0.2:
                            col = SKY_LIGHT + dot * 15.0
                        elif dot > -0.3:
                            col = SKY_BASE + dot * 20.0
                        else:
                            col = SKY_DARK
                    else:
                        if dot > 0.35:
                            col = GOLD_LIGHT + dot * 15.0
                        elif dot > -0.25:
                            col = GOLD_BASE + dot * 20.0
                        else:
                            col = GOLD_DARK
                    curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Delicate stamped copper feather rib lines & rivets
    cd.line([(42, 85), (22, 81)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)
    cd.line([(41, 87), (20, 91)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)
    cd.line([(42, 89), (25, 99)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)

    for rx, ry in [(35, 84), (33, 89), (36, 95)]:
        cd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    林冠輕量化合金素體底盤 (chassis_toucan_canopy_alloy_default)
    Features:
    - 2.0 ~ 2.2 head-body ratio chibi bird chassis.
    - Stamped brass alloy (#FFD028) with ivory porcelain chest plate (#FFFDF8).
    - Robust brass 3-claw bird feet with black rubber non-slip pads (left: (50, 105), right: (76, 105)).
    - Soft contact ground shadow for realistic standing weight.
    - Left wing/arm resting forward (38..48, 70..80), right arm wrist ball joint at (86..91, 70..76).
    - STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE STRICTLY 0 PIXELS.
    - STRICT 0-ART18: bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))

    # 2. Bird Legs and 3-Claw Brass Feet (y: 96..112)
    # Left foot centered at (50, 106), Right foot centered at (76, 106)
    for bx, by in [(50.0, 106.0), (76.0, 106.0)]:
        # Brass leg cylinder / thigh strut
        for y in range(int(by - 12), int(by - 2)):
            for x in range(int(bx - 5), int(bx + 6)):
                dx = (x - bx) / 4.5
                dy = (y - (by - 7)) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    if dot > 0.35:
                        col = GOLD_LIGHT + dot * 15.0
                    elif dot > -0.2:
                        col = GOLD_BASE + dot * 20.0
                    else:
                        col = GOLD_DARK + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass spherical ankle joint at (bx, by - 2)
        for y in range(int(by - 4), int(by + 1)):
            for x in range(int(bx - 3), int(bx + 4)):
                if (x - bx)**2 + (y - (by - 1.5))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 1.5) / 3.0
                    col = GOLD_SHINE if dot > 0.4 else (GOLD_BASE + dot * 25.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # 3 Spreading Bird Claws (Left claw, Middle claw, Right claw)
        claws = [
            ((bx, by - 1), (bx - 7, by + 5)),   # outer claw
            ((bx, by - 1), (bx, by + 6)),       # center claw
            ((bx, by - 1), (bx + 7, by + 5))    # inner claw
        ]
        for (cx1, cy1), (cx2, cy2) in claws:
            for t in np.linspace(0.0, 1.0, 16):
                px = cx1 + t * (cx2 - cx1)
                py = cy1 + t * (cy2 - cy1)
                w_rad = 2.0 * (1.0 - t * 0.4)
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        if dx**2 + dy**2 <= w_rad:
                            ix, iy = int(px + dx), int(py + dy)
                            if 0 <= ix < W and 0 <= iy < H and ix < 94:
                                dot = -0.5 * dx - 0.7 * dy
                                col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                                chassis_img.putpixel((ix, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Non-slip rubber sole pads at claw tips
        for tx, ty in [(bx - 7, by + 5), (bx, by + 6), (bx + 7, by + 5)]:
            for dy in [0, 1]:
                for dx in [-1, 0, 1]:
                    ix, iy = int(tx + dx), int(ty + dy)
                    if 0 <= ix < W and 0 <= iy < H and ix < 94:
                        chassis_img.putpixel((ix, iy), tuple(STEEL_DARK.astype(int)) + (255,))

    # 3. Main Torso Brass Alloy Shell (x: 44..84, y: 58..95)
    cx, cy = 64.0, 77.0
    for y in range(58, 96):
        for x in range(44, 85):
            dx = (x - cx) / 18.5
            dy = (y - cy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, -0.6 * dx - 0.7 * dy + 0.4 * nz - 0.55) / 0.45

                if dot > 0.45:
                    col = GOLD_SHINE * 0.7 + GOLD_LIGHT * 0.3 + spec * 25.0
                elif dot > 0.05:
                    col = GOLD_BASE + (dot - 0.05) * 35.0
                elif dot > -0.35:
                    col = GOLD_DARK + (dot + 0.35) * 25.0
                else:
                    col = GOLD_DEEP

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Glazed Ivory Porcelain Throat & Chest Plate (x: 49..79, y: 61..91)
    pcx, pcy = 64.0, 76.0
    for y in range(61, 92):
        for x in range(49, 80):
            pdx = (x - pcx) / 13.5
            pdy = (y - pcy) / 14.0
            pdsq = pdx**2 + pdy**2
            if pdsq <= 1.0:
                pnz = math.sqrt(max(0.0, 1.0 - pdsq))
                pdot = -0.55 * pdx - 0.70 * pdy + 0.45 * pnz
                shine = max(0.0, 1.0 - ((x - (pcx - 3))**2 + (y - (pcy - 4))**2)**0.5 / 4.5)**2

                if pdot > 0.55:
                    col = IVORY_LIGHT + shine * 15.0
                elif pdot > 0.15:
                    col = IVORY_BASE * 0.7 + IVORY_LIGHT * 0.3 + (pdot - 0.15) * 35.0
                elif pdot > -0.25:
                    col = IVORY_SHADOW + (pdot + 0.25) * 30.0
                elif pdot > -0.60:
                    col = IVORY_DARK
                else:
                    col = IVORY_DEEP

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Seams & micro exhaust ventilation slit on porcelain chest
    chd = ImageDraw.Draw(chassis_img)
    chd.line([(64, 64), (64, 88)], fill=tuple(IVORY_DEEP.astype(int)) + (255,), width=1)
    # Horizontal vent slots at chest center
    for vy in [70, 74, 78]:
        chd.line([(60, vy), (68, vy)], fill=tuple(GOLD_DARK.astype(int)) + (255,), width=1)
        chd.point((64, vy), fill=tuple(SKY_LIGHT.astype(int)) + (255,))

    for ry in [68, 76, 84]:
        for rx in [55, 73]:
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 5. Wings / Arms:
    # Left wing/arm: resting forward at (x: 36..47, y: 64..79)
    for y in range(64, 79):
        for x in range(36, 48):
            dx = (x - 42.0) / 5.0
            dy = (y - 71.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right arm: extending to hold firearm grip (x: 82..91, y: 66..78) - STRICT x < 94!
    for y in range(66, 79):
        for x in range(82, 92):
            dx = (x - 87.0) / 4.5
            dy = (y - 72.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right spherical wrist ball joint at (88..91, 70..74)
    chd.ellipse([88, 70, 91, 74], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    chassis_img.putpixel((89, 71), (255, 255, 255, 255))

    # STRICT 0-ART9/11 check: clear all x >= 94
    arr = np.array(chassis_img)
    arr[:, 94:, :] = 0
    clean_img = Image.fromarray(arr, "RGBA")

    out_chassis = apply_antialiased_outline(clean_img, outline_color=OUTLINE, min_alpha=50)

    # Re-enforce x >= 94 is strictly 0 after outline
    arr_out = np.array(out_chassis)
    arr_out[:, 94:, :] = 0
    return Image.fromarray(arr_out, "RGBA")


def build_head_unit() -> Image.Image:
    """
    SLICE 4: HEAD UNIT (z=20)
    彩晶折光巨嘴面罩 (head_toucan_prism_bill_visor_cowl)
    Features:
    - 2.2 head-body ratio Chibi toucan helmet with porcelain cheeks (#FFFDF8).
    - Prominent crest of stamped thin-copper emerald feathers (#4ED86A) on forehead (y: 12..28).
    - Iconic magnificent curved toucan prism bill extending forward-right (x: 70..106, y: 40..58)
      with dopamine rainbow enamel gradient:
      #FFD028 (Lemon Yellow) -> #FFA010 (Sunset Orange) -> #4ED86A (Mint Green) -> #38A0FF (Sky Blue tip).
    - Internal openwork slit showing brass gear ratchets and optical prism track.
    - STRICT 0-ART27: Hollow eye sockets (alpha = 0) at:
      Left eye:  x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Emerald Crest Feathers on forehead apex (x: 52..76, y: 12..28)
    crest_tiers = [
        (64.0, 16.0, 6.0, 6.0),
        (60.0, 22.0, 8.0, 6.0),
        (68.0, 22.0, 8.0, 6.0)
    ]
    for tcx, tcy, trw, trh in crest_tiers:
        for y in range(int(tcy - trh), int(tcy + trh + 1)):
            for x in range(int(tcx - trw), int(tcx + trw + 1)):
                dx = (x - tcx) / trw
                dy = (y - tcy) / trh
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    if dot > 0.35:
                        col = MINT_SHINE * 0.4 + MINT_LIGHT * 0.6
                    elif dot > -0.15:
                        col = MINT_BASE + dot * 25.0
                    elif dot > -0.5:
                        col = MINT_DARK
                    else:
                        col = MINT_DEEP
                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Brass crest fastening ring at (64, 26)
    hd.ellipse([60, 24, 68, 28], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.point((64, 25), fill=tuple(CORAL_BASE.astype(int)) + (255,))

    # 2. Main Head Cranial Dome & Face (x: 44..84, y: 22..62)
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                is_dome = (y < 36) or (y > 55) or (dx**2 > 0.48)

                if is_dome:
                    # Brass cranial helmet
                    if dot > 0.45:
                        col = GOLD_SHINE * 0.7 + GOLD_LIGHT * 0.3 + dot * 20.0
                    elif dot > 0.05:
                        col = GOLD_BASE + (dot - 0.05) * 35.0
                    elif dot > -0.35:
                        col = GOLD_DARK + (dot + 0.35) * 25.0
                    else:
                        col = GOLD_DEEP
                else:
                    # Glazed ivory porcelain faceplate / cheeks
                    pdot = dot
                    shine = max(0.0, 1.0 - ((x - (hcx - 3))**2 + (y - (hcy - 4))**2)**0.5 / 5.0)**2
                    if pdot > 0.50:
                        col = IVORY_LIGHT + shine * 15.0
                    elif pdot > 0.10:
                        col = IVORY_BASE * 0.7 + IVORY_LIGHT * 0.3 + (pdot - 0.10) * 30.0
                    elif pdot > -0.30:
                        col = IVORY_SHADOW + (pdot + 0.30) * 25.0
                    elif pdot > -0.65:
                        col = IVORY_DARK
                    else:
                        col = IVORY_DEEP

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Forehead brass brow arch with warm sunset orange accent
    hd.arc([48, 28, 80, 40], start=180, end=360, fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    hd.arc([49, 29, 79, 39], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)

    # 3. Magnificent Curved Toucan Prism Bill (x: 70..106, y: 40..58)
    # Upper curve: (70, 43) -> (90, 42) -> (104, 48) -> (106, 52)
    # Lower curve: (106, 52) -> (98, 56) -> (82, 57) -> (72, 54)
    # Four-color dopamine rainbow enamel gradient:
    # x: 70..80 (#FFD028 Yellow) -> x: 80..89 (#FFA010 Orange) -> x: 89..98 (#4ED86A Mint Green) -> x: 98..106 (#38A0FF Sky Blue)
    bill_poly = [
        (70, 43), (80, 42), (92, 43), (102, 47), (106, 51), (106, 53),
        (100, 56), (88, 57), (76, 56), (71, 52)
    ]
    min_bx = int(min(p[0] for p in bill_poly))
    max_bx = int(max(p[0] for p in bill_poly))
    min_by = int(min(p[1] for p in bill_poly))
    max_by = int(max(p[1] for p in bill_poly))

    for y in range(min_by, max_by + 1):
        for x in range(min_bx, max_bx + 1):
            if point_in_polygon(x, y, bill_poly):
                # Gradient parameter t along bill length from base to tip
                t = (x - 70.0) / 36.0
                vert_t = (y - 42.0) / 15.0
                dot = -0.55 * (x - 88.0) / 18.0 - 0.70 * (y - 49.0) / 8.0

                if t < 0.28:
                    # 1. Lemon Yellow (#FFD028)
                    base_c = GOLD_BASE
                    light_c = GOLD_LIGHT
                    dark_c = GOLD_DARK
                elif t < 0.55:
                    # 2. Sunset Orange (#FFA010)
                    mix = (t - 0.28) / 0.27
                    base_c = GOLD_BASE * (1.0 - mix) + ORANGE_BASE * mix
                    light_c = GOLD_LIGHT * (1.0 - mix) + ORANGE_LIGHT * mix
                    dark_c = GOLD_DARK * (1.0 - mix) + ORANGE_DARK * mix
                elif t < 0.80:
                    # 3. Mint Green (#4ED86A)
                    mix = (t - 0.55) / 0.25
                    base_c = ORANGE_BASE * (1.0 - mix) + MINT_BASE * mix
                    light_c = ORANGE_LIGHT * (1.0 - mix) + MINT_LIGHT * mix
                    dark_c = ORANGE_DARK * (1.0 - mix) + MINT_DARK * mix
                else:
                    # 4. Sky Blue Tip (#38A0FF)
                    mix = (t - 0.80) / 0.20
                    base_c = MINT_BASE * (1.0 - mix) + SKY_BASE * mix
                    light_c = MINT_LIGHT * (1.0 - mix) + SKY_LIGHT * mix
                    dark_c = MINT_DARK * (1.0 - mix) + SKY_DARK * mix

                if dot > 0.3:
                    col = light_c + dot * 15.0
                elif dot > -0.2:
                    col = base_c + dot * 20.0
                else:
                    col = dark_c

                # Top ridge highlight
                if y == 43 and x < 95:
                    col = col * 0.7 + WHITE_SHINE * 0.3

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Delicate openwork slit / optical prism groove along bill center
    hd.line([(74, 49), (98, 50)], fill=tuple(STEEL_DARK.astype(int)) + (255,), width=1)
    hd.line([(76, 50), (96, 51)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)
    # Bill tip shiny glint
    head_img.putpixel((105, 52), (255, 255, 255, 255))

    # Hollow out eye sockets for optic_core insertion (0-ART27)
    head_arr = np.array(head_img)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_arr[ey, ex, :] = 0
        for ex in range(70, 79):
            head_arr[ey, ex, :] = 0
    head_img = Image.fromarray(head_arr).copy()

    # Apply outline with eye sockets ignored
    ignore_eyes = [(49, 37, 59, 47), (69, 37, 79, 47)]
    out_head = apply_antialiased_outline(head_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=ignore_eyes)

    # Strictly re-enforce zero alpha in hollow eye sockets after outline pass
    head_arr = np.array(out_head)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_arr[ey, ex, :] = 0
        for ex in range(70, 79):
            head_arr[ey, ex, :] = 0

    return Image.fromarray(head_arr, "RGBA")


def build_costume() -> Image.Image:
    """
    SLICE 5: COSTUME (z=30)
    蔓谷探險巡林獵裝 (costume_toucan_vine_valley_scout_harness)
    Features:
    - Scout harvest explorer harness / vest in dopamine mint green (#4ED86A).
    - Sunset warm orange windproof rolled edges (#FFA010).
    - Miniature brass row buttons & buckle (#FFD028).
    - Front bib section (54..74, 62..72), harness vest (48..80, 72..94).
    - STRICT 0-ART26b: y >= 96 MUST BE STRICTLY 0 PIXELS.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    for y in range(62, 95):
        if y < 72:
            x_min = 54 - int((y - 62) * 0.4)
            x_max = 74 + int((y - 62) * 0.4)
        else:
            x_min = 50 - int((y - 72) * 0.3)
            x_max = 78 + int((y - 72) * 0.3)

        for x in range(x_min, x_max + 1):
            dx = (x - 64.0) / ((x_max - x_min) / 2.0)
            dy = (y - 78.0) / 16.0
            dot = -0.55 * dx - 0.70 * dy

            # Mint green scout vest canvas
            if dot > 0.40:
                col = MINT_SHINE * 0.4 + MINT_LIGHT * 0.6
            elif dot > 0.0:
                col = MINT_BASE + dot * 20.0
            elif dot > -0.35:
                col = MINT_DARK + (dot + 0.35) * 25.0
            else:
                col = MINT_DEEP

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sunset Orange Rolled Edges & Hem Trim (#FFA010)
    cd.line([(54, 62), (74, 62)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=2)
    cd.line([(47, 94), (81, 94)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)

    # Lateral vest seam lines
    cd.line([(54, 63), (49, 93)], fill=tuple(ORANGE_DARK.astype(int)) + (255,), width=1)
    cd.line([(74, 63), (79, 93)], fill=tuple(ORANGE_DARK.astype(int)) + (255,), width=1)

    # Center Placket & 4 Miniature Brass Buttons (#FFD028)
    cd.line([(64, 64), (64, 92)], fill=tuple(ORANGE_DEEP.astype(int)) + (255,), width=1)

    button_coords = [(64, 67), (64, 74), (64, 81), (64, 88)]
    for bx, by in button_coords:
        cd.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
        costume_img.putpixel((bx, by - 1), (255, 255, 255, 255))

    # Scout Compass / Whistle Pocket on left chest (53..60, 76..84)
    cd.rectangle([54, 76, 60, 83], outline=tuple(ORANGE_BASE.astype(int)) + (255,), width=1)
    cd.polygon([(57, 78), (55, 81), (59, 81)], fill=tuple(CORAL_BASE.astype(int)) + (255,))

    out_costume = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)

    # STRICT 0-ART26b check: enforce y >= 96 is completely zeroed out
    arr = np.array(out_costume)
    arr[96:, :, :] = 0
    return Image.fromarray(arr, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=25)
    翡翠石英瞄準目鏡 (face_toucan_emerald_quartz_monocle)
    Features:
    - High-transparency biconvex emerald quartz crystal lenses inserted into head_unit hollow eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    - Emerald quartz crystal tint (#4ED86A / #38A0FF).
    - Gold crosshair reticle lines (#FFD028).
    - Specular white eye reflection glint.
    - STRICT 0-ART27: Center alpha MUST BE 255.
    - Hollow sockets 100% covered by dark frame + crystal, zero holes.
    """
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    eye_centers = [(54, 42), (74, 42)]
    radius = 4.0

    for cx, cy in eye_centers:
        # 1. Fill entire socket rectangle with dark blue-purple eye frame (#1F1A3A)
        cored.rounded_rectangle([cx - 4, cy - 4, cx + 4, cy + 4], radius=1, fill=tuple(OUTLINE.astype(int)) + (255,))

        # 2. Emerald Quartz crystal lens inside frame
        for y in range(int(cy - radius), int(cy + radius + 1)):
            for x in range(int(cx - radius), int(cx + radius + 1)):
                dx = (x - cx) / radius
                dy = (y - cy) / radius
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.25:
                        col = MINT_SHINE * 0.7 + WHITE_SHINE * 0.3
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = MINT_LIGHT * (1.0 - t) + MINT_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = MINT_BASE * (1.0 - t) + SKY_BASE * t + dot * 12.0
                    else:
                        col = SKY_DARK * 0.7 + OUTLINE * 0.3
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Gold reticle crosshairs & crystal facet lines
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(GOLD_SHINE.astype(int)) + (255,))

        # Specular white eye reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(MINT_LIGHT.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    林冠聚能氣動銃 (weapon_toucan_canopy_prism_pneumatic_arquebus)
    Features:
    - Long octagonal engraved brass pneumatic barrel from x: 68 to x: 124, y: 70..76.
    - Flower-shaped petal pressure muzzle brake at (118..124, 69..77).
    - Side-mounted revolving clockwork feed magazine / wheel at (82..94, 76..84) with sunset orange and mint dots.
    - High-pressure pneumatic reservoir cylinder under barrel (74..104, 75..79).
    - Grip and receiver positioned around standard right-hand grip (88, 76).
    - Completely decoupled from character body/limbs (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Receiver & Walnut/Brass Stock (x: 62..86, y: 71..80)
    stock_poly = [(62, 74), (72, 72), (86, 73), (88, 77), (84, 80), (74, 80), (64, 78)]
    wd.polygon(stock_poly, fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    for y in range(72, 80):
        for x in range(64, 86):
            p = weapon_img.getpixel((x, y))
            if p[3] > 0:
                dot = -0.55 * (x - 74.0) / 12.0 - 0.70 * (y - 76.0) / 4.0
                if dot > 0.3:
                    col = GOLD_LIGHT + dot * 12.0
                elif dot > -0.2:
                    col = GOLD_BASE + dot * 18.0
                else:
                    col = GOLD_DARK + (dot + 0.2) * 15.0
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Trigger guard at (84, 78)
    wd.ellipse([82, 76, 88, 82], fill=tuple(GOLD_DARK.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    wd.point((85, 78), fill=tuple(GOLD_BASE.astype(int)) + (255,))

    # 2. Side-Mounted Revolving Clockwork Feed Magazine (x: 82..94, y: 76..85)
    mcx, mcy = 88.0, 80.5
    for y in range(int(mcy - 5), int(mcy + 6)):
        for x in range(int(mcx - 5), int(mcx + 6)):
            dist = math.sqrt((x - mcx)**2 + (y - mcy)**2)
            if dist <= 4.8:
                dot = -0.5 * (x - mcx) / 4.8 - 0.7 * (y - mcy) / 4.8
                if dist > 3.2:
                    col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                elif dist > 1.5:
                    col = ORANGE_BASE if (x + y) % 2 == 0 else MINT_BASE
                else:
                    col = GOLD_SHINE
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Under-Barrel High-Pressure Brass Pneumatic Cylinder (x: 74..104, y: 75..79)
    for y in range(75, 80):
        for x in range(74, 105):
            spec = max(0.0, 1.0 - abs(y - 77.0) / 2.0)
            dot = -0.55 * (x - 89.0) / 15.0 - 0.70 * (y - 77.0) / 2.0
            col = GOLD_LIGHT if dot > 0.25 else (GOLD_BASE if dot > -0.25 else GOLD_DARK)
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Main Long Octagonal Engraved Arquebus Barrel (x: 68..120, y: 70..75)
    for y in range(70, 76):
        for x in range(68, 121):
            spec = max(0.0, 1.0 - abs(y - 72.5) / 2.5)
            shine = max(0.0, 1.0 - abs(y - 71.5) / 1.2)**2
            dot = -0.55 * (x - 94.0) / 26.0 - 0.70 * (y - 72.5) / 2.5
            if dot > 0.25:
                col = GOLD_LIGHT + dot * 15.0 + 25.0 * shine
            elif dot > -0.25:
                col = GOLD_BASE + dot * 20.0
            else:
                col = GOLD_DARK + (dot + 0.25) * 15.0
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Engraved vines and rings along barrel
    for rx in [86, 98, 110]:
        wd.line([(rx, 69), (rx, 76)], fill=tuple(MINT_BASE.astype(int)) + (255,), width=1)

    # 5. Petal-Shaped Pressure Relief Muzzle Brake (x: 118..124, y: 69..77)
    wd.rectangle([118, 70, 122, 76], fill=tuple(GOLD_DARK.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    wd.line([(120, 69), (124, 69)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=1)
    wd.line([(120, 77), (124, 77)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=1)
    # Needle spark center
    wd.line([(122, 73), (125, 73)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)
    weapon_img.putpixel((125, 73), (255, 255, 255, 255))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第六十一族 彩喙巨嘴鳥 (toucan) ===")

    key_img = build_winding_key()
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    curio_img = build_back_curio()
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    chassis_img = build_chassis()
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    head_img = build_head_unit()
    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    costume_img = build_costume()
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    core_img = build_optic_core()
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    weapon_img = build_weapon()
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slice_data = [
        ("winding_key", "key_toucan_tri_vane_canopy_rotor_brass", key_img),
        ("back_curio", "curio_toucan_segmented_copper_rudder_tail", curio_img),
        ("chassis", "chassis_toucan_canopy_alloy_default", chassis_img),
        ("head_unit", "head_toucan_prism_bill_visor_cowl", head_img),
        ("costume", "costume_toucan_vine_valley_scout_harness", costume_img),
        ("optic_core", "face_toucan_emerald_quartz_monocle", core_img),
        ("weapon", "weapon_toucan_canopy_prism_pneumatic_arquebus", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{TOUCAN_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        # 128px
        p128 = f"{slot_dir}/{item_id}.png"
        img_128.save(p128)
        # 512px LANCZOS
        p512 = f"{slot_dir}/{item_id}_512.png"
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(p512)
        print(f"  ✓ Saved {slot} 128x128 and 512x512 LANCZOS: {item_id}")

    # Copy universal key & weapon
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_toucan_tri_vane_canopy_rotor_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_toucan_canopy_prism_pneumatic_arquebus.png")
    print("  ✓ Universal key and weapon copies updated")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{TOUCAN_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{TOUCAN_PD_DIR}/proof_paperdoll_toucan_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{TOUCAN_PD_DIR}/proof_paperdoll_toucan_magenta.png"
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

    strip_path = f"{TOUCAN_PD_DIR}/proof_toucan_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/toucan_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/toucan_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/toucan_idle.png
    p_idle_64 = f"{PLAYER_DIR}/toucan_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/toucan_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/toucan_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/toucan_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/toucan_idle.png"
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
        char_resized = char_crop.resize((sc_w, sc_h), Image.Resampling.LANCZOS)
        showcase = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        px = (800 - sc_w) // 2
        py = (1200 - sc_h) // 2 + 50
        showcase.alpha_composite(char_resized, (px, py))
        showcase_path = f"{SHOWCASE_DIR}/toucan_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)


if __name__ == "__main__":
    build_all()
