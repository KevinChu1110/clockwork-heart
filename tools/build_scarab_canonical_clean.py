#!/usr/bin/env python3
"""
build_scarab_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十族 黑曜金龜 (The Obsidian Scarab, scarab) 7 Paperdoll Slices.
Follows:
- docs/world/OBSIDIAN_SCARAB_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, quenched obsidian cast iron #2B2630,
  glazed ivory-white porcelain faceplate #FFFDF8, cold-rolled brass hinges & antennas #FFD028,
  twin brass exhaust vents with micro steam clouds #FFD028/#2B2630,
  molten amber quartz crystal visor #FFA010/#FFD028 with deep blue-purple frame #1F1A3A,
  crucible artisan apron #FFA010/#4ED86A/#FF5E8A,
  floating crucible obsidian shield-focus #2B2630/#FFD028/#FFA010,
  four-leaf forge cross-fire brass key #FFD028/#FF5E8A)
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
SCARAB_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/scarab"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Obsidian Scarab Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = np.array([255, 253, 248], dtype=float)
IVORY_LIGHT  = np.array([255, 255, 255], dtype=float)
IVORY_SHADOW = np.array([232, 226, 214], dtype=float)
IVORY_DARK   = np.array([205, 196, 180], dtype=float)
IVORY_DEEP   = np.array([170, 160, 142], dtype=float)

# 2. Quenched Obsidian / Cast Iron (#2B2630) - Tuned for deep metallic obsidian luster
OBSIDIAN_SHINE  = np.array([135, 125, 155], dtype=float)    # Specular rim light
OBSIDIAN_LIGHT  = np.array([92, 84, 108], dtype=float)      # Highlight on curved metal
OBSIDIAN_BASE   = np.array([58, 52, 68], dtype=float)       # Core dark quenched obsidian
OBSIDIAN_SHADOW = np.array([43, 38, 50], dtype=float)       # Cel shadow #2B2630
OBSIDIAN_DARK   = np.array([28, 24, 34], dtype=float)       # Deep crevice
OBSIDIAN_DEEP   = np.array([18, 15, 22], dtype=float)

# 3. Metal / Dopamine Foundry Brass Gold (#FFD028)
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 4. Accent / Dopamine Warm Orange (#FFA010)
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 5. Mint Green Enamel (#4ED86A)
MINT_SHINE  = np.array([190, 255, 205], dtype=float)
MINT_LIGHT  = np.array([130, 240, 155], dtype=float)
MINT_BASE   = np.array([78, 216, 106], dtype=float)
MINT_DARK   = np.array([42, 160, 68], dtype=float)
MINT_DEEP   = np.array([24, 110, 44], dtype=float)

# 6. Secondary / Celestial Sky Blue (#38A0FF)
SKY_SHINE = np.array([195, 235, 255], dtype=float)
SKY_LIGHT = np.array([120, 205, 255], dtype=float)
SKY_BASE  = np.array([56, 160, 255], dtype=float)
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([14, 60, 130], dtype=float)

# 7. Coral Pink (#FF5E8A)
CORAL_SHINE = np.array([255, 208, 228], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 8. Amber Optic Crystal (#FFB020)
AMBER_SHINE = np.array([255, 245, 180], dtype=float)
AMBER_LIGHT = np.array([255, 215, 90], dtype=float)
AMBER_BASE  = np.array([255, 176, 32], dtype=float)
AMBER_DARK  = np.array([215, 120, 10], dtype=float)

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
    四葉鍛造十字火紋黃銅發條鑰匙 (key_scarab_crucible_cross_fire_brass)
    Four-Leaf Forge Crucible Brass Key.
    Central ring around (40, 30) with 4 flame-shaped cross wings (top, bottom, left, right),
    center coral pink rivet (CORAL_BASE), warm golden bronze outline OUTLINE_KEY.
    Strictly follows 0-ART29 & 0-QA16: no dark block run >= 13, white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Base shaft extending from chassis socket at (44, 48) to center collar (40, 30)
    shaft_pts = [(45, 48), (47, 49), (42, 32), (39, 31)]
    kd.polygon(shaft_pts, fill=tuple(GOLD_DARK.astype(int)) + (255,))
    kd.line([(40, 32), (46, 48)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)

    # 4 Flame-shaped cross wings radiating from (40, 30)
    # Wing definitions: (cx, cy) = (40, 30)
    kcx, kcy = 40.0, 30.0

    # Top wing: (40, 30) -> (40, 11)
    top_poly = [(36, 27), (33, 19), (40, 10), (47, 19), (44, 27)]
    # Bottom wing: (40, 30) -> (40, 49)
    bot_poly = [(36, 33), (33, 41), (40, 50), (47, 41), (44, 33)]
    # Left wing: (40, 30) -> (21, 30)
    left_poly = [(37, 26), (29, 23), (20, 30), (29, 37), (37, 34)]
    # Right wing: (40, 30) -> (59, 30)
    right_poly = [(43, 26), (51, 23), (60, 30), (51, 37), (43, 34)]

    flame_wings = [top_poly, bot_poly, left_poly, right_poly]
    for poly in flame_wings:
        min_x = int(min(p[0] for p in poly))
        max_x = int(max(p[0] for p in poly))
        min_y = int(min(p[1] for p in poly))
        max_y = int(max(p[1] for p in poly))
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if point_in_polygon(x, y, poly):
                    dist = math.sqrt((x - kcx)**2 + (y - kcy)**2)
                    dot = -0.55 * (x - kcx) / (dist + 1e-5) - 0.70 * (y - kcy) / (dist + 1e-5)
                    # Beveled flame leaf shading
                    if dot > 0.35:
                        col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                    elif dot > -0.15:
                        col = GOLD_BASE + dot * 25.0
                    elif dot > -0.55:
                        col = GOLD_DARK + (dot + 0.15) * 20.0
                    else:
                        col = GOLD_DEEP
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Inner cutouts in wings for filigree lightness (keeps weight down)
    cutouts = [
        [(38, 22), (40, 16), (42, 22)],  # top
        [(38, 38), (40, 44), (42, 38)],  # bottom
        [(32, 28), (26, 30), (32, 32)],  # left
        [(48, 28), (54, 30), (48, 32)],  # right
    ]
    for c_poly in cutouts:
        for y in range(int(min(p[1] for p in c_poly)), int(max(p[1] for p in c_poly)) + 1):
            for x in range(int(min(p[0] for p in c_poly)), int(max(p[0] for p in c_poly)) + 1):
                if point_in_polygon(x, y, c_poly):
                    key_img.putpixel((x, y), (0, 0, 0, 0))

    # Center decorative collar & coral button around (40, 30)
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
    雙聯微型高壓洩壓排煙管短尾 (curio_scarab_twin_vent_exhaust_tail)
    Twin Micro-Vent Exhaust Tail extending from hips at (46, 88) left-upward to (22, 76),
    dual polished brass exhaust pipes with brass flanges and miniature steam puffs.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Universal joint ball at (44, 88)
    jcx, jcy = 44.0, 88.0
    for y in range(83, 94):
        for x in range(39, 50):
            dx = (x - jcx) / 4.5
            dy = (y - jcy) / 4.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                col = GOLD_LIGHT if dot > 0.35 else (GOLD_BASE if dot > -0.25 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Twin angled exhaust pipes:
    # Pipe 1 (Upper): from (42, 86) to (24, 76)
    # Pipe 2 (Lower): from (40, 90) to (22, 82)
    pipes = [
        ((42.0, 86.0), (24.0, 76.0), 3.2),
        ((40.0, 90.0), (22.0, 82.0), 2.8)
    ]

    for p_start, p_end, radius in pipes:
        x1, y1 = p_start
        x2, y2 = p_end
        length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        vx = (x2 - x1) / length
        vy = (y2 - y1) / length
        nx = -vy
        ny = vx

        for t in np.linspace(0.0, 1.0, 35):
            cx = x1 + t * (x2 - x1)
            cy = y1 + t * (y2 - y1)
            for w_off in np.linspace(-radius, radius, 15):
                px = int(round(cx + w_off * nx))
                py = int(round(cy + w_off * ny))
                if 0 <= px < W and 0 <= py < H:
                    dot = -0.6 * (w_off / radius) - 0.5 * (t - 0.5)
                    if dot > 0.35:
                        col = GOLD_LIGHT + dot * 15.0
                    elif dot > -0.25:
                        col = GOLD_BASE + dot * 20.0
                    else:
                        col = GOLD_DARK
                    curio_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass nozzle ring at pipe end (x2, y2)
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                if dx**2 + dy**2 <= (radius + 0.8)**2:
                    px, py = int(x2 + dx), int(y2 + dy)
                    if 0 <= px < W and 0 <= py < H:
                        col = GOLD_SHINE if (dx < 0 or dy < 0) else GOLD_DARK
                        curio_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Cute miniature steam puffs at nozzle tips:
    # Puff 1: near (19, 73)
    # Puff 2: near (16, 80)
    puffs = [(19.0, 73.0, 4.5), (16.0, 80.0, 3.8)]
    for sx, sy, sr in puffs:
        for y in range(int(sy - sr - 2), int(sy + sr + 3)):
            for x in range(int(sx - sr - 2), int(sx + sr + 3)):
                dist = math.sqrt((x - sx)**2 + (y - sy)**2)
                if dist <= sr:
                    alpha = int(np.clip((1.0 - dist / sr) * 160.0 + 40.0, 0, 220))
                    dot = -0.5 * (x - sx) / sr - 0.7 * (y - sy) / sr
                    col = WHITE_SHINE if dot > 0 else IVORY_LIGHT
                    curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (alpha,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    黑曜耐火鑄鐵矮萌底盤 (chassis_scarab_obsidian_forge_default)
    2.2 head-body ratio chibi chassis, cast iron / quenched obsidian body (#2B2630),
    ivory porcelain belly plate (#FFFDF8), brass ball joints (#FFD028),
    six-legged beetle articulation with rubber pads on main feet.
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))

    # 2. Main Feet (y: 98..111)
    # Left foot: centered at (50, 105), Right foot: centered at (76, 105)
    for bx, by in [(50.0, 105.0), (76.0, 105.0)]:\
        # Thigh / Leg obsidian metal cylinder
        for y in range(int(by - 14), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.0
                dy = (y - (by - 8)) / 7.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.7 * dy
                    if dot > 0.35:
                        col = OBSIDIAN_LIGHT + dot * 15.0
                    elif dot > -0.2:
                        col = OBSIDIAN_BASE + dot * 20.0
                    else:
                        col = OBSIDIAN_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass knee cap joint
        for y in range(int(by - 11), int(by - 6)):
            for x in range(int(bx - 3), int(bx + 4)):
                if (x - bx)**2 + (y - (by - 8.5))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 8.5) / 3.0
                    col = GOLD_SHINE if dot > 0.4 else (GOLD_BASE + dot * 25.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Foot boot base with heat-resistant silicone sole
        for y in range(int(by - 5), int(by + 6)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.5
                dy = (y - by) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    if y >= by + 3:
                        col = OBSIDIAN_DARK if dot < 0 else OBSIDIAN_SHADOW
                    else:
                        if dot > 0.4:
                            col = OBSIDIAN_LIGHT + dot * 15.0
                        elif dot > -0.2:
                            col = OBSIDIAN_BASE + dot * 20.0
                        else:
                            col = OBSIDIAN_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Side legs articulation (beetle 6-leg trait, stylized chibi)
    # Left middle leg: (35, 76), Left front leg: (34, 90)
    # Right middle leg: (86, 92)
    side_legs = [
        ((44.0, 74.0), (33.0, 77.0)),
        ((44.0, 86.0), (32.0, 92.0)),
        ((80.0, 86.0), (88.0, 93.0))
    ]
    for (lx1, ly1), (lx2, ly2) in side_legs:
        for t in np.linspace(0.0, 1.0, 20):
            cx = lx1 + t * (lx2 - lx1)
            cy = ly1 + t * (ly2 - ly1)
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx**2 + dy**2 <= 1:
                        px, py = int(cx + dx), int(cy + dy)
                        if 0 <= px < W and 0 <= py < H and px < 94:
                            col = GOLD_BASE if (dx < 0 or dy < 0) else GOLD_DARK
                            chassis_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Main Torso Quenched Obsidian Body (x: 44..84, y: 58..95)
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
                    col = OBSIDIAN_SHINE * 0.7 + OBSIDIAN_LIGHT * 0.3 + spec * 25.0
                elif dot > 0.05:
                    col = OBSIDIAN_BASE + (dot - 0.05) * 35.0
                elif dot > -0.35:
                    col = OBSIDIAN_SHADOW + (dot + 0.35) * 25.0
                else:
                    col = OBSIDIAN_DARK

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 5. Glazed Ivory Porcelain Belly Plate (x: 49..79, y: 61..91)
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

    # 6. Shoulders & Arms:
    # Left arm: resting beside torso (x: 36..46, y: 64..78)
    for y in range(64, 79):
        for x in range(36, 47):
            dx = (x - 41.0) / 4.5
            dy = (y - 71.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = OBSIDIAN_LIGHT if dot > 0.3 else (OBSIDIAN_BASE if dot > -0.2 else OBSIDIAN_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right arm: extending forward to hold focus (x: 82..91, y: 66..78)
    # STRICT 0-ART9/11: x MUST NOT exceed 93!
    for y in range(66, 79):
        for x in range(82, 92):
            dx = (x - 87.0) / 4.5
            dy = (y - 72.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = OBSIDIAN_LIGHT if dot > 0.3 else (OBSIDIAN_BASE if dot > -0.2 else OBSIDIAN_SHADOW)
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
    黑曜淬火雙叉金角面罩 (head_scarab_quenched_obsidian_cowl)
    Quenched obsidian dome helmet, ivory porcelain cheeks,
    twin-horn brass mechanical antennas (Twin-Horn Brass Antennas #FFD028).
    STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
      Left eye: x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Twin-Horn Brass Mechanical Antennas (Scarab signature crown horns)
    # Origin at forehead center (64, 25), branching left to (52, 6) and right to (76, 6)
    # Left horn: (64, 25) -> (58, 16) -> (52, 6)
    left_horn_pts = [(64.0, 25.0), (58.0, 16.0), (52.0, 6.0)]
    for t in np.linspace(0.0, 1.0, 30):
        # Quadratic curve
        hx = (1.0 - t)**2 * 64.0 + 2.0 * (1.0 - t) * t * 58.0 + t**2 * 52.0
        hy = (1.0 - t)**2 * 25.0 + 2.0 * (1.0 - t) * t * 16.0 + t**2 * 6.0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx**2 + dy**2 <= 1:
                    px, py = int(hx + dx), int(hy + dy)
                    if 0 <= px < W and 0 <= py < H:
                        col = GOLD_LIGHT if (dx < 0 or dy < 0) else GOLD_DARK
                        head_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left horn tip golden resonant sphere
    hd.ellipse([50, 4, 55, 9], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((52, 6), (255, 255, 255, 255))

    # Right horn: (64, 25) -> (70, 16) -> (76, 6)
    for t in np.linspace(0.0, 1.0, 30):
        hx = (1.0 - t)**2 * 64.0 + 2.0 * (1.0 - t) * t * 70.0 + t**2 * 76.0
        hy = (1.0 - t)**2 * 25.0 + 2.0 * (1.0 - t) * t * 16.0 + t**2 * 6.0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx**2 + dy**2 <= 1:
                    px, py = int(hx + dx), int(hy + dy)
                    if 0 <= px < W and 0 <= py < H:
                        col = GOLD_LIGHT if (dx < 0 or dy < 0) else GOLD_DARK
                        head_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right horn tip golden resonant sphere
    hd.ellipse([73, 4, 78, 9], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((75, 6), (255, 255, 255, 255))

    # Horn base rosette collar at (64, 25)
    hd.ellipse([60, 22, 68, 28], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([62, 23, 66, 27], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    head_img.putpixel((64, 24), (255, 255, 255, 255))

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
                    # Polished quenched obsidian helmet
                    if dot > 0.45:
                        col = OBSIDIAN_SHINE * 0.7 + OBSIDIAN_LIGHT * 0.3 + dot * 20.0
                    elif dot > 0.05:
                        col = OBSIDIAN_BASE + (dot - 0.05) * 35.0
                    elif dot > -0.35:
                        col = OBSIDIAN_SHADOW + (dot + 0.35) * 25.0
                    else:
                        col = OBSIDIAN_DARK
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

    # Forehead brass arch & gear crest
    hd = ImageDraw.Draw(head_img)
    hd.arc([48, 28, 80, 40], start=180, end=360, fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    hd.arc([49, 29, 79, 39], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)

    # Stylized mechanical beetle ventilation pore at nose (64, 50)
    hd.ellipse([62, 49, 66, 52], fill=tuple(OBSIDIAN_DARK.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
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
    SLICE 5: COSTUME (z=30)
    赤焰熔爐隔熱工匠護裙 (costume_scarab_crucible_artisan_apron)
    Crucible artisan apron, dopamine warm orange canvas (#FFA010),
    mint green trim (#4ED86A), coral pink flame emblem (#FF5E8A),
    4 brass dome buttons (#FFD028).
    STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # Apron Body: from y=62 to y=94 (strictly decoupled at y < 96)
    # Bib section: (54..74, 62..72), Skirt section: (48..80, 72..94)
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

            # Warm orange apron canvas
            if dot > 0.40:
                col = ORANGE_SHINE * 0.4 + ORANGE_LIGHT * 0.6
            elif dot > 0.0:
                col = ORANGE_BASE + dot * 20.0
            elif dot > -0.35:
                col = ORANGE_DARK + (dot + 0.35) * 25.0
            else:
                col = ORANGE_DEEP

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Mint Green Neck & Hem Trim
    cd.line([(54, 62), (74, 62)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=2)
    cd.line([(47, 94), (81, 94)], fill=tuple(MINT_BASE.astype(int)) + (255,), width=2)

    # Front Bib Straps & 4 Brass Buttons
    cd.line([(55, 62), (55, 74)], fill=tuple(MINT_DARK.astype(int)) + (255,), width=1)
    cd.line([(73, 62), (73, 74)], fill=tuple(MINT_DARK.astype(int)) + (255,), width=1)

    button_coords = [(64, 67), (64, 74), (64, 81), (64, 88)]
    for bx, by in button_coords:
        cd.ellipse([bx - 2, by - 2, bx + 2, by + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
        costume_img.putpixel((bx, by - 1), (255, 255, 255, 255))

    # Artisan pocket at right side (69..77, 78..86) with Coral flame badge
    cd.rectangle([70, 79, 77, 86], outline=tuple(MINT_BASE.astype(int)) + (255,), width=1)
    cd.polygon([(73, 85), (71, 82), (73, 80), (75, 82)], fill=tuple(CORAL_BASE.astype(int)) + (255,))

    out_costume = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)

    # STRICT 0-ART26b check: enforce y >= 96 is completely zeroed out
    arr = np.array(out_costume)
    arr[96:, :, :] = 0
    return Image.fromarray(arr, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=25)
    熔金琥珀水晶石英透鏡 (face_scarab_amber_crystal_visor)
    Pair of molten amber quartz crystal lenses inserted into head_unit hollow eye sockets:
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
        # 1. Fill entire socket rectangle with dark blue-purple eyemask frame (#1F1A3A / ORANGE_DEEP)
        cored.rounded_rectangle([cx - 4, cy - 4, cx + 4, cy + 4], radius=1, fill=tuple(OUTLINE.astype(int)) + (255,))

        # 2. Molten Amber Quartz crystal lens inside frame
        for y in range(int(cy - radius), int(cy + radius + 1)):
            for x in range(int(cx - radius), int(cx + radius + 1)):
                dx = (x - cx) / radius
                dy = (y - cy) / radius
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.25:
                        col = AMBER_SHINE
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = AMBER_LIGHT * (1.0 - t) + AMBER_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = AMBER_BASE * (1.0 - t) + ORANGE_DARK * t + dot * 12.0
                    else:
                        col = ORANGE_DEEP * 0.7 + OUTLINE * 0.3
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Gold reticle crosshairs & crystal facet lines
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(GOLD_SHINE.astype(int)) + (255,))

        # Specular white eye reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(AMBER_LIGHT.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    赤焰黑曜護體靈晶 (weapon_scarab_crucible_obsidian_focus)
    Single-held shield-focus at right hand (0-MKT7 compliant).
    Floating multifaceted quenched obsidian crystal core centered at (102, 68), radius ~10px,
    surrounded by dual counter-rotating brass dial tuning rings (#FFD028 / #FFA010) and mint crystal aura.
    Zero body or arm baked into weapon (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    fcx, fcy = 102.0, 68.0

    # 1. Subtle mint energy aura (faint outer glow)
    for dy in range(-14, 15):
        for dx in range(-14, 15):
            dist = math.sqrt(dx**2 + dy**2)
            if 9.0 < dist <= 14.0:
                alpha = int(np.clip((1.0 - (dist - 9.0) / 5.0) * 80.0, 0, 100))
                px, py = int(fcx + dx), int(fcy + dy)
                if 0 <= px < W and 0 <= py < H:
                    weapon_img.putpixel((px, py), tuple(MINT_BASE.astype(int)) + (alpha,))

    # 2. Outer Brass Tuning Dial Ring (radius 11..13)
    for dy in range(-14, 15):
        for dx in range(-14, 15):
            dist = math.sqrt(dx**2 + dy**2)
            if 11.0 <= dist <= 13.0:
                angle = math.atan2(dy, dx)
                notch = math.cos(angle * 8.0)
                dot = -0.55 * (dx / dist) - 0.70 * (dy / dist)
                if notch > 0.4:
                    col = GOLD_SHINE if dot > 0 else GOLD_BASE
                else:
                    col = GOLD_DARK if dot < 0 else GOLD_BASE
                px, py = int(fcx + dx), int(fcy + dy)
                if 0 <= px < W and 0 <= py < H:
                    weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Inner Counter-Rotating Golden Ring (radius 8.5..9.5)
    for dy in range(-11, 12):
        for dx in range(-11, 12):
            dist = math.sqrt(dx**2 + dy**2)
            if 8.2 <= dist <= 9.8:
                angle = math.atan2(dy, dx)
                notch = math.sin(angle * 6.0)
                col = ORANGE_LIGHT if notch > 0 else GOLD_BASE
                px, py = int(fcx + dx), int(fcy + dy)
                if 0 <= px < W and 0 <= py < H:
                    weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Central Multifaceted Quenched Obsidian Crystal Core (radius ~7.5)
    for dy in range(-8, 9):
        for dx in range(-8, 9):
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= 7.5:
                # Octagonal crystal facet simulation
                facet = math.cos(math.atan2(dy, dx) * 4.0)
                nz = math.sqrt(max(0.0, 1.0 - (dist / 7.5)**2))
                dot = -0.55 * (dx / 7.5) - 0.70 * (dy / 7.5) + 0.45 * nz
                spec = max(0.0, dot - 0.45) / 0.55

                if dist < 2.5:
                    # Molten energy core
                    col = AMBER_SHINE * 0.8 + WHITE_SHINE * 0.2
                elif facet > 0.3:
                    # Bright obsidian facet
                    col = OBSIDIAN_SHINE * 0.7 + AMBER_LIGHT * 0.3 + spec * 30.0
                elif dot > 0.1:
                    col = OBSIDIAN_LIGHT + dot * 20.0
                elif dot > -0.3:
                    col = OBSIDIAN_BASE + (dot + 0.3) * 20.0
                else:
                    col = OBSIDIAN_SHADOW

                px, py = int(fcx + dx), int(fcy + dy)
                if 0 <= px < W and 0 <= py < H:
                    weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Specular glint on crystal facet
    wd.ellipse([int(fcx - 3), int(fcy - 4), int(fcx - 1), int(fcy - 2)], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
    wd.point((int(fcx + 2), int(fcy + 2)), fill=tuple(AMBER_LIGHT.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第六十族 黑曜金龜 (scarab) ===")

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
        ("winding_key", "key_scarab_crucible_cross_fire_brass", key_img),
        ("back_curio", "curio_scarab_twin_vent_exhaust_tail", curio_img),
        ("chassis", "chassis_scarab_obsidian_forge_default", chassis_img),
        ("head_unit", "head_scarab_quenched_obsidian_cowl", head_img),
        ("costume", "costume_scarab_crucible_artisan_apron", costume_img),
        ("optic_core", "face_scarab_amber_crystal_visor", core_img),
        ("weapon", "weapon_scarab_crucible_obsidian_focus", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{SCARAB_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_scarab_crucible_cross_fire_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_scarab_crucible_obsidian_focus.png")
    print("  ✓ Universal key and weapon copies updated")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{SCARAB_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{SCARAB_PD_DIR}/proof_paperdoll_scarab_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SCARAB_PD_DIR}/proof_paperdoll_scarab_magenta.png"
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

    strip_path = f"{SCARAB_PD_DIR}/proof_scarab_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/scarab_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/scarab_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/scarab_idle.png
    p_idle_64 = f"{PLAYER_DIR}/scarab_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/scarab_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/scarab_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/scarab_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/scarab_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/scarab_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)


if __name__ == "__main__":
    build_all()
