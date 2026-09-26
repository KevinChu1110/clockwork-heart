#!/usr/bin/env python3
"""
render_five_slots.py
Generate 5 slot icons for Clockwork Heart (發條之心) core tuning system:
1. slot_01_spring_generator.png  (發條發電機 - Winding Dynamo & Mainspring)
2. slot_02_chassis_armor.png      (機殼裝甲 - Chestplate Chassis & Ball Joints)
3. slot_03_escapement_governor.png(擒縱調速器 - Balance Wheel, Hairspring & Ruby Pallet Fork)
4. slot_04_transmission_gears.png  (傳動齒輪組 - Interlocking Dual Gears & Steel Bridge)
5. slot_05_resonance_core.png     (共鳴核心 - Glowing Aether Heart & Brass Gimbal Cage)

Specs:
- 128x128 RGBA PNG with transparent background
- 512x512 master rendered with subpixel geometry and supersampling, then Lanczos downscaled
- Dark blue-purple unified outline #1F1A3A
- Dopamine toy colors (sun gold #FFD028, orange #FFA010, mint #4ED86A, coral #FF5E8A, sky blue #38A0FF, ivory #FFFDF8)
- Zero fur, zero emoji, zero text
- Strictly mechanical clockwork toy aesthetics
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

OUTLINE_COLOR = (31, 26, 58, 255)  # #1F1A3A


def create_outline_from_alpha(img_rgba: Image.Image, radius: int = 14) -> Image.Image:
    """Create a dark #1F1A3A backing outline from an RGBA image's alpha mask."""
    alpha = img_rgba.split()[3]
    dilated_alpha = alpha.filter(ImageFilter.MaxFilter(radius * 2 + 1))
    
    # Base outline canvas
    outline_img = Image.new("RGBA", img_rgba.size, (0, 0, 0, 0))
    outline_draw = ImageDraw.Draw(outline_img)
    
    # Fill where dilated alpha > 20
    d_arr = np.array(dilated_alpha)
    outline_arr = np.zeros((img_rgba.size[1], img_rgba.size[0], 4), dtype=np.uint8)
    mask = d_arr > 30
    outline_arr[mask] = OUTLINE_COLOR
    outline_base = Image.fromarray(outline_arr, mode="RGBA")
    
    # Composite the original image on top of outline
    return Image.alpha_composite(outline_base, img_rgba)


def draw_rivet(draw: ImageDraw.Draw, cx: float, cy: float, r: float = 12.0, base_color=(255, 215, 60)):
    """Draw a chunky 3D metallic dome rivet with outline, highlight, and shadow."""
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=base_color, outline=OUTLINE_COLOR, width=max(2, int(r * 0.3)))
    # Shadow arc at bottom
    draw.arc([cx - r * 0.85, cy - r * 0.85, cx + r * 0.85, cy + r * 0.85], 30, 150, fill=(160, 90, 15, 220), width=max(2, int(r * 0.25)))
    # Specular glint at top-left
    hr = r * 0.35
    draw.ellipse([cx - r * 0.45, cy - r * 0.45, cx - r * 0.45 + hr, cy - r * 0.45 + hr], fill=(255, 255, 255, 240))


def draw_hex_bolt(draw: ImageDraw.Draw, cx: float, cy: float, r: float = 14.0, base_color=(255, 195, 45)):
    """Draw a chunky hexagonal bolt with central slot."""
    pts = []
    for i in range(6):
        angle = math.radians(i * 60 + 15)
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=base_color, outline=OUTLINE_COLOR)
    # Bevel lines to center
    for i in range(6):
        angle = math.radians(i * 60 + 15)
        draw.line([(cx, cy), pts[i]], fill=(180, 110, 20, 180), width=2)
    # Center indentation
    ir = r * 0.4
    draw.ellipse([cx - ir, cy - ir, cx + ir, cy + ir], fill=(130, 70, 10, 255), outline=OUTLINE_COLOR, width=2)


