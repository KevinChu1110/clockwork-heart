#!/usr/bin/env python3
"""
build_fawn_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for Emerald Fawn (翠角鹿 / The Emerald Fawn) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/EMERALD_FAWN_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero flesh, zero slime, all stamped tinplate, brass vernier calipers, brass key)
- references/art_direction.md (Dopamine high-saturation palette, clean enamel/wood-tint lacquer, deep outline)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r
- Benchmarked directly against Xuanji Tortoise, Colossus Elephant, Spring-Leg Frog, and Porcelain Panda standards.
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
FAWN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fawn"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (Emerald Fawn Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline

# Primary: Ivory White Stamped Tinplate (#FFFDF8)
IVORY_PRIMARY = (255, 253, 248, 255)
IVORY_LIGHT   = (255, 255, 255, 255)
IVORY_SHADE   = (225, 222, 215, 255)
IVORY_DEEP    = (185, 180, 172, 255)

# Secondary: Warm Timber Stamped Lacquer (#C4783A)
TIMBER_BASE   = (196, 120, 58, 255)
TIMBER_LIGHT  = (235, 160, 95, 255)
TIMBER_SHINE  = (255, 195, 140, 255)
TIMBER_DARK   = (145, 80, 32, 255)
TIMBER_DEEP   = (95, 48, 18, 255)

# Accent: Precision Brass Caliper & Gold (#FFD028 / #D4A017)
BRASS_GOLD    = (212, 160, 23, 255)
BRASS_LIGHT   = (255, 225, 95, 255)
BRASS_SHINE   = (255, 250, 175, 255)
BRASS_DARK    = (150, 105, 12, 255)
BRASS_DEEP    = (90, 60, 8, 255)

GOLD_PRIMARY  = (255, 208, 40, 255)
GOLD_LIGHT    = (255, 235, 115, 255)
GOLD_SHINE    = (255, 250, 185, 255)
GOLD_DARK     = (195, 145, 18, 255)

# Detail: Mint Vine Green & Emerald (#4ED86A)
MINT_GREEN    = (78, 216, 106, 255)
MINT_LIGHT    = (140, 240, 165, 255)
MINT_SHINE    = (200, 255, 215, 255)
MINT_DARK     = (36, 140, 62, 255)
MINT_DEEP     = (18, 78, 35, 255)

# Scout Uniform Dark Forest Green (#2D6A4F)
FOREST_BASE   = (45, 106, 79, 255)
FOREST_LIGHT  = (72, 148, 112, 255)
FOREST_DARK   = (28, 72, 54, 255)

# Warm Highlight: High-Torque Warm Orange (#FFA010)
ORANGE_ACCENT = (255, 160, 16, 255)
ORANGE_LIGHT  = (255, 205, 80, 255)
ORANGE_DARK   = (190, 95, 10, 255)

# Rubber Hoof & Mechanism (#26262B)
RUBBER_BASE   = (38, 38, 43, 255)
RUBBER_LIGHT  = (68, 68, 78, 255)
RUBBER_DARK   = (22, 22, 26, 255)

# Steel Spring & Rods
STEEL_LIGHT   = (195, 205, 220, 255)
STEEL_MID     = (130, 142, 160, 255)
STEEL_DARK    = (70, 78, 92, 255)

# Amber Lens Optics
AMBER_CORE    = (255, 180, 30, 255)
AMBER_LIGHT   = (255, 225, 90, 255)
AMBER_DARK    = (180, 95, 10, 255)
AMBER_DEEP    = (110, 50, 5, 255)

WHITE_SHINE   = (255, 255, 255, 255)


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL EMERALD FAWN SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_fawn_clover_leaf_brass.png
    # Brass Clover-Leaf Wind-up Key (黃銅四葉草風葉發條鑰匙)
    # Prominently mounted on the deer's spine/back (socket at 68, 64)
    # Extending up and to the right: Key Head at (88, 38)
    # Fully visible outside head/body silhouette, iconic clockwork key!
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Key shaft entering spine socket at (68, 64) up to (88, 38)
    for t in np.linspace(0.0, 1.0, 40):
        sx = 68.0 + t * 20.0
        sy = 64.0 - t * 26.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(212 + 35 * spec, 0, 255))
                    g_s = int(np.clip(160 + 30 * spec, 0, 255))
                    b_s = int(np.clip(23 + 45 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Center socket boss at spine (68, 64)
    kd.ellipse([64, 60, 72, 68], fill=BRASS_DARK, outline=OUTLINE)
    kd.ellipse([65, 61, 71, 67], fill=BRASS_GOLD)

    # Key Head: Symmetrical Clover-Leaf 4 aerofoil petals centered at (88, 38)
    kcx, kcy = 88.0, 38.0
    r_hub = 4.2
    r_petal = 13.5

    for y in range(int(kcy - r_petal - 3), int(kcy + r_petal + 4)):
        for x in range(int(kcx - r_petal - 3), int(kcx + r_petal + 4)):
            dx = x - kcx
            dy = y - kcy
            dist = (dx**2 + dy**2)**0.5
            if dist <= r_petal:
                angle = np.arctan2(dy, dx)
                clover = np.cos(4.0 * angle)
                petal_bound = r_hub + (r_petal - r_hub) * max(0.0, (clover + 0.35) / 1.35)
                if dist <= petal_bound:
                    if dist <= r_hub:
                        spec = max(0.0, 1.0 - dist / r_hub)
                        r_k = int(np.clip(212 + 40 * spec, 0, 255))
                        g_k = int(np.clip(160 + 45 * spec, 0, 255))
                        b_k = int(np.clip(23 + 60 * spec, 0, 255))
                    else:
                        spec = max(0.0, 1.0 - ((x - (kcx - 3))**2 + (y - (kcy - 3))**2)**0.5 / 12.0)
                        shine = max(0.0, 1.0 - ((x - (kcx - 4))**2 + (y - (kcy - 4))**2)**0.5 / 5.0)**2
                        # Hollow cutout in petals
                        if dist > 6.2 and dist < 10.2 and clover > 0.65:
                            continue
                        r_k = int(np.clip(212 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        g_k = int(np.clip(160 * (0.8 + 0.3 * spec) + 40 * shine, 0, 255))
                        b_k = int(np.clip(23 * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                    key_img.putpixel((x, y), (r_k, g_k, b_k, 255))

    # Center Hub hole
    kd.ellipse([int(kcx - r_hub), int(kcy - r_hub), int(kcx + r_hub), int(kcy + r_hub)], outline=OUTLINE, width=1)
    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=OUTLINE)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=BRASS_SHINE)

    # Clean thick outline around the key
    k_px = key_img.load()
    if k_px is not None:
        for y in range(int(kcy - r_petal - 2), int(kcy + r_petal + 3)):
            for x in range(int(kcx - r_petal - 2), int(kcx + r_petal + 3)):
                p = k_px[x, y]
                if isinstance(p, tuple) and p[3] > 100:
                    for nx, ny in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]:
                        np_px = k_px[nx, ny]
                        if isinstance(np_px, tuple) and np_px[3] == 0:
                            kd.point((nx, ny), fill=OUTLINE)

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Floating Side Accessory)
    # File: back_curio/curio_fawn_floating_pinecone_chime.png
    # Floating Pinecone Chime (懸浮發條小松果風鈴)
    # Positioned at right side (x: 100..116, y: 56..80), clean & self-contained
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    bcx, bcy = 106.0, 64.0

    # Hanging suspension ring
    cd.ellipse([int(bcx - 3), int(bcy - 14), int(bcx + 3), int(bcy - 8)], outline=OUTLINE, width=1)
    cd.ellipse([int(bcx - 2), int(bcy - 13), int(bcx + 2), int(bcy - 9)], fill=BRASS_LIGHT)

    # Pinecone body
    for y in range(int(bcy - 8), int(bcy + 10)):
        for x in range(int(bcx - 7), int(bcx + 8)):
            dx = (x - bcx) / 6.5
            dy = (y - bcy - 1) / 8.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (bcx - 2))**2 + (y - (bcy - 2))**2)**0.5 / 8.0)
                shine = max(0.0, 1.0 - ((x - (bcx - 2))**2 + (y - (bcy - 2))**2)**0.5 / 3.0)**2
                scale_tier = (y - int(bcy - 8)) % 3
                scale_edge = 1.0 if scale_tier == 0 else 0.0

                r_p = int(np.clip(196 * (0.85 + 0.3 * spec) + 40 * shine - 25 * scale_edge, 0, 255))
                g_p = int(np.clip(120 * (0.85 + 0.3 * spec) + 35 * shine - 15 * scale_edge, 0, 255))
                b_p = int(np.clip(58 * (0.85 + 0.3 * spec) + 20 * shine - 10 * scale_edge, 0, 255))
                curio_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    cd.ellipse([int(bcx - 6), int(bcy - 7), int(bcx + 6), int(bcy + 9)], outline=OUTLINE, width=1)

    # Chime tines hanging below pinecone
    for tx in [bcx - 3, bcx + 3]:
        for ty in range(int(bcy + 9), int(bcy + 17)):
            curio_img.putpixel((int(tx), int(ty)), BRASS_GOLD)
        cd.ellipse([int(tx - 1), int(bcy + 16), int(tx + 1), int(bcy + 18)], fill=GOLD_PRIMARY, outline=OUTLINE)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Base)
    # File: chassis/chassis_fawn_timber_tinplate_default.png
    # Features:
    # - Agile forest scout stance (林間遊俠側身聽風架式)
    # - Soft ground contact shadow at (64, 116)
    # - 4 mechanical articulated legs with rubber hooves (#26262B)
    # - Rear shock springs on hind legs
    # - Dual-tone stamped tinplate: Ivory belly (#FFFDF8) & Warm Timber flanks (#C4783A)
    # - Escapement balance-wheel viewport at chest (54, 72)
    # - Left hand grip joint at (32, 74)
    # - Right hand bowstring thimble joint at (46, 74)
    # - Strictly ZERO weapon baked in (0-ART9, 0-ART11 compliant: x >= 95 is strictly 0)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 32, 116 - 4, 64 + 32, 116 + 5], fill=(31, 26, 58, 120))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Hooves & Legs
    hoof_coords = [(42.0, 113.0), (56.0, 113.0), (74.0, 113.0), (86.0, 113.0)]

    for hcx, hcy in hoof_coords:
        ch_d.ellipse([int(hcx - 5), int(hcy), int(hcx + 5), int(hcy + 4)], fill=RUBBER_BASE, outline=OUTLINE)
        ch_d.point((int(hcx - 1), int(hcy + 1)), fill=RUBBER_LIGHT)
        ch_d.rectangle([int(hcx - 4), int(hcy - 3), int(hcx + 4), int(hcy)], fill=BRASS_GOLD, outline=OUTLINE)
        ch_d.point((int(hcx), int(hcy - 2)), fill=BRASS_SHINE)

    for lcx, ltop, lbot in [(42.0, 84, 110), (56.0, 86, 110), (74.0, 88, 110), (86.0, 88, 110)]:
        is_rear = (lcx >= 70.0)
        for y in range(ltop, lbot):
            for x in range(int(lcx - 3), int(lcx + 4)):
                dx = abs(x - lcx)
                if dx <= 2.2:
                    spec = max(0.0, 1.0 - dx / 2.2)
                    if is_rear and y >= 92 and y <= 104:
                        coil = int((y - 92) % 3)
                        if coil == 0:
                            r_l, g_l, b_l = STEEL_LIGHT[:3]
                        elif coil == 1:
                            r_l, g_l, b_l = STEEL_MID[:3]
                        else:
                            r_l, g_l, b_l = STEEL_DARK[:3]
                    else:
                        r_l = int(np.clip(196 * (0.8 + 0.3 * spec), 0, 255))
                        g_l = int(np.clip(120 * (0.8 + 0.3 * spec), 0, 255))
                        b_l = int(np.clip(58 * (0.8 + 0.3 * spec), 0, 255))
                    chassis_img.putpixel((x, y), (r_l, g_l, b_l, 255))

        knee_y = 96 if not is_rear else 98
        ch_d.ellipse([int(lcx - 3), knee_y - 3, int(lcx + 3), knee_y + 3], fill=BRASS_GOLD, outline=OUTLINE)
        ch_d.point((int(lcx - 1), knee_y - 1), fill=BRASS_SHINE)

    # Conical tail with brass plug at rear (x: 86..94, y: 80..88)
    for y in range(80, 88):
        for x in range(86, 95):
            if ((x - 88)**2 + (y - 84)**2)**0.5 <= 3.8:
                spec = max(0.0, 1.0 - ((x - 86)**2 + (y - 82)**2)**0.5 / 3.0)
                chassis_img.putpixel((x, y), (int(196 + 40 * spec), int(120 + 35 * spec), int(58 + 30 * spec), 255))
    ch_d.ellipse([86, 80, 94, 88], outline=OUTLINE, width=1)
    ch_d.point((90, 84), fill=BRASS_GOLD)

    # 3. Torso: Dual-tone Tinplate Panels (x: 40..86, y: 56..96)
    for y in range(56, 96):
        for x in range(40, 86):
            prog = (y - 56) / 40.0
            cur_hw = 16.0 + 5.0 * np.sin(prog * np.pi)
            dx = (x - 63.0) / cur_hw
            dy = (y - 76.0) / 20.0
            dist_sq = dx**2 + dy**2

            if dist_sq <= 1.0:
                d_light = ((x - 55.0)**2 + (y - 66.0)**2)**0.5
                spec = max(0.0, 1.0 - d_light / 18.0)
                shine = max(0.0, 1.0 - d_light / 5.5)**2
                edge_shade = max(0.0, (dist_sq - 0.35) / 0.65)

                is_front_breast = (x <= 66 and y <= 86)
                if is_front_breast:
                    r_p = int(np.clip(255 * (1.0 - 0.16 * edge_shade) + 20 * shine, 0, 255))
                    g_p = int(np.clip(253 * (1.0 - 0.15 * edge_shade) + 20 * shine, 0, 255))
                    b_p = int(np.clip(248 * (1.0 - 0.12 * edge_shade) + 20 * shine, 0, 255))
                else:
                    r_p = int(np.clip(196 * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_p = int(np.clip(120 * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                    b_p = int(np.clip(58 * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))

                chassis_img.putpixel((x, y), (r_p, g_p, b_p, 255))

    ch_d.ellipse([40, 56, 86, 96], outline=OUTLINE, width=1)

    # Rivet lines along panel seams
    for ry in [62, 70, 78, 86]:
        ch_d.point((47, ry), fill=BRASS_GOLD)
        ch_d.point((67, ry), fill=BRASS_GOLD)

    # Escapement Balance-Wheel Viewport at chest (54, 72)
    ch_d.ellipse([50, 68, 58, 76], fill=OUTLINE)
    ch_d.ellipse([51, 69, 57, 75], fill=BRASS_DARK)
    ch_d.ellipse([52, 70, 56, 74], fill=GOLD_PRIMARY, outline=BRASS_GOLD)
    ch_d.point((54, 72), fill=MINT_LIGHT)

    # 4. Forearms & Wrist Sockets
    # Left wrist at (32, 74)
    ch_d.ellipse([29, 71, 35, 77], fill=BRASS_GOLD, outline=OUTLINE)
    # Right wrist at (46, 74)
    ch_d.ellipse([43, 71, 49, 77], fill=BRASS_GOLD, outline=OUTLINE)

    # Neck collar ring (connector for head unit)
    ch_d.ellipse([54, 48, 74, 56], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.point((64, 51), fill=BRASS_SHINE)

    # Strict compliance: clean weapon zone (x >= 95)
    for y in range(H):
        for x in range(95, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_fawn_vernier_caliper_horns.png
    # Features:
    # - Stamped tinplate compact fawn head (x: 44..84, y: 28..56)
    # - Exactly 2 tinplate leaf ears with copper wire pickup mesh
    # - High-rising Dual Brass Vernier Caliper Antlers
    # - 0-ART27 COMPLIANT: Recessed hollow eye sockets at (53, 42) and (73, 42)
    # - Rounded bottom chin with horizontal ventilation louvers
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # Antlers: Dual Brass Vernier Caliper Antlers
    # Left antler: (54, 28) up to (30, 8)
    for t in np.linspace(0.0, 1.0, 45):
        ax = 54.0 - t * 24.0
        ay = 28.0 - t * 20.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    head_img.putpixel((int(ax + dx), int(ay + dy)), BRASS_GOLD)
    for tick_t in [0.3, 0.5, 0.7, 0.9]:
        tx = int(54.0 - tick_t * 24.0)
        ty = int(28.0 - tick_t * 20.0)
        hd.line([(tx - 2, ty - 2), (tx + 1, ty + 1)], fill=GOLD_SHINE, width=1)
    hd.line([(42, 18), (34, 14)], fill=BRASS_GOLD, width=2)
    hd.ellipse([32, 12, 36, 16], fill=GOLD_PRIMARY, outline=OUTLINE)
    hd.polygon([(30, 8), (24, 6), (28, 12)], fill=MINT_GREEN, outline=OUTLINE)

    # Right antler: (74, 28) up to (98, 8)
    for t in np.linspace(0.0, 1.0, 45):
        ax = 74.0 + t * 24.0
        ay = 28.0 - t * 20.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    head_img.putpixel((int(ax + dx), int(ay + dy)), BRASS_GOLD)
    for tick_t in [0.3, 0.5, 0.7, 0.9]:
        tx = int(74.0 + tick_t * 24.0)
        ty = int(28.0 - tick_t * 20.0)
        hd.line([(tx - 1, ty + 1), (tx + 2, ty - 2)], fill=GOLD_SHINE, width=1)
    hd.line([(86, 18), (94, 14)], fill=BRASS_GOLD, width=2)
    hd.ellipse([92, 12, 96, 16], fill=GOLD_PRIMARY, outline=OUTLINE)
    hd.polygon([(98, 8), (104, 6), (100, 12)], fill=MINT_GREEN, outline=OUTLINE)

    # Ears: Exactly Two Tinplate Leaf Ears
    for y in range(18, 35):
        for x in range(43, 53):
            prog = (y - 18) / 16.0
            ew = 4.0 * np.sin(prog * np.pi)
            if abs(x - 48.0) <= ew:
                spec = max(0.0, 1.0 - abs(x - 47.0) / 3.0)
                head_img.putpixel((x, y), (int(196 + 35 * spec), int(120 + 30 * spec), int(58 + 25 * spec), 255))
    hd.ellipse([44, 18, 52, 34], outline=OUTLINE, width=1)
    for y in range(22, 31, 2):
        hd.point((48, y), fill=BRASS_SHINE)

    for y in range(18, 35):
        for x in range(75, 85):
            prog = (y - 18) / 16.0
            ew = 4.0 * np.sin(prog * np.pi)
            if abs(x - 80.0) <= ew:
                spec = max(0.0, 1.0 - abs(x - 79.0) / 3.0)
                head_img.putpixel((x, y), (int(196 + 35 * spec), int(120 + 30 * spec), int(58 + 25 * spec), 255))
    hd.ellipse([76, 18, 84, 34], outline=OUTLINE, width=1)
    for y in range(22, 31, 2):
        hd.point((80, y), fill=BRASS_SHINE)

    # Head Dome & Faceplate
    hcx, hcy = 64.0, 42.0
    for y in range(28, 56):
        for x in range(44, 85):
            dx = (x - hcx) / 19.0
            dy = (y - hcy) / 13.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                is_front_plate = (y >= 36)
                if is_front_plate:
                    r_h = int(np.clip(255 * (1.0 - 0.15 * edge_shade) + 20 * shine, 0, 255))
                    g_h = int(np.clip(253 * (1.0 - 0.14 * edge_shade) + 20 * shine, 0, 255))
                    b_h = int(np.clip(248 * (1.0 - 0.10 * edge_shade) + 20 * shine, 0, 255))
                else:
                    r_h = int(np.clip(196 * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                    g_h = int(np.clip(120 * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                    b_h = int(np.clip(58 * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))

                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    hd.ellipse([45, 28, 83, 55], outline=OUTLINE, width=1)

    # Chin louver slits
    for ly in [50, 52]:
        hd.line([(60, ly), (68, ly)], fill=OUTLINE, width=1)

    # 0-ART27 Hollow Eye Sockets
    eye_centers = [(53.0, 42.0), (73.0, 42.0)]
    r_eye_socket = 4.2
    for ecx, ecy in eye_centers:
        for y in range(int(ecy - r_eye_socket - 2), int(ecy + r_eye_socket + 3)):
            for x in range(int(ecx - r_eye_socket - 2), int(ecx + r_eye_socket + 3)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_eye_socket:
                    head_img.putpixel((x, y), (0, 0, 0, 0))
        hd.ellipse([int(ecx - r_eye_socket), int(ecy - r_eye_socket), int(ecx + r_eye_socket), int(ecy + r_eye_socket)], outline=OUTLINE, width=1)
        hd.ellipse([int(ecx - r_eye_socket - 1), int(ecy - r_eye_socket - 1), int(ecx + r_eye_socket + 1), int(ecy + r_eye_socket + 1)], outline=BRASS_GOLD, width=1)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 25)
    # File: optic_core/face_fawn_amber_lens_alert_eyes.png
    # Features:
    # - Dual Amber Glass Optical Convex Lenses (雙聯琥珀光學凸透鏡)
    # - Centered exactly at (53, 42) and (73, 42)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ecx, ecy in eye_centers:
        r_lens = 3.8
        for y in range(int(ecy - r_lens - 1), int(ecy + r_lens + 2)):
            for x in range(int(ecx - r_lens - 1), int(ecx + r_lens + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    norm_dist = dist / r_lens
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 2.8)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 1.3)**2
                    rim = max(0.0, (norm_dist - 0.5) / 0.5)

                    r_o = int(np.clip(255 * (0.7 + 0.3 * spec) + 40 * shine - 30 * rim, 0, 255))
                    g_o = int(np.clip(180 * (0.6 + 0.4 * spec) + 50 * shine - 40 * rim, 0, 255))
                    b_o = int(np.clip(25 * (0.5 + 0.5 * spec) + 80 * shine + 20 * rim, 0, 255))
                    core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

        c_d.ellipse([int(ecx - r_lens), int(ecy - r_lens), int(ecx + r_lens), int(ecy + r_lens)], outline=OUTLINE, width=1)
        c_d.point((int(ecx), int(ecy)), fill=AMBER_DEEP)
        c_d.point((int(ecx + 1), int(ecy)), fill=AMBER_DARK)
        c_d.point((int(ecx - 1), int(ecy - 1)), fill=WHITE_SHINE)
        c_d.point((int(ecx), int(ecy - 1)), fill=GOLD_SHINE)

    for bx, by in [(48, 46), (78, 46)]:
        c_d.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=GOLD_PRIMARY, outline=OUTLINE)
        c_d.point((bx, by), fill=WHITE_SHINE)

    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 30)
    # File: costume/costume_fawn_emerald_scout_tunic.png
    # Features:
    # - Emerald Scout Tunic (翡翠林緣巡守背帶工裝)
    # - Forest green light capelet over shoulders (x: 42..84, y: 52..68)
    # - Diagonal scout harness belt with polished brass buckle
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ct_d = ImageDraw.Draw(costume_img)

    for y in range(52, 68):
        for x in range(42, 85):
            prog = (y - 52) / 16.0
            cw = 18.0 + 3.0 * np.sin(prog * np.pi)
            dx = abs(x - 63.5)
            if dx <= cw:
                spec = max(0.0, 1.0 - ((x - 55.0)**2 + (y - 56.0)**2)**0.5 / 14.0)
                r_c = int(np.clip(45 * (0.8 + 0.3 * spec) + 15 * np.sin(x * 0.5), 0, 255))
                g_c = int(np.clip(106 * (0.8 + 0.3 * spec) + 20 * np.sin(y * 0.5), 0, 255))
                b_c = int(np.clip(79 * (0.8 + 0.3 * spec) + 10 * np.sin(x * 0.3 + y * 0.3), 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    ct_d.ellipse([42, 52, 84, 68], outline=OUTLINE, width=1)

    for x in range(44, 83, 3):
        ct_d.point((x, 66), fill=MINT_LIGHT)

    for t in np.linspace(0.0, 1.0, 30):
        sx = 48.0 + t * 26.0
        sy = 64.0 + t * 22.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    st_val = 145 + int(30 * (1 - abs(dx) / 1.5))
                    costume_img.putpixel((int(sx + dx), int(sy + dy)), (st_val, int(st_val * 0.55), int(st_val * 0.22), 255))

    ct_d.ellipse([58, 71, 64, 77], fill=BRASS_GOLD, outline=OUTLINE)
    ct_d.ellipse([59, 72, 63, 76], fill=GOLD_PRIMARY)
    ct_d.point((61, 73), fill=BRASS_SHINE)

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40, Top Layer)
    # File: weapon/weapon_fawn_vernier_shortbow.png
    # Features:
    # - Verdant Caliber-Horn Composite Bow / Wind-Listening Vernier Shortbow
    # - SINGLE-WIELD (0-MKT7): Left hand grips bow riser at (32, 74)
    #   Right hand holds drawn thimble at (46, 74)
    # - Bow limbs arch cleanly on the left (x: 18..34, y: 46..102)
    # - Metallic bowstring extends strictly between pulleys (22, 48), thimble (46, 74), and (22, 100)
    # - Arrow extends forward from (46, 74) through riser (32, 74) to tip at (16, 74)
    # - ZERO pixels crossing body or reaching weapon zone x >= 95
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Upper limb: from grip (32, 74) through (20, 60) to tip pulley (22, 48)
    for t in np.linspace(0.0, 1.0, 45):
        bx = (1 - t)**2 * 32.0 + 2 * (1 - t) * t * 18.0 + t**2 * 22.0
        by = (1 - t)**2 * 74.0 + 2 * (1 - t) * t * 60.0 + t**2 * 48.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    dist = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist / 1.5)
                    r_w = int(np.clip(196 * (0.8 + 0.3 * spec) + 20 * np.sin(t * 12.0), 0, 255))
                    g_w = int(np.clip(120 * (0.8 + 0.3 * spec) + 15 * np.sin(t * 12.0), 0, 255))
                    b_w = int(np.clip(58 * (0.8 + 0.3 * spec) + 10 * np.sin(t * 12.0), 0, 255))
                    weapon_img.putpixel((int(bx + dx), int(by + dy)), (r_w, g_w, b_w, 255))

    # Lower limb: from grip (32, 74) through (18, 88) to tip pulley (22, 100)
    for t in np.linspace(0.0, 1.0, 45):
        bx = (1 - t)**2 * 32.0 + 2 * (1 - t) * t * 18.0 + t**2 * 22.0
        by = (1 - t)**2 * 74.0 + 2 * (1 - t) * t * 88.0 + t**2 * 100.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    dist = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist / 1.5)
                    r_w = int(np.clip(196 * (0.8 + 0.3 * spec) + 20 * np.sin(t * 12.0), 0, 255))
                    g_w = int(np.clip(120 * (0.8 + 0.3 * spec) + 15 * np.sin(t * 12.0), 0, 255))
                    b_w = int(np.clip(58 * (0.8 + 0.3 * spec) + 10 * np.sin(t * 12.0), 0, 255))
                    weapon_img.putpixel((int(bx + dx), int(by + dy)), (r_w, g_w, b_w, 255))

    # Pulleys at limb tips
    for pcx, pcy in [(22.0, 48.0), (22.0, 100.0)]:
        for y in range(int(pcy - 3), int(pcy + 4)):
            for x in range(int(pcx - 3), int(pcx + 4)):
                dist = ((x - pcx)**2 + (y - pcy)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    r_p = int(np.clip(212 + 35 * spec, 0, 255))
                    g_p = int(np.clip(160 + 30 * spec, 0, 255))
                    b_p = int(np.clip(23 + 40 * spec, 0, 255))
                    weapon_img.putpixel((x, y), (r_p, g_p, b_p, 255))
        wd.ellipse([int(pcx - 3), int(pcy - 3), int(pcx + 3), int(pcy + 3)], outline=OUTLINE, width=1)
        wd.point((int(pcx), int(pcy)), fill=GOLD_SHINE)

    # Center Bow Riser & Caliper Sight Bracket at (30..36, 68..80)
    for y in range(68, 81):
        for x in range(30, 37):
            spec = max(0.0, 1.0 - abs(x - 33.0) / 3.0)
            r_r = int(np.clip(212 + 35 * spec, 0, 255))
            g_r = int(np.clip(160 + 30 * spec, 0, 255))
            b_r = int(np.clip(23 + 40 * spec, 0, 255))
            weapon_img.putpixel((x, y), (r_r, g_r, b_r, 255))
    wd.rectangle([30, 68, 36, 80], outline=OUTLINE, width=1)

    # Caliper sight pin
    for px in range(32, 38):
        wd.point((px, 66), fill=GOLD_LIGHT)
    wd.point((38, 66), fill=MINT_SHINE)

    # Left Hand Alloy Gauntlet gripping the riser at (30..36, 72..77)
    wd.ellipse([30, 72, 36, 77], fill=IVORY_PRIMARY, outline=OUTLINE)
    wd.point((33, 74), fill=BRASS_GOLD)

    # Clean bowstring: (22, 48) -> drawn thimble at (46, 74) -> (22, 100)
    wd.line([(22, 48), (46, 74)], fill=STEEL_LIGHT, width=1)
    wd.line([(46, 74), (22, 100)], fill=STEEL_LIGHT, width=1)

    # Right Hand Alloy Thimble holding the drawn string at (44..49, 72..76)
    wd.ellipse([44, 72, 49, 76], fill=BRASS_GOLD, outline=OUTLINE)
    wd.point((46, 74), fill=BRASS_SHINE)

    # Arrow: resting on riser, pointing forward from (46, 74) through (32, 74) to tip (16, 74)
    for ax in range(18, 47):
        spec = 1.0 if ax % 3 == 0 else 0.7
        weapon_img.putpixel((ax, 74), (int(130 * spec), int(142 * spec), int(160 * spec), 255))

    # Arrowhead: sharp three-prong penetrating head at (15..19, 72..76)
    wd.polygon([(15, 74), (19, 72), (18, 74), (19, 76)], fill=STEEL_LIGHT, outline=OUTLINE)
    wd.point((15, 74), fill=MINT_SHINE)

    # Arrow fletching feathers (mint vine feathers) at (42..45, 72..76)
    wd.line([(42, 72), (45, 74)], fill=MINT_GREEN, width=1)
    wd.line([(42, 76), (45, 74)], fill=MINT_GREEN, width=1)

    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE SLICES (128x128 & 512x512)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "chassis_fawn_timber_tinplate_default", chassis_img),
        ("head_unit", "head_fawn_vernier_caliper_horns", head_img),
        ("winding_key", "key_fawn_clover_leaf_brass", key_img),
        ("costume", "costume_fawn_emerald_scout_tunic", costume_img),
        ("optic_core", "face_fawn_amber_lens_alert_eyes", core_img),
        ("weapon", "weapon_fawn_vernier_shortbow", weapon_img),
        ("back_curio", "curio_fawn_floating_pinecone_chime", curio_img)
    ]

    for slot, item_id, img in slices:
        out_dir = f"{FAWN_PD_DIR}/{slot}"
        os.makedirs(out_dir, exist_ok=True)
        dst_128 = f"{out_dir}/{item_id}.png"
        img.save(dst_128)

        # 512x512 with LANCZOS
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{out_dir}/{item_id}_512.png"
        img_512.save(dst_512)

    # Universal copies
    shutil.copyfile(f"{FAWN_PD_DIR}/winding_key/key_fawn_clover_leaf_brass.png", f"{KEY_DIR}/key_fawn_clover_leaf_brass.png")
    shutil.copyfile(f"{FAWN_PD_DIR}/weapon/weapon_fawn_vernier_shortbow.png", f"{WEAPON_DIR}/weapon_fawn_vernier_shortbow.png")
    print("  ✓ Slices saved (128 & 512) and universal copies synchronized")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # ─────────────────────────────────────────────────────────────
    composite = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    composite.alpha_composite(key_img)
    composite.alpha_composite(curio_img)
    composite.alpha_composite(chassis_img)
    composite.alpha_composite(head_img)
    composite.alpha_composite(core_img)
    composite.alpha_composite(costume_img)
    composite.alpha_composite(weapon_img)

    proof_comp = f"{FAWN_PD_DIR}/proof_paperdoll_fawn_composite.png"
    composite.save(proof_comp)

    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{FAWN_PD_DIR}/proof_paperdoll_fawn_magenta.png"
    magenta_bg.save(proof_mag)

    strip_w = W * 7 + 8 * 8
    strip_h = H + 24
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["Key", "Curio", "Chassis", "Head", "Optic", "Costume", "Weapon"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, core_img, costume_img, weapon_img]

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        sd.rectangle([px, py, px + W, py + H], fill=(42, 36, 62, 255), outline=OUTLINE)
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 2), name, fill=(255, 208, 40, 255))

    strip_path = f"{FAWN_PD_DIR}/proof_fawn_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")


if __name__ == "__main__":
    build_all()
