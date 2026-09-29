#!/usr/bin/env python3
"""
build_kingfisher_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十八族 穿雲翠鳥 (The Jade Kingfisher, kingfisher) 7 Paperdoll Slices.
Follows:
- docs/world/JADE_KINGFISHER_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, stamped tinplate chassis #38A0FF / #FFFDF8,
  bird beak lance cowl with sharp cone beak #FFD028,
  dual high-transparency zen slate quartz goggles #4ED86A / #FFD028,
  dojo lacquer woven cuirass with Tai-Chi mirror #FFA010 / #FFD028 / #FF5E8A,
  bamboo fiber folded wings with mint bumper and segmented spring tail balance unit #38A0FF / #4ED86A,
  Tai-Chi dual-ring brass wind-up key with center coral pink rivet #FFD028 / #FF5E8A,
  green bamboo spring lance #4ED86A / #FFD028 / #FFA010)
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

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_bfb84d21"
KINGFISHER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kingfisher"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Jade Kingfisher Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Primary Metal / Sky Blue Enamel Lacquer (#38A0FF)
SKY_SHINE  = np.array([210, 240, 255], dtype=float)
SKY_LIGHT  = np.array([130, 205, 255], dtype=float)
SKY_BASE   = np.array([56, 160, 255], dtype=float)      # #38A0FF
SKY_SHADOW = np.array([32, 115, 210], dtype=float)
SKY_DARK   = np.array([20, 75, 160], dtype=float)
SKY_DEEP   = np.array([14, 45, 110], dtype=float)

# 2. Secondary Ivory Porcelain Belly Plate & High-impact Bevels (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)

# 3. Dopamine Zen Gold & Forged Brass Beak/Gears (#FFD028)
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)     # #FFD028
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 4. Dopamine Mint Green / Zen Bamboo (#4ED86A) - Spear Shaft, Wing Bumpers, Goggles
MINT_SHINE = np.array([195, 255, 215], dtype=float)
MINT_LIGHT = np.array([135, 242, 165], dtype=float)
MINT_BASE  = np.array([78, 216, 106], dtype=float)     # #4ED86A
MINT_DARK  = np.array([42, 160, 68], dtype=float)
MINT_DEEP  = np.array([22, 105, 42], dtype=float)

# 5. Dopamine Sunset Warm Orange (#FFA010) - Cuirass Harness, Tassels
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)    # #FFA010
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 6. Dopamine Coral Pink (#FF5E8A) - Key Rivet, Harness Accent
PINK_SHINE = np.array([255, 210, 230], dtype=float)
PINK_LIGHT = np.array([255, 150, 182], dtype=float)
PINK_BASE  = np.array([255, 94, 138], dtype=float)     # #FF5E8A
PINK_DARK  = np.array([195, 55, 95], dtype=float)

# 7. Quartz Cyan / Deep Optical Lens (#60C3F0)
CYAN_SHINE = np.array([230, 255, 255], dtype=float)
CYAN_LIGHT = np.array([140, 235, 255], dtype=float)
CYAN_BASE  = np.array([60, 195, 240], dtype=float)
CYAN_DARK  = np.array([25, 135, 185], dtype=float)

# 8. Rubber / Joint Dark Metallic
RUBBER_LIGHT = np.array([72, 68, 86], dtype=float)
RUBBER_BASE  = np.array([48, 44, 58], dtype=float)
RUBBER_DARK  = np.array([28, 24, 36], dtype=float)

WHITE_SHINE = np.array([255, 255, 255], dtype=float)


def apply_antialiased_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=50, ignore_regions=None) -> Image.Image:
    """
    Applies a clean 1px dark outline with smooth anti-aliasing on outer boundaries.
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

            cardinal_hits = 0
            for dx, dy in neighbors_4:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    cardinal_hits += 1

            diag_hits = 0
            for dx, dy in neighbors_diag:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and opaque_mask[ny, nx]:
                    diag_hits += 1

            if cardinal_hits > 0 or diag_hits > 0:
                strength = min(1.0, cardinal_hits * 0.45 + diag_hits * 0.20)
                outline_alpha[y, x] = strength * 220.0
                outline_rgb[y, x] = outline_color

    res = arr.copy()
    for y in range(h):
        for x in range(w):
            if not opaque_mask[y, x] and outline_alpha[y, x] > 0:
                res[y, x, :3] = outline_rgb[y, x].astype(np.uint8)
                res[y, x, 3] = int(outline_alpha[y, x])
    return Image.fromarray(res, "RGBA")


