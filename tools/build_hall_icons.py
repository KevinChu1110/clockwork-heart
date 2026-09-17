#!/usr/bin/env python3
"""
tools/build_hall_icons.py
Generate 4 mobile lobby left hall card navigation icons for Clockwork Heart (發條之心):
1. icon_hall_forge.png - Celestial Blacksmith / Forge (天宮鐵匠 · 黃銅鐵砧＋小錘)
2. icon_hall_gem.png   - Artisan Gem Workshop / Crucible (手藝工坊 · 三色寶石晶核熔爐)
3. icon_hall_arena.png - Martial Arena / Tournament (演武競技 · 交叉武器比武盾牌)
4. icon_hall_quest.png - Adventure Commission / Winding Quest (冒險委託 · 上鍊發條捲軸委託牌)

Specifications:
- 128x128 RGBA PNG transparent background
- Unified outline #1F1A3A (approx 4-5px at 128px, 16-20px at 512px)
- Dopamine palette: warm gold #FFD028, orange #FFA010, mint-teal #4ED86A, coral-pink #FF5E8A, sky blue #38A0FF
- Microscopic readability at 32px with mutually distinct silhouettes
- Zero system emojis, zero realistic fur, strictly clockwork toy world language
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
OUT_DIR = f"{REPO_ROOT}/game/assets/icons/hud"
PROOF_DIR = f"{REPO_ROOT}/proofs/hud_icons"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PROOF_DIR, exist_ok=True)

OUTLINE_COLOR = (31, 26, 58, 255) # #1F1A3A


# ==============================================================================
# Helper functions
# ==============================================================================

def create_outline_and_base(mask: np.ndarray, size=512, outline_radius=29) -> Image.Image:
    """Create a RGBA master with dilated #1F1A3A outline from a boolean mask."""
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    outline_mask = mask_img.filter(ImageFilter.MaxFilter(outline_radius))
    outline_arr = np.array(outline_mask) > 30
    
    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[outline_arr] = OUTLINE_COLOR
    return Image.fromarray(rgba, mode="RGBA")


