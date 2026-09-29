#!/usr/bin/env python3
"""
build_lynx_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十九族 提線猞猁 (The Marionette Lynx, lynx) 7 Paperdoll Slices.
Follows:
- docs/design/MARIONETTE_LYNX_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, polished walnut wood shell #8B5A2B,
  glazed ivory-white porcelain faceplate #FFFDF8, cold-rolled brass hinges #FFD028,
  twin brass wire resonance ear tufts #FFD028/#4ED86A, twin-segment pendulum bobtail #8B5A2B/#FFD028,
  emerald quartz goggle lenses #4ED86A/#38A0FF with warm orange acrobat markings #FFA010,
  dawn marionette five-blade steel claws #7A8A9E/#FFD028, twin-ring chime brass key #FFD028/#FF5E8A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
LYNX_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lynx"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Marionette Lynx Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (145, 115, 30, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (235, 230, 218, 255)
IVORY_DARK   = (210, 202, 185, 255)
IVORY_DEEP   = (180, 170, 150, 255)

# 2. Polished Walnut Wood (#8B5A2B) - Tuned for warm luster and < 60 L2 coherence with head unit
WALNUT_LIGHT = (195, 145, 92, 255)      # Highlight on curved wood
WALNUT_BASE  = (155, 108, 58, 255)       # Core warm walnut brown
WALNUT_SHADOW= (125, 80, 40, 255)        # Cel shadow
WALNUT_DARK  = (88, 52, 24, 255)         # Deep crevice

# 3. Metal / Dopamine Gold & Brass (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Accent / Dopamine Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 80, 255)
ORANGE_SHINE = (255, 225, 145, 255)
ORANGE_DARK  = (205, 115, 8, 255)
ORANGE_DEEP  = (145, 75, 5, 255)

# 5. Mint Bamboo Green Enamel (#4ED86A)
MINT_BASE   = (78, 216, 106, 255)
MINT_LIGHT  = (130, 240, 155, 255)
MINT_SHINE  = (190, 255, 205, 255)
MINT_DARK   = (42, 160, 68, 255)
MINT_DEEP   = (24, 110, 44, 255)

# 6. Secondary / Celestial Sky Blue (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)
SKY_DEEP  = (14, 60, 130, 255)

# 7. Cold Stamped Steel & Tungsten Claw Alloy (#7A8A9E)
STEEL_BASE  = (122, 138, 158, 255)
STEEL_LIGHT = (165, 180, 198, 255)
STEEL_SHINE = (215, 228, 240, 255)
STEEL_DARK  = (88, 102, 120, 255)
STEEL_DEEP  = (58, 68, 82, 255)

# 8. Dark Acrobat Fabric Navy (#1F1A3A, #2D274A)
NAVY_BASE  = (45, 39, 74, 255)
NAVY_LIGHT = (72, 64, 110, 255)
NAVY_DARK  = (28, 22, 48, 255)

# 9. Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_DARK  = (195, 55, 95, 255)

WHITE_SHINE = (255, 255, 255, 255)


def apply_clean_outline(img: Image.Image, outline_color=OUTLINE, min_alpha=80, ignore_regions=None) -> None:
    """Safe, non-recursive, snapshot-based 1px outline pass.
    Prevents flood-fill / propagation bugs that create rectangular black artifact blocks (0-ART29).
    """
    snapshot = img.copy()
    px_snap_data = snapshot.load()
    if px_snap_data is None:
        return

    w, h = img.size
    px_dest = img.load()
    if px_dest is None:
        return

    for y in range(h):
        for x in range(w):
            p = px_snap_data[x, y]  # type: ignore
            if p[3] > min_alpha:
                continue

            if ignore_regions:
                skip = False
                for item in ignore_regions:
                    if len(item) == 4:
                        rx1, ry1, rx2, ry2 = item
                        if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                            skip = True
                            break
                if skip:
                    continue

            # Check 4-connectivity
            has_opaque_neighbor = False
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h:
                    np_px = px_snap_data[nx, ny]  # type: ignore
                    if np_px[3] >= min_alpha:
                        has_opaque_neighbor = True
                        break

            if has_opaque_neighbor:
                px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第五十九族 提線猞猁 (lynx) ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (z=5)
    # 雙環八音風鈴黃銅發條鑰匙 (key_lynx_twin_ring_chime_brass)
    # Centered at (40, 30), dual symmetrical acoustic chime rings, coral center button
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # Stem: from body connection at (46, 50) to key hub at (40, 30)
    stem_pts = [(46, 50), (45, 48), (43, 40), (40, 30)]
    for i in range(len(stem_pts) - 1):
        x1, y1 = stem_pts[i]
        x2, y2 = stem_pts[i+1]
        kd.line([(x1, y1), (x2, y2)], fill=GOLD_DARK, width=6)
        kd.line([(x1, y1), (x2, y2)], fill=GOLD_BASE, width=4)
        kd.line([(x1, y1), (x2, y2)], fill=GOLD_LIGHT, width=2)

    # Key hub center
    kcx, kcy = 40.0, 30.0

    # Twin acoustic windchime rings (left loop and right loop)
    # Left loop: centered at (29, 30), radius ~9
    kd.ellipse([19, 21, 38, 39], fill=GOLD_BASE, outline=GOLD_DARK)
    kd.ellipse([23, 25, 34, 35], fill=(0, 0, 0, 0))  # Hollow ring center
    kd.ellipse([20, 22, 37, 38], outline=GOLD_LIGHT, width=1)
    # Left chime vane fin at top and bottom
    kd.polygon([(26, 21), (28, 15), (32, 21)], fill=GOLD_BASE, outline=GOLD_DARK)
    kd.polygon([(26, 39), (28, 45), (32, 39)], fill=GOLD_BASE, outline=GOLD_DARK)

    # Right loop: centered at (51, 30), radius ~9
    kd.ellipse([42, 21, 61, 39], fill=GOLD_BASE, outline=GOLD_DARK)
    kd.ellipse([46, 25, 57, 35], fill=(0, 0, 0, 0))  # Hollow ring center
    kd.ellipse([43, 22, 60, 38], outline=GOLD_LIGHT, width=1)
    # Right chime vane fin at top and bottom
    kd.polygon([(48, 21), (52, 15), (54, 21)], fill=GOLD_BASE, outline=GOLD_DARK)
    kd.polygon([(48, 39), (52, 45), (54, 39)], fill=GOLD_BASE, outline=GOLD_DARK)

    # Center decorative collar & coral button
    kd.ellipse([int(kcx - 6), int(kcy - 6), int(kcx + 6), int(kcy + 6)], fill=GOLD_DEEP, outline=GOLD_DARK)
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=CORAL_BASE, outline=CORAL_DARK)
    kd.ellipse([int(kcx - 1), int(kcy - 1), int(kcx + 1), int(kcy + 1)], fill=CORAL_LIGHT)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    # Golden filigree outline pass (no dark black block, satisfies 0-ART29)
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=60)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (z=8)
    # 雙節同軸鐘擺平衡配重短尾 (curio_lynx_pendulum_bobtail_balance)
    # Extends from pelvis at (46, 88) left-upward to (22, 80), dual turned walnut segments,
    # brass universal joint, brass spherical pendulum balance weight.
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Node 1: Pelvis anchor at (46, 88)
    # Node 2: First walnut segment joint at (37, 85)
    # Node 3: Second walnut segment joint at (28, 81)
    # Node 4: Brass bobtail pendulum sphere at (20, 78)

    # Draw first turned walnut wood cylinder segment (46, 88) -> (37, 85)
    cd.line([(46, 88), (37, 85)], fill=WALNUT_DARK, width=8)
    cd.line([(46, 88), (37, 85)], fill=WALNUT_BASE, width=6)
    cd.line([(46, 88), (37, 85)], fill=WALNUT_LIGHT, width=2)
    # Brass coupling ring at node 2
    cd.ellipse([34, 82, 40, 88], fill=GOLD_BASE, outline=GOLD_DARK)
    cd.point((37, 85), fill=GOLD_SHINE)

    # Draw second turned walnut wood cylinder segment (37, 85) -> (28, 81)
    cd.line([(37, 85), (28, 81)], fill=WALNUT_DARK, width=7)
    cd.line([(37, 85), (28, 81)], fill=WALNUT_BASE, width=5)
    cd.line([(37, 85), (28, 81)], fill=WALNUT_LIGHT, width=2)
    # Brass universal gimbal joint at node 3
    cd.ellipse([25, 78, 31, 84], fill=GOLD_BASE, outline=GOLD_DARK)
    cd.point((28, 81), fill=GOLD_SHINE)

    # Brass spherical pendulum bobtail weight around (20, 78), diameter ~12px
    pendulum_cx, pendulum_cy = 20.0, 78.0
    for y in range(72, 85):
        for x in range(14, 27):
            dx = (x - pendulum_cx) / 5.5
            dy = (y - pendulum_cy) / 5.5
            if dx**2 + dy**2 <= 1.0:
                dist = math.sqrt(dx**2 + dy**2)
                if dist < 0.35:
                    c = GOLD_SHINE
                elif dist < 0.65:
                    c = GOLD_LIGHT
                elif dist < 0.85:
                    c = GOLD_BASE
                else:
                    c = GOLD_DARK
                curio_img.putpixel((x, y), c)

    # Pendulum decorative equator groove & coral center pin
    cd.ellipse([14, 75, 26, 81], outline=GOLD_DARK, width=1)
    cd.ellipse([18, 76, 22, 80], fill=CORAL_BASE, outline=GOLD_DEEP)
    cd.point((19, 77), fill=WHITE_SHINE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (z=10)
    # 提線木偶精雕胡桃木矮萌底盤 (chassis_lynx_marionette_walnut_default)
    # 2.2 head-body ratio chibi chassis, polished walnut body, ivory porcelain belly,
    # brass ball joints, short agile legs with rubber pads.
    # STRICT: x >= 94 MUST BE 0 PIXELS (0-ART9/11).
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Main Chassis Body (Seamless Full Coverage): x: 44..84, y: 58..95
    for y in range(58, 96):
        for x in range(44, 85):
            dx = (x - 64.0) / 18.5
            dy = (y - 77.0) / 18.5
            if dx**2 + dy**2 <= 1.0:
                dist = math.sqrt(dx**2 + dy**2)
                # Rich polished walnut shading (0-ART18 multi-tone depth)
                if dist < 0.4:
                    c = WALNUT_LIGHT
                elif dist < 0.7:
                    c = WALNUT_BASE
                elif dist < 0.9:
                    c = WALNUT_SHADOW
                else:
                    c = WALNUT_DARK
                chassis_img.putpixel((x, y), c)

    # 2. Glazed Ivory Porcelain Chest/Belly Plate: x: 49..79, y: 61..91
    for y in range(61, 92):
        for x in range(49, 80):
            dx = (x - 64.0) / 13.5
            dy = (y - 76.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                dist = math.sqrt(dx**2 + dy**2)
                # Ivory porcelain glossy cel-shading
                if dist < 0.35:
                    c = IVORY_LIGHT
                elif dist < 0.65:
                    c = IVORY_BASE
                elif dist < 0.85:
                    c = IVORY_SHADOW
                else:
                    c = IVORY_DARK
                chassis_img.putpixel((x, y), c)

    # Seams & brass rivets on porcelain belly
    chd.line([(64, 64), (64, 88)], fill=IVORY_DEEP, width=1)
    for ry in [68, 76, 84]:
        for rx in [56, 72]:
            chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=GOLD_DARK)
            chd.point((rx, ry), fill=WHITE_SHINE)

    # 3. Legs and Feet:
    # Left leg: thigh at (52, 92), foot at (50, 108)
    chd.ellipse([46, 88, 58, 100], fill=WALNUT_BASE, outline=WALNUT_DARK)
    chd.ellipse([49, 91, 55, 97], fill=GOLD_BASE)  # brass knee joint
    # Left foot: short rounded chibi foot with rubber damper sole
    chd.rounded_rectangle([44, 98, 56, 110], radius=4, fill=WALNUT_BASE, outline=OUTLINE)
    chd.rounded_rectangle([45, 99, 55, 106], radius=3, fill=WALNUT_LIGHT)
    chd.rectangle([44, 108, 56, 111], fill=NAVY_BASE, outline=OUTLINE)  # sole rubber pad

    # Right leg: thigh at (74, 92), foot at (76, 108)
    chd.ellipse([68, 88, 80, 100], fill=WALNUT_BASE, outline=WALNUT_DARK)
    chd.ellipse([71, 91, 77, 97], fill=GOLD_BASE)  # brass knee joint
    # Right foot
    chd.rounded_rectangle([70, 98, 82, 110], radius=4, fill=WALNUT_BASE, outline=OUTLINE)
    chd.rounded_rectangle([71, 99, 81, 106], radius=3, fill=WALNUT_LIGHT)
    chd.rectangle([70, 108, 82, 111], fill=NAVY_BASE, outline=OUTLINE)  # sole rubber pad

    # 4. Arms and Paws:
    # Left arm (feline defensive guard paw): from shoulder (46, 64) inward to (36, 74)
    chd.line([(46, 64), (40, 69), (36, 74)], fill=WALNUT_DARK, width=6)
    chd.line([(46, 64), (40, 69), (36, 74)], fill=WALNUT_BASE, width=4)
    chd.line([(46, 64), (40, 69), (36, 74)], fill=WALNUT_LIGHT, width=2)
    # Left brass elbow ball joint
    chd.ellipse([37, 67, 42, 72], fill=GOLD_BASE, outline=GOLD_DARK)
    # Left paw (feline curled paw with ivory plate)
    chd.ellipse([32, 71, 39, 78], fill=IVORY_BASE, outline=OUTLINE)
    chd.point((34, 73), fill=WHITE_SHINE)

    # Right arm (claw-wielding wrist): from shoulder (78, 64) outward to (88, 72)
    # STRICT 0-ART9/11: DO NOT EXCEED x=92 (x >= 94 must be 0!)
    chd.line([(78, 64), (84, 68), (89, 73)], fill=WALNUT_DARK, width=6)
    chd.line([(78, 64), (84, 68), (89, 73)], fill=WALNUT_BASE, width=4)
    chd.line([(78, 64), (84, 68), (89, 73)], fill=WALNUT_LIGHT, width=2)
    # Right brass elbow ball joint
    chd.ellipse([82, 66, 87, 71], fill=GOLD_BASE, outline=GOLD_DARK)
    # Right wrist & palm grip (stops cleanly at x=91)
    chd.ellipse([85, 70, 91, 77], fill=IVORY_BASE, outline=OUTLINE)
    chd.point((88, 72), fill=WHITE_SHINE)

    # Bridge small gaps between limbs and body to ensure 0 holes (0-QA16 Metric 3 / 0-ART29)
    chd.ellipse([81, 70, 85, 74], fill=WALNUT_BASE)
    chd.ellipse([44, 80, 48, 84], fill=WALNUT_BASE)
    chd.ellipse([46, 86, 50, 90], fill=WALNUT_BASE)

    # Clear any accidental pixels at x >= 94 (0-ART9/11)
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr).copy()

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=80, ignore_regions=[(94, 0, 127, 127)])
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (z=20)
    # 白瓷提線雙天線金耳兜帽 (head_lynx_bazaar_marionette_tufted_cowl)
    # Polished walnut head cowl, ivory porcelain faceplate, dual upright brass wire resonance ear tufts.
    # STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
    # Left eye: x: 50..58, y: 38..46
    # Right eye: x: 70..78, y: 38..46
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Dual Upright Brass Wire Resonance Ear Tufts (Lynx signature ears):
    # Left Ear: base at (46, 28), ear tip at (38, 10)
    # Outer carved walnut ear shell
    ear_l_poly = [(48, 28), (43, 20), (37, 10), (43, 14), (49, 25)]
    hd.polygon(ear_l_poly, fill=WALNUT_BASE, outline=OUTLINE)
    hd.line([(48, 28), (37, 10)], fill=WALNUT_LIGHT, width=2)
    # Inner mint enamel lacquer inlay
    hd.polygon([(47, 26), (43, 20), (40, 14), (44, 18), (48, 24)], fill=MINT_BASE)
    # Left brass wire antenna tufts (3 fine resonant brass wires extending up from ear tip)
    hd.line([(37, 10), (35, 3)], fill=GOLD_BASE, width=2)
    hd.line([(38, 11), (38, 4)], fill=GOLD_LIGHT, width=1)
    hd.line([(39, 12), (42, 5)], fill=GOLD_BASE, width=1)
    hd.ellipse([34, 2, 36, 4], fill=GOLD_SHINE)
    hd.ellipse([37, 3, 39, 5], fill=GOLD_SHINE)
    hd.ellipse([41, 4, 43, 6], fill=GOLD_SHINE)
    # Left ear brass base hinge
    hd.ellipse([44, 24, 49, 29], fill=GOLD_BASE, outline=GOLD_DARK)
    hd.point((46, 26), fill=WHITE_SHINE)

    # Right Ear: base at (80, 28), ear tip at (90, 10)
    # Outer carved walnut ear shell
    ear_r_poly = [(80, 28), (85, 20), (91, 10), (85, 14), (79, 25)]
    hd.polygon(ear_r_poly, fill=WALNUT_BASE, outline=OUTLINE)
    hd.line([(80, 28), (91, 10)], fill=WALNUT_LIGHT, width=2)
    # Inner mint enamel lacquer inlay
    hd.polygon([(81, 26), (85, 20), (88, 14), (84, 18), (80, 24)], fill=MINT_BASE)
    # Right brass wire antenna tufts (3 fine resonant brass wires)
    hd.line([(91, 10), (93, 3)], fill=GOLD_BASE, width=2)
    hd.line([(90, 11), (90, 4)], fill=GOLD_LIGHT, width=1)
    hd.line([(89, 12), (86, 5)], fill=GOLD_BASE, width=1)
    hd.ellipse([92, 2, 94, 4], fill=GOLD_SHINE)
    hd.ellipse([89, 3, 91, 5], fill=GOLD_SHINE)
    hd.ellipse([85, 4, 87, 6], fill=GOLD_SHINE)
    # Right ear brass base hinge
    hd.ellipse([79, 24, 84, 29], fill=GOLD_BASE, outline=GOLD_DARK)
    hd.point((81, 26), fill=WHITE_SHINE)

    # 2. Main Head Cowl & Marionette Visor: x: 44..84, y: 22..62
    hcx, hcy = 64.0, 42.0
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            if dx**2 + dy**2 <= 1.0:
                dist = math.sqrt(dx**2 + dy**2)
                # Polished walnut head shell on top, bottom rim & sides
                is_hood = (y < 38) or (y > 55) or (dx**2 > 0.48)
                if is_hood:
                    if dist < 0.6:
                        c = WALNUT_LIGHT
                    elif dist < 0.85:
                        c = WALNUT_BASE
                    else:
                        c = WALNUT_SHADOW
                else:
                    # Ivory porcelain faceplate
                    if dist < 0.5:
                        c = IVORY_LIGHT
                    elif dist < 0.8:
                        c = IVORY_BASE
                    elif dist < 0.95:
                        c = IVORY_SHADOW
                    else:
                        c = IVORY_DARK
                head_img.putpixel((x, y), c)

    # Forehead brass gear & windchime crest emblem
    hd.arc([46, 28, 82, 40], start=180, end=360, fill=ORANGE_BASE, width=3)
    hd.arc([47, 29, 81, 39], start=180, end=360, fill=GOLD_BASE, width=1)
    hd.polygon([(64, 25), (68, 30), (64, 35), (60, 30)], fill=GOLD_BASE, outline=GOLD_DARK)
    hd.ellipse([62, 28, 66, 32], fill=CORAL_BASE, outline=GOLD_DARK)
    hd.point((64, 30), fill=WHITE_SHINE)

    # Feline stylized wooden muzzle line & nose rivet
    hd.line([(61, 49), (67, 49)], fill=IVORY_DEEP, width=1)
    hd.line([(64, 49), (64, 53)], fill=IVORY_DEEP, width=1)
    hd.line([(61, 53), (67, 53)], fill=IVORY_SHADOW, width=1)
    hd.ellipse([62, 47, 66, 50], fill=ORANGE_BASE, outline=GOLD_DARK)  # nose pad
    hd.point((64, 48), fill=WHITE_SHINE)

    # Hollow out eye sockets for optic_core insertion (0-ART27)
    # Left eye socket: x: 50..58, y: 38..46
    # Right eye socket: x: 70..78, y: 38..46
    head_arr = np.array(head_img)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_arr[ey, ex, :] = 0
        for ex in range(70, 79):
            head_arr[ey, ex, :] = 0
    head_img = Image.fromarray(head_arr).copy()

    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=80, ignore_regions=[(49, 37, 59, 47), (69, 37, 79, 47)])

    # Re-enforce zero alpha in hollow eye sockets after outline pass
    hd = ImageDraw.Draw(head_img)
    for ey in range(38, 47):
        for ex in range(50, 59):
            head_img.putpixel((ex, ey), (0, 0, 0, 0))
        for ex in range(70, 79):
            head_img.putpixel((ex, ey), (0, 0, 0, 0))

    # Outer decorative eye socket rims (without invading hollow centers)
    hd.ellipse([49, 37, 59, 47], outline=ORANGE_DARK, width=1)
    hd.ellipse([69, 37, 79, 47], outline=ORANGE_DARK, width=1)
    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (z=25)
    # 晨曦小鎮提線雜技工裝背心 (costume_lynx_marionette_acrobat_vest)
    # Dopamine warm orange acrobat canvas vest, mint green piping, brass pulley buckles,
    # hanging spun beeswax thread tassels.
    # STRICT 0-ART26b: y >= 96 MUST BE STRICTLY 0 PIXELS!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Acrobat Vest & Harness (Torso overlay): x: 50..78, y: 58..88
    # Warm orange fabric vest with acrobatic cut
    for y in range(58, 88):
        for x in range(50, 78):
            dx = (x - 64.0) / 13.0
            dy = (y - 72.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                # V-neck chest cutout revealing porcelain plate underneath
                is_v_neck = (y < 68) and (abs(x - 64) < (68 - y) * 1.2)
                if not is_v_neck:
                    if y > 80:
                        c = ORANGE_DARK
                    elif x < 60:
                        c = ORANGE_LIGHT
                    else:
                        c = ORANGE_BASE
                    costume_img.putpixel((x, y), c)

    # Mint green enamel piping along collar and edges
    cosd.line([(55, 58), (64, 69), (73, 58)], fill=MINT_BASE, width=2)
    cosd.line([(56, 59), (64, 70), (72, 59)], fill=MINT_LIGHT, width=1)

    # Golden marionette pulley buckle & diagonal strap
    cosd.line([(54, 62), (74, 82)], fill=GOLD_DARK, width=3)
    cosd.line([(54, 62), (74, 82)], fill=GOLD_BASE, width=2)
    cosd.ellipse([61, 69, 67, 75], fill=GOLD_BASE, outline=OUTLINE)
    cosd.ellipse([62, 70, 66, 74], fill=MINT_BASE)
    cosd.point((64, 72), fill=WHITE_SHINE)

    # Twin brass buttons on lapels
    cosd.ellipse([54, 66, 58, 70], fill=GOLD_BASE, outline=GOLD_DARK)
    cosd.point((56, 68), fill=WHITE_SHINE)
    cosd.ellipse([70, 66, 74, 70], fill=GOLD_BASE, outline=GOLD_DARK)
    cosd.point((72, 68), fill=WHITE_SHINE)

    # Acrobat waist belt with thread spool pouch (y: 84..88)
    cosd.rectangle([52, 84, 76, 88], fill=NAVY_BASE, outline=OUTLINE)
    cosd.rectangle([53, 85, 75, 87], fill=MINT_BASE)
    cosd.ellipse([62, 84, 66, 88], fill=GOLD_BASE, outline=GOLD_DARK)
    # Small beeswax thread tassels at flanks (stops at y=92)
    cosd.line([(53, 88), (51, 92)], fill=GOLD_LIGHT, width=1)
    cosd.line([(75, 88), (77, 92)], fill=GOLD_LIGHT, width=1)

    # STRICT 0-ART26b: Clear all pixels at y >= 96
    cos_arr = np.array(costume_img)
    cos_arr[96:, :, :] = 0
    costume_img = Image.fromarray(cos_arr).copy()

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (z=30)
    # 雙色翡翠寶石目鏡彩釉面甲 (face_lynx_emerald_quartz_eyemask)
    # Two-tone emerald quartz goggle lenses, warm orange acrobatic mask trim,
    # golden crosshair reticles (#FFD028 / #4ED86A).
    # Centers: Left eye at (54, 42), Right eye at (74, 42)
    # STRICT 0-ART27: Min alpha >= 200 at (54, 42) and (74, 42).
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    # Acrobat Warm Orange Mask Flairs around eyes
    # Left eye wing markings:
    cored.polygon([(46, 42), (39, 40), (43, 44)], fill=ORANGE_BASE)
    cored.polygon([(54, 47), (52, 52), (56, 49)], fill=ORANGE_BASE)
    # Right eye wing markings:
    cored.polygon([(82, 42), (89, 40), (85, 44)], fill=ORANGE_BASE)
    cored.polygon([(74, 47), (76, 52), (72, 49)], fill=ORANGE_BASE)

    # Draw both eyes
    for cx in [54, 74]:
        cy = 42
        # Outer lens rim
        cored.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=ORANGE_DARK, outline=OUTLINE)
        # Deep emerald / sky blue quartz lens fill
        for y in range(cy - 4, cy + 5):
            for x in range(cx - 4, cx + 5):
                dx = (x - cx) / 4.0
                dy = (y - cy) / 4.0
                if dx**2 + dy**2 <= 1.0:
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist < 0.3:
                        c = MINT_SHINE  # Glowing emerald quartz center
                    elif dist < 0.65:
                        c = MINT_BASE   # Emerald green mid-tone
                    elif dist < 0.85:
                        c = SKY_BASE    # Sky blue outer refraction
                    else:
                        c = NAVY_BASE   # Rim shade
                    core_img.putpixel((x, y), c)

        # Golden crosshair reticle lines
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=GOLD_BASE, width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=GOLD_BASE, width=1)
        cored.point((cx, cy), fill=GOLD_SHINE)

        # Specular white eye reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=WHITE_SHINE)
        cored.point((cx + 2, cy + 2), fill=MINT_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (z=40)
    # 晨曦提線裂空機關爪 (weapon_lynx_dawn_marionette_steel_claws)
    # Single-held steel claw at right hand (0-MKT7).
    # Wrist mount at (96, 72), extending 5 cold-rolled tungsten steel curved claws outward.
    # Base carved walnut gauntlet, brass wire pulley hub, razor sharp claw tips.
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # Gauntlet wrist mount: centered at (97, 72), width ~14, height ~16
    wd.rounded_rectangle([92, 65, 103, 79], radius=3, fill=WALNUT_BASE, outline=OUTLINE)
    wd.rounded_rectangle([93, 66, 102, 78], radius=2, fill=WALNUT_LIGHT)
    # Brass pulley ring on gauntlet
    wd.ellipse([94, 68, 100, 74], fill=GOLD_BASE, outline=GOLD_DARK)
    wd.ellipse([95, 69, 99, 73], fill=MINT_BASE)
    wd.point((97, 71), fill=WHITE_SHINE)

    # 5 Stamped Tungsten Steel Arc Claws:
    # Originating from knuckles at x=102..104, spanning y=63..79
    # Claw 1 (Top claw): from (103, 64) curving to (118, 59)
    # Claw 2 (Upper-mid): from (104, 67) curving to (122, 65)
    # Claw 3 (Center claw): from (105, 71) curving to (124, 71)
    # Claw 4 (Lower-mid): from (104, 75) curving to (122, 77)
    # Claw 5 (Bottom claw): from (103, 78) curving to (118, 83)

    claws_def = [
        ((103, 64), (110, 62), (118, 59)),
        ((104, 67), (113, 66), (122, 65)),
        ((105, 71), (114, 71), (124, 71)),
        ((104, 75), (113, 76), (122, 77)),
        ((103, 78), (110, 80), (118, 83)),
    ]

    for p_base, p_mid, p_tip in claws_def:
        # Thick blade spine
        wd.line([p_base, p_mid, p_tip], fill=STEEL_DARK, width=3)
        wd.line([p_base, p_mid, p_tip], fill=STEEL_BASE, width=2)
        wd.line([p_base, p_mid, p_tip], fill=STEEL_LIGHT, width=1)
        # Razor blade tip highlight
        wd.point(p_tip, fill=STEEL_SHINE)
        # Golden brass rivet at blade root
        wd.ellipse([p_base[0] - 2, p_base[1] - 2, p_base[0] + 2, p_base[1] + 2], fill=GOLD_BASE, outline=GOLD_DARK)
        wd.point(p_base, fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slice_data = [
        ("winding_key", "key_lynx_twin_ring_chime_brass", key_img),
        ("back_curio", "curio_lynx_pendulum_bobtail_balance", curio_img),
        ("chassis", "chassis_lynx_marionette_walnut_default", chassis_img),
        ("head_unit", "head_lynx_bazaar_marionette_tufted_cowl", head_img),
        ("costume", "costume_lynx_marionette_acrobat_vest", costume_img),
        ("optic_core", "face_lynx_emerald_quartz_eyemask", core_img),
        ("weapon", "weapon_lynx_dawn_marionette_steel_claws", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{LYNX_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_lynx_twin_ring_chime_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_lynx_dawn_marionette_steel_claws.png")
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

    proof_comp = f"{LYNX_PD_DIR}/proof_paperdoll_lynx_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{LYNX_PD_DIR}/proof_paperdoll_lynx_magenta.png"
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

    strip_path = f"{LYNX_PD_DIR}/proof_lynx_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/lynx_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/lynx_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/lynx_idle.png
    p_idle_64 = f"{PLAYER_DIR}/lynx_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/lynx_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/lynx_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/lynx_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/lynx_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/lynx_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THE MARIONETTE LYNX CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
