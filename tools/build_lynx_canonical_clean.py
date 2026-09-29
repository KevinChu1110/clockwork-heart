#!/usr/bin/env python3
"""
build_lynx_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十九族 提線猞猁 (The Marionette Lynx, lynx) 7 Paperdoll Slices.
Follows:
- docs/design/MARIONETTE_LYNX_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, polished walnut wood shell #8B5A2B,
  glazed ivory-white porcelain faceplate #FFFDF8, cold-rolled brass hinges #FFD028,
  twin brass wire resonance ear tufts #FFD028/#4ED86A, twin-segment pendulum bobtail #8B5A2B/#FFD028,
  emerald quartz goggle lenses #4ED86A/#38A0FF with warm orange acrobat markings #FFA010,
  dawn marionette five-blade steel claws #7A8A9E/#FFD028, twin-ring chime brass key #FFD028/#FF5E8A)
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
LYNX_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lynx"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Marionette Lynx Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = np.array([255, 253, 248], dtype=float)
IVORY_LIGHT  = np.array([255, 255, 255], dtype=float)
IVORY_SHADOW = np.array([232, 226, 214], dtype=float)
IVORY_DARK   = np.array([205, 196, 180], dtype=float)
IVORY_DEEP   = np.array([170, 160, 142], dtype=float)

# 2. Polished Walnut Wood (#8B5A2B) - Tuned for warm luster and < 60 L2 coherence with head unit
WALNUT_LIGHT  = np.array([195, 145, 92], dtype=float)      # Highlight on curved wood
WALNUT_BASE   = np.array([155, 108, 58], dtype=float)       # Core warm walnut brown
WALNUT_SHADOW = np.array([125, 80, 40], dtype=float)        # Cel shadow
WALNUT_DARK   = np.array([88, 52, 24], dtype=float)         # Deep crevice
WALNUT_DEEP   = np.array([62, 36, 16], dtype=float)

# 3. Metal / Dopamine Gold & Brass (#FFD028)
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

# 5. Mint Bamboo Green Enamel (#4ED86A)
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

# 7. Cold Stamped Steel & Tungsten Claw Alloy (#7A8A9E)
STEEL_SHINE = np.array([215, 228, 240], dtype=float)
STEEL_LIGHT = np.array([168, 182, 200], dtype=float)
STEEL_BASE  = np.array([122, 138, 158], dtype=float)
STEEL_DARK  = np.array([88, 102, 120], dtype=float)
STEEL_DEEP  = np.array([58, 68, 82], dtype=float)

# 8. Dark Acrobat Fabric Navy (#1F1A3A, #2D274A)
NAVY_LIGHT = np.array([72, 64, 110], dtype=float)
NAVY_BASE  = np.array([45, 39, 74], dtype=float)
NAVY_DARK  = np.array([28, 22, 48], dtype=float)

# 9. Coral Pink (#FF5E8A)
CORAL_SHINE = np.array([255, 208, 228], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

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
                    if r[0] <= x <= r[2] and r[1] <= y <= r[3]:
                        skip = True
                        break
                if skip:
                    continue

            n4_count = 0
            for dx, dy in neighbors_4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    n4_count += 1

            ndiag_count = 0
            for dx, dy in neighbors_diag:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    ndiag_count += 1

            if n4_count > 0:
                if n4_count >= 3:
                    a = 255.0
                elif n4_count == 2:
                    a = 225.0 + ndiag_count * 7.0
                else:
                    a = 175.0 + ndiag_count * 15.0
                outline_alpha[y, x] = min(255.0, a)
                outline_rgb[y, x] = outline_color[:3]
            elif ndiag_count > 0:
                a = 60.0 + ndiag_count * 25.0
                outline_alpha[y, x] = min(140.0, a)
                outline_rgb[y, x] = outline_color[:3]

    for y in range(h):
        for x in range(w):
            if not opaque_mask[y, x] and outline_alpha[y, x] > 0:
                cur_a = float(arr[y, x, 3])
                new_a = max(cur_a, outline_alpha[y, x])
                arr[y, x, 3] = int(round(new_a))
                arr[y, x, :3] = np.clip(outline_rgb[y, x], 0, 255).astype(np.uint8)

    return Image.fromarray(arr)


def point_in_polygon(x, y, poly):
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if ((y1 > y) != (y2 > y)) and (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1):
            inside = not inside
    return inside


def build_winding_key() -> Image.Image:
    """
    SLICE 1: WINDING KEY (z=5)
    雙環八音風鈴黃銅發條鑰匙 (key_lynx_twin_ring_chime_brass)
    Centered at (40, 30), dual symmetrical acoustic chime rings, coral center button.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Stem: from body (46, 50) to hub (40, 30)
    for t in np.linspace(0.0, 1.0, 35):
        sx = 46.0 * (1.0 - t) + 40.0 * t
        sy = 50.0 * (1.0 - t) + 30.0 * t
        for offset in range(-3, 4):
            nx, ny = -20.0 / 20.88, 6.0 / 20.88
            px = int(round(sx + offset * nx))
            py = int(round(sy + offset * ny))
            if 0 <= px < W and 0 <= py < H:
                dot = -offset / 3.0
                if dot > 0.4:
                    col = GOLD_LIGHT + dot * 20.0
                elif dot > -0.2:
                    col = GOLD_BASE + dot * 25.0
                else:
                    col = GOLD_DARK + dot * 20.0
                key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Twin acoustic windchime rings: Left loop at (29, 30), Right loop at (51, 30)
    # Left ring: center (29, 30), outer radius 9.5, inner radius 5.0
    lcx, lcy = 29.0, 30.0
    for y in range(19, 41):
        for x in range(18, 40):
            dist = math.sqrt((x - lcx)**2 + (y - lcy)**2)
            if 5.0 <= dist <= 9.5:
                # Radial tubular cross-section
                t_tube = abs(dist - 7.25) / 2.25  # 0 at center of tube, 1 at edges
                dot = -0.55 * (x - lcx) / dist - 0.70 * (y - lcy) / dist
                spec = max(0.0, dot - 0.4) / 0.6
                if dot > 0.35:
                    col = GOLD_LIGHT * (1.0 - t_tube * 0.4) + GOLD_SHINE * (0.4 * (1.0 - t_tube)) + spec * 25.0
                elif dot > -0.25:
                    col = GOLD_BASE * (1.0 - t_tube * 0.4) + GOLD_DARK * (t_tube * 0.4) + dot * 20.0
                else:
                    col = GOLD_DARK * (1.0 - t_tube * 0.3) + GOLD_DEEP * (t_tube * 0.3) + dot * 15.0
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right ring: center (51, 30), outer radius 9.5, inner radius 5.0
    rcx, rcy = 51.0, 30.0
    for y in range(19, 41):
        for x in range(40, 62):
            dist = math.sqrt((x - rcx)**2 + (y - rcy)**2)
            if 5.0 <= dist <= 9.5:
                t_tube = abs(dist - 7.25) / 2.25
                dot = -0.55 * (x - rcx) / dist - 0.70 * (y - rcy) / dist
                spec = max(0.0, dot - 0.4) / 0.6
                if dot > 0.35:
                    col = GOLD_LIGHT * (1.0 - t_tube * 0.4) + GOLD_SHINE * (0.4 * (1.0 - t_tube)) + spec * 25.0
                elif dot > -0.25:
                    col = GOLD_BASE * (1.0 - t_tube * 0.4) + GOLD_DARK * (t_tube * 0.4) + dot * 20.0
                else:
                    col = GOLD_DARK * (1.0 - t_tube * 0.3) + GOLD_DEEP * (t_tube * 0.3) + dot * 15.0
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Vane fin tabs on left and right loops
    fins = [
        [(26, 21), (29, 14), (32, 21)],  # Left top fin
        [(26, 39), (29, 46), (32, 39)],  # Left bottom fin
        [(48, 21), (51, 14), (54, 21)],  # Right top fin
        [(48, 39), (51, 46), (54, 39)],  # Right bottom fin
    ]
    for poly in fins:
        for y in range(int(min(p[1] for p in poly)), int(max(p[1] for p in poly)) + 1):
            for x in range(int(min(p[0] for p in poly)), int(max(p[0] for p in poly)) + 1):
                if point_in_polygon(x, y, poly):
                    t = (y - min(p[1] for p in poly)) / (max(p[1] for p in poly) - min(p[1] for p in poly) + 1e-5)
                    col = GOLD_LIGHT * (1.0 - t) + GOLD_DARK * t
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Center decorative collar & coral button around (40, 30)
    kcx, kcy = 40.0, 30.0
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
    雙節同軸鐘擺平衡配重短尾 (curio_lynx_pendulum_bobtail_balance)
    Extends from pelvis at (46, 88) left-upward to (20, 78), dual turned walnut segments,
    brass universal joint, brass spherical pendulum balance weight.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    tail_nodes = [
        (46.0, 88.0, 4.0),
        (37.0, 85.0, 3.5),
        (28.0, 81.0, 3.0)
    ]

    # Two turned walnut cylinder segments
    for i in range(len(tail_nodes) - 1):
        x1, y1, r1 = tail_nodes[i]
        x2, y2, r2 = tail_nodes[i+1]
        for t in np.linspace(0.0, 1.0, 25):
            cx = x1 + t * (x2 - x1)
            cy = y1 + t * (y2 - y1)
            r = r1 + t * (r2 - r1)
            for dy in range(-int(r), int(r) + 1):
                for dx in range(-int(r), int(r) + 1):
                    dsq = (dx**2 + dy**2) / (r**2)
                    if dsq <= 1.0:
                        dot = -0.6 * dx / r - 0.6 * dy / r
                        grain = math.sin((cx + dx) * 1.8 + (cy + dy) * 0.4) * 4.0
                        if dot > 0.35:
                            col = WALNUT_LIGHT + dot * 20.0 + grain
                        elif dot > -0.25:
                            col = WALNUT_BASE + dot * 25.0 + grain
                        else:
                            col = WALNUT_SHADOW + dot * 20.0 + grain
                        px, py = int(round(cx + dx)), int(round(cy + dy))
                        if 0 <= px < W and 0 <= py < H:
                            curio_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass coupling ring at joint
        for y in range(int(y1 - 4), int(y1 + 5)):
            for x in range(int(x1 - 4), int(x1 + 5)):
                dist = math.sqrt((x - x1)**2 + (y - y1)**2)
                if dist <= 3.2:
                    dot = -0.5 * (x - x1) / 3.2 - 0.7 * (y - y1) / 3.2
                    col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                    curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        curio_img.putpixel((int(x1), int(y1)), (255, 255, 255, 255))

    # Universal joint at node 3
    x3, y3 = 28.0, 81.0
    for y in range(int(y3 - 4), int(y3 + 5)):
        for x in range(int(x3 - 4), int(x3 + 5)):
            dist = math.sqrt((x - x3)**2 + (y - y3)**2)
            if dist <= 3.2:
                dot = -0.5 * (x - x3) / 3.2 - 0.7 * (y - y3) / 3.2
                col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    curio_img.putpixel((int(x3), int(y3)), (255, 255, 255, 255))

    # Brass spherical pendulum bobtail weight at (20, 78), radius ~5.5
    pcx, pcy = 20.0, 78.0
    for y in range(71, 86):
        for x in range(13, 28):
            dx = (x - pcx) / 5.5
            dy = (y - pcy) / 5.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, dot - 0.5) / 0.5
                dist = math.sqrt(dsq)

                # Center coral gem inlay (dist <= 0.4)
                if dist <= 0.4:
                    col = CORAL_LIGHT if dot > 0.2 else (CORAL_BASE if dot > -0.3 else CORAL_DARK)
                elif 0.4 < dist <= 0.55:
                    col = GOLD_DARK  # inlay collar
                else:
                    if dot > 0.40:
                        col = GOLD_LIGHT * 0.75 + GOLD_SHINE * 0.25 + spec * 25.0
                    elif dot > -0.10:
                        col = GOLD_BASE + (dot + 0.10) * 35.0
                    elif dot > -0.45:
                        col = GOLD_DARK + (dot + 0.45) * 25.0
                    else:
                        col = GOLD_DEEP
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    curio_img.putpixel((int(pcx - 1), int(pcy - 1)), (255, 255, 255, 255))
    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    提線木偶精雕胡桃木矮萌底盤 (chassis_lynx_marionette_walnut_default)
    2.2 head-body ratio chibi chassis, polished walnut body, ivory porcelain belly,
    brass ball joints, short agile legs with rubber pads.
    STRICT: x >= 94 MUST BE 0 PIXELS (0-ART9/11).
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))

    # 2. Feet and Boots (y: 98..111)
    # Left foot: centered at (50, 105), Right foot: centered at (76, 105)
    for bx, by in [(50.0, 105.0), (76.0, 105.0)]:
        # Thigh / Leg wood cylinder
        for y in range(int(by - 14), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.0
                dy = (y - (by - 8)) / 7.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.7 * dy
                    grain = math.sin(x * 2.0) * 4.0
                    if dot > 0.3:
                        col = WALNUT_LIGHT + grain + dot * 15.0
                    elif dot > -0.2:
                        col = WALNUT_BASE + grain + dot * 20.0
                    else:
                        col = WALNUT_SHADOW + grain + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass knee cap
        for y in range(int(by - 11), int(by - 6)):
            for x in range(int(bx - 3), int(bx + 4)):
                if (x - bx)**2 + (y - (by - 8.5))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 8.5) / 3.0
                    col = GOLD_SHINE if dot > 0.4 else (GOLD_BASE + dot * 25.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Foot shoe base with rubber damper sole
        for y in range(int(by - 5), int(by + 6)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.5
                dy = (y - by) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    if y >= by + 3:
                        col = NAVY_BASE + dot * 8.0 if dot > 0 else NAVY_DARK
                    else:
                        if dot > 0.4:
                            col = WALNUT_LIGHT + dot * 15.0
                        elif dot > -0.2:
                            col = WALNUT_BASE + dot * 20.0
                        else:
                            col = WALNUT_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Main Torso Walnut Body (x: 44..84, y: 58..95)
    cx, cy = 64.0, 77.0
    for y in range(58, 96):
        for x in range(44, 85):
            dx = (x - cx) / 18.5
            dy = (y - cy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, -0.6 * dx - 0.7 * dy + 0.4 * nz - 0.6) / 0.4
                grain = math.sin(x * 1.6 + y * 0.2) * 5.0

                if dot > 0.45:
                    col = WALNUT_LIGHT * 0.85 + spec * 25.0 + grain
                elif dot > 0.05:
                    col = WALNUT_BASE + grain + (dot - 0.05) * 40.0
                elif dot > -0.35:
                    col = WALNUT_SHADOW + grain + (dot + 0.35) * 30.0
                else:
                    col = WALNUT_DARK + grain * 0.5

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Glazed Ivory Porcelain Belly/Chest Plate (x: 49..79, y: 61..91)
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
            chd.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=tuple(GOLD_DARK.astype(int)) + (255,))
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,))
            chassis_img.putpixel((rx, ry), (255, 255, 255, 255))

    # 5. Arms and Paws
    # Left arm (feline defensive guard paw): from shoulder (46, 64) inward to (36, 74)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 46.0 * (1.0 - t)**2 + 40.0 * 2 * (1.0 - t) * t + 36.0 * t**2
        ay = 64.0 * (1.0 - t)**2 + 69.0 * 2 * (1.0 - t) * t + 74.0 * t**2
        chd.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=tuple(WALNUT_BASE.astype(int)) + (255,))
        chd.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=tuple(WALNUT_LIGHT.astype(int)) + (255,))
    # Left brass elbow ball joint
    chd.ellipse([37, 67, 42, 72], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    # Left paw (feline curled paw with ivory plate)
    chd.ellipse([32, 71, 39, 78], fill=tuple(IVORY_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    chassis_img.putpixel((34, 73), (255, 255, 255, 255))

    # Right arm (claw-wielding wrist): from shoulder (78, 64) outward to (88, 72)
    # STRICT 0-ART9/11: DO NOT EXCEED x=92 (x >= 94 must be 0!)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 78.0 * (1.0 - t)**2 + 84.0 * 2 * (1.0 - t) * t + 89.0 * t**2
        ay = 64.0 * (1.0 - t)**2 + 68.0 * 2 * (1.0 - t) * t + 73.0 * t**2
        chd.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=tuple(WALNUT_BASE.astype(int)) + (255,))
        chd.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=tuple(WALNUT_LIGHT.astype(int)) + (255,))
    # Right brass elbow ball joint
    chd.ellipse([82, 66, 87, 71], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    # Right wrist & palm grip (stops cleanly at x=91)
    chd.ellipse([85, 70, 91, 77], fill=tuple(IVORY_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    chassis_img.putpixel((88, 72), (255, 255, 255, 255))

    # Bridge small gaps between limbs and body to ensure 0 holes (0-QA16 Metric 3 / 0-ART29)
    chd.ellipse([43, 69, 47, 73], fill=tuple(WALNUT_BASE.astype(int)) + (255,))
    chd.ellipse([81, 70, 85, 74], fill=tuple(WALNUT_BASE.astype(int)) + (255,))
    chd.ellipse([44, 80, 48, 84], fill=tuple(WALNUT_BASE.astype(int)) + (255,))
    chd.ellipse([46, 86, 50, 90], fill=tuple(WALNUT_BASE.astype(int)) + (255,))

    # Clear any accidental pixels at x >= 94 (0-ART9/11) before outline
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr).copy()

    out_chassis = apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=[(94, 0, 127, 127)])
    arr = np.array(out_chassis)
    arr[:, 94:, :] = 0
    return Image.fromarray(arr)


def build_head_unit() -> Image.Image:
    """
    SLICE 4: HEAD UNIT (z=20)
    白瓷提線雙天線金耳兜帽 (head_lynx_bazaar_marionette_tufted_cowl)
    Polished walnut head cowl, ivory porcelain faceplate, dual upright brass wire resonance ear tufts.
    STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
      Left eye: x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Dual Upright Brass Wire Resonance Ear Tufts (Lynx signature ears)
    # Left Ear: base at (46, 28), ear tip at (38, 10)
    ear_l_poly = [(48, 28), (43, 20), (37, 10), (43, 14), (49, 25)]
    hd.polygon(ear_l_poly, fill=tuple(WALNUT_BASE.astype(int)) + (255,))
    hd.line([(48, 28), (37, 10)], fill=tuple(WALNUT_LIGHT.astype(int)) + (255,), width=2)
    # Inner mint enamel lacquer inlay
    hd.polygon([(47, 26), (43, 20), (40, 14), (44, 18), (48, 24)], fill=tuple(MINT_BASE.astype(int)) + (255,))
    # Left brass wire antenna tufts (3 fine resonant brass wires extending up from ear tip)
    hd.line([(37, 10), (35, 3)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    hd.line([(38, 11), (38, 4)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    hd.line([(39, 12), (42, 5)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.ellipse([34, 2, 36, 4], fill=tuple(GOLD_SHINE.astype(int)) + (255,))
    hd.ellipse([37, 3, 39, 5], fill=tuple(GOLD_SHINE.astype(int)) + (255,))
    hd.ellipse([41, 4, 43, 6], fill=tuple(GOLD_SHINE.astype(int)) + (255,))
    # Left ear brass base hinge
    hd.ellipse([44, 24, 49, 29], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((46, 26), (255, 255, 255, 255))

    # Right Ear: base at (80, 28), ear tip at (90, 10)
    ear_r_poly = [(80, 28), (85, 20), (91, 10), (85, 14), (79, 25)]
    hd.polygon(ear_r_poly, fill=tuple(WALNUT_BASE.astype(int)) + (255,))
    hd.line([(80, 28), (91, 10)], fill=tuple(WALNUT_LIGHT.astype(int)) + (255,), width=2)
    # Inner mint enamel lacquer inlay
    hd.polygon([(81, 26), (85, 20), (88, 14), (84, 18), (80, 24)], fill=tuple(MINT_BASE.astype(int)) + (255,))
    # Right brass wire antenna tufts
    hd.line([(91, 10), (93, 3)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    hd.line([(90, 11), (90, 4)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    hd.line([(89, 12), (86, 5)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.ellipse([92, 2, 94, 4], fill=tuple(GOLD_SHINE.astype(int)) + (255,))
    hd.ellipse([89, 3, 91, 5], fill=tuple(GOLD_SHINE.astype(int)) + (255,))
    hd.ellipse([85, 4, 87, 6], fill=tuple(GOLD_SHINE.astype(int)) + (255,))
    # Right ear brass base hinge
    hd.ellipse([79, 24, 84, 29], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((81, 26), (255, 255, 255, 255))

    # 2. Main Head Cowl & Marionette Visor (x: 44..84, y: 22..62)
    hcx, hcy = 64.0, 42.0
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                grain = math.sin(x * 1.5 + y * 0.3) * 5.0
                is_hood = (y < 38) or (y > 55) or (dx**2 > 0.48)

                if is_hood:
                    # Polished walnut head cowl
                    if dot > 0.45:
                        col = WALNUT_LIGHT * 0.85 + grain + dot * 20.0
                    elif dot > 0.05:
                        col = WALNUT_BASE + grain + (dot - 0.05) * 35.0
                    elif dot > -0.35:
                        col = WALNUT_SHADOW + grain + (dot + 0.35) * 25.0
                    else:
                        col = WALNUT_DARK + grain * 0.5
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

    # Forehead brass gear & windchime crest emblem
    hd = ImageDraw.Draw(head_img)
    hd.arc([46, 28, 82, 40], start=180, end=360, fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=3)
    hd.arc([47, 29, 81, 39], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.polygon([(64, 25), (68, 30), (64, 35), (60, 30)], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([62, 28, 66, 32], fill=tuple(CORAL_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((64, 30), (255, 255, 255, 255))

    # Feline stylized wooden muzzle line & nose rivet
    hd.line([(61, 49), (67, 49)], fill=tuple(IVORY_DEEP.astype(int)) + (255,), width=1)
    hd.line([(64, 49), (64, 53)], fill=tuple(IVORY_DEEP.astype(int)) + (255,), width=1)
    hd.line([(61, 53), (67, 53)], fill=tuple(IVORY_SHADOW.astype(int)) + (255,), width=1)
    hd.ellipse([62, 47, 66, 50], fill=tuple(ORANGE_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((64, 48), (255, 255, 255, 255))

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

    # Outer decorative eye socket rims
    hd2 = ImageDraw.Draw(out_head)
    hd2.ellipse([49, 37, 59, 47], outline=tuple(ORANGE_DARK.astype(int)) + (255,), width=1)
    hd2.ellipse([69, 37, 79, 47], outline=tuple(ORANGE_DARK.astype(int)) + (255,), width=1)

    # Final re-clear of inner eye sockets (40..44, 52..56 / 72..76)
    head_arr2 = np.array(out_head)
    for ey in range(40, 45):
        for ex in range(52, 57):
            head_arr2[ey, ex, :] = 0
        for ex in range(72, 77):
            head_arr2[ey, ex, :] = 0

    return Image.fromarray(head_arr2)


def build_costume() -> Image.Image:
    """
    SLICE 5: COSTUME (z=25)
    晨曦小鎮提線雜技工裝背心 (costume_lynx_marionette_acrobat_vest)
    Dopamine warm orange acrobat canvas vest, mint green piping, brass pulley buckles,
    hanging spun beeswax thread tassels.
    STRICT 0-ART26b: y >= 96 MUST BE STRICTLY 0 PIXELS!
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Acrobat Vest & Harness (Torso overlay): x: 50..78, y: 58..88
    for y in range(58, 88):
        for x in range(50, 78):
            dx = (x - 64.0) / 13.0
            dy = (y - 72.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                is_v_neck = (y < 68) and (abs(x - 64) < (68 - y) * 1.2)
                if not is_v_neck:
                    dot = -0.5 * dx - 0.7 * dy
                    fold = math.sin((x + y) * 1.4) * 6.0
                    if y > 80:
                        col = ORANGE_DARK + dot * 10.0 + fold
                    elif x < 60:
                        col = ORANGE_LIGHT + dot * 15.0 + fold
                    else:
                        col = ORANGE_BASE + dot * 12.0 + fold
                    costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Mint green enamel piping along collar and edges
    cosd.line([(55, 58), (64, 69), (73, 58)], fill=tuple(MINT_BASE.astype(int)) + (255,), width=2)
    cosd.line([(56, 59), (64, 70), (72, 59)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=1)

    # Golden marionette pulley buckle & diagonal strap
    cosd.line([(54, 62), (74, 82)], fill=tuple(GOLD_DARK.astype(int)) + (255,), width=3)
    cosd.line([(54, 62), (74, 82)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    cosd.line([(54, 62), (74, 82)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cosd.ellipse([61, 69, 67, 75], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    cosd.ellipse([62, 70, 66, 74], fill=tuple(MINT_BASE.astype(int)) + (255,))
    costume_img.putpixel((64, 72), (255, 255, 255, 255))

    # Twin brass buttons on lapels
    cosd.ellipse([54, 66, 58, 70], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    costume_img.putpixel((56, 68), (255, 255, 255, 255))
    cosd.ellipse([70, 66, 74, 70], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    costume_img.putpixel((72, 68), (255, 255, 255, 255))

    # Acrobat waist belt with thread spool pouch (y: 84..88)
    for sy in range(84, 89):
        for sx in range(52, 77):
            s_dot = (sx - 64.0) / 12.0
            if sy == 85 or sy == 86:
                col = MINT_BASE + s_dot * 15.0
            else:
                col = NAVY_BASE + s_dot * 8.0
            costume_img.putpixel((sx, sy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    cosd.ellipse([62, 84, 66, 88], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Small beeswax thread tassels at flanks (stops at y=92)
    cosd.line([(53, 88), (51, 92)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cosd.line([(75, 88), (77, 92)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)

    # STRICT 0-ART26b: clear y >= 96
    arr = np.array(costume_img)
    arr[96:, :, :] = 0
    costume_img = Image.fromarray(arr).copy()

    out_cos = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)
    arr_out = np.array(out_cos)
    arr_out[96:, :, :] = 0
    return Image.fromarray(arr_out)


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=30)
    雙色翡翠寶石目鏡彩釉面甲 (face_lynx_emerald_quartz_eyemask)
    Two-tone emerald quartz goggle lenses, warm orange acrobatic mask trim,
    golden crosshair reticles (#FFD028 / #4ED86A).
    Centers: Left eye at (54, 42), Right eye at (74, 42)
    STRICT 0-ART27: Min alpha >= 200 at (54, 42) and (74, 42).
    """
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    # Acrobat Warm Orange Mask Flairs around eyes
    left_wing_1 = [(46, 42), (39, 40), (43, 44)]
    for y in range(39, 45):
        for x in range(39, 47):
            if point_in_polygon(x, y, left_wing_1):
                col = ORANGE_LIGHT if x < 43 else ORANGE_BASE
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    left_wing_2 = [(54, 47), (52, 52), (56, 49)]
    for y in range(47, 53):
        for x in range(51, 57):
            if point_in_polygon(x, y, left_wing_2):
                col = ORANGE_BASE if y < 50 else ORANGE_DARK
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    right_wing_1 = [(82, 42), (89, 40), (85, 44)]
    for y in range(39, 45):
        for x in range(81, 90):
            if point_in_polygon(x, y, right_wing_1):
                col = ORANGE_LIGHT if x > 85 else ORANGE_BASE
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    right_wing_2 = [(74, 47), (76, 52), (72, 49)]
    for y in range(47, 53):
        for x in range(71, 77):
            if point_in_polygon(x, y, right_wing_2):
                col = ORANGE_BASE if y < 50 else ORANGE_DARK
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Goggle lenses with smooth radial gradient
    for cx in [54, 74]:
        cy = 42
        cored.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=tuple(ORANGE_DARK.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
        for y in range(cy - 4, cy + 5):
            for x in range(cx - 4, cx + 5):
                dx = (x - cx) / 4.0
                dy = (y - cy) / 4.0
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.25:
                        col = MINT_SHINE
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = MINT_BASE * (1.0 - t) + SKY_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = SKY_DARK * (1.0 - t) + NAVY_BASE * t + dot * 12.0
                    else:
                        col = NAVY_BASE * 0.5 + NAVY_DARK * 0.5 + dot * 8.0
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Golden reticle crosshairs
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
    晨曦提線裂空機關爪 (weapon_lynx_dawn_marionette_steel_claws)
    Single-held steel claw at right hand.
    Wrist mount at (96, 72), extending 5 cold-rolled tungsten steel curved claws outward.
    Base carved walnut gauntlet, brass wire pulley hub, razor sharp claw tips.
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Gauntlet wrist mount: centered at (97, 72), width ~14, height ~16
    for y in range(65, 80):
        for x in range(92, 104):
            dx = (x - 98.0) / 5.5
            dy = (y - 72.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                if dot > 0.3:
                    col = WALNUT_LIGHT + dot * 15.0
                elif dot > -0.2:
                    col = WALNUT_BASE + dot * 20.0
                else:
                    col = WALNUT_SHADOW + dot * 15.0
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Brass pulley ring on gauntlet
    wd.ellipse([94, 68, 100, 74], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    wd.ellipse([95, 69, 99, 73], fill=tuple(MINT_BASE.astype(int)) + (255,))
    weapon_img.putpixel((97, 71), (255, 255, 255, 255))

    # 5 Stamped Tungsten Steel Arc Claws:
    claws_def = [
        ((103.0, 64.0), (110.0, 62.0), (118.0, 59.0)),
        ((104.0, 67.0), (113.0, 66.0), (122.0, 65.0)),
        ((105.0, 71.0), (114.0, 71.0), (124.0, 71.0)),
        ((104.0, 75.0), (113.0, 76.0), (122.0, 77.0)),
        ((103.0, 78.0), (110.0, 80.0), (118.0, 83.0)),
    ]

    for p_base, p_mid, p_tip in claws_def:
        # Draw curved quadratic bezier claw
        for t in np.linspace(0.0, 1.0, 30):
            bx = (1.0 - t)**2 * p_base[0] + 2.0 * (1.0 - t) * t * p_mid[0] + t**2 * p_tip[0]
            by = (1.0 - t)**2 * p_base[1] + 2.0 * (1.0 - t) * t * p_mid[1] + t**2 * p_tip[1]
            
            # Thick blade spine
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dx**2 + dy**2 <= 1:
                        px = int(round(bx + dx))
                        py = int(round(by + dy))
                        if 0 <= px < W and 0 <= py < H:
                            if dy < 0 or (dy == 0 and dx < 0):
                                col = STEEL_LIGHT + t * 15.0
                            elif dy == 0 and dx == 0:
                                col = STEEL_BASE + t * 10.0
                            else:
                                col = STEEL_DARK
                            weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Razor blade tip highlight
        tip_x, tip_y = int(round(p_tip[0])), int(round(p_tip[1]))
        if 0 <= tip_x < W and 0 <= tip_y < H:
            weapon_img.putpixel((tip_x, tip_y), tuple(STEEL_SHINE.astype(int)) + (255,))

        # Golden brass rivet at blade root
        base_x, base_y = int(round(p_base[0])), int(round(p_base[1]))
        wd.ellipse([base_x - 2, base_y - 2, base_x + 2, base_y + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
        weapon_img.putpixel((base_x, base_y), (255, 255, 255, 255))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第五十九族 提線猞猁 (lynx) ===")

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
        ("winding_key", "key_lynx_twin_ring_chime_brass", key_img),
        ("back_curio", "curio_lynx_pendulum_bobtail_balance", curio_img),
        ("chassis", "chassis_lynx_marionette_walnut_default", chassis_img),
        ("head_unit", "head_lynx_bazaar_marionette_tufted_cowl", head_img),
        ("costume", "costume_lynx_marionette_acrobat_vest", costume_img),
        ("optic_core", "face_lynx_emerald_quartz_eyemask", core_img),
        ("weapon", "weapon_lynx_dawn_marionette_steel_claws", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{LYNX_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_lynx_twin_ring_chime_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_lynx_dawn_marionette_steel_claws.png")
    print("  ✓ Universal key and weapon copies updated")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{LYNX_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{LYNX_PD_DIR}/proof_paperdoll_lynx_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{LYNX_PD_DIR}/proof_paperdoll_lynx_magenta.png"
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

    strip_path = f"{LYNX_PD_DIR}/proof_lynx_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/lynx_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/lynx_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/lynx_idle.png
    p_idle_64 = f"{PLAYER_DIR}/lynx_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/lynx_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/lynx_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/lynx_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/lynx_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/lynx_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THE MARIONETTE LYNX CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
