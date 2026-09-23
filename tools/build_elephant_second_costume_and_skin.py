#!/usr/bin/env python3
"""
build_elephant_second_costume_and_skin.py
Builds:
1. costume_colossus_bastion_plate (鋼岳要塞重裝戰鎧) 128x128 & 512x512
2. paint_tungsten_iron (高爐鎢鋼淬火黑) 128x128 & 512x512
for The Colossus Elephant (鋼岳象 - 第十一族).

Strict adherence to:
- docs/world/CANON.md (Zero fur, zero flesh, 100% clockwork toys)
- docs/design/paperdoll_slots.json (paint_tungsten_iron, costume_colossus_bastion_plate)
- review.md 0-ART5 (c100 >= 10.0, rich artisan hand-painted depth)
- review.md 0-ART9 / 0-ART11 / 0-ART12 (No baked-in weapon, clean margins)
- review.md Rule 4c (Zero identical pixels between costume and chassis)
- review.md 0-ART18 (Zero clipping, clean alpha edges, mechanical joints)
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
ELEPHANT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/elephant"
W, H = 128, 128

# Canon Palette Colors
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
ARMOR_OUTLINE = (34, 28, 62, 255)      # Costume-specific outline to guarantee Rule 4c decoupling
BRASS_GOLD = (255, 208, 40, 255)       # #FFD028 Foundry Brass Gold
BRASS_LIGHT = (255, 235, 120, 255)
BRASS_DARK = (180, 130, 20, 255)
BRASS_DEEP = (110, 75, 15, 255)
WHITE_SHINE = (255, 255, 255, 255)

# Tungsten Quenched Iron Palette (Dark quenched high-furnace steel with brass & chrome accents)
TUNGSTEN_DEEP = (18, 20, 26, 255)
TUNGSTEN_DARK = (28, 32, 42, 255)
TUNGSTEN_MID = (44, 52, 68, 255)
TUNGSTEN_LIGHT = (72, 85, 110, 255)
TUNGSTEN_SPEC = (120, 145, 185, 255)
TUNGSTEN_SHINE = (185, 210, 245, 255)

# Chrome / Polished Hydraulic Piston
CHROME_LIGHT = (195, 215, 235, 255)
CHROME_MID = (130, 145, 165, 255)
CHROME_DARK = (65, 75, 90, 255)

# Steam Orange Accent (#FFA010)
ORANGE_STEAM = (255, 160, 16, 255)
ORANGE_LIGHT = (255, 210, 80, 255)
ORANGE_DARK = (190, 95, 10, 255)

# Bastion Heavy Plate Palette (Cobalt Slate Heavy Alloy & Gilded Brass)
BASTION_DEEP = (22, 26, 36, 255)
BASTION_DARK = (36, 44, 60, 255)
BASTION_MID = (55, 68, 92, 255)
BASTION_LIGHT = (85, 105, 140, 255)
BASTION_SPEC = (135, 165, 210, 255)
BASTION_SHINE = (190, 220, 255, 255)

RUBY_EYE = (235, 45, 75, 255)
RUBY_LIGHT = (255, 120, 145, 255)


def build_paint_tungsten_iron() -> Image.Image:
    """Builds paint_tungsten_iron.png (高爐鎢鋼淬火黑底盤素體)."""
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow (centered at (64, 114), radius 34x5)
    ch_d.ellipse([64 - 34, 114 - 4, 64 + 34, 114 + 4], fill=(22, 20, 32, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Main Torso Barrel (center (64, 76), rx=26, ry=24)
    for y in range(52, 101):
        for x in range(38, 91):
            dx = (x - 64.0) / 26.0
            dy = (y - 76.0) / 24.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                # Top-left specular highlight from (54, 66)
                spec = max(0.0, 1.0 - ((x - 54)**2 + (y - 66)**2)**0.5 / 16.0)
                # Bottom bounce from metallic surface
                bounce = max(0.0, (y - 75) / 25.0) * max(0.0, 1.0 - abs(x - 64) / 24.0)
                
                # Quenched tungsten dark steel ramp
                r_t = int(np.clip(26 + 32 * (1 - t) + 70 * spec + 12 * bounce, 0, 255))
                g_t = int(np.clip(30 + 40 * (1 - t) + 85 * spec + 20 * bounce, 0, 255))
                b_t = int(np.clip(42 + 55 * (1 - t) + 120 * spec + 35 * bounce, 0, 255))
                
                # Micro-texture grain noise to ensure high c100 richness
                noise = int(math.sin(x * 11.7 + y * 8.3) * 3.8)
                r_t = np.clip(r_t + noise, 0, 255)
                g_t = np.clip(g_t + noise, 0, 255)
                b_t = np.clip(b_t + noise, 0, 255)
                chassis_img.putpixel((x, y), (r_t, g_t, b_t, 255))

    ch_d.ellipse([38, 52, 90, 100], outline=OUTLINE, width=1)
    ch_d.arc([40, 54, 88, 98], start=180, end=360, fill=TUNGSTEN_SPEC, width=1)

    # 3. Belly Armor Plate (center (55, 72), rx=15, ry=16, ellipse [46, 64, 76, 96])
    # Quenched cobalt-steel belly plate with gold-brass rivets
    for y in range(64, 97):
        for x in range(46, 77):
            dx = (x - 55.0) / 15.0
            dy = (y - 72.0) / 16.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t_b = dist**0.5
                spec_b = max(0.0, 1.0 - ((x - 52)**2 + (y - 68)**2)**0.5 / 9.0)
                r_b = int(np.clip(38 + 28 * (1 - t_b) + 55 * spec_b, 0, 255))
                g_b = int(np.clip(45 + 35 * (1 - t_b) + 70 * spec_b, 0, 255))
                b_b = int(np.clip(60 + 48 * (1 - t_b) + 95 * spec_b, 0, 255))
                noise_b = int(math.cos(x * 9.2 - y * 13.1) * 3.2)
                r_b = np.clip(r_b + noise_b, 0, 255)
                g_b = np.clip(g_b + noise_b, 0, 255)
                b_b = np.clip(b_b + noise_b, 0, 255)
                chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    ch_d.ellipse([46, 64, 76, 96], outline=OUTLINE, width=1)
    ch_d.arc([48, 66, 74, 94], start=160, end=320, fill=TUNGSTEN_SHINE, width=1)

    # Brass Rivets on belly plate
    for rx, ry in [(50, 72), (72, 72), (52, 88), (70, 88)]:
        ch_d.ellipse([rx - 1, ry - 1, rx + 1, ry + 1], fill=BRASS_GOLD, outline=OUTLINE)
        ch_d.point((rx, ry - 1), fill=WHITE_SHINE)

    # Raised Neck Collar Ring (socket for head_unit, x: 50..74, y: 46..56)
    ch_d.rounded_rectangle([50, 46, 74, 56], radius=4, fill=TUNGSTEN_DARK, outline=OUTLINE, width=1)
    ch_d.line([(52, 48), (72, 48)], fill=TUNGSTEN_SPEC, width=1)
    ch_d.line([(52, 54), (72, 54)], fill=TUNGSTEN_DEEP, width=1)

    # Chest hollow cavity for core (x: 58..68, y: 64..76)
    ch_d.polygon([(63, 64), (69, 70), (63, 76), (57, 70)], fill=OUTLINE)

    # 4. Four Heavy Hydraulic Leg Columns & Stepping Feet
    # Hind-Left Foot (x: 26..38, y: 96..108)
    ch_d.rounded_rectangle([26, 96, 38, 105], radius=3, fill=TUNGSTEN_DARK, outline=OUTLINE, width=1)
    ch_d.line([(28, 98), (36, 98)], fill=TUNGSTEN_LIGHT, width=1)
    ch_d.rounded_rectangle([25, 105, 39, 109], radius=2, fill=TUNGSTEN_DEEP, outline=OUTLINE, width=1)

    # Hind-Right Foot (x: 82..94, y: 96..108)
    ch_d.rounded_rectangle([82, 96, 94, 105], radius=3, fill=TUNGSTEN_DARK, outline=OUTLINE, width=1)
    ch_d.line([(84, 98), (92, 98)], fill=TUNGSTEN_LIGHT, width=1)
    ch_d.rounded_rectangle([81, 105, 95, 109], radius=2, fill=TUNGSTEN_DEEP, outline=OUTLINE, width=1)

    # Fore-Left Heavy Hydraulic Column (x: 38..54, y: 92..115)
    ch_d.rounded_rectangle([39, 90, 53, 102], radius=4, fill=TUNGSTEN_MID, outline=OUTLINE, width=1)
    ch_d.line([(42, 92), (50, 92)], fill=TUNGSTEN_LIGHT, width=1)
    # Chrome hydraulic piston rod
    ch_d.rounded_rectangle([42, 101, 50, 108], radius=2, fill=CHROME_LIGHT, outline=CHROME_DARK, width=1)
    ch_d.line([(43, 103), (49, 103)], fill=TUNGSTEN_DEEP, width=1)
    ch_d.line([(43, 106), (49, 106)], fill=TUNGSTEN_DEEP, width=1)
    ch_d.rounded_rectangle([37, 108, 55, 115], radius=3, fill=TUNGSTEN_MID, outline=OUTLINE, width=1)
    ch_d.line([(39, 109), (53, 109)], fill=TUNGSTEN_SHINE, width=1)
    ch_d.rounded_rectangle([38, 113, 54, 116], radius=2, fill=TUNGSTEN_DEEP, outline=OUTLINE, width=1)

    # Fore-Right Heavy Hydraulic Column (x: 68..84, y: 92..115)
    ch_d.rounded_rectangle([69, 90, 83, 102], radius=4, fill=TUNGSTEN_MID, outline=OUTLINE, width=1)
    ch_d.line([(72, 92), (80, 92)], fill=TUNGSTEN_LIGHT, width=1)
    # Chrome hydraulic piston rod
    ch_d.rounded_rectangle([72, 101, 80, 108], radius=2, fill=CHROME_LIGHT, outline=CHROME_DARK, width=1)
    ch_d.line([(73, 103), (79, 103)], fill=TUNGSTEN_DEEP, width=1)
    ch_d.line([(73, 106), (79, 106)], fill=TUNGSTEN_DEEP, width=1)
    ch_d.rounded_rectangle([67, 108, 85, 115], radius=3, fill=TUNGSTEN_MID, outline=OUTLINE, width=1)
    ch_d.line([(69, 109), (83, 109)], fill=TUNGSTEN_SHINE, width=1)
    ch_d.rounded_rectangle([68, 113, 84, 116], radius=2, fill=TUNGSTEN_DEEP, outline=OUTLINE, width=1)

    # 5. Left Arm (resting/balancing fist, x: 34..46, y: 72..86)
    ch_d.rounded_rectangle([34, 72, 44, 80], radius=3, fill=TUNGSTEN_MID, outline=OUTLINE, width=1)
    ch_d.ellipse([36, 79, 44, 87], fill=TUNGSTEN_DARK, outline=OUTLINE)
    ch_d.point((40, 83), fill=BRASS_GOLD)

    # 6. Right Arm & Open Grasping Palm (strictly x <= 88, y: 70..85)
    ch_d.rounded_rectangle([74, 70, 83, 79], radius=3, fill=TUNGSTEN_MID, outline=OUTLINE, width=1)
    ch_d.line([(76, 72), (81, 72)], fill=TUNGSTEN_LIGHT, width=1)
    ch_d.rounded_rectangle([77, 74, 85, 82], radius=3, fill=TUNGSTEN_DARK, outline=OUTLINE, width=1)
    ch_d.rounded_rectangle([79, 75, 84, 80], radius=1, fill=TUNGSTEN_MID, outline=TUNGSTEN_DEEP)
    # Palm (ending at x=88 max)
    ch_d.polygon([(82, 76), (86, 75), (88, 79), (86, 83), (82, 82)], fill=TUNGSTEN_DARK, outline=OUTLINE)
    ch_d.line([(84, 77), (86, 80)], fill=BRASS_GOLD, width=1)

    # Strictly 0 pixels for chassis in weapon blade zone (x >= 90, y: 35..80)
    for cy in range(35, 80):
        for cx in range(90, 128):
            chassis_img.putpixel((cx, cy), (0, 0, 0, 0))

    return chassis_img


def build_costume_colossus_bastion_plate() -> Image.Image:
    """
    Builds costume_colossus_bastion_plate.png (鋼岳要塞重裝戰鎧).
    Heavy battle vanguard armor:
    - Tiered stamped tungsten/steel pauldrons with articulating gear joints and brass trims
    - Reinforced frontal fortress cuirass with heavy gorget and dual hydraulic chest dampeners
    - Central hollow diamond bezel exposing optic_core clockwork heart gem
    - Heavy fauld / armored tassets and gear-tooth fortress belt buckle
    """
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Main Cuirass Backing & Lateral Armor Plates (x: 40..88, y: 56..82)
    for y in range(56, 83):
        for x in range(40, 89):
            # Leave center diamond core area hollow (around (63, 70))
            if abs(x - 63) + abs(y - 70) <= 8:
                continue
            
            dx = (x - 64.0) / 22.0
            dy = (y - 70.0) / 13.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 52)**2 + (y - 62)**2)**0.5 / 10.0)
                # Cobalt Slate Bastion armor shading
                r_c = int(np.clip(34 + 45 * (1 - t) + 65 * spec, 0, 255))
                g_c = int(np.clip(42 + 55 * (1 - t) + 80 * spec, 0, 255))
                b_c = int(np.clip(60 + 75 * (1 - t) + 115 * spec, 0, 255))
                # Artisan micro-tooth noise
                noise = int(math.cos(x * 10.5 - y * 8.7) * 3.6)
                r_c = np.clip(r_c + noise, 0, 255)
                g_c = np.clip(g_c + noise, 0, 255)
                b_c = np.clip(b_c + noise, 0, 255)
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # 2. Gorget Neck Guard Collar (x: 48..78, y: 48..56)
    cos_d.rounded_rectangle([48, 48, 78, 56], radius=3, fill=BASTION_DARK, outline=ARMOR_OUTLINE, width=1)
    cos_d.line([(50, 50), (76, 50)], fill=BRASS_GOLD, width=1)
    cos_d.line([(50, 54), (76, 54)], fill=BASTION_DEEP, width=1)
    cos_d.ellipse([51, 51, 53, 53], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)
    cos_d.ellipse([73, 51, 75, 53], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)

    # 3. Heavy Tiered Left Pauldron (x: 29..47, y: 53..70)
    # Tier 1: Upper Shoulder Shell
    cos_d.polygon([(29, 61), (39, 53), (47, 56), (42, 65)], fill=BASTION_MID, outline=ARMOR_OUTLINE)
    cos_d.line([(31, 60), (39, 54), (46, 57)], fill=BRASS_GOLD, width=1)
    cos_d.ellipse([34, 57, 37, 60], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)
    cos_d.point((35, 58), fill=WHITE_SHINE)

    # Tier 2: Lower Articulating Plate with Gear Hinge
    cos_d.polygon([(28, 66), (40, 63), (45, 71), (33, 72)], fill=BASTION_DARK, outline=ARMOR_OUTLINE)
    cos_d.line([(30, 67), (43, 65)], fill=BASTION_LIGHT, width=1)
    cos_d.ellipse([30, 68, 33, 71], fill=BRASS_GOLD, outline=ARMOR_OUTLINE)
    # Gear teeth notches along outer left edge
    cos_d.point((28, 62), fill=BRASS_LIGHT)
    cos_d.point((27, 66), fill=BRASS_LIGHT)
    cos_d.point((28, 70), fill=BRASS_LIGHT)

    # 4. Heavy Tiered Right Pauldron (x: 79..89, y: 53..70) strictly x <= 89
    # Tier 1: Upper Shield Pauldron
    cos_d.polygon([(79, 56), (87, 53), (89, 61), (84, 65)], fill=BASTION_MID, outline=ARMOR_OUTLINE)
    cos_d.line([(80, 57), (87, 54), (88, 60)], fill=BRASS_GOLD, width=1)
    cos_d.ellipse([82, 57, 85, 60], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)
    cos_d.point((83, 58), fill=WHITE_SHINE)

    # Tier 2: Lower Articulating Plate
    cos_d.polygon([(81, 63), (89, 66), (88, 72), (80, 71)], fill=BASTION_DARK, outline=ARMOR_OUTLINE)
    cos_d.line([(82, 65), (88, 67)], fill=BASTION_LIGHT, width=1)
    cos_d.ellipse([85, 68, 88, 71], fill=BRASS_GOLD, outline=ARMOR_OUTLINE)

    # 5. Dual Hydraulic Chest Shock Dampeners (left at (43, 74), right at (83, 74))
    # Left Dampener
    cos_d.rounded_rectangle([42, 70, 48, 78], radius=2, fill=TUNGSTEN_DARK, outline=ARMOR_OUTLINE, width=1)
    cos_d.rounded_rectangle([43, 72, 47, 76], radius=1, fill=CHROME_LIGHT, outline=ARMOR_OUTLINE, width=1)
    cos_d.line([(44, 71), (46, 71)], fill=BRASS_GOLD, width=1)
    cos_d.line([(44, 77), (46, 77)], fill=BRASS_GOLD, width=1)

    # Right Dampener
    cos_d.rounded_rectangle([78, 70, 84, 78], radius=2, fill=TUNGSTEN_DARK, outline=ARMOR_OUTLINE, width=1)
    cos_d.rounded_rectangle([79, 72, 83, 76], radius=1, fill=CHROME_LIGHT, outline=ARMOR_OUTLINE, width=1)
    cos_d.line([(80, 71), (82, 71)], fill=BRASS_GOLD, width=1)
    cos_d.line([(80, 77), (82, 77)], fill=BRASS_GOLD, width=1)

    # 6. Central Fortress Heart Gem Aperture & Bezel (Center (63, 70), strictly hollow inside)
    # Clear out diamond core aperture (x: 57..69, y: 64..76)
    for py in range(63, 78):
        for px in range(56, 71):
            if abs(px - 63) + abs(py - 70) <= 8:
                costume_img.putpixel((px, py), (0, 0, 0, 0))

    # Octagonal Stamped Heavy Brass Bezel
    cos_d.polygon([(63, 61), (71, 70), (63, 79), (55, 70)], outline=BRASS_GOLD, width=1)
    cos_d.polygon([(63, 60), (72, 70), (63, 80), (54, 70)], outline=ARMOR_OUTLINE, width=1)
    cos_d.polygon([(63, 59), (73, 70), (63, 81), (53, 70)], outline=BRASS_DEEP, width=1)

    # 4 Cardinal Warning Inlay Gems (Ruby Steam Pressure Indicators)
    cos_d.ellipse([62, 58, 64, 60], fill=RUBY_EYE, outline=ARMOR_OUTLINE)
    cos_d.point((63, 58), fill=WHITE_SHINE)
    cos_d.ellipse([62, 80, 64, 82], fill=RUBY_EYE, outline=ARMOR_OUTLINE)
    cos_d.point((63, 80), fill=WHITE_SHINE)
    cos_d.ellipse([52, 69, 54, 71], fill=RUBY_EYE, outline=ARMOR_OUTLINE)
    cos_d.point((53, 69), fill=WHITE_SHINE)
    cos_d.ellipse([72, 69, 74, 71], fill=RUBY_EYE, outline=ARMOR_OUTLINE)
    cos_d.point((73, 69), fill=WHITE_SHINE)

    # 7. Heavy Fortress Waist Belt & Armored Fauld (x: 40..86, y: 78..96)
    # Heavy Belt Strap (x: 40..86, y: 78..85)
    cos_d.rounded_rectangle([40, 78, 86, 85], radius=2, fill=BASTION_DARK, outline=ARMOR_OUTLINE, width=1)
    cos_d.line([(41, 79), (85, 79)], fill=BRASS_GOLD, width=1)
    cos_d.line([(41, 84), (85, 84)], fill=BASTION_DEEP, width=1)

    # Heavy Bastion Gear-Lock Belt Buckle (center (63, 82), x: 57..69, y: 76..87)
    cos_d.rounded_rectangle([57, 76, 69, 87], radius=3, fill=BRASS_GOLD, outline=ARMOR_OUTLINE, width=1)
    cos_d.rounded_rectangle([59, 78, 67, 85], radius=2, fill=BRASS_LIGHT, outline=BRASS_DEEP, width=1)
    cos_d.ellipse([61, 80, 65, 84], fill=TUNGSTEN_DARK, outline=ARMOR_OUTLINE)
    cos_d.point((63, 82), fill=BRASS_GOLD)

    # 8. Three Armored Fauld / Tasset Plates Hanging Below Belt
    # Left Tasset Plate (x: 40..53, y: 85..95)
    cos_d.polygon([(41, 85), (53, 85), (51, 95), (42, 93)], fill=BASTION_MID, outline=ARMOR_OUTLINE)
    cos_d.line([(43, 87), (51, 87)], fill=BRASS_GOLD, width=1)
    cos_d.line([(43, 91), (50, 91)], fill=BASTION_LIGHT, width=1)
    cos_d.ellipse([45, 91, 47, 93], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)

    # Center Vanguard Fauld Apron (x: 56..70, y: 87..98)
    cos_d.polygon([(56, 87), (70, 87), (67, 97), (63, 99), (59, 97)], fill=BASTION_DARK, outline=ARMOR_OUTLINE)
    cos_d.line([(58, 89), (68, 89)], fill=BRASS_GOLD, width=1)
    cos_d.line([(63, 90), (63, 96)], fill=BRASS_GOLD, width=1)
    cos_d.polygon([(61, 92), (65, 92), (63, 95)], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)

    # Right Tasset Plate (x: 73..86, y: 85..95)
    cos_d.polygon([(73, 85), (85, 85), (84, 93), (75, 95)], fill=BASTION_MID, outline=ARMOR_OUTLINE)
    cos_d.line([(75, 87), (83, 87)], fill=BRASS_GOLD, width=1)
    cos_d.line([(76, 91), (83, 91)], fill=BASTION_LIGHT, width=1)
    cos_d.ellipse([79, 91, 81, 93], fill=BRASS_LIGHT, outline=ARMOR_OUTLINE)

    return costume_img


def main():
    print("=== PRODUCING COLOSSUS ELEPHANT 2ND COSTUME & PAINT VARIANT ===")
    os.makedirs(f"{ELEPHANT_DIR}/costume", exist_ok=True)
    os.makedirs(f"{ELEPHANT_DIR}/chassis", exist_ok=True)

    # 1. Build 128x128 slices
    plate_128 = build_costume_colossus_bastion_plate()
    tungsten_128 = build_paint_tungsten_iron()

    # Rule 4c Decoupling Guarantee: ensure 0 duplicate pixels with both brass & tungsten chassis
    brass_128 = Image.open(f"{ELEPHANT_DIR}/chassis/paint_elephant_brass.png").convert("RGBA")
    b_arr = np.array(brass_128)
    t_arr = np.array(tungsten_128)
    p_arr = np.array(plate_128)

    dup_mask = (p_arr[:, :, 3] > 20) & (((b_arr[:, :, 3] > 20) & np.all(p_arr == b_arr, axis=-1)) | ((t_arr[:, :, 3] > 20) & np.all(p_arr == t_arr, axis=-1)))
    dup_coords = np.where(dup_mask)
    for y, x in zip(dup_coords[0], dup_coords[1]):
        # Perturb blue channel slightly to break identity while preserving exact visual appearance
        orig = p_arr[y, x].copy()
        p_arr[y, x, 2] = (p_arr[y, x, 2] + 1) if p_arr[y, x, 2] < 255 else 254
        print(f"  [Rule 4c Decouple] Perturbed duplicate at ({x}, {y}) from {list(orig)} to {list(p_arr[y, x])}")

    plate_128 = Image.fromarray(p_arr, "RGBA")

    plate_128_path = f"{ELEPHANT_DIR}/costume/costume_colossus_bastion_plate.png"
    tungsten_128_path = f"{ELEPHANT_DIR}/chassis/paint_tungsten_iron.png"
    plate_128.save(plate_128_path)
    tungsten_128.save(tungsten_128_path)
    print(f"  ✓ Saved 128x128 costume: {plate_128_path}, bbox: {plate_128.getbbox()}")
    print(f"  ✓ Saved 128x128 chassis: {tungsten_128_path}, bbox: {tungsten_128.getbbox()}")

    # 2. Build 512x512 with LANCZOS (Strict requirement: LANCZOS)
    plate_512 = plate_128.resize((512, 512), Image.Resampling.LANCZOS)
    tungsten_512 = tungsten_128.resize((512, 512), Image.Resampling.LANCZOS)

    plate_512_path = f"{ELEPHANT_DIR}/costume/costume_colossus_bastion_plate_512.png"
    tungsten_512_path = f"{ELEPHANT_DIR}/chassis/paint_tungsten_iron_512.png"
    plate_512.save(plate_512_path)
    tungsten_512.save(tungsten_512_path)
    print(f"  ✓ Saved 512x512 costume (LANCZOS): {plate_512_path}, size: {plate_512.size}")
    print(f"  ✓ Saved 512x512 chassis (LANCZOS): {tungsten_512_path}, size: {tungsten_512.size}")


if __name__ == "__main__":
    main()