def build_winding_key() -> Image.Image:
    """
    SLICE 1: WINDING KEY (z=5)
    天元太極雙輪黃銅發條鑰匙 (key_kingfisher_zen_taichi_gear_brass)
    Dual-Ring Tai-Chi Brass Wind-up Key.
    Central axle extending from chassis socket (46, 50) to key center (38, 28).
    Dual-ring interlocking Tai-Chi cogs: upper lobe center (38, 22), lower lobe center (38, 34).
    Each lobe has outer gear teeth (8 teeth per lobe).
    Central junction hub with Dopamine Coral Pink (#FF5E8A) shockproof rivet.
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

    # 2. Dual-Ring Tai-Chi Gear Lobes
    # Upper ring centered at (38, 21.5), Lower ring centered at (38, 33.5)
    rings = [(38.0, 21.5), (38.0, 33.5)]
    for rcx, rcy in rings:
        for y in range(int(rcy - 12), int(rcy + 13)):
            for x in range(int(rcx - 12), int(rcx + 13)):
                dx = x - rcx
                dy = y - rcy
                r = math.sqrt(dx**2 + dy**2)
                ang = math.atan2(dy, dx)
                teeth = 1.0 * math.cos(ang * 8)
                r_outer = 9.5 + teeth
                r_inner = 5.2

                if r_inner <= r <= r_outer:
                    dot = -0.55 * (dx / r) - 0.70 * (dy / r)
                    if dot > 0.35:
                        col = GOLD_SHINE * 0.35 + GOLD_LIGHT * 0.65 + dot * 12.0
                    elif dot > 0.05:
                        col = GOLD_BASE + dot * 20.0
                    elif dot > -0.35:
                        col = GOLD_DARK + (dot + 0.35) * 16.0
                    else:
                        col = GOLD_DEEP + (dot + 0.7) * 10.0
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Interlocking Tai-Chi Swirl Bridge between lobes (y: 24..31, x: 33..43)
    for y in range(24, 32):
        for x in range(33, 44):
            dx = (x - kcx) / 4.5
            dy = (y - kcy) / 3.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = GOLD_LIGHT + dot * 14.0 if dot > 0.2 else (GOLD_BASE + dot * 18.0 if dot > -0.3 else GOLD_DARK)
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Central Hub with Dopamine Coral Pink (#FF5E8A) Rivet at (38, 28)
    for y in range(int(kcy - 5), int(kcy + 6)):
        for x in range(int(kcx - 5), int(kcx + 6)):
            dx = x - kcx
            dy = y - kcy
            r = math.sqrt(dx**2 + dy**2)
            if r <= 4.2:
                dot = -0.55 * dx / 4.2 - 0.70 * dy / 4.2
                if r <= 2.2:
                    col = PINK_SHINE if dot > 0.4 else (PINK_LIGHT if dot > 0.0 else PINK_BASE)
                else:
                    col = GOLD_LIGHT if dot > 0.2 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    return apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    剛竹纖維高彈摺疊雙翼與分節避震尾翎 (curio_kingfisher_bamboo_wings_spring_tail)
    Bamboo Fiber Folded Wings & Spring Damped Tail.
    - Wings anchor to center spine (x=64) extending continuously outward:
      Left wing: x: 18..64, y: 44..80
      Right wing: x: 64..91, y: 44..80 (strictly x <= 92)
      Enamel sky blue plates (#38A0FF) with dopamine mint green bumper leading edges (#4ED86A).
      Aerodynamic feather slats with internal spring ribs.
    - Tail: 3-segment articulated bamboo fiber tail feathers extending down-left (y: 80..112, x: 26..50)
      with golden spherical counterweight bead (#FFD028) at the tip.
    Anchoring to center spine guarantees 0 gaps/holes between wings and chassis.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Left Folded Wing (extends from spine x=64 out to x=18, y: 44..80)
    for y in range(44, 81):
        ty = (y - 44.0) / 36.0
        if ty < 0.35:
            xmin = int(round(46.0 - ty * 78.0))
        else:
            t_low = (ty - 0.35) / 0.65
            xmin = int(round(19.0 + t_low * 27.0))

        xmin = max(18, xmin)
        xmax = 64  # anchors to center spine
        for x in range(xmin, xmax + 1):
            dist_edge = (x - xmin) / max(1.0, float(46.0 - xmin))
            dot = -0.5 * (x - 36.0) / 20.0 - 0.7 * (y - 62.0) / 18.0
            if dist_edge < 0.18 and x < 44:
                col = MINT_SHINE if dist_edge < 0.06 else (MINT_BASE + dot * 12.0 if dist_edge < 0.12 else MINT_DARK)
            else:
                if dot > 0.3:
                    col = SKY_SHINE * 0.35 + SKY_LIGHT * 0.65 + dot * 15.0
                elif dot > -0.1:
                    col = SKY_BASE + dot * 20.0
                else:
                    col = SKY_SHADOW + (dot + 0.1) * 15.0
            curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Wing Slat Lines & Spring Hinges
    cd.line([(34, 52), (24, 68)], fill=tuple(SKY_DEEP.astype(int)) + (255,), width=1)
    cd.line([(40, 54), (32, 72)], fill=tuple(SKY_DARK.astype(int)) + (255,), width=1)
    cd.ellipse([40, 60, 44, 64], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 2. Right Folded Wing (extends from spine x=64 out to x=91, y: 44..80) - strictly x <= 91
    for y in range(44, 81):
        ty = (y - 44.0) / 36.0
        if ty < 0.35:
            xmax = int(round(72.0 + ty * 52.0))
        else:
            t_low = (ty - 0.35) / 0.65
            xmax = int(round(90.0 - t_low * 20.0))

        xmax = min(91, xmax)
        xmin = 64  # anchors to center spine
        for x in range(xmin, xmax + 1):
            dist_edge = (xmax - x) / max(1.0, float(xmax - 70.0))
            dot = 0.5 * (x - 76.0) / 16.0 - 0.7 * (y - 62.0) / 18.0
            if dist_edge < 0.18 and x > 72:
                col = MINT_SHINE if dist_edge < 0.06 else (MINT_BASE + dot * 12.0 if dist_edge < 0.12 else MINT_DARK)
            else:
                if dot > 0.3:
                    col = SKY_SHINE * 0.35 + SKY_LIGHT * 0.65 + dot * 15.0
                elif dot > -0.1:
                    col = SKY_BASE + dot * 20.0
                else:
                    col = SKY_SHADOW + (dot + 0.1) * 15.0
            curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Wing Slat Lines
    cd.line([(76, 52), (84, 68)], fill=tuple(SKY_DEEP.astype(int)) + (255,), width=1)
    cd.line([(70, 54), (78, 72)], fill=tuple(SKY_DARK.astype(int)) + (255,), width=1)
    cd.ellipse([66, 60, 70, 64], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 3. Articulated 3-Segment Bamboo Fiber Tail (y: 80..112, x: 26..52)
    # Segments: (50, 82) -> (42, 94) -> (34, 104) -> (28, 110)
    tail_pts = [
        np.array([50.0, 82.0]),
        np.array([42.0, 93.0]),
        np.array([35.0, 103.0]),
        np.array([28.0, 110.0])
    ]
    for i in range(len(tail_pts) - 1):
        p0, p1 = tail_pts[i], tail_pts[i+1]
        width_seg = 3.8 - i * 0.8
        for t in np.linspace(0.0, 1.0, 28):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-int(width_seg), int(width_seg) + 1):
                dot = d / max(1.0, width_seg)
                if abs(d) == int(width_seg):
                    col = MINT_DARK
                elif dot < -0.2:
                    col = MINT_SHINE if i == 0 else MINT_LIGHT
                else:
                    col = MINT_BASE + dot * 12.0
                if 0 <= ix + d < W and 0 <= iy < H:
                    curio_img.putpixel((ix + d, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Brass Nodes / Hinge Rings along Tail
    for nx, ny in [(42, 93), (35, 103)]:
        for dy in [-1, 0, 1]:
            for dx in [-2, -1, 0, 1, 2]:
                curio_img.putpixel((nx + dx, ny + dy), tuple(GOLD_BASE.astype(int)) + (255,))

    # Golden Counterweight Bead at Tail Tip (28, 110)
    cd.ellipse([25, 107, 31, 113], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    curio_img.putpixel((27, 109), tuple(GOLD_SHINE.astype(int)) + (255,))
    curio_img.putpixel((28, 109), tuple(WHITE_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    竹影沖壓彩釉琺瑯金屬底盤 (chassis_kingfisher_enamel_default)
    2.2 head-body ratio chibi kingfisher chassis, stamped tinplate (#38A0FF / SKY),
    sturdy low-gravity stance, ivory belly shock absorber plate (#FFFDF8 / IVORY),
    brass spherical ball-joints, anti-slip black rubber claw pads on foot soles.
    Torso seamlessly covers y: 54..96, x: 44..84 to guarantee zero internal core holes.
    Pelvis bridges y: 86..96 between legs.
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    STRICT 0-ART18: Bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Ground contact shadow (y: 114..120)
    chd.ellipse([64 - 26, 116 - 4, 64 + 26, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 16, 116 - 3, 64 + 16, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.1))

    # 2. Pelvis / Hip Core Plate (y: 86..96, x: 46..82)
    for y in range(86, 97):
        for x in range(46, 83):
            dot = -0.5 * (x - 64.0) / 18.0 - 0.7 * (y - 91.0) / 6.0
            col = SKY_LIGHT + dot * 12.0 if dot > 0.2 else (SKY_BASE + dot * 18.0 if dot > -0.3 else SKY_SHADOW)
            chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Sturdy Legs & Rubber Claws with Brass Hinges (y: 92..113)
    for bx, by in [(48.0, 107.0), (78.0, 107.0)]:
        # Leg cylinder connecting smoothly to pelvis
        for y in range(int(by - 15), int(by)):
            for x in range(int(bx - 6), int(bx + 7)):
                dx = (x - bx) / 6.0
                dy = (y - (by - 7.5)) / 7.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    if dot > 0.35:
                        col = SKY_LIGHT + dot * 16.0
                    elif dot > -0.2:
                        col = SKY_BASE + dot * 20.0
                    else:
                        col = SKY_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Spherical Brass Ball-Joint at Ankle (by - 9.0)
        for y in range(int(by - 12), int(by - 6)):
            for x in range(int(bx - 4), int(bx + 5)):
                if (x - bx)**2 + (y - (by - 9.0))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 9.0) / 3.0
                    col = GOLD_LIGHT + dot * 12.0 if dot > 0.3 else (GOLD_BASE + dot * 15.0 if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Black Anti-slip Rubber Foot Pad with Claws (by - 3..by + 6)
        for y in range(int(by - 3), int(by + 7)):
            for x in range(int(bx - 8), int(bx + 9)):
                dx = (x - bx) / 8.0
                dy = (y - by) / 5.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    col = RUBBER_LIGHT + dot * 12.0 if dot > 0.2 else (RUBBER_BASE + dot * 15.0 if dot > -0.3 else RUBBER_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Three Golden Claw Rivets
        for rx_off in [-5, 0, 5]:
            chd.ellipse([bx + rx_off - 1, by + 4, bx + rx_off + 1, by + 6],
                        fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 4. Main Torso Chassis (y: 54..95, x: 44..84)
    tcx, tcy = 64.0, 74.0
    for y in range(54, 96):
        w_factor = 19.0 if y >= 64 else (19.0 - (64 - y) * 0.25)
        for x in range(int(tcx - w_factor), int(tcx + w_factor + 1)):
            dx = (x - tcx) / w_factor
            dy = (y - tcy) / 20.0
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.40:
                    col = SKY_SHINE * 0.35 + SKY_LIGHT * 0.65 + dot * 14.0
                elif dot > 0.05:
                    col = SKY_BASE + dot * 20.0
                elif dot > -0.35:
                    col = SKY_SHADOW + (dot + 0.35) * 16.0
                else:
                    col = SKY_DARK + (dot + 0.65) * 12.0
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 5. Ivory Porcelain Belly Plate (y: 64..88, x: 52..76)
    for y in range(64, 89):
        for x in range(52, 77):
            dx = (x - tcx) / 12.0
            dy = (y - 76.0) / 11.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.70 * dy
                if dot > 0.35:
                    col = IVORY_SHINE * 0.4 + IVORY_LIGHT * 0.6 + dot * 10.0
                elif dot > 0.0:
                    col = IVORY_BASE + dot * 14.0
                elif dot > -0.35:
                    col = IVORY_SHADOW + (dot + 0.35) * 12.0
                else:
                    col = IVORY_DARK
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Belly Plate Brass Screws
    for px, py in [(55, 68), (73, 68), (55, 84), (73, 84)]:
        chd.ellipse([px - 1, py - 1, px + 1, py + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,))

    # 6. Upper Arms & Spherical Shoulder Hinges (y: 64..82)
    # Left Arm: shoulder (44, 64) -> hand (38, 76)
    for t in np.linspace(0.0, 1.0, 24):
        ax = 44.0 * (1.0 - t) + 38.0 * t
        ay = 64.0 * (1.0 - t) + 76.0 * t
        for r in range(-3, 4):
            px = int(round(ax + r * 0.8))
            py = int(round(ay - r * 0.6))
            if 0 <= px < W and 0 <= py < H:
                dot = r / 3.0
                col = SKY_LIGHT if dot > 0.2 else (SKY_BASE if dot > -0.3 else SKY_SHADOW)
                chassis_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Spherical Brass Shoulder Joint
    chd.ellipse([41, 62, 47, 68], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    chassis_img.putpixel((43, 64), tuple(GOLD_SHINE.astype(int)) + (255,))

    # Left Hand Wrist Clamp at (38, 76)
    chd.ellipse([35, 73, 41, 79], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Right Arm: shoulder (84, 64) -> weapon hand (82, 76)
    # STRICT 0-ART9/11: DO NOT EXCEED x=93! (max x = 88)
    for t in np.linspace(0.0, 1.0, 24):
        ax = 82.0 * (1.0 - t) + 82.0 * t
        ay = 64.0 * (1.0 - t) + 76.0 * t
        for r in range(-3, 4):
            px = int(round(ax + r * 0.8))
            py = int(round(ay - r * 0.6))
            if 0 <= px <= 91 and 0 <= py < H:
                dot = r / 3.0
                col = SKY_LIGHT if dot > 0.2 else (SKY_BASE if dot > -0.3 else SKY_SHADOW)
                chassis_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Spherical Brass Shoulder Joint at (83, 65)
    chd.ellipse([80, 62, 86, 68], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    chassis_img.putpixel((82, 64), tuple(GOLD_SHINE.astype(int)) + (255,))

    # Right Hand Clamp at (82, 76)
    chd.ellipse([79, 73, 85, 79], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Enforce strict 0-ART9 / 0-ART11 boundary
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr, "RGBA")

    return apply_antialiased_outline(chassis_img, outline_color=OUTLINE, min_alpha=50)


def build_head_unit() -> Image.Image:
    """
    SLICE 4: HEAD UNIT (z=20)
    雙聯微調黃銅鳥喙長刺面盔 (head_kingfisher_beak_lance_cowl)
    Dual Micro-Vernier Bird Beak Lance Cowl.
    - Cranial dome cowl in sky blue enamel (#38A0FF) at y: 20..61, x: 44..85.
    - Aerodynamic dual swept-back feather crest vanes at top/sides.
    - Forehead streamline deflector brow in ivory (#FFFDF8) with brass center vernier scale.
    - Protruding pointed brass bird beak lance mask: tapered wedge cone from (58..70, 46) down to needle point at (64, 56).
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
                    col = SKY_SHINE * 0.35 + SKY_LIGHT * 0.65 + dot * 16.0
                elif dot > 0.10:
                    col = SKY_BASE + dot * 22.0
                elif dot > -0.30:
                    col = SKY_SHADOW + (dot + 0.3) * 18.0
                else:
                    col = SKY_DARK + (dot + 0.6) * 12.0
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Dual Swept-back Feather Crest Vanes (Top Sides)
    # Left Crest Vane: (48, 26) -> (36, 15)
    for t in np.linspace(0.0, 1.0, 24):
        vx = 48.0 * (1.0 - t) + 36.0 * t
        vy = 26.0 * (1.0 - t) + 15.0 * t - math.sin(t * math.pi) * 3.0
        for w_v in [-2, -1, 0, 1, 2]:
            ix = int(round(vx + w_v * 0.7))
            iy = int(round(vy - w_v * 0.7))
            if 0 <= ix < W and 0 <= iy < H:
                col = MINT_SHINE if w_v == -2 else (SKY_LIGHT if w_v <= 0 else SKY_SHADOW)
                head_img.putpixel((ix, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    hd.ellipse([34, 13, 38, 17], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Right Crest Vane: (80, 26) -> (92, 15)
    for t in np.linspace(0.0, 1.0, 24):
        vx = 80.0 * (1.0 - t) + 92.0 * t
        vy = 26.0 * (1.0 - t) + 15.0 * t - math.sin(t * math.pi) * 3.0
        for w_v in [-2, -1, 0, 1, 2]:
            ix = int(round(vx - w_v * 0.7))
            iy = int(round(vy - w_v * 0.7))
            if 0 <= ix < W and 0 <= iy < H:
                col = MINT_SHINE if w_v == -2 else (SKY_LIGHT if w_v <= 0 else SKY_SHADOW)
                head_img.putpixel((ix, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    hd.ellipse([90, 13, 94, 17], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 3. Forehead Streamline Deflector Brow Plate (y: 24..37, x: 53..75)
    for y in range(24, 38):
        for x in range(53, 76):
            dx = (x - hcx) / 11.0
            dy = (y - 30.5) / 6.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = IVORY_LIGHT + dot * 12.0 if dot > 0.2 else (IVORY_BASE + dot * 16.0 if dot > -0.3 else IVORY_SHADOW)
                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Forehead brass center vernier strip & scale rivets
    for y in range(22, 37):
        head_img.putpixel((63, y), tuple(GOLD_LIGHT.astype(int)) + (255,))
        head_img.putpixel((64, y), tuple(GOLD_BASE.astype(int)) + (255,))
        head_img.putpixel((65, y), tuple(GOLD_DARK.astype(int)) + (255,))

    # 4. Pointed Brass Bird Beak Lance Mask (Center Nose Cowl)
    # Tapered from base (58..70, 46) down to sharp beak tip (64, 56)
    for y in range(46, 57):
        t_beak = (y - 46.0) / 10.0
        half_w = 6.0 * (1.0 - t_beak) + 0.5
        for x in range(int(round(64.0 - half_w)), int(round(64.0 + half_w + 1))):
            dx = (x - 64.0) / max(0.5, half_w)
            dot = -0.7 * dx - 0.5 * t_beak
            if dot > 0.35:
                col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6 + dot * 12.0
            elif dot > -0.2:
                col = GOLD_BASE + dot * 18.0
            else:
                col = GOLD_DARK + (dot + 0.5) * 15.0
            head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Beak Center Ridge Highlight
    for y in range(46, 56):
        head_img.putpixel((64, y), tuple(GOLD_SHINE.astype(int)) + (255,))

    # 5. STRICT 0-ART27: Hollow out eye sockets [38:47, 50:59] and [38:47, 70:79]
    arr_h = np.array(head_img)
    arr_h[38:47, 50:59, :] = 0
    arr_h[38:47, 70:79, :] = 0
    head_img = Image.fromarray(arr_h, "RGBA")

    # Anti-aliased outer silhouette (ignoring eye socket cutouts so they remain 100% hollow)
    ignore_eye_rects = [(50, 38, 58, 46), (70, 38, 78, 46)]
    return apply_antialiased_outline(head_img, outline_color=OUTLINE, min_alpha=50, ignore_regions=ignore_eye_rects)


def build_optic_core() -> Image.Image:
    """
    SLICE 5: OPTIC CORE (z=30)
    雙聯高透青石琉璃圓形目鏡 (face_kingfisher_zen_slate_goggles)
    High-Transparency Zen Slate Quartz Goggles.
    - Inserted into head_unit eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    - Dark anti-glare eyemask frame 100% fills socket rectangle [cx-4..cx+4, cy-4..cy+4].
    - Convex quartz glass with mint green & cyan glow (#4ED86A / #60C3F0).
    - Crosshair reticle and golden needle indicator (#FFD028).
    - STRICT 0-ART27: Center pixels at (54, 42) and (74, 42) MUST have alpha >= 200.
    """
    optic_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(optic_img)

    for cx, cy in [(54, 42), (74, 42)]:
        # Dark anti-glare socket fill
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

        # Concentric Golden Crosshair Reticle & Pointer
        od.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        od.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        od.line([(cx, cy), (cx - 2, cy - 2)], fill=tuple(GOLD_SHINE.astype(int)) + (255,), width=1)
        optic_img.putpixel((cx, cy), tuple(GOLD_SHINE.astype(int)) + (255,))

        # Specular Highlight Catchlights
        optic_img.putpixel((cx - 2, cy - 2), tuple(WHITE_SHINE.astype(int)) + (255,))
        optic_img.putpixel((cx - 1, cy - 2), tuple(WHITE_SHINE.astype(int)) + (255,))

    # Coral Pink Side Gasket Accents
    for bx in [45, 83]:
        od.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=tuple(PINK_BASE.astype(int)) + (230,))
        optic_img.putpixel((bx, 46), tuple(PINK_LIGHT.astype(int)) + (255,))

    # Nose Bridge Clamp between eyes
    od.line([(62, 42), (66, 42)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)

    return apply_antialiased_outline(optic_img, outline_color=OUTLINE, min_alpha=50)


def build_costume() -> Image.Image:
    """
    SLICE 5: COSTUME (z=25)
    天元道場生漆編織輕量戰袍胸甲 (costume_kingfisher_dojo_lacquer_cuirass)
    Dojo Lacquer Woven Cuirass.
    - Braided metallic shoulder straps (y: 56..68, x: 50..57 and 71..78) in sunset warm orange (#FFA010).
    - Lacquer cuirass breastplate (y: 64..93, x: 48..80) in sky blue (#38A0FF) and dark titanium.
    - Center Tai-Chi / Bagua circular polished brass mirror (x: 60..68, y: 72..80) with Yin-Yang swirl (#FFD028 / #1F1A3A)
      and center coral pink rivet (#FF5E8A).
    - Quick-release side buckles and woven belt sash.
    - STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS (completely decoupled from lower chassis).
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # 1. Braided Shoulder Harness Straps (y: 56..68)
    for y in range(56, 68):
        for x in range(50, 57):
            dot = -0.6 * (x - 53.0) / 3.0
            col = ORANGE_LIGHT + dot * 12.0 if dot > 0.2 else (ORANGE_BASE + dot * 16.0 if dot > -0.3 else ORANGE_DARK)
            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
        for x in range(71, 78):
            dot = 0.6 * (x - 74.0) / 3.0
            col = ORANGE_LIGHT + dot * 12.0 if dot > 0.2 else (ORANGE_BASE + dot * 16.0 if dot > -0.3 else ORANGE_DARK)
            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Stamped Lacquer Cuirass Breastplate (y: 64..93, x: 48..80)
    for y in range(64, 93):
        for x in range(48, 81):
            dx = (x - 64.0) / 16.0
            dy = (y - 78.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.55 * dx - 0.65 * dy
                if dot > 0.35:
                    col = SKY_SHINE * 0.35 + SKY_LIGHT * 0.65 + dot * 15.0
                elif dot > 0.05:
                    col = SKY_BASE + dot * 20.0
                elif dot > -0.3:
                    col = SKY_SHADOW + (dot + 0.3) * 16.0
                else:
                    col = SKY_DARK
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Sunset Orange & Gold War Honor Sash across Chest
    for y in range(68, 76):
        for x in range(52, 77):
            if (x - 64.0)**2 / 14.0**2 + (y - 78.0)**2 / 14.0**2 <= 1.0:
                stripe = ((x + y) // 4) % 2
                col = (GOLD_LIGHT if stripe == 0 else ORANGE_LIGHT)
                costume_img.putpixel((x, y), tuple(col.astype(int)) + (255,))

    # 4. Center Tai-Chi / Bagua Polished Brass Heart-Guard Mirror (x: 59..69, y: 73..83)
    for y in range(73, 84):
        for x in range(59, 70):
            dx = x - 64.0
            dy = y - 78.0
            r = math.sqrt(dx**2 + dy**2)
            if r <= 4.5:
                dot = -0.6 * dx / 4.5 - 0.6 * dy / 4.5
                if r <= 2.2:
                    col = PINK_SHINE if dot > 0.3 else PINK_BASE
                else:
                    col = GOLD_SHINE if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Brass Rim Bezel around Mirror
    cd.ellipse([58, 72, 70, 84], outline=tuple(GOLD_DARK.astype(int)) + (255,), width=1)

    # 5. Quick-Release Brass Side Buckles at (49, 82) and (79, 82)
    cd.rectangle([48, 80, 51, 84], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    cd.rectangle([77, 80, 80, 84], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))

    # Strict 0-ART26b: y >= 96 MUST BE 0 PIXELS
    c_arr = np.array(costume_img)
    c_arr[96:, :, :] = 0
    costume_img = Image.fromarray(c_arr, "RGBA")

    return apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    青竹旋簧刺槍 (weapon_kingfisher_bamboo_spring_lance)
    Green Bamboo Spring Lance.
    - Knight class lance/spear.
    - Long bamboo shaft: extends from bottom-right (84, 104) up through handgrip (78, 76)
      to lance handguard (74, 52) and spiral spearhead (68, 20).
    - Bamboo pole coated with dopamine mint green lacquer (#4ED86A) and golden node rings (#FFD028).
    - Circular Tai-Chi brass handguard disk at (74, 52) with orange silk tassel cord (#FFA010).
    - Spring-loaded conical spiral brass drill bit from (74, 50) up to sharp needle point at (68, 20).
    - Helical grooves and multi-tone brass reflections (GOLD_SHINE, GOLD_BASE, GOLD_DARK).
    - Decoupled from chassis (strictly independent).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Bamboo Spear Shaft (84, 104) -> (74, 52)
    shaft_pts = [
        np.array([84.0, 104.0]),
        np.array([80.0, 84.0]),
        np.array([76.0, 68.0]),
        np.array([74.0, 52.0])
    ]
    for i in range(len(shaft_pts) - 1):
        p0, p1 = shaft_pts[i], shaft_pts[i+1]
        for t in np.linspace(0.0, 1.0, 36):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-2, 3):
                dot = d / 2.0
                if abs(d) == 2:
                    col = MINT_DARK
                elif dot < -0.2:
                    col = MINT_SHINE if dot < -0.6 else MINT_LIGHT
                else:
                    col = MINT_BASE + dot * 12.0
                if 0 <= ix + d < W and 0 <= iy < H:
                    weapon_img.putpixel((ix + d, iy), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Bamboo Segment Rings (Gold Nodes) at (82, 94), (78, 76), (75, 60)
    for nx, ny in [(82, 94), (78, 76), (75, 60)]:
        for dx in range(-3, 4):
            for dy in [-1, 0, 1]:
                if 0 <= nx + dx < W and 0 <= ny + dy < H:
                    weapon_img.putpixel((nx + dx, ny + dy), tuple(GOLD_BASE.astype(int)) + (255,))
        weapon_img.putpixel((nx - 1, ny), tuple(GOLD_SHINE.astype(int)) + (255,))

    # 2. Handgrip Wrap at (78, 76)
    for gy in range(73, 80):
        for gx in range(75, 82):
            if (gy + gx) % 2 == 0:
                weapon_img.putpixel((gx, gy), tuple(ORANGE_LIGHT.astype(int)) + (255,))

    # 3. Tai-Chi Circular Brass Handguard Disk at (74, 52)
    gcx, gcy = 74.0, 52.0
    for y in range(48, 57):
        for x in range(68, 81):
            dx = (x - gcx) / 5.5
            dy = (y - gcy) / 3.8
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = GOLD_SHINE if dot > 0.3 else (GOLD_BASE if dot > -0.2 else GOLD_DARK)
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Orange Silk Tassel Cord hanging from guard (72..70, 54..66)
    tassel_pts = [(71, 54), (70, 58), (69, 63), (69, 67)]
    for tx, ty in tassel_pts:
        wd.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=tuple(ORANGE_BASE.astype(int)) + (255,))
    wd.ellipse([68, 66, 70, 70], fill=tuple(PINK_BASE.astype(int)) + (255,))

    # 4. Spring-loaded Conical Spiral Brass Drill Bit (74, 50) -> (68, 20)
    for y in range(20, 51):
        t = (50.0 - y) / 30.0  # 0 at base (y=50), 1 at tip (y=20)
        cx = 74.0 * (1.0 - t) + 68.0 * t
        half_w = 4.5 * (1.0 - t) + 0.6

        # Helical groove modulation
        groove_phase = math.sin(y * 0.75)

        for x in range(int(round(cx - half_w)), int(round(cx + half_w + 1))):
            dx = (x - cx) / max(0.6, half_w)
            dot = -0.6 * dx - 0.5 * t
            if groove_phase > 0.4 and abs(dx) < 0.5:
                # Darker groove inside helix
                col = GOLD_DARK
            elif dot > 0.35:
                col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6 + dot * 14.0
            elif dot > -0.15:
                col = GOLD_BASE + dot * 18.0
            else:
                col = GOLD_DARK + (dot + 0.5) * 12.0
            weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Lance Tip Sparkle Catchlight at (68, 20)
    weapon_img.putpixel((68, 20), tuple(WHITE_SHINE.astype(int)) + (255,))
    weapon_img.putpixel((67, 21), tuple(GOLD_SHINE.astype(int)) + (255,))
    weapon_img.putpixel((68, 21), tuple(WHITE_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_kingfisher_slices():
    print("=== BUILDING JADE KINGFISHER 7 PAPERDOLL SLICES ===")

    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_kingfisher_zen_taichi_gear_brass", key_img),
        ("back_curio", "curio_kingfisher_bamboo_wings_spring_tail", curio_img),
        ("chassis", "chassis_kingfisher_enamel_default", chassis_img),
        ("head_unit", "head_kingfisher_beak_lance_cowl", head_img),
        ("costume", "costume_kingfisher_dojo_lacquer_cuirass", costume_img),
        ("optic_core", "face_kingfisher_zen_slate_goggles", core_img),
        ("weapon", "weapon_kingfisher_bamboo_spring_lance", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{KINGFISHER_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_kingfisher_zen_taichi_gear_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_kingfisher_zen_taichi_gear_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_kingfisher_bamboo_spring_lance.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_kingfisher_bamboo_spring_lance_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    ordered_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for s_im in ordered_slices:
        composite.alpha_composite(s_im)

    proof_comp = f"{KINGFISHER_PD_DIR}/proof_paperdoll_kingfisher_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{KINGFISHER_PD_DIR}/proof_paperdoll_kingfisher_magenta.png"
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

    strip_path = f"{KINGFISHER_PD_DIR}/proof_kingfisher_all_7_slices.png"
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
    p_idle_x3 = f"{PLAYER_DIR}/kingfisher_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    p_idle_64 = f"{PLAYER_DIR}/kingfisher_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/kingfisher_idle.png"
    idle_with_shadow.save(p_party_idle)

    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/kingfisher_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/kingfisher_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # Compatibility symlink: game/assets/sprites/player/kingfisher -> paperdoll/kingfisher
    kf_alias_dir = f"{PLAYER_DIR}/kingfisher"
    if os.path.exists(kf_alias_dir):
        if os.path.islink(kf_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/kingfisher -> paperdoll/kingfisher already exists")
        else:
            files = os.listdir(kf_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(kf_alias_dir, f))
                os.rmdir(kf_alias_dir)
                os.symlink("paperdoll/kingfisher", kf_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/kingfisher -> paperdoll/kingfisher")
    else:
        try:
            os.symlink("paperdoll/kingfisher", kf_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/kingfisher -> paperdoll/kingfisher")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL JADE KINGFISHER PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_kingfisher_slices()
