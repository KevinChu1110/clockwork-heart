#!/usr/bin/env python3
"""
build_kite_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十二族 熱流赤鳶 (The Thermal Kite, kite) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/THERMAL_KITE_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological feathers, zero bird flesh, copper tinplate,
  stamped raptor cowl & scissor alloy beak, four-leaf turbine heat-relief brass winding key,
  flame-retardant canvas welder cape & vernier caliper belt, amber quartz rangefinder optic core,
  crucible quenched recurve bow, articulated spring-steel cooling flap wings)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Copper Tinplate (#FFA010 / #FFD028) & Sunny Cream Ivory White (#FFFDF8)
    2. Breastplate & Talons: Obsidian Quenched Tungsten Steel (#3A3644)
    3. Industrial Gold Brass: Polished Gilded Brass (#FFD028)
    4. Accent Mint Green: Fresh Mint Green (#4ED86A)
    5. Optic Quartz: Celestial Cyan Quartz (#38A0FF) & Amber Quartz (#FFA010 / #FFD028)
    6. Cute Coral Pink: Coral Pink Damping Pads (#FF5E8A)
    7. Cold Stamped Steel: Steel Gray (#605C6E / #878296)
    8. Dark Outline: Deep Warm Blue-Purple Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KITE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Thermal Kite Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Warm Orange Copper Tinplate (#FFA010)
COPPER_BASE   = (255, 160, 16, 255)
COPPER_LIGHT  = (255, 195, 75, 255)
COPPER_SHINE  = (255, 235, 160, 255)
COPPER_DARK   = (195, 110, 8, 255)
COPPER_DEEP   = (135, 70, 5, 255)

# 2. Breastplate & Mechanical Chassis: Obsidian Tungsten Steel (#3A3644)
OBS_BASE   = (58, 54, 68, 255)
OBS_LIGHT  = (96, 92, 110, 255)
OBS_SHINE  = (135, 130, 150, 255)
OBS_DARK   = (38, 35, 46, 255)
OBS_DEEP   = (26, 24, 32, 255)

# 3. Canvas Cape & Underbelly: Sunny Cream Ivory White (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADOW = (235, 226, 210, 255)
IVORY_DARK   = (210, 198, 178, 255)
IVORY_DEEP   = (180, 168, 148, 255)

# 4. Industrial Gold Brass & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 5. Fresh Mint Green Trim & Sensor (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 6. Coral Pink Damping Pads (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 7. Celestial Cyan Quartz Core & Fluid (#38A0FF)
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
                for (rx1, ry1, rx2, ry2) in ignore_regions:
                    if rx1 <= x <= rx2 and ry1 <= y <= ry2:
                        skip = True
                        break
                if skip:
                    continue

            # If pixel is currently transparent
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
    print("=== BUILDING 100% MODULAR CANONICAL THERMAL KITE SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_kite_turbine_relief_brass.png
    # Features:
    # - 四葉渦輪散熱發條鑰匙 (Four-Leaf Turbine Heat-Relief Brass Key)
    # - Centered at (72, 22), shaft extends down-left to spine socket boss (64, 56)
    # - 4 aerodynamic turbine heat-relief vanes curving gracefully at 0, 90, 180, 270 deg
    # - Central cyan lubricant gem (#38A0FF) at hub (72, 22)
    # - Polished brass gradient (#FFD028, #FFA010, #FFFDF8)
    # - Complies strictly with 0-ART29 dark limit (< 260 px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft from spine socket (64, 56) to turbine hub (72, 24)
    for t in np.linspace(0.0, 1.0, 32):
        sx = 64.0 + (72.0 - 64.0) * t
        sy = 56.0 + (24.0 - 56.0) * t
        for offset in [-2.0, -1.0, 0.0, 1.0, 2.0]:
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.3))
            shade = 1.0 - abs(offset) / 2.5
            r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * shade), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * shade), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine Socket Boss at (61..67, 54..60)
    for y in range(54, 61):
        for x in range(61, 68):
            d = ((x - 64.0)**2 + (y - 57.0)**2)**0.5
            if d <= 3.5:
                key_img.putpixel((x, y), GOLD_LIGHT if d < 1.8 else GOLD_DARK)

    # 2. Four Turbine Vanes around center (72, 22)
    k_cx, k_cy = 72.0, 22.0
    r_hub = 3.6
    r_tip = 12.5

    # Render 4 curved aerodynamic turbine vanes
    for vane_idx in range(4):
        base_angle = vane_idx * (np.pi / 2.0)
        for t in np.linspace(0.0, 1.0, 36):
            # Curved spiral vane path
            ang = base_angle + t * 0.85
            rad = r_hub + t * (r_tip - r_hub)
            vx = k_cx + rad * np.cos(ang)
            vy = k_cy + rad * np.sin(ang)

            vane_w = 1.2 + 2.4 * np.sin(t * np.pi)
            for w_off in np.linspace(-vane_w, vane_w, 9):
                nx = -np.sin(ang) * w_off
                ny = np.cos(ang) * w_off
                px = int(round(vx + nx))
                py = int(round(vy + ny))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - abs(w_off) / (vane_w + 0.1))
                    shine = max(0.0, 1.0 - ((px - 70.0)**2 + (py - 16.0)**2)**0.5 / 6.0)**2
                    r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * spec) + 35 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * spec) + 40 * shine, 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    # Outer Turbine Rim (segmented curved protective cowl)
    for y in range(8, 36):
        for x in range(58, 86):
            d = ((x - k_cx)**2 + (y - k_cy)**2)**0.5
            if abs(d - r_tip) <= 1.2:
                # 4 relief cutouts along outer rim
                ang = np.arctan2(y - k_cy, x - k_cx) % (np.pi / 2.0)
                if 0.15 <= ang <= 1.4:
                    spec = max(0.0, 1.0 - abs(x - 70.0) / 10.0)
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec), 0, 255))
                    key_img.putpixel((x, y), (r, g, b, 255))

    # Central Hub & Cyan Bearing Gem
    for y in range(18, 27):
        for x in range(68, 77):
            d = ((x - k_cx)**2 + (y - k_cy)**2)**0.5
            if d <= r_hub:
                if d <= 1.8:
                    # Cyan jewel core
                    spec = max(0.0, 1.0 - d / 1.8)
                    r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                    g = int(np.clip(CYAN_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                    b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                    key_img.putpixel((x, y), (r, g, b, 255))
                else:
                    key_img.putpixel((x, y), GOLD_SHINE if y < k_cy else GOLD_DARK)

    key_img.putpixel((int(k_cx), int(k_cy - 1)), WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8)
    # File: back_curio/curio_kite_spring_steel_cooling_wings.png
    # Features:
    # - 多節沖壓冷軋彈簧鋼同軸散熱羽翼 (Articulated Spring-Steel Cooling Flap Wings)
    # - Left wing folds back-left (x: 18..52, y: 50..100) with 5 stepped spring-steel louvers
    # - Right wing base folds back-right (x: 74..93, y: 52..90) strictly x < 94!
    # - Twin-fork hinged rudder tail at bottom (x: 56..72, y: 88..106)
    # - Overlapping metallic lamellae with rivet pins and brass hinges (#FFD028)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Twin-Fork Hinged Tail (x: 56..72, y: 88..106)
    # Left tail fork
    tail_pts_left = [(60, 88), (64, 88), (56, 104), (52, 103)]
    cd.polygon(tail_pts_left, fill=OBS_BASE, outline=OUTLINE)
    # Right tail fork
    tail_pts_right = [(64, 88), (68, 88), (76, 103), (72, 104)]
    cd.polygon(tail_pts_right, fill=OBS_BASE, outline=OUTLINE)
    # Central tail hinge pin
    cd.ellipse([62, 86, 66, 90], fill=GOLD_BASE, outline=OUTLINE)
    cd.point((64, 88), fill=GOLD_SHINE)

    # 2. Left Wing Articulated Louvers (5 overlapping spring-steel blades)
    blade_defs_left = [
        # (tip_x, tip_y, base_x, base_y, width)
        (20, 68, 44, 58, 4.2),
        (22, 77, 46, 62, 4.4),
        (26, 85, 48, 67, 4.2),
        (32, 92, 50, 72, 3.8),
        (38, 97, 52, 76, 3.5),
        (46, 98, 54, 80, 3.2),
    ]

    for bx, by, rx, ry, bw in blade_defs_left:
        dx = by - ry
        dy = -(bx - rx)
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            nx = dx / length * bw
            ny = dy / length * bw
            poly = [(rx - nx, ry - ny), (rx + nx, ry + ny), (bx + nx * 0.3, by + ny * 0.3), (bx, by), (bx - nx * 0.3, by - ny * 0.3)]
            cd.polygon(poly, fill=OBS_BASE, outline=OUTLINE)

    # Shading pass over Left Wing to give multi-tone cold steel depth
    for y in range(50, 102):
        for x in range(18, 58):
            p = curio_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 100:
                dist_root = ((x - 50.0)**2 + (y - 70.0)**2)**0.5
                spec = max(0.0, 1.0 - abs(x - 34.0) / 18.0)
                shine = max(0.0, 1.0 - ((x - 30.0)**2 + (y - 78.0)**2)**0.5 / 12.0)**2
                shade = max(0.0, (dist_root - 10.0) / 25.0)

                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine - 15 * shade, 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine - 15 * shade, 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine - 15 * shade, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    for bx, by, rx, ry, bw in blade_defs_left:
        # Central cooling slit with cyan trace
        mid_x = int((rx + bx) / 2)
        mid_y = int((ry + by) / 2)
        cd.line([(rx, ry), (bx, by)], fill=OBS_LIGHT, width=1)
        cd.point((mid_x, mid_y), fill=CYAN_BASE)
        cd.point((int(rx), int(ry)), fill=GOLD_BASE)

    # Left Wing Hinge Arm & Brass Linkage
    cd.line([(44, 58), (54, 76)], fill=GOLD_BASE, width=2)
    cd.line([(45, 59), (55, 77)], fill=GOLD_LIGHT, width=1)
    cd.ellipse([42, 56, 46, 60], fill=GOLD_SHINE, outline=OUTLINE)
    cd.ellipse([52, 74, 56, 78], fill=GOLD_SHINE, outline=OUTLINE)

    # 3. Right Wing Base Blades (strictly x < 94)
    blade_defs_right = [
        (88, 60, 76, 56, 3.6),
        (91, 66, 77, 60, 3.8),
        (92, 73, 78, 65, 3.8),
        (90, 80, 78, 70, 3.6),
        (86, 86, 77, 75, 3.2),
    ]

    for bx, by, rx, ry, bw in blade_defs_right:
        dx = by - ry
        dy = -(bx - rx)
        length = (dx**2 + dy**2)**0.5
        if length > 0:
            nx = dx / length * bw
            ny = dy / length * bw
            poly = [(rx - nx, ry - ny), (rx + nx, ry + ny), (bx + nx * 0.3, by + ny * 0.3), (bx, by), (bx - nx * 0.3, by - ny * 0.3)]
            cd.polygon(poly, fill=OBS_BASE, outline=OUTLINE)

    # Shading pass over Right Wing
    for y in range(54, 90):
        for x in range(74, 94):
            p = curio_img.getpixel((x, y))
            if isinstance(p, (tuple, list)) and p[3] > 100:
                spec = max(0.0, 1.0 - abs(x - 84.0) / 10.0)
                shine = max(0.0, 1.0 - ((x - 86.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

    for bx, by, rx, ry, bw in blade_defs_right:
        cd.line([(rx, ry), (bx, by)], fill=OBS_LIGHT, width=1)
        cd.point((int(rx), int(ry)), fill=GOLD_BASE)

    # Right Wing Pivot Hinge
    cd.line([(76, 56), (82, 72)], fill=GOLD_BASE, width=2)
    cd.ellipse([74, 54, 78, 58], fill=GOLD_SHINE, outline=OUTLINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10)
    # File: chassis/chassis_kite_copper_obsidian_default.png
    # Features:
    # - 2.2 Head-to-Body Q-version mechanical bird automaton chassis
    # - Warm orange-gold copper plated tinplate (#FFA010) with obsidian breastplate (#3A3644)
    # - Bare chassis torso (x: 44..84, y: 56..94) with multi-tone depth (0-ART18: >= 20 colors)
    # - 3-toed tungsten steel grasping claws with coral silicone damper pads at bottom (y: 96..112)
    # - Left wing/arm guarding pose at x: 34..48, y: 64..84
    # - Right arm at x: 80..93, y: 62..82
    # - STRICT 0-ART9/11: weapon zone x >= 94 MUST BE ZERO PIXELS!
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    chd = ImageDraw.Draw(chassis_img)

    # 1. Main Torso Ellipsoid Hull (x: 44..84, y: 56..94)
    cx_t, cy_t = 64.0, 75.0
    rx_t, ry_t = 19.0, 18.0

    # Upper Shoulder / Neck Plate to ensure zero seam gap with head
    for y in range(46, 62):
        for x in range(52, 77):
            if ((x - 64.0)/12.0)**2 + ((y - 54.0)/7.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), COPPER_DARK)

    # Hip / Pelvis Plate connecting torso cleanly to legs (y: 86..96)
    for y in range(86, 96):
        for x in range(48, 81):
            if ((x - 64.0)/15.0)**2 + ((y - 90.0)/6.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), COPPER_DARK)

    for y in range(56, 95):
        for x in range(44, 85):
            dx = (x - cx_t) / rx_t
            dy = (y - cy_t) / ry_t
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 70.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.4) / 0.6)

                # Underbelly vs flank plates
                is_belly = (abs(x - 64.0) <= 9.0 and y >= 64)
                if is_belly:
                    # Ivory cream underbelly panel with warm shading
                    r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                    g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                    b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec) + 25 * shine - 25 * edge_shade, 0, 255))
                else:
                    # Copper tinplate with rich multi-tone shading (0-ART18)
                    r = int(np.clip(COPPER_BASE[0] * (0.75 + 0.4 * spec) + 30 * shine - 30 * edge_shade, 0, 255))
                    g = int(np.clip(COPPER_BASE[1] * (0.75 + 0.4 * spec) + 30 * shine - 30 * edge_shade, 0, 255))
                    b = int(np.clip(COPPER_BASE[2] * (0.75 + 0.4 * spec) + 35 * shine - 30 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r, g, b, 255))

    # 2. Obsidian Quenched Refractory Brick Breastplate (x: 55..73, y: 64..78)
    for y in range(64, 79):
        for x in range(55, 74):
            dx = (x - 64.0) / 9.0
            dy = (y - 71.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 62.0)**2 + (y - 68.0)**2)**0.5 / 7.0)
                shine = max(0.0, 1.0 - ((x - 62.0)**2 + (y - 68.0)**2)**0.5 / 2.5)**2
                r = int(np.clip(OBS_BASE[0] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(OBS_BASE[1] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                b = int(np.clip(OBS_BASE[2] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))

    # 4 Brass Rivets securing the obsidian breastplate
    rivet_pos = [(58, 67), (70, 67), (58, 75), (70, 75)]
    for rx, ry in rivet_pos:
        chd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE)
        chassis_img.putpixel((rx, ry), WHITE_SHINE)

    # 3. Neck Ring & Ball Joint (x: 56..72, y: 46..56)
    for y in range(46, 57):
        for x in range(56, 73):
            if ((x - 64.0)/8.0)**2 + ((y - 51.0)/5.0)**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 62.0) / 7.0)
                r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * spec), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * spec), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((x, y), (r, g, b, 255))

    # 4. Left Arm / Claw (x: 34..48, y: 64..84)
    # Shoulder ball joint
    chd.ellipse([42, 60, 48, 66], fill=GOLD_BASE, outline=OUTLINE)
    # Forearm plate
    arm_poly_l = [(45, 63), (48, 65), (38, 80), (34, 76)]
    chd.polygon(arm_poly_l, fill=COPPER_BASE, outline=OUTLINE)
    # Talon fingers grasping
    chd.ellipse([33, 76, 39, 82], fill=OBS_BASE, outline=OUTLINE)
    chd.point((35, 78), fill=GOLD_SHINE)

    # 5. Right Arm (x: 80..93, y: 62..82) - STRICTLY x <= 93
    chd.ellipse([80, 60, 86, 66], fill=GOLD_BASE, outline=OUTLINE)
    arm_poly_r = [(81, 65), (85, 63), (93, 76), (89, 80)]
    chd.polygon(arm_poly_r, fill=COPPER_BASE, outline=OUTLINE)
    # Hand grip plate
    chd.ellipse([88, 76, 93, 82], fill=OBS_BASE, outline=OUTLINE)
    chd.point((90, 78), fill=GOLD_SHINE)

    # 6. Talons / Claws (3-toed tungsten steel talons at y: 96..112)
    # Left Talon (centered at x=53, y=104)
    tl_pts = [(53, 94), (55, 94), (58, 108), (56, 110), (51, 110), (48, 108)]
    chd.polygon(tl_pts, fill=OBS_BASE, outline=OUTLINE)
    # Toe digits
    chd.polygon([(48, 106), (44, 111), (47, 112)], fill=OBS_LIGHT, outline=OUTLINE)
    chd.polygon([(52, 108), (52, 113), (55, 113)], fill=OBS_LIGHT, outline=OUTLINE)
    chd.polygon([(56, 107), (60, 112), (58, 113)], fill=OBS_LIGHT, outline=OUTLINE)
    # Coral silicone damping pads at ankle
    chd.ellipse([51, 98, 55, 102], fill=CORAL_BASE, outline=OUTLINE)

    # Right Talon (centered at x=75, y=104)
    tr_pts = [(73, 94), (75, 94), (80, 108), (78, 110), (73, 110), (70, 108)]
    chd.polygon(tr_pts, fill=OBS_BASE, outline=OUTLINE)
    # Toe digits
    chd.polygon([(70, 107), (66, 112), (69, 113)], fill=OBS_LIGHT, outline=OUTLINE)
    chd.polygon([(74, 108), (74, 113), (77, 113)], fill=OBS_LIGHT, outline=OUTLINE)
    chd.polygon([(78, 106), (82, 111), (80, 112)], fill=OBS_LIGHT, outline=OUTLINE)
    # Coral silicone damping pads at ankle
    chd.ellipse([73, 98, 77, 102], fill=CORAL_BASE, outline=OUTLINE)

    # STRICT 0-ART9/11 enforcement: zero pixels at x >= 94
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)

    # Re-enforce strictly 0 pixels at x >= 94 after outline pass
    for y in range(H):
        for x in range(94, W):
            chassis_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 50)
    # File: head_unit/head_kite_raptor_cowl_beak.png
    # Features:
    # - 沖壓耐熱赤銅猛禽頭罩與合金剪刀喙 (Stamped Copper Raptor Cowl & Scissor Beak)
    # - Aerodynamic copper cowl covering head (x: 40..88, y: 18..54) in warm orange copper (#FFA010)
    # - Dual dorsal cooling fins extending at top (x: 58..70, y: 12..24) with ventilation slits
    # - Scissor alloy beak (#3A3644 tungsten steel) protruding forward-down at x: 58..70, y: 44..55
    # - Brass acoustic louver grilles at ear positions (x: 42..45, y: 34..42 and x: 83..86, y: 34..42)
    # - Eye socket outer brass bezel rings at (52, 40) and (76, 40)
    # - STRICT 0-ART27: Inner eye socket centers MUST be completely hollow (alpha == 0)
    #   at (39..41, 51..53) and (39..41, 75..77)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Dual Dorsal Cooling Fins (x: 58..70, y: 12..24)
    fin_pts_left = [(60, 24), (58, 14), (63, 13), (64, 24)]
    hd.polygon(fin_pts_left, fill=COPPER_BASE, outline=OUTLINE)
    fin_pts_right = [(64, 24), (65, 13), (70, 14), (68, 24)]
    hd.polygon(fin_pts_right, fill=COPPER_BASE, outline=OUTLINE)
    hd.line([(59, 17), (62, 17)], fill=MINT_BASE, width=1)
    hd.line([(66, 17), (69, 17)], fill=MINT_BASE, width=1)

    # 2. Main Raptor Cowl Dome (x: 40..88, y: 18..54)
    cx_h, cy_h = 64.0, 36.0
    for y in range(18, 54):
        for x in range(40, 89):
            dx = (x - cx_h) / 22.0
            dy = (y - cy_h) / 16.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 30.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r = int(np.clip(COPPER_BASE[0] * (0.8 + 0.45 * spec) + 35 * shine - 20 * edge_shade, 0, 255))
                g = int(np.clip(COPPER_BASE[1] * (0.8 + 0.45 * spec) + 35 * shine - 20 * edge_shade, 0, 255))
                b = int(np.clip(COPPER_BASE[2] * (0.8 + 0.45 * spec) + 40 * shine - 20 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 3. Brow Cooling Slots & Mint Guide Line (y: 28..31, x: 44..84)
    for bx in range(44, 85):
        if ((bx - cx_h)/22.0)**2 + ((29.0 - cy_h)/16.0)**2 <= 0.98:
            head_img.putpixel((bx, 29), GOLD_BASE)
            head_img.putpixel((bx, 30), MINT_BASE)
            if bx % 4 == 0:
                head_img.putpixel((bx, 28), GOLD_LIGHT)

    # 4. Scissor Alloy Beak (Dual cutting blades in tungsten steel, x: 58..70, y: 44..55)
    beak_pts = [(58, 45), (70, 45), (66, 54), (64, 55), (62, 54)]
    hd.polygon(beak_pts, fill=OBS_BASE, outline=OUTLINE)
    # Scissor cutting shear line
    hd.line([(59, 49), (69, 49)], fill=OUTLINE, width=1)
    hd.line([(60, 48), (68, 48)], fill=OBS_LIGHT, width=1)
    # Pivot pin for scissor blades
    hd.ellipse([63, 46, 65, 48], fill=GOLD_BASE)
    hd.point((64, 47), fill=WHITE_SHINE)

    # 5. Dual Brass Acoustic Louver Grilles at Ears
    for ex in [42, 84]:
        for ey in [35, 37, 39, 41]:
            hd.line([(ex, ey), (ex + 2, ey)], fill=GOLD_BASE, width=1)

    # 6. Golden Brass Bezel Rings surrounding Eye Sockets
    for ecx in [52.0, 76.0]:
        for y in range(34, 47):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - 40.0)**2)**0.5
                if 2.5 <= dist <= 5.8:
                    spec = max(0.0, 1.0 - abs(x - (ecx - 1.0)) / 5.0)
                    r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.2 * spec), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.2 * spec), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec), 0, 255))
                    head_img.putpixel((x, y), (r, g, b, 255))

    # 7. STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye socket centers MUST be completely transparent (alpha = 0)
    for y in range(38, 43):
        for x in range(50, 55):
            if ((x - 52.0)**2 + (y - 40.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(74, 79):
            if ((x - 76.0)**2 + (y - 40.0)**2)**0.5 <= 2.2:
                head_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(head_img, ignore_regions=[(48, 36, 56, 44), (72, 36, 80, 44)])

    # Re-enforce 0-ART27 hollow eye socket centers
    for y in range(39, 42):
        for x in range(51, 54):
            head_img.putpixel((x, y), (0, 0, 0, 0))
        for x in range(75, 78):
            head_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 45)
    # File: optic_core/face_kite_amber_quartz_rangefinder.png
    # Features:
    # - 單片橙紅耐火石英測距目鏡 (Amber Quartz Rangefinder Optic Core)
    # - Right eye (76, 40): Amber quartz monocle lens with vernier reticle and crosshairs
    # - Left eye (52, 40): Cute black dot matrix clockwork pupil with reflection highlight
    # - Aligns with 0-ART27: Center pixels at (52, 40) and (76, 40) have alpha > 200
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    crd = ImageDraw.Draw(core_img)

    # 1. Left Eye (52, 40): Clockwork Dot Matrix Pupil
    ecx_l, ecy_l = 52.0, 40.0
    r_core = 5.0
    for y in range(35, 46):
        for x in range(47, 58):
            dist = ((x - ecx_l)**2 + (y - ecy_l)**2)**0.5
            if dist <= r_core:
                spec = max(0.0, 1.0 - ((x - 50.0)**2 + (y - 38.0)**2)**0.5 / 4.0)
                shine = max(0.0, 1.0 - ((x - 50.0)**2 + (y - 38.0)**2)**0.5 / 2.0)**2
                # Deep outline with clockwork cyan sub-glint
                r = int(np.clip(OUTLINE[0] * (0.8 + 0.2 * spec), 0, 255))
                g = int(np.clip(OUTLINE[1] * (0.8 + 0.2 * spec), 0, 255))
                b = int(np.clip(OUTLINE[2] * (0.8 + 0.2 * spec) + 40 * shine, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))
    crd.ellipse([int(ecx_l - r_core), int(ecy_l - r_core), int(ecx_l + r_core), int(ecy_l + r_core)], outline=OUTLINE, width=1)
    core_img.putpixel((51, 39), WHITE_SHINE)
    core_img.putpixel((52, 39), CYAN_SHINE)

    # 2. Right Eye (76, 40): Amber Quartz Rangefinder Lens & Vernier Reticle
    ecx_r, ecy_r = 76.0, 40.0
    r_mono = 5.8
    for y in range(34, 47):
        for x in range(70, 83):
            dist = ((x - ecx_r)**2 + (y - ecy_r)**2)**0.5
            if dist <= r_mono:
                spec = max(0.0, 1.0 - ((x - 74.0)**2 + (y - 38.0)**2)**0.5 / 4.5)
                shine = max(0.0, 1.0 - ((x - 74.0)**2 + (y - 38.0)**2)**0.5 / 2.0)**2
                # Amber quartz glowing gradient
                r = int(np.clip(COPPER_LIGHT[0] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(COPPER_LIGHT[1] * (0.85 + 0.2 * spec) + 20 * shine, 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.2 * spec) + 30 * shine, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))

    # Brass outer ring and vernier bezel
    crd.ellipse([int(ecx_r - r_mono), int(ecy_r - r_mono), int(ecx_r + r_mono), int(ecy_r + r_mono)], outline=GOLD_BASE, width=1)
    crd.ellipse([int(ecx_r - r_mono - 1), int(ecy_r - r_mono - 1), int(ecx_r + r_mono + 1), int(ecy_r + r_mono + 1)], outline=OUTLINE, width=1)

    # Vernier crosshair reticle (Coral/Cyan fine lines)
    crd.line([(int(ecx_r - 3), int(ecy_r)), (int(ecx_r + 3), int(ecy_r))], fill=CORAL_BASE, width=1)
    crd.line([(int(ecx_r), int(ecy_r - 3)), (int(ecx_r), int(ecy_r + 3))], fill=CORAL_BASE, width=1)
    # Rangefinder mounting bracket arm extending to helmet rim
    crd.line([(int(ecx_r + r_mono), int(ecy_r)), (int(ecx_r + r_mono + 3), int(ecy_r - 2))], fill=GOLD_BASE, width=1)

    core_img.putpixel((75, 39), WHITE_SHINE)
    print("  ✓ Slice 5 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: COSTUME (Z: 30)
    # File: costume/costume_kite_welder_cape_belt.png
    # Features:
    # - 阻燃帆布焊接短披風與游標腰帶 (Flame-Retardant Canvas Welder Cape & Vernier Caliper Belt)
    # - Cream Ivory White (#FFFDF8) heavy canvas cape draped over shoulders and chest (x: 42..86, y: 56..88)
    # - Rolled flame-retardant warm orange edge piping (#FFA010)
    # - Slanted chest strap with mint stitch line (#4ED86A)
    # - Vernier caliper belt at waist (x: 46..82, y: 84..94)
    # - Twin-needle brass pressure gauge buckle at center (x: 58..70, y: 85..93)
    # - STRICT 0-ART26b: lower zone y >= 96 MUST BE STRICTLY 0 PIXELS!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ctd = ImageDraw.Draw(costume_img)

    for y in range(56, 92):
        for x in range(42, 87):
            dx = (x - 64.0) / 19.0
            dy = (y - 70.0) / 16.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 66.0)**2)**0.5 / 16.0)
                shine = max(0.0, 1.0 - ((x - 58.0)**2 + (y - 66.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dx**2 + dy**2 - 0.5) / 0.5)

                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec) + 20 * shine - 25 * edge_shade, 0, 255))
                costume_img.putpixel((x, y), (r, g, b, 255))

    # Rolled Warm Orange Flame-Retardant Edge Piping (Outer hem contour)
    for x in range(44, 85):
        y_bot = int(round(70.0 + 16.0 * (max(0.0, 1.0 - ((x - 64.0)/19.0)**2))**0.5))
        if y_bot <= 92:
            costume_img.putpixel((x, y_bot), COPPER_BASE)
            costume_img.putpixel((x, y_bot - 1), COPPER_LIGHT)

    # Slanted chest harness strap (mint stitching)
    ctd.line([(50, 62), (72, 82)], fill=OBS_BASE, width=2)
    ctd.line([(51, 63), (73, 83)], fill=MINT_BASE, width=1)

    # Vernier Caliper Belt across waist (x: 48..80, y: 84..90)
    for y in range(85, 91):
        for x in range(48, 81):
            costume_img.putpixel((x, y), OBS_BASE if y % 2 == 0 else OBS_LIGHT)
    # Vernier measurement ticks
    for vx in range(50, 79, 3):
        costume_img.putpixel((vx, 85), GOLD_BASE)

    # Twin-Needle Brass Pressure Gauge Buckle at center (x: 58..70, y: 85..93)
    ctd.ellipse([58, 85, 70, 93], fill=GOLD_BASE, outline=OUTLINE)
    ctd.ellipse([60, 86, 68, 92], fill=IVORY_BASE)
    # Gauge needles (dual needles pointing at different pressures)
    ctd.line([(64, 89), (62, 87)], fill=OUTLINE, width=1)
    ctd.line([(64, 89), (66, 88)], fill=CORAL_BASE, width=1)
    # Cyan alert tick on gauge rim
    ctd.point((67, 86), fill=CYAN_BASE)

    # STRICT 0-ART26b enforcement: zero pixels at y >= 96
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    apply_clean_outline(costume_img)

    # Re-enforce zero pixels at y >= 96 after outline pass
    for y in range(96, H):
        for x in range(W):
            costume_img.putpixel((x, y), (0, 0, 0, 0))

    print("  ✓ Slice 6 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 60)
    # File: weapon/weapon_kite_crucible_recurve_bow.png
    # Features:
    # - 熱流淬火複合機關弓 (Crucible Quenched Recurve Bow)
    # - Right-hand single held (0-MKT7 compliant)
    # - Obsidian quenched spring-steel recurve limbs arching along right side
    # - Central high-temperature pressure relief valve dial at riser/grip (94, 74)
    # - Upper limb: from (95, 68) up through (102, 48) to tip cam pulley at (108, 26)
    # - Lower limb: from (95, 78) down through (102, 98) to tip cam pulley at (108, 116)
    # - High-tension piano wire string from (108, 26) -> drawn thimble (86, 73) -> (108, 116)
    # - Nocked quenched penetrator arrow pointing across rest
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Grip & Central Riser at (92..98, 68..78)
    for y in range(68, 79):
        for x in range(92, 99):
            spec = max(0.0, 1.0 - abs(x - 95.0) / 3.0)
            r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
            weapon_img.putpixel((x, y), (r, g, b, 255))

    # Central High-Temperature Pressure Relief Valve Dial at (95, 73)
    wd.ellipse([92, 70, 98, 76], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([93, 71, 97, 75], fill=OBS_BASE)
    wd.line([(95, 73), (97, 72)], fill=CYAN_BASE, width=1)
    wd.point((95, 73), fill=WHITE_SHINE)

    # 2. Upper Recurve Limb: from (95, 68) through (102, 48) to (108, 26)
    upper_pts = [
        np.array([95.0, 68.0]),
        np.array([97.0, 56.0]),
        np.array([102.0, 44.0]),
        np.array([108.0, 26.0])
    ]
    for i in range(len(upper_pts) - 1):
        p0, p1 = upper_pts[i], upper_pts[i+1]
        for t in np.linspace(0.0, 1.0, 36):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-1, 2):
                if 0 <= ix + d < W and 0 <= iy < H:
                    weapon_img.putpixel((ix + d, iy), OBS_BASE)
                    weapon_img.putpixel((ix, iy), OBS_LIGHT)

    # 3. Lower Recurve Limb: from (95, 78) through (102, 98) to (108, 116)
    lower_pts = [
        np.array([95.0, 78.0]),
        np.array([97.0, 90.0]),
        np.array([102.0, 102.0]),
        np.array([108.0, 116.0])
    ]
    for i in range(len(lower_pts) - 1):
        p0, p1 = lower_pts[i], lower_pts[i+1]
        for t in np.linspace(0.0, 1.0, 36):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-1, 2):
                if 0 <= ix + d < W and 0 <= iy < H:
                    weapon_img.putpixel((ix + d, iy), OBS_BASE)
                    weapon_img.putpixel((ix, iy), OBS_LIGHT)

    # Limb joints & rivet pins
    for jx, jy in [(98, 50), (105, 34), (98, 96), (105, 108)]:
        wd.ellipse([jx - 1, jy - 1, jx + 1, jy + 1], fill=GOLD_BASE)
        weapon_img.putpixel((jx, jy), GOLD_SHINE)

    # 4. Eccentric Cam Pulleys at Limb Tips: (108, 26) and (108, 116)
    for px, py in [(108, 26), (108, 116)]:
        wd.ellipse([px - 3, py - 3, px + 3, py + 3], fill=GOLD_BASE, outline=OUTLINE)
        wd.ellipse([px - 1, py - 1, px + 1, py + 1], fill=OBS_BASE)
        weapon_img.putpixel((px, py), WHITE_SHINE)

    # 5. High-Tension Piano Wire Bowstring: (108, 26) -> drawn thimble (86, 73) -> (108, 116)
    for t in np.linspace(0.0, 1.0, 50):
        sx1 = int(round(108.0 * (1 - t) + 86.0 * t))
        sy1 = int(round(26.0 * (1 - t) + 73.0 * t))
        if 0 <= sx1 < W and 0 <= sy1 < H:
            weapon_img.putpixel((sx1, sy1), GOLD_LIGHT if t > 0.5 else IVORY_BASE)

        sx2 = int(round(86.0 * (1 - t) + 108.0 * t))
        sy2 = int(round(73.0 * (1 - t) + 116.0 * t))
        if 0 <= sx2 < W and 0 <= sy2 < H:
            weapon_img.putpixel((sx2, sy2), GOLD_LIGHT if t < 0.5 else IVORY_BASE)

    # 6. Drawn String Thimble at (86, 73)
    wd.ellipse([84, 71, 88, 75], fill=GOLD_BASE, outline=OUTLINE)
    weapon_img.putpixel((86, 73), WHITE_SHINE)

    # 7. Nocked Quenched Penetrator Arrow: from (86, 73) through riser (95, 73) to tip (114, 73)
    for ax in range(86, 115):
        spec = 1.0 if ax % 3 == 0 else 0.75
        r = int(np.clip(180 * spec, 0, 255))
        g = int(np.clip(170 * spec, 0, 255))
        b = int(np.clip(190 * spec, 0, 255))
        weapon_img.putpixel((ax, 73), (r, g, b, 255))

    # Arrowhead: Quenched tungsten steel penetrating head (x: 114..120, y: 71..75)
    wd.polygon([(114, 71), (120, 73), (114, 75), (116, 73)], fill=OBS_LIGHT, outline=OUTLINE)
    # Cyan cooling fluid tip glow
    weapon_img.putpixel((118, 73), CYAN_LIGHT)
    weapon_img.putpixel((119, 73), WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_kite_turbine_relief_brass", key_img),
        ("back_curio", "curio_kite_spring_steel_cooling_wings", curio_img),
        ("chassis", "chassis_kite_copper_obsidian_default", chassis_img),
        ("head_unit", "head_kite_raptor_cowl_beak", head_img),
        ("costume", "costume_kite_welder_cape_belt", costume_img),
        ("optic_core", "face_kite_amber_quartz_rangefinder", core_img),
        ("weapon", "weapon_kite_crucible_recurve_bow", weapon_img)
    ]

    for slot, item_id, img_128 in slices_map:
        slot_dir = f"{KITE_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)

        # 128x128 Save
        p_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(p_128)

        # 512x512 Genuine LANCZOS Resampling Save
        p_512 = f"{slot_dir}/{item_id}_512.png"
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(p_512)
        print(f"  ✓ Saved [{slot:<12}] 128 & 512 LANCZOS: {item_id}")

    # Copy universal key and weapon to universal paperdoll directory
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copyfile(f"{KITE_PD_DIR}/winding_key/key_kite_turbine_relief_brass.png", f"{KEY_DIR}/key_kite_turbine_relief_brass.png")
    shutil.copyfile(f"{KITE_PD_DIR}/weapon/weapon_kite_crucible_recurve_bow.png", f"{WEAPON_DIR}/weapon_kite_crucible_recurve_bow.png")
    print("  ✓ Synced key & weapon to universal folders")

    # ─────────────────────────────────────────────────────────────
    # GENERATE COMPOSITE & PROOFS
    # Layer order:
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

    proof_comp = f"{KITE_PD_DIR}/proof_paperdoll_kite_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{KITE_PD_DIR}/proof_paperdoll_kite_magenta.png"
    magenta_bg.save(proof_mag)

    # Strip of all 7 slices with CJK font
    strip_w = W * 7 + 8 * 8
    strip_h = H + 28
    strip_img = Image.new("RGBA", (strip_w, strip_h), (24, 20, 36, 255))
    sd = ImageDraw.Draw(strip_img)

    slot_names = ["發條鑰匙", "背部奇玩", "底盤素體", "頭部組件", "服裝外裝", "光學核心", "手持武器"]
    strip_slices = [key_img, curio_img, chassis_img, head_img, costume_img, core_img, weapon_img]

    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc", 14)
    except Exception:
        font = ImageFont.load_default()

    for i, (name, s_img) in enumerate(zip(slot_names, strip_slices)):
        px = 8 + i * (W + 8)
        py = 8
        strip_img.alpha_composite(s_img, (px, py))
        sd.text((px + 4, py + H + 6), name, fill=(255, 208, 40, 255), font=font)

    strip_path = f"{KITE_PD_DIR}/proof_kite_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/kite_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/kite_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/kite_idle.png
    p_idle_64 = f"{PLAYER_DIR}/kite_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/kite_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/kite_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/kite_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/kite_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/kite_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL THERMAL KITE CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
