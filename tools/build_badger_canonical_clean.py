#!/usr/bin/env python3
"""
build_badger_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十六族 破星蜜獾 (The Starbreaker Honey Badger, badger) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/STARBREAKER_BADGER_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological badger skin/hair, zero flesh, high-density polymer ABS/POM
  space chassis with dorsal ivory ridge plates, flathead ballistic visor, four-vane radar antenna gold key,
  orbital EVA heavy harness, amber LED dot-matrix visor, starbreaker ripper claw, dual cold-gas reaction thrusters)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (Starbreaker Honey Badger canonical colors):
    1. Base: Ivory White / Snow Enamel (#FFFDF8)
    2. Primary: Deep Matte Space Black / Dark Violet-Black (#1F1A3A)
    3. Secondary / Trim & Winding Key: Dopamine Gold (#FFD028)
    4. Accent / Conduits & Plasma: Celestial Sky Blue / Neon Plasma (#38A0FF)
    5. Blush Coral Pink: Miniature Exhaust Relief Ports (#FF5E8A)
    6. Stamped Titanium Steel: Alloy Blades & Ball Joints (#7A8A9E, #5C6A7B)
    7. Dark Outline: Deep Blue-Purple (#1F1A3A)
    8. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
BADGER_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/badger"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Starbreaker Honey Badger Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory White / Snow Enamel (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (235, 228, 218, 255)
IVORY_DARK   = (210, 200, 185, 255)
IVORY_DEEP   = (175, 165, 150, 255)

# 2. Primary: Deep Matte Space Black / Dark Violet-Black (#1F1A3A)
ABS_BASE  = (38, 32, 64, 255)
ABS_LIGHT = (64, 56, 102, 255)
ABS_SHINE = (100, 90, 145, 255)
ABS_DARK  = (24, 20, 42, 255)
ABS_DEEP  = (18, 15, 32, 255)

# 3. Secondary: Dopamine Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Accent / Conduits & Plasma: Celestial Sky Blue / Neon Plasma (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)
SKY_DEEP  = (14, 60, 130, 255)

# 5. Blush Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 6. Mechanical Stamped Steel & Titanium (#7A8A9E)
STEEL_BASE  = (122, 138, 158, 255)
STEEL_LIGHT = (165, 180, 198, 255)
STEEL_SHINE = (210, 222, 235, 255)
STEEL_DARK  = (92, 106, 123, 255)
STEEL_DEEP  = (61, 72, 86, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL STARBREAKER BADGER SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_badger_four_vane_antenna_gold.png
    # Features:
    # - 四葉天線金黃發條鑰匙 (Four-Vane Radar Antenna Gold Winding Key)
    # - Shaft extends from spine socket (64, 56) to central antenna hub at (68, 26)
    # - 4 aerodynamic radar antenna vanes pointing crosswise (up-left, up-right, down-left, down-right)
    # - Center pulse beacon diode with warm amber housing & pulsing cyan emitter
    # - Warm golden bronze outline (OUTLINE_KEY) compliant with 0-ART29 dark limit (< 260px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft from spine socket (64, 56) to antenna hub (68, 26)
    for t in np.linspace(0.0, 1.0, 30):
        sx = 64.0 + (68.0 - 64.0) * t
        sy = 56.0 + (26.0 - 56.0) * t
        for offset in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.2))
            shade = 1.0 - abs(offset) / 2.5
            r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * shade), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * shade), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine socket mount boss at (64, 56)
    kd.ellipse([60, 52, 68, 60], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([62, 54, 66, 58], fill=GOLD_BASE)

    # 2. Four-Vane Radar Antenna Blades radiating from (68, 26)
    # 4 aerodynamic radar vanes: angles at -135, -45, 45, 135 deg (cross layout)
    hub_x, hub_y = 68.0, 26.0
    vane_angles = [-2.356, -0.785, 0.785, 2.356]  # -135°, -45°, 45°, 135° in radians
    vane_len = 16.0

    for ang in vane_angles:
        cos_a = np.cos(ang)
        sin_a = np.sin(ang)
        for t in np.linspace(0.2, 1.0, 25):
            vx = hub_x + cos_a * (vane_len * t)
            vy = hub_y + sin_a * (vane_len * t)
            # Tapered blade width: wider in middle (t=0.6)
            blade_w = 3.5 * (1.0 - abs(t - 0.55) / 0.55) + 1.0
            perp_x = -sin_a
            perp_y = cos_a
            for w_off in np.linspace(-blade_w, blade_w, int(blade_w * 2.5 + 2)):
                px = int(round(vx + perp_x * w_off))
                py = int(round(vy + perp_y * w_off))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - abs(w_off) / (blade_w + 0.1))
                    r = int(np.clip(GOLD_BASE[0] * (0.75 + 0.35 * spec) + 35 * (spec**2), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.75 + 0.35 * spec) + 30 * (spec**2), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.75 + 0.35 * spec) + 40 * (spec**2), 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    # Outer decorative connecting ring / arc for antenna stability
    for deg in range(0, 360, 3):
        rad = np.radians(deg)
        rx = int(round(hub_x + np.cos(rad) * 11.0))
        ry = int(round(hub_y + np.sin(rad) * 11.0))
        if 0 <= rx < W and 0 <= ry < H:
            key_img.putpixel((rx, ry), GOLD_LIGHT)

    # 3. Center Pulse Beacon Hub
    kd.ellipse([int(hub_x - 6), int(hub_y - 6), int(hub_x + 6), int(hub_y + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 4), int(hub_y - 4), int(hub_x + 4), int(hub_y + 4)], fill=GOLD_BASE)
    kd.ellipse([int(hub_x - 2), int(hub_y - 2), int(hub_x + 2), int(hub_y + 2)], fill=SKY_BASE)
    kd.point((int(hub_x), int(hub_y)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_badger_dual_coldgas_reaction_thruster.png
    # Features:
    # - 雙聯冷氣反推推進背包 (Dual Cold-Gas Reaction Thruster Backpack)
    # - Twin high-pressure cylindrical tanks positioned on left & right:
    #   Left tank: (42..52, 38..66)
    #   Right tank: (76..86, 38..66)
    # - Connecting structural bridge at (52..76, 52..58) (leaves center clear for key)
    # - Brass pressure relief valves on top with coral pink seal rings
    # - Bottom directional vector thruster nozzles with glowing cyan exhaust plume
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Central titanium mounting bracket
    cd.rectangle([50, 52, 78, 59], fill=STEEL_DARK, outline=OUTLINE)
    cd.rectangle([52, 53, 76, 57], fill=STEEL_BASE)
    cd.line([(54, 55), (74, 55)], fill=STEEL_LIGHT, width=1)

    tanks = [
        (46.0, 52.0, -1),  # Left tank center x=46, y=52
        (82.0, 52.0, 1)    # Right tank center x=82, y=52
    ]

    for tcx, tcy, side in tanks:
        # Cylinder tank body: x: tcx-6..tcx+6, y: 38..66
        for y in range(38, 67):
            for x in range(int(tcx - 6), int(tcx + 7)):
                dx = (x - tcx) / 6.0
                if abs(dx) <= 1.0:
                    spec = max(0.0, 1.0 - abs(dx))
                    shine = max(0.0, 1.0 - abs(dx - 0.2))**2
                    # Deep space polymer / titanium tank body
                    is_stripe = (y in (44, 45, 59, 60))
                    if is_stripe:
                        # Gold reinforcement ring
                        r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.35 * spec), 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.35 * spec), 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.35 * spec), 0, 255))
                    else:
                        r = int(np.clip(STEEL_BASE[0] * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                        g = int(np.clip(STEEL_BASE[1] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                        b = int(np.clip(STEEL_BASE[2] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    curio_img.putpixel((x, y), (r, g, b, 255))

        # Top pressure valve cap
        cd.ellipse([int(tcx - 5), 35, int(tcx + 5), 40], fill=GOLD_DARK, outline=OUTLINE)
        cd.ellipse([int(tcx - 3), 36, int(tcx + 3), 39], fill=GOLD_BASE)
        # Coral pink seal ring
        cd.line([(int(tcx - 3), 38), (int(tcx + 3), 38)], fill=CORAL_BASE, width=1)
        cd.point((int(tcx), 36), fill=GOLD_LIGHT)

        # Bottom reaction nozzle
        nozzle_top_y = 66
        nozzle_bot_y = 73
        for ny in range(nozzle_top_y, nozzle_bot_y + 1):
            t_n = (ny - nozzle_top_y) / (nozzle_bot_y - nozzle_top_y)
            nw = 4.0 + t_n * 3.5
            for nx in range(int(tcx - nw), int(tcx + nw + 1)):
                spec = max(0.0, 1.0 - abs(nx - tcx) / (nw + 0.1))
                r = int(np.clip(STEEL_DARK[0] * (0.8 + 0.35 * spec), 0, 255))
                g = int(np.clip(STEEL_DARK[1] * (0.8 + 0.35 * spec), 0, 255))
                b = int(np.clip(STEEL_DARK[2] * (0.8 + 0.35 * spec), 0, 255))
                curio_img.putpixel((nx, ny), (r, g, b, 255))

        # Glowing cold-gas cyan exhaust plume below nozzle
        for py in range(74, 82):
            p_prog = (py - 74) / 8.0
            pw = (1.0 - p_prog) * 3.5
            for px in range(int(tcx - pw), int(tcx + pw + 1)):
                fade = (1.0 - p_prog) * (1.0 - abs(px - tcx) / (pw + 0.5))
                alpha = int(np.clip(fade * 220, 0, 255))
                if alpha > 10:
                    curio_img.putpixel((px, py), (SKY_BASE[0], SKY_BASE[1], SKY_BASE[2], alpha))

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_badger_polymer_space_default.png
    # Features:
    # - 高密度聚合物平頭抗衝擊素體 (High-Density Polymer Flathead Chassis)
    # - 2.2 chibi heavy low-center-of-gravity space engineer body
    # - Ground contact shadow at (64, 116)
    # - Dual articulated impact magnetic boots at (44, 113) and (72, 113)
    # - Thick shock-absorbing legs with titanium ball-joint knees at (46, 96) and (70, 96)
    # - Sturdy torso (x: 46..82, y: 58..92) with deep matte space polymer (#1F1A3A),
    #   ivory white dorsal spine ridge panels (#FFFDF8), and transparent observation window
    # - Solid neck collar at (50..78, 44..58) for seamless head seating (zero holes)
    # - Left hand clenched at (40, 78) for zero-G balance
    # - Right upper arm tucked at (82..92, 66..76)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 34, 116 - 6, 64 + 34, 116 + 6], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Articulated Twin Magnetic Boots at (44, 113) and (72, 113)
    boot_pos = [(44.0, 113.0), (72.0, 113.0)]
    for bx, by in boot_pos:
        # Magnetic damping sole plate
        ch_d.ellipse([int(bx - 9), int(by - 3), int(bx + 9), int(by + 3)], fill=ABS_DEEP, outline=OUTLINE)
        # Deep space polymer boot cap with ivory toe cap
        ch_d.ellipse([int(bx - 8), int(by - 3), int(bx + 8), int(by + 2)], fill=ABS_BASE)
        ch_d.ellipse([int(bx - 6), int(by - 2), int(bx + 2), int(by + 1)], fill=IVORY_BASE)
        # Gold magnetic clamping clasp
        ch_d.line([(int(bx - 4), int(by)), (int(bx + 4), int(by))], fill=GOLD_BASE, width=1)
        ch_d.point((int(bx), int(by - 1)), fill=WHITE_SHINE)

    # 3. Thick Articulated Polymer Legs with Titanium Ball Joints
    leg_paths = [
        ((44.0, 112.0), (50.0, 88.0)),
        ((72.0, 112.0), (68.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-6, 7):
                spec = max(0.0, 1.0 - abs(dx) / 6.0)
                shine = max(0.0, 1.0 - abs(dx - 1.5) / 3.0)**2
                r = int(np.clip(ABS_BASE[0] * (0.8 + 0.45 * spec) + 40 * shine, 0, 255))
                g = int(np.clip(ABS_BASE[1] * (0.8 + 0.45 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(ABS_BASE[2] * (0.8 + 0.45 * spec) + 30 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        # Knee titanium ball joint
        ch_d.ellipse([mid_x - 4, mid_y - 3, mid_x + 4, mid_y + 3], fill=STEEL_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=STEEL_LIGHT)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 50..78, y: 44..58)
    for ny in range(44, 59):
        for nx in range(50, 79):
            dx = (nx - 64.0) / 14.0
            dy = (ny - 51.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(ABS_BASE[0] * (0.85 + 0.3 * spec), 0, 255))
                g = int(np.clip(ABS_BASE[1] * (0.85 + 0.3 * spec), 0, 255))
                b = int(np.clip(ABS_BASE[2] * (0.85 + 0.3 * spec), 0, 255))
                chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Heavy Torso (x: 46..82, y: 58..94)
    # Stamped deep space polymer with ivory dorsal plates and observation window
    for ty in range(58, 95):
        for tx in range(46, 83):
            dx = (tx - 64.0) / 18.0
            dy = (ty - 75.0) / 17.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 68.0)**2)**0.5 / 12.0)**2

                # Dorsal / side white plates (ivory badge)
                is_ivory_ridge = (tx <= 52 or tx >= 76) or (ty <= 64 and abs(tx - 64.0) <= 6.0)
                if is_ivory_ridge:
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                else:
                    r = int(np.clip(ABS_BASE[0] * (0.85 + 0.4 * spec) + 45 * shine, 0, 255))
                    g = int(np.clip(ABS_BASE[1] * (0.85 + 0.4 * spec) + 40 * shine, 0, 255))
                    b = int(np.clip(ABS_BASE[2] * (0.85 + 0.4 * spec) + 35 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Center Movement Observation Window at (64, 73)
    # Transparent polycarbonate window with micro gearwork inside
    ch_d.ellipse([58, 67, 70, 79], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.ellipse([59, 68, 69, 78], fill=ABS_DEEP)
    # Visible tiny gears inside
    ch_d.ellipse([61, 70, 67, 76], fill=GOLD_BASE, outline=GOLD_DARK)
    ch_d.point((64, 73), fill=SKY_BASE)
    ch_d.line([(62, 73), (66, 73)], fill=SKY_LIGHT, width=1)
    ch_d.point((64, 71), fill=WHITE_SHINE)

    # 6. Left Arm & Glove Clenched at (40, 78)
    for t in np.linspace(0.0, 1.0, 20):
        ax = 48.0 - t * 8.0
        ay = 64.0 + t * 14.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), ABS_BASE)
    ch_d.ellipse([36, 74, 44, 82], fill=ABS_DARK, outline=OUTLINE)
    ch_d.ellipse([38, 76, 42, 80], fill=IVORY_BASE)

    # 7. Right Upper Arm tucked at (82..92, 66..76) (strictly x < 94)
    for t in np.linspace(0.0, 1.0, 16):
        ax = 80.0 + t * 9.0   # max ax = 89
        ay = 64.0 + t * 8.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px = int(ax + dx)
                py = int(ay + dy)
                if px < 94 and dx**2 + dy**2 <= 9:
                    chassis_img.putpixel((px, py), ABS_BASE)

    # Outline pass
    apply_clean_outline(chassis_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART9/11 enforcement: Zero pixels at x >= 94
    ch_px = chassis_img.load()
    for y in range(H):
        for x in range(94, W):
            ch_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_badger_flathead_ballistic_visor.png
    # Features:
    # - 平頭防暴沖壓護額 (Flathead Ballistic Stamping Visor)
    # - Broad flat-topped fearless badger silhouette (x: 36..92, y: 20..56)
    # - Stamped ivory white polymer ballistic plate (#FFFDF8) with matte space black base
    # - Side circular brass cooling vents / communication earcups at (38..44, 38..44) and (84..90, 38..44)
    # - Cheek miniature coral pink exhaust relief ports at (46, 50) and (82, 50)
    # - Snout plate at x: 54..74, y: 46..56 with matte black nose tip at (64, 52)
    # - STRICT 0-ART27: Eye sockets centered at (54, 42) and (74, 42) must be hollow (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Base Skull Helmet centered at (64, 40)
    # Flattened top (y: 22..28, x: 44..84)
    hcx, hcy = 64.0, 42.0
    for y in range(22, 58):
        for x in range(38, 91):
            dx = (x - hcx) / 24.0
            # Flathead contour: top is squashed flatter
            if y < 34:
                dy = (y - 34.0) / 12.0
            else:
                dy = (y - 34.0) / 22.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 24.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 5))**2 + (y - (hcy - 5))**2)**0.5 / 6.0)**2

                # Characteristic badger marking: ivory spine band and brow plates
                is_center_stripe = (abs(x - hcx) <= 5.0)
                is_side_brow = (y in (28, 29, 30) and 46 <= x <= 82)
                if is_center_stripe or is_side_brow:
                    # Shaded ivory plate with cel shading (min RGB < 230 so no white run artifact)
                    r = int(np.clip(238 * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    g = int(np.clip(230 * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(218 * (0.85 + 0.25 * spec) + 20 * shine, 0, 255))
                else:
                    r = int(np.clip(ABS_BASE[0] * (0.85 + 0.4 * spec) + 40 * shine, 0, 255))
                    g = int(np.clip(ABS_BASE[1] * (0.85 + 0.4 * spec) + 35 * shine, 0, 255))
                    b = int(np.clip(ABS_BASE[2] * (0.85 + 0.4 * spec) + 30 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 2. Stamped Stiffening Brow Ridge across forehead (x: 44..84, y: 31..35)
    # Segmented into 3 plates with panel seams and gold rivets
    for by in range(31, 36):
        for bx in range(44, 85):
            spec = max(0.0, 1.0 - abs(bx - 64.0) / 20.0)
            is_seam = (bx in (57, 71))
            if is_seam:
                head_img.putpixel((bx, by), STEEL_DARK)
            else:
                r = int(np.clip(235 * (0.82 + 0.25 * spec), 0, 245))
                g = int(np.clip(228 * (0.82 + 0.25 * spec), 0, 240))
                b = int(np.clip(215 * (0.82 + 0.25 * spec), 0, 230))
                head_img.putpixel((bx, by), (r, g, b, 255))

    # Gold brow trim line and titanium rivets
    hd.line([(44, 35), (56, 35)], fill=GOLD_BASE, width=1)
    hd.line([(58, 35), (70, 35)], fill=GOLD_BASE, width=1)
    hd.line([(72, 35), (84, 35)], fill=GOLD_BASE, width=1)
    for rx in (48, 54, 64, 74, 80):
        hd.point((rx, 33), fill=GOLD_LIGHT)
        hd.point((rx, 34), fill=GOLD_DARK)

    # 3. Side Communication Earcups / Circular Brass Cooling Vents at (40, 40) and (88, 40)
    for ex in [40, 88]:
        hd.ellipse([ex - 5, 35, ex + 5, 45], fill=GOLD_DARK, outline=OUTLINE)
        hd.ellipse([ex - 3, 37, ex + 3, 43], fill=GOLD_BASE)
        hd.point((ex, 40), fill=GOLD_LIGHT)

    # 4. Lower Snout Plate & Nose Tip (x: 54..74, y: 46..56)
    for sy in range(46, 57):
        for sx in range(54, 75):
            dx = (sx - 64.0) / 10.0
            dy = (sy - 51.0) / 5.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                head_img.putpixel((sx, sy), (r, g, b, 255))

    # Nose tip
    hd.ellipse([62, 50, 66, 54], fill=ABS_DEEP, outline=OUTLINE)
    hd.point((63, 51), fill=ABS_LIGHT)

    # Dual Coral Pink miniature cheek exhaust vents at (46, 50) and (82, 50)
    hd.ellipse([46 - 2, 50 - 2, 46 + 2, 50 + 2], fill=CORAL_BASE, outline=OUTLINE)
    hd.point((46, 50), fill=CORAL_LIGHT)
    hd.ellipse([82 - 2, 50 - 2, 82 + 2, 50 + 2], fill=CORAL_BASE, outline=OUTLINE)
    hd.point((82, 50), fill=CORAL_LIGHT)

    # 5. Hollow Eye Sockets for 0-ART27:
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
    # File: costume/costume_badger_eva_heavy_harness.png
    # Features:
    # - 軌道高抗衝擊防護工裝 (Orbital EVA Heavy Impact Harness)
    # - Double-layered polymer chestplate fitting snugly over torso (x: 46..82, y: 58..92)
    # - Streamlined shoulder pauldrons with gold magnetic clasps at (38..50, 56..66) and (78..90, 56..66)
    # - Neon sky-blue magnetic guide conduits across harness
    # - Center chest gear star exploration emblem
    # - 4 shock-absorbing waist tassets extending down to y: 92
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Breastplate Front Plate (x: 48..80, y: 60..86)
    for y in range(60, 87):
        for x in range(48, 81):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 16.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            # Dual-layer EVA harness plate
            is_accent = (abs(x - 64.0) <= 3.0) or (y in (66, 67, 80, 81))
            if is_accent:
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec), 0, 255))
            else:
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Center Star Explorer Gear Emblem at (64, 72)
    cos_d.ellipse([60, 68, 68, 76], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([62, 70, 66, 74], fill=SKY_BASE)
    cos_d.point((64, 72), fill=WHITE_SHINE)

    # 2. Shoulder Pauldrons
    pauldrons = [
        (44.0, 61.0),  # Left shoulder
        (84.0, 61.0)   # Right shoulder
    ]
    for px, py in pauldrons:
        cos_d.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=ABS_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=IVORY_BASE)
        # Gold magnetic quick-release buckle
        cos_d.line([(int(px - 3), int(py)), (int(px + 3), int(py))], fill=GOLD_BASE, width=1)
        cos_d.point((int(px), int(py - 1)), fill=WHITE_SHINE)

    # 3. Neon Sky-Blue Magnetic Guide Conduits running diagonally across chest
    conduit_paths = [
        ((44.0, 64.0), (60.0, 72.0)),
        ((84.0, 64.0), (68.0, 72.0)),
        ((60.0, 74.0), (52.0, 84.0)),
        ((68.0, 74.0), (76.0, 84.0))
    ]
    for (cx0, cy0), (cx1, cy1) in conduit_paths:
        for t in np.linspace(0.0, 1.0, 15):
            cx = int(round(cx0 + t * (cx1 - cx0)))
            cy = int(round(cy0 + t * (cy1 - cy0)))
            costume_img.putpixel((cx, cy), SKY_LIGHT)

    # 4. Four Segmented Waist Tassets (hanging from y: 86 down to y: 92)
    tasset_x_spans = [(50, 55), (57, 62), (66, 71), (73, 78)]
    for x0, x1 in tasset_x_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=ABS_BASE, outline=OUTLINE)
        cos_d.line([(x0 + 1, 88), (x1 - 1, 88)], fill=GOLD_BASE, width=1)
        cos_d.point((int(0.5 * (x0 + x1)), 90), fill=IVORY_LIGHT)

    apply_clean_outline(costume_img, outline_color=OUTLINE, min_alpha=100)

    # STRICT 0-ART26b enforcement: Zero pixels at y >= 96
    cos_px = costume_img.load()
    for y in range(96, H):
        for x in range(W):
            cos_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_badger_amber_led_matrix_visor.png
    # Features:
    # - 琥珀點陣 LED 護目面罩 (Amber LED Matrix Visor)
    # - Twin dynamic Amber LED dot-matrix reticles centered at (54, 42) and (74, 42)
    # - High-transparency curved cyan quartz visor band
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:\
        # Outer Brass Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Quartz Glass)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    # Amber LED glowing quartz
                    r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Dot-Matrix Aiming Reticle (Cross pattern of bright amber points)
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), GOLD_LIGHT)
        core_img.putpixel((int(ex + 1), int(ey)), GOLD_LIGHT)
        core_img.putpixel((int(ex), int(ey - 1)), GOLD_LIGHT)
        core_img.putpixel((int(ex), int(ey + 1)), GOLD_LIGHT)
        # Miniature sky-blue tracking corner dots
        core_img.putpixel((int(ex - 2), int(ey - 2)), SKY_LIGHT)
        core_img.putpixel((int(ex + 2), int(ey - 2)), SKY_LIGHT)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_badger_starbreaker_ripper_claw.png
    # Features:
    # - 逐星裂空機關爪 (Starbreaker Ripper Claw)
    # - Single-hand claw gauntlet mounted on right wrist/hand (x: 88..124, y: 56..94)
    # - Heavy mechanical gauntlet cuff locking onto wrist at (88..96, 68..76) with neon sky-blue magnetic coils
    # - Rear cold-gas reaction micro-booster nozzle on claw back with glowing cyan exhaust jet
    # - Three curved high-carbon titanium alloy cutting claw blades with titanium-nitride gold sharpened edges
    # - Single-wield compliant (review.md 0-MKT7)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wp_d = ImageDraw.Draw(weapon_img)

    # 1. Wrist Magnetic Gauntlet Cuff (x: 88..98, y: 68..80)
    for y in range(68, 81):
        for x in range(88, 99):
            spec = max(0.0, 1.0 - abs(y - 74.5) / 6.0)
            shine = max(0.0, 1.0 - abs(x - 93.0) / 5.0)**2
            is_coil = (y in (71, 72, 77, 78))
            if is_coil:
                r = int(np.clip(SKY_BASE[0] * (0.8 + 0.35 * spec), 0, 255))
                g = int(np.clip(SKY_BASE[1] * (0.8 + 0.35 * spec), 0, 255))
                b = int(np.clip(SKY_BASE[2] * (0.8 + 0.35 * spec), 0, 255))
            else:
                r = int(np.clip(STEEL_BASE[0] * (0.85 + 0.35 * spec) + 40 * shine, 0, 255))
                g = int(np.clip(STEEL_BASE[1] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(STEEL_BASE[2] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
            weapon_img.putpixel((x, y), (r, g, b, 255))

    # Gold quick-clamp bracket
    wp_d.line([(90, 74), (97, 74)], fill=GOLD_BASE, width=2)
    wp_d.point((93, 74), fill=WHITE_SHINE)

    # 2. Rear Cold-Gas Reaction Booster on claw back (x: 88..96, y: 60..67)
    wp_d.rectangle([90, 62, 96, 67], fill=STEEL_DARK, outline=OUTLINE)
    wp_d.ellipse([91, 60, 95, 63], fill=GOLD_BASE, outline=OUTLINE)
    # Cyan exhaust jet puffing backwards
    for jy in range(55, 61):
        j_prog = (60 - jy) / 6.0
        jw = (1.0 - j_prog) * 2.5
        for jx in range(int(93 - jw), int(93 + jw + 1)):
            fade = (1.0 - j_prog)
            alpha = int(np.clip(fade * 200, 0, 255))
            if alpha > 10:
                weapon_img.putpixel((jx, jy), (SKY_BASE[0], SKY_BASE[1], SKY_BASE[2], alpha))

    # 3. Three Rip-Cutting Alloy Claw Blades
    # Claw base hub at (96..100, 70..82)
    # Blade 1 (Upper Claw): from (98, 70) curving to (118, 64)
    # Blade 2 (Middle Claw): from (100, 75) curving to (122, 75)
    # Blade 3 (Lower Claw): from (98, 80) curving to (118, 88)
    claw_defs = [
        ((98.0, 70.0), (118.0, 64.0), -1.5),
        ((100.0, 75.0), (122.0, 75.0), 0.0),
        ((98.0, 80.0), (118.0, 88.0), 1.5)
    ]

    for (x0, y0), (x1, y1), curvature in claw_defs:
        for t in np.linspace(0.0, 1.0, 35):
            # Curved claw path
            bx = x0 + t * (x1 - x0)
            by = y0 + t * (y1 - y0) + np.sin(t * np.pi) * curvature
            thick = 3.2 * (1.0 - 0.7 * t) + 0.6
            for d in np.linspace(-thick, thick, int(thick * 3.0 + 2)):
                px = int(round(bx))
                py = int(round(by + d))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - abs(d) / (thick + 0.1))
                    shine = max(0.0, 1.0 - abs(d - 0.5) / 1.5)**2
                    # Titanium blade with gold cutting edge on lower edge (d > 0)
                    if d >= 0:
                        r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.35 * spec) + 50 * shine, 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    else:
                        r = int(np.clip(STEEL_BASE[0] * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                        g = int(np.clip(STEEL_BASE[1] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                        b = int(np.clip(STEEL_BASE[2] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                    weapon_img.putpixel((px, py), (r, g, b, 255))

        # Sharp gleaming tips
        tip_x, tip_y = int(round(x1)), int(round(y1 + curvature * 0.2))
        weapon_img.putpixel((tip_x, tip_y), WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=80)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slice_data = [
        ("winding_key", "key_badger_four_vane_antenna_gold", key_img),
        ("back_curio", "curio_badger_dual_coldgas_reaction_thruster", curio_img),
        ("chassis", "chassis_badger_polymer_space_default", chassis_img),
        ("head_unit", "head_badger_flathead_ballistic_visor", head_img),
        ("costume", "costume_badger_eva_heavy_harness", costume_img),
        ("optic_core", "face_badger_amber_led_matrix_visor", core_img),
        ("weapon", "weapon_badger_starbreaker_ripper_claw", weapon_img)
    ]

    for slot, item_id, img_128 in slice_data:
        slot_dir = f"{BADGER_PD_DIR}/{slot}"
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
    key_img.save(f"{KEY_DIR}/key_badger_four_vane_antenna_gold.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_badger_starbreaker_ripper_claw.png")
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

    proof_comp = f"{BADGER_PD_DIR}/proof_paperdoll_badger_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{BADGER_PD_DIR}/proof_paperdoll_badger_magenta.png"
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

    strip_path = f"{BADGER_PD_DIR}/proof_badger_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/badger_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/badger_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/badger_idle.png
    p_idle_64 = f"{PLAYER_DIR}/badger_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/badger_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/badger_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/badger_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/badger_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/badger_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL STARBREAKER BADGER CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
