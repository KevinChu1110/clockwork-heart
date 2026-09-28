#!/usr/bin/env python3
"""
build_capybara_canonical_clean.py
Definitive, 100% decoupled modular sprite builder for 第四十七族 澄心水豚 (The Serene Capybara, capybara) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json & game/data/tables/paperdoll_slots.json
- docs/world/SERENE_CAPYBARA_DESIGN_PROPOSAL.md
- docs/world/CANON.md (100% zero fur, zero biological hair, zero biological tissue,
  warm ivory porcelain and polished basswood chassis with exposed brass rivets and tourbillon belly window,
  zen monk bamboo woven cowl hat with mandarin orange counterbalance, three-leaf bamboo dual-ring gold winding key,
  tea ceremony coarse hemp wrap robe, amber serene squinted quartz optic lens,
  floating serene taiji jade crystal with counter-rotating brass gear rings, geothermal purple clay tea furnace backpack)
- references/art_direction.md & references/brand_assets.md:
  Dopamine palette (The Serene Capybara canonical colors):
    1. Base: Ivory White / Snow Enamel (#FFFDF8)
    2. Primary Timber: Polished Basswood (#C29864, #A67C46)
    3. Secondary / Trim & Key: Dopamine Gold / Brass (#FFD028, #D4A520)
    4. Accent / Crystal & Leaves: Celadon Jade / Spring Green (#4ED86A, #7BF595)
    5. Counterbalance: Warm Mandarin Orange (#FFA010)
    6. Robe: Deep Indigo & Rice White (#3A4454 / #FFFDF8)
    7. Backpack: Purple Clay Ceramic (#7A4232)
    8. Blush / Relief Vents: Coral Pink (#FF5E8A)
    9. Lens / Qi Highlights: Celestial Sky Blue (#38A0FF)
    10. Dark Outline: Deep Blue-Purple (#1F1A3A)
    11. Key Outline: Warm Golden Bronze (#8C6E19) for 0-ART29 compliance
- review.md 0-ART5, 0-ART9, 0-ART11, 0-ART18, 0-ART25, 0-ART26b, 0-ART27, 0-ART28r, 0-ART29, 0-QA16, 0-QA30, 0-QA31
- Zero black square / box artifacts (0-ART29 clean snapshot-based outline pass)
"""

import os
import shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
CAPYBARA_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/capybara"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
SHOWCASE_DIR = f"{PLAYER_DIR}/showcase"
PARTY_DIR = f"{PLAYER_DIR}/party"
WEB_HERO_DIR = f"{REPO_ROOT}/web/media/hero"

W, H = 128, 128

# Canon Palette Colors (The Serene Capybara Specification)
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
OUTLINE_KEY = (140, 110, 25, 255)       # Warm golden bronze for key filigree (complies with 0-ART29 dark limit)

# 1. Base: Ivory White / Snow Enamel (#FFFDF8)
IVORY_BASE   = (255, 253, 248, 255)
IVORY_LIGHT  = (255, 255, 255, 255)
IVORY_SHADE  = (235, 228, 218, 255)
IVORY_DARK   = (210, 200, 185, 255)
IVORY_DEEP   = (175, 165, 150, 255)

# 2. Polished Basswood Timber (#C29864, #A67C46)
TIMBER_LIGHT = (218, 178, 126, 255)
TIMBER_BASE  = (194, 152, 100, 255)
TIMBER_DARK  = (166, 124, 70, 255)
TIMBER_DEEP  = (130, 95, 50, 255)

# 3. Dopamine Gold / Brass (#FFD028)
GOLD_BASE  = (255, 208, 40, 255)
GOLD_LIGHT = (255, 235, 115, 255)
GOLD_SHINE = (255, 250, 185, 255)
GOLD_DARK  = (195, 145, 18, 255)
GOLD_DEEP  = (130, 90, 10, 255)

# 4. Celadon Jade / Spring Green (#4ED86A)
JADE_BASE  = (78, 216, 106, 255)
JADE_LIGHT = (123, 245, 149, 255)
JADE_SHINE = (190, 255, 205, 255)
JADE_DARK  = (43, 166, 72, 255)
JADE_DEEP  = (25, 115, 48, 255)

# 5. Warm Mandarin Orange (#FFA010)
ORANGE_BASE  = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 195, 75, 255)
ORANGE_SHINE = (255, 225, 140, 255)
ORANGE_DARK  = (210, 115, 8, 255)

# 6. Deep Indigo Zen Fabric (#3A4454)
INDIGO_BASE  = (58, 68, 84, 255)
INDIGO_LIGHT = (85, 100, 122, 255)
INDIGO_SHINE = (120, 140, 170, 255)
INDIGO_DARK  = (42, 50, 62, 255)
INDIGO_DEEP  = (28, 34, 44, 255)

# 7. Purple Clay Ceramic (#7A4232)
CLAY_BASE  = (122, 66, 50, 255)
CLAY_LIGHT = (158, 92, 72, 255)
CLAY_DARK  = (92, 48, 36, 255)
CLAY_DEEP  = (68, 32, 24, 255)

# 8. Blush Coral Pink (#FF5E8A)
CORAL_BASE  = (255, 94, 138, 255)
CORAL_LIGHT = (255, 145, 178, 255)
CORAL_DARK  = (195, 55, 95, 255)

