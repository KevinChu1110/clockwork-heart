#!/usr/bin/env python3
"""
build_donkey_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十九族 闢道頑驢 (The Sapper Donkey, donkey) 7 Paperdoll Slices.

Follows:
- docs/world/SAPPER_DONKEY_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, stamped cold-rolled tinplate chassis #FFFDF8,
  dual ratchet folding ears cowl #FFA010,
  dual high-clarity slate quartz goggles #38A0FF / #FFD028,
  sapper riveted brass-reinforced lacquer cuirass with inspection sashes #4ED86A / #38A0FF / #FF5E8A,
  dual cograil timber pack and segmented counterweight balance tail #FFD028 / #FF5E8A,
  dawn three-leaf clover carved brass winding key with coral pink center rivet #FFD028 / #FF5E8A,
  bazaar cograil clearing axe with shock-absorbing ratchet #FFD028 / steel dual blades)
- references/art_direction.md & references/brand_assets.md
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34, 0-QA39
- High-depth multi-tone cel-shading (>= 3 steps per slot, metal highlights & shadow bevels)
- Subpixel anti-aliased silhouette borders (alpha levels > 2)
- chassis 128 unique colors >= 74, all 7 slots c/100px >= 3.0%
- proof composite unique colors >= 300, core holes <= 0px, head vs chassis color L2 < 60.0
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DONKEY_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/donkey"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Sapper Donkey Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Ivory Porcelain & Cold-rolled Tinplate (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)   # #FFFDF8
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)
IVORY_DEEP   = np.array([140, 132, 120], dtype=float)

# 2. Sunset Warm Orange (#FFA010) - Cowl & Folding Ears
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)    # #FFA010
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 3. Forged Brass & Dawn Gold (#FFD028) - Winding Key, Gears, Tail Counterweight
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)     # #FFD028
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 4. Mint Green Inspection Ribbon (#4ED86A) - Harness Accent
MINT_SHINE = np.array([195, 255, 215], dtype=float)
MINT_LIGHT = np.array([135, 242, 165], dtype=float)
MINT_BASE  = np.array([78, 216, 106], dtype=float)     # #4ED86A
MINT_DARK  = np.array([42, 160, 68], dtype=float)
MINT_DEEP  = np.array([22, 105, 42], dtype=float)

# 5. Sky Blue Goggles & Sapper Sashes (#38A0FF)
SKY_SHINE  = np.array([210, 240, 255], dtype=float)
SKY_LIGHT  = np.array([130, 205, 255], dtype=float)
SKY_BASE   = np.array([56, 160, 255], dtype=float)      # #38A0FF
SKY_SHADOW = np.array([32, 115, 210], dtype=float)
SKY_DARK   = np.array([20, 75, 160], dtype=float)

# 6. Coral Pink Rivet & Rubber Seals (#FF5E8A)
PINK_SHINE = np.array([255, 210, 230], dtype=float)
PINK_LIGHT = np.array([255, 150, 182], dtype=float)
PINK_BASE  = np.array([255, 94, 138], dtype=float)     # #FF5E8A
PINK_DARK  = np.array([195, 55, 95], dtype=float)

# 7. Walnut Timber for Pack & Axe Shaft
WALNUT_LIGHT = np.array([165, 125, 90], dtype=float)
WALNUT_BASE  = np.array([120, 85, 55], dtype=float)
WALNUT_DARK  = np.array([80, 50, 30], dtype=float)
WALNUT_DEEP  = np.array([55, 32, 18], dtype=float)

# 8. High-Carbon Sapper Steel (Axe Blades & Joint Pins)
STEEL_SHINE = np.array([245, 250, 255], dtype=float)
STEEL_LIGHT = np.array([200, 215, 235], dtype=float)
STEEL_BASE  = np.array([145, 165, 190], dtype=float)
STEEL_DARK  = np.array([95, 110, 130], dtype=float)
STEEL_DEEP  = np.array([55, 65, 80], dtype=float)

# 9. Industrial Rubber & Joint Seals
RUBBER_LIGHT = np.array([72, 68, 86], dtype=float)
RUBBER_BASE  = np.array([48, 44, 58], dtype=float)
RUBBER_DARK  = np.array([28, 24, 36], dtype=float)

WHITE_SHINE = np.array([255, 255, 255], dtype=float)


def apply_antialiased_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=50, ignore_regions=None) -> Image.Image:
    """
    Applies a clean 1px dark outline with smooth anti-aliasing on outer boundaries.
    Guarantees subpixel anti-aliasing and zero blocky halo.
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
                        if r[0] <= x <= r[2] and r[1] <= y <= r[3]:
                            skip = True
                            break
                    elif len(r) == 3:
                        if (x - r[0])**2 + (y - r[1])**2 <= r[2]**2:
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
                strength = min(1.0, cnt_4 * 0.35 + cnt_diag * 0.18)
                outline_alpha[y, x] = max(outline_alpha[y, x], strength * 255.0)
                outline_rgb[y, x] = outline_color

    res_arr = arr.copy().astype(float)
    out_mask = (outline_alpha > 10) & (~opaque_mask)
    res_arr[out_mask, :3] = outline_rgb[out_mask]
    res_arr[out_mask, 3] = outline_alpha[out_mask]

    return Image.fromarray(np.clip(res_arr, 0, 255).astype(np.uint8))


