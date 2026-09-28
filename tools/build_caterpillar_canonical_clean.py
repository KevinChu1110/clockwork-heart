#!/usr/bin/env python3
"""
build_caterpillar_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十族 風箱毛蟲 (The Bellows Caterpillar, caterpillar) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/BELLOWS_CATERPILLAR_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  segmented stamped brass rings & accordion bellows chassis, dual-row ratchet roller gear feet,
  ivory ceramic thermal shield, dual-sensor bellows cowl helmet, dual-ring bellows winding key,
  deepwood sapper cuirass, dual round amber condenser optic lenses,
  vine valley bellows compression hammer, segmented soft-steel pressure pack)
- references/art_direction.md & references/brand_assets.md:
  Dopamine + Bellows Sapper palette:
    1. Base: Ivory Ceramic Glaze / Polished Nickel (#FFFDF8, #E8ECF2, #CCD4E0)
    2. Primary 1: Dopamine Brass Gold (#FFD028, #D4A520, #FFF59D)
    3. Primary 2: Mint Emerald Green (#4ED86A, #78EB90, #2DA548)
    4. Metal: Deep Forest Green (#204028, #2A5234, #18301E)
    5. Secondary: Dawn Dopamine Warm Orange (#FFA010, #FFB84D)
    6. Accent: Dopamine Coral Pink (#FF5E8A, #FF2A6D, #FFA8C5)
    7. Dark Outline: Deep Blue-Purple (#1F1A3A)
    8. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_75f26312"
CATERPILLAR_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/caterpillar"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Bellows Caterpillar Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory Ceramic / Heat Insulation (#FFFDF8, #E8ECF2)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (232, 236, 242, 255)
IVORY_DARK   = (204, 212, 224, 255)

# 2. Dopamine Foundry Brass Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Mint Emerald Green (#4ED86A)
EMERALD_BASE  = (78, 216, 106, 255)
EMERALD_LIGHT = (120, 235, 145, 255)
EMERALD_SHINE = (175, 248, 190, 255)
EMERALD_DARK  = (45, 165, 75, 255)
EMERALD_DEEP  = (28, 115, 50, 255)

# 4. Deep Forest Green / Accordion Leather (#204028)
FOREST_LIGHT = (52, 98, 64, 255)
FOREST_MID   = (40, 78, 48, 255)
FOREST_BASE  = (32, 64, 40, 255)
FOREST_DARK  = (24, 48, 30, 255)
FOREST_DEEP  = (16, 34, 20, 255)

# 5. Dawn Dopamine Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 6. Dopamine Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 195, 215, 255)
CORAL_DARK  = (210, 45, 95, 255)

# 7. Amber Optic Crystal (#FFB020)
AMBER_BASE  = (255, 176, 32, 255)
AMBER_LIGHT = (255, 215, 90, 255)
AMBER_SHINE = (255, 245, 180, 255)
AMBER_DARK  = (215, 120, 10, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL BELLOWS CATERPILLAR SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_caterpillar_dual_ring_bellows_key.png
    # Features:
    # - 雙環重裝風箱發條鑰匙 (Dual-Ring Bellows Heavy Winding Key)
    # - Robust forged brass central shaft extending from (64, 56) to (64, 25)
    # - Symmetrical dual concentric circular ring loops at left (48, 25) and right (80, 25)
    # - Inner ventilation hollow circular cutouts in each ring (rad 5.5)
    # - Central escapement hub at (64, 25) with coral pink rivet (#FF5E8A)
    # - Warm golden bronze outline (OUTLINE_KEY) compliant with 0-ART29 (< 260px dark, run < 13)
    # - 4 corners strictly transparent (alpha = 0)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    hub_x, hub_y = 64.0, 25.0

    # 1. Key Shaft with Machined Flanges from (64, 56) to (64, 25)
    for t in np.linspace(0.0, 1.0, 32):
        sy = 56.0 + (hub_y - 56.0) * t
        is_collar = (abs(t - 0.35) < 0.06) or (abs(t - 0.75) < 0.06)
        half_w = 3.0 if is_collar else 2.0

        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            px = int(round(hub_x + offset))
            py = int(round(sy))
            shade = 1.0 - abs(offset) / (half_w + 0.5)
            if is_collar:
                r = int(np.clip(GOLD_LIGHT[0] * (0.85 + 0.25 * shade), 0, 255))
                g = int(np.clip(GOLD_LIGHT[1] * (0.85 + 0.25 * shade), 0, 255))
                b = int(np.clip(GOLD_LIGHT[2] * (0.85 + 0.25 * shade), 0, 255))
            else:
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine socket mount boss at (64, 56)
    kd.ellipse([60, 52, 68, 60], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([62, 54, 66, 58], fill=GOLD_BASE)

    # 2. Dual Concentric Ring Loops: Left at (48, 25), Right at (80, 25)
    ring_radius = 12.0
    inner_rad = 5.5
    loop_centers = [(48.0, 25.0), (80.0, 25.0)]

    for cx, cy in loop_centers:
        for dy in range(int(-ring_radius - 1), int(ring_radius + 2)):
            for dx in range(int(-ring_radius - 1), int(ring_radius + 2)):
                d = (dx**2 + dy**2)**0.5
                if d <= ring_radius:
                    px = int(round(cx + dx))
                    py = int(round(cy + dy))
                    if 0 <= px < W and 0 <= py < H:
                        spec = max(0.0, 1.0 - abs(d - 8.5) / 4.0)
                        shine = max(0.0, 1.0 - abs(dx + 2) / 3.0)**2 if dy < 0 else 0.0
                        r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                        key_img.putpixel((px, py), (r, g, b, 255))

    # Hollow cutouts in each ring
    k_px = key_img.load()
    for cx, cy in loop_centers:
        for dy in range(int(-inner_rad - 1), int(inner_rad + 2)):
            for dx in range(int(-inner_rad - 1), int(inner_rad + 2)):
                if (dx**2 + dy**2)**0.5 <= inner_rad:
                    px = int(round(cx + dx))
                    py = int(round(cy + dy))
                    if 0 <= px < W and 0 <= py < H:
                        k_px[px, py] = (0, 0, 0, 0)

    # 3. Horizontal Sturdy Crossbar connecting the rings through the hub
    kd.rectangle([48, 23, 80, 27], fill=GOLD_BASE)
    kd.line([(48, 24), (80, 24)], fill=GOLD_LIGHT, width=1)
    kd.line([(48, 26), (80, 26)], fill=GOLD_DARK, width=1)

    # 4. Central Escapement Hub & Coral Pink Rivet
    kd.ellipse([int(hub_x - 7), int(hub_y - 7), int(hub_x + 7), int(hub_y + 7)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 5), int(hub_y - 5), int(hub_x + 5), int(hub_y + 5)], fill=GOLD_BASE)
    # Coral pink center rivet (#FF5E8A)
    kd.ellipse([int(hub_x - 3), int(hub_y - 3), int(hub_x + 3), int(hub_y + 3)], fill=CORAL_BASE, outline=OUTLINE_KEY)
    kd.point((int(hub_x), int(hub_y - 1)), fill=CORAL_LIGHT)
    kd.point((int(hub_x), int(hub_y)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)

    # Re-clear 4 corners strictly (0-ART29)
    for cy in range(3):
        for cx in range(3):
            k_px[cx, cy] = (0, 0, 0, 0)
            k_px[W - 1 - cx, cy] = (0, 0, 0, 0)
            k_px[cx, H - 1 - cy] = (0, 0, 0, 0)
            k_px[W - 1 - cx, H - 1 - cy] = (0, 0, 0, 0)

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_caterpillar_segmented_pressure_pack.png
    # Features:
    # - 分節軟鋼風箱蓄壓氣包 (Segmented Bellows Pressure-Reservoir Pack)
    # - 3-stage telescopic soft-steel and brass pressure pack at back-left (x: 38..60, y: 52..86)
    # - Golden metal protective lattice mesh (#FFD028 / #D4A520)
    # - Miniature orange dial pressure gauge at (45, 56) (#FFA010)
    # - Brass flexible exhaust tube looping down from (48, 80) to (44, 92)
    # - Clear central channel for winding key insertion (x: 61..67 is kept clear)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Three Cylindrical Pressure Pack Stages (x: 38..59, y: 54..82)
    stages = [
        (54, 63, 10.0, GOLD_BASE, GOLD_DARK),
        (63, 73, 9.5, EMERALD_BASE, FOREST_BASE),
        (73, 82, 9.0, GOLD_BASE, GOLD_DARK)
    ]
    for y0, y1, half_w, col_base, col_dark in stages:
        cx = 48.0
        for y in range(y0, y1 + 1):
            for x in range(int(cx - half_w), int(cx + half_w + 1)):
                if x >= 60:  # strictly preserve central winding key channel
                    continue
                spec = max(0.0, 1.0 - abs(x - cx) / (half_w + 0.1))
                shine = max(0.0, 1.0 - abs(x - (cx - 2.5)) / 3.0)**2
                r = int(np.clip(col_base[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(col_base[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(col_base[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

        # Horizontal reinforcing collar ring at junction
        cd.rectangle([int(cx - half_w - 1), y1 - 1, min(59, int(cx + half_w + 1)), y1 + 1], fill=GOLD_LIGHT, outline=OUTLINE)

    # 2. Golden Wire Mesh Lattice Texturing
    for y in range(55, 81, 4):
        for x in range(39, 58, 4):
            cd.point((x, y), fill=GOLD_SHINE)
            cd.point((x + 2, y + 2), fill=GOLD_DARK)

    # 3. Miniature Dial Pressure Gauge at (45, 56)
    cd.ellipse([41, 52, 49, 60], fill=GOLD_DARK, outline=OUTLINE)
    cd.ellipse([42, 53, 48, 59], fill=ORANGE_BASE)
    cd.line([(45, 56), (47, 54)], fill=WHITE_SHINE, width=1)
    cd.point((45, 56), fill=CORAL_BASE)

    # 4. Brass Flexible Exhaust Pipe looping from (48, 81) to (43, 92)
    pipe_pts = [
        (48.0, 81.0), (49.0, 85.0), (47.0, 89.0), (43.0, 92.0)
    ]
    for i in range(len(pipe_pts) - 1):
        p0, p1 = pipe_pts[i], pipe_pts[i + 1]
        for t in np.linspace(0.0, 1.0, 10):
            px = int(round(p0[0] + t * (p1[0] - p0[0])))
            py = int(round(p0[1] + t * (p1[1] - p0[1])))
            cd.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD_BASE, outline=OUTLINE)
            cd.point((px, py), fill=GOLD_LIGHT)

    # Exhaust nozzle tip at (43, 92)
    cd.ellipse([41, 90, 45, 94], fill=GOLD_DARK, outline=OUTLINE)
    cd.point((43, 92), fill=ORANGE_BASE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_caterpillar_brass_bellows_default.png
    # Features:
    # - 多節沖壓銅環風箱底盤 (Segmented Brass-Ring Accordion Bellows Chassis)
    # - 2.2 chibi ratio, stout low-center-of-gravity sapper stance
    # - Dual-row ratchet roller gear feet (left tread x: 38..56, right tread x: 68..86) along y: 112..116
    # - Torso: 6 tiers of concentric stamped brass rings (#FFD028) & forest green bellows (#204028)
    # - Belly: Ivory ceramic heat shield (#FFFDF8 / #E8ECF2) at center (x: 52..76, y: 66..88)
    # - Left arm forward in sapper guard at (36..48, 68..78)
    # - Right arm at (80..92, 68..76) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # - Plate color distance L2 < 60.0 with head_unit (0-ART28q)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Dual-Row Ratchet Roller Gear Feet (4 pairs along base at y: 110..116)
    # Left track rollers at x: 38, 45, 52, 59
    # Right track rollers at x: 67, 74, 81, 88
    track_rollers = [38, 45, 52, 59, 67, 74, 81, 88]
    for rx in track_rollers:
        ry = 113
        # Gear wheel outer disc
        ch_d.ellipse([rx - 4, ry - 3, rx + 4, ry + 3], fill=GOLD_DARK, outline=OUTLINE)
        ch_d.ellipse([rx - 3, ry - 2, rx + 3, ry + 2], fill=GOLD_BASE)
        # Gear teeth / ratchet cleats
        ch_d.point((rx - 3, ry - 2), fill=GOLD_SHINE)
        ch_d.point((rx + 3, ry + 2), fill=GOLD_DARK)
        ch_d.point((rx, ry), fill=FOREST_BASE)

    # Continuous brass track guard rail connecting the rollers
    ch_d.rectangle([34, 106, 62, 111], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.line([(35, 107), (61, 107)], fill=GOLD_LIGHT, width=1)
    ch_d.rectangle([64, 106, 91, 111], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.line([(65, 107), (90, 107)], fill=GOLD_LIGHT, width=1)

    # 3. Upper Chest Flange & Neck Joint (x: 46..82, y: 44..59)
    for ny in range(44, 60):
        for nx in range(46, 83):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 18.0)
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # Lower chassis backing frame (connecting torso to track guard rail solidly)
    for ty in range(86, 108):
        for tx in range(40, 88):
            dx = (tx - 64.0) / 22.0
            dy = (ty - 96.0) / 13.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # 4. Main Stout Torso with 6 Accordion Bellows Segments (x: 42..86, y: 58..102)
    # Segments y-spans:
    # Seg 1: 58..64 (Brass Ring)
    # Seg 2: 65..71 (Forest Leather Bellows with Emerald tint)
    # Seg 3: 72..78 (Brass Ring)
    # Seg 4: 79..85 (Forest Leather Bellows with Emerald tint)
    # Seg 5: 86..92 (Brass Ring)
    # Seg 6: 93..102 (Lower Brass Bellows Skirting)
    for ty in range(58, 103):
        seg_idx = int((ty - 58) / 7.2)
        is_brass_ring = (seg_idx % 2 == 0)
        for tx in range(42, 87):
            dx = (tx - 64.0) / 20.5
            dy = (ty - 78.0) / 22.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 70.0)**2)**0.5 / 12.0)**2
                is_belly_ceramic = (52 <= tx <= 76 and 66 <= ty <= 88)

                if is_belly_ceramic:
                    # Ivory ceramic thermal shield tile (#FFFDF8) with smooth gradients
                    r = int(np.clip(238 * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
                    g = int(np.clip(234 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                    b = int(np.clip(226 * (0.85 + 0.25 * spec) + 20 * shine, 0, 242))
                elif is_brass_ring:
                    # Stamped Brass Ring Plates (#FFD028)
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                else:
                    # Dark Forest Green Accordion Leather Bellows (#204028)
                    r = int(np.clip(FOREST_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(FOREST_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(FOREST_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Brass Rivets along each ring rim
    for ry in [60, 67, 74, 81, 88, 95]:
        for rx in [46, 82]:
            ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_LIGHT, outline=OUTLINE)

    # Sapper Dial / Pressure relief port on belly at (64, 76)
    ch_d.ellipse([59, 71, 69, 81], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([60, 72, 68, 80], fill=EMERALD_BASE)
    ch_d.ellipse([62, 74, 66, 78], fill=GOLD_BASE)
    ch_d.point((64, 76), fill=ORANGE_BASE)
    ch_d.point((63, 75), fill=WHITE_SHINE)

    # 5. Left Arm in forward sapper guarding posture at (36..48, 68..80)
    for t in np.linspace(0.0, 1.0, 18):
        ax = 52.0 - t * 12.0
        ay = 66.0 + t * 8.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), GOLD_BASE)
    ch_d.ellipse([36, 72, 46, 80], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([38, 74, 44, 78], fill=EMERALD_BASE)
    ch_d.point((41, 76), fill=GOLD_LIGHT)

    # 6. Right Arm positioned at (78..88, 68..76) (strictly x < 94)
    for t in np.linspace(0.0, 1.0, 16):
        ax = 78.0 + t * 9.0  # max ax = 87
        ay = 66.0 + t * 6.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px = int(ax + dx)
                py = int(ay + dy)
                if px < 94 and dx**2 + dy**2 <= 9:
                    chassis_img.putpixel((px, py), GOLD_BASE)
    # Right brass wrist / ball joint
    ch_d.ellipse([84, 71, 91, 78], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.point((87, 74), fill=GOLD_LIGHT)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART9/11 enforcement: Zero pixels at x >= 94
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_caterpillar_sensor_bellows_cowl.png
    # Features:
    # - 雙探針風箱護額頭盔 (Dual-Sensor Bellows Brow Cowl Helmet)
    # - Stamped brass hemispherical cowl shell (#FFD028)
    # - Stamped protective brow visor plate at y: 26..36, x: 44..84
    # - Dual spiral spring feeler sensor antennas reaching up to y: 14 with brass beads at tips
    # - Dual coral pink cheek ventilation ports at (44, 50) and (84, 50) (#FF5E8A)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Base Arched Helmet Cowl Shell (x: 42..86, y: 34..57)
    for y in range(34, 58):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - 45.0) / 11.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 21.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 7.0)**2
                # Rich brass tone to maintain 0-ART28q color distance with chassis
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Dual Coral Pink Cheek Vent Ports at (44, 50) and (84, 50)
    for cx in (44, 84):
        hd.ellipse([cx - 2, 50 - 2, cx + 2, 50 + 2], fill=CORAL_BASE, outline=OUTLINE)
        hd.point((cx, 50), fill=GOLD_LIGHT)

    # 2. Dual Spiral Spring Feeler Sensor Antennas reaching up to (40, 14) and (88, 14)
    # Left antenna
    left_antenna_pts = [(52, 30), (48, 24), (44, 18), (40, 14)]
    for i in range(len(left_antenna_pts) - 1):
        p0, p1 = left_antenna_pts[i], left_antenna_pts[i + 1]
        for t in np.linspace(0.0, 1.0, 12):
            px = int(round(p0[0] + t * (p1[0] - p0[0])))
            py = int(round(p0[1] + t * (p1[1] - p0[1])))
            hd.ellipse([px - 1, py - 1, px + 1, py + 1], fill=GOLD_BASE)
    # Left antenna tip bead
    hd.ellipse([38, 12, 42, 16], fill=GOLD_LIGHT, outline=OUTLINE)
    hd.point((40, 13), fill=WHITE_SHINE)

    # Right antenna
    right_antenna_pts = [(76, 30), (80, 24), (84, 18), (88, 14)]
    for i in range(len(right_antenna_pts) - 1):
        p0, p1 = right_antenna_pts[i], right_antenna_pts[i + 1]
        for t in np.linspace(0.0, 1.0, 12):
            px = int(round(p0[0] + t * (p1[0] - p0[0])))
            py = int(round(p0[1] + t * (p1[1] - p0[1])))
            hd.ellipse([px - 1, py - 1, px + 1, py + 1], fill=GOLD_BASE)
    # Right antenna tip bead
    hd.ellipse([86, 12, 90, 16], fill=GOLD_LIGHT, outline=OUTLINE)
    hd.point((88, 13), fill=WHITE_SHINE)

    # 3. Stamped Golden Brow Visor (x: 44..84, y: 26..36)
    for y in range(26, 37):
        hw = 12.0 + (y - 26.0) * 0.8
        for x in range(int(hcx - hw), int(hcx + hw + 1)):
            spec = max(0.0, 1.0 - abs(x - hcx) / (hw + 0.1))
            shine = max(0.0, 1.0 - abs(x - (hcx - 2)) / 5.0)**2
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 15 * shine, 0, 255))
            head_img.putpixel((x, y), (r, g, b, 255))
    hd.line([(int(hcx - 18), 36), (int(hcx + 18), 36)], fill=EMERALD_BASE, width=1)

    # 4. Hollow Eye Sockets for 0-ART27:
    # Clear eye sockets centered at (54, 42) and (74, 42), radius 3.5px
    h_px = head_img.load()
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    # Outline pass ignoring eye sockets
    ignore_eyes = [(50, 38, 58, 46), (70, 38, 78, 46)]
    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=100, ignore_regions=ignore_eyes)

    # Re-enforce strictly hollow eye sockets after outline pass
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_caterpillar_deepwood_sapper_cuirass.png
    # Features:
    # - 蔓谷深林工兵板甲 (Deepwood Sapper Cuirass)
    # - Heavy deep forest green chest cuirass plate (#204028)
    # - Dopamine brass gold protective corner brackets (#FFD028)
    # - Warm orange safety warning straps / buckles (#FFA010)
    # - Miniature sapper gear emblem in center chest at (64, 72)
    # - Pauldrons on shoulders at (42, 60) and (86, 60)
    # - Belt and buckle ending strictly at y: 92
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Chest Cuirass (x: 46..82, y: 60..86)
    for y in range(60, 87):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            # Orange safety hazard chevron striping on chestplate trim
            is_orange_chevron = (64 <= y <= 66 and (x + y) % 6 < 3)
            if is_orange_chevron:
                r = int(np.clip(ORANGE_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(ORANGE_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(ORANGE_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(FOREST_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(FOREST_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(FOREST_BASE[2] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Center Embossed Brass Sapper Gear Totem at (64, 72)
    cos_d.ellipse([60, 68, 68, 76], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([62, 70, 66, 74], fill=FOREST_BASE)
    cos_d.point((64, 72), fill=GOLD_LIGHT)

    # 2. Heavy Double-Stamped Curved Pauldrons at (42, 60) and (86, 60)
    for px, py in [(42.0, 60.0), (86.0, 60.0)]:
        cos_d.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=GOLD_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=EMERALD_BASE)
        cos_d.point((int(px), int(py)), fill=GOLD_LIGHT)

    # 3. Waist Heavy Plate Belt & Buckle hanging from y: 86 down to y: 92
    waist_spans = [(48, 55), (57, 63), (65, 71), (73, 80)]
    for x0, x1 in waist_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=FOREST_DARK, outline=OUTLINE)
        cos_d.line([(x0 + 1, 88), (x1 - 1, 88)], fill=GOLD_BASE, width=1)
        cos_d.point((int(0.5 * (x0 + x1)), 90), fill=GOLD_LIGHT)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART26b enforcement: Zero pixels at y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_caterpillar_amber_condenser_lens.png
    # Features:
    # - 雙圓琥珀聚光透鏡 (Amber Condenser Quartz Optic Lens)
    # - Convex quartz crystal lenses centered at (54, 42) and (74, 42)
    # - Brass retention bezels with vernier gear teeth
    # - Dopamine warm orange (#FFA010) & amber glow with concentric reticles
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:
        # Outer Brass Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Amber Condenser Quartz)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r = int(np.clip(AMBER_BASE[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(AMBER_BASE[1] * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    b = int(np.clip(AMBER_BASE[2] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Concentric dial crosshair & focus highlight
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), AMBER_SHINE)
        core_img.putpixel((int(ex + 1), int(ey)), AMBER_LIGHT)
        core_img.putpixel((int(ex), int(ey - 1)), AMBER_LIGHT)
        core_img.putpixel((int(ex), int(ey + 1)), AMBER_DARK)

    # Vernier micro gear teeth on bezel
    c_d.point((49, 41), fill=GOLD_LIGHT)
    c_d.point((79, 41), fill=GOLD_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    # 0-ART27 verification: Ensure center pixels at (54, 42) and (74, 42) are completely opaque
    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_caterpillar_vine_valley_compression_hammer.png
    # Features:
    # - 蔓谷風箱重壓鎚 (Vine Valley Bellows Compression Hammer)
    # - Forged anvil hammer head with internal compression cylinder at x: 76..98, y: 22..46
    # - Embedded warm orange pneumatic compression bellows cylinder (#FFA010) with cooling vents
    # - Thick brass handle shaft extending down to y: 88 (x: 85..89)
    # - Heavy shock-absorbing sapper grip wrapping
    # - Spherical brass counterweight pommel at (87, 91)
    # - Complies strictly with review.md 0-MKT7 single-weapon standard
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Main Anvil Hammer Head (x: 76..98, y: 22..46)
    hammer_poly = [
        (76, 26), (82, 22), (92, 22), (98, 26),
        (98, 42), (92, 46), (82, 46), (76, 42)
    ]
    wd.polygon(hammer_poly, fill=FOREST_BASE, outline=OUTLINE)

    # Hammer bevel and shading
    for y in range(23, 46):
        for x in range(77, 98):
            dx = (x - 87.0) / 10.0
            dy = (y - 34.0) / 11.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                shine = max(0.0, 1.0 - abs(x - 84.0) / 4.0)**2 if y < 32 else 0.0
                is_bellows_cylinder = (83 <= x <= 91 and 27 <= y <= 41)
                if is_bellows_cylinder:
                    # Orange pneumatic compression cylinder (#FFA010) with vent grilles
                    is_grille = (y % 3 == 0)
                    col = GOLD_LIGHT if is_grille else ORANGE_BASE
                    r = int(np.clip(col[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(col[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(col[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                else:
                    r = int(np.clip(FOREST_BASE[0] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(FOREST_BASE[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(FOREST_BASE[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Hammer strike face trim
    wd.line([(77, 26), (77, 42)], fill=GOLD_BASE, width=1)
    wd.line([(97, 26), (97, 42)], fill=GOLD_BASE, width=1)

    # 2. Heavy Brass Handle Shaft (x: 85..89, y: 46..88)
    for y in range(46, 89):
        is_wrap = (y % 4 == 0 or y % 4 == 1)
        c = GOLD_BASE if is_wrap else (140, 94, 40, 255)
        for x in range(85, 90):
            spec = max(0.0, 1.0 - abs(x - 87.0) / 2.5)
            r = int(np.clip(c[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(c[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(c[2] * (0.85 + 0.25 * spec), 0, 255))
            weapon_img.putpixel((x, y), (r, g, b, 255))
    wd.rectangle([85, 46, 89, 88], outline=OUTLINE)

    # 3. Spherical Brass Counterweight Pommel at (87, 91)
    wd.ellipse([84, 89, 90, 95], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([85, 90, 89, 94], fill=GOLD_LIGHT)
    wd.point((87, 91), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_caterpillar_dual_ring_bellows_key", key_img),
        ("back_curio", "curio_caterpillar_segmented_pressure_pack", curio_img),
        ("chassis", "chassis_caterpillar_brass_bellows_default", chassis_img),
        ("head_unit", "head_caterpillar_sensor_bellows_cowl", head_img),
        ("costume", "costume_caterpillar_deepwood_sapper_cuirass", costume_img),
        ("optic_core", "face_caterpillar_amber_condenser_lens", core_img),
        ("weapon", "weapon_caterpillar_vine_valley_compression_hammer", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{CATERPILLAR_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{CATERPILLAR_PD_DIR}/winding_key/key_caterpillar_dual_ring_bellows_key.png",
                 f"{KEY_DIR}/key_caterpillar_dual_ring_bellows_key.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{CATERPILLAR_PD_DIR}/weapon/weapon_caterpillar_vine_valley_compression_hammer.png",
                 f"{WEAPON_DIR}/weapon_caterpillar_vine_valley_compression_hammer.png")

    # ─────────────────────────────────────────────────────────────
    # COMPOSITE CHARACTER & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # Ordering: winding_key -> back_curio -> chassis -> head_unit -> costume -> optic_core -> weapon
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{CATERPILLAR_PD_DIR}/proof_paperdoll_caterpillar_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{CATERPILLAR_PD_DIR}/proof_paperdoll_caterpillar_magenta.png"
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

    strip_path = f"{CATERPILLAR_PD_DIR}/proof_caterpillar_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/caterpillar_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/caterpillar_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/caterpillar_idle.png
    p_idle_64 = f"{PLAYER_DIR}/caterpillar_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/caterpillar_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/caterpillar_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/caterpillar_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/caterpillar_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/caterpillar_idle_hd.png)
    os.makedirs(SHOWCASE_DIR, exist_ok=True)
    comp_bbox = composite.getbbox()
    if comp_bbox:
        char_crop = idle_with_shadow.crop(comp_bbox)
        target_h = 920
        aspect = char_crop.width / char_crop.height
        sc_w = int(target_h * aspect)
        sc_h = target_h
        scaled_showcase = char_crop.resize((sc_w, sc_h), Image.Resampling.LANCZOS)

        showcase_hd = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_paste_x = (800 - sc_w) // 2
        sc_paste_y = 1120 - sc_h

        sc_shadow = Image.new("RGBA", (800, 1200), (0, 0, 0, 0))
        sc_sdraw = ImageDraw.Draw(sc_shadow)
        sc_sdraw.ellipse((400 - 220, 1120 - 22, 400 + 220, 1120 + 22), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{SHOWCASE_DIR}/caterpillar_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL BELLOWS CATERPILLAR CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
