#!/usr/bin/env python3
"""
build_scorpion_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第七十族 伏影沙蠍 (The Duneshadow Scorpion, scorpion) 7 Paperdoll Slices.

Follows:
- docs/world/DUNESHADOW_SCORPION_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, zero venom, stamped cold-rolled tinplate chassis #FFA010 / #FFD028,
  stamped dune-visor metal cowl with side louvers and antenna,
  dual high-clarity amber quartz goggles #FFD028 / #FFA010,
  scavenger riveted lacquer plate cuirass with inspection sashes #4ED86A / #38A0FF,
  articulated spring stinger tail rail and counterweight damping hammer #FFD028 / #FFA010,
  dune cross-cog carved brass winding key with coral pink center rivet #FFD028 / #FF5E8A,
  duneshadow spike dart with gyro bearing and tungsten tips)
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
SCORPION_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/scorpion"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Duneshadow Scorpion Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Sunset Warm Orange (#FFA010) - Chassis lacquer & Cowl accents
ORANGE_SHINE = np.array([255, 232, 160], dtype=float)
ORANGE_LIGHT = np.array([255, 198, 85], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)    # #FFA010
ORANGE_SHADOW= np.array([215, 118, 10], dtype=float)
ORANGE_DARK  = np.array([168, 82, 8], dtype=float)
ORANGE_DEEP  = np.array([120, 52, 6], dtype=float)

# 2. Forged Brass & Dawn Gold (#FFD028) - Winding Key, Gears, Tail Segments, Goggles
GOLD_SHINE = np.array([255, 252, 195], dtype=float)
GOLD_LIGHT = np.array([255, 236, 120], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)     # #FFD028
GOLD_SHADOW= np.array([205, 155, 22], dtype=float)
GOLD_DARK  = np.array([150, 105, 12], dtype=float)
GOLD_DEEP  = np.array([105, 70, 8], dtype=float)

# 3. Desert Amber Quartz (#FFAA15) - Optic Core Lenses
AMBER_SHINE = np.array([255, 245, 180], dtype=float)
AMBER_LIGHT = np.array([255, 215, 75], dtype=float)
AMBER_BASE  = np.array([255, 170, 20], dtype=float)
AMBER_SHADOW= np.array([220, 125, 12], dtype=float)
AMBER_DARK  = np.array([160, 80, 8], dtype=float)

# 4. Ivory Porcelain & Cold-rolled Tinplate (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)   # #FFFDF8
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)

# 5. Mint Green Inspection Ribbon (#4ED86A) - Harness Accent
MINT_SHINE = np.array([195, 255, 215], dtype=float)
MINT_LIGHT = np.array([135, 242, 165], dtype=float)
MINT_BASE  = np.array([78, 216, 106], dtype=float)     # #4ED86A
MINT_DARK  = np.array([42, 160, 68], dtype=float)

# 6. Sky Blue Reticle & Sashes (#38A0FF)
SKY_SHINE  = np.array([210, 240, 255], dtype=float)
SKY_LIGHT  = np.array([130, 205, 255], dtype=float)
SKY_BASE   = np.array([56, 160, 255], dtype=float)      # #38A0FF
SKY_SHADOW = np.array([32, 115, 210], dtype=float)
SKY_DARK   = np.array([20, 75, 160], dtype=float)

# 7. Coral Pink Rivet & Rubber Seals (#FF5E8A)
PINK_SHINE = np.array([255, 210, 230], dtype=float)
PINK_LIGHT = np.array([255, 150, 182], dtype=float)
PINK_BASE  = np.array([255, 94, 138], dtype=float)     # #FF5E8A
PINK_DARK  = np.array([195, 55, 95], dtype=float)

# 8. High-Carbon Sapper Steel (Dart Blades & Joints)
STEEL_SHINE = np.array([248, 252, 255], dtype=float)
STEEL_LIGHT = np.array([210, 225, 242], dtype=float)
STEEL_BASE  = np.array([150, 170, 195], dtype=float)
STEEL_DARK  = np.array([100, 115, 135], dtype=float)
STEEL_DEEP  = np.array([58, 68, 82], dtype=float)

# 9. Industrial Rubber & Joint Seals
RUBBER_LIGHT = np.array([74, 70, 88], dtype=float)
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
    Winding Key: key_scorpion_cross_brass
    Dune Cross-Cog Carved Brass Winding Key with Center Coral Pink Rivet.
    Positioned at back spine (x: 52..76, y: 44..70).
    Follows 0-ART29: Warm bronze outline, strictly 0 dark box pixels.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Drive Shaft from spine socket (64, 68) up to center pivot (64, 46)
    for y in range(46, 69):
        t = (y - 46) / 23.0
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

    # 2. Four Cross-Cog Rings/Lobes centered at (64, 46)
    # North (64, 33), South (64, 59), West (51, 46), East (77, 46)
    lobes = [
        (64.0, 34.0, 7.8, 3.8),   # Top
        (64.0, 58.0, 7.0, 3.5),   # Bottom
        (52.0, 46.0, 7.5, 3.8),   # Left
        (76.0, 46.0, 7.5, 3.8),   # Right
    ]

    for cx, cy, r_out, r_in in lobes:
        for y in range(int(cy - r_out - 1), int(cy + r_out + 2)):
            for x in range(int(cx - r_out - 1), int(cx + r_out + 2)):
                if 0 <= x < W and 0 <= y < H:
                    dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                    if r_in <= dist <= r_out:
                        angle = math.atan2(y - cy, x - cx)
                        # Bevel gear lighting
                        dot = -math.cos(angle - 0.7)
                        # Small gear teeth indentations
                        tooth = math.cos(angle * 6.0)
                        if dot > 0.35:
                            col = GOLD_SHINE * 0.45 + GOLD_LIGHT * 0.55 + dot * 14.0 + tooth * 8.0
                        elif dot > -0.2:
                            col = GOLD_BASE + dot * 18.0 + tooth * 6.0
                        else:
                            col = GOLD_DARK + (dot + 0.3) * 14.0
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

    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=60)


def build_back_curio() -> Image.Image:
    """
    Back Curio: curio_scorpion_spring_stinger_tail
    Five-Segment Articulated Spring Stinger Tail Rail with Counterweight Damping Hammer.
    Positioned curving up and over from lower spine (x: 52, y: 78) upward to left arch (x: 32..46, y: 22..58)
    and apex stinger nozzle + brass counterweight hammer at (38, 22).
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # Curve trajectory for 5 tail segments:
    # Seg 1: base (52, 78) to (44, 72)
    # Seg 2: (44, 72) to (36, 62)
    # Seg 3: (36, 62) to (32, 48)
    # Seg 4: (32, 48) to (34, 34)
    # Seg 5: (34, 34) to (42, 24)
    segments = [
        # (cx, cy, radius_x, radius_y, angle, length)
        (50.0, 76.0, 5.0, 6.0, 0.4),
        (42.0, 68.0, 5.5, 6.2, 0.6),
        (35.0, 56.0, 5.2, 6.0, 1.1),
        (32.0, 42.0, 5.0, 5.8, 1.5),
        (36.0, 30.0, 4.6, 5.2, 2.0),
    ]

    # Draw spring guide wire / tension cables behind segments
    for t_step in np.linspace(0.0, 1.0, 80):
        # Quadratic bezier curve for spring cable
        # P0=(52, 78), P1=(24, 50), P2=(42, 22)
        px = (1 - t_step)**2 * 52.0 + 2 * (1 - t_step) * t_step * 24.0 + t_step**2 * 42.0
        py = (1 - t_step)**2 * 78.0 + 2 * (1 - t_step) * t_step * 50.0 + t_step**2 * 22.0
        ix, iy = int(round(px)), int(round(py))
        if 0 <= ix < W and 0 <= iy < H:
            curio_img.putpixel((ix, iy), tuple(STEEL_LIGHT.astype(int)) + (255,))
            if ix + 1 < W:
                curio_img.putpixel((ix + 1, iy), tuple(STEEL_DARK.astype(int)) + (255,))

    # Draw each articulated brass tail segment
    for i, (scx, scy, rx, ry, ang) in enumerate(segments):
        for y in range(int(scy - ry - 2), int(scy + ry + 3)):
            for x in range(int(scx - rx - 2), int(scx + rx + 3)):
                if 0 <= x < W and 0 <= y < H:
                    dx = (x - scx)
                    dy = (y - scy)
                    # Rotate by segment angle
                    rx_rot = dx * math.cos(-ang) - dy * math.sin(-ang)
                    ry_rot = dx * math.sin(-ang) + dy * math.cos(-ang)
                    dist_sq = (rx_rot / rx)**2 + (ry_rot / ry)**2
                    if dist_sq <= 1.0:
                        dot = -0.5 * (rx_rot / rx) - 0.5 * (ry_rot / ry)
                        # Alternating brass and sunset orange plates
                        if i % 2 == 0:
                            if dot > 0.35:
                                col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6 + dot * 12.0
                            elif dot > 0.0:
                                col = GOLD_BASE + dot * 15.0
                            else:
                                col = GOLD_DARK
                        else:
                            if dot > 0.35:
                                col = ORANGE_LIGHT + dot * 12.0
                            elif dot > 0.0:
                                col = ORANGE_BASE + dot * 15.0
                            else:
                                col = ORANGE_DARK

                        # Segment joint rivets
                        if math.sqrt(rx_rot**2 + ry_rot**2) <= 1.8:
                            col = RUBBER_LIGHT if dot > 0 else RUBBER_DARK

                        curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Stinger tip: Counterweight balance hammer & guide nozzle at (43, 22)
    hx, hy = 43.0, 22.0
    for y in range(16, 29):
        for x in range(37, 50):
            dist = math.sqrt((x - hx)**2 + (y - hy)**2)
            if dist <= 5.2:
                dot = -0.6 * (x - hx) / 5.2 - 0.6 * (y - hy) / 5.2
                if dist <= 2.2:
                    col = GOLD_SHINE if dot > 0 else GOLD_LIGHT
                elif dot > 0.3:
                    col = GOLD_LIGHT + dot * 15.0
                elif dot > -0.2:
                    col = GOLD_BASE
                else:
                    col = GOLD_DARK
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Guide nozzle tungsten dart-launching pin pointing forward-right
    for t in range(0, 7):
        nx = int(round(hx + 3.0 + t * 0.9))
        ny = int(round(hy + 1.0 + t * 0.4))
        if 0 <= nx < W and 0 <= ny < H:
            curio_img.putpixel((nx, ny), tuple(STEEL_LIGHT.astype(int)) + (255,))
            if ny + 1 < H:
                curio_img.putpixel((nx, ny + 1), tuple(STEEL_DARK.astype(int)) + (255,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    Chassis: chassis_scorpion_stock
    2.2 Chibi Stamped Cold-rolled Tinplate (#FFA010 & #FFD028) scorpion body with multi-tone depth.
    Features:
    - 0-ART9/11: Strictly 0 pixels at x >= 94.
    - 0-ART18: Bare torso (y: 58..94, x: 44..84) rich multi-tone cel-shading (unique colors >= 20).
    - 0-ART28q: Color coherence with head_unit (L2 distance < 60.0).
    - Six chibi mechanical crawler legs with anti-slip rubber pads.
    - Left pincer claw resting/guarding at x: 34..48, y: 58..78.
    - Right arm extending forward to x: 74..93, y: 60..82 ready to grip dart.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 0. Neck / Shoulder Transition Block to seal core against holes (x: 46..82, y: 53..61)
    for y in range(53, 62):
        for x in range(46, 83):
            dot = -(x - 64.0) * 0.05 - (y - 57.0) * 0.08
            col = ORANGE_BASE + dot * 16.0
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
                    col = ORANGE_SHINE * 0.35 + ORANGE_LIGHT * 0.65 + dot * 12.0
                elif dot > 0.35:
                    col = ORANGE_LIGHT + dot * 15.0
                elif dot > 0.05:
                    col = ORANGE_BASE + dot * 18.0
                elif dot > -0.25:
                    col = ORANGE_SHADOW + (dot + 0.25) * 16.0
                elif dot > -0.55:
                    col = ORANGE_DARK + (dot + 0.55) * 14.0
                else:
                    col = ORANGE_DEEP + (dot + 0.8) * 12.0

                # Subtle mechanical seams & brass rivets
                if abs(dx) < 0.06 or (y in (66, 76, 84) and abs(dx) < 0.75):
                    col = col * 0.85 + RUBBER_BASE * 0.15
                elif y in (68, 78) and abs(dx) in (0.3, 0.35, 0.4):
                    col = GOLD_LIGHT

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Lower Abdomen / Pelvis (x: 48..80, y: 86..94)
    for y in range(86, 95):
        for x in range(48, 81):
            dx = (x - 64.0) / 16.0
            if abs(dx) <= 1.0:
                col = ORANGE_SHADOW if abs(dx) < 0.5 else ORANGE_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Six Mechanical Crawler Legs
    # Left legs (3): (40..52, y: 88..115)
    # Right legs (3): (76..88, y: 88..115)
    leg_anchors = [
        # (root_x, root_y, tip_x, tip_y, is_left)
        (50.0, 84.0, 38.0, 102.0, True),    # Left Front
        (52.0, 88.0, 42.0, 110.0, True),    # Left Mid
        (54.0, 92.0, 48.0, 116.0, True),    # Left Rear
        (78.0, 84.0, 90.0, 102.0, False),   # Right Front
        (76.0, 88.0, 86.0, 110.0, False),   # Right Mid
        (74.0, 92.0, 80.0, 116.0, False),   # Right Rear
    ]

    for rx0, ry0, tx0, ty0, is_l in leg_anchors:
        for t_step in np.linspace(0.0, 1.0, 24):
            # Curved joint arc
            mid_lift = -4.0
            lx = (1 - t_step) * rx0 + t_step * tx0
            ly = (1 - t_step) * ry0 + t_step * ty0 + math.sin(t_step * math.pi) * mid_lift
            thickness = 3.4 - t_step * 1.0
            for oy in range(int(round(ly - thickness)), int(round(ly + thickness + 1))):
                for ox in range(int(round(lx - thickness)), min(94, int(round(lx + thickness + 1)))):
                    if 0 <= ox < W and 0 <= oy < H:
                        dist = math.sqrt((ox - lx)**2 + (oy - ly)**2)
                        if dist <= thickness:
                            dot = -0.5 * (ox - lx) / thickness - 0.5 * (oy - ly) / thickness
                            if t_step > 0.85:
                                # Black rubber suction pad
                                col = RUBBER_LIGHT if dot > 0 else RUBBER_BASE
                            elif t_step < 0.3:
                                # Brass ball joint socket
                                col = GOLD_LIGHT if dot > 0 else GOLD_DARK
                            else:
                                # Orange tinplate leg armor
                                col = ORANGE_LIGHT if dot > 0 else ORANGE_BASE
                            chassis_img.putpixel((ox, oy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Arms & Pincers
    # Left Arm & Pincer (x: 34..48, y: 58..78)
    for y in range(58, 79):
        t = (y - 58) / 20.0
        acx = 44.0 - t * 4.0
        for x in range(int(round(acx - 4.0)), int(round(acx + 4.0))):
            dx = (x - acx) / 4.0
            if abs(dx) <= 1.0:
                dot = -0.6 * dx - 0.4 * t
                if 66 <= y <= 70:
                    col = GOLD_LIGHT if dot > 0 else GOLD_DARK
                elif y >= 72:
                    # Pincer shears
                    col = GOLD_BASE if dot > 0 else GOLD_DARK
                else:
                    col = ORANGE_BASE if dot > 0 else ORANGE_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Pincer Dual Blades (x: 32..42, y: 72..82)
    for y in range(72, 82):
        for x in range(32, 42):
            # Curved claw shears
            dist1 = math.sqrt((x - 35)**2 + (y - 77)**2)
            dist2 = math.sqrt((x - 39)**2 + (y - 77)**2)
            if dist1 <= 3.0 or dist2 <= 3.0:
                col = GOLD_LIGHT if (x + y) % 2 == 0 else GOLD_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Arm (x: 74..93, y: 60..82): strictly x <= 93 (0-ART9/11)
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
                    col = ORANGE_BASE if dot > 0 else ORANGE_SHADOW
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50)


def build_head_unit() -> Image.Image:
    """
    Head Unit: head_scorpion_dune_visor
    Stamped Dune-Visor Metal Cowl with Brass Louvers and Antenna.
    Features:
    - 0-ART27: Hollow eye sockets! Left socket (y: 41..44, x: 53..56) and
      Right socket (y: 41..44, x: 72..75) MUST have alpha == 0!
    - Stamped antenna pointing up at center-top (64, 14..29).
    - Brass louvered heat grilles on sides (x: 44..50, 78..84, y: 38..48).
    - Harmonized orange and ivory plates (0-ART28q L2 < 60.0).
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Stamped Antenna (x: 63..65, y: 14..30)
    for y in range(14, 31):
        t = (y - 14) / 16.0
        for x in (63, 64, 65):
            dot = -(x - 64.0) * 0.5
            col = GOLD_LIGHT if dot >= 0 else GOLD_DARK
            head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    # Antenna tip bulb (64, 14) radius 2.5
    for y in range(12, 17):
        for x in range(62, 67):
            if (x - 64.0)**2 + (y - 14.0)**2 <= 5.0:
                col = GOLD_SHINE if x <= 64 and y <= 14 else GOLD_BASE
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Main Head Dome Visor (x: 44..84, y: 29..56)
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
                    # Forehead visor plate in warm orange (#FFA010)
                    if dot > 0.4:
                        col = ORANGE_SHINE * 0.3 + ORANGE_LIGHT * 0.7 + dot * 10.0
                    elif dot > 0.05:
                        col = ORANGE_LIGHT + dot * 14.0
                    elif dot > -0.3:
                        col = ORANGE_BASE + (dot + 0.3) * 12.0
                    else:
                        col = ORANGE_SHADOW + (dot + 0.6) * 10.0
                else:
                    # Face cowl in orange lacquer matching chassis
                    if dot > 0.45:
                        col = ORANGE_LIGHT + dot * 12.0
                    elif dot > 0.15:
                        col = ORANGE_BASE + dot * 15.0
                    elif dot > -0.2:
                        col = ORANGE_SHADOW + (dot + 0.2) * 14.0
                    elif dot > -0.5:
                        col = ORANGE_DARK + (dot + 0.5) * 12.0
                    else:
                        col = ORANGE_DEEP + (dot + 0.8) * 10.0

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Brass Louvered Heat Grilles on cheeks (x: 45..50, 78..83, y: 38..48)
    for y in range(38, 49):
        # Louver ribs every 2 pixels
        is_louver_ridge = (y % 2 == 0)
        for x in list(range(45, 51)) + list(range(77, 83)):
            col = GOLD_LIGHT if is_louver_ridge else GOLD_DARK
            head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Desert Dune Crest at forehead (64, 34)
    for y in range(32, 37):
        for x in range(61, 67):
            if (x - 64)**2 + (y - 34)**2 <= 4.0:
                head_img.putpixel((x, y), tuple(GOLD_BASE.astype(int)) + (255,))

    # 5. HOLLOW EYE SOCKETS (0-ART27 MANDATE)
    # Left socket (y: 41..44, x: 53..56) and right socket (y: 41..44, x: 72..75) must be 100% alpha = 0
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
    Optic Core: face_scorpion_amber_goggles
    Dual High-Clarity Amber Quartz Spherical Goggles.
    Features:
    - 0-ART27: Center pixels at (54, 42) and (74, 42) must have alpha > 200.
    - Deep blue-purple titanium bezel with warm amber (#FFAA15) and cyan reticle crosshair (#38A0FF).
    - Vivid white catchlights for living toy gaze.
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
                        # Titanium anti-glare bezel (#1F1A3A / #2B2446)
                        col = OUTLINE * 0.8 + SKY_DARK * 0.2
                    elif dist <= 1.4:
                        # Cyan crosshair reticle (#38A0FF)
                        if abs(x - round(ecx)) <= 0.6 or abs(y - round(ecy)) <= 0.6:
                            col = SKY_LIGHT
                        else:
                            col = AMBER_SHINE
                    else:
                        # Amber quartz crystal lens (#FFD028 / #FFA010)
                        if dot > 0.4:
                            col = AMBER_SHINE * 0.5 + AMBER_LIGHT * 0.5
                        elif dot > 0.0:
                            col = AMBER_BASE
                        else:
                            col = AMBER_SHADOW

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
    Costume: costume_scorpion_scavenger_plate
    Scavenger Riveted Brass-Reinforced Lacquer Cuirass with Inspection Sashes.
    Features:
    - 0-ART26b: Strictly 0 pixels at y >= 96.
    - Mint Green (#4ED86A) and Sky Blue (#38A0FF) diagonal inspection sashes.
    - Polished brass gear pectoral medallion at (64, 68) with coral pink center (#FF5E8A).
    - Utility belt and brass buckles at y: 84..91.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Main Cuirass Plate (x: 48..80, y: 56..92)
    for y in range(56, 93):
        t = (y - 56) / 36.0
        half_w = 15.0 - t * 2.0
        for x in range(int(round(64 - half_w)), int(round(64 + half_w + 1))):
            dx = (x - 64.0) / half_w
            dot = -0.5 * dx - 0.5 * (t - 0.5)

            # Base deep lacquer plate with continuous shading
            if dot > 0.3:
                col = RUBBER_LIGHT + dot * 12.0
            elif dot > -0.2:
                col = RUBBER_BASE + (dot + 0.2) * 10.0
            else:
                col = RUBBER_DARK + (dot + 0.5) * 8.0

            # Cross Inspection Sashes:
            # Sash 1 (Mint Green): from top-left (50, 56) to bottom-right (76, 84)
            sash1_dist = abs((x - 50.0) * 0.73 - (y - 56.0) * 0.68)
            if sash1_dist <= 2.2:
                col = MINT_SHINE if dot > 0.2 else (MINT_BASE + dot * 15.0 if dot > -0.2 else MINT_DARK)

            # Sash 2 (Sky Blue): from top-right (78, 56) to bottom-left (52, 84)
            sash2_dist = abs((x - 78.0) * 0.73 + (y - 56.0) * 0.68)
            if sash2_dist <= 2.2:
                col = SKY_SHINE if dot > 0.2 else (SKY_BASE + dot * 15.0 if dot > -0.2 else SKY_DARK)

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Pectoral Gear Medallion at (64, 68) radius 5.5
    for y in range(62, 75):
        for x in range(58, 71):
            dist = math.sqrt((x - 64.0)**2 + (y - 68.0)**2)
            if dist <= 5.5:
                dot = -(x - 64.0) * 0.15 - (y - 68.0) * 0.15
                if dist <= 2.4:
                    col = PINK_LIGHT if dot > 0 else PINK_BASE
                else:
                    col = GOLD_LIGHT if dot > 0.1 else GOLD_DARK
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Utility Belt and Buckles (y: 84..91, x: 50..78)
    for y in range(84, 92):
        for x in range(50, 79):
            if abs(x - 64.0) <= 13.0:
                dot = -(x - 64.0) * 0.05
                if abs(x - 64.0) <= 3.5:
                    # Central brass belt buckle
                    col = GOLD_LIGHT if dot > 0 else GOLD_BASE
                else:
                    # Heavy rubber tool belt
                    col = RUBBER_LIGHT if dot > 0 else RUBBER_DARK
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    Weapon: weapon_scorpion_duneshadow_dart
    Duneshadow Spike Dart with Central Brass Gyro Bearing & Swirl Evacuation Vents.
    Poised in right hand at (x: 82..124, y: 50..86).
    Aerodynamic multi-point shuriken dart with tungsten piercing tips.
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # Center hub of dart at (102, 68)
    dcx, dcy = 102.0, 68.0

    # 4 Aerodynamic curved dart blades at 0, 90, 180, 270 degrees
    # Radius reaches up to 20 px
    for y in range(48, 88):
        for x in range(82, 123):
            dx = x - dcx
            dy = y - dcy
            dist = math.sqrt(dx**2 + dy**2)
            if dist <= 20.0:
                angle = math.atan2(dy, dx)
                # 4-blade aerodynamic dart shuriken
                # r_bound(theta) = r_core + r_spike * max(0, cos(4*theta))
                shape = math.cos(4.0 * angle)
                max_reach = 5.0 + 15.0 * max(0.0, shape)**1.8
                if dist <= max_reach:
                    dot = -math.cos(angle - 0.7)
                    if dist <= 4.5:
                        # Central brass gyro bearing
                        dot_c = -0.6 * (dx / 4.5) - 0.6 * (dy / 4.5)
                        if dist <= 1.8:
                            col = GOLD_SHINE
                        elif dot_c > 0.1:
                            col = GOLD_LIGHT
                        else:
                            col = GOLD_DARK
                    elif dist >= max_reach - 2.5:
                        # Tungsten edge catchlight
                        col = STEEL_SHINE if dot > 0 else STEEL_LIGHT
                    else:
                        # Stamped cold-rolled steel blade
                        if dot > 0.35:
                            col = STEEL_LIGHT + dot * 12.0
                        elif dot > -0.2:
                            col = STEEL_BASE + dot * 15.0
                        else:
                            col = STEEL_DARK

                    weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_scorpion_slices():
    print("=== BUILDING DUNESHADOW SCORPION 7 PAPERDOLL SLICES ===")

    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_scorpion_cross_brass", key_img),
        ("back_curio", "curio_scorpion_spring_stinger_tail", curio_img),
        ("chassis", "chassis_scorpion_stock", chassis_img),
        ("head_unit", "head_scorpion_dune_visor", head_img),
        ("costume", "costume_scorpion_scavenger_plate", costume_img),
        ("optic_core", "face_scorpion_amber_goggles", core_img),
        ("weapon", "weapon_scorpion_duneshadow_dart", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{SCORPION_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_scorpion_cross_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_scorpion_cross_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_scorpion_duneshadow_dart.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_scorpion_duneshadow_dart_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    ordered_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_im in ordered_slices:
        composite.alpha_composite(s_im)

    proof_comp = f"{SCORPION_PD_DIR}/proof_paperdoll_scorpion_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SCORPION_PD_DIR}/proof_paperdoll_scorpion_magenta.png"
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

    strip_path = f"{SCORPION_PD_DIR}/proof_scorpion_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([30, 108, 98, 120], fill=(31, 26, 58, 110))
    shd.ellipse([40, 110, 88, 118], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/scorpion_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    p_idle_64 = f"{PLAYER_DIR}/scorpion_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/scorpion_idle.png"
    idle_with_shadow.save(p_party_idle)

    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/scorpion_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/scorpion_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # Compatibility symlink: game/assets/sprites/player/scorpion -> paperdoll/scorpion
    sc_alias_dir = f"{PLAYER_DIR}/scorpion"
    if os.path.exists(sc_alias_dir):
        if os.path.islink(sc_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/scorpion -> paperdoll/scorpion already exists")
        else:
            files = os.listdir(sc_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(sc_alias_dir, f))
                os.rmdir(sc_alias_dir)
                os.symlink("paperdoll/scorpion", sc_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/scorpion -> paperdoll/scorpion")
    else:
        try:
            os.symlink("paperdoll/scorpion", sc_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/scorpion -> paperdoll/scorpion")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL DUNESHADOW SCORPION PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_scorpion_slices()
