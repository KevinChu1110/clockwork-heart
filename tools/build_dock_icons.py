#!/usr/bin/env python3
"""
tools/build_dock_icons.py
Generate 5 mobile bottom dock navigation icons for Clockwork Heart (發條之心):
1. icon_dock_village.png  - Clockwork Village House (發條新村)
2. icon_dock_equip.png    - Character Armor Plate (角色裝備)
3. icon_dock_campaign.png - 4-Direction Gear Compass (四區出征)
4. icon_dock_soul.png     - Clockwork Soul Urn (聚魂殿堂)
5. icon_dock_bag.png      - Brass-Clasped Metal Trunk (冒險背包)

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


# ==============================================================================
# 1. Village Icon (發條新村 - Clockwork Village House)
# ==============================================================================

def create_dock_village_master(size=512) -> Image.Image:
    """
    Render 512x512 Clockwork Village House:
    - Distinctive gable roof with chimney and golden brass winding key atop ridge.
    - Warm cream/ivory plate house walls with mechanical seams and rivets.
    - Rich arched wooden/amber door with brass round knob.
    - Glowing mint-teal circular gear porthole window.
    - Side gear teeth visible for mechanical toy flavor.
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # House body geometry
    wall_left, wall_right = 130, 382
    wall_top, wall_bottom = 265, 452
    wall_mask = (x_coords >= wall_left) & (x_coords <= wall_right) & (y_coords >= wall_top) & (y_coords <= wall_bottom)
    
    # Roof geometry: Triangle from apex (256, 155) to left eave (95, 275) to right eave (417, 275)
    # Line equations:
    # Left slope: y - 155 = ((275 - 155) / (95 - 256)) * (x - 256) = (120 / -161) * (x - 256)
    # y >= 155 and y <= 275, between left slope and right slope
    roof_mask = (y_coords >= 155) & (y_coords <= 275) & \
                (y_coords >= 155 + (120.0 / -161.0) * (x_coords - 256.0)) & \
                (y_coords >= 155 + (120.0 / 161.0) * (x_coords - 256.0))
    
    # Chimney on right slope: x in 320..365, y in 120..220
    chimney_mask = (x_coords >= 320) & (x_coords <= 365) & (y_coords >= 135) & (y_coords <= 220)
    
    # Top Winding Key atop roof ridge:
    # Stem: x in 238..274, y in 80..165
    key_stem = (x_coords >= 240) & (x_coords <= 272) & (y_coords >= 85) & (y_coords <= 165)
    # Wings at top (y=75): Left wing center (185, 75), Right wing center (327, 75)
    dist_l = np.sqrt((x_coords - 185.0)**2 + (y_coords - 75.0)**2)
    dist_r = np.sqrt((x_coords - 327.0)**2 + (y_coords - 75.0)**2)
    dist_mid = np.sqrt((x_coords - 256.0)**2 + (y_coords - 92.0)**2)
    key_wings = (dist_l <= 48.0) | (dist_r <= 48.0) | (dist_mid <= 40.0) | \
                ((x_coords >= 185) & (x_coords <= 327) & (y_coords >= 52) & (y_coords <= 98))
    # Cutout holes in key wings
    hole_l = dist_l < 22.0
    hole_r = dist_r < 22.0
    key_mask = (key_stem | key_wings) & (~hole_l) & (~hole_r)
    
    # Side gear partially peeking from left wall: center (125, 340), r=55
    dist_gear = np.sqrt((x_coords - 125.0)**2 + (y_coords - 340.0)**2)
    angle_gear = np.arctan2(y_coords - 340.0, x_coords - 125.0)
    teeth = np.mod(angle_gear + math.pi, 2.0 * math.pi / 6.0) / (2.0 * math.pi / 6.0)
    side_gear_mask = (dist_gear <= 55.0) & (dist_gear >= 25.0) & (x_coords < wall_left)
    
    combined_mask = wall_mask | roof_mask | chimney_mask | key_mask | side_gear_mask
    
    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Side Gear (Brass)
    for y in range(280, 400):
        for x in range(70, wall_left + 1):
            if side_gear_mask[y, x]:
                diag = (x - 70) / 60.0
                col = (int(220 + diag * 30), int(160 + diag * 40), int(30 + diag * 20), 255)
                img.putpixel((x, y), col)
                
    # 2. Fill Chimney (Red brick / warm copper metal plate)
    for y in range(135, 220):
        for x in range(320, 366):
            if chimney_mask[y, x]:
                u = (x - 320) / 46.0
                r = int(210 - u * 40)
                g = int(70 - u * 20)
                b = int(50 - u * 15)
                img.putpixel((x, y), (r, g, b, 255))
    draw.rectangle([315, 130, 370, 146], fill=(255, 215, 75, 255), outline=OUTLINE_COLOR, width=6)
    
    # 3. Fill House Wall (Warm ivory-cream metal plate #FFFDF8 / #EAE5D8)
    for y in range(wall_top, wall_bottom + 1):
        for x in range(wall_left, wall_right + 1):
            if wall_mask[y, x]:
                u = (x - wall_left) / (wall_right - wall_left)
                v = (y - wall_top) / (wall_bottom - wall_top)
                diag = 0.4 * u + 0.6 * v
                r = int(255 - diag * 35)
                g = int(250 - diag * 40)
                b = int(240 - diag * 45)
                img.putpixel((x, y), (r, g, b, 255))
                
    # Wall seam & baseboard
    draw.line([(256, wall_top), (256, wall_bottom)], fill=(31, 26, 58, 160), width=5)
    draw.rectangle([wall_left - 4, wall_bottom - 22, wall_right + 4, wall_bottom + 6], 
                   fill=(210, 195, 175, 255), outline=OUTLINE_COLOR, width=7)
    
    # 4. Fill Roof (Coral-Red Enamel Plates #FF5E8A / #E84050)
    for y in range(155, 276):
        for x in range(90, 420):
            if roof_mask[y, x]:
                v = (y - 155) / 120.0
                u = (x - 256) / 161.0
                # Top-left lighting
                diag = 0.5 * (u + 1.0) * 0.5 + 0.5 * v
                if u < 0: # Left side facing light
                    r = int(255 - abs(u) * 20)
                    g = int(105 - abs(u) * 30)
                    b = int(140 - abs(u) * 40)
                else: # Right side in shading
                    r = int(230 - u * 60)
                    g = int(60 - u * 30)
                    b = int(80 - u * 40)
                img.putpixel((x, y), (r, g, b, 255))
                
    # Roof horizontal overlapping tile lines
    for ry in [195, 235]:
        draw.line([(int(256 - (ry - 155) * (161 / 120)), ry), 
                   (int(256 + (ry - 155) * (161 / 120)), ry)], fill=OUTLINE_COLOR, width=7)
        draw.line([(int(256 - (ry - 155) * (161 / 120) + 4), ry - 4), 
                   (int(256 + (ry - 155) * (161 / 120) - 4), ry - 4)], fill=(255, 190, 210, 220), width=4)
        
    # Roof eaves fascia board (Gold brass edge)
    roof_poly = [(256, 150), (426, 275), (416, 290), (256, 168), (96, 290), (86, 275)]
    draw.polygon(roof_poly, fill=(255, 218, 55, 255), outline=OUTLINE_COLOR)
    draw.line([(256, 150), (426, 275)], fill=OUTLINE_COLOR, width=8)
    draw.line([(256, 150), (86, 275)], fill=OUTLINE_COLOR, width=8)
    draw.line([(86, 275), (426, 275)], fill=OUTLINE_COLOR, width=8)
    # Eaves highlight
    draw.line([(256, 156), (105, 273)], fill=(255, 255, 210, 250), width=6)
    
    # 5. Fill Winding Key atop roof (Luminous Brass)
    for y in range(40, 170):
        for x in range(130, 380):
            if key_mask[y, x]:
                diag = ((x - 130) / 250.0 + (y - 40) / 130.0) * 0.5
                r = int(255 - diag * 40)
                g = int(230 - diag * 65)
                b = int(80 - diag * 60)
                img.putpixel((x, y), (r, g, b, 255))
    # Inner holes outline
    draw.ellipse([185 - 22, 75 - 22, 185 + 22, 75 + 22], outline=OUTLINE_COLOR, width=8)
    draw.ellipse([327 - 22, 75 - 22, 327 + 22, 75 + 22], outline=OUTLINE_COLOR, width=8)
    # Key outer edge and highlight
    draw.line([(240, 85), (240, 165)], fill=OUTLINE_COLOR, width=7)
    draw.line([(272, 85), (272, 165)], fill=OUTLINE_COLOR, width=7)
    draw.arc([185 - 44, 75 - 44, 185 + 44, 75 + 44], 140, 310, fill=(255, 255, 220, 255), width=7)
    draw.arc([327 - 44, 75 - 44, 327 + 44, 75 + 44], 160, 300, fill=(255, 255, 220, 255), width=7)
    # Key hub boss
    draw.ellipse([256 - 20, 92 - 20, 256 + 20, 92 + 20], fill=(255, 240, 100, 255), outline=OUTLINE_COLOR, width=6)
    
    # 6. Arched Doorway (Amber caramel wood/metal with brass studs)
    door_l, door_r = 216, 296
    door_t, door_b = 345, wall_bottom - 15
    draw.rectangle([door_l, door_t + 25, door_r, door_b], fill=(185, 105, 25, 255), outline=OUTLINE_COLOR, width=7)
    draw.ellipse([door_l, door_t, door_r, door_t + 55], fill=(185, 105, 25, 255), outline=OUTLINE_COLOR, width=7)
    # Inner door trim
    draw.rectangle([door_l + 8, door_t + 32, door_r - 8, door_b - 6], fill=(215, 135, 45, 255))
    draw.ellipse([door_l + 8, door_t + 8, door_r - 8, door_t + 54], fill=(215, 135, 45, 255))
    # Door knob / keyhole
    draw.ellipse([door_r - 24, door_t + 52, door_r - 12, door_t + 64], fill=(255, 225, 60, 255), outline=OUTLINE_COLOR, width=3)
    
    # 7. Glowing Clockwork Window (Mint-Teal #4ED86A, #34E5C2)
    # Gear-edged circular porthole window at upper wall center (x=256, y=235) or left/right
    win_cx, win_cy = 175, 335
    win_r = 30
    draw.ellipse([win_cx - win_r - 6, win_cy - win_r - 6, win_cx + win_r + 6, win_cy + win_r + 6], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=7)
    draw.ellipse([win_cx - win_r, win_cy - win_r, win_cx + win_r, win_cy + win_r], 
                 fill=(20, 140, 100, 255), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([win_cx - win_r + 5, win_cy - win_r + 5, win_cx + win_r - 5, win_cy + win_r - 5], 
                 fill=(78, 216, 106, 255))
    draw.ellipse([win_cx - win_r + 10, win_cy - win_r + 10, win_cx + 8, win_cy + 8], 
                 fill=(160, 250, 200, 255))
    draw.ellipse([win_cx - 10, win_cy - 12, win_cx - 2, win_cy - 4], fill=(255, 255, 255, 250))
    # Window cross mullion
    draw.line([(win_cx - win_r + 4, win_cy), (win_cx + win_r - 4, win_cy)], fill=OUTLINE_COLOR, width=5)
    draw.line([(win_cx, win_cy - win_r + 4), (win_cx, win_cy + win_r - 4)], fill=OUTLINE_COLOR, width=5)
    
    # Right window
    rwin_cx, rwin_cy = 337, 335
    draw.ellipse([rwin_cx - win_r - 6, rwin_cy - win_r - 6, rwin_cx + win_r + 6, rwin_cy + win_r + 6], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=7)
    draw.ellipse([rwin_cx - win_r, rwin_cy - win_r, rwin_cx + win_r, rwin_cy + win_r], 
                 fill=(20, 140, 100, 255), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([rwin_cx - win_r + 5, rwin_cy - win_r + 5, rwin_cx + win_r - 5, rwin_cy + win_r - 5], 
                 fill=(78, 216, 106, 255))
    draw.ellipse([rwin_cx - win_r + 10, rwin_cy - win_r + 10, rwin_cx + 8, rwin_cy + 8], 
                 fill=(160, 250, 200, 255))
    draw.ellipse([rwin_cx - 10, rwin_cy - 12, rwin_cx - 2, rwin_cy - 4], fill=(255, 255, 255, 250))
    draw.line([(rwin_cx - win_r + 4, rwin_cy), (rwin_cx + win_r - 4, rwin_cy)], fill=OUTLINE_COLOR, width=5)
    draw.line([(rwin_cx, rwin_cy - win_r + 4), (rwin_cx, rwin_cy + win_r - 4)], fill=OUTLINE_COLOR, width=5)
    
    # Rivets on wall corners
    draw_rivet(draw, wall_left + 16, wall_top + 20, 9.0)
    draw_rivet(draw, wall_right - 16, wall_top + 20, 9.0)
    draw_rivet(draw, wall_left + 16, wall_bottom - 32, 9.0)
    draw_rivet(draw, wall_right - 16, wall_bottom - 32, 9.0)
    
    return img


# ==============================================================================
# 2. Equip Icon (角色裝備 - Knight Breastplate Armor & Core)
# ==============================================================================

def create_dock_equip_master(size=512) -> Image.Image:
    """
    Render 512x512 Character Armor Plate:
    - Polished toy mechanical knight cuirass with prominent shoulder pauldrons.
    - Tiered brass pauldrons on left and right with dome rivets.
    - Central glowing emerald-mint mechanical power core (#4ED86A) with gold bezel.
    - Segmented lower fauld armor plates.
    """
    cx, cy = size / 2.0, size / 2.0
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # Cuirass torso mask (polygon & curves)
    # Collar: (200, 110) to (312, 110), curves down to (256, 140)
    # Shoulder points: (160, 150), (352, 150)
    # Chest widest: (130, 230), (382, 230)
    # Waist taper: (165, 340), (347, 340)
    # Fauld skirt bottom: (145, 430), (367, 430), apex bottom (256, 455)
    torso_poly = [
        (256, 135), (312, 110), (352, 150), (382, 230), 
        (347, 340), (367, 430), (256, 455), (145, 430), 
        (165, 340), (130, 230), (160, 150), (200, 110)
    ]
    torso_img = Image.new("L", (size, size), 0)
    ImageDraw.Draw(torso_img).polygon(torso_poly, fill=255)
    torso_mask = np.array(torso_img) > 128
    
    # Pauldrons (curved shoulder bells): Left (115, 175) r=68, Right (397, 175) r=68
    dist_pl = np.sqrt((x_coords - 120.0)**2 + (y_coords - 170.0)**2)
    dist_pr = np.sqrt((x_coords - 392.0)**2 + (y_coords - 170.0)**2)
    pauldron_l = (dist_pl <= 68.0) & (y_coords >= 110) & (y_coords <= 235) & (x_coords <= 175)
    pauldron_r = (dist_pr <= 68.0) & (y_coords >= 110) & (y_coords <= 235) & (x_coords >= 337)
    
    # Neck gorget rim
    neck_mask = (y_coords >= 95) & (y_coords <= 135) & (x_coords >= 195) & (x_coords <= 317)
    
    combined_mask = torso_mask | pauldron_l | pauldron_r | neck_mask
    
    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Torso Armor (Ivory-Silver Steel / Toy Plate #F0F4FA to #C8D4E6)
    for y in range(110, 456):
        for x in range(130, 383):
            if torso_mask[y, x]:
                u = (x - cx) / 130.0
                v = (y - cy) / 170.0
                diag = 0.5 * (u + 1.0) * 0.5 + 0.5 * (v + 1.0) * 0.5
                # Curvature shading: center is highlighted, sides are deeper
                curve = 1.0 - (u**2) * 0.45
                if u < -0.1: # Light side
                    r = int((245 + u * 15) * curve)
                    g = int((248 + u * 15) * curve)
                    b = int((255 + u * 10) * curve)
                else: # Shadow side
                    r = int((235 - u * 45) * curve)
                    g = int((238 - u * 45) * curve)
                    b = int((248 - u * 40) * curve)
                img.putpixel((x, y), (max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b)), 255))
                
    # 2. Fill Pauldrons (Warm Gold Brass Plates)
    for y in range(110, 236):
        for x in range(50, 180):
            if pauldron_l[y, x]:
                diag = ((x - 50) / 130.0 + (y - 110) / 125.0) * 0.5
                r = int(255 - diag * 30)
                g = int(225 - diag * 50)
                b = int(70 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))
        for x in range(330, 465):
            if pauldron_r[y, x]:
                diag = ((x - 330) / 135.0 + (y - 110) / 125.0) * 0.5
                r = int(240 - diag * 55)
                g = int(195 - diag * 75)
                b = int(55 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))
                
    # Pauldron tier lines & highlights
    draw.arc([120 - 64, 170 - 64, 120 + 64, 170 + 64], 140, 280, fill=(255, 255, 220, 255), width=7)
    draw.arc([392 - 64, 170 - 64, 392 + 64, 170 + 64], 180, 280, fill=(255, 255, 220, 255), width=7)
    draw.line([(85, 175), (160, 175)], fill=OUTLINE_COLOR, width=7)
    draw.line([(352, 175), (427, 175)], fill=OUTLINE_COLOR, width=7)
    draw_rivet(draw, 105, 150, 8.0)
    draw_rivet(draw, 407, 150, 8.0)
    
    # 3. Gold Trim along breastplate borders
    draw.line([(200, 110), (312, 110)], fill=(255, 218, 55, 255), width=12)
    draw.line([(200, 110), (312, 110)], fill=OUTLINE_COLOR, width=7)
    # Center vertical plate seam
    draw.line([(256, 140), (256, 455)], fill=OUTLINE_COLOR, width=7)
    draw.line([(252, 140), (252, 450)], fill=(255, 255, 255, 220), width=4)
    
    # 4. Lower Fauld Segmented Plates
    for fy in [355, 395]:
        draw.line([(int(256 - (455 - fy) * 0.7), fy), (int(256 + (455 - fy) * 0.7), fy)], fill=OUTLINE_COLOR, width=7)
        draw.line([(int(256 - (455 - fy) * 0.7 + 5), fy - 4), (int(256 + (455 - fy) * 0.7 - 5), fy - 4)], 
                  fill=(255, 255, 255, 220), width=4)
        
    # Fauld rivets
    draw_rivet(draw, 185, 375, 7.5)
    draw_rivet(draw, 327, 375, 7.5)
    draw_rivet(draw, 205, 415, 7.5)
    draw_rivet(draw, 307, 415, 7.5)
    draw_rivet(draw, 256, 435, 8.0)
    
    # 5. Center Power Core (Clockwork Heart Gem)
    core_x, core_y = 256, 240
    core_r = 54
    # Outer brass bezel
    draw.ellipse([core_x - core_r, core_y - core_r, core_x + core_r, core_y + core_r], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=8)
    draw.arc([core_x - core_r + 4, core_y - core_r + 4, core_x + core_r - 4, core_y + core_r - 4], 
             130, 310, fill=(255, 255, 220, 255), width=6)
    
    # Inner emerald-mint glowing core
    c_inner = 38
    draw.ellipse([core_x - c_inner, core_y - c_inner, core_x + c_inner, core_y + c_inner], 
                 fill=(18, 120, 85, 255), outline=OUTLINE_COLOR, width=6)
    draw.ellipse([core_x - c_inner + 5, core_y - c_inner + 5, core_x + c_inner - 5, core_y + c_inner - 5], 
                 fill=(78, 216, 106, 255))
    draw.ellipse([core_x - c_inner + 12, core_y - c_inner + 10, core_x + 15, core_y + 12], 
                 fill=(140, 250, 185, 255))
    # Specular glint
    draw.ellipse([core_x - 16, core_y - 20, core_x + 2, core_y - 4], fill=(255, 255, 255, 250))
    
    # Decorative screw notches on brass bezel
    for a in [0, 90, 180, 270]:
        rad = math.radians(a)
        bx = core_x + 46 * math.cos(rad)
        by = core_y + 46 * math.sin(rad)
        draw_rivet(draw, bx, by, 5.5)
        
    return img


