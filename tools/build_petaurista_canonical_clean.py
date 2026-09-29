#!/usr/bin/env python3
"""
build_petaurista_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十八族 嵐翼鼯鼠 (The Stormwing Petaurista, petaurista) 7 Paperdoll Slices.
Follows:
- docs/design/STORMWING_PETAURISTA_DESIGN_PROPOSAL.md
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/CANON.md (100% zero fur, zero biological tissue, lacquered bamboo wood shell #4ED86A,
  glazed ivory-white porcelain faceplate #FFFDF8, cold-rolled brass hinges #FFD028,
  folding bamboo-lath glider wing flaps #4ED86A/#1F1A3A, dual bamboo-leaf acoustic sonar ears #4ED86A/#FFD028,
  segmented bamboo-weave rudder tail #4ED86A/#FFD028, obsidian quartz goggle lenses #1F1A3A with cinnabar markings #FF5E8A,
  zen octagonal bamboo shuriken #4ED86A/#FFD028/#7A8A9E, three-leaf windchime brass key #FFD028/#FF5E8A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
PETAURISTA_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/petaurista"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Stormwing Petaurista Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base / Ivory Porcelain (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (235, 230, 218, 255)
IVORY_DARK   = (210, 202, 185, 255)
IVORY_DEEP   = (180, 170, 150, 255)

# 2. Primary / Mint Bamboo Green (#4ED86A)
MINT_BASE   = (78, 216, 106, 255)      # #4ED86A Mint Green Enamel
MINT_LIGHT  = (130, 240, 155, 255)     # Highlight
MINT_SHINE  = (190, 255, 205, 255)     # Specular
MINT_DARK   = (42, 160, 68, 255)       # Cel shadow
MINT_DEEP   = (24, 110, 44, 255)       # Deep seam

# 3. Metal / Dopamine Gold & Brass (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Accent / Cinnabar Red & Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 5. Secondary / Celestial Sky Blue (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)
SKY_DEEP  = (14, 60, 130, 255)

# 6. Cold Stamped Steel & Shuriken Alloy (#7A8A9E)
STEEL_BASE  = (122, 138, 158, 255)
STEEL_LIGHT = (165, 180, 198, 255)
STEEL_SHINE = (210, 222, 235, 255)
STEEL_DARK  = (92, 106, 123, 255)
STEEL_DEEP  = (61, 72, 86, 255)

# 7. Dark Ninja Navy Vest & Goggle Rim (#1F1A3A, #2D274A)
NAVY_BASE  = (45, 39, 74, 255)
NAVY_LIGHT = (72, 64, 110, 255)
NAVY_DARK  = (28, 22, 48, 255)

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
            if px_snap[x, y][3] > min_alpha:
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
                    if px_snap[nx, ny][3] >= min_alpha:
                        has_opaque_neighbor = True
                        break

            if has_opaque_neighbor:
                px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING CANONICAL 7 PAPERDOLL SLICES FOR 第五十八族 嵐翼鼯鼠 (petaurista) ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (z=5)
    # 三葉禪韻風鈴黃銅發條鑰匙 (key_petaurista_three_leaf_windchime_brass)
    # Centered at (40, 30), three elegant windchime acoustic blades, coral button
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

    # Three windchime leaves at 0, 120, 240 degrees (with offset angle)
    base_angles = [math.radians(-90), math.radians(30), math.radians(150)]
    for ang in base_angles:
        # Each leaf is a windchime chime vane with central resonant slot
        # Outer tip at r=16
        tip_x = kcx + 17.0 * math.cos(ang)
        tip_y = kcy + 17.0 * math.sin(ang)
        side_l_x = kcx + 11.0 * math.cos(ang - 0.45)
        side_l_y = kcy + 11.0 * math.sin(ang - 0.45)
        side_r_x = kcx + 11.0 * math.cos(ang + 0.45)
        side_r_y = kcy + 11.0 * math.sin(ang + 0.45)

        leaf_poly = [
            (int(kcx), int(kcy)),
            (int(side_l_x), int(side_l_y)),
            (int(tip_x), int(tip_y)),
            (int(side_r_x), int(side_r_y))
        ]
        kd.polygon(leaf_poly, fill=GOLD_BASE, outline=GOLD_DARK)

        # Highlight ridge
        kd.line([(int(kcx), int(kcy)), (int(tip_x), int(tip_y))], fill=GOLD_LIGHT, width=2)
        # Resonant slot circle near tip
        slot_x = kcx + 12.0 * math.cos(ang)
        slot_y = kcy + 12.0 * math.sin(ang)
        kd.ellipse([int(slot_x - 2), int(slot_y - 2), int(slot_x + 2), int(slot_y + 2)], fill=OUTLINE_KEY)
        kd.point((int(slot_x), int(slot_y)), fill=GOLD_SHINE)

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
    # 多節同軸竹編平衡舵短尾 (curio_petaurista_bamboo_weave_rudder_tail)
    # Extends from pelvis at (46, 88) left-upward to (16, 76), flat rudder paddle
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Segmented tail joints: 4 segments linking to an aerodynamic oval rudder vane
    tail_nodes = [
        (48.0, 90.0, 7.0),
        (40.0, 88.0, 6.5),
        (32.0, 84.0, 6.0),
        (24.0, 80.0, 5.5),
        (16.0, 76.0, 5.0)
    ]

    # Draw tail segments
    for i in range(len(tail_nodes) - 1):
        x1, y1, r1 = tail_nodes[i]
        x2, y2, r2 = tail_nodes[i+1]
        cd.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=MINT_DARK, width=int(r1 + r2))
        cd.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=MINT_BASE, width=int(r1 + r2 - 2))
        cd.line([(int(x1), int(y1)), (int(x2), int(y2))], fill=MINT_LIGHT, width=2)
        # Brass coupling ring at joint
        cd.ellipse([int(x1 - 3), int(y1 - 3), int(x1 + 3), int(y1 + 3)], fill=GOLD_BASE, outline=GOLD_DARK)
        cd.point((int(x1), int(y1)), fill=GOLD_SHINE)

    # Rudder paddle at tail tip around (16, 76)
    # Flat horizontal / angled aerodynamic woven bamboo rudder
    rudder_cx, rudder_cy = 16.0, 76.0
    for y in range(64, 88):
        for x in range(6, 26):
            dx = (x - rudder_cx) / 9.0
            dy = (y - rudder_cy) / 10.0
            if dx**2 + dy**2 <= 1.0:
                # Woven bamboo lattice texture
                pattern = (x + y) % 3
                if pattern == 0:
                    c = MINT_LIGHT
                elif pattern == 1:
                    c = MINT_BASE
                else:
                    c = MINT_DARK
                curio_img.putpixel((x, y), c)

    # Rudder rim and brass trim
    cd.ellipse([6, 64, 25, 87], outline=GOLD_BASE, width=1)
    cd.ellipse([7, 65, 24, 86], outline=MINT_DARK, width=1)
    # Stabilizer fin vane tip
    cd.line([(16, 64), (16, 86)], fill=GOLD_LIGHT, width=1)
    cd.line([(8, 76), (24, 76)], fill=GOLD_LIGHT, width=1)
    cd.ellipse([14, 74, 18, 78], fill=GOLD_BASE, outline=OUTLINE)
    cd.point((16, 76), fill=WHITE_SHINE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (z=10)
    # 生漆竹木拼花矮萌底盤 (chassis_petaurista_lacquered_bamboo_default)
    # 2.2 head-body ratio chibi chassis, porcelain chest plate, brass ball joints,
    # feet with rubber pads. STRICT: x >= 94 MUST BE 0 PIXELS (0-ART9/11).
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Main Chassis Body (Seamless Full Coverage): x: 44..84, y: 58..95
    for y in range(58, 96):
        for x in range(44, 84):
            dx = (x - 64.0) / 18.5
            dy = (y - 77.0) / 18.5
            if dx**2 + dy**2 <= 1.0:
                dist = math.sqrt(dx**2 + dy**2)
                # Rich lacquered bamboo shading (0-ART18 multi-tone depth)
                if dist < 0.4:
                    c = MINT_LIGHT
                elif dist < 0.7:
                    c = MINT_BASE
                else:
                    c = MINT_DARK
                chassis_img.putpixel((x, y), c)

    # 2. Glazed Ivory Porcelain Chest/Belly Plate: x: 50..78, y: 62..90
    for y in range(62, 91):
        for x in range(50, 78):
            dx = (x - 64.0) / 12.0
            dy = (y - 76.0) / 13.0
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

    # 4. Legs and Feet:
    # Left leg: thigh at (52, 92), foot at (50, 108)
    chd.ellipse([46, 88, 58, 100], fill=MINT_BASE, outline=MINT_DARK)
    chd.ellipse([49, 91, 55, 97], fill=GOLD_BASE)  # brass knee joint
    # Left foot: short rounded chibi foot with rubber damper sole
    chd.rounded_rectangle([44, 98, 56, 110], radius=4, fill=MINT_BASE, outline=OUTLINE)
    chd.rounded_rectangle([45, 99, 55, 106], radius=3, fill=MINT_LIGHT)
    chd.rectangle([44, 108, 56, 111], fill=NAVY_BASE, outline=OUTLINE)  # sole rubber pad

    # Right leg: thigh at (74, 92), foot at (76, 108)
    chd.ellipse([68, 88, 80, 100], fill=MINT_BASE, outline=MINT_DARK)
    chd.ellipse([71, 91, 77, 97], fill=GOLD_BASE)  # brass knee joint
    # Right foot
    chd.rounded_rectangle([70, 98, 82, 110], radius=4, fill=MINT_BASE, outline=OUTLINE)
    chd.rounded_rectangle([71, 99, 81, 106], radius=3, fill=MINT_LIGHT)
    chd.rectangle([70, 108, 82, 111], fill=NAVY_BASE, outline=OUTLINE)  # sole rubber pad

    # 5. Arms and Paws:
    # Left arm (gliding balance paw): from shoulder (46, 64) outward to (34, 76)
    chd.line([(46, 64), (38, 70), (34, 76)], fill=MINT_DARK, width=6)
    chd.line([(46, 64), (38, 70), (34, 76)], fill=MINT_BASE, width=4)
    chd.line([(46, 64), (38, 70), (34, 76)], fill=MINT_LIGHT, width=2)
    # Left brass elbow ball joint
    chd.ellipse([36, 68, 41, 73], fill=GOLD_BASE, outline=GOLD_DARK)
    # Left paw (poised with claw tips)
    chd.ellipse([30, 73, 37, 80], fill=IVORY_BASE, outline=OUTLINE)
    chd.point((32, 75), fill=WHITE_SHINE)

    # Right arm (dart-holding wrist): from shoulder (78, 64) outward to (88, 72)
    # STRICT 0-ART9/11: DO NOT EXCEED x=92 (x >= 94 must be 0!)
    chd.line([(78, 64), (84, 68), (89, 73)], fill=MINT_DARK, width=6)
    chd.line([(78, 64), (84, 68), (89, 73)], fill=MINT_BASE, width=4)
    chd.line([(78, 64), (84, 68), (89, 73)], fill=MINT_LIGHT, width=2)
    # Right brass elbow ball joint
    chd.ellipse([82, 66, 87, 71], fill=GOLD_BASE, outline=GOLD_DARK)
    # Right wrist & palm grip (stops at x=92)
    chd.ellipse([85, 70, 92, 77], fill=IVORY_BASE, outline=OUTLINE)
    chd.point((88, 72), fill=WHITE_SHINE)

    # Clear any accidental pixels at x >= 94 (0-ART9/11)
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr).copy()

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=80, ignore_regions=[(94, 0, 127, 127)])
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (z=20)
    # 白瓷竹葉耳暗忍面甲兜帽 (head_petaurista_zen_bamboo_ninja_cowl)
    # Glossy ivory porcelain faceplate, bamboo ninja hood, bamboo-leaf sonar ears.
    # STRICT 0-ART27: Eye sockets hollow (alpha = 0) at:
    # Left eye: x: 52..56, y: 40..44
    # Right eye: x: 72..76, y: 40..44
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Bamboo-leaf Sonar Acoustic Ears (behind head cowl):
    # Left Ear: from (46, 26) up-left to (36, 6)
    ear_l_poly = [(46, 28), (42, 20), (35, 6), (42, 12), (48, 24)]
    hd.polygon(ear_l_poly, fill=MINT_BASE, outline=OUTLINE)
    hd.line([(46, 28), (35, 6)], fill=MINT_LIGHT, width=2)
    # Left ear brass base hinge
    hd.ellipse([43, 24, 48, 29], fill=GOLD_BASE, outline=GOLD_DARK)
    hd.point((45, 26), fill=WHITE_SHINE)

    # Right Ear: from (82, 26) up-right to (92, 6)
    ear_r_poly = [(82, 28), (86, 20), (93, 6), (86, 12), (80, 24)]
    hd.polygon(ear_r_poly, fill=MINT_BASE, outline=OUTLINE)
    hd.line([(82, 28), (93, 6)], fill=MINT_LIGHT, width=2)
    # Right ear brass base hinge
    hd.ellipse([80, 24, 85, 29], fill=GOLD_BASE, outline=GOLD_DARK)
    hd.point((82, 26), fill=WHITE_SHINE)

    # 2. Main Head Cowl & Bamboo Ninja Hood: x: 44..84, y: 22..62
    hcx, hcy = 64.0, 42.0
    for y in range(22, 63):
        for x in range(44, 85):
            dx = (x - hcx) / 19.5
            dy = (y - hcy) / 18.5
            if dx**2 + dy**2 <= 1.0:
                dist = math.sqrt(dx**2 + dy**2)
                # Bamboo hood on top & sides (y < 36 or sides)
                is_hood = (y < 35) or (dx**2 > 0.65)
                if is_hood:
                    if dist < 0.6:
                        c = MINT_LIGHT
                    elif dist < 0.85:
                        c = MINT_BASE
                    else:
                        c = MINT_DARK
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

    # Hood forehead bamboo headband & crest
    hd.arc([46, 28, 82, 40], start=180, end=360, fill=NAVY_BASE, width=3)
    hd.arc([47, 29, 81, 39], start=180, end=360, fill=SKY_BASE, width=1)
    # Brass forehead ninja crest emblem
    hd.polygon([(64, 25), (68, 30), (64, 35), (60, 30)], fill=GOLD_BASE, outline=GOLD_DARK)
    hd.point((64, 30), fill=WHITE_SHINE)

    # Bamboo respirator nose slit at (64, 49)
    hd.line([(62, 49), (66, 49)], fill=IVORY_DEEP, width=1)
    hd.point((64, 50), fill=GOLD_DARK)

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
    hd.ellipse([49, 37, 59, 47], outline=NAVY_BASE, width=1)
    hd.ellipse([69, 37, 79, 47], outline=NAVY_BASE, width=1)
    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (z=25)
    # 天元竹林摺疊翼膜暗忍胸甲 (costume_petaurista_folding_glider_wing_harness)
    # Dark navy ninja chest harness, sky blue trim, golden quick-release buckle,
    # dual folding lacquered bamboo glider wing laths at flanks.
    # STRICT 0-ART26b: y >= 96 MUST BE STRICTLY 0 PIXELS!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cosd = ImageDraw.Draw(costume_img)

    # 1. Glider Wing Flaps (Folded along flanks):
    # Left wing flap: from flank (46, 66) extending to (28, 86)
    # 3 folding bamboo laths
    lath_left_1 = [(48, 64), (32, 74), (28, 86), (42, 82), (48, 76)]
    cosd.polygon(lath_left_1, fill=MINT_BASE, outline=OUTLINE)
    cosd.line([(48, 64), (28, 86)], fill=GOLD_BASE, width=2)
    cosd.line([(42, 68), (34, 84)], fill=MINT_LIGHT, width=1)
    # Wing membrane accent
    cosd.polygon([(36, 76), (30, 84), (40, 81)], fill=SKY_BASE)

    # Right wing flap: from flank (80, 66) extending to (92, 84) (keeps x <= 93)
    lath_right_1 = [(80, 64), (92, 74), (91, 84), (82, 82), (78, 76)]
    cosd.polygon(lath_right_1, fill=MINT_BASE, outline=OUTLINE)
    cosd.line([(80, 64), (91, 84)], fill=GOLD_BASE, width=2)
    cosd.line([(84, 68), (88, 82)], fill=MINT_LIGHT, width=1)
    cosd.polygon([(86, 76), (90, 82), (83, 80)], fill=SKY_BASE)

    # Wing folding brass hinges
    cosd.ellipse([44, 68, 49, 73], fill=GOLD_BASE, outline=GOLD_DARK)
    cosd.ellipse([79, 68, 84, 73], fill=GOLD_BASE, outline=GOLD_DARK)

    # 2. Ninja Vest & Harness (Torso overlay): x: 50..78, y: 58..88
    # Dark navy fabric vest with diagonal cut
    for y in range(58, 88):
        for x in range(50, 78):
            dx = (x - 64.0) / 13.0
            dy = (y - 72.0) / 14.0
            if dx**2 + dy**2 <= 1.0:
                # V-neck chest cutout revealing porcelain plate underneath
                is_v_neck = (y < 68) and (abs(x - 64) < (68 - y) * 1.2)
                if not is_v_neck:
                    if y > 80:
                        c = NAVY_DARK
                    elif x < 60:
                        c = NAVY_LIGHT
                    else:
                        c = NAVY_BASE
                    costume_img.putpixel((x, y), c)

    # Sky blue piping along collar and edges
    cosd.line([(55, 58), (64, 69), (73, 58)], fill=SKY_BASE, width=2)
    cosd.line([(56, 59), (64, 70), (72, 59)], fill=SKY_LIGHT, width=1)

    # Golden chest buckle & diagonal strap
    cosd.line([(54, 62), (74, 82)], fill=GOLD_DARK, width=3)
    cosd.line([(54, 62), (74, 82)], fill=GOLD_BASE, width=2)
    cosd.ellipse([62, 70, 68, 76], fill=GOLD_BASE, outline=OUTLINE)
    cosd.ellipse([63, 71, 67, 75], fill=CORAL_BASE)
    cosd.point((64, 72), fill=WHITE_SHINE)

    # Waist sash belt (y: 84..88)
    cosd.rectangle([52, 84, 76, 88], fill=NAVY_BASE, outline=OUTLINE)
    cosd.rectangle([53, 85, 75, 87], fill=SKY_BASE)
    cosd.ellipse([62, 84, 66, 88], fill=GOLD_BASE, outline=GOLD_DARK)

    # STRICT 0-ART26b: Clear all pixels at y >= 96
    cos_arr = np.array(costume_img)
    cos_arr[96:, :, :] = 0
    costume_img = Image.fromarray(cos_arr).copy()

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (z=30)
    # 黑曜石英目鏡硃砂忍者面甲 (face_petaurista_obsidian_goggle_cinnabar_mask)
    # Deep obsidian quartz lenses, cinnabar red eye markings (#FF5E8A),
    # golden bagua compass crosshair reticles (#FFD028 / #4ED86A).
    # Centers: Left eye at (54, 42), Right eye at (74, 42)
    # STRICT 0-ART27: Min alpha >= 200 at (54, 42) and (74, 42).
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cored = ImageDraw.Draw(core_img)

    # Cinnabar Red Ninja Face Markings around eyes
    # Left eye wing markings:
    cored.polygon([(46, 42), (40, 40), (43, 44)], fill=CORAL_BASE)
    cored.polygon([(54, 47), (52, 52), (56, 49)], fill=CORAL_BASE)
    # Right eye wing markings:
    cored.polygon([(82, 42), (88, 40), (85, 44)], fill=CORAL_BASE)
    cored.polygon([(74, 47), (76, 52), (72, 49)], fill=CORAL_BASE)

    # Draw both eyes
    for cx in [54, 74]:
        cy = 42
        # Outer lens rim
        cored.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=NAVY_DARK, outline=OUTLINE)
        # Deep obsidian lens fill
        for y in range(cy - 4, cy + 5):
            for x in range(cx - 4, cx + 5):
                dx = (x - cx) / 4.0
                dy = (y - cy) / 4.0
                if dx**2 + dy**2 <= 1.0:
                    dist = math.sqrt(dx**2 + dy**2)
                    if dist < 0.3:
                        c = MINT_LIGHT  # Glowing green compass reticle center
                    elif dist < 0.65:
                        c = SKY_BASE    # Cyan quartz mid-tone
                    elif dist < 0.85:
                        c = NAVY_BASE   # Obsidian deep shade
                    else:
                        c = NAVY_DARK   # Rim shade
                    core_img.putpixel((x, y), c)

        # Golden compass reticle lines
        cored.line([(cx - 3, cy), (cx + 3, cy)], fill=GOLD_BASE, width=1)
        cored.line([(cx, cy - 3), (cx, cy + 3)], fill=GOLD_BASE, width=1)
        cored.point((cx, cy), fill=GOLD_SHINE)

        # Specular white eye reflection dot
        cored.ellipse([cx - 2, cy - 3, cx, cy - 1], fill=WHITE_SHINE)
        cored.point((cx + 2, cy + 2), fill=SKY_LIGHT)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (z=40)
    # 竹影八卦旋刃機關鏢 (weapon_petaurista_zen_octagonal_bamboo_dart)
    # Single-held shuriken at right hand (0-MKT7).
    # Center at (104, 68), diameter ~32px.
    # 8-point cold-stamped steel arc blades with bamboo core (#4ED86A),
    # center brass ball bearing (#FFD028) and acoustic tuning fork hole.
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    wcx, wcy = 104.0, 68.0

    # 8-point Octagonal Shuriken Blades
    num_blades = 8
    outer_r = 16.0
    inner_r = 8.0

    blade_pts = []
    for i in range(num_blades * 2):
        ang = math.radians(i * (360.0 / (num_blades * 2)) - 22.5)
        r = outer_r if (i % 2 == 0) else inner_r
        bx = wcx + r * math.cos(ang)
        by = wcy + r * math.sin(ang)
        blade_pts.append((int(bx), int(by)))

    # Base cold steel blade fill
    wd.polygon(blade_pts, fill=STEEL_BASE, outline=OUTLINE)

    # Shading and bevel on each blade tip
    for i in range(num_blades):
        tip_idx = i * 2
        p_tip = blade_pts[tip_idx]
        p_in1 = blade_pts[(tip_idx - 1) % len(blade_pts)]
        p_in2 = blade_pts[(tip_idx + 1) % len(blade_pts)]

        # Highlight half
        wd.polygon([(int(wcx), int(wcy)), p_tip, p_in1], fill=STEEL_LIGHT)
        # Shadow half
        wd.polygon([(int(wcx), int(wcy)), p_tip, p_in2], fill=STEEL_DARK)
        # Ridge line
        wd.line([(int(wcx), int(wcy)), p_tip], fill=STEEL_SHINE, width=1)

    # Lacquered Bamboo Inlay Plate (octagonal green ring at r=6..10)
    for y in range(int(wcy - 10), int(wcy + 11)):
        for x in range(int(wcx - 10), int(wcx + 11)):
            dx = (x - wcx)
            dy = (y - wcy)
            dist = math.sqrt(dx**2 + dy**2)
            if 5.5 <= dist <= 9.5:
                # Bamboo green inlay
                if dist < 7.5:
                    c = MINT_LIGHT
                else:
                    c = MINT_BASE
                weapon_img.putpixel((x, y), c)

    # Center Brass Hub & Ball Bearing (r=5)
    wd.ellipse([int(wcx - 5), int(wcy - 5), int(wcx + 5), int(wcy + 5)], fill=GOLD_DARK, outline=OUTLINE)
    wd.ellipse([int(wcx - 4), int(wcy - 4), int(wcx + 4), int(wcy + 4)], fill=GOLD_BASE)
    wd.ellipse([int(wcx - 2), int(wcy - 2), int(wcx + 2), int(wcy + 2)], fill=CORAL_BASE, outline=OUTLINE)
    wd.point((int(wcx), int(wcy)), fill=WHITE_SHINE)

    # 4 Acoustic Tuning Fork Sound Holes around center at r=7.5
    for h_ang in [0, 90, 180, 270]:
        rad = math.radians(h_ang + 45)
        hx = wcx + 7.5 * math.cos(rad)
        hy = wcy + 7.5 * math.sin(rad)
        wd.ellipse([int(hx - 1), int(hy - 1), int(hx + 1), int(hy + 1)], fill=OUTLINE)
        wd.point((int(hx), int(hy)), fill=GOLD_LIGHT)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slice_data = [
        ("winding_key", "key_petaurista_three_leaf_windchime_brass", key_img),
        ("back_curio", "curio_petaurista_bamboo_weave_rudder_tail", curio_img),
        ("chassis", "chassis_petaurista_lacquered_bamboo_default", chassis_img),
        ("head_unit", "head_petaurista_zen_bamboo_ninja_cowl", head_img),
        ("costume", "costume_petaurista_folding_glider_wing_harness", costume_img),
        ("optic_core", "face_petaurista_obsidian_goggle_cinnabar_mask", core_img),
        ("weapon", "weapon_petaurista_zen_octagonal_bamboo_dart", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{PETAURISTA_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_petaurista_three_leaf_windchime_brass.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_petaurista_zen_octagonal_bamboo_dart.png")
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

    proof_comp = f"{PETAURISTA_PD_DIR}/proof_paperdoll_petaurista_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{PETAURISTA_PD_DIR}/proof_paperdoll_petaurista_magenta.png"
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

    strip_path = f"{PETAURISTA_PD_DIR}/proof_petaurista_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/petaurista_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/petaurista_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/petaurista_idle.png
    p_idle_64 = f"{PLAYER_DIR}/petaurista_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/petaurista_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/petaurista_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/petaurista_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/petaurista_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/petaurista_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THE STORMWING PETAURISTA CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
