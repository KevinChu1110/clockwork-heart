#!/usr/bin/env python3
"""
build_crane_slices.py
Production tool to build the 7 canonical paperdoll slices for Cloud Crane (雲嵐鶴).
Conforms to:
- docs/design/paperdoll_slots.json
- docs/design/CLOUD_CRANE_DESIGN_PROPOSAL.md
- docs/world/CANON.md
- art_direction.md 15-item checklist
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
CRANE_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/crane"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

def create_crane_slices():
    print("=== BUILDING CLOUD CRANE 7 PAPERDOLL SLICES ===")
    
    # 1. Base master composite from center 128x128
    master = Image.open("/tmp/crane_center_128.png").convert("RGBA")
    m_arr = np.array(master)
    
    # Clean up low-alpha noise
    for y in range(H):
        for x in range(W):
            if master.getpixel((x, y))[3] < 20:
                master.putpixel((x, y), (0, 0, 0, 0))

    # ── SLICE 1: WINDING KEY (Z: 5) ──
    # File: winding_key/key_tri_wing_zephyr.png
    # Protruding on the left upper back (x: 28..46, y: 32..54)
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(30, 56):
        for x in range(26, 46):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            # Brass / dark metal winding key loop and stem
            # The head is at x >= 44 in this row, key is x <= 45
            is_key_lobe = (x <= 44 and 32 <= y <= 48 and (r > 60 or (r > 40 and g > 35)))
            is_key_stem = (36 <= x <= 45 and 44 <= y <= 54 and r > 50)
            if is_key_lobe or is_key_stem:
                key_img.putpixel((x, y), p)
    
    # Enhance winding key clarity & 3-wing propeller design
    kd = ImageDraw.Draw(key_img)
    # Winglet lobe highlight and ring
    kd.ellipse([33, 34, 43, 44], outline=(31, 26, 58, 255), width=1)
    kd.ellipse([34, 35, 42, 43], outline=(255, 208, 40, 255), width=1)
    kd.ellipse([37, 38, 39, 40], fill=(0, 0, 0, 0)) # center cutout hole
    kd.line([(38, 44), (43, 50)], fill=(210, 160, 30, 255), width=2)
    kd.line([(37, 44), (42, 50)], fill=(31, 26, 58, 255), width=1)
    print("  ✓ Winding key generated, bbox:", key_img.getbbox())

    # ── SLICE 2: BACK CURIO (Z: 8) ──
    # File: back_curio/curio_origami_crane.png
    # Floating clockwork origami crane at upper left (x: 12..38, y: 22..44)
    # + articulated crane tail feather foil at lower back (x: 36..52, y: 74..94)
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    # Place scaled hovering origami crane
    origami_raw = Image.open("/tmp/origami_crane_raw.png").convert("RGBA")
    origami_scaled = origami_raw.resize((26, 20), Image.Resampling.LANCZOS)
    curio_img.paste(origami_scaled, (12, 22), origami_scaled)
    
    # Tail feather vanes (behind lower torso Z: 8)
    for y in range(74, 96):
        for x in range(36, 54):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            # Metallic silver / grey rear tail vanes
            is_tail_vane = (x <= 50 and 76 <= y <= 94 and (100 < r < 230 and 100 < g < 230 and 120 < b < 245))
            if is_tail_vane:
                curio_img.putpixel((x, y), p)
    print("  ✓ Back curio generated, bbox:", curio_img.getbbox())

    # ── SLICE 6: WEAPON (Z: 40) ──
    # File: weapon/wpn_zephyr_wing_bow.png
    # Zephyr Wing Compound Bow on right side (x: 78..106, y: 48..112)
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    # Bow upper blade, cams, pulleys, riser, lower limb
    for y in range(48, 102):
        for x in range(78, 107):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 20: continue
            p = (r, g, b, a)
            is_bow_upper = (y <= 78 and x >= 94)
            is_bow_tip = (y <= 62 and x >= 90)
            is_joint = (76 <= y <= 85 and 91 <= x <= 98)
            is_lower = (y >= 84 and 80 <= x <= 93)
            is_grip = (80 <= y <= 85 and 81 <= x <= 91)
            if is_bow_upper or is_bow_tip or is_joint or is_lower or is_grip:
                weapon_img.putpixel((x, y), p)
    
    # Refine bow with crisp tungsten wire bowstring & brass cams
    wd = ImageDraw.Draw(weapon_img)
    # Upper pulley cam at (99, 54)
    wd.ellipse([97, 52, 103, 58], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255))
    # Lower pulley cam at (82, 94)
    wd.ellipse([80, 92, 86, 98], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255))
    # High-tension tungsten wire bowstring
    wd.line([(98, 56), (82, 94)], fill=(220, 230, 245, 220), width=1)
    print("  ✓ Weapon generated, bbox:", weapon_img.getbbox())

    # ── SLICE 5: OPTIC CORE (Z: 30) ──
    # File: optic_core/core_vermilion_lens.png
    # Vermilion red rangefinder eyes + amber jaw LED + cyan chest heart core
    optic_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    # Red rangefinder eyes (y in [33..43], x in [61..77])
    for y in range(32, 44):
        for x in range(60, 78):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            # Vermilion red eyes: R > 150, G < 90, B < 90
            if r > 140 and g < 90 and b < 90:
                optic_img.putpixel((x, y), p)
                
    # Chest Clockwork Heart Gem (cyan/azure jewel, y in [58..72], x in [56..72])
    for y in range(58, 74):
        for x in range(56, 72):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            # Cyan gem: B > 160, G > 160, R < 120
            if b > 150 and g > 150 and r < 130:
                optic_img.putpixel((x, y), p)

    # Polish optic core features
    od = ImageDraw.Draw(optic_img)
    # Left eye lens (around 64, 38)
    od.ellipse([63, 36, 67, 40], fill=(255, 60, 90, 255), outline=(180, 20, 40, 255))
    od.point((64, 37), fill=(255, 220, 230, 255)) # specular highlight
    # Right eye lens (around 73, 38)
    od.ellipse([72, 36, 76, 40], fill=(255, 60, 90, 255), outline=(180, 20, 40, 255))
    od.point((73, 37), fill=(255, 220, 230, 255)) # specular highlight
    # Chest heart gem (around 64, 65)
    od.polygon([(64, 62), (68, 66), (64, 71), (60, 66)], fill=(56, 160, 255, 255), outline=(255, 208, 40, 255))
    od.point((63, 64), fill=(200, 240, 255, 255)) # gem facet shine
    print("  ✓ Optic core generated, bbox:", optic_img.getbbox())

    # ── SLICE 4: COSTUME (Z: 25) ──
    # File: costume/costume_zephyr_robe.png
    # Zephyr Wind-Walker Robe (tunic, belt, flaps, crossover lapel)
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(52, 95):
        for x in range(42, 86):
            # Skip chest core (optic core Z: 30)
            if optic_img.getpixel((x, y))[3] > 50:
                continue
            # Skip weapon area
            if weapon_img.getpixel((x, y))[3] > 50:
                continue
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            # The robe consists of blue panels (#38A0FF), white tunic panels, navy belt/borders
            # Exclude exposed arm/hand (x >= 75 and y >= 66)
            is_arm_hand = (x >= 75 and 66 <= y <= 78 and r > 160 and g > 160 and b > 160)
            if not is_arm_hand:
                costume_img.putpixel((x, y), p)

    # Frame chest opening for optic core
    cd = ImageDraw.Draw(costume_img)
    # Gold Tianyuan button on lapel at (60, 60)
    cd.ellipse([58, 59, 61, 62], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255))
    # Belt clasp at (64, 76)
    cd.rectangle([62, 75, 66, 78], fill=(255, 208, 40, 255), outline=(31, 26, 58, 255))
    print("  ✓ Costume generated, bbox:", costume_img.getbbox())

    # ── SLICE 3: HEAD UNIT (Z: 20) ──
    # File: head_unit/head_cloud_crane_stock.png
    # Cranium dome, octagonal red crest valve, titanium tweezer beak, bellows neck collar, ear dial
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(11, 57):
        for x in range(40, 86):
            # Skip winding key (Z: 5)
            if key_img.getpixel((x, y))[3] > 50:
                continue
            # Skip optic eyes (Z: 30)
            if optic_img.getpixel((x, y))[3] > 50:
                continue
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            head_img.putpixel((x, y), p)

    # Polish octagonal crest relief valve atop head (y: 11..19, x: 60..68)
    hd = ImageDraw.Draw(head_img)
    # Brass base flange at (61..67, 19..21)
    hd.rectangle([60, 18, 68, 21], fill=(210, 160, 30, 255), outline=(31, 26, 58, 255))
    # Octagonal vermilion valve cap
    hd.polygon([(62, 12), (66, 12), (68, 14), (68, 17), (66, 19), (62, 19), (60, 17), (60, 14)], 
               fill=(255, 70, 90, 255), outline=(180, 20, 40, 255))
    hd.line([(62, 13), (66, 13)], fill=(255, 170, 180, 255)) # top bevel shine
    
    # Titanium tweezer beak mechanical seam line at (70..83, 44..46)
    hd.line([(70, 45), (82, 45)], fill=(31, 26, 58, 255), width=1)
    hd.line([(70, 46), (82, 46)], fill=(160, 175, 190, 255), width=1)
    
    # Ear dial with brass rim at (44, 38)
    hd.ellipse([43, 36, 48, 41], fill=(210, 160, 30, 255), outline=(31, 26, 58, 255))
    
    # Recessed eye sockets underneath where optic core will sit
    hd.ellipse([62, 35, 68, 41], outline=(31, 26, 58, 255))
    hd.ellipse([71, 35, 77, 41], outline=(31, 26, 58, 255))
    print("  ✓ Head unit generated, bbox:", head_img.getbbox())

    # ── SLICE 1: CHASSIS & PAINT SHELL (Z: 10) ──
    # File: chassis/paint_crane_porcelain.png
    # Full body automaton skeleton, limbs, ball joints, springs, 3-toed titanium feet + soft ground shadow
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    # 1. Soft ground contact shadow
    s_draw = ImageDraw.Draw(chassis_img)
    s_draw.ellipse([64 - 26, 120 - 5, 64 + 26, 120 + 5], fill=(31, 26, 58, 120))
    # Gaussian blur the shadow
    shadow_layer = chassis_img.copy().filter(ImageFilter.GaussianBlur(1.8))
    chassis_img = shadow_layer

    # 2. Legs, knees, springs, pistons, and feet (y in [80..122], x in [40..80])
    for y in range(80, 123):
        for x in range(40, 80):
            raw_p = master.getpixel((x, y))
            if not isinstance(raw_p, tuple) or len(raw_p) < 4: continue
            r, g, b, a = int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])
            if a < 25: continue
            p = (r, g, b, a)
            # If costume covers the upper thighs, keep chassis legs
            chassis_img.putpixel((x, y), p)

    # 3. Arms and hands (x: 34..50 on left, x: 74..84 on right)
    for y in range(54, 82):
        for x in range(34, 50): # left arm
            raw_p = master.getpixel((x, y))
            if isinstance(raw_p, tuple) and len(raw_p) >= 4 and int(raw_p[3]) >= 25:
                chassis_img.putpixel((x, y), (int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])))
        for x in range(74, 85): # right arm/sleeve
            raw_p = master.getpixel((x, y))
            if isinstance(raw_p, tuple) and len(raw_p) >= 4 and int(raw_p[3]) >= 25:
                chassis_img.putpixel((x, y), (int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])))

    # Natural clenched fist at y: 81..84, x: 80..84
    for y in range(81, 85):
        for x in range(80, 85):
            raw_p = master.getpixel((x, y))
            if isinstance(raw_p, tuple) and len(raw_p) >= 4 and int(raw_p[3]) >= 20:
                chassis_img.putpixel((x, y), (int(raw_p[0]), int(raw_p[1]), int(raw_p[2]), int(raw_p[3])))

    # 4. Underlying torso and neck support (so removing costume leaves a complete chassis)
    ch_draw = ImageDraw.Draw(chassis_img)
    # Torso base shell in cold porcelain white (#F5F7FA) and cobalt blue (#38A0FF)
    ch_draw.rounded_rectangle([52, 54, 76, 80], radius=5, fill=(245, 247, 250, 255), outline=(31, 26, 58, 255))
    # Chest center panel
    ch_draw.rectangle([56, 58, 72, 72], fill=(56, 160, 255, 255), outline=(31, 26, 58, 255))
    # Brass waist ball joint
    ch_draw.ellipse([58, 76, 70, 84], fill=(210, 160, 30, 255), outline=(31, 26, 58, 255))
    # Shoulder ball joints
    ch_draw.ellipse([44, 55, 52, 63], fill=(210, 160, 30, 255), outline=(31, 26, 58, 255))
    ch_draw.ellipse([74, 57, 82, 65], fill=(210, 160, 30, 255), outline=(31, 26, 58, 255))
    
    # Crisp outline for bare right fist
    ch_draw.line([(80, 84), (83, 84)], fill=(31, 26, 58, 255))
    ch_draw.line([(84, 81), (84, 83)], fill=(31, 26, 58, 255))

    # Titanium talons reinforcement
    ch_draw.line([(48, 120), (43, 121)], fill=(31, 26, 58, 255), width=2)
    ch_draw.line([(52, 120), (52, 122)], fill=(31, 26, 58, 255), width=2)
    ch_draw.line([(56, 120), (61, 121)], fill=(31, 26, 58, 255), width=2)
    ch_draw.line([(70, 120), (65, 121)], fill=(31, 26, 58, 255), width=2)
    ch_draw.line([(75, 120), (75, 122)], fill=(31, 26, 58, 255), width=2)
    ch_draw.line([(79, 120), (84, 121)], fill=(31, 26, 58, 255), width=2)

    print("  ✓ Chassis generated, bbox:", chassis_img.getbbox())

    # ── SAVE ALL 7 SLICES ──
    slices = [
        ("winding_key", "key_tri_wing_zephyr.png", key_img),
        ("back_curio", "curio_origami_crane.png", curio_img),
        ("chassis", "paint_crane_porcelain.png", chassis_img),
        ("head_unit", "head_cloud_crane_stock.png", head_img),
        ("costume", "costume_zephyr_robe.png", costume_img),
        ("optic_core", "core_vermilion_lens.png", optic_img),
        ("weapon", "wpn_zephyr_wing_bow.png", weapon_img),
    ]

    for slot_id, fname, img in slices:
        slot_dir = f"{CRANE_PD_DIR}/{slot_id}"
        os.makedirs(slot_dir, exist_ok=True)
        path = f"{slot_dir}/{fname}"
        img.save(path)
        print(f"Saved: {path} (bbox: {img.getbbox()})")

    # Also save universal copies for key and weapon
    os.makedirs(KEY_DIR, exist_ok=True)
    key_img.save(f"{KEY_DIR}/key_tri_wing_zephyr.png")
    os.makedirs(WEAPON_DIR, exist_ok=True)
    weapon_img.save(f"{WEAPON_DIR}/wpn_zephyr_wing_bow.png")
    print("  ✓ Saved universal key and weapon copies")

if __name__ == "__main__":
    create_crane_slices()