def draw_sparkle(draw: ImageDraw.Draw, cx: float, cy: float, r: float = 20.0, color=(255, 255, 255, 250)):
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
# 1. 發條發電機 (Spring Dynamo / Winding Generator)
# ==============================================================================
def render_slot_01_generator(size: int = 512) -> Image.Image:
    """
    Slot 1: 發條發電機
    - Circular brass dynamo stator frame with stator windings & flange bolts
    - Flat spiral Archimedean mainspring ribbon coiled inside
    - Prominent brass winding key at center-right
    - Kinetic energy arcs / sparks
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2.0, size / 2.0
    
    # 1. Dynamo outer chassis: 8-flanged circular stator housing
    housing_r = 195.0
    # Outer housing polygon with 8 tabs
    housing_pts = []
    for i in range(16):
        angle = math.radians(i * 22.5)
        r = housing_r if (i % 2 == 0) else (housing_r - 20)
        housing_pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(housing_pts, fill=(55, 65, 85, 255), outline=OUTLINE_COLOR)
    
    # Outer brass rim band
    draw.ellipse([cx - 170, cy - 170, cx + 170, cy + 170], fill=(225, 175, 40, 255), outline=OUTLINE_COLOR, width=6)
    # Stator copper coils (radial blocks around perimeter)
    for i in range(8):
        angle = math.radians(i * 45)
        # Copper coil block
        bx = cx + 145 * math.cos(angle)
        by = cy + 145 * math.sin(angle)
        draw.ellipse([bx - 18, by - 18, bx + 18, by + 18], fill=(235, 120, 35, 255), outline=OUTLINE_COLOR, width=3)
        draw_rivet(draw, bx, by, r=8, base_color=(255, 205, 50))
    
    # Inner dark spring chamber
    draw.ellipse([cx - 125, cy - 125, cx + 125, cy + 125], fill=(35, 30, 45, 255), outline=OUTLINE_COLOR, width=6)
    
    # 2. Archimedean spiral mainspring (發條鋼帶)
    # Render multiple thick concentric spiral coils with metallic brass/gold gradient
    num_pts = 600
    turns = 3.8
    spiral_pts = []
    for step in range(num_pts):
        t = step / float(num_pts)
        theta = t * turns * 2 * math.pi
        r = 28 + (115 - 28) * t
        x = cx + r * math.cos(theta)
        y = cy + r * math.sin(theta)
        spiral_pts.append((x, y))
    
    # Draw spring ribbon with dark shadow underlay
    for i in range(len(spiral_pts) - 1):
        p1 = spiral_pts[i]
        p2 = spiral_pts[i + 1]
        t = i / float(len(spiral_pts))
        w = int(14 - t * 6)
        # Shadow
        draw.line([p1, p2], fill=(20, 15, 30, 255), width=w + 6)
        # Ribbon body (metallic copper-brass)
        col = (int(255 - t * 40), int(190 - t * 40), int(40 + t * 40), 255)
        draw.line([p1, p2], fill=col, width=w)
        # Highlight edge
        draw.line([p1, p2], fill=(255, 240, 140, 255), width=max(2, w // 3))
    
    # Outer spring anchor block at top-right
    anchor_x = cx + 115 * math.cos(turns * 2 * math.pi)
    anchor_y = cy + 115 * math.sin(turns * 2 * math.pi)
    draw.rectangle([anchor_x - 14, anchor_y - 14, anchor_x + 14, anchor_y + 14], fill=(210, 150, 30, 255), outline=OUTLINE_COLOR, width=4)
    draw_hex_bolt(draw, anchor_x, anchor_y, r=10)
    
    # 3. Central Winding Key (發條鑰匙)
    # Key shaft and head angled diagonally at -35 degrees
    angle_k = math.radians(-35)
    cos_k, sin_k = math.cos(angle_k), math.sin(angle_k)
    perp_x, perp_y = -sin_k, cos_k
    
    # Center arbor hub
    draw.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=(255, 205, 45, 255), outline=OUTLINE_COLOR, width=5)
    
    # Key stem
    stem_len = 110.0
    k_head_cx = cx + stem_len * cos_k
    k_head_cy = cy + stem_len * sin_k
    
    # Draw thick stem from hub to key head
    stem_pts = [
        (cx - 16 * perp_x, cy - 16 * perp_y),
        (cx + 16 * perp_x, cy + 16 * perp_y),
        (k_head_cx + 16 * perp_x, k_head_cy + 16 * perp_y),
        (k_head_cx - 16 * perp_x, k_head_cy - 16 * perp_y)
    ]
    draw.polygon(stem_pts, fill=(245, 185, 35, 255), outline=OUTLINE_COLOR)
    # Stem collar
    collar_pos_x = cx + 55 * cos_k
    collar_pos_y = cy + 55 * sin_k
    draw.ellipse([collar_pos_x - 22, collar_pos_y - 22, collar_pos_x + 22, collar_pos_y + 22], fill=(255, 220, 60, 255), outline=OUTLINE_COLOR, width=4)
    
    # Key Head: Classic dual-lobed brass winding key wings
    lobe_dist = 52.0
    lobe_r = 44.0
    hole_r = 18.0
    
    l1_x = k_head_cx + lobe_dist * perp_x
    l1_y = k_head_cy + lobe_dist * perp_y
    l2_x = k_head_cx - lobe_dist * perp_x
    l2_y = k_head_cy - lobe_dist * perp_y
    
    # Lobes outer circles
    draw.ellipse([l1_x - lobe_r, l1_y - lobe_r, l1_x + lobe_r, l1_y + lobe_r], fill=(255, 215, 50, 255), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([l2_x - lobe_r, l2_y - lobe_r, l2_x + lobe_r, l2_y + lobe_r], fill=(255, 215, 50, 255), outline=OUTLINE_COLOR, width=5)
    # Connecting wing body
    wing_body_pts = [
        (l1_x + lobe_r * perp_x * 0.5, l1_y + lobe_r * perp_y * 0.5),
        (l2_x - lobe_r * perp_x * 0.5, l2_y - lobe_r * perp_y * 0.5),
        (k_head_cx - 24 * cos_k, k_head_cy - 24 * sin_k),
        (k_head_cx + 24 * cos_k, k_head_cy + 24 * sin_k)
    ]
    draw.polygon(wing_body_pts, fill=(255, 215, 50, 255), outline=OUTLINE_COLOR)
    # Key center cap
    draw.ellipse([k_head_cx - 26, k_head_cy - 26, k_head_cx + 26, k_head_cy + 26], fill=(255, 235, 100, 255), outline=OUTLINE_COLOR, width=4)
    # Cutout holes in lobes
    draw.ellipse([l1_x - hole_r, l1_y - hole_r, l1_x + hole_r, l1_y + hole_r], fill=(31, 26, 58, 255), outline=OUTLINE_COLOR, width=4)
    draw.ellipse([l2_x - hole_r, l2_y - hole_r, l2_x + hole_r, l2_y + hole_r], fill=(31, 26, 58, 255), outline=OUTLINE_COLOR, width=4)
    
    # Highlights & rivets on lobes
    draw_rivet(draw, l1_x, l1_y, r=7, base_color=(255, 255, 180))
    draw_rivet(draw, l2_x, l2_y, r=7, base_color=(255, 255, 180))
    
    # 4. Energy sparks (mint #4ED86A / cyan) radiating from dynamo
    draw_sparkle(draw, cx - 110, cy - 80, r=22, color=(78, 216, 106, 255))
    draw_sparkle(draw, cx - 70, cy + 110, r=18, color=(56, 160, 255, 255))
    draw_sparkle(draw, cx + 80, cy - 130, r=16, color=(255, 255, 255, 255))
    
    # Center hub jewel
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=3)
    draw.ellipse([cx - 8, cy - 8, cx + 2, cy + 2], fill=(255, 255, 255, 230))
    
    # Apply outer thick border
    return create_outline_from_alpha(img, radius=8)


# ==============================================================================
# 2. 機殼裝甲 (Chassis Armor / Plate Frame)
# ==============================================================================
def render_slot_02_chassis(size: int = 512) -> Image.Image:
    """
    Slot 2: 機殼裝甲
    - Heavy toy chestplate chassis (curved plates with toy proportions)
    - Ball-joint articulation sockets at shoulder corners (left/right)
    - Upper ivory-white enamel breastplate (#F7F4EB)
    - Lower segmented brass plating with center keel rib
    - Heavy corner hex bolts, plate rivets, and seam lines
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2.0, size / 2.0 + 10.0
    
    # 1. Backplate / shadow frame
    backplate_pts = [
        (cx - 130, cy - 170),  # Top left shoulder
        (cx + 130, cy - 170),  # Top right shoulder
        (cx + 175, cy - 90),   # Upper right wing
        (cx + 155, cy + 40),   # Mid right rib
        (cx + 110, cy + 160),  # Bottom right waist
        (cx, cy + 195),        # Bottom tip
        (cx - 110, cy + 160),  # Bottom left waist
        (cx - 155, cy + 40),   # Mid left rib
        (cx - 175, cy - 90),   # Upper left wing
    ]
    draw.polygon(backplate_pts, fill=(45, 55, 75, 255), outline=OUTLINE_COLOR)
    
    # 2. Left & Right Shoulder Ball-Joint Sockets (球形關節球窩)
    # Left socket
    ls_x, ls_y = cx - 145, cy - 115
    draw.ellipse([ls_x - 42, ls_y - 42, ls_x + 42, ls_y + 42], fill=(60, 68, 88, 255), outline=OUTLINE_COLOR, width=5)
    # Brass sphere ball inside
    draw.ellipse([ls_x - 30, ls_y - 30, ls_x + 30, ls_y + 30], fill=(245, 185, 45, 255), outline=OUTLINE_COLOR, width=4)
    draw_rivet(draw, ls_x, ls_y, r=10, base_color=(255, 230, 80))
    
    # Right socket
    rs_x, rs_y = cx + 145, cy - 115
    draw.ellipse([rs_x - 42, rs_y - 42, rs_x + 42, rs_y + 42], fill=(60, 68, 88, 255), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([rs_x - 30, rs_y - 30, rs_x + 30, rs_y + 30], fill=(245, 185, 45, 255), outline=OUTLINE_COLOR, width=4)
    draw_rivet(draw, rs_x, rs_y, r=10, base_color=(255, 230, 80))
    
    # 3. Lower Abdomen Plate: Segmented Brass/Bronze Armor
    lower_pts = [
        (cx - 135, cy - 10),
        (cx + 135, cy - 10),
        (cx + 100, cy + 150),
        (cx, cy + 185),
        (cx - 100, cy + 150)
    ]
    draw.polygon(lower_pts, fill=(225, 165, 35, 255), outline=OUTLINE_COLOR)
    
    # Horizontal armor segments in lower plate
    for y_offset in [35, 80, 125]:
        draw.line([(cx - 115 + (y_offset * 0.25), cy + y_offset), (cx + 115 - (y_offset * 0.25), cy + y_offset)], fill=OUTLINE_COLOR, width=4)
        draw.line([(cx - 110 + (y_offset * 0.25), cy + y_offset + 3), (cx + 110 - (y_offset * 0.25), cy + y_offset + 3)], fill=(255, 220, 90, 180), width=2)
    
    # 4. Upper Breastplate: Cream / Ivory Enamel Toy Plate (#FFFDF8 / #F4EEDC)
    upper_pts = [
        (cx - 95, cy - 160),   # Neck left
        (cx, cy - 135),        # Neck notch center
        (cx + 95, cy - 160),   # Neck right
        (cx + 145, cy - 85),   # Shoulder right
        (cx + 135, cy + 5),    # Chest right lower
        (cx, cy + 35),         # Chest bottom V-point
        (cx - 135, cy + 5),    # Chest left lower
        (cx - 145, cy - 85)    # Shoulder left
    ]
    draw.polygon(upper_pts, fill=(248, 244, 235, 255), outline=OUTLINE_COLOR)
    
    # Inner gold border bevel on ivory chestplate
    inner_upper_pts = [
        (cx - 80, cy - 145),
        (cx, cy - 122),
        (cx + 80, cy - 145),
        (cx + 125, cy - 80),
        (cx + 115, cy - 5),
        (cx, cy + 22),
        (cx - 115, cy - 5),
        (cx - 125, cy - 80)
    ]
    draw.polygon(inner_upper_pts, outline=(235, 185, 50, 255), width=4)
    
    # Center Keel Rib (vertical reinforced spine / mechanical ridge)
    keel_pts = [
        (cx - 18, cy - 120),
        (cx + 18, cy - 120),
        (cx + 14, cy + 175),
        (cx, cy + 185),
        (cx - 14, cy + 175)
    ]
    draw.polygon(keel_pts, fill=(210, 150, 30, 255), outline=OUTLINE_COLOR)
    draw.line([(cx, cy - 115), (cx, cy + 178)], fill=(255, 235, 120, 240), width=3)
    
    # 5. Core socket / Crest on upper chest
    crest_cy = cy - 45
    draw.ellipse([cx - 36, crest_cy - 36, cx + 36, crest_cy + 36], fill=(50, 60, 80, 255), outline=OUTLINE_COLOR, width=4)
    draw.ellipse([cx - 25, crest_cy - 25, cx + 25, crest_cy + 25], fill=(255, 195, 45, 255), outline=OUTLINE_COLOR, width=3)
    # Mint power indicator pip
    draw.ellipse([cx - 14, crest_cy - 14, cx + 14, crest_cy + 14], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=2)
    draw.ellipse([cx - 8, crest_cy - 8, cx, crest_cy], fill=(255, 255, 255, 240))
    
    # 6. Heavy Bolts and Rivets
    # Corner hex bolts on upper plate
    draw_hex_bolt(draw, cx - 115, cy - 70, r=12)
    draw_hex_bolt(draw, cx + 115, cy - 70, r=12)
    draw_hex_bolt(draw, cx - 85, cy + 125, r=11)
    draw_hex_bolt(draw, cx + 85, cy + 125, r=11)
    
    # Dome rivets along waist & neck
    draw_rivet(draw, cx - 60, cy - 145, r=8)
    draw_rivet(draw, cx + 60, cy - 145, r=8)
    draw_rivet(draw, cx - 75, cy + 25, r=7)
    draw_rivet(draw, cx + 75, cy + 25, r=7)
    draw_rivet(draw, cx, cy + 140, r=9, base_color=(255, 220, 70))
    
    # Specular shines
    draw_sparkle(draw, cx + 90, cy - 120, r=16, color=(255, 255, 255, 240))
    
    return create_outline_from_alpha(img, radius=8)


# ==============================================================================
# 3. 擒縱調速器 (Escapement Governor / Balance Regulator)
# ==============================================================================
def render_slot_03_escapement(size: int = 512) -> Image.Image:
    """
    Slot 3: 擒縱調速器
    - Large circular horological Balance Wheel (擺輪) with 3 curved spokes
    - Radial timing screws / poise weights around the rim
    - Delicate concentric coiled Hairspring (游絲)
    - Articulated Anchor Escapement Fork (擒縱叉) with dual vibrant ruby jewels (#FF2E7E)
    - Escape wheel ratchet teeth
    - Center ruby shock-absorber cap bearing
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2.0 - 15.0, size / 2.0 + 20.0
    
    # 1. Escapement Fork & Wheel in upper right
    ef_cx, ef_cy = cx + 130.0, cy - 135.0
    
    # Escape wheel (partial visible ratchet wheel)
    ew_r = 75.0
    ew_pts = []
    ew_teeth = 12
    for i in range(ew_teeth):
        a1 = math.radians(i * (360.0 / ew_teeth))
        a2 = a1 + math.radians(18)
        a3 = a1 + math.radians(28)
        ew_pts.append((ef_cx + (ew_r - 20) * math.cos(a1), ef_cy + (ew_r - 20) * math.sin(a1)))
        ew_pts.append((ef_cx + ew_r * math.cos(a2), ef_cy + ew_r * math.sin(a2)))
        ew_pts.append((ef_cx + (ew_r - 10) * math.cos(a3), ef_cy + (ew_r - 10) * math.sin(a3)))
    draw.polygon(ew_pts, fill=(225, 175, 45, 255), outline=OUTLINE_COLOR)
    draw.ellipse([ef_cx - 24, ef_cy - 24, ef_cx + 24, ef_cy + 24], fill=(70, 80, 100, 255), outline=OUTLINE_COLOR, width=3)
    draw_rivet(draw, ef_cx, ef_cy, r=8, base_color=(255, 215, 60))
    
    # Escapement Anchor Fork (擒縱叉) linking escape wheel to balance
    fork_pivot_x, fork_pivot_y = cx + 55.0, cy - 65.0
    # Fork bridge
    draw.line([(fork_pivot_x, fork_pivot_y), (ef_cx - 30, ef_cy + 20)], fill=(75, 85, 105, 255), width=16)
    draw.line([(fork_pivot_x, fork_pivot_y), (cx + 10, cy - 15)], fill=(75, 85, 105, 255), width=14)
    # Fork outline
    draw.line([(fork_pivot_x, fork_pivot_y), (ef_cx - 30, ef_cy + 20)], fill=OUTLINE_COLOR, width=3)
    draw.line([(fork_pivot_x, fork_pivot_y), (cx + 10, cy - 15)], fill=OUTLINE_COLOR, width=3)
    
    # Pallet Jewels (兩顆紅寶石叉瓦 - Entry & Exit Ruby Pallets)
    ruby_color = (255, 46, 126, 255)  # #FF2E7E Vibrant Ruby Magenta
    # Ruby 1 (Entry pallet)
    r1_x, r1_y = ef_cx - 45, ef_cy + 5
    draw.polygon([(r1_x - 12, r1_y - 6), (r1_x + 12, r1_y - 12), (r1_x + 8, r1_y + 12), (r1_x - 14, r1_y + 10)], fill=ruby_color, outline=OUTLINE_COLOR)
    draw.ellipse([r1_x - 4, r1_y - 4, r1_x + 4, r1_y + 4], fill=(255, 180, 210, 240))
    # Ruby 2 (Exit pallet)
    r2_x, r2_y = ef_cx - 10, ef_cy + 50
    draw.polygon([(r2_x - 10, r2_y - 10), (r2_x + 14, r2_y - 4), (r2_x + 10, r2_y + 14), (r2_x - 12, r2_y + 8)], fill=ruby_color, outline=OUTLINE_COLOR)
    draw.ellipse([r2_x - 4, r2_y - 4, r2_x + 4, r2_y + 4], fill=(255, 180, 210, 240))
    
    # Fork Pivot Jewel
    draw.ellipse([fork_pivot_x - 14, fork_pivot_y - 14, fork_pivot_x + 14, fork_pivot_y + 14], fill=ruby_color, outline=OUTLINE_COLOR, width=3)
    draw.ellipse([fork_pivot_x - 5, fork_pivot_y - 5, fork_pivot_x + 2, fork_pivot_y + 2], fill=(255, 255, 255, 240))
    
    # 2. Balance Wheel Outer Rim (擺輪金屬外環)
    bal_r = 160.0
    bal_thick = 28.0
    
    # Timing screws on balance wheel rim (8 radial screws)
    for i in range(12):
        angle = math.radians(i * 30 + 15)
        # Don't draw where fork overlaps
        if 20 <= (i * 30 + 15) <= 75:
            continue
        sx = cx + (bal_r + 14) * math.cos(angle)
        sy = cy + (bal_r + 14) * math.sin(angle)
        draw.ellipse([sx - 10, sy - 10, sx + 10, sy + 10], fill=(255, 220, 60, 255), outline=OUTLINE_COLOR, width=3)
        draw.line([(sx - 6 * math.cos(angle + math.pi/2), sy - 6 * math.sin(angle + math.pi/2)),
                   (sx + 6 * math.cos(angle + math.pi/2), sy + 6 * math.sin(angle + math.pi/2))], fill=(140, 80, 10, 255), width=2)
    
    # Rim outer circle
    draw.ellipse([cx - bal_r, cy - bal_r, cx + bal_r, cy + bal_r], fill=(245, 185, 45, 255), outline=OUTLINE_COLOR, width=6)
    # Rim inner cutout (creates thick ring)
    inner_bal_r = bal_r - bal_thick
    draw.ellipse([cx - inner_bal_r, cy - inner_bal_r, cx + inner_bal_r, cy + inner_bal_r], fill=(35, 30, 48, 255), outline=OUTLINE_COLOR, width=5)
    
    # 3. 3 Curved Spokes (三條優雅的擺輪金屬輪幅)
    for i in range(3):
        spoke_angle = math.radians(i * 120 - 30)
        # Spoke polygon tapering from hub to rim
        cos_s, sin_s = math.cos(spoke_angle), math.sin(spoke_angle)
        perp_s_x, perp_s_y = -sin_s, cos_s
        spoke_pts = [
            (cx + 35 * cos_s - 16 * perp_s_x, cy + 35 * sin_s - 16 * perp_s_y),
            (cx + 35 * cos_s + 16 * perp_s_x, cy + 35 * sin_s + 16 * perp_s_y),
            (cx + inner_bal_r * cos_s + 10 * perp_s_x, cy + inner_bal_r * sin_s + 10 * perp_s_y),
            (cx + inner_bal_r * cos_s - 10 * perp_s_x, cy + inner_bal_r * sin_s - 10 * perp_s_y)
        ]
        draw.polygon(spoke_pts, fill=(255, 205, 55, 255), outline=OUTLINE_COLOR)
        # Highlight along center of spoke
        draw.line([(cx + 35 * cos_s, cy + 35 * sin_s), (cx + inner_bal_r * cos_s, cy + inner_bal_r * sin_s)], fill=(255, 245, 140, 220), width=4)
    
    # 4. Concentric Hairspring (精密游絲)
    # Steel-blue fine coiled spring around balance staff
    spring_turns = 4.2
    spring_steps = 450
    h_pts = []
    for step in range(spring_steps):
        t = step / float(spring_steps)
        theta = t * spring_turns * 2 * math.pi
        r = 38 + (inner_bal_r - 42) * t
        hx = cx + r * math.cos(theta)
        hy = cy + r * math.sin(theta)
        h_pts.append((hx, hy))
    
    for i in range(len(h_pts) - 1):
        p1 = h_pts[i]
        p2 = h_pts[i + 1]
        draw.line([p1, p2], fill=(56, 160, 255, 240), width=4)
        draw.line([p1, p2], fill=(200, 235, 255, 200), width=2)
    
    # 5. Center Balance Staff Hub with Incabloc Shock Jewel (避震紅寶石軸承)
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(225, 165, 35, 255), outline=OUTLINE_COLOR, width=5)
    # Lyre-shaped brass spring holder (因加百祿避震簧槽)
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(70, 75, 95, 255), outline=OUTLINE_COLOR, width=4)
    # Center Ruby jewel
    draw.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=ruby_color, outline=OUTLINE_COLOR, width=3)
    draw.ellipse([cx - 9, cy - 9, cx + 2, cy + 2], fill=(255, 255, 255, 245))
    
    # Decorative sparkle
    draw_sparkle(draw, cx - 110, cy - 90, r=18, color=(255, 255, 255, 240))
    draw_sparkle(draw, ef_cx + 25, ef_cy - 40, r=16, color=(255, 46, 126, 240))
    
    return create_outline_from_alpha(img, radius=8)


# ==============================================================================
# 4. 傳動齒輪組 (Transmission Gearbox / Gear Train)
# ==============================================================================
def render_slot_04_gears(size: int = 512) -> Image.Image:
    """
    Slot 4: 傳動齒輪組
    - Two prominent interlocking chunky clockwork gears (large driver & smaller driven pinion)
    - Distinct colors (sun-gold #FFD028 and coral-orange/coral-pink #FF5E8A)
    - Distinct trapezoidal cogs meshing together precisely
    - Metallic connecting transmission bridge/bracket linking the dual axles
    - Central hexagonal retaining nuts and rivets
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Gear 1: Large drive gear at lower-left
    g1_cx, g1_cy = 190.0, 310.0
    g1_r_outer = 150.0
    g1_r_inner = 110.0
    g1_teeth = 8
    
    # Gear 2: Driven pinion gear at upper-right
    g2_cx, g2_cy = 345.0, 175.0
    g2_r_outer = 115.0
    g2_r_inner = 80.0
    g2_teeth = 6
    
    def generate_gear_polygon(cx, cy, r_outer, r_inner, num_teeth, phase=0.0):
        pts = []
        d_theta = 2 * math.pi / num_teeth
        for i in range(num_teeth):
            th0 = i * d_theta + phase
            th1 = th0 + d_theta * 0.22  # Rising flank
            th2 = th0 + d_theta * 0.50  # Outer tooth tip
            th3 = th0 + d_theta * 0.72  # Falling flank
            
            pts.append((cx + r_inner * math.cos(th0), cy + r_inner * math.sin(th0)))
            pts.append((cx + r_outer * math.cos(th1), cy + r_outer * math.sin(th1)))
            pts.append((cx + r_outer * math.cos(th2), cy + r_outer * math.sin(th2)))
            pts.append((cx + r_inner * math.cos(th3), cy + r_inner * math.sin(th3)))
        return pts
    
    # 1. Backing shadow for both gears
    g1_pts = generate_gear_polygon(g1_cx, g1_cy, g1_r_outer, g1_r_inner, g1_teeth, phase=math.radians(10))
    g2_pts = generate_gear_polygon(g2_cx, g2_cy, g2_r_outer, g2_r_inner, g2_teeth, phase=math.radians(38))
    
    # Draw gear 1 (Sun Gold #FFD028)
    draw.polygon(g1_pts, fill=(255, 208, 40, 255), outline=OUTLINE_COLOR)
    # Gear 1 recessed concentric plate
    draw.ellipse([g1_cx - 95, g1_cy - 95, g1_cx + 95, g1_cy + 95], fill=(230, 165, 30, 255), outline=OUTLINE_COLOR, width=5)
    # Gear 1 lightening holes (4 cutouts)
    for i in range(4):
        h_angle = math.radians(i * 90 + 45)
        hx = g1_cx + 56 * math.cos(h_angle)
        hy = g1_cy + 56 * math.sin(h_angle)
        draw.ellipse([hx - 18, hy - 18, hx + 18, hy + 18], fill=(40, 35, 55, 255), outline=OUTLINE_COLOR, width=4)
        draw.ellipse([hx - 8, hy - 8, hx - 2, hy - 2], fill=(255, 240, 140, 160))
    
    # Draw gear 2 (Coral Orange / Coral Pink #FF5E8A & #FFA010)
    draw.polygon(g2_pts, fill=(255, 110, 80, 255), outline=OUTLINE_COLOR)
    # Gear 2 inner stepped band
    draw.ellipse([g2_cx - 68, g2_cy - 68, g2_cx + 68, g2_cy + 68], fill=(235, 80, 60, 255), outline=OUTLINE_COLOR, width=4)
    # Gear 2 lightening holes (3 cutouts)
    for i in range(3):
        h_angle = math.radians(i * 120 + 20)
        hx = g2_cx + 40 * math.cos(h_angle)
        hy = g2_cy + 40 * math.sin(h_angle)
        draw.ellipse([hx - 14, hy - 14, hx + 14, hy + 14], fill=(40, 35, 55, 255), outline=OUTLINE_COLOR, width=3)
    
    # 2. Transmission Bridge / Bracket linking both gear pivots (鋼製傳動連桿夾板)
    bridge_angle = math.atan2(g2_cy - g1_cy, g2_cx - g1_cx)
    cos_b, sin_b = math.cos(bridge_angle), math.sin(bridge_angle)
    perp_b_x, perp_b_y = -sin_b, cos_b
    
    bridge_w = 40.0
    bridge_pts = [
        (g1_cx + 45 * perp_b_x, g1_cy + 45 * perp_b_y),
        (g2_cx + 36 * perp_b_x, g2_cy + 36 * perp_b_y),
        (g2_cx - 36 * perp_b_x, g2_cy - 36 * perp_b_y),
        (g1_cx - 45 * perp_b_x, g1_cy - 45 * perp_b_y)
    ]
    draw.polygon(bridge_pts, fill=(75, 85, 110, 255), outline=OUTLINE_COLOR)
    # Inner metallic plate highlight on bridge
    draw.line([(g1_cx, g1_cy), (g2_cx, g2_cy)], fill=(200, 215, 240, 240), width=6)
    
    # Round hubs on bridge ends
    draw.ellipse([g1_cx - 50, g1_cy - 50, g1_cx + 50, g1_cy + 50], fill=(85, 95, 120, 255), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([g2_cx - 40, g2_cy - 40, g2_cx + 40, g2_cy + 40], fill=(85, 95, 120, 255), outline=OUTLINE_COLOR, width=5)
    
    # 3. Retaining Hex Bolts on both hubs
    draw_hex_bolt(draw, g1_cx, g1_cy, r=22, base_color=(255, 210, 50))
    draw_hex_bolt(draw, g2_cx, g2_cy, r=18, base_color=(255, 210, 50))
    
    # Mid-bridge adjustment screw / oil port
    mid_bx = (g1_cx + g2_cx) / 2.0
    mid_by = (g1_cy + g2_cy) / 2.0
    draw_rivet(draw, mid_bx, mid_by, r=10, base_color=(78, 216, 106))
    
    # 4. Meshing sparks / kinetic glints
    mesh_x = (g1_cx + g2_cx) / 2.0 - 15.0
    mesh_y = (g1_cy + g2_cy) / 2.0 + 35.0
    draw_sparkle(draw, mesh_x, mesh_y, r=20, color=(255, 255, 255, 250))
    draw_sparkle(draw, g2_cx + 80, g2_cy - 60, r=16, color=(255, 220, 90, 240))
    draw_sparkle(draw, g1_cx - 95, g1_cy + 85, r=16, color=(255, 255, 255, 240))
    
    return create_outline_from_alpha(img, radius=8)


# ==============================================================================
# 5. 共鳴核心 (Resonance Core / Aether Heart)
# ==============================================================================
def render_slot_05_core(size: int = 512) -> Image.Image:
    """
    Slot 5: 共鳴核心
    - Glowing cyan-emerald multifaceted reactor crystal (#00FFCC / #4ED86A)
    - Outer 4-claw brass gimbal cage holding the core securely
    - Encircling resonant induction coil rings with copper copper bindings
    - Intense internal bloom, geometric facets, and 4-pointed starbursts
    - Zero doubt: unmistakably the radiant magical heart of the clockwork toy!
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size / 2.0, size / 2.0
    
    # 1. Outer Brass Gimbal Ring (八角/圓形黃銅外框夾具)
    outer_cage_r = 185.0
    cage_pts = []
    for i in range(8):
        angle = math.radians(i * 45)
        cage_pts.append((cx + outer_cage_r * math.cos(angle), cy + outer_cage_r * math.sin(angle)))
    draw.polygon(cage_pts, fill=(50, 45, 65, 255), outline=OUTLINE_COLOR)
    
    # Copper resonant induction coil band
    draw.ellipse([cx - 165, cy - 165, cx + 165, cy + 165], fill=(225, 140, 30, 255), outline=OUTLINE_COLOR, width=6)
    draw.ellipse([cx - 145, cy - 145, cx + 145, cy + 145], fill=(30, 25, 42, 255), outline=OUTLINE_COLOR, width=6)
    
    # 4 Corner mounting flanges with hex bolts
    for i in range(4):
        angle = math.radians(i * 90 + 45)
        fx = cx + 160 * math.cos(angle)
        fy = cy + 160 * math.sin(angle)
        draw.ellipse([fx - 22, fy - 22, fx + 22, fy + 22], fill=(255, 205, 45, 255), outline=OUTLINE_COLOR, width=4)
        draw_hex_bolt(draw, fx, fy, r=12)
    
    # 2. Glowing Cyan-Emerald Core Aura (多層發光晶石光暈)
    core_r = 115.0
    # Outer cyan bloom
    draw.ellipse([cx - core_r - 10, cy - core_r - 10, cx + core_r + 10, cy + core_r + 10], fill=(0, 220, 180, 180))
    # Mid-layer intense emerald-mint
    draw.ellipse([cx - core_r, cy - core_r, cx + core_r, cy + core_r], fill=(0, 255, 170, 255), outline=OUTLINE_COLOR, width=5)
    
    # 3. Geometric Crystal Facets (八邊形切割晶面)
    facet_r = 85.0
    facet_pts = []
    for i in range(8):
        angle = math.radians(i * 45 + 22.5)
        facet_pts.append((cx + facet_r * math.cos(angle), cy + facet_r * math.sin(angle)))
    draw.polygon(facet_pts, fill=(80, 255, 215, 255), outline=(0, 180, 140, 255), width=3)
    
    # Internal facet lines to center
    inner_facet_r = 45.0
    inner_facet_pts = []
    for i in range(8):
        angle = math.radians(i * 45 + 22.5)
        pt_inner = (cx + inner_facet_r * math.cos(angle), cy + inner_facet_r * math.sin(angle))
        inner_facet_pts.append(pt_inner)
        draw.line([facet_pts[i], pt_inner], fill=(160, 255, 240, 255), width=3)
    draw.polygon(inner_facet_pts, fill=(180, 255, 245, 255), outline=(0, 200, 160, 255), width=2)
    
    # Center white-hot energy core
    draw.ellipse([cx - 24, cy - 24, cx + 24, cy + 24], fill=(255, 255, 255, 255))
    
    # 4. 4 Heavy Mechanical Claws / Clamp Brackets gripping the core from outside
    claw_dirs = [0, 90, 180, 270]  # Right, Bottom, Left, Top
    for deg in claw_dirs:
        rad = math.radians(deg)
        cos_c, sin_c = math.cos(rad), math.sin(rad)
        perp_c_x, perp_c_y = -sin_c, cos_c
        
        # Claw root at cage rim
        root_x = cx + 160 * cos_c
        root_y = cy + 160 * sin_c
        # Claw tip extending over crystal edge
        tip_x = cx + 78 * cos_c
        tip_y = cy + 78 * sin_c
        
        claw_poly = [
            (root_x + 22 * perp_c_x, root_y + 22 * perp_c_y),
            (tip_x + 14 * perp_c_x, tip_y + 14 * perp_c_y),
            (tip_x - 14 * perp_c_x, tip_y - 14 * perp_c_y),
            (root_x - 22 * perp_c_x, root_y - 22 * perp_c_y)
        ]
        draw.polygon(claw_poly, fill=(245, 185, 45, 255), outline=OUTLINE_COLOR)
        # Claw retaining bolt
        draw_rivet(draw, (root_x + tip_x) / 2.0, (root_y + tip_y) / 2.0, r=8, base_color=(255, 235, 100))
        # Claw tip clamp tooth
        draw.ellipse([tip_x - 12, tip_y - 12, tip_x + 12, tip_y + 12], fill=(255, 220, 60, 255), outline=OUTLINE_COLOR, width=3)
    
    # 5. Radiant Aether Sparkles & Energy Discharge
    draw_sparkle(draw, cx - 45, cy - 45, r=26, color=(255, 255, 255, 255))
    draw_sparkle(draw, cx + 55, cy + 35, r=20, color=(160, 255, 240, 255))
    draw_sparkle(draw, cx - 120, cy + 90, r=18, color=(78, 216, 106, 255))
    draw_sparkle(draw, cx + 115, cy - 95, r=18, color=(56, 160, 255, 255))
    
    return create_outline_from_alpha(img, radius=8)


# ==============================================================================
# Main Generation Function
# ==============================================================================
def main():
    repo_root = "/opt/side/bravesoul-game"
    proof_dir = f"{repo_root}/proofs/t_40ae1da1"
    game_asset_dir = f"{repo_root}/game/assets/icons/core_slots"
    
    os.makedirs(proof_dir, exist_ok=True)
    os.makedirs(game_asset_dir, exist_ok=True)
    
    generators = [
        ("slot_01_spring_generator.png", render_slot_01_generator),
        ("slot_02_chassis_armor.png", render_slot_02_chassis),
        ("slot_03_escapement_governor.png", render_slot_03_escapement),
        ("slot_04_transmission_gears.png", render_slot_04_gears),
        ("slot_05_resonance_core.png", render_slot_05_core),
    ]
    
    print("=== Generating 5 Clockwork Core Slot Icons ===")
    for filename, gen_fn in generators:
        # 1. Render 512x512 master
        master_img = gen_fn(512)
        master_path = os.path.join(proof_dir, f"master_512_{filename}")
        master_img.save(master_path)
        
        # 2. Downscale with Lanczos to 128x128 production icon
        icon_128 = master_img.resize((128, 128), resample=Image.Resampling.LANCZOS)
        
        # Save to proofs/t_40ae1da1/
        proof_path = os.path.join(proof_dir, filename)
        icon_128.save(proof_path)
        
        # Also save to game/assets/icons/core_slots/
        asset_path = os.path.join(game_asset_dir, filename)
        icon_128.save(asset_path)
        
        print(f"  [OK] {filename} (128x128) -> {proof_path} & {asset_path}")

    print("All 5 slot icons generated successfully!")


if __name__ == "__main__":
    main()
