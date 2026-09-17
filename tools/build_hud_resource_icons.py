#!/usr/bin/env python3
"""
tools/build_hud_resource_icons.py
Generate top HUD resource icons (Energy Winding Key, Gold Coin, Stardust Gem)
for Clockwork Heart (發條之心) mobile lobby HUD.
Outputs 128x128 RGBA PNGs to game/assets/icons/hud/ and inspection proofs.
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

# Outline color from ART_DAILY_CONSTITUTION §3 & User Profile:
# Deep blue-purple #1F1A3A
OUTLINE_COLOR = (31, 26, 58, 255)

def create_energy_key_master(size=512) -> Image.Image:
    """Render 512x512 Energy Winding Key with rich brass cel-shading and glowing teal/mint core."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    hub_x, hub_y = 256.0, 205.0
    
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    
    # Distance to stem
    stem_mask = (x_coords >= 228) & (x_coords <= 284) & (y_coords >= 200) & (y_coords <= 442)
    # Stem base rounded bottom
    stem_bottom = ((x_coords - 256.0)**2 + (y_coords - 442.0)**2) <= (28.0**2)
    # Key bit teeth (mechanical notch on right)
    bit_notch1 = (x_coords >= 270) & (x_coords <= 330) & (y_coords >= 382) & (y_coords <= 408)
    bit_notch2 = (x_coords >= 270) & (x_coords <= 320) & (y_coords >= 418) & (y_coords <= 440)
    # Collar ring on stem
    collar_mask = (x_coords >= 214) & (x_coords <= 298) & (y_coords >= 288) & (y_coords <= 320)
    
    # Wings
    dist_l_wing = np.sqrt((x_coords - 140.0)**2 + (y_coords - 165.0)**2)
    dist_r_wing = np.sqrt((x_coords - 372.0)**2 + (y_coords - 165.0)**2)
    dist_top_lobe = np.sqrt((x_coords - 256.0)**2 + (y_coords - 136.0)**2)
    dist_hub = np.sqrt((x_coords - hub_x)**2 + (y_coords - hub_y)**2)
    
    wings_solid = (dist_l_wing <= 88.0) | (dist_r_wing <= 88.0) | (dist_top_lobe <= 68.0) | (dist_hub <= 70.0)
    bridge_mask = (x_coords >= 140) & (x_coords <= 372) & (y_coords >= 115) & (y_coords <= 222)
    
    # Circular cutouts in wings (enlarged slightly for maximum 32px clarity)
    hole_l = dist_l_wing < 38.0
    hole_r = dist_r_wing < 38.0
    
    key_body = (wings_solid | bridge_mask | stem_mask | stem_bottom | bit_notch1 | bit_notch2 | collar_mask) & (~hole_l) & (~hole_r)
    
    # Create mask image for outline expansion
    mask_img = Image.fromarray((key_body * 255).astype(np.uint8), mode='L')
    outline_mask = mask_img.filter(ImageFilter.MaxFilter(29)) # ~14px dilation
    outline_arr = np.array(outline_mask) > 30
    
    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[outline_arr] = OUTLINE_COLOR
    
    key_indices = np.where(key_body)
    for y, x in zip(key_indices[0], key_indices[1]):
        u = (x - 100.0) / 320.0
        v = (y - 100.0) / 350.0
        diag = 0.5 * u + 0.5 * v
        
        if diag < 0.25:
            t = diag / 0.25
            r = int(255 * (1 - t) + 255 * t)
            g = int(245 * (1 - t) + 210 * t)
            b = int(125 * (1 - t) + 40 * t)
        elif diag < 0.65:
            t = (diag - 0.25) / 0.40
            r = int(255 * (1 - t) + 230 * t)
            g = int(210 * (1 - t) + 145 * t)
            b = int(40 * (1 - t) + 15 * t)
        else:
            t = min(1.0, (diag - 0.65) / 0.35)
            r = int(230 * (1 - t) + 160 * t)
            g = int(145 * (1 - t) + 85 * t)
            b = int(15 * (1 - t) + 5 * t)
            
        # Left wing highlight
        dl = dist_l_wing[y, x]
        dr = dist_r_wing[y, x]
        if y < 170 and ((125 <= x <= 165) or (350 <= x <= 385) or (240 <= x <= 270)):
            if y < 118 or (dl > 70 and y < 150) or (dr > 70 and y < 150):
                r = min(255, r + 45)
                g = min(255, g + 40)
                b = min(255, b + 60)
                
        # Stem vertical highlight
        if 231 <= x <= 245 and 210 <= y <= 440:
            r = min(255, r + 45)
            g = min(255, g + 40)
            b = min(255, b + 35)
            
        # Stem vertical shadow
        if 268 <= x <= 282 and 210 <= y <= 440:
            r = max(80, r - 50)
            g = max(45, g - 45)
            b = max(5, b - 10)
            
        rgba[y, x] = [r, g, b, 255]
        
    img = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img)
    
    # Inner rim around wing holes
    draw.ellipse([140 - 46, 165 - 46, 140 + 46, 165 + 46], outline=(31, 26, 58, 255), width=9)
    draw.ellipse([372 - 46, 165 - 46, 372 + 46, 165 + 46], outline=(31, 26, 58, 255), width=9)
    
    # Central Hub Ornament: Clockwork Heart / Emerald-Mint Power Core
    draw.ellipse([hub_x - 54, hub_y - 54, hub_x + 54, hub_y + 54], outline=(31, 26, 58, 255), width=9)
    draw.ellipse([hub_x - 49, hub_y - 49, hub_x + 49, hub_y + 49], fill=(255, 218, 55, 255))
    draw.arc([hub_x - 49, hub_y - 49, hub_x + 49, hub_y + 49], 120, 320, fill=(255, 255, 180, 255), width=6)
    
    # Glowing Mint Core (#4ED86A, #34E5C2)
    draw.ellipse([hub_x - 36, hub_y - 36, hub_x + 36, hub_y + 36], fill=(20, 130, 95, 255), outline=(31, 26, 58, 255), width=7)
    draw.ellipse([hub_x - 30, hub_y - 30, hub_x + 30, hub_y + 30], fill=(78, 216, 106, 255))
    draw.ellipse([hub_x - 24, hub_y - 26, hub_x + 18, hub_y + 18], fill=(140, 250, 180, 255))
    # Specular glint
    draw.ellipse([hub_x - 16, hub_y - 20, hub_x + 3, hub_y - 3], fill=(255, 255, 255, 250))
    
    # Collar detail on stem
    draw.rectangle([212, 288, 300, 320], outline=(31, 26, 58, 255), width=8)
    draw.line([(220, 294), (292, 294)], fill=(255, 250, 160, 230), width=5)
    draw.line([(220, 314), (292, 314)], fill=(120, 60, 5, 230), width=5)
    
    # Wing gloss sweeps
    draw.arc([140 - 78, 165 - 78, 140 + 78, 165 + 78], 180, 280, fill=(255, 255, 235, 230), width=9)
    draw.arc([372 - 78, 165 - 78, 372 + 78, 165 + 78], 190, 270, fill=(255, 255, 235, 230), width=9)
    
    return img


