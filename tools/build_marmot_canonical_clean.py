#!/usr/bin/env python3
"""
build_marmot_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十五族 碎石旱獺 (The Rockbreaker Marmot, marmot) 7 Paperdoll Slices.
Follows:
- docs/world/ROCKBREAKER_MARMOT_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, weathered tinplate chassis #5A6E7F / #FFFDF8,
  alloy chisel visor helmet with prominent cold-rolled brass chisel buckteeth #FFD028,
  amber dust goggles optic core #FFA010/#FFD028,
  scavenger work harness cuirass with hazard warning stripes #D49B4B/#FFA010/#FFD028,
  cylindrical pneumatic sand-exhaust tail #5A6E7F/#4ED86A,
  dual-pawl cog-shaped brass wind-up key with center coral pink rivet #FFD028/#FF5E8A,
  dual eccentric piston boxing gauntlets #FFA010/#FFD028/#38A0FF)
- references/art_direction.md & references/brand_assets.md
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
- High-depth multi-tone cel-shading (>= 3 steps per slot, metal highlights & shadow bevels)
- Subpixel anti-aliased silhouette borders (alpha levels > 2)
- chassis 128 unique colors >= 120, all 7 slots c/100px >= 3.0%
- proof composite unique colors >= 300, core holes <= 0px, head vs chassis color L2 < 60.0
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARMOT_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/marmot"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Rockbreaker Marmot Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Primary Metal / Weathered Tinplate Iron (#5A6E7F)
TIN_SHINE  = np.array([215, 230, 245], dtype=float)
TIN_LIGHT  = np.array([135, 160, 185], dtype=float)
TIN_BASE   = np.array([90, 110, 127], dtype=float)
TIN_SHADOW = np.array([68, 85, 100], dtype=float)
TIN_DARK   = np.array([45, 58, 70], dtype=float)
TIN_DEEP   = np.array([32, 42, 52], dtype=float)

# 2. Secondary Ivory Shock Absorber Plate & High-impact Bevels (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)

# 3. Dopamine Sunset Warm Orange (#FFA010) - Piston Cylinders, Warning Hazard Stripes, Amber Glow
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 4. Dopamine Forged Brass & Golden Chisel Teeth (#FFD028) - Dual-Pawl Key, Buckteeth, Anvil Striking Face
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 5. Weathered Tan Canvas (#D49B4B) - Scavenger Work Harness Cuirass
CANVAS_SHINE = np.array([245, 215, 165], dtype=float)
CANVAS_LIGHT = np.array([230, 185, 115], dtype=float)
CANVAS_BASE  = np.array([212, 155, 75], dtype=float)
CANVAS_DARK  = np.array([165, 115, 45], dtype=float)
CANVAS_DEEP  = np.array([120, 80, 28], dtype=float)

# 6. Dopamine Mint Green (#4ED86A) - Pneumatic Exhaust Indicator Ring, Pressure Gauge
MINT_SHINE = np.array([195, 255, 215], dtype=float)
MINT_LIGHT = np.array([135, 242, 165], dtype=float)
MINT_BASE  = np.array([78, 216, 106], dtype=float)
MINT_DARK  = np.array([42, 160, 68], dtype=float)
MINT_DEEP  = np.array([22, 105, 42], dtype=float)

# 7. Dopamine Sky Blue (#38A0FF) - Quick Release Buckle, Gauntlet Damping Pads
SKY_SHINE = np.array([205, 238, 255], dtype=float)
SKY_LIGHT = np.array([135, 210, 255], dtype=float)
SKY_BASE  = np.array([56, 160, 255], dtype=float)
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([15, 60, 130], dtype=float)

# 8. Dopamine Coral Pink (#FF5E8A) - Key Center Rivet, Pressure Gasket
CORAL_SHINE = np.array([255, 210, 230], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 9. Deep Indigo-Black / Anti-Glare Mask (#1A243B) - Goggle Metal Bezels
SPACE_SHINE = np.array([75, 92, 122], dtype=float)
SPACE_BASE  = np.array([26, 36, 59], dtype=float)
SPACE_DARK  = np.array([16, 22, 38], dtype=float)

WHITE_SHINE = np.array([255, 255, 255], dtype=float)


def apply_antialiased_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=50, ignore_regions=None) -> Image.Image:
    """
    Applies a clean 1px dark outline with smooth anti-aliasing on the outer boundary.
    - Solid interior remains solid (alpha=255).
    - Outline pixels bordering transparent space receive fractional alpha (50..225).
    - Guarantees alpha levels > 2 (anti-aliasing).
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
    雙向棘爪減速黃銅發條鑰匙 (key_marmot_dual_pawl_brass)
    Dual-Pawl Clockwise Brass Wind-up Key.
    Central axle extending from chassis socket (46, 50) to key center (38, 28).
    Heavy forged cog-shaped key handle with 6 outer ratchet teeth (radii 11..18).
    Dual pawl ratchet mechanism and central coral pink rivet (#FF5E8A) with brass bezel.
    Warm golden bronze outline OUTLINE_KEY.
    Strictly follows 0-ART29 & 0-QA16: no dark block run >= 13, white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    kcx, kcy = 38.0, 28.0

    # 1. Axle connecting chassis socket (46, 50) to key center (38, 28)
    for t in np.linspace(0.0, 1.0, 32):
        ax = 46.0 * (1.0 - t) + kcx * t
        ay = 50.0 * (1.0 - t) + kcy * t
        for off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(ax + off * 0.8))
            py = int(round(ay - off * 0.6))
            if 0 <= px < W and 0 <= py < H:
                dot = off / 1.5
                col = GOLD_LIGHT if dot > 0.2 else (GOLD_BASE if dot > -0.4 else GOLD_DARK)
                key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Cog-shaped Ratchet Key Ring (6 gear teeth)
    # Base circle r = 10..15, Teeth extend to r = 18
    num_teeth = 6
    for y in range(int(kcy - 19), int(kcy + 20)):
        for x in range(int(kcx - 19), int(kcx + 20)):
            dx = x - kcx
            dy = y - kcy
            r = math.sqrt(dx**2 + dy**2)
            if r < 5.5:
                continue
            ang = math.atan2(dy, dx)
            # Ratchet tooth profile: saw-tooth / cog shape
            tooth_mod = (ang * num_teeth / (2.0 * math.pi)) % 1.0
            r_max = 14.5 + (3.5 if tooth_mod < 0.65 else 0.5)

            if 8.5 <= r <= r_max:
                dot = -0.55 * (dx / r) - 0.70 * (dy / r)
                # Shading with dopamine gold and brass highlights
                if dot > 0.40:
                    col = GOLD_SHINE * 0.5 + GOLD_LIGHT * 0.5
                elif dot > 0.05:
                    col = GOLD_BASE + dot * 20.0
                elif dot > -0.35:
                    col = GOLD_DARK + (dot + 0.35) * 15.0
                else:
                    col = GOLD_DEEP
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Dual Ratchet Pawls at angles (-45 deg and 135 deg)
    pawl_angles = [-math.pi / 4.0, math.pi * 3.0 / 4.0]
    for ang in pawl_angles:
        cos_a = math.cos(ang)
        sin_a = math.sin(ang)
        for r_step in np.linspace(6.0, 16.0, 25):
            sx = kcx + r_step * cos_a
            sy = kcy + r_step * sin_a
            for perp in [-0.8, 0.0, 0.8]:
                px = int(round(sx - perp * sin_a))
                py = int(round(sy + perp * cos_a))
                if 0 <= px < W and 0 <= py < H:
                    col = GOLD_LIGHT if perp < 0 else GOLD_BASE
                    key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Central Coral Pink Rivet (#FF5E8A) with brass bezel at (38, 28)
    for y in range(int(kcy - 4), int(kcy + 5)):
        for x in range(int(kcx - 4), int(kcx + 5)):
            r = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if r <= 4.2:
                dot = -0.6 * (x - kcx) / 4.2 - 0.6 * (y - kcy) / 4.2
                if r <= 2.5:
                    col = CORAL_SHINE if dot > 0.3 else (CORAL_BASE if dot > -0.3 else CORAL_DARK)
                else:
                    col = GOLD_SHINE if dot > 0.3 else GOLD_BASE
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    key_img.putpixel((int(kcx - 1), int(kcy - 1)), (255, 255, 255, 255))

    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    減震氣動平衡排砂尾 (curio_marmot_pneumatic_sand_tail)
    Pneumatic Sand Exhaust Tail.
    Cylindrical pneumatic exhaust tail mounted to lower rump (48, 88), extending down-left to (28, 96).
    Length ~22px, stamped weathered tinplate cylinder (#5A6E7F),
    mint green indicator ring (#4ED86A), brass cyclone exhaust hood (#FFD028).
    Puffs of micro steam/sand pressure relief.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Base at (48, 88), Tip at (26, 96)
    p_base = np.array([48.0, 88.0])
    p_tip  = np.array([26.0, 96.0])

    num_samples = 80
    curve_pts = []
    for t in np.linspace(0.0, 1.0, num_samples):
        # Slight downward arch
        mid_drop = 3.0 * math.sin(t * math.pi)
        pt = (1.0 - t) * p_base + t * p_tip + np.array([0.0, mid_drop])
        curve_pts.append(pt)

    # Render cylindrical body along the spine
    for i, pt in enumerate(curve_pts):
        t_val = i / float(num_samples)
        radius = 5.2 * (1.0 - t_val * 0.25)

        if i < num_samples - 1:
            tangent = curve_pts[i + 1] - pt
        else:
            tangent = pt - curve_pts[i - 1]
        t_len = np.linalg.norm(tangent) + 1e-6
        normal = np.array([-tangent[1], tangent[0]]) / t_len

        # Cylinder segments: base metal -> mint ring (t=0.6..0.75) -> brass tip (t=0.85..1.0)
        is_mint = (0.58 <= t_val <= 0.74)
        is_brass_tip = (t_val > 0.85)

        for off in np.linspace(-radius, radius, 17):
            s_pt = pt + normal * off
            px, py = int(round(s_pt[0])), int(round(s_pt[1]))
            if 0 <= px < W and 0 <= py < H:
                dist = abs(off) / radius
                dot = -0.55 * (normal[0] * (off / radius)) - 0.70 * (normal[1] * (off / radius))

                if is_mint:
                    if dist < 0.35:
                        col = MINT_SHINE
                    elif dist < 0.75:
                        col = MINT_LIGHT + dot * 15.0
                    else:
                        col = MINT_BASE + dot * 10.0
                elif is_brass_tip:
                    if dist < 0.35:
                        col = GOLD_SHINE
                    elif dist < 0.75:
                        col = GOLD_LIGHT + dot * 15.0
                    else:
                        col = GOLD_BASE
                else:
                    # Tinplate iron
                    if dist < 0.35:
                        col = TIN_SHINE * 0.4 + TIN_LIGHT * 0.6
                    elif dist < 0.75:
                        col = TIN_BASE + dot * 15.0
                    else:
                        col = TIN_SHADOW + dot * 12.0

                curio_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Tip Cyclone Exhaust Nozzle Cap at (25, 96)
    tcx, tcy = 25.0, 96.0
    for y in range(int(tcy - 4), int(tcy + 5)):
        for x in range(int(tcx - 4), int(tcx + 5)):
            r = math.sqrt((x - tcx)**2 + (y - tcy)**2)
            if r <= 3.8:
                dot = -0.55 * (x - tcx) / 3.8 - 0.70 * (y - tcy) / 3.8
                col = GOLD_SHINE if dot > 0.35 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    out_curio = apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)

    # Soft steam / sand exhaust dust puff behind tail (translucent, no black outline)
    puffs = [(20.0, 96.0, 4.0), (14.0, 97.0, 3.0)]
    for gx, gy, gr in puffs:
        for y in range(int(gy - gr - 1), int(gy + gr + 2)):
            for x in range(int(gx - gr - 1), int(gx + gr + 2)):
                dist = math.sqrt((x - gx)**2 + (y - gy)**2)
                if dist <= gr and 0 <= x < W and 0 <= y < H:
                    alpha = int(np.clip((1.0 - dist / gr) * 80.0, 0, 90))
                    curr = out_curio.getpixel((x, y))
                    if curr[3] == 0:
                        out_curio.putpixel((x, y), tuple(ORANGE_LIGHT.astype(int)) + (alpha,))

    return out_curio


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    碎石耐磨馬口鐵底盤 (chassis_marmot_quarry_tinplate_default)
    2.2 head-body ratio chibi marmot chassis, weathered tinplate iron (#5A6E7F / TIN),
    wide horse stance (扎馬步抱樁微屈膝), ivory belly shock absorber plate (#FFFDF8 / IVORY),
    tungsten ball-joints, anti-slip brass rivets on foot soles.
    Forearms held in ready boxing guard in front of chest.
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    STRICT 0-ART18: Bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Ground contact shadow (y: 114..120)
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.1))

    # 2. Sturdy Legs & Brass Riveted Feet (y: 94..113)
    # Left foot: centered at (48, 107), Right foot: centered at (78, 107)
    for bx, by in [(48.0, 107.0), (78.0, 107.0)]:\
        # Lower leg tinplate cylinder
        for y in range(int(by - 14), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.5
                dy = (y - (by - 7.5)) / 7.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    if dot > 0.35:
                        col = TIN_LIGHT + dot * 12.0
                    elif dot > -0.2:
                        col = TIN_BASE + dot * 16.0
                    else:
                        col = TIN_SHADOW + dot * 14.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Cold-rolled tungsten knee joint sphere (sky blue/brass accent)
        for y in range(int(by - 12), int(by - 6)):
            for x in range(int(bx - 4), int(bx + 5)):
                if (x - bx)**2 + (y - (by - 9.0))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 9.0) / 3.0
                    col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Foot Sole Plate (Wide anti-slip stamped iron sole)
        for y in range(int(by - 4), int(by + 7)):
            for x in range(int(bx - 9), int(bx + 10)):
                dx = (x - bx) / 8.5
                dy = (y - by) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    col = TIN_LIGHT if dot > 0.3 else (TIN_BASE if dot > -0.3 else TIN_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Anti-slip brass grip rivets on foot sole (3 rivets per foot)
        for rx_off in [-5, 0, 5]:
            chd.ellipse([bx + rx_off - 1, by + 4, bx + rx_off + 1, by + 6], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 3. Main Torso Chassis (y: 58..95, x: 44..84)
    # Chunky 2.2 head-body ratio tinplate body
    tcx, tcy = 64.0, 76.0
    for y in range(58, 96):
        for x in range(44, 85):
            dx = (x - tcx) / 19.0
            dy = (y - tcy) / 17.0
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz

                # Multi-tone depth cel-shading (0-ART18: rich unique colors >= 10)
                if dot > 0.50:
                    col = TIN_SHINE * 0.4 + TIN_LIGHT * 0.6 + dot * 10.0
                elif dot > 0.20:
                    col = TIN_LIGHT * 0.7 + TIN_BASE * 0.3 + (dot - 0.20) * 25.0
                elif dot > -0.15:
                    col = TIN_BASE + dot * 20.0
                elif dot > -0.45:
                    col = TIN_SHADOW + (dot + 0.45) * 20.0
                else:
                    col = TIN_DARK + (dot + 0.65) * 15.0

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Belly Ivory Cream White Shock Absorber Plate (#FFFDF8)
    for y in range(65, 92):
        for x in range(52, 77):
            dx = (x - tcx) / 11.5
            dy = (y - (tcy + 2.0)) / 12.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                if dot > 0.30:
                    col = IVORY_SHINE * 0.5 + IVORY_LIGHT * 0.5
                elif dot > -0.10:
                    col = IVORY_LIGHT * 0.6 + IVORY_BASE * 0.4
                else:
                    col = IVORY_SHADOW
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Rivet lines and panel grooves on belly plate
    chd = ImageDraw.Draw(chassis_img)
    chd.line([(64, 67), (64, 89)], fill=tuple(TIN_DARK.astype(int)) + (255,), width=1)
    chd.line([(55, 77), (73, 77)], fill=tuple(TIN_DARK.astype(int)) + (255,), width=1)
    for ry in [71, 79, 87]:
        for rx in [56, 72]:
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 5. Shoulders & Forearms in Martial Arts Boxing Guard:
    # Left Arm: held inward in front of chest (x: 37..48, y: 66..82)
    for y in range(66, 83):
        for x in range(37, 49):
            dx = (x - 43.0) / 5.5
            dy = (y - 74.5) / 8.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = TIN_LIGHT if dot > 0.3 else (TIN_BASE if dot > -0.2 else TIN_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Wrist joint node (x: 42..46, y: 74..78)
    chd.ellipse([42, 74, 46, 78], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Right Arm: held in forward boxing guard (x: 79..91, y: 66..81)
    # STRICT 0-ART9/11: x MUST NOT exceed 93!
    for y in range(66, 81):
        for x in range(79, 92):
            dx = (x - 85.0) / 5.5
            dy = (y - 73.5) / 7.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = TIN_LIGHT if dot > 0.3 else (TIN_BASE if dot > -0.2 else TIN_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Wrist joint node (x: 85..89, y: 72..76)
    chd.ellipse([85, 72, 89, 76], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

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
    雙聯合金鑿齒護目面罩 (head_marmot_alloy_chisel_visor)
    Alloy Chisel Visor Helmet.
    Half-sphere stamped tinplate helmet dome (#5A6E7F / TIN),
    prominent cold-rolled brass chisel buckteeth (#FFD028 / GOLD),
    acoustic hemisphere ear cups on sides ((36, 26) and (92, 26)),
    sand-filter vents on cheeks.
    STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
      Left eye:  x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    STRICT 0-ART28q: Average plate color distance to chassis L2 < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Hemisphere Brass Acoustic Ear Cups on Top/Sides ((36, 26) and (92, 26))
    for ex_c, ey_c, is_right in [(36.0, 26.0, False), (92.0, 26.0, True)]:
        ang_rot = math.radians(20.0 if is_right else -20.0)
        cos_e, sin_e = math.cos(ang_rot), math.sin(ang_rot)
        rx, ry = 7.5, 9.5

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
                    # Brass rim with tinplate inner concavity
                    if dist > 0.75:
                        col = GOLD_SHINE if dot > 0.2 else GOLD_BASE
                    elif dist > 0.45:
                        col = TIN_LIGHT if dot > 0.3 else (TIN_BASE if dot > -0.2 else TIN_SHADOW)
                    else:
                        col = TIN_DARK

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

                # Weathered tinplate helmet shell (matches chassis for 0-ART28q L2 < 60.0)
                if dot > 0.45:
                    col = TIN_SHINE * 0.4 + TIN_LIGHT * 0.6 + dot * 12.0
                elif dot > 0.10:
                    col = TIN_LIGHT * 0.6 + TIN_BASE * 0.4 + (dot - 0.10) * 25.0
                elif dot > -0.25:
                    col = TIN_BASE + dot * 20.0
                elif dot > -0.55:
                    col = TIN_SHADOW + (dot + 0.55) * 18.0
                else:
                    col = TIN_DARK

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Forehead Reinforcement Arch & Ivory Brow Ridge
    hd = ImageDraw.Draw(head_img)
    hd.arc([49, 25, 79, 38], start=180, end=360, fill=tuple(IVORY_LIGHT.astype(int)) + (255,), width=2)
    hd.arc([51, 27, 77, 37], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.ellipse([62, 28, 66, 32], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), outline=tuple(ORANGE_DARK.astype(int)) + (255,))

    # 4. Cheek Sand-Filter Vents ((48, 49) and (80, 49))
    for vx in [48, 80]:
        hd.ellipse([vx - 2, 47, vx + 2, 51], fill=tuple(TIN_DARK.astype(int)) + (255,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
        hd.point((vx, 49), fill=tuple(MINT_LIGHT.astype(int)) + (255,))

    # 5. Prominent Cold-Rolled Brass Chisel Buckteeth (#FFD028)
    # Extending from lower jaw (y: 53..61) at x: 60..63 (left) and x: 65..68 (right)
    # Iconic marmot chisel teeth!
    for tooth_x1, tooth_x2 in [(60, 63), (65, 68)]:
        for ty in range(53, 62):
            for tx in range(tooth_x1, tooth_x2 + 1):
                dot = -0.5 * ((tx - tooth_x1) / 3.0) - 0.7 * ((ty - 53) / 8.0)
                if ty >= 59:
                    # Sharp chisel cutting edge (brilliant gold shine)
                    col = GOLD_SHINE
                elif dot > 0.2:
                    col = GOLD_LIGHT
                else:
                    col = GOLD_BASE
                head_img.putpixel((tx, ty), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        # Chisel bevel line
        hd.line([(tooth_x1, 60), (tooth_x2, 60)], fill=tuple(WHITE_SHINE.astype(int)) + (255,), width=1)

    # 6. Hollow out eye sockets for optic_core insertion (0-ART27)
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
    舊庫拾荒加固帆布工裝胸甲 (costume_marmot_scavenger_canvas_harness)
    Scavenger Work Harness Cuirass.
    Weathered tan canvas (#D49B4B) with galvanized tinplate chest guard (#5A6E7F),
    vibrant sunset orange (#FFA010) and dopamine gold (#FFD028) hazard warning stripes across chest,
    central pressure dial with mint pointer (#4ED86A), sky blue quick-release buckle (#38A0FF).
    STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # Harness Cuirass Body: from y=62 to y=94 (strictly decoupled at y < 96)
    for y in range(62, 95):
        if y < 74:
            x_min = 52 - int((y - 62) * 0.35)
            x_max = 76 + int((y - 62) * 0.35)
        else:
            x_min = 48 - int((y - 74) * 0.20)
            x_max = 80 + int((y - 74) * 0.20)

        for x in range(x_min, x_max + 1):
            dx = (x - 64.0) / ((x_max - x_min) / 2.0)
            dy = (y - 78.0) / 16.0
            dot = -0.55 * dx - 0.70 * dy

            # Weathered tan canvas texture & shading
            if dot > 0.40:
                col = CANVAS_SHINE * 0.4 + CANVAS_LIGHT * 0.6
            elif dot > 0.0:
                col = CANVAS_BASE + dot * 20.0
            elif dot > -0.35:
                col = CANVAS_DARK + (dot + 0.35) * 18.0
            else:
                col = CANVAS_DEEP

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Diagonal Hazard Warning Stripes (#FFA010 Orange and #FFD028 Gold) across chest
    cd.line([(53, 65), (64, 79)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    cd.line([(75, 65), (64, 79)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=2)
    cd.line([(49, 92), (79, 92)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=2)

    # Center Pressure Gauge & Coral Pink Valve Gasket at (64, 78)
    cd.ellipse([60, 74, 68, 82], fill=tuple(SPACE_BASE.astype(int)) + (255,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
    cd.ellipse([62, 76, 66, 80], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    # Mint green pressure gauge pointer
    cd.line([(64, 78), (66, 76)], fill=tuple(MINT_LIGHT.astype(int)) + (255,), width=1)
    costume_img.putpixel((64, 77), (255, 255, 255, 255))

    # Sky Blue Metallic Quick-Release Clasp at waist (64, 88)
    cd.rounded_rectangle([61, 86, 67, 90], radius=1, fill=tuple(SKY_LIGHT.astype(int)) + (255,), outline=tuple(SKY_DARK.astype(int)) + (255,))

    # Shoulder Straps with Brass Rivets
    for sx_c in [52, 76]:
        cd.ellipse([sx_c - 2, 63, sx_c + 2, 67], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    out_costume = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)

    # STRICT 0-ART26b check: enforce y >= 96 is completely zeroed out
    arr = np.array(out_costume)
    arr[96:, :, :] = 0
    return Image.fromarray(arr, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=30)
    雙聯琥珀防塵石英風鏡 (face_marmot_amber_dust_goggles)
    Amber Dust Goggles Optic Core.
    Pair of large round amber dust goggles inserted into head_unit eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    Surrounded by anti-glare dark indigo-violet eyemask frames (#1F1A3A),
    glowing amber/gold quartz lenses with concentric reticle lines & warm glow.
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

        # 2. Spherical Amber Dust Goggle Quartz lens inside frame
        for y in range(int(cy - radius), int(cy + radius + 1)):
            for x in range(int(cx - radius), int(cx + radius + 1)):
                dx = (x - cx) / radius
                dy = (y - cy) / radius
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.25:
                        col = ORANGE_SHINE
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = ORANGE_LIGHT * (1.0 - t) + ORANGE_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = ORANGE_BASE * (1.0 - t) + ORANGE_DARK * t + dot * 12.0
                    else:
                        col = ORANGE_DEEP * 0.7 + OUTLINE * 0.3
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Concentric reticle lines & gold crosshair dots
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(ORANGE_SHINE.astype(int)) + (255,))

        # Specular white reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(GOLD_BASE.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    廢土偏心衝壓機關拳套 (weapon_marmot_eccentric_piston_fists)
    Eccentric Piston Boxing Gauntlets.
    Follows 0-MKT7: Symmetrical paired boxing gauntlets with primary/secondary pose:
      1. Primary Gauntlet (Right Fist, forward punch guard):
         Centered over right wrist at (86, 73).
         Stamped weathered tinplate cuff (#5A6E7F),
         oversized sunset orange piston cylinder (#FFA010) with sky blue damping pad (#38A0FF),
         dual-layer forged gold steel anvil striking face (#FFD028).
      2. Secondary Gauntlet (Left Fist, defensive body guard):
         Centered over left wrist at (44, 76).
         Matching orange cylinder, forged gold anvil face, micro pressure relief valve.
    Zero body or arm baked into weapon (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # ─────────────────────────────────────────────────────────────
    # 1. Primary Gauntlet (Right Fist at 86, 73)
    # ─────────────────────────────────────────────────────────────
    rcx, rcy = 86.0, 73.0

    # Piston Cylinder Chamber (Orange #FFA010) - bounds (80..92, 67..79)
    for y in range(int(rcy - 6), int(rcy + 7)):
        for x in range(int(rcx - 6), int(rcx + 7)):
            dx = (x - rcx) / 5.5
            dy = (y - rcy) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.40:
                    col = ORANGE_SHINE * 0.4 + ORANGE_LIGHT * 0.6
                elif dot > 0.0:
                    col = ORANGE_BASE + dot * 20.0
                elif dot > -0.35:
                    col = ORANGE_DARK + (dot + 0.35) * 18.0
                else:
                    col = ORANGE_DEEP
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Heavy Forged Brass Anvil Striking Face (#FFD028) at fist front (87..92, 70..76)
    for y in range(int(rcy - 3), int(rcy + 4)):
        for x in range(int(rcx + 1), int(rcx + 7)):
            dot = -0.5 * ((x - rcx) / 6.0) - 0.7 * ((y - rcy) / 3.0)
            col = GOLD_SHINE if dot > 0.2 else (GOLD_BASE if dot > -0.3 else GOLD_DARK)
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sky Blue Damping Pad & Micro Piston Exhaust Vent
    wd.ellipse([rcx - 5, rcy - 5, rcx - 1, rcy - 1], fill=tuple(SKY_LIGHT.astype(int)) + (255,), outline=tuple(SKY_DARK.astype(int)) + (255,))
    wd.point((int(rcx + 5), int(rcy - 1)), fill=tuple(WHITE_SHINE.astype(int)) + (255,))

    # ─────────────────────────────────────────────────────────────
    # 2. Secondary Gauntlet (Left Fist at 44, 76)
    # ─────────────────────────────────────────────────────────────
    lcx, lcy = 44.0, 76.0

    # Piston Cylinder Chamber (Orange #FFA010) - bounds (38..50, 70..82)
    for y in range(int(lcy - 6), int(lcy + 7)):
        for x in range(int(lcx - 6), int(lcx + 7)):
            dx = (x - lcx) / 5.5
            dy = (y - lcy) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                if dot > 0.35:
                    col = ORANGE_SHINE * 0.4 + ORANGE_LIGHT * 0.6
                elif dot > 0.0:
                    col = ORANGE_BASE + dot * 20.0
                elif dot > -0.35:
                    col = ORANGE_DARK
                else:
                    col = ORANGE_DEEP
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Forged Brass Anvil Face at fist front (39..44, 73..79)
    for y in range(int(lcy - 3), int(lcy + 4)):
        for x in range(int(lcx - 5), int(lcx + 1)):
            dot = -0.5 * ((x - lcx) / 5.0) - 0.7 * ((y - lcy) / 3.0)
            col = GOLD_SHINE if dot > 0.2 else (GOLD_BASE if dot > -0.3 else GOLD_DARK)
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sky Blue Damping Pad on left gauntlet
    wd.ellipse([lcx + 1, lcy - 5, lcx + 5, lcy - 1], fill=tuple(SKY_LIGHT.astype(int)) + (255,), outline=tuple(SKY_DARK.astype(int)) + (255,))
    wd.point((int(lcx - 3), int(lcy - 1)), fill=tuple(WHITE_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_marmot_slices():
    print("=== BUILDING ROCKBREAKER MARMOT 7 PAPERDOLL SLICES ===")

    # Generate each slice independently
    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_marmot_dual_pawl_brass", key_img),
        ("back_curio", "curio_marmot_pneumatic_sand_tail", curio_img),
        ("chassis", "chassis_marmot_quarry_tinplate_default", chassis_img),
        ("head_unit", "head_marmot_alloy_chisel_visor", head_img),
        ("costume", "costume_marmot_scavenger_canvas_harness", costume_img),
        ("optic_core", "face_marmot_amber_dust_goggles", core_img),
        ("weapon", "weapon_marmot_eccentric_piston_fists", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{MARMOT_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_marmot_dual_pawl_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_marmot_dual_pawl_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_marmot_eccentric_piston_fists.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_marmot_eccentric_piston_fists_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{MARMOT_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{MARMOT_PD_DIR}/proof_paperdoll_marmot_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{MARMOT_PD_DIR}/proof_paperdoll_marmot_magenta.png"
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

    strip_path = f"{MARMOT_PD_DIR}/proof_marmot_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([36, 108, 92, 120], fill=(31, 26, 58, 110))
    shd.ellipse([46, 110, 82, 118], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/marmot_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/marmot_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/marmot_idle.png
    p_idle_64 = f"{PLAYER_DIR}/marmot_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/marmot_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/marmot_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/marmot_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/marmot_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/marmot_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # 6. Ensure symlink/compatibility: game/assets/sprites/player/marmot -> paperdoll/marmot
    marmot_alias_dir = f"{PLAYER_DIR}/marmot"
    # If it's a directory with only .gitkeep, replace with symlink
    if os.path.exists(marmot_alias_dir):
        if os.path.islink(marmot_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/marmot -> paperdoll/marmot already exists")
        else:
            # Check contents
            files = os.listdir(marmot_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(marmot_alias_dir, f))
                os.rmdir(marmot_alias_dir)
                os.symlink("paperdoll/marmot", marmot_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/marmot -> paperdoll/marmot")
    else:
        try:
            os.symlink("paperdoll/marmot", marmot_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/marmot -> paperdoll/marmot")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL ROCKBREAKER MARMOT PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_marmot_slices()
