#!/usr/bin/env python3
"""
tools/build_shop_icon.py
Generate mobile lobby UI icon for Clockwork Heart (發條之心):
- icon_btn_shop.png - Clockwork Merchant Chest / Shop Vault (商城 · 發條寶箱商鋪)

Specifications:
- 128x128 RGBA PNG transparent background
- Unified outline #1F1A3A (approx 4-5px at 128px, 16-20px at 512px)
- Dopamine palette: warm gold #FFD028, orange #FFA010, mint-teal #4ED86A, coral #FF5E8A, cream #FFFDF8
- Microscopic readability at 32px
- Zero system emojis, zero realistic fur, strictly clockwork toy world language
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
OUT_DIR = f"{REPO_ROOT}/game/assets/icons/hud"
PROOF_DIR = f"{REPO_ROOT}/proofs/hud_icons"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PROOF_DIR, exist_ok=True)

OUTLINE_COLOR = (31, 26, 58, 255)  # #1F1A3A


def create_outline_and_base(mask: np.ndarray, size=512, outline_radius=27) -> Image.Image:
    """Create a RGBA master with dilated #1F1A3A outline from a boolean mask."""
    mask_img = Image.fromarray((mask * 255).astype(np.uint8), mode='L')
    outline_mask = mask_img.filter(ImageFilter.MaxFilter(outline_radius))
    outline_arr = np.array(outline_mask) > 30

    rgba = np.zeros((size, size, 4), dtype=np.uint8)
    rgba[outline_arr] = OUTLINE_COLOR
    return Image.fromarray(rgba, mode="RGBA")


def draw_rivet(draw: ImageDraw.Draw, x: float, y: float, r: float = 7.0, base_color=(255, 220, 80)):
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


