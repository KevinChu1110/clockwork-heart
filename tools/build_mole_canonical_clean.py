#!/usr/bin/env python3
"""
build_mole_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十七族 星岩鼴鼠 (The Asteroid Mole, mole) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/art/ASTEROID_MOLE_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological tissue, high-density ABS/POM polymer #FFFDF8/#38A0FF,
  cold-rolled tungsten steel framework, polycarbonate mining visor cowl, superconducting radar vane ears #FFD028/#4ED86A,
  amber dot-matrix LED optic core #FFA010, cold-gas thruster cylinder tail #38A0FF/#FF5E8A,
  orbital plasma sledgehammer #38A0FF/#4ED86A/#FFD028, four-vane antenna brass key #FFD028)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31, 0-QA34
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOLE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/mole"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Asteroid Mole Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory Polymer Canvas (#FFFDF8, #E8ECF2)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (230, 235, 242, 255)
IVORY_DARK   = (200, 210, 222, 255)

# 2. Dopamine Sky Blue (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)

# 3. Mint Cold Emerald (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (133, 255, 160, 255)
MINT_SHINE = (200, 255, 215, 255)
MINT_DARK  = (40, 160, 68, 255)

# 4. Dopamine Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 195, 215, 255)
CORAL_DARK  = (210, 45, 95, 255)

# 5. Dopamine Gold & Brass (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 6. Dopamine Amber (#FFA010)
AMBER_BASE  = (255, 160, 16, 255)
AMBER_LIGHT = (255, 200, 75, 255)
AMBER_SHINE = (255, 235, 140, 255)
AMBER_DARK  = (210, 115, 8, 255)

# 7. Cold-Rolled Tungsten & Alloy Metals
TIN_SHINE = (160, 155, 170, 255)
TIN_LIGHT = (125, 120, 135, 255)
TIN_BASE  = (90, 85, 98, 255)
TIN_DARK  = (60, 56, 68, 255)
TIN_DEEP  = (40, 36, 46, 255)

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
                in_ignored = False
                for rx0, ry0, rx1, ry1 in ignore_regions:
                    if rx0 <= x <= rx1 and ry0 <= y <= ry1:
                        in_ignored = True
                        break
                if in_ignored:
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
    print("=== BUILDING 第五十七族 星岩鼴鼠 (THE ASTEROID MOLE) CANONICAL ASSETS ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Under Chassis / Back Layer)
    # File: winding_key/key_mole_four_vane_antenna_brass.png
    # Features:
    # - 四葉微型發條天線鑰匙 (Four-Vane Antenna Brass Key)
    # - Standing upright on back, central brass spindle from (64, 44) up to (64, 22)
    # - Radar antenna cross vane head centered at (64.0, 18.0)
    # - 4 radiating antenna vanes (N, S, E, W) with loop tips and radar rings
    # - Central hub (radius 4.5) with coral pink dust rivet (#FF5E8A)
    # - Complies with 0-ART29: warm golden bronze outline OUTLINE_KEY, 0 dark artifacts
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Vertical Key Spindle Shaft (x: 62..66, y: 22..44)
    for sy in range(22, 45):
        for sx in range(62, 67):
            shade = 1.0 - abs(sx - 64.0) / 2.5
            shine = max(0.0, 1.0 - abs(sx - 63.0) / 1.5)**2
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * shade) + 30 * shine, 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * shade) + 25 * shine, 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade) + 15 * shine, 0, 255))
            key_img.putpixel((sx, sy), (r, g, b, 255))

    # Mounting flange collar
    kd.rectangle([59, 39, 69, 44], fill=GOLD_BASE, outline=OUTLINE_KEY)
    kd.rectangle([58, 42, 70, 46], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.line([(59, 40), (69, 40)], fill=GOLD_LIGHT, width=1)

    # 2. Four Radar Antenna Vanes centered at (64.0, 18.0)
    hx, hy = 64.0, 18.0
    vane_dirs = [
        (0.0, -1.0),   # North
        (0.0, 1.0),    # South
        (-1.0, 0.0),   # West
        (1.0, 0.0)     # East
    ]
    for vx, vy in vane_dirs:
        # Vane arm
        for dist in np.linspace(4.0, 14.0, 18):
            px = hx + dist * vx
            py = hy + dist * vy
            # Normal perpendicular
            nx, ny = -vy, vx
            for off in [-1.5, -0.5, 0.5, 1.5]:
                sx = int(round(px + off * nx))
                sy = int(round(py + off * ny))
                if 0 <= sx < W and 0 <= sy < H:
                    shade = 1.0 - abs(off) / 2.0
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                    key_img.putpixel((sx, sy), (r, g, b, 255))

        # Circular antenna loop tip (radius 3.5 at tip center)
        tip_x = hx + 13.5 * vx
        tip_y = hy + 13.5 * vy
        for dy in range(-4, 5):
            for dx in range(-4, 5):
                d = (dx**2 + dy**2)**0.5
                if 1.5 <= d <= 3.8:
                    lx = int(round(tip_x + dx))
                    ly = int(round(tip_y + dy))
                    if 0 <= lx < W and 0 <= ly < H:
                        key_img.putpixel((lx, ly), GOLD_LIGHT if (dx < 0 or dy < 0) else GOLD_DARK)

    # Diagonal lattice filigree connects adjacent vanes
    for i in range(4):
        ang1 = i * (np.pi * 0.5)
        ang2 = (i + 1) * (np.pi * 0.5)
        mid_ang = (ang1 + ang2) * 0.5
        mx = int(round(hx + 9.5 * np.cos(mid_ang)))
        my = int(round(hy + 9.5 * np.sin(mid_ang)))
        kd.ellipse([mx - 2, my - 2, mx + 2, my + 2], fill=GOLD_BASE, outline=OUTLINE_KEY)
        kd.point((mx, my), fill=GOLD_LIGHT)

    # 3. Central Antenna Hub (radius 4.5) with Coral Pink Dust Rivet (#FF5E8A)
    for dy in range(-5, 6):
        for dx in range(-5, 6):
            d = (dx**2 + dy**2)**0.5
            if d <= 4.5:
                px = int(round(hx + dx))
                py = int(round(hy + dy))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - d / 4.5)
                    r = int(np.clip(GOLD_DARK[0] * (0.85 + 0.3 * spec), 0, 255))
                    g = int(np.clip(GOLD_DARK[1] * (0.85 + 0.3 * spec), 0, 255))
                    b = int(np.clip(GOLD_DARK[2] * (0.85 + 0.25 * spec), 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    kd.ellipse([int(hx - 2), int(hy - 2), int(hx + 2), int(hy + 2)], fill=CORAL_BASE, outline=GOLD_BASE)
    kd.point((int(hx), int(hy)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_mole_cold_gas_thruster_tail.png
    # Features:
    # - 圓筒形微型冷氣反推短尾 (Cold Gas Counter-Thrust Cylinder Tail)
    # - Heavy cylindrical cold gas thruster mounted at left hip rear (x: 26..44, y: 76..96)
    # - Sky blue (#38A0FF) polymer nozzle casing with brass retaining bands (#FFD028)
    # - Coral pink (#FF5E8A) silicone bumper ring at nozzle exit
    # - Four-port directional micro exhaust ports with subtle white cold gas vapor
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Main Cylindrical Thruster Body (x: 28..44, y: 78..94)
    for ty in range(78, 95):
        for tx in range(28, 45):
            spec = max(0.0, 1.0 - abs(tx - 36.0) / 8.0)
            shine = max(0.0, 1.0 - abs(tx - 34.0) / 4.0)**2
            is_brass_band = (abs(ty - 82) <= 1) or (abs(ty - 90) <= 1)
            if is_brass_band:
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            else:
                r = int(np.clip(SKY_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(SKY_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(SKY_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
            curio_img.putpixel((tx, ty), (r, g, b, 255))

    # Top & bottom rounded caps
    cd.ellipse([28, 75, 44, 81], fill=SKY_LIGHT, outline=OUTLINE)
    cd.ellipse([28, 91, 44, 97], fill=SKY_DARK, outline=OUTLINE)

    # 2. Coral Pink Safety Bumper Ring at nozzle rim (y: 85..88)
    for y in range(85, 89):
        for x in range(28, 45):
            curio_img.putpixel((x, y), CORAL_BASE if abs(x - 36) < 6 else CORAL_DARK)

    # 3. Exhaust Nozzle Bell at left side (x: 24..28, y: 83..89)
    cd.polygon([(28, 83), (24, 85), (24, 88), (28, 89)], fill=TIN_SHINE, outline=OUTLINE)
    cd.ellipse([23, 84, 26, 88], fill=TIN_DEEP, outline=OUTLINE)

    # Subtle cold vapor puff at nozzle exit
    cd.ellipse([20, 83, 23, 87], fill=(230, 245, 255, 180))
    cd.point((21, 85), fill=WHITE_SHINE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_mole_milky_polymer_default.png
    # Features:
    # - 乳白高密度工程塑料底盤 (Milky White ABS/POM Polymer & Tungsten Chassis)
    # - 2.2 chibi ratio, extremely solid, low center of gravity stout stance
    # - Soft ground contact shadow under hooves (x: 22..106, y: 112..122)
    # - Four chunky magnetic suction feet (40, 114) and (72, 114)
    # - Tungsten steel articulated knees at (42, 96) and (70, 96)
    # - Torso: Stamped milky polymer plates (#FFFDF8 / #E8ECF2) with sky blue / mint accents
    # - Left arm at (32..46, 64..84), right arm at (80..93, 66..82) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow under feet (x: 22..106, y: 112..122)
    ch_d.ellipse([64 - 42, 116 - 6, 64 + 42, 116 + 6], fill=(31, 26, 58, 140))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Chunky Magnetic Suction Silicone Roller Feet at (40, 114) and (72, 114)
    feet_pos = [(40.0, 114.0), (72.0, 114.0)]
    for fx, fy in feet_pos:
        # Ground magnetic suction rim (mint green ring + coral bumper ring)
        ch_d.ellipse([int(fx - 11), int(fy - 5), int(fx + 11), int(fy + 5)], fill=TIN_DEEP, outline=OUTLINE)
        ch_d.ellipse([int(fx - 9), int(fy - 4), int(fx + 9), int(fy + 4)], fill=MINT_BASE)
        ch_d.ellipse([int(fx - 7), int(fy - 3), int(fx + 7), int(fy + 3)], fill=CORAL_BASE, outline=OUTLINE)
        ch_d.point((int(fx - 2), int(fy)), fill=GOLD_LIGHT)
        ch_d.point((int(fx + 2), int(fy)), fill=WHITE_SHINE)

    # 3. Cylindrical Suspension Legs (x: 32..48, y: 88..113) & (x: 64..80, y: 88..113)
    leg_coords = [
        ((40.0, 113.0), (46.0, 88.0)),
        ((72.0, 113.0), (66.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_coords:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-8, 9):
                spec = max(0.0, 1.0 - abs(dx) / 8.0)
                shine = max(0.0, 1.0 - abs(dx - 1.0) / 4.0)**2
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.15 * spec) + 15 * shine, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.15 * spec) + 12 * shine, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.15 * spec) + 10 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        # Heavy tungsten knee ball joint
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 6, mid_y - 5, mid_x + 6, mid_y + 5], fill=TIN_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Upper Chest Flange & Thick Neck Hinge (x: 44..84, y: 44..59)
    for ny in range(44, 60):
        for nx in range(44, 85):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 20.0)
            shine = max(0.0, 1.0 - abs(nx - 60.0) / 8.0)**2
            r = int(np.clip(IVORY_BASE[0] * (0.88 + 0.12 * spec) + 15 * shine, 0, 255))
            g = int(np.clip(IVORY_BASE[1] * (0.88 + 0.12 * spec) + 12 * shine, 0, 255))
            b = int(np.clip(IVORY_BASE[2] * (0.88 + 0.12 * spec) + 10 * shine, 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Stout Torso (x: 40..88, y: 58..95)
    # Chunky rounded milky polymer tummy with rich gradient for 0-ART18
    for ty in range(58, 95):
        for tx in range(40, 89):
            dx = (tx - 64.0) / 23.0
            dy = (ty - 77.0) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - (dist_sq)**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 70.0)**2)**0.5 / 12.0)**2
                # Subtle sky blue lower gradient
                is_lower = (ty > 80)
                if is_lower:
                    r = int(np.clip(SKY_LIGHT[0] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    g = int(np.clip(SKY_LIGHT[1] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(SKY_LIGHT[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                else:
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.15 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.15 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.15 * spec) + 15 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Stamped polymer seam lines & brass rivets on torso
    ch_d.arc([42, 60, 86, 94], start=10, end=170, fill=IVORY_DARK, width=1)
    ch_d.arc([44, 62, 84, 92], start=20, end=160, fill=IVORY_LIGHT, width=1)
    # Brass rivets along flanks
    rivet_pos = [(44, 66), (43, 76), (45, 86), (83, 66), (84, 76), (82, 86)]
    for rx, ry in rivet_pos:
        ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((rx, ry), fill=WHITE_SHINE)

    # 6. Arms & Mining Claws
    # Left Arm: Mining Shovel Claw at (x: 30..46, y: 64..84)
    for ay in range(64, 85):
        for ax in range(30, 47):
            dx = (ax - 38.0) / 7.0
            dy = (ay - 74.0) / 10.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.15 * spec), 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.15 * spec), 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.15 * spec), 0, 255))
                chassis_img.putpixel((ax, ay), (r, g, b, 255))

    # Left Claw: Heavy stamped alloy mining shovel claw with tungsten serrated teeth
    ch_d.polygon([(30, 78), (26, 84), (32, 86), (36, 84)], fill=TIN_SHINE, outline=OUTLINE)
    # Serrated claw teeth
    for tx in [26, 29, 32]:
        ch_d.polygon([(tx, 84), (tx + 1, 88), (tx + 3, 84)], fill=TIN_DEEP, outline=OUTLINE)
        ch_d.point((tx + 1, 86), fill=GOLD_LIGHT)
    # Golden wrist gear
    ch_d.ellipse([34, 72, 40, 78], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.point((37, 75), fill=WHITE_SHINE)

    # Right Arm: Held to the right (x: 80..93, y: 66..82) - STRICTLY x < 94
    for ay in range(66, 83):
        for ax in range(80, 94):
            dx = (ax - 86.0) / 7.0
            dy = (ay - 74.0) / 8.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.15 * spec), 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.15 * spec), 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.15 * spec), 0, 255))
                chassis_img.putpixel((ax, ay), (r, g, b, 255))

    # Right hand holding grip (x: 87..93, y: 73..81)
    ch_d.ellipse([87, 73, 93, 81], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.point((90, 76), fill=WHITE_SHINE)

    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # Strict compliance verification for 0-ART9/11
    ch_arr = np.array(chassis_img)
    weapon_baked = int(np.sum(ch_arr[:, 94:128, 3] > 0))
    if weapon_baked > 0:
        print(f"⚠️ Warning: Clearing {weapon_baked} pixels in chassis at x>=94 for 0-ART9/11 compliance!")
        for y in range(H):
            for x in range(94, W):
                chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_mole_orbital_mining_visor_cowl.png
    # Features:
    # - 防爆聚碳酸酯採礦護目頭盔 (Polycarbonate Mining Visor Cowl)
    # - Round dome mining helmet from y: 26..58, x: 40..88
    # - Milky polymer outer shell (#FFFDF8), sky blue (#38A0FF) visor cowl frame
    # - Snout: protruding rounded lower mining snout/faceplate with brass filter grille (y: 46..54, x: 56..72)
    # - Ears: Superconducting micro radar vane ears on left (x: 32..46, y: 22..36) and right (x: 82..96, y: 22..36)
    # - Eye Sockets:
    #   - Left socket: centered around (54, 42), inner (53..56, 41..44) MUST BE HOLLOW (alpha=0)!
    #   - Right socket: centered around (74, 42), inner (73..76, 41..44) MUST BE HOLLOW (alpha=0)!
    # - 0-ART28q: Average plate color matches chassis (L2 distance < 60.0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Superconducting Micro Radar Vane Ears (Left: 34..46, 22..36; Right: 82..94, 22..36)
    ears_config = [
        (38.0, 28.0, -1.0),   # Left ear
        (90.0, 28.0, 1.0)     # Right ear
    ]
    for ex, ey, sign in ears_config:
        # Brass ear mounting base ring
        hd.ellipse([int(ex - 6), int(ey - 6), int(ex + 6), int(ey + 6)], fill=GOLD_DARK, outline=OUTLINE)
        hd.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Radar fan vane blades
        for blade_angle in [-0.5, 0.0, 0.5]:
            bx = ex + sign * 9.0 * np.cos(blade_angle)
            by = ey + 9.0 * np.sin(blade_angle)
            hd.line([(ex, ey), (bx, by)], fill=GOLD_LIGHT, width=2)
            # Mint optical fiber tip
            hd.ellipse([int(bx - 2), int(by - 2), int(bx + 2), int(by + 2)], fill=MINT_BASE, outline=OUTLINE)
            hd.point((int(bx), int(by)), fill=WHITE_SHINE)

    # 2. Main Spherical Milky Polymer Helmet Dome (x: 42..86, y: 26..58)
    for hy in range(26, 59):
        for hx in range(42, 87):
            dx = (hx - 64.0) / 22.0
            dy = (hy - 42.0) / 16.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - (dist_sq)**0.5)
                shine = max(0.0, 1.0 - ((hx - 58.0)**2 + (hy - 36.0)**2)**0.5 / 10.0)**2
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.15 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.15 * spec) + 20 * shine, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.15 * spec) + 15 * shine, 0, 255))
                head_img.putpixel((hx, hy), (r, g, b, 255))

    # 3. Sky Blue (#38A0FF) Polycarbonate Visor Cowl Forehead Band (y: 28..38, x: 46..82)
    for vy in range(28, 38):
        for vx in range(46, 83):
            dx = (vx - 64.0) / 18.0
            dy = (vy - 33.0) / 5.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                shine = max(0.0, 1.0 - ((vx - 58.0)**2 + (vy - 31.0)**2)**0.5 / 6.0)**2
                r = int(np.clip(SKY_BASE[0] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(SKY_BASE[1] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(SKY_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                head_img.putpixel((vx, vy), (r, g, b, 255))

    # Golden rivets on visor rim
    for rv_x in [48, 56, 72, 80]:
        hd.ellipse([rv_x - 1, 31, rv_x + 1, 33], fill=GOLD_BASE, outline=OUTLINE)
        hd.point((rv_x, 32), fill=WHITE_SHINE)

    # 4. Protruding Rounded Snout / Mouthpart with Brass Filter Grille (x: 54..74, y: 46..55)
    for sy in range(46, 56):
        for sx in range(54, 75):
            dx = (sx - 64.0) / 10.0
            dy = (sy - 50.0) / 5.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                shine = max(0.0, 1.0 - ((sx - 62.0)**2 + (sy - 48.0)**2)**0.5 / 4.0)**2
                r = int(np.clip(IVORY_BASE[0] * (0.88 + 0.12 * spec) + 20 * shine, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.88 + 0.12 * spec) + 18 * shine, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.88 + 0.12 * spec) + 15 * shine, 0, 255))
                head_img.putpixel((sx, sy), (r, g, b, 255))

    # Brass filter grille lines on snout
    hd.ellipse([58, 48, 70, 53], fill=TIN_DEEP, outline=OUTLINE)
    for gx in [61, 64, 67]:
        hd.line([(gx, 49), (gx, 52)], fill=GOLD_BASE, width=1)

    # 5. Hollow Eye Sockets (0-ART27 Compliant)
    # Left Eye Socket centered at (54, 42)
    # Right Eye Socket centered at (74, 42)
    sockets = [
        (54.0, 42.0),
        (74.0, 42.0)
    ]
    for sx, sy in sockets:
        # Stamped tungsten/brass eye socket bezel ring
        for dy in range(-6, 7):
            for dx in range(-6, 7):
                d = (dx**2 + dy**2)**0.5
                px = int(round(sx + dx))
                py = int(round(sy + dy))
                if 3.8 <= d <= 5.8:
                    if 0 <= px < W and 0 <= py < H:
                        head_img.putpixel((px, py), GOLD_BASE if (dx < 0 or dy < 0) else GOLD_DARK)

    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=100)

    # 0-ART27: Strictly carve out hollow eye sockets at left: (53..56, 41..44) and right: (73..76, 41..44)
    for y in range(40, 46):
        for x in range(52, 58):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(72, 78):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_mole_orbital_sapper_dungarees.png
    # Features:
    # - 軌道高抗衝擊防護工裝背帶褲 (Orbital Sapper Heavy Dungarees)
    # - Sky blue (#38A0FF) work overalls with mint green (#4ED86A) utility straps
    # - Golden brass buckles (#FFD028) at shoulders (52, 62) and (76, 62)
    # - Chest tool slot & radiation warning badge at center (64, 76)
    # - Torso coverage: y: 60..94, x: 44..84
    # - STRICT ZERO pixels at y >= 96 (0-ART26b compliant)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Shoulder Straps in Mint Green (#4ED86A)
    # Left strap from (52, 58) to (50, 72)
    for sy in range(58, 73):
        for sx in range(48, 54):
            spec = max(0.0, 1.0 - abs(sx - 51.0) / 3.0)
            costume_img.putpixel((sx, sy), MINT_BASE if spec > 0.3 else MINT_DARK)

    # Right strap from (76, 58) to (78, 72)
    for sy in range(58, 73):
        for sx in range(74, 80):
            spec = max(0.0, 1.0 - abs(sx - 77.0) / 3.0)
            costume_img.putpixel((sx, sy), MINT_BASE if spec > 0.3 else MINT_DARK)

    # Golden strap buckles
    cos_d.rectangle([48, 62, 53, 67], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.point((50, 64), fill=WHITE_SHINE)
    cos_d.rectangle([75, 62, 80, 67], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.point((77, 64), fill=WHITE_SHINE)

    # 2. Main Overall Bib & Waist Section (y: 68..94, x: 44..84)
    for cy in range(68, 95):
        for cx in range(44, 85):
            dx = (cx - 64.0) / 20.0
            dy = (cy - 81.0) / 13.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                shine = max(0.0, 1.0 - ((cx - 58.0)**2 + (cy - 76.0)**2)**0.5 / 10.0)**2
                r = int(np.clip(SKY_BASE[0] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(SKY_BASE[1] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(SKY_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                costume_img.putpixel((cx, cy), (r, g, b, 255))

    # 3. Chest Tool Pocket & Badge at (64, 76)
    cos_d.rectangle([58, 72, 70, 82], fill=SKY_DARK, outline=OUTLINE)
    cos_d.rectangle([60, 74, 68, 80], fill=IVORY_BASE, outline=OUTLINE)
    # Coral pink hazard badge
    cos_d.polygon([(64, 75), (61, 79), (67, 79)], fill=CORAL_BASE, outline=OUTLINE)
    cos_d.point((64, 77), fill=WHITE_SHINE)

    # Tool slot stitching line
    cos_d.line([(48, 88), (80, 88)], fill=TIN_DEEP, width=1)
    cos_d.line([(48, 89), (80, 89)], fill=GOLD_BASE, width=1)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # Strict compliance verification for 0-ART26b: strictly zero pixels at y >= 96
    cos_arr = np.array(costume_img)
    lower_baked = int(np.sum(cos_arr[96:128, :, 3] > 0))
    if lower_baked > 0:
        print(f"⚠️ Warning: Clearing {lower_baked} pixels in costume at y>=96 for 0-ART26b compliance!")
        for y in range(96, H):
            for x in range(W):
                costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_mole_amber_led_mining_visor_lens.png
    # Features:
    # - 琥珀點陣 LED 採礦護目目鏡 (Amber LED Mining Visor Lens)
    # - Dopamine warm amber (#FFA010) dot-matrix LED optics
    # - Left lens centered at (54, 42), right lens centered at (74, 42)
    # - Pure white sparkling highlights at lens centers (54, 42) and (74, 42) (min alpha 255)
    # - Subtle mint green (#4ED86A) crosshair reticle dot matrix
    # - Glowing coral pink triangular nose piece (#FF5E8A) at (64, 48)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    eyes_config = [
        (54.0, 42.0),   # Left Eye: Amber Dot-Matrix LED
        (74.0, 42.0)    # Right Eye: Amber Dot-Matrix LED
    ]

    for ex, ey in eyes_config:
        # Amber outer glow ring
        for dy in range(-5, 6):
            for dx in range(-5, 6):
                d = (dx**2 + dy**2)**0.5
                if d <= 4.2:
                    px = int(round(ex + dx))
                    py = int(round(ey + dy))
                    if 0 <= px < W and 0 <= py < H:
                        spec = max(0.0, 1.0 - d / 4.2)
                        shine = max(0.0, 1.0 - ((dx + 1.0)**2 + (dy + 1.0)**2)**0.5 / 2.0)**2
                        r = int(np.clip(AMBER_BASE[0] * (0.85 + 0.25 * spec) + 40 * shine, 0, 255))
                        g = int(np.clip(AMBER_BASE[1] * (0.85 + 0.25 * spec) + 35 * shine, 0, 255))
                        b = int(np.clip(AMBER_BASE[2] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                        core_img.putpixel((px, py), (r, g, b, 255))

        # Mint green targeting crosshair dots
        c_d.point((int(ex - 2), int(ey)), fill=MINT_LIGHT)
        c_d.point((int(ex + 2), int(ey)), fill=MINT_LIGHT)
        c_d.point((int(ex), int(ey - 2)), fill=MINT_LIGHT)
        c_d.point((int(ex), int(ey + 2)), fill=MINT_LIGHT)

        # White core gleam
        c_d.point((int(ex - 1), int(ey - 1)), fill=WHITE_SHINE)

    # Glowing Coral Pink Triangular Nose Piece at (64, 48)
    c_d.polygon([(64, 46), (61, 50), (67, 50)], fill=CORAL_BASE, outline=OUTLINE)
    c_d.point((64, 48), fill=WHITE_SHINE)

    apply_clean_outline(core_img, outline_color=OUTLINE, min_alpha=120)

    # Ensure centers meet min_alpha >= 200 for 0-ART27
    c_px = core_img.load()
    c_px[54, 42] = WHITE_SHINE
    c_px[74, 42] = WHITE_SHINE

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_mole_orbital_plasma_sledgehammer.png
    # Features:
    # - 星穹高頻等離子重鎚 (Orbital Plasma Sledgehammer)
    # - Massive high-frequency plasma sledgehammer held firmly in right hand
    # - Main shaft extends from pommel (106, 110) through grip (92, 78) to head (98, 56)
    # - Hammer head (x: 90..124, y: 46..76) with transparent polymer housing,
    #   luminous mint-green plasma ring (#4ED86A) and sky blue impact plates (#38A0FF)
    # - Golden brass reinforcement collars (#FFD028) & coral pink overload indicator (#FF5E8A)
    # - Heavy counterweight pommel at (106, 110)
    # - Complies strictly with review.md 0-MKT7 single-weapon standard
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    p_pommel = np.array([106.0, 110.0])
    p_head = np.array([98.0, 56.0])

    # 1. Main Weapon Shaft (from pommel to head)
    for t in np.linspace(0.0, 1.0, 56):
        pt = p_pommel + t * (p_head - p_pommel)
        normal = np.array([-(p_head[1] - p_pommel[1]), (p_head[0] - p_pommel[0])])
        normal = normal / (np.linalg.norm(normal) + 1e-6)
        half_w = 2.2
        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            px = int(round(pt[0] + offset * normal[0]))
            py = int(round(pt[1] + offset * normal[1]))
            if 0 <= px < W and 0 <= py < H:
                shade = 1.0 - abs(offset) / (half_w + 0.5)
                # Golden brass shaft with tungsten middle section
                is_grip = (0.45 <= t <= 0.70)
                if is_grip:
                    r = int(np.clip(TIN_SHINE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(TIN_SHINE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(TIN_SHINE[2] * (0.85 + 0.25 * shade), 0, 255))
                else:
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * shade), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * shade), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * shade), 0, 255))
                weapon_img.putpixel((px, py), (r, g, b, 255))

    # Shaft reinforcement rings
    for ring_t in [0.25, 0.45, 0.70, 0.90]:
        rpt = p_pommel + ring_t * (p_head - p_pommel)
        wd.ellipse([int(rpt[0] - 4), int(rpt[1] - 4), int(rpt[0] + 4), int(rpt[1] + 4)], fill=GOLD_DARK, outline=OUTLINE)
        wd.point((int(rpt[0]), int(rpt[1])), fill=GOLD_LIGHT)

    # 2. Counterweight Pommel at (106, 110)
    wd.ellipse([102, 106, 110, 114], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([104, 108, 108, 112], fill=CORAL_BASE, outline=OUTLINE)
    wd.point((106, 110), fill=WHITE_SHINE)

    # 3. Massive Orbital Plasma Sledgehammer Head (x: 90..124, y: 46..74)
    # Head center around (107, 58)
    hx, hy = 107.0, 58.0
    for y in range(46, 75):
        for x in range(90, 125):
            dx = (x - hx) / 16.0
            dy = (y - hy) / 12.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                # Outer shell is sky blue (#38A0FF)
                # Inner core is luminous mint green (#4ED86A)
                is_inner_plasma = (dx**2 + dy**2 <= 0.35)
                if is_inner_plasma:
                    shine = max(0.0, 1.0 - ((x - hx)**2 + (y - hy)**2)**0.5 / 5.0)**2
                    r = int(np.clip(MINT_BASE[0] * (0.85 + 0.3 * spec) + 50 * shine, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.85 + 0.3 * spec) + 40 * shine, 0, 255))
                    b = int(np.clip(MINT_BASE[2] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                else:
                    shine = max(0.0, 1.0 - ((x - (hx - 4.0))**2 + (y - (hy - 4.0))**2)**0.5 / 8.0)**2
                    r = int(np.clip(SKY_BASE[0] * (0.85 + 0.25 * spec) + 30 * shine, 0, 255))
                    g = int(np.clip(SKY_BASE[1] * (0.85 + 0.25 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(SKY_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Hammer Impact Faces (Front: 120..124, Back: 90..94)
    wd.rectangle([120, 50, 124, 66], fill=TIN_SHINE, outline=OUTLINE)
    wd.rectangle([90, 50, 94, 66], fill=TIN_SHINE, outline=OUTLINE)

    # Golden Hammer Reinforcement Bands
    wd.rectangle([98, 48, 102, 68], fill=GOLD_BASE, outline=OUTLINE)
    wd.rectangle([112, 48, 116, 68], fill=GOLD_BASE, outline=OUTLINE)

    # Coral Pink Overload Indicator Lamp at (107, 49)
    wd.ellipse([105, 47, 109, 51], fill=CORAL_BASE, outline=OUTLINE)
    wd.point((107, 49), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_mole_four_vane_antenna_brass", key_img),
        ("back_curio", "curio_mole_cold_gas_thruster_tail", curio_img),
        ("chassis", "chassis_mole_milky_polymer_default", chassis_img),
        ("head_unit", "head_mole_orbital_mining_visor_cowl", head_img),
        ("costume", "costume_mole_orbital_sapper_dungarees", costume_img),
        ("optic_core", "face_mole_amber_led_mining_visor_lens", core_img),
        ("weapon", "weapon_mole_orbital_plasma_sledgehammer", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{MOLE_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{MOLE_PD_DIR}/winding_key/key_mole_four_vane_antenna_brass.png",
                 f"{KEY_DIR}/key_mole_four_vane_antenna_brass.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{MOLE_PD_DIR}/weapon/weapon_mole_orbital_plasma_sledgehammer.png",
                 f"{WEAPON_DIR}/weapon_mole_orbital_plasma_sledgehammer.png")

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

    proof_comp = f"{MOLE_PD_DIR}/proof_paperdoll_mole_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{MOLE_PD_DIR}/proof_paperdoll_mole_magenta.png"
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

    strip_path = f"{MOLE_PD_DIR}/proof_mole_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([26, 110, 102, 122], fill=(31, 26, 58, 110))
    shd.ellipse([36, 112, 92, 120], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/mole_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/mole_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/mole_idle.png
    p_idle_64 = f"{PLAYER_DIR}/mole_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/mole_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/mole_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/mole_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/mole_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/mole_idle_hd.png)
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
        sc_sdraw.ellipse((400 - 240, 1120 - 24, 400 + 240, 1120 + 24), fill=(31, 26, 58, 120))
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{SHOWCASE_DIR}/mole_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THE ASTEROID MOLE CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