def create_gold_coin_master(size=512) -> Image.Image:
    """Render 512x512 Gear-Edged Gold Coin with high-contrast amber field and brilliant raised star cog."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cx, cy = size / 2.0, size / 2.0
    
    y_coords, x_coords = np.mgrid[0:size, 0:size]
    dx = x_coords - cx
    dy = y_coords - cy
    dist = np.sqrt(dx**2 + dy**2)
    angle = np.arctan2(dy, dx)
    
    # 8 Gear Cogs along perimeter
    num_teeth = 8
    r_outer = 222.0
    r_root = 178.0
    
    period = 2.0 * math.pi / num_teeth
    mod_angle = np.mod(angle + math.pi, period) / period
    
    # Crisper, bolder tooth profile
    tooth_factor = np.clip((0.26 - np.abs(mod_angle - 0.5)) * 14.0, 0.0, 1.0)
    gear_radius = r_root + (r_outer - r_root) * tooth_factor
    
    coin_mask = dist <= gear_radius
    
    mask_img = Image.fromarray((coin_mask * 255).astype(np.uint8), mode='L')
    outline_mask = mask_img.filter(ImageFilter.MaxFilter(29))
    outline_arr = np.array(outline_mask) > 30
    
    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[outline_arr] = OUTLINE_COLOR
    
    coin_indices = np.where(coin_mask)
    for y, x in zip(coin_indices[0], coin_indices[1]):
        u = (x - cx) / 222.0
        v = (y - cy) / 222.0
        diag = (u + v) * 0.5
        
        norm_diag = np.clip((diag + 0.9) / 1.8, 0.0, 1.0)
        if norm_diag < 0.3:
            t = norm_diag / 0.3
            r = int(255 * (1 - t) + 255 * t)
            g = int(250 * (1 - t) + 220 * t)
            b = int(145 * (1 - t) + 50 * t)
        elif norm_diag < 0.7:
            t = (norm_diag - 0.3) / 0.4
            r = int(255 * (1 - t) + 235 * t)
            g = int(220 * (1 - t) + 155 * t)
            b = int(50 * (1 - t) + 10 * t)
        else:
            t = (norm_diag - 0.7) / 0.3
            r = int(235 * (1 - t) + 170 * t)
            g = int(155 * (1 - t) + 95 * t)
            b = int(10 * (1 - t) + 0 * t)
            
        rgba[y, x] = [r, g, b, 255]
        
    img = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img)
    
    # Outer Gear Rim Channel
    draw.ellipse([cx - 176, cy - 176, cx + 176, cy + 176], outline=(31, 26, 58, 255), width=9)
    
    # Raised Gold Rim
    draw.ellipse([cx - 168, cy - 168, cx + 168, cy + 168], outline=(255, 235, 110, 255), width=10)
    draw.arc([cx - 168, cy - 168, cx + 168, cy + 168], 120, 330, fill=(255, 255, 220, 255), width=12)
    draw.arc([cx - 168, cy - 168, cx + 168, cy + 168], -30, 120, fill=(160, 85, 5, 255), width=12)
    
    # Recessed Inner Face (Radius 140) with DEEPER AMBER contrast:
    # Rich warm amber-bronze (#C87200 to #A65200) so the central gold star pops brilliantly!
    draw.ellipse([cx - 142, cy - 142, cx + 142, cy + 142], outline=(31, 26, 58, 255), width=8)
    
    inner_mask = dist <= 138.0
    for y in range(int(cy - 138), int(cy + 139)):
        for x in range(int(cx - 138), int(cx + 139)):
            if inner_mask[y, x]:
                u = (x - cx) / 138.0
                v = (y - cy) / 138.0
                d = (u + v) * 0.5
                # Deep rich saturated amber background
                r = int(np.clip(210 - d * 55, 140, 240))
                g = int(np.clip(125 - d * 50, 65, 170))
                b = int(np.clip(10 - d * 10, 0, 30))
                # Top edge cast shadow
                if v < -0.4:
                    r = int(r * 0.82)
                    g = int(g * 0.82)
                img.putpixel((x, y), (r, g, b, 255))
                
    draw = ImageDraw.Draw(img)
    
    # Center Emblem: High-Brightness Raised 4-point Star & Cog Hub
    # Central star polygon (scaled to r=100 outer, r=42 inner)
    star_pts = []
    r_s_outer = 100.0
    r_s_inner = 42.0
    for i in range(8):
        a = i * (math.pi / 4.0) - math.pi / 2.0
        r_pt = r_s_outer if (i % 2 == 0) else r_s_inner
        star_pts.append((cx + r_pt * math.cos(a), cy + r_pt * math.sin(a)))
        
    # Thick dark outline around star
    draw.polygon(star_pts, fill=(255, 242, 100, 255), outline=(31, 26, 58, 255))
    draw.line(star_pts + [star_pts[0]], fill=(31, 26, 58, 255), width=10)
    
    # Facets on star points: Upper-left facets are bright ivory-gold (#FFFDD0), lower-right are rich gold
    for i in range(8):
        p1 = star_pts[i]
        p2 = star_pts[(i + 1) % 8]
        if i in [6, 7, 0]: # Upper-left points
            f_col = (255, 255, 210, 255)
        elif i in [1, 5]: # Side points
            f_col = (255, 225, 75, 255)
        else: # Bottom/lower points
            f_col = (245, 185, 30, 255)
        draw.polygon([(cx, cy), p1, p2], fill=f_col)
        draw.line([(cx, cy), p1], fill=(31, 26, 58, 180), width=4)
        
    draw.line(star_pts + [star_pts[0]], fill=(31, 26, 58, 255), width=8)
    
    # Central Hub Boss
    draw.ellipse([cx - 38, cy - 38, cx + 38, cy + 38], outline=(31, 26, 58, 255), width=8)
    draw.ellipse([cx - 34, cy - 34, cx + 34, cy + 34], fill=(255, 245, 130, 255))
    draw.arc([cx - 34, cy - 34, cx + 34, cy + 34], 130, 320, fill=(255, 255, 230, 255), width=6)
    
    # Center Axle Hole
    draw.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(31, 26, 58, 255))
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(65, 52, 90, 255))
    draw.ellipse([cx - 6, cy - 8, cx + 1, cy - 1], fill=(255, 255, 255, 230))
    
    # Gloss sheen
    gloss_img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(gloss_img)
    gdraw.polygon([(90, 130), (190, 65), (135, 325), (60, 360)], fill=(255, 255, 255, 75))
    gdraw.polygon([(170, 75), (220, 50), (180, 235), (140, 255)], fill=(255, 255, 255, 50))
    
    gloss_mask = (dist <= 170.0)
    gloss_arr = np.array(gloss_img)
    gloss_arr[~gloss_mask] = 0
    img = Image.alpha_composite(img, Image.fromarray(gloss_arr, mode="RGBA"))
    
    return img


def create_stardust_gem_master(size=512) -> Image.Image:
    """Render 512x512 Stardust Gem Crystal: clean 4-pointed radiant crystal without noisy outer particles."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    cx, cy = size / 2.0, size / 2.0
    
    # Slightly larger crystal (radius 228 vertical, 196 horizontal) for high visual presence
    p_top = (cx, cy - 228.0)     # (256, 28)
    p_bot = (cx, cy + 228.0)     # (256, 484)
    p_left = (cx - 196.0, cy)    # (60, 256)
    p_right = (cx + 196.0, cy)   # (452, 256)
    
    # Inner diamond waist corners
    w_r = 78.0
    p_tl = (cx - w_r, cy - w_r)  # (178, 178)
    p_tr = (cx + w_r, cy - w_r)  # (334, 178)
    p_br = (cx + w_r, cy + w_r)  # (334, 334)
    p_bl = (cx - w_r, cy + w_r)  # (178, 334)
    
    # Central faceted jewel core corners
    c_r = 48.0
    c_top = (cx, cy - c_r - 18.0) # (256, 190)
    c_bot = (cx, cy + c_r + 18.0) # (256, 322)
    c_left = (cx - c_r, cy)       # (208, 256)
    c_right = (cx + c_r, cy)      # (304, 256)
    
    # Generate master silhouette mask
    mask_img = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask_img)
    main_poly = [p_top, p_tr, p_right, p_br, p_bot, p_bl, p_left, p_tl]
    mdraw.polygon(main_poly, fill=255)
    
    # Dilate for 16px outline
    outline_mask = mask_img.filter(ImageFilter.MaxFilter(29))
    outline_arr = np.array(outline_mask) > 30
    
    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[outline_arr] = OUTLINE_COLOR
    img = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img)
    
    # Facet layout with dopamine palette:
    # Luminous Cyan-White (#F0FDFF), Bright Sky Blue (#38A0FF), Teal-Mint (#4ED8AA), Deep Cobalt (#155998)
    facets = [
        # Upper-left apex facets (High crystalline glow)
        ([p_top, p_tl, c_top], (180, 245, 255, 255)),
        ([p_left, p_tl, c_left], (130, 230, 255, 255)),
        ([p_tl, c_top, c_left], (230, 253, 255, 255)), # Pure diamond sparkle facet
        
        # Upper-right facets (Vibrant Dopamine Sky Blue)
        ([p_top, p_tr, c_top], (70, 185, 255, 255)),
        ([p_right, p_tr, c_right], (40, 155, 255, 255)),
        ([p_tr, c_top, c_right], (140, 220, 255, 255)),
        
        # Lower-left facets (Mint-Cyan reflection)
        ([p_bl, c_bot, c_left], (78, 216, 175, 255)), # Mint-cyan (#4ED8AF)
        ([p_left, p_bl, c_left], (35, 175, 215, 255)),
        ([p_bot, p_bl, c_bot], (25, 140, 205, 255)),
        
        # Lower-right facets (Deep Cobalt shaded jewel)
        ([p_br, c_bot, c_right], (28, 115, 195, 255)),
        ([p_right, p_br, c_right], (18, 92, 172, 255)),
        ([p_bot, p_br, c_bot], (12, 75, 150, 255)),
    ]
    
    for poly, col in facets:
        draw.polygon(poly, fill=col)
        
    # Internal facet crease lines
    for poly, _ in facets:
        draw.line(poly + [poly[0]], fill=(31, 26, 58, 190), width=5)
        
    # Outer boundary crisp line
    draw.line(main_poly + [main_poly[0]], fill=(31, 26, 58, 255), width=8)
    
    # Central Luminous Core (Glowing Diamond Star Nucleus)
    center_poly = [c_top, c_right, c_bot, c_left]
    draw.polygon(center_poly, fill=(255, 255, 255, 255), outline=(31, 26, 58, 255))
    draw.line(center_poly + [center_poly[0]], fill=(31, 26, 58, 255), width=8)
    
    # Radiant inner pulse
    draw.polygon([(cx, cy - 38), (cx + 28, cy), (cx, cy + 38), (cx - 28, cy)], fill=(225, 255, 255, 255))
    draw.polygon([(cx, cy - 22), (cx + 16, cy), (cx, cy + 22), (cx - 16, cy)], fill=(255, 255, 255, 255))
    
    # Specular glint strokes along upper left facets
    draw.line([p_top, p_tl], fill=(255, 255, 255, 250), width=7)
    draw.line([p_left, p_tl], fill=(255, 255, 255, 250), width=7)
    draw.line([c_top, c_left], fill=(255, 255, 255, 250), width=6)
    
    # Starburst sparkle cross at apex (cx - 30, cy - 30)
    sparkle_cx, sparkle_cy = cx - 22.0, cy - 22.0
    draw.line([(sparkle_cx - 18, sparkle_cy), (sparkle_cx + 18, sparkle_cy)], fill=(255, 255, 255, 255), width=4)
    draw.line([(sparkle_cx, sparkle_cy - 18), (sparkle_cx, sparkle_cy + 18)], fill=(255, 255, 255, 255), width=4)
    draw.ellipse([sparkle_cx - 4, sparkle_cy - 4, sparkle_cx + 4, sparkle_cy + 4], fill=(255, 255, 255, 255))
    
    return img


