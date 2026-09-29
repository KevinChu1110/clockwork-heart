#!/usr/bin/env python3
"""
build_firefly_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十六族 靈燈飛螢 (The Lantern Firefly, firefly) 7 Paperdoll Slices.
Follows:
- docs/world/LANTERN_FIREFLY_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero leather, zero insect flesh, zero biological tissue,
  stamped thin brass sheets & tinplate #4ED86A mint green & #FFFDF8 ivory white,
  head unit with dual spring brass antenna tuners with golden indicator spheres #FFD028,
  dual spherical lantern quartz eyes #FFD028/#FFA010 set in deep indigo rings #1F1A3A,
  clockwork vine harness cuirass with dopamine hazard stripes #4ED86A/#38A0FF/#FFA010,
  translucent injection-molded resin glowing abdomen bulb #4ED86A/#FFD028 with micro gears & brass elytra wings,
  floral-gear 4-lobe brass wind-up key with center coral pink rivet #FFD028/#FF5E8A,
  luminescent vine clockwork staff with glowing resin mushroom & copper sap glass pipe)
- references/art_direction.md & references/brand_assets.md
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34, 0-QA39
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
FIREFLY_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/firefly"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Lantern Firefly Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Primary Metal / Stamped Thinplate Emerald Mint Green (#4ED86A)
MINT_SHINE  = np.array([215, 255, 230], dtype=float)
MINT_LIGHT  = np.array([145, 245, 175], dtype=float)
MINT_BASE   = np.array([78, 216, 106], dtype=float)    # #4ED86A
MINT_SHADOW = np.array([48, 168, 80], dtype=float)
MINT_DARK   = np.array([28, 118, 55], dtype=float)
MINT_DEEP   = np.array([18, 78, 38], dtype=float)

# 2. Secondary Ivory Shock Absorber Plate & Enamel Highlights (#FFFDF8)
IVORY_SHINE  = np.array([255, 255, 255], dtype=float)
IVORY_LIGHT  = np.array([255, 253, 248], dtype=float)
IVORY_BASE   = np.array([242, 238, 230], dtype=float)
IVORY_SHADOW = np.array([214, 208, 196], dtype=float)
IVORY_DARK   = np.array([182, 174, 162], dtype=float)

# 3. Dopamine Sunset Warm Orange (#FFA010) - Filament Glow, Hazard Stripes, Quartz Reticle
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)    # #FFA010
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 4. Dopamine Forged Brass & Golden Tuners (#FFD028) - Floral Key, Antenna Spheres, Staff Joints
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)     # #FFD028
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 5. Deep Forest Vine Weave (#2E7248) - Clockwork Vine Harness Cuirass
VINE_SHINE = np.array([165, 235, 185], dtype=float)
VINE_LIGHT = np.array([95, 195, 130], dtype=float)
VINE_BASE  = np.array([46, 145, 85], dtype=float)
VINE_DARK  = np.array([28, 105, 58], dtype=float)
VINE_DEEP  = np.array([16, 68, 38], dtype=float)

# 6. Dopamine Sky Blue (#38A0FF) - Quick Release Buckles, Glass Tube Glow
SKY_SHINE = np.array([205, 238, 255], dtype=float)
SKY_LIGHT = np.array([135, 210, 255], dtype=float)
SKY_BASE  = np.array([56, 160, 255], dtype=float)      # #38A0FF
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([15, 60, 130], dtype=float)

# 7. Dopamine Coral Pink (#FF5E8A) - Key Center Rivet, Pressure Gasket
CORAL_SHINE = np.array([255, 210, 230], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)    # #FF5E8A
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 8. Deep Indigo-Black / Anti-Glare Mask (#1F1A3A) - Eyemask Bezel
SPACE_BASE  = np.array([31, 26, 58], dtype=float)
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
    花蕾造型四瓣齒輪黃銅發條鑰匙 (key_firefly_floral_gear_brass)
    Floral-gear 4-lobe brass wind-up key.
    Central axle extending from chassis socket (46, 50) to key center (38, 28).
    Floral-gear shaped key handle with 4 distinct rounded petal/gear lobes (radii 10..18).
    Central dopamine coral pink rivet (#FF5E8A) with brass bezel.
    Warm golden bronze outline OUTLINE_KEY.
    Strictly follows 0-ART29 & 0-QA16: no dark block run >= 13, white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

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

    # 2. Floral 4-Lobed Gear Key Ring (4 floral petal gear lobes)
    # Radii: base circle ~8.5..14.5, lobes extend to ~18.0
    for y in range(int(kcy - 20), int(kcy + 21)):
        for x in range(int(kcx - 20), int(kcx + 21)):
            dx = x - kcx
            dy = y - kcy
            r = math.sqrt(dx**2 + dy**2)
            if r < 5.2:
                continue
            ang = math.atan2(dy, dx)
            # 4-lobe floral pattern + micro cog scalloping
            petal = math.cos(4.0 * ang)
            micro_tooth = 0.8 * math.cos(16.0 * ang)
            r_max = 14.0 + 3.8 * petal + micro_tooth

            if 8.0 <= r <= r_max:
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

    # 3. Four petal cross-spokes connecting to central hub
    for p_ang in [0.0, math.pi / 2.0, math.pi, math.pi * 3.0 / 2.0]:
        cos_p, sin_p = math.cos(p_ang), math.sin(p_ang)
        for r_step in np.linspace(5.0, 14.0, 25):
            sx = kcx + r_step * cos_p
            sy = kcy + r_step * sin_p
            for perp in [-0.8, 0.0, 0.8]:
                px = int(round(sx - perp * sin_p))
                py = int(round(sy + perp * cos_p))
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
    注塑樹脂熒光腹囊與沖壓透光薄翅 (curio_firefly_luminescent_resin_abdomen)
    Luminescent Resin Abdomen & Brass Elytra Wings.
    Translucent glowing abdomen bulb at lower rear (38, 88), extending down-left to (28, 96).
    Translucent mint green (#4ED86A) and lemon gold (#FFD028) injection resin bulb
    with visible internal micro clockwork gears.
    Pair of delicate stamped brass filigree elytra wings slightly raised (28..52, 52..72).
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Stamped Brass Filigree Elytra Wings (spread slightly up and left)
    # Wing 1 (Upper): from root (48, 68) to tip (26, 52)
    # Wing 2 (Lower): from root (48, 70) to tip (32, 62)
    for (wx1, wy1, wx2, wy2, w_w) in [(48, 68, 26, 52, 6.0), (48, 71, 31, 62, 5.0)]:
        v_w = np.array([wx2 - wx1, wy2 - wy1], dtype=float)
        len_w = np.linalg.norm(v_w)
        u_w = v_w / len_w
        n_w = np.array([-u_w[1], u_w[0]])

        for t_w in np.linspace(0.0, 1.0, 50):
            pt = np.array([wx1, wy1]) + t_w * v_w
            cur_w = w_w * math.sin(t_w * math.pi)
            for off in np.linspace(-cur_w, cur_w, 15):
                px = int(round(pt[0] + off * n_w[0]))
                py = int(round(pt[1] + off * n_w[1]))
                if 0 <= px < W and 0 <= py < H:
                    dist = abs(off) / (cur_w + 1e-4)
                    # Leaf-vein pattern cutout: slight alternation
                    vein_cut = (int(t_w * 10.0) % 2 == 1) and (0.3 < dist < 0.6)
                    if vein_cut:
                        col = GOLD_DARK
                    elif dist < 0.35:
                        col = GOLD_SHINE
                    elif dist < 0.75:
                        col = GOLD_LIGHT
                    else:
                        col = GOLD_BASE
                    curio_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Translucent Injection-Molded Resin Abdomen Bulb
    # Centered at (36, 88), radius ~10.5 horizontally, 13.0 vertically
    acx, acy = 36.0, 88.0
    for y in range(int(acy - 14), int(acy + 15)):
        for x in range(int(acx - 12), int(acx + 13)):
            dx = (x - acx) / 10.5
            dy = (y - acy) / 13.0
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                dist = math.sqrt(dsq)
                dot = -0.5 * dx - 0.7 * dy
                # Resin core: bright lemon gold glow at center, transitioning to vibrant mint green
                if dist < 0.30:
                    col = GOLD_SHINE * 0.7 + MINT_SHINE * 0.3
                elif dist < 0.60:
                    t = (dist - 0.30) / 0.30
                    col = GOLD_LIGHT * (1.0 - t) + MINT_LIGHT * t + dot * 12.0
                elif dist < 0.85:
                    t = (dist - 0.60) / 0.25
                    col = MINT_BASE * (1.0 - t) + MINT_SHADOW * t + dot * 10.0
                else:
                    col = MINT_DARK

                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Micro Clockwork Gear visible inside translucent abdomen at (36, 88)
    for y in range(int(acy - 4), int(acy + 5)):
        for x in range(int(acx - 4), int(acx + 5)):
            r = math.sqrt((x - acx)**2 + (y - acy)**2)
            if r <= 3.6:
                ang = math.atan2(y - acy, x - acx)
                gear_tooth = (math.cos(6.0 * ang) > 0.0) or (r <= 2.2)
                if gear_tooth:
                    col = GOLD_DARK if r > 2.2 else GOLD_BASE
                    curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))
    # Glowing tungsten filament coil dot
    curio_img.putpixel((int(acx), int(acy)), (255, 255, 255, 255))
    curio_img.putpixel((int(acx - 1), int(acy)), tuple(ORANGE_LIGHT.astype(int)) + (255,))

    out_curio = apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)

    # Soft ambient glowing spore particles around abdomen (translucent, no black outline)
    spores = [(24.0, 84.0, 3.5), (28.0, 99.0, 3.0), (20.0, 93.0, 2.5)]
    for sx, sy, sr in spores:
        for y in range(int(sy - sr - 1), int(sy + sr + 2)):
            for x in range(int(sx - sr - 1), int(sx + sr + 2)):
                dist = math.sqrt((x - sx)**2 + (y - sy)**2)
                if dist <= sr and 0 <= x < W and 0 <= y < H:
                    alpha = int(np.clip((1.0 - dist / sr) * 80.0, 0, 85))
                    curr = out_curio.getpixel((x, y))
                    if curr[3] == 0:
                        out_curio.putpixel((x, y), tuple(MINT_LIGHT.astype(int)) + (alpha,))

    return out_curio


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    深林沖壓薄銅馬口鐵底盤 (chassis_firefly_emerald_tinplate_default)
    2.2 head-body ratio chibi firefly chassis, stamped emerald mint green tinplate (#4ED86A / MINT),
    slightly bent standing posture (微屈膝靈動立姿), ivory belly shock absorber plate (#FFFDF8 / IVORY),
    brass ball-joints, anti-slip rubber suction pads with brass rivets on foot soles.
    Right arm held forward ready to grasp staff, Left arm held gently across chest.
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
    for bx, by in [(48.0, 107.0), (78.0, 107.0)]:
        # Lower leg emerald mint tinplate cylinder
        for y in range(int(by - 14), int(by)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.5
                dy = (y - (by - 7.5)) / 7.0
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.55 * dx - 0.70 * dy
                    if dot > 0.35:
                        col = MINT_LIGHT + dot * 12.0
                    elif dot > -0.2:
                        col = MINT_BASE + dot * 16.0
                    else:
                        col = MINT_SHADOW + dot * 14.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Cold-rolled brass knee joint sphere (#FFD028)
        for y in range(int(by - 12), int(by - 6)):
            for x in range(int(bx - 4), int(bx + 5)):
                if (x - bx)**2 + (y - (by - 9.0))**2 <= 9.0:
                    dot = -0.6 * (x - bx) / 3.0 - 0.6 * (y - by + 9.0) / 3.0
                    col = GOLD_LIGHT if dot > 0.3 else (GOLD_BASE if dot > -0.3 else GOLD_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Foot Sole Plate (Anti-slip rubber suction sole with emerald frame)
        for y in range(int(by - 4), int(by + 7)):
            for x in range(int(bx - 9), int(bx + 10)):
                dx = (x - bx) / 8.5
                dy = (y - by) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    col = MINT_LIGHT if dot > 0.3 else (MINT_BASE if dot > -0.3 else MINT_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Anti-slip brass grip rivets on foot sole (3 rivets per foot)
        for rx_off in [-5, 0, 5]:
            chd.ellipse([bx + rx_off - 1, by + 4, bx + rx_off + 1, by + 6], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 3. Main Torso Chassis (y: 58..95, x: 44..84)
    # Chunky 2.2 head-body ratio mint green tinplate body with solid neck pillar (y: 54..63, x: 56..72)
    # Neck connector pillar ensuring seamless connection to head
    for y in range(54, 64):
        for x in range(56, 73):
            dx = (x - 64.0) / 8.0
            dot = -0.55 * dx - 0.70 * ((y - 58.0) / 5.0)
            col = MINT_LIGHT if dot > 0.2 else (MINT_BASE if dot > -0.3 else MINT_SHADOW)
            chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

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
                    col = MINT_SHINE * 0.4 + MINT_LIGHT * 0.6 + dot * 10.0
                elif dot > 0.20:
                    col = MINT_LIGHT * 0.7 + MINT_BASE * 0.3 + (dot - 0.20) * 25.0
                elif dot > -0.15:
                    col = MINT_BASE + dot * 20.0
                elif dot > -0.45:
                    col = MINT_SHADOW + (dot + 0.45) * 20.0
                else:
                    col = MINT_DARK + (dot + 0.65) * 15.0

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
    chd.line([(64, 67), (64, 89)], fill=tuple(MINT_DARK.astype(int)) + (255,), width=1)
    chd.line([(55, 77), (73, 77)], fill=tuple(MINT_DARK.astype(int)) + (255,), width=1)
    for ry in [71, 79, 87]:
        for rx in [56, 72]:
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 5. Shoulders & Forearms:
    # Left Arm: held gently across chest (x: 37..48, y: 66..82)
    for y in range(66, 83):
        for x in range(37, 49):
            dx = (x - 43.0) / 5.5
            dy = (y - 74.5) / 8.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = MINT_LIGHT if dot > 0.3 else (MINT_BASE if dot > -0.2 else MINT_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Wrist joint node (x: 42..46, y: 74..78)
    chd.ellipse([42, 74, 46, 78], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Right Arm: held forward ready to hold staff (x: 79..91, y: 66..81)
    # STRICT 0-ART9/11: x MUST NOT exceed 93!
    for y in range(66, 81):
        for x in range(79, 92):
            dx = (x - 85.0) / 5.5
            dy = (y - 73.5) / 7.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = MINT_LIGHT if dot > 0.3 else (MINT_BASE if dot > -0.2 else MINT_SHADOW)
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
    雙聯微調黃銅觸角調諧冠 (head_firefly_brass_antenna_cowl)
    Dual Brass Antenna Tuner Cowl.
    Half-sphere stamped thinplate cowl dome (#4ED86A / MINT),
    matching chassis plate color for 0-ART28q (L2 < 60.0).
    Dual delicate spring brass wire antenna tuners (#FFD028) with golden polished spheres.
    Acoustic hemisphere ear cups on sides ((36, 26) and (92, 26)).
    STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
      Left eye:  x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    STRICT 0-ART28q: Average plate color distance to chassis L2 < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Acoustic Brass Ear Cones on Sides ((36, 26) and (92, 26))
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

                # Emerald mint green cowl shell (matches chassis for 0-ART28q L2 < 60.0)
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

    # 3. Forehead Ivory Brow Ridge Arch & Tuning Dial
    hd = ImageDraw.Draw(head_img)
    hd.arc([49, 25, 79, 38], start=180, end=360, fill=tuple(IVORY_LIGHT.astype(int)) + (255,), width=2)
    hd.arc([51, 27, 77, 37], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.ellipse([62, 28, 66, 32], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), outline=tuple(ORANGE_DARK.astype(int)) + (255,))

    # 4. Cheek Vents ((48, 49) and (80, 49))
    for vx in [48, 80]:
        hd.ellipse([vx - 2, 47, vx + 2, 51], fill=tuple(MINT_DARK.astype(int)) + (255,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
        hd.point((vx, 49), fill=tuple(GOLD_LIGHT.astype(int)) + (255,))

    # 5. Dual Spring Brass Antenna Tuners (#FFD028)
    # Left antenna: root at (57, 24), curveto tip (46, 8)
    # Right antenna: root at (71, 24), curveto tip (82, 8)
    antenna_specs = [
        (57.0, 24.0, 52.0, 16.0, 46.0, 8.0, False),
        (71.0, 24.0, 76.0, 16.0, 82.0, 8.0, True)
    ]
    for x0, y0, x1, y1, x2, y2, is_right in antenna_specs:
        # Brass socket base bolt
        hd.ellipse([x0 - 2, y0 - 2, x0 + 2, y0 + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
        # Quadratic bezier curve for spring wire
        for t in np.linspace(0.0, 1.0, 40):
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
        # Specular shine point
        head_img.putpixel((int(x2 - 1), int(y2 - 1)), (255, 255, 255, 255))

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
    藤蔓工裝編織輕量背心胸甲 (costume_firefly_vine_harness_cuirass)
    Clockwork Vine Harness Cuirass.
    Deep forest vine weave (#2E7248) with stamped brass chest plate (#FFD028),
    vibrant sky blue (#38A0FF) and sunset orange (#FFA010) hazard warning stripes across chest,
    central resin lubrication vial dial with mint pointer (#4ED86A), sky blue quick-release buckle (#38A0FF).
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

            # Vine woven harness texture & shading
            if dot > 0.40:
                col = VINE_SHINE * 0.4 + VINE_LIGHT * 0.6
            elif dot > 0.0:
                col = VINE_BASE + dot * 20.0
            elif dot > -0.35:
                col = VINE_DARK + (dot + 0.35) * 18.0
            else:
                col = VINE_DEEP

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Diagonal Hazard Warning Stripes (#38A0FF Sky Blue and #FFA010 Orange) across chest
    cd.line([(53, 65), (64, 79)], fill=tuple(SKY_BASE.astype(int)) + (255,), width=2)
    cd.line([(75, 65), (64, 79)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    cd.line([(49, 92), (79, 92)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=2)

    # Center Resin Dial & Coral Pink Valve Gasket at (64, 78)
    cd.ellipse([60, 74, 68, 82], fill=tuple(SPACE_BASE.astype(int)) + (255,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
    cd.ellipse([62, 76, 66, 80], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    # Mint green indicator pointer
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
    雙聯聚碳酸酯夜燈球形目鏡 (face_firefly_dual_lantern_quartz_eyes)
    Dual Lantern Quartz Eyes.
    Pair of spherical quartz lantern lenses inserted into head_unit eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    Surrounded by anti-glare dark indigo-violet eyemask frames (#1F1A3A),
    glowing warm gold (#FFD028) & sunset orange (#FFA010) lantern quartz lenses with tungsten filament.
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

        # 2. Spherical Lantern Quartz Lens inside frame
        for y in range(int(cy - radius), int(cy + radius + 1)):
            for x in range(int(cx - radius), int(cx + radius + 1)):
                dx = (x - cx) / radius
                dy = (y - cy) / radius
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    dist = math.sqrt(dist_sq)
                    dot = -0.5 * dx - 0.7 * dy
                    if dist < 0.25:
                        col = GOLD_SHINE
                    elif dist < 0.55:
                        t = (dist - 0.25) / 0.30
                        col = GOLD_LIGHT * (1.0 - t) + GOLD_BASE * t + dot * 15.0
                    elif dist < 0.85:
                        t = (dist - 0.55) / 0.30
                        col = ORANGE_BASE * (1.0 - t) + ORANGE_DARK * t + dot * 12.0
                    else:
                        col = ORANGE_DEEP * 0.7 + OUTLINE * 0.3
                    core_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Concentric reticle lines & warm filament dots
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(WHITE_SHINE.astype(int)) + (255,))

        # Specular white reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(ORANGE_BASE.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    深林熒光藤蔓發條長杖 (weapon_firefly_luminescent_vine_staff)
    Luminescent Vine Clockwork Staff.
    Held in right hand, extending from ferrule (86, 98) through hand grip (90, 74)
    up to crowned resin mushroom head at (100, 36).
    Segmented brass tubes, spiraling clockwork wire vines (#4ED86A),
    transparent glass tube with glowing copper sap (#FFA010/#38A0FF),
    and crowned with a miniature glowing resin mushroom (#4ED86A/#FFD028) & tuning prism at (100, 36).
    Zero body or arm baked into weapon (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Staff shaft line from p_bot=(86, 98) to p_top=(100, 36)
    p_bot = np.array([86.0, 98.0])
    p_top = np.array([100.0, 36.0])
    v_shaft = p_top - p_bot
    len_shaft = np.linalg.norm(v_shaft)
    u_shaft = v_shaft / len_shaft
    n_shaft = np.array([-u_shaft[1], u_shaft[0]])

    # 1. Main Staff Shaft
    num_steps = 70
    for i in range(num_steps):
        t = i / float(num_steps - 1)
        pt = p_bot + t * v_shaft
        y_cur = pt[1]

        # Middle section is transparent glass tube with copper sap (t: 0.35..0.60)
        is_glass = (0.35 <= t <= 0.60)
        # Handle grip wrapping (t: 0.20..0.35)
        is_grip = (0.20 <= t <= 0.35)

        for off in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(pt[0] + off * n_shaft[0]))
            py = int(round(pt[1] + off * n_shaft[1]))
            if 0 <= px < W and 0 <= py < H:
                dot = -0.7 * (off / 2.0)
                if is_glass:
                    if abs(off) <= 1.0:
                        col = ORANGE_SHINE * 0.7 + SKY_SHINE * 0.3
                    elif abs(off) < 1.8:
                        col = ORANGE_BASE
                    else:
                        col = SKY_LIGHT
                elif is_grip:
                    if abs(off) <= 1.0:
                        col = MINT_SHINE
                    else:
                        col = MINT_BASE
                else:
                    if dot > 0.2:
                        col = GOLD_SHINE
                    elif dot > -0.3:
                        col = GOLD_BASE
                    else:
                        col = GOLD_DARK

                weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Mechanical Vine Spirals around shaft
    for t_v in np.linspace(0.1, 0.9, 14):
        pt_v = p_bot + t_v * v_shaft
        v_wave = 2.4 * math.sin(t_v * 20.0)
        vx = int(round(pt_v[0] + v_wave * n_shaft[0]))
        vy = int(round(pt_v[1] + v_wave * n_shaft[1]))
        if 0 <= vx < W and 0 <= vy < H:
            wd.ellipse([vx - 1, vy - 1, vx + 1, vy + 1], fill=tuple(MINT_LIGHT.astype(int)) + (255,), outline=tuple(MINT_DARK.astype(int)) + (255,))

    # 3. Staff Head: Miniature Glowing Resin Mushroom & Tuning Prism at p_top (100, 36)
    mcx, mcy = 100.0, 36.0
    for y in range(int(mcy - 7), int(mcy + 4)):
        for x in range(int(mcx - 6), int(mcx + 7)):
            dx = (x - mcx) / 6.0
            dy = (y - mcy) / 6.0
            if dx**2 + dy**2 <= 1.0 and dy <= 0.3:
                dot = -0.5 * dx - 0.7 * dy
                if dot > 0.4:
                    col = MINT_SHINE
                elif dot > 0.0:
                    col = MINT_BASE + dot * 15.0
                else:
                    col = MINT_SHADOW
                weapon_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Mushroom golden rim & tuning prism at top
    wd.line([(mcx - 5, mcy + 1), (mcx + 5, mcy + 1)], fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    wd.ellipse([mcx - 2, mcy - 8, mcx + 2, mcy - 4], fill=tuple(GOLD_SHINE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
    weapon_img.putpixel((int(mcx), int(mcy - 6)), (255, 255, 255, 255))

    # 4. Staff Bottom Ferrule (near 86, 98)
    bx_f, by_f = int(p_bot[0]), int(p_bot[1])
    wd.rounded_rectangle([bx_f - 2, by_f - 1, bx_f + 2, by_f + 3], radius=1, fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_firefly_slices():
    print("=== BUILDING LANTERN FIREFLY 7 PAPERDOLL SLICES ===")

    # Generate each slice independently
    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_firefly_floral_gear_brass", key_img),
        ("back_curio", "curio_firefly_luminescent_resin_abdomen", curio_img),
        ("chassis", "chassis_firefly_emerald_tinplate_default", chassis_img),
        ("head_unit", "head_firefly_brass_antenna_cowl", head_img),
        ("costume", "costume_firefly_vine_harness_cuirass", costume_img),
        ("optic_core", "face_firefly_dual_lantern_quartz_eyes", core_img),
        ("weapon", "weapon_firefly_luminescent_vine_staff", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{FIREFLY_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_firefly_floral_gear_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_firefly_floral_gear_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_firefly_luminescent_vine_staff.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_firefly_luminescent_vine_staff_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{FIREFLY_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{FIREFLY_PD_DIR}/proof_paperdoll_firefly_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{FIREFLY_PD_DIR}/proof_paperdoll_firefly_magenta.png"
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

    strip_path = f"{FIREFLY_PD_DIR}/proof_firefly_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/firefly_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/firefly_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/firefly_idle.png
    p_idle_64 = f"{PLAYER_DIR}/firefly_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/firefly_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/firefly_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/firefly_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/firefly_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/firefly_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # 6. Ensure symlink/compatibility: game/assets/sprites/player/firefly -> paperdoll/firefly
    firefly_alias_dir = f"{PLAYER_DIR}/firefly"
    if os.path.exists(firefly_alias_dir):
        if os.path.islink(firefly_alias_dir):
            print("  ✓ Compatibility symlink game/assets/sprites/player/firefly -> paperdoll/firefly already exists")
        else:
            files = os.listdir(firefly_alias_dir)
            if files == [".gitkeep"] or len(files) == 0:
                for f in files:
                    os.remove(os.path.join(firefly_alias_dir, f))
                os.rmdir(firefly_alias_dir)
                os.symlink("paperdoll/firefly", firefly_alias_dir)
                print("  ✓ Replaced empty directory with symlink game/assets/sprites/player/firefly -> paperdoll/firefly")
    else:
        try:
            os.symlink("paperdoll/firefly", firefly_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/firefly -> paperdoll/firefly")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL LANTERN FIREFLY PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_firefly_slices()
