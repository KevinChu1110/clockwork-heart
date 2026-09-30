#!/usr/bin/env python3
"""
build_mantis_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第七十一族 翠刃螳螂 (The Jade Mantis, mantis) 7 Paperdoll Slices.

Follows:
- docs/world/JADE_MANTIS_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, zero chitin/flesh, zero venom,
  stamped thin brass sheets & tinplate #4ED86A mint green & #FFFDF8 ivory white,
  stamped canopy angled cowl with side louvers & dual spiral brass antennae #FFD028,
  dual spherical high-clarity emerald quartz goggles #4ED86A / #38A0FF / #FFD028 set in deep indigo rings #1F1A3A,
  vine-laced brass plate cuirass with inspection sashes #38A0FF / #FFA010 & gear chest medallion,
  segmented spring balance pack & micro bellows #FFD028 / #4ED86A,
  double-loop vine-filigree brass wind-up key with center coral pink rivet #FFD028 / #FF5E8A,
  jade scythe claw with high-carbon steel blades & eccentric cam gear bearing)
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
MANTIS_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/mantis"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Jade Mantis Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Primary Metal / Stamped Thinplate Emerald Mint Green (#4ED86A) - Chassis, Cowl, Armor
MINT_SHINE  = np.array([215, 255, 230], dtype=float)
MINT_LIGHT  = np.array([145, 245, 175], dtype=float)
MINT_BASE   = np.array([78, 216, 106], dtype=float)     # #4ED86A
MINT_SHADOW = np.array([48, 168, 80], dtype=float)
MINT_DARK   = np.array([28, 118, 55], dtype=float)
MINT_DEEP   = np.array([18, 78, 38], dtype=float)

# 2. Secondary Ivory Enamel Highlights & Shock Absorbers (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)   # #FFFDF8
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)

# 3. Forged Brass & Dawn Gold (#FFD028) - Winding Key, Gears, Antennas, Blade Bevels
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)      # #FFD028
GOLD_SHADOW= np.array([205, 155, 22], dtype=float)
GOLD_DARK  = np.array([150, 105, 12], dtype=float)
GOLD_DEEP  = np.array([105, 70, 8], dtype=float)

# 4. Dopamine Sunset Warm Orange (#FFA010) - Cam Bearings, Hazard Stripes, Bellows Louvers
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)    # #FFA010
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 5. Deep Forest Vine Weave (#2E7248) - Relief on Cuirass & Backpack
VINE_SHINE = np.array([165, 235, 185], dtype=float)
VINE_LIGHT = np.array([95, 195, 130], dtype=float)
VINE_BASE  = np.array([46, 145, 85], dtype=float)
VINE_DARK  = np.array([28, 105, 58], dtype=float)
VINE_DEEP  = np.array([16, 68, 38], dtype=float)

# 6. Dopamine Sky Blue (#38A0FF) - Concentric Reticle, Buckles, Safety Sashes
SKY_SHINE  = np.array([210, 240, 255], dtype=float)
SKY_LIGHT  = np.array([130, 205, 255], dtype=float)
SKY_BASE   = np.array([56, 160, 255], dtype=float)      # #38A0FF
SKY_SHADOW = np.array([32, 115, 210], dtype=float)
SKY_DARK   = np.array([20, 75, 160], dtype=float)

# 7. Dopamine Coral Pink (#FF5E8A) - Winding Key Center Rivet, Antenna Tips
CORAL_SHINE = np.array([255, 210, 230], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)     # #FF5E8A
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 8. High-Carbon Sapper Steel - Scythe Claw Blade & Balance Springs
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
    Applies a clean 1px dark outline with smooth subpixel anti-aliasing on boundaries.
    Guarantees alpha levels > 2 and zero blocky halo.
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
    SLICE 1: WINDING KEY (z=5)
    蔓谷雙環藤蔓雕花黃銅發條鑰匙 (key_mantis_vine_brass)
    Dual-Loop Vine-Filigree Brass Wind-up Key with Coral Pink Rivet (#FF5E8A).
    Positioned at upper left back (x: 22..52, y: 16..48) breaking silhouette cleanly.
    Drive shaft connects from chassis spine socket (48, 52) to key center hub at (36, 28).
    Two interlaced filigree brass rings (radius 7.5 and 9.5) with vine scrollwork & bevel gear teeth.
    Warm bronze outline (OUTLINE_KEY).
    Follows 0-ART29: max dark run < 13, max white run < 40, zero dark box artifacts.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    kcx, kcy = 36.0, 28.0

    # 1. Drive Shaft connecting spine socket (48, 52) to key hub (36, 28)
    for t in np.linspace(0.0, 1.0, 36):
        ax = 48.0 * (1.0 - t) + kcx * t
        ay = 52.0 * (1.0 - t) + kcy * t
        for off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(ax + off * 0.8))
            py = int(round(ay - off * 0.6))
            if 0 <= px < W and 0 <= py < H:
                dot = off / 1.5
                col = GOLD_LIGHT if dot > 0.2 else (GOLD_BASE if dot > -0.4 else GOLD_DARK)
                key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Dual Interlaced Vine-Filigree Brass Loops
    # Loop 1: centered at (31.0, 26.0), outer r=8.2, inner r=4.2
    # Loop 2: centered at (41.0, 28.0), outer r=8.2, inner r=4.2
    loops = [
        (31.0, 26.0, 8.2, 4.2),
        (41.0, 28.0, 8.2, 4.2)
    ]
    for lcx, lcy, r_out, r_in in loops:
        for y in range(int(lcy - r_out - 1), int(lcy + r_out + 2)):
            for x in range(int(lcx - r_out - 1), int(lcx + r_out + 2)):
                if 0 <= x < W and 0 <= y < H:
                    dist = math.sqrt((x - lcx)**2 + (y - lcy)**2)
                    if r_in <= dist <= r_out:
                        ang = math.atan2(y - lcy, x - lcx)
                        dot = -0.5 * math.cos(ang - 0.7) - 0.5 * math.sin(ang - 0.7)
                        # Vine scrollwork wave
                        wave = math.cos(ang * 5.0)
                        if dot > 0.35:
                            col = GOLD_SHINE * 0.45 + GOLD_LIGHT * 0.55 + dot * 12.0 + wave * 6.0
                        elif dot > -0.15:
                            col = GOLD_BASE + dot * 16.0 + wave * 4.0
                        else:
                            col = GOLD_DARK + (dot + 0.3) * 12.0
                        key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Central Vine Carved Hub (36, 28) radius 5.0
    for y in range(int(kcy - 5), int(kcy + 6)):
        for x in range(int(kcx - 5), int(kcx + 6)):
            r = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if r <= 5.0:
                dot = -0.6 * (x - kcx) / 5.0 - 0.6 * (y - kcy) / 5.0
                if r <= 2.6:
                    # Coral pink center rivet (#FF5E8A)
                    if r <= 1.2:
                        col = CORAL_SHINE
                    elif dot > 0.1:
                        col = CORAL_LIGHT
                    else:
                        col = CORAL_BASE
                else:
                    # Golden brass bezel
                    col = GOLD_SHINE if dot > 0.3 else (GOLD_LIGHT if dot > -0.2 else GOLD_DARK)
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Specular highlight
    key_img.putpixel((int(kcx - 1), int(kcy - 1)), (255, 255, 255, 255))

    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    多節同軸彈簧平衡背囊與微型排氣風箱 (curio_mantis_spring_pack)
    Segmented Spring Balance Pack & Micro Bellows.
    Positioned along upper back spine (x: 38..56, y: 48..84).
    Consists of:
    - 3-segment articulated stamped brass plates (#FFD028, #4ED86A) with balance spring cables.
    - Micro accordion bellows with sunset orange (#FFA010) & sky blue (#38A0FF) seals.
    - Upper steam exhaust vent nozzle at (39, 52) pointing back-left.
    - Zero biological wings, zero tissue.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Spring Guide Tension Cables (P0=(48, 82), P1=(34, 66), P2=(42, 50))
    for t_step in np.linspace(0.0, 1.0, 60):
        px = (1 - t_step)**2 * 48.0 + 2 * (1 - t_step) * t_step * 34.0 + t_step**2 * 42.0
        py = (1 - t_step)**2 * 82.0 + 2 * (1 - t_step) * t_step * 66.0 + t_step**2 * 50.0
        ix, iy = int(round(px)), int(round(py))
        if 0 <= ix < W and 0 <= iy < H:
            curio_img.putpixel((ix, iy), tuple(STEEL_LIGHT.astype(int)) + (255,))
            if ix + 1 < W:
                curio_img.putpixel((ix + 1, iy), tuple(STEEL_DARK.astype(int)) + (255,))

    # 2. Three Articulated Stamped Brass Balance Segments
    # Segment 1 (Lower): (46.0, 78.0, rx=5.2, ry=5.8)
    # Segment 2 (Mid):   (42.0, 66.0, rx=5.8, ry=6.2)
    # Segment 3 (Upper): (41.0, 54.0, rx=5.5, ry=5.8)
    segments = [
        (46.0, 78.0, 5.2, 5.8, 0.2),
        (42.0, 66.0, 5.8, 6.2, 0.4),
        (41.0, 54.0, 5.5, 5.8, 0.5)
    ]
    for i, (scx, scy, rx, ry, ang) in enumerate(segments):
        for y in range(int(scy - ry - 2), int(scy + ry + 3)):
            for x in range(int(scx - rx - 2), int(scx + rx + 3)):
                if 0 <= x < W and 0 <= y < H:
                    dx = x - scx
                    dy = y - scy
                    rx_rot = dx * math.cos(-ang) - dy * math.sin(-ang)
                    ry_rot = dx * math.sin(-ang) + dy * math.cos(-ang)
                    dist_sq = (rx_rot / rx)**2 + (ry_rot / ry)**2
                    if dist_sq <= 1.0:
                        dot = -0.5 * (rx_rot / rx) - 0.7 * (ry_rot / ry)
                        # Alternating brass and mint green enamel plate
                        if i % 2 == 0:
                            if dot > 0.35:
                                col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6 + dot * 12.0
                            elif dot > 0.0:
                                col = GOLD_BASE + dot * 15.0
                            else:
                                col = GOLD_DARK
                        else:
                            if dot > 0.35:
                                col = MINT_LIGHT + dot * 12.0
                            elif dot > 0.0:
                                col = MINT_BASE + dot * 15.0
                            else:
                                col = MINT_SHADOW

                        # Center joint brass rivet
                        if math.sqrt(rx_rot**2 + ry_rot**2) <= 1.6:
                            col = RUBBER_LIGHT if dot > 0 else RUBBER_DARK

                        curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Micro Accordion Exhaust Bellows (x: 36..46, y: 60..74)
    for by in range(60, 75):
        t_b = (by - 60) / 14.0
        fold = (by % 3 == 0)
        for bx in range(36, 44):
            dot = -0.5 * (bx - 40.0) / 4.0
            if fold:
                col = ORANGE_LIGHT if dot > 0 else ORANGE_BASE
            else:
                col = SKY_LIGHT if dot > 0 else SKY_BASE
            curio_img.putpixel((bx, by), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Upper Steam Exhaust Vent Nozzle at (39, 50)
    nx, ny = 39.0, 50.0
    for y in range(46, 54):
        for x in range(35, 43):
            dist = math.sqrt((x - nx)**2 + (y - ny)**2)
            if dist <= 3.4:
                dot = -0.6 * (x - nx) / 3.4 - 0.6 * (y - ny) / 3.4
                col = GOLD_SHINE if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Tungsten nozzle tip pointing back-left
    for t in range(0, 5):
        px = int(round(nx - 2.0 - t * 0.8))
        py = int(round(ny - 1.0 - t * 0.5))
        if 0 <= px < W and 0 <= py < H:
            curio_img.putpixel((px, py), tuple(STEEL_LIGHT.astype(int)) + (255,))
            if py + 1 < H:
                curio_img.putpixel((px, py + 1), tuple(STEEL_DARK.astype(int)) + (255,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    蔓谷沖壓薄銅螳螂底盤 (chassis_mantis_stock)
    2.2 Chibi Stamped Thinplate Emerald Mint Green (#4ED86A) mantis body.
    Features:
    - STRICT 0-ART9/11: Strictly 0 pixels at x >= 94.
    - STRICT 0-ART18: Bare torso (y: 58..94, x: 44..84) rich multi-tone cel-shading (unique colors >= 20).
    - STRICT 0-ART28q: Color coherence with head_unit (L2 distance < 60.0).
    - Six chibi mechanical crawler legs with anti-slip rubber pads.
    - Left pincer/mantis scythe forearm folded defensively across chest at x: 34..48, y: 58..78.
    - Right arm extending forward to x: 74..93, y: 60..80 ready to grip jade scythe claw.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 0. Neck / Shoulder Transition Block to seal core against holes (x: 46..82, y: 53..61)
    for y in range(53, 62):
        for x in range(46, 83):
            dot = -(x - 64.0) * 0.05 - (y - 57.0) * 0.08
            col = MINT_BASE + dot * 16.0
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
                    col = MINT_SHINE * 0.35 + MINT_LIGHT * 0.65 + dot * 12.0
                elif dot > 0.35:
                    col = MINT_LIGHT + dot * 15.0
                elif dot > 0.05:
                    col = MINT_BASE + dot * 18.0
                elif dot > -0.25:
                    col = MINT_SHADOW + (dot + 0.25) * 16.0
                elif dot > -0.55:
                    col = MINT_DARK + (dot + 0.55) * 14.0
                else:
                    col = MINT_DEEP + (dot + 0.8) * 12.0

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
                col = MINT_SHADOW if abs(dx) < 0.5 else MINT_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Six Mechanical Crawler Legs
    # Left legs (3): (40..52, y: 88..115)
    # Right legs (3): (76..88, y: 88..115) - STRICT x < 94!
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
                                # Mint green thinplate leg armor
                                col = MINT_LIGHT if dot > 0 else MINT_BASE
                            chassis_img.putpixel((ox, oy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Arms & Pincers
    # Left Arm & Folded Mantis Scythe Forearm (x: 34..48, y: 58..78)
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
                    col = GOLD_BASE if dot > 0 else GOLD_DARK
                else:
                    col = MINT_BASE if dot > 0 else MINT_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Folded Scythe Blades (x: 32..42, y: 72..82)
    for y in range(72, 82):
        for x in range(32, 43):
            dx = (x - 37.0) / 4.5
            dy = (y - 77.0) / 4.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.7 * dx - 0.7 * dy
                col = MINT_LIGHT if dot > 0.3 else (MINT_BASE if dot > -0.2 else MINT_DARK)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Arm: extending forward to grip claw (x: 74..93, y: 60..80) - STRICT x < 94!
    for y in range(60, 81):
        t = (y - 60) / 20.0
        rcx = 76.0 + t * 9.0
        for x in range(int(round(rcx - 3.5)), min(94, int(round(rcx + 3.5)))):
            dx = (x - rcx) / 3.5
            if abs(dx) <= 1.0:
                dot = -0.5 * dx - 0.5 * t
                if 66 <= y <= 70:
                    col = GOLD_LIGHT if dot > 0 else GOLD_DARK
                else:
                    col = MINT_LIGHT if dot > 0.3 else (MINT_BASE if dot > -0.2 else MINT_DARK)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Wrist Socket Node at (86..90, y: 72..76)
    for y in range(72, 77):
        for x in range(86, 91):
            if x < 94:
                dist = math.sqrt((x - 88.5)**2 + (y - 74.5)**2)
                if dist <= 2.2:
                    col = GOLD_SHINE if (x - 88.5) < 0 else GOLD_BASE
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

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
    沖壓林冠折角金屬面盔 (head_mantis_canopy_cowl)
    Stamped Canopy Angled Metal Cowl.
    Inverted triangular aerodynamic cowl (#4ED86A mint green) with side cooling louvers & brass trim.
    Dual long spiral brass antenna tuners (#FFD028) with golden indicator spheres.
    Acoustic side cheek grilles on sides ((36, 26) and (92, 26)).
    STRICT 0-ART27: Hollow eye sockets (alpha = 0) at:
      Left eye socket:  x: 50..58, y: 38..46
      Right eye socket: x: 70..78, y: 38..46
    STRICT 0-ART28q: Average plate color distance to chassis L2 < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Acoustic Brass Ear Cones / Side Cheek Louvers on sides ((36, 26) and (92, 26))
    for ex_c, ey_c, is_right in [(36.0, 26.0, False), (92.0, 26.0, True)]:
        ang_rot = math.radians(20.0 if is_right else -20.0)
        cos_e, sin_e = math.cos(ang_rot), math.sin(ang_rot)
        rx, ry = 7.0, 9.0

        for y in range(int(ey_c - ry - 2), int(ey_c + ry + 3)):
            for x in range(int(ex_c - rx - 2), int(ex_c + rx + 3)):
                dx_w = x - ex_c
                dy_w = y - ey_c
                dx_l = dx_w * cos_e + dy_w * sin_e
                dy_l = -dx_w * sin_e + dy_w * cos_e

                dsq = (dx_l / rx)**2 + (dy_l / ry)**2
                if dsq <= 1.0:
                    dist = math.sqrt(dsq)
                    dot = -0.5 * (dx_l / rx) - 0.7 * (dy_l / ry)
                    if dist > 0.75:
                        col = GOLD_SHINE if dot > 0.2 else GOLD_BASE
                    elif dist > 0.45:
                        col = MINT_LIGHT if dot > 0.3 else (MINT_BASE if dot > -0.2 else MINT_SHADOW)
                    else:
                        col = MINT_DARK

                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass pivot hinge at ear root
        hx = ex_c + (3.0 if not is_right else -3.0)
        hy = ey_c + 7.0
        hd.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 2. Main Helmet Dome (x: 44..84, y: 22..60)
    hcx, hcy = 64.0, 41.0
    for y in range(22, 61):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.0
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz

                # Mint green cowl shell (matches chassis for 0-ART28q L2 < 60.0)
                if dot > 0.45:
                    col = MINT_SHINE * 0.4 + MINT_LIGHT * 0.6 + dot * 12.0
                elif dot > 0.10:
                    col = MINT_LIGHT * 0.6 + MINT_BASE * 0.4 + (dot - 0.10) * 25.0
                elif dot > -0.25:
                    col = MINT_BASE + dot * 20.0
                elif dot > -0.55:
                    col = MINT_SHADOW + (dot + 0.55) * 18.0
                else:
                    col = MINT_DARK

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Forehead Inverted Triangular Deflector Brow & Ivory Streamline
    hd.arc([49, 25, 79, 38], start=180, end=360, fill=tuple(IVORY_LIGHT.astype(int)) + (255,), width=2)
    hd.arc([51, 27, 77, 37], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.ellipse([62, 28, 66, 32], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), outline=tuple(ORANGE_DARK.astype(int)) + (255,))

    # 4. Cheek Cooling Louvers ((48, 49) and (80, 49))
    for vx in [48, 80]:
        hd.ellipse([vx - 2, 47, vx + 2, 51], fill=tuple(MINT_DARK.astype(int)) + (255,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
        hd.point((vx, 49), fill=tuple(GOLD_LIGHT.astype(int)) + (255,))

    # 5. Dual Spiral Brass Antennae (#FFD028)
    # Left antenna: root at (57, 24), curving up-left to (44, 8)
    # Right antenna: root at (71, 24), curving up-right to (84, 8)
    antenna_specs = [
        (57.0, 24.0, 50.0, 16.0, 44.0, 8.0, False),
        (71.0, 24.0, 78.0, 16.0, 84.0, 8.0, True)
    ]
    for x0, y0, x1, y1, x2, y2, is_right in antenna_specs:
        hd.ellipse([x0 - 2, y0 - 2, x0 + 2, y0 + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
        for t in np.linspace(0.0, 1.0, 45):
            bx = (1.0 - t)**2 * x0 + 2.0 * (1.0 - t) * t * x1 + t**2 * x2
            by = (1.0 - t)**2 * y0 + 2.0 * (1.0 - t) * t * y1 + t**2 * y2
            for off in [-0.5, 0.5]:
                px = int(round(bx + off))
                py = int(round(by))
                if 0 <= px < W and 0 <= py < H:
                    head_img.putpixel((px, py), tuple(GOLD_LIGHT.astype(int)) + (255,))

        # Polished Golden Sphere Indicator Tip (radius 2.5) at (x2, y2)
        for y in range(int(y2 - 3), int(y2 + 4)):
            for x in range(int(x2 - 3), int(x2 + 4)):
                r = math.sqrt((x - x2)**2 + (y - y2)**2)
                if r <= 2.6:
                    dot = -0.5 * (x - x2) / 2.6 - 0.7 * (y - y2) / 2.6
                    col = GOLD_SHINE if dot > 0.2 else (GOLD_BASE if dot > -0.3 else GOLD_DARK)
                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        head_img.putpixel((int(x2 - 1), int(y2 - 1)), (255, 255, 255, 255))

    # 6. Hollow out eye sockets for optic_core insertion (STRICT 0-ART27)
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
    蔓谷藤蔓鉚接生漆板甲胸甲 (costume_mantis_vine_plate)
    Vine-Laced Brass Plate Cuirass.
    Stamped thinplate mint green (#4ED86A) and brass (#FFD028) cuirass with vine relief,
    dopamine sky blue (#38A0FF) and sunset orange (#FFA010) inspection sashes,
    polished brass gear chest medallion (#FFD028) at center (64, 73).
    STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # 1. Main Cuirass Shell (x: 48..80, y: 62..93)
    ccx, ccy = 64.0, 76.0
    for y in range(62, 94):
        for x in range(48, 81):
            dx = (x - ccx) / 15.5
            dy = (y - ccy) / 14.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                if dot > 0.40:
                    col = MINT_SHINE * 0.3 + MINT_LIGHT * 0.7 + dot * 10.0
                elif dot > 0.05:
                    col = MINT_BASE + dot * 15.0
                elif dot > -0.30:
                    col = MINT_SHADOW + (dot + 0.30) * 12.0
                else:
                    col = MINT_DARK

                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Vine Filigree Relief across breastplate
    for y in range(65, 88):
        for x in range(50, 79):
            dx = x - ccx
            wave = math.sin(dx * 0.4) * 3.0 + 74.0
            if abs(y - wave) < 1.4:
                dot = -0.5 * dx / 15.0
                col = VINE_LIGHT if dot > 0 else VINE_BASE
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Dopamine Inspection Sashes:
    # Sky blue sash running diagonal from (52, 63) to (76, 88)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 52.0 * (1.0 - t) + 76.0 * t
        sy = 63.0 * (1.0 - t) + 88.0 * t
        for off in [-1.0, 0.0, 1.0]:
            px = int(round(sx - off * 0.7))
            py = int(round(sy + off * 0.7))
            if 0 <= px < W and 0 <= py < 96:
                costume_img.putpixel((px, py), tuple(SKY_BASE.astype(int)) + (255,))

    # Sunset orange safety stripe running diagonal from (76, 63) to (52, 88)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 76.0 * (1.0 - t) + 52.0 * t
        sy = 63.0 * (1.0 - t) + 88.0 * t
        for off in [-0.8, 0.0, 0.8]:
            px = int(round(sx + off * 0.7))
            py = int(round(sy + off * 0.7))
            if 0 <= px < W and 0 <= py < 96:
                costume_img.putpixel((px, py), tuple(ORANGE_BASE.astype(int)) + (255,))

    # 4. Central Polished Brass Gear Chest Medallion at (64, 73) radius 5.5
    for y in range(67, 80):
        for x in range(58, 71):
            r = math.sqrt((x - 64.0)**2 + (y - 73.0)**2)
            if r <= 5.5:
                ang = math.atan2(y - 73.0, x - 64.0)
                tooth = (math.cos(6.0 * ang) > 0.0) or (r <= 3.8)
                if tooth:
                    dot = -0.5 * (x - 64.0) / 5.5 - 0.7 * (y - 73.0) / 5.5
                    if r <= 2.2:
                        col = SKY_LIGHT if dot > 0 else SKY_BASE
                    else:
                        col = GOLD_SHINE if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                    costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 5. Quick-Release Brass Buckles & Belt Trim at waist (y: 90..94)
    for bx in [54, 74]:
        cd.rectangle([bx - 2, 89, bx + 2, 93], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # STRICT 0-ART26b check: clear all y >= 96
    arr = np.array(costume_img)
    arr[96:, :, :] = 0
    clean_costume = Image.fromarray(arr, "RGBA")

    out_costume = apply_antialiased_outline(clean_costume, outline_color=OUTLINE, min_alpha=50)

    # Re-enforce y >= 96 is strictly 0 after outline pass
    arr_out = np.array(out_costume)
    arr_out[96:, :, :] = 0
    return Image.fromarray(arr_out, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=30)
    雙聯高透翡翠石英琉璃球形目鏡 (face_mantis_emerald_goggles)
    Dual Spherical High-Clarity Emerald Quartz Glass Goggles.
    Centers:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    Surrounded by anti-glare dark indigo-violet eyemask frames (#1F1A3A),
    glowing emerald quartz (#4ED86A), sky blue (#38A0FF) reticle & dawn gold (#FFD028) highlights.
    STRICT 0-ART27: Center alpha MUST BE 255.
    Hollow sockets 100% covered by dark frame + crystal, zero holes.
    """
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    eye_centers = [(54, 42), (74, 42)]
    radius = 4.3

    for cx, cy in eye_centers:
        # 1. Fill entire socket rectangle with dark anti-glare eyemask frame (#1F1A3A)
        cored.rounded_rectangle([cx - 4, cy - 4, cx + 4, cy + 4], radius=1, fill=tuple(OUTLINE.astype(int)) + (255,))

        # 2. Spherical Emerald Quartz Lens inside frame
        for y in range(int(cy - radius), int(cy + radius + 1)):
            for x in range(int(cx - radius), int(cx + radius + 1)):
                dx = (x - cx) / radius
                dy = (y - cy) / radius
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.25:
                        col = GOLD_SHINE * 0.5 + MINT_SHINE * 0.5
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = MINT_LIGHT * (1.0 - t) + MINT_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = SKY_BASE * (1.0 - t) + MINT_DARK * t + dot * 12.0
                    else:
                        col = OUTLINE * 0.5 + MINT_DEEP * 0.5
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Concentric reticle lines & warm focus dots
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(SKY_LIGHT.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(SKY_LIGHT.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(WHITE_SHINE.astype(int)) + (255,))

        # Specular white reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(GOLD_BASE.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    翠刃連斬機關爪 (weapon_mantis_scythe_claw)
    Jade Scythe Claw (Monk Martial Artist Claw).
    Held in right hand, extending from hand socket (86, 74) forward and up-right (x: 76..114, y: 50..86).
    Triple folded cold-rolled steel blades with miniature eccentric cam gear bearing (#FFD028, #FFA010)
    and tungsten tips (#STEEL_LIGHT, #STEEL_BASE).
    Zero body or arm baked into weapon (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Eccentric Cam Bearing Hub at hand grip (87, 73) radius 5.2
    bcx, bcy = 87.0, 73.0
    for y in range(int(bcy - 6), int(bcy + 7)):
        for x in range(int(bcx - 6), int(bcx + 7)):
            r = math.sqrt((x - bcx)**2 + (y - bcy)**2)
            if r <= 5.2:
                dot = -0.6 * (x - bcx) / 5.2 - 0.6 * (y - bcy) / 5.2
                if r <= 2.2:
                    col = ORANGE_SHINE if dot > 0 else ORANGE_BASE
                else:
                    col = GOLD_SHINE if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Triple Folded Scythe Blades:
    # Blade 1 (Upper Sickle): from (88, 70) curving to tip at (108, 52)
    # Blade 2 (Main Forward): from (90, 73) curving to tip at (114, 68)
    # Blade 3 (Lower Scythe): from (88, 76) curving to tip at (106, 84)
    blade_specs = [
        # (root_x, root_y, ctrl_x, ctrl_y, tip_x, tip_y, max_width)
        (88.0, 70.0, 96.0, 56.0, 108.0, 52.0, 3.6),
        (90.0, 73.0, 102.0, 68.0, 114.0, 68.0, 4.2),
        (88.0, 76.0, 96.0, 82.0, 106.0, 84.0, 3.4),
    ]

    for rx0, ry0, cx0, cy0, tx0, ty0, max_w in blade_specs:
        for t in np.linspace(0.0, 1.0, 60):
            # Quadratic bezier curve
            bx = (1 - t)**2 * rx0 + 2 * (1 - t) * t * cx0 + t**2 * tx0
            by = (1 - t)**2 * ry0 + 2 * (1 - t) * t * cy0 + t**2 * ty0
            cur_w = max_w * (1.0 - t * 0.7)

            # Normal vector
            tang_x = 2 * (1 - t) * (cx0 - rx0) + 2 * t * (tx0 - cx0)
            tang_y = 2 * (1 - t) * (cy0 - ry0) + 2 * t * (ty0 - cy0)
            norm_len = math.sqrt(tang_x**2 + tang_y**2) + 1e-4
            nx = -tang_y / norm_len
            ny = tang_x / norm_len

            for off in np.linspace(-cur_w, cur_w, 15):
                px = int(round(bx + off * nx))
                py = int(round(by + off * ny))
                if 0 <= px < W and 0 <= py < H:
                    dist = abs(off) / (cur_w + 1e-4)
                    dot = -0.5 * nx * (off / (cur_w + 1e-4)) - 0.5 * ny
                    if dist < 0.35:
                        col = STEEL_SHINE if dot > 0 else STEEL_LIGHT
                    elif dist < 0.75:
                        col = MINT_LIGHT if dot > 0.2 else MINT_BASE
                    else:
                        col = STEEL_BASE if dot > -0.2 else STEEL_DARK

                    # Golden spine trim near root
                    if t < 0.4 and dist < 0.5:
                        col = GOLD_LIGHT if dot > 0 else GOLD_BASE

                    weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_mantis_slices():
    print("=== BUILDING JADE MANTIS 7 PAPERDOLL SLICES ===")

    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_mantis_vine_brass", key_img),
        ("back_curio", "curio_mantis_spring_pack", curio_img),
        ("chassis", "chassis_mantis_stock", chassis_img),
        ("head_unit", "head_mantis_canopy_cowl", head_img),
        ("costume", "costume_mantis_vine_plate", costume_img),
        ("optic_core", "face_mantis_emerald_goggles", core_img),
        ("weapon", "weapon_mantis_scythe_claw", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{MANTIS_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_mantis_vine_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_mantis_vine_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_mantis_scythe_claw.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_mantis_scythe_claw_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    ordered_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_im in ordered_slices:
        composite.alpha_composite(s_im)

    proof_comp = f"{MANTIS_PD_DIR}/proof_paperdoll_mantis_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{MANTIS_PD_DIR}/proof_paperdoll_mantis_magenta.png"
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

    strip_path = f"{MANTIS_PD_DIR}/proof_mantis_all_7_slices.png"
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
    p_idle_x3 = f"{PLAYER_DIR}/mantis_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    p_idle_64 = f"{PLAYER_DIR}/mantis_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/mantis_idle.png"
    idle_with_shadow.save(p_party_idle)

    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/mantis_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/mantis_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # Compatibility symlink: game/assets/sprites/player/mantis -> paperdoll/mantis
    mantis_alias_dir = f"{PLAYER_DIR}/mantis"
    if os.path.exists(mantis_alias_dir):
        if os.path.islink(mantis_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/mantis -> paperdoll/mantis already exists")
        else:
            files = os.listdir(mantis_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(mantis_alias_dir, f))
                os.rmdir(mantis_alias_dir)
                os.symlink("paperdoll/mantis", mantis_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/mantis -> paperdoll/mantis")
    else:
        try:
            os.symlink("paperdoll/mantis", mantis_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/mantis -> paperdoll/mantis")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL JADE MANTIS PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_mantis_slices()