# ==============================================================================
# 3. Campaign Icon (四區出征 - 4-Direction Gear Compass)
# ==============================================================================

def create_dock_campaign_master(size=512) -> Image.Image:
    """
    Render 512x512 4-Direction Gear Compass:
    - Prominent circular brass compass frame with 4 extended cardinal points (N, S, E, W).
    - Deep royal/celestial navy blue compass face (#182B4D to #244578).
    - Bold 4-pointed navigation star needle (North pointing up in brilliant gold, South in coral).
    - Concentric brass guide rings and clockwork hour/degree notches.
    """
    cx, cy = size / 2.0, size / 2.0
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    # 4 Cardinal teeth extending far out (N, S, E, W to radius 228)
    # Secondary diagonal cogs (NE, SE, SW, NW to radius 195)
    # Base circle radius 175
    r_base = 175.0
    
    # Main circular mask
    main_circle = dist <= r_base
    
    # 4 Cardinal arrow points
    # North (top): apex (256, 42), base y=100
    n_poly = [(256, 42), (292, 120), (220, 120)]
    # South (bottom): apex (256, 470), base y=392
    s_poly = [(256, 470), (220, 392), (292, 392)]
    # East (right): apex (470, 256), base x=392
    e_poly = [(470, 256), (392, 220), (392, 292)]
    # West (left): apex (42, 256), base x=120
    w_poly = [(42, 256), (120, 292), (120, 220)]
    
    cardinal_img = Image.new("L", (size, size), 0)
    cdraw = ImageDraw.Draw(cardinal_img)
    cdraw.polygon(n_poly, fill=255)
    cdraw.polygon(s_poly, fill=255)
    cdraw.polygon(e_poly, fill=255)
    cdraw.polygon(w_poly, fill=255)
    
    # 4 Diagonal gear teeth at 45, 135, 225, 315 deg
    for da in [45, 135, 225, 315]:
        rad = math.radians(da)
        tx = cx + 202 * math.cos(rad)
        ty = cy + 202 * math.sin(rad)
        cdraw.ellipse([tx - 22, ty - 22, tx + 22, ty + 22], fill=255)
        
    combined_mask = main_circle | (np.array(cardinal_img) > 128)
    
    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Brass Compass Body & Outer Cogs
    for y in range(40, 475):
        for x in range(40, 475):
            if combined_mask[y, x]:
                u = (x - cx) / 228.0
                v = (y - cy) / 228.0
                diag = (u + v) * 0.5
                norm_diag = np.clip((diag + 0.9) / 1.8, 0.0, 1.0)
                if norm_diag < 0.35:
                    t = norm_diag / 0.35
                    r = int(255 * (1 - t) + 255 * t)
                    g = int(245 * (1 - t) + 215 * t)
                    b = int(140 * (1 - t) + 45 * t)
                elif norm_diag < 0.75:
                    t = (norm_diag - 0.35) / 0.40
                    r = int(255 * (1 - t) + 225 * t)
                    g = int(215 * (1 - t) + 145 * t)
                    b = int(45 * (1 - t) + 15 * t)
                else:
                    t = (norm_diag - 0.75) / 0.25
                    r = int(225 * (1 - t) + 160 * t)
                    g = int(145 * (1 - t) + 85 * t)
                    b = int(15 * (1 - t) + 5 * t)
                img.putpixel((x, y), (r, g, b, 255))
                
    # 2. Outer Bezel Rings
    draw.ellipse([cx - 175, cy - 175, cx + 175, cy + 175], outline=OUTLINE_COLOR, width=8)
    draw.ellipse([cx - 165, cy - 165, cx + 165, cy + 165], outline=(255, 235, 110, 255), width=8)
    draw.arc([cx - 165, cy - 165, cx + 165, cy + 165], 130, 310, fill=(255, 255, 220, 255), width=10)
    
    # 3. Celestial Navy Blue Compass Dial (Radius 142)
    dial_r = 142.0
    dial_mask = dist <= dial_r
    for y in range(int(cy - dial_r), int(cy + dial_r + 1)):
        for x in range(int(cx - dial_r), int(cx + dial_r + 1)):
            if dial_mask[y, x]:
                u = (x - cx) / dial_r
                v = (y - cy) / dial_r
                d = (u + v) * 0.5
                r = int(np.clip(35 - d * 20, 15, 60))
                g = int(np.clip(65 - d * 30, 25, 100))
                b = int(np.clip(135 - d * 45, 60, 180))
                img.putpixel((x, y), (r, g, b, 255))
                
    draw = ImageDraw.Draw(img)
    draw.ellipse([cx - dial_r, cy - dial_r, cx + dial_r, cy + dial_r], outline=OUTLINE_COLOR, width=8)
    
    # Concentric inner golden rings & 12 clock ticks
    draw.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=(255, 218, 55, 180), width=4)
    draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], outline=(255, 218, 55, 120), width=3)
    for h in range(12):
        ha = math.radians(h * 30 - 90)
        t_len = 16 if (h % 3 == 0) else 9
        x1 = cx + (dial_r - 6) * math.cos(ha)
        y1 = cy + (dial_r - 6) * math.sin(ha)
        x2 = cx + (dial_r - 6 - t_len) * math.cos(ha)
        y2 = cy + (dial_r - 6 - t_len) * math.sin(ha)
        col = (255, 235, 120, 240) if (h % 3 == 0) else (255, 218, 55, 180)
        draw.line([(x1, y1), (x2, y2)], fill=col, width=5 if (h % 3 == 0) else 3)
        
    # 4. Compass Star Needle
    # North Needle Point (Points UP: Golden #FFD028 with white highlight)
    n_needle_apex = (cx, cy - 128)
    s_needle_apex = (cx, cy + 128)
    w_needle_apex = (cx - 48, cy)
    e_needle_apex = (cx + 48, cy)
    
    # North left facet (Brilliant Ivory Gold)
    draw.polygon([(cx, cy), n_needle_apex, w_needle_apex], fill=(255, 250, 180, 255), outline=OUTLINE_COLOR)
    # North right facet (Warm Gold)
    draw.polygon([(cx, cy), n_needle_apex, e_needle_apex], fill=(255, 195, 30, 255), outline=OUTLINE_COLOR)
    
    # South left facet (Coral Pink)
    draw.polygon([(cx, cy), s_needle_apex, w_needle_apex], fill=(255, 94, 138, 255), outline=OUTLINE_COLOR)
    # South right facet (Deep Crimson Coral)
    draw.polygon([(cx, cy), s_needle_apex, e_needle_apex], fill=(195, 40, 75, 255), outline=OUTLINE_COLOR)
    
    # Crisp needle borders
    draw.line([(cx, cy), n_needle_apex], fill=OUTLINE_COLOR, width=6)
    draw.line([(cx, cy), s_needle_apex], fill=OUTLINE_COLOR, width=6)
    draw.line([w_needle_apex, n_needle_apex, e_needle_apex, s_needle_apex, w_needle_apex], fill=OUTLINE_COLOR, width=7)
    
    # 5. Center Axle Boss (Raised Brass Dome + Mint Gem)
    draw.ellipse([cx - 32, cy - 32, cx + 32, cy + 32], fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=7)
    draw.ellipse([cx - 20, cy - 20, cx + 20, cy + 20], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([cx - 10, cy - 12, cx + 5, cy + 4], fill=(180, 255, 220, 255))
    draw.ellipse([cx - 6, cy - 8, cx - 1, cy - 2], fill=(255, 255, 255, 250))
    
    return img


# ==============================================================================
# 4. Soul Icon (聚魂殿堂 - Clockwork Soul Urn / Spirit Jar)
# ==============================================================================

def create_dock_soul_master(size=512) -> Image.Image:
    """
    Render 512x512 Clockwork Soul Urn:
    - Antique brass screw-cap stopper on top with clockwork winding knob loop.
    - Glass amphora jar with deep purple-navy edges (#1F1A3A, #2D1845).
    - Floating luminous spiraling spirit flame inside: brilliant cyan-mint (#4ED86A, #34E5C2) and magenta violet.
    - Flared ornate brass metal pedestal base with rivets.
    """
    cx, cy = size / 2.0, size / 2.0
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # Stopper handle loop: top (256, 50), w=75, h=55
    dist_loop = np.sqrt((x_coords - 256.0)**2 + ((y_coords - 75.0) * 1.3)**2)
    loop_mask = (dist_loop <= 42.0) & (dist_loop >= 18.0) & (y_coords <= 110)
    
    # Brass stopper cap: x in 205..307, y in 100..145
    cap_mask = (x_coords >= 205) & (x_coords <= 307) & (y_coords >= 100) & (y_coords <= 145)
    
    # Neck collar: x in 222..290, y in 145..175
    neck_mask = (x_coords >= 222) & (x_coords <= 290) & (y_coords >= 145) & (y_coords <= 175)
    
    # Jar glass body: from neck (y=175, w=70) expanding to y=295 (w=290), tapering to y=410 (w=180)
    # Elliptical / curved profile:
    # Center of jar bulb: (256, 295), rx=145, ry=120
    dist_jar = ((x_coords - 256.0) / 145.0)**2 + ((y_coords - 295.0) / 120.0)**2
    jar_mask = (dist_jar <= 1.0) & (y_coords >= 175) & (y_coords <= 415)
    
    # Pedestal base: x in 140..372, y in 410..465
    base_mask = (x_coords >= 140) & (x_coords <= 372) & (y_coords >= 410) & (y_coords <= 462) & \
                (y_coords >= 410 + abs(x_coords - 256) * 0.15)
                
    combined_mask = loop_mask | cap_mask | neck_mask | jar_mask | base_mask
    
    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Pedestal Base (Brass)
    for y in range(410, 465):
        for x in range(135, 378):
            if base_mask[y, x]:
                diag = ((x - 140) / 232.0 + (y - 410) / 55.0) * 0.5
                r = int(245 - diag * 40)
                g = int(200 - diag * 60)
                b = int(55 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))
    draw.line([(140, 412), (372, 412)], fill=OUTLINE_COLOR, width=8)
    draw.line([(135, 460), (377, 460)], fill=OUTLINE_COLOR, width=8)
    draw.line([(145, 416), (367, 416)], fill=(255, 255, 210, 240), width=5)
    draw_rivet(draw, 175, 436, 8.0)
    draw_rivet(draw, 256, 436, 8.0)
    draw_rivet(draw, 337, 436, 8.0)
    
    # 2. Fill Glass Chamber (Dark Purple-Navy Mysterious Base #1F1535)
    for y in range(175, 415):
        for x in range(110, 405):
            if jar_mask[y, x]:
                u = (x - 256.0) / 145.0
                v = (y - 295.0) / 120.0
                d = np.sqrt(u**2 + v**2)
                # Outer edge is deep purple-navy; center is illuminated by soul
                r = int(np.clip(35 + (1 - d) * 20, 20, 60))
                g = int(np.clip(25 + (1 - d) * 35, 15, 75))
                b = int(np.clip(60 + (1 - d) * 70, 35, 150))
                img.putpixel((x, y), (r, g, b, 255))
                
    # 3. Luminous Ethereal Soul Flame inside Jar
    # Multi-layered glowing spirit wisp
    flame_cx, flame_cy = 256, 290
    # Outer soul aura (Teal & Violet glow)
    for r_aura in range(75, 20, -5):
        alpha_factor = (75 - r_aura) / 55.0
        col_r = int(45 + alpha_factor * 30)
        col_g = int(140 + alpha_factor * 76)
        col_b = int(180 + alpha_factor * 20)
        draw.ellipse([flame_cx - r_aura, flame_cy - r_aura + 10, flame_cx + r_aura, flame_cy + r_aura + 10], 
                     fill=(col_r, col_g, col_b, int(80 * alpha_factor)))
                     
    # Inner Flame Core (Curved Spirit Droplet: Mint-Cyan #4ED86A, #34E5C2)
    flame_poly = [
        (flame_cx, flame_cy - 65),     # Top tip
        (flame_cx + 38, flame_cy - 10), # Right belly
        (flame_cx + 25, flame_cy + 42), # Right lower
        (flame_cx, flame_cy + 55),     # Bottom curve
        (flame_cx - 25, flame_cy + 42), # Left lower
        (flame_cx - 38, flame_cy - 10)  # Left belly
    ]
    draw.polygon(flame_poly, fill=(52, 229, 194, 255), outline=OUTLINE_COLOR)
    draw.line(flame_poly + [flame_poly[0]], fill=OUTLINE_COLOR, width=6)
    
    # Flame inner brightness & nucleus
    inner_poly = [
        (flame_cx, flame_cy - 45),
        (flame_cx + 22, flame_cy - 8),
        (flame_cx + 14, flame_cy + 30),
        (flame_cx, flame_cy + 38),
        (flame_cx - 14, flame_cy + 30),
        (flame_cx - 22, flame_cy - 8)
    ]
    draw.polygon(inner_poly, fill=(160, 255, 230, 255))
    draw.ellipse([flame_cx - 12, flame_cy - 18, flame_cx + 12, flame_cy + 12], fill=(255, 255, 255, 255))
    
    # Whimsical swirling soul tail
    tail_pts = [(flame_cx, flame_cy - 65), (flame_cx - 18, flame_cy - 85), (flame_cx - 8, flame_cy - 100)]
    draw.line(tail_pts, fill=(52, 229, 194, 255), width=8)
    draw.line(tail_pts, fill=(255, 255, 255, 255), width=4)
    
    # Sparkle stars in jar
    for sx, sy in [(200, 240), (315, 245), (210, 350), (300, 345)]:
        draw.line([(sx - 8, sy), (sx + 8, sy)], fill=(255, 255, 255, 230), width=3)
        draw.line([(sx, sy - 8), (sx, sy + 8)], fill=(255, 255, 255, 230), width=3)
        draw.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 255, 255, 255))
        
    # Glass boundary and highlight reflection
    draw.arc([cx - 143, 295 - 118, cx + 143, 295 + 118], 130, 270, fill=(255, 255, 255, 220), width=9)
    draw.arc([cx - 135, 295 - 110, cx + 135, 295 + 110], 140, 230, fill=(255, 255, 255, 160), width=6)
    
    # 4. Stopper Cap & Neck (Brass)
    for y in range(100, 176):
        for x in range(200, 312):
            if cap_mask[y, x] or neck_mask[y, x]:
                diag = ((x - 200) / 112.0 + (y - 100) / 76.0) * 0.5
                r = int(255 - diag * 35)
                g = int(220 - diag * 55)
                b = int(70 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))
    draw.rectangle([205, 100, 307, 145], outline=OUTLINE_COLOR, width=7)
    draw.rectangle([222, 145, 290, 175], outline=OUTLINE_COLOR, width=7)
    # Cap ridges
    for rx in [230, 256, 282]:
        draw.line([(rx, 105), (rx, 140)], fill=OUTLINE_COLOR, width=5)
        
    # 5. Stopper Winding Loop atop
    for y in range(35, 110):
        for x in range(210, 305):
            if loop_mask[y, x]:
                diag = (x - 210) / 95.0
                r = int(255 - diag * 35)
                g = int(220 - diag * 50)
                b = int(70 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))
    draw.arc([256 - 42, 75 - 32, 256 + 42, 75 + 32], 180, 360, fill=(255, 255, 210, 240), width=6)
    
    return img