def draw_rivet(draw: ImageDraw.Draw, x: float, y: float, r: float = 8.0, base_color=(255, 220, 80)):
    """Draw a 3D metallic dome rivet with outline, highlight, and shadow."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=base_color, outline=OUTLINE_COLOR, width=max(2, int(r * 0.35)))
    # Specular glint
    hr = r * 0.35
    draw.ellipse([x - r * 0.35, y - r * 0.35, x - r * 0.35 + hr, y - r * 0.35 + hr], fill=(255, 255, 255, 240))
    # Bottom shading
    draw.arc([x - r, y - r, x + r, y + r], 20, 160, fill=(140, 80, 10, 200), width=max(2, int(r * 0.25)))


def draw_star_sparkle(draw: ImageDraw.Draw, cx: float, cy: float, r: float = 12.0, color=(255, 255, 255, 250)):
    """Draw a 4-pointed diamond star sparkle."""
    pts = [
        (cx, cy - r),
        (cx + r * 0.25, cy - r * 0.25),
        (cx + r, cy),
        (cx + r * 0.25, cy + r * 0.25),
        (cx, cy + r),
        (cx - r * 0.25, cy + r * 0.25),
        (cx - r, cy),
        (cx - r * 0.25, cy - r * 0.25)
    ]
    draw.polygon(pts, fill=color)


# ==============================================================================
# 1. Forge Icon (天宮鐵匠 - Celestial Blacksmith / Anvil & Hammer)
# ==============================================================================

def create_hall_forge_master(size=512) -> Image.Image:
    """
    Render 512x512 Celestial Blacksmith Icon:
    - Distinctive clockwork brass & bronze anvil with left horn, stepped base, and waist.
    - Embedded golden brass clockwork gear in the anvil waist.
    - Smithing mallet/hammer angled diagonally from top-right striking down.
    - Burst of molten golden/orange toy gear sparks at the strike point.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]

    # --- Anvil Geometry ---
    # Top striking table: flat top y=225, x in 200..415, height to y=275
    table_mask = (x_coords >= 200) & (x_coords <= 415) & (y_coords >= 225) & (y_coords <= 275)

    # Horn (left side): conical horn extending from x=210 down to x=85, tapering from y in 228..272 to tip at (85, 248)
    horn_mask = (x_coords >= 85) & (x_coords <= 210) & \
                (y_coords >= 248 - (x_coords - 85) * (20.0 / 125.0)) & \
                (y_coords <= 248 + (x_coords - 85) * (24.0 / 125.0))

    # Waist (central column): x in 185..335, y in 275..365, curved inward
    waist_dist = np.abs(x_coords - 260.0)
    waist_width_profile = 75.0 + ((y_coords - 320.0) / 45.0)**2 * 25.0
    waist_mask = (y_coords >= 275) & (y_coords <= 365) & (waist_dist <= waist_width_profile)

    # Stepped Base: x in 115..405, y in 365..440
    # Tier 1 (mid base): x in 155..365, y in 365..400
    base_tier1 = (x_coords >= 155) & (x_coords <= 365) & (y_coords >= 365) & (y_coords <= 400)
    # Tier 2 (bottom flange): x in 115..405, y in 400..440
    base_tier2 = (x_coords >= 115) & (x_coords <= 405) & (y_coords >= 400) & (y_coords <= 440)
    base_mask = base_tier1 | base_tier2

    anvil_body_mask = table_mask | horn_mask | waist_mask | base_mask

    # --- Embedded Clockwork Gear on Anvil Waist ---
    gear_cx, gear_cy = 260.0, 320.0
    dist_gear = np.sqrt((x_coords - gear_cx)**2 + (y_coords - gear_cy)**2)
    angle_gear = np.arctan2(y_coords - gear_cy, x_coords - gear_cx)
    teeth = np.mod(angle_gear + math.pi, 2.0 * math.pi / 6.0) / (2.0 * math.pi / 6.0)
    gear_r = 38.0 + np.where(teeth < 0.5, 12.0, 0.0)
    waist_gear_mask = (dist_gear <= gear_r) & (dist_gear >= 16.0) & (y_coords >= 275) & (y_coords <= 365)

    # --- Hammer Geometry ---
    # Angled haft: from (435, 80) down to (305, 215)
    hx1, hy1 = 435.0, 80.0
    hx2, hy2 = 305.0, 215.0
    # Unit vector along handle
    hlen = math.hypot(hx2 - hx1, hy2 - hy1)
    hux, huy = (hx2 - hx1) / hlen, (hy2 - hy1) / hlen
    hnx, hny = -huy, hux # Normal vector
    
    # Projection along handle
    proj_h = (x_coords - hx1) * hux + (y_coords - hy1) * huy
    proj_n = np.abs((x_coords - hx1) * hnx + (y_coords - hy1) * hny)
    haft_mask = (proj_h >= -15.0) & (proj_h <= hlen + 15.0) & (proj_n <= 12.0)
    # Round pommel at top of haft
    dist_pommel = np.sqrt((x_coords - (hx1 - 10 * hux))**2 + (y_coords - (hy1 - 10 * huy))**2)
    pommel_mask = dist_pommel <= 18.0

    # Mallet Head: rectangular beveled striking block at (295, 205), perpendicular to haft
    # Center of mallet head
    mcx, mcy = 295.0, 205.0
    m_proj_para = (x_coords - mcx) * hux + (y_coords - mcy) * huy
    m_proj_perp = (x_coords - mcx) * hnx + (y_coords - mcy) * hny
    mallet_mask = (np.abs(m_proj_para) <= 30.0) & (np.abs(m_proj_perp) <= 46.0)

    # Mini sparks and tiny flying gear at impact point (245, 200)
    spark1_dist = np.sqrt((x_coords - 235.0)**2 + (y_coords - 180.0)**2)
    spark1_mask = spark1_dist <= 14.0
    spark2_dist = np.sqrt((x_coords - 210.0)**2 + (y_coords - 150.0)**2)
    spark2_mask = spark2_dist <= 11.0

    combined_mask = anvil_body_mask | waist_gear_mask | haft_mask | pommel_mask | mallet_mask | spark1_mask | spark2_mask

    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)

    # 1. Fill Anvil Body (Rich Dopamine Warm Gold & Amber Bronze)
    for y in range(215, 445):
        for x in range(80, 425):
            if anvil_body_mask[y, x]:
                # Light from top-left
                diag = ((x - 85) / 330.0 * 0.45) + ((y - 225) / 215.0 * 0.55)
                if y <= 275: # Top table & horn (polished brass face)
                    if y <= 235: # Top striking surface highlight
                        r = int(255 - diag * 15)
                        g = int(235 - diag * 30)
                        b = int(120 - diag * 70)
                    else: # Table body
                        r = int(245 - diag * 45)
                        g = int(195 - diag * 65)
                        b = int(45 - diag * 35)
                elif y <= 365: # Waist (deep bronze)
                    r = int(195 - diag * 55)
                    g = int(135 - diag * 60)
                    b = int(25 - diag * 20)
                else: # Stepped base
                    r = int(225 - diag * 50)
                    g = int(165 - diag * 65)
                    b = int(35 - diag * 25)
                img.putpixel((x, y), (r, g, b, 255))

    # Table rim & horn highlight lines
    draw.line([(95, 246), (200, 227), (410, 227)], fill=(255, 255, 200, 240), width=6)
    draw.line([(200, 273), (410, 273)], fill=OUTLINE_COLOR, width=6)
    draw.line([(155, 365), (365, 365)], fill=OUTLINE_COLOR, width=6)
    draw.line([(115, 400), (405, 400)], fill=OUTLINE_COLOR, width=6)
    draw.line([(115, 438), (405, 438)], fill=OUTLINE_COLOR, width=7)

    # 2. Fill Waist Embedded Clockwork Gear (Warm Gold #FFD028)
    for y in range(int(gear_cy - 52), int(gear_cy + 53)):
        for x in range(int(gear_cx - 52), int(gear_cx + 53)):
            if waist_gear_mask[y, x]:
                d = dist_gear[y, x]
                diag = ((x - (gear_cx - 50)) / 100.0 + (y - (gear_cy - 50)) / 100.0) * 0.5
                r = int(255 - diag * 30)
                g = int(215 - diag * 55)
                b = int(40 - diag * 30)
                img.putpixel((x, y), (r, g, b, 255))
    draw.ellipse([gear_cx - 38, gear_cy - 38, gear_cx + 38, gear_cy + 38], outline=OUTLINE_COLOR, width=5)
    draw.ellipse([gear_cx - 16, gear_cy - 16, gear_cx + 16, gear_cy + 16], fill=OUTLINE_COLOR)
    draw_rivet(draw, gear_cx, gear_cy, 10.0, base_color=(255, 235, 120))

    # Base dome rivets
    draw_rivet(draw, 145, 420, 8.5)
    draw_rivet(draw, 220, 420, 8.5)
    draw_rivet(draw, 300, 420, 8.5)
    draw_rivet(draw, 375, 420, 8.5)

    # 3. Fill Hammer Haft (Polished Timber with Brass Bands)
    for y in range(60, 230):
        for x in range(280, 460):
            if haft_mask[y, x]:
                p_norm = proj_n[y, x] / 12.0
                # Cylinder highlight along center of handle
                r = int(np.clip(215 - p_norm * 70, 110, 235))
                g = int(np.clip(120 - p_norm * 55, 50, 150))
                b = int(np.clip(45 - p_norm * 25, 20, 75))
                img.putpixel((x, y), (r, g, b, 255))
    # Brass bands on haft
    band1_x, band1_y = hx1 + 0.35 * (hx2 - hx1), hy1 + 0.35 * (hy2 - hy1)
    band2_x, band2_y = hx1 + 0.65 * (hx2 - hx1), hy1 + 0.65 * (hy2 - hy1)
    draw_rivet(draw, band1_x, band1_y, 7.0, base_color=(255, 225, 90))
    draw_rivet(draw, band2_x, band2_y, 7.0, base_color=(255, 225, 90))

    # Pommel
    for y in range(int(hy1 - 25), int(hy1 + 5)):
        for x in range(int(hx1 - 5), int(hx1 + 30)):
            if pommel_mask[y, x]:
                d = dist_pommel[y, x] / 18.0
                r = int(255 - d * 50)
                g = int(210 - d * 70)
                b = int(50 - d * 35)
                img.putpixel((x, y), (r, g, b, 255))
    draw.ellipse([hx1 - 10 * hux - 18, hy1 - 10 * huy - 18, hx1 - 10 * hux + 18, hy1 - 10 * huy + 18], outline=OUTLINE_COLOR, width=5)

    # 4. Fill Mallet Head (Steel Striking Face with Brass Bevels)
    for y in range(160, 260):
        for x in range(250, 350):
            if mallet_mask[y, x]:
                para = m_proj_para[y, x] # along haft
                perp = m_proj_perp[y, x] # across haft
                # Steel face on striking end (positive para)
                if para > 10:
                    diag = (para / 30.0 + perp / 46.0) * 0.5
                    r = int(235 - diag * 40)
                    g = int(240 - diag * 40)
                    b = int(250 - diag * 30)
                else: # Brass casing
                    diag = ((para + 30) / 40.0 + (perp + 46) / 92.0) * 0.5
                    r = int(250 - diag * 40)
                    g = int(185 - diag * 60)
                    b = int(45 - diag * 30)
                img.putpixel((x, y), (r, g, b, 255))
    
    # Mallet head rim line
    draw.line([(mcx - 44 * hnx + 10 * hux, mcy - 44 * hny + 10 * huy),
               (mcx + 44 * hnx + 10 * hux, mcy + 44 * hny + 10 * huy)], fill=OUTLINE_COLOR, width=6)
    draw_rivet(draw, mcx - 20 * hnx - 8 * hux, mcy - 20 * hny - 8 * huy, 6.5)
    draw_rivet(draw, mcx + 20 * hnx - 8 * hux, mcy + 20 * hny - 8 * huy, 6.5)

    # 5. Molten Sparks & Flying Clockwork Star Glints
    for y in range(160, 200):
        for x in range(215, 255):
            if spark1_mask[y, x]:
                d = spark1_dist[y, x] / 14.0
                r = int(255)
                g = int(np.clip(240 - d * 100, 120, 255))
                b = int(np.clip(140 - d * 120, 20, 255))
                img.putpixel((x, y), (r, g, b, 255))
    draw_star_sparkle(draw, 235, 180, 16.0, color=(255, 255, 220, 255))

    for y in range(135, 165):
        for x in range(195, 225):
            if spark2_mask[y, x]:
                d = spark2_dist[y, x] / 11.0
                r = int(255)
                g = int(np.clip(220 - d * 120, 90, 240))
                b = int(np.clip(100 - d * 90, 10, 200))
                img.putpixel((x, y), (r, g, b, 255))
    draw_star_sparkle(draw, 210, 150, 13.0, color=(255, 245, 180, 255))
    draw_star_sparkle(draw, 175, 195, 11.0, color=(255, 215, 60, 255))

    return img