# 9. Celestial Sky Blue (#38A0FF)
SKY_BASE  = (56, 160, 255, 255)
SKY_LIGHT = (120, 205, 255, 255)
SKY_SHINE = (195, 235, 255, 255)
SKY_DARK  = (24, 105, 195, 255)

WHITE_SHINE = (255, 255, 255, 255)
SMOKE_WHITE = (240, 248, 255, 180)


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
    print("=== BUILDING 100% MODULAR CANONICAL SERENE CAPYBARA SLICES ===")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5, Back Layer)
    # File: winding_key/key_capybara_bamboo_dual_ring_gold.png
    # Features:
    # - 三葉竹節雙環金黃發條鑰匙 (Three-Leaf Bamboo Dual-Ring Gold Winding Key)
    # - Shaft extends from spine socket (64, 56) to central bamboo hub at (68, 24)
    # - Bamboo node rings on shaft at y=48, y=38
    # - Dual outer rings shaped like tea-spoon curves
    # - Three radiating bamboo leaf vanes from hub (up, left-down, right-down)
    # - Central axis embedded with translucent celadon jade spirit pearl
    # - Warm golden bronze outline (OUTLINE_KEY) compliant with 0-ART29 dark limit (< 260px, run < 13)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)

    # 1. Key Shaft with Bamboo Nodes from (64, 56) to (68, 24)
    for t in np.linspace(0.0, 1.0, 32):
        sx = 64.0 + (68.0 - 64.0) * t
        sy = 56.0 + (24.0 - 56.0) * t
        # Bamboo node widening at t ~ 0.25 and t ~ 0.65
        is_node = (abs(t - 0.28) < 0.05) or (abs(t - 0.68) < 0.05)
        half_w = 3.0 if is_node else 2.0

        for offset in np.linspace(-half_w, half_w, int(half_w * 2 + 1)):
            px = int(round(sx + offset * 0.8))
            py = int(round(sy - offset * 0.2))
            shade = 1.0 - abs(offset) / (half_w + 0.5)
            if is_node:
                r = int(np.clip(GOLD_LIGHT[0] * (0.8 + 0.25 * shade), 0, 255))
                g = int(np.clip(GOLD_LIGHT[1] * (0.8 + 0.25 * shade), 0, 255))
                b = int(np.clip(GOLD_LIGHT[2] * (0.8 + 0.25 * shade), 0, 255))
            else:
                r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.25 * shade), 0, 255))
                g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.25 * shade), 0, 255))
                b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * shade), 0, 255))
            key_img.putpixel((px, py), (r, g, b, 255))

    # Spine socket mount boss at (64, 56)
    kd.ellipse([60, 52, 68, 60], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([62, 54, 66, 58], fill=GOLD_BASE)

    # 2. Dual outer rings (Tea-spoon inspired dual circles)
    hub_x, hub_y = 68.0, 24.0
    for ring_r in [11.0, 16.0]:
        for deg in range(0, 360, 2):
            rad = np.radians(deg)
            rx = int(round(hub_x + np.cos(rad) * ring_r))
            ry = int(round(hub_y + np.sin(rad) * ring_r))
            if 0 <= rx < W and 0 <= ry < H:
                c = GOLD_LIGHT if ring_r == 16.0 else GOLD_BASE
                key_img.putpixel((rx, ry), c)

    # 3. Three Bamboo Leaf Vanes radiating from hub
    # Angles: -90° (up), 140° (down-left), 40° (down-right)
    leaf_angles = [-1.571, 2.443, 0.698]
    leaf_len = 14.0
    for ang in leaf_angles:
        cos_a = np.cos(ang)
        sin_a = np.sin(ang)
        for t in np.linspace(0.2, 1.0, 22):
            vx = hub_x + cos_a * (leaf_len * t)
            vy = hub_y + sin_a * (leaf_len * t)
            leaf_w = 3.0 * (1.0 - abs(t - 0.5) / 0.5) + 0.8
            perp_x = -sin_a
            perp_y = cos_a
            for w_off in np.linspace(-leaf_w, leaf_w, int(leaf_w * 2.5 + 2)):
                px = int(round(vx + perp_x * w_off))
                py = int(round(vy + perp_y * w_off))
                if 0 <= px < W and 0 <= py < H:
                    spec = max(0.0, 1.0 - abs(w_off) / (leaf_w + 0.1))
                    r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.3 * spec) + 30 * (spec**2), 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.3 * spec) + 25 * (spec**2), 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.3 * spec) + 20 * (spec**2), 0, 255))
                    key_img.putpixel((px, py), (r, g, b, 255))

    # 4. Central Bamboo Hub with Celadon Jade Spirit Pearl
    kd.ellipse([int(hub_x - 6), int(hub_y - 6), int(hub_x + 6), int(hub_y + 6)], fill=GOLD_DARK, outline=OUTLINE_KEY)
    kd.ellipse([int(hub_x - 4), int(hub_y - 4), int(hub_x + 4), int(hub_y + 4)], fill=GOLD_BASE)
    # Jade pearl in center
    kd.ellipse([int(hub_x - 3), int(hub_y - 3), int(hub_x + 3), int(hub_y + 3)], fill=JADE_BASE)
    kd.ellipse([int(hub_x - 1), int(hub_y - 2), int(hub_x + 1), int(hub_y)], fill=JADE_LIGHT)
    kd.point((int(hub_x), int(hub_y - 1)), fill=WHITE_SHINE)

    apply_clean_outline(key_img, outline_color=OUTLINE_KEY, min_alpha=120)
    print("  ✓ Slice 1 Winding Key completed, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8, Under Chassis / Back Layer)
    # File: back_curio/curio_capybara_steaming_tea_kettle_backpack.png
    # Features:
    # - 地熱竹香茶爐背包 (Geothermal Steaming Tea Kettle Backpack)
    # - Purple clay ceramic (紫砂 #7A4232) & brass (#FFD028) cylindrical furnace tanks
    #   Left kettle: (40..50, 42..66)
    #   Right kettle: (78..88, 42..66)
    # - Central brass mounting bracket at (50..78, 52..58) (leaves center clear for key)
    # - Bamboo-joint thermal exhaust pipes on kettle lids with golden valves
    # - Soft white steam clouds swirling upward from top (y: 30..42)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(curio_img)

    # Central brass bracket
    cd.rectangle([50, 52, 78, 59], fill=GOLD_DARK, outline=OUTLINE)
    cd.rectangle([52, 53, 76, 57], fill=GOLD_BASE)
    cd.line([(54, 55), (74, 55)], fill=GOLD_LIGHT, width=1)

    kettles = [
        (45.0, 54.0, -1),  # Left kettle center
        (83.0, 54.0, 1)    # Right kettle center
    ]

    for kcx, kcy, side in kettles:
        # Purple clay ceramic cylindrical pot body (x: kcx-6..kcx+6, y: 42..68)
        for y in range(42, 69):
            for x in range(int(kcx - 6), int(kcx + 7)):
                dx = (x - kcx) / 6.0
                if abs(dx) <= 1.0:
                    spec = max(0.0, 1.0 - abs(dx))
                    shine = max(0.0, 1.0 - abs(dx - 0.25))**2
                    is_brass_band = (y in (48, 49, 61, 62))
                    if is_brass_band:
                        r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.35 * spec), 0, 255))
                        g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.35 * spec), 0, 255))
                        b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.35 * spec), 0, 255))
                    else:
                        r = int(np.clip(CLAY_BASE[0] * (0.85 + 0.35 * spec) + 35 * shine, 0, 255))
                        g = int(np.clip(CLAY_BASE[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                        b = int(np.clip(CLAY_BASE[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                    curio_img.putpixel((x, y), (r, g, b, 255))

        # Brass lid & Bamboo-joint thermal exhaust valve
        cd.ellipse([int(kcx - 5), 38, int(kcx + 5), 44], fill=GOLD_DARK, outline=OUTLINE)
        cd.ellipse([int(kcx - 3), 39, int(kcx + 3), 43], fill=GOLD_BASE)
        # Bamboo steam pipe
        cd.rectangle([int(kcx - 2), 34, int(kcx + 2), 39], fill=TIMBER_BASE, outline=OUTLINE)
        cd.point((int(kcx), 35), fill=GOLD_LIGHT)

        # Delicate white tea steam clouds rising from top (y: 28..36)
        steam_offset_x = -2 * side
        for sy in range(26, 36):
            sprog = (36 - sy) / 10.0
            sw = 3.5 * (1.0 - sprog * 0.5)
            scx = kcx + steam_offset_x + np.sin(sprog * 3.14) * 2.0
            for sx in range(int(scx - sw), int(scx + sw + 1)):
                if 0 <= sx < W and 0 <= sy < H:
                    dist = abs(sx - scx) / (sw + 0.1)
                    alpha = int(np.clip((1.0 - dist) * (1.0 - sprog * 0.6) * 200, 0, 255))
                    if alpha > 15:
                        curio_img.putpixel((sx, sy), (245, 250, 255, alpha))

        # Bottom drain spigot
        cd.ellipse([int(kcx - 3), 68, int(kcx + 3), 72], fill=GOLD_DARK, outline=OUTLINE)
        cd.point((int(kcx), 70), fill=GOLD_BASE)

    apply_clean_outline(curio_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 2 Back Curio completed, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS (Z: 10, Body Base)
    # File: chassis/chassis_capybara_porcelain_timber_default.png
    # Features:
    # - 溫潤青瓷椴木禪意底盤 (Ivory Porcelain & Basswood Zen Chassis)
    # - 2.2 chibi chubby, sturdy, calm, low center-of-gravity capybara body
    # - Soft ground contact shadow at (64, 116)
    # - Short, thick polished basswood legs with brass sphere ball joints
    # - Porcelain ivory belly & torso (x: 44..84, y: 58..94) with multi-tone depth
    # - Center belly tourbillon observation window with rotating brass balance wheel at (64, 75)
    # - Left hand resting or forming peaceful zen mudra at (38..46, 76..84)
    # - Right arm raised gently to support/guide floating crystal at (82..92, 66..76)
    # - STRICT ZERO pixels at x >= 94 (0-ART9 / 0-ART11 compliant)
    # - Multi-tone depth with unique colors >= 20 in torso (0-ART18 compliant)
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow
    ch_d.ellipse([64 - 36, 116 - 6, 64 + 36, 116 + 6], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.2))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Articulated Short Sturdy Basswood Paws / Boots at (44, 113) and (72, 113)
    foot_pos = [(44.0, 113.0), (72.0, 113.0)]
    for fx, fy in foot_pos:
        # Sole plate
        ch_d.ellipse([int(fx - 9), int(fy - 3), int(fx + 9), int(fy + 3)], fill=TIMBER_DEEP, outline=OUTLINE)
        # Basswood rounded paw
        ch_d.ellipse([int(fx - 8), int(fy - 3), int(fx + 8), int(fy + 2)], fill=TIMBER_BASE)
        # Ivory porcelain toe plates with brass rivets
        ch_d.ellipse([int(fx - 6), int(fy - 2), int(fx + 2), int(fy + 1)], fill=IVORY_BASE)
        ch_d.point((int(fx - 3), int(fy)), fill=GOLD_BASE)
        ch_d.point((int(fx + 1), int(fy)), fill=GOLD_BASE)
        ch_d.point((int(fx), int(fy - 1)), fill=WHITE_SHINE)

    # 3. Short, thick basswood legs with brass ball-joint knees
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
                r = int(np.clip(TIMBER_BASE[0] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(TIMBER_BASE[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(TIMBER_BASE[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                chassis_img.putpixel((int(lx + dx), int(ly)), (r, g, b, 255))
        mid_x = int(0.5 * (lx0 + lx1))
        mid_y = int(0.5 * (ly0 + ly1))
        # Brass ball joint at knee
        ch_d.ellipse([mid_x - 4, mid_y - 3, mid_x + 4, mid_y + 3], fill=GOLD_BASE, outline=OUTLINE)
        ch_d.point((mid_x, mid_y), fill=GOLD_LIGHT)

    # 4. Solid Neck Collar / Upper Chest Flange (x: 50..78, y: 44..58)
    for ny in range(44, 59):
        for nx in range(50, 79):
            dx = (nx - 64.0) / 14.0
            dy = (ny - 51.0) / 7.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(IVORY_BASE[0] * (0.85 + 0.25 * spec), 0, 255))
                g = int(np.clip(IVORY_BASE[1] * (0.85 + 0.25 * spec), 0, 255))
                b = int(np.clip(IVORY_BASE[2] * (0.85 + 0.25 * spec), 0, 255))
                chassis_img.putpixel((nx, ny), (r, g, b, 255))

    # 5. Main Chubby Rounded Torso (x: 44..84, y: 58..95)
    # Celadon ivory porcelain panels with polished basswood flank ribs
    for ty in range(58, 95):
        for tx in range(44, 85):
            dx = (tx - 64.0) / 19.0
            dy = (ty - 76.0) / 18.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - dist_sq**0.5)
                shine = max(0.0, 1.0 - ((tx - 58.0)**2 + (ty - 68.0)**2)**0.5 / 12.0)**2
                # Flank ribs: basswood; Center: porcelain
                is_wood_flank = (tx <= 50 or tx >= 78)
                if is_wood_flank:
                    r = int(np.clip(TIMBER_BASE[0] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                    g = int(np.clip(TIMBER_BASE[1] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
                    b = int(np.clip(TIMBER_BASE[2] * (0.85 + 0.35 * spec) + 15 * shine, 0, 255))
                else:
                    # Shaded ivory porcelain (keep min RGB < 235 for anti-white run)
                    r = int(np.clip(238 * (0.85 + 0.25 * spec) + 25 * shine, 0, 250))
                    g = int(np.clip(232 * (0.85 + 0.25 * spec) + 25 * shine, 0, 248))
                    b = int(np.clip(222 * (0.85 + 0.25 * spec) + 25 * shine, 0, 242))
                chassis_img.putpixel((tx, ty), (r, g, b, 255))

    # Tourbillon Quartz Observation Window at (64, 75)
    # High-transparency quartz glass with brass balance wheel & tourbillon cage inside
    ch_d.ellipse([57, 68, 71, 82], fill=GOLD_DARK, outline=OUTLINE)
    ch_d.ellipse([58, 69, 70, 81], fill=TIMBER_DEEP)
    # Brass balance wheel and bridge
    ch_d.ellipse([60, 71, 68, 79], fill=GOLD_BASE, outline=GOLD_DARK)
    ch_d.line([(60, 75), (68, 75)], fill=GOLD_LIGHT, width=1)
    ch_d.line([(64, 71), (64, 79)], fill=GOLD_LIGHT, width=1)
    # Center jewel pivot (ruby/coral pink)
    ch_d.point((64, 75), fill=CORAL_BASE)
    ch_d.point((63, 74), fill=WHITE_SHINE)

    # 6. Left Arm & Paw formed in peaceful mudra at (38..46, 76..84)
    for t in np.linspace(0.0, 1.0, 18):
        ax = 48.0 - t * 8.0
        ay = 66.0 + t * 12.0
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                if dx**2 + dy**2 <= 16:
                    chassis_img.putpixel((int(ax + dx), int(ay + dy)), TIMBER_BASE)
    ch_d.ellipse([36, 76, 44, 84], fill=TIMBER_DARK, outline=OUTLINE)
    ch_d.ellipse([38, 78, 42, 82], fill=IVORY_BASE)
    ch_d.point((40, 80), fill=GOLD_BASE)

    # 7. Right Upper Arm raised gently at (82..92, 66..76) (strictly x < 94)
    for t in np.linspace(0.0, 1.0, 16):
        ax = 80.0 + t * 9.0  # max ax = 89
        ay = 66.0 + t * 7.0
        for dx in range(-3, 4):
            for dy in range(-3, 4):
                px = int(ax + dx)
                py = int(ay + dy)
                if px < 94 and dx**2 + dy**2 <= 9:
                    chassis_img.putpixel((px, py), TIMBER_BASE)

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
    # File: head_unit/head_capybara_zen_monk_cowl_hat.png
    # Features:
    # - 天元禪修竹笠斗笠 (Zen Monk Bamboo Cowl Hat)
    # - Bamboo woven conical hat sitting on head (x: 34..94, y: 16..38)
    # - Hat apex decorated with dopamine warm orange mini mandarin orange (小金橘 #FFA010)
    #   counterbalance with emerald leaf (#4ED86A)
    # - Rim has three miniature brass bells / wind chimes at (38, 38), (64, 40), (90, 38)
    # - Under hat: calm, serene capybara snout (x: 52..76, y: 46..56), rounded wooden ears
    #   at (36..42, 38..44) and (86..92, 38..44)
    # - Nose tip at (64, 51)
    # - Cheeks have mini coral pink (#FF5E8A) cooling relief slits at (46, 50) and (82, 50)
    # - STRICT 0-ART27: Hollow eye sockets centered at (54, 42) and (74, 42) (alpha == 0)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    hcx, hcy = 64.0, 42.0

    # 1. Base Capybara Face & Snout Under Hat (x: 40..88, y: 34..57)
    for y in range(34, 58):
        for x in range(40, 89):
            dx = (x - hcx) / 22.0
            dy = (y - 46.0) / 11.0
            dist_sq = dx**2 + dy**2
            if dist_sq <= 1.0:
                spec = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 22.0)
                shine = max(0.0, 1.0 - ((x - (hcx - 4))**2 + (y - (hcy - 4))**2)**0.5 / 6.0)**2
                # Ivory porcelain face with warm basswood cheeks
                is_cheek = (x <= 48 or x >= 80)
                if is_cheek:
                    r = int(np.clip(TIMBER_BASE[0] * (0.85 + 0.3 * spec) + 20 * shine, 0, 255))
                    g = int(np.clip(TIMBER_BASE[1] * (0.85 + 0.3 * spec) + 15 * shine, 0, 255))
                    b = int(np.clip(TIMBER_BASE[2] * (0.85 + 0.3 * spec) + 10 * shine, 0, 255))
                else:
                    r = int(np.clip(238 * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
                    g = int(np.clip(232 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                    b = int(np.clip(220 * (0.85 + 0.25 * spec) + 20 * shine, 0, 240))
                head_img.putpixel((x, y), (r, g, b, 255))

    # 2. Side Basswood Ears at (38, 40) and (90, 40)
    for ex in [38, 90]:
        hd.ellipse([ex - 5, 36, ex + 5, 46], fill=TIMBER_DARK, outline=OUTLINE)
        hd.ellipse([ex - 3, 38, ex + 3, 44], fill=TIMBER_BASE)
        hd.point((ex, 41), fill=GOLD_BASE)

    # 3. Lower Broad Rounded Snout (x: 52..76, y: 46..56) & Nose Tip
    for sy in range(46, 57):
        for sx in range(52, 77):
            dx = (sx - hcx) / 11.0
            dy = (sy - 51.0) / 5.0
            if dx**2 + dy**2 <= 1.0:
                spec = max(0.0, 1.0 - (dx**2 + dy**2)**0.5)
                r = int(np.clip(TIMBER_LIGHT[0] * (0.85 + 0.3 * spec), 0, 255))
                g = int(np.clip(TIMBER_LIGHT[1] * (0.85 + 0.3 * spec), 0, 255))
                b = int(np.clip(TIMBER_LIGHT[2] * (0.85 + 0.3 * spec), 0, 255))
                head_img.putpixel((sx, sy), (r, g, b, 255))

    # Nose tip (stamped ebony / dark wood button)
    hd.ellipse([62, 49, 66, 53], fill=(42, 34, 28, 255), outline=OUTLINE)
    hd.point((63, 50), fill=TIMBER_LIGHT)

    # Cheek miniature coral pink cooling relief vents at (46, 51) and (82, 51)
    hd.ellipse([46 - 2, 51 - 2, 46 + 2, 51 + 2], fill=CORAL_BASE, outline=OUTLINE)
    hd.point((46, 51), fill=CORAL_LIGHT)
    hd.ellipse([82 - 2, 51 - 2, 82 + 2, 51 + 2], fill=CORAL_BASE, outline=OUTLINE)
    hd.point((82, 51), fill=CORAL_LIGHT)

    # 4. Woven Bamboo Conical Cowl Hat (x: 32..96, y: 16..38)
    # Conical hat shape: apex at (64, 18), base line from (32, 36) to (96, 36)
    for y in range(16, 38):
        t_y = (y - 16.0) / 21.0
        hw = 3.0 + t_y * 29.0  # width grows down
        for x in range(int(hcx - hw), int(hcx + hw + 1)):
            dx = (x - hcx) / (hw + 0.1)
            if abs(dx) <= 1.0:
                spec = max(0.0, 1.0 - abs(dx))
                # Woven bamboo lattice texture
                is_weave = ((x + y) % 4 in (0, 1))
                if is_weave:
                    r = int(np.clip(TIMBER_LIGHT[0] * (0.85 + 0.3 * spec), 0, 255))
                    g = int(np.clip(TIMBER_LIGHT[1] * (0.85 + 0.3 * spec), 0, 255))
                    b = int(np.clip(TIMBER_LIGHT[2] * (0.85 + 0.3 * spec), 0, 255))
                else:
                    r = int(np.clip(TIMBER_DARK[0] * (0.85 + 0.3 * spec), 0, 255))
                    g = int(np.clip(TIMBER_DARK[1] * (0.85 + 0.3 * spec), 0, 255))
                    b = int(np.clip(TIMBER_DARK[2] * (0.85 + 0.3 * spec), 0, 255))
                head_img.putpixel((x, y), (r, g, b, 255))

    # Gold rim border on hat
    hd.line([(34, 36), (94, 36)], fill=GOLD_BASE, width=1)

    # Three miniature brass wind chime bells hanging from hat rim
    for bx in [40, 64, 88]:
        hd.line([(bx, 36), (bx, 39)], fill=GOLD_DARK, width=1)
        hd.ellipse([bx - 2, 39, bx + 2, 43], fill=GOLD_BASE, outline=OUTLINE)
        hd.point((bx, 40), fill=GOLD_LIGHT)

    # 5. Dopamine Warm Mandarin Orange (#FFA010) Winding Counterbalance on hat apex
    # Orange centered at (64, 14) with tiny green leaf at (67, 11)
    hd.ellipse([64 - 5, 14 - 5, 64 + 5, 14 + 5], fill=ORANGE_BASE, outline=OUTLINE)
    hd.ellipse([64 - 3, 14 - 3, 64 + 2, 14 + 2], fill=ORANGE_LIGHT)
    hd.point((63, 13), fill=ORANGE_SHINE)
    # Tiny green leaf (#4ED86A)
    hd.ellipse([67, 10, 71, 13], fill=JADE_BASE, outline=OUTLINE)
    hd.point((69, 11), fill=JADE_LIGHT)

    # 6. Hollow Eye Sockets for 0-ART27:
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
    # File: costume/costume_capybara_tea_ceremony_wrap.png
    # Features:
    # - 道場茶道防塵練功袍 (Tea Ceremony Coarse Hemp Wrap Robe)
    # - Double-layer indigo (#3A4454) and rice white (#FFFDF8) wrap robe
    # - Gold borders & coral pink (#FF5E8A) tea ceremony braided cords
    # - Taiji yin-yang gear embroidery emblem on chest at (64, 72)
    # - Shoulder drape fitting snugly over shoulders (x: 42..86, y: 58..70)
    # - Robe skirt hangs down to y: 92
    # - STRICT 0-ART26b: Decoupled costume with strictly ZERO pixels at y >= 96
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Chest Robe (x: 46..82, y: 60..86)
    for y in range(60, 87):
        for x in range(46, 83):
            spec = max(0.0, 1.0 - abs(x - 64.0) / 18.0)
            shine = max(0.0, 1.0 - ((x - 60.0)**2 + (y - 70.0)**2)**0.5 / 10.0)**2
            # Diagonal wrap seam: left side rice white, right side indigo
            is_white_lapel = (x < 62 and (x + y) % 3 == 0) or (x in (60, 61))
            if is_white_lapel:
                r = int(np.clip(238 * (0.85 + 0.25 * spec) + 20 * shine, 0, 250))
                g = int(np.clip(232 * (0.85 + 0.25 * spec) + 20 * shine, 0, 248))
                b = int(np.clip(220 * (0.85 + 0.25 * spec) + 20 * shine, 0, 240))
            else:
                r = int(np.clip(INDIGO_BASE[0] * (0.85 + 0.35 * spec) + 30 * shine, 0, 255))
                g = int(np.clip(INDIGO_BASE[1] * (0.85 + 0.35 * spec) + 25 * shine, 0, 255))
                b = int(np.clip(INDIGO_BASE[2] * (0.85 + 0.35 * spec) + 20 * shine, 0, 255))
            costume_img.putpixel((x, y), (r, g, b, 255))

    # Gold lapel trim line
    cos_d.line([(48, 62), (64, 76)], fill=GOLD_BASE, width=1)
    cos_d.line([(80, 62), (64, 76)], fill=GOLD_BASE, width=1)

    # Center Taiji Yin-Yang Gear Embroidery at (64, 72)
    cos_d.ellipse([60, 68, 68, 76], fill=GOLD_DARK, outline=OUTLINE)
    cos_d.ellipse([61, 69, 67, 75], fill=GOLD_BASE)
    # Yin-yang swirling contrast dots
    cos_d.point((63, 71), fill=INDIGO_DARK)
    cos_d.point((65, 73), fill=IVORY_BASE)

    # 2. Shoulder Drapes
    shoulders = [
        (44.0, 61.0),  # Left shoulder
        (84.0, 61.0)   # Right shoulder
    ]
    for px, py in shoulders:
        cos_d.ellipse([int(px - 6), int(py - 5), int(px + 6), int(py + 5)], fill=INDIGO_BASE, outline=OUTLINE)
        cos_d.ellipse([int(px - 4), int(py - 3), int(px + 4), int(py + 3)], fill=INDIGO_LIGHT)
        # Coral pink braided knot
        cos_d.line([(int(px - 3), int(py)), (int(px + 3), int(py))], fill=CORAL_BASE, width=1)
        cos_d.point((int(px), int(py - 1)), fill=CORAL_LIGHT)

    # 3. Four Segmented Waist Tassets (hanging from y: 86 down to y: 92)
    tasset_x_spans = [(48, 54), (56, 62), (66, 72), (74, 80)]
    for x0, x1 in tasset_x_spans:
        cos_d.rectangle([x0, 86, x1, 92], fill=INDIGO_BASE, outline=OUTLINE)
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
    # File: optic_core/face_capybara_amber_zen_lens.png
    # Features:
    # - 安詳微瞇琥珀石英目鏡 (Serene Amber Zen Lens)
    # - High-transparency curved amber quartz lenses centered at (54, 42) and (74, 42)
    # - Serene, gently squinted/smiling micro-arc reflecting ultimate composure
    # - Concentric micrometer cursor reticles & celestial sky-blue guide lines (#38A0FF)
    # - Brass retention bezel (#FFD028)
    # - Aligns 100% with head unit eye sockets (0-ART27 min alpha >= 200)
    # - High color richness (0-QA31 unique colors >= 15)
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    c_d = ImageDraw.Draw(core_img)

    for ex, ey in [(54.0, 42.0), (74.0, 42.0)]:
        # Outer Brass Retention Bezel
        c_d.ellipse([int(ex - 5), int(ey - 5), int(ex + 5), int(ey + 5)], fill=GOLD_DARK, outline=OUTLINE)
        c_d.ellipse([int(ex - 4), int(ey - 4), int(ex + 4), int(ey + 4)], fill=GOLD_BASE)

        # Lens Body with Multi-Tone Shading (Amber Quartz)
        for y in range(int(ey - 3), int(ey + 4)):
            for x in range(int(ex - 3), int(ex + 4)):
                dist = ((x - ex)**2 + (y - ey)**2)**0.5
                if dist <= 3.2:
                    spec = max(0.0, 1.0 - dist / 3.2)
                    shine = max(0.0, 1.0 - ((x - (ex - 1.0))**2 + (y - (ey - 1.0))**2)**0.5 / 1.5)**2
                    # Amber glowing quartz
                    r = int(np.clip(GOLD_BASE[0] * (0.8 + 0.3 * spec) + 80 * shine, 0, 255))
                    g = int(np.clip(GOLD_BASE[1] * (0.8 + 0.3 * spec) + 50 * shine, 0, 255))
                    b = int(np.clip(GOLD_BASE[2] * (0.8 + 0.25 * spec) + 30 * shine, 0, 255))
                    core_img.putpixel((x, y), (r, g, b, 255))

        # Serene Squinted Eye Zen Arc (Gentle horizontal smile arc)
        core_img.putpixel((int(ex), int(ey)), WHITE_SHINE)
        core_img.putpixel((int(ex - 1), int(ey)), GOLD_LIGHT)
        core_img.putpixel((int(ex + 1), int(ey)), GOLD_LIGHT)
        core_img.putpixel((int(ex - 2), int(ey - 1)), SKY_LIGHT)
        core_img.putpixel((int(ex + 2), int(ey - 1)), SKY_LIGHT)
        # Subtle celestial sky-blue guide dot below
        core_img.putpixel((int(ex), int(ey + 1)), SKY_BASE)

    print("  ✓ Slice 6 Optic Core completed, bbox:", core_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/weapon_capybara_serene_taiji_crystal.png
    # Features:
    # - 澄心太極護體靈晶 (Serene Taiji Bagua Spirit Crystal)
    # - Floating translucent octagonal celadon jade crystal (#4ED86A)
    #   centered at (104, 72) in front of right hand (x: 88..124, y: 56..94)
    # - Counter-rotating dual concentric brass gear rings (#FFD028, #D4A520)
    # - Yin-yang taiji center core with white/green spiritual glow
    # - Three miniature orbiting jade spirit blades (at 0°, 120°, 240°)
    # - Single-wield compliant (review.md 0-MKT7)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wp_d = ImageDraw.Draw(weapon_img)

    wcx, wcy = 104.0, 72.0

    # 1. Outer Brass Taiji Gear Ring (Radius: 15..17)
    for deg in range(0, 360, 2):
        rad = np.radians(deg)
        # Gear teeth every 30 deg
        is_tooth = (deg % 30 < 15)
        rr = 17.5 if is_tooth else 15.0
        rx = int(round(wcx + np.cos(rad) * rr))
        ry = int(round(wcy + np.sin(rad) * rr))
        if 0 <= rx < W and 0 <= ry < H:
            weapon_img.putpixel((rx, ry), GOLD_BASE)

    # 2. Main Octagonal Celadon Jade Crystal Body (Radius: 13)
    for y in range(int(wcy - 14), int(wcy + 15)):
        for x in range(int(wcx - 14), int(wcx + 15)):
            dist = ((x - wcx)**2 + (y - wcy)**2)**0.5
            # Octagonal contour check
            oct_d = max(abs(x - wcx), abs(y - wcy), (abs(x - wcx) + abs(y - wcy)) * 0.707)
            if oct_d <= 13.0:
                spec = max(0.0, 1.0 - oct_d / 13.0)
                shine = max(0.0, 1.0 - ((x - (wcx - 3.0))**2 + (y - (wcy - 3.0))**2)**0.5 / 6.0)**2
                # Translucent celadon jade
                r = int(np.clip(JADE_BASE[0] * (0.8 + 0.35 * spec) + 40 * shine, 0, 255))
                g = int(np.clip(JADE_BASE[1] * (0.8 + 0.35 * spec) + 35 * shine, 0, 255))
                b = int(np.clip(JADE_BASE[2] * (0.8 + 0.35 * spec) + 30 * shine, 0, 255))
                weapon_img.putpixel((x, y), (r, g, b, 255))

    # Inner Gold Taiji Core Ring (Radius: 7)
    wp_d.ellipse([int(wcx - 7), int(wcy - 7), int(wcx + 7), int(wcy + 7)], fill=GOLD_DARK, outline=OUTLINE)
    wp_d.ellipse([int(wcx - 5), int(wcy - 5), int(wcx + 5), int(wcy + 5)], fill=JADE_LIGHT)

    # Yin-yang spiral dots in crystal core
    wp_d.point((int(wcx - 2), int(wcy - 1)), fill=WHITE_SHINE)
    wp_d.point((int(wcx + 2), int(wcy + 1)), fill=JADE_DEEP)

    # 3. Three Miniature Orbiting Jade Blades
    blade_angles = [0.0, 2.094, 4.189]  # 0, 120, 240 deg
    orbit_r = 20.0
    for ang in blade_angles:
        bx = wcx + np.cos(ang) * orbit_r
        by = wcy + np.sin(ang) * orbit_r
        wp_d.ellipse([int(bx - 3), int(by - 3), int(bx + 3), int(by + 3)], fill=JADE_BASE, outline=OUTLINE)
        wp_d.ellipse([int(bx - 1), int(by - 1), int(bx + 1), int(by + 1)], fill=JADE_LIGHT)
        wp_d.point((int(bx), int(by)), fill=WHITE_SHINE)

    apply_clean_outline(weapon_img, outline_color=OUTLINE, min_alpha=100)
    print("  ✓ Slice 7 Weapon completed, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # EXPORT INDIVIDUAL SLICES (128x128 and 512x512 LANCZOS)
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("chassis", "chassis_capybara_porcelain_timber_default", chassis_img),
        ("head_unit", "head_capybara_zen_monk_cowl_hat", head_img),
        ("winding_key", "key_capybara_bamboo_dual_ring_gold", key_img),
        ("costume", "costume_capybara_tea_ceremony_wrap", costume_img),
        ("optic_core", "face_capybara_amber_zen_lens", core_img),
        ("weapon", "weapon_capybara_serene_taiji_crystal", weapon_img),
        ("back_curio", "curio_capybara_steaming_tea_kettle_backpack", curio_img)
    ]

    for slot, item_id, img_128 in slices:
        slot_dir = f"{CAPYBARA_PD_DIR}/{slot}"
        os.makedirs(slot_dir, exist_ok=True)
        path_128 = f"{slot_dir}/{item_id}.png"
        img_128.save(path_128)

        # 512x512 LANCZOS High-Definition Export
        img_512 = img_128.resize((512, 512), Image.Resampling.LANCZOS)
        path_512 = f"{slot_dir}/{item_id}_512.png"
        img_512.save(path_512)
        print(f"  ✓ Exported {slot}: {item_id} (128x128 & 512x512 LANCZOS)")

    # Universal shared key and weapon directories
    os.makedirs(KEY_DIR, exist_ok=True)
    os.makedirs(WEAPON_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_capybara_bamboo_dual_ring_gold.png")
    weapon_img.save(f"{WEAPON_DIR}/weapon_capybara_serene_taiji_crystal.png")
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

    proof_comp = f"{CAPYBARA_PD_DIR}/proof_paperdoll_capybara_composite.png"
    composite.save(proof_comp)

    # Magenta background composite (for 0-ART29 / hole detection)
    magenta_bg = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    magenta_bg.alpha_composite(composite)
    proof_mag = f"{CAPYBARA_PD_DIR}/proof_paperdoll_capybara_magenta.png"
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

    strip_path = f"{CAPYBARA_PD_DIR}/proof_capybara_all_7_slices.png"
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

    # 1. 128x128 game/assets/sprites/player/capybara_idle_x3.png
    os.makedirs(PLAYER_DIR, exist_ok=True)
    p_idle_x3 = f"{PLAYER_DIR}/capybara_idle_x3.png"
    idle_with_shadow.save(p_idle_x3)

    # 2. 64x64 game/assets/sprites/player/capybara_idle.png
    p_idle_64 = f"{PLAYER_DIR}/capybara_idle.png"
    idle_64 = idle_with_shadow.resize((64, 64), Image.Resampling.LANCZOS)
    idle_64.save(p_idle_64)

    # 3. 128x128 game/assets/sprites/player/party/capybara_idle.png
    os.makedirs(PARTY_DIR, exist_ok=True)
    p_party_idle = f"{PARTY_DIR}/capybara_idle.png"
    idle_with_shadow.save(p_party_idle)

    # 4. 128x128 web/media/hero/capybara_idle.png
    os.makedirs(WEB_HERO_DIR, exist_ok=True)
    p_web_idle = f"{WEB_HERO_DIR}/capybara_idle.png"
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

        showcase_out = f"{SHOWCASE_DIR}/capybara_idle_hd.png"
        showcase_hd.save(showcase_out)
        print("  ✓ Showcase HD generated successfully:", showcase_out)

    print("🎉 ALL SERENE CAPYBARA CANONICAL ASSETS PRODUCED!")


if __name__ == "__main__":
    build_all()
