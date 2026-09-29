#!/usr/bin/env python3
"""
build_lemur_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第六十四族 星環狐猴 (The Star-Ring Lemur, lemur) 7 Paperdoll Slices.
Follows:
- docs/world/STAR_RING_LEMUR_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, ivory polymer chassis #FFFDF8,
  orbital luminescent radar cowl with mint fiber glow #4ED86A,
  amber pulsar dual visors #FFA010/#FFD028,
  astronaut stealth harness cuirass #38A0FF/#FFA010,
  segmented neon optical fiber star-ring antenna tail #1A243B/#4ED86A/#FFD028,
  tri-ring orbit brass wind-up key with center coral pink rivet #FFD028/#FF5E8A,
  orbital pulse twin daggers with sky blue ionization groove & mint guard teeth #38A0FF/#4ED86A)
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
LEMUR_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lemur"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (Star-Ring Lemur Specification)
OUTLINE = np.array([31, 26, 58], dtype=float)           # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = np.array([145, 115, 30], dtype=float)     # Warm golden bronze for key filigree (0-ART29)

# 1. Base / Ivory High-Impact Polymer (#FFFDF8) - Lemur Core Chassis & Helmet
POLYMER_SHINE  = np.array([255, 255, 255], dtype=float)
POLYMER_LIGHT  = np.array([255, 253, 248], dtype=float)
POLYMER_BASE   = np.array([242, 238, 230], dtype=float)
POLYMER_SHADOW = np.array([214, 208, 196], dtype=float)
POLYMER_DARK   = np.array([182, 174, 162], dtype=float)
POLYMER_DEEP   = np.array([145, 136, 125], dtype=float)

# 2. Secondary / Dopamine Celestial Sky Blue (#38A0FF) - Stealth Harness, Dagger Primary Blade
SKY_SHINE = np.array([205, 238, 255], dtype=float)
SKY_LIGHT = np.array([135, 210, 255], dtype=float)
SKY_BASE  = np.array([56, 160, 255], dtype=float)
SKY_DARK  = np.array([24, 105, 195], dtype=float)
SKY_DEEP  = np.array([15, 60, 130], dtype=float)

# 3. Mint Green / Optical Fiber Cold Light (#4ED86A) - Fiber Tail Rings, Radar Rim, Dagger Parrying Teeth
MINT_SHINE = np.array([195, 255, 215], dtype=float)
MINT_LIGHT = np.array([135, 242, 165], dtype=float)
MINT_BASE  = np.array([78, 216, 106], dtype=float)
MINT_DARK  = np.array([42, 160, 68], dtype=float)
MINT_DEEP  = np.array([22, 105, 42], dtype=float)

# 4. Metal / Dopamine Foundry Brass Gold (#FFD028) - Orbit Key, Antenna Sphere, Dagger Guard Ring
GOLD_SHINE = np.array([255, 250, 185], dtype=float)
GOLD_LIGHT = np.array([255, 235, 115], dtype=float)
GOLD_BASE  = np.array([255, 208, 40], dtype=float)
GOLD_DARK  = np.array([195, 145, 18], dtype=float)
GOLD_DEEP  = np.array([130, 90, 10], dtype=float)

# 5. Accent / Dopamine Warm Sunset Orange (#FFA010) - Amber Visors, Harness Warning Stripes
ORANGE_SHINE = np.array([255, 225, 145], dtype=float)
ORANGE_LIGHT = np.array([255, 195, 80], dtype=float)
ORANGE_BASE  = np.array([255, 160, 16], dtype=float)
ORANGE_DARK  = np.array([205, 115, 8], dtype=float)
ORANGE_DEEP  = np.array([145, 75, 5], dtype=float)

# 6. Coral Pink (#FF5E8A) - Key Center Rivet, Shock Damper Rings
CORAL_SHINE = np.array([255, 210, 230], dtype=float)
CORAL_LIGHT = np.array([255, 150, 182], dtype=float)
CORAL_BASE  = np.array([255, 94, 138], dtype=float)
CORAL_DARK  = np.array([195, 55, 95], dtype=float)

# 7. Deep Space Matte Night Blue-Black (#1A243B) - Fiber Tail Black Rings, Visor Anti-Glare Eye Mask
SPACE_SHINE = np.array([75, 92, 122], dtype=float)
SPACE_LIGHT = np.array([48, 62, 88], dtype=float)
SPACE_BASE  = np.array([26, 36, 59], dtype=float)
SPACE_DARK  = np.array([16, 22, 38], dtype=float)
SPACE_DEEP  = np.array([10, 14, 25], dtype=float)

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
    三環軌道星環黃銅發條鑰匙 (key_lemur_tri_ring_orbit_brass)
    Tri-Ring Orbit Brass Wind-up Key.
    Central axle extending from chassis socket (44, 48) to key center (38, 28).
    Three concentric orbital rings (radii 18, 12, 6) with 3 radial spokes at 90, 210, 330 deg.
    Center coral pink rivet, warm golden bronze outline OUTLINE_KEY.
    Strictly follows 0-ART29 & 0-QA16: no dark block run >= 13, white run < 40.
    """
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    kcx, kcy = 38.0, 28.0

    # 1. Axle connecting chassis socket (44, 48) to key center (38, 28)
    for t in np.linspace(0.0, 1.0, 30):
        ax = 45.0 * (1.0 - t) + kcx * t
        ay = 48.0 * (1.0 - t) + kcy * t
        for off in [-1.5, -0.5, 0.5, 1.5]:
            px = int(round(ax + off * 0.8))
            py = int(round(ay - off * 0.6))
            if 0 <= px < W and 0 <= py < H:
                dot = off / 1.5
                col = GOLD_LIGHT if dot > 0.2 else (GOLD_BASE if dot > -0.4 else GOLD_DARK)
                key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 2. Three Concentric Planetary Orbit Rings
    # Outer ring: r = 16..19.5, Mid ring: r = 10.5..13.5, Inner collar: r = 5.0..7.5
    rings = [
        (16.0, 19.5, 0.0),
        (10.5, 13.5, 0.5),
        (5.0, 7.5, 1.0)
    ]
    for r_in, r_out, phase in rings:
        for y in range(int(kcy - r_out - 1), int(kcy + r_out + 2)):
            for x in range(int(kcx - r_out - 1), int(kcx + r_out + 2)):
                dx = x - kcx
                dy = y - kcy
                r = math.sqrt(dx**2 + dy**2)
                if r_in <= r <= r_out:
                    ang = math.atan2(dy, dx)
                    dot = -0.55 * (dx / r) - 0.70 * (dy / r)
                    # Decorative tick marks along outer ring
                    tick = (math.cos(ang * 12.0 + phase) > 0.5) if r_out > 15.0 else False
                    if tick:
                        col = GOLD_SHINE
                    elif dot > 0.40:
                        col = GOLD_SHINE * 0.5 + GOLD_LIGHT * 0.5
                    elif dot > 0.0:
                        col = GOLD_BASE + dot * 20.0
                    elif dot > -0.35:
                        col = GOLD_DARK
                    else:
                        col = GOLD_DEEP
                    key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 3. Three Radial Spokes at angles: -90 deg, 30 deg, 150 deg
    spoke_angles = [-math.pi / 2.0, math.pi / 6.0, math.pi * 5.0 / 6.0]
    for ang in spoke_angles:
        cos_a = math.cos(ang)
        sin_a = math.sin(ang)
        for r_step in np.linspace(6.0, 18.5, 30):
            sx = kcx + r_step * cos_a
            sy = kcy + r_step * sin_a
            for perp in [-0.8, 0.0, 0.8]:
                px = int(round(sx - perp * sin_a))
                py = int(round(sy + perp * cos_a))
                if 0 <= px < W and 0 <= py < H:
                    col = GOLD_LIGHT if perp < 0 else GOLD_BASE
                    key_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Central Coral Pink Rivet (#FF5E8A) with brass bezel
    for y in range(int(kcy - 4), int(kcy + 5)):
        for x in range(int(kcx - 4), int(kcx + 5)):
            r = math.sqrt((x - kcx)**2 + (y - kcy)**2)
            if r <= 3.8:
                dot = -0.6 * (x - kcx) / 3.8 - 0.6 * (y - kcy) / 3.8
                if r <= 2.2:
                    col = CORAL_SHINE if dot > 0.3 else (CORAL_BASE if dot > -0.3 else CORAL_DARK)
                else:
                    col = GOLD_SHINE if dot > 0.3 else GOLD_BASE
                key_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    key_img.putpixel((int(kcx - 1), int(kcy - 1)), (255, 255, 255, 255))

    out_key = apply_antialiased_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=50)
    return out_key


