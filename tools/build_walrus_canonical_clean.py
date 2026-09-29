#!/usr/bin/env python3
"""
build_walrus_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十二族 破冰海象 (The Icebreaker Walrus, walrus) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/ICEBREAKER_WALRUS_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological tissue, stamped pressure-proof titanium alloy plates #FFFDF8/#38A0FF,
  cold-rolled tungsten icebreaker chisel tusks #FFD028, flexible brass sonar whiskers #FFD028,
  quartz pressure dome optic core #4ED86A, double-breasted sailor peacoat cuirass #38A0FF/#FFA010,
  dual ballast decompression tanks #38A0FF/#FFD028, dual-fluke anchor handwheel brass key #FFD028/#FF5E8A,
  heavy-backed naval icebreaker cutlass #38A0FF/#FFD028)
- references/art_direction.md & references/brand_assets.md
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALRUS_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/walrus"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Icebreaker Walrus Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep indigo-violet thick outline
OUTLINE_KEY = np.array([142, 112, 28], dtype=float)     # Warm golden bronze outline for key (complies with 0-ART29 dark limit < 13)

# 1. Base: Polished Ivory Porcelain & Titanium White (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)
IVORY_BASE   = np.array([244, 242, 236], dtype=float)
IVORY_SHADE  = np.array([218, 222, 228], dtype=float)
IVORY_DARK   = np.array([185, 192, 204], dtype=float)

# 2. Azure Blue Waterproof Titanium Plates (#38A0FF)
AZURE_SHINE  = np.array([195, 235, 255], dtype=float)
AZURE_LIGHT  = np.array([115, 200, 255], dtype=float)
AZURE_BASE   = np.array([56, 160, 255], dtype=float)
AZURE_SHADE  = np.array([30, 115, 205], dtype=float)
AZURE_DARK   = np.array([18, 75, 150], dtype=float)
AZURE_DEEP   = np.array([12, 45, 105], dtype=float)

# 3. Dopamine Gold & Forged Brass (#FFD028)
GOLD_SHINE   = np.array([255, 250, 190], dtype=float)
GOLD_LIGHT   = np.array([255, 232, 105], dtype=float)
GOLD_BASE    = np.array([255, 208, 40], dtype=float)
GOLD_SHADE   = np.array([205, 150, 20], dtype=float)
GOLD_DARK    = np.array([145, 95, 10], dtype=float)

# 4. Sunset Warm Orange Trimming (#FFA010)
ORANGE_SHINE = np.array([255, 228, 140], dtype=float)
ORANGE_LIGHT = np.array([255, 192, 70], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)
ORANGE_SHADE = np.array([215, 115, 10], dtype=float)
ORANGE_DARK  = np.array([160, 75, 8], dtype=float)

# 5. Mint Green Optic Core (#4ED86A)
MINT_SHINE   = np.array([215, 255, 225], dtype=float)
MINT_LIGHT   = np.array([140, 248, 165], dtype=float)
MINT_BASE    = np.array([78, 216, 106], dtype=float)
MINT_SHADE   = np.array([45, 165, 75], dtype=float)
MINT_DARK    = np.array([24, 110, 50], dtype=float)

# 6. Coral Pink Accent (#FF5E8A)
CORAL_SHINE  = np.array([255, 210, 228], dtype=float)
CORAL_LIGHT  = np.array([255, 148, 180], dtype=float)
CORAL_BASE   = np.array([255, 94, 138], dtype=float)
CORAL_DARK   = np.array([195, 50, 92], dtype=float)

# 7. Cold-Rolled Steel & Naval Cutlass Metal
STEEL_SHINE  = np.array([240, 248, 255], dtype=float)
STEEL_LIGHT  = np.array([195, 215, 235], dtype=float)
STEEL_BASE   = np.array([150, 172, 195], dtype=float)
STEEL_SHADE  = np.array([98, 118, 142], dtype=float)
STEEL_DARK   = np.array([55, 68, 85], dtype=float)

WHITE_SHINE  = np.array([255, 255, 255], dtype=float)


def apply_antialiased_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=50, ignore_regions=None) -> Image.Image:
    """
    Applies a clean 1px dark outline with smooth anti-aliasing on the outer boundary.
    Solid interior remains solid (alpha=255).
    Guarantees anti-aliasing without bleed into ignored regions (e.g. eye sockets, lower chassis cutoffs).
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

    res = np.zeros((h, w, 4), dtype=np.uint8)
    for y in range(h):
        for x in range(w):
            if opaque_mask[y, x]:
                res[y, x] = arr[y, x]
            elif outline_alpha[y, x] > 0:
                res[y, x, :3] = outline_rgb[y, x]
                res[y, x, 3] = int(outline_alpha[y, x])
    return Image.fromarray(res, "RGBA")