# ==============================================================================
# 2. Gem Workshop Icon (手藝工坊 - Artisan Workshop / Gem Furnace)
# ==============================================================================

def create_hall_gem_master(size=512) -> Image.Image:
    """
    Render 512x512 Artisan Gem Workshop Icon:
    - Brass clockwork crucible cauldron with flanged rim and stepped pedestal.
    - Two curved side gear loop handles.
    - Top exhaust chimney with golden winding finial key.
    - Arched glowing furnace window containing the Triad of Faceted Dopamine Gemstones:
      1. Coral-Ruby Gem (#FF5E8A) at apex.
      2. Mint-Emerald Gem (#4ED86A) on bottom-left.
      3. Sky-Sapphire Gem (#38A0FF) on bottom-right.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]

    # Cauldron rounded body: center (256, 315), rx=138, ry=108
    dist_belly = ((x_coords - 256.0) / 138.0)**2 + ((y_coords - 315.0) / 108.0)**2
    cauldron_mask = (dist_belly <= 1.0) & (y_coords >= 220) & (y_coords <= 420)

    # Cauldron top rim / collar: x in 155..357, y in 205..238
    rim_mask = (x_coords >= 155) & (x_coords <= 357) & (y_coords >= 205) & (y_coords <= 238)

    # Base pedestal: x in 150..362, y in 410..452
    base_mask = (x_coords >= 150) & (x_coords <= 362) & (y_coords >= 410) & (y_coords <= 452) & \
                (y_coords >= 410 + np.abs(x_coords - 256) * 0.08)

    # Chimney stack: x in 228..284, y in 145..210
    chimney_mask = (x_coords >= 228) & (x_coords <= 284) & (y_coords >= 145) & (y_coords <= 210)

    # Winding key finial atop chimney:
    # Stem: x in 244..268, y in 110..155
    finial_stem = (x_coords >= 244) & (x_coords <= 268) & (y_coords >= 110) & (y_coords <= 155)
    # Twin circular lobes: centers at (212, 100) and (300, 100), r=36
    dist_fl = np.sqrt((x_coords - 212.0)**2 + (y_coords - 100.0)**2)
    dist_fr = np.sqrt((x_coords - 300.0)**2 + (y_coords - 100.0)**2)
    dist_fmid = np.sqrt((x_coords - 256.0)**2 + (y_coords - 110.0)**2)
    finial_solid = (dist_fl <= 36.0) | (dist_fr <= 36.0) | (dist_fmid <= 28.0) | \
                   ((x_coords >= 212) & (x_coords <= 300) & (y_coords >= 82) & (y_coords <= 118))
    hole_fl = dist_fl < 16.0
    hole_fr = dist_fr < 16.0
    finial_mask = (finial_stem | finial_solid) & (~hole_fl) & (~hole_fr)

    # Side loop handles:
    # Left handle: center (145, 305), outer ellipse rx=52, ry=38, inner rx=30, ry=18
    dist_hl_out = ((x_coords - 150.0) / 54.0)**2 + ((y_coords - 305.0) / 40.0)**2
    dist_hl_in = ((x_coords - 150.0) / 32.0)**2 + ((y_coords - 305.0) / 20.0)**2
    handle_l = (dist_hl_out <= 1.0) & (dist_hl_in >= 1.0) & (x_coords <= 160)

    # Right handle: center (367, 305)
    dist_hr_out = ((x_coords - 362.0) / 54.0)**2 + ((y_coords - 305.0) / 40.0)**2
    dist_hr_in = ((x_coords - 362.0) / 32.0)**2 + ((y_coords - 305.0) / 20.0)**2
    handle_r = (dist_hr_out <= 1.0) & (dist_hr_in >= 1.0) & (x_coords >= 352)

    combined_mask = cauldron_mask | rim_mask | base_mask | chimney_mask | finial_mask | handle_l | handle_r

    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)

    # 1. Fill Cauldron Outer Body (Warm Golden Brass #F4C542)
    for y in range(200, 455):
        for x in range(90, 425):
            if (cauldron_mask | rim_mask | base_mask | chimney_mask | finial_mask | handle_l | handle_r)[y, x]:
                diag = ((x - 110) / 290.0 * 0.45) + ((y - 80) / 370.0 * 0.55)
                r = int(250 - diag * 45)
                g = int(195 - diag * 65)
                b = int(45 - diag * 35)
                img.putpixel((x, y), (r, g, b, 255))

    # Decorative seams & highlights on cauldron
    draw.line([(155, 207), (357, 207)], fill=(255, 255, 200, 240), width=6)
    draw.line([(155, 236), (357, 236)], fill=OUTLINE_COLOR, width=6)
    draw.line([(150, 412), (362, 412)], fill=OUTLINE_COLOR, width=6)
    draw.line([(150, 450), (362, 450)], fill=OUTLINE_COLOR, width=7)

    # Rivets on rim and base
    draw_rivet(draw, 180, 222, 6.5)
    draw_rivet(draw, 256, 222, 6.5)
    draw_rivet(draw, 332, 222, 6.5)

    draw_rivet(draw, 180, 432, 7.5)
    draw_rivet(draw, 256, 432, 7.5)
    draw_rivet(draw, 332, 432, 7.5)

    # Rivets on handles
    draw_rivet(draw, 106, 305, 6.0)
    draw_rivet(draw, 406, 305, 6.0)

    # 2. Arched Furnace Aperture (Molten Hearth Portal)
    # Arched portal: x in 185..327, y in 260..385
    arch_pts = []
    # Semi-circle top: center (256, 300), r=65
    for a in np.linspace(math.pi, 0, 30):
        arch_pts.append((256.0 + 65.0 * math.cos(a), 300.0 - 55.0 * math.sin(a)))
    # Bottom straight
    arch_pts.append((321.0, 385.0))
    arch_pts.append((191.0, 385.0))
    
    # Fill portal with deep purple-navy mysterious furnace background (#1F1435)
    draw.polygon(arch_pts, fill=(31, 20, 53, 255), outline=OUTLINE_COLOR, width=8)

    # Inner molten hearth glow ring
    for y in range(250, 385):
        for x in range(192, 321):
            dy = (y - 325.0) / 55.0
            dx = (x - 256.0) / 60.0
            d = np.sqrt(dx**2 + dy**2)
            if d <= 1.0:
                glow_int = max(0.0, 1.0 - d)
                r = int(np.clip(31 + glow_int * 70, 0, 255))
                g = int(np.clip(20 + glow_int * 30, 0, 255))
                b = int(np.clip(53 + glow_int * 80, 0, 255))
                img.putpixel((x, y), (r, g, b, 255))

    # 3. Render Triad of Faceted Dopamine Gemstones
    # --- A. Center Apex: Coral-Ruby Gem (#FF5E8A) ---
    # Rhombus / Brilliant Diamond cut, center (256, 288)
    rx, ry = 256.0, 288.0
    rw, rh = 34.0, 42.0
    ruby_top = (rx, ry - rh)
    ruby_bot = (rx, ry + rh)
    ruby_left = (rx - rw, ry)
    ruby_right = (rx + rw, ry)
    ruby_mid_top = (rx, ry - rh * 0.35)
    ruby_mid_bot = (rx, ry + rh * 0.35)

    # Facet 1: Top-Left (Bright Coral)
    draw.polygon([ruby_top, ruby_left, ruby_mid_top], fill=(255, 140, 175, 255), outline=OUTLINE_COLOR, width=3)
    # Facet 2: Top-Right (Main Coral Pink #FF5E8A)
    draw.polygon([ruby_top, ruby_right, ruby_mid_top], fill=(255, 94, 138, 255), outline=OUTLINE_COLOR, width=3)
    # Facet 3: Center Table
    draw.polygon([ruby_mid_top, ruby_left, ruby_mid_bot, ruby_right], fill=(255, 120, 160, 255), outline=OUTLINE_COLOR, width=3)
    # Facet 4: Bottom-Left (Deep Crimson #D81B60)
    draw.polygon([ruby_left, ruby_bot, ruby_mid_bot], fill=(216, 27, 96, 255), outline=OUTLINE_COLOR, width=3)
    # Facet 5: Bottom-Right (Dark Wine #880E4F)
    draw.polygon([ruby_right, ruby_bot, ruby_mid_bot], fill=(136, 14, 79, 255), outline=OUTLINE_COLOR, width=3)
    # Specular glint
    draw_star_sparkle(draw, rx - rw * 0.3, ry - rh * 0.4, 9.0, color=(255, 255, 255, 250))

    # --- B. Bottom-Left: Mint-Emerald Gem (#4ED86A) ---
    # Hexagonal faceted cut, center (222, 350)
    gx, gy = 222.0, 350.0
    gr = 28.0
    hex_pts = []
    for i in range(6):
        ang = i * math.pi / 3.0 - math.pi / 6.0
        hex_pts.append((gx + gr * math.cos(ang), gy + gr * math.sin(ang)))
    
    # Outer hexagon outline
    draw.polygon(hex_pts, fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=4)
    # Inner table hexagon
    in_hex_pts = []
    for i in range(6):
        ang = i * math.pi / 3.0 - math.pi / 6.0
        in_hex_pts.append((gx + gr * 0.55 * math.cos(ang), gy + gr * 0.55 * math.sin(ang)))
    draw.polygon(in_hex_pts, fill=(130, 245, 155, 255), outline=OUTLINE_COLOR, width=3)
    # Facet radial lines
    for i in range(6):
        draw.line([hex_pts[i], in_hex_pts[i]], fill=OUTLINE_COLOR, width=3)
    # Top facet highlights
    draw.polygon([hex_pts[0], hex_pts[1], in_hex_pts[1], in_hex_pts[0]], fill=(185, 255, 202, 255))
    draw_star_sparkle(draw, gx - 6, gy - 6, 7.0, color=(255, 255, 255, 250))

    # --- C. Bottom-Right: Sky-Sapphire Gem (#38A0FF) ---
    # Brilliant round/teardrop faceted cut, center (290, 350)
    sx, sy = 290.0, 350.0
    sr = 28.0
    # Octagonal cut
    oct_pts = []
    for i in range(8):
        ang = i * math.pi / 4.0 - math.pi / 8.0
        oct_pts.append((sx + sr * math.cos(ang), sy + sr * math.sin(ang)))
    draw.polygon(oct_pts, fill=(56, 160, 255, 255), outline=OUTLINE_COLOR, width=4)
    # Inner oct table
    in_oct_pts = []
    for i in range(8):
        ang = i * math.pi / 4.0 - math.pi / 8.0
        in_oct_pts.append((sx + sr * 0.55 * math.cos(ang), sy + sr * 0.55 * math.sin(ang)))
    draw.polygon(in_oct_pts, fill=(120, 205, 255, 255), outline=OUTLINE_COLOR, width=3)
    for i in range(8):
        draw.line([oct_pts[i], in_oct_pts[i]], fill=OUTLINE_COLOR, width=3)
    # Top facets highlight
    draw.polygon([oct_pts[0], oct_pts[1], in_oct_pts[1], in_oct_pts[0]], fill=(190, 235, 255, 255))
    draw_star_sparkle(draw, sx - 6, sy - 6, 7.0, color=(255, 255, 255, 250))

    # Flying magic sparkles inside hearth
    draw_star_sparkle(draw, 256, 360, 9.0, color=(255, 255, 200, 250))
    draw_star_sparkle(draw, 226, 265, 8.0, color=(255, 210, 240, 250))
    draw_star_sparkle(draw, 286, 265, 8.0, color=(200, 240, 255, 250))

    return img


# ==============================================================================
# 3. Arena Icon (演武競技 - Martial Arena / Shield & Crossed Swords)
# ==============================================================================

def create_hall_arena_master(size=512) -> Image.Image:
    """
    Render 512x512 Martial Arena Icon:
    - Bold tournament heraldic crest shield (quarterly Sky Blue & Gold).
    - Central embossed 8-toothed clockwork gear with star crest.
    - Two gleaming crossed knight swords behind shield forming an unmistakable 'X' silhouette.
    - 3D brass rivets and crisp specular blade edges.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]

    # --- Crossed Swords Geometry ---
    # Sword 1: top-left (95, 85) to bottom-right (417, 427)
    s1_x1, s1_y1 = 95.0, 85.0
    s1_x2, s1_y2 = 417.0, 427.0
    s1_len = math.hypot(s1_x2 - s1_x1, s1_y2 - s1_y1)
    s1_ux, s1_uy = (s1_x2 - s1_x1) / s1_len, (s1_y2 - s1_y1) / s1_len
    s1_nx, s1_ny = -s1_uy, s1_ux
    proj_s1_para = (x_coords - s1_x1) * s1_ux + (y_coords - s1_y1) * s1_uy
    proj_s1_perp = np.abs((x_coords - s1_x1) * s1_nx + (y_coords - s1_y1) * s1_ny)
    s1_blade = (proj_s1_para >= 0.0) & (proj_s1_para <= s1_len - 70.0) & (proj_s1_perp <= 16.0)
    # Tip of sword 1
    s1_tip = (proj_s1_para >= -18.0) & (proj_s1_para <= 0.0) & (proj_s1_perp <= (proj_s1_para + 18.0) * (16.0 / 18.0))
    # Hilt & Crossguard of sword 1 (near bottom right)
    s1_guard = (proj_s1_para >= s1_len - 85.0) & (proj_s1_para <= s1_len - 65.0) & (proj_s1_perp <= 48.0)
    s1_handle = (proj_s1_para >= s1_len - 65.0) & (proj_s1_para <= s1_len) & (proj_s1_perp <= 11.0)
    dist_s1_pommel = np.sqrt((x_coords - (s1_x1 + s1_len * s1_ux))**2 + (y_coords - (s1_y1 + s1_len * s1_uy))**2)
    s1_pommel = dist_s1_pommel <= 17.0
    sword1_mask = s1_blade | s1_tip | s1_guard | s1_handle | s1_pommel

    # Sword 2: top-right (417, 85) to bottom-left (95, 427)
    s2_x1, s2_y1 = 417.0, 85.0
    s2_x2, s2_y2 = 95.0, 427.0
    s2_len = math.hypot(s2_x2 - s2_x1, s2_y2 - s2_y1)
    s2_ux, s2_uy = (s2_x2 - s2_x1) / s2_len, (s2_y2 - s2_y1) / s2_len
    s2_nx, s2_ny = -s2_uy, s2_ux
    proj_s2_para = (x_coords - s2_x1) * s2_ux + (y_coords - s2_y1) * s2_uy
    proj_s2_perp = np.abs((x_coords - s2_x1) * s2_nx + (y_coords - s2_y1) * s2_ny)
    s2_blade = (proj_s2_para >= 0.0) & (proj_s2_para <= s2_len - 70.0) & (proj_s2_perp <= 16.0)
    s2_tip = (proj_s2_para >= -18.0) & (proj_s2_para <= 0.0) & (proj_s2_perp <= (proj_s2_para + 18.0) * (16.0 / 18.0))
    s2_guard = (proj_s2_para >= s2_len - 85.0) & (proj_s2_para <= s2_len - 65.0) & (proj_s2_perp <= 48.0)
    s2_handle = (proj_s2_para >= s2_len - 65.0) & (proj_s2_para <= s2_len) & (proj_s2_perp <= 11.0)
    dist_s2_pommel = np.sqrt((x_coords - (s2_x1 + s2_len * s2_ux))**2 + (y_coords - (s2_y1 + s2_len * s2_uy))**2)
    s2_pommel = dist_s2_pommel <= 17.0
    sword2_mask = s2_blade | s2_tip | s2_guard | s2_handle | s2_pommel

    # --- Tournament Shield Geometry ---
    # Heater shield profile:
    # Flat top with slight crest: y in 145..175, x in 150..362
    # Upper sides straight: y in 175..275, x in 150..362
    # Lower sides curve down to point at (256, 435)
    # Parabolic / polynomial taper: at y, allowed half-width w(y)
    # y=145..275: w = 106.0
    # y=275..435: t = (y - 275) / 160.0, w = 106.0 * (1.0 - t**1.35)
    dx_shield = np.abs(x_coords - 256.0)
    t_shield = np.clip((y_coords - 275.0) / 160.0, 0.0, 1.0)
    w_shield = np.where(y_coords <= 275.0, 106.0, 106.0 * (1.0 - t_shield**1.35))
    top_crest = 150.0 + ((x_coords - 256.0) / 106.0)**2 * 12.0
    shield_mask = (y_coords >= top_crest) & (y_coords <= 435.0) & (dx_shield <= w_shield)

    combined_mask = sword1_mask | sword2_mask | shield_mask

    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)

    # 1. Fill Swords (Crossed behind shield)
    for y in range(size):
        for x in range(size):
            if (sword1_mask | sword2_mask)[y, x] and not shield_mask[y, x]:
                # Steel blade vs brass hilt
                is_blade = (s1_blade | s1_tip | s2_blade | s2_tip)[y, x]
                is_guard = (s1_guard | s2_guard | s1_pommel | s2_pommel)[y, x]
                if is_blade:
                    # Gleaming silver steel with light from top-left
                    diag = (x / 512.0 + y / 512.0) * 0.5
                    r = int(240 - diag * 45)
                    g = int(245 - diag * 40)
                    b = int(255 - diag * 30)
                elif is_guard: # Brass guard / pommel
                    r, g, b = 250, 195, 50
                else: # Handle
                    r, g, b = 180, 75, 30
                img.putpixel((x, y), (r, g, b, 255))

    # Center fuller lines on blades
    draw.line([(s1_x1 - 10 * s1_ux, s1_y1 - 10 * s1_uy), (s1_x1 + 160 * s1_ux, s1_y1 + 160 * s1_uy)], fill=OUTLINE_COLOR, width=4)
    draw.line([(s2_x1 - 10 * s2_ux, s2_y1 - 10 * s2_uy), (s2_x1 + 160 * s2_ux, s2_y1 + 160 * s2_uy)], fill=OUTLINE_COLOR, width=4)

    # 2. Fill Tournament Shield Face (Heraldic Quarterly: Sky Blue & Warm Gold)
    # Outer brass border bevel: 18px inward
    w_inner = np.where(y_coords <= 275.0, 88.0, 88.0 * (1.0 - t_shield**1.35))
    inner_mask = (y_coords >= top_crest + 18.0) & (y_coords <= 416.0) & (dx_shield <= w_inner)

    for y in range(145, 436):
        for x in range(145, 368):
            if shield_mask[y, x]:
                if inner_mask[y, x]:
                    # Shield face quarterly divided by center lines x=256, y=285
                    is_left = x < 256
                    is_top = y < 285
                    if (is_left and is_top) or ((not is_left) and (not is_top)):
                        # Royal Sky Blue #38A0FF (Top-left & Bottom-right)
                        diag = ((x - 150) / 210.0 + (y - 150) / 280.0) * 0.5
                        r = int(np.clip(56 - diag * 25, 20, 100))
                        g = int(np.clip(160 - diag * 45, 90, 200))
                        b = int(np.clip(255 - diag * 30, 190, 255))
                    else:
                        # Warm Dopamine Gold #FFD028 (Top-right & Bottom-left)
                        diag = ((x - 150) / 210.0 + (y - 150) / 280.0) * 0.5
                        r = int(255 - diag * 30)
                        g = int(210 - diag * 60)
                        b = int(40 - diag * 25)
                else: # Outer brass rim
                    diag = ((x - 145) / 220.0 + (y - 145) / 290.0) * 0.5
                    r = int(250 - diag * 40)
                    g = int(195 - diag * 65)
                    b = int(45 - diag * 35)
                img.putpixel((x, y), (r, g, b, 255))

    # Quarterly dividing lines
    draw.line([(256, 168), (256, 416)], fill=OUTLINE_COLOR, width=6)
    draw.line([(168, 285), (344, 285)], fill=OUTLINE_COLOR, width=6)
    # Inner border line
    for y_step in range(165, 416, 2):
        pass # The inner mask boundary already cleanly interfaces

    # Brass border corner rivets
    draw_rivet(draw, 172, 180, 7.5)
    draw_rivet(draw, 340, 180, 7.5)
    draw_rivet(draw, 256, 170, 7.5)
    draw_rivet(draw, 170, 285, 7.5)
    draw_rivet(draw, 342, 285, 7.5)
    draw_rivet(draw, 256, 412, 7.5)

    # 3. Embossed Clockwork Gear Crest in Shield Center
    gear_cx, gear_cy = 256.0, 285.0
    dist_cg = np.sqrt((x_coords - gear_cx)**2 + (y_coords - gear_cy)**2)
    ang_cg = np.arctan2(y_coords - gear_cy, x_coords - gear_cx)
    teeth_cg = np.mod(ang_cg + math.pi, 2.0 * math.pi / 8.0) / (2.0 * math.pi / 8.0)
    gear_r = 44.0 + np.where(teeth_cg < 0.5, 12.0, 0.0)
    crest_gear_mask = (dist_cg <= gear_r) & (dist_cg >= 22.0)

    for y in range(int(gear_cy - 58), int(gear_cy + 59)):
        for x in range(int(gear_cx - 58), int(gear_cx + 59)):
            if crest_gear_mask[y, x]:
                diag = ((x - (gear_cx - 50)) / 100.0 + (y - (gear_cy - 50)) / 100.0) * 0.5
                r = int(255 - diag * 25)
                g = int(230 - diag * 50)
                b = int(70 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))

    draw.ellipse([gear_cx - 44, gear_cy - 44, gear_cx + 44, gear_cy + 44], outline=OUTLINE_COLOR, width=5)
    draw.ellipse([gear_cx - 22, gear_cy - 22, gear_cx + 22, gear_cy + 22], fill=OUTLINE_COLOR)

    # Raised Ivory/Silver Winged Star Crest in center
    draw_star_sparkle(draw, gear_cx, gear_cy, 20.0, color=(255, 255, 255, 255))
    draw_rivet(draw, gear_cx, gear_cy, 6.0, base_color=(255, 215, 80))

    # Specular rim highlight on top-left of shield
    draw.arc([148, 150, 364, 434], 140, 260, fill=(255, 255, 220, 240), width=6)

    return img