# ==============================================================================
# 5. Bag Icon (冒險背包 - Brass-Clasped Metal Adventure Trunk)
# ==============================================================================

def create_dock_bag_master(size=512) -> Image.Image:
    """
    Render 512x512 Brass-Clasped Metal Adventure Trunk:
    - Sturdy rounded rectangular chest with horizontal split (lid & body).
    - Rich warm caramel / amber leather enamel shell (#FFA010 to #D47000).
    - Arched brass top carrying handle with mounting brackets.
    - Heavy brass reinforced corner braces with rivets.
    - Large golden brass center lock buckle with prominent keyhole.
    """
    cx, cy = size / 2.0, size / 2.0
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # Top handle arch: from x=195 to x=317, rising from y=170 up to y=80
    dist_handle = np.sqrt(((x_coords - 256.0) / 1.1)**2 + (y_coords - 145.0)**2)
    handle_mask = (dist_handle <= 75.0) & (dist_handle >= 42.0) & (y_coords <= 175)
    
    # Trunk body: x in 90..422 (w=332), y in 170..440 (h=270), corner radius 36
    b_l, b_r = 92, 420
    b_t, b_b = 170, 440
    rad = 36.0
    
    # Distance to rounded rect edges
    dx = np.maximum(0, np.maximum(b_l + rad - x_coords, x_coords - (b_r - rad)))
    dy = np.maximum(0, np.maximum(b_t + rad - y_coords, y_coords - (b_b - rad)))
    trunk_mask = (dx**2 + dy**2) <= (rad**2)
    
    combined_mask = trunk_mask | handle_mask
    
    img = create_outline_and_base(combined_mask, size=size, outline_radius=29)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Handle (Brass)
    for y in range(65, 180):
        for x in range(160, 350):
            if handle_mask[y, x]:
                diag = (x - 160) / 190.0
                r = int(255 - diag * 35)
                g = int(220 - diag * 50)
                b = int(70 - diag * 40)
                img.putpixel((x, y), (r, g, b, 255))
    draw.arc([256 - 72, 145 - 72, 256 + 72, 145 + 72], 190, 350, fill=(255, 255, 220, 240), width=7)
    # Handle brackets
    draw.rectangle([185, 155, 215, 185], fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=6)
    draw.rectangle([297, 155, 327, 185], fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=6)
    draw_rivet(draw, 200, 170, 6.0)
    draw_rivet(draw, 312, 170, 6.0)
    
    # 2. Fill Trunk Body (Warm Dopamine Caramel Leather/Enamel #FFA010 to #D47000)
    for y in range(b_t, b_b + 1):
        for x in range(b_l, b_r + 1):
            if trunk_mask[y, x]:
                u = (x - b_l) / (b_r - b_l)
                v = (y - b_t) / (b_b - b_t)
                diag = 0.4 * u + 0.6 * v
                r = int(255 - diag * 45)
                g = int(170 - diag * 65)
                b = int(25 - diag * 15)
                img.putpixel((x, y), (r, g, b, 255))
                
    # 3. Horizontal Split Seam (Lid vs Body)
    split_y = 265
    draw.line([(b_l + 4, split_y), (b_r - 4, split_y)], fill=OUTLINE_COLOR, width=9)
    draw.line([(b_l + 8, split_y - 5), (b_r - 8, split_y - 5)], fill=(255, 220, 100, 220), width=4)
    draw.line([(b_l + 8, split_y + 5), (b_r - 8, split_y + 5)], fill=(150, 75, 5, 220), width=4)
    
    # 4. Vertical Brass Straps
    for sx in [170, 342]:
        sw = 38
        draw.rectangle([sx - sw//2, b_t, sx + sw//2, b_b], fill=(255, 218, 55, 255), outline=OUTLINE_COLOR, width=7)
        draw.line([(sx - sw//2 + 5, b_t + 10), (sx - sw//2 + 5, b_b - 10)], fill=(255, 255, 210, 220), width=4)
        draw.line([(sx + sw//2 - 5, b_t + 10), (sx + sw//2 - 5, b_b - 10)], fill=(160, 95, 10, 220), width=4)
        # Strap rivets
        draw_rivet(draw, sx, b_t + 25, 6.5)
        draw_rivet(draw, sx, split_y - 35, 6.5)
        draw_rivet(draw, sx, split_y + 35, 6.5)
        draw_rivet(draw, sx, b_b - 25, 6.5)
        
    # 5. Heavy Brass Corner Braces
    corner_size = 54
    # Top-left corner
    draw.polygon([(b_l, b_t + corner_size), (b_l, b_t), (b_l + corner_size, b_t), 
                  (b_l + corner_size, b_t + 22), (b_l + 22, b_t + corner_size)], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR)
    draw_rivet(draw, b_l + 24, b_t + 24, 7.0)
    
    # Top-right corner
    draw.polygon([(b_r, b_t + corner_size), (b_r, b_t), (b_r - corner_size, b_t), 
                  (b_r - corner_size, b_t + 22), (b_r - 22, b_t + corner_size)], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR)
    draw_rivet(draw, b_r - 24, b_t + 24, 7.0)
    
    # Bottom-left corner
    draw.polygon([(b_l, b_b - corner_size), (b_l, b_b), (b_l + corner_size, b_b), 
                  (b_l + corner_size, b_b - 22), (b_l + 22, b_b - corner_size)], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR)
    draw_rivet(draw, b_l + 24, b_b - 24, 7.0)
    
    # Bottom-right corner
    draw.polygon([(b_r, b_b - corner_size), (b_r, b_b), (b_r - corner_size, b_b), 
                  (b_r - corner_size, b_b - 22), (b_r - 22, b_b - corner_size)], 
                 fill=(255, 218, 55, 255), outline=OUTLINE_COLOR)
    draw_rivet(draw, b_r - 24, b_b - 24, 7.0)
    
    # 6. Center Brass Lock Clasp & Keyhole
    lock_w, lock_h = 74, 86
    draw.rounded_rectangle([cx - lock_w//2, split_y - lock_h//2, cx + lock_w//2, split_y + lock_h//2], 
                           radius=18, fill=(255, 230, 75, 255), outline=OUTLINE_COLOR, width=8)
    draw.arc([cx - lock_w//2 + 5, split_y - lock_h//2 + 5, cx + lock_w//2 - 5, split_y + lock_h//2 - 5], 
             130, 310, fill=(255, 255, 220, 255), width=6)
             
    # Keyhole
    kh_y = split_y + 4
    draw.ellipse([cx - 10, kh_y - 14, cx + 10, kh_y + 4], fill=OUTLINE_COLOR)
    draw.polygon([(cx - 7, kh_y), (cx + 7, kh_y), (cx + 10, kh_y + 18), (cx - 10, kh_y + 18)], fill=OUTLINE_COLOR)
    
    # Clasp top green indicator gem
    draw.ellipse([cx - 8, split_y - lock_h//2 + 10, cx + 8, split_y - lock_h//2 + 26], 
                 fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=3)
                 
    return img


# ==============================================================================
# Build and Verification Proof
# ==============================================================================

def generate_all():
    print("Generating 5 Clockwork Heart Mobile Dock Icons...")
    
    generators = [
        ("icon_dock_village.png", "發條新村", create_dock_village_master),
        ("icon_dock_equip.png",   "角色裝備", create_dock_equip_master),
        ("icon_dock_campaign.png","四區出征", create_dock_campaign_master),
        ("icon_dock_soul.png",    "聚魂殿堂", create_dock_soul_master),
        ("icon_dock_bag.png",     "冒險背包", create_dock_bag_master),
    ]
    
    icons_128 = []
    icons_64 = []
    icons_32 = []
    paths = []
    
    for filename, name_zh, gen_fn in generators:
        master = gen_fn(size=512)
        im_128 = master.resize((128, 128), Image.Resampling.LANCZOS)
        out_path = f"{OUT_DIR}/{filename}"
        im_128.save(out_path, "PNG")
        print(f"  -> Saved 128x128: {out_path}")
        
        im_64 = im_128.resize((64, 64), Image.Resampling.LANCZOS)
        im_32 = im_128.resize((32, 32), Image.Resampling.LANCZOS)
        
        icons_128.append(im_128)
        icons_64.append(im_64)
        icons_32.append(im_32)
        paths.append(out_path)
        
    # Build comprehensive verification proof
    build_proof(icons_128, icons_64, icons_32, generators)
    return paths


def build_proof(icons_128, icons_64, icons_32, generators):
    proof_w, proof_h = 1000, 920
    proof = Image.new("RGBA", (proof_w, proof_h), (250, 248, 242, 255))
    pdraw = ImageDraw.Draw(proof)
    
    font_title = ImageFont.truetype(FONT_PATH, 24)
    font_sub = ImageFont.truetype(FONT_PATH, 16)
    font_hud_lbl = ImageFont.truetype(FONT_PATH, 15)
    font_small = ImageFont.truetype(FONT_PATH, 13)
    font_tab = ImageFont.truetype(FONT_PATH, 14)
    
    # Top banner
    pdraw.rectangle([0, 0, proof_w, 75], fill=(31, 26, 58, 255))
    pdraw.text((24, 14), "《發條之心》底部 Dock 五個自繪圖示（去純文字頁籤驗收）", font=font_title, fill=(255, 255, 255, 255))
    pdraw.text((24, 46), "規格：128x128 RGBA · #1F1A3A 統一描邊 · 多巴胺色盤 · 32px 階梯微觀可辨識", font=font_small, fill=(200, 215, 240, 255))
    
    def draw_checker(x, y, w, h, grid=16):
        for cy in range(y, y + h, grid):
            for cx in range(x, x + w, grid):
                col = (236, 233, 226, 255) if ((cx // grid + cy // grid) % 2 == 0) else (255, 255, 255, 255)
                pdraw.rectangle([cx, cy, min(cx + grid, x + w), min(cy + grid, y + h)], fill=col)
        pdraw.rectangle([x, y, x + w, y + h], outline=(210, 205, 195, 255), width=2)
        
    # Row 1: 128x128 Standard Assets
    y1 = 110
    for i, (ic, (filename, name_zh, _)) in enumerate(zip(icons_128, generators)):
        bx = 35 + i * 190
        pdraw.text((bx, y1 - 25), f"標準 128x128", font=font_sub, fill=(90, 75, 115, 255))
        draw_checker(bx, y1, 144, 144)
        proof.paste(ic, (bx + 8, y1 + 8), ic)
        pdraw.text((bx, y1 + 152), f"{name_zh}\n{filename}", font=font_small, fill=(40, 35, 55, 255))
        
    # Row 2: Scaled Clarity Ladder (64px & 32px)
    y2 = 330
    pdraw.text((35, y2 - 25), "階梯縮放清晰度對比（64px 預覽 ｜ 32px 手機大廳 Dock 實際按鈕尺寸）", font=font_sub, fill=(90, 75, 115, 255))
    
    for i in range(5):
        bx = 35 + i * 190
        # 64px
        draw_checker(bx, y2, 80, 80)
        proof.paste(icons_64[i], (bx + 8, y2 + 8), icons_64[i])
        pdraw.text((bx + 18, y2 + 84), "64px", font=font_small, fill=(130, 120, 140, 255))
        
        # 32px
        draw_checker(bx + 95, y2 + 16, 48, 48)
        proof.paste(icons_32[i], (bx + 103, y2 + 24), icons_32[i])
        pdraw.text((bx + 105, y2 + 84), "32px", font=font_small, fill=(130, 120, 140, 255))
        
    # Row 3: Simulated Mobile Dock Bar (Active state in warm orange jelly button, Inactive in cream card)
    y3 = 480
    pdraw.text((35, y3 - 25), "手機大廳底部 Dock 實機模擬預覽（果凍厚底按鈕 · #1F1A3A 描邊 · 開源粉圓體）", font=font_sub, fill=(90, 75, 115, 255))
    
    dock_bg_rect = [25, y3, proof_w - 25, y3 + 225]
    pdraw.rectangle(dock_bg_rect, fill=(244, 240, 232, 255), outline=(215, 210, 200, 255), width=2)
    
    pdraw.text((45, y3 + 15), "【模擬：橫屏手遊底部 Dock 雙拇指熱區預覽（發條新村為已選中狀態）】", font=font_hud_lbl, fill=(80, 70, 95, 255))
    
    # Dock bar container
    bar_x, bar_y = 45, y3 + 45
    bar_w, bar_h = 910, 68
    pdraw.rounded_rectangle([bar_x, bar_y, bar_x + bar_w, bar_y + bar_h], radius=20, 
                            fill=(255, 253, 248, 255), outline=(210, 200, 185, 255), width=2)
                            
    tab_w = 172
    tab_gap = 10
    tab_names = ["發條新村", "角色裝備", "四區出征", "聚魂殿堂", "冒險背包"]
    
    for i in range(5):
        tx = bar_x + 10 + i * (tab_w + tab_gap)
        ty = bar_y + 7
        th = 54
        is_active = (i == 0) # Tab 0 active
        
        if is_active:
            # Active button: Warm orange jelly button with 5px thick bottom border
            # Bottom shadow plate (thick bottom)
            pdraw.rounded_rectangle([tx, ty + 4, tx + tab_w, ty + th + 4], radius=14, fill=(185, 95, 10, 255))
            # Main face
            pdraw.rounded_rectangle([tx, ty, tx + tab_w, ty + th], radius=14, 
                                    fill=(255, 160, 16, 255), outline=OUTLINE_COLOR, width=3)
            # Top highlight rim
            pdraw.arc([tx + 4, ty + 3, tx + tab_w - 4, ty + 20], 180, 360, fill=(255, 215, 120, 255), width=3)
            
            # Icon 32x32
            proof.paste(icons_32[i], (tx + 14, ty + 11), icons_32[i])
            # Text label
            pdraw.text((tx + 56, ty + 16), tab_names[i], font=font_tab, fill=(255, 255, 255, 255))
        else:
            # Inactive button: Cream card with 3px #1F1A3A outline
            pdraw.rounded_rectangle([tx, ty + 2, tx + tab_w, ty + th + 2], radius=14, fill=(235, 228, 216, 255))
            pdraw.rounded_rectangle([tx, ty, tx + tab_w, ty + th], radius=14, 
                                    fill=(255, 253, 248, 255), outline=OUTLINE_COLOR, width=3)
            # Icon 32x32
            proof.paste(icons_32[i], (tx + 14, ty + 11), icons_32[i])
            # Text label
            pdraw.text((tx + 56, ty + 16), tab_names[i], font=font_tab, fill=(45, 38, 60, 255))
            
    # Subtitle for comparison with old text-only dock
    pdraw.text((45, y3 + 130), "【對比：修改前純文字 PPT 頁籤（無圖示、缺乏視覺引導、手指熱區冷硬）】", font=font_small, fill=(170, 55, 55, 255))
    
    old_bar_y = y3 + 155
    old_bar_h = 48
    pdraw.rounded_rectangle([bar_x, old_bar_y, bar_x + bar_w, old_bar_y + old_bar_h], radius=14, 
                            fill=(255, 253, 248, 255), outline=(225, 220, 210, 255), width=1)
    for i in range(5):
        tx = bar_x + 10 + i * (tab_w + tab_gap)
        ty = old_bar_y + 4
        th = 40
        pdraw.rounded_rectangle([tx, ty, tx + tab_w, ty + th], radius=8, 
                                fill=(245, 242, 235, 255), outline=(210, 205, 195, 255), width=1)
        pdraw.text((tx + 54, ty + 10), tab_names[i], font=font_small, fill=(120, 110, 130, 255))
        
    # Row 4: Harmony Check with Approved Top HUD Icons
    y4 = 740
    pdraw.text((35, y4 - 15), "【風格全體系合規檢驗：與已過審頂部三資源圖示（能量／金幣／星屑）同框檢驗】", font=font_sub, fill=(90, 75, 115, 255))
    
    hud_ref_rect = [25, y4 + 10, proof_w - 25, y4 + 150]
    pdraw.rectangle(hud_ref_rect, fill=(244, 240, 232, 255), outline=(215, 210, 200, 255), width=2)
    
    # Load the 3 approved resource icons
    ref_names = ["icon_energy_key.png", "icon_gold_coin.png", "icon_gem_stardust.png"]
    ref_labels = ["能量鑰匙", "齒輪金幣", "星屑晶石"]
    for j, (rname, rlbl) in enumerate(zip(ref_names, ref_labels)):
        rpath = f"{OUT_DIR}/{rname}"
        if os.path.exists(rpath):
            rim = Image.open(rpath).resize((64, 64), Image.Resampling.LANCZOS)
            rx = 60 + j * 150
            draw_checker(rx, y4 + 35, 80, 80)
            proof.paste(rim, (rx + 8, y4 + 43), rim)
            pdraw.text((rx + 12, y4 + 120), f"[已過審] {rlbl}", font=font_small, fill=(35, 110, 70, 255))
            
    pdraw.text((540, y4 + 45), "合規驗證重點：", font=font_hud_lbl, fill=(31, 26, 58, 255))
    checklist = [
        "1. 統一 #1F1A3A 描邊色彩與 4-5px 等寬線條層次",
        "2. 嚴格左上向右下高光光影，塊面賽璐璐層次",
        "3. 零系統 Emoji、零毛皮、純機械玩具語彙",
        "4. 縮至 32px 保持極高特徵剪影辨識度"
    ]
    for k, item in enumerate(checklist):
        pdraw.text((540, y4 + 72 + k * 18), item, font=font_small, fill=(60, 50, 80, 255))
        
    proof_path = f"{PROOF_DIR}/proof_dock_five_icons.png"
    proof.save(proof_path, "PNG")
    print(f"Saved verification proof: {proof_path}")
    return proof_path


if __name__ == "__main__":
    generate_all()