def build_winding_key() -> Image.Image:
    """
    SLICE 1: WINDING KEY (z=5)
    雙葉鍍金海錨輪轂黃銅發條鑰匙 (key_walrus_anchor_handwheel_brass)
    Dual-Fluke Anchor Handwheel Brass Key.
    Located behind upper-left back around center (42, 32).
    Anchor handwheel with circular outer ring, 4 spokes, dual flukes at bottom,
    central hub with Coral Pink (#FF5E8A) protective rivet.
    Uses OUTLINE_KEY (warm golden bronze) to guarantee 0-ART29 dark limit < 13 & white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    kcx, kcy = 42.0, 32.0

    # 1. Key shaft from chassis socket (46, 52) to center (kcx, kcy)
    shaft_pts = [(47, 52), (49, 53), (44, 34), (41, 33)]
    kd.polygon(shaft_pts, fill=tuple(GOLD_DARK.astype(int)) + (255,))
    kd.line([(42, 34), (48, 52)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)

    # 2. Outer circular handwheel ring: outer r=14, inner r=10
    for y in range(int(kcy - 16), int(kcy + 17)):
        for x in range(int(kcx - 16), int(kcx + 17)):
            dist = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if 9.5 <= dist <= 14.5:
                # Radial and directional shading
                angle = math.atan2(y - kcy, x - kcx)
                dot = -0.6 * math.cos(angle) - 0.7 * math.sin(angle)
                if dot > 0.4:
                    col = GOLD_SHINE * 0.7 + GOLD_LIGHT * 0.3
                elif dot > -0.1:
                    col = GOLD_BASE + dot * 25.0
                elif dot > -0.5:
                    col = GOLD_SHADE + (dot + 0.1) * 20.0
                else:
                    col = GOLD_DARK
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Four Handwheel Spokes (Horizontal, Vertical, and 45-degree anchor crossbar)
    # Horizontal crossbar
    for x in range(int(kcx - 10), int(kcx + 11)):
        for y in [int(kcy - 1), int(kcy), int(kcy + 1)]:
            if (x - kcx)**2 + (y - kcy)**2 <= 100:
                col = GOLD_LIGHT if y < kcy else GOLD_SHADE
                key_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # Vertical crossbar
    for y in range(int(kcy - 10), int(kcy + 11)):
        for x in [int(kcx - 1), int(kcx), int(kcx + 1)]:
            if (x - kcx)**2 + (y - kcy)**2 <= 100:
                col = GOLD_LIGHT if x < kcx else GOLD_SHADE
                key_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # 4. Dual Anchor Flukes extending from lower rim of handwheel
    # Left fluke curving from (34, 42) -> (28, 40) -> (26, 34)
    left_fluke = [(36, 42), (32, 45), (27, 43), (25, 36), (28, 36), (30, 40), (34, 40)]
    kd.polygon(left_fluke, fill=tuple(GOLD_BASE.astype(int)) + (255,))
    # Right fluke curving from (50, 42) -> (56, 45) -> (59, 36)
    right_fluke = [(48, 42), (52, 45), (57, 43), (59, 36), (56, 36), (54, 40), (50, 40)]
    kd.polygon(right_fluke, fill=tuple(GOLD_BASE.astype(int)) + (255,))

    # 5. Central Hub with Coral Pink Rivet (#FF5E8A)
    # Hub brass ring
    for y in range(int(kcy - 4), int(kcy + 5)):
        for x in range(int(kcx - 4), int(kcx + 5)):
            dsq = (x - kcx)**2 + (y - kcy)**2
            if dsq <= 16:
                col = GOLD_LIGHT if x < kcx else GOLD_SHADE
                key_img.putpixel((x, y), tuple(col.astype(int)) + (255,))
    # Coral Pink center rivet
    for y in range(int(kcy - 2), int(kcy + 3)):
        for x in range(int(kcx - 2), int(kcx + 3)):
            dsq = (x - kcx)**2 + (y - kcy)**2
            if dsq <= 4.5:
                col = CORAL_SHINE if (x <= kcx and y <= kcy) else CORAL_BASE
                key_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    雙聯減壓壓載氣箱與防鏽油壺 (curio_walrus_dual_ballast_tanks)
    Dual Ballast Decompression Tanks & De-rusting Reservoir.
    Mounted behind the character's left back at x: 25..46, y: 48..84.
    Two vertical cylindrical tanks:
    - Left tank: Azure blue (#38A0FF) with gold brass bands (#FFD028) & orange relief valve (#FFA010).
    - Right tank / oil reservoir: brass tank with clear oil level gauge (#4ED86A).
    - Micro bubbles floating upward (x: 26..38, y: 38..48).
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Tank 1: Left Cylinder (x: 26..35, y: 52..80)
    for y in range(52, 81):
        for x in range(26, 36):
            dx = (x - 30.5) / 4.5
            if abs(dx) <= 1.0:
                dot = -0.7 * dx
                if 63 <= y <= 66 or 72 <= y <= 75:  # Brass reinforcing rings
                    col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                else:  # Azure blue pressure vessel
                    if dot > 0.4:
                        col = AZURE_LIGHT
                    elif dot > -0.1:
                        col = AZURE_BASE + dot * 30.0
                    else:
                        col = AZURE_DARK
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Tank 1 top valve cap (x: 28..33, y: 48..51)
    for y in range(48, 52):
        for x in range(28, 34):
            col = ORANGE_LIGHT if x < 31 else ORANGE_SHADE
            curio_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # Tank 2: Right Cylinder / Reservoir (x: 35..44, y: 55..83)
    for y in range(55, 84):
        for x in range(35, 45):
            dx = (x - 39.5) / 4.5
            if abs(dx) <= 1.0:
                dot = -0.7 * dx
                if 64 <= y <= 74 and abs(dx) <= 0.5:  # Glass oil inspection window
                    col = MINT_LIGHT if dot > 0.1 else MINT_BASE
                else:  # Gold / Brass casing
                    if dot > 0.4:
                        col = GOLD_SHINE
                    elif dot > -0.1:
                        col = GOLD_BASE + dot * 25.0
                    else:
                        col = GOLD_DARK
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Tank 2 top valve wheel (x: 37..42, y: 51..54)
    for y in range(51, 55):
        for x in range(37, 43):
            col = GOLD_LIGHT if x < 40 else GOLD_SHADE
            curio_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # Connecting manifold pipe between tanks (y: 68..70, x: 33..37)
    for y in range(68, 71):
        for x in range(33, 38):
            curio_img.putpixel((x, y), tuple(GOLD_BASE.astype(int)) + (255,))

    # Micro bubble release particles floating up
    bubbles = [(29, 44, 2), (32, 40, 1.5), (28, 36, 1.2), (34, 34, 1.8)]
    for bx, by, br in bubbles:
        for y in range(int(by - br - 1), int(by + br + 2)):
            for x in range(int(bx - br - 1), int(bx + br + 2)):
                d = math.sqrt((x - bx)**2 + (y - by)**2)
                if d <= br:
                    col = AZURE_SHINE if (x <= bx and y <= by) else AZURE_LIGHT
                    curio_img.putpixel((x, y), tuple(col.astype(int)) + (220,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    深淵耐壓鍍鈦合金底盤 (chassis_walrus_icebreaker_alloy_default)
    2.2 head-body ratio chibi walrus chassis:
    - Stamped titanium alloy body: Ivory white (#FFFDF8) and Azure blue (#38A0FF).
    - Polished ivory ceramic belly plate (#FFFDF8 / #E8ECF2) with rivets.
    - Thick rounded flippers in azure blue with black rubber traction pads.
    - Ground shadow at bottom (y: 114..120).
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    STRICT 0-ART18: Bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    chd.ellipse([64 - 28, 114 - 3, 64 + 28, 114 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 114 - 2, 64 + 18, 114 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.0))

    # 2. Lower Body Flippers / Feet (y: 96..114)
    # Left flipper centered around (50, 106)
    # Right flipper centered around (74, 106)
    for fx, fy in [(50.0, 106.0), (74.0, 106.0)]:
        for y in range(int(fy - 9), int(fy + 8)):
            for x in range(int(fx - 10), int(fx + 11)):
                if x >= 94:
                    continue
                dx = (x - fx) / 9.5
                dy = (y - fy) / 6.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.7 * dy
                    if y >= fy + 4:  # Black rubber traction pad sole
                        col = np.array([45, 42, 58]) + dot * 10.0
                    else:  # Azure blue flipper metal
                        if dot > 0.4:
                            col = AZURE_LIGHT + dot * 15.0
                        elif dot > -0.1:
                            col = AZURE_BASE + dot * 25.0
                        else:
                            col = AZURE_SHADE + dot * 20.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Main Torso Titanium Shell (x: 43..87, y: 55..96)
    tcx, tcy = 64.0, 76.0
    for y in range(55, 97):
        for x in range(43, 88):
            if x >= 94:
                continue
            dx = (x - tcx) / 20.5
            dy = (y - tcy) / 20.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, -0.6 * dx - 0.7 * dy + 0.4 * nz - 0.55) / 0.45

                if dot > 0.45:
                    col = AZURE_LIGHT + spec * 25.0
                elif dot > 0.05:
                    col = AZURE_BASE + (dot - 0.05) * 35.0
                elif dot > -0.35:
                    col = AZURE_SHADE + (dot + 0.35) * 25.0
                else:
                    col = AZURE_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Polished Ivory Ceramic Belly Plate (x: 50..78, y: 61..93)
    bcx, bcy = 64.0, 77.0
    for y in range(61, 94):
        for x in range(50, 79):
            if x >= 94:
                continue
            bdx = (x - bcx) / 13.5
            bdy = (y - bcy) / 15.0
            bdsq = bdx**2 + bdy**2
            if bdsq <= 1.0:
                bnz = math.sqrt(max(0.0, 1.0 - bdsq))
                bdot = -0.55 * bdx - 0.70 * bdy + 0.45 * bnz
                shine = max(0.0, 1.0 - ((x - (bcx - 3))**2 + (y - (bcy - 4))**2)**0.5 / 4.5)**2

                if bdot > 0.55:
                    col = IVORY_LIGHT + shine * 15.0
                elif bdot > 0.15:
                    col = IVORY_BASE + (bdot - 0.15) * 20.0
                elif bdot > -0.25:
                    col = IVORY_SHADE + (bdot + 0.25) * 15.0
                else:
                    col = IVORY_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Belly plate brass rivets and horizontal segment seam
    for ry in [68, 77, 86]:
        for rx in [53, 75]:
            chassis_img.putpixel((rx, ry), tuple(GOLD_LIGHT.astype(int)) + (255,))
            chassis_img.putpixel((rx + 1, ry), tuple(GOLD_DARK.astype(int)) + (255,))

    # 5. Left front flipper (resting on chest defensively at x: 38..52, y: 68..86)
    flx, fly = 44.0, 76.0
    for y in range(68, 87):
        for x in range(37, 53):
            dx = (x - flx) / 7.0
            dy = (y - fly) / 8.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = AZURE_LIGHT if dot > 0.3 else (AZURE_BASE if dot > -0.2 else AZURE_SHADE)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 6. Right arm shoulder joint and upper neck transition (x: 77..88, y: 55..83, under x < 94)
    for y in range(55, 68):
        for x in range(80, 86):
            if x < 94:
                col = AZURE_BASE if (x - 80) < (y - 55) else AZURE_SHADE
                chassis_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    for y in range(68, 83):
        for x in range(77, 89):
            if x < 94:
                dx = (x - 83.0) / 5.5
                dy = (y - 75.0) / 6.5
                if dx**2 + dy**2 <= 1.0:
                    col = AZURE_BASE if dy < 0 else AZURE_SHADE
                    chassis_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    return apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=[(94, 0, 127, 127)])


def build_head_unit() -> Image.Image:
    """
    SLICE 4: HEAD UNIT (z=20)
    雙聯鎢鋼破冰長牙面罩 (head_walrus_tungsten_tusk_cowl)
    - Stamped titanium bathysphere cowl head: Ivory white (#FFFDF8) and Azure blue (#38A0FF).
    - Dual cold-rolled tungsten icebreaker chisel tusks (#FFD028 / #FFA010) extending downwards.
    - 8 flexible brass sonar sensor wire whiskers (#FFD028).
    - STRICT 0-ART27: Eye sockets (left x: 50..58, y: 38..46; right x: 70..78, y: 38..46) MUST BE 100% HOLLOW (alpha=0)!
    - STRICT 0-ART28q: Average plate color distance with chassis MUST BE < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Main Dome Head (x: 42..86, y: 22..58)
    for y in range(22, 59):
        for x in range(42, 87):
            dx = (x - hcx) / 20.5
            dy = (y - hcy) / 17.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz
                spec = max(0.0, -0.6 * dx - 0.7 * dy + 0.4 * nz - 0.55) / 0.45

                # Upper head & sides: Azure blue plates; Lower snout: Ivory ceramic
                if y < 50 or (abs(x - hcx) > 9.0 and y < 56):
                    if dot > 0.45:
                        col = AZURE_LIGHT + spec * 25.0
                    elif dot > 0.05:
                        col = AZURE_BASE + (dot - 0.05) * 35.0
                    elif dot > -0.35:
                        col = AZURE_SHADE + (dot + 0.35) * 25.0
                    else:
                        col = AZURE_DARK
                else:
                    if dot > 0.45:
                        col = IVORY_LIGHT + spec * 20.0
                    elif dot > 0.05:
                        col = IVORY_BASE + (dot - 0.05) * 25.0
                    elif dot > -0.35:
                        col = IVORY_SHADE + (dot + 0.35) * 20.0
                    else:
                        col = IVORY_DARK
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Bathysphere forehead dome rim & decorative rivets
    for rx in range(48, 81, 6):
        head_img.putpixel((rx, 26), tuple(GOLD_LIGHT.astype(int)) + (255,))
        head_img.putpixel((rx, 27), tuple(GOLD_DARK.astype(int)) + (255,))

    # 2. Snout / Muzzle Bulb (x: 52..76, y: 46..57)
    for y in range(46, 58):
        for x in range(52, 77):
            dx = (x - hcx) / 11.5
            dy = (y - 51.5) / 5.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = IVORY_LIGHT if dot > 0.3 else (IVORY_BASE if dot > -0.2 else IVORY_SHADE)
                head_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # Snout central nose seam
    for y in range(48, 54):
        head_img.putpixel((64, y), tuple(np.array([45, 40, 65])) + (255,))

    # 3. Dual Forged Tungsten Icebreaker Chisels (Tusks)
    # Left Tusk: root at (53..57, 52), extending down to (49..53, 84)
    # Right Tusk: root at (71..75, 52), extending down to (75..79, 84)
    for tx_root, tx_tip, tdir in [(55.0, 50.0, -1), (73.0, 78.0, 1)]:
        for y in range(52, 85):
            prog = (y - 52.0) / 32.0  # 0.0 to 1.0
            cur_cx = tx_root + prog * (tx_tip - tx_root)
            half_w = (1.0 - prog * 0.65) * 2.8  # tapering down to 1.0 px
            for x in range(int(cur_cx - half_w - 0.5), int(cur_cx + half_w + 1.5)):
                dx = (x - cur_cx) / max(0.8, half_w)
                if abs(dx) <= 1.0:
                    # Engraved depth rings every 8 pixels
                    if int(y) in [58, 66, 74]:
                        col = ORANGE_BASE if dx < 0 else ORANGE_DARK
                    else:
                        dot = -0.7 * dx
                        if dot > 0.3:
                            col = GOLD_SHINE
                        elif dot > -0.2:
                            col = GOLD_BASE + dot * 25.0
                        else:
                            col = GOLD_DARK
                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Tusk socket collars (brass rings at tusk base)
    for y in [52, 53]:
        for x in range(52, 58):
            head_img.putpixel((x, y), tuple(GOLD_LIGHT.astype(int)) + (255,))
        for x in range(70, 76):
            head_img.putpixel((x, y), tuple(GOLD_LIGHT.astype(int)) + (255,))

    # 4. Eight Flexible Brass Sonar Whiskers
    # Left whiskers (4 curving out towards left)
    l_whiskers = [
        [(52, 51), (46, 50), (38, 52)],
        [(52, 53), (45, 54), (37, 58)],
        [(53, 55), (46, 58), (39, 64)],
        [(54, 56), (48, 62), (42, 68)]
    ]
    for pts in l_whiskers:
        hd.line(pts, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        tip = pts[-1]
        hd.ellipse([tip[0] - 1, tip[1] - 1, tip[0] + 1, tip[1] + 1], fill=tuple(GOLD_LIGHT.astype(int)) + (255,))

    # Right whiskers (4 curving out towards right)
    r_whiskers = [
        [(76, 51), (82, 50), (90, 52)],
        [(76, 53), (83, 54), (91, 58)],
        [(75, 55), (82, 58), (89, 64)],
        [(74, 56), (80, 62), (86, 68)]
    ]
    for pts in r_whiskers:
        hd.line(pts, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
        tip = pts[-1]
        hd.ellipse([tip[0] - 1, tip[1] - 1, tip[0] + 1, tip[1] + 1], fill=tuple(GOLD_LIGHT.astype(int)) + (255,))

    # 5. STRICT 0-ART27: Hollow Eye Sockets (left: x 50..58, y 38..46; right: x 70..78, y 38..46)
    # Clear socket regions completely to alpha=0!
    for y in range(38, 47):
        for x in range(50, 59):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(70, 79):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    # Apply outline with eye socket regions ignored so outline won't fill sockets!
    ignore_eye_sockets = [(50, 38, 58, 46), (70, 38, 78, 46)]
    return apply_antialiased_outline(head_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=ignore_eye_sockets)


def build_costume() -> Image.Image:
    """
    SLICE 5: COSTUME (z=25)
    深淵領航雙排扣水手胸甲 (costume_walrus_abyssal_peacoat_cuirass)
    - Double-breasted sailor peacoat cuirass in Azure blue (#38A0FF).
    - Sunset orange (#FFA010) lapel collar trimming around neck.
    - 6 embossed brass anchor buttons (#FFD028).
    - Waist belt with golden buckle (y: 90..94).
    STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS (lower chassis completely decoupled)!
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    cx, cy = 64.0, 75.0

    # 1. Peacoat Cuirass Body (x: 46..84, y: 56..95)
    for y in range(56, 96):
        for x in range(46, 85):
            dx = (x - cx) / 17.5
            dy = (y - cy) / 18.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.4:
                    col = AZURE_LIGHT
                elif dot > 0.0:
                    col = AZURE_BASE + dot * 25.0
                elif dot > -0.35:
                    col = AZURE_SHADE + (dot + 0.35) * 20.0
                else:
                    col = AZURE_DARK
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Sunset Orange Lapel Collar Trimming (y: 56..68)
    # Left lapel: (48, 56) -> (58, 66) -> (50, 68)
    left_lapel = [(47, 56), (56, 56), (60, 65), (52, 68), (47, 62)]
    cd.polygon(left_lapel, fill=tuple(ORANGE_BASE.astype(int)) + (255,))
    cd.line([(47, 56), (60, 65)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=1)

    # Right lapel: (80, 56) -> (70, 66) -> (78, 68)
    right_lapel = [(81, 56), (72, 56), (68, 65), (76, 68), (81, 62)]
    cd.polygon(right_lapel, fill=tuple(ORANGE_BASE.astype(int)) + (255,))
    cd.line([(81, 56), (68, 65)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=1)

    # Inner neck v-opening (showing ivory white shirt at y: 56..64, x: 60..68)
    for y in range(56, 65):
        w_v = max(0, 4 - (y - 56) // 2)
        for x in range(64 - w_v, 64 + w_v + 1):
            costume_img.putpixel((x, y), tuple(IVORY_LIGHT.astype(int)) + (255,))

    # 3. Six Embossed Brass Anchor Buttons (#FFD028)
    # Symmetric 2x3 grid
    buttons = [
        (56, 71), (72, 71),
        (56, 79), (72, 79),
        (57, 87), (71, 87)
    ]
    for bx, by in buttons:
        for y in range(by - 2, by + 3):
            for x in range(bx - 2, bx + 3):
                if (x - bx)**2 + (y - by)**2 <= 4.0:
                    col = GOLD_SHINE if (x <= bx and y <= by) else GOLD_DARK
                    costume_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # 4. Waist Belt with Gold Buckle (y: 90..95)
    for y in range(90, 96):
        for x in range(48, 82):
            if y < 96:
                costume_img.putpixel((x, y), tuple(np.array([45, 42, 60])) + (255,))
    # Gold buckle at center (x: 60..68, y: 90..95)
    for y in range(90, 96):
        for x in range(60, 69):
            if y < 96:
                if x in [60, 68] or y in [90, 95]:
                    costume_img.putpixel((x, y), tuple(GOLD_LIGHT.astype(int)) + (255,))
                else:
                    costume_img.putpixel((x, y), tuple(GOLD_DARK.astype(int)) + (255,))

    # STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS
    return apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=[(0, 96, 127, 127)])


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=30)
    雙聯耐壓石英泡罩目鏡 (face_walrus_quartz_dome_eyes)
    - Left eye centered at (54, 42), radius ~4.5
    - Right eye centered at (74, 42), radius ~4.5
    - Deep indigo violet frame (#1F1A3A), glowing Mint Green (#4ED86A) and Cyan (#38A0FF) quartz lens,
      and concentric pressure gauge markings with white specular highlight.
    STRICT 0-ART27: Solid pixels at eye centers (alpha >= 200).
    """
    optic_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    centers = [(54.0, 42.0), (74.0, 42.0)]
    for ecx, ecy in centers:
        # Outer indigo violet metal frame (radius 5.5)
        for y in range(int(ecy - 6), int(ecy + 7)):
            for x in range(int(ecx - 6), int(ecx + 7)):
                d = math.sqrt((x - ecx)**2 + (y - ecy)**2)
                if 4.2 <= d <= 5.8:
                    col = OUTLINE if d > 5.0 else np.array([55, 48, 85])
                    optic_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

        # Inner Quartz Lens with gradient (radius <= 4.2)
        for y in range(int(ecy - 4), int(ecy + 5)):
            for x in range(int(ecx - 4), int(ecx + 5)):
                d = math.sqrt((x - ecx)**2 + (y - ecy)**2)
                if d <= 4.2:
                    dot = -0.6 * (x - ecx) / 4.2 - 0.7 * (y - ecy) / 4.2
                    if dot > 0.4:
                        col = MINT_SHINE
                    elif dot > 0.0:
                        col = MINT_LIGHT + dot * 25.0
                    elif dot > -0.3:
                        col = MINT_BASE + dot * 20.0
                    else:
                        col = AZURE_BASE
                    optic_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Specular glint on upper-left of lens (white highlight)
        optic_img.putpixel((int(ecx - 2), int(ecy - 2)), tuple(WHITE_SHINE.astype(int)) + (255,))
        optic_img.putpixel((int(ecx - 1), int(ecy - 2)), tuple(WHITE_SHINE.astype(int)) + (255,))

        # Concentric dial dot in lower-right
        optic_img.putpixel((int(ecx + 1), int(ecy + 1)), tuple(GOLD_LIGHT.astype(int)) + (255,))

    return apply_antialiased_outline(optic_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    深淵破冰海軍短闊劍 (weapon_walrus_abyssal_icebreaker_cutlass)
    Single-wield naval boarding cutlass:
    - Held in right hand at x: 80..116, y: 40..106.
    - Cold-rolled steel blade (#STEEL_BASE/#STEEL_LIGHT) with saw-toothed icebreaker notches on spine.
    - Stamped hemispherical brass cup-hilt guard (#FFD028 / #FFA010) at (86, 80).
    - Grip and pommel with anchor ring (88, 88).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Cutlass Blade: extends from hilt at (88, 76) up to tip at (104, 42)
    # Blade is curved slightly backwards (towards right)
    blade_poly = [
        (87, 76), (92, 75),  # hilt base
        (97, 62), (103, 50), (106, 42),  # curved spine (back)
        (104, 42), (99, 48), (93, 58), (89, 68), (85, 76)  # cutting edge (front)
    ]
    wd.polygon(blade_poly, fill=tuple(STEEL_BASE.astype(int)) + (255,))

    # Saw-tooth icebreaker notches on spine
    notches = [(98, 60), (101, 54), (104, 47)]
    for nx, ny in notches:
        wd.line([(nx, ny), (nx + 2, ny - 1)], fill=tuple(STEEL_SHINE.astype(int)) + (255,), width=1)

    # Polished fuller and cutting edge highlight
    edge_pts = [(86, 76), (90, 68), (94, 58), (100, 48), (105, 42)]
    wd.line(edge_pts, fill=tuple(STEEL_SHINE.astype(int)) + (255,), width=1)

    # Shading on blade
    for t in np.linspace(0.0, 1.0, 40):
        bx = 89.0 + t * (104.0 - 89.0)
        by = 75.0 + t * (43.0 - 75.0)
        for d in [-1, 0, 1]:
            px, py = int(bx + d), int(by)
            if weapon_img.getpixel((px, py))[3] > 0:
                col = STEEL_LIGHT if d < 0 else STEEL_SHADE
                weapon_img.putpixel((px, py), tuple(col.astype(int)) + (255,))

    # 2. Hemispherical Brass Cup-Hilt Guard (centered at 88, 77, radius 7.5)
    for y in range(71, 85):
        for x in range(81, 96):
            dx = (x - 88.0) / 7.0
            dy = (y - 77.5) / 6.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.7 * dy
                if dot > 0.4:
                    col = GOLD_SHINE
                elif dot > -0.1:
                    col = GOLD_BASE + dot * 25.0
                elif dot > -0.4:
                    col = ORANGE_BASE
                else:
                    col = GOLD_DARK
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Cup-hilt compass rose engraving
    wd.line([(88, 74), (88, 81)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    wd.line([(84, 78), (92, 78)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)

    # 3. Grip handle (y: 80..89, x: 86..91)
    for y in range(80, 90):
        for x in range(86, 91):
            col = np.array([45, 42, 60]) if y % 2 == 0 else GOLD_BASE
            weapon_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # 4. Pommel with Anchor Ring (y: 89..95, x: 86..91)
    wd.ellipse([86, 90, 91, 95], outline=tuple(GOLD_LIGHT.astype(int)) + (255,))
    wd.point((88, 92), fill=tuple(GOLD_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第六十二族 破冰海象 (walrus) ===")

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
        ("winding_key", "key_walrus_anchor_handwheel_brass", key_img),
        ("back_curio", "curio_walrus_dual_ballast_tanks", curio_img),
        ("chassis", "chassis_walrus_icebreaker_alloy_default", chassis_img),
        ("head_unit", "head_walrus_tungsten_tusk_cowl", head_img),
        ("costume", "costume_walrus_abyssal_peacoat_cuirass", costume_img),
        ("optic_core", "face_walrus_quartz_dome_eyes", core_img),
        ("weapon", "weapon_walrus_abyssal_icebreaker_cutlass", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{WALRUS_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_walrus_anchor_handwheel_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_walrus_abyssal_icebreaker_cutlass.png")
    print("  ✓ Universal key and weapon copies updated")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{WALRUS_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{WALRUS_PD_DIR}/proof_paperdoll_walrus_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{WALRUS_PD_DIR}/proof_paperdoll_walrus_magenta.png"
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

    strip_path = f"{WALRUS_PD_DIR}/proof_walrus_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/walrus_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/walrus_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/walrus_idle.png
    p_idle_64 = f"{PLAYER_DIR}/walrus_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/walrus_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/walrus_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/walrus_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/walrus_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/walrus_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)


if __name__ == "__main__":
    build_all()
