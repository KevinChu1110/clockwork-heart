#!/usr/bin/env python3
"""
build_gecko_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十五族 巡管守宮 (The Conduit Gecko, gecko) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CONDUIT_GECKO_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological gecko skin, cold-rolled brass sheet chassis,
  conduit scout crest & cowl, dual-ring relief valve brass winding key,
  high-pressure stealth harness & tassets, dual-slit aperture quartz lens,
  brass ratchet polygon conduit shuriken, segmented gear balance tail)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (Dawson Day 258 Series & Conduit Gecko canonical colors):
    1. Primary Hull: Cold-Rolled Brass Sheet with Mint Green Patina Enamel (#4ED86A)
    2. Chest & Underbelly: Sunny Cream Ivory White (#FFFDF8)
    3. Secondary / Trim & Winding Key: Dopamine Gold (#FFD028)
    4. Warm Brass Metal & Buckles: Industrial Warm Brass (#FFA010)
    5. Cold Stamped Tungsten Steel & Blades: Tungsten Steel (#7A8A9E, #5C6A7B)
    6. Coral Pink Vents & Suction Pads: Coral Pink (#FF5E8A)
    7. Celestial Cyan Quartz Core & Gauge: Cyan Quartz (#38A0FF)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
GECKO_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/gecko"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Conduit Gecko Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Cold-Rolled Brass Sheet with Mint Green Patina Enamel (#4ED86A)
MINT_BASE   = (78, 216, 106, 255)      # #4ED86A Mint Green Enamel
MINT_LIGHT  = (128, 238, 150, 255)     # Highlight
MINT_SHINE  = (185, 255, 200, 255)     # Specular
MINT_DARK   = (42, 160, 68, 255)       # Cel shadow
MINT_DEEP   = (24, 110, 44, 255)       # Deep seam

# 2. Chest & Underbelly: Sunny Cream Ivory White (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (238, 230, 215, 255)
IVORY_DARK   = (215, 202, 182, 255)
IVORY_DEEP   = (185, 172, 152, 255)

# 3. Secondary / Trim & Winding Key: Dopamine Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Warm Brass Metal & Buckles (#FFA010)
BRASS_BASE  = (255, 160, 16, 255)
BRASS_LIGHT = (255, 205, 80, 255)
BRASS_SHINE = (255, 240, 160, 255)
BRASS_DARK  = (190, 105, 10, 255)
BRASS_DEEP  = (130, 65, 8, 255)

# 5. Cold Stamped Tungsten Steel & Blades (#7A8A9E)
STEEL_BASE  = (122, 138, 158, 255)
STEEL_LIGHT = (165, 180, 198, 255)
STEEL_SHINE = (210, 222, 235, 255)
STEEL_DARK  = (92, 106, 123, 255)
STEEL_DEEP  = (61, 72, 86, 255)

# 6. Coral Pink Miniature Pressure Relief Ports & Paws (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 7. Celestial Cyan Quartz Core, Pressure Dial & Reticles (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

WHITE_SHINE = (255, 255, 255, 255)


def apply_clean_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=80, ignore_regions=None) -> None:
    """Safe, non-recursive, snapshot-based 1px outline pass.
    Prevents flood-fill / propagation bugs that create rectangular black artifact blocks (0-ART29).
    """
    snapshot = img.copy()
    px_snap = snapshot.load()
    if px_snap is None:
        return

    w, h = img.size
    px_dest = img.load()
    if px_dest is None:
        return

    for y in range(h):
        for x in range(w):
            if ignore_regions:
                skip = False
                for item in ignore_regions:
                    if len(item) == 4:
                        rx1, ry1, rx2, ry2 = item
                        if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                            skip = True
                            break
                    elif len(item) == 3:
                        cx, cy, rad = item
                        if (x - cx)**2 + (y - cy)**2 <= rad**2:
                            skip = True
                            break
                if skip:
                    continue

            p_curr = px_snap[x, y]
            a_curr = p_curr[3] if isinstance(p_curr, (tuple, list)) else 0
            if a_curr < min_alpha:
                has_solid_neighbor = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            p_nb = px_snap[nx, ny]
                            a_nb = p_nb[3] if isinstance(p_nb, (tuple, list)) else 0
                            if a_nb >= min_alpha:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break
                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL CONDUIT GECKO SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_gecko_dual_ring_relief_valve_brass.png
    # Features:
    # - 雙環洩壓黃銅發條鑰匙 (Dual-Ring Relief Valve Brass Winding Key)
    # - Centered at upper back, shaft extends from spine socket (64, 56) to dual rings (72, 24)
    # - Dual interlocking circular relief valve loops with center spring valve hole
    # - Polished brass gradient (#FFD028, #FFA010, #FFFDF8)
    # - Outline with warm golden bronze OUTLINE_KEY (satisfies 0-ART29 dark limit < 260px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft from spine socket (64, 56) to dual valve loop hub (72, 28)
    for t in np.linspace(0.0, 1.0, 26):
        sx = 64.0 + (72.0 - 64.0) * t
        sy = 56.0 + (28.0 - 56.0) * t
        for offset in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.3))
            shade = 1.0 - abs(offset) / 2.5
            r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * shade), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * shade), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine socket mount boss at (64, 56)
    kd.ellipse([60, 52, 68, 60], fill=BRASS_DARK, outline=OUTLINE_KEY)
    kd.ellipse([62, 54, 66, 58], fill=GOLD_BASE)

    # 2. Dual Interlocking Relief Valve Rings (Loops)
    # Loop 1 (Lower-Left Valve Ring) centered at (67.0, 22.0), outer rad=7.5, inner rad=3.8
    # Loop 2 (Upper-Right Valve Ring) centered at (77.0, 24.0), outer rad=7.0, inner rad=3.5
    rings = [
        (67.0, 22.0, 7.5, 3.8),
        (77.0, 24.0, 7.0, 3.5)
    ]
    for cx, cy, rout, rin in rings:
        for y in range(int(cy - rout - 1), int(cy + rout + 2)):
            for x in range(int(cx - rout - 1), int(cx + rout + 2)):
                d = ((x - cx)**2 + (y - cy)**2)**0.5
                if rin <= d <= rout:
                    norm = (d - rin) / (rout - rin)
                    spec = max(0.0, 1.0 - abs(norm - 0.45) / 0.55)
                    r = int(np.clip(GOLD_BASE[0] * (0.75 + 0.35 * spec) + 30 * (spec**2), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.75 + 0.35 * spec) + 30 * (spec**2), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.75 + 0.35 * spec) + 40 * (spec**2), 0, 255))
                    key_img.putpixel((x, y), (r, g, b, 255))

    # Center valve pin & spring relief aperture at junction (72, 23)
    kd.ellipse([70, 21, 74, 25], fill=BRASS_DARK, outline=OUTLINE_KEY)
    kd.ellipse([71, 22, 73, 24], fill=CORAL_BASE)
    kd.point((72, 22), fill=WHITE_SHINE)

    # Clean outline pass
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=80)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_gecko_segmented_gear_balance_tail.png
    # Features:
    # - 微型同軸多節齒輪平衡尾 (Segmented Gear Balance Tail)
    # - Originates from lower spine / pelvis at (58, 86)
    # - Dynamic S-curve sweeps down-left and arcs gracefully upwards
    # - 6 articulated hollow brass segments (#FFA010 / #FFD028) with mint green enamel (#4ED86A)
    # - End of tail features miniature magnetic anti-fall catch hook at (20, 70)
    # - Rich color depth with c100 richness
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Tail spline control points:
    # P0: (58, 86) [pelvis root]
    # P1: (48, 95) [mid descent]
    # P2: (36, 102) [lowest dip]
    # P3: (24, 98) [rebound curve]
    # P4: (18, 86) [upward sweep]
    # P5: (20, 72) [tip with catch-hook]
    tail_pts = np.array([
        [58.0, 86.0],
        [48.0, 95.0],
        [36.0, 102.0],
        [24.0, 98.0],
        [18.0, 86.0],
        [20.0, 72.0]
    ])

    # Draw 6 articulated segments along curve
    t_vals = np.linspace(0.0, 1.0, 80)
    # Cubic spline approximation via piecewise Bézier / linear interpolation
    curve_points = []
    for t in t_vals:
        # Catmull-Rom or multi-point interpolation
        idx = t * (len(tail_pts) - 1)
        i0 = int(np.floor(idx))
        i1 = min(i0 + 1, len(tail_pts) - 1)
        f = idx - i0
        pt = (1.0 - f) * tail_pts[i0] + f * tail_pts[i1]
        curve_points.append(pt)

    # 1. High-tension piano wire core line
    for i in range(len(curve_points) - 1):
        pA = curve_points[i]
        pB = curve_points[i + 1]
        cd.line([(pA[0], pA[1]), (pB[0], pB[1])], fill=STEEL_LIGHT, width=2)

    # 2. Six articulated hollow segments
    seg_centers = [curve_points[int(len(curve_points) * frac)] for frac in [0.1, 0.28, 0.46, 0.64, 0.82, 0.96]]
    seg_radii = [6.0, 5.5, 5.0, 4.5, 4.0, 3.5]

    for (sx, sy), srad in zip(seg_centers, seg_radii):
        # Outer brass segment shell
        for y in range(int(sy - srad - 1), int(sy + srad + 2)):
            for x in range(int(sx - srad - 1), int(sx + srad + 2)):
                dist = ((x - sx)**2 + (y - sy)**2)**0.5
                if dist <= srad:
                    spec = max(0.0, 1.0 - dist / srad)
                    shine = max(0.0, 1.0 - ((x - (sx - 1.0))**2 + (y - (sy - 1.0))**2)**0.5 / (srad * 0.6))**2
                    # Alternate shell plate: Mint Green enamel with Brass rim
                    if dist >= srad - 1.5:
                        r = int(np.clip(BRASS_BASE[0] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                        g = int(np.clip(BRASS_BASE[1] * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                        b = int(np.clip(BRASS_BASE[2] * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                    else:
                        r = int(np.clip(MINT_BASE[0] * (0.75 + 0.45 * spec) + 45 * shine, 0, 255))
                        g = int(np.clip(MINT_BASE[1] * (0.75 + 0.45 * spec) + 45 * shine, 0, 255))
                        b = int(np.clip(MINT_BASE[2] * (0.75 + 0.45 * spec) + 45 * shine, 0, 255))
                    curio_img.putpixel((x, y), (r, g, b, 255))

        # Miniature joint cog center
        cd.ellipse([int(sx - 2), int(sy - 2), int(sx + 2), int(sy + 2)], fill=GOLD_BASE, outline=OUTLINE)
        cd.point((int(sx), int(sy)), fill=WHITE_SHINE)

    # 3. Magnetic catch-hook at tail tip (20, 72)
    tip_x, tip_y = int(tail_pts[-1][0]), int(tail_pts[-1][1])
    cd.ellipse([tip_x - 3, tip_y - 4, tip_x + 3, tip_y + 2], fill=GOLD_BASE, outline=OUTLINE)
    # Hook curved prongs
    cd.arc([tip_x - 5, tip_y - 7, tip_x + 5, tip_y + 1], start=180, end=360, fill=BRASS_LIGHT, width=2)
    cd.point((tip_x, tip_y - 2), fill=CYAN_LIGHT)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_gecko_brass_patina_default.png
    # Features:
    # - 2.2 Chibi low-gravity agile chassis
    # - Soft ground contact shadow at (64, 116)
    # - Splayed gecko limbs with suction cog-pads on feet and left hand
    # - Left foot at (44, 113), right foot at (78, 113)
    # - Left hand extended at (34, 76) for wall grip balance
    # - Right arm tucked with wrist mount at (80, 72)
    # - STRICT 0-ART9 / 0-ART11 COMPLIANCE: x >= 94 MUST BE 0 PIXELS!
    # - Solid neck collar flange at (x: 52..76, y: 46..58) to seat head seamlessly
    # - Chest steam pressure gauge at (64, 68) with cyan glowing needle (#38A0FF)
    # - Multi-tone cel depth with unique colors >= 20 (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 5, 64 + 28, 116 + 5], fill=(31, 26, 58, 110))
    ch_d.ellipse([64 - 20, 116 - 3, 64 + 20, 116 + 3], fill=(31, 26, 58, 150))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Foot Paws with Micro-Vacuum Suction Pads at (44, 113) and (78, 113)
    paw_positions = [(44.0, 113.0), (78.0, 113.0)]
    for px, py in paw_positions:
        # Base foot pad
        ch_d.ellipse([int(px - 7), int(py - 3), int(px + 7), int(py + 3)], fill=MINT_BASE, outline=OUTLINE)
        # Coral pink center suction cushion
        ch_d.ellipse([int(px - 4), int(py - 2), int(px + 4), int(py + 2)], fill=CORAL_BASE)
        ch_d.ellipse([int(px - 2), int(py - 1), int(px + 2), int(py + 1)], fill=CORAL_LIGHT)
        # Splayed gecko toe claw tips
        for tdx in [-6, -2, 2, 6]:
            ch_d.point((int(px + tdx), int(py + 2)), fill=GOLD_BASE)
            ch_d.point((int(px + tdx), int(py + 3)), fill=BRASS_DARK)
        ch_d.point((int(px), int(py)), fill=WHITE_SHINE)

    # 3. Articulated Legs
    # Left leg: (44, 112) -> knee (46, 98) -> hip (54, 88)
    # Right leg: (78, 112) -> knee (74, 98) -> hip (68, 88)
    leg_paths = [
        [(44.0, 112.0), (46.0, 98.0), (54.0, 88.0)],
        [(78.0, 112.0), (74.0, 98.0), (68.0, 88.0)]
    ]
    for lpts in leg_paths:
        for t in np.linspace(0.0, 1.0, 24):
            if t <= 0.5:
                lx = lpts[0][0] + (lpts[1][0] - lpts[0][0]) * (t * 2.0)
                ly = lpts[0][1] + (lpts[1][1] - lpts[0][1]) * (t * 2.0)
            else:
                lx = lpts[1][0] + (lpts[2][0] - lpts[1][0]) * ((t - 0.5) * 2.0)
                ly = lpts[1][1] + (lpts[2][1] - lpts[1][1]) * ((t - 0.5) * 2.0)
            for dx in range(-4, 5):
                spec = max(0.0, 1.0 - abs(dx) / 4.5)
                r = int(np.clip(MINT_BASE[0] * (0.8 + 0.4 * spec), 0, 255))
                g = int(np.clip(MINT_BASE[1] * (0.8 + 0.4 * spec), 0, 255))
                b = int(np.clip(MINT_BASE[2] * (0.8 + 0.4 * spec), 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Knee gear dial
        kx, ky = int(lpts[1][0]), int(lpts[1][1])
        ch_d.ellipse([kx - 3, ky - 3, kx + 3, ky + 3], fill=BRASS_BASE, outline=OUTLINE)
        ch_d.point((kx, ky), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 52..76, y: 46..58)
    for y in range(46, 59):
        hw = 11.0 + (y - 46) * 0.25
        for x in range(int(64 - hw), int(64 + hw + 1)):
            spec = max(0.0, 1.0 - abs(x - 64) / (hw + 1.0))
            r = int(np.clip(MINT_DARK[0] * (0.85 + 0.3 * spec), 0, 255))
            g = int(np.clip(MINT_DARK[1] * (0.85 + 0.3 * spec), 0, 255))
            b = int(np.clip(MINT_DARK[2] * (0.85 + 0.3 * spec), 0, 255))
            chassis_img.putpixel((x, y), (r, g, b, 255))

    # 5. Main Torso Volumetric Rendering (x: 48..80, y: 56..94)
    tcx, tcy = 64.0, 74.0
    trx, try_ = 16.0, 18.0
    for y in range(56, 96):
        for x in range(46, 82):
            dx = (x - tcx) / trx
            dy = (y - tcy) / try_
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 1.1))
                shine = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 0.45))**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Center underbelly is Ivory Cream with Louvered Slats
                is_underbelly = (abs(x - tcx) <= 8.5) and (y >= 60)
                if is_underbelly:
                    is_slat_groove = (y % 4 == 0)
                    if is_slat_groove:
                        r = int(np.clip(IVORY_DARK[0] * (0.8 + 0.2 * spec), 0, 255))
                        g = int(np.clip(IVORY_DARK[1] * (0.8 + 0.2 * spec), 0, 255))
                        b = int(np.clip(IVORY_DARK[2] * (0.8 + 0.2 * spec), 0, 255))
                    else:
                        r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                else:
                    # Mint Green cold-rolled brass enamel
                    r = int(np.clip(MINT_BASE[0] * (0.75 + 0.45 * spec) + 50 * shine - 30 * edge_shade, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.75 + 0.45 * spec) + 50 * shine - 30 * edge_shade, 0, 255))
                    b = int(np.clip(MINT_BASE[2] * (0.75 + 0.45 * spec) + 50 * shine - 30 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r, g, b, 255))

    # Exposed brass structural rivets on flank seams
    for ry in [64, 72, 80, 88]:
        for rx in [50, 78]:
            ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=BRASS_LIGHT)
            ch_d.point((rx, ry), fill=WHITE_SHINE)

    # Chest Steam Pressure Gauge / Winding Dial at (64, 68)
    gx, gy = 64, 68
    ch_d.ellipse([gx - 6, gy - 6, gx + 6, gy + 6], fill=BRASS_DARK, outline=OUTLINE)
    ch_d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=GOLD_BASE)
    ch_d.ellipse([gx - 4, gy - 4, gx + 4, gy + 4], fill=CYAN_DEEP)
    ch_d.ellipse([gx - 3, gy - 3, gx + 3, gy + 3], fill=CYAN_BASE)
    # Dial indicator needle
    ch_d.line([(gx, gy), (gx + 2, gy - 3)], fill=WHITE_SHINE, width=1)
    ch_d.point((gx, gy), fill=BRASS_LIGHT)

    # 6. Left Arm & Suction Paw
    # Reaching out to left for wall-grip / balance: shoulder (50, 62) -> elbow (38, 70) -> paw (34, 76)
    arm_l_pts = [(50.0, 62.0), (40.0, 68.0), (34.0, 76.0)]
    for t in np.linspace(0.0, 1.0, 20):
        if t <= 0.5:
            ax = arm_l_pts[0][0] + (arm_l_pts[1][0] - arm_l_pts[0][0]) * (t * 2.0)
            ay = arm_l_pts[0][1] + (arm_l_pts[1][1] - arm_l_pts[0][1]) * (t * 2.0)
        else:
            ax = arm_l_pts[1][0] + (arm_l_pts[2][0] - arm_l_pts[1][0]) * ((t - 0.5) * 2.0)
            ay = arm_l_pts[1][1] + (arm_l_pts[2][1] - arm_l_pts[1][1]) * ((t - 0.5) * 2.0)
        for dx in range(-3, 4):
            spec = max(0.0, 1.0 - abs(dx) / 3.5)
            r = int(np.clip(MINT_BASE[0] * (0.8 + 0.35 * spec), 0, 255))
            g = int(np.clip(MINT_BASE[1] * (0.8 + 0.35 * spec), 0, 255))
            b = int(np.clip(MINT_BASE[2] * (0.8 + 0.35 * spec), 0, 255))
            chassis_img.putpixel((int(ax + dx), int(ay)), (r, g, b, 255))

    # Left paw with suction pad at (34, 76)
    ch_d.ellipse([31, 73, 37, 79], fill=MINT_BASE, outline=OUTLINE)
    ch_d.ellipse([32, 74, 36, 78], fill=CORAL_BASE)
    ch_d.point((34, 76), fill=WHITE_SHINE)

    # 7. Right Arm & Grip Mount
    # Brought across front of torso: shoulder (76, 62) -> elbow (82, 70) -> hand (80, 74)
    # STRICT 0-ART9/11: max x <= 86 so x >= 94 is 100% 0 pixels!
    arm_r_pts = [(76.0, 62.0), (83.0, 68.0), (80.0, 74.0)]
    for t in np.linspace(0.0, 1.0, 18):
        if t <= 0.5:
            ax = arm_r_pts[0][0] + (arm_r_pts[1][0] - arm_r_pts[0][0]) * (t * 2.0)
            ay = arm_r_pts[0][1] + (arm_r_pts[1][1] - arm_r_pts[0][1]) * (t * 2.0)
        else:
            ax = arm_r_pts[1][0] + (arm_r_pts[2][0] - arm_r_pts[1][0]) * ((t - 0.5) * 2.0)
            ay = arm_r_pts[1][1] + (arm_r_pts[2][1] - arm_r_pts[1][1]) * ((t - 0.5) * 2.0)
        for dx in range(-3, 4):
            px = int(ax + dx)
            if px < 90:  # Enforce strict boundary
                spec = max(0.0, 1.0 - abs(dx) / 3.5)
                r = int(np.clip(MINT_BASE[0] * (0.8 + 0.35 * spec), 0, 255))
                g = int(np.clip(MINT_BASE[1] * (0.8 + 0.35 * spec), 0, 255))
                b = int(np.clip(MINT_BASE[2] * (0.8 + 0.35 * spec), 0, 255))
                chassis_img.putpixel((px, int(ay)), (r, g, b, 255))

    # Right hand grip at (80, 74)
    ch_d.ellipse([77, 71, 83, 77], fill=BRASS_BASE, outline=OUTLINE)
    ch_d.point((80, 74), fill=WHITE_SHINE)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=80)

    # Explicit enforcement of 0-ART9 / 0-ART11: zero chassis pixels in weapon zone (x >= 94)
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr, "RGBA")
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_gecko_conduit_scout_crest_cowl.png
    # Features:
    # - 管網巡檢防刮護額 (Conduit Scout Crest Cowl)
    # - Streamlined aerodynamic brass hood & cowl with forward crest peak at (64, 26)
    # - Lateral ear exhaust louvers at (42, 42) and (86, 42)
    # - Forehead brass protective brow ridge at y: 35..38
    # - Cute rounded gecko muzzle & jaw at y: 46..56, ivory white with brass rim
    # - Upturned mouth corners with coral pink pressure relief ports (#FF5E8A) at (52, 52) and (76, 52)
    # - STRICT 0-ART27 MANDATORY: Eye socket zones (52, 40) and (76, 40) MUST BE HOLLOW (alpha=0)!
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0
    hrx, hry = 22.0, 16.0

    # 1. Main Cranial Dome & Snout
    for y in range(26, 58):
        for x in range(41, 87):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / (hrx * 1.1))
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / (hrx * 0.45))**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Lower snout / cheek plate (y >= 46, abs(x - 64) <= 15)
                is_snout = (y >= 46) and (abs(x - hcx) <= 15)
                if is_snout:
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.15 * spec) - 15 * edge_shade, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.15 * spec) - 15 * edge_shade, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.15 * spec) - 20 * edge_shade, 0, 255))
                else:
                    # Mint green cranial plate
                    r = int(np.clip(MINT_BASE[0] * (0.75 + 0.45 * spec) + 50 * shine - 25 * edge_shade, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.75 + 0.45 * spec) + 50 * shine - 25 * edge_shade, 0, 255))
                    b = int(np.clip(MINT_BASE[2] * (0.75 + 0.45 * spec) + 50 * shine - 25 * edge_shade, 0, 255))

                head_img.putpixel((x, y), (r, g, b, 255))

    # 2. Forward Crest Peak at (64, 26) & Protective Brow Ridge
    # Crest peak
    hd.polygon([(64, 23), (60, 28), (68, 28)], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((64, 24), fill=WHITE_SHINE)

    # Brow ridge bar across forehead (49..79, 34..37)
    for x in range(49, 80):
        spec = max(0.0, 1.0 - abs(x - 64) / 16.0)
        hd.line([(x, 34), (x, 36)], fill=(
            int(np.clip(BRASS_BASE[0] * (0.8 + 0.3 * spec), 0, 255)),
            int(np.clip(BRASS_BASE[1] * (0.8 + 0.3 * spec), 0, 255)),
            int(np.clip(BRASS_BASE[2] * (0.8 + 0.3 * spec), 0, 255)),
            255
        ))

    # 3. Lateral Ear Exhaust Louvers at (42, 42) and (86, 42)
    for ex, ey in [(42, 42), (86, 42)]:
        hd.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=BRASS_DARK, outline=OUTLINE)
        hd.ellipse([ex - 2, ey - 2, ex + 2, ey + 2], fill=GOLD_BASE)
        hd.point((ex, ey), fill=WHITE_SHINE)

    # 4. Cute Muzzle Smile & Coral Pink Pressure Relief Ports
    # Smile mouth curve at y: 52..54
    hd.arc([54, 50, 74, 56], start=20, end=160, fill=OUTLINE, width=1)
    # Coral Pink relief ports at (52, 52) and (76, 52)
    for cx, cy in [(52, 52), (76, 52)]:
        hd.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=CORAL_BASE, outline=OUTLINE)
        hd.point((cx, cy), fill=WHITE_SHINE)

    # Clean outline pass BEFORE hollowing eye sockets
    apply_clean_outline(head_img, ignore_regions=[(52, 40, 6), (76, 40, 6)])

    # 5. STRICT 0-ART27 COMPLIANCE: HOLLOW EYE SOCKETS
    # Left eye socket center at (52, 40), Right eye socket center at (76, 40)
    # Ensure radius 4.4 around both centers is STRICTLY 0 alpha!
    h_arr = np.array(head_img)
    for ey, ex in [(40, 52), (40, 76)]:
        for y in range(ey - 5, ey + 6):
            for x in range(ex - 5, ex + 6):
                if (x - ex)**2 + (y - ey)**2 <= 19:
                    h_arr[y, x, :] = 0
    head_img = Image.fromarray(h_arr, "RGBA")
    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_gecko_highpressure_stealth_harness.png
    # Features:
    # - 耐熱工裝暗忍胸甲與防刮短裙甲 (High-Pressure Stealth Harness & Tassets)
    # - Upper body: Crossed double brass straps over shoulders (y: 52..74)
    # - Center breastplate with warm gold buckles (#FFA010)
    # - Waist belt at y: 78..84 with central gear buckle
    # - Lower 3-piece guard tassets at y: 84..94
    # - STRICT 0-ART26b COMPLIANCE: y >= 96 MUST BE STRICTLY 0 PIXELS!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Shoulder Harness Straps
    # Left strap from (52, 50) to (62, 76)
    cos_d.line([(52, 50), (62, 76)], fill=BRASS_DARK, width=3)
    cos_d.line([(52, 50), (62, 76)], fill=GOLD_BASE, width=1)
    # Right strap from (76, 50) to (66, 76)
    cos_d.line([(76, 50), (66, 76)], fill=BRASS_DARK, width=3)
    cos_d.line([(76, 50), (66, 76)], fill=GOLD_BASE, width=1)

    # 2. Central Armor Plate & Pressure Bracket (x: 54..74, y: 64..78)
    for y in range(64, 79):
        hw = 9.0 + (78 - y) * 0.15
        for x in range(int(64 - hw), int(64 + hw + 1)):
            spec = max(0.0, 1.0 - abs(x - 64) / (hw + 1.0))
            r = int(np.clip(STEEL_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
            g = int(np.clip(STEEL_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
            b = int(np.clip(STEEL_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Cutout center for chest gauge visibility (leave gauge unobstructed)
    for cy in range(65, 72):
        for cx in range(61, 68):
            if (cx - 64)**2 + (cy - 68)**2 <= 14:
                costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    # Gold harness buckles at (56, 68) and (72, 68)
    for bx in [56, 72]:
        cos_d.ellipse([bx - 2, 67, bx + 2, 71], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.point((bx, 69), fill=WHITE_SHINE)

    # 3. Waist Belt at y: 78..84
    for y in range(78, 85):
        for x in range(50, 79):
            spec = max(0.0, 1.0 - abs(x - 64) / 15.0)
            r = int(np.clip(BRASS_DARK[0] * (0.85 + 0.3 * spec), 0, 255))
            g = int(np.clip(BRASS_DARK[1] * (0.85 + 0.3 * spec), 0, 255))
            b = int(np.clip(BRASS_DARK[2] * (0.85 + 0.3 * spec), 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Center Belt Gear Buckle at (64, 81)
    cos_d.ellipse([61, 78, 67, 84], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.point((64, 81), fill=WHITE_SHINE)

    # 4. Streamlined 3-piece Tassets at y: 84..94 (x: 50..78)
    # Left tasset: x: 50..58, y: 84..93
    # Center tasset: x: 60..68, y: 84..94
    # Right tasset: x: 70..78, y: 84..93
    tassets = [
        (50, 58, 84, 93),
        (60, 68, 84, 94),
        (70, 78, 84, 93)
    ]
    for x1, x2, y1, y2 in tassets:
        for y in range(y1, y2 + 1):
            for x in range(x1, x2 + 1):
                spec = max(0.0, 1.0 - abs(x - (x1 + x2) * 0.5) / 5.0)
                r = int(np.clip(STEEL_LIGHT[0] * (0.8 + 0.35 * spec), 0, 255))
                g = int(np.clip(STEEL_LIGHT[1] * (0.8 + 0.35 * spec), 0, 255))
                b = int(np.clip(STEEL_LIGHT[2] * (0.8 + 0.35 * spec), 0, 255))
                costume_img.putpixel((x, y), (r, g, b, 255))
        # Gold bottom trim on tassets
        cos_d.line([(x1, y2), (x2, y2)], fill=GOLD_BASE, width=1)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=80)

    # STRICT 0-ART26b ENFORCEMENT: y >= 96 MUST BE 0 PIXELS!
    cos_arr = np.array(costume_img)
    cos_arr[96:, :, :] = 0
    costume_img = Image.fromarray(cos_arr, "RGBA")
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_gecko_dual_slit_aperture_quartz_lens.png
    # Features:
    # - 雙目裂隙光圈石英目鏡 (Dual-Slit Aperture Quartz Lens)
    # - Dual convex golden quartz lenses centered at (52, 40) and (76, 40)
    # - Vertical dark slit aperture for iconic gecko slit pupil look
    # - Glowing cyan reticle tick marks (#38A0FF)
    # - Nose bridge highlight at (64, 46)
    # - Center alpha at (52, 40) and (76, 40) is 255 (0-ART27 compliant)
    # - Rich color depth >= 15 unique colors in optic zone (0-QA31 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    core_d = ImageDraw.Draw(core_img)

    eye_centers = [(52.0, 40.0), (76.0, 40.0)]
    for ecx, ecy in eye_centers:
        for y in range(int(ecy - 6), int(ecy + 7)):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= 4.8:
                    norm = dist / 4.8
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 4.0)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 1.8)**2

                    if norm >= 0.85:
                        # Golden brass bezel
                        r = int(np.clip(BRASS_DARK[0] * (0.8 + 0.3 * spec), 0, 255))
                        g = int(np.clip(BRASS_DARK[1] * (0.8 + 0.3 * spec), 0, 255))
                        b = int(np.clip(BRASS_DARK[2] * (0.8 + 0.3 * spec), 0, 255))
                    else:
                        # Quartz lens amber-gold depth
                        r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.45 * spec) + 50 * shine, 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.45 * spec) + 50 * shine, 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.45 * spec) + 60 * shine, 0, 255))

                    core_img.putpixel((x, y), (r, g, b, 255))

        # Vertical mechanical slit aperture (width 1.5, height 6)
        iex, iey = int(ecx), int(ecy)
        core_d.line([(iex, iey - 3), (iex, iey + 3)], fill=OUTLINE, width=1)
        core_d.point((iex, iey), fill=(15, 12, 28, 255))

        # Glowing cyan rangefinder reticle tick marks at top & bottom
        core_d.point((iex, iey - 4), fill=CYAN_LIGHT)
        core_d.point((iex, iey + 4), fill=CYAN_LIGHT)
        # Specular glint on upper-left quadrant
        core_d.point((iex - 2, iey - 2), fill=WHITE_SHINE)

    # Miniature nose bridge highlight at (64, 46)
    core_d.polygon([(63, 46), (65, 46), (64, 45)], fill=BRASS_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_gecko_conduit_ratchet_dart.png
    # Features:
    # - 黃銅棘輪多角機關鏢 (Brass Ratchet Polygon Conduit Shuriken)
    # - Handheld in right hand, centered at (82, 70)
    # - Four curved cold-rolled steel shuriken blades radiating at 45, 135, 225, 315 deg
    # - Center precision brass ratchet wheel (#FFA010 / #FFD028) with 8 teeth and cyan center gem (#38A0FF)
    # - Single-wielded, no overlap with left side, completely decoupled
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wcx, wcy = 82.0, 70.0

    # 1. Four Curved Shuriken Blades
    blade_angles = [np.pi / 4, 3 * np.pi / 4, 5 * np.pi / 4, 7 * np.pi / 4]
    blade_len = 14.0

    for ang in blade_angles:
        # Tip point
        tx = wcx + np.cos(ang) * blade_len
        ty = wcy + np.sin(ang) * blade_len

        # Base left & right points
        b1_x = wcx + np.cos(ang - 0.45) * 5.0
        b1_y = wcy + np.sin(ang - 0.45) * 5.0
        b2_x = wcx + np.cos(ang + 0.45) * 5.0
        b2_y = wcy + np.sin(ang + 0.45) * 5.0

        # Draw blade polygon
        wd.polygon([(b1_x, b1_y), (tx, ty), (b2_x, b2_y)], fill=STEEL_LIGHT, outline=OUTLINE)
        # Blade bevel highlight
        wd.line([(wcx, wcy), (tx, ty)], fill=STEEL_SHINE, width=1)
        # Golden tip notch
        tip_notch_x = wcx + np.cos(ang) * (blade_len - 3.0)
        tip_notch_y = wcy + np.sin(ang) * (blade_len - 3.0)
        wd.point((int(round(tip_notch_x)), int(round(tip_notch_y))), fill=GOLD_BASE)

    # 2. Central Brass Ratchet Wheel (radius ~6 px)
    for y in range(int(wcy - 7), int(wcy + 8)):
        for x in range(int(wcx - 7), int(wcx + 8)):
            d = ((x - wcx)**2 + (y - wcy)**2)**0.5
            if d <= 6.5:
                spec = max(0.0, 1.0 - d / 6.5)
                shine = max(0.0, 1.0 - ((x - (wcx - 1.5))**2 + (y - (wcy - 1.5))**2)**0.5 / 3.0)**2
                r = int(np.clip(BRASS_BASE[0] * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                g = int(np.clip(BRASS_BASE[1] * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                b = int(np.clip(BRASS_BASE[2] * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # 8 Ratchet cogs around the rim
    for i in range(8):
        c_ang = i * (2.0 * np.pi / 8.0)
        cx = int(round(wcx + np.cos(c_ang) * 6.5))
        cy = int(round(wcy + np.sin(c_ang) * 6.5))
        wd.point((cx, cy), fill=GOLD_SHINE)

    # 3. Center Glowing Cyan Gem & Precision Pivot
    wd.ellipse([int(wcx - 3), int(wcy - 3), int(wcx + 3), int(wcy + 3)], fill=CYAN_BASE, outline=OUTLINE)
    wd.ellipse([int(wcx - 2), int(wcy - 2), int(wcx + 2), int(wcy + 2)], fill=CYAN_LIGHT)
    wd.point((int(wcx - 1), int(wcy - 1)), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slice_data = [
        ("winding_key", "key_gecko_dual_ring_relief_valve_brass", key_img),
        ("back_curio", "curio_gecko_segmented_gear_balance_tail", curio_img),
        ("chassis", "chassis_gecko_brass_patina_default", chassis_img),
        ("head_unit", "head_gecko_conduit_scout_crest_cowl", head_img),
        ("costume", "costume_gecko_highpressure_stealth_harness", costume_img),
        ("optic_core", "face_gecko_dual_slit_aperture_quartz_lens", core_img),
        ("weapon", "weapon_gecko_conduit_ratchet_dart", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{GECKO_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_gecko_dual_ring_relief_valve_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_gecko_conduit_ratchet_dart.png")
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
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{GECKO_PD_DIR}/proof_paperdoll_gecko_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{GECKO_PD_DIR}/proof_paperdoll_gecko_magenta.png"
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

    strip_path = f"{GECKO_PD_DIR}/proof_gecko_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/gecko_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/gecko_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/gecko_idle.png
    p_idle_64 = f"{PLAYER_DIR}/gecko_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/gecko_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/gecko_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/gecko_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/gecko_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/gecko_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL CONDUIT GECKO CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
