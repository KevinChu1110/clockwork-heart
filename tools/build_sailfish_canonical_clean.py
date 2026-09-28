#!/usr/bin/env python3
"""
build_sailfish_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十一族 破浪旗魚 (The Hydrofoil Sailfish, sailfish) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/HYDROFOIL_SAILFISH_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, deep-sea cobalt blue titanium armor plates,
  ivory white porcelain cheek/belly plates, dual quartz dial rangefinder lenses,
  articulated clockwork sail-fin mantle, abyssal helm trident winding key,
  hydrofoil spiral piercing lance)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Ivory Titanium White (#FFFDF8)
    2. Secondary Hull: Deep Sea Cobalt Blue (#1E3A8A)
    3. Optic Core & LEDs: Amber Starlight / Gold (#FFD028)
    4. Wave & Fluid: Sky Cyan / Abyssal Blue (#38A0FF)
    5. Alert Orange: Wasteland / High-pressure Orange (#FFA010)
    6. Mint Green: Resonator & Seals (#4ED86A)
    7. Frame & Tungsten: Pearl Silver / Titanium Steel (#E2E8F0 / #4A5568)
    8. Outline: Deep Blue-Purple Thick Outline (#1F1A3A)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
SAILFISH_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Hydrofoil Sailfish Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Ivory Titanium White (#FFFDF8)
IVORY_BASE  = (255, 253, 248, 255)
IVORY_LIGHT = (255, 255, 255, 255)
IVORY_SHADE = (228, 222, 212, 255)
IVORY_DARK  = (195, 188, 175, 255)
IVORY_DEEP  = (160, 152, 140, 255)

# 2. Secondary Hull: Deep Sea Cobalt Blue (#1E3A8A)
COBALT_BASE  = (30, 58, 138, 255)
COBALT_LIGHT = (48, 88, 195, 255)
COBALT_SHINE = (96, 148, 245, 255)
COBALT_DARK  = (18, 36, 92, 255)
COBALT_DEEP  = (10, 20, 58, 255)

# 3. Optic Core & LEDs: Amber Starlight / Gold (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (205, 148, 18, 255)
GOLD_DEEP  = (145, 95, 10, 255)

# 4. Wave & Fluid: Sky Cyan / Abyssal Blue (#38A0FF)
CYAN_BASE  = (56, 160, 255, 255)
CYAN_LIGHT = (120, 205, 255, 255)
CYAN_SHINE = (195, 235, 255, 255)
CYAN_DARK  = (24, 105, 195, 255)
CYAN_DEEP  = (14, 60, 130, 255)

# 5. Alert Orange: Wasteland / High-pressure Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 192, 64, 255)
ORANGE_SHINE = (255, 224, 128, 255)
ORANGE_DARK  = (210, 115, 8, 255)
ORANGE_DEEP  = (150, 75, 4, 255)

# 6. Mint Green: Resonator & Seals (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 7. Frame & Tungsten: Pearl Silver / Titanium Steel (#E2E8F0 / #4A5568)
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (140, 155, 175, 255)
STEEL_SHINE = (226, 232, 240, 255)
STEEL_DARK  = (42, 50, 64, 255)
STEEL_DEEP  = (26, 32, 42, 255)

# 8. Accent & Seals: Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_SHINE = (255, 200, 220, 255)
CORAL_DARK  = (200, 50, 95, 255)

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
            if px_snap[x, y][3] < min_alpha:
                # Check 8 neighbors in snapshot
                has_solid_neighbor = False
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < w and 0 <= ny < h:
                            if px_snap[nx, ny][3] >= min_alpha:
                                has_solid_neighbor = True
                                break
                    if has_solid_neighbor:
                        break

                if has_solid_neighbor:
                    px_dest[x, y] = outline_color


def build_all():
    print("=== BUILDING 100% MODULAR CANONICAL HYDROFOIL SAILFISH SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_sailfish_abyssal_helm_trident.png
    # Abyssal Helm Trident Winding Key (深海三叉舵輪發條鑰匙)
    # Socket boss at spine (64, 58), shaft extends diagonally up-right to (92, 22)
    # Protrudes clearly beyond head silhouette (x: 80..112, y: 8..36)
    # Features:
    # - Solid brass shaft with radial bevel shading
    # - Nautical helm wheel with 6 radiating spokes and outer rim
    # - 3 trident spear prongs crowning helm top: center (92, 8), left (82, 12), right (102, 12)
    # - Central sapphire/cyan jewel bearing at (92, 22)
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 58) to (92, 22)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 28.0
        sy = 58.0 - t * 36.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Base socket collar at (64, 58)
    kd.ellipse([64 - 5, 58 - 5, 64 + 5, 58 + 5], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 58 - 3, 64 + 3, 58 + 3], fill=GOLD_BASE)
    kd.ellipse([64 - 1, 58 - 1, 64 + 1, 58 + 1], fill=CYAN_BASE)

    # 2. Nautical Helm Wheel at (92, 22)
    kcx, kcy = 92.0, 22.0
    helm_radius = 10.0

    # 6 Helm Spokes
    for angle in np.linspace(0, 2 * np.pi, 6, endpoint=False):
        for dist in np.linspace(2.0, helm_radius + 3.0, 20):
            px = int(round(kcx + dist * np.cos(angle)))
            py = int(round(kcy + dist * np.sin(angle)))
            if 0 <= px < W and 0 <= py < H:
                key_img.putpixel((px, py), GOLD_BASE)
        # Rounded knob at each spoke handle tip
        tx = int(round(kcx + (helm_radius + 3.0) * np.cos(angle)))
        ty = int(round(kcy + (helm_radius + 3.0) * np.sin(angle)))
        kd.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=GOLD_LIGHT, outline=OUTLINE_KEY)

    # Helm Outer Ring (radius 9..11)
    for ang in np.linspace(0, 2 * np.pi, 64):
        for r in [9.0, 10.0, 11.0]:
            px = int(round(kcx + r * np.cos(ang)))
            py = int(round(kcy + r * np.sin(ang)))
            if 0 <= px < W and 0 <= py < H:
                if r == 10.0:
                    key_img.putpixel((px, py), GOLD_LIGHT)
                else:
                    key_img.putpixel((px, py), GOLD_BASE)

    # 3. Three Trident Spear Prongs Crowning Helm
    # Center prong: (92, 11) up to tip at (92, 6)
    for ty in range(6, 12):
        key_img.putpixel((int(kcx), ty), GOLD_SHINE)
        key_img.putpixel((int(kcx - 1), ty), GOLD_BASE)
        key_img.putpixel((int(kcx + 1), ty), GOLD_BASE)
    kd.polygon([(int(kcx), 4), (int(kcx - 2), 7), (int(kcx + 2), 7)], fill=GOLD_SHINE, outline=OUTLINE_KEY)

    # Left prong: curves from (84, 18) up to (82, 10)
    for t in np.linspace(0.0, 1.0, 15):
        lx = int(round(86.0 * (1 - t) + 82.0 * t))
        ly = int(round(16.0 * (1 - t) + 10.0 * t))
        key_img.putpixel((lx, ly), GOLD_BASE)
        key_img.putpixel((lx + 1, ly), GOLD_LIGHT)
    kd.polygon([(81, 9), (84, 10), (81, 13)], fill=GOLD_LIGHT, outline=OUTLINE_KEY)

    # Right prong: curves from (100, 18) up to (102, 10)
    for t in np.linspace(0.0, 1.0, 15):
        rx = int(round(98.0 * (1 - t) + 102.0 * t))
        ry = int(round(16.0 * (1 - t) + 10.0 * t))
        key_img.putpixel((rx, ry), GOLD_BASE)
        key_img.putpixel((rx - 1, ry), GOLD_LIGHT)
    kd.polygon([(103, 9), (100, 10), (103, 13)], fill=GOLD_LIGHT, outline=OUTLINE_KEY)

    # 4. Central Sapphire/Cyan Bearing at (92, 22)
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 3), int(kcy - 3), int(kcx + 3), int(kcy + 3)], fill=CYAN_BASE)
    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=CYAN_LIGHT)
    kd.point((int(kcx - 1), int(kcy - 1)), fill=WHITE_SHINE)

    # Clean outline pass with warm bronze outline to guarantee 0-ART29 compliance
    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_sailfish_clockwork_sailfin_mantle.png
    # Articulated Clockwork Sail-Fin Mantle (多節聯動發條折疊背鰭帆)
    # Originates along upper dorsal spine (48..66, 44..66).
    # Sweeps up and arches forward-up to tall sail peak at (34, 16),
    # forming the iconic sailfish fan mantle that distinguishes it across silhouettes!
    # Features:
    # - 7 articulated radiating ribs/spines with gold and bronze hinges
    # - Cobalt blue (#1E3A8A) and Sky Cyan (#38A0FF) hydrofoil membrane webbing
    # - Gold (#FFD028) trim along scalloped crest line
    # - Micro hydrofoil vent slots and fluid flow highlights
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Sail Fin Perimeter Polygon:
    # Starts at neck attachment (60, 42) -> arches up to peak (34, 16) ->
    # scalloped trailing edge down to (26, 36) -> (28, 52) -> (36, 64) ->
    # lower spine attachment (48, 68) -> along spine back to (60, 42).
    sail_polygon = [
        (60, 42),
        (52, 28),
        (42, 20),
        (34, 16),  # Crest peak
        (28, 24),
        (26, 36),  # Mid trailing cusp
        (28, 48),
        (32, 58),
        (40, 66),
        (48, 68),  # Lower attachment
        (56, 58),
        (62, 48)
    ]
    cd.polygon(sail_polygon, fill=COBALT_BASE)

    # Multi-tone gradient & fluid wave texturing across the fin membrane
    for y in range(16, 70):
        for x in range(24, 64):
            if curio_img.getpixel((x, y))[3] > 0:
                dist_peak = ((x - 34)**2 + (y - 16)**2)**0.5
                spec = max(0.0, 1.0 - dist_peak / 45.0)
                shine = max(0.0, 1.0 - abs(x - 38) / 14.0)**2

                # Wave interference pattern
                wave = np.sin((x + y * 1.5) * 0.4) * 0.5 + 0.5

                r_f = int(np.clip(30 * (0.8 + 0.4 * spec) + 40 * shine, 0, 255))
                g_f = int(np.clip(58 * (0.8 + 0.6 * spec) + 80 * shine + 30 * wave, 0, 255))
                b_f = int(np.clip(138 * (0.8 + 0.7 * spec) + 90 * shine + 50 * wave, 0, 255))
                curio_img.putpixel((x, y), (r_f, g_f, b_f, 255))

    # 7 Radiating Titanium Ribs / Hinged Struts from base hub (54, 56)
    base_hub = (54.0, 56.0)
    rib_tips = [
        (60, 42),
        (52, 28),
        (42, 20),
        (34, 16),
        (28, 24),
        (26, 36),
        (28, 48)
    ]
    for r_idx, tip in enumerate(rib_tips):
        # Draw rib line
        for t in np.linspace(0.0, 1.0, 40):
            rx = int(round(base_hub[0] * (1 - t) + tip[0] * t))
            ry = int(round(base_hub[1] * (1 - t) + tip[1] * t))
            if 0 <= rx < W and 0 <= ry < H and curio_img.getpixel((rx, ry))[3] > 0:
                curio_img.putpixel((rx, ry), STEEL_SHINE)
                if r_idx % 2 == 0:
                    curio_img.putpixel((rx + 1, ry), GOLD_LIGHT)
        # Gold hinge rivet at each rib tip
        cd.ellipse([tip[0] - 1, tip[1] - 1, tip[0] + 1, tip[1] + 1], fill=GOLD_BASE, outline=OUTLINE)

    # Scalloped Golden Crest Edge along (34, 16) to (26, 36)
    for p0, p1 in zip(sail_polygon[2:8], sail_polygon[3:9]):
        cd.line([p0, p1], fill=GOLD_LIGHT, width=1)

    # Base Spine Hinge Gear Hub at (54, 56)
    cd.ellipse([50, 52, 58, 60], fill=GOLD_DARK, outline=OUTLINE)
    cd.ellipse([52, 54, 56, 58], fill=GOLD_BASE)
    cd.point((54, 56), fill=WHITE_SHINE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_sailfish_abyssal_titanium_default.png
    # Features:
    # - 2.2 Chibi high-gloss deep-sea cobalt blue titanium chassis (#1E3A8A)
    # - Soft ground contact shadow at (64, 116)
    # - Hydrodynamic diving boots at (48, 112) and (70, 112) with rubber suction sole pads
    # - Stamped titanium torso hull with ivory white (#FFFDF8) ceramic belly plate
    # - Bare chassis torso crop (60:84, 48:72) has >= 20 unique colors (0-ART18 compliant)
    # - Dual-blade streamlined hydrofoil propulsion rudder tail at rump (44..28, 88..102)
    # - Right hand tucked at ribs with weapon grip socket at (80, 72)
    # - Left hand extended forward to hold lance at (36, 74)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 28, 116 - 4, 64 + 28, 116 + 5], fill=(31, 26, 58, 120))
    ch_d.ellipse([64 - 18, 116 - 3, 64 + 18, 116 + 4], fill=(31, 26, 58, 160))

    # 2. Hydrodynamic Diving Boots & Ankle Struts
    # Left foot: (48, 112), Right foot: (70, 112)
    for fx, fy in [(48, 112), (70, 112)]:
        # Brass ankle ball joint
        ch_d.ellipse([fx - 3, fy - 6, fx + 3, fy - 2], fill=GOLD_BASE, outline=OUTLINE)
        # Diving boot body (streamlined titanium shoe)
        ch_d.ellipse([fx - 7, fy - 2, fx + 6, fy + 4], fill=COBALT_BASE, outline=OUTLINE)
        # Gold toe cap
        ch_d.ellipse([fx - 7, fy, fx - 2, fy + 4], fill=GOLD_BASE)
        # Dark suction cup rubber sole pad
        ch_d.line([(fx - 6, fy + 4), (fx + 5, fy + 4)], fill=STEEL_DEEP, width=1)
        # High-pressure seal ring
        ch_d.point((fx, fy), fill=MINT_LIGHT)

    # Leg pillars connecting pelvis to ankles
    # Left leg: (54, 94) -> (48, 108)
    for t in np.linspace(0.0, 1.0, 20):
        lx = int(54 * (1 - t) + 48 * t)
        ly = int(94 * (1 - t) + 108 * t)
        for dx in range(-3, 4):
            chassis_img.putpixel((lx + dx, ly), STEEL_BASE)
    # Right leg: (68, 94) -> (70, 108)
    for t in np.linspace(0.0, 1.0, 20):
        rx = int(68 * (1 - t) + 70 * t)
        ry = int(94 * (1 - t) + 108 * t)
        for dx in range(-3, 4):
            chassis_img.putpixel((rx + dx, ry), STEEL_BASE)

    # 3. Dual-Blade Streamlined Propulsion Rudder Tail at Rump
    # Rump root at (46, 88), curves back-down to (30, 96) and (24, 102)
    tail_pts = [
        np.array([46.0, 88.0]),
        np.array([38.0, 92.0]),
        np.array([30.0, 96.0]),
        np.array([24.0, 102.0])
    ]
    for idx in range(len(tail_pts) - 1):
        p0, p1 = tail_pts[idx], tail_pts[idx+1]
        for t in np.linspace(0.0, 1.0, 20):
            pos = p0 + t * (p1 - p0)
            ix, iy = int(round(pos[0])), int(round(pos[1]))
            for d in range(-2, 3):
                chassis_img.putpixel((ix + d, iy), COBALT_BASE)
                chassis_img.putpixel((ix, iy + d), CYAN_BASE)
    # Dual rudder fin blades
    ch_d.polygon([(24, 102), (18, 96), (20, 104)], fill=CYAN_BASE, outline=OUTLINE)
    ch_d.polygon([(24, 102), (20, 108), (28, 106)], fill=COBALT_LIGHT, outline=OUTLINE)
    ch_d.point((24, 102), fill=GOLD_BASE)

    # 4. Main Torso Hull (Cobalt Blue Titanium + Ivory Ceramic Belly Plate)
    tcx, tcy = 62.0, 74.0
    trx, try_ = 18.0, 20.0

    # Solid Pelvis & Hip Plate (48..76, 88..96) connecting torso to legs
    for y in range(88, 96):
        for x in range(48, 76):
            if ((x - 62.0)/14.0)**2 + ((y - 92.0)/4.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), STEEL_BASE)

    for y in range(54, 96):
        for x in range(44, 82):
            dx = (x - tcx) / trx
            dy = (y - tcy) / try_
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 1.1))
                shine = max(0.0, 1.0 - ((x - (tcx - 4))**2 + (y - (tcy - 4))**2)**0.5 / (trx * 0.4))**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                # Ivory Ceramic Belly Plate (x: 52..72, y: 64..88)
                is_belly = (52 <= x <= 72) and (64 <= y <= 88) and (((x - 62)/10.0)**2 + ((y - 76)/12.0)**2 <= 1.0)
                if is_belly:
                    # Multi-tone ivory & subtle marine shading to satisfy 0-ART18 (>= 20 unique colors in 60:84, 48:72)
                    b_spec = max(0.0, 1.0 - ((x - 60)**2 + (y - 72)**2)**0.5 / 10.0)
                    r_b = int(np.clip(255 * (0.88 + 0.12 * b_spec) - 20 * edge_shade, 0, 255))
                    g_b = int(np.clip(253 * (0.88 + 0.12 * b_spec) - 18 * edge_shade, 0, 255))
                    b_b = int(np.clip(248 * (0.85 + 0.15 * b_spec) - 22 * edge_shade + 12 * shine, 0, 255))
                    chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))
                else:
                    # Primary Cobalt Blue Titanium Plate
                    r_m = int(np.clip(30 * (0.82 + 0.18 * spec) + 30 * shine - 10 * edge_shade, 0, 255))
                    g_m = int(np.clip(58 * (0.82 + 0.18 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                    b_m = int(np.clip(138 * (0.80 + 0.20 * spec) + 80 * shine - 25 * edge_shade, 0, 255))
                    chassis_img.putpixel((x, y), (r_m, g_m, b_m, 255))

    # Fluid Flow Pressure Grooves across flanks (thin cyan/mint hydro lines)
    for gy in [66, 72, 78, 84]:
        for gx in range(48, 76):
            if ((gx - tcx)/trx)**2 + ((gy - tcy)/try_)**2 <= 0.82:
                if (gx + gy) % 4 == 0:
                    chassis_img.putpixel((gx, gy), CYAN_LIGHT)
                elif (gx + gy) % 4 == 2:
                    chassis_img.putpixel((gx, gy), MINT_LIGHT)

    # 5. Arms & Hands
    # Left Arm: extended forward to weapon grip socket at (36, 74)
    for y in range(54, 68):
        for x in range(38, 52):
            if ((x - 45.0)/7.0)**2 + ((y - 60.0)/8.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), COBALT_BASE)
    for t in np.linspace(0.0, 1.0, 30):
        ax = int(46 * (1 - t) + 36 * t)
        ay = int(62 * (1 - t) + 74 * t)
        for d in range(-3, 4):
            for dy in range(-2, 3):
                if d**2 + dy**2 <= 9:
                    chassis_img.putpixel((ax + d, ay + dy), STEEL_LIGHT)
    ch_d.ellipse([32, 70, 42, 78], fill=IVORY_BASE, outline=OUTLINE)
    ch_d.point((36, 74), fill=GOLD_BASE)

    # Right Arm: tucked at ribs with socket at (80, 72)
    # Strictly stop before x=94 to comply with 0-ART9/11
    for y in range(58, 72):
        for x in range(74, 86):
            if ((x - 79.0)/6.0)**2 + ((y - 65.0)/7.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), COBALT_BASE)
    for t in np.linspace(0.0, 1.0, 20):
        ax = int(72 * (1 - t) + 80 * t)
        ay = int(66 * (1 - t) + 72 * t)
        if ax < 94:
            for d in range(-2, 3):
                if ax + d < 94:
                    chassis_img.putpixel((ax + d, ay), STEEL_LIGHT)
    ch_d.ellipse([76, 68, 84, 76], fill=IVORY_BASE, outline=OUTLINE)
    ch_d.point((80, 72), fill=GOLD_BASE)

    # 6. Neck Collar & Upper Shoulder Foundation (44..84, 46..58)
    for y in range(46, 58):
        for x in range(44, 85):
            if ((x - 64.0)/20.0)**2 + ((y - 54.0)/10.0)**2 <= 1.0:
                chassis_img.putpixel((x, y), STEEL_BASE)

    # Zero out strictly at x >= 94 (0-ART9/11)
    ch_arr = np.array(chassis_img)
    ch_arr[:, 94:, :] = 0
    chassis_img = Image.fromarray(ch_arr).copy()

    apply_clean_outline(chassis_img)
    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_sailfish_hydrofoil_visor_crest.png
    # Features:
    # - Hydrofoil Visor Crest (深潛騎士折疊導流鰭盔)
    # - Stamped cobalt blue (#1E3A8A) titanium helm cranium (x: 40..88, y: 22..56)
    # - Streamlined conical rostrum snout extending from (46, 44) forward-down to (32, 48)
    # - Crown dorsal crest fin rising from (64, 22) to (64, 12) with alert orange (#FFA010) stripes
    # - Turret eye housings encircling the eye sockets at (52, 40) and (76, 40)
    # - STRICT HOLLOW EYE SOCKETS AT (52, 40) AND (76, 40) (0-ART27 compliant)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Main Sculpted Faceplate & Cranium
    hcx, hcy = 64.0, 40.0
    hrx, hry = 22.0, 18.0

    for y in range(22, 58):
        for x in range(40, 89):
            dx = (x - hcx) / hrx
            dy = (y - hcy) / hry
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / (hrx * 1.1))
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / (hrx * 0.4))**2
                edge_shade = max(0.0, (dist_sq - 0.5) / 0.5)

                r_h = int(np.clip(30 * (0.85 + 0.15 * spec) + 30 * shine - 10 * edge_shade, 0, 255))
                g_h = int(np.clip(58 * (0.85 + 0.15 * spec) + 50 * shine - 15 * edge_shade, 0, 255))
                b_h = int(np.clip(138 * (0.82 + 0.18 * spec) + 80 * shine - 20 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 2. Conical Hydrofoil Rostrum Snout (Streamlined beak/cone)
    # Extends forward-down from face at (46, 44) to tip at (32, 48)
    rostrum_poly = [
        (46, 42),
        (32, 48),  # Snout tip
        (46, 52)
    ]
    hd.polygon(rostrum_poly, fill=STEEL_LIGHT, outline=OUTLINE)
    # Inner gold concentric hydrofoil ring
    hd.polygon([(42, 44), (35, 48), (42, 50)], fill=GOLD_BASE)
    hd.point((32, 48), fill=WHITE_SHINE)

    # 3. Crown Dorsal Crest Fin (Aerodynamic Flow Fin)
    # Base from (54, 24) to (74, 24), rising up to crest peak at (64, 12)
    crest_poly = [(64, 12), (74, 24), (54, 24)]
    hd.polygon(crest_poly, fill=ORANGE_BASE, outline=OUTLINE)
    # Inner gold & cyan chevron
    hd.polygon([(64, 15), (71, 23), (57, 23)], fill=GOLD_BASE)
    hd.polygon([(64, 18), (68, 22), (60, 22)], fill=CYAN_BASE)

    # Dorsal crest rivets
    for ry in [14, 18, 22]:
        hd.ellipse([63, ry - 1, 65, ry + 1], fill=GOLD_DARK)

    # 4. Turret Collar Rings encircling eye sockets at (52, 40) and (76, 40)
    for ex, ey in [(52, 40), (76, 40)]:
        # Brass turret collar gear ring (radius 8..10)
        for ang in np.linspace(0, 2 * np.pi, 24):
            gx = int(ex + 8.5 * np.cos(ang))
            gy = int(ey + 8.5 * np.sin(ang))
            head_img.putpixel((gx, gy), GOLD_BASE)
        hd.ellipse([ex - 9, ey - 9, ex + 9, ey + 9], outline=OUTLINE, width=1)

    # Forehead brow visor arch
    for bx in range(48, 81):
        by = int(32 - 3.0 * np.cos((bx - 64)/16.0 * np.pi))
        head_img.putpixel((bx, by), ORANGE_BASE)
        head_img.putpixel((bx, by + 1), ORANGE_DARK)

    # Clean outline pass BEFORE hollowing eye sockets
    apply_clean_outline(head_img, ignore_regions=[(47, 35, 57, 45), (71, 35, 81, 45)])

    # 5. Strict Hollow Eye Sockets for 0-ART27 (alpha == 0 at eye zones)
    # Left eye socket at (52, 40), Right eye socket at (76, 40)
    h_arr = np.array(head_img)
    for ey, ex in [(40, 52), (40, 76)]:
        for y in range(ey - 5, ey + 6):
            for x in range(ex - 5, ex + 6):
                if (x - ex)**2 + (y - ey)**2 <= 20:
                    h_arr[y, x, :] = 0
    head_img = Image.fromarray(h_arr, "RGBA").copy()

    print("  ✓ Slice 4 Head Unit completed, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_sailfish_abyssal_knight_cuirass.png
    # Features:
    # - Abyssal Knight Cuirass (海淵深潛騎士重裝護胸甲)
    # - Double-layer reinforced cobalt blue (#1E3A8A) titanium plate (x: 44..80, y: 58..88)
    # - Ivory ceramic (#FFFDF8) and coral gold (#FFD028) embossed anchor insignia on chest
    # - Micro pressure relief valve at center (62, 68) with gold gear and white glint
    # - Streamlined shoulder pauldron plates at (44, 60) and (80, 60)
    # - 0-ART26b compliant: strictly ZERO pixels at y >= 96 (no lower legs/feet baked)
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # Cuirass Body (x: 44..80, y: 58..88)
    for y in range(58, 89):
        for x in range(44, 81):
            dx = (x - 62.0) / 18.0
            dy = (y - 72.0) / 15.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - ((x - 58)**2 + (y - 68)**2)**0.5 / 16.0)
                edge = max(0.0, (dx**2 + dy**2 - 0.4) / 0.6)
                r_c = int(np.clip(30 * (0.8 + 0.3 * spec) + 30 * spec - 10 * edge, 0, 255))
                g_c = int(np.clip(58 * (0.8 + 0.3 * spec) + 50 * spec - 15 * edge, 0, 255))
                b_c = int(np.clip(138 * (0.8 + 0.4 * spec) + 70 * spec - 20 * edge, 0, 255))
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Gold and Ivory Breastplate Trim
    for x in range(48, 77):
        costume_img.putpixel((x, 58), GOLD_BASE)
        costume_img.putpixel((x, 59), GOLD_LIGHT)
        if 46 <= x <= 78:
            costume_img.putpixel((x, 86), GOLD_BASE)
            costume_img.putpixel((x, 87), GOLD_DARK)

    # Embossed Anchor Insignia on Breastplate (center at 62, 76)
    # Vertical stock
    for y in range(72, 82):
        costume_img.putpixel((62, y), GOLD_LIGHT)
        costume_img.putpixel((61, y), GOLD_BASE)
        costume_img.putpixel((63, y), GOLD_BASE)
    # Crossbar
    for x in range(58, 67):
        costume_img.putpixel((x, 74), GOLD_LIGHT)
    # Flukes curve
    for x in range(57, 68):
        yf = int(80 + 2.0 * ((x - 62)/5.0)**2)
        if yf <= 84:
            costume_img.putpixel((x, yf), GOLD_BASE)
            costume_img.putpixel((x, yf - 1), GOLD_LIGHT)

    # Micro Pressure Relief Valve at (62, 66)
    cos_d.ellipse([58, 62, 66, 70], fill=STEEL_DARK, outline=OUTLINE)
    cos_d.ellipse([59, 63, 65, 69], fill=GOLD_BASE)
    cos_d.ellipse([61, 65, 63, 67], fill=CYAN_BASE)
    cos_d.point((62, 66), fill=WHITE_SHINE)

    # Streamlined Pauldrons at Shoulders (44, 60) and (80, 60)
    for sx in [44, 80]:
        cos_d.ellipse([sx - 4, 60 - 4, sx + 4, 60 + 4], fill=GOLD_DARK, outline=OUTLINE)
        cos_d.ellipse([sx - 2, 60 - 2, sx + 2, 60 + 2], fill=COBALT_LIGHT)
        cos_d.point((sx, 60), fill=GOLD_LIGHT)

    # Strict check: 0-ART26b compliance (no pixels at y >= 96)
    cos_arr = np.array(costume_img)
    cos_arr[96:, :, :] = 0
    costume_img = Image.fromarray(cos_arr).copy()

    apply_clean_outline(costume_img)
    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_sailfish_dual_abyssal_optic_lens.png
    # Features:
    # - Dual Abyssal Optic Lenses (雙聯深海石英同心刻度目鏡)
    # - Centers precisely aligned with head sockets: Left (52, 40), Right (76, 40)
    # - Solid lens centers (alpha=255) with sky cyan & amber starlight LEDs (0-ART27 compliant)
    # - Concentric laser rangefinder reticles and targeting crosshairs
    # - Cheerful coral pink blush LEDs at (44, 46) and (84, 46)
    # - Cute small digital mouth at (64, 48)
    # - Color richness >= 15 unique colors (0-QA31 compliant)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(core_img)

    for ecx, ecy in [(52.0, 40.0), (76.0, 40.0)]:
        # Solid circular convex quartz lens housing
        for y in range(int(ecy - 6), int(ecy + 7)):
            for x in range(int(ecx - 6), int(ecx + 7)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= 4.8:
                    norm = dist / 4.8
                    spec = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 4.0)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.2))**2 + (y - (ecy - 1.2))**2)**0.5 / 1.8)**2

                    if norm >= 0.85:
                        # Gold retaining bezel ring
                        r_o = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                        g_o = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                        b_o = int(np.clip(40 * (0.8 + 0.5 * spec), 0, 255))
                    else:
                        # Deep Sea Cyan Quartz Lens with Amber Core
                        r_o = int(np.clip(40 * (1.0 - spec) + 255 * shine, 0, 255))
                        g_o = int(np.clip(160 * (0.75 + 0.25 * spec) + 50 * shine, 0, 255))
                        b_o = int(np.clip(255 * (0.8 + 0.2 * spec), 0, 255))

                    core_img.putpixel((x, y), (r_o, g_o, b_o, 255))

        # Rangefinder crosshair reticle
        core_img.putpixel((int(ecx), int(ecy)), WHITE_SHINE)
        core_img.putpixel((int(ecx - 1), int(ecy)), GOLD_LIGHT)
        core_img.putpixel((int(ecx + 1), int(ecy)), GOLD_LIGHT)
        core_img.putpixel((int(ecx), int(ecy - 1)), GOLD_LIGHT)
        core_img.putpixel((int(ecx), int(ecy + 1)), GOLD_LIGHT)
        # Concentric dial dots at radius 3px
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3)]:
            core_img.putpixel((int(ecx + dx), int(ecy + dy)), CYAN_SHINE)

    # Coral Pink LED Blush Dots
    for bx in [44, 84]:
        cod.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=CORAL_BASE)
        cod.point((bx, 46), fill=CORAL_LIGHT)

    # Digital Mouth Indicator
    cod.line([(62, 48), (64, 49), (66, 48)], fill=OUTLINE, width=1)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_sailfish_hydrofoil_lance.png
    # Features:
    # - Hydrofoil Spiral Piercing Lance (破浪螺旋合金衝刺長槍)
    # - Held in forward hand at (36, 74) (0-MKT7 single-wield compliant)
    # - Shaft extends from rear counterweight at (54, 88) through grip (36, 74) to tip at (10, 48)
    # - Total length ~52px
    # - Three-bladed spiral tungsten steel piercing cone (三葉螺旋鎢鋼破浪錐) between (24, 60) and (10, 48)
    # - Water-reduction disc hand guard at (34, 72)
    # - Spiral vortex hydro flutes in sky cyan (#38A0FF) and gold (#FFD028)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Lance Shaft: from rear counterweight (54, 88) to cone base at (24, 60)
    for t in np.linspace(0.0, 1.0, 60):
        lx = 54.0 - t * 30.0
        ly = 88.0 - t * 28.0
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if dx**2 + dy**2 <= 2:
                    dist = (dx**2 + dy**2)**0.5
                    spec = max(0.0, 1.0 - dist / 1.5)
                    # Pearl silver tungsten shaft with gold sleeve near grip
                    is_gold_sleeve = (t > 0.45 and t < 0.70)
                    if is_gold_sleeve:
                        r_w = int(np.clip(255 * (0.85 + 0.15 * spec), 0, 255))
                        g_w = int(np.clip(208 * (0.85 + 0.15 * spec), 0, 255))
                        b_w = int(np.clip(40 * (0.85 + 0.5 * spec) + 50 * spec, 0, 255))
                    else:
                        r_w = int(np.clip(226 * (0.85 + 0.15 * spec), 0, 255))
                        g_w = int(np.clip(232 * (0.85 + 0.15 * spec), 0, 255))
                        b_w = int(np.clip(240 * (0.85 + 0.15 * spec), 0, 255))
                    weapon_img.putpixel((int(lx + dx), int(ly + dy)), (r_w, g_w, b_w, 255))

    # Rear Counterweight & Pressure Ring at (52..56, 86..90)
    wd.ellipse([51, 85, 57, 91], fill=GOLD_BASE, outline=OUTLINE)
    wd.point((54, 88), fill=WHITE_SHINE)

    # Disc Hand Guard (水滴護手盤) at (34, 72)
    wd.ellipse([30, 68, 38, 76], fill=COBALT_BASE, outline=OUTLINE)
    wd.ellipse([32, 70, 36, 74], fill=GOLD_BASE)
    wd.point((34, 72), fill=CYAN_LIGHT)

    # 2. Three-bladed Spiral Piercing Cone: from (24, 60) down to sharp tip at (10, 48)
    # The cone tapers from width ~8px at base (24, 60) down to 1px at tip (10, 48)
    cone_pts = []
    for t in np.linspace(0.0, 1.0, 40):
        cx = 24.0 - t * 14.0
        cy = 60.0 - t * 12.0
        half_w = 4.0 * (1.0 - t) + 0.5
        # Perpendicular normal
        nx = -12.0 / 18.4
        ny = 14.0 / 18.4
        for w_off in np.linspace(-half_w, half_w, int(half_w * 4 + 1)):
            px = int(round(cx + w_off * nx))
            py = int(round(cy + w_off * ny))
            if 0 <= px < W and 0 <= py < H:
                # Spiral flute pattern
                spiral_phase = (t * 8.0 + w_off) % 2.5
                if spiral_phase < 1.0:
                    weapon_img.putpixel((px, py), CYAN_BASE)
                elif spiral_phase < 1.8:
                    weapon_img.putpixel((px, py), STEEL_SHINE)
                else:
                    weapon_img.putpixel((px, py), GOLD_BASE)

    # Needle Probe Lance Tip at (10, 48)
    wd.polygon([(10, 48), (14, 49), (13, 52)], fill=GOLD_LIGHT, outline=OUTLINE)
    wd.point((10, 48), fill=WHITE_SHINE)

    # Hand Gauntlet: Armored glove gripping lance at (33..39, 71..77)
    wd.ellipse([33, 71, 39, 77], fill=IVORY_BASE, outline=OUTLINE)
    wd.point((36, 74), fill=GOLD_BASE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_sailfish_abyssal_helm_trident", key_img),
        ("back_curio", "curio_sailfish_clockwork_sailfin_mantle", curio_img),
        ("chassis", "chassis_sailfish_abyssal_titanium_default", chassis_img),
        ("costume", "costume_sailfish_abyssal_knight_cuirass", costume_img),
        ("head_unit", "head_sailfish_hydrofoil_visor_crest", head_img),
        ("optic_core", "face_sailfish_dual_abyssal_optic_lens", core_img),
        ("weapon", "weapon_sailfish_hydrofoil_lance", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{SAILFISH_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{SAILFISH_PD_DIR}/winding_key/key_sailfish_abyssal_helm_trident.png",
                    f"{KEY_DIR}/key_sailfish_abyssal_helm_trident.png")
    shutil.copyfile(f"{SAILFISH_PD_DIR}/weapon/weapon_sailfish_hydrofoil_lance.png",
                    f"{WEAPON_DIR}/weapon_sailfish_hydrofoil_lance.png")
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

    proof_comp = f"{SAILFISH_PD_DIR}/proof_paperdoll_sailfish_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{SAILFISH_PD_DIR}/proof_paperdoll_sailfish_magenta.png"
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

    strip_path = f"{SAILFISH_PD_DIR}/proof_sailfish_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/sailfish_idle_hd.png)
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
        showcase_hd.alpha_composite(sc_shadow)
        showcase_hd.alpha_composite(scaled_showcase, (sc_paste_x, sc_paste_y))

        showcase_out = f"{showcase_dir}/sailfish_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL SAILFISH CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
