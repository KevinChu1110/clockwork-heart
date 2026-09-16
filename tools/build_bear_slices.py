#!/usr/bin/env python3
"""
build_bear_slices.py
Production script for The Iron Bear (玄軸熊, 8th Race) 7 Paperdoll Slices.
Follows:
- docs/design/paperdoll_slots.json
- docs/design/IRON_BEAR_DESIGN_PROPOSAL.md
- docs/world/CANON.md
- art_direction.md 15-item checklist
- Review criteria 23f-1 (Warrior/Viking hammer archetype) & zero fur/organic tissue.
"""

import os
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

# Dopamine Palette & Canon Colors
OUTLINE = (31, 26, 58, 255)          # Deep blue-purple outline (#1F1A3A)
PRIMARY_AMBER = (217, 119, 36, 255)  # Caramel Amber Enamel (#D97724)
AMBER_DARK = (165, 80, 20, 255)
AMBER_LIGHT = (245, 150, 60, 255)
WHITE_PLATE = (255, 248, 231, 255)   # Cream Marble White (#FFF8E7)
WHITE_SHINE = (255, 255, 250, 255)
BRASS_GOLD = (255, 208, 40, 255)    # Tianyuan Brass (#FFD028)
BRASS_DARK = (200, 155, 25, 255)
EMERALD_MINT = (78, 216, 106, 255)  # Mint Emerald Core (#4ED86A)
EMERALD_LIGHT = (140, 245, 165, 255)
EMERALD_DARK = (30, 140, 60, 255)
DARK_IRON = (70, 75, 90, 255)
STEEL_GRAY = (140, 150, 165, 255)
OVERALLS_NAVY = (50, 60, 80, 255)   # Workshop Overalls Dark Navy (#323C50)
OVERALLS_LIGHT = (75, 90, 115, 255)

