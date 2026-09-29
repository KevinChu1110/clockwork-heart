#!/usr/bin/env python3
"""
build_manta_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十七族 潮汐蝠魟 (The Tidal Manta, manta) 7 Paperdoll Slices.
Follows:
- docs/world/TIDAL_MANTA_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, stamped marine titanium chassis #38A0FF / #FFFDF8,
  hydrofoil horn cowl with dual brass horns #FFD028,
  dual high-pressure quartz glass goggles #4ED86A / #FFD028,
  deepsea diver harness cuirass with hazard warning stripes #FFA010 / #FFD028,
  flexible titanium alloy gliding wings with mint bumper and antenna tail balance unit #38A0FF / #4ED86A,
  starfish-shaped 5-gear brass wind-up key with center coral pink rivet #FFD028 / #FF5E8A,
  abyssal hydro-pulse compound bow #38A0FF / #4ED86A / #FFD028)
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
MANTA_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/manta"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Tidal Manta Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Primary Metal / Marine Stamped Titanium Sheets (#38A0FF Sky Blue)
TI_SHINE  = np.array([210, 240, 255], dtype=float)
TI_LIGHT  = np.array([130, 205, 255], dtype=float)
TI_BASE   = np.array([56, 160, 255], dtype=float)      # #38A0FF
TI_SHADOW = np.array([32, 115, 210], dtype=float)
TI_DARK   = np.array([20, 75, 160], dtype=float)
TI_DEEP   = np.array([14, 45, 110], dtype=float)

# 2. Secondary Ivory Shock Absorber Plate & High-impact Bevels (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)

# 3. Dopamine Forged Brass & Golden Horns/Key (#FFD028)
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)     # #FFD028
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 4. Dopamine Mint Green (#4ED86A) - Bow Drawstring, Gauge Ticks, Wing Bumper
MINT_SHINE = np.array([195, 255, 215], dtype=float)
MINT_LIGHT = np.array([135, 242, 165], dtype=float)
MINT_BASE  = np.array([78, 216, 106], dtype=float)     # #4ED86A
MINT_DARK  = np.array([42, 160, 68], dtype=float)
MINT_DEEP  = np.array([22, 105, 42], dtype=float)

# 5. Dopamine Sunset Warm Orange (#FFA010) - Cuirass Hazard Stripes, Buckles
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)    # #FFA010
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 6. Dopamine Coral Pink (#FF5E8A) - Key Center Rivet, Bushing Gaskets
PINK_SHINE = np.array([255, 210, 230], dtype=float)
PINK_LIGHT = np.array([255, 150, 182], dtype=float)
PINK_BASE  = np.array([255, 94, 138], dtype=float)     # #FF5E8A
PINK_DARK  = np.array([195, 55, 95], dtype=float)

# 7. Quartz Cyan / Deepsea Godray Focus (#60C3F0)
CYAN_SHINE = np.array([230, 255, 255], dtype=float)
CYAN_LIGHT = np.array([140, 235, 255], dtype=float)
CYAN_BASE  = np.array([60, 195, 240], dtype=float)
CYAN_DARK  = np.array([25, 135, 185], dtype=float)

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
    海星造型五齒輪黃銅發條鑰匙 (key_manta_starfish_gear_brass)
    Starfish-shaped 5-gear Brass Wind-up Key.
    Central axle extending from chassis socket (46, 50) to key center (38, 28).
    Heavy forged brass starfish key handle with 5 outer cog lobes (radii 9..17).
    Center coral pink shockproof rivet (#FF5E8A) with brass bezel.
    Warm golden bronze outline OUTLINE_KEY.
    Strictly follows 0-ART29 & 0-QA16: no dark block run >= 13, white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    kcx, kcy = 38.0, 28.0

    # 1. Axle connecting chassis socket (46, 50) to key center (38, 28)
    for t in np.linspace(0.0, 1.0, 36):
        ax = 46.0 * (1.0 - t) + kcx * t
        ay = 50.0 * (1.0 - t) + kcy * t
        for off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(ax + off * 0.8))
            py = int(round(ay - off * 0.6))
            if 0 <= px < W and 0 <= py < H:
                dot = off / 1.5
                col = GOLD_LIGHT + dot * 12.0 if dot > 0.1 else (GOLD_BASE + dot * 18.0 if dot > -0.4 else GOLD_DARK)
                key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Starfish-shaped 5-gear key handle
    num_lobes = 5
    for y in range(int(kcy - 19), int(kcy + 20)):
        for x in range(int(kcx - 19), int(kcx + 20)):
            dx = x - kcx
            dy = y - kcy
            r = math.sqrt(dx**2 + dy**2)
            if r < 4.0:
                continue
            ang = math.atan2(dy, dx) + math.pi / 2.0

            arm_val = math.cos(ang * num_lobes)
            gear_ripple = 0.8 * math.cos(ang * num_lobes * 4)
            r_max = 11.0 + 4.5 * arm_val + (1.2 if arm_val > 0.3 else 0.0) + gear_ripple

            if 5.5 <= r <= r_max:
                dot = -0.55 * (dx / r) - 0.70 * (dy / r)
                if dot > 0.40:
                    col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6 + dot * 12.0
                elif dot > 0.05:
                    col = GOLD_BASE + dot * 22.0
                elif dot > -0.35:
                    col = GOLD_DARK + (dot + 0.35) * 18.0
                else:
                    col = GOLD_DEEP + (dot + 0.7) * 10.0
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Outer Cog Accent Ring (radius 5.5..8.5)
    for y in range(int(kcy - 9), int(kcy + 10)):
        for x in range(int(kcx - 9), int(kcx + 10)):
            r = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if 5.5 <= r <= 8.5:
                dot = -0.6 * (x - kcx) / r - 0.6 * (y - kcy) / r
                col = GOLD_LIGHT + dot * 14.0 if dot > 0.2 else (GOLD_BASE + dot * 16.0 if dot > -0.3 else GOLD_DARK)
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Central Hub with Dopamine Coral Pink (#FF5E8A) Rivet
    for y in range(int(kcy - 5), int(kcy + 6)):
        for x in range(int(kcx - 5), int(kcx + 6)):
            r = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if r <= 4.8:
                dot = -0.5 * (x - kcx) / 4.8 - 0.7 * (y - kcy) / 4.8
                if r <= 3.2:
                    if dot > 0.35:
                        col = PINK_SHINE * 0.5 + PINK_LIGHT * 0.5 + dot * 10.0
                    elif dot > -0.1:
                        col = PINK_BASE + dot * 15.0
                    else:
                        col = PINK_DARK
                else:
                    col = GOLD_LIGHT if dot > 0.2 else GOLD_DARK
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    key_img.putpixel((int(kcx - 1), int(kcy - 1)), tuple(WHITE_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    柔性鈦合金滑翔翼翅與天線平衡細尾 (curio_manta_flexible_wings_antenna_tail)
    Flexible Titanium Gliding Wings & Antenna Tail Balance Unit.
    - Wings anchor to center spine (x=64) extending continuously outward:
      Left wing: x: 14..64, y: 48..84
      Right wing: x: 64..92, y: 48..84 (strictly x < 94)
      Mint green bumper leading edge (#4ED86A) and titanium plates (#38A0FF).
    - Tail: multi-segment coaxial antenna tail extending down-left (y 80..112, x 26..50) with golden beacon sphere at tip.
    Anchoring to center spine guarantees 0 gaps/holes between wings and chassis.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Left Gliding Wing (extends from spine x=64 out to x=14, y: 48..84)
    for y in range(48, 85):
        ty = (y - 48.0) / 36.0
        if ty < 0.35:
            xmin = int(round(44.0 - ty * 80.0))
        else:
            t_low = (ty - 0.35) / 0.65
            xmin = int(round(16.0 + t_low * 26.0))

        xmin = max(14, xmin)
        xmax = 64  # anchors to center spine
        for x in range(xmin, xmax + 1):
            dist_edge = (x - xmin) / max(1.0, float(50.0 - xmin))
            dot = -0.5 * (x - 36.0) / 20.0 - 0.7 * (y - 65.0) / 18.0
            if dist_edge < 0.16 and x < 44:
                col = MINT_SHINE if dist_edge < 0.05 else (MINT_BASE + dot * 12.0 if dist_edge < 0.11 else MINT_DARK)
            else:
                if dot > 0.3:
                    col = TI_SHINE * 0.4 + TI_LIGHT * 0.6 + dot * 15.0
                elif dot > -0.1:
                    col = TI_BASE + dot * 20.0
                else:
                    col = TI_SHADOW + (dot + 0.1) * 15.0
            curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Wing Panel rib / joint lines
    cd.line([(32, 54), (24, 72)], fill=tuple(TI_DEEP.astype(int)) + (255,), width=1)
    cd.line([(38, 56), (32, 76)], fill=tuple(TI_DARK.astype(int)) + (255,), width=1)
    cd.ellipse([40, 62, 44, 66], fill=tuple(PINK_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 2. Right Gliding Wing (extends from spine x=64 out to x=92, y: 48..84) - strictly x <= 92
    for y in range(48, 85):
        ty = (y - 48.0) / 36.0
        if ty < 0.35:
            xmax = int(round(72.0 + ty * 55.0))
        else:
            t_low = (ty - 0.35) / 0.65
            xmax = int(round(91.0 - t_low * 21.0))

        xmax = min(92, xmax)
        xmin = 64  # anchors to center spine
        for x in range(xmin, xmax + 1):
            dist_edge = (xmax - x) / max(1.0, float(xmax - 70.0))
            dot = 0.5 * (x - 76.0) / 16.0 - 0.7 * (y - 65.0) / 18.0
            if dist_edge < 0.16 and x > 72:
                col = MINT_SHINE if dist_edge < 0.05 else (MINT_BASE + dot * 12.0 if dist_edge < 0.11 else MINT_DARK)
            else:
                if dot > 0.3:
                    col = TI_SHINE * 0.4 + TI_LIGHT * 0.6 + dot * 15.0
                elif dot > -0.1:
                    col = TI_BASE + dot * 20.0
                else:
                    col = TI_SHADOW + (dot + 0.1) * 15.0
            curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    cd.line([(78, 54), (84, 72)], fill=tuple(TI_DEEP.astype(int)) + (255,), width=1)
    cd.line([(74, 56), (78, 76)], fill=tuple(TI_DARK.astype(int)) + (255,), width=1)
    cd.ellipse([70, 62, 74, 66], fill=tuple(PINK_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 3. Flexible Multi-Segment Antenna Tail Balance Unit (y: 82..112, x: 26..54)
    tail_pts = []
    for t in np.linspace(0.0, 1.0, 36):
        tx = (1.0 - t)**2 * 52.0 + 2.0 * (1.0 - t) * t * 40.0 + t**2 * 29.0
        ty = (1.0 - t)**2 * 82.0 + 2.0 * (1.0 - t) * t * 96.0 + t**2 * 108.0
        tail_pts.append((tx, ty))

    for i, (tx, ty) in enumerate(tail_pts):
        r_seg = 2.4 * (1.0 - 0.45 * (i / 36.0))
        for y in range(int(ty - r_seg - 1), int(ty + r_seg + 2)):
            for x in range(int(tx - r_seg - 1), int(tx + r_seg + 2)):
                d = math.sqrt((x - tx)**2 + (y - ty)**2)
                if d <= r_seg and 0 <= x < W and 0 <= y < H:
                    is_ring = (i % 7 < 2)
                    dot = -0.6 * (x - tx) / r_seg - 0.6 * (y - ty) / r_seg
                    if is_ring:
                        col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else GOLD_DARK
                    else:
                        col = TI_LIGHT + dot * 15.0 if dot > 0.2 else (TI_BASE + dot * 18.0 if dot > -0.3 else TI_SHADOW)
                    curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Beacon Sphere at Tail Tip (28, 109)
    bcx, bcy = 28.0, 109.0
    for y in range(int(bcy - 4), int(bcy + 5)):
        for x in range(int(bcx - 4), int(bcx + 5)):
            r = math.sqrt((x - bcx)**2 + (y - bcy)**2)
            if r <= 3.6:
                dot = -0.55 * (x - bcx) / 3.6 - 0.70 * (y - bcy) / 3.6
                col = GOLD_SHINE if dot > 0.35 else (GOLD_BASE + dot * 18.0 if dot > -0.2 else GOLD_DARK)
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    out_curio = apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)

    for y in range(int(bcy - 6), int(bcy + 7)):
        for x in range(int(bcx - 6), int(bcx + 7)):
            r = math.sqrt((x - bcx)**2 + (y - bcy)**2)
            if 3.6 < r <= 6.0 and 0 <= x < W and 0 <= y < H:
                alpha = int(np.clip((1.0 - (r - 3.6) / 2.4) * 85.0, 0, 95))
                curr = out_curio.getpixel((x, y))
                if curr[3] == 0:
                    out_curio.putpixel((x, y), tuple(CYAN_LIGHT.astype(int)) + (alpha,))

    return out_curio


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    深海沖壓耐蝕鍍鈦金屬底盤 (chassis_manta_titanium_default)
    2.2 head-body ratio chibi manta chassis, marine stamped titanium (#38A0FF / TI),
    wide low-gravity stance (低重心滑步微屈膝), ivory belly shock absorber plate (#FFFDF8 / IVORY),
    tungsten ball-joints, anti-slip brass suction pads on foot soles.
    Torso seamlessly covers y: 54..96, x: 44..84 to guarantee zero internal core holes.
    Pelvis bridges y: 88..96 between legs.
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    STRICT 0-ART18: Bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Ground contact shadow (y: 114..120)
    chd.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.1))

    # 2. Pelvis / Hip Core Plate (y: 86..96, x: 46..82) - guarantees no groin notches
    for y in range(86, 97):
        for x in range(46, 83):
            dot = -0.5 * (x - 64.0) / 18.0 - 0.7 * (y - 91.0) / 6.0
            col = TI_LIGHT + dot * 12.0 if dot > 0.2 else (TI_BASE + dot * 18.0 if dot > -0.3 else TI_SHADOW)
            chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Sturdy Legs & Brass Riveted Feet (y: 93..113)
    for bx, by in [(48.0, 107.0), (78.0, 107.0)]:
        # Upper/lower leg cylinder connecting smoothly to pelvis
        for y in range(int(by - 15), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.5
                dy = (y - (by - 7.5)) / 7.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    if dot > 0.35:
                        col = TI_LIGHT + dot * 16.0
                    elif dot > -0.2:
                        col = TI_BASE + dot * 20.0
                    else:
                        col = TI_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        for y in range(int(by - 12), int(by - 6)):
            for x in range(int(bx - 4), int(bx + 5)):
                if (x - bx)**2 + (y - (by - 9.0))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 9.0) / 3.0
                    col = GOLD_LIGHT + dot * 12.0 if dot > 0.3 else (GOLD_BASE + dot * 15.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        for y in range(int(by - 4), int(by + 7)):
            for x in range(int(bx - 9), int(bx + 10)):
                dx = (x - bx) / 8.5
                dy = (y - by) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    col = TI_LIGHT + dot * 14.0 if dot > 0.3 else (TI_BASE + dot * 18.0 if dot > -0.3 else TI_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        for rx_off in [-5, 0, 5]:
            chd.ellipse([bx + rx_off - 1, by + 4, bx + rx_off + 1, by + 6], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 4. Main Torso Chassis (y: 54..95, x: 44..84)
    # Starts at y=54 to seamlessly overlap head_unit and eliminate neck gap holes
    tcx, tcy = 64.0, 74.0
    for y in range(54, 96):
        # Shoulder / pectoral flare at y: 54..66
        w_factor = 19.5 if y >= 64 else (19.5 - (64 - y) * 0.25)
        for x in range(int(tcx - w_factor), int(tcx + w_factor + 1)):
            dx = (x - tcx) / w_factor
            dy = (y - tcy) / 20.0
            rad = dx**2 + dy**2
            if rad <= 1.0:
                dot = -0.55 * dx - 0.65 * dy
                if dot > 0.35:
                    col = TI_SHINE * 0.3 + TI_LIGHT * 0.7 + dot * 15.0
                elif dot > 0.05:
                    col = TI_BASE + dot * 22.0
                elif dot > -0.3:
                    col = TI_SHADOW + (dot + 0.3) * 18.0
                else:
                    col = TI_DARK + (dot + 0.6) * 12.0

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 5. Ivory Belly Insulated Baseplate (y: 62..93, x: 50..78)
    for y in range(62, 94):
        for x in range(50, 79):
            dx = (x - tcx) / 13.5
            dy = (y - 78.0) / 15.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.40:
                    col = IVORY_SHINE * 0.5 + IVORY_LIGHT * 0.5 + dot * 12.0
                elif dot > 0.10:
                    col = IVORY_BASE + dot * 16.0
                elif dot > -0.25:
                    col = IVORY_SHADOW + (dot + 0.25) * 14.0
                else:
                    col = IVORY_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Mechanical panel lines and brass screws
    for py in [68, 76, 84]:
        chd.line([(55, py), (73, py)], fill=tuple(TI_DEEP.astype(int)) + (255,), width=1)
    chd.line([(64, 64), (64, 90)], fill=tuple(TI_DARK.astype(int)) + (255,), width=1)
    for bx, by in [(54, 70), (74, 70), (54, 82), (74, 82)]:
        chd.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,))

    # 6. Left Arm (Grip Arm holding bow at 38, 76)
    for t in np.linspace(0.0, 1.0, 28):
        ax = 48.0 * (1.0 - t) + 38.0 * t
        ay = 64.0 * (1.0 - t) + 76.0 * t
        for y in range(int(ay - 4), int(ay + 5)):
            for x in range(int(ax - 4), int(ax + 5)):
                if (x - ax)**2 + (y - ay)**2 <= 18.0:
                    dot = -0.5 * (x - ax) / 4.2 - 0.6 * (y - ay) / 4.2
                    col = TI_LIGHT + dot * 15.0 if dot > 0.2 else (TI_BASE + dot * 18.0 if dot > -0.3 else TI_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for y in range(73, 80):
        for x in range(35, 42):
            if (x - 38.0)**2 + (y - 76.0)**2 <= 11.0:
                dot = -0.6 * (x - 38.0) / 3.3 - 0.6 * (y - 76.0) / 3.3
                col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else GOLD_BASE
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 7. Right Arm (Draw Arm poised near bowstring at 68, 76)
    for t in np.linspace(0.0, 1.0, 22):
        ax = 78.0 * (1.0 - t) + 86.0 * t
        ay = 64.0 * (1.0 - t) + 72.0 * t
        ax = min(ax, 88.0)
        for y in range(int(ay - 4), int(ay + 5)):
            for x in range(int(ax - 4), int(ax + 5)):
                if (x - ax)**2 + (y - ay)**2 <= 16.0 and x < 93:
                    dot = 0.5 * (x - ax) / 4.0 - 0.6 * (y - ay) / 4.0
                    col = TI_LIGHT + dot * 15.0 if dot > 0.2 else (TI_BASE + dot * 18.0 if dot > -0.3 else TI_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for t in np.linspace(0.0, 1.0, 22):
        ax = 86.0 * (1.0 - t) + 68.0 * t
        ay = 72.0 * (1.0 - t) + 76.0 * t
        for y in range(int(ay - 3), int(ay + 4)):
            for x in range(int(ax - 3), int(ax + 4)):
                if (x - ax)**2 + (y - ay)**2 <= 10.0 and x < 93:
                    dot = -0.5 * (x - ax) / 3.0 - 0.6 * (y - ay) / 3.0
                    col = TI_LIGHT + dot * 15.0 if dot > 0.2 else (TI_BASE + dot * 18.0 if dot > -0.3 else TI_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for y in range(73, 80):
        for x in range(65, 72):
            if (x - 68.0)**2 + (y - 76.0)**2 <= 10.0:
                dot = -0.6 * (x - 68.0) / 3.1 - 0.6 * (y - 76.0) / 3.1
                col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else GOLD_BASE
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Strict clamp: enforce x >= 94 to be strictly 0 pixels
    arr = np.array(chassis_img)
    arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(arr, "RGBA")

    out_chassis = apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50)

    arr_out = np.array(out_chassis)
    arr_out[:, 94:, :] = 0
    return Image.fromarray(arr_out, "RGBA")


def build_head_unit() -> Image.Image:
    """
    SLICE 4: HEAD UNIT (z=20)
    雙聯微型導流頭角導航冠 (head_manta_hydrofoil_horn_cowl)
    Dual Hydrofoil Horn Cowl.
    - Cranial cowl: rounded stamped titanium helmet (y: 20..61, x: 44..85).
    - Dual hydrofoil horns: forward-reaching curved brass horns at left (36, 16) and right (92, 16).
      Horn tips feature 3px golden vernier balls.
    - Forehead streamline deflector vane with brass rivets.
    - STRICT 0-ART27: Eye sockets [38:47, 50:59] and [38:47, 70:79] MUST BE 100% HOLLOW (alpha=0).
    - L2 color distance with chassis plate < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 41.0

    # 1. Main Cranial Cowl Helmet Dome (y: 20..61, x: 44..85)
    for y in range(20, 62):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 19.0
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.40:
                    col = TI_SHINE * 0.4 + TI_LIGHT * 0.6 + dot * 16.0
                elif dot > 0.10:
                    col = TI_BASE + dot * 22.0
                elif dot > -0.30:
                    col = TI_SHADOW + (dot + 0.3) * 18.0
                else:
                    col = TI_DARK + (dot + 0.6) * 12.0
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Forehead Streamline Deflector Vane & Brow Plate (y: 24..37, x: 52..76)
    for y in range(24, 38):
        for x in range(53, 76):
            dx = (x - hcx) / 11.0
            dy = (y - 30.5) / 6.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = IVORY_LIGHT + dot * 12.0 if dot > 0.2 else (IVORY_BASE + dot * 16.0 if dot > -0.3 else IVORY_SHADOW)
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Forehead crest center ridge (brass strip)
    for y in range(22, 37):
        head_img.putpixel((63, y), tuple(GOLD_LIGHT.astype(int)) + (255,))
        head_img.putpixel((64, y), tuple(GOLD_BASE.astype(int)) + (255,))
        head_img.putpixel((65, y), tuple(GOLD_DARK.astype(int)) + (255,))

    # 3. Dual Hydrofoil Horns (Left: 46,32 -> 36,16; Right: 82,32 -> 92,16)
    horn_left = []
    for t in np.linspace(0.0, 1.0, 25):
        hx = 46.0 * (1.0 - t) + 36.0 * t
        hy = 32.0 * (1.0 - t) + 16.0 * t - math.sin(t * math.pi) * 3.5
        horn_left.append((hx, hy))

    for i, (hx, hy) in enumerate(horn_left):
        r_horn = 3.5 * (1.0 - 0.5 * (i / 25.0))
        for y in range(int(hy - r_horn - 1), int(hy + r_horn + 2)):
            for x in range(int(hx - r_horn - 1), int(hx + r_horn + 2)):
                if (x - hx)**2 + (y - hy)**2 <= r_horn**2:
                    dot = -0.6 * (x - hx) / r_horn - 0.6 * (y - hy) / r_horn
                    col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else (GOLD_BASE + dot * 16.0 if dot > -0.3 else GOLD_DARK)
                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    hd.ellipse([34, 14, 38, 18], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    horn_right = []
    for t in np.linspace(0.0, 1.0, 25):
        hx = 82.0 * (1.0 - t) + 92.0 * t
        hy = 32.0 * (1.0 - t) + 16.0 * t - math.sin(t * math.pi) * 3.5
        horn_right.append((hx, hy))

    for i, (hx, hy) in enumerate(horn_right):
        r_horn = 3.5 * (1.0 - 0.5 * (i / 25.0))
        for y in range(int(hy - r_horn - 1), int(hy + r_horn + 2)):
            for x in range(int(hx - r_horn - 1), int(hx + r_horn + 2)):
                if (x - hx)**2 + (y - hy)**2 <= r_horn**2:
                    dot = 0.6 * (x - hx) / r_horn - 0.6 * (y - hy) / r_horn
                    col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else (GOLD_BASE + dot * 16.0 if dot > -0.3 else GOLD_DARK)
                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    hd.ellipse([90, 14, 94, 18], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 4. STRICT 0-ART27: Hollow out exact eye sockets:
    # Left eye:  x: 50..58, y: 38..46
    # Right eye: x: 70..78, y: 38..46
    head_arr = np.array(head_img)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_arr[ey, ex, :] = 0
        for ex in range(70, 79):
            head_arr[ey, ex, :] = 0
    head_img = Image.fromarray(head_arr).copy()

    ignore_eyes = [(49, 37, 59, 47), (69, 37, 79, 47)]
    out_head = apply_antialiased_outline(head_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=ignore_eyes)

    head_arr = np.array(out_head)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_arr[ey, ex, :] = 0
        for ex in range(70, 79):
            head_arr[ey, ex, :] = 0

    return Image.fromarray(head_arr, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 5: OPTIC CORE (z=30)
    雙聯耐高壓深海石英泡罩目鏡 (face_manta_high_pressure_quartz_goggles)
    High-Pressure Quartz Goggles.
    - Inserted into head_unit eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    - Dark anti-glare eyemask frame 100% fills socket rectangle [cx-4..cx+4, cy-4..cy+4].
    - Convex quartz dome with cyan/mint/gold glow (#4ED86A / #FFD028 / #38A0FF)
    - Crosshair reticle and needle indicator
    - STRICT 0-ART27: Center pixels at (54, 42) and (74, 42) MUST have alpha >= 200.
    """
    optic_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(optic_img)

    for cx, cy in [(54, 42), (74, 42)]:
        od.rounded_rectangle([cx - 4, cy - 4, cx + 4, cy + 4], radius=1, fill=tuple(OUTLINE.astype(int)) + (255,))

        radius = 4.2
        for y in range(int(cy - radius - 1), int(cy + radius + 2)):
            for x in range(int(cx - radius - 1), int(cx + radius + 2)):
                dx = (x - cx) / radius
                dy = (y - cy) / radius
                dsq = dx**2 + dy**2
                if dsq <= 1.0:
                    dist = math.sqrt(dsq)
                    dot = -0.55 * dx - 0.70 * dy
                    if dist < 0.25:
                        col = CYAN_SHINE * 0.7 + MINT_SHINE * 0.3 + dot * 10.0
                    elif dist < 0.60:
                        col = MINT_LIGHT * 0.6 + CYAN_BASE * 0.4 + dot * 18.0
                    elif dist < 0.85:
                        col = MINT_BASE * 0.7 + CYAN_DARK * 0.3 + dot * 15.0
                    else:
                        col = MINT_DARK * 0.8 + OUTLINE * 0.2
                    optic_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        od.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        od.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        od.line([(cx, cy), (cx - 2, cy - 2)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)
        optic_img.putpixel((cx, cy), tuple(GOLD_SHINE.astype(int)) + (255,))

        optic_img.putpixel((cx - 2, cy - 2), tuple(WHITE_SHINE.astype(int)) + (255,))
        optic_img.putpixel((cx - 1, cy - 2), tuple(WHITE_SHINE.astype(int)) + (255,))

    for bx in [45, 83]:
        od.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=tuple(PINK_BASE.astype(int)) + (230,))
        optic_img.putpixel((bx, 46), tuple(PINK_LIGHT.astype(int)) + (255,))

    od.line([(62, 50), (64, 52), (66, 50)], fill=tuple(OUTLINE.astype(int)) + (255,), width=1)

    return apply_antialiased_outline(optic_img, outline_color=OUTLINE, min_alpha=50)


def build_costume() -> Image.Image:
    """
    SLICE 5: COSTUME (z=25)
    深海潛水工裝編織輕量胸甲 (costume_manta_diver_harness_cuirass)
    Deepsea Diver Harness Cuirass.
    - Braided metallic shoulder straps (y: 56..68, x: 48..56 and 72..80).
    - Stamped titanium cuirass breastplate (y: 64..92, x: 48..80).
    - Dopamine hazard warning stripes: alternating sunset orange (#FFA010) and gold (#FFD028).
    - Center quick-release buckle at (64, 78) with coral pink gasket.
    - Mini emergency relief valve at (54, 82).
    - STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS (completely decoupled from lower chassis).
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    for y in range(56, 68):
        for x in range(50, 57):
            dot = -0.6 * (x - 53.0) / 3.0
            col = ORANGE_LIGHT + dot * 12.0 if dot > 0.2 else (ORANGE_BASE + dot * 16.0 if dot > -0.3 else ORANGE_DARK)
            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        for x in range(71, 78):
            dot = 0.6 * (x - 74.0) / 3.0
            col = ORANGE_LIGHT + dot * 12.0 if dot > 0.2 else (ORANGE_BASE + dot * 16.0 if dot > -0.3 else ORANGE_DARK)
            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for y in range(64, 93):
        for x in range(48, 81):
            dx = (x - 64.0) / 16.0
            dy = (y - 78.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.65 * dy
                if dot > 0.35:
                    col = TI_SHINE * 0.4 + TI_LIGHT * 0.6 + dot * 15.0
                elif dot > 0.05:
                    col = TI_BASE + dot * 20.0
                elif dot > -0.3:
                    col = TI_SHADOW + (dot + 0.3) * 16.0
                else:
                    col = TI_DARK
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for y in range(68, 76):
        for x in range(52, 77):
            if (x - 64.0)**2 / 14.0**2 + (y - 78.0)**2 / 14.0**2 <= 1.0:
                stripe = ((x + y) // 4) % 2
                dot = -0.5 * (x - 64.0) / 12.0
                if stripe == 0:
                    col = ORANGE_BASE + dot * 18.0
                else:
                    col = GOLD_BASE + dot * 18.0
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for y in range(78, 83):
        for x in range(61, 68):
            dot = -0.5 * (x - 64.0) / 3.0 - 0.6 * (y - 80.0) / 2.0
            col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else (GOLD_BASE + dot * 15.0 if dot > -0.2 else GOLD_DARK)
            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    costume_img.putpixel((64, 80), tuple(PINK_BASE.astype(int)) + (255,))

    cd.ellipse([52, 81, 56, 85], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    cd.point((54, 83), fill=tuple(MINT_LIGHT.astype(int)) + (255,))

    out_costume = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)

    arr_c = np.array(out_costume)
    arr_c[96:, :, :] = 0
    return Image.fromarray(arr_c, "RGBA")


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    海淵流體脈衝複合機關弓 (weapon_manta_hydro_compound_bow)
    Abyssal Hydro-Pulse Compound Bow.
    - Bow class weapon (Ranger / bow).
    - Handle / riser at (38, 76) gripped by left hand.
    - Upper bow limb arching up-forward from (38, 72) to upper coaxial pulley at (32, 42).
    - Lower bow limb arching down-forward from (38, 82) to lower coaxial pulley at (32, 102).
    - Bow limbs shaped like mini manta hydrofoil wings (#38A0FF) with mint bumper edge.
    - Dual coaxial pulleys with water pressure chambers.
    - Mint green high-tensile drawstring (#4ED86A) between pulleys.
    - Central quartz focus sight at (36, 68).
    - Nocked hydro-pulse energy arrow / bubble chamber along shelf (36..54, 74..78).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    for y in range(71, 84):
        for x in range(36, 41):
            dot = -0.6 * (x - 38.0) / 2.0
            col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else (GOLD_BASE + dot * 16.0 if dot > -0.3 else GOLD_DARK)
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    for y in [73, 76, 79, 82]:
        wd.line([(36, y), (40, y)], fill=tuple(ORANGE_BASE.astype(int)) + (255,))

    upper_limb_pts = [
        np.array([38.0, 71.0]),
        np.array([35.0, 60.0]),
        np.array([31.0, 50.0]),
        np.array([32.0, 42.0])
    ]
    for i in range(len(upper_limb_pts) - 1):
        p0, p1 = upper_limb_pts[i], upper_limb_pts[i+1]
        for t in np.linspace(0.0, 1.0, 32):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-2, 3):
                dot = d / 2.0
                if d == -2:
                    col = MINT_BASE + dot * 10.0
                elif d <= 0:
                    col = TI_LIGHT + dot * 15.0
                else:
                    col = TI_SHADOW + dot * 15.0
                weapon_img.putpixel((ix + d, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    lower_limb_pts = [
        np.array([38.0, 83.0]),
        np.array([35.0, 92.0]),
        np.array([31.0, 98.0]),
        np.array([32.0, 102.0])
    ]
    for i in range(len(lower_limb_pts) - 1):
        p0, p1 = lower_limb_pts[i], lower_limb_pts[i+1]
        for t in np.linspace(0.0, 1.0, 32):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-2, 3):
                dot = d / 2.0
                if d == -2:
                    col = MINT_BASE + dot * 10.0
                elif d <= 0:
                    col = TI_LIGHT + dot * 15.0
                else:
                    col = TI_SHADOW + dot * 15.0
                weapon_img.putpixel((ix + d, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    for cy in [42, 102]:
        for y in range(cy - 4, cy + 5):
            for x in range(32 - 4, 32 + 5):
                r = math.sqrt((x - 32.0)**2 + (y - float(cy))**2)
                if r <= 4.2:
                    dot = -0.5 * (x - 32.0) / 4.2 - 0.6 * (y - float(cy)) / 4.2
                    col = GOLD_LIGHT + dot * 12.0 if dot > 0.2 else (GOLD_BASE + dot * 15.0 if dot > -0.2 else GOLD_DARK)
                    weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        weapon_img.putpixel((32, cy), tuple(PINK_BASE.astype(int)) + (255,))

    for t in np.linspace(0.0, 1.0, 42):
        sx = int(round(32.0 * (1.0 - t) + 48.0 * t))
        sy = int(round(42.0 * (1.0 - t) + 76.0 * t))
        col1 = MINT_LIGHT + (t - 0.5) * 12.0
        col2 = MINT_BASE + (t - 0.5) * 12.0
        weapon_img.putpixel((sx, sy), tuple(np.clip(col1, 0, 255).astype(int)) + (255,))
        weapon_img.putpixel((sx + 1, sy), tuple(np.clip(col2, 0, 255).astype(int)) + (255,))

    for t in np.linspace(0.0, 1.0, 42):
        sx = int(round(48.0 * (1.0 - t) + 32.0 * t))
        sy = int(round(76.0 * (1.0 - t) + 102.0 * t))
        col1 = MINT_LIGHT + (t - 0.5) * 12.0
        col2 = MINT_BASE + (t - 0.5) * 12.0
        weapon_img.putpixel((sx, sy), tuple(np.clip(col1, 0, 255).astype(int)) + (255,))
        weapon_img.putpixel((sx + 1, sy), tuple(np.clip(col2, 0, 255).astype(int)) + (255,))

    wd.ellipse([34, 66, 38, 70], fill=tuple(CYAN_SHINE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    weapon_img.putpixel((36, 68), tuple(WHITE_SHINE.astype(int)) + (255,))

    for x in range(36, 56):
        dot = (x - 36.0) / 20.0
        weapon_img.putpixel((x, 76), tuple(np.clip(CYAN_SHINE + dot * 10.0, 0, 255).astype(int)) + (255,))
        weapon_img.putpixel((x, 75), tuple(np.clip(CYAN_LIGHT + dot * 12.0, 0, 255).astype(int)) + (255,))
        weapon_img.putpixel((x, 77), tuple(np.clip(CYAN_DARK + dot * 10.0, 0, 255).astype(int)) + (255,))
    wd.polygon([(34, 76), (37, 73), (37, 79)], fill=tuple(MINT_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_manta_slices():
    print("=== BUILDING TIDAL MANTA 7 PAPERDOLL SLICES ===")

    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_manta_starfish_gear_brass", key_img),
        ("back_curio", "curio_manta_flexible_wings_antenna_tail", curio_img),
        ("chassis", "chassis_manta_titanium_default", chassis_img),
        ("head_unit", "head_manta_hydrofoil_horn_cowl", head_img),
        ("costume", "costume_manta_diver_harness_cuirass", costume_img),
        ("optic_core", "face_manta_high_pressure_quartz_goggles", core_img),
        ("weapon", "weapon_manta_hydro_compound_bow", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{MANTA_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_manta_starfish_gear_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_manta_starfish_gear_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_manta_hydro_compound_bow.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_manta_hydro_compound_bow_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    ordered_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_im in ordered_slices:
        composite.alpha_composite(s_im)

    proof_comp = f"{MANTA_PD_DIR}/proof_paperdoll_manta_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{MANTA_PD_DIR}/proof_paperdoll_manta_magenta.png"
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

    strip_path = f"{MANTA_PD_DIR}/proof_manta_all_7_slices.png"
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

    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/manta_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    p_idle_64 = f"{PLAYER_DIR}/manta_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/manta_idle.png"
    idle_with_shadow.save(p_party_idle)

    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/manta_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/manta_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    manta_alias_dir = f"{PLAYER_DIR}/manta"
    if os.path.exists(manta_alias_dir):
        if os.path.islink(manta_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/manta -> paperdoll/manta already exists")
        else:
            files = os.listdir(manta_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(manta_alias_dir, f))
                os.rmdir(manta_alias_dir)
                os.symlink("paperdoll/manta", manta_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/manta -> paperdoll/manta")
    else:
        try:
            os.symlink("paperdoll/manta", manta_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/manta -> paperdoll/manta")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL TIDAL MANTA PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_manta_slices()
