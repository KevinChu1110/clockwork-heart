#!/usr/bin/env python3
"""
build_takin_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十三族 破竹羚牛 (The Bamboo-Cleaving Takin, takin) 7 Paperdoll Slices.
Follows:
- docs/world/BAMBOO_CLEAVING_TAKIN_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, bronze cast iron alloy chassis #486658,
  glazed ivory-white porcelain belly plate #FFFDF8, cold-rolled tungsten steel cowl with brass twisted horns #FFD028,
  twin bamboo-oil flasks with pneumatic pressure-relief valve & steam puffs,
  emerald quartz crystal visors #4ED86A/#38A0FF with deep blue-purple frame #1F1A3A,
  zen pioneer heavy robe with single-sided forged brass pauldron #FFA010/#FFD028/#EADDC3,
  zen bamboo-cleaving battle axe with bamboo-weave grip and taichi/zen venting vents,
  tri-leaf zen brass wind-up key with center coral pink rivet #FFD028/#FF5E8A)
- review.md 0-ART5, 0-ART6, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
- High-depth multi-tone cel-shading (>= 3 steps per slot, metal highlights & shadow bevels)
- Subpixel anti-aliased silhouette borders (alpha levels > 2)
- chassis 128 unique colors >= 150, all 7 slots c/100px >= 3.0%
- proof composite unique colors >= 300, core holes <= 5px, head vs chassis overlap < 10%
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAKIN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Bamboo-Cleaving Takin Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = np.array([255, 253, 248], dtype=float)
IVORY_LIGHT  = np.array([255, 255, 255], dtype=float)
IVORY_SHADOW = np.array([232, 226, 214], dtype=float)
IVORY_DARK   = np.array([205, 196, 180], dtype=float)
IVORY_DEEP   = np.array([170, 160, 142], dtype=float)

# 2. Bronze Cast Iron Alloy (#486658 / #5A7E6C) - Takin Core Metal
BRONZE_SHINE  = np.array([148, 180, 162], dtype=float)
BRONZE_LIGHT  = np.array([112, 146, 128], dtype=float)
BRONZE_BASE   = np.array([76, 106, 92], dtype=float)
BRONZE_SHADOW = np.array([54, 78, 68], dtype=float)
BRONZE_DARK   = np.array([36, 54, 46], dtype=float)
BRONZE_DEEP   = np.array([22, 36, 30], dtype=float)

# 3. Tungsten Steel Cowl (#4A5A62) - Tuned close to bronze for 0-ART28q (L2 < 60.0)
STEEL_SHINE  = np.array([146, 172, 170], dtype=float)
STEEL_LIGHT  = np.array([110, 138, 134], dtype=float)
STEEL_BASE   = np.array([76, 102, 98], dtype=float)
STEEL_SHADOW = np.array([54, 76, 72], dtype=float)
STEEL_DARK   = np.array([36, 52, 50], dtype=float)
STEEL_DEEP   = np.array([22, 34, 32], dtype=float)

# 4. Metal / Dopamine Foundry Brass Gold (#FFD028) - Twisted Horns, Key, Pauldron, Rivets
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 5. Accent / Dopamine Warm Sunset Orange (#FFA010)
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 6. Mint Green / Bamboo Emerald (#4ED86A) - Visors, Oil Flasks, Bamboo Grip
MINT_SHINE  = np.array([190, 255, 205], dtype=float)
MINT_LIGHT  = np.array([130, 240, 155], dtype=float)
MINT_BASE   = np.array([78, 216, 106], dtype=float)
MINT_DARK   = np.array([42, 160, 68], dtype=float)
MINT_DEEP   = np.array([24, 110, 44], dtype=float)

# 7. Secondary / Celestial Sky Blue (#38A0FF)
SKY_SHINE = np.array([195, 235, 255], dtype=float)
SKY_LIGHT = np.array([120, 205, 255], dtype=float)
SKY_BASE  = np.array([56, 160, 255], dtype=float)
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([14, 60, 130], dtype=float)

# 8. Coral Pink (#FF5E8A) - Rivets, Knots
CORAL_SHINE = np.array([255, 208, 228], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 9. Natural Raw Linen Robe (#EADDC3)
ROBE_SHINE  = np.array([252, 248, 238], dtype=float)
ROBE_LIGHT  = np.array([244, 236, 216], dtype=float)
ROBE_BASE   = np.array([226, 214, 188], dtype=float)
ROBE_SHADOW = np.array([196, 182, 154], dtype=float)
ROBE_DARK   = np.array([160, 144, 118], dtype=float)
ROBE_DEEP   = np.array([120, 105, 84], dtype=float)

# 10. Sharp Bamboo-Cleaving Axe Blade (#C2E5D3)
BLADE_SHINE  = np.array([238, 252, 245], dtype=float)
BLADE_LIGHT  = np.array([196, 232, 214], dtype=float)
BLADE_BASE   = np.array([142, 200, 170], dtype=float)
BLADE_SHADOW = np.array([90, 152, 122], dtype=float)
BLADE_DARK   = np.array([50, 102, 80], dtype=float)

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
                for rx1, ry1, rx2, ry2 in ignore_regions:
                    if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                        skip = True
                        break
                if skip:
                    continue

            # Check neighbors
            cnt_4 = 0
            for dx, dy in neighbors_4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    cnt_4 += 1

            cnt_diag = 0
            for dx, dy in neighbors_diag:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    cnt_diag += 1

            if cnt_4 > 0 or cnt_diag > 0:
                coverage = (cnt_4 * 1.0 + cnt_diag * 0.4) / 4.4
                a = int(np.clip(coverage * 230.0 + 35.0, 50.0, 255.0))
                outline_alpha[y, x] = a
                outline_rgb[y, x] = outline_color

    # Composite: original on top of outline
    res = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            if opaque_mask[y, x]:
                res[y, x] = arr[y, x]
            elif outline_alpha[y, x] > 0:
                res[y, x, :3] = outline_rgb[y, x]
                res[y, x, 3] = int(outline_alpha[y, x])
    return Image.fromarray(res, "RGBA")


def point_in_polygon(x: float, y: float, poly: list) -> bool:
    inside = False
    n = len(poly)
    for i in range(n):
        p1x, p1y = poly[i]
        p2x, p2y = poly[(i + 1) % n]
        if min(p1y, p2y) < y <= max(p1y, p2y):
            if x <= max(p1x, p2x):
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                if p1x == p2x or x <= xinters:
                    inside = not inside
    return inside


def build_winding_key() -> Image.Image:
    """
    SLICE 1: WINDING KEY (z=5)
    三葉天元雕花黃銅發條鑰匙 (key_takin_tri_leaf_zen_brass)
    Tri-Leaf Zen Brass Wind-up Key.
    Central axle collar extending from chassis at (44, 48) to (38, 28).
    Three filigree lotus/bamboo-leaf shaped wings radiating from (38, 28) at 90 deg (up),
    210 deg (down-left), and 330 deg (down-right).
    Center coral pink rivet (CORAL_BASE), warm golden bronze outline OUTLINE_KEY.
    Strictly follows 0-ART29 & 0-QA16: no dark block run >= 13, white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    kcx, kcy = 38.0, 28.0

    # Axle connecting chassis socket (44, 48) to key center (38, 28)
    axle_pts = [(45, 48), (47, 49), (40, 29), (37, 28)]
    kd.polygon(axle_pts, fill=tuple(GOLD_DARK.astype(int)) + (255,))
    kd.line([(38, 29), (45, 48)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)

    # Three leaves at angles:
    # Leaf 1: Top (angle = -90 deg / 270 deg) -> points upward to (38, 10)
    # Leaf 2: Bottom-Left (angle = 150 deg) -> points to (20, 38)
    # Leaf 3: Bottom-Right (angle = 30 deg) -> points to (56, 38)
    leaf_angles = [-math.pi / 2.0, math.pi * 5.0 / 6.0, math.pi / 6.0]

    for ang in leaf_angles:
        # Construct a bamboo/lotus petal polygon
        cos_a = math.cos(ang)
        sin_a = math.sin(ang)
        # Perpendicular
        perp_x = -sin_a
        perp_y = cos_a

        # Points along petal: base (r=6), waist (r=14, w=7), tip (r=20)
        p_base_l = (kcx + 6.0 * cos_a - 3.5 * perp_x, kcy + 6.0 * sin_a - 3.5 * perp_y)
        p_mid_l  = (kcx + 14.0 * cos_a - 6.5 * perp_x, kcy + 14.0 * sin_a - 6.5 * perp_y)
        p_tip    = (kcx + 20.0 * cos_a, kcy + 20.0 * sin_a)
        p_mid_r  = (kcx + 14.0 * cos_a + 6.5 * perp_x, kcy + 14.0 * sin_a + 6.5 * perp_y)
        p_base_r = (kcx + 6.0 * cos_a + 3.5 * perp_x, kcy + 6.0 * sin_a + 3.5 * perp_y)

        poly = [p_base_l, p_mid_l, p_tip, p_mid_r, p_base_r]

        min_x = max(0, int(min(p[0] for p in poly)))
        max_x = min(W - 1, int(max(p[0] for p in poly)))
        min_y = max(0, int(min(p[1] for p in poly)))
        max_y = min(H - 1, int(max(p[1] for p in poly)))

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if point_in_polygon(x, y, poly):
                    dist = math.sqrt((x - kcx)**2 + (y - kcy)**2)
                    dot = -0.55 * (x - kcx) / (dist + 1e-5) - 0.70 * (y - kcy) / (dist + 1e-5)
                    # Beveled shading
                    if dot > 0.35:
                        col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                    elif dot > -0.15:
                        col = GOLD_BASE + dot * 25.0
                    elif dot > -0.55:
                        col = GOLD_DARK + (dot + 0.15) * 20.0
                    else:
                        col = GOLD_DEEP
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Inner cutout for filigree lightness
        c_base = (kcx + 9.0 * cos_a, kcy + 9.0 * sin_a)
        c_mid_l = (kcx + 14.0 * cos_a - 2.5 * perp_x, kcy + 14.0 * sin_a - 2.5 * perp_y)
        c_tip = (kcx + 17.5 * cos_a, kcy + 17.5 * sin_a)
        c_mid_r = (kcx + 14.0 * cos_a + 2.5 * perp_x, kcy + 14.0 * sin_a + 2.5 * perp_y)
        c_poly = [c_base, c_mid_l, c_tip, c_mid_r]

        c_min_x = max(0, int(min(p[0] for p in c_poly)))
        c_max_x = min(W - 1, int(max(p[0] for p in c_poly)))
        c_min_y = max(0, int(min(p[1] for p in c_poly)))
        c_max_y = min(H - 1, int(max(p[1] for p in c_poly)))

        for y in range(c_min_y, c_max_y + 1):
            for x in range(c_min_x, c_max_x + 1):
                if point_in_polygon(x, y, c_poly):
                    key_img.putpixel((x, y), (0, 0, 0, 0))

    # Center decorative collar & coral button around (38, 28)
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
    雙聯竹露油壺減震閥 (curio_takin_dual_bamboo_oil_flasks)
    Twin Bamboo-Oil Flasks & Pneumatic Steam Damper Valve.
    Mounted on left hip/back bracket at (44, 84).
    Dual jade-green bamboo cylindrical flasks with brass protective mesh cage (x: 22..40, y: 72..92),
    brass pressure regulator valve, and micro steam puffs venting upward at (20, 70).
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Back mounting bracket / ball joint at (43, 85)
    jcx, jcy = 43.0, 85.0
    for y in range(80, 91):
        for x in range(38, 48):
            dx = (x - jcx) / 4.5
            dy = (y - jcy) / 4.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                col = GOLD_LIGHT if dot > 0.35 else (GOLD_BASE if dot > -0.25 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Dual Flasks:
    # Flask 1 (Inner/Upper): centered at (34, 82), radius 4.5, height 12
    # Flask 2 (Outer/Lower): centered at (26, 86), radius 4.0, height 11
    flasks = [
        (34.0, 82.0, 4.5, 6.0),
        (26.0, 86.0, 4.0, 5.5)
    ]

    for fcx, fcy, rx, ry_half in flasks:
        # Flask body (Jade Bamboo-Oil Glass with brass cage)
        for y in range(int(fcy - ry_half), int(fcy + ry_half + 1)):
            for x in range(int(fcx - rx), int(fcx + rx + 1)):
                dx = (x - fcx) / rx
                dy = (y - fcy) / ry_half
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    # Glass liquid center with brass cage ribs
                    is_brass_rib = (abs(x - fcx) < 1.0) or (abs(y - fcy) < 1.0) or (abs(y - (fcy - ry_half * 0.5)) < 1.0)
                    if is_brass_rib:
                        col = GOLD_LIGHT if dot > 0.2 else GOLD_BASE
                    else:
                        if dot > 0.4:
                            col = MINT_SHINE * 0.6 + MINT_LIGHT * 0.4
                        elif dot > 0.0:
                            col = MINT_BASE + dot * 20.0
                        elif dot > -0.35:
                            col = MINT_DARK
                        else:
                            col = MINT_DEEP
                    curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Top brass cap & nozzle
        for dy in range(-3, 1):
            for dx in range(-int(rx - 1), int(rx)):
                px = int(fcx + dx)
                py = int(fcy - ry_half + dy)
                if 0 <= px < W and 0 <= py < H:
                    curio_img.putpixel((px, py), tuple(np.clip(GOLD_BASE, 0, 255).astype(int)) + (255,))

    # 3. Pressure relief pipe from outer flask (26, 81) curving upward to nozzle (20, 72)
    pipe_pts = [(26.0, 81.0), (22.0, 76.0), (20.0, 72.0)]
    for t in np.linspace(0.0, 1.0, 25):
        px = int((1.0 - t)**2 * pipe_pts[0][0] + 2.0 * (1.0 - t) * t * pipe_pts[1][0] + t**2 * pipe_pts[2][0])
        py = int((1.0 - t)**2 * pipe_pts[0][1] + 2.0 * (1.0 - t) * t * pipe_pts[1][1] + t**2 * pipe_pts[2][1])
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx**2 + dy**2 <= 1:
                    curio_img.putpixel((px + dx, py + dy), tuple(GOLD_BASE.astype(int)) + (255,))

    # Brass nozzle ring at (20, 72)
    cd.ellipse([18, 70, 22, 74], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Apply outline on solid metal parts FIRST so steam doesn't get dark borders
    curio_outlined = apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)

    # Cute miniature steam puffs at nozzle tip (attached directly to nozzle, no floating border)
    puffs = [(19.0, 68.0, 2.5), (17.5, 64.5, 2.0)]
    for sx, sy, sr in puffs:
        for y in range(int(sy - sr - 1), int(sy + sr + 2)):
            for x in range(int(sx - sr - 1), int(sx + sr + 2)):
                dist = math.sqrt((x - sx)**2 + (y - sy)**2)
                if dist <= sr:
                    alpha = int(np.clip((1.0 - dist / sr) * 140.0 + 30.0, 0, 180))
                    dot = -0.5 * (x - sx) / sr - 0.7 * (y - sy) / sr
                    col = WHITE_SHINE if dot > 0 else IVORY_LIGHT
                    curio_outlined.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (alpha,))

    return curio_outlined


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    青古銅鑄鐵重裝底盤 (chassis_takin_bronze_cast_default)
    2.2 head-body ratio chibi chassis, bronze cast iron body (#486658 / BRONZE),
    ivory porcelain belly plate (#FFFDF8), brass knee & shoulder ball joints (#FFD028),
    heavy anti-skid slate/bronze hooves (y: 98..112).
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    STRICT 0-ART18: Bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))

    # 2. Main Feet / Hooves (y: 98..112)
    # Left hoof: centered at (50, 105), Right hoof: centered at (76, 105)
    for bx, by in [(50.0, 105.0), (76.0, 105.0)]:
        # Thigh / Leg bronze metal cylinder
        for y in range(int(by - 14), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.0
                dy = (y - (by - 8)) / 7.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.7 * dy
                    if dot > 0.35:
                        col = BRONZE_LIGHT + dot * 15.0
                    elif dot > -0.2:
                        col = BRONZE_BASE + dot * 20.0
                    else:
                        col = BRONZE_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass knee cap joint
        for y in range(int(by - 11), int(by - 6)):
            for x in range(int(bx - 3), int(bx + 4)):
                if (x - bx)**2 + (y - (by - 8.5))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 8.5) / 3.0
                    col = GOLD_SHINE if dot > 0.4 else (GOLD_BASE + dot * 25.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Hoof boot base (cloven hoof split plate)
        for y in range(int(by - 5), int(by + 7)):
            for x in range(int(bx - 8), int(bx + 9)):
                dx = (x - bx) / 7.5
                dy = (y - by) / 6.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    # Center hoof slit
                    is_slit = (abs(x - bx) < 1.0) and (y >= by)
                    if is_slit:
                        col = BRONZE_DEEP
                    elif y >= by + 4:
                        col = BRONZE_DARK if dot < 0 else BRONZE_SHADOW
                    else:
                        if dot > 0.4:
                            col = BRONZE_LIGHT + dot * 15.0
                        elif dot > -0.2:
                            col = BRONZE_BASE + dot * 20.0
                        else:
                            col = BRONZE_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Main Torso Bronze Cast Body (x: 44..84, y: 58..95)
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
                    col = BRONZE_SHINE * 0.7 + BRONZE_LIGHT * 0.3 + spec * 25.0
                elif dot > 0.05:
                    col = BRONZE_BASE + (dot - 0.05) * 35.0
                elif dot > -0.35:
                    col = BRONZE_SHADOW + (dot + 0.35) * 25.0
                else:
                    col = BRONZE_DARK

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Glazed Ivory Porcelain Belly Plate (x: 49..79, y: 61..91)
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

    # Seams & brass rivets on porcelain belly
    chd = ImageDraw.Draw(chassis_img)
    chd.line([(64, 64), (64, 88)], fill=tuple(IVORY_DEEP.astype(int)) + (255,), width=1)
    for ry in [68, 76, 84]:
        for rx in [56, 72]:
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 5. Shoulders & Arms:
    # Left arm: resting beside torso (x: 36..47, y: 64..81)
    for y in range(64, 82):
        for x in range(36, 48):
            dx = (x - 41.5) / 5.0
            dy = (y - 72.0) / 8.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = BRONZE_LIGHT if dot > 0.3 else (BRONZE_BASE if dot > -0.2 else BRONZE_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right arm: extending forward to hold axe grip (x: 82..91, y: 66..78)
    # STRICT 0-ART9/11: x MUST NOT exceed 93!
    for y in range(66, 79):
        for x in range(82, 92):
            dx = (x - 87.0) / 4.5
            dy = (y - 72.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = BRONZE_LIGHT if dot > 0.3 else (BRONZE_BASE if dot > -0.2 else BRONZE_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right palm / wrist node (x: 88..91, y: 70..74)
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
    黃銅反曲扭角重盔 (head_takin_brass_twisted_horn_cowl)
    Tungsten steel helmet dome (#4A5A62), ivory porcelain cheeks,
    signature Brass Twisted Horns (#FFD028 / #FFA010) arching up and back,
    convex takin bridge muzzle with brass septum ring.
    STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
      Left eye: x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    STRICT 0-ART28q: Average plate color distance to chassis L2 < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Signature Brass Twisted Horns (Takin signature curved horns)
    # Origin at forehead top-center (64, 24).
    # Takin horns curve outward sideways, then sweep upward and backward gracefully!
    # Left Horn: (62, 23) -> (46, 20) -> (36, 12) -> (40, 4)
    left_horn_pts = [(62.0, 23.0), (44.0, 20.0), (34.0, 11.0), (38.0, 4.0)]
    for t in np.linspace(0.0, 1.0, 40):
        # Cubic curve
        hx = (1-t)**3 * left_horn_pts[0][0] + 3*(1-t)**2*t * left_horn_pts[1][0] + 3*(1-t)*t**2 * left_horn_pts[2][0] + t**3 * left_horn_pts[3][0]
        hy = (1-t)**3 * left_horn_pts[0][1] + 3*(1-t)**2*t * left_horn_pts[1][1] + 3*(1-t)*t**2 * left_horn_pts[2][1] + t**3 * left_horn_pts[3][1]
        radius = 3.8 * (1.0 - t * 0.65)
        for dy in range(-int(radius + 1), int(radius + 2)):
            for dx in range(-int(radius + 1), int(radius + 2)):
                if dx**2 + dy**2 <= radius**2:
                    px, py = int(hx + dx), int(hy + dy)
                    if 0 <= px < W and 0 <= py < H:
                        dot = -0.55 * (dx / (radius + 1e-5)) - 0.70 * (dy / (radius + 1e-5))
                        if dot > 0.4:
                            col = GOLD_SHINE * 0.6 + GOLD_LIGHT * 0.4
                        elif dot > 0.0:
                            col = GOLD_BASE + dot * 20.0
                        elif dot > -0.4:
                            col = GOLD_DARK
                        else:
                            col = GOLD_DEEP
                        head_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Horn: (66, 23) -> (84, 20) -> (94, 11.0) -> (90, 4.0)
    right_horn_pts = [(66.0, 23.0), (84.0, 20.0), (94.0, 11.0), (90.0, 4.0)]
    for t in np.linspace(0.0, 1.0, 40):
        hx = (1-t)**3 * right_horn_pts[0][0] + 3*(1-t)**2*t * right_horn_pts[1][0] + 3*(1-t)*t**2 * right_horn_pts[2][0] + t**3 * right_horn_pts[3][0]
        hy = (1-t)**3 * right_horn_pts[0][1] + 3*(1-t)**2*t * right_horn_pts[1][1] + 3*(1-t)*t**2 * right_horn_pts[2][1] + t**3 * right_horn_pts[3][1]
        radius = 3.8 * (1.0 - t * 0.65)
        for dy in range(-int(radius + 1), int(radius + 2)):
            for dx in range(-int(radius + 1), int(radius + 2)):
                if dx**2 + dy**2 <= radius**2:
                    px, py = int(hx + dx), int(hy + dy)
                    if 0 <= px < W and 0 <= py < H:
                        dot = -0.55 * (dx / (radius + 1e-5)) - 0.70 * (dy / (radius + 1e-5))
                        if dot > 0.4:
                            col = GOLD_SHINE * 0.6 + GOLD_LIGHT * 0.4
                        elif dot > 0.0:
                            col = GOLD_BASE + dot * 20.0
                        elif dot > -0.4:
                            col = GOLD_DARK
                        else:
                            col = GOLD_DEEP
                        head_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Horn tips golden resonant spheres
    hd.ellipse([36, 2, 41, 7], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([87, 2, 92, 7], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Horn base rosette collar at (64, 24)
    hd.ellipse([60, 21, 68, 27], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([62, 22, 66, 26], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    head_img.putpixel((64, 23), (255, 255, 255, 255))

    # 2. Main Head Dome & Visor (x: 44..84, y: 22..62)
    hcx, hcy = 64.0, 42.0
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                is_dome = (y < 38) or (y > 55) or (dx**2 > 0.48)

                if is_dome:
                    # Polished tungsten steel / bronze helmet
                    if dot > 0.45:
                        col = STEEL_SHINE * 0.7 + STEEL_LIGHT * 0.3 + dot * 20.0
                    elif dot > 0.05:
                        col = STEEL_BASE + (dot - 0.05) * 35.0
                    elif dot > -0.35:
                        col = STEEL_SHADOW + (dot + 0.35) * 25.0
                    else:
                        col = STEEL_DARK
                else:
                    # Ivory porcelain faceplate
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

    # Forehead brass brow plate & gear crest
    hd = ImageDraw.Draw(head_img)
    hd.arc([48, 28, 80, 40], start=180, end=360, fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    hd.arc([49, 29, 79, 39], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)

    # Stylized Takin convex nose bridge & brass muzzle septum ring (64, 52)
    hd.ellipse([61, 48, 67, 54], fill=tuple(STEEL_DARK.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([62, 53, 66, 57], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((64, 50), (255, 255, 255, 255))

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
    SLICE 5: COSTUME (z=25)
    天元拓荒道袍重肩甲 (costume_takin_zen_pioneer_heavy_robe)
    Natural raw linen short robe (#EADDC3) with sunset orange trim (#FFA010),
    single-sided heavy forged brass pauldron on left shoulder (x: 34..48, y: 58..72 #FFD028),
    deep blue-purple woven sash (#1F1A3A), mint green prayer cord (#4ED86A).
    STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # Robe Body: from y=62 to y=94 (strictly decoupled at y < 96)
    # Collar/Chest: (54..74, 62..72), Skirt: (48..80, 72..94)
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

            # Natural linen canvas
            if dot > 0.40:
                col = ROBE_SHINE * 0.4 + ROBE_LIGHT * 0.6
            elif dot > 0.0:
                col = ROBE_BASE + dot * 20.0
            elif dot > -0.35:
                col = ROBE_SHADOW + (dot + 0.35) * 25.0
            else:
                col = ROBE_DARK

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sunset Orange Trim on Collar & Lapel
    cd.line([(54, 62), (64, 76)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    cd.line([(74, 62), (64, 76)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    cd.line([(47, 94), (81, 94)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=2)

    # Deep Blue-Purple Sash around waist (y: 80..85)
    for y in range(80, 86):
        for x in range(51, 78):
            costume_img.putpixel((x, y), tuple(OUTLINE.astype(int)) + (255,))
    cd.line([(51, 80), (77, 80)], fill=tuple(GOLD_DARK.astype(int)) + (255,), width=1)
    cd.line([(51, 85), (77, 85)], fill=tuple(GOLD_DARK.astype(int)) + (255,), width=1)

    # Mint Green Prayer Knot at waist center (64, 83)
    cd.ellipse([62, 81, 66, 85], fill=tuple(MINT_BASE.astype(int)) + (255,), outline=tuple(MINT_DARK.astype(int)) + (255,))
    cd.polygon([(63, 85), (61, 92), (63, 91), (65, 92)], fill=tuple(MINT_LIGHT.astype(int)) + (255,))

    # Left Shoulder Heavy Forged Brass Pauldron (x: 35..48, y: 58..73)
    # Curved tiered defensive pauldron
    for y in range(58, 74):
        for x in range(35, 49):
            pdx = (x - 41.5) / 6.5
            pdy = (y - 65.5) / 7.5
            if pdx**2 + pdy**2 <= 1.0:
                pdot = -0.6 * pdx - 0.6 * pdy
                if pdot > 0.35:
                    pcol = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                elif pdot > -0.15:
                    pcol = GOLD_BASE + pdot * 25.0
                elif pdot > -0.5:
                    pcol = GOLD_DARK
                else:
                    pcol = GOLD_DEEP
                costume_img.putpixel((x, y), tuple(np.clip(pcol, 0, 255).astype(int)) + (255,))

    # Pauldron tier ribs & rivets
    cd.arc([35, 59, 48, 70], start=180, end=360, fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cd.arc([36, 64, 47, 73], start=180, end=360, fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    for ry, rx in [(62, 38), (62, 45), (68, 41)]:
        cd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(CORAL_BASE.astype(int)) + (255,))

    out_costume = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)

    # STRICT 0-ART26b check: enforce y >= 96 is completely zeroed out
    arr = np.array(out_costume)
    arr[96:, :, :] = 0
    return Image.fromarray(arr, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=30)
    翡翠石英耐震雙目鏡 (face_takin_emerald_quartz_visors)
    Pair of emerald quartz crystal visors inserted into head_unit hollow eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    STRICT 0-ART27: Center alpha MUST BE 255.
    Hollow sockets 100% covered by dark frame + crystal, zero holes.
    """
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    eye_centers = [(54, 42), (74, 42)]
    radius = 4.0

    for cx, cy in eye_centers:
        # 1. Fill entire socket rectangle with dark blue-purple eyemask frame (#1F1A3A)
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
                        col = MINT_SHINE
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = MINT_LIGHT * (1.0 - t) + MINT_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = MINT_BASE * (1.0 - t) + MINT_DARK * t + dot * 12.0
                    else:
                        col = MINT_DEEP * 0.7 + OUTLINE * 0.3
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Concentric stress reticle & facet lines
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(SKY_LIGHT.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(SKY_LIGHT.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(MINT_SHINE.astype(int)) + (255,))

        # Specular white eye reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(SKY_BASE.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    天元破竹開山巨斧 (weapon_takin_zen_bamboo_cleaving_axe)
    Single-held double-bladed great axe held in right hand (0-MKT7 compliant).
    Shaft: resilient bamboo-fiber composite weave (x: 88..94, y: 15..105).
    Axe Head: massive double-bladed crescent axe head centered around (102, 45):
      - Outer cutting edge: sharp cold-rolled bronze/steel (BLADE_LIGHT/BLADE_BASE)
      - Inner axe body: bronze plate with cutout taichi / zen wind-slits
      - Counterweight spike: upper tip (102, 20) and bottom pommel (91, 104)
    Zero body or arm baked into weapon (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Bamboo Haft / Shaft: from (91, 20) down to (91, 104)
    # Slight forward tilt: top (93, 20), bottom (89, 104)
    for t in np.linspace(0.0, 1.0, 85):
        sx = 93.0 - t * 4.0
        sy = 20.0 + t * 84.0
        # Shaft diameter: ~3px (radius 1.5)
        for w_off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(sx + w_off))
            py = int(round(sy))
            if 0 <= px < W and 0 <= py < H:
                # Bamboo node pattern every ~14px
                is_node = (int(sy) % 14 in [0, 1])
                if is_node:
                    col = GOLD_BASE if w_off < 0 else GOLD_DARK
                else:
                    dot = -0.6 * (w_off / 1.5)
                    col = MINT_BASE if dot > 0.2 else (MINT_DARK if dot > -0.2 else BRONZE_DARK)
                weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Bottom Pommel (89, 104) with brass ring & coral bead
    wd.ellipse([86, 102, 92, 107], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    wd.ellipse([88, 104, 90, 106], fill=tuple(CORAL_BASE.astype(int)) + (255,))

    # 3. Double-Bladed Crescent Axe Head: centered around socket at (93, 45)
    # Right Main Cleaving Blade: extending forward (x: 93..122, y: 24..66)
    # Left Balance Crescent Blade: extending backward (x: 74..93, y: 32..58)
    # Right Crescent Polygon:
    right_blade_poly = [
        (93, 40), (102, 30), (114, 25), (122, 34),
        (124, 45), (122, 56), (114, 65), (102, 60), (93, 50)
    ]

    min_x = min(p[0] for p in right_blade_poly)
    max_x = max(p[0] for p in right_blade_poly)
    min_y = min(p[1] for p in right_blade_poly)
    max_y = max(p[1] for p in right_blade_poly)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if point_in_polygon(x, y, right_blade_poly):
                dist_to_edge = (x - 93.0) / 31.0
                dist_to_center = abs(y - 45.0) / 20.0
                dot = -0.55 * (x - 108.0) / 16.0 - 0.70 * (y - 45.0) / 20.0

                # Outer sharp edge (x >= 115)
                if x >= 115:
                    col = BLADE_SHINE if dot > 0.2 else (BLADE_LIGHT if dot > -0.2 else BLADE_BASE)
                elif x >= 106:
                    col = BLADE_BASE if dot > 0.1 else (BLADE_SHADOW if dot > -0.3 else BLADE_DARK)
                else:
                    col = BRONZE_LIGHT if dot > 0.2 else (BRONZE_BASE if dot > -0.2 else BRONZE_SHADOW)

                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Crescent Counter-Blade (x: 76..93, y: 33..57)
    left_blade_poly = [
        (93, 41), (86, 34), (77, 36), (75, 45), (77, 54), (86, 56), (93, 49)
    ]
    min_x = min(p[0] for p in left_blade_poly)
    max_x = max(p[0] for p in left_blade_poly)
    min_y = min(p[1] for p in left_blade_poly)
    max_y = max(p[1] for p in left_blade_poly)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if point_in_polygon(x, y, left_blade_poly):
                dot = -0.6 * (x - 85.0) / 9.0 - 0.6 * (y - 45.0) / 11.0
                if x <= 80:
                    col = BLADE_SHINE if dot > 0 else BLADE_LIGHT
                else:
                    col = BRONZE_LIGHT if dot > 0.2 else (BRONZE_BASE if dot > -0.2 else BRONZE_SHADOW)
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Taichi / Zen Wind-Slits cutout in right blade: (103..111, 40..50)
    wind_cutout = [(104, 42), (108, 38), (111, 43), (108, 48), (104, 46)]
    for y in range(37, 50):
        for x in range(103, 113):
            if point_in_polygon(x, y, wind_cutout):
                weapon_img.putpixel((x, y), (0, 0, 0, 0))

    # Central Brass Socket Bracket at (93, 45)
    wd.ellipse([90, 41, 96, 49], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    wd.ellipse([92, 43, 94, 47], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    weapon_img.putpixel((93, 44), (255, 255, 255, 255))

    # Top Axe Spike (93, 16..22)
    wd.polygon([(91, 22), (93, 16), (95, 22)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第六十三族 破竹羚牛 (takin) ===")

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
        ("winding_key", "key_takin_tri_leaf_zen_brass", key_img),
        ("back_curio", "curio_takin_dual_bamboo_oil_flasks", curio_img),
        ("chassis", "chassis_takin_bronze_cast_default", chassis_img),
        ("head_unit", "head_takin_brass_twisted_horn_cowl", head_img),
        ("costume", "costume_takin_zen_pioneer_heavy_robe", costume_img),
        ("optic_core", "face_takin_emerald_quartz_visors", core_img),
        ("weapon", "weapon_takin_zen_bamboo_cleaving_axe", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{TAKIN_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_takin_tri_leaf_zen_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_takin_tri_leaf_zen_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_takin_zen_bamboo_cleaving_axe.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_takin_zen_bamboo_cleaving_axe_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{TAKIN_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{TAKIN_PD_DIR}/proof_paperdoll_takin_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{TAKIN_PD_DIR}/proof_paperdoll_takin_magenta.png"
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

    strip_path = f"{TAKIN_PD_DIR}/proof_takin_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/takin_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/takin_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/takin_idle.png
    p_idle_64 = f"{PLAYER_DIR}/takin_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/takin_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/takin_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/takin_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/takin_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/takin_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)


if __name__ == "__main__":
    build_all()
