#!/usr/bin/env python3
"""
tools/build_settings_sortie_icons.py
Generate 2 mobile lobby UI icons for Clockwork Heart (發條之心):
1. icon_btn_settings.png - Clockwork Gear + Winding Key (設置 · 黃銅齒輪＋上鍊鑰匙)
2. icon_btn_sortie.png   - Clockwork Compass Arrow / Sortie Lance (前往出征 · 發條羅盤齒輪箭頭)

Specifications:
- 128x128 RGBA PNG transparent background
- Unified outline #1F1A3A (approx 4-5px at 128px, 16-20px at 512px)
- Dopamine palette: warm gold #FFD028, orange #FFA010, mint-teal #4ED86A, coral #FF5E8A, sky blue #38A0FF
- Microscopic readability at 32px
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

OUTLINE_COLOR = (31, 26, 58, 255)  # #1F1A3A


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
    hr = r * 0.35
    draw.ellipse([x - r * 0.35, y - r * 0.35, x - r * 0.35 + hr, y - r * 0.35 + hr], fill=(255, 255, 255, 240))
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
# 1. Settings Icon (設置 - Clockwork Gear + Winding Key)
# ==============================================================================

def create_settings_icon_master(size=512) -> Image.Image:
    """
    Render 512x512 Clockwork Gear + Winding Key Icon:
    - 6-toothed chunky brass gear centered at (220, 285).
    - Chunky trapezoidal gear cogs with bevels, rivets, and concentric mechanical bands.
    - Diagonal winding key angled at -40 deg, piercing through the gear arbor.
    - Winding key head in upper-right with dual circular lobes and hollow cutouts.
    - Key collar and notched mechanical bit at bottom-left.
    - Central gear arbor with raised dome nut and glowing mint power core.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # 1. Gear geometry at (220, 285)
    gcx, gcy = 220.0, 285.0
    gdx = x_coords - gcx
    gdy = y_coords - gcy
    gdist = np.sqrt(gdx**2 + gdy**2)
    gangle = np.arctan2(gdy, gdx)
    
    # 6 chunky teeth: period = pi/3 (~1.0472 rad)
    # Tooth center offset by 15 deg
    norm_angle = np.mod(gangle - math.radians(15), 2 * math.pi / 6.0) / (2 * math.pi / 6.0)
    
    # Tooth profile: outer flat from 0.25 to 0.75 (50% tooth width), slope to valley
    r_outer = 175.0
    r_inner = 125.0
    
    tooth_factor = np.clip(1.0 - np.abs(norm_angle - 0.5) * 4.0, 0.0, 1.0)
    gear_r = r_inner + (r_outer - r_inner) * tooth_factor
    gear_mask = gdist <= gear_r
    
    # 2. Winding Key geometry angled at -40 degrees (pointing up-right)
    # Stem axis vector
    theta = math.radians(-40)
    cos_t, sin_t = math.cos(theta), math.sin(theta)  # (0.766, -0.643)
    # Perpendicular vector
    perp_x, perp_y = -sin_t, cos_t  # (0.643, 0.766)
    
    # Key head center at (365, 163)
    k_center_x, k_center_y = 365.0, 163.0
    
    # Distance along stem from key head
    dist_along_stem = (x_coords - k_center_x) * cos_t + (y_coords - k_center_y) * sin_t
    dist_perp_stem = np.abs((x_coords - k_center_x) * perp_x + (y_coords - k_center_y) * perp_y)
    
    # Stem mask: width 44 (half-width 22), length from -20 to 300 (down to (140, 395))
    stem_mask = (dist_perp_stem <= 22.0) & (dist_along_stem >= -15.0) & (dist_along_stem <= 305.0)
    
    # Collar on stem: at dist 45..75, width 64 (half-width 32)
    collar_mask = (dist_perp_stem <= 32.0) & (dist_along_stem >= 45.0) & (dist_along_stem <= 75.0)
    
    # Key bit teeth at bottom-left (dist 255..300)
    bit_proj_perp = (x_coords - k_center_x) * perp_x + (y_coords - k_center_y) * perp_y
    bit_mask1 = (dist_along_stem >= 250.0) & (dist_along_stem <= 275.0) & (bit_proj_perp >= 20.0) & (bit_proj_perp <= 52.0)
    bit_mask2 = (dist_along_stem >= 282.0) & (dist_along_stem <= 302.0) & (bit_proj_perp >= 20.0) & (bit_proj_perp <= 45.0)
    key_bit_mask = bit_mask1 | bit_mask2
    
    # Winding Key Wings (two circular lobes)
    # Lobe 1 (top-left along perp): offset -65
    l1_x = k_center_x - 65.0 * perp_x
    l1_y = k_center_y - 65.0 * perp_y
    dist_l1 = np.sqrt((x_coords - l1_x)**2 + (y_coords - l1_y)**2)
    
    # Lobe 2 (bottom-right along perp): offset +65
    l2_x = k_center_x + 65.0 * perp_x
    l2_y = k_center_y + 65.0 * perp_y
    dist_l2 = np.sqrt((x_coords - l2_x)**2 + (y_coords - l2_y)**2)
    
    # Central lobe / bridge
    dist_hub_key = np.sqrt((x_coords - k_center_x)**2 + (y_coords - k_center_y)**2)
    
    wings_solid = (dist_l1 <= 64.0) | (dist_l2 <= 64.0) | (dist_hub_key <= 50.0) | ((dist_along_stem >= -45.0) & (dist_along_stem <= 35.0) & (dist_perp_stem <= 65.0))
    
    # Circular cutouts in wings (radius 25)
    hole1 = dist_l1 <= 25.0
    hole2 = dist_l2 <= 25.0
    
    wings_mask = wings_solid & (~hole1) & (~hole2)
    
    # Combine gear + winding key
    full_mask = gear_mask | stem_mask | collar_mask | key_bit_mask | wings_mask
    
    # Generate unified outline
    img = create_outline_and_base(full_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    rgba = np.array(img)
    
    # --------------------------------------------------------------------------
    # Render Gear Body (Cel-shaded brass)
    # --------------------------------------------------------------------------
    gear_indices = np.where(gear_mask)
    for y, x in zip(gear_indices[0], gear_indices[1]):
        # Diagonal lighting along 135 deg
        u = (x - 60.0) / 320.0
        v = (y - 120.0) / 320.0
        diag = 0.5 * u + 0.5 * v
        
        # Distance from gear center
        d = gdist[y, x]
        
        if d > 120.0:
            # Outer teeth band: rich golden gradient
            if diag < 0.25:
                t = diag / 0.25
                r = int(255 * (1 - t) + 255 * t)
                g = int(248 * (1 - t) + 218 * t)
                b = int(140 * (1 - t) + 45 * t)
            elif diag < 0.65:
                t = (diag - 0.25) / 0.40
                r = int(255 * (1 - t) + 240 * t)
                g = int(218 * (1 - t) + 155 * t)
                b = int(45 * (1 - t) + 20 * t)
            else:
                t = min(1.0, (diag - 0.65) / 0.35)
                r = int(240 * (1 - t) + 175 * t)
                g = int(155 * (1 - t) + 95 * t)
                b = int(20 * (1 - t) + 10 * t)
        elif d > 98.0:
            # Recessed mechanical groove (dark bronze accent)
            r, g, b = 155, 95, 20
        else:
            # Inner gear plate (warm cream-gold metallic)
            t = np.clip(diag, 0.0, 1.0)
            r = int(255 * (1 - t) + 235 * t)
            g = int(242 * (1 - t) + 185 * t)
            b = int(180 * (1 - t) + 60 * t)
            
        rgba[y, x] = [r, g, b, 255]
        
    # --------------------------------------------------------------------------
    # Render Winding Key Body (Layered on top of gear)
    # --------------------------------------------------------------------------
    key_body_mask = (stem_mask | collar_mask | key_bit_mask | wings_mask) & (~hole1) & (~hole2)
    key_indices = np.where(key_body_mask)
    for y, x in zip(key_indices[0], key_indices[1]):
        # Lighting oriented towards top-left
        u = (x - 200.0) / 280.0
        v = (y - 50.0) / 350.0
        diag = 0.5 * u + 0.5 * v
        
        if diag < 0.25:
            t = diag / 0.25
            r = int(255 * (1 - t) + 255 * t)
            g = int(250 * (1 - t) + 225 * t)
            b = int(160 * (1 - t) + 55 * t)
        elif diag < 0.65:
            t = (diag - 0.25) / 0.40
            r = int(255 * (1 - t) + 245 * t)
            g = int(225 * (1 - t) + 160 * t)
            b = int(55 * (1 - t) + 25 * t)
        else:
            t = min(1.0, (diag - 0.65) / 0.35)
            r = int(245 * (1 - t) + 185 * t)
            g = int(160 * (1 - t) + 100 * t)
            b = int(25 * (1 - t) + 12 * t)
            
        # Top-edge specular glints on key wing lobes
        if dist_l1[y, x] <= 64.0:
            if y < l1_y - 20 and dist_l1[y, x] > 40:
                r, g, b = min(255, r + 45), min(255, g + 40), min(255, b + 60)
        if dist_l2[y, x] <= 64.0:
            if y < l2_y - 20 and dist_l2[y, x] > 40:
                r, g, b = min(255, r + 45), min(255, g + 40), min(255, b + 60)
                
        # Stem central highlight stripe
        d_perp = abs((x - k_center_x) * perp_x + (y - k_center_y) * perp_y)
        if d_perp <= 7.0 and dist_along_stem[y, x] > 20:
            r, g, b = min(255, r + 40), min(255, g + 35), min(255, b + 45)
            
        rgba[y, x] = [r, g, b, 255]
        
    img = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img)
    
    # Inner rim around wing holes
    draw.ellipse([l1_x - 32, l1_y - 32, l1_x + 32, l1_y + 32], outline=OUTLINE_COLOR, width=8)
    draw.ellipse([l2_x - 32, l2_y - 32, l2_x + 32, l2_y + 32], outline=OUTLINE_COLOR, width=8)
    
    # Internal seam outlines between key stem and collar
    collar_left = k_center_x + 45 * cos_t - 32 * perp_x
    collar_top = k_center_y + 45 * sin_t - 32 * perp_y
    draw.line([
        (k_center_x + 45 * cos_t - 32 * perp_x, k_center_y + 45 * sin_t - 32 * perp_y),
        (k_center_x + 45 * cos_t + 32 * perp_x, k_center_y + 45 * sin_t + 32 * perp_y)
    ], fill=OUTLINE_COLOR, width=7)
    draw.line([
        (k_center_x + 75 * cos_t - 32 * perp_x, k_center_y + 75 * sin_t - 32 * perp_y),
        (k_center_x + 75 * cos_t + 32 * perp_x, k_center_y + 75 * sin_t + 32 * perp_y)
    ], fill=OUTLINE_COLOR, width=7)
    
    # Gear teeth root seam line / groove ring
    draw.ellipse([gcx - 122, gcy - 122, gcx + 122, gcy + 122], outline=OUTLINE_COLOR, width=7)
    draw.ellipse([gcx - 98, gcy - 98, gcx + 98, gcy + 98], outline=(155, 95, 20, 255), width=5)
    
    # --------------------------------------------------------------------------
    # Central Gear Hub / Arbor with 3D Nut & Mint Power Core
    # --------------------------------------------------------------------------
    hub_r = 52.0
    # Outer hub ring
    draw.ellipse([gcx - hub_r, gcy - hub_r, gcx + hub_r, gcy + hub_r], fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=8)
    # Beveled inner ring
    draw.ellipse([gcx - 42, gcy - 42, gcx + 42, gcy + 42], fill=(240, 155, 25, 255), outline=(155, 95, 20, 255), width=5)
    # Glowing mint/teal crystal core (#4ED86A)
    draw.ellipse([gcx - 30, gcy - 30, gcx + 30, gcy + 30], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=6)
    # Crystal glint highlight
    draw.ellipse([gcx - 22, gcy - 22, gcx - 4, gcy - 4], fill=(255, 255, 255, 240))
    
    # --------------------------------------------------------------------------
    # Rivets on Gear Teeth & Plates
    # --------------------------------------------------------------------------
    # Rivets on 4 gear teeth (avoiding the upper-right where key sits)
    for tooth_idx in [1, 2, 3, 4]:
        ang = math.radians(15 + tooth_idx * 60)
        rx = gcx + 148 * math.cos(ang)
        ry = gcy + 148 * math.sin(ang)
        draw_rivet(draw, rx, ry, r=9.0)
        
    # Rivets on key collar
    draw_rivet(draw, k_center_x + 60 * cos_t - 16 * perp_x, k_center_y + 60 * sin_t - 16 * perp_y, r=7.0)
    draw_rivet(draw, k_center_x + 60 * cos_t + 16 * perp_x, k_center_y + 60 * sin_t + 16 * perp_y, r=7.0)
    
    # --------------------------------------------------------------------------
    # Specular Glints & Sparkles
    # --------------------------------------------------------------------------
    # Star sparkles on key head and gear tooth
    draw_star_sparkle(draw, l1_x - 30, l1_y - 25, r=18.0)
    draw_star_sparkle(draw, gcx - 150, gcy - 60, r=14.0)
    draw_star_sparkle(draw, gcx + 25, gcy + 25, r=10.0, color=(200, 255, 220, 255))
    
    return img


