#!/usr/bin/env python3
"""
build_salamander_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第二十六族 熔火蜥蜴 (The Magma Salamander, salamander) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/MAGMA_SALAMANDER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped obsidian tungsten plates,
  ivory enamel cheek/jaw plates, twin folding radiator crest fins, vulcanized silicone crawler boots with claw grips,
  four-vane heat-sink forging winding key, 5-segment articulated damping tail, foundry stamping sledgehammer weapon)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Obsidian Tungsten (#2A2B32)
    2. Secondary Trim: Magma Warm Gold (#D47A2A)
    3. Faceplate Enamel: Ivory White (#FFFDF8)
    4. Accent & Key: Dopamine Gold (#FFD028)
    5. Optic Core & Energy: Amber Crystal (#FFA010)
    6. Tungsten Frame & Boots: Cold-Rolled Tungsten Steel (#4A5568)
    7. Costume Straps & Seals: Coral Pink (#FF5E8A)
    8. Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
SALAMANDER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/salamander"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Magma Salamander Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 85, 25, 255)       # Warm magma bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Obsidian Tungsten (#2A2B32)
TUNGSTEN_BASE  = (42, 43, 50, 255)
TUNGSTEN_LIGHT = (72, 74, 86, 255)
TUNGSTEN_SHINE = (112, 116, 134, 255)
TUNGSTEN_DARK  = (28, 29, 36, 255)
TUNGSTEN_DEEP  = (18, 19, 24, 255)

# 2. Secondary Trim: Magma Warm Gold (#D47A2A)
MAGMA_BASE  = (212, 122, 42, 255)
MAGMA_LIGHT = (245, 155, 65, 255)
MAGMA_SHINE = (255, 195, 120, 255)
MAGMA_DARK  = (160, 85, 25, 255)
MAGMA_DEEP  = (110, 55, 15, 255)

# 3. Faceplate & Chest Enamel: Ivory White (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (230, 224, 215, 255)
IVORY_DARK    = (195, 188, 178, 255)

# 4. Accent: Dopamine Golden Brass & Winding Key (#FFD028 / #D4A017)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 5. Detail: Amber Optic Crystal & Geothermal Core (#FFA010)
AMBER_BASE  = (255, 160, 16, 255)
AMBER_LIGHT = (255, 195, 75, 255)
AMBER_SHINE = (255, 235, 160, 255)
AMBER_DARK  = (190, 105, 8, 255)
AMBER_DEEP  = (130, 68, 5, 255)

# 6. Cold-Rolled Tungsten Steel Frame & Boots (#4A5568)
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (118, 132, 155, 255)
STEEL_SHINE = (175, 188, 210, 255)
STEEL_DARK  = (48, 56, 70, 255)

# 7. Highlight: Coral Pink High-Pressure Seals & Buckles (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 150, 180, 255)
CORAL_DARK  = (190, 45, 85, 255)

# Fireproof Leather Apron (Costume)
APRON_BASE  = (92, 54, 32, 255)
APRON_LIGHT = (130, 78, 46, 255)
APRON_DARK  = (60, 34, 18, 255)

# Vulcanized Industrial Black Silicone Boots (#202026)
SILICONE_BASE  = (32, 32, 38, 255)
SILICONE_LIGHT = (65, 65, 78, 255)

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
    points_to_outline = set()

    for y in range(h):
        for x in range(w):
            p = px_snap[x, y]
            if isinstance(p, tuple) and len(p) >= 4 and p[3] >= min_alpha:
                for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                    if 0 <= nx < w and 0 <= ny < h:
                        np_px = px_snap[nx, ny]
                        if isinstance(np_px, tuple) and len(np_px) >= 4 and np_px[3] == 0:
                            if ignore_regions:
                                in_ignored = False
                                for ig_x, ig_y, ig_r in ignore_regions:
                                    if (nx - ig_x)**2 + (ny - ig_y)**2 <= ig_r**2:
                                        in_ignored = True
                                        break
                                if in_ignored:
                                    continue
                            points_to_outline.add((nx, ny))

    for px, py in points_to_outline:
        img.putpixel((px, py), outline_color)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL MAGMA SALAMANDER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_salamander_four_vane_heatsink.png
    # Four-Vane Heat-Sink Forging Key (四葉散熱鍛造發條鑰匙)
    # Socket boss at upper spine (64, 60), shaft extends diagonally up-right to (86, 26)
    # Features:
    # - Polished alloy/brass shaft with bevel shading
    # - Four-vane wheel with outer radiator heat-sink louvers (#FFD028 / #D47A2A)
    # - Central forged rivet with amber thermal pivot (#FFA010)
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 60) to (86, 26)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 22.0
        sy = 60.0 - t * 34.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (64, 60)
    kd.ellipse([60, 56, 68, 64], fill=MAGMA_DARK, outline=OUTLINE_KEY)
    kd.ellipse([61, 57, 67, 63], fill=MAGMA_BASE)
    kd.ellipse([63, 59, 65, 61], fill=AMBER_BASE)

    # 2. Key Hub at (86, 26) with Four-Vane Radiator Head
    kcx, kcy = 86.0, 26.0

    # Draw outer ring connecting vanes
    r_outer = 13.0
    r_inner = 8.5
    for y in range(int(kcy - r_outer - 2), int(kcy + r_outer + 3)):
        for x in range(int(kcx - r_outer - 2), int(kcx + r_outer + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if r_inner <= dist <= r_outer:
                norm_r = (dist - r_inner) / (r_outer - r_inner)
                spec = max(0.0, np.sin(norm_r * np.pi))
                shine = max(0.0, 1.0 - ((x - (kcx - 3.0))**2 + (y - (kcy - 3.0))**2)**0.5 / 6.0)**2
                r_w = int(np.clip(212 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                g_w = int(np.clip(122 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                b_w = int(np.clip(42 * (0.8 + 0.5 * spec) + 60 * shine, 0, 255))
                key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Four Vanes at 0, 90, 180, 270 degrees from center
    vane_offsets = [
        (0.0, -11.0, 4.0, 6.0),   # North
        (0.0, 11.0, 4.0, 6.0),    # South
        (-11.0, 0.0, 6.0, 4.0),   # West
        (11.0, 0.0, 6.0, 4.0),    # East
    ]
    for vx, vy, rx, ry in vane_offsets:
        vcx = kcx + vx
        vcy = kcy + vy
        for y in range(int(vcy - ry - 1), int(vcy + ry + 2)):
            for x in range(int(vcx - rx - 1), int(vcx + rx + 2)):
                if ((x - vcx)/rx)**2 + ((y - vcy)/ry)**2 <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (vcx - 1.5))**2 + (y - (vcy - 1.5))**2)**0.5 / 5.0)
                    r_v = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                    g_v = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
                    b_v = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Radiator Louvers / Grille Slots on vanes
    for lx in range(int(kcx - 2), int(kcx + 3)):
        key_img.putpixel((lx, int(kcy - 12)), GOLD_LIGHT)
        key_img.putpixel((lx, int(kcy + 12)), GOLD_LIGHT)
    for ly in range(int(kcy - 2), int(kcy + 3)):
        key_img.putpixel((int(kcx - 12), ly), GOLD_LIGHT)
        key_img.putpixel((int(kcx + 12), ly), GOLD_LIGHT)

    # Central Core & Rivet at (86, 26)
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=MAGMA_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 4), int(kcy - 4), int(kcx + 4), int(kcy + 4)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=AMBER_BASE)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline to guarantee 0-ART29 compliance
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_salamander_segmented_damping_tail.png
    # 5-Segment Articulated Heavy Tungsten Damping Tail (五節重鋼同軸阻尼大尾巴)
    # Originates at sacrum (48, 92), sweeps down-left to touch ground at (18, 112):
    # (48, 92) -> (40, 97) -> (32, 102) -> (24, 107) -> (16, 112)
    # Features:
    # - 5 articulated segment hubs with concentric tungsten armor plates (#2A2B32)
    # - Magma warm gold bevel rings (#D47A2A) on segment junctions
    # - Central heat dissipation grooves & high-pressure graphite lubricant ports (#FFD028)
    # - Flat heavy anvil bumper tip at ground level for stable tripod support
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    tail_segments = [
        (48.0, 92.0, 7.0, 5.0),    # Seg 1: Sacral base
        (40.0, 97.0, 6.5, 4.5),    # Seg 2: Descending curve
        (32.0, 102.0, 6.0, 4.0),   # Seg 3: Mid segment
        (24.0, 107.0, 5.5, 3.5),   # Seg 4: Lower segment
        (16.0, 112.0, 5.0, 3.0),   # Seg 5: Ground anchor tip
    ]

    # Draw transmission cable / core spine between segments
    for i in range(len(tail_segments) - 1):
        (x0, y0, _, _), (x1, y1, _, _) = tail_segments[i], tail_segments[i+1]
        for t in np.linspace(0.0, 1.0, 20):
            bx = x0 + t * (x1 - x0)
            by = y0 + t * (y1 - y0)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx**2 + dy**2 <= 4:
                        curio_img.putpixel((int(bx + dx), int(by + dy)), MAGMA_BASE)

    # Draw each segment plate
    for seg_idx, (scx, scy, srx, sry) in enumerate(tail_segments):
        for y in range(int(scy - sry - 2), int(scy + sry + 3)):
            for x in range(int(scx - srx - 2), int(scx + srx + 3)):
                dx = (x - scx) / srx
                dy = (y - scy) / sry
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (scx - 2))**2 + (y - (scy - 2))**2)**0.5 / (srx * 1.2))
                    shine = max(0.0, 1.0 - ((x - (scx - 2))**2 + (y - (scy - 2))**2)**0.5 / (srx * 0.5))**2
                    edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                    # Outer gold trim
                    is_rim = dist_sq >= 0.75
                    if is_rim:
                        r_t = int(np.clip(212 * (0.8 + 0.3 * spec) + 35 * shine - 20 * edge_shade, 0, 255))
                        g_t = int(np.clip(122 * (0.8 + 0.3 * spec) + 35 * shine - 20 * edge_shade, 0, 255))
                        b_t = int(np.clip(42 * (0.8 + 0.4 * spec) + 40 * shine - 10 * edge_shade, 0, 255))
                    else:
                        # Obsidian tungsten main plate
                        r_t = int(np.clip(42 * (0.75 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                        g_t = int(np.clip(43 * (0.75 + 0.45 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                        b_t = int(np.clip(50 * (0.75 + 0.45 * spec) + 55 * shine - 15 * edge_shade, 0, 255))

                    curio_img.putpixel((x, y), (r_t, g_t, b_t, 255))

        # Lubrication bolt / pivot rivet in segment center
        cd.ellipse([int(scx - 2), int(scy - 2), int(scx + 2), int(scy + 2)], fill=GOLD_BASE, outline=OUTLINE)
        cd.point((int(scx - 1), int(scy - 1)), fill=WHITE_SHINE)

    # Segment 5 Tip: Heavy Tungsten Skid Plate at (16, 112)
    cd.rectangle([11, 110, 18, 114], fill=STEEL_BASE, outline=OUTLINE)
    cd.line([(12, 111), (17, 111)], fill=STEEL_LIGHT, width=1)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_salamander_magma_tungsten_default.png
    # Features:
    # - 2.2 Chibi low-center-of-gravity magma crawler chassis
    # - Soft ground contact shadow at (64, 116)
    # - Heavy tungsten claw boots with 3 grip teeth at (46, 113) and (72, 113)
    # - Thick articulated crawler legs with ball-and-socket joints (#4A5568 / #FF5E8A)
    # - Solid neck collar at (x: 54..74, y: 48..58) for seamless head seating
    # - Obsidian tungsten chassis hull (#2A2B32) with magma gold trim (#D47A2A)
    # - Ivory White (#FFFDF8) enamel belly & chest plate
    # - Three horizontal heat-sink ventilation louvers on belly
    # - Left hand clenched low at (40, 84)
    # - Right arm tucked at ribs with weapon grip joint at (82, 75)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 32, 116 - 4, 64 + 32, 116 + 5], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Heavy Tungsten Claw Boots with Front Grip Teeth
    boot_pos = [(46.0, 113.0), (72.0, 113.0)]
    for bx, by in boot_pos:
        ch_d.ellipse([int(bx - 8), int(by - 3), int(bx + 8), int(by + 3)], fill=SILICONE_BASE, outline=OUTLINE)
        ch_d.ellipse([int(bx - 6), int(by - 2), int(bx + 6), int(by + 2)], fill=STEEL_BASE)
        ch_d.ellipse([int(bx - 4), int(by - 1), int(bx + 4), int(by + 2)], fill=TUNGSTEN_LIGHT)
        # 3 Flat claw teeth
        for cdx in [-4, 0, 4]:
            ch_d.line([(int(bx + cdx), int(by + 2)), (int(bx + cdx), int(by + 4))], fill=STEEL_LIGHT, width=1)
        ch_d.point((int(bx), int(by)), fill=WHITE_SHINE)

    # 3. Thick Crawler Legs with Tungsten Armor & Coral Seals
    leg_paths = [
        ((46.0, 112.0), (52.0, 88.0)),
        ((72.0, 112.0), (68.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-5, 6):
                spec = max(0.0, 1.0 - abs(dx) / 5.0)
                r_l = int(np.clip(42 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                g_l = int(np.clip(43 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                b_l = int(np.clip(50 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 3, mid_y - 2, mid_x + 3, mid_y + 2], fill=CORAL_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 54..74, y: 48..58)
    for ny in range(48, 59):
        for nx in range(54, 75):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 10.0)
            r_n = int(np.clip(42 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            g_n = int(np.clip(43 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            b_n = int(np.clip(50 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 5. Torso Body Shell (x: 43..85, y: 56..97)
    cx_t, cy_t = 64.0, 77.0
    for y in range(56, 98):
        for x in range(43, 86):
            dx = (x - cx_t) / 20.5
            dy = (y - cy_t) / 19.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 20.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Ivory enamel shock-absorbing chest & belly plate
                is_chest_plate = ((x - 64.0)**2 / 11.0**2 + (y - 76.0)**2 / 12.0**2 <= 1.0)
                if is_chest_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    # Outer obsidian tungsten shell with warm magma trim
                    is_rim = dist_sq >= 0.75
                    if is_rim:
                        r_t = int(np.clip(212 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        g_t = int(np.clip(122 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        b_t = int(np.clip(42 * (0.8 + 0.4 * spec) + 35 * shine - 10 * edge_shade, 0, 255))
                    else:
                        r_t = int(np.clip(42 * (0.75 + 0.5 * spec) - 15 * edge_shade + 50 * shine, 0, 255))
                        g_t = int(np.clip(43 * (0.75 + 0.5 * spec) - 15 * edge_shade + 50 * shine, 0, 255))
                        b_t = int(np.clip(50 * (0.75 + 0.5 * spec) - 15 * edge_shade + 55 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Center mini clockwork regulator window at (64, 76)
    ch_d.ellipse([61, 73, 67, 79], fill=OUTLINE)
    ch_d.ellipse([62, 74, 66, 78], fill=MAGMA_BASE)
    ch_d.point((64, 76), fill=AMBER_BASE)
    ch_d.point((63, 75), fill=WHITE_SHINE)

    # Three ventilation / heat-sink slits on belly plate
    for sy in [82, 85, 88]:
        ch_d.line([(59, sy), (69, sy)], fill=MAGMA_DARK, width=1)
        ch_d.line([(60, sy), (68, sy)], fill=OUTLINE, width=1)

    # 6. Left Arm & Clenched Claw Palm (low, near hip)
    ch_d.line([(48, 74), (40, 84)], fill=STEEL_BASE, width=4)
    ch_d.ellipse([36, 82, 43, 89], fill=TUNGSTEN_BASE, outline=OUTLINE)
    ch_d.ellipse([38, 84, 41, 87], fill=MAGMA_BASE)

    # 7. Right Arm & Grip Hub (tucked at ribs)
    ch_d.line([(74, 73), (82, 75)], fill=STEEL_BASE, width=4)
    ch_d.ellipse([79, 73, 85, 79], fill=TUNGSTEN_BASE, outline=OUTLINE)
    ch_d.point((82, 76), fill=MAGMA_BASE)

    apply_clean_outline(chassis_img)

    # Strictly 0 pixels at x >= 94 (0-ART9/11)
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_salamander_radiator_crest_horns.png
    # Features:
    # - Low-profile streamlined reptile skull dome at (64, 44), rx=19.0, ry=15.5
    # - Obsidian tungsten cranial plate (#2A2B32) with magma gold beveling (#D47A2A)
    # - Ivory White (#FFFDF8) enamel cheeks and broad lower jaw
    # - Nostril steam vents & determined sapper mouth seam
    # - Twin folding thin copper radiator crest fins (耳部機關) at (36..46, 16..30) and (82..92, 16..30)
    # - Countersunk screws on jaw and cheeks
    # - HOLLOW EYE SOCKETS centered at (52, 40) and (76, 40) (alpha == 0 for 0-ART27)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 44.0
    hrx, hry = 19.0, 15.5
    eye_centers = [(52, 40), (76, 40)]

    # 1. Base Skull Dome (Obsidian Tungsten, Magma Gold, Ivory Enamel Cheeks)
    for y in range(int(hcy - hry - 2), int(hcy + hry + 3)):
        for x in range(int(hcx - hrx - 2), int(hcx + hrx + 3)):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 17.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 5.5)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                is_muzzle = (y >= 43 and abs(x - hcx) <= 15.5 and ((x - hcx)/15.0)**2 + ((y - 48)/10.0)**2 <= 1.0)
                if is_muzzle:
                    r_h = int(np.clip(255 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    g_h = int(np.clip(253 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                    b_h = int(np.clip(248 * (0.88 + 0.2 * spec) - 35 * edge_shade + 25 * shine, 0, 255))
                else:
                    # Cranial plate: obsidian tungsten with magma gold bevel
                    is_rim = dist_sq >= 0.72
                    if is_rim:
                        r_h = int(np.clip(212 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        g_h = int(np.clip(122 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        b_h = int(np.clip(42 * (0.8 + 0.4 * spec) + 35 * shine - 10 * edge_shade, 0, 255))
                    else:
                        r_h = int(np.clip(42 * (0.75 + 0.5 * spec) - 15 * edge_shade + 50 * shine, 0, 255))
                        g_h = int(np.clip(43 * (0.75 + 0.5 * spec) - 15 * edge_shade + 50 * shine, 0, 255))
                        b_h = int(np.clip(50 * (0.75 + 0.5 * spec) - 15 * edge_shade + 55 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Snout nostrils & determined sapper mouth seam
    hd.ellipse([61, 46, 63, 48], fill=OUTLINE)
    hd.ellipse([65, 46, 67, 48], fill=OUTLINE)
    hd.line([(59, 52), (69, 52)], fill=OUTLINE, width=1)
    hd.line([(64, 49), (64, 52)], fill=OUTLINE, width=1)

    # Cheek Screws
    hd.ellipse([45, 46, 47, 48], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((46, 47), fill=WHITE_SHINE)
    hd.ellipse([81, 46, 83, 48], fill=GOLD_BASE, outline=OUTLINE)
    hd.point((82, 47), fill=WHITE_SHINE)

    # 2. Twin Folding Radiator Crest Fins (薄銅散熱葉片導流鰭角)
    # Left Crest Fin: sweeps from (46, 33) to (32, 17)
    hd.polygon([(46, 33), (32, 18), (39, 14), (50, 28)], fill=MAGMA_BASE, outline=OUTLINE)
    hd.polygon([(45, 31), (34, 19), (39, 16), (48, 27)], fill=GOLD_BASE)
    for ly in range(20, 31, 3):
        hd.line([(44 - (30 - ly)//3, ly), (48 - (30 - ly)//3, ly)], fill=MAGMA_DARK, width=1)
    hd.ellipse([46, 30, 50, 34], fill=MAGMA_DARK, outline=OUTLINE)
    hd.point((48, 32), fill=CORAL_BASE)

    # Right Crest Fin: sweeps from (82, 33) to (96, 17)
    hd.polygon([(82, 33), (96, 18), (89, 14), (78, 28)], fill=MAGMA_BASE, outline=OUTLINE)
    hd.polygon([(83, 31), (94, 19), (89, 16), (80, 27)], fill=GOLD_BASE)
    for ry in range(20, 31, 3):
        hd.line([(80 + (30 - ry)//3, ry), (84 + (30 - ry)//3, ry)], fill=MAGMA_DARK, width=1)
    hd.ellipse([78, 30, 82, 34], fill=MAGMA_DARK, outline=OUTLINE)
    hd.point((80, 32), fill=CORAL_BASE)

    # Forehead Radiator Plate / Brow Ridge
    for bx in range(54, 75):
        head_img.putpixel((bx, 33), MAGMA_BASE)
        head_img.putpixel((bx, 34), GOLD_BASE)
    hd.line([(58, 32), (70, 32)], fill=GOLD_LIGHT, width=1)

    # 3. HOLLOW EYE SOCKETS (0-ART27 compliance)
    for ecx, ecy in eye_centers:
        hd.ellipse([ecx - 6, ecy - 6, ecx + 6, ecy + 6], outline=MAGMA_BASE, width=1)
        hd.ellipse([ecx - 5, ecy - 5, ecx + 5, ecy + 5], outline=OUTLINE, width=1)
        for y in range(ecy - 4, ecy + 5):
            for x in range(ecx - 4, ecx + 5):
                if (x - ecx)**2 + (y - ecy)**2 <= 3.5**2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    ignore_eyes = [(ecx, ecy, 3.8) for ecx, ecy in eye_centers]
    apply_clean_outline(head_img, ignore_regions=ignore_eyes)

    # Re-verify eye centers strictly alpha = 0
    for ecx, ecy in eye_centers:
        for y in range(ecy - 3, ecy + 4):
            for x in range(ecx - 3, ecx + 4):
                if (x - ecx)**2 + (y - ecy)**2 <= 3.2**2:
                    head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 30)
    # File: optic_core/face_salamander_amber_dial_lens.png
    # Features:
    # - Twin High-Temperature Amber Optical Crystal Lenses at (52, 40) and (76, 40)
    # - Magma brass mounting bezel rings (#D47A2A / #1F1A3A)
    # - Amber crystal lens with concentric pressure gauge reticle and redline pointer (#FFA010)
    # - Brilliant white glints
    # - Fully opaque lens center (alpha == 255, min_alpha > 200, 0-ART27 & 0-QA31 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in eye_centers:
        r_lens = 4.5
        c_d.ellipse([int(ex - r_lens - 1), int(ey - r_lens - 1), int(ex + r_lens + 1), int(ey + r_lens + 1)],
                    fill=MAGMA_DARK, outline=OUTLINE)

        for y in range(int(ey - r_lens - 1), int(ey + r_lens + 2)):
            for x in range(int(ex - r_lens - 1), int(ex + r_lens + 2)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= r_lens:
                    spec = max(0.0, 1.0 - dist / r_lens)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.2))**2 + (y - (ey - 1.2))**2)**0.5 / 2.0)**2
                    is_reticle = (abs(dist - 2.5) <= 0.4)
                    if is_reticle:
                        r_c, g_c, b_c = 255, 235, 160
                    else:
                        r_c = int(np.clip(255 * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                        g_c = int(np.clip(160 * (0.85 + 0.25 * spec) + 50 * shine, 0, 255))
                        b_c = int(np.clip(16 * (0.85 + 0.3 * spec) + 50 * shine, 0, 255))
                    core_img.putpixel((x, y), (r_c, g_c, b_c, 255))

        c_d.ellipse([int(ex - r_lens), int(ey - r_lens), int(ex + r_lens), int(ey + r_lens)],
                    outline=GOLD_BASE, width=1)
        # Pressure dial pointer in coral / redline
        c_d.line([(int(ex), int(ey)), (int(ex + 2), int(ey - 2))], fill=CORAL_BASE, width=1)
        c_d.point((int(ex - 1), int(ey - 1)), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 25)
    # File: costume/costume_salamander_foundry_sapper_apron.png
    # Features:
    # - Foundry Sapper Apron (地熱工兵耐火鉚接圍裙)
    # - Deep heat-resistant leather apron (#5C3620)
    # - Coral pink suspender straps (#FF5E8A) with brass rivets
    # - Dopamine gold gear toolbelt (#FFD028) with oiler pouch at left hip
    # - Miniature round steam pressure gauge on chest center (64, 69)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    for y in range(58, 90):
        for x in range(48, 80):
            dx = (x - 64.0) / 14.5
            dy = (y - 74.0) / 14.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 60)**2 + (y - 69)**2)**0.5 / 14.0)
                shine = max(0.0, 1.0 - ((x - 60)**2 + (y - 69)**2)**0.5 / 4.0)**2
                is_apron = (abs(x - 64.0) <= 12.0 and y >= 64)
                if is_apron:
                    r_v = int(np.clip(92 * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    g_v = int(np.clip(54 * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    b_v = int(np.clip(32 * (0.8 + 0.35 * spec) + 25 * shine, 0, 255))
                    costume_img.putpixel((x, y), (r_v, g_v, b_v, 255))

    # Coral Pink Cross-Suspender Straps (from shoulders down to apron)
    strap_points_left = [(52, 58), (54, 64), (56, 70)]
    for sx, sy in strap_points_left:
        cos_d.ellipse([sx - 1, sy - 1, sx + 2, sy + 2], fill=CORAL_BASE, outline=OUTLINE)
    strap_points_right = [(76, 58), (74, 64), (72, 70)]
    for sx, sy in strap_points_right:
        cos_d.ellipse([sx - 2, sy - 1, sx + 1, sy + 2], fill=CORAL_BASE, outline=OUTLINE)

    # Toolbelt at (x: 50..78, y: 80..83) in Dopamine Gold (#FFD028)
    for bx in range(50, 79):
        costume_img.putpixel((bx, 80), GOLD_DARK)
        costume_img.putpixel((bx, 81), GOLD_BASE)
        costume_img.putpixel((bx, 82), GOLD_LIGHT)
        costume_img.putpixel((bx, 83), GOLD_DARK)

    # Central Round Steam Pressure Gauge on chest (64, 69)
    cos_d.ellipse([60, 65, 68, 73], fill=MAGMA_DARK, outline=OUTLINE)
    cos_d.ellipse([61, 66, 67, 72], fill=GOLD_BASE)
    cos_d.ellipse([62, 67, 66, 71], fill=IVORY_PRIMARY)
    cos_d.line([(64, 69), (66, 68)], fill=CORAL_BASE, width=1)
    cos_d.point((64, 69), fill=AMBER_BASE)
    cos_d.point((63, 67), fill=WHITE_SHINE)

    # Miniature Oiler Pouch / Grease Gun Clip at Left Hip (49, 78)
    cos_d.rectangle([47, 77, 53, 83], fill=APRON_DARK, outline=OUTLINE)
    cos_d.rectangle([48, 78, 52, 80], fill=MAGMA_BASE)
    cos_d.ellipse([49, 79, 51, 81], fill=GOLD_BASE, outline=OUTLINE)

    apply_clean_outline(costume_img)
    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_salamander_foundry_stamping_sledgehammer.png
    # Features:
    # - Foundry Stamping Sledgehammer (熔爐衝壓巨錘)
    # - Right-hand single held (0-MKT7 compliant) at (82, 75)
    # - Heat-resistant tungsten shaft (#4A5568 / #76849B) extending from (80, 84) through grip (82, 75) up-right to (100, 48)
    # - Heavy pneumatic anvil stamping hammer head (approx 26px x 24px) at (96..124, 28..52)
    # - Stamped anvil face, pneumatic exhaust ports, golden high-pressure valve (#FFD028)
    # - Amber geothermal core crystal (#FFA010) in hammer core
    # - Coral pink heat-shield collar rings (#FF5E8A)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Tungsten Shaft: from (79, 86) to (103, 44)
    for t in np.linspace(0.0, 1.0, 60):
        sx = 79.0 + t * 24.0
        sy = 86.0 - t * 42.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(74 * (0.8 + 0.45 * spec) + 50 * spec, 0, 255))
                    g_s = int(np.clip(85 * (0.8 + 0.45 * spec) + 50 * spec, 0, 255))
                    b_s = int(np.clip(104 * (0.8 + 0.45 * spec) + 55 * spec, 0, 255))
                    weapon_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Grip wrapped zone at (82, 75)
    for gy in range(73, 78):
        wd.line([(80, gy), (84, gy)], fill=MAGMA_BASE, width=1)
    wd.point((82, 74), fill=GOLD_BASE)

    # Pommel knob with coral jewel at (78, 87)
    wd.ellipse([76, 85, 80, 89], fill=MAGMA_DARK, outline=OUTLINE)
    wd.ellipse([77, 86, 79, 88], fill=CORAL_BASE)
    wd.point((77, 86), fill=WHITE_SHINE)

    # Heat-shield collar ring on shaft before hammer head at (97, 53)
    wd.ellipse([95, 51, 99, 55], fill=CORAL_BASE, outline=OUTLINE)

    # 2. Heavy Pneumatic Stamping Hammer Head centered at (108, 38)
    hm_cx, hm_cy = 108.0, 38.0
    hm_w, hm_h = 13.0, 11.0  # half-widths

    for y in range(int(hm_cy - hm_h - 1), int(hm_cy + hm_h + 2)):
        for x in range(int(hm_cx - hm_w - 1), int(hm_cx + hm_w + 2)):
            dx = (x - hm_cx) / hm_w
            dy = (y - hm_cy) / hm_h
            if abs(dx) <= 1.0 and abs(dy) <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hm_cx - 4))**2 + (y - (hm_cy - 4))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hm_cx - 4))**2 + (y - (hm_cy - 4))**2)**0.5 / 5.0)**2

                # Outer forging steel with magma gold bevel
                is_rim = (abs(dx) >= 0.78 or abs(dy) >= 0.78)
                if is_rim:
                    r_h = int(np.clip(212 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    g_h = int(np.clip(122 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    b_h = int(np.clip(42 * (0.8 + 0.4 * spec) + 35 * shine, 0, 255))
                else:
                    # Obsidian tungsten heavy hammer body
                    r_h = int(np.clip(42 * (0.75 + 0.5 * spec) + 45 * shine, 0, 255))
                    g_h = int(np.clip(43 * (0.75 + 0.5 * spec) + 45 * shine, 0, 255))
                    b_h = int(np.clip(50 * (0.75 + 0.5 * spec) + 50 * shine, 0, 255))

                weapon_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # Anvil striking face (flat right edge of hammer) at x: 120..122, y: 30..46
    for y in range(30, 47):
        weapon_img.putpixel((120, y), STEEL_LIGHT)
        weapon_img.putpixel((121, y), STEEL_SHINE)

    # Pneumatic exhaust ports on top of hammer at (104, 26) and (112, 26)
    wd.ellipse([102, 25, 106, 28], fill=MAGMA_DARK, outline=OUTLINE)
    wd.ellipse([103, 26, 105, 27], fill=GOLD_BASE)
    wd.ellipse([110, 25, 114, 28], fill=MAGMA_DARK, outline=OUTLINE)
    wd.ellipse([111, 26, 113, 27], fill=GOLD_BASE)

    # Amber Geothermal Power Core in hammer center (108, 38)
    wd.ellipse([104, 34, 112, 42], fill=MAGMA_DARK, outline=OUTLINE)
    wd.ellipse([105, 35, 111, 41], fill=GOLD_BASE)
    wd.ellipse([106, 36, 110, 40], fill=AMBER_BASE)
    wd.point((107, 37), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_salamander_four_vane_heatsink", key_img),
        ("back_curio", "curio_salamander_segmented_damping_tail", curio_img),
        ("chassis", "chassis_salamander_magma_tungsten_default", chassis_img),
        ("head_unit", "head_salamander_radiator_crest_horns", head_img),
        ("optic_core", "face_salamander_amber_dial_lens", core_img),
        ("costume", "costume_salamander_foundry_sapper_apron", costume_img),
        ("weapon", "weapon_salamander_foundry_stamping_sledgehammer", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{SALAMANDER_PD_DIR}/{slot}"
        os.makedirs(out_dir, exist_ok=True)
        dst_128 = f"{out_dir}/{item_id}.png"
        img.save(dst_128)

        # 512x512 with LANCZOS
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{out_dir}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copyfile(f"{SALAMANDER_PD_DIR}/winding_key/key_salamander_four_vane_heatsink.png",
                    f"{KEY_DIR}/key_salamander_four_vane_heatsink.png")
    shutil.copyfile(f"{SALAMANDER_PD_DIR}/weapon/weapon_salamander_foundry_stamping_sledgehammer.png",
                    f"{WEAPON_DIR}/weapon_salamander_foundry_stamping_sledgehammer.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order by layer_z_index:
    # z=5: winding_key
    # z=8: back_curio
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

    proof_comp = f"{SALAMANDER_PD_DIR}/proof_paperdoll_salamander_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SALAMANDER_PD_DIR}/proof_paperdoll_salamander_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices
    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Optic", "Costume", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, core_img, costume_img, weapon_img]

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255))

    strip_path = f"{SALAMANDER_PD_DIR}/proof_salamander_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/salamander_idle_hd.png)
    # ─────────────────────────────────────────────────────────────
    showcase_dir = f"{REPO_ROOT}/game/assets/sprites/player/showcase"
    os.makedirs(showcase_dir, exist_ok=True)
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
        sc_sdraw.ellipse((400 - 180, 1120 - 18, 400 + 180, 1120 + 18), fill=(31, 26, 58, 110))
        sc_shadow = sc_shadow.filter(ImageFilter.GaussianBlur(radius=10))

        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))
        showcase_dst = f"{showcase_dir}/salamander_idle_hd.png"
        showcase_hd.save(showcase_dst)
        print("  ✓ Showcase HD saved:", showcase_dst)


if __name__ == "__main__":
    build_all()
