#!/usr/bin/env python3
"""
tools/build_item_icons.py
Generate 12 item icons for Clockwork Heart (發條之心) inventory:
- Consumables: hp_s, hp_m, bread, antidote, dust_crumb
- Materials: iron_scrap, wolf_fang, mist_shard, hunt_core, windup_fragment
- Key items: friendship_key, medal

Follows docs/ART_DAILY_CONSTITUTION.md:
- Deep warm brown / dark blue-purple outline (#1F1A3A)
- Bright cel-shading & dopamine color palette
- Clockwork toy aesthetic: brass metal plates, rivets, gears, zero fur/flesh
- 64x64 transparent PNG output to game/assets/icons/items/
- Proof sheet to proofs/item_icons/proof_items_overview.png
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

REPO_ROOT = "/opt/side/bravesoul-game"
OUT_DIR = f"{REPO_ROOT}/game/assets/icons/items"
PROOF_DIR = f"{REPO_ROOT}/proofs/item_icons"
FONT_PATH = f"{REPO_ROOT}/game/assets/fonts/jf-openhuninn-2.1.ttf"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PROOF_DIR, exist_ok=True)

OUTLINE_COLOR = (31, 26, 58, 255)  # #1F1A3A deep dark outline

# ----------------------------------------------------------------------
# Geometry and Rendering Helpers
# ----------------------------------------------------------------------

def create_outline_and_base(mask: np.ndarray, size=512, outline_radius=25) -> Image.Image:
    """Create a RGBA image with dilated outline from boolean mask."""
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    outline_mask = mask_img.filter(ImageFilter.MaxFilter(outline_radius))
    outline_arr = np.array(outline_mask) > 30
    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[outline_arr] = OUTLINE_COLOR
    return Image.fromarray(rgba, mode="RGBA")

def draw_rivet(draw: ImageDraw.Draw, x: float, y: float, r: float = 7.0, base_color=(255, 215, 60)):
    """Draw a 3D metallic dome rivet with outline, highlight, and shadow."""
    draw.ellipse([x - r, y - r, x + r, y + r], fill=base_color, outline=OUTLINE_COLOR, width=max(2, int(r * 0.35)))
    hr = r * 0.35
    draw.ellipse([x - r * 0.35, y - r * 0.35, x - r * 0.35 + hr, y - r * 0.35 + hr], fill=(255, 255, 255, 240))
    draw.arc([x - r, y - r, x + r, y + r], 20, 160, fill=(140, 80, 10, 200), width=max(2, int(r * 0.25)))

def get_brass_gradient_color(u: float, v: float):
    """Rich metallic golden brass gradient with warm lighting from top-left."""
    diag = 0.45 * u + 0.55 * v
    if diag < 0.25:
        t = diag / 0.25
        r = int(255 * (1 - t) + 255 * t)
        g = int(250 * (1 - t) + 220 * t)
        b = int(140 * (1 - t) + 60 * t)
    elif diag < 0.65:
        t = (diag - 0.25) / 0.40
        r = int(255 * (1 - t) + 235 * t)
        g = int(220 * (1 - t) + 155 * t)
        b = int(60 * (1 - t) + 20 * t)
    else:
        t = min(1.0, (diag - 0.65) / 0.35)
        r = int(235 * (1 - t) + 170 * t)
        g = int(155 * (1 - t) + 95 * t)
        b = int(20 * (1 - t) + 10 * t)
    return (r, g, b, 255)

# ----------------------------------------------------------------------
# 1. hp_s (小紅水) - Small Health Potion
# ----------------------------------------------------------------------
def render_hp_s(size=512) -> Image.Image:
    """
    Clockwork round flask with brass cap, brass neck ring, glowing strawberry red liquid.
    """
    y, x = np.mgrid[0:size, 0:size]
    # Flask bulb: sphere center (256, 320), radius 140
    dist_bulb = np.sqrt((x - 256.0)**2 + (y - 320.0)**2)
    bulb_mask = dist_bulb <= 138.0
    
    # Flask neck: x 216..296, y 155..230
    neck_mask = (x >= 216) & (x <= 296) & (y >= 155) & (y <= 230)
    
    # Brass cap & collar: y 100..165, x 195..317
    cap_mask = (x >= 200) & (x <= 312) & (y >= 105) & (y <= 165)
    # Winding stopper ring
    dist_ring = np.sqrt((x - 256.0)**2 + (y - 85.0)**2)
    stopper_ring = (dist_ring <= 40.0) & (dist_ring >= 18.0) & (y <= 115)
    
    total_mask = bulb_mask | neck_mask | cap_mask | stopper_ring
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Glass body with deep glowing ruby-red potion & glass reflections
    for py in range(155, 465):
        for px in range(110, 405):
            if bulb_mask[py, px] or neck_mask[py, px]:
                # Glass container background (soft dark tint)
                u = (px - 118) / 276.0
                v = (py - 155) / 305.0
                dist_c = np.sqrt((px - 256.0)**2 + (py - 320.0)**2) / 138.0
                
                # Liquid level is at y = 220
                if py >= 220 and dist_c <= 0.94:
                    # Inside red potion
                    # Radial gradient from bright candy-red (#FF3366) to deep crimson (#A00A2C)
                    liquid_dist = np.sqrt((px - 225.0)**2 + (py - 295.0)**2) / 140.0
                    lr = int(255 - liquid_dist * 85)
                    lg = int(60 - liquid_dist * 50)
                    lb = int(105 - liquid_dist * 75)
                    lr = max(130, min(255, lr))
                    lg = max(10, min(80, lg))
                    lb = max(25, min(120, lb))
                    
                    # Highlight crescent on upper-left
                    if px < 210 and py < 340 and dist_c > 0.65:
                        lr = min(255, lr + 65)
                        lg = min(255, lg + 55)
                        lb = min(255, lb + 65)
                    img.putpixel((px, py), (lr, lg, lb, 255))
                else:
                    # Glass neck / empty glass top
                    gr = int(220 + u * 20 - v * 40)
                    gg = int(235 + u * 15 - v * 30)
                    gb = int(250 - v * 20)
                    img.putpixel((px, py), (gr, gg, gb, 255))
                    
    # Liquid surface meniscus line
    draw.ellipse([256 - 95, 215, 256 + 95, 235], fill=(255, 120, 160, 255), outline=OUTLINE_COLOR, width=4)
    # Floating heart bubble inside potion
    draw.ellipse([230, 275, 282, 327], fill=(255, 110, 150, 255), outline=(180, 20, 50, 255), width=4)
    draw.ellipse([238, 282, 252, 296], fill=(255, 255, 255, 230))
    # Specular glass arc on left
    draw.arc([140, 205, 372, 435], 135, 215, fill=(255, 255, 255, 240), width=16)
    # Secondary highlight
    draw.arc([165, 230, 347, 410], 145, 195, fill=(255, 255, 255, 180), width=8)
    
    # 2. Brass Cap & Neck Collar
    for py in range(65, 175):
        for px in range(190, 325):
            if cap_mask[py, px] or stopper_ring[py, px]:
                u = (px - 190) / 135.0
                v = (py - 65) / 110.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    # Brass cap details & collar
    draw.rectangle([198, 142, 314, 166], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=6)
    draw.rectangle([210, 105, 302, 142], fill=(245, 195, 45, 255), outline=OUTLINE_COLOR, width=6)
    # Rivets on collar
    draw_rivet(draw, 225, 154, r=6)
    draw_rivet(draw, 256, 154, r=6)
    draw_rivet(draw, 287, 154, r=6)
    # Stopper ring hole inner outline
    draw.ellipse([256 - 18, 85 - 18, 256 + 18, 85 + 18], fill=(0, 0, 0, 0), outline=OUTLINE_COLOR, width=6)
    
    return img

# ----------------------------------------------------------------------
# 2. hp_m (中紅水) - Medium Health Potion
# ----------------------------------------------------------------------
def render_hp_m(size=512) -> Image.Image:
    """
    Clockwork potion bottle with brass cage / reinforcing brackets, graduation ticks,
    winding key stopper, and rich crimson glowing elixir.
    """
    y, x = np.mgrid[0:size, 0:size]
    # Bottle body: rectangular base with chamfered top corners (x: 135..377, y: 200..450)
    body_box = (x >= 140) & (x <= 372) & (y >= 210) & (y <= 445)
    # Chamfered shoulders
    chamfer_l = (y >= 170) & (y <= 210) & (y >= 210 - (x - 140.0) * 0.8)
    chamfer_r = (y >= 170) & (y <= 210) & (y >= 210 - (372.0 - x) * 0.8)
    neck_mask = (x >= 210) & (x <= 302) & (y >= 125) & (y <= 175)
    
    # Winding key stopper at top
    key_stem = (x >= 238) & (x <= 274) & (y >= 70) & (y <= 130)
    dist_l = np.sqrt((x - 200.0)**2 + (y - 75.0)**2)
    dist_r = np.sqrt((x - 312.0)**2 + (y - 75.0)**2)
    key_wings = (dist_l <= 46.0) | (dist_r <= 46.0) | ((x >= 200) & (x <= 312) & (y >= 50) & (y <= 95))
    hole_l = dist_l < 20.0
    hole_r = dist_r < 20.0
    key_mask = (key_stem | key_wings) & (~hole_l) & (~hole_r)
    
    bottle_mask = body_box | chamfer_l | chamfer_r | neck_mask
    total_mask = bottle_mask | key_mask
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Bottle Glass and Potion
    for py in range(165, 450):
        for px in range(135, 378):
            if bottle_mask[py, px]:
                u = (px - 140) / 232.0
                v = (py - 165) / 285.0
                if py >= 215:
                    # Inside rich potion (#FF1744 -> #880E4F)
                    diag = 0.3 * u + 0.7 * v
                    pr = int(255 - diag * 90)
                    pg = int(35 - diag * 25)
                    pb = int(75 - diag * 40)
                    # Specular left band
                    if 155 <= px <= 185:
                        pr = min(255, pr + 60)
                        pg = min(255, pg + 40)
                        pb = min(255, pb + 60)
                    img.putpixel((px, py), (pr, pg, pb, 255))
                else:
                    # Upper glass chamber
                    img.putpixel((px, py), (225, 238, 252, 255))
                    
    # Liquid surface
    draw.line([(175, 215), (337, 215)], fill=(255, 120, 160, 255), width=7)
    # Glass vertical highlight
    draw.line([(165, 220), (165, 430)], fill=(255, 255, 255, 220), width=10)
    
    # 2. Brass protective cage & base brackets
    # Base bracket
    draw.rectangle([132, 420, 380, 456], fill=(245, 195, 45, 255), outline=OUTLINE_COLOR, width=6)
    # Corner guards
    draw.rectangle([132, 380, 158, 430], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=5)
    draw.rectangle([354, 380, 380, 430], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=5)
    # Measurement ticks on right edge
    for ty in [250, 290, 330, 370]:
        draw.line([(340, ty), (365, ty)], fill=OUTLINE_COLOR, width=5)
        draw.line([(342, ty), (363, ty)], fill=(255, 220, 80, 255), width=3)
    # Neck collar
    draw.rectangle([202, 140, 310, 172], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=6)
    
    # Rivets on base & collar
    draw_rivet(draw, 170, 438, r=6)
    draw_rivet(draw, 256, 438, r=6)
    draw_rivet(draw, 342, 438, r=6)
    draw_rivet(draw, 230, 156, r=5)
    draw_rivet(draw, 282, 156, r=5)
    
    # 3. Winding Key Stopper
    for py in range(45, 145):
        for px in range(190, 325):
            if key_mask[py, px]:
                u = (px - 190) / 135.0
                v = (py - 45) / 100.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    draw.ellipse([200 - 20, 75 - 20, 200 + 20, 75 + 20], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=5)
    draw.ellipse([312 - 20, 75 - 20, 312 + 20, 75 + 20], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=5)
    # Center jewel on key
    draw.ellipse([256 - 16, 75 - 16, 256 + 16, 75 + 16], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=4)
    draw.ellipse([256 - 6, 75 - 8, 256 + 2, 75], fill=(255, 255, 255, 220))
    
    return img

# ----------------------------------------------------------------------
# 3. bread (乾糧) - Toy World Rations / Butter Biscuit Bar
# ----------------------------------------------------------------------
def render_bread(size=512) -> Image.Image:
    """
    Baked golden-honey biscuit bar stamped with a clockwork gear / cross mark,
    wrapped in cream-white parchment with a brass clamp.
    """
    y, x = np.mgrid[0:size, 0:size]
    # Main biscuit body: rounded rectangle (x: 110..402, y: 130..390)
    # Soft rounded pill / block
    dx = np.maximum(0, np.maximum(145 - x, x - 367))
    dy = np.maximum(0, np.maximum(165 - y, y - 355))
    dist_bread = np.sqrt(dx**2 + dy**2)
    biscuit_mask = dist_bread <= 35.0
    
    # Brass clamp / tag at top-right
    dist_tag = np.sqrt((x - 380.0)**2 + (y - 150.0)**2)
    tag_mask = (dist_tag <= 32.0)
    
    total_mask = biscuit_mask | tag_mask
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Baked Biscuit Surface (Golden-Honey warm gradient #F89B29 -> #E67E22)
    for py in range(120, 400):
        for px in range(100, 412):
            if biscuit_mask[py, px]:
                u = (px - 110) / 292.0
                v = (py - 130) / 260.0
                # Diagonal warm toasted gradient
                diag = 0.4 * u + 0.6 * v
                br = int(255 - diag * 40)
                bg = int(185 - diag * 65)
                bb = int(75 - diag * 45)
                # Edge crust browning
                d_edge = dist_bread[py, px] / 35.0
                if d_edge > 0.6:
                    br = int(br * 0.88)
                    bg = int(bg * 0.82)
                    bb = int(bb * 0.75)
                img.putpixel((px, py), (br, bg, bb, 255))
                
    # Parchment wrapper around middle: y: 225..315
    for py in range(225, 315):
        for px in range(105, 407):
            if biscuit_mask[py, px]:
                v = (py - 225) / 90.0
                wr = int(255 - v * 20)
                wg = int(252 - v * 22)
                wb = int(240 - v * 30)
                img.putpixel((px, py), (wr, wg, wb, 255))
                
    # Parchment wrapper border lines
    draw.line([(108, 225), (404, 225)], fill=OUTLINE_COLOR, width=6)
    draw.line([(108, 315), (404, 315)], fill=OUTLINE_COLOR, width=6)
    # Blue stripe on wrapper (Clockwork brand)
    draw.rectangle([108, 255, 404, 285], fill=(56, 160, 255, 255), outline=OUTLINE_COLOR, width=5)
    
    # Stamped Clockwork Gear on Upper Biscuit Face
    hub_x, hub_y = 256, 175
    # Gear stamp: dark toasted indentation
    draw.ellipse([hub_x - 36, hub_y - 36, hub_x + 36, hub_y + 36], fill=(195, 110, 25, 255), outline=OUTLINE_COLOR, width=5)
    # 6 gear teeth
    for a_deg in range(0, 360, 60):
        rad = math.radians(a_deg)
        tx = hub_x + int(math.cos(rad) * 44)
        ty = hub_y + int(math.sin(rad) * 44)
        draw.rectangle([tx - 8, ty - 8, tx + 8, ty + 8], fill=(195, 110, 25, 255), outline=OUTLINE_COLOR, width=4)
    # Inner stamped hole
    draw.ellipse([hub_x - 16, hub_y - 16, hub_x + 16, hub_y + 16], fill=(245, 170, 60, 255), outline=OUTLINE_COLOR, width=4)
    
    # Toasted dots on lower biscuit
    for dx_dot, dy_dot in [(-60, 350), (-20, 360), (30, 352), (70, 365), (0, 340)]:
        draw.ellipse([hub_x + dx_dot - 4, dy_dot - 4, hub_x + dx_dot + 4, dy_dot + 4], fill=(175, 90, 20, 255))
        
    # Brass clamp tag at top right
    draw.ellipse([380 - 28, 150 - 28, 380 + 28, 150 + 28], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=5)
    draw_rivet(draw, 380, 150, r=9)
    
    return img

# ----------------------------------------------------------------------
# 4. antidote (清焰露) - Purifying Dew / Mint Elixir
# ----------------------------------------------------------------------
def render_antidote(size=512) -> Image.Image:
    """
    Slender teardrop crystal vial with brass filigree collar,
    glowing luminous mint-teal elixir (#00E699 / #4ED86A).
    """
    y, x = np.mgrid[0:size, 0:size]
    # Teardrop bottle: bulb at center (256, 330), r=120, narrowing up to (256, 170), width=60
    dist_bulb = np.sqrt((x - 256.0)**2 + (y - 330.0)**2)
    bulb_part = dist_bulb <= 125.0
    
    # Neck taper
    neck_slope = (y >= 165) & (y <= 330) & (np.abs(x - 256.0) <= (30.0 + (y - 165.0) * 0.58))
    vial_glass = bulb_part | neck_slope
    
    # Stopper & collar at top (y: 80..165, x: 215..297)
    collar_mask = (x >= 210) & (x <= 302) & (y >= 135) & (y <= 175)
    stopper_loop = (np.sqrt((x - 256.0)**2 + (y - 105.0)**2) <= 35.0) & (np.sqrt((x - 256.0)**2 + (y - 105.0)**2) >= 15.0)
    stopper_stem = (x >= 238) & (x <= 274) & (y >= 115) & (y <= 145)
    
    total_mask = vial_glass | collar_mask | stopper_loop | stopper_stem
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Glowing Mint-Teal Liquid
    for py in range(165, 460):
        for px in range(125, 387):
            if vial_glass[py, px]:
                dist_c = np.sqrt((px - 256.0)**2 + (py - 330.0)**2) / 125.0
                u = (px - 130) / 252.0
                v = (py - 165) / 295.0
                
                if py >= 220:
                    # Pure mint green glow (#00E699 / #4ED86A to #007A5E)
                    mr = int(0 + (1 - v) * 50)
                    mg = int(245 - dist_c * 80)
                    mb = int(160 + (1 - dist_c) * 60)
                    # Bright core spark
                    if np.sqrt((px - 245)**2 + (py - 320)**2) < 45:
                        mr = min(255, mr + 150)
                        mg = 255
                        mb = min(255, mb + 80)
                    img.putpixel((px, py), (mr, mg, mb, 255))
                else:
                    # Clear crystal neck
                    img.putpixel((px, py), (225, 250, 245, 255))
                    
    # Meniscus line
    draw.ellipse([256 - 55, 214, 256 + 55, 228], fill=(130, 255, 210, 255), outline=OUTLINE_COLOR, width=4)
    # Glass highlight arc
    draw.arc([150, 230, 362, 440], 130, 210, fill=(255, 255, 255, 230), width=12)
    # Floating spark diamond inside
    cx, cy = 256, 320
    draw.polygon([(cx, cy - 25), (cx + 18, cy), (cx, cy + 25), (cx - 18, cy)], fill=(255, 255, 255, 240))
    
    # 2. Brass collar & leaf filigree
    for py in range(75, 176):
        for px in range(210, 305):
            if collar_mask[py, px] or stopper_loop[py, px] or stopper_stem[py, px]:
                u = (px - 210) / 95.0
                v = (py - 75) / 100.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    draw.rectangle([212, 142, 300, 168], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=6)
    draw_rivet(draw, 235, 155, r=5)
    draw_rivet(draw, 277, 155, r=5)
    # Stopper inner hole outline
    draw.ellipse([256 - 15, 105 - 15, 256 + 15, 105 + 15], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=5)
    
    return img

# ----------------------------------------------------------------------
# 5. dust_crumb (星屑碎) - Stardust Gem Crumb
# ----------------------------------------------------------------------
def render_dust_crumb(size=512) -> Image.Image:
    """
    Faceted cosmic stardust crystal fragment: celestial sapphire/violet (#38A0FF / #9B51E0)
    gem with brass clockwork prong claw setting.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Star crystal polyhedron vertices:
    # Top apex (256, 95), Bottom apex (256, 425), Left apex (105, 256), Right apex (407, 256)
    # Plus intermediate inner facets
    # Diamond boundary: |x - 256|/151 + |y - 256|/169 <= 1.0
    dist_diamond = np.abs(x - 256.0) / 151.0 + np.abs(y - 256.0) / 169.0
    gem_mask = dist_diamond <= 1.0
    
    # Brass base prongs at bottom-left and bottom-right
    prong_l = (x >= 140) & (x <= 185) & (y >= 335) & (y <= 420)
    prong_r = (x >= 327) & (x <= 372) & (y >= 335) & (y <= 420)
    prong_b = (x >= 225) & (x <= 287) & (y >= 405) & (y <= 455)
    prongs = prong_l | prong_r | prong_b
    
    total_mask = gem_mask | prongs
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # Define multifaceted faces with contrasting blues and violets
    # Facet 1: Top-Left (#60B8FF)
    draw.polygon([(256, 95), (256, 256), (195, 205), (105, 256)], fill=(75, 175, 255, 255))
    # Facet 2: Upper Central (#9BE5FF - main bright facet)
    draw.polygon([(256, 95), (317, 205), (256, 256), (195, 205)], fill=(160, 230, 255, 255))
    # Facet 3: Top-Right (#38A0FF)
    draw.polygon([(256, 95), (407, 256), (317, 205)], fill=(56, 160, 255, 255))
    # Facet 4: Center Table (#7B61FF - royal violet)
    draw.polygon([(195, 205), (256, 256), (256, 335), (170, 290)], fill=(123, 97, 255, 255))
    # Facet 5: Center-Right Table (#5E40E5)
    draw.polygon([(317, 205), (256, 256), (256, 335), (342, 290)], fill=(94, 64, 229, 255))
    # Facet 6: Bottom-Left (#4D2DB7)
    draw.polygon([(105, 256), (170, 290), (256, 335), (256, 425)], fill=(65, 40, 160, 255))
    # Facet 7: Bottom-Right (#321B87 - deep shadow)
    draw.polygon([(407, 256), (342, 290), (256, 335), (256, 425)], fill=(45, 25, 125, 255))
    
    # Internal facet wireframe lines
    facet_lines = [
        ((256, 95), (256, 425)),
        ((105, 256), (407, 256)),
        ((256, 95), (195, 205)),
        ((256, 95), (317, 205)),
        ((195, 205), (256, 256)),
        ((317, 205), (256, 256)),
        ((195, 205), (170, 290)),
        ((317, 205), (342, 290)),
        ((170, 290), (256, 335)),
        ((342, 290), (256, 335)),
    ]
    for p1, p2 in facet_lines:
        draw.line([p1, p2], fill=OUTLINE_COLOR, width=5)
        
    # Specular Glint Star on Upper Central Facet
    sx, sy = 240, 160
    draw.polygon([(sx, sy - 30), (sx + 8, sy - 8), (sx + 30, sy), (sx + 8, sy + 8),
                  (sx, sy + 30), (sx - 8, sy + 8), (sx - 30, sy), (sx - 8, sy - 8)],
                 fill=(255, 255, 255, 250))
    # Tiny sparkle dot
    draw.ellipse([335 - 5, 230 - 5, 335 + 5, 230 + 5], fill=(255, 255, 255, 240))
    
    # Brass Claw Clamps
    for py in range(330, 460):
        for px in range(135, 380):
            if prongs[py, px]:
                u = (px - 135) / 245.0
                v = (py - 330) / 130.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    draw.line([(140, 340), (180, 415)], fill=OUTLINE_COLOR, width=6)
    draw.line([(372, 340), (332, 415)], fill=OUTLINE_COLOR, width=6)
    draw_rivet(draw, 165, 385, r=6)
    draw_rivet(draw, 347, 385, r=6)
    draw_rivet(draw, 256, 430, r=7)
    
    return img

# ----------------------------------------------------------------------
# 6. iron_scrap (鐵屑) - Iron Scrap / Mechanical Cog Fragments
# ----------------------------------------------------------------------
def render_iron_scrap(size=512) -> Image.Image:
    """
    Clockwork mechanical workshop scrap: broken brass/steel cog sector with teeth,
    hexagonal nut, and riveted metal plate with scratches.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Component 1: Broken Cog Sector (Top-Left to Bottom-Right)
    # Center (190, 240), r_outer=160, r_inner=70
    dist_cog = np.sqrt((x - 190.0)**2 + (y - 240.0)**2)
    angle_cog = np.arctan2(y - 240.0, x - 190.0)
    # Sector spanning angle -1.5 to 1.5 rad
    sector = (angle_cog >= -1.4) & (angle_cog <= 1.4)
    # Gear teeth profile
    teeth_wave = np.sin(angle_cog * 8.0)
    r_teeth = 135.0 + teeth_wave * 25.0
    cog_body = sector & (dist_cog >= 60.0) & (dist_cog <= r_teeth)
    
    # Component 2: Hexagonal Nut (Bottom-Right, center 335, 335, r=75)
    # Hexagon mask: max(|x*cos(a) + y*sin(a)|) for a in [0, 60, 120]
    hx = x - 335.0
    hy = y - 335.0
    hex_dist = np.maximum(np.abs(hx), np.abs(hx * 0.5 + hy * 0.866))
    hex_dist = np.maximum(hex_dist, np.abs(hx * 0.5 - hy * 0.866))
    nut_body = hex_dist <= 72.0
    nut_hole = np.sqrt(hx**2 + hy**2) < 28.0
    nut_mask = nut_body & (~nut_hole)
    
    # Component 3: Flat Metal Strip / Plate with Rivets across upper-right
    plate_mask = (x >= 240) & (x <= 405) & (y >= 125) & (y <= 185)
    
    total_mask = cog_body | nut_mask | plate_mask
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Cog Body (Lacquered Blue-Steel / Pewter with brass edge)
    for py in range(70, 420):
        for px in range(120, 380):
            if cog_body[py, px]:
                u = (px - 120) / 260.0
                v = (py - 70) / 350.0
                diag = 0.4 * u + 0.6 * v
                # Cool steel-blue gradient
                sr = int(160 - diag * 60)
                sg = int(185 - diag * 55)
                sb = int(210 - diag * 40)
                img.putpixel((px, py), (sr, sg, sb, 255))
                
    # Cog inner rim outline
    draw.arc([190 - 60, 240 - 60, 190 + 60, 240 + 60], -80, 80, fill=OUTLINE_COLOR, width=6)
    # Cog outer tooth outline
    draw.arc([190 - 135, 240 - 135, 190 + 135, 240 + 135], -80, 80, fill=OUTLINE_COLOR, width=5)
    
    # 2. Fill Flat Metal Plate (Warm Brass)
    for py in range(125, 186):
        for px in range(240, 406):
            if plate_mask[py, px]:
                u = (px - 240) / 165.0
                v = (py - 125) / 60.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
    draw.rectangle([240, 125, 405, 185], fill=None, outline=OUTLINE_COLOR, width=6)
    draw_rivet(draw, 275, 155, r=7)
    draw_rivet(draw, 370, 155, r=7)
    
    # 3. Fill Hexagonal Nut (Bright Golden Brass)
    for py in range(260, 415):
        for px in range(260, 415):
            if nut_mask[py, px]:
                u = (px - 260) / 155.0
                v = (py - 260) / 155.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    # Hex nut chamfer facet lines
    draw.ellipse([335 - 28, 335 - 28, 335 + 28, 335 + 28], fill=None, outline=OUTLINE_COLOR, width=6)
    # Screw threads inside nut hole
    for ty in [325, 335, 345]:
        draw.line([(318, ty), (352, ty - 4)], fill=OUTLINE_COLOR, width=3)
    # Outer hex perimeter
    hex_pts = []
    for deg in range(0, 360, 60):
        rad = math.radians(deg)
        hex_pts.append((335 + int(math.cos(rad) * 72), 335 + int(math.sin(rad) * 72)))
    draw.polygon(hex_pts, fill=None, outline=OUTLINE_COLOR, width=6)
    
    return img

# ----------------------------------------------------------------------
# 7. wolf_fang (狼牙) - Mechanical Beast Fang Plate
# ----------------------------------------------------------------------
def render_wolf_fang(size=512) -> Image.Image:
    """
    Lacquered steel mechanical beast fang mounted in a heavy brass base socket
    with dual rivets and clockwork gear teeth at the mount. Zero fur!
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Curved Fang Blade: Ivory lacquered steel plate
    # Base at bottom-right (270..380, 290..410), curving gracefully to sharp tip at (130, 110)
    # Quadratic bezier spine from (340, 370) to (210, 280) to (130, 110)
    # We can model fang as polygon with curved profile
    # Let's compute distance along spine
    spine_x = 130.0 + (x - 130.0)
    # Outer convex arc (upper-left): center (380, 80), radius ~260
    # Inner concave arc (lower-right): center (280, 20), radius ~290
    dist_outer = np.sqrt((x - 380.0)**2 + (y - 80.0)**2)
    dist_inner = np.sqrt((x - 270.0)**2 + (y - 20.0)**2)
    fang_body = (dist_outer >= 235.0) & (dist_outer <= 325.0) & (dist_inner <= 350.0) & (y >= 105) & (y <= 385) & (x >= 125) & (x <= 365)
    
    # Brass base socket at bottom: centered around (310, 350)
    socket_mask = (x >= 235) & (x <= 405) & (y >= 295) & (y <= 425) & ((x - 235) * 0.7 + (y - 295) >= 20)
    # Mini gear tooth on socket base
    dist_gear = np.sqrt((x - 385.0)**2 + (y - 395.0)**2)
    socket_gear = (dist_gear <= 35.0)
    
    total_mask = fang_body | socket_mask | socket_gear
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Fang Blade (Ivory-Enamel Metal Plate #FFFDF8 -> #D5CDBD)
    for py in range(100, 390):
        for px in range(120, 370):
            if fang_body[py, px]:
                u = (px - 125) / 245.0
                v = (py - 105) / 285.0
                diag = 0.5 * u + 0.5 * v
                # Clean glossy porcelain/ivory finish
                fr = int(255 - diag * 40)
                fg = int(252 - diag * 42)
                fb = int(245 - diag * 50)
                # Outer edge shine
                if dist_outer[py, px] < 255:
                    fr = min(255, fr + 15)
                    fg = min(255, fg + 15)
                    fb = min(255, fb + 15)
                img.putpixel((px, py), (fr, fg, fb, 255))
                
    # Fang central longitudinal ridge line
    draw.line([(130, 110), (195, 210)], fill=OUTLINE_COLOR, width=5)
    draw.line([(195, 210), (285, 340)], fill=OUTLINE_COLOR, width=5)
    # Bright specular line on blade edge
    draw.line([(138, 120), (188, 200)], fill=(255, 255, 255, 240), width=6)
    
    # 2. Fill Brass Base Socket
    for py in range(290, 430):
        for px in range(230, 420):
            if socket_mask[py, px] or socket_gear[py, px]:
                u = (px - 230) / 190.0
                v = (py - 290) / 140.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    # Socket edge bands and mechanical plate seam
    draw.line([(240, 305), (370, 420)], fill=OUTLINE_COLOR, width=7)
    draw.line([(270, 295), (400, 410)], fill=OUTLINE_COLOR, width=7)
    # Heavy mounting rivets on the socket
    draw_rivet(draw, 280, 355, r=8)
    draw_rivet(draw, 335, 395, r=8)
    draw_rivet(draw, 335, 340, r=7)
    
    return img

# ----------------------------------------------------------------------
# 8. mist_shard (霧晶) - Mist Shard / Luminous Teal Crystal
# ----------------------------------------------------------------------
def render_mist_shard(size=512) -> Image.Image:
    """
    Floating rhomboid ice-cyan / misty aqua crystal prism with
    a delicate brass internal clockwork gear silhouette shining through.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Rhombus Crystal Prism:
    # Top (256, 75), Bottom (256, 435), Left (130, 256), Right (382, 256)
    dist_prism = np.abs(x - 256.0) / 126.0 + np.abs(y - 256.0) / 180.0
    prism_mask = dist_prism <= 1.0
    
    # Brass clamp band across center: y: 236..276, x: 125..387
    band_mask = (y >= 240) & (y <= 272) & prism_mask
    # Top suspension ring
    dist_ring = np.sqrt((x - 256.0)**2 + (y - 75.0)**2)
    ring_mask = (dist_ring <= 36.0) & (dist_ring >= 16.0) & (y <= 95)
    
    total_mask = prism_mask | ring_mask
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # Facet Polygons:
    # 1. Left Upper Facet (#70E0D0 - vivid mint-cyan)
    draw.polygon([(256, 75), (130, 256), (256, 256)], fill=(112, 224, 208, 255))
    # 2. Right Upper Facet (#A8F5E5 - luminous bright highlight)
    draw.polygon([(256, 75), (382, 256), (256, 256)], fill=(185, 250, 240, 255))
    # 3. Left Lower Facet (#20B2AA - sea green shadow)
    draw.polygon([(130, 256), (256, 435), (256, 256)], fill=(40, 178, 170, 255))
    # 4. Right Lower Facet (#008B8B - deep cyan shadow)
    draw.polygon([(382, 256), (256, 435), (256, 256)], fill=(10, 140, 145, 255))
    
    # Internal Clockwork Gear Silhouette faintly visible inside the misty crystal
    hub_x, hub_y = 256, 256
    draw.ellipse([hub_x - 55, hub_y - 55, hub_x + 55, hub_y + 55], fill=(230, 195, 65, 180), outline=(31, 26, 58, 160), width=4)
    # Gear teeth
    for deg in range(0, 360, 45):
        rad = math.radians(deg)
        tx = hub_x + int(math.cos(rad) * 65)
        ty = hub_y + int(math.sin(rad) * 65)
        draw.rectangle([tx - 8, ty - 8, tx + 8, ty + 8], fill=(230, 195, 65, 180), outline=(31, 26, 58, 160), width=3)
    draw.ellipse([hub_x - 22, hub_y - 22, hub_x + 22, hub_y + 22], fill=(185, 250, 240, 220), outline=(31, 26, 58, 160), width=3)
    
    # Facet separator lines
    draw.line([(256, 75), (256, 435)], fill=OUTLINE_COLOR, width=5)
    draw.line([(130, 256), (382, 256)], fill=OUTLINE_COLOR, width=5)
    
    # Specular glint on upper right ridge
    draw.line([(262, 100), (360, 240)], fill=(255, 255, 255, 230), width=6)
    # Sparkle Star
    draw.polygon([(300, 170 - 20), (300 + 5, 170 - 5), (300 + 20, 170), (300 + 5, 170 + 5),
                  (300, 170 + 20), (300 - 5, 170 + 5), (300 - 20, 170), (300 - 5, 170 - 5)],
                 fill=(255, 255, 255, 255))
                 
    # Brass Clamp Band across crystal equator
    for py in range(240, 273):
        for px in range(125, 388):
            if band_mask[py, px]:
                u = (px - 125) / 263.0
                v = (py - 240) / 33.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
    draw.rectangle([130, 240, 382, 272], fill=None, outline=OUTLINE_COLOR, width=6)
    draw_rivet(draw, 190, 256, r=6)
    draw_rivet(draw, 256, 256, r=6)
    draw_rivet(draw, 322, 256, r=6)
    
    # Top suspension brass loop
    for py in range(50, 96):
        for px in range(220, 295):
            if ring_mask[py, px]:
                img.putpixel((px, py), get_brass_gradient_color(0.5, 0.2))
    draw.ellipse([256 - 16, 75 - 16, 256 + 16, 75 + 16], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=5)
    
    return img

# ----------------------------------------------------------------------
# 9. hunt_core (溢核) - Gyroscopic Overflow Engine Core
# ----------------------------------------------------------------------
def render_hunt_core(size=512) -> Image.Image:
    """
    Pulsing magenta / neon ruby energy sphere (#FF2A85 / #FF5E8A) encased in
    concentric brass gimbal rings with gear teeth and rivets.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Central Pulsing Energy Core: Sphere center (256, 256), r=95
    dist_core = np.sqrt((x - 256.0)**2 + (y - 256.0)**2)
    core_mask = dist_core <= 95.0
    
    # Outer Gimbal Ring (Brass with gear notches): r_out=175, r_in=130
    dist_ring1 = np.sqrt((x - 256.0)**2 + (y - 256.0)**2)
    ring1_mask = (dist_ring1 <= 175.0) & (dist_ring1 >= 130.0)
    
    # 8 Gear Teeth on Outer Gimbal Ring
    angle = np.arctan2(y - 256.0, x - 256.0)
    teeth_profile = np.cos(angle * 8.0)
    teeth_mask = (dist_ring1 <= 192.0) & (dist_ring1 >= 170.0) & (teeth_profile > 0.6)
    
    # Tilted Inner Gimbal Ring (Ellipse): rx=125, ry=50
    # Rotation by 45 degrees
    xr = (x - 256.0) * 0.707 + (y - 256.0) * 0.707
    yr = -(x - 256.0) * 0.707 + (y - 256.0) * 0.707
    dist_inner_gimbal = (xr / 125.0)**2 + (yr / 45.0)**2
    inner_gimbal = (dist_inner_gimbal <= 1.25) & (dist_inner_gimbal >= 0.75)
    
    total_mask = core_mask | ring1_mask | teeth_mask | inner_gimbal
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Outer Gimbal Ring & Teeth (Golden Brass)
    for py in range(60, 455):
        for px in range(60, 455):
            if ring1_mask[py, px] or teeth_mask[py, px]:
                u = (px - 60) / 395.0
                v = (py - 60) / 395.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    draw.ellipse([256 - 175, 256 - 175, 256 + 175, 256 + 175], fill=None, outline=OUTLINE_COLOR, width=6)
    draw.ellipse([256 - 130, 256 - 130, 256 + 130, 256 + 130], fill=None, outline=OUTLINE_COLOR, width=6)
    
    # Rivets on Outer Gimbal Ring
    for deg in [45, 135, 225, 315]:
        rad = math.radians(deg)
        rx = 256 + int(math.cos(rad) * 152)
        ry = 256 + int(math.sin(rad) * 152)
        draw_rivet(draw, rx, ry, r=7)
        
    # 2. Fill Glowing Energy Core Sphere (Magenta/Fuchsia #FF2A85 / #FF5E8A)
    for py in range(155, 355):
        for px in range(155, 355):
            if core_mask[py, px]:
                d = dist_core[py, px] / 95.0
                # Radial glow from white-pink center to vibrant fuchsia
                cr = 255
                cg = int(50 + (1 - d) * 150)
                cb = int(140 + (1 - d) * 100)
                if d < 0.35:
                    cg = 230
                    cb = 240
                img.putpixel((px, py), (cr, cg, cb, 255))
                
    draw.ellipse([256 - 95, 256 - 95, 256 + 95, 256 + 95], fill=None, outline=OUTLINE_COLOR, width=6)
    # Energy equator rings inside core
    draw.ellipse([256 - 80, 256 - 25, 256 + 80, 256 + 25], fill=None, outline=(255, 255, 255, 220), width=5)
    
    # 3. Fill Tilted Inner Brass Ring
    for py in range(140, 370):
        for px in range(140, 370):
            if inner_gimbal[py, px] and not core_mask[py, px]:
                img.putpixel((px, py), get_brass_gradient_color(0.6, 0.4))
                
    # Center White Sparkle
    draw.ellipse([256 - 15, 256 - 15, 256 + 15, 256 + 15], fill=(255, 255, 255, 250))
    
    return img

# ----------------------------------------------------------------------
# 10. windup_fragment (發條碎片) - Windup Cog & Spring Fragment
# ----------------------------------------------------------------------
def render_windup_fragment(size=512) -> Image.Image:
    """
    Curved golden brass clockwork gear sector with 4 crisp teeth, riveted flange,
    and a spiraling blued-steel clockwork mainspring fragment.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Gear Sector: center (330, 180), angle from 110 deg to 240 deg (pointing down-left)
    angle_g = np.arctan2(y - 180.0, x - 330.0)
    dist_g = np.sqrt((x - 330.0)**2 + (y - 180.0)**2)
    sector_g = (angle_g >= 1.8) & (angle_g <= 3.1)
    
    # Gear teeth wave
    teeth_wave = np.sin(angle_g * 10.0)
    r_outer = 175.0 + teeth_wave * 28.0
    gear_arc = sector_g & (dist_g >= 90.0) & (dist_g <= r_outer)
    
    # Inner Hub Flange with rivet hole
    hub_mask = (dist_g <= 92.0) & (dist_g >= 40.0) & sector_g
    hole_flange = np.sqrt((x - 260.0)**2 + (y - 230.0)**2) < 16.0
    hub_mask = hub_mask & (~hole_flange)
    
    # Coiled Mainspring Fragment (Blued steel spiral ribbon):
    # Archimedean spiral: r = a + b * theta
    # Represented by concentric spring bands curving towards (160, 360)
    dist_spring1 = np.abs(np.sqrt((x - 220.0)**2 + (y - 260.0)**2) - 110.0) <= 16.0
    dist_spring2 = np.abs(np.sqrt((x - 200.0)**2 + (y - 280.0)**2) - 65.0) <= 16.0
    spring_angle = np.arctan2(y - 270.0, x - 210.0)
    spring_mask = (dist_spring1 | dist_spring2) & (spring_angle >= 0.5) & (spring_angle <= 3.0) & (y >= 230)
    
    total_mask = gear_arc | hub_mask | spring_mask
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Coiled Spring (Tempered Blued Steel #3A506B / #5BC0BE)
    for py in range(220, 440):
        for px in range(70, 320):
            if spring_mask[py, px]:
                u = (px - 70) / 250.0
                v = (py - 220) / 220.0
                diag = 0.5 * u + 0.5 * v
                sr = int(65 + diag * 30)
                sg = int(125 + diag * 50)
                sb = int(190 + diag * 40)
                img.putpixel((px, py), (sr, sg, sb, 255))
                
    # Spring metallic sheen line
    draw.arc([220 - 110, 260 - 110, 220 + 110, 260 + 110], 45, 170, fill=(180, 230, 255, 230), width=6)
    
    # 2. Fill Gear Sector & Hub (Bright Golden Brass)
    for py in range(70, 360):
        for px in range(120, 380):
            if gear_arc[py, px] or hub_mask[py, px]:
                u = (px - 120) / 260.0
                v = (py - 70) / 290.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    # Gear border outlines
    draw.arc([330 - 90, 180 - 90, 330 + 90, 180 + 90], 105, 178, fill=OUTLINE_COLOR, width=6)
    # Rivet on the hub flange
    draw_rivet(draw, 290, 210, r=8)
    draw_rivet(draw, 230, 250, r=8)
    # Cutout hole outline
    draw.ellipse([260 - 16, 230 - 16, 260 + 16, 230 + 16], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=5)
    
    return img

# ----------------------------------------------------------------------
# 11. friendship_key (友誼鑰匙) - Heart Friendship Winding Key
# ----------------------------------------------------------------------
def render_friendship_key(size=512) -> Image.Image:
    """
    Heart-shaped twin wing winding key in bright golden brass (#FFD028 / #FFA010)
    with central emerald jewel and dual-notched key bit.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Key stem: x: 232..280, y: 180..425
    stem_mask = (x >= 234) & (x <= 278) & (y >= 180) & (y <= 425)
    # Stem rounded bottom
    stem_bottom = ((x - 256.0)**2 + (y - 425.0)**2) <= (22.0**2)
    # Key bit teeth at bottom right (x: 278..328, y: 360..415)
    bit_notch1 = (x >= 278) & (x <= 332) & (y >= 365) & (y <= 388)
    bit_notch2 = (x >= 278) & (x <= 322) & (y >= 398) & (y <= 422)
    # Stem collar
    collar_mask = (x >= 218) & (x <= 294) & (y >= 265) & (y <= 295)
    
    # Heart Wings at Top: Center (256, 150)
    # Left lobe center (175, 130), Right lobe center (337, 130)
    dist_l = np.sqrt((x - 175.0)**2 + (y - 130.0)**2)
    dist_r = np.sqrt((x - 337.0)**2 + (y - 130.0)**2)
    dist_hub = np.sqrt((x - 256.0)**2 + (y - 165.0)**2)
    
    wings_solid = (dist_l <= 68.0) | (dist_r <= 68.0) | (dist_hub <= 65.0) | \
                  ((x >= 175) & (x <= 337) & (y >= 90) & (y <= 185))
                  
    # Heart cutouts inside wings: Left (175, 130) r=28, Right (337, 130) r=28
    hole_l = dist_l < 30.0
    hole_r = dist_r < 30.0
    
    key_body = (wings_solid | stem_mask | stem_bottom | bit_notch1 | bit_notch2 | collar_mask) & (~hole_l) & (~hole_r)
    img = create_outline_and_base(key_body, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Key Body with Warm Golden Brass
    for py in range(60, 450):
        for px in range(105, 350):
            if key_body[py, px]:
                u = (px - 105) / 245.0
                v = (py - 60) / 390.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    # Wing hole inner outlines
    draw.ellipse([175 - 30, 130 - 30, 175 + 30, 130 + 30], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=6)
    draw.ellipse([337 - 30, 130 - 30, 337 + 30, 130 + 30], fill=(0,0,0,0), outline=OUTLINE_COLOR, width=6)
    
    # Stem vertical highlight & shadow
    draw.line([(244, 185), (244, 420)], fill=(255, 255, 255, 220), width=6)
    draw.line([(268, 185), (268, 420)], fill=(160, 95, 15, 220), width=6)
    
    # Collar ring with rivets
    draw.rectangle([218, 265, 294, 295], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=5)
    draw_rivet(draw, 238, 280, r=5)
    draw_rivet(draw, 274, 280, r=5)
    
    # 2. Central Emerald Heart Gem
    cx, cy = 256, 165
    draw.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=6)
    # Emerald Jewel (#4ED86A)
    draw.ellipse([cx - 30, cy - 30, cx + 30, cy + 30], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=5)
    # Emerald facet sparkle
    draw.ellipse([cx - 15, cy - 18, cx - 3, cy - 6], fill=(255, 255, 255, 230))
    
    return img

# ----------------------------------------------------------------------
# 12. medal (勳章) - Martial Achievement Cog Medal
# ----------------------------------------------------------------------
def render_medal(size=512) -> Image.Image:
    """
    6-toothed golden brass cog medal with embossed clockwork heart relief,
    suspended from a bicolored royal blue and warm orange ribbon.
    """
    y, x = np.mgrid[0:size, 0:size]
    
    # Ribbon at Top: V-shaped hanging ribbon from (180, 60) to (332, 60) down to (256, 220)
    # Left strap: (180, 60) -> (225, 60) -> (256, 210) -> (210, 210)
    # Right strap: (287, 60) -> (332, 60) -> (256, 210) -> (302, 210)
    ribbon_mask = (y >= 60) & (y <= 220) & (np.abs(x - 256.0) <= (76.0 - (y - 60.0) * 0.15))
    
    # Medal Cog Disk: Center (256, 310), r=120
    dist_medal = np.sqrt((x - 256.0)**2 + (y - 310.0)**2)
    angle_medal = np.arctan2(y - 310.0, x - 256.0)
    # 6 Cog Teeth
    teeth_wave = np.cos(angle_medal * 6.0)
    r_outer = 118.0 + teeth_wave * 22.0
    medal_cog = dist_medal <= r_outer
    
    # Suspension hanger clasp: x 220..292, y 185..220
    clasp_mask = (x >= 220) & (x <= 292) & (y >= 185) & (y <= 220)
    
    total_mask = ribbon_mask | medal_cog | clasp_mask
    img = create_outline_and_base(total_mask, size=size, outline_radius=27)
    draw = ImageDraw.Draw(img)
    
    # 1. Fill Ribbon: Dual Color (Left Royal Blue #38A0FF, Right Warm Orange #FFA010)
    for py in range(60, 220):
        for px in range(160, 350):
            if ribbon_mask[py, px]:
                if px < 256:
                    # Blue stripe
                    img.putpixel((px, py), (56, 160, 255, 255))
                else:
                    # Orange stripe
                    img.putpixel((px, py), (255, 160, 16, 255))
                    
    draw.line([(256, 60), (256, 220)], fill=OUTLINE_COLOR, width=5)
    # Ribbon top bar
    draw.rectangle([170, 52, 342, 68], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=5)
    
    # 2. Fill Brass Clasp
    for py in range(185, 221):
        for px in range(220, 293):
            if clasp_mask[py, px]:
                img.putpixel((px, py), get_brass_gradient_color(0.5, 0.3))
    draw.rectangle([220, 185, 292, 220], fill=None, outline=OUTLINE_COLOR, width=5)
    draw_rivet(draw, 256, 202, r=6)
    
    # 3. Fill Golden Cog Medal
    for py in range(170, 450):
        for px in range(115, 395):
            if medal_cog[py, px]:
                u = (px - 115) / 280.0
                v = (py - 170) / 280.0
                img.putpixel((px, py), get_brass_gradient_color(u, v))
                
    # Outer Cog rim
    draw.ellipse([256 - 95, 310 - 95, 256 + 95, 310 + 95], fill=None, outline=OUTLINE_COLOR, width=6)
    # Inner circular disc (#FFFDF8 cream enamel inlay)
    draw.ellipse([256 - 80, 310 - 80, 256 + 80, 310 + 80], fill=(255, 250, 235, 255), outline=OUTLINE_COLOR, width=5)
    
    # Embossed Clockwork Heart Emblem in Center
    cx, cy = 256, 310
    draw.ellipse([cx - 42, cy - 42, cx + 42, cy + 42], fill=(255, 215, 60, 255), outline=OUTLINE_COLOR, width=5)
    # Emerald Clockwork Heart core
    draw.ellipse([cx - 28, cy - 28, cx + 28, cy + 28], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=4)
    # Glint
    draw.ellipse([cx - 14, cy - 18, cx - 2, cy - 6], fill=(255, 255, 255, 230))
    
    # Rivets around outer rim
    for deg in range(30, 390, 60):
        rad = math.radians(deg)
        rx = 256 + int(math.cos(rad) * 115)
        ry = 310 + int(math.sin(rad) * 115)
        draw_rivet(draw, rx, ry, r=6)
        
    return img

# ----------------------------------------------------------------------
# Main Generator and Proof Sheet Builder
# ----------------------------------------------------------------------

ITEMS = [
    # Consumables
    ("hp_s", "小紅水", "消耗品", render_hp_s),
    ("hp_m", "中紅水", "消耗品", render_hp_m),
    ("bread", "乾糧", "消耗品", render_bread),
    ("antidote", "清焰露", "消耗品", render_antidote),
    ("dust_crumb", "星屑碎", "消耗品", render_dust_crumb),
    # Materials
    ("iron_scrap", "鐵屑", "素材", render_iron_scrap),
    ("wolf_fang", "狼牙", "素材", render_wolf_fang),
    ("mist_shard", "霧晶", "素材", render_mist_shard),
    ("hunt_core", "溢核", "素材", render_hunt_core),
    ("windup_fragment", "發條碎片", "素材", render_windup_fragment),
    # Key items
    ("friendship_key", "友誼鑰匙", "重要物", render_friendship_key),
    ("medal", "勳章", "重要物", render_medal),
]

def build_all():
    print(f"Generating {len(ITEMS)} item icons...")
    
    rendered_masters = {}
    
    for item_id, name_tw, cat, render_func in ITEMS:
        print(f"  Rendering [{cat}] {item_id} ({name_tw})...")
        master_img = render_func(size=512)
        rendered_masters[item_id] = master_img
        
        # Downsample to 64x64 transparent PNG
        icon_64 = master_img.resize((64, 64), Image.Resampling.LANCZOS)
        out_path = os.path.join(OUT_DIR, f"{item_id}.png")
        icon_64.save(out_path, format="PNG")
        print(f"    Saved 64x64 -> {out_path}")
        
    # Generate Consolidated Proof Sheet
    print("Building overview proof sheet...")
    # 4 columns x 3 rows
    cols = 4
    rows = 3
    cell_w, cell_h = 320, 240
    sheet_w = cols * cell_w + 80
    sheet_h = rows * cell_h + 160
    
    # Cream dopamine background (#FFFDF8)
    sheet = Image.new("RGBA", (sheet_w, sheet_h), (255, 253, 248, 255))
    draw = ImageDraw.Draw(sheet)
    
    # Load Font
    try:
        title_font = ImageFont.truetype(FONT_PATH, 34)
        subtitle_font = ImageFont.truetype(FONT_PATH, 20)
        label_font = ImageFont.truetype(FONT_PATH, 22)
        cat_font = ImageFont.truetype(FONT_PATH, 16)
    except Exception as e:
        print(f"Font load error: {e}, using default")
        title_font = subtitle_font = label_font = cat_font = ImageFont.load_default()
        
    # Title banner
    draw.rectangle([0, 0, sheet_w, 100], fill=(31, 26, 58, 255))
    draw.text((40, 22), "《發條之心》背包道具圖示驗收清單（12 款 64x64）", fill=(255, 208, 40, 255), font=title_font)
    draw.text((40, 64), "規範：深暖褐描邊(#1F1A3A) · 亮色賽璐璐 · 金屬黃銅質感 · 零毛皮玩具世界觀 · 64x64 PNG", fill=(220, 225, 240, 255), font=subtitle_font)
    
    # Category colors
    cat_colors = {
        "消耗品": (255, 94, 138, 255),  # Coral Pink
        "素材": (56, 160, 255, 255),    # Sky Blue
        "重要物": (255, 180, 0, 255),   # Golden Yellow
    }
    
    for idx, (item_id, name_tw, cat, _) in enumerate(ITEMS):
        c = idx % cols
        r = idx // cols
        cx = 40 + c * cell_w
        cy = 120 + r * cell_h
        
        # Cell background card (Rounded soft card)
        draw.rounded_rectangle([cx, cy, cx + cell_w - 20, cy + cell_h - 20], radius=16, 
                               fill=(245, 243, 238, 255), outline=OUTLINE_COLOR, width=3)
        
        # Category Tag badge
        draw.rounded_rectangle([cx + 14, cy + 14, cx + 84, cy + 40], radius=8, fill=cat_colors[cat])
        draw.text((cx + 22, cy + 18), cat, fill=(255, 255, 255, 255), font=cat_font)
        
        # Name & ID
        draw.text((cx + 94, cy + 14), name_tw, fill=OUTLINE_COLOR, font=label_font)
        draw.text((cx + 94, cy + 42), f"id: {item_id}", fill=(110, 105, 125, 255), font=cat_font)
        
        # 128x128 preview (enlarged for easy detail review)
        preview_128 = rendered_masters[item_id].resize((128, 128), Image.Resampling.LANCZOS)
        # Background box for 128 preview (transparent checker or mint card)
        box_x, box_y = cx + 24, cy + 70
        draw.rounded_rectangle([box_x, box_y, box_x + 132, box_y + 132], radius=12, fill=(255, 255, 255, 255), outline=(200, 195, 210, 255), width=2)
        sheet.paste(preview_128, (box_x + 2, box_y + 2), preview_128)
        
        # Native 64x64 preview (as seen in game)
        icon_64 = preview_128.resize((64, 64), Image.Resampling.LANCZOS)
        box64_x, box64_y = cx + 180, cy + 70
        draw.rounded_rectangle([box64_x, box64_y, box64_x + 72, box64_y + 72], radius=10, fill=(230, 238, 245, 255), outline=(180, 190, 210, 255), width=2)
        sheet.paste(icon_64, (box64_x + 4, box64_y + 4), icon_64)
        draw.text((box64_x + 8, box64_y + 80), "64x64 實機", fill=(130, 125, 145, 255), font=cat_font)
        
        # Dark slot test (HUD / dark inventory cell preview)
        dark_x, dark_y = cx + 180, cy + 115
        draw.rounded_rectangle([dark_x, dark_y, dark_x + 72, dark_y + 72], radius=10, fill=(31, 26, 58, 255), outline=(60, 50, 90, 255), width=2)
        sheet.paste(icon_64, (dark_x + 4, dark_y + 4), icon_64)
        draw.text((dark_x + 8, dark_y + 54), "深底", fill=(255, 255, 255, 200), font=cat_font)

    proof_path = os.path.join(PROOF_DIR, "proof_items_overview.png")
    sheet.save(proof_path, format="PNG")
    print(f"Proof sheet saved to -> {proof_path}")
    print("Done!")

if __name__ == "__main__":
    build_all()