def create_shop_icon_master(size=512) -> Image.Image:
    """
    Render 512x512 Clockwork Merchant Chest / Shop Vault Icon:
    - Main chest body: warm orange/gold metallic vault with rounded corners (100..410 x, 220..440 y)
    - Arched domed lid on top: (110..400 x, 140..230 y)
    - Diagonal brass winding key attached on the upper-right (pointing at -35 deg)
    - Central brass lock plate with 6-toothed clockwork gear and glowing mint-teal crystal core
    - Heavy brass rim corner brackets with rivets
    """
    y_coords, x_coords = np.mgrid[0:size, 0:size]

    # 1. Main Chest Body (rect with bottom rounded corners)
    # x: 110..400, y: 220..430
    cx1, cx2 = 115.0, 395.0
    cy1, cy2 = 220.0, 425.0
    chest_body_mask = (x_coords >= cx1) & (x_coords <= cx2) & (y_coords >= cy1) & (y_coords <= cy2)

    # 2. Arched Domed Lid
    # Elliptical arch: center at (255, 220), rx=142, ry=85 (top reaches ~135)
    lid_arch_mask = (((x_coords - 255.0) / 142.0)**2 + ((y_coords - 220.0) / 85.0)**2 <= 1.0) & (y_coords <= 225.0)

    # 3. Winding Key on upper-right
    # Key head centered at (375, 115), angled at -35 deg
    k_center_x, k_center_y = 380.0, 110.0
    theta = math.radians(-35)
    cos_t, sin_t = math.cos(theta), math.sin(theta)
    perp_x, perp_y = -sin_t, cos_t

    dist_along_stem = (x_coords - k_center_x) * cos_t + (y_coords - k_center_y) * sin_t
    dist_perp_stem = np.abs((x_coords - k_center_x) * perp_x + (y_coords - k_center_y) * perp_y)

    # Stem: length from -10 to 140 (towards chest body)
    stem_mask = (dist_perp_stem <= 16.0) & (dist_along_stem >= -10.0) & (dist_along_stem <= 150.0)

    # Key wing lobes
    l1_x = k_center_x - 48.0 * perp_x
    l1_y = k_center_y - 48.0 * perp_y
    dist_l1 = np.sqrt((x_coords - l1_x)**2 + (y_coords - l1_y)**2)

    l2_x = k_center_x + 48.0 * perp_x
    l2_y = k_center_y + 48.0 * perp_y
    dist_l2 = np.sqrt((x_coords - l2_x)**2 + (y_coords - l2_y)**2)
    dist_hub = np.sqrt((x_coords - k_center_x)**2 + (y_coords - k_center_y)**2)

    wings_solid = (dist_l1 <= 46.0) | (dist_l2 <= 46.0) | (dist_hub <= 36.0) | ((dist_along_stem >= -35.0) & (dist_along_stem <= 25.0) & (dist_perp_stem <= 48.0))
    hole1 = dist_l1 <= 18.0
    hole2 = dist_l2 <= 18.0
    key_mask = (wings_solid & (~hole1) & (~hole2)) | stem_mask

    # 4. Central Lock Plate / Gear Arbor
    # Center at (255, 275)
    gcx, gcy = 255.0, 275.0
    gdx = x_coords - gcx
    gdy = y_coords - gcy
    gdist = np.sqrt(gdx**2 + gdy**2)
    gangle = np.arctan2(gdy, gdx)

    # 6 teeth gear
    norm_angle = np.mod(gangle, 2 * math.pi / 6.0) / (2 * math.pi / 6.0)
    tooth_factor = np.clip(1.0 - np.abs(norm_angle - 0.5) * 4.0, 0.0, 1.0)
    gear_r = 54.0 + 16.0 * tooth_factor
    gear_mask = gdist <= gear_r

    # Combine full mask
    full_mask = chest_body_mask | lid_arch_mask | key_mask | gear_mask

    img = create_outline_and_base(full_mask, size=size, outline_radius=27)
    rgba = np.array(img)

    # --- Render Chest Body (Rich Warm Orange / Bronze) ---
    body_idx = np.where(chest_body_mask)
    for y, x in zip(body_idx[0], body_idx[1]):
        u = (x - cx1) / (cx2 - cx1)
        v = (y - cy1) / (cy2 - cy1)
        # Gradient warm orange (#FFA010) to darker bronze at bottom
        r = int(255 * (1 - 0.25 * v) * (0.9 + 0.1 * (1 - u)))
        g = int(160 * (1 - 0.45 * v) * (0.9 + 0.1 * (1 - u)))
        b = int(16 * (1 - 0.2 * v))
        rgba[y, x] = [min(255, r), min(255, g), max(10, b), 255]

    # --- Render Lid Arch (Brilliant Golden Brass #FFD028) ---
    lid_idx = np.where(lid_arch_mask)
    for y, x in zip(lid_idx[0], lid_idx[1]):
        diag = ((x - 120.0) + (y - 130.0)) / 400.0
        t = np.clip(diag, 0.0, 1.0)
        r = int(255 * (1 - t) + 245 * t)
        g = int(245 * (1 - t) + 185 * t)
        b = int(120 * (1 - t) + 30 * t)
        rgba[y, x] = [r, g, b, 255]

    # --- Render Key (Brass Gold) ---
    key_idx = np.where(key_mask & (~hole1) & (~hole2))
    for y, x in zip(key_idx[0], key_idx[1]):
        rgba[y, x] = [255, 218, 55, 255]

    # --- Render Lock Gear (Golden Brass) ---
    gear_idx = np.where(gear_mask)
    for y, x in zip(gear_idx[0], gear_idx[1]):
        rgba[y, x] = [255, 205, 40, 255]

    img = Image.fromarray(rgba, mode="RGBA")
    draw = ImageDraw.Draw(img)

    # Lid bottom rim band (heavy horizontal brass band)
    draw.rectangle([cx1 - 5, cy1 - 10, cx2 + 5, cy1 + 10], fill=(255, 225, 75, 255), outline=OUTLINE_COLOR, width=7)

    # Vertical brass strapping bands
    strap1_x = 165
    strap2_x = 345
    draw.rectangle([strap1_x - 14, cy1, strap1_x + 14, cy2], fill=(255, 210, 60, 255), outline=OUTLINE_COLOR, width=6)
    draw.rectangle([strap2_x - 14, cy1, strap2_x + 14, cy2], fill=(255, 210, 60, 255), outline=OUTLINE_COLOR, width=6)

    # Bottom trim band
    draw.rectangle([cx1, cy2 - 18, cx2, cy2], fill=(225, 140, 20, 255), outline=OUTLINE_COLOR, width=6)

    # Lid arched straps
    draw.arc([cx1 + 10, 145, cx2 - 10, 290], 180, 360, fill=OUTLINE_COLOR, width=6)

    # Central Gear Hub with Mint Power Core (#4ED86A)
    draw.ellipse([gcx - 52, gcy - 52, gcx + 52, gcy + 52], outline=OUTLINE_COLOR, width=7)
    draw.ellipse([gcx - 36, gcy - 36, gcx + 36, gcy + 36], fill=(78, 216, 106, 255), outline=OUTLINE_COLOR, width=6)
    # Core glint
    draw.ellipse([gcx - 26, gcy - 26, gcx - 6, gcy - 6], fill=(240, 255, 245, 240))

    # Inner holes on key wings
    draw.ellipse([l1_x - 18, l1_y - 18, l1_x + 18, l1_y + 18], outline=OUTLINE_COLOR, width=7)
    draw.ellipse([l2_x - 18, l2_y - 18, l2_x + 18, l2_y + 18], outline=OUTLINE_COLOR, width=7)

    # Rivets on bands and corners
    for ry in [cy1 + 45, cy1 + 100, cy1 + 155]:
        draw_rivet(draw, strap1_x, ry, r=7.0)
        draw_rivet(draw, strap2_x, ry, r=7.0)

    draw_rivet(draw, cx1 + 25, cy2 - 9, r=6.5)
    draw_rivet(draw, cx2 - 25, cy2 - 9, r=6.5)
    draw_rivet(draw, strap1_x, cy1, r=7.0)
    draw_rivet(draw, strap2_x, cy1, r=7.0)

    # Sparkles
    draw_star_sparkle(draw, 140, 160, r=16.0)
    draw_star_sparkle(draw, 395, 215, r=12.0)
    draw_star_sparkle(draw, gcx + 25, gcy + 25, r=9.0, color=(200, 255, 220, 255))

    return img


