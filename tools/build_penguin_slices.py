#!/usr/bin/env python3
"""
build_penguin_slices.py (v2 - Clean isolation & no vector artifacts)
Definitive production script for The Steam Penguin (蒸氣企鵝, 9th Race) 7 Paperdoll Slices.
"""

import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"
KEY_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/key"
WEAPON_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/weapon"

W, H = 128, 128

OUTLINE = (31, 26, 58, 255)
NAVY_PRIMARY = (30, 58, 138, 255)
NAVY_DARK = (20, 35, 80, 255)
NAVY_LIGHT = (48, 88, 180, 255)
WHITE_PLATE = (255, 253, 248, 255)
WHITE_SHINE = (255, 255, 255, 255)
BRASS_GOLD = (255, 208, 40, 255)
BRASS_ORANGE = (255, 160, 16, 255)
BRASS_DARK = (160, 100, 15, 255)
BRASS_DEEP = (100, 60, 10, 255)
CYAN_QUARTZ = (56, 160, 255, 255)
CYAN_LIGHT = (160, 240, 255, 255)
STEEL_DARK = (55, 62, 75, 255)
STEEL_MID = (100, 112, 130, 255)
STEEL_LIGHT = (170, 185, 205, 255)

def build_slices():
    print("=== BUILDING THE STEAM PENGUIN 7 PAPERDOLL SLICES (V2 CLEAN) ===")
    master = Image.open("/tmp/penguin_aligned_flipped.png").convert("RGBA")

    # ─────────────────────────────────────────────────────────────
    # SLICE 1: WINDING KEY (Z: 5)
    # File: winding_key/key_twin_ring_helm.png
    # Location: Upper back on left (x: 8..35, y: 15..45)
    # ─────────────────────────────────────────────────────────────
    key_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(14, 46):
        for x in range(7, 36):
            p = master.getpixel((x, y))
            if not isinstance(p, tuple) or len(p) < 4: continue
            r, g, b, a = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            if a < 25: continue
            if x <= 34 and y <= 43:
                key_img.putpixel((x, y), (r, g, b, a))

    kd = ImageDraw.Draw(key_img)
    kd.line([(24, 30), (33, 40)], fill=BRASS_DEEP, width=3)
    kd.line([(25, 29), (34, 39)], fill=BRASS_ORANGE, width=2)
    kd.line([(26, 28), (35, 38)], fill=BRASS_GOLD, width=1)
    kd.point((27, 27), fill=(255, 255, 255, 255))

    kd.ellipse([10, 15, 30, 35], outline=OUTLINE, width=1)
    kd.ellipse([11, 16, 29, 34], outline=BRASS_DARK, width=1)
    kd.ellipse([12, 17, 28, 33], outline=BRASS_GOLD, width=1)
    kd.ellipse([13, 18, 27, 32], outline=BRASS_ORANGE, width=1)
    kd.ellipse([14, 19, 26, 31], outline=OUTLINE, width=1)
    kd.ellipse([16, 21, 24, 29], fill=(0, 0, 0, 0))
    kd.ellipse([18, 23, 22, 27], fill=BRASS_GOLD, outline=BRASS_DARK)
    kd.point((19, 24), fill=(255, 255, 255, 255))

    spokes = [(20, 12), (20, 38), (7, 25), (33, 25)]
    for sx, sy in spokes:
        kd.rounded_rectangle([sx-1, sy-1, sx+1, sy+1], radius=1, fill=BRASS_GOLD, outline=OUTLINE)
        kd.point((sx, sy), fill=(255, 255, 255, 255))

    # ─────────────────────────────────────────────────────────────
    # SLICE 2: BACK CURIO (Z: 8)
    # File: back_curio/curio_mini_steam_boiler.png
    # Location: Mid back on left (x: 7..34, y: 28..76)
    # Fully hand-shaded metallic brass cylinder & dome (ZERO flat fills!)
    # ─────────────────────────────────────────────────────────────
    curio_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    # 1. Base master pixels for mounting bracket & backdrop
    for y in range(40, 78):
        for x in range(6, 36):
            p = master.getpixel((x, y))
            if not isinstance(p, tuple) or len(p) < 4: continue
            r, g, b, a = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            if a < 25: continue
            if x <= 33 and 42 <= y <= 75:
                curio_img.putpixel((x, y), (r, g, b, a))

    # 2. Detailed hand-painted cylindrical boiler body (x: 12..30, y: 48..72)
    # Horizontal curvature light model with 6+ ramp steps
    for by in range(48, 73):
        for bx in range(12, 31):
            t = (bx - 12) / 18.0 # 0.0 (left) to 1.0 (right)
            # Outline borders
            if bx in (12, 30) or by == 72:
                col = OUTLINE
            elif by in (54, 64): # Riveted reinforcing bands
                if t < 0.15: col = BRASS_DARK
                elif t < 0.35: col = WHITE_SHINE
                elif t < 0.55: col = BRASS_GOLD
                elif t < 0.8: col = BRASS_ORANGE
                else: col = BRASS_DEEP
            else: # Main cylinder wall shading
                if t < 0.12: col = BRASS_DARK
                elif t < 0.22: col = BRASS_GOLD
                elif t < 0.35: col = (255, 248, 200, 255) # Specular highlight band
                elif t < 0.55: col = BRASS_ORANGE
                elif t < 0.75: col = (210, 130, 20, 255)
                elif t < 0.90: col = BRASS_DARK
                else: col = BRASS_DEEP
            curio_img.putpixel((bx, by), col)

    # Rivet heads along bands
    for ry in (54, 64):
        for rx in (14, 21, 28):
            curio_img.putpixel((rx, ry), (255, 255, 255, 255))
            curio_img.putpixel((rx+1, ry), OUTLINE)

    # 3. Spherical domed top (x: 13..29, y: 43..48)
    for dy in range(42, 49):
        for dx in range(13, 30):
            # Ellipse formula: ((dx-21)/8)^2 + ((dy-48)/6)^2 <= 1
            nx = (dx - 21.0) / 8.0
            ny = (dy - 48.0) / 6.0
            dist_sq = nx**2 + ny**2
            if dist_sq <= 1.0:
                # Dome outline
                if dist_sq >= 0.82:
                    col = OUTLINE
                else:
                    # Directional spherical highlight from top-left (approx (18, 44))
                    light_dist = ((dx - 18)**2 + (dy - 44)**2)**0.5
                    if light_dist < 2.0:
                        col = (255, 255, 255, 255)
                    elif light_dist < 4.0:
                        col = (255, 245, 180, 255)
                    elif light_dist < 6.0:
                        col = BRASS_GOLD
                    elif light_dist < 8.0:
                        col = BRASS_ORANGE
                    else:
                        col = BRASS_DARK
                curio_img.putpixel((dx, dy), col)

    # 4. Top valve & exhaust chimney pipe (x: 19..23, y: 38..42)
    cd = ImageDraw.Draw(curio_img)
    # Chimney neck
    cd.rectangle([19, 39, 23, 42], fill=BRASS_DARK, outline=OUTLINE)
    cd.line([(20, 40), (20, 42)], fill=BRASS_GOLD)
    cd.line([(21, 40), (21, 42)], fill=WHITE_SHINE)
    # Chimney rim lip
    cd.rectangle([18, 38, 24, 39], fill=BRASS_GOLD, outline=OUTLINE)
    cd.point((19, 38), fill=WHITE_SHINE)
    cd.point((20, 38), fill=WHITE_SHINE)
    cd.point((22, 38), fill=OUTLINE) # opening hole

    # 5. Pressure gauge (x: 16..25, y: 56..65) with 3D beveled bezel
    cd.ellipse([16, 56, 25, 65], fill=BRASS_DARK, outline=OUTLINE) # Bezel shadow
    cd.ellipse([17, 56, 24, 63], fill=BRASS_GOLD) # Bezel highlight
    cd.ellipse([18, 57, 23, 62], fill=WHITE_PLATE, outline=OUTLINE) # Dial face
    # Dial tick marks
    cd.point((19, 58), fill=OUTLINE)
    cd.point((22, 58), fill=OUTLINE)
    cd.point((20, 60), fill=OUTLINE) # center pivot
    cd.line([(20, 60), (22, 59)], fill=(220, 35, 35, 255), width=1) # Red indicator needle
    cd.point((18, 58), fill=(255, 255, 255, 255)) # Glass glare glint

    # 6. Volumetric Curling Steam Vapor Plume (rising from nozzle at (21, 38))
    # Soft shaded clouds with layered opacity
    steam_blobs = [
        (21, 34, 2.5, (245, 250, 255, 200)),
        (22, 30, 3.5, (235, 245, 255, 170)),
        (19, 26, 4.0, (220, 240, 255, 140)),
        (24, 23, 4.5, (210, 235, 255, 110)),
        (20, 19, 3.5, (200, 230, 255, 80)),
    ]
    for sx, sy, srad, scol in steam_blobs:
        for py in range(int(sy - srad - 1), int(sy + srad + 2)):
            for px in range(int(sx - srad - 1), int(sx + srad + 2)):
                sdist = ((px - sx)**2 + (py - sy)**2)**0.5
                if sdist <= srad:
                    alpha_factor = 1.0 - (sdist / srad)**1.5
                    final_a = int(scol[3] * alpha_factor)
                    if final_a > 15:
                        curio_img.putpixel((px, py), (scol[0], scol[1], scol[2], final_a))

    # ─────────────────────────────────────────────────────────────
    # SLICE 3: CHASSIS & PAINT SHELL (Z: 10)
    # File: chassis/paint_penguin_navy.png
    # Clean chassis: zero weapons in hand, zero key/boiler artifacts, zero yellow markers at feet
    # ─────────────────────────────────────────────────────────────
    chassis_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ch_draw = ImageDraw.Draw(chassis_img)

    # Clean Ground Contact Shadow (centered under feet at x=52, y=114, radius_x=32, radius_y=5)
    ch_draw.ellipse([52 - 32, 114 - 4, 52 + 32, 114 + 4], fill=(31, 26, 58, 140))
    chassis_img = chassis_img.filter(ImageFilter.GaussianBlur(1.4))
    ch_draw = ImageDraw.Draw(chassis_img)

    for y in range(16, 114):
        for x in range(10, 115):
            p = master.getpixel((x, y))
            if not isinstance(p, tuple) or len(p) < 4: continue
            r, g, b, a = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            if a < 25: continue

            # 1. EXCLUDE key and boiler (key is upper x <= 34, y <= 45; boiler is x <= 28, 42 <= y <= 75)
            if x <= 32 and y <= 45:
                continue
            if x <= 28 and 42 <= y <= 75:
                continue

            # 2. EXCLUDE weapon area (handled exclusively by Z:40)
            if x >= 74 and 50 <= y <= 88:
                continue

            # 3. EXCLUDE head & face (handled by Z:20 head_unit)
            if y <= 48 and x >= 46:
                continue

            # 4. EXCLUDE raw gray shadow pixels and hollow between legs
            if y >= 95:
                # White background or neutral gray shadow
                if (r > 120 and g > 120 and b > 130) or (r > 200 and g > 200 and b > 200):
                    continue
                # Gap between the two legs/feet
                if 45 <= x <= 56 and y >= 97:
                    continue
                # Outside outer bounds of feet
                if x <= 26 or x >= 78:
                    continue

            # Feet & Legs: 95 <= y <= 113
            is_feet = (95 <= y <= 113 and 25 <= x <= 78)
            # Rear body shell: x <= 48 and 48 <= y <= 95
            is_rear_body = (x <= 48 and 48 <= y <= 95)
            # Torso under-base: solid navy under costume so costume swap leaves no hole
            is_torso_base = (48 <= y <= 95 and 36 <= x <= 80)
            # Rear flipper & shoulder
            is_rear_flipper = (35 <= x <= 48 and 50 <= y <= 85)
            # Forward shoulder/arm base (excluding the weapon)
            is_fwd_arm_base = (55 <= y <= 75 and 70 <= x <= 78)

            if is_feet or is_rear_body or is_torso_base or is_rear_flipper or is_fwd_arm_base:
                if is_torso_base and not is_feet and (r > 160 and g > 150):
                    # Solid navy under-chassis base for belly region
                    chassis_img.putpixel((x, y), NAVY_PRIMARY)
                else:
                    chassis_img.putpixel((x, y), (r, g, b, a))

    # ─────────────────────────────────────────────────────────────
    # SLICE 4: HEAD UNIT (Z: 20)
    # File: head_unit/head_steam_penguin_stock.png
    # Location: Head dome, goggles frames, strap, and brass beak (x: 35..85, y: 16..54)
    # ─────────────────────────────────────────────────────────────
    head_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hd = ImageDraw.Draw(head_img)

    for y in range(15, 56):
        for x in range(34, 88):
            p = master.getpixel((x, y))
            if not isinstance(p, tuple) or len(p) < 4: continue
            r, g, b, a = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            if a < 25: continue

            # Head cap, goggles frame, strap, beak
            # Put dark lens backing socket where cyan quartz lens sits
            is_cyan_lens = (30 <= y <= 42 and 48 <= x <= 72 and r < 120 and g > 160 and b > 180)
            if is_cyan_lens:
                head_img.putpixel((x, y), (20, 30, 45, 255))
            else:
                head_img.putpixel((x, y), (r, g, b, a))

    # Subtle metallic enhancements on goggles and beak
    hd.ellipse([48, 30, 60, 42], outline=BRASS_GOLD, width=1)
    hd.ellipse([61, 30, 73, 42], outline=BRASS_GOLD, width=1)
    hd.line([(59, 35), (62, 35)], fill=BRASS_GOLD, width=2)
    hd.line([(62, 44), (76, 44)], fill=OUTLINE, width=1)
    hd.line([(63, 43), (74, 43)], fill=BRASS_GOLD, width=1)

    # ─────────────────────────────────────────────────────────────
    # SLICE 5: COSTUME (Z: 25)
    # File: costume/costume_navigator_harness.png
    # Location: Cream-white chest armor plate, bolts, navigator harness (x: 40..85, y: 48..96)
    # Clean extraction from master WITHOUT artificial vector overlay lines!
    # ─────────────────────────────────────────────────────────────
    costume_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    for y in range(46, 96):
        for x in range(40, 84):
            p = master.getpixel((x, y))
            if not isinstance(p, tuple) or len(p) < 4: continue
            r, g, b, a = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            if a < 25: continue

            # Costume breastplate and harness
            # Match white/cream plate, brass harness collar and waist belt
            is_belly_area = (48 <= y <= 94 and 42 <= x <= 82)
            if is_belly_area:
                # White plate or brass collar/belt
                if r > 130 or (r > 90 and g > 75 and b < 70):
                    costume_img.putpixel((x, y), (r, g, b, a))

    # ─────────────────────────────────────────────────────────────
    # SLICE 6: OPTIC CORE (Z: 30)
    # File: optic_core/core_cyan_quartz.png
    # Location: Glowing cyan quartz eye lenses, reflection glints, chest gem
    # ─────────────────────────────────────────────────────────────
    core_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    core_d = ImageDraw.Draw(core_img)

    # 1. Left Goggle Lens (center at 54, 36)
    for y in range(31, 42):
        for x in range(49, 60):
            dx = x - 54.5
            dy = y - 36.5
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.8:
                angle = (np.arctan2(dy, dx) + np.pi) / (2 * np.pi)
                t = dist / 4.8
                specular = max(0.0, 1.0 - ((x - 52.5)**2 + (y - 34.5)**2)**0.5 / 2.5)
                r = int(np.clip(20 + 200 * specular + 40 * (1 - t), 0, 255))
                g = int(np.clip(80 + 160 * specular + 150 * (1 - t) + 20 * np.sin(angle * 6), 0, 255))
                b = int(np.clip(140 + 115 * specular + 110 * (1 - t), 0, 255))
                a = int(np.clip(255 if dist <= 4.0 else (4.8 - dist) / 0.8 * 255, 0, 255))
                core_img.putpixel((x, y), (r, g, b, a))

    # 2. Right Goggle Lens (center at 67, 36)
    for y in range(31, 42):
        for x in range(62, 73):
            dx = x - 67.5
            dy = y - 36.5
            dist = (dx**2 + dy**2)**0.5
            if dist <= 4.8:
                angle = (np.arctan2(dy, dx) + np.pi) / (2 * np.pi)
                t = dist / 4.8
                specular = max(0.0, 1.0 - ((x - 65.5)**2 + (y - 34.5)**2)**0.5 / 2.5)
                r = int(np.clip(20 + 200 * specular + 40 * (1 - t), 0, 255))
                g = int(np.clip(80 + 160 * specular + 150 * (1 - t) + 20 * np.sin(angle * 6), 0, 255))
                b = int(np.clip(140 + 115 * specular + 110 * (1 - t), 0, 255))
                a = int(np.clip(255 if dist <= 4.0 else (4.8 - dist) / 0.8 * 255, 0, 255))
                core_img.putpixel((x, y), (r, g, b, a))

    # Specular glints
    core_d.point((52, 34), fill=(255, 255, 255, 255))
    core_d.point((53, 34), fill=(240, 250, 255, 255))
    core_d.point((65, 34), fill=(255, 255, 255, 255))
    core_d.point((66, 34), fill=(240, 250, 255, 255))

    # 3. Chest Heart Gem: Faceted rhombic luminous cyan quartz crystal at (61, 68)
    for y in range(62, 75):
        for x in range(55, 68):
            dx = abs(x - 61.0) / 5.5
            dy = abs(y - 68.0) / 5.5
            if dx + dy <= 1.0:
                t = dx + dy
                quad = (1 if x >= 61 else 0) + (2 if y >= 68 else 0)
                facet_boost = [40, 10, -20, 20][quad]
                specular = max(0.0, 1.0 - ((x - 60)**2 + (y - 66)**2)**0.5 / 2.0)
                r = int(np.clip(30 + facet_boost + 200 * specular, 0, 255))
                g = int(np.clip(120 + facet_boost + 130 * specular + 40 * (1 - t), 0, 255))
                b = int(np.clip(210 + facet_boost * 0.5 + 45 * specular, 0, 255))
                core_img.putpixel((x, y), (r, g, b, 255))

    core_d.polygon([(61, 62), (67, 68), (61, 74), (55, 68)], outline=OUTLINE)
    core_d.line([(61, 63), (61, 73)], fill=(180, 240, 255, 220))
    core_d.line([(56, 68), (66, 68)], fill=(180, 240, 255, 220))
    core_d.point((60, 66), fill=(255, 255, 255, 255))
    core_d.point((61, 66), fill=(255, 255, 255, 255))

    # ─────────────────────────────────────────────────────────────
    # SLICE 7: WEAPON (Z: 40)
    # File: weapon/wpn_twin_harpoon_gun.png
    # Clean single primary steam twin harpoon gun (x: 74..118, y: 50..86)
    # ─────────────────────────────────────────────────────────────
    weapon_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

    for y in range(48, 88):
        for x in range(74, 118):
            p = master.getpixel((x, y))
            if not isinstance(p, tuple) or len(p) < 4: continue
            r, g, b, a = int(p[0]), int(p[1]), int(p[2]), int(p[3])
            if a < 25: continue
            weapon_img.putpixel((x, y), (r, g, b, a))

    # ─────────────────────────────────────────────────────────────
    # SAVE ALL 7 SLICES AND VERIFY QUALITY METRICS
    # ─────────────────────────────────────────────────────────────
    slices = [
        ("winding_key", 5, "key_twin_ring_helm.png", key_img),
        ("back_curio", 8, "curio_mini_steam_boiler.png", curio_img),
        ("chassis", 10, "paint_penguin_navy.png", chassis_img),
        ("head_unit", 20, "head_steam_penguin_stock.png", head_img),
        ("costume", 25, "costume_navigator_harness.png", costume_img),
        ("optic_core", 30, "core_cyan_quartz.png", core_img),
        ("weapon", 40, "wpn_twin_harpoon_gun.png", weapon_img),
    ]

    print("\n--- Saving Slices and Calculating c100 ---")
    for slot_id, z, fname, im in slices:
        out_dir = f"{PENGUIN_PD_DIR}/{slot_id}"
        os.makedirs(out_dir, exist_ok=True)
        out_p = f"{out_dir}/{fname}"
        im.save(out_p)

        if slot_id == "winding_key":
            os.makedirs(KEY_DIR, exist_ok=True)
            im.save(f"{KEY_DIR}/{fname}")
        elif slot_id == "weapon":
            os.makedirs(WEAPON_DIR, exist_ok=True)
            im.save(f"{WEAPON_DIR}/{fname}")

        bbox = im.getbbox()
        assert bbox is not None, f"Slice {fname} is transparent!"
        arr = np.array(im)
        top_a = np.max(arr[0, :, 3])
        bot_a = np.max(arr[H-1, :, 3])
        left_a = np.max(arr[:, 0, 3])
        right_a = np.max(arr[:, W-1, 3])
        assert max(top_a, bot_a, left_a, right_a) < 200, f"0-ART4 failed on {fname}: border alpha too high!"

        opaque = np.sum(arr[:, :, 3] > 8)
        colors = len(set(tuple(px[:3]) for px in arr[arr[:, :, 3] > 8]))
        c100 = (colors / opaque * 100) if opaque > 0 else 0
        print(f"  ✓ {slot_id:12s} (Z:{z:2d}) -> {fname:32s} bbox={bbox} opaque={opaque:4d} cols={colors:4d} c100={c100:5.1f}")
        assert c100 >= 10.0, f"0-ART5 failed on {fname}: c100={c100:.1f} < 10.0!"

    # ─────────────────────────────────────────────────────────────
    # BUILD COMPOSITE AND PROOFS
    # ─────────────────────────────────────────────────────────────
    comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for slot_id, z, fname, im in slices:
        comp.alpha_composite(im)

    comp_p = f"{PENGUIN_PD_DIR}/proof_paperdoll_penguin_composite.png"
    comp.save(comp_p)
    print(f"\n  ✓ Composite saved to {comp_p}, bbox: {comp.getbbox()}")

    mag = Image.new("RGBA", (W, H), (255, 0, 255, 255))
    mag.alpha_composite(comp)
    mag_p = f"{PENGUIN_PD_DIR}/proof_paperdoll_penguin_magenta.png"
    mag.save(mag_p)
    print(f"  ✓ Magenta test saved to {mag_p}")

    board = Image.new("RGBA", (7 * 140 + 20, 180), (28, 24, 40, 255))
    bd = ImageDraw.Draw(board)
    for i, (slot_id, z, fname, im) in enumerate(slices):
        x = 10 + i * 140
        y = 10
        bd.rounded_rectangle([x, y, x + 128, y + 128], radius=6, fill=(45, 38, 58, 255), outline=(90, 75, 110, 255))
        board.alpha_composite(im, (x, y))
        tb = bd.textbbox((0, 0), slot_id)
        tw = tb[2] - tb[0]
        bd.text((x + (128 - tw) // 2, y + 135), slot_id, fill=(255, 215, 64, 255))

    board_p = f"{PENGUIN_PD_DIR}/proof_penguin_all_7_slices.png"
    board.save(board_p)
    print(f"  ✓ 7-slice visual board saved to {board_p}")

    crops = [
        ("verification_crop_head.png", (45, 16, 85, 54)),
        ("verification_crop_eyes.png", (48, 28, 76, 44)),
        ("verification_crop_key.png", (8, 14, 36, 44)),
        ("verification_crop_curio.png", (8, 40, 36, 75)),
        ("verification_crop_costume.png", (42, 48, 84, 94)),
        ("verification_crop_core.png", (54, 58, 70, 76)),
        ("verification_crop_weapon.png", (72, 48, 118, 88)),
        ("verification_crop_feet.png", (30, 96, 92, 122)),
    ]
    for cname, box in crops:
        c_img = comp.crop(box)
        scale_factor = max(1, 400 // max(c_img.size))
        c_large = c_img.resize((c_img.width * scale_factor, c_img.height * scale_factor), Image.Resampling.NEAREST)
        c_large.save(f"{PENGUIN_PD_DIR}/{cname}")
    print(f"  ✓ All verification crops saved to {PENGUIN_PD_DIR}")

if __name__ == "__main__":
    build_slices()
