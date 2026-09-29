#!/usr/bin/env python3
"""
build_petaurista_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十八族 嵐翼鼯鼠 (The Stormwing Petaurista, petaurista) 7 Paperdoll Slices.
Follows:
- docs/design/STORMWING_PETAURISTA_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, lacquered bamboo wood shell #4ED86A,
  glazed ivory-white porcelain faceplate #FFFDF8, cold-rolled brass hinges #FFD028,
  folding bamboo-lath glider wing flaps #4ED86A/#1F1A3A, dual bamboo-leaf acoustic sonar ears #4ED86A/#FFD028,
  segmented bamboo-weave rudder tail #4ED86A/#FFD028, obsidian quartz goggle lenses #1F1A3A with cinnabar markings #FF5E8A,
  zen octagonal bamboo shuriken #4ED86A/#FFD028/#7A8A9E, three-leaf windchime brass key #FFD028/#FF5E8A)
- review.md 0-ART5, 0-ART6, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
- High-depth multi-tone cel-shading (>= 3 steps per slot, metal highlights & shadow bevels)
- Subpixel anti-aliased silhouette borders (alpha levels > 2)
- chassis 128 unique colors >= 150, all 7 slots c/100px >= 5.0%
- proof composite unique colors >= 300, core holes <= 5px, head vs chassis overlap < 10%
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PETAURISTA_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/petaurista"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Stormwing Petaurista Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([140, 110, 25], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = np.array([255, 253, 248], dtype=float)
IVORY_LIGHT  = np.array([255, 255, 255], dtype=float)
IVORY_SHADOW = np.array([232, 226, 214], dtype=float)
IVORY_DARK   = np.array([205, 196, 180], dtype=float)
IVORY_DEEP   = np.array([170, 160, 142], dtype=float)

# 2. Primary / Mint Bamboo Green (#4ED86A)
MINT_BASE   = np.array([78, 216, 106], dtype=float)
MINT_LIGHT  = np.array([130, 240, 155], dtype=float)
MINT_SHINE  = np.array([192, 255, 208], dtype=float)
MINT_DARK   = np.array([40, 158, 68], dtype=float)
MINT_DEEP   = np.array([24, 110, 44], dtype=float)

# 3. Metal / Dopamine Gold & Brass (#FFD028)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 4. Accent / Cinnabar Red & Coral Pink (#FF5E8A)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_SHINE = np.array([255, 208, 228], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)
CORAL_DEEP  = np.array([135, 30, 65], dtype=float)

# 5. Secondary / Celestial Sky Blue (#38A0FF)
SKY_BASE  = np.array([56, 160, 255], dtype=float)
SKY_LIGHT = np.array([125, 208, 255], dtype=float)
SKY_SHINE = np.array([195, 235, 255], dtype=float)
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([14, 60, 130], dtype=float)

# 6. Cold Stamped Steel & Shuriken Alloy (#7A8A9E)
STEEL_BASE  = np.array([122, 138, 158], dtype=float)
STEEL_LIGHT = np.array([168, 182, 200], dtype=float)
STEEL_SHINE = np.array([215, 226, 238], dtype=float)
STEEL_DARK  = np.array([88, 102, 120], dtype=float)
STEEL_DEEP  = np.array([58, 68, 82], dtype=float)

# 7. Dark Ninja Navy Vest & Goggle Rim (#1F1A3A, #2D274A)
NAVY_BASE  = np.array([45, 39, 74], dtype=float)
NAVY_LIGHT = np.array([72, 64, 110], dtype=float)
NAVY_DARK  = np.array([28, 22, 48], dtype=float)

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
                col = GOLD_BASE + dot * 35.0
                key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Three windchime acoustic blades at -90, 30, 150 deg
    kcx, kcy = 40.0, 30.0
    base_angles = [math.radians(-90), math.radians(30), math.radians(150)]
    for ang in base_angles:
        tip_x = kcx + 17.5 * math.cos(ang)
        tip_y = kcy + 17.5 * math.sin(ang)
        side_l_x = kcx + 11.0 * math.cos(ang - 0.45)
        side_l_y = kcy + 11.0 * math.sin(ang - 0.45)
        side_r_x = kcx + 11.0 * math.cos(ang + 0.45)
        side_r_y = kcy + 11.0 * math.sin(ang + 0.45)

        poly_l = [(kcx, kcy), (side_l_x, side_l_y), (tip_x, tip_y)]
        poly_r = [(kcx, kcy), (tip_x, tip_y), (side_r_x, side_r_y)]

        all_x = [kcx, tip_x, side_l_x, side_r_x]
        all_y = [kcy, tip_y, side_l_y, side_r_y]
        min_x, max_x = int(min(all_x)) - 1, int(max(all_x)) + 1
        min_y, max_y = int(min(all_y)) - 1, int(max(all_y)) + 1

        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if point_in_polygon(x, y, poly_l):
                    dist_tip = math.sqrt((x - tip_x)**2 + (y - tip_y)**2)
                    dot = -0.5 * (x - kcx) / 18.0 - 0.7 * (y - kcy) / 18.0
                    col = GOLD_LIGHT * 0.75 + GOLD_SHINE * 0.25 + dot * 25.0 - dist_tip * 1.5
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
                elif point_in_polygon(x, y, poly_r):
                    dist_tip = math.sqrt((x - tip_x)**2 + (y - tip_y)**2)
                    dot = -0.5 * (x - kcx) / 18.0 - 0.7 * (y - kcy) / 18.0
                    col = GOLD_BASE * 0.6 + GOLD_DARK * 0.4 + dot * 20.0 - dist_tip * 1.5
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Ridge line
        kd.line([(int(kcx), int(kcy)), (int(tip_x), int(tip_y))], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)

        # Resonant slot circle near tip
        slot_x = kcx + 12.0 * math.cos(ang)
        slot_y = kcy + 12.0 * math.sin(ang)
        for sy in range(int(slot_y - 3), int(slot_y + 4)):
            for sx in range(int(slot_x - 3), int(slot_x + 4)):
                s_dist = math.sqrt((sx - slot_x)**2 + (sy - slot_y)**2)
                if s_dist <= 2.5:
                    if s_dist <= 1.2:
                        col = GOLD_DARK
                    else:
                        col = OUTLINE_KEY
                    key_img.putpixel((sx, sy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        key_img.putpixel((int(slot_x), int(slot_y)), tuple(GOLD_SHINE.astype(int)) + (255,))

    # Center decorative collar & coral button
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
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    tail_nodes = [
        (48.0, 90.0, 7.0),
        (40.0, 88.0, 6.5),
        (32.0, 84.0, 6.0),
        (24.0, 80.0, 5.5),
        (16.0, 76.0, 5.0)
    ]

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
                            col = MINT_LIGHT + dot * 20.0 + grain
                        elif dot > -0.25:
                            col = MINT_BASE + dot * 25.0 + grain
                        else:
                            col = MINT_DARK + dot * 20.0 + grain
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

    # Rudder paddle at tail tip around (16, 76)
    rudder_cx, rudder_cy = 16.0, 76.0
    for y in range(63, 89):
        for x in range(5, 27):
            dx = (x - rudder_cx) / 9.5
            dy = (y - rudder_cy) / 11.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                dist = math.sqrt(dist_sq)
                dot = -0.6 * dx - 0.6 * dy
                grain = math.sin((x + y) * 1.8) * 6.0
                if dist > 0.85:
                    col = GOLD_DARK + grain * 0.5
                elif dist > 0.70:
                    col = GOLD_BASE + grain * 0.5
                else:
                    pattern = (x + y) % 3
                    if pattern == 0:
                        col = MINT_LIGHT + dot * 25.0 + grain
                    elif pattern == 1:
                        col = MINT_BASE + dot * 20.0 + grain
                    else:
                        col = MINT_DARK + dot * 15.0 + grain
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Stabilizer fin vane & brass hub
    cd.line([(16, 64), (16, 87)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cd.line([(7, 76), (25, 76)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cd.ellipse([13, 73, 19, 79], fill=tuple(GOLD_DEEP.astype(int)) + (255,))
    cd.ellipse([14, 74, 18, 78], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    cd.ellipse([15, 75, 17, 77], fill=tuple(GOLD_LIGHT.astype(int)) + (255,))
    curio_img.putpixel((16, 76), (255, 255, 255, 255))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))

    # 2. Feet and Boots (y: 98..111)
    for bx, by in [(50.0, 105.0), (76.0, 105.0)]:
        for y in range(int(by - 14), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.0
                dy = (y - (by - 8)) / 7.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.7 * dy
                    grain = math.sin(x * 2.0) * 4.0
                    if dot > 0.3:
                        col = MINT_LIGHT + grain + dot * 15.0
                    elif dot > -0.2:
                        col = MINT_BASE + grain + dot * 20.0
                    else:
                        col = MINT_DARK + grain + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass knee cap
        for y in range(int(by - 11), int(by - 6)):
            for x in range(int(bx - 3), int(bx + 4)):
                if (x - bx)**2 + (y - (by - 8.5))**2 <= 9.0:
                    dist = math.sqrt((x - (bx - 1))**2 + (y - (by - 9.5))**2)
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 8.5) / 3.0
                    col = GOLD_SHINE if dot > 0.4 else (GOLD_BASE + dot * 25.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Foot shoe base
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
                            col = MINT_LIGHT + dot * 15.0
                        elif dot > -0.2:
                            col = MINT_BASE + dot * 20.0
                        else:
                            col = MINT_DARK + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Main Torso Bamboo Body (x: 44..84, y: 58..95)
    cx, cy = 64.0, 77.0
    for y in range(58, 96):
        for x in range(44, 84):
            dx = (x - cx) / 18.5
            dy = (y - cy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, -0.6 * dx - 0.7 * dy + 0.4 * nz - 0.6) / 0.4
                grain = math.sin(x * 1.6 + y * 0.2) * 5.0

                if dot > 0.45:
                    col = MINT_LIGHT * 0.85 + MINT_SHINE * 0.15 + grain + spec * 30.0
                elif dot > 0.05:
                    col = MINT_BASE + grain + (dot - 0.05) * 40.0
                elif dot > -0.35:
                    col = MINT_DARK + grain + (dot + 0.35) * 30.0
                else:
                    col = MINT_DEEP + grain * 0.5

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Glazed Ivory Porcelain Belly/Chest Plate (x: 50..78, y: 62..90)
    pcx, pcy = 64.0, 76.0
    for y in range(62, 91):
        for x in range(50, 78):
            pdx = (x - pcx) / 12.0
            pdy = (y - pcy) / 13.0
            pdsq = pdx**2 + pdy**2
            if pdsq <= 1.0:
                pnz = math.sqrt(max(0.0, 1.0 - pdsq))
                pdot = -0.55 * pdx - 0.70 * pdy + 0.45 * pnz
                shine = max(0.0, 1.0 - ((x - (pcx - 3))**2 + (y - (pcy - 4))**2)**0.5 / 4.0)**2

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

    # Seams & brass rivets
    chd = ImageDraw.Draw(chassis_img)
    chd.line([(64, 64), (64, 88)], fill=tuple(IVORY_DEEP.astype(int)) + (255,), width=1)
    for ry in [68, 76, 84]:
        for rx in [56, 72]:
            chd.ellipse([rx - 2, ry - 2, rx + 2, ry + 2], fill=tuple(GOLD_DARK.astype(int)) + (255,))
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,))
            chassis_img.putpixel((rx, ry), (255, 255, 255, 255))

    # Arms and paws
    for t in np.linspace(0.0, 1.0, 20):
        ax = 46.0 * (1.0 - t)**2 + 38.0 * 2 * (1.0 - t) * t + 34.0 * t**2
        ay = 64.0 * (1.0 - t)**2 + 70.0 * 2 * (1.0 - t) * t + 76.0 * t**2
        chd.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=tuple(MINT_BASE.astype(int)) + (255,))
        chd.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=tuple(MINT_LIGHT.astype(int)) + (255,))
    chd.ellipse([36, 68, 41, 73], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    chd.ellipse([30, 73, 37, 80], fill=tuple(IVORY_BASE.astype(int)) + (255,))
    chassis_img.putpixel((32, 75), (255, 255, 255, 255))

    # Right arm (stops at x <= 92):
    for t in np.linspace(0.0, 1.0, 20):
        ax = 78.0 * (1.0 - t)**2 + 84.0 * 2 * (1.0 - t) * t + 89.0 * t**2
        ay = 64.0 * (1.0 - t)**2 + 68.0 * 2 * (1.0 - t) * t + 73.0 * t**2
        chd.ellipse([ax - 3, ay - 3, ax + 3, ay + 3], fill=tuple(MINT_BASE.astype(int)) + (255,))
        chd.ellipse([ax - 2, ay - 2, ax + 2, ay + 2], fill=tuple(MINT_LIGHT.astype(int)) + (255,))
    chd.ellipse([82, 66, 87, 71], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    chd.ellipse([85, 70, 92, 77], fill=tuple(IVORY_BASE.astype(int)) + (255,))
    chassis_img.putpixel((88, 72), (255, 255, 255, 255))

    out_chassis = apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=[(94, 0, 127, 127)])
    arr = np.array(out_chassis)
    arr[:, 94:, :] = 0
    return Image.fromarray(arr)


def build_head_unit() -> Image.Image:
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Bamboo-leaf Sonar Acoustic Ears
    ear_l_poly = [(46, 28), (42, 20), (35, 6), (42, 12), (48, 24)]
    hd.polygon(ear_l_poly, fill=tuple(MINT_BASE.astype(int)) + (255,))
    hd.line([(46, 28), (35, 6)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=2)
    hd.line([(45, 26), (36, 8)], fill=tuple(MINT_SHINE.astype(int)) + (255,), width=1)
    hd.ellipse([43, 24, 48, 29], fill=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([44, 25, 47, 28], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    head_img.putpixel((45, 26), (255, 255, 255, 255))

    ear_r_poly = [(82, 28), (86, 20), (93, 6), (86, 12), (80, 24)]
    hd.polygon(ear_r_poly, fill=tuple(MINT_BASE.astype(int)) + (255,))
    hd.line([(82, 28), (93, 6)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=2)
    hd.line([(83, 26), (92, 8)], fill=tuple(MINT_SHINE.astype(int)) + (255,), width=1)
    hd.ellipse([80, 24, 85, 29], fill=tuple(GOLD_DARK.astype(int)) + (255,))
    hd.ellipse([81, 25, 84, 28], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    head_img.putpixel((82, 26), (255, 255, 255, 255))

    # 2. Main Head Cowl & Bamboo Ninja Hood (x: 44..84, y: 22..62)
    hcx, hcy = 64.0, 42.0
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, dot - 0.65) / 0.35
                grain = math.sin(x * 1.5 + y * 0.3) * 5.0

                is_hood = (y < 35) or (dx**2 > 0.65)
                if is_hood:
                    if dot > 0.45:
                        col = MINT_LIGHT * 0.85 + MINT_SHINE * 0.15 + grain + spec * 25.0
                    elif dot > 0.05:
                        col = MINT_BASE + grain + (dot - 0.05) * 35.0
                    elif dot > -0.35:
                        col = MINT_DARK + grain + (dot + 0.35) * 25.0
                    else:
                        col = MINT_DEEP + grain * 0.5
                else:
                    pdot = dot
                    shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 5.0)**2
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

    # Forehead headband & crest
    hd = ImageDraw.Draw(head_img)
    hd.arc([46, 28, 82, 40], start=180, end=360, fill=tuple(NAVY_BASE.astype(int)) + (255,), width=3)
    hd.arc([47, 29, 81, 39], start=180, end=360, fill=tuple(SKY_BASE.astype(int)) + (255,), width=1)
    hd.polygon([(64, 25), (68, 30), (64, 35), (60, 30)], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    head_img.putpixel((64, 30), (255, 255, 255, 255))

    # Respirator nose slit at (64, 49)
    hd.line([(62, 49), (66, 49)], fill=tuple(IVORY_DEEP.astype(int)) + (255,), width=1)
    head_img.putpixel((64, 50), tuple(GOLD_DARK.astype(int)) + (255,))

    # Hollow out eye sockets (0-ART27)
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

    # Strictly re-enforce zero alpha in hollow eye sockets
    head_arr = np.array(out_head)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_arr[ey, ex, :] = 0
        for ex in range(70, 79):
            head_arr[ey, ex, :] = 0

    # Outer decorative eye socket rims
    hd2 = ImageDraw.Draw(out_head)
    hd2.ellipse([49, 37, 59, 47], outline=tuple(NAVY_BASE.astype(int)) + (255,), width=1)
    hd2.ellipse([69, 37, 79, 47], outline=tuple(NAVY_BASE.astype(int)) + (255,), width=1)

    # Final re-clear of inner eye sockets (40..44, 52..56 / 72..76)
    head_arr2 = np.array(out_head)
    for ey in range(40, 45):
        for ex in range(52, 57):
            head_arr2[ey, ex, :] = 0
        for ex in range(72, 77):
            head_arr2[ey, ex, :] = 0

    return Image.fromarray(head_arr2)


def build_costume() -> Image.Image:
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Glider Wing Flaps with rich procedural cel gradient
    lath_left_1 = [(48, 64), (32, 74), (28, 86), (42, 82), (48, 76)]
    for y in range(63, 87):
        for x in range(27, 49):
            if point_in_polygon(x, y, lath_left_1):
                t_l = (x - 28.0) / 20.0
                t_w = (y - 64.0) / 22.0
                dot = -0.5 * (1.0 - t_l) - 0.7 * (1.0 - t_w)
                col = MINT_LIGHT * (0.6 + 0.4 * t_l) + MINT_BASE * (0.4 * (1.0 - t_l)) + dot * 25.0
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    cosd.line([(48, 64), (28, 86)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    cosd.line([(47, 64), (27, 86)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cosd.line([(42, 68), (34, 84)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=1)
    for y in range(75, 85):
        for x in range(29, 41):
            if point_in_polygon(x, y, [(36, 76), (30, 84), (40, 81)]):
                col = SKY_BASE + (x - 30) * 8.0
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    lath_right_1 = [(80, 64), (92, 74), (91, 84), (82, 82), (78, 76)]
    for y in range(63, 85):
        for x in range(77, 93):
            if point_in_polygon(x, y, lath_right_1):
                t_l = (92.0 - x) / 15.0
                t_w = (y - 64.0) / 20.0
                dot = -0.5 * (1.0 - t_l) - 0.7 * (1.0 - t_w)
                col = MINT_LIGHT * (0.6 + 0.4 * t_l) + MINT_BASE * (0.4 * (1.0 - t_l)) + dot * 25.0
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    cosd.line([(80, 64), (91, 84)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    cosd.line([(81, 64), (92, 84)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cosd.line([(84, 68), (88, 82)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=1)
    for y in range(75, 83):
        for x in range(82, 91):
            if point_in_polygon(x, y, [(86, 76), (90, 82), (83, 80)]):
                col = SKY_BASE + (90 - x) * 8.0
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Wing folding brass hinges
    cosd.ellipse([44, 68, 49, 73], fill=tuple(GOLD_DARK.astype(int)) + (255,))
    cosd.ellipse([45, 69, 48, 72], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    costume_img.putpixel((46, 70), (255, 255, 255, 255))

    cosd.ellipse([79, 68, 84, 73], fill=tuple(GOLD_DARK.astype(int)) + (255,))
    cosd.ellipse([80, 69, 83, 72], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    costume_img.putpixel((81, 70), (255, 255, 255, 255))

    # 2. Ninja Vest & Harness: x: 50..78, y: 58..88
    for y in range(58, 88):
        for x in range(50, 78):
            dx = (x - 64.0) / 13.0
            dy = (y - 72.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                is_v_neck = (y < 68) and (abs(x - 64) < (68 - y) * 1.2)
                if not is_v_neck:
                    dot = -0.5 * dx - 0.7 * dy
                    fold = math.sin((x + y) * 1.5) * 6.0
                    if y > 80:
                        col = NAVY_DARK + dot * 10.0 + fold
                    elif x < 60:
                        col = NAVY_LIGHT + dot * 15.0 + fold
                    else:
                        col = NAVY_BASE + dot * 12.0 + fold
                    costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sky blue piping
    cosd.line([(55, 58), (64, 69), (73, 58)], fill=tuple(SKY_BASE.astype(int)) + (255,), width=2)
    cosd.line([(56, 59), (64, 70), (72, 59)], fill=tuple(SKY_LIGHT.astype(int)) + (255,), width=1)

    # Golden buckle & diagonal strap
    cosd.line([(54, 62), (74, 82)], fill=tuple(GOLD_DARK.astype(int)) + (255,), width=3)
    cosd.line([(54, 62), (74, 82)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    cosd.line([(54, 62), (74, 82)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    cosd.ellipse([62, 70, 68, 76], fill=tuple(GOLD_DARK.astype(int)) + (255,))
    cosd.ellipse([63, 71, 67, 75], fill=tuple(GOLD_BASE.astype(int)) + (255,))
    cosd.ellipse([64, 72, 66, 74], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    costume_img.putpixel((65, 73), (255, 255, 255, 255))

    # Waist sash belt (y: 84..88)
    for sy in range(84, 89):
        for sx in range(52, 77):
            s_dot = (sx - 64.0) / 12.0
            if sy == 85 or sy == 86:
                col = SKY_BASE + s_dot * 15.0
            else:
                col = NAVY_BASE + s_dot * 8.0
            costume_img.putpixel((sx, sy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    cosd.line([(53, 85), (75, 85)], fill=tuple(SKY_LIGHT.astype(int)) + (255,), width=1)
    cosd.ellipse([62, 84, 66, 88], fill=tuple(GOLD_BASE.astype(int)) + (255,))

    # STRICT 0-ART26b: clear y >= 96
    arr = np.array(costume_img)
    arr[96:, :, :] = 0
    costume_img = Image.fromarray(arr).copy()

    out_cos = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)
    arr_out = np.array(out_cos)
    arr_out[96:, :, :] = 0
    return Image.fromarray(arr_out)


def build_optic_core() -> Image.Image:
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    # Cinnabar Red Ninja Markings
    left_wing_1 = [(46, 42), (40, 40), (43, 44)]
    for y in range(39, 45):
        for x in range(39, 47):
            if point_in_polygon(x, y, left_wing_1):
                col = CORAL_LIGHT if x < 43 else CORAL_BASE
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    left_wing_2 = [(54, 47), (52, 52), (56, 49)]
    for y in range(47, 53):
        for x in range(51, 57):
            if point_in_polygon(x, y, left_wing_2):
                col = CORAL_BASE if y < 50 else CORAL_DARK
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    right_wing_1 = [(82, 42), (88, 40), (85, 44)]
    for y in range(39, 45):
        for x in range(81, 89):
            if point_in_polygon(x, y, right_wing_1):
                col = CORAL_LIGHT if x > 85 else CORAL_BASE
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    right_wing_2 = [(74, 47), (76, 52), (72, 49)]
    for y in range(47, 53):
        for x in range(71, 77):
            if point_in_polygon(x, y, right_wing_2):
                col = CORAL_BASE if y < 50 else CORAL_DARK
                core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Goggle lenses with smooth radial gradient
    for cx in [54, 74]:
        cy = 42
        cored.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=tuple(NAVY_DARK.astype(int)) + (255,))
        for y in range(cy - 4, cy + 5):
            for x in range(cx - 4, cx + 5):
                dx = (x - cx) / 4.0
                dy = (y - cy) / 4.0
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.22:
                        col = MINT_SHINE
                    elif dist < 0.45:
                        t = (dist - 0.22) / 0.23
                        col = MINT_BASE * (1.0 - t) + SKY_BASE * t + dot * 15.0
                    elif dist < 0.75:
                        t = (dist - 0.45) / 0.30
                        col = SKY_DARK * (1.0 - t) + NAVY_BASE * t + dot * 12.0
                    else:
                        col = NAVY_BASE * 0.4 + NAVY_DARK * 0.6 + dot * 8.0
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Golden reticle crosshairs
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(GOLD_SHINE.astype(int)) + (255,))

        # White eye reflection glint
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=(255, 255, 255, 255))
        cored.point((cx + 2, cy + 2), fill=tuple(SKY_LIGHT.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wcx, wcy = 104.0, 68.0
    num_blades = 8
    outer_r = 16.0
    inner_r = 8.0

    blade_pts = []
    for i in range(num_blades * 2):
        ang = math.radians(i * (360.0 / (num_blades * 2)) - 22.5)
        r = outer_r if (i % 2 == 0) else inner_r
        bx = wcx + r * math.cos(ang)
        by = wcy + r * math.sin(ang)
        blade_pts.append((int(round(bx)), int(round(by))))

    wd.polygon(blade_pts, fill=tuple(STEEL_BASE.astype(int)) + (255,))

    for i in range(num_blades):
        tip_idx = i * 2
        p_tip = blade_pts[tip_idx]
        p_in1 = blade_pts[(tip_idx - 1) % len(blade_pts)]
        p_in2 = blade_pts[(tip_idx + 1) % len(blade_pts)]

        # Highlight facet
        poly_h = [(int(wcx), int(wcy)), p_tip, p_in1]
        for y in range(min(p_tip[1], p_in1[1], int(wcy)), max(p_tip[1], p_in1[1], int(wcy)) + 1):
            for x in range(min(p_tip[0], p_in1[0], int(wcx)), max(p_tip[0], p_in1[0], int(wcx)) + 1):
                if point_in_polygon(x, y, poly_h):
                    dist = math.sqrt((x - wcx)**2 + (y - wcy)**2) / 16.0
                    col = STEEL_LIGHT + dist * 25.0
                    weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Shadow facet
        poly_s = [(int(wcx), int(wcy)), p_tip, p_in2]
        for y in range(min(p_tip[1], p_in2[1], int(wcy)), max(p_tip[1], p_in2[1], int(wcy)) + 1):
            for x in range(min(p_tip[0], p_in2[0], int(wcx)), max(p_tip[0], p_in2[0], int(wcx)) + 1):
                if point_in_polygon(x, y, poly_s):
                    dist = math.sqrt((x - wcx)**2 + (y - wcy)**2) / 16.0
                    col = STEEL_DARK - dist * 15.0
                    weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        wd.line([(int(wcx), int(wcy)), p_tip], fill=tuple(STEEL_SHINE.astype(int)) + (255,), width=1)

    # Lacquered Bamboo Inlay Ring (r=5.5..9.5)
    for y in range(int(wcy - 10), int(wcy + 11)):
        for x in range(int(wcx - 10), int(wcx + 11)):
            dist = math.sqrt((x - wcx)**2 + (y - wcy)**2)
            if 5.5 <= dist <= 9.5:
                dot = -0.5 * (x - wcx) / dist - 0.7 * (y - wcy) / dist
                if dist < 7.5:
                    col = MINT_LIGHT + dot * 20.0
                else:
                    col = MINT_BASE + dot * 15.0
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Center Brass Hub (r=5)
    for y in range(int(wcy - 5), int(wcy + 6)):
        for x in range(int(wcx - 5), int(wcx + 6)):
            dist = math.sqrt((x - wcx)**2 + (y - wcy)**2)
            if dist <= 5.0:
                dot = -0.5 * (x - wcx) / 5.0 - 0.7 * (y - wcy) / 5.0
                if dist > 3.2:
                    col = GOLD_DARK + dot * 15.0
                elif dist > 1.8:
                    col = GOLD_BASE + dot * 25.0
                else:
                    col = CORAL_BASE + dot * 15.0
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    weapon_img.putpixel((int(wcx), int(wcy)), (255, 255, 255, 255))

    # 4 Acoustic Tuning Fork Sound Holes
    for h_ang in [0, 90, 180, 270]:
        rad = math.radians(h_ang + 45)
        hx = int(round(wcx + 7.5 * math.cos(rad)))
        hy = int(round(wcy + 7.5 * math.sin(rad)))
        wd.ellipse([hx - 1, hy - 1, hx + 1, hy + 1], fill=tuple(OUTLINE.astype(int)) + (255,))
        weapon_img.putpixel((hx, hy), tuple(GOLD_LIGHT.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第五十八族 嵐翼鼯鼠 (petaurista) ===")

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
        ("winding_key", "key_petaurista_three_leaf_windchime_brass", key_img),
        ("back_curio", "curio_petaurista_bamboo_weave_rudder_tail", curio_img),
        ("chassis", "chassis_petaurista_lacquered_bamboo_default", chassis_img),
        ("head_unit", "head_petaurista_zen_bamboo_ninja_cowl", head_img),
        ("costume", "costume_petaurista_folding_glider_wing_harness", costume_img),
        ("optic_core", "face_petaurista_obsidian_goggle_cinnabar_mask", core_img),
        ("weapon", "weapon_petaurista_zen_octagonal_bamboo_dart", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{PETAURISTA_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_petaurista_three_leaf_windchime_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_petaurista_zen_octagonal_bamboo_dart.png")
    print("  ✓ Universal key and weapon copies updated")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # Render order:
    # z=5:  winding_key
    # z=8:  back_curio
    # z=10: chassis
    # z=20: head_unit
    # z=25: costume
    # z=30: optic_core
    # z=40: weapon
    # Reload saved 128px PNG files from disk so composite is 100% bitwise
    # identical to downstream re-composite (diff bbox = None).
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p_slice = f"{PETAURISTA_PD_DIR}/{slot}/{item_id}.png"
        s_img = Image.open(p_slice).convert("RGBA")
        composite.alpha_composite(s_img)

    proof_comp = f"{PETAURISTA_PD_DIR}/proof_paperdoll_petaurista_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{PETAURISTA_PD_DIR}/proof_paperdoll_petaurista_magenta.png"
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

    strip_path = f"{PETAURISTA_PD_DIR}/proof_petaurista_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/petaurista_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/petaurista_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/petaurista_idle.png
    p_idle_64 = f"{PLAYER_DIR}/petaurista_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/petaurista_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/petaurista_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/petaurista_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/petaurista_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/petaurista_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THE STORMWING PETAURISTA CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