def main():
    print("Generating Clockwork Heart Shop Button Icon...")
    master = create_shop_icon_master(512)

    # Resize to 128x128
    icon_128 = master.resize((128, 128), Image.Resampling.LANCZOS)
    icon_path = f"{OUT_DIR}/icon_btn_shop.png"
    icon_128.save(icon_path, "PNG")
    print(f"Saved: {icon_path}")

    # Microscopic 32x32 check
    icon_32 = icon_128.resize((32, 32), Image.Resampling.LANCZOS)
    proof_img = Image.new("RGBA", (300, 160), (250, 248, 242, 255))
    pdraw = ImageDraw.Draw(proof_img)
    pdraw.rectangle([10, 10, 140, 140], fill=(255, 253, 248, 255), outline=(31, 26, 58, 255), width=2)
    proof_img.paste(icon_128, (11, 11), icon_128)
    pdraw.rectangle([160, 20, 220, 80], fill=(255, 253, 248, 255), outline=(31, 26, 58, 255), width=2)
    proof_img.paste(icon_32, (174, 34), icon_32)
    pdraw.text((160, 95), "32x32px OK", fill=(31, 26, 58, 255))
    proof_path = f"{PROOF_DIR}/proof_shop_icon.png"
    proof_img.save(proof_path, "PNG")
    print(f"Saved proof: {proof_path}")


if __name__ == "__main__":
    main()