def build_back_curio() -> Image.Image:
    """
    SLICE 2: BACK CURIO (z=8)
    多節霓光光纖星環天線尾 (curio_lemur_neon_ring_fiber_tail)
    Segmented Neon Optical Fiber Star-Ring Antenna Tail.
    Seven segmented coaxial alternating rings (Matte Night Blue-Black #1A243B & Luminescent Mint #4ED86A).
    Signature acrobatic S-curve tail arching gracefully from hips (48, 88) up to antenna orb (28, 38).
    Omnidirectional golden attitude sphere at tail tip with rainbow fiber glow.
    """
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Tail Spine Bezier Curve Control Points:
    # Hip base (48, 90) -> (36, 78) -> (22, 60) -> (24, 42) -> Tip (32, 32)
    p0 = np.array([48.0, 90.0])
    p1 = np.array([32.0, 78.0])
    p2 = np.array([18.0, 58.0])
    p3 = np.array([24.0, 40.0])
    p4 = np.array([34.0, 32.0])

    num_samples = 120
    curve_pts = []
    for t in np.linspace(0.0, 1.0, num_samples):
        # 4th degree Bezier
        pt = ((1-t)**4 * p0 + 4*(1-t)**3*t * p1 + 6*(1-t)**2*t**2 * p2 + 4*(1-t)*t**3 * p3 + t**4 * p4)
        curve_pts.append(pt)

    # Draw segmented rings along the tail (7 distinct segments)
    # Segments alternate: Space Black (#1A243B) and Mint Fiber (#4ED86A)
    for i, pt in enumerate(curve_pts):
        t_val = i / float(num_samples)
        seg_idx = int(t_val * 7.0)
        is_mint_ring = (seg_idx % 2 == 1)

        # Radius tapers slightly from 4.8 at base to 3.2 near tip
        radius = 4.8 * (1.0 - t_val * 0.35)

        # Normal vector to curve
        if i < num_samples - 1:
            tangent = curve_pts[i + 1] - pt
        else:
            tangent = pt - curve_pts[i - 1]
        t_len = np.linalg.norm(tangent) + 1e-6
        normal = np.array([-tangent[1], tangent[0]]) / t_len

        for off in np.linspace(-radius, radius, 15):
            s_pt = pt + normal * off
            px, py = int(round(s_pt[0])), int(round(s_pt[1]))
            if 0 <= px < W and 0 <= py < H:
                dist = abs(off) / radius
                dot = -0.6 * (normal[0] * (off / radius)) - 0.6 * (normal[1] * (off / radius))

                if is_mint_ring:
                    # Luminescent optical fiber ring
                    if dist < 0.4:
                        col = MINT_SHINE * 0.7 + WHITE_SHINE * 0.3
                    elif dist < 0.75:
                        col = MINT_LIGHT + dot * 15.0
                    else:
                        col = MINT_BASE + dot * 10.0
                else:
                    # Matte black polymer ring
                    if dist < 0.3:
                        col = SPACE_SHINE + dot * 20.0
                    elif dist < 0.7:
                        col = SPACE_BASE + dot * 15.0
                    else:
                        col = SPACE_DARK

                curio_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Tip Attitude Antenna Sphere at (34, 32)
    tcx, tcy = 34.0, 32.0
    for y in range(int(tcy - 5), int(tcy + 6)):
        for x in range(int(tcx - 5), int(tcx + 6)):
            r = math.sqrt((x - tcx)**2 + (y - tcy)**2)
            if r <= 4.5:
                dot = -0.55 * (x - tcx) / 4.5 - 0.70 * (y - tcy) / 4.5
                if dot > 0.40:
                    col = GOLD_SHINE * 0.6 + GOLD_LIGHT * 0.4
                elif dot > 0.0:
                    col = GOLD_BASE + dot * 20.0
                elif dot > -0.35:
                    col = GOLD_DARK
                else:
                    col = GOLD_DEEP
                curio_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Micro Antenna Needle tip extending to (38, 25)
    cd.line([(34, 30), (39, 24)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
    curio_img.putpixel((39, 24), (255, 255, 255, 255))

    out_curio = apply_antialiased_outline(curio_img, outline_color=OUTLINE, min_alpha=50)

    # Add soft mint fiber optical corona around tail tip (without harsh black borders)
    glow_puffs = [(34.0, 32.0, 3.5), (28.0, 38.0, 3.0)]
    for gx, gy, gr in glow_puffs:
        for y in range(int(gy - gr - 1), int(gy + gr + 2)):
            for x in range(int(gx - gr - 1), int(gx + gr + 2)):
                dist = math.sqrt((x - gx)**2 + (y - gy)**2)
                if dist <= gr:
                    alpha = int(np.clip((1.0 - dist / gr) * 90.0, 0, 110))
                    curr = out_curio.getpixel((x, y))
                    if curr[3] == 0:
                        out_curio.putpixel((x, y), tuple(MINT_LIGHT.astype(int)) + (alpha,))

    return out_curio


def build_chassis() -> Image.Image:
    """
    SLICE 3: CHASSIS (z=10)
    星穹輕量聚合物高機動底盤 (chassis_lemur_orbit_polymer_default)
    2.2 head-body ratio chibi chassis, ivory polymer body (#FFFDF8 / POLYMER),
    sky blue & mint conductive silicone anti-skid hand/foot pads,
    nylon self-lubricating ball joints at knees, ankles, and shoulders.
    STRICT 0-ART9 / 0-ART11: x >= 94 MUST BE 0 PIXELS.
    STRICT 0-ART18: Bare torso unique colors >= 10.
    """
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow (y: 114..120)
    chd.ellipse([64 - 26, 116 - 4, 64 + 26, 116 + 5], fill=(31, 26, 58, 125))
    chd.ellipse([64 - 16, 116 - 3, 64 + 16, 116 + 4], fill=(31, 26, 58, 165))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.1))

    # 2. Lower Limbs & Anti-Skid Silicone Paw Pads (y: 96..112)
    # Left foot: centered at (50, 105), Right foot: centered at (74, 105)
    for bx, by in [(50.0, 105.0), (74.0, 105.0)]:
        # Thigh / Lower leg ivory polymer cylinder
        for y in range(int(by - 13), int(by)):
            for x in range(int(bx - 6), int(bx + 7)):
                dx = (x - bx) / 5.5
                dy = (y - (by - 7.5)) / 6.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.7 * dy
                    if dot > 0.35:
                        col = POLYMER_LIGHT + dot * 12.0
                    elif dot > -0.2:
                        col = POLYMER_BASE + dot * 18.0
                    else:
                        col = POLYMER_SHADOW + dot * 15.0
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Nylon spherical knee joint (brass / sky blue bezel)
        for y in range(int(by - 10), int(by - 5)):
            for x in range(int(bx - 3), int(bx + 4)):
                if (x - bx)**2 + (y - (by - 7.5))**2 <= 7.0:
                    dot = -0.6 * (x - bx) / 2.6 - 0.6 * (y - by + 7.5) / 2.6
                    col = SKY_LIGHT if dot > 0.3 else (SKY_BASE if dot > -0.3 else SKY_DARK)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Paw Footpad Base (Conductive Silicone Grip Pad)
        for y in range(int(by - 5), int(by + 7)):
            for x in range(int(bx - 7), int(bx + 8)):
                dx = (x - bx) / 6.5
                dy = (y - by) / 5.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.5 * dx - 0.6 * dy
                    # Sole pad is mint silicone, upper shell is ivory polymer
                    if y >= by + 2:
                        col = MINT_SHINE if dot > 0.3 else (MINT_BASE if dot > -0.3 else MINT_DARK)
                    else:
                        col = POLYMER_LIGHT if dot > 0.3 else (POLYMER_BASE if dot > -0.3 else POLYMER_SHADOW)
                    chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Paw toe pads (3 micro rounded silicone nodes)
        for tx in [bx - 4, bx, bx + 4]:
            chd.ellipse([tx - 1, by + 4, tx + 1, by + 6], fill=tuple(MINT_LIGHT.astype(int)) + (255,))

    # 3. Main Torso Chassis (y: 58..94, x: 44..84)
    # Chibi egg-like aerodynamic polymer capsule
    tcx, tcy = 64.0, 75.0
    for y in range(58, 95):
        for x in range(44, 85):
            dx = (x - tcx) / 18.0
            dy = (y - tcy) / 16.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz

                # Multi-tone depth cel-shading (0-ART18: rich unique colors >= 10)
                if dot > 0.50:
                    col = POLYMER_SHINE * 0.4 + POLYMER_LIGHT * 0.6 + dot * 10.0
                elif dot > 0.20:
                    col = POLYMER_LIGHT * 0.7 + POLYMER_BASE * 0.3 + (dot - 0.20) * 25.0
                elif dot > -0.15:
                    col = POLYMER_BASE + dot * 20.0
                elif dot > -0.45:
                    col = POLYMER_SHADOW + (dot + 0.45) * 20.0
                else:
                    col = POLYMER_DARK + (dot + 0.65) * 15.0

                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # 4. Belly Insulative Glaze Plate & Anti-Static Seams
    for y in range(64, 91):
        for x in range(52, 77):
            dx = (x - tcx) / 11.5
            dy = (y - (tcy + 2.0)) / 12.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                if dot > 0.30:
                    col = POLYMER_SHINE * 0.5 + POLYMER_LIGHT * 0.5
                elif dot > -0.10:
                    col = POLYMER_LIGHT * 0.6 + POLYMER_BASE * 0.4
                else:
                    col = POLYMER_SHADOW
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Fine panel groove & micro rivets
    chd = ImageDraw.Draw(chassis_img)
    chd.line([(64, 66), (64, 88)], fill=tuple(SKY_DARK.astype(int)) + (255,), width=1)
    chd.line([(54, 76), (74, 76)], fill=tuple(SKY_DARK.astype(int)) + (255,), width=1)
    for ry in [70, 78, 86]:
        for rx in [56, 72]:
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # 5. Shoulders & Arms:
    # Left Arm: held inward holding parrying dagger (x: 36..48, y: 64..79)
    for y in range(64, 80):
        for x in range(36, 49):
            dx = (x - 42.5) / 5.5
            dy = (y - 71.5) / 7.5
            if dx**2 + dy**2 <= 1.0:
                dot = -0.6 * dx - 0.6 * dy
                col = POLYMER_LIGHT if dot > 0.3 else (POLYMER_BASE if dot > -0.2 else POLYMER_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Left Palm Node with Silicone Grip (x: 42..46, y: 74..78)
    chd.ellipse([42, 74, 46, 78], fill=tuple(MINT_BASE.astype(int)) + (255,), outline=tuple(MINT_DARK.astype(int)) + (255,))

    # Right Arm: extending forward holding main dagger (x: 80..91, y: 65..78)
    # STRICT 0-ART9/11: x MUST NOT exceed 93!
    for y in range(65, 78):
        for x in range(80, 92):
            dx = (x - 85.5) / 5.0
            dy = (y - 71.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                dot = -0.5 * dx - 0.7 * dy
                col = POLYMER_LIGHT if dot > 0.3 else (POLYMER_BASE if dot > -0.2 else POLYMER_SHADOW)
                chassis_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Right Palm / Wrist node (x: 88..91, y: 70..74)
    chd.ellipse([88, 70, 91, 74], fill=tuple(MINT_BASE.astype(int)) + (255,), outline=tuple(MINT_DARK.astype(int)) + (255,))
    chassis_img.putpixel((89, 71), (255, 255, 255, 255))

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
    星軌冷光雷達耳罩面甲 (head_lemur_orbit_radar_cowl)
    Ivory polymer helmet dome (#FFFDF8 / POLYMER),
    signature large orbital radar cowl ears with mint luminescent rim (#38A0FF / #4ED86A),
    brass pivot hinges, streamlined forehead sensor ridge.
    STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
      Left eye: x: 50..58, y: 38..46
      Right eye: x: 70..78, y: 38..46
    STRICT 0-ART28q: Average plate color distance to chassis L2 < 60.0.
    """
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Signature Large Orbital Radar Cowl Ears (Iconic Lemur radar dish ears)
    # Left Ear: center (34, 28), radius rx=11, ry=14, rotated ~-20 deg
    # Right Ear: center (94, 28), radius rx=11, ry=14, rotated ~+20 deg
    for ex_c, ey_c, is_right in [(34.0, 28.0, False), (94.0, 28.0, True)]:
        ang_rot = math.radians(22.0 if is_right else -22.0)
        cos_e, sin_e = math.cos(ang_rot), math.sin(ang_rot)
        rx, ry = 10.5, 13.5

        for y in range(int(ey_c - ry - 2), int(ey_c + ry + 3)):
            for x in range(int(ex_c - rx - 2), int(ex_c + rx + 3)):
                # Rotate into ear-local coords
                dx_w = x - ex_c
                dy_w = y - ey_c
                dx_l = dx_w * cos_e + dy_w * sin_e
                dy_l = -dx_w * sin_e + dy_w * cos_e

                dsq = (dx_l / rx)**2 + (dy_l / ry)**2
                if dsq <= 1.0:
                    dist = math.sqrt(dsq)
                    dot = -0.5 * (dx_l / rx) - 0.7 * (dy_l / ry)

                    # Outer rim has glowing mint optical fiber ring
                    if dist > 0.78:
                        col = MINT_SHINE if dot > 0.2 else MINT_BASE
                    elif dist > 0.55:
                        # Polycarbonate translucent radar dome (Sky Blue)
                        col = SKY_LIGHT if dot > 0.3 else (SKY_BASE if dot > -0.2 else SKY_DARK)
                    else:
                        # Inner acoustic concavity (Ivory polymer dish)
                        col = POLYMER_LIGHT if dot > 0.4 else (POLYMER_BASE if dot > -0.1 else POLYMER_SHADOW)

                    head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Brass pivot hinge at ear root (attaching to helmet)
        hx = ex_c + (5.0 if not is_right else -5.0)
        hy = ey_c + 9.0
        hd.ellipse([hx - 2, hy - 2, hx + 2, hy + 2], fill=tuple(GOLD_BASE.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))
        head_img.putpixel((int(hx), int(hy)), (255, 255, 255, 255))

    # 2. Main Helmet Dome (x: 44..84, y: 22..62)
    hcx, hcy = 64.0, 42.0
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            dsq = dx**2 + dy**2
            if dsq <= 1.0:
                nz = math.sqrt(max(0.0, 1.0 - dsq))
                dot = -0.55 * dx - 0.70 * dy + 0.45 * nz

                # Ivory polymer helmet shell (matches chassis for 0-ART28q L2 < 60.0)
                if dot > 0.45:
                    col = POLYMER_SHINE * 0.4 + POLYMER_LIGHT * 0.6 + dot * 12.0
                elif dot > 0.10:
                    col = POLYMER_LIGHT * 0.6 + POLYMER_BASE * 0.4 + (dot - 0.10) * 25.0
                elif dot > -0.25:
                    col = POLYMER_BASE + dot * 20.0
                elif dot > -0.55:
                    col = POLYMER_SHADOW + (dot + 0.55) * 18.0
                else:
                    col = POLYMER_DARK

                head_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Forehead Sensor Crest & Orbit Ring Marking
    hd = ImageDraw.Draw(head_img)
    hd.arc([50, 25, 78, 38], start=180, end=360, fill=tuple(SKY_BASE.astype(int)) + (255,), width=2)
    hd.arc([52, 27, 76, 37], start=180, end=360, fill=tuple(GOLD_BASE.astype(int)) + (255,), width=1)
    hd.ellipse([62, 28, 66, 32], fill=tuple(MINT_LIGHT.astype(int)) + (255,), outline=tuple(MINT_DARK.astype(int)) + (255,))
    head_img.putpixel((64, 29), (255, 255, 255, 255))

    # Muzzle & Anti-Static Sensor Nose (64, 52)
    hd.ellipse([61, 49, 67, 54], fill=tuple(SPACE_BASE.astype(int)) + (255,), outline=tuple(OUTLINE.astype(int)) + (255,))
    hd.point((64, 51), fill=tuple(ORANGE_LIGHT.astype(int)) + (255,))

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

    return Image.fromarray(head_arr, "RGBA")


def build_costume() -> Image.Image:
    """
    SLICE 5: COSTUME (z=25)
    宇航匿蹤輕量安全吊帶胸甲 (costume_lemur_astro_stealth_harness)
    High-density metallic woven nylon harness (#38A0FF) with sunset orange warning trims (#FFA010),
    micro cold-gas vector thrusters on both shoulders (x: 36..47, y: 58..72 and x: 81..92, y: 58..72),
    central pressure release dial and dopamine coral pink gasket.
    STRICT 0-ART26b: y >= 96 MUST BE 0 PIXELS.
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # Harness Cuirass Body: from y=62 to y=94 (strictly decoupled at y < 96)
    for y in range(62, 95):
        if y < 74:
            x_min = 52 - int((y - 62) * 0.3)
            x_max = 76 + int((y - 62) * 0.3)
        else:
            x_min = 49 - int((y - 74) * 0.2)
            x_max = 79 + int((y - 74) * 0.2)

        for x in range(x_min, x_max + 1):
            dx = (x - 64.0) / ((x_max - x_min) / 2.0)
            dy = (y - 78.0) / 16.0
            dot = -0.55 * dx - 0.70 * dy

            # Sky blue tactical harness fabric
            if dot > 0.40:
                col = SKY_SHINE * 0.4 + SKY_LIGHT * 0.6
            elif dot > 0.0:
                col = SKY_BASE + dot * 20.0
            elif dot > -0.35:
                col = SKY_DARK + (dot + 0.35) * 20.0
            else:
                col = SKY_DEEP

            costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sunset Orange Reflective Warning Stripes & Harness Straps
    cd.line([(53, 64), (64, 78)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    cd.line([(75, 64), (64, 78)], fill=tuple(ORANGE_BASE.astype(int)) + (255,), width=2)
    cd.line([(48, 93), (80, 93)], fill=tuple(ORANGE_LIGHT.astype(int)) + (255,), width=2)

    # Center Pressure Dial & Coral Pink Valve Gasket at (64, 78)
    cd.ellipse([60, 74, 68, 82], fill=tuple(SPACE_BASE.astype(int)) + (255,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
    cd.ellipse([62, 76, 66, 80], fill=tuple(CORAL_BASE.astype(int)) + (255,))
    costume_img.putpixel((64, 77), (255, 255, 255, 255))

    # Dual Shoulder Micro Cold-Gas Thrusters
    # Left Thruster: (37..47, 59..72), Right Thruster: (81..91, 59..72)
    for tx_c, is_right in [(42.0, False), (86.0, True)]:
        for y in range(59, 73):
            for x in range(int(tx_c - 5), int(tx_c + 6)):
                dx = (x - tx_c) / 5.0
                dy = (y - 65.5) / 6.5
                if dx**2 + dy**2 <= 1.0:
                    dot = -0.6 * dx - 0.6 * dy
                    if dot > 0.35:
                        col = GOLD_SHINE * 0.4 + GOLD_LIGHT * 0.6
                    elif dot > -0.15:
                        col = GOLD_BASE + dot * 20.0
                    else:
                        col = GOLD_DARK
                    costume_img.putpixel((x, y), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

        # Thruster nozzle vent rings
        cd.ellipse([tx_c - 3, 60, tx_c + 3, 64], fill=tuple(SPACE_DARK.astype(int)) + (255,), outline=tuple(GOLD_LIGHT.astype(int)) + (255,))
        cd.point((tx_c, 62), fill=tuple(MINT_LIGHT.astype(int)) + (255,))

    out_costume = apply_antialiased_outline(costume_img, outline_color=OUTLINE, min_alpha=50)

    # STRICT 0-ART26b check: enforce y >= 96 is completely zeroed out
    arr = np.array(out_costume)
    arr[96:, :, :] = 0
    return Image.fromarray(arr, "RGBA")


def build_optic_core() -> Image.Image:
    """
    SLICE 6: OPTIC CORE (z=30)
    琥珀脈衝星穹雙目鏡 (face_lemur_amber_pulsar_visors)
    Pair of spherical high-transmittance amber pulsar visors inserted into head_unit eye sockets:
      Left Eye:  center (54, 42), bounds (50..58, 38..46)
      Right Eye: center (74, 42), bounds (70..78, 38..46)
    Surrounded by anti-glare dark blue-purple eyemask frames (#1F1A3A),
    amber / gold pulsing radar reticle lines & warm glow.
    STRICT 0-ART27: Center alpha MUST BE 255.
    Hollow sockets 100% covered by dark frame + crystal, zero holes.
    """
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    eye_centers = [(54, 42), (74, 42)]
    radius = 4.2

    for cx, cy in eye_centers:
        # 1. Fill entire socket rectangle with dark blue-purple eyemask frame (#1F1A3A)
        cored.rounded_rectangle([cx - 4, cy - 4, cx + 4, cy + 4], radius=1, fill=tuple(OUTLINE.astype(int)) + (255,))

        # 2. Spherical Amber Pulsar lens inside frame
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

        # Concentric radar reticle lines (Pulsar grid)
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), width=1)
        cored.point((cx, cy), fill=tuple(ORANGE_SHINE.astype(int)) + (255,))

        # Specular white eye reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=tuple(WHITE_SHINE.astype(int)) + (255,))
        cored.point((cx + 2, cy + 2), fill=tuple(GOLD_BASE.astype(int)) + (255,))

    return apply_antialiased_outline(core_img, outline_color=OUTLINE, min_alpha=50)


def build_weapon() -> Image.Image:
    """
    SLICE 7: WEAPON (z=40)
    星軌脈衝雙鋒短匕 (weapon_lemur_orbital_pulse_daggers)
    Orbital Pulse Twin Daggers.
    Follows 0-MKT7: Asymmetric pair of daggers with distinct primary/secondary roles:
      1. Primary Dagger (Right Hand, reverse grip):
         Hilt centered at (89, 72).
         Blade angles downward across chest from (89, 72) to (98, 58) and (80, 84).
         Sky Blue (#38A0FF) ionized energy groove, micro cold-gas exhaust vent,
         stamped polycarbonate star-ring guard with gold brass ring (#FFD028).
      2. Secondary Parrying Dagger (Left Hand, defensive guard):
         Hilt centered at (44, 76).
         Shorter parrying blade extending from (44, 76) to (50, 92),
         Mint green (#4ED86A) optical range-finding parrying teeth.
    Zero body or arm baked into weapon (0-ART9/11).
    """
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # ─────────────────────────────────────────────────────────────
    # 1. Primary Dagger (Right Hand, reverse grip)
    # Hilt at (89, 72), Main Blade tip sweeps to (76, 88)
    # ─────────────────────────────────────────────────────────────
    h_cx, h_cy = 89.0, 72.0

    # Star-Ring Guard (Gold Brass Ring + Polycarbonate disc)
    wd.ellipse([h_cx - 5, h_cy - 5, h_cx + 5, h_cy + 5], fill=tuple(SKY_BASE.astype(int)) + (200,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
    wd.ellipse([h_cx - 3, h_cy - 3, h_cx + 3, h_cy + 3], fill=tuple(GOLD_LIGHT.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Pommel & Cold-Gas Vent (opposite blade, extending to (96, 62))
    for t in np.linspace(0.0, 1.0, 18):
        px = int(round(h_cx + t * 7.0))
        py = int(round(h_cy - t * 9.0))
        for off in [-1, 0, 1]:
            weapon_img.putpixel((px + off, py), tuple(GOLD_BASE.astype(int)) + (255,))
    wd.ellipse([95, 60, 99, 64], fill=tuple(MINT_LIGHT.astype(int)) + (255,), outline=tuple(GOLD_DARK.astype(int)) + (255,))

    # Main Blade: Reverse grip slicing downward-forward to (75, 87)
    blade_pts = [(88.0, 74.0), (84.0, 80.0), (76.0, 88.0), (81.0, 84.0), (89.0, 76.0)]
    for t in np.linspace(0.0, 1.0, 45):
        # Blade centerline
        bx = (1-t) * 88.0 + t * 76.0
        by = (1-t) * 74.0 + t * 88.0
        width = 3.6 * (1.0 - t * 0.7)
        # Normal
        nx, ny = -0.76, -0.65
        for w_off in np.linspace(-width, width, 9):
            px = int(round(bx + w_off * nx))
            py = int(round(by + w_off * ny))
            if 0 <= px < W and 0 <= py < H:
                dot = w_off / width
                if abs(w_off) < 0.9:
                    # Sky Blue Ionization Groove
                    col = SKY_SHINE if t < 0.7 else WHITE_SHINE
                elif dot > 0:
                    col = SKY_LIGHT
                else:
                    col = SKY_BASE
                weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Sharp cutting tip highlight at (76, 88)
    wd.point((76, 88), fill=tuple(WHITE_SHINE.astype(int)) + (255,))

    # ─────────────────────────────────────────────────────────────
    # 2. Secondary Parrying Dagger (Left Hand, defensive guard)
    # Hilt at (44, 76), Parrying Blade extending to (52, 92)
    # ─────────────────────────────────────────────────────────────
    sh_cx, sh_cy = 44.0, 76.0

    # Star-Ring Guard on parrying dagger
    wd.ellipse([sh_cx - 4, sh_cy - 4, sh_cx + 4, sh_cy + 4], fill=tuple(MINT_BASE.astype(int)) + (200,), outline=tuple(GOLD_BASE.astype(int)) + (255,))
    wd.ellipse([sh_cx - 2, sh_cy - 2, sh_cx + 2, sh_cy + 2], fill=tuple(GOLD_LIGHT.astype(int)) + (255,))

    # Parrying Pommel (extending up-left to (38, 68))
    for t in np.linspace(0.0, 1.0, 14):
        px = int(round(sh_cx - t * 6.0))
        py = int(round(sh_cy - t * 8.0))
        weapon_img.putpixel((px, py), tuple(GOLD_BASE.astype(int)) + (255,))
    wd.ellipse([37, 67, 40, 70], fill=tuple(GOLD_SHINE.astype(int)) + (255,))

    # Parrying Blade: extending down-right to (52, 92)
    for t in np.linspace(0.0, 1.0, 35):
        bx = (1-t) * 45.0 + t * 52.0
        by = (1-t) * 78.0 + t * 92.0
        width = 2.8 * (1.0 - t * 0.6)
        nx, ny = -0.89, 0.45
        for w_off in np.linspace(-width, width, 7):
            px = int(round(bx + w_off * nx))
            py = int(round(by + w_off * ny))
            if 0 <= px < W and 0 <= py < H:
                # Mint green optical parrying blade with serrated teeth
                if abs(w_off) < 0.8:
                    col = MINT_SHINE if t < 0.6 else WHITE_SHINE
                elif w_off > 0:
                    col = MINT_LIGHT
                else:
                    col = MINT_BASE
                weapon_img.putpixel((px, py), tuple(np.clip(col, 0, 255).astype(int)) + (255,))

    # Optical range-finding serration teeth on parrying edge
    for ty in [82, 86, 90]:
        tx = int(round(45.0 + (ty - 78.0) * (7.0 / 14.0) - 2.5))
        wd.point((tx, ty), fill=tuple(MINT_SHINE.astype(int)) + (255,))

    return apply_antialiased_outline(weapon_img, outline_color=OUTLINE, min_alpha=50)


def build_all_lemur_slices():
    print("=== BUILDING STAR-RING LEMUR 7 PAPERDOLL SLICES ===")

    # Generate each slice independently
    key_img = build_winding_key()
    curio_img = build_back_curio()
    chassis_img = build_chassis()
    head_img = build_head_unit()
    costume_img = build_costume()
    core_img = build_optic_core()
    weapon_img = build_weapon()

    slice_data = [
        ("winding_key", "key_lemur_tri_ring_orbit_brass", key_img),
        ("back_curio", "curio_lemur_neon_ring_fiber_tail", curio_img),
        ("chassis", "chassis_lemur_orbit_polymer_default", chassis_img),
        ("head_unit", "head_lemur_orbit_radar_cowl", head_img),
        ("costume", "costume_lemur_astro_stealth_harness", costume_img),
        ("optic_core", "face_lemur_amber_pulsar_visors", core_img),
        ("weapon", "weapon_lemur_orbital_pulse_daggers", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{LEMUR_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_lemur_tri_ring_orbit_brass.png")
    key_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{KEY_DIR}/key_lemur_tri_ring_orbit_brass_512.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_lemur_orbital_pulse_daggers.png")
    weapon_img.resize((512, 512), Image.Resampling.LANCZOS).save(f"{WEAPON_DIR}/weapon_lemur_orbital_pulse_daggers_512.png")
    print("  ✓ Universal key and weapon copies updated (128 & 512)")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot, item_id, _ in slice_data:
        p128 = f"{LEMUR_PD_DIR}/{slot}/{item_id}.png"
        s_im = Image.open(p128).convert("RGBA")
        composite.alpha_composite(s_im)

    proof_comp = f"{LEMUR_PD_DIR}/proof_paperdoll_lemur_composite.png"
    composite.save(proof_comp)

    # Magenta background composite
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{LEMUR_PD_DIR}/proof_paperdoll_lemur_magenta.png"
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

    strip_path = f"{LEMUR_PD_DIR}/proof_lemur_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/lemur_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/lemur_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/lemur_idle.png
    p_idle_64 = f"{PLAYER_DIR}/lemur_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/lemur_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/lemur_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/lemur_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/lemur_idle.png"
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
        showcase_path = f"{SHOWCASE_DIR}/lemur_idle_hd.png"
        showcase.save(showcase_path)
        print("  ✓ Showcase HD generated successfully:", showcase_path)

    # 6. Ensure symlink/compatibility: game/assets/sprites/player/lemur -> paperdoll/lemur
    lemur_alias_dir = f"{PLAYER_DIR}/lemur"
    if not os.path.exists(lemur_alias_dir):
        try:
            os.symlink(f"paperdoll/lemur", lemur_alias_dir)
            print("  ✓ Created compatibility symlink game/assets/sprites/player/lemur -> paperdoll/lemur")
        except Exception as e:
            print("  Note on symlink:", e)

    print("\n🎉 ALL LEMUR PAPERDOLL SLICES AND CANONICAL ASSETS BUILT SUCCESSFULLY!")


if __name__ == "__main__":
    build_all_lemur_slices()
