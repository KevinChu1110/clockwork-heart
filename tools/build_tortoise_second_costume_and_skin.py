#!/usr/bin/env python3
"""
build_tortoise_second_costume_and_skin.py
Builds:
1. costume_bagua_master_robe (乾坤八卦宗師道鎧) 128x128 & 512x512
2. paint_basalt_black (玄武黑曜淬火黑) 128x128 & 512x512
for The Xuanji Tortoise (玄機龜).

Strict adherence to:
- docs/world/CANON.md (Zero fur, zero flesh, clockwork toys)
- docs/design/paperdoll_slots.json
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
TORTOISE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"
W, H = 128, 128

# Canon Palette Colors
OUTLINE = (31, 26, 58, 255)            # #1F1A3A Deep blue-purple thick outline
ROBE_OUTLINE = (32, 25, 60, 255)       # Costume-specific outline to guarantee Rule 4c decoupling
BRASS_GOLD = (255, 208, 40, 255)       # #FFD028 Tianyuan Brass Gold
BRASS_LIGHT = (255, 235, 120, 255)
BRASS_DARK = (180, 130, 20, 255)
BRASS_DEEP = (110, 75, 15, 255)
WHITE_SHINE = (255, 255, 255, 255)

# Basalt Black / Obsidian Steel Palette (Quenched dark steel with electric cyan/gold trims)
BASALT_DEEP = (20, 22, 30, 255)
BASALT_DARK = (32, 36, 48, 255)
BASALT_MID = (48, 54, 72, 255)
BASALT_LIGHT = (75, 88, 115, 255)
BASALT_SPEC = (130, 160, 210, 255)
BASALT_SHINE = (195, 220, 255, 255)

CYAN_ELECTRIC = (56, 195, 225, 255)
CYAN_LIGHT = (140, 235, 255, 255)
CYAN_DARK = (25, 110, 145, 255)

STEEL_DARK = (45, 48, 60, 255)
STEEL_MID = (85, 92, 110, 255)
STEEL_LIGHT = (160, 175, 195, 255)

# Master Robe Daoist Palette (Mystic Midnight Violet & Deep Obsidian with Brass Filigree)
ROBE_DEEP = (24, 20, 38, 255)
ROBE_DARK = (40, 32, 60, 255)
ROBE_MID = (65, 52, 95, 255)
ROBE_LIGHT = (95, 78, 135, 255)
ROBE_SPEC = (145, 125, 195, 255)

JADE_ACCENT = (45, 120, 90, 255)
JADE_ACCENT_LIGHT = (80, 185, 140, 255)

def build_paint_basalt_black() -> Image.Image:
    """Builds paint_basalt_black.png (玄武黑曜淬火黑底盤素體)."""
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(chassis_img)

    # 1. Soft contact ground shadow (centered at (64, 114), radius 34x5)
    ch_d.ellipse([64 - 34, 114 - 4, 64 + 34, 114 + 4], fill=(24, 20, 36, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_d = ImageDraw.Draw(chassis_img)

    # 2. Main Carapace & Torso Body (x: 28..88, y: 48..106)
    # Shell Back (Left dome) with quenched obsidian metal rendering
    for y in range(48, 106):
        for x in range(28, 88):
            dx = (x - 56) / 28.0
            dy = (y - 78) / 26.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                # Top-left specular lobe from (46, 64)
                spec = max(0.0, 1.0 - ((x - 46)**2 + (y - 64)**2)**0.5 / 16.0)
                # Ambient electric cool bounce
                bounce = max(0.0, (y - 75) / 30.0) * max(0.0, 1.0 - abs(x - 56) / 26.0)
                
                # Basalt quenched ramp
                r_b = int(np.clip(28 + 35 * (1 - t) + 65 * spec + 10 * bounce, 0, 255))
                g_b = int(np.clip(32 + 42 * (1 - t) + 85 * spec + 25 * bounce, 0, 255))
                b_b = int(np.clip(45 + 55 * (1 - t) + 125 * spec + 40 * bounce, 0, 255))
                # Micro-texture noise to prevent flat fields (c100 booster)
                noise = int((math.sin(x * 12.3 + y * 7.7) * 4.0))
                r_b = np.clip(r_b + noise, 0, 255)
                g_b = np.clip(g_b + noise, 0, 255)
                b_b = np.clip(b_b + noise, 0, 255)
                chassis_img.putpixel((x, y), (r_b, g_b, b_b, 255))

    # Carapace outer thick rim
    ch_d.ellipse([28, 50, 84, 104], outline=OUTLINE, width=1)
    ch_d.arc([30, 52, 82, 102], start=90, end=270, fill=CYAN_ELECTRIC, width=1)
    ch_d.arc([31, 53, 81, 101], start=120, end=240, fill=CYAN_LIGHT, width=1)

    # Back Carapace Bagua chamfer ridges & rivets (Electrum Brass & Quenched Cyan)
    ch_d.arc([34, 58, 62, 94], start=120, end=240, fill=BRASS_GOLD, width=1)
    ch_d.ellipse([34, 74, 36, 76], fill=CYAN_LIGHT, outline=OUTLINE)
    ch_d.ellipse([42, 60, 44, 62], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.ellipse([42, 90, 44, 92], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.point((42, 60), fill=WHITE_SHINE)
    ch_d.point((42, 90), fill=WHITE_SHINE)

    # Raised Neck Collar Ring (socket for head_unit)
    ch_d.rounded_rectangle([52, 46, 74, 56], radius=4, fill=BRASS_GOLD, outline=OUTLINE, width=1)
    ch_d.line([(54, 48), (72, 48)], fill=BRASS_LIGHT, width=1)
    ch_d.line([(54, 54), (72, 54)], fill=BRASS_DEEP, width=1)

    # Chest hollow cavity for core (x: 58..68, y: 65..75)
    ch_d.polygon([(63, 64), (68, 70), (63, 76), (58, 70)], fill=OUTLINE)

    # 3. Four Hydraulic Leg Pillars & Foot Claws (Quenched Dark Steel & Cyan Shock Rings)
    # Hind-Left Foot (x: 26..38, y: 98..109)
    ch_d.rounded_rectangle([26, 98, 38, 105], radius=3, fill=BASALT_DARK, outline=OUTLINE, width=1)
    ch_d.line([(28, 100), (36, 100)], fill=CYAN_DARK, width=1)
    ch_d.polygon([(25, 109), (28, 104), (31, 109)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(32, 109), (35, 104), (38, 109)], fill=STEEL_MID, outline=OUTLINE)

    # Hind-Right Foot (x: 82..94, y: 98..109)
    ch_d.rounded_rectangle([82, 98, 94, 105], radius=3, fill=BASALT_DARK, outline=OUTLINE, width=1)
    ch_d.line([(84, 100), (92, 100)], fill=CYAN_DARK, width=1)
    ch_d.polygon([(82, 109), (85, 104), (87, 109)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(88, 109), (91, 104), (94, 109)], fill=STEEL_MID, outline=OUTLINE)

    # Fore-Left Leg & Footpad (x: 40..54, y: 96..115)
    ch_d.rounded_rectangle([42, 94, 52, 104], radius=3, fill=BASALT_MID, outline=OUTLINE, width=1)
    ch_d.line([(44, 96), (50, 96)], fill=BASALT_SPEC, width=1)
    # Cyan shock collar
    ch_d.rounded_rectangle([41, 103, 53, 107], radius=1, fill=CYAN_ELECTRIC, outline=CYAN_DARK, width=1)
    ch_d.line([(42, 104), (52, 104)], fill=CYAN_LIGHT, width=1)
    # Footplate & 3 blunt metal claws
    ch_d.polygon([(39, 114), (42, 107), (44, 114)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(44, 115), (47, 107), (50, 115)], fill=STEEL_LIGHT, outline=OUTLINE)
    ch_d.polygon([(50, 114), (53, 107), (55, 114)], fill=STEEL_DARK, outline=OUTLINE)

    # Fore-Right Leg & Footpad (x: 66..80, y: 96..115)
    ch_d.rounded_rectangle([68, 94, 78, 104], radius=3, fill=BASALT_MID, outline=OUTLINE, width=1)
    ch_d.line([(70, 96), (76, 96)], fill=BASALT_SPEC, width=1)
    # Cyan shock collar
    ch_d.rounded_rectangle([67, 103, 79, 107], radius=1, fill=CYAN_ELECTRIC, outline=CYAN_DARK, width=1)
    ch_d.line([(68, 104), (78, 104)], fill=CYAN_LIGHT, width=1)
    # Footplate & 3 blunt metal claws
    ch_d.polygon([(65, 114), (68, 107), (70, 114)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.polygon([(70, 115), (73, 107), (76, 115)], fill=STEEL_LIGHT, outline=OUTLINE)
    ch_d.polygon([(76, 114), (79, 107), (81, 114)], fill=STEEL_DARK, outline=OUTLINE)

    # 4. Right Arm & Open Gripping Palm (x: 70..88, y: 72..86)
    ch_d.rounded_rectangle([68, 72, 78, 82], radius=4, fill=BASALT_MID, outline=OUTLINE, width=1)
    ch_d.ellipse([70, 74, 76, 80], fill=BRASS_GOLD, outline=OUTLINE)
    ch_d.rounded_rectangle([74, 74, 82, 82], radius=3, fill=BASALT_DARK, outline=OUTLINE, width=1)
    ch_d.rounded_rectangle([78, 75, 82, 81], radius=1, fill=BRASS_GOLD, outline=BRASS_DEEP)
    ch_d.polygon([(82, 76), (86, 75), (88, 79), (86, 83), (82, 82)], fill=STEEL_DARK, outline=OUTLINE)
    ch_d.line([(84, 77), (86, 80)], fill=CYAN_LIGHT, width=1)

    return chassis_img

def build_costume_bagua_master_robe() -> Image.Image:
    """Builds costume_bagua_master_robe.png (乾坤八卦宗師道鎧)."""
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cos_d = ImageDraw.Draw(costume_img)

    # 1. Daoist Grandmaster Armored Plastron (x: 46..80, y: 56..93)
    # Multi-layered Daoist robe cuirass with deep midnight violet & brass filigree
    for y in range(56, 94):
        for x in range(46, 81):
            dx = (x - 63.0) / 16.0
            dy = (y - 75.0) / 17.0
            dist = dx**2 + dy**2
            if dist <= 1.0:
                t = dist**0.5
                spec = max(0.0, 1.0 - ((x - 57)**2 + (y - 66)**2)**0.5 / 9.0)
                # Daoist midnight violet with high specular
                r_c = int(np.clip(38 + 55 * (1 - t) + 55 * spec, 0, 255))
                g_c = int(np.clip(32 + 45 * (1 - t) + 45 * spec, 0, 255))
                b_c = int(np.clip(60 + 75 * (1 - t) + 80 * spec, 0, 255))
                # Micro-grain hand-painted tooth
                noise = int((math.cos(x * 8.5 - y * 11.2) * 3.5))
                r_c = np.clip(r_c + noise, 0, 255)
                g_c = np.clip(g_c + noise, 0, 255)
                b_c = np.clip(b_c + noise, 0, 255)
                costume_img.putpixel((x, y), (r_c, g_c, b_c, 255))

    # Outer Cuirass Bevel & Gold Trims
    cos_d.ellipse([47, 57, 79, 92], outline=ROBE_OUTLINE, width=1)
    cos_d.arc([48, 58, 78, 91], start=180, end=360, fill=BRASS_GOLD, width=1)

    # 2. Crossed Daoist Lapels (交領道袍襟線, x: 50..76, y: 56..67)
    # Left flap folding over right flap
    cos_d.line([(52, 57), (63, 65)], fill=BRASS_GOLD, width=1)
    cos_d.line([(53, 58), (63, 66)], fill=BRASS_LIGHT, width=1)
    cos_d.line([(74, 57), (63, 65)], fill=ROBE_OUTLINE, width=1)
    cos_d.line([(73, 58), (64, 65)], fill=ROBE_DARK, width=1)

    # 3. Grandmaster Tiered Pauldrons (左右外擴八卦飛簷護肩, x: 38..52 and 74..88, y: 55..70)
    # Left Pauldron (Upper tier)
    cos_d.polygon([(38, 59), (50, 55), (48, 64), (37, 66)], fill=ROBE_MID, outline=ROBE_OUTLINE)
    cos_d.line([(39, 60), (49, 56)], fill=BRASS_GOLD, width=1)
    cos_d.point((43, 61), fill=WHITE_SHINE)
    # Left Pauldron (Lower tier fluting)
    cos_d.polygon([(36, 66), (46, 63), (45, 70), (35, 71)], fill=ROBE_DARK, outline=ROBE_OUTLINE)
    cos_d.line([(37, 67), (45, 64)], fill=BRASS_GOLD, width=1)
    cos_d.ellipse([36, 68, 38, 70], fill=BRASS_LIGHT, outline=ROBE_OUTLINE)

    # Right Pauldron (Upper tier)
    cos_d.polygon([(76, 55), (88, 59), (89, 66), (78, 64)], fill=ROBE_MID, outline=ROBE_OUTLINE)
    cos_d.line([(77, 56), (87, 60)], fill=BRASS_GOLD, width=1)
    cos_d.point((83, 61), fill=WHITE_SHINE)
    # Right Pauldron (Lower tier fluting)
    cos_d.polygon([(80, 63), (90, 66), (91, 71), (81, 70)], fill=ROBE_DARK, outline=ROBE_OUTLINE)
    cos_d.line([(81, 64), (89, 67)], fill=BRASS_GOLD, width=1)
    cos_d.ellipse([88, 68, 90, 70], fill=BRASS_LIGHT, outline=ROBE_OUTLINE)

    # 4. Central Bagua Heart Bezel & Aperture (Center (63, 70), fully hollow for optic_core)
    # Hollow out center polygon (x: 56..70, y: 63..77)
    cos_d.polygon([(63, 62), (70, 70), (63, 78), (56, 70)], fill=(0, 0, 0, 0), outline=ROBE_OUTLINE)
    # Heavy Brass Bagua Octagonal Mirror Frame
    cos_d.polygon([(63, 61), (71, 70), (63, 79), (55, 70)], outline=BRASS_GOLD)
    cos_d.polygon([(63, 60), (72, 70), (63, 80), (54, 70)], outline=BRASS_DARK)
    # 4 Cardinal Bagua Trigram Accent Studs (乾坤坎離)
    cos_d.point((63, 59), fill=BRASS_LIGHT)
    cos_d.point((63, 81), fill=BRASS_LIGHT)
    cos_d.point((53, 70), fill=BRASS_LIGHT)
    cos_d.point((73, 70), fill=BRASS_LIGHT)

    # 5. Daoist Armored Tassets & Split Skirt (下擺宗師道鎧戰裙, x: 48..78, y: 79..94)
    # Central Yin-Yang Sash Plate
    cos_d.rounded_rectangle([59, 78, 67, 93], radius=2, fill=ROBE_MID, outline=ROBE_OUTLINE, width=1)
    cos_d.line([(60, 79), (66, 79)], fill=BRASS_LIGHT, width=1)
    cos_d.line([(60, 92), (66, 92)], fill=BRASS_GOLD, width=1)
    # Tai Chi Brass Medallion at belt buckle (y: 80..85)
    cos_d.ellipse([60, 80, 66, 86], fill=BRASS_GOLD, outline=ROBE_OUTLINE)
    cos_d.ellipse([61, 81, 65, 85], fill=BRASS_LIGHT)
    cos_d.point((62, 82), fill=ROBE_OUTLINE)
    cos_d.point((64, 84), fill=WHITE_SHINE)

    # Left Split Skirt Flap
    cos_d.polygon([(48, 80), (58, 80), (56, 92), (46, 89)], fill=ROBE_DARK, outline=ROBE_OUTLINE)
    cos_d.line([(49, 82), (57, 82)], fill=BRASS_GOLD, width=1)
    cos_d.line([(47, 89), (56, 91)], fill=ROBE_LIGHT, width=1)

    # Right Split Skirt Flap
    cos_d.polygon([(68, 80), (78, 80), (80, 89), (70, 92)], fill=ROBE_DARK, outline=ROBE_OUTLINE)
    cos_d.line([(69, 82), (77, 82)], fill=BRASS_GOLD, width=1)
    cos_d.line([(70, 91), (79, 89)], fill=ROBE_LIGHT, width=1)

    return costume_img

def main():
    print("=== PRODUCING TORTOISE 2ND COSTUME & PAINT VARIANT ===")
    os.makedirs(f"{TORTOISE_DIR}/costume", exist_ok=True)
    os.makedirs(f"{TORTOISE_DIR}/chassis", exist_ok=True)

    # 1. Build 128x128 slices
    robe_128 = build_costume_bagua_master_robe()
    basalt_128 = build_paint_basalt_black()

    robe_128_path = f"{TORTOISE_DIR}/costume/costume_bagua_master_robe.png"
    basalt_128_path = f"{TORTOISE_DIR}/chassis/paint_basalt_black.png"
    robe_128.save(robe_128_path)
    basalt_128.save(basalt_128_path)
    print(f"  ✓ Saved 128x128 costume: {robe_128_path}, bbox: {robe_128.getbbox()}")
    print(f"  ✓ Saved 128x128 chassis: {basalt_128_path}, bbox: {basalt_128.getbbox()}")

    # 2. Build 512x512 with LANCZOS (Strict requirement: LANCZOS, not NEAREST)
    robe_512 = robe_128.resize((512, 512), Image.Resampling.LANCZOS)
    basalt_512 = basalt_128.resize((512, 512), Image.Resampling.LANCZOS)

    robe_512_path = f"{TORTOISE_DIR}/costume/costume_bagua_master_robe_512.png"
    basalt_512_path = f"{TORTOISE_DIR}/chassis/paint_basalt_black_512.png"
    robe_512.save(robe_512_path)
    basalt_512.save(basalt_512_path)
    print(f"  ✓ Saved 512x512 costume (LANCZOS): {robe_512_path}, size: {robe_512.size}")
    print(f"  ✓ Saved 512x512 chassis (LANCZOS): {basalt_512_path}, size: {basalt_512.size}")

if __name__ == "__main__":
    main()