def build_and_save_icons():
    print("Generating 512x512 Master Renders...")
    key_master = create_energy_key_master(512)
    coin_master = create_gold_coin_master(512)
    gem_master = create_stardust_gem_master(512)
    
    print("Downscaling to 128x128 canonical HUD icons via Lanczos...")
    key_128 = key_master.resize((128, 128), Image.Resampling.LANCZOS)
    coin_128 = coin_master.resize((128, 128), Image.Resampling.LANCZOS)
    gem_128 = gem_master.resize((128, 128), Image.Resampling.LANCZOS)
    
    key_path = f"{OUT_DIR}/icon_energy_key.png"
    coin_path = f"{OUT_DIR}/icon_gold_coin.png"
    gem_path = f"{OUT_DIR}/icon_gem_stardust.png"
    
    key_128.save(key_path, "PNG")
    coin_128.save(coin_path, "PNG")
    gem_128.save(gem_path, "PNG")
    print(f"Saved: {key_path}")
    print(f"Saved: {coin_path}")
    print(f"Saved: {gem_path}")
    
    # 32px scaled versions
    key_32 = key_128.resize((32, 32), Image.Resampling.LANCZOS)
    coin_32 = coin_128.resize((32, 32), Image.Resampling.LANCZOS)
    gem_32 = gem_128.resize((32, 32), Image.Resampling.LANCZOS)
    
    # Build comprehensive verification proof
    proof_w, proof_h = 880, 720
    proof = Image.new("RGBA", (proof_w, proof_h), (250, 248, 242, 255))
    pdraw = ImageDraw.Draw(proof)
    
    # Load font
    font_title = ImageFont.truetype(FONT_PATH, 24)
    font_sub = ImageFont.truetype(FONT_PATH, 16)
    font_hud_lbl = ImageFont.truetype(FONT_PATH, 15)
    font_hud_val = ImageFont.truetype(FONT_PATH, 17)
    font_small = ImageFont.truetype(FONT_PATH, 13)
    
    # Top banner
    pdraw.rectangle([0, 0, proof_w, 75], fill=(31, 26, 58, 255))
    pdraw.text((24, 14), "《發條之心》頂部 HUD 三資源自繪圖示（去 Emoji 化驗收）", font=font_title, fill=(255, 255, 255, 255))
    pdraw.text((24, 46), "規格：128x128 RGBA · #1F1A3A 統一描邊 · 多巴胺色盤 · 32px 高度微觀可辨識", font=font_small, fill=(200, 215, 240, 255))
    
    def draw_checker(x, y, w, h, grid=16):
        for cy in range(y, y + h, grid):
            for cx in range(x, x + w, grid):
                col = (236, 233, 226, 255) if ((cx // grid + cy // grid) % 2 == 0) else (255, 255, 255, 255)
                pdraw.rectangle([cx, cy, min(cx + grid, x + w), min(cy + grid, y + h)], fill=col)
        pdraw.rectangle([x, y, x + w, y + h], outline=(210, 205, 195, 255), width=2)
        
    # Row 1: 128x128
    y1 = 110
    labels = ["能量：發條鑰匙\nicon_energy_key.png", "金幣：齒輪金幣\nicon_gold_coin.png", "星屑：晶核星芒\nicon_gem_stardust.png"]
    icons_128 = [key_128, coin_128, gem_128]
    
    for i, (ic, lbl) in enumerate(zip(icons_128, labels)):
        bx = 55 + i * 270
        pdraw.text((bx, y1 - 25), f"標準 128x128 原始檔", font=font_sub, fill=(90, 75, 115, 255))
        draw_checker(bx, y1, 144, 144)
        proof.paste(ic, (bx + 8, y1 + 8), ic)
        pdraw.text((bx + 155, y1 + 35), lbl, font=font_small, fill=(40, 35, 55, 255))
        
    # Row 2: 64x64 & 32x32
    y2 = 300
    icons_64 = [ic.resize((64, 64), Image.Resampling.LANCZOS) for ic in icons_128]
    icons_32 = [key_32, coin_32, gem_32]
    
    pdraw.text((55, y2 - 25), "階梯縮放清晰度對比（64px 預覽 ｜ 32px 手機大廳 HUD 實際尺寸）", font=font_sub, fill=(90, 75, 115, 255))
    
    for i in range(3):
        bx = 55 + i * 270
        # 64x64
        draw_checker(bx, y2, 80, 80)
        proof.paste(icons_64[i], (bx + 8, y2 + 8), icons_64[i])
        pdraw.text((bx + 18, y2 + 84), "64px", font=font_small, fill=(130, 120, 140, 255))
        
        # 32x32
        draw_checker(bx + 115, y2 + 16, 48, 48)
        proof.paste(icons_32[i], (bx + 123, y2 + 24), icons_32[i])
        pdraw.text((bx + 125, y2 + 84), "32px", font=font_small, fill=(130, 120, 140, 255))
        
    # Row 3: Simulated Mobile Lobby Capsules (Cream background, Pill shape, Icon + Text)
    y3 = 450
    pdraw.text((55, y3 - 25), "手機大廳 HUD 實機膠囊模擬效果（粉圓體 Open-Huninn · 奶油多巴胺卡）", font=font_sub, fill=(90, 75, 115, 255))
    
    hud_bg_rect = [40, y3, proof_w - 40, y3 + 235]
    pdraw.rectangle(hud_bg_rect, fill=(244, 240, 232, 255), outline=(215, 210, 200, 255), width=2)
    
    # Sub-section title
    pdraw.text((60, y3 + 15), "【大廳頂部導航狀態列預覽】", font=font_hud_lbl, fill=(80, 70, 95, 255))
    
    capsule_specs = [
        (key_32, "能量", "15/15", (185, 120, 15)),
        (coin_32, "金幣", "8,888", (185, 120, 15)),
        (gem_32, "星屑", "30", (185, 120, 15))
    ]
    
    for i, (ic32, lbl_text, val_text, col) in enumerate(capsule_specs):
        cx = 58 + i * 260
        cy = y3 + 50
        cw, ch = 238, 54
        
        # Pill Container: Warm cream with subtle border
        pdraw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(255, 253, 248, 255), outline=(215, 205, 190, 255), width=2)
        
        # Icon 32x32 on left
        proof.paste(ic32, (cx + 12, cy + 11), ic32)
        
        # Label (能量 / 金幣 / 星屑) in warm golden-brown
        pdraw.text((cx + 54, cy + 17), lbl_text, font=font_hud_lbl, fill=col)
        
        # Value (15/15 / 8,888 / 30) in dark charcoal #1F1A3A
        pdraw.text((cx + 104, cy + 16), val_text, font=font_hud_val, fill=(35, 30, 45, 255))
        
    # Compare with Old Text-Only State (Row below)
    pdraw.text((60, y3 + 125), "【對比：修改前純文字 ERP 感膠囊（Kevin 痛點）】", font=font_small, fill=(160, 60, 60, 255))
    
    old_specs = [
        ("能量", "15/15", (185, 120, 15)),
        ("金幣", "8,888", (185, 120, 15)),
        ("星屑", "30", (185, 120, 15))
    ]
    for i, (lbl_text, val_text, col) in enumerate(old_specs):
        cx = 58 + i * 260
        cy = y3 + 155
        cw, ch = 238, 48
        pdraw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=24, fill=(255, 253, 248, 255), outline=(225, 220, 210, 255), width=1)
        pdraw.text((cx + 25, cy + 14), lbl_text, font=font_hud_lbl, fill=col)
        pdraw.text((cx + 85, cy + 13), val_text, font=font_hud_val, fill=(35, 30, 45, 255))
        
    proof_path = f"{PROOF_DIR}/proof_top_hud_three_resource_icons.png"
    proof.save(proof_path, "PNG")
    print(f"Saved verification proof: {proof_path}")
    return key_path, coin_path, gem_path, proof_path

if __name__ == "__main__":
    build_and_save_icons()