def build_winding_key() -> Image.Image:
    """
    Winding Key: key_donkey_dawn_clover_brass
    Dawn Three-Leaf Clover Carved Brass Winding Key with Center Coral Pink Rivet.
    Positioned at back spine (x: 52..76, y: 44..70).
    Follows 0-ART29: Warm bronze outline, strictly 0 dark box pixels.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Drive Shaft from spine socket (64, 66) up to center pivot (64, 46)
    for y in range(46, 68):
        t = (y - 46) / 22.0
        width = 3.2
        for x in range(int(round(64 - width)), int(round(64 + width + 1))):
            dx = (x - 64.0) / width
            dot = -0.5 * dx
            if dot > 0.2:
                col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
            elif dot > -0.2:
                col = GOLD_BASE
            else:
                col = GOLD_DARK
            key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Three-leaf Clover filigree rings centered at (64, 46)
    # Leaf 1: Top (64, 34), radius 8
    # Leaf 2: Bottom-Left (52, 48), radius 7
    # Leaf 3: Bottom-Right (76, 48), radius 7
    leaves = [
        (64.0, 34.0, 8.0, 4.2),
        (52.0, 48.0, 7.5, 3.8),
        (76.0, 48.0, 7.5, 3.8),
    ]

    for cx, cy, r_out, r_in in leaves:
        for y in range(int(cy - r_out - 1), int(cy + r_out + 2)):
            for x in range(int(cx - r_out - 1), int(cx + r_out + 2)):
                if 0 <= x < W and 0 <= y < H:
                    dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                    if r_in <= dist <= r_out:
                        # Angle for baroque bevel lighting
                        angle = math.atan2(y - cy, x - cx)
                        dot = -math.cos(angle - 0.7)
                        if dot > 0.35:
                            col = GOLD_SHINE * 0.5 + GOLD_LIGHT * 0.5 + dot * 15.0
                        elif dot > -0.2:
                            col = GOLD_BASE + dot * 20.0
                        else:
                            col = GOLD_DARK + (dot + 0.3) * 15.0
                        key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Center Gear Hub (64, 46) radius 6.5
    for y in range(39, 54):
        for x in range(57, 72):
            dist = math.sqrt((x - 64.0)**2 + (y - 46.0)**2)
            if dist <= 6.5:
                dot = -(x - 64.0) * 0.1 - (y - 46.0) * 0.1
                if dist <= 3.2:
                    # Coral pink center damping rivet (#FF5E8A)
                    if dist <= 1.2:
                        col = PINK_SHINE
                    elif dot > 0.1:
                        col = PINK_LIGHT
                    else:
                        col = PINK_BASE
                else:
                    if dot > 0.2:
                        col = GOLD_LIGHT
                    else:
                        col = GOLD_DARK
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Apply specialized warm golden outline to prevent dark block artifact (0-ART29)
    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=60)


def build_back_curio() -> Image.Image:
    """
    Back Curio: curio_donkey_cograil_pack_tail
    Dual Cograil Timber Pack & Segmented Counterweight Balance Tail.
    Features:
    - Left & right walnut timber pack brackets with spare cogwheel and railroad ties (x: 34..46, y: 56..76)
    - Three-segment brass counterweight balance tail swinging from (48, 80) down to (36, 108) with brass pendulum hammer.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Left Timber Pack & Railway Sleepers (x: 34..46, y: 56..76)
    for y in range(56, 76):
        for x in range(34, 46):
            # Two horizontal timber beams with brass corner brackets
            is_bracket = (x in (34, 35, 44, 45) and y in (56, 57, 65, 66, 74, 75))
            if is_bracket:
                col = GOLD_BASE if (x + y) % 2 == 0 else GOLD_LIGHT
            elif y in (58, 59, 60, 61, 62):
                # Upper wooden beam
                dx = (x - 40.0) / 6.0
                col = WALNUT_LIGHT if dx < 0 else WALNUT_BASE
            elif y in (67, 68, 69, 70, 71):
                # Lower wooden beam
                dx = (x - 40.0) / 6.0
                col = WALNUT_BASE if dx < 0 else WALNUT_DARK
            elif 37 <= x <= 43 and 61 <= y <= 67:
                # Spare brass cogwheel poking out
                dist = math.sqrt((x - 40.0)**2 + (y - 64.0)**2)
                if dist <= 3.2:
                    col = GOLD_LIGHT if x < 40 else GOLD_DARK
                else:
                    continue
            else:
                continue
            curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right side timber rail tip peaking at (83..89, 58..72)
    for y in range(58, 72):
        for x in range(83, 90):
            if y in (60, 61, 62, 69, 70, 71) and x <= 88:
                col = WALNUT_BASE if y < 65 else WALNUT_DARK
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Segmented Brass Balance Tail
    # Origin at spine lower hitch (48, 80) -> link 1 (44, 88) -> link 2 (40, 96) -> hammer (36, 106)
    tail_pts = [(48.0, 80.0), (45.0, 87.0), (41.0, 95.0), (37.0, 104.0)]
    for i in range(len(tail_pts) - 1):
        x1, y1 = tail_pts[i]
        x2, y2 = tail_pts[i + 1]
        steps = 14
        for s in range(steps + 1):
            t = s / float(steps)
            cx = x1 * (1.0 - t) + x2 * t
            cy = y1 * (1.0 - t) + y2 * t
            w_seg = 2.4 - t * 0.4
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx**2 + dy**2 <= w_seg**2:
                        col = GOLD_LIGHT if dx < 0 else GOLD_DARK
                        curio_img.putpixel((int(round(cx + dx)), int(round(cy + dy))), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Brass Pendulum Hammer at (37, 105), radius 5.5
    for y in range(99, 112):
        for x in range(31, 44):
            dist = math.sqrt((x - 37.0)**2 + (y - 105.0)**2)
            if dist <= 5.5:
                dot = -(x - 37.0) * 0.15 - (y - 105.0) * 0.15
                if dist <= 2.2:
                    col = PINK_BASE if dot < 0 else PINK_LIGHT
                elif dot > 0.25:
                    col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                elif dot > -0.2:
                    col = GOLD_BASE
                else:
                    col = GOLD_DARK
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    Chassis: chassis_donkey_tinplate_default
    2.2 Chibi Stamped Cold-rolled Tinplate (#FFFDF8) body with multi-tone depth.
    Features:
    - 0-ART9/11: Strictly 0 pixels at x >= 94.
    - 0-ART18: Bare torso (y: 58..94, x: 44..84) rich multi-tone cel-shading (unique colors >= 20).
    - 0-ART28q: Color coherence with head_unit (L2 distance < 60.0).
    - Rounded chibi legs (y: 92..116) with heavy anti-slip black rubber hooves.
    - Left arm resting, right arm positioned at x: 74..92 ready to hold axe.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 0. Neck / Shoulder Transition Block to seal core against holes (x: 45..83, y: 53..60)
    for y in range(53, 61):
        for x in range(46, 83):
            dot = -(x - 64.0) * 0.05 - (y - 57.0) * 0.08
            col = IVORY_BASE + dot * 15.0
            chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 1. Main Torso Barrel (x: 45..83, y: 56..92)
    tcx, tcy = 64.0, 74.0
    rx, ry = 18.5, 17.0
    for y in range(56, 93):
        for x in range(45, 84):
            dx = (x - tcx) / rx
            dy = (y - tcy) / ry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                nx = dx
                ny = dy
                nz = math.sqrt(max(0.0, 1.0 - dist_sq))
                # Light from upper-left (-0.5, -0.6, 0.6)
                dot = -0.5 * nx - 0.6 * ny + 0.6 * nz

                if dot > 0.65:
                    col = IVORY_SHINE * 0.35 + IVORY_LIGHT * 0.65 + dot * 12.0
                elif dot > 0.35:
                    col = IVORY_LIGHT + dot * 15.0
                elif dot > 0.05:
                    col = IVORY_BASE + dot * 18.0
                elif dot > -0.25:
                    col = IVORY_SHADOW + (dot + 0.25) * 16.0
                elif dot > -0.55:
                    col = IVORY_DARK + (dot + 0.55) * 14.0
                else:
                    col = IVORY_DEEP + (dot + 0.8) * 12.0

                # Subtle mechanical seams
                if abs(dx) < 0.06 or (y == 74 and abs(dx) < 0.75):
                    col = col * 0.9 + RUBBER_BASE * 0.1

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Pelvis / Lower Abdomen (x: 48..80, y: 86..94)
    for y in range(86, 95):
        for x in range(48, 81):
            dx = (x - 64.0) / 16.0
            if abs(dx) <= 1.0:
                col = IVORY_SHADOW if abs(dx) < 0.5 else IVORY_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Chibi Legs (Left: x: 48..60, y: 92..116; Right: x: 68..80, y: 92..116)
    legs = [
        (54.0, 48, 60),  # Left leg
        (74.0, 68, 80),  # Right leg
    ]
    for lcx, lx1, lx2 in legs:
        for y in range(92, 117):
            t = (y - 92) / 24.0
            half_w = 5.2 + t * 0.6
            for x in range(lx1, lx2 + 1):
                dx = (x - lcx) / half_w
                if abs(dx) <= 1.0:
                    dot = -0.6 * dx - 0.4 * t
                    if y >= 110:
                        # Black rubber hoof pad
                        if dot > 0.3:
                            col = RUBBER_LIGHT
                        elif dot > -0.2:
                            col = RUBBER_BASE
                        else:
                            col = RUBBER_DARK
                    else:
                        # Stamped tinplate leg armor
                        if dot > 0.4:
                            col = IVORY_LIGHT
                        elif dot > 0.0:
                            col = IVORY_BASE
                        elif dot > -0.4:
                            col = IVORY_SHADOW
                        else:
                            col = IVORY_DARK
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Arms
    # Left Arm (x: 36..48, y: 60..84): resting downward with brass elbow ball joint
    for y in range(60, 84):
        t = (y - 60) / 24.0
        acx = 45.0 - t * 4.0
        for x in range(int(round(acx - 4.5)), int(round(acx + 4.5))):
            dx = (x - acx) / 4.5
            if abs(dx) <= 1.0:
                dot = -0.6 * dx - 0.4 * t
                if 68 <= y <= 72:
                    # Brass elbow joint
                    col = GOLD_LIGHT if dot > 0 else GOLD_DARK
                elif y >= 80:
                    # Hand clamp
                    col = RUBBER_LIGHT if dot > 0 else RUBBER_BASE
                else:
                    col = IVORY_BASE if dot > 0 else IVORY_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Arm (x: 74..93, y: 60..82): holding axe handle forward
    # Strict boundary: x must NOT exceed 93 (0-ART9/11)
    for y in range(60, 83):
        t = (y - 60) / 22.0
        acx = 76.0 + t * 11.0
        for x in range(int(round(acx - 4.2)), min(94, int(round(acx + 4.2)))):
            dx = (x - acx) / 4.2
            if abs(dx) <= 1.0:
                dot = -0.5 * dx - 0.4 * t
                if 68 <= y <= 72:
                    col = GOLD_LIGHT if dot > 0 else GOLD_DARK
                elif y >= 78:
                    col = RUBBER_LIGHT if dot > 0 else RUBBER_BASE
                else:
                    col = IVORY_BASE if dot > 0 else IVORY_SHADOW
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50)


def build_head_unit() -> Image.Image:
    """
    Head Unit: head_donkey_ratchet_ears_cowl
    Rounded Cowl with Dual Ratchet Folding Long Ears.
    Features:
    - 0-ART27: Hollow eye sockets! Left socket (y: 41..44, x: 53..56) and
      Right socket (y: 41..44, x: 72..75) must have alpha == 0!
    - Stamped brass folding donkey ears poking upwards to y: 12..32.
    - Stamped muzzle and forehead gear crest with warm orange (#FFA010) and ivory (#FFFDF8).
    - 0-ART28q: Cowl plate L2 distance with chassis < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Dual Folding Long Ears (Left: 38..52, 12..34; Right: 76..90, 12..34)
    # Left Ear: from base (50, 32) up to tip (40, 12)
    for y in range(12, 34):
        t = (33 - y) / 21.0  # 0 at base, 1 at tip
        cx = 50.0 * (1.0 - t) + 39.0 * t
        half_w = 4.2 * (1.0 - t * 0.4) + 0.8
        for x in range(int(round(cx - half_w)), int(round(cx + half_w + 1))):
            dx = (x - cx) / max(0.5, half_w)
            if abs(dx) <= 1.0:
                dot = -0.6 * dx - 0.5 * t
                # Inner ear trough vs outer brass plate
                if abs(dx) < 0.45 and t < 0.85:
                    # Orange lacquer inner fold
                    col = ORANGE_LIGHT if dot > 0 else ORANGE_BASE
                else:
                    # Warm ivory/brass outer rim
                    col = IVORY_LIGHT if dot > 0.2 else (IVORY_BASE if dot > -0.2 else IVORY_DARK)
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Ear: from base (78, 32) up to tip (89, 12)
    for y in range(12, 34):
        t = (33 - y) / 21.0
        cx = 78.0 * (1.0 - t) + 89.0 * t
        half_w = 4.2 * (1.0 - t * 0.4) + 0.8
        for x in range(int(round(cx - half_w)), int(round(cx + half_w + 1))):
            dx = (x - cx) / max(0.5, half_w)
            if abs(dx) <= 1.0:
                dot = -0.6 * dx - 0.5 * t
                if abs(dx) < 0.45 and t < 0.85:
                    col = ORANGE_LIGHT if dot > 0 else ORANGE_BASE
                else:
                    col = IVORY_LIGHT if dot > 0.2 else (IVORY_BASE if dot > -0.2 else IVORY_DARK)
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Ear ratchet hinges at bases: (50, 32) and (78, 32)
    for hx in (50, 78):
        for y in range(30, 35):
            for x in range(hx - 3, hx + 4):
                if (x - hx)**2 + (y - 32.0)**2 <= 8.0:
                    col = GOLD_LIGHT if x < hx else GOLD_DARK
                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Main Head Dome Cowl (x: 44..84, y: 30..56)
    hcx, hcy = 64.0, 42.0
    hrx, hry = 19.0, 13.5
    for y in range(29, 56):
        for x in range(44, 85):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                nx = dx
                ny = dy
                nz = math.sqrt(max(0.0, 1.0 - dist_sq))
                dot = -0.55 * nx - 0.55 * ny + 0.6 * nz

                if y < 38:
                    # Forehead helmet plate in warm orange (#FFA010)
                    if dot > 0.4:
                        col = ORANGE_LIGHT
                    elif dot > 0.0:
                        col = ORANGE_BASE
                    else:
                        col = ORANGE_DARK
                else:
                    # Face cowl in ivory (#FFFDF8)
                    if dot > 0.5:
                        col = IVORY_SHINE * 0.4 + IVORY_LIGHT * 0.6
                    elif dot > 0.2:
                        col = IVORY_LIGHT
                    elif dot > -0.15:
                        col = IVORY_BASE
                    elif dot > -0.45:
                        col = IVORY_SHADOW
                    else:
                        col = IVORY_DARK

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Donkey Muzzle / Snout (x: 55..73, y: 46..55)
    for y in range(46, 56):
        for x in range(55, 74):
            dx = (x - 64.0) / 9.0
            dy = (y - 51.0) / 5.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.5 * dy
                if y >= 53:
                    # Snout tip / mouth plate
                    col = RUBBER_LIGHT if dot > 0 else RUBBER_BASE
                else:
                    col = IVORY_BASE if dot > 0.2 else (IVORY_SHADOW if dot > -0.2 else IVORY_DARK)
                # Twin nostril rivets
                if y == 52 and x in (61, 67):
                    col = RUBBER_DARK
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Forehead Cog Crest at (64, 34)
    for y in range(32, 37):
        for x in range(62, 67):
            if (x - 64)**2 + (y - 34)**2 <= 4.0:
                head_img.putpixel((x, y), tuple(GOLD_BASE.astype(int)) + (255,))

    # 4. HOLLOW EYE SOCKETS (0-ART27 MANDATE)
    # Strict requirement: left socket (y: 41..44, x: 53..56) and right socket (y: 41..44, x: 72..75) must be 100% alpha = 0
    for y in range(40, 46):
        for x in range(52, 58):
            head_img.putpixel((x, y), (0, 0, 0, 0))
    for y in range(40, 46):
        for x in range(71, 77):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    # Apply outline ignoring the hollow sockets
    hollow_ignore = [(52, 40, 57, 45), (71, 40, 76, 45)]
    return apply_antialiased_outline(head_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=hollow_ignore)


def build_optic_core() -> Image.Image:
    """
    Optic Core: face_donkey_slate_goggles
    Dual High-Clarity Slate Quartz Spherical Goggles.
    Features:
    - 0-ART27: Center pixels at (54, 42) and (74, 42) must have alpha > 200.
    - Deep blue-purple titanium bezel with vivid Sky Blue (#38A0FF) and Dawn Gold (#FFD028) reticle.
    - Crisp white catchlights for living toy gaze.
    """
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    eyes = [
        (54.5, 42.5),  # Left eye center
        (73.5, 42.5),  # Right eye center
    ]

    for ecx, ecy in eyes:
        for y in range(38, 48):
            for x in range(int(ecx - 5), int(ecx + 6)):
                dist = math.sqrt((x - ecx)**2 + (y - ecy)**2)
                if dist <= 4.6:
                    nx = (x - ecx) / 4.6
                    ny = (y - ecy) / 4.6
                    dot = -0.6 * nx - 0.6 * ny

                    if dist >= 3.6:
                        # Outer deep blue-purple titanium bezel
                        col = OUTLINE * 0.8 + SKY_DARK * 0.2
                    elif dist <= 1.4:
                        # Core reticle pupil / gold reticle crosshair
                        if abs(x - round(ecx)) <= 0.6 or abs(y - round(ecy)) <= 0.6:
                            col = GOLD_LIGHT
                        else:
                            col = SKY_LIGHT
                    else:
                        # High-transparency slate quartz lens
                        if dot > 0.4:
                            col = SKY_SHINE * 0.5 + SKY_LIGHT * 0.5
                        elif dot > 0.0:
                            col = SKY_BASE
                        else:
                            col = SKY_SHADOW

                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # White catchlights
        core_img.putpixel((int(round(ecx - 1.2)), int(round(ecy - 1.2))), tuple(WHITE_SHINE.astype(int)) + (255,))
        core_img.putpixel((int(round(ecx - 0.2)), int(round(ecy - 1.2))), tuple(WHITE_SHINE.astype(int)) + (255,))

    # Goggles bridge connecting the two lenses (x: 60..68, y: 42)
    for x in range(59, 69):
        for y in (42, 43):
            col = GOLD_DARK if y == 43 else GOLD_LIGHT
            core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_costume() -> Image.Image:
    """
    Costume: costume_donkey_sapper_harness
    Sapper Riveted Brass-Reinforced Lacquer Cuirass with Inspection Sashes.
    Features:
    - 0-ART26b: Strictly 0 pixels at y >= 96.
    - Mint Green (#4ED86A) and Sky Blue (#38A0FF) cross inspection sashes.
    - Polished brass gear pectoral medallion at (64, 68) with coral pink center (#FF5E8A).
    - Utility belt and buckle at y: 84..91.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Main Cuirass Plate (x: 48..80, y: 56..92)
    for y in range(56, 93):
        t = (y - 56) / 36.0
        half_w = 15.0 - t * 2.0
        for x in range(int(round(64 - half_w)), int(round(64 + half_w + 1))):
            dx = (x - 64.0) / half_w
            dot = -0.5 * dx - 0.5 * (t - 0.5)

            # Base heavy lacquer cuirass (deep metallic lacquer)
            if dot > 0.3:
                col = RUBBER_LIGHT
            elif dot > -0.2:
                col = RUBBER_BASE
            else:
                col = RUBBER_DARK

            # Cross Inspection Sashes:
            # Sash 1 (Mint Green): from top-left (50, 56) to bottom-right (76, 84)
            sash1_dist = abs((x - 50.0) * 0.73 - (y - 56.0) * 0.68)
            if sash1_dist <= 2.2:
                col = MINT_SHINE if dot > 0.2 else (MINT_BASE if dot > -0.2 else MINT_DARK)

            # Sash 2 (Sky Blue): from top-right (78, 56) to bottom-left (52, 84)
            sash2_dist = abs((x - 78.0) * -0.73 - (y - 56.0) * 0.68)
            if sash2_dist <= 2.2:
                col = SKY_SHINE if dot > 0.2 else (SKY_BASE if dot > -0.2 else SKY_DARK)

            # Utility tool belt (y: 84..90)
            if 84 <= y <= 90:
                if y in (84, 90):
                    col = WALNUT_DARK
                else:
                    col = WALNUT_BASE if abs(dx) < 0.7 else WALNUT_LIGHT

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Polished Brass Gear Pectoral Medallion at (64, 68), radius 5.8
    for y in range(62, 75):
        for x in range(58, 71):
            dist = math.sqrt((x - 64.0)**2 + (y - 68.0)**2)
            if dist <= 5.8:
                dot = -(x - 64.0) * 0.2 - (y - 68.0) * 0.2
                if dist <= 2.0:
                    col = PINK_LIGHT if dot > 0 else PINK_BASE
                elif dot > 0.3:
                    col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                elif dot > -0.2:
                    col = GOLD_BASE
                else:
                    col = GOLD_DARK
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Belt Buckle at (64, 87)
    for y in range(85, 90):
        for x in range(61, 68):
            if abs(x - 64) <= 3 and abs(y - 87) <= 2:
                col = GOLD_LIGHT if x < 64 else GOLD_DARK
                if abs(x - 64) <= 1 and abs(y - 87) <= 1:
                    col = RUBBER_DARK
                costume_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    return apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    Weapon: weapon_donkey_bazaar_clearing_axe
    Bazaar Cograil Clearing Axe (Viking Heavy Axe).
    Features:
    - Aged walnut wood handle with brass knurled handgrip (y: 42..114, x: 94..98).
    - Heavy double-beveled high-carbon steel axe head (y: 44..74, x: 84..124).
    - Shock-absorbing brass reduction ratchet at axe eye (x: 96, y: 58).
    - Sharp tempered steel cutting edge with specular highlights.
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Axe Shaft: from (95, 42) down to (97, 114)
    for y in range(42, 115):
        t = (y - 42) / 72.0
        cx = 95.0 + t * 2.0
        width = 2.4
        for x in range(int(round(cx - width)), int(round(cx + width + 1))):
            dx = (x - cx) / width
            dot = -0.6 * dx
            if 72 <= y <= 84:
                # Brass knurled anti-slip handgrip
                if (x + y) % 2 == 0:
                    col = GOLD_LIGHT
                else:
                    col = GOLD_BASE if dot > 0 else GOLD_DARK
            elif y >= 110:
                # Bottom brass buttcap spike
                col = GOLD_LIGHT if dot > 0 else GOLD_DARK
            else:
                # Walnut wood shaft
                col = WALNUT_LIGHT if dot > 0.2 else (WALNUT_BASE if dot > -0.2 else WALNUT_DARK)
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Axe Eye & Brass Reduction Ratchet at (96, 58)
    for y in range(52, 65):
        for x in range(90, 102):
            dist = math.sqrt((x - 96.0)**2 + (y - 58.0)**2)
            if dist <= 5.2:
                dot = -(x - 96.0) * 0.15 - (y - 58.0) * 0.15
                if dist <= 2.2:
                    col = PINK_BASE if dot < 0 else PINK_LIGHT
                elif dot > 0.25:
                    col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                elif dot > -0.2:
                    col = GOLD_BASE
                else:
                    col = GOLD_DARK
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Main Forward Clearing Axe Blade (x: 96..124, y: 44..72)
    for y in range(44, 73):
        ty = (y - 58.0) / 14.0  # -1 at top, +1 at bottom
        blade_reach = 26.0 * (1.0 - ty**2 * 0.45)
        for x in range(96, int(round(96.0 + blade_reach + 1))):
            tx = (x - 96.0) / max(1.0, blade_reach)
            dot = 0.7 * tx - 0.4 * ty

            # Blade profile
            if tx >= 0.88:
                # Tempered sharp cutting edge
                col = STEEL_SHINE if dot > 0 else STEEL_LIGHT
            elif tx >= 0.5:
                # Beveled wedge
                col = STEEL_LIGHT if dot > 0.2 else STEEL_BASE
            else:
                # Reinforced blade cheek
                col = STEEL_BASE if dot > 0 else STEEL_DARK

            # Chip relief groove
            if 0.35 <= tx <= 0.48 and abs(ty) < 0.6:
                col = STEEL_DEEP

            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Rear Pick / Debris Spike (x: 84..96, y: 52..64)
    for y in range(52, 65):
        ty = (y - 58.0) / 6.0
        rear_reach = 11.0 * (1.0 - abs(ty) * 0.7)
        for x in range(int(round(96.0 - rear_reach)), 96):
            tx = (96.0 - x) / max(1.0, rear_reach)
            col = STEEL_LIGHT if tx > 0.7 else STEEL_DARK
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Edge catchlight at blade apex (122, 58)
    weapon_img.putpixel((122, 57), tuple(WHITE_SHINE.astype(int)) + (255,))
    weapon_img.putpixel((123, 58), tuple(WHITE_SHINE.astype(int)) + (255,))
    weapon_img.putpixel((122, 59), tuple(WHITE_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_donkey_slices():
    print("=== BUILDING SAPPER DONKEY 7 PAPERDOLL SLICES ===")

    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_donkey_dawn_clover_brass", key_img),
        ("back_curio", "curio_donkey_cograil_pack_tail", curio_img),
        ("chassis", "chassis_donkey_tinplate_default", chassis_img),
        ("head_unit", "head_donkey_ratchet_ears_cowl", head_img),
        ("costume", "costume_donkey_sapper_harness", costume_img),
        ("optic_core", "face_donkey_slate_goggles", core_img),
        ("weapon", "weapon_donkey_bazaar_clearing_axe", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{DONKEY_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_donkey_dawn_clover_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_donkey_dawn_clover_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_donkey_bazaar_clearing_axe.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_donkey_bazaar_clearing_axe_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    ordered_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_im in ordered_slices:
        composite.alpha_composite(s_im)

    proof_comp = f"{DONKEY_PD_DIR}/proof_paperdoll_donkey_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{DONKEY_PD_DIR}/proof_paperdoll_donkey_magenta.png"
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

    strip_path = f"{DONKEY_PD_DIR}/proof_donkey_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([32, 108, 96, 120], fill=(31, 26, 58, 110))
    shd.ellipse([42, 110, 86, 118], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/donkey_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    p_idle_64 = f"{PLAYER_DIR}/donkey_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/donkey_idle.png"
    idle_with_shadow.save(p_party_idle)

    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/donkey_idle.png"
    idle_with_shadow.save(p_web_idle)
    print("  ✓ Official Idle assets (64, 128, party, web) generated successfully")

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
        showcase_path = f"{SHOWCASE_DIR}/donkey_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # Compatibility symlink: game/assets/sprites/player/donkey -> paperdoll/donkey
    dk_alias_dir = f"{PLAYER_DIR}/donkey"
    if os.path.exists(dk_alias_dir):
        if os.path.islink(dk_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/donkey -> paperdoll/donkey already exists")
        else:
            files = os.listdir(dk_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(dk_alias_dir, f))
                os.rmdir(dk_alias_dir)
                os.symlink("paperdoll/donkey", dk_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/donkey -> paperdoll/donkey")
    else:
        try:
            os.symlink("paperdoll/donkey", dk_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/donkey -> paperdoll/donkey")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL SAPPER DONKEY PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_donkey_slices()