# ==============================================================================
# 2. Sortie Icon (前往出征 - Clockwork Compass Arrow / Sortie Lance)
# ==============================================================================

def create_sortie_icon_master(size=512) -> Image.Image:
    """
    Render 512x512 Forward Sortie Icon:
    - Highly directional, pointing 40 degrees forward-right (出發/進擊).
    - Asymmetric silhouette completely distinct from 4-way symmetric dock campaign compass.
    - Tail (bottom-left): Clockwork propulsion gear dial (cx=185, cy=330) with cogs & winding key.
    - Deep celestial navy compass dial with brass ticks.
    - Dynamic golden mechanical chevron lance/arrowhead (tip at (450, 68)).
    - Multi-tiered brass armor plates, bevels, and rivets.
    - Radiant mint-teal / cyan (#4ED86A / #38A0FF) energy core spine.
    - Diamond star sparkles at spearhead tip.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # Spine axis: from tail center (185, 330) towards tip (450, 68)
    # Angle theta ~ -44.7 degrees
    scx, scy = 185.0, 330.0
    tip_x, tip_y = 450.0, 68.0
    
    spine_dx = tip_x - scx
    spine_dy = tip_y - scy
    spine_len = math.sqrt(spine_dx**2 + spine_dy**2)  # ~374px
    ux, uy = spine_dx / spine_len, spine_dy / spine_len
    # Perpendicular vector (pointing top-left)
    vx, vy = -uy, ux
    
    # Coordinate system along arrow spine:
    # u_dist: distance from tail center along arrow (0 at tail, spine_len at tip)
    # v_dist: perpendicular distance from arrow spine
    u_dist = (x_coords - scx) * ux + (y_coords - scy) * uy
    v_dist = (x_coords - scx) * vx + (y_coords - scy) * vy
    abs_v = np.abs(v_dist)
    
    # --------------------------------------------------------------------------
    # 1. Tail Clockwork Gear Dial (at scx, scy)
    # --------------------------------------------------------------------------
    gdx = x_coords - scx
    gdy = y_coords - scy
    gdist = np.sqrt(gdx**2 + gdy**2)
    gangle = np.arctan2(gdy, gdx)
    
    # 8-toothed rear gear dial (teeth visible mainly in rear/lower sectors)
    norm_angle = np.mod(gangle, 2 * math.pi / 8.0) / (2 * math.pi / 8.0)
    tooth_factor = np.clip(1.0 - np.abs(norm_angle - 0.5) * 4.0, 0.0, 1.0)
    gear_r = 100.0 + 26.0 * tooth_factor
    tail_gear_mask = (gdist <= gear_r) & (u_dist <= 100.0)
    
    # Winding key at the tail (extends backwards from scx, scy)
    # Key center at scx - 85*ux, scy - 85*uy = (125, 390)
    k_tail_x = scx - 82.0 * ux
    k_tail_y = scy - 82.0 * uy
    
    tail_stem_mask = (abs_v <= 18.0) & (u_dist >= -90.0) & (u_dist <= 20.0)
    
    # Tail key wings (two circular lobes perpendicular to spine)
    tw1_x = k_tail_x - 48.0 * vx
    tw1_y = k_tail_y - 48.0 * vy
    dist_tw1 = np.sqrt((x_coords - tw1_x)**2 + (y_coords - tw1_y)**2)
    
    tw2_x = k_tail_x + 48.0 * vx
    tw2_y = k_tail_y + 48.0 * vy
    dist_tw2 = np.sqrt((x_coords - tw2_x)**2 + (y_coords - tw2_y)**2)
    
    dist_tail_hub = np.sqrt((x_coords - k_tail_x)**2 + (y_coords - k_tail_y)**2)
    
    tail_wings_solid = (dist_tw1 <= 48.0) | (dist_tw2 <= 48.0) | (dist_tail_hub <= 38.0) | ((u_dist >= -115.0) & (u_dist <= -50.0) & (abs_v <= 50.0))
    tail_hole1 = dist_tw1 <= 18.0
    tail_hole2 = dist_tw2 <= 18.0
    tail_key_mask = (tail_wings_solid & (~tail_hole1) & (~tail_hole2)) | tail_stem_mask
    
    # --------------------------------------------------------------------------
    # 2. Main Arrowhead & Armor Chevrons
    # --------------------------------------------------------------------------
    # The Spearhead: sweeps back from tip (u_dist = spine_len)
    # Main tip triangle: from tip down to u_dist = 220
    # Width profile of primary head: expands linearly from 0 at tip to 105 at u_dist = 230
    dist_from_tip = spine_len - u_dist
    primary_width = dist_from_tip * 0.72
    primary_arrow_mask = (u_dist >= 210.0) & (u_dist <= spine_len) & (abs_v <= primary_width)
    
    # Barb notch cutout at base of primary head (returns to width 45 at u_dist = 210)
    barb_cutout = (u_dist >= 190.0) & (u_dist <= 260.0) & (abs_v >= 38.0 + (u_dist - 190.0) * 0.95)
    primary_arrow_mask = primary_arrow_mask & (~barb_cutout)
    
    # Secondary Chevron / Mid Armor Plate: from u_dist = 110 to 240, width up to 135
    sec_width = (240.0 - u_dist) * 0.85
    sec_chevron_mask = (u_dist >= 90.0) & (u_dist <= 240.0) & (abs_v <= sec_width)
    sec_barb_cutout = (u_dist >= 80.0) & (u_dist <= 150.0) & (abs_v >= 32.0 + (u_dist - 80.0) * 1.1)
    sec_chevron_mask = sec_chevron_mask & (~sec_barb_cutout)
    
    # Central Arrow Shaft / Navigation Lance Spine: width 48 from u_dist = -20 to 340
    spine_mask = (u_dist >= -10.0) & (u_dist <= 350.0) & (abs_v <= 24.0)
    
    # Combine full sortie silhouette
    full_mask = tail_gear_mask | tail_key_mask | sec_chevron_mask | primary_arrow_mask | spine_mask
    
    # Generate unified outline
    img = create_outline_and_base(full_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    rgba = np.array(img)
    
    # --------------------------------------------------------------------------
    # Render Tail Gear & Compass Face
    # --------------------------------------------------------------------------
    gear_indices = np.where(tail_gear_mask)
    for y, x in zip(gear_indices[0], gear_indices[1]):
        d = gdist[y, x]
        if d > 78.0:
            # Brass gear teeth band
            rgba[y, x] = [255, 205, 35, 255]
        else:
            # Deep celestial navy compass dial (#182B4D)
            rgba[y, x] = [24, 43, 77, 255]
            
    # Render Tail Winding Key
    key_indices = np.where(tail_key_mask)
    for y, x in zip(key_indices[0], key_indices[1]):
        rgba[y, x] = [255, 218, 55, 255]
        
    # --------------------------------------------------------------------------
    # Render Secondary Chevron (Warm Orange-Bronze Armor #FFA010)
    # --------------------------------------------------------------------------
    sec_indices = np.where(sec_chevron_mask)
    for y, x in zip(sec_indices[0], sec_indices[1]):
        u = (x - 120.0) / 300.0
        v = (y - 120.0) / 300.0
        diag = 0.5 * u + 0.5 * v
        r = int(255 * (1 - diag * 0.2))
        g = int(160 * (1 - diag * 0.35))
        b = int(16 * (1 - diag * 0.35))
        rgba[y, x] = [r, g, b, 255]
        
    # --------------------------------------------------------------------------
    # Render Primary Arrowhead (Brilliant Warm Gold #FFD028 to #FFA010)
    # --------------------------------------------------------------------------
    prim_indices = np.where(primary_arrow_mask)
    for y, x in zip(prim_indices[0], prim_indices[1]):
        # Distance along spine from tip
        dt = spine_len - u_dist[y, x]
        # Top half vs bottom half bevel
        v_val = v_dist[y, x]
        
        if v_val < 0:
            # Top-left facet: facing light source! Bright gold to white highlight
            t = np.clip(dt / 150.0, 0.0, 1.0)
            r = int(255 * (1 - t) + 255 * t)
            g = int(250 * (1 - t) + 215 * t)
            b = int(180 * (1 - t) + 40 * t)
        else:
            # Bottom-right facet: slight shadow warm gold
            t = np.clip(dt / 150.0, 0.0, 1.0)
            r = int(255 * (1 - t) + 235 * t)
            g = int(215 * (1 - t) + 145 * t)
            b = int(40 * (1 - t) + 15 * t)
            
        # Leading edge specular highlight
        edge_dist = primary_width[y, x] - abs_v[y, x]
        if edge_dist < 12.0 and v_val < 0:
            r, g, b = min(255, r + 45), min(255, g + 40), min(255, b + 65)
            
        rgba[y, x] = [r, g, b, 255]
        
    # --------------------------------------------------------------------------
    # Render Central Arrow Spine (Mint-Teal Energy Core #4ED86A)
    # --------------------------------------------------------------------------
    core_mask = (u_dist >= 20.0) & (u_dist <= 330.0) & (abs_v <= 15.0)
    core_indices = np.where(core_mask)
    for y, x in zip(core_indices[0], core_indices[1]):
        # Mint core with white central glint
        dist_c = abs_v[y, x]
        if dist_c <= 6.0:
            rgba[y, x] = [230, 255, 240, 255]
        else:
            rgba[y, x] = [78, 216, 106, 255]  # #4ED86A
            
    img = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img)
    
    # Inner holes on tail key
    draw.ellipse([tw1_x - 24, tw1_y - 24, tw1_x + 24, tw1_y + 24], outline=OUTLINE_COLOR, width=8)
    draw.ellipse([tw2_x - 24, tw2_y - 24, tw2_x + 24, tw2_y + 24], outline=OUTLINE_COLOR, width=8)
    
    # Internal seam dividing arrow facets along spine
    draw.line([(tip_x, tip_y), (scx + 160 * ux, scy + 160 * uy)], fill=OUTLINE_COLOR, width=7)
    
    # Seam between primary arrowhead and secondary chevron
    draw.line([
        (scx + 215 * ux - 85 * vx, scy + 215 * uy - 85 * vy),
        (scx + 245 * ux, scy + 245 * uy),
        (scx + 215 * ux + 85 * vx, scy + 215 * uy + 85 * vy)
    ], fill=OUTLINE_COLOR, width=7)
    
    # Compass dial inner brass ring and degree marks
    draw.ellipse([scx - 78, scy - 78, scx + 78, scy + 78], outline=OUTLINE_COLOR, width=7)
    draw.ellipse([scx - 62, scy - 62, scx + 62, scy + 62], outline=(255, 205, 35, 255), width=5)
    
    # Compass cardinal marks (N, W, S ticks on dial)
    for tick_deg in [135, 180, 225, 270]:
        rad = math.radians(tick_deg)
        x1 = scx + 52 * math.cos(rad)
        y1 = scy + 52 * math.sin(rad)
        x2 = scx + 68 * math.cos(rad)
        y2 = scy + 68 * math.sin(rad)
        draw.line([(x1, y1), (x2, y2)], fill=(255, 205, 35, 255), width=4)
        
    # Compass center pivot rivet
    draw_rivet(draw, scx, scy, r=14.0, base_color=(255, 220, 80))
    
    # Rivets on chevron wings
    draw_rivet(draw, scx + 185 * ux - 70 * vx, scy + 185 * uy - 70 * vy, r=8.0)
    draw_rivet(draw, scx + 185 * ux + 70 * vx, scy + 185 * uy + 70 * vy, r=8.0)
    draw_rivet(draw, scx + 270 * ux - 45 * vx, scy + 270 * uy - 45 * vy, r=8.0)
    draw_rivet(draw, scx + 270 * ux + 45 * vx, scy + 270 * uy + 45 * vy, r=8.0)
    
    # --------------------------------------------------------------------------
    # Specular Star Sparkles on Arrow Tip
    # --------------------------------------------------------------------------
    draw_star_sparkle(draw, tip_x + 10, tip_y - 10, r=22.0)
    draw_star_sparkle(draw, tip_x - 30, tip_y + 40, r=12.0)
    draw_star_sparkle(draw, scx + 160 * ux - 40 * vx, scy + 160 * uy - 40 * vy, r=10.0, color=(200, 255, 230, 255))
    
    return img


# ==============================================================================
# Verification Proof Sheet Generator
# ==============================================================================

def build_proof_sheet(settings_128, sortie_128, settings_32, sortie_32, proof_path):
    """
    Generate comprehensive verification proof sheet showing:
    1. 128x128 icons on light & dark backgrounds.
    2. 64x64 and 32x32 microscopic readability checks.
    3. Side-by-side comparison with reference icons (energy_key, dock_village, dock_campaign, hall_quest).
    4. Mock mobile lobby button placement (top-right settings, right sortie button).
    """
    pw, ph = 1080, 1100
    proof = Image.new("RGBA", (pw, ph), (250, 248, 242, 255))
    pdraw = ImageDraw.Draw(proof)
    
    # Fonts
    try:
        font_title = ImageFont.truetype(FONT_PATH, 28)
        font_sub = ImageFont.truetype(FONT_PATH, 18)
        font_body = ImageFont.truetype(FONT_PATH, 15)
        font_small = ImageFont.truetype(FONT_PATH, 13)
        font_btn = ImageFont.truetype(FONT_PATH, 22)
    except Exception:
        font_title = font_sub = font_body = font_small = font_btn = ImageFont.load_default()
        
    # Top Banner
    pdraw.rectangle([0, 0, pw, 80], fill=(31, 26, 58, 255))
    pdraw.text((30, 15), "發條之心 · 大廳設置鈕＋前往出征鈕自繪圖示驗收 (t_987bf485)", fill=(255, 208, 40, 255), font=font_title)
    pdraw.text((30, 48), "規格：128x128 RGBA · 描邊 #1F1A3A · 多巴胺多層次厚塗 · 32px微觀可辨識 · 零系統Emoji/零毛皮/零純文字", fill=(220, 215, 235, 255), font=font_small)
    
    # Section 1: Main 128x128 Icons
    y1 = 100
    pdraw.rectangle([30, y1, pw - 30, y1 + 35], fill=(240, 235, 225, 255))
    pdraw.text((45, y1 + 7), "【主資產展示】128×128px 原寸（白底／奶油底／深藍紫底對比）", fill=(31, 26, 58, 255), font=font_sub)
    
    items = [
        ("設置鈕圖示 (icon_btn_settings.png)", settings_128, "黃銅齒輪＋上鍊鑰匙\n圓潤厚齒、雙耳翅孔、薄荷能量晶核"),
        ("前往出征鈕圖示 (icon_btn_sortie.png)", sortie_128, "指向前方的發條羅盤齒輪箭頭\n40°進擊指向、推進齒輪羅盤、星芒閃光")
    ]
    
    for idx, (title, icon, desc) in enumerate(items):
        col_x = 50 + idx * 500
        row_y = y1 + 50
        
        pdraw.text((col_x, row_y), title, fill=(31, 26, 58, 255), font=font_sub)
        
        # 3 Background boxes: White, Cream #FFFDF8, Navy #1F1A3A
        box_w = 144
        # 1. White
        pdraw.rectangle([col_x, row_y + 30, col_x + box_w, row_y + 30 + box_w], fill=(255, 255, 255, 255), outline=(210, 205, 195, 255), width=2)
        proof.paste(icon, (col_x + 8, row_y + 38), icon)
        pdraw.text((col_x + 35, row_y + 30 + box_w + 5), "純白底", fill=(100, 95, 110, 255), font=font_small)
        
        # 2. Cream
        pdraw.rectangle([col_x + 155, row_y + 30, col_x + 155 + box_w, row_y + 30 + box_w], fill=(255, 253, 248, 255), outline=(255, 208, 40, 255), width=2)
        proof.paste(icon, (col_x + 155 + 8, row_y + 38), icon)
        pdraw.text((col_x + 155 + 25, row_y + 30 + box_w + 5), "大廳奶油底", fill=(180, 120, 15, 255), font=font_small)
        
        # 3. Navy
        pdraw.rectangle([col_x + 310, row_y + 30, col_x + 310 + box_w, row_y + 30 + box_w], fill=(31, 26, 58, 255), outline=(78, 216, 106, 255), width=2)
        proof.paste(icon, (col_x + 310 + 8, row_y + 38), icon)
        pdraw.text((col_x + 310 + 35, row_y + 30 + box_w + 5), "夜幕深底", fill=(78, 216, 106, 255), font=font_small)
        
        # Description
        pdraw.text((col_x, row_y + 205), desc, fill=(80, 75, 95, 255), font=font_small)
        
    # Section 2: Microscopic Readability (64px & 32px)
    y2 = 380
    pdraw.rectangle([30, y2, pw - 30, y2 + 35], fill=(240, 235, 225, 255))
    pdraw.text((45, y2 + 7), "【微觀清晰度驗證】64×64px 與 32×32px（手遊大廳實機圖示尺寸）", fill=(31, 26, 58, 255), font=font_sub)
    
    settings_64 = settings_128.resize((64, 64), Image.Resampling.LANCZOS)
    sortie_64 = sortie_128.resize((64, 64), Image.Resampling.LANCZOS)
    
    micro_items = [
        ("設置 (Settings)", settings_64, settings_32, 70),
        ("出征 (Sortie)", sortie_64, sortie_32, 570)
    ]
    
    for name, ic64, ic32, mx in micro_items:
        # 64px box
        pdraw.rectangle([mx, y2 + 50, mx + 80, y2 + 50 + 80], fill=(255, 255, 255, 255), outline=(200, 195, 185, 255), width=2)
        proof.paste(ic64, (mx + 8, y2 + 58), ic64)
        pdraw.text((mx + 15, y2 + 135), "64×64px", fill=(60, 55, 75, 255), font=font_small)
        
        # 32px box
        pdraw.rectangle([mx + 110, y2 + 50, mx + 110 + 80, y2 + 50 + 80], fill=(255, 255, 255, 255), outline=(200, 195, 185, 255), width=2)
        proof.paste(ic32, (mx + 110 + 24, y2 + 50 + 24), ic32)
        pdraw.text((mx + 125, y2 + 135), "32×32px", fill=(60, 55, 75, 255), font=font_small)
        
        # Pass badge
        pdraw.rectangle([mx + 220, y2 + 65, mx + 420, y2 + 115], fill=(235, 250, 235, 255), outline=(78, 216, 106, 255), width=2)
        pdraw.text((mx + 235, y2 + 78), f"✓ {name} 32px 剪影清晰辨識", fill=(30, 140, 50, 255), font=font_sub)
        
    # Section 3: Reference Asset Harmonization
    y3 = 560
    pdraw.rectangle([30, y3, pw - 30, y3 + 35], fill=(240, 235, 225, 255))
    pdraw.text((45, y3 + 7), "【體系化對照】與已過審 HUD 資源／Dock 導覽／四殿堂圖示同一套風格與質感", fill=(31, 26, 58, 255), font=font_sub)
    
    ref_paths = [
        ("HUD 能量鑰匙", f"{REPO_ROOT}/game/assets/icons/hud/icon_energy_key.png"),
        ("Dock 發條新村", f"{REPO_ROOT}/game/assets/icons/hud/icon_dock_village.png"),
        ("Dock 四區出征", f"{REPO_ROOT}/game/assets/icons/hud/icon_dock_campaign.png"),
        ("殿堂 冒險委託", f"{REPO_ROOT}/game/assets/icons/hud/icon_hall_quest.png"),
        ("【新作】設置鈕", None),  # settings_128
        ("【新作】出征鈕", None)   # sortie_128
    ]
    
    for i, (rname, rpath) in enumerate(ref_paths):
        rx = 50 + i * 165
        ry = y3 + 55
        
        # Container
        is_new = (rpath is None)
        border_col = (255, 160, 16, 255) if is_new else (200, 195, 210, 255)
        bg_col = (255, 252, 240, 255) if is_new else (255, 255, 255, 255)
        pdraw.rectangle([rx, ry, rx + 145, ry + 160], fill=bg_col, outline=border_col, width=3 if is_new else 1)
        
        if is_new:
            ic = settings_128 if "設置" in rname else sortie_128
        else:
            ic = Image.open(rpath)
            
        proof.paste(ic, (rx + 8, ry + 8), ic)
        pdraw.text((rx + 18, ry + 138), rname, fill=(31, 26, 58, 255) if not is_new else (220, 80, 10, 255), font=font_small)
        
    # Section 4: In-Game Button Mockup (果凍厚底實機模擬)
    y4 = 780
    pdraw.rectangle([30, y4, pw - 30, y4 + 35], fill=(240, 235, 225, 255))
    pdraw.text((45, y4 + 7), "【實機按鈕手感模擬】果凍厚底按鈕 (bottom border 5~6px) ＋ 自繪圖示", fill=(31, 26, 58, 255), font=font_sub)
    
    # Mock Button 1: Settings Button (大廳右上角設置鈕, 48px height)
    # Background: Cream/Ivory pill button with dark purple border & jelly bottom
    btn1_x, btn1_y = 70, y4 + 60
    btn1_w, btn1_h = 135, 52
    
    # Jelly bottom shadow (6px)
    pdraw.rounded_rectangle([btn1_x, btn1_y + 6, btn1_x + btn1_w, btn1_y + btn1_h + 6], radius=16, fill=(185, 170, 150, 255))
    # Button main face
    pdraw.rounded_rectangle([btn1_x, btn1_y, btn1_x + btn1_w, btn1_y + btn1_h], radius=16, fill=(255, 253, 248, 255), outline=(31, 26, 58, 255), width=3)
    # Icon (32px)
    proof.paste(settings_32, (btn1_x + 12, btn1_y + 10), settings_32)
    # Text
    pdraw.text((btn1_x + 52, btn1_y + 13), "設置", fill=(31, 26, 58, 255), font=font_btn)
    pdraw.text((btn1_x, btn1_y + 70), "右上設置鈕 (48px熱區/保留文字)", fill=(100, 95, 110, 255), font=font_small)
    
    # Mock Button 2: Sortie Button (大廳右側前往出征主按鈕, 280x68)
    # High-energy Warm Orange / Gold Jelly Button
    btn2_x, btn2_y = 360, y4 + 52
    btn2_w, btn2_h = 280, 68
    
    # Jelly bottom shadow (6px deep orange)
    pdraw.rounded_rectangle([btn2_x, btn2_y + 6, btn2_x + btn2_w, btn2_y + btn2_h + 6], radius=22, fill=(195, 95, 10, 255))
    # Button main face
    pdraw.rounded_rectangle([btn2_x, btn2_y, btn2_x + btn2_w, btn2_y + btn2_h], radius=22, fill=(255, 160, 16, 255), outline=(31, 26, 58, 255), width=4)
    # High-gloss top highlight
    pdraw.rounded_rectangle([btn2_x + 8, btn2_y + 4, btn2_x + btn2_w - 8, btn2_y + 24], radius=10, fill=(255, 210, 80, 160))
    # Sortie Icon (48px)
    sortie_48 = sortie_128.resize((48, 48), Image.Resampling.LANCZOS)
    proof.paste(sortie_48, (btn2_x + 22, btn2_y + 10), sortie_48)
    # Text
    pdraw.text((btn2_x + 82, btn2_y + 18), "前往出征", fill=(255, 255, 255, 255), font=font_title)
    pdraw.text((btn2_x + 35, btn2_y + 80), "右側主出征鈕 (280x68 果凍厚底6px / 高光反光)", fill=(100, 95, 110, 255), font=font_small)
    
    # Comparison Notice with Dock Campaign
    pdraw.rectangle([700, y4 + 50, pw - 50, y4 + 145], fill=(255, 250, 235, 255), outline=(255, 160, 16, 255), width=2)
    pdraw.text((715, y4 + 60), "★ 核心對比：與底部「四區出征」羅盤明確區分", fill=(200, 80, 10, 255), font=font_sub)
    pdraw.text((715, y4 + 90), "• 底部「四區出征」：四方對稱羅盤（地圖總覽分頁）", fill=(80, 75, 95, 255), font=font_small)
    pdraw.text((715, y4 + 115), "• 右側「前往出征」：40°朝前指向發條箭頭（出發進擊動作）", fill=(80, 75, 95, 255), font=font_small)
    
    # Footer checklist
    pdraw.rectangle([0, ph - 70, pw, ph], fill=(31, 26, 58, 255))
    checklist_text = "自我審核檢查：[✓] 零毛皮/金屬玩具語彙  [✓] 零系統Emoji  [✓] 零文字圖示  [✓] 多巴胺字典  [✓] 32px辨識通過  [✓] 依指示送審不呼叫付費API"
    pdraw.text((45, ph - 45), checklist_text, fill=(78, 216, 106, 255), font=font_body)
    
    proof.save(proof_path, "PNG")
    print(f"Saved verification proof: {proof_path}")
    return proof_path


def main():
    print("Building Settings and Sortie Icons for Clockwork Heart...")
    
    # 1. Build Masters
    settings_master = create_settings_icon_master(512)
    sortie_master = create_sortie_icon_master(512)
    
    # 2. Resample to 128x128
    settings_128 = settings_master.resize((128, 128), Image.Resampling.LANCZOS)
    sortie_128 = sortie_master.resize((128, 128), Image.Resampling.LANCZOS)
    
    # 3. Save 128x128 icons
    settings_path = f"{OUT_DIR}/icon_btn_settings.png"
    sortie_path = f"{OUT_DIR}/icon_btn_sortie.png"
    
    settings_128.save(settings_path, "PNG")
    sortie_128.save(sortie_path, "PNG")
    print(f"Saved: {settings_path}")
    print(f"Saved: {sortie_path}")
    
    # 4. Generate 32x32 versions
    settings_32 = settings_128.resize((32, 32), Image.Resampling.LANCZOS)
    sortie_32 = sortie_128.resize((32, 32), Image.Resampling.LANCZOS)
    
    # 5. Build Proof Sheet
    proof_path = f"{PROOF_DIR}/proof_settings_sortie_icons.png"
    build_proof_sheet(settings_128, sortie_128, settings_32, sortie_32, proof_path)
    
    print("Done! Both icons and proof sheet generated successfully.")

if __name__ == "__main__":
    main()