def build_all_slices():
    print("=== REFINING THE IRON BEAR 7 CANONICAL PAPERDOLL SLICES ===")
    
    base_aligned = Image.open("/tmp/bear_aligned_128.png").convert("RGBA")
    
    # ─────────────────────────────────────────────────────────────
    # SLICE 1: CHASSIS & PAINT SHELL (Z: 10)
    # File: chassis/paint_bear_amber.png
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cd = ImageDraw.Draw(chassis_img)
    
    # 1. Soft ground contact shadow (centered at (64, 120))
    cd.ellipse([64 - 28, 120 - 5, 64 + 28, 120 + 5], fill=(31, 26, 58, 130))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.6))
    cd = ImageDraw.Draw(chassis_img)
    
    # 2. Extract legs, lower torso, arms from base
    for y in range(H):
        for x in range(W):
            raw_p = base_aligned.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 30: continue
            
            is_leg_left = (88 <= y <= 121 and 38 <= x <= 62)
            is_leg_right = (88 <= y <= 121 and 64 <= x <= 88)
            is_left_arm = (56 <= y <= 84 and 28 <= x <= 46)
            is_right_arm = (56 <= y <= 84 and 74 <= x <= 92)
            
            if is_leg_left or is_leg_right or is_left_arm or is_right_arm:
                chassis_img.putpixel((x, y), (r, g, b, a))
                
    # 3. Enhance chassis details
    cd.ellipse([34, 54, 44, 64], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cd.point((37, 57), fill=WHITE_SHINE)
    cd.ellipse([80, 54, 90, 64], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cd.point((83, 57), fill=WHITE_SHINE)
    
    # Torso backing plates
    cd.rounded_rectangle([44, 56, 84, 90], radius=8, fill=PRIMARY_AMBER, outline=OUTLINE, width=1)
    cd.rounded_rectangle([50, 72, 78, 88], radius=4, fill=WHITE_PLATE, outline=OUTLINE, width=1)
    cd.line([(52, 74), (76, 74)], fill=WHITE_SHINE)
    cd.ellipse([52, 76, 54, 78], fill=BRASS_GOLD)
    cd.ellipse([74, 76, 76, 78], fill=BRASS_GOLD)
    
    # Hand clamps (clean mechanical clenched fists, zero placeholder rods)
    cd.polygon([(32, 80), (35, 76), (42, 78), (44, 84), (37, 85)], fill=DARK_IRON, outline=OUTLINE)
    cd.line([(34, 82), (36, 85)], fill=BRASS_GOLD, width=1)
    cd.polygon([(82, 78), (89, 76), (92, 82), (88, 86), (81, 83)], fill=DARK_IRON, outline=OUTLINE)
    cd.line([(86, 82), (89, 85)], fill=BRASS_GOLD, width=1)
    
    # Footplates
    cd.rounded_rectangle([40, 114, 60, 121], radius=2, fill=DARK_IRON, outline=OUTLINE, width=1)
    cd.line([(42, 115), (58, 115)], fill=WHITE_SHINE)
    cd.ellipse([43, 117, 45, 119], fill=BRASS_GOLD)
    cd.ellipse([54, 117, 56, 119], fill=BRASS_GOLD)
    cd.rounded_rectangle([66, 114, 86, 121], radius=2, fill=DARK_IRON, outline=OUTLINE, width=1)
    cd.line([(68, 115), (84, 115)], fill=WHITE_SHINE)
    cd.ellipse([69, 117, 71, 119], fill=BRASS_GOLD)
    cd.ellipse([80, 117, 82, 119], fill=BRASS_GOLD)
    
    # Brass Grounding Tail Coupler on base chassis spine
    cd.ellipse([60, 92, 68, 98], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cd.ellipse([62, 93, 66, 97], fill=BRASS_DARK)
    cd.point((63, 94), fill=WHITE_SHINE)
    print("  ✓ Chassis generated, bbox:", chassis_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: HEAD UNIT (Z: 20)
    # File: head_unit/head_iron_bear_stock.png
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)
    
    for y in range(18, 57):
        for x in range(32, 98):
            raw_p = base_aligned.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 30: continue
            
            # Skip optic eyes (Z: 30)
            is_eye = (34 <= y <= 44 and ((48 <= x <= 58) or (68 <= x <= 78)) and (g > 150 and r < 120))
            if is_eye: continue
            
            # Skip winding key area on upper left
            if x <= 36 and y <= 50 and (r > 160 and g > 130 and b < 80):
                continue
                
            # Clean up all neck/cheek stray debris:
            # 1. Any pixel with x >= 83 in y >= 45 is outside right cheek contour
            if x >= 83 and y >= 45:
                continue
            # 2. In y >= 50, right boundary should strictly be x <= 78
            if x >= 79 and y >= 50:
                continue
                
            head_img.putpixel((x, y), (r, g, b, a))
            
    # Left Ear Disc
    hd.ellipse([27, 19, 45, 37], fill=PRIMARY_AMBER, outline=OUTLINE, width=2)
    hd.ellipse([29, 21, 43, 35], outline=BRASS_GOLD, width=2)
    hd.ellipse([32, 24, 40, 32], fill=DARK_IRON, outline=OUTLINE, width=1)
    for hx in [34, 38]:
        for hy in [26, 30]:
            hd.point((hx, hy), fill=BRASS_GOLD)
    hd.point((36, 28), fill=WHITE_SHINE)
    
    # Right Ear Disc
    hd.ellipse([82, 19, 100, 37], fill=PRIMARY_AMBER, outline=OUTLINE, width=2)
    hd.ellipse([84, 21, 98, 35], outline=BRASS_GOLD, width=2)
    hd.ellipse([87, 24, 95, 32], fill=DARK_IRON, outline=OUTLINE, width=1)
    for hx in [89, 93]:
        for hy in [26, 30]:
            hd.point((hx, hy), fill=BRASS_GOLD)
    hd.point((91, 28), fill=WHITE_SHINE)
    
    # Forehead dome shine
    hd.arc([46, 20, 82, 42], start=200, end=340, fill=WHITE_SHINE, width=1)
    # Metal division line with brass dome rivets
    hd.line([(64, 20), (64, 36)], fill=OUTLINE, width=1)
    hd.ellipse([63, 24, 65, 26], fill=BRASS_GOLD)
    hd.ellipse([63, 30, 65, 32], fill=BRASS_GOLD)
    
    # Muzzle Cowl in polished cream white metal
    hd.rounded_rectangle([52, 42, 76, 56], radius=7, fill=WHITE_PLATE, outline=OUTLINE, width=2)
    hd.line([(55, 44), (73, 44)], fill=WHITE_SHINE)
    
    # Exhaust Vent Nose (with 3 vent slots)
    hd.rounded_rectangle([60, 44, 68, 50], radius=3, fill=OUTLINE, outline=OUTLINE)
    hd.line([(62, 47), (62, 49)], fill=DARK_IRON, width=1)
    hd.line([(64, 47), (64, 49)], fill=DARK_IRON, width=1)
    hd.line([(66, 47), (66, 49)], fill=DARK_IRON, width=1)
    hd.point((63, 45), fill=BRASS_GOLD)
    
    # Bear Smile Seam
    hd.line([(64, 50), (64, 53)], fill=OUTLINE, width=1)
    hd.arc([59, 50, 64, 55], start=0, end=130, fill=OUTLINE, width=1)
    hd.arc([64, 50, 69, 55], start=50, end=180, fill=OUTLINE, width=1)
    
    hd.ellipse([49, 34, 59, 44], outline=OUTLINE, width=1)
    hd.ellipse([69, 34, 79, 44], outline=OUTLINE, width=1)
    print("  ✓ Head unit generated, bbox:", head_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: WINDING KEY (Z: 5)
    # File: winding_key/key_cross_pendulum.png
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    kd = ImageDraw.Draw(key_img)
    
    kd.line([(26, 38), (40, 52)], fill=BRASS_DARK, width=4)
    kd.line([(26, 38), (40, 52)], fill=BRASS_GOLD, width=2)
    kd.line([(25, 37), (39, 51)], fill=OUTLINE, width=1)
    kd.line([(27, 39), (41, 53)], fill=OUTLINE, width=1)
    
    # Center gear hub
    kd.ellipse([21, 33, 31, 43], fill=BRASS_DARK, outline=OUTLINE, width=2)
    kd.ellipse([23, 35, 29, 41], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    kd.ellipse([25, 37, 27, 39], fill=OUTLINE)
    
    # Cross arms: N, S, W, E
    kd.line([(26, 34), (26, 26)], fill=BRASS_GOLD, width=3)
    kd.line([(25, 34), (25, 26)], fill=OUTLINE, width=1)
    kd.line([(27, 34), (27, 26)], fill=OUTLINE, width=1)
    kd.ellipse([22, 20, 30, 28], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    kd.point((24, 22), fill=WHITE_SHINE)
    
    kd.line([(26, 42), (26, 50)], fill=BRASS_GOLD, width=3)
    kd.line([(25, 42), (25, 50)], fill=OUTLINE, width=1)
    kd.line([(27, 42), (27, 50)], fill=OUTLINE, width=1)
    kd.ellipse([22, 48, 30, 56], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    kd.point((24, 50), fill=WHITE_SHINE)
    
    kd.line([(22, 38), (14, 38)], fill=BRASS_GOLD, width=3)
    kd.line([(22, 37), (14, 37)], fill=OUTLINE, width=1)
    kd.line([(22, 39), (14, 39)], fill=OUTLINE, width=1)
    kd.ellipse([8, 34, 16, 42], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    kd.point((10, 36), fill=WHITE_SHINE)
    
    kd.line([(30, 38), (38, 38)], fill=BRASS_GOLD, width=3)
    kd.line([(30, 37), (38, 37)], fill=OUTLINE, width=1)
    kd.line([(30, 39), (38, 39)], fill=OUTLINE, width=1)
    kd.ellipse([36, 34, 44, 42], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    kd.point((38, 36), fill=WHITE_SHINE)
    
    kd.ellipse([36, 50, 44, 58], fill=BRASS_DARK, outline=OUTLINE, width=1)
    kd.ellipse([38, 52, 42, 56], fill=BRASS_GOLD)
    print("  ✓ Winding key generated, bbox:", key_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: COSTUME (Z: 25)
    # File: costume/costume_ironclad_overalls.png
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cod = ImageDraw.Draw(costume_img)
    
    for y in range(60, 94):
        for x in range(42, 86):
            raw_p = base_aligned.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 30: continue
            
            # Leave window for Optic Core (x: 57..71, y: 65..77)
            if 65 <= y <= 77 and 57 <= x <= 71:
                continue
                
            if x >= 78 and y <= 84 and (r > 160 or g > 160):
                continue
                
            costume_img.putpixel((x, y), (r, g, b, a))
            
    # Straps and Buckles
    cod.polygon([(44, 58), (49, 58), (54, 68), (49, 68)], fill=OVERALLS_NAVY, outline=OUTLINE)
    cod.line([(45, 59), (50, 68)], fill=OVERALLS_LIGHT)
    cod.rectangle([48, 66, 55, 71], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cod.rectangle([50, 68, 53, 69], fill=OUTLINE)
    
    cod.polygon([(83, 58), (78, 58), (73, 68), (78, 68)], fill=OVERALLS_NAVY, outline=OUTLINE)
    cod.line([(82, 59), (77, 68)], fill=OVERALLS_LIGHT)
    cod.rectangle([72, 66, 79, 71], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cod.rectangle([74, 68, 77, 69], fill=OUTLINE)
    
    # Reinforced brass rim around core window
    cod.rounded_rectangle([56, 64, 72, 78], radius=3, outline=BRASS_GOLD, width=1)
    cod.rounded_rectangle([55, 63, 73, 79], radius=3, outline=OUTLINE, width=1)
    
    cod.line([(48, 79), (56, 79)], fill=OUTLINE, width=1)
    cod.line([(72, 79), (80, 79)], fill=OUTLINE, width=1)
    cod.ellipse([46, 80, 48, 82], fill=BRASS_GOLD)
    cod.ellipse([79, 80, 81, 82], fill=BRASS_GOLD)
    
    cod.rectangle([41, 78, 44, 86], fill=DARK_IRON, outline=OUTLINE, width=1)
    cod.ellipse([40, 76, 45, 80], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    
    cod.line([(46, 91), (82, 91)], fill=OUTLINE, width=1)
    cod.line([(46, 89), (82, 89)], fill=OVERALLS_LIGHT, width=1)
    print("  ✓ Costume generated, bbox:", costume_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: OPTIC CORE (Z: 30)
    # File: optic_core/core_emerald_lens.png
    # ─────────────────────────────────────────────────────────────
    optic_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(optic_img)
    
    # Left Mint-Emerald Eye (center 54, 39)
    od.ellipse([49, 34, 59, 44], fill=EMERALD_DARK, outline=OUTLINE, width=1)
    od.ellipse([50, 35, 58, 43], fill=EMERALD_MINT)
    od.ellipse([51, 36, 56, 41], fill=EMERALD_LIGHT)
    od.ellipse([52, 36, 54, 38], fill=WHITE_SHINE)
    od.point((55, 41), fill=EMERALD_LIGHT)
    
    # Right Mint-Emerald Eye (center 74, 39)
    od.ellipse([69, 34, 79, 44], fill=EMERALD_DARK, outline=OUTLINE, width=1)
    od.ellipse([70, 35, 78, 43], fill=EMERALD_MINT)
    od.ellipse([71, 36, 76, 41], fill=EMERALD_LIGHT)
    od.ellipse([72, 36, 74, 38], fill=WHITE_SHINE)
    od.point((75, 41), fill=EMERALD_LIGHT)
    
    # Chest Heart Gem (center 64, 71)
    od.polygon([(61, 65), (67, 65), (71, 68), (71, 74), (67, 77), (61, 77), (57, 74), (57, 68)],
               fill=BRASS_GOLD, outline=OUTLINE)
    od.polygon([(64, 66), (70, 71), (64, 76), (58, 71)], fill=EMERALD_DARK, outline=OUTLINE)
    od.polygon([(64, 67), (69, 71), (64, 75), (59, 71)], fill=EMERALD_MINT)
    od.polygon([(64, 67), (67, 70), (64, 71), (61, 70)], fill=EMERALD_LIGHT)
    od.point((63, 68), fill=WHITE_SHINE)
    od.point((64, 69), fill=WHITE_SHINE)
    print("  ✓ Optic core generated, bbox:", optic_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: WEAPON (Z: 40)
    # File: weapon/wpn_eccentric_gyro_sledge.png
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    wd = ImageDraw.Draw(weapon_img)
    
    for y in range(44, 114):
        for x in range(74, 115):
            raw_p = base_aligned.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 30: continue
            
            is_sledge_head = (44 <= y <= 80 and 80 <= x <= 114)
            is_sledge_shaft = (74 <= y <= 114 and 74 <= x <= 96 and (r > 90 or g > 80))
            if is_sledge_head or is_sledge_shaft:
                weapon_img.putpixel((x, y), (r, g, b, a))
                
    # Counterweight steel block (solid heavy war hammer face)
    wd.rounded_rectangle([82, 45, 96, 60], radius=3, fill=STEEL_GRAY, outline=OUTLINE, width=2)
    wd.line([(84, 47), (94, 47)], fill=WHITE_SHINE, width=1)
    wd.ellipse([84, 54, 87, 57], fill=BRASS_GOLD)
    wd.ellipse([91, 54, 94, 57], fill=BRASS_GOLD)
    
    # Heavy strike plate on left face of hammer
    wd.rectangle([80, 46, 83, 59], fill=DARK_IRON, outline=OUTLINE, width=1)
    
    # Eccentric Flywheel on outer right side (center (104, 56), radius 11)
    wd.ellipse([94, 46, 114, 66], fill=BRASS_DARK, outline=OUTLINE, width=2)
    wd.ellipse([96, 48, 112, 64], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    
    # Eccentric off-center axle pivot at (101, 54)
    wd.ellipse([98, 51, 104, 57], fill=DARK_IRON, outline=OUTLINE, width=1)
    wd.ellipse([99, 52, 103, 56], fill=EMERALD_MINT)
    wd.point((100, 53), fill=WHITE_SHINE)
    
    # Heavy eccentric cam lobes & balancing flywheel teeth
    wd.line([(101, 54), (110, 60)], fill=OUTLINE, width=2)
    wd.line([(101, 54), (96, 61)], fill=OUTLINE, width=2)
    wd.line([(101, 54), (107, 48)], fill=OUTLINE, width=2)
    
    # Pneumatic dampener piston cylinder under head (x: 88..98, y: 62..70)
    wd.rectangle([88, 62, 98, 69], fill=DARK_IRON, outline=OUTLINE, width=1)
    wd.line([(89, 64), (97, 64)], fill=BRASS_GOLD)
    
    # Sledge shaft knurling & end pommel
    wd.line([(86, 70), (82, 110)], fill=OUTLINE, width=4)
    wd.line([(86, 70), (82, 110)], fill=BRASS_GOLD, width=2)
    for ky in [78, 84, 90, 96, 102]:
        wd.ellipse([82, ky, 86, ky + 3], fill=DARK_IRON, outline=OUTLINE)
    wd.ellipse([79, 108, 85, 114], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    wd.point((81, 110), fill=WHITE_SHINE)
    print("  ✓ Weapon generated, bbox:", weapon_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: BACK CURIO (Z: 8)
    # File: back_curio/curio_music_honey_cask.png
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    cud = ImageDraw.Draw(curio_img)
    
    # Hovering Music Honey-Cask on upper right (x: 98..112, y: 18..36)
    cud.ellipse([98, 18, 112, 24], fill=PRIMARY_AMBER, outline=OUTLINE, width=1)
    cud.rectangle([98, 21, 112, 33], fill=AMBER_DARK, outline=OUTLINE, width=1)
    cud.ellipse([98, 30, 112, 36], fill=PRIMARY_AMBER, outline=OUTLINE, width=1)
    
    cud.line([(98, 24), (112, 24)], fill=BRASS_GOLD, width=2)
    cud.line([(98, 29), (112, 29)], fill=BRASS_GOLD, width=2)
    cud.point((100, 24), fill=WHITE_SHINE)
    cud.point((105, 24), fill=WHITE_SHINE)
    cud.point((110, 24), fill=WHITE_SHINE)
    
    # Miniature clockwork bee
    cud.ellipse([102, 14, 108, 18], fill=BRASS_GOLD, outline=OUTLINE, width=1)
    cud.line([(100, 13), (103, 15)], fill=WHITE_SHINE, width=1)
    cud.line([(107, 15), (110, 13)], fill=WHITE_SHINE, width=1)
    cud.point((105, 14), fill=EMERALD_MINT)
    
    cud.point((96, 20), fill=BRASS_GOLD)
    cud.point((94, 17), fill=EMERALD_MINT)
    cud.point((114, 22), fill=BRASS_GOLD)
    print("  ✓ Back curio generated, bbox:", curio_img.getbbox())

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES & UNIVERSAL COPIES
    # ─────────────────────────────────────────────────────────────
    canonical_slices = [
        ("winding_key", 5, "key_cross_pendulum.png", key_img),
        ("back_curio", 8, "curio_music_honey_cask.png", curio_img),
        ("chassis", 10, "paint_bear_amber.png", chassis_img),
        ("head_unit", 20, "head_iron_bear_stock.png", head_img),
        ("costume", 25, "costume_ironclad_overalls.png", costume_img),
        ("optic_core", 30, "core_emerald_lens.png", optic_img),
        ("weapon", 40, "wpn_eccentric_gyro_sledge.png", weapon_img),
    ]
    
    for slot_id, z, fname, im in canonical_slices:
        target_dir = f"{BEAR_PD_DIR}/{slot_id}"
        os.makedirs(target_dir, exist_ok=True)
        target_path = f"{target_dir}/{fname}"
        im.save(target_path)
        print(f"  ✓ Saved [{slot_id:12s}] (Z:{z:2d}) -> {target_path} (bbox: {im.getbbox()})")
        
    # Universal equipment copies
    os.makedirs(KEY_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_cross_pendulum.png")
    os.makedirs(WEAPON_DIR, exist_ok=True)
    weapon_img.save(f"{WEAPON_DIR}/wpn_eccentric_gyro_sledge.png")
    print("  ✓ Saved universal copies for key and weapon")

if __name__ == "__main__":
    build_all_slices()
