#!/usr/bin/env python3
"""
build_cuttlefish_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第五十一族 墨影烏賊 (The Inksmoke Cuttlefish, cuttlefish) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/design/INKSMOKE_CUTTLEFISH_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue, zero organic slime/tentacles,
  stamped titanium alloy cyan enamel chassis with ivory ceramic ventral plate,
  four pairs of segmented soft-steel mechanical tentacle roller claws,
  diving cowl helmet with articulated brass wave balance fins and crown relief valve,
  tri-vane turbine hydrodynamic winding key with coral pink rivet,
  abyssal navy shinobi cuirass with dopamine cyan trim and mint-green shockproof corners,
  dual convex quartz optic lenses with mint-green reticle,
  abyssal inksmoke twin curved daggers with mint-green quenched edge,
  dual-cylinder pneumatic ink-siphon backpack with pressure dials)
- references/art_direction.md & references/brand_assets.md:
  Dopamine + Abyssal Shinobi palette:
    1. Base: Ivory Ceramic Glaze / Polished Nickel (#FFFDF8, #E8ECF2, #CCD4E0)
    2. Primary Hull: Dopamine Abyssal Cyan Enamel (#38A0FF, #1869C3, #78C5FF)
    3. Secondary / Trim: Polished Gilded Brass (#FFD028, #D4A520, #FFF59D)
    4. Shinobi Cuirass: Deepsea Navy Waterproof Canvas (#1A3558, #2A507E, #10223A)
    5. Accent 1: Mint Cold Emerald Quenched Glow (#4ED86A, #78EB90, #2DA548)
    6. Accent 2: Dopamine Coral Pink (#FF5E8A, #FF2A6D, #FFA8C5)
    7. Dial / Pressure: Dawn Dopamine Warm Orange (#FFA010, #FFB84D)
    8. Dark Outline: Deep Warm Blue-Purple (#1F1A3A)
    9. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28n, 0-ART28q, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFont

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUTTLEFISH_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/cuttlefish"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Inksmoke Cuttlefish Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep warm blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory Ceramic / Polished Nickel (#FFFDF8, #E8ECF2)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (232, 236, 242, 255)
IVORY_DARK   = (204, 212, 224, 255)

# 2. Primary Hull: Dopamine Abyssal Cyan Enamel (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

# 3. Gilded Brass Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Shinobi Navy Waterproof Canvas (#1A3558)
NAVY_BASE  = (26, 53, 88, 255)
NAVY_LIGHT = (42, 80, 126, 255)
NAVY_SHINE = (64, 112, 168, 255)
NAVY_DARK  = (16, 34, 58, 255)
NAVY_DEEP  = (10, 22, 38, 255)

# 5. Mint Emerald Green Quenched Glow (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 6. Dopamine Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 205, 225, 255)
CORAL_DARK  = (195, 55, 95, 255)
CORAL_DEEP  = (135, 30, 65, 255)

# 7. Dawn Dopamine Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (195, 110, 8, 255)

# 8. Stamped Titanium Steel (#485468)
STEEL_BASE  = (72, 84, 104, 255)
STEEL_LIGHT = (108, 122, 148, 255)
STEEL_SHINE = (150, 166, 196, 255)
STEEL_DARK  = (44, 52, 68, 255)
STEEL_DEEP  = (28, 34, 46, 255)

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
    print("=== BUILDING 100% MODULAR CANONICAL INKSMOKE CUTTLEFISH SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_cuttlefish_tri_vane_turbine_brass.png
    # Features:
    # - 三葉深海渦輪水流發條鑰匙 (Tri-Vane Turbine Marine Winding Key)
    # - Robust forged brass central shaft extending from (64, 56) to (64, 25)
    # - Central escapement hub at (64, 25) with coral pink rivet (#FF5E8A)
    # - Three symmetrical curved turbine impeller blades:
    #   Blade 1: pointing up (angle -90° / -y) to (64, 11)
    #   Blade 2: down-left (angle 150°) to (49, 34)
    #   Blade 3: down-right (angle 30°) to (79, 34)
    # - Inner hydrodynamic flow cutouts in each turbine blade
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

    # 2. Three Curved Hydrodynamic Turbine Impeller Vanes
    angles_deg = [-90.0, 30.0, 150.0]
    blade_centers = []

    for ang in angles_deg:
        rad = np.radians(ang)
        tcx = hub_x + 14.0 * np.cos(rad)
        tcy = hub_y + 14.0 * np.sin(rad)
        blade_centers.append((tcx, tcy))

        blade_radius = 8.5
        for dy in range(int(-blade_radius - 1), int(blade_radius + 2)):
            for dx in range(int(-blade_radius - 1), int(blade_radius + 2)):
                d = (dx**2 + dy**2)**0.5
                if d <= blade_radius:
                    px = int(round(tcx + dx))
                    py = int(round(tcy + dy))
                    if 0 <= px < W and 0 <= py < H:
                        spec = max(0.0, 1.0 - abs(d - 5.5) / 3.0)
                        shine = max(0.0, 1.0 - abs(dx + 1.5) / 3.0)**2 if dy < 0 else 0.0
                        r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                        key_img.putpixel((px, py), (r, g, b, 255))

    for tcx, tcy in blade_centers:
        for t in np.linspace(0.0, 1.0, 16):
            rx = int(round(hub_x + t * (tcx - hub_x)))
            ry = int(round(hub_y + t * (tcy - hub_y)))
            kd.ellipse([rx - 3, ry - 3, rx + 3, ry + 3], fill=GOLD_BASE)

    # Hydrodynamic flow hollow cutouts in each blade (radius 3.2px)
    k_px = key_img.load()
    inner_rad = 3.2
    for tcx, tcy in blade_centers:
        for dy in range(int(-inner_rad - 1), int(inner_rad + 2)):
            for dx in range(int(-inner_rad - 1), int(inner_rad + 2)):
                if (dx**2 + dy**2)**0.5 <= inner_rad:
                    px = int(round(tcx + dx))
                    py = int(round(tcy + dy))
                    if 0 <= px < W and 0 <= py < H:
                        k_px[px, py] = (0, 0, 0, 0)

    # 3. Central Escapement Hub & Coral Pink Rivet
    kd.ellipse([int(hub_x - 7), int(hub_y - 7), int(hub_x + 7), int(hub_y + 7)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 5), int(hub_y - 5), int(hub_x + 5), int(hub_y + 5)], fill=GOLD_BASE)
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
    # File: back_curio/curio_cuttlefish_pneumatic_ink_siphon.png
    # Features:
    # - 氣動高壓發煙雙聯墨囊氣罐 (Pneumatic High-Pressure Ink-Siphon Pack)
    # - Dual symmetrical vertical stamped titanium cyan tanks
    # - Rich multi-tone shading with brushed metal highlights
    # - Clear central corridor (x: 58..70) strictly kept clear for winding key!
    # - Gold brass retention straps & reinforcement bands (#FFD028)
    # - Top brass siphon exhaust nozzles & miniature orange pressure gauges (#FFA010)
    # - Flexible braided brass conduit loops at bottom connecting to chassis
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    tanks = [
        (48.0, 42, 54, 52, 82),   # Left tank cx=48
        (80.0, 74, 86, 52, 82)    # Right tank cx=80
    ]

    for cx, x0, x1, y0, y1 in tanks:
        hw = (x1 - x0) / 2.0
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                dx = (x - cx) / hw
                spec = max(0.0, 1.0 - abs(dx))
                shine = max(0.0, 1.0 - abs(x - (cx - 1.5)) / 2.0)**2
                # Subtle vertical brushed gradient
                vert_grad = 0.9 + 0.2 * ((y - y0) / float(y1 - y0))
                r = int(np.clip(CYAN_BASE[0] * (0.75 + 0.35 * spec) * vert_grad + 40 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.75 + 0.35 * spec) * vert_grad + 30 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.75 + 0.35 * spec) * vert_grad + 20 * shine, 0, 255))
                curio_img.putpixel((x, y), (r, g, b, 255))

        # Gold Reinforcement Rings along tank body (y: 60, y: 72)
        for ry in (60, 72):
            for x in range(x0 - 1, x1 + 2):
                spec = max(0.0, 1.0 - abs(x - cx) / hw)
                r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                curio_img.putpixel((x, ry), (r, g, b, 255))
                curio_img.putpixel((x, ry - 1), (int(r * 0.8), int(g * 0.8), int(b * 0.8), 255))
                curio_img.putpixel((x, ry + 1), (int(r * 0.7), int(g * 0.7), int(b * 0.7), 255))

        # Top Brass Siphon Nozzle & Cap
        cd.ellipse([int(cx - 4), y0 - 4, int(cx + 4), y0 + 2], fill=GOLD_BASE, outline=OUTLINE)
        cd.point((int(cx), y0 - 3), fill=GOLD_LIGHT)
        cd.rectangle([int(cx - 2), y0 - 7, int(cx + 2), y0 - 3], fill=GOLD_DARK, outline=OUTLINE)
        cd.point((int(cx), y0 - 6), fill=ORANGE_BASE)

        # Miniature Round Pressure Dial on upper tank (at y: 56)
        cd.ellipse([int(cx - 3), 54, int(cx + 3), 60], fill=GOLD_DARK, outline=OUTLINE)
        cd.ellipse([int(cx - 2), 55, int(cx + 2), 59], fill=ORANGE_BASE)
        cd.point((int(cx), 57), fill=CORAL_BASE)
        cd.point((int(cx + 1), 56), fill=WHITE_SHINE)

    # Bottom Flexible Braided Brass Conduit Loops connecting back into chassis
    for p_pts in [
        [(48.0, 82.0), (45.0, 86.0), (44.0, 90.0), (48.0, 92.0)],
        [(80.0, 82.0), (83.0, 86.0), (84.0, 90.0), (80.0, 92.0)]
    ]:
        for i in range(len(p_pts) - 1):
            p0, p1 = p_pts[i], p_pts[i + 1]
            for t in np.linspace(0.0, 1.0, 10):
                px = int(round(p0[0] + t * (p1[0] - p0[0])))
                py = int(round(p0[1] + t * (p1[1] - p0[1])))
                cd.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD_BASE, outline=OUTLINE)
                cd.point((px, py), fill=GOLD_LIGHT)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)

    # Strictly preserve central corridor for winding key (x: 59..69)
    c_px = curio_img.load()
    for y in range(H):
        for x in range(59, 70):
            c_px[x, y] = (0, 0, 0, 0)

    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_cuttlefish_abyssal_cyan_default.png
    # Features:
    # - 鍍鈦合金與琉璃海藍搪瓷素體底盤 (Abyssal Cyan Enamel Titanium Chassis)
    # - 2.2 chibi ratio, compact hydrodynamic torso
    # - 4 pairs (8 total) of segmented soft-steel mechanical tentacle roller claws along base (y: 104..116)
    # - Torso: stamped titanium cyan enamel (#38A0FF) with ivory ceramic ventral plate (#FFFDF8)
    # - Silver waterproof hex bolts & deep blue-purple seams
    # - Left arm forward in shinobi guard posture at (34..48, 68..80)
    # - Right arm at (78..88, 66..76) (strictly x < 94)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # - Plate color distance L2 < 60.0 with head_unit (0-ART28q)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Four Pairs of Segmented Mechanical Tentacle Roller Claws (x: 40..88, y: 102..116)
    tentacle_xs = [42, 48, 54, 60, 68, 74, 80, 86]
    for tx in tentacle_xs:
        for t in np.linspace(0.0, 1.0, 10):
            ty = 98.0 + t * 15.0
            curv = np.sin(t * np.pi) * 1.5 * (1 if tx < 64 else -1)
            px = int(round(tx + curv))
            py = int(round(ty))
            ch_d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=STEEL_BASE, outline=OUTLINE)
            ch_d.point((px, py), fill=STEEL_LIGHT)

        # Roller wheel foot with brass rim & rubber tread pad at (tx, 113)
        ch_d.ellipse([tx - 3, 111, tx + 3, 116], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.ellipse([tx - 2, 112, tx + 2, 115], fill=STEEL_DARK)
        ch_d.point((tx, 113), fill=MINT_LIGHT)

    # Continuous brass skid plate uniting the feet along y: 104..108
    ch_d.rectangle([38, 104, 62, 108], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.line([(39, 105), (61, 105)], fill=GOLD_LIGHT, width=1)
    ch_d.rectangle([66, 104, 90, 108], fill=GOLD_BASE, outline=OUTLINE)
    ch_d.line([(67, 105), (89, 105)], fill=GOLD_LIGHT, width=1)

    # 2. Upper Torso Flange & Neck Collar (x: 46..82, y: 44..59)
    for ny in range(44, 60):
        for nx in range(46, 83):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 18.0)
            r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
            chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # Lower chassis backing frame (connecting torso to feet frame solidly)
    for ty in range(86, 106):
        for tx in range(42, 86):
            dx = (tx - 64.0) / 21.0
            dy = (ty - 96.0) / 12.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # 3. Main Streamlined Chibi Torso (x: 42..86, y: 58..102)
    for ty in range(58, 103):
        for tx in range(42, 87):
            dx = (tx - 64.0) / 20.5
            dy = (ty - 78.0) / 22.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 70.0)**2)**0.5 / 12.0)**2
                is_belly_ceramic = (52 <= tx <= 76 and 66 <= ty <= 88)

                if is_belly_ceramic:
                    r = int(np.clip(238 * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
                    g = int(np.clip(234 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                    b = int(np.clip(226 * (0.85 + 0.25 * spec) + 20 * shine, 0, 242))
                else:
                    r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                    g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                    b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Silver Waterproof Hex Bolts & Seam Details
    for by in [62, 70, 78, 86, 94]:
        for bx in [45, 83]:
            ch_d.ellipse([bx - 1, by - 1, bx + 1, by + 1], fill=IVORY_LIGHT, outline=OUTLINE)
            ch_d.point((bx, by), fill=STEEL_LIGHT)

    # Central Ventral Hydro-Seam & Pressure Gauge on Belly at (64, 76)
    ch_d.ellipse([59, 71, 69, 81], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([60, 72, 68, 80], fill=CYAN_BASE)
    ch_d.ellipse([62, 74, 66, 78], fill=GOLD_BASE)
    ch_d.point((64, 76), fill=MINT_BASE)
    ch_d.point((63, 75), fill=WHITE_SHINE)

    # 4. Left Arm in forward shinobi guard posture at (34..48, 68..80)
    for t in np.linspace(0.0, 1.0, 18):
        ax = 52.0 - t * 13.0
        ay = 66.0 + t * 8.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), CYAN_BASE)
    ch_d.ellipse([34, 72, 44, 80], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([36, 74, 42, 78], fill=CYAN_LIGHT)
    ch_d.point((39, 76), fill=GOLD_LIGHT)

    # 5. Right Arm positioned at (78..88, 66..76) (strictly x < 94)
    for t in np.linspace(0.0, 1.0, 16):
        ax = 78.0 + t * 9.0  # max ax = 87
        ay = 66.0 + t * 6.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px = int(ax + dx)
                py = int(ay + dy)
                if px < 94 and dx**2 + dy**2 <= 9:
                    chassis_img.putpixel((px, py), CYAN_BASE)
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
    # File: head_unit/head_cuttlefish_diving_cowl_fins.png
    # Features:
    # - 深潛圓頂頭盔與氣動平衡側鰭 (Diving Cowl with Balance Fins)
    # - Stamped titanium bell-shaped cowl shell in cyan enamel (#38A0FF)
    # - Top crown brass pressure relief valve (#FFD028) at (64, 22..30)
    # - Pair of articulated thin stamped brass wave balance side-fins at left (24..42) and right (86..104)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Base Bell-Shaped Diving Cowl Shell (x: 42..86, y: 32..57)
    for y in range(32, 58):
        for x in range(42, 87):
            dx = (x - hcx) / 21.0
            dy = (y - 45.0) / 12.5
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 21.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 7.0)**2
                r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 2. Articulated Thin Stamped Brass Wave Balance Side-Fins
    left_fin_pts = [(42, 38), (34, 35), (25, 38), (24, 44), (32, 46), (42, 44)]
    hd.polygon(left_fin_pts, fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(40, 40), (28, 41)], fill=GOLD_LIGHT, width=1)
    hd.line([(40, 42), (30, 43)], fill=MINT_BASE, width=1)
    hd.ellipse([40, 39, 44, 43], fill=GOLD_DARK, outline=OUTLINE)
    hd.point((42, 41), fill=CORAL_BASE)

    right_fin_pts = [(86, 38), (94, 35), (103, 38), (104, 44), (96, 46), (86, 44)]
    hd.polygon(right_fin_pts, fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(88, 40), (100, 41)], fill=GOLD_LIGHT, width=1)
    hd.line([(88, 42), (98, 43)], fill=MINT_BASE, width=1)
    hd.ellipse([84, 39, 88, 43], fill=GOLD_DARK, outline=OUTLINE)
    hd.point((86, 41), fill=CORAL_BASE)

    # 3. Top Crown Brass Pressure Relief Valve (at x: 64, y: 22..32)
    hd.rectangle([60, 28, 68, 33], fill=GOLD_BASE, outline=OUTLINE)
    hd.line([(61, 29), (67, 29)], fill=GOLD_LIGHT, width=1)
    hd.rectangle([62, 24, 66, 28], fill=GOLD_DARK, outline=OUTLINE)
    hd.ellipse([59, 21, 69, 25], fill=GOLD_BASE, outline=OUTLINE)
    hd.ellipse([62, 22, 66, 24], fill=CORAL_BASE)
    hd.point((64, 23), fill=WHITE_SHINE)

    # Stamped visor eyebrow ridge across y: 33..36, x: 46..82
    for y in range(33, 37):
        hw = 12.0 + (y - 33.0) * 1.5
        for x in range(int(hcx - hw), int(hcx + hw + 1)):
            spec = max(0.0, 1.0 - abs(x - hcx) / (hw + 0.1))
            r = int(np.clip(GOLD_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(GOLD_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(GOLD_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
            head_img.putpixel((x, y), (r, g, b, 255))
    hd.line([(int(hcx - 17), 36), (int(hcx + 17), 36)], fill=MINT_BASE, width=1)

    # 4. Hollow Eye Sockets for 0-ART27:
    h_px = head_img.load()
    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    ignore_eyes = [(50, 38, 58, 46), (70, 38, 78, 46)]
    apply_clean_outline(head_img, outline_color=OUTLINE, min_alpha=100, ignore_regions=ignore_eyes)

    for ey, ex_center in [(42, 54), (42, 74)]:
        for dy in range(-3, 4):
            for dx in range(-3, 4):
                if dx**2 + dy**2 <= 9:
                    h_px[ex_center + dx, ey + dy] = (0, 0, 0, 0)

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_cuttlefish_abyssal_shinobi_cuirass.png
    # Features:
    # - 海淵夜行輕量耐壓背心 (Abyssal Shinobi Lightweight Cuirass)
    # - Deepsea waterproof navy canvas base (#1A3558)
    # - Front curved titanium cyan stamped breastplate (#38A0FF)
    # - Mint-green shockproof corner brackets (#4ED86A)
    # - Center embossed deepsea wave & gear emblem at (64, 72)
    # - Shoulder hydro-conduit strap baffles at (42, 60) and (86, 60)
    # - Shinobi utility belt and gold buckle ending strictly at y: 92
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Navy Shinobi Cuirass Vest (x: 46..82, y: 60..86)
    for y in range(60, 87):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2

            is_cyan_chest = (52 <= x <= 76 and 64 <= y <= 82)
            is_mint_corner = is_cyan_chest and ((x in (52, 53, 75, 76) and y in (64, 65, 81, 82)))

            if is_mint_corner:
                r = int(np.clip(MINT_BASE[0] * (0.85 + 0.3 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(MINT_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(MINT_BASE[2] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
            elif is_cyan_chest:
                r = int(np.clip(CYAN_BASE[0] * (0.85 + 0.3 * spec) + 35 * shine, 0, 255))
                g = int(np.clip(CYAN_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(CYAN_BASE[2] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
            else:
                r = int(np.clip(NAVY_BASE[0] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                g = int(np.clip(NAVY_BASE[1] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(NAVY_BASE[2] * (0.85 + 0.3 * spec) + 25 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Center Embossed Gold Deepsea Wave Totem at (64, 72)
    cos_d.ellipse([60, 68, 68, 76], fill=GOLD_BASE, outline=OUTLINE)
    cos_d.ellipse([62, 70, 66, 74], fill=CYAN_BASE)
    cos_d.point((64, 72), fill=GOLD_LIGHT)

    # 2. Shoulder Hydro-Conduit Strap Baffles at (42, 60) and (86, 60)
    for px, py in [(42.0, 60.0), (86.0, 60.0)]:
        cos_d.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=CYAN_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=GOLD_BASE)
        cos_d.point((int(px), int(py)), fill=MINT_LIGHT)

    # 3. Waist Shinobi Utility Belt & Buckle hanging from y: 86 down to y: 92
    waist_spans = [(48, 55), (57, 63), (65, 71), (73, 80)]
    for x0, x1 in waist_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=NAVY_DARK, outline=OUTLINE)
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
    # File: optic_core/face_cuttlefish_dual_quartz_optic_lens.png
    # Features:
    # - 雙聯水下耐壓石英探照目鏡 (Dual Pressure-Proof Quartz Optic Lenses)
    # - Convex quartz crystal lenses centered at (54, 42) and (74, 42)
    # - Brass vernier adjustment gear rings
    # - Dopamine cyan (#38A0FF) & mint emerald glow (#4ED86A) with horizontal rangefinder reticle
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha = 255)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:
        # Outer Brass Vernier Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Quartz Cyan / Mint Interference Film)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.3 * spec) + 60 * shine, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.8 + 0.3 * spec) + 70 * shine, 0, 255))
                    b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.25 * spec) + 50 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Concentric dial crosshair & focus highlight
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), MINT_SHINE)
        core_img.putpixel((int(ex + 1), int(ey)), MINT_LIGHT)
        core_img.putpixel((int(ex), int(ey - 1)), CYAN_SHINE)
        core_img.putpixel((int(ex), int(ey + 1)), CYAN_DARK)

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
    # File: weapon/weapon_cuttlefish_abyssal_inksmoke_dagger.png
    # Features:
    # - 海淵墨影雙鋒匕 (Abyssal Inksmoke Twin Daggers)
    # - Dual curved daggers of stamped titanium alloy in dopamine cyan (#38A0FF)
    # - Quenched mint-green cutting edges (#4ED86A) with multi-tone depth
    # - Deep blue fluid siphon flutes and bleed vents
    # - Polished brass wave-embossed crossguards (#FFD028) with gradient highlights
    # - Primary dagger: right hand reverse grip held forward (x: 84..105, y: 64..87)
    # - Secondary dagger: left claw guarding chest (x: 30..44, y: 70..88)
    # - Rich multi-tone shading to easily exceed 0-ART5 color richness limit
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Primary Dagger (Right Hand, sweeping forward / down at x: 84..104, y: 64..86)
    # Brass Crossguard with gradient at (86, 70)
    for gy in range(67, 74):
        for gx in range(82, 91):
            dx = (gx - 86.0) / 4.5
            dy = (gy - 70.0) / 3.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.3 * spec) + 30 * (1.0 - abs(dy)), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.3 * spec) + 25 * (1.0 - abs(dy)), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.3 * spec) + 15 * (1.0 - abs(dy)), 0, 255))
                weapon_img.putpixel((gx, gy), (r, g, b, 255))

    # Pommel & Handle (x: 84..88, y: 62..70)
    for hy in range(62, 70):
        for hx in range(84, 89):
            spec = max(0.0, 1.0 - abs(hx - 86.0) / 2.0)
            c = GOLD_BASE if hy % 2 == 0 else GOLD_LIGHT
            r = int(np.clip(c[0] * (0.85 + 0.25 * spec), 0, 255))
            g = int(np.clip(c[1] * (0.85 + 0.25 * spec), 0, 255))
            b = int(np.clip(c[2] * (0.85 + 0.25 * spec), 0, 255))
            weapon_img.putpixel((hx, hy), (r, g, b, 255))

    # Curved Cyan Blade with Mint Quenched Edge
    blade_poly_main = [
        (86, 73), (92, 75), (98, 80), (102, 86),
        (104, 82), (102, 74), (96, 70), (88, 71)
    ]
    wd.polygon(blade_poly_main, fill=CYAN_BASE, outline=OUTLINE)

    for y in range(69, 88):
        for x in range(86, 105):
            if wd._image.getpixel((x, y))[3] > 100:
                is_edge = (x >= 99 or y >= 82)
                t_along = (x - 86.0) / 18.0
                t_across = (y - 70.0) / 16.0
                shine = max(0.0, 1.0 - abs(t_across - 0.5) * 2.0)
                if is_edge:
                    # Mint green cutting edge with smooth gradient
                    r = int(np.clip(MINT_BASE[0] * (0.85 + 0.3 * t_along) + 30 * shine, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.85 + 0.3 * t_along) + 30 * shine, 0, 255))
                    b = int(np.clip(MINT_BASE[2] * (0.85 + 0.3 * t_along) + 30 * shine, 0, 255))
                else:
                    # Titanium cyan blade body with fluid reflection
                    r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.35 * t_along) + 40 * shine, 0, 255))
                    g = int(np.clip(CYAN_BASE[1] * (0.8 + 0.35 * t_along) + 30 * shine, 0, 255))
                    b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.35 * t_along) + 20 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Fluid siphon flute line
    wd.line([(88, 73), (98, 79)], fill=NAVY_DARK, width=1)
    wd.point((92, 75), fill=WHITE_SHINE)

    # 2. Secondary Dagger (Left Claw, tucked across chest at x: 30..44, y: 70..88)
    # Guard at (40, 76)
    for gy in range(73, 80):
        for gx in range(36, 45):
            dx = (gx - 40.0) / 4.5
            dy = (gy - 76.0) / 3.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.3 * spec), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.3 * spec), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.3 * spec), 0, 255))
                weapon_img.putpixel((gx, gy), (r, g, b, 255))

    # Handle
    for hy in range(70, 76):
        for hx in range(38, 43):
            c = GOLD_BASE if hy % 2 == 0 else GOLD_LIGHT
            weapon_img.putpixel((hx, hy), c)

    # Curved Blade curving down-left to (30, 88)
    blade_poly_sub = [
        (40, 78), (38, 82), (34, 86), (30, 88),
        (32, 84), (36, 80), (40, 77)
    ]
    wd.polygon(blade_poly_sub, fill=CYAN_BASE, outline=OUTLINE)
    for y in range(76, 89):
        for x in range(30, 42):
            if wd._image.getpixel((x, y))[3] > 100:
                is_edge = (x <= 33 or y >= 85)
                t_along = (40.0 - x) / 10.0
                shine = max(0.0, 1.0 - abs((y - 82.0) / 6.0))
                if is_edge:
                    r = int(np.clip(MINT_BASE[0] * (0.85 + 0.3 * t_along) + 30 * shine, 0, 255))
                    g = int(np.clip(MINT_BASE[1] * (0.85 + 0.3 * t_along) + 30 * shine, 0, 255))
                    b = int(np.clip(MINT_BASE[2] * (0.85 + 0.3 * t_along) + 30 * shine, 0, 255))
                else:
                    r = int(np.clip(CYAN_BASE[0] * (0.8 + 0.35 * t_along) + 35 * shine, 0, 255))
                    g = int(np.clip(CYAN_BASE[1] * (0.8 + 0.35 * t_along) + 25 * shine, 0, 255))
                    b = int(np.clip(CYAN_BASE[2] * (0.8 + 0.35 * t_along) + 15 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    wd.line([(38, 79), (33, 85)], fill=NAVY_DARK, width=1)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE 128x128 & 512x512 SLICES
    # ─────────────────────────────────────────────────────────────
    slices_data = [
        ("winding_key", "key_cuttlefish_tri_vane_turbine_brass", key_img),
        ("back_curio", "curio_cuttlefish_pneumatic_ink_siphon", curio_img),
        ("chassis", "chassis_cuttlefish_abyssal_cyan_default", chassis_img),
        ("head_unit", "head_cuttlefish_diving_cowl_fins", head_img),
        ("costume", "costume_cuttlefish_abyssal_shinobi_cuirass", costume_img),
        ("optic_core", "face_cuttlefish_dual_quartz_optic_lens", core_img),
        ("weapon", "weapon_cuttlefish_abyssal_inksmoke_dagger", weapon_img)
    ]

    for slot, item_id, s_img in slices_data:
        slot_dir = f"{CUTTLEFISH_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        p128 = f"{slot_dir}/{item_id}.png"
        s_img.save(p128)

        # 512x512 Genuine Lanczos scaling
        p512 = f"{slot_dir}/{item_id}_512.png"
        s_img_512 = s_img.resize((512, 512), Image.Resampling.LANCZOS)
        s_img_512.save(p512)

    # Universal dirs
    os.makedirs(KEY_DIR, exist_ok=True)
    shutil.copy2(f"{CUTTLEFISH_PD_DIR}/winding_key/key_cuttlefish_tri_vane_turbine_brass.png",
                 f"{KEY_DIR}/key_cuttlefish_tri_vane_turbine_brass.png")

    os.makedirs(WEAPON_DIR, exist_ok=True)
    shutil.copy2(f"{CUTTLEFISH_PD_DIR}/weapon/weapon_cuttlefish_abyssal_inksmoke_dagger.png",
                 f"{WEAPON_DIR}/weapon_cuttlefish_abyssal_inksmoke_dagger.png")

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

    proof_comp = f"{CUTTLEFISH_PD_DIR}/proof_paperdoll_cuttlefish_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{CUTTLEFISH_PD_DIR}/proof_paperdoll_cuttlefish_magenta.png"
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

    strip_path = f"{CUTTLEFISH_PD_DIR}/proof_cuttlefish_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # OFFICIAL IDLE ASSETS & SHOWCASE HD
    # ─────────────────────────────────────────────────────────────
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    shd = ImageDraw.Draw(shadow_layer)
    shd.ellipse([30, 110, 98, 122], fill=(31, 26, 58, 110))
    shd.ellipse([40, 112, 88, 120], fill=(31, 26, 58, 160))

    idle_with_shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    idle_with_shadow.alpha_composite(shadow_layer)
    idle_with_shadow.alpha_composite(composite)

    # 1. 128x128 game/assets/sprites/player/cuttlefish_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/cuttlefish_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/cuttlefish_idle.png
    p_idle_64 = f"{PLAYER_DIR}/cuttlefish_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/cuttlefish_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/cuttlefish_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/cuttlefish_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/cuttlefish_idle.png"
    idle_with_shadow.save(p_web_idle)

    # 5. 800x1200 RGBA showcase HD (game/assets/sprites/player/showcase/cuttlefish_idle_hd.png)
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

        showcase_out = f"{SHOWCASE_DIR}/cuttlefish_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL INKSMOKE CUTTLEFISH CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
