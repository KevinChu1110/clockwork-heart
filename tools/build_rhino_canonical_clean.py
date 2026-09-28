#!/usr/bin/env python3
"""
build_rhino_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第三十二族 重角犀牛 (The Heavyhorn Rhino, rhino) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/world/HEAVYHORN_RHINO_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero flesh, stamped matte cast iron plates,
  dual pneumatic stamping horns with annealed golden tips, dual amber quartz observation lenses,
  crucible crosshair relief winding key, articulated steam furnace exhaust,
  crucible breaker heavy steel waraxe)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (8 canonical colors):
    1. Primary Hull: Stamped Matte Cast Iron Black (#2B2836)
    2. Secondary Trim: Quenched Refractory Obsidian Deep Purple-Black (#1F1A3A)
    3. Forge Gold & Key: Annealed Molten Gold (#FFD028)
    4. Accent & Piping: Molten Lava Warm Orange (#FFA010)
    5. Optic Core & LEDs: Amber Quartz Dial Lens (#FBBF24)
    6. Coolant & Seals: Sky Cyan / Coolant Blue (#38A0FF)
    7. Frame & Frame Screws: Cold-Rolled Titanium Steel (#4A5568 / #E2E8F0)
    8. Backing & Highlights: Ceramic White (#FFFDF8)
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28, 0-ART28r, 0-ART29, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
RHINO_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rhino"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Canon Palette Colors (The Heavyhorn Rhino Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Primary Hull: Stamped Matte Cast Iron Black (#2B2836)
IRON_BASE  = (43, 40, 54, 255)
IRON_LIGHT = (72, 68, 88, 255)
IRON_SHINE = (110, 105, 130, 255)
IRON_DARK  = (28, 26, 36, 255)
IRON_DEEP  = (18, 16, 24, 255)

# 2. Forge Gold & Winding Key (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 3. Molten Lava Warm Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 235, 160, 255)
ORANGE_DARK  = (190, 105, 8, 255)
ORANGE_DEEP  = (130, 68, 5, 255)

# 4. Amber Quartz Optic Lens (#FBBF24)
AMBER_BASE  = (251, 191, 36, 255)
AMBER_LIGHT = (254, 220, 110, 255)
AMBER_SHINE = (255, 245, 180, 255)
AMBER_DARK  = (210, 140, 15, 255)
AMBER_DEEP  = (150, 90, 8, 255)

# 5. Coolant Sky Blue / Seals & Indicators (#38A0FF)
COOLANT_BASE  = (56, 160, 255, 255)
COOLANT_LIGHT = (120, 205, 255, 255)
COOLANT_SHINE = (195, 235, 255, 255)
COOLANT_DARK  = (24, 105, 195, 255)
COOLANT_DEEP  = (14, 60, 130, 255)

# 6. Mint Green: Pressure Safe Indicators (#4ED86A)
MINT_BASE  = (78, 216, 106, 255)
MINT_LIGHT = (128, 238, 150, 255)
MINT_SHINE = (185, 255, 200, 255)
MINT_DARK  = (42, 160, 68, 255)
MINT_DEEP  = (24, 110, 44, 255)

# 7. Ceramic White: Chest Anvil Plate (#FFFDF8)
CERAMIC_BASE  = (255, 253, 248, 255)
CERAMIC_LIGHT = (255, 255, 255, 255)
CERAMIC_SHADE = (228, 222, 212, 255)
CERAMIC_DARK  = (195, 188, 175, 255)

# 8. Frame & Tungsten: Cold-Rolled Steel (#4A5568 / #E2E8F0)
STEEL_BASE  = (74, 85, 104, 255)
STEEL_LIGHT = (120, 135, 155, 255)
STEEL_SHINE = (180, 195, 215, 255)
STEEL_DARK  = (45, 55, 72, 255)
STEEL_DEEP  = (26, 32, 42, 255)

# 9. Coral Pink Blush Sensors (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
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
    print("=== BUILDING 100% MODULAR CANONICAL HEAVYHORN RHINO SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_rhino_crucible_crosshair_key.png
    # Crucible Crosshair Relief Winding Key (熔爐十字洩壓發條鑰匙)
    # Socket boss at spine (64, 58), shaft extends diagonally up-right to (88, 24)
    # Protrudes clearly beyond head silhouette (x: 74..104, y: 10..38)
    # Features:
    # - Solid brass & cast iron shaft with radial bevel shading
    # - Crosshair winged hub with 4 arms (N, S, E, W) and polished spherical end knobs
    # - Central obsidian bearing & miniature sky blue relief valve pointer
    # - STRICTLY transparent corners (0-ART29 compliant)
    # - Zero dark background card / strip (0-ART29 compliant: dark < 260px, max_run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key shaft from (64, 58) to (88, 24)
    for t in np.linspace(0.0, 1.0, 50):
        sx = 64.0 + t * 24.0
        sy = 58.0 - t * 34.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    r_s = int(np.clip(255 * (0.8 + 0.25 * spec), 0, 255))
                    g_s = int(np.clip(208 * (0.8 + 0.25 * spec), 0, 255))
                    b_s = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * spec, 0, 255))
                    key_img.putpixel((int(sx + dx), int(sy + dy)), (r_s, g_s, b_s, 255))

    # Base socket collar at spine (64, 58)
    kd.ellipse([64 - 5, 58 - 5, 64 + 5, 58 + 5], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([64 - 3, 58 - 3, 64 + 3, 58 + 3], fill=GOLD_BASE)
    kd.ellipse([64 - 1, 58 - 1, 64 + 1, 58 + 1], fill=COOLANT_BASE)

    # 2. Crosshair Hub at (88, 24)
    kcx, kcy = 88.0, 24.0
    r_hub = 10.0

    # Draw outer reinforcement ring connecting crosshair arms
    r_outer = 9.5
    r_inner = 6.5
    for y in range(int(kcy - r_outer - 2), int(kcy + r_outer + 3)):
        for x in range(int(kcx - r_outer - 2), int(kcx + r_outer + 3)):
            dist = ((x - kcx)**2 + (y - kcy)**2)**0.5
            if r_inner <= dist <= r_outer:
                norm_r = (dist - r_inner) / (r_outer - r_inner)
                spec = max(0.0, np.sin(norm_r * np.pi))
                shine = max(0.0, 1.0 - ((x - (kcx - 2.5))**2 + (y - (kcy - 2.5))**2)**0.5 / 5.0)**2
                r_w = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                g_w = int(np.clip(208 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                b_w = int(np.clip(40 * (0.8 + 0.5 * spec) + 50 * shine, 0, 255))
                key_img.putpixel((x, y), (r_w, g_w, b_w, 255))

    # Four Crosshair Arms (N, S, W, E)
    arm_defs = [
        (0.0, -11.0, 3.5, 6.0),   # North
        (0.0, 11.0, 3.5, 6.0),    # South
        (-11.0, 0.0, 6.0, 3.5),   # West
        (11.0, 0.0, 6.0, 3.5),    # East
    ]
    for vx, vy, rx, ry in arm_defs:
        vcx = kcx + vx
        vcy = kcy + vy
        for y in range(int(vcy - ry - 1), int(vcy + ry + 2)):
            for x in range(int(vcx - rx - 1), int(vcx + rx + 2)):
                if ((x - vcx)/rx)**2 + ((y - vcy)/ry)**2 <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (vcx - 1.2))**2 + (y - (vcy - 1.2))**2)**0.5 / 4.0)
                    r_v = int(np.clip(255 * (0.85 + 0.25 * spec), 0, 255))
                    g_v = int(np.clip(208 * (0.85 + 0.25 * spec), 0, 255))
                    b_v = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
                    key_img.putpixel((x, y), (r_v, g_v, b_v, 255))

        # Spherical Thermal Knob at end of each arm
        tx = int(round(kcx + vx * 1.25))
        ty = int(round(kcy + vy * 1.25))
        kd.ellipse([tx - 2, ty - 2, tx + 2, ty + 2], fill=ORANGE_BASE, outline=OUTLINE_KEY)
        kd.ellipse([tx - 1, ty - 1, tx + 1, ty + 1], fill=GOLD_LIGHT)
        kd.point((tx, ty), fill=WHITE_SHINE)

    # Central Bearing Boss & Relief Valve Dial
    kd.ellipse([int(kcx - 5), int(kcy - 5), int(kcx + 5), int(kcy + 5)], fill=IRON_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(kcx - 4), int(kcy - 4), int(kcx + 4), int(kcy + 4)], fill=GOLD_BASE)
    kd.ellipse([int(kcx - 2), int(kcy - 2), int(kcx + 2), int(kcy + 2)], fill=IRON_BASE)

    # Miniature Sky Blue Relief Pointer at 45 degrees
    kd.line([(int(kcx), int(kcy)), (int(kcx + 3), int(kcy - 3))], fill=COOLANT_LIGHT, width=1)
    kd.point((int(kcx), int(kcy)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY)

    # Strict check: 0-ART29 corners transparent
    for cy, cx in [(0, 0), (0, 127), (127, 0), (127, 127)]:
        key_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_rhino_steam_furnace_exhaust.png
    # Articulated Steam Furnace Exhaust & Tail (多管連動發條蒸汽排煙爐與發條配重短尾)
    # Features:
    # - Back furnace pack boiler at (44..60, 46..64)
    # - Three stepped vertical brass exhaust pipes rising from boiler:
    #     Pipe 1 (left):   x=36, y: 52..28 (h=24px, w=5px)
    #     Pipe 2 (middle): x=44, y: 48..20 (h=28px, w=6px)
    #     Pipe 3 (right):  x=52, y: 44..14 (h=30px, w=6px)
    # - Flared brass pipe rims with lava orange (#FFA010) pressure collars
    # - Soft round puffy steam puffs (#FFFDF8 with soft blue-grey shading)
    # - Pressure dial on furnace flank with mint green / sky blue needle
    # - Short articulated heavy metal tail at (46, 92) curving to (38, 102) with counterweight
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # 1. Back Furnace Boiler Pack (x: 44..60, y: 48..66)
    for fy in range(48, 67):
        for fx in range(44, 61):
            spec = max(0.0, 1.0 - ((fx - 52.0)**2 + (fy - 56.0)**2)**0.5 / 10.0)
            r_b = int(np.clip(43 * (0.8 + 0.45 * spec) + 25 * spec, 0, 255))
            g_b = int(np.clip(40 * (0.8 + 0.45 * spec) + 25 * spec, 0, 255))
            b_b = int(np.clip(54 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            curio_img.putpixel((fx, fy), (r_b, g_b, b_b, 255))

    # Boiler rivets & heat grille slots
    cd.rectangle([46, 52, 58, 64], outline=IRON_DEEP, fill=None)
    for rx in [46, 58]:
        for ry in [52, 58, 64]:
            cd.point((rx, ry), fill=GOLD_BASE)

    # 2. Three Stepped Vertical Brass Exhaust Pipes
    pipe_specs = [
        (36, 52, 28, 5, "left"),
        (44, 48, 20, 6, "mid"),
        (52, 44, 14, 6, "right")
    ]
    for px, py_bottom, py_top, pw, name in pipe_specs:
        half_w = pw // 2
        for py in range(py_top, py_bottom + 1):
            for x_off in range(-half_w, half_w + 1):
                cur_x = px + x_off
                norm_w = abs(x_off) / float(half_w)
                spec = max(0.0, 1.0 - norm_w)
                shine = max(0.0, 1.0 - abs(x_off - (-1)) / 2.0)**2

                # Brass cylinder shading with orange heat bands
                is_band = (py in range(py_top + 4, py_top + 8))
                if is_band:
                    r_p = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    g_p = int(np.clip(160 * (0.8 + 0.3 * spec) + 30 * shine, 0, 255))
                    b_p = int(np.clip(16 * (0.8 + 0.5 * spec) + 40 * shine, 0, 255))
                else:
                    r_p = int(np.clip(255 * (0.75 + 0.35 * spec) + 45 * shine, 0, 255))
                    g_p = int(np.clip(208 * (0.75 + 0.35 * spec) + 45 * shine, 0, 255))
                    b_p = int(np.clip(40 * (0.75 + 0.45 * spec) + 60 * shine, 0, 255))

                curio_img.putpixel((cur_x, py), (r_p, g_p, b_p, 255))

        # Flared Collar Lip at top
        cd.ellipse([px - half_w - 1, py_top - 2, px + half_w + 1, py_top + 2], fill=GOLD_LIGHT, outline=OUTLINE)
        cd.ellipse([px - half_w, py_top - 1, px + half_w, py_top + 1], fill=IRON_DEEP)

    # 3. Soft Puffy Steam Clouds Escaping Top of Pipes
    steam_puffs = [
        (34.0, 22.0, 5.0, 4.0),
        (42.0, 13.0, 6.0, 5.0),
        (52.0, 7.0, 7.0, 6.0),
    ]
    for scx, scy, srx, sry in steam_puffs:
        for y in range(int(scy - sry - 1), int(scy + sry + 2)):
            for x in range(int(scx - srx - 1), int(scx + srx + 2)):
                dx = (x - scx) / srx
                dy = (y - scy) / sry
                dist_sq = dx**2 + dy**2
                if dist_sq <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (scx - 1.5))**2 + (y - (scy - 1.5))**2)**0.5 / (srx * 1.2))
                    # Soft white/ivory puff with pale sky blue shadow
                    r_sm = int(np.clip(255 * (0.9 + 0.1 * spec), 0, 255))
                    g_sm = int(np.clip(253 * (0.9 + 0.1 * spec), 0, 255))
                    b_sm = int(np.clip(248 * (0.85 + 0.25 * spec) + 30 * (1.0 - spec), 0, 255))
                    a_sm = int(np.clip(240 * (1.0 - 0.4 * dist_sq), 0, 255))
                    curio_img.putpixel((x, y), (r_sm, g_sm, b_sm, a_sm))

    # 4. Flank Pressure Gauge at (38, 60)
    cd.ellipse([34, 56, 42, 64], fill=GOLD_BASE, outline=OUTLINE)
    cd.ellipse([35, 57, 41, 63], fill=CERAMIC_BASE)
    cd.line([(38, 60), (40, 58)], fill=MINT_BASE, width=1)
    cd.point((38, 60), fill=COOLANT_BASE)

    # 5. Articulated Short Counterweight Tail at Sacrum (46, 92) -> (36, 102)
    tail_pts = [
        (46.0, 92.0, 4.0, 3.5),
        (41.0, 97.0, 3.5, 3.0),
        (36.0, 102.0, 4.5, 4.0),  # End counterweight bulb
    ]
    for i in range(len(tail_pts) - 1):
        (x0, y0, _, _), (x1, y1, _, _) = tail_pts[i], tail_pts[i+1]
        for t in np.linspace(0.0, 1.0, 15):
            bx = x0 + t * (x1 - x0)
            by = y0 + t * (y1 - y0)
            for dx in range(-2, 3):
                for dy in range(-2, 3):
                    if dx**2 + dy**2 <= 4:
                        curio_img.putpixel((int(bx + dx), int(by + dy)), IRON_BASE)

    for scx, scy, srx, sry in tail_pts:
        for y in range(int(scy - sry - 1), int(scy + sry + 2)):
            for x in range(int(scx - srx - 1), int(scx + srx + 2)):
                if ((x - scx)/srx)**2 + ((y - scy)/sry)**2 <= 1.0:
                    spec = max(0.0, 1.0 - ((x - (scx - 1.0))**2 + (y - (scy - 1.0))**2)**0.5 / srx)
                    r_t = int(np.clip(43 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                    g_t = int(np.clip(40 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                    b_t = int(np.clip(54 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                    curio_img.putpixel((x, y), (r_t, g_t, b_t, 255))
        cd.point((int(scx), int(scy)), fill=GOLD_BASE)

    apply_clean_outline(curio_img)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_rhino_molten_iron_default.png
    # Heavyhorn Rhino Cast Iron Chassis (重角犀牛熔鑄粗鐵素體)
    # Features:
    # - 2.2 Chibi low-center-of-gravity cast iron chassis
    # - Soft ground contact shadow at (64, 116)
    # - Heavy cylindrical cast iron legs and boots with graphite soles at (45, 113) and (73, 113)
    # - Solid neck collar at (x: 52..76, y: 46..58) for seamless head seating (zero holes)
    # - Stamped matte cast iron hull (#2B2836) with molten warm gold rivets
    # - Ivory/ceramic white (#FFFDF8) chest anvil backing plate with geothermal amber core
    # - Left hand clenched low at (38, 78) with knuckle armor
    # - Right arm tucked at ribs with weapon grip joint at (82, 72)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 34, 116 - 5, 64 + 34, 116 + 6], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Heavy Cast Iron Mechanical Boots with Graphite Soles
    boot_pos = [(45.0, 113.0), (73.0, 113.0)]
    for bx, by in boot_pos:
        # Sole plate (graphite ceramic)
        ch_d.ellipse([int(bx - 9), int(by - 3), int(bx + 9), int(by + 3)], fill=STEEL_DEEP, outline=OUTLINE)
        # Upper boot cap (cast iron)
        ch_d.ellipse([int(bx - 7), int(by - 2), int(bx + 7), int(by + 2)], fill=IRON_BASE)
        ch_d.ellipse([int(bx - 5), int(by - 1), int(bx + 5), int(by + 2)], fill=IRON_LIGHT)
        # Steel toe cap reinforcement
        ch_d.line([(int(bx - 5), int(by + 1)), (int(bx + 5), int(by + 1))], fill=STEEL_SHINE, width=1)
        ch_d.point((int(bx), int(by)), fill=WHITE_SHINE)

    # 3. Thick Articulated Legs with Coolant Blue Gasket Rings
    leg_paths = [
        ((45.0, 112.0), (52.0, 88.0)),
        ((73.0, 112.0), (68.0, 88.0))
    ]
    for (lx0, ly0), (lx1, ly1) in leg_paths:
        for t in np.linspace(0.0, 1.0, 26):
            lx = lx0 + t * (lx1 - lx0)
            ly = ly0 - t * (ly0 - ly1)
            for dx in range(-6, 7):
                spec = max(0.0, 1.0 - abs(dx) / 6.0)
                r_l = int(np.clip(43 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                g_l = int(np.clip(40 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                b_l = int(np.clip(54 * (0.8 + 0.45 * spec) + 45 * spec, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r_l, g_l, b_l, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        ch_d.ellipse([mid_x - 4, mid_y - 2, mid_x + 4, mid_y + 2], fill=COOLANT_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=WHITE_SHINE)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 52..76, y: 46..58)
    for ny in range(46, 59):
        for nx in range(52, 77):
            spec = max(0.0, 1.0 - abs(nx - 64.0) / 12.0)
            r_n = int(np.clip(43 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            g_n = int(np.clip(40 * (0.8 + 0.45 * spec) + 30 * spec, 0, 255))
            b_n = int(np.clip(54 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
            chassis_img.putpixel((nx, ny), (r_n, g_n, b_n, 255))

    # 5. Torso Body Shell (x: 40..88, y: 56..98)
    cx_t, cy_t = 64.0, 78.0
    for y in range(56, 99):
        for x in range(40, 89):
            dx = (x - cx_t) / 22.0
            dy = (y - cy_t) / 20.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 22.0)
                shine = max(0.0, 1.0 - ((x - (cx_t - 5))**2 + (y - (cy_t - 5))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                # Ceramic white shock-absorbing chest anvil plate
                is_chest_plate = ((x - 64.0)**2 / 12.0**2 + (y - 77.0)**2 / 13.0**2 <= 1.0)
                if is_chest_plate:
                    r_t = int(np.clip(255 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    g_t = int(np.clip(253 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                    b_t = int(np.clip(248 * (0.88 + 0.2 * spec) - 40 * edge_shade + 20 * shine, 0, 255))
                else:
                    # Outer cast iron shell with warm gold trim
                    is_rim = dist_sq >= 0.75
                    if is_rim:
                        r_t = int(np.clip(255 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        g_t = int(np.clip(208 * (0.8 + 0.3 * spec) + 30 * shine - 20 * edge_shade, 0, 255))
                        b_t = int(np.clip(40 * (0.8 + 0.4 * spec) + 35 * shine - 10 * edge_shade, 0, 255))
                    else:
                        r_t = int(np.clip(43 * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                        g_t = int(np.clip(40 * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                        b_t = int(np.clip(54 * (0.8 + 0.45 * spec) + 45 * shine - 15 * edge_shade, 0, 255))

                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    # Glowing Amber Geothermal Core on chest (x: 64, y: 77)
    ch_d.ellipse([64 - 5, 77 - 5, 64 + 5, 77 + 5], fill=ORANGE_DARK, outline=OUTLINE)
    ch_d.ellipse([64 - 4, 77 - 4, 64 + 4, 77 + 4], fill=AMBER_BASE)
    ch_d.ellipse([64 - 2, 77 - 2, 64 + 2, 77 + 2], fill=AMBER_LIGHT)
    ch_d.point((63, 76), fill=WHITE_SHINE)

    # 6. Left Arm: Curved at waist, clenched fist with knuckle armor at (38, 78)
    left_arm_pts = [
        ((46.0, 68.0), (38.0, 78.0))
    ]
    for (ax0, ay0), (ax1, ay1) in left_arm_pts:
        for t in np.linspace(0.0, 1.0, 20):
            ax = ax0 + t * (ax1 - ax0)
            ay = ay0 + t * (ay1 - ay0)
            for dx in range(-4, 5):
                for dy in range(-4, 5):
                    if dx**2 + dy**2 <= 16:
                        spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 4.0)
                        r_a = int(np.clip(43 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        g_a = int(np.clip(40 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        b_a = int(np.clip(54 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                        chassis_img.putpixel((int(ax + dx), int(ay + dy)), (r_a, g_a, b_a, 255))
    ch_d.ellipse([34, 74, 42, 82], fill=STEEL_BASE, outline=OUTLINE)
    ch_d.ellipse([36, 76, 40, 80], fill=GOLD_BASE)
    ch_d.point((38, 78), fill=WHITE_SHINE)

    # 7. Right Arm: Tucked at ribs, ending at (82, 72)
    # STRICT 0-ART9/11: Right arm must not exceed x=93!
    for t in np.linspace(0.0, 1.0, 20):
        rax = 78.0 + t * 4.0
        ray = 66.0 + t * 6.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    px = int(rax + dx)
                    py = int(ray + dy)
                    if px < 94:
                        spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 4.0)
                        r_a = int(np.clip(43 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        g_a = int(np.clip(40 * (0.8 + 0.45 * spec) + 35 * spec, 0, 255))
                        b_a = int(np.clip(54 * (0.8 + 0.45 * spec) + 40 * spec, 0, 255))
                        chassis_img.putpixel((px, py), (r_a, g_a, b_a, 255))

    # Right wrist ball joint at (82, 72)
    ch_d.ellipse([79, 69, 85, 75], fill=COOLANT_BASE, outline=OUTLINE)
    ch_d.point((82, 72), fill=WHITE_SHINE)

    # Strict clamp to x < 94 to ensure 0-ART9/11 compliance
    for cy in range(H):
        for cx in range(94, W):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    apply_clean_outline(chassis_img)

    # Ensure zero pixels at x >= 94 again after outline
    for cy in range(H):
        for cx in range(94, W):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 3 Chassis completed, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_rhino_crucible_battering_crest.png
    # Features:
    # - Crucible Battering Crest / Heavyhorn Helmet (鍛爐衝壓雙重撞角頭盔)
    # - Full cast iron helmet (38..90, 16..58)
    # - Dual pneumatic horns:
    #   - Main four-sided pyramid stamping horn:
    #     Base at nose bridge (64, 26), extends up-forward to sharp tip at (64, 6)
    #     Annealed golden tip (#FFD028) with heat dissipation slots
    #   - Secondary forehead horn behind main horn at (64, 16..22)
    # - Cheeks and brow with stamped cast iron plates and orange hazard bevels
    # - Brass ear valve resonance bosses at (40, 42) and (88, 42)
    # - STRICT 0-ART27:
    #   Left eye socket at (52, 40) MUST BE HOLLOW (alpha=0 at x in [51, 53], y in [39, 41])
    #   Right eye socket at (76, 40) MUST BE HOLLOW (alpha=0 at x in [75, 77], y in [39, 41])
    #   Heavy brass cog bezel encircling sockets!
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    # 1. Main Helmet Dome & Cheek Guards (x: 40..88, y: 20..58)
    cx_h, cy_h = 64.0, 36.0
    for y in range(20, 52):
        for x in range(40, 89):
            dx = (x - cx_h) / 22.0
            dy = (y - cy_h) / 16.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 20.0)
                shine = max(0.0, 1.0 - ((x - (cx_h - 4))**2 + (y - (cy_h - 4))**2)**0.5 / 6.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_h = int(np.clip(43 * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                g_h = int(np.clip(40 * (0.8 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))
                b_h = int(np.clip(54 * (0.8 + 0.45 * spec) + 45 * shine - 15 * edge_shade, 0, 255))
                head_img.putpixel((x, y), (r_h, g_h, b_h, 255))

    # 2. Snout Base Plate at (54..74, 46..57)
    for y in range(46, 58):
        for x in range(54, 75):
            dx = (x - 64.0) / 10.0
            dy = (y - 51.0) / 6.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - abs(x - 64.0) / 10.0)
                r_sn = int(np.clip(43 * (0.85 + 0.3 * spec) + 20 * spec, 0, 255))
                g_sn = int(np.clip(40 * (0.85 + 0.3 * spec) + 20 * spec, 0, 255))
                b_sn = int(np.clip(54 * (0.85 + 0.3 * spec) + 25 * spec, 0, 255))
                head_img.putpixel((x, y), (r_sn, g_sn, b_sn, 255))

    # Snout nostrils/slits
    hd.ellipse([56, 53, 59, 55], fill=IRON_DEEP)
    hd.ellipse([69, 53, 72, 55], fill=IRON_DEEP)

    # 3. Brow Armor Band & Lava Orange Warning Strips (y: 28..31)
    for bx in range(44, 85):
        head_img.putpixel((bx, 29), ORANGE_BASE)
        head_img.putpixel((bx, 30), GOLD_BASE)

    # 4. Ear Valve Resonance Bosses at (40, 42) and (88, 42)
    for ex in [40, 88]:
        hd.ellipse([ex - 5, 42 - 5, ex + 5, 42 + 5], fill=IRON_DARK, outline=OUTLINE)
        hd.ellipse([ex - 4, 42 - 4, ex + 4, 42 + 4], fill=GOLD_BASE)
        hd.ellipse([ex - 2, 42 - 2, ex + 2, 42 + 2], fill=COOLANT_BASE)
        hd.point((ex, 42), fill=WHITE_SHINE)

    # 5. Eye Bezel Rings (surrounding eye sockets)
    for ecx in [52.0, 76.0]:
        for y in range(35, 46):
            for x in range(int(ecx - 5), int(ecx + 6)):
                dist = ((x - ecx)**2 + (y - 40.0)**2)**0.5
                if 2.5 <= dist <= 5.5:
                    head_img.putpixel((x, y), GOLD_BASE)

    # 6. DUAL PNEUMATIC STAMPING HORNS (DRAWN ON TOP OF HELMET & SNOUT)
    # ── (A) Forehead Crown Horn (Upper Horn: y=2..16) ──
    for y in range(2, 17):
        t = (16 - y) / 14.0   # 0 at base (y=16), 1 at tip (y=2)
        half_w = 6.0 * (1.0 - t) + 0.8
        for x in range(int(round(64.0 - half_w)), int(round(64.0 + half_w + 1))):
            norm_x = (x - 64.0) / half_w if half_w > 0 else 0.0
            spec = max(0.0, 1.0 - abs(norm_x))
            is_gold_tip = (t >= 0.45)
            if is_gold_tip:
                r_hn = int(np.clip(255 * (0.85 + 0.15 * spec), 0, 255))
                g_hn = int(np.clip(208 * (0.85 + 0.15 * spec), 0, 255))
                b_hn = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
            else:
                is_ridge = abs(norm_x) < 0.25
                if is_ridge:
                    r_hn = int(np.clip(72 * (0.9 + 0.2 * spec), 0, 255))
                    g_hn = int(np.clip(68 * (0.9 + 0.2 * spec), 0, 255))
                    b_hn = int(np.clip(88 * (0.9 + 0.2 * spec), 0, 255))
                else:
                    r_hn = int(np.clip(43 * (0.8 + 0.4 * spec), 0, 255))
                    g_hn = int(np.clip(40 * (0.8 + 0.4 * spec), 0, 255))
                    b_hn = int(np.clip(54 * (0.8 + 0.4 * spec), 0, 255))
            head_img.putpixel((x, y), (r_hn, g_hn, b_hn, 255))
    hd.point((64, 2), fill=WHITE_SHINE)

    # ── (B) Nasal Snout Horn (Lower Protruding Rhino Horn: y=26..52) ──
    # Prominently rooted on the snout, rising to a sharp golden point at (64, 26)
    for y in range(26, 53):
        t = (52 - y) / 26.0   # 0 at base (y=52), 1 at tip (y=26)
        half_w = 5.5 * (1.0 - t) + 0.8
        for x in range(int(round(64.0 - half_w)), int(round(64.0 + half_w + 1))):
            norm_x = (x - 64.0) / half_w if half_w > 0 else 0.0
            spec = max(0.0, 1.0 - abs(norm_x))
            is_gold_tip = (t >= 0.55)
            if is_gold_tip:
                r_hn = int(np.clip(255 * (0.88 + 0.12 * spec), 0, 255))
                g_hn = int(np.clip(208 * (0.88 + 0.12 * spec), 0, 255))
                b_hn = int(np.clip(40 * (0.85 + 0.4 * spec) + 40 * spec, 0, 255))
            else:
                is_ridge = abs(norm_x) < 0.25
                if is_ridge:
                    r_hn = int(np.clip(72 * (0.9 + 0.2 * spec), 0, 255))
                    g_hn = int(np.clip(68 * (0.9 + 0.2 * spec), 0, 255))
                    b_hn = int(np.clip(88 * (0.9 + 0.2 * spec), 0, 255))
                else:
                    r_hn = int(np.clip(43 * (0.8 + 0.45 * spec), 0, 255))
                    g_hn = int(np.clip(40 * (0.8 + 0.45 * spec), 0, 255))
                    b_hn = int(np.clip(54 * (0.8 + 0.45 * spec), 0, 255))
            head_img.putpixel((x, y), (r_hn, g_hn, b_hn, 255))

    # Golden tip point highlight on nasal horn
    hd.point((64, 26), fill=WHITE_SHINE)

    # Outline contour on nasal horn edges to ensure it pops out from the snout
    for y in range(26, 53):
        t = (52 - y) / 26.0
        half_w = 5.5 * (1.0 - t) + 0.8
        lx = int(round(64.0 - half_w)) - 1
        rx = int(round(64.0 + half_w + 1))
        if 0 <= lx < W:
            head_img.putpixel((lx, y), OUTLINE)
        if 0 <= rx < W:
            head_img.putpixel((rx, y), OUTLINE)
    # Cap at base of nasal horn
    for x in range(58, 71):
        head_img.putpixel((x, 52), OUTLINE)

    # 7. STRICT 0-ART27 HOLLOW EYE SOCKETS
    # Inner eye socket centers MUST be completely transparent (alpha = 0)
    # for optic_core to shine through without clipping / double face artifact
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
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_rhino_crucible_smith_plate.png
    # Features:
    # - Crucible Smith Plate / Fireproof Battering Cuirass (熔火鍛造重裝護胸甲)
    # - Heavy curved breastplate covering (44..84, 56..92)
    # - Central embossed golden anvil crest (GOLD_BASE) on chest
    # - Dual diagonal lava orange (#FFA010) hazard stripes
    # - Paired heavy curved pauldrons at left (36..46, 56..68) and right (76..88, 56..68)
    # - STRICT 0-ART26b: Lower leg zone y >= 96 strictly ZERO pixels!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(costume_img)

    # 1. Breastplate Curved Hull (x: 44..84, y: 56..92)
    for y in range(56, 93):
        for x in range(44, 85):
            dx = (x - 64.0) / 19.0
            dy = (y - 74.0) / 17.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 18.0)
                shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 5.0)**2
                edge_shade = max(0.0, (dist_sq - 0.45) / 0.55)

                r_c = int(np.clip(43 * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                g_c = int(np.clip(40 * (0.75 + 0.45 * spec) + 35 * shine - 15 * edge_shade, 0, 255))
                b_c = int(np.clip(54 * (0.75 + 0.45 * spec) + 40 * shine - 15 * edge_shade, 0, 255))

                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 2. Golden Anvil Crest in Center of Breastplate (58..70, 68..78)
    # Anvil flat top:
    cd.rectangle([58, 68, 70, 71], fill=GOLD_BASE, outline=OUTLINE)
    # Anvil waist & horn:
    cd.polygon([(60, 71), (68, 71), (67, 75), (61, 75)], fill=GOLD_LIGHT)
    # Anvil base:
    cd.rectangle([59, 75, 69, 78], fill=GOLD_DARK, outline=OUTLINE)
    cd.point((64, 69), fill=WHITE_SHINE)

    # 3. Dual Lava Orange Hazard Stripes across lower breastplate (y: 82..88)
    for x in range(48, 81):
        if (x + 82) % 8 < 4:
            costume_img.putpixel((x, 83), ORANGE_BASE)
            costume_img.putpixel((x, 84), ORANGE_LIGHT)
            costume_img.putpixel((x, 85), ORANGE_BASE)

    # 4. Shoulder Pauldrons (Left: 36..46, 56..68; Right: 76..88, 56..68)
    pauldrons = [(41.0, 62.0), (81.0, 62.0)]
    for px, py in pauldrons:
        cd.ellipse([int(px - 7), int(py - 6), int(px + 7), int(py + 6)], fill=IRON_LIGHT, outline=OUTLINE)
        cd.ellipse([int(px - 5), int(py - 4), int(px + 5), int(py + 4)], fill=GOLD_BASE)
        cd.ellipse([int(px - 3), int(py - 2), int(px + 3), int(py + 2)], fill=IRON_DARK)
        cd.point((int(px), int(py)), fill=WHITE_SHINE)

    # Brass Rivets along armor trim
    for rx, ry in [(46, 60), (82, 60), (48, 90), (80, 90), (64, 91)]:
        cd.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=GOLD_BASE, outline=OUTLINE)

    # Collar Neck Guard Flange at (56..72, 54..58)
    cd.rounded_rectangle([56, 54, 72, 58], radius=2, fill=IRON_LIGHT, outline=OUTLINE)
    cd.line([(58, 56), (70, 56)], fill=COOLANT_BASE, width=1)

    # STRICT 0-ART26b: Lower leg zone y >= 96 strictly ZERO pixels!
    for cy in range(96, H):
        for cx in range(W):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    apply_clean_outline(costume_img)

    # Re-enforce y >= 96 zero pixels after outline
    for cy in range(96, H):
        for cx in range(W):
            costume_img.putpixel((cx, cy), (0, 0, 0, 0))

    print("  ✓ Slice 5 Costume completed, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/face_rhino_dual_amber_pyro_optic.png
    # Features:
    # - Dual Amber Quartz Pyro Optic Lenses (雙聯琥珀金石英觀火目鏡)
    # - Left lens centered at (52, 40)
    # - Right lens centered at (76, 40)
    # - Precision convex lens shading in amber quartz (#FBBF24 / #FFA010)
    # - Reticle temperature lines, specular white highlight, mint green status LEDs
    # - Coral pink blush sensor dots at (44, 46) and (84, 46)
    # - Digital smile/vent indicator at (62..66, 49)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(core_img)

    for ecx in [52.0, 76.0]:
        ecy = 40.0
        r_lens = 3.8
        for y in range(int(ecy - r_lens - 1), int(ecy + r_lens + 2)):
            for x in range(int(ecx - r_lens - 1), int(ecx + r_lens + 2)):
                dist = ((x - ecx)**2 + (y - ecy)**2)**0.5
                if dist <= r_lens:
                    norm_d = dist / r_lens
                    spec = max(0.0, 1.0 - norm_d)
                    shine = max(0.0, 1.0 - ((x - (ecx - 1.0))**2 + (y - (ecy - 1.0))**2)**0.5 / 2.0)**2

                    r_e = int(np.clip(251 * (0.85 + 0.15 * spec) + 50 * shine, 0, 255))
                    g_e = int(np.clip(191 * (0.85 + 0.15 * spec) + 50 * shine, 0, 255))
                    b_e = int(np.clip(36 * (0.85 + 0.5 * spec) + 60 * shine, 0, 255))

                    core_img.putpixel((x, y), (r_e, g_e, b_e, 255))

        # Precision Specular White Glint
        core_img.putpixel((int(ecx - 1), int(ecy - 1)), WHITE_SHINE)
        core_img.putpixel((int(ecx), int(ecy - 1)), WHITE_SHINE)

        # Concentric reticle crosshair indicator
        core_img.putpixel((int(ecx), int(ecy)), AMBER_DEEP)

        # Mint Green Status LED at upper-outer corner
        led_x = int(ecx - 2 if ecx < 64 else ecx + 2)
        core_img.putpixel((led_x, int(ecy - 2)), MINT_LIGHT)

    # Coral Pink Blush Sensor Dots
    for bx in [44, 84]:
        cod.ellipse([bx - 2, 46 - 1, bx + 2, 46 + 1], fill=CORAL_BASE)
        cod.point((bx, 46), fill=CORAL_LIGHT)

    # Digital Mouth Indicator
    cod.line([(62, 49), (64, 50), (66, 49)], fill=OUTLINE, width=1)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_rhino_crucible_breaker_axe.png
    # Features:
    # - Crucible Breaker Heavy Steel Waraxe (熔爐破陣重鋼戰斧)
    # - Single-wield compliant (0-MKT7): held in forward right hand gauntlet at (78, 72)
    # - Shaft: reinforced steel handle from pommel at (70, 94) through grip (78, 72) to axe head at (90, 48)
    # - Heavy Golden Counterweight Pommel at butt (70, 94) with pressure ring
    # - Axe Head at (90, 48):
    #   - Massive crescent single-edged blade spanning x: 94..114, y: 32..64
    #   - Dark obsidian quenched steel body (#1F1A3A / #2B2836)
    #   - Molten annealed gold cutting edge (#FFD028)
    #   - Three circular steam relief vent holes in blade face
    #   - Rear flat pneumatic stamping hammer block at x: 80..90, y: 44..52
    # - Armored right gauntlet gripping shaft at (75..81, 69..75)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)

    # 1. Shaft: from pommel (70, 94) to axe head (90, 48)
    for t in np.linspace(0.0, 1.0, 60):
        sx = 70.0 + t * 20.0
        sy = 94.0 - t * 46.0
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                if dx**2 + dy**2 <= 4:
                    spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5 / 2.0)
                    is_sleeve = (0.45 <= t <= 0.70)
                    if is_sleeve:
                        r_w = int(np.clip(255 * (0.85 + 0.15 * spec), 0, 255))
                        g_w = int(np.clip(208 * (0.85 + 0.15 * spec), 0, 255))
                        b_w = int(np.clip(40 * (0.85 + 0.5 * spec) + 50 * spec, 0, 255))
                    else:
                        r_w = int(np.clip(74 * (0.85 + 0.25 * spec) + 40 * spec, 0, 255))
                        g_w = int(np.clip(85 * (0.85 + 0.25 * spec) + 40 * spec, 0, 255))
                        b_w = int(np.clip(104 * (0.85 + 0.25 * spec) + 45 * spec, 0, 255))
                    weapon_img.putpixel((int(sx + dx), int(sy + dy)), (r_w, g_w, b_w, 255))

    # Butt Counterweight Pommel at (70, 94)
    wd.ellipse([67, 91, 73, 97], fill=GOLD_BASE, outline=OUTLINE)
    wd.ellipse([68, 92, 72, 96], fill=GOLD_LIGHT)
    wd.point((70, 94), fill=WHITE_SHINE)

    # 2. Axe Center Socket at (90, 48)
    wd.rectangle([87, 44, 93, 52], fill=IRON_LIGHT, outline=OUTLINE)
    wd.ellipse([88, 45, 92, 51], fill=GOLD_BASE)

    # 3. Rear Flat Pneumatic Stamping Hammer Block (x: 80..88, y: 43..53)
    wd.rounded_rectangle([78, 43, 88, 53], radius=2, fill=IRON_BASE, outline=OUTLINE)
    wd.rectangle([78, 44, 82, 52], fill=STEEL_LIGHT)  # Anvil striking face
    wd.point((80, 48), fill=WHITE_SHINE)

    # 4. Massive Crescent Single-Edged Axe Blade (x: 90..116, y: 30..66)
    # The crescent blade sweeps from socket (90, 48) out to cutting edge arc
    for y in range(28, 68):
        # Arc top to bottom
        t_arc = (y - 48.0) / 20.0
        if abs(t_arc) <= 1.0:
            max_x = int(round(90.0 + 25.0 * np.cos(t_arc * np.pi * 0.45)))
            for x in range(90, max_x + 1):
                norm_blade = (x - 90.0) / (max_x - 90.0) if max_x > 90 else 0.0
                spec = max(0.0, 1.0 - abs(y - 48.0) / 20.0)

                # Annealed golden cutting bevel on outer edge
                is_edge = (norm_blade >= 0.75)
                if is_edge:
                    edge_norm = (norm_blade - 0.75) / 0.25
                    r_b = int(np.clip(255 * (0.85 + 0.15 * edge_norm), 0, 255))
                    g_b = int(np.clip(208 * (0.85 + 0.15 * edge_norm), 0, 255))
                    b_b = int(np.clip(40 * (0.85 + 0.4 * edge_norm) + 30 * edge_norm, 0, 255))
                else:
                    # Dark obsidian quenched steel body
                    r_b = int(np.clip(43 * (0.8 + 0.4 * norm_blade) + 20 * spec, 0, 255))
                    g_b = int(np.clip(40 * (0.8 + 0.4 * norm_blade) + 20 * spec, 0, 255))
                    b_b = int(np.clip(54 * (0.8 + 0.4 * norm_blade) + 25 * spec, 0, 255))

                weapon_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Three Circular Steam Relief Vent Holes through the blade face
    vent_holes = [(98, 42), (102, 48), (98, 54)]
    for vx, vy in vent_holes:
        wd.ellipse([vx - 2, vy - 2, vx + 2, vy + 2], fill=(0, 0, 0, 0), outline=GOLD_BASE)

    # 5. Right Armored Gauntlet Gripping Axe at (78, 72)
    wd.ellipse([74, 68, 82, 76], fill=IRON_LIGHT, outline=OUTLINE)
    wd.ellipse([75, 69, 81, 75], fill=GOLD_BASE)
    wd.point((78, 72), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES (128x128 & 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices_map = [
        ("winding_key", "key_rhino_crucible_crosshair_key", key_img),
        ("back_curio", "curio_rhino_steam_furnace_exhaust", curio_img),
        ("chassis", "chassis_rhino_molten_iron_default", chassis_img),
        ("costume", "costume_rhino_crucible_smith_plate", costume_img),
        ("head_unit", "head_rhino_crucible_battering_crest", head_img),
        ("optic_core", "face_rhino_dual_amber_pyro_optic", core_img),
        ("weapon", "weapon_rhino_crucible_breaker_axe", weapon_img),
    ]

    for slot, item_id, img in slices_map:
        out_dir = f"{RHINO_PD_DIR}/{slot}"
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
    shutil.copyfile(f"{RHINO_PD_DIR}/winding_key/key_rhino_crucible_crosshair_key.png",
                    f"{KEY_DIR}/key_rhino_crucible_crosshair_key.png")
    shutil.copyfile(f"{RHINO_PD_DIR}/weapon/weapon_rhino_crucible_breaker_axe.png",
                    f"{WEAPON_DIR}/weapon_rhino_crucible_breaker_axe.png")
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

    proof_comp = f"{RHINO_PD_DIR}/proof_paperdoll_rhino_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{RHINO_PD_DIR}/proof_paperdoll_rhino_magenta.png"
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

    strip_path = f"{RHINO_PD_DIR}/proof_rhino_all_7_slices.png"
    strip_img.save(strip_path)
    print("  ✓ Composite & Proofs generated successfully")

    # ─────────────────────────────────────────────────────────────
    # SHOWCASE HD (game/assets/sprites/player/showcase/rhino_idle_hd.png)
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

        showcase_out = f"{showcase_dir}/rhino_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL HEAVYHORN RHINO CANONICAL ASSETS PRODUCED!")

if __name__ == "__main__":
    build_all()