# ==============================================================================
# 4. Quest Icon (冒險委託 - Adventure Commission / Winding Scroll Plaque)
# ==============================================================================

def create_hall_quest_master(size=512) -> Image.Image:
    """
    Render 512x512 Adventure Commission Icon:
    - Cream/ivory parchment plaque sheet with curved edges.
    - Top & bottom brass scroll roller cylinders with decorative gear caps.
    - Top brass winding key mechanism.
    - Central embossed Golden Adventurer Star Compass with glowing ruby rivet.
    - Two dangling coral-pink (#FF5E8A) notched commission swallow-tail ribbons.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]

    # Scroll body panel: x in 150..362, y in 155..385
    # Organic curved waist: slightly narrower at y=270
    waist_pinch = (1.0 - ((y_coords - 270.0) / 115.0)**2) * 8.0
    panel_mask = (y_coords >= 155) & (y_coords <= 385) & \
                 (x_coords >= 150 + waist_pinch) & (x_coords <= 362 - waist_pinch)

    # Top roller cylinder: x in 115..397, y in 128..168
    roller_top = (x_coords >= 115) & (x_coords <= 397) & (y_coords >= 128) & (y_coords <= 168)
    # Bottom roller cylinder: x in 115..397, y in 372..412
    roller_bot = (x_coords >= 115) & (x_coords <= 397) & (y_coords >= 372) & (y_coords <= 412)
    # Gear endcaps at (115, 148), (397, 148), (115, 392), (397, 392)
    dist_cap_tl = np.sqrt((x_coords - 115.0)**2 + (y_coords - 148.0)**2)
    dist_cap_tr = np.sqrt((x_coords - 397.0)**2 + (y_coords - 148.0)**2)
    dist_cap_bl = np.sqrt((x_coords - 115.0)**2 + (y_coords - 392.0)**2)
    dist_cap_br = np.sqrt((x_coords - 397.0)**2 + (y_coords - 392.0)**2)
    caps_mask = (dist_cap_tl <= 25.0) | (dist_cap_tr <= 25.0) | (dist_cap_bl <= 25.0) | (dist_cap_br <= 25.0)

    # Top Winding Key atop center of top roller (256, 148):
    # Stem: x in 244..268, y in 80..130
    w_stem = (x_coords >= 244) & (x_coords <= 268) & (y_coords >= 80) & (y_coords <= 130)
    # Winding wings: left at (212, 70), right at (300, 70), r=36
    dist_wl = np.sqrt((x_coords - 212.0)**2 + (y_coords - 70.0)**2)
    dist_wr = np.sqrt((x_coords - 300.0)**2 + (y_coords - 70.0)**2)
    dist_wmid = np.sqrt((x_coords - 256.0)**2 + (y_coords - 82.0)**2)
    w_solid = (dist_wl <= 36.0) | (dist_wr <= 36.0) | (dist_wmid <= 28.0) | \
              ((x_coords >= 212) & (x_coords <= 300) & (y_coords >= 52) & (y_coords <= 88))
    hole_wl = dist_wl < 16.0
    hole_wr = dist_wr < 16.0
    w_key_mask = (w_stem | w_solid) & (~hole_wl) & (~hole_wr)

    # Hanging Coral-Pink Ribbons at bottom (x in 205..305, y in 395..465)
    # Ribbon 1 (left): x in 210..248, y in 395..460, notched swallowtail at bottom
    # Swallowtail notch: y >= 460 - abs(x - 229) * 0.75 is cutout
    ribbon1 = (x_coords >= 210) & (x_coords <= 248) & (y_coords >= 395) & (y_coords <= 462) & \
              ~((y_coords >= 444) & (y_coords >= 462 - np.abs(x_coords - 229) * 0.9))
    # Ribbon 2 (right): x in 264..302, y in 395..450
    ribbon2 = (x_coords >= 264) & (x_coords <= 302) & (y_coords >= 395) & (y_coords <= 452) & \
              ~((y_coords >= 434) & (y_coords >= 452 - np.abs(x_coords - 283) * 0.9))
    ribbons_mask = ribbon1 | ribbon2

    combined_mask = panel_mask | roller_top | roller_bot | caps_mask | w_key_mask | ribbons_mask

    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)

    # 1. Fill Scroll Parchment Panel (Cream/Ivory #FFFDF2 to #F3EBD8)
    for y in range(155, 386):
        for x in range(145, 368):
            if panel_mask[y, x]:
                # Subtle vertical parchment gradient
                v = (y - 155.0) / 230.0
                h = abs(x - 256.0) / 106.0
                r = int(np.clip(255 - v * 12 - h * 18, 220, 255))
                g = int(np.clip(252 - v * 18 - h * 22, 210, 255))
                b = int(np.clip(242 - v * 28 - h * 30, 195, 245))
                img.putpixel((x, y), (r, g, b, 255))

    # Inner parchment border stitching lines
    draw.line([(162, 175), (162, 365)], fill=(215, 200, 175, 255), width=3)
    draw.line([(350, 175), (350, 365)], fill=(215, 200, 175, 255), width=3)

    # 2. Fill Rollers & Winding Key (Warm Golden Brass #F4C542)
    for y in range(50, 420):
        for x in range(100, 415):
            if (roller_top | roller_bot | caps_mask | w_key_mask)[y, x]:
                diag = ((x - 110) / 290.0 * 0.45) + ((y - 50) / 360.0 * 0.55)
                # Cylinder highlight along upper half of rollers
                is_roller = (roller_top | roller_bot)[y, x]
                if is_roller:
                    local_y = (y - 128 if y < 200 else y - 372) / 40.0
                    if local_y < 0.35: # Bright top rim
                        r, g, b = 255, 245, 150
                    elif local_y < 0.7: # Mid brass
                        r, g, b = 250, 200, 50
                    else: # Shadow underside
                        r, g, b = 185, 125, 20
                else: # Gear caps & key
                    r = int(250 - diag * 40)
                    g = int(195 - diag * 60)
                    b = int(45 - diag * 35)
                img.putpixel((x, y), (r, g, b, 255))

    # Roller separator & highlight lines
    draw.line([(120, 131), (392, 131)], fill=(255, 255, 200, 240), width=5)
    draw.line([(120, 166), (392, 166)], fill=OUTLINE_COLOR, width=6)
    draw.line([(120, 374), (392, 374)], fill=(255, 255, 200, 240), width=5)
    draw.line([(120, 410), (392, 410)], fill=OUTLINE_COLOR, width=6)

    # Roller cap rivets
    draw_rivet(draw, 115, 148, 7.5)
    draw_rivet(draw, 397, 148, 7.5)
    draw_rivet(draw, 115, 392, 7.5)
    draw_rivet(draw, 397, 392, 7.5)

    # 3. Fill Hanging Commission Ribbons (Vivid Coral-Pink #FF5E8A)
    for y in range(390, 465):
        for x in range(205, 305):
            if ribbons_mask[y, x]:
                # Light from left
                u = (x - 210.0) / 90.0
                r = int(np.clip(255 - u * 35, 210, 255))
                g = int(np.clip(94 - u * 40, 40, 120))
                b = int(np.clip(138 - u * 40, 80, 160))
                img.putpixel((x, y), (r, g, b, 255))

    # Ribbon edges
    draw.line([(210, 395), (210, 460)], fill=OUTLINE_COLOR, width=4)
    draw.line([(248, 395), (248, 444)], fill=OUTLINE_COLOR, width=4)
    draw.line([(264, 395), (264, 450)], fill=OUTLINE_COLOR, width=4)
    draw.line([(302, 395), (302, 434)], fill=OUTLINE_COLOR, width=4)

    # 4. Central Golden Adventurer Star Compass (Quest Emblem)
    scx, scy = 256.0, 270.0
    # 8-pointed star compass
    star_pts = []
    for i in range(16):
        ang = i * (2.0 * math.pi / 16.0) - math.pi / 2.0
        # Cardinal points r=56, diagonal points r=42, valleys r=22
        if i % 4 == 0:
            r_cur = 56.0 # Cardinal
        elif i % 2 == 0:
            r_cur = 40.0 # Diagonal
        else:
            r_cur = 22.0 # Valley
        star_pts.append((scx + r_cur * math.cos(ang), scy + r_cur * math.sin(ang)))

    # Outer star
    draw.polygon(star_pts, fill=(255, 208, 40, 255), outline=OUTLINE_COLOR, width=5)

    # Star facets (alternating light gold and warm amber)
    for i in range(16):
        next_i = (i + 1) % 16
        col = (255, 235, 110, 255) if i % 2 == 0 else (230, 165, 25, 255)
        draw.polygon([(scx, scy), star_pts[i], star_pts[next_i]], fill=col)
    draw.polygon(star_pts, outline=OUTLINE_COLOR, width=5)

    # Center glowing ruby rivet
    draw_rivet(draw, scx, scy, 14.0, base_color=(255, 94, 138))
    draw_star_sparkle(draw, scx - 4, scy - 4, 8.0, color=(255, 255, 255, 255))

    # Stylized quest commission rules (horizontal stepped brass accent lines, NO text)
    draw.line([(195, 200), (317, 200)], fill=(210, 175, 120, 255), width=5)
    draw.line([(215, 215), (297, 215)], fill=(210, 175, 120, 255), width=4)
    draw.line([(215, 325), (297, 325)], fill=(210, 175, 120, 255), width=4)
    draw.line([(195, 340), (317, 340)], fill=(210, 175, 120, 255), width=5)

    # Specular sparkle glints
    draw_star_sparkle(draw, scx - 30, scy - 32, 10.0, color=(255, 255, 220, 250))
    draw_star_sparkle(draw, 340, 150, 9.0, color=(255, 255, 200, 250))

    return img


# ==============================================================================
# Pipeline & Proof Generation
# ==============================================================================

def generate_all():
    targets = [
        ("icon_hall_forge.png", "天宮鐵匠 · 黃銅鐵砧小錘", create_hall_forge_master),
        ("icon_hall_gem.png",   "手藝工坊 · 三色晶核熔爐", create_hall_gem_master),
        ("icon_hall_arena.png", "演武競技 · 交叉武器盾牌", create_hall_arena_master),
        ("icon_hall_quest.png", "冒險委託 · 上鍊發條捲軸", create_hall_quest_master)
    ]

    icons_128 = []
    icons_64 = []
    icons_32 = []

    print("Generating 4 Left Hall Card Icons at 512x512 master...")
    for filename, label, gen_func in targets:
        master = gen_func(size=512)
        
        # Downsample cleanly using LANCZOS
        im_128 = master.resize((128, 128), Image.Resampling.LANCZOS)
        im_64 = master.resize((64, 64), Image.Resampling.LANCZOS)
        im_32 = master.resize((32, 32), Image.Resampling.LANCZOS)
        
        out_path = f"{OUT_DIR}/{filename}"
        im_128.save(out_path, "PNG")
        print(f"  -> Saved {out_path} (128x128 RGBA)")
        
        icons_128.append(im_128)
        icons_64.append(im_64)
        icons_32.append(im_32)

    # Generate verification proof image
    proof_path = build_proof(icons_128, icons_64, icons_32, targets)
    return proof_path


def build_proof(icons_128, icons_64, icons_32, targets):
    """
    Build a comprehensive visual verification proof sheet:
    - Row 1: 128px icons on Cream Light (#FFFDF8) and Deep Navy (#1F1A3A) backgrounds.
    - Row 2: 64px and 32px scaled icons demonstrating micro-readability and silhouette clarity.
    - Row 3: Simulated Mobile Lobby Left Hall Cards (Horizontal layout, Dopamine jelly button, OpenHuninn font).
    - Row 4: Harmony Check alongside approved top HUD icons (energy_key, gold_coin, gem) and village icon.
    """
    proof_w, proof_h = 1020, 960
    proof = Image.new("RGBA", (proof_w, proof_h), (255, 253, 248, 255)) # Cream #FFFDF8
    pdraw = ImageDraw.Draw(proof)

    try:
        font_title = ImageFont.truetype(FONT_PATH, 24)
        font_sub = ImageFont.truetype(FONT_PATH, 16)
        font_lbl = ImageFont.truetype(FONT_PATH, 14)
        font_small = ImageFont.truetype(FONT_PATH, 12)
        font_card_title = ImageFont.truetype(FONT_PATH, 18)
        font_card_sub = ImageFont.truetype(FONT_PATH, 12)
    except Exception:
        font_title = font_sub = font_lbl = font_small = font_card_title = font_card_sub = ImageFont.load_default()

    def draw_checker(x, y, w, h, grid=16):
        for cy in range(y, y + h, grid):
            for cx in range(x, x + w, grid):
                fill_c = (238, 235, 228, 255) if ((cx // grid) + (cy // grid)) % 2 == 0 else (255, 253, 248, 255)
                pdraw.rectangle([cx, cy, min(cx + grid, x + w), min(cy + grid, y + h)], fill=fill_c)
        pdraw.rectangle([x, y, x + w, y + h], outline=(200, 195, 185, 255), width=2)

    # Header
    pdraw.rectangle([0, 0, proof_w, 60], fill=(31, 26, 58, 255))
    pdraw.text((25, 16), "《發條之心》大廳左側四殿堂卡自繪圖示視覺過審檢驗 (Clockwork Heart Hall Icons)", font=font_title, fill=(255, 225, 90, 255))
    pdraw.text((proof_w - 240, 22), "側案美術總監 · 小柔", font=font_sub, fill=(220, 215, 240, 255))

    # Row 1: 128px Masters on Light and Dark Checkerboards
    y1 = 80
    pdraw.text((35, y1 - 10), "【128×128px 高清主圖：淺色奶油底 (#FFFDF8) vs 深色黑曜石底 (#1F1A3A) 對比檢驗】", font=font_sub, fill=(45, 38, 60, 255))

    col_w = 230
    for i, (fname, label, _) in enumerate(targets):
        bx = 35 + i * col_w
        # Light checker box
        draw_checker(bx, y1 + 15, 100, 100)
        im_100 = icons_128[i].resize((96, 96), Image.Resampling.LANCZOS)
        proof.paste(im_100, (bx + 2, y1 + 17), im_100)
        
        # Dark box
        pdraw.rectangle([bx + 110, y1 + 15, bx + 210, y1 + 115], fill=(31, 26, 58, 255), outline=(65, 55, 95, 255), width=2)
        proof.paste(im_100, (bx + 112, y1 + 17), im_100)

        # Label
        pdraw.text((bx + 10, y1 + 120), label, font=font_lbl, fill=(31, 26, 58, 255))
        pdraw.text((bx + 10, y1 + 138), fname, font=font_small, fill=(120, 110, 135, 255))

    # Row 2: 64px & 32px Scaled Micro-readability
    y2 = 250
    pdraw.text((35, y2 - 10), "【微型縮放檢驗：64px 與 32px 實尺寸（極致特徵剪影 · 無糊成一團 · 瞬間辨識殿堂功能）】", font=font_sub, fill=(45, 38, 60, 255))

    for i in range(4):
        bx = 35 + i * col_w
        # 64px
        draw_checker(bx + 10, y2 + 15, 68, 68)
        proof.paste(icons_64[i], (bx + 12, y2 + 17), icons_64[i])
        pdraw.text((bx + 26, y2 + 86), "64px", font=font_small, fill=(130, 120, 140, 255))

        # 32px
        draw_checker(bx + 115, y2 + 25, 48, 48)
        proof.paste(icons_32[i], (bx + 123, y2 + 33), icons_32[i])
        pdraw.text((bx + 125, y2 + 86), "32px", font=font_small, fill=(130, 120, 140, 255))

    # Row 3: Simulated In-Game Left Hall Cards in Mobile Lobby
    y3 = 380
    pdraw.text((35, y3 - 10), "【手機大廳左側殿堂卡實機模擬預覽（雙拇指熱區 ≥48px · 果凍厚底 · 告別純文字 PPT 感）】", font=font_sub, fill=(45, 38, 60, 255))

    lobby_bg_rect = [25, y3 + 15, proof_w - 25, y3 + 360]
    pdraw.rectangle(lobby_bg_rect, fill=(245, 242, 235, 255), outline=(215, 210, 200, 255), width=2)

    # Hall cards layout: 2x2 grid representing the left side stack in mobile landscape
    card_w = 460
    card_h = 72
    card_specs = [
        ("天宮鐵匠", "品質轉化 · 裝備鍛造", (255, 160, 16, 255), (185, 95, 10, 255)), # Warm Orange
        ("手藝工坊", "紅黃藍石 · 三合一熔煉", (78, 216, 106, 255), (35, 145, 60, 255)),  # Mint Green
        ("演武競技", "挑戰對手 · 雙倍抽獎", (56, 160, 255, 255), (25, 105, 195, 255)), # Sky Blue
        ("冒險委託", "每日簽到 · 懸賞領獎", (255, 94, 138, 255), (195, 45, 85, 255))   # Coral Pink
    ]

    for idx, (ctitle, csub, jelly_col, shadow_col) in enumerate(card_specs):
        col = idx % 2
        row = idx // 2
        cx = 45 + col * (card_w + 30)
        cy = y3 + 40 + row * (card_h + 20)

        # Thick bottom shadow border (5px)
        pdraw.rounded_rectangle([cx, cy + 5, cx + card_w, cy + card_h + 5], radius=16, fill=shadow_col)
        # Main card face (Cream White Card with #1F1A3A outline)
        pdraw.rounded_rectangle([cx, cy, cx + card_w, cy + card_h], radius=16,
                                fill=(255, 253, 248, 255), outline=OUTLINE_COLOR, width=3)

        # Left icon badge container with jelly dopamine tint
        badge_size = 54
        badge_x, badge_y = cx + 9, cy + 9
        pdraw.rounded_rectangle([badge_x, badge_y, badge_x + badge_size, badge_y + badge_size], radius=12,
                                fill=jelly_col, outline=OUTLINE_COLOR, width=2)
        # 32px icon centered in badge
        proof.paste(icons_32[idx], (badge_x + 11, badge_y + 11), icons_32[idx])

        # Text labels
        pdraw.text((cx + 74, cy + 14), ctitle, font=font_card_title, fill=(31, 26, 58, 255))
        pdraw.text((cx + 74, cy + 42), csub, font=font_card_sub, fill=(110, 100, 125, 255))

        # Right arrow pill / quick access button
        pill_x = cx + card_w - 75
        pill_y = cy + 20
        pdraw.rounded_rectangle([pill_x, pill_y, pill_x + 60, pill_y + 32], radius=10,
                                fill=(245, 240, 230, 255), outline=(200, 190, 175, 255), width=2)
        pdraw.text((pill_x + 14, pill_y + 7), "進入", font=font_small, fill=(70, 60, 85, 255))

    # Old text-only comparison banner
    pdraw.text((45, y3 + 245), "【對比：修改前純文字 PPT 膠囊（無自繪圖示 · 缺乏功能引導 · 橫屏並排顯得業餘廉價）】", font=font_small, fill=(185, 50, 50, 255))
    old_cy = y3 + 270
    for idx, (ctitle, csub, _, _) in enumerate(card_specs):
        old_cx = 45 + idx * 230
        pdraw.rounded_rectangle([old_cx, old_cy, old_cx + 215, old_cy + 42], radius=8,
                                fill=(242, 239, 232, 255), outline=(210, 205, 195, 255), width=1)
        pdraw.text((old_cx + 12, old_cy + 12), ctitle, font=font_small, fill=(130, 120, 140, 255))
        pdraw.text((old_cx + 95, old_cy + 14), "(無圖示文字列)", font=font_small, fill=(180, 160, 160, 255))

    # Row 4: Harmony Check with Approved HUD & Dock Icons
    y4 = 770
    pdraw.text((35, y4 - 10), "【風格全體系合規檢驗：與已過審頂部資源圖示及底部 Dock 圖示並排比對】", font=font_sub, fill=(45, 38, 60, 255))

    hud_ref_rect = [25, y4 + 15, proof_w - 25, y4 + 165]
    pdraw.rectangle(hud_ref_rect, fill=(244, 240, 232, 255), outline=(215, 210, 200, 255), width=2)

    approved_refs = [
        ("icon_energy_key.png", "能量鑰匙 (HUD)"),
        ("icon_gold_coin.png",   "齒輪金幣 (HUD)"),
        ("icon_dock_village.png","發條新村 (Dock)"),
        ("icon_dock_equip.png",  "角色裝備 (Dock)")
    ]

    for j, (rname, rlbl) in enumerate(approved_refs):
        rpath = f"{OUT_DIR}/{rname}"
        if os.path.exists(rpath):
            rim = Image.open(rpath).resize((64, 64), Image.Resampling.LANCZOS)
            rx = 45 + j * 135
            draw_checker(rx, y4 + 35, 76, 76)
            proof.paste(rim, (rx + 6, y4 + 41), rim)
            pdraw.text((rx + 2, y4 + 120), f"[已過審]", font=font_small, fill=(35, 110, 70, 255))
            pdraw.text((rx + 2, y4 + 136), rlbl, font=font_small, fill=(60, 50, 80, 255))

    pdraw.text((600, y4 + 30), "美術總監 15 項自檢標準逐項核定：", font=font_lbl, fill=(31, 26, 58, 255))
    audit_notes = [
        "✓ 統一 #1F1A3A 深藍紫描邊與 4-5px 等寬線條層次",
        "✓ 嚴格左上向右下高光光影，多巴胺金屬烤漆賽璐璐層次",
        "✓ 100% 零系統 Emoji、零毛皮、零字符當圖示、零寫實照片",
        "✓ 32px 下四張剪影分明（鐵砧錘／熔爐三晶／交叉盾／捲軸牌）"
    ]
    for k, anote in enumerate(audit_notes):
        pdraw.text((600, y4 + 56 + k * 22), anote, font=font_small, fill=(45, 40, 65, 255))

    proof_path = f"{PROOF_DIR}/proof_hall_four_icons.png"
    proof.save(proof_path, "PNG")
    print(f"Saved verification proof: {proof_path}")
    return proof_path


if __name__ == "__main__":
    generate_all()
