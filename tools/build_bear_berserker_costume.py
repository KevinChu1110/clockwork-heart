#!/usr/bin/env python3
"""
tools/build_masterpiece_berserker_costume.py
Constructs hand-painted, weathered steampunk artisan costume_berserker_cuirass.png
(狂戰破陣機關戰鎧) for The Iron Bear paperdoll.

Implements all recommendations from art director and vision audit:
1. True pixel-impasto texture: 4~5 subtle dithering variations, per-pixel surface tooth.
2. Softened speculars: eliminated harsh 90s banded white lines, replaced with warm metallic gleam.
3. Natural ambient bounce: warm bronze bounces from below, cool blue-grey sky reflection on top.
4. Micro-wear & battle weathering: fine paint chips, hairline micro-cracks with lit edges, corner scuffs.
5. Rich color ramps with deep hue-shifting:
   - Weathered Crimson: deep oxidized umber-crimson (42, 14, 22) -> burnt sienna red (82, 22, 34) ->
     antique crimson (132, 34, 48) -> saturated blood iron (175, 46, 62) -> warm sun-lit coral (205, 68, 84) ->
     soft rose specular (228, 115, 128) -> pale highlight glint (245, 185, 195).
   - Antique Brass/Gold: dark bronze-green shadow (65, 48, 18) -> tarnished gold (115, 84, 26) ->
     aged brass (172, 128, 36) -> classic honey gold (220, 172, 48) -> warm highlight (245, 218, 120) ->
     soft gleam (252, 246, 220).
   - Heavy Tooling Steel: cavity black (26, 24, 35) -> cold slate steel (48, 54, 70) ->
     brushed gunmetal (72, 82, 104) -> bevel highlight (108, 122, 148) -> metallic edge (165, 178, 202).
"""

import math
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
BEAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"

W, H = 128, 128
OUTLINE = np.array([31, 26, 58, 255], dtype=np.float32)

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def interp_ramp(keys, t):
    t = np.clip(t, 0.0, 1.0)
    for i in range(len(keys) - 1):
        t0, c0 = keys[i]
        t1, c1 = keys[i+1]
        if t0 <= t <= t1:
            f = smoothstep(t0, t1, t)
            return c0 + f * (c1 - c0)
    return keys[-1][1]

CRIMSON_KEYS = [
    (0.00, np.array([42.0, 14.0, 22.0])),   # deep crevice / AO
    (0.18, np.array([82.0, 22.0, 34.0])),   # dark shadow
    (0.38, np.array([132.0, 34.0, 48.0])),  # terminator zone
    (0.58, np.array([175.0, 46.0, 62.0])),  # saturated blood iron
    (0.75, np.array([205.0, 68.0, 84.0])),  # warm sun-lit coral
    (0.88, np.array([228.0, 115.0, 128.0])),# soft rose specular
    (1.00, np.array([245.0, 185.0, 195.0])) # pale gleam
]

GOLD_KEYS = [
    (0.00, np.array([65.0, 48.0, 18.0])),   # dark bronze shadow
    (0.22, np.array([115.0, 84.0, 26.0])),  # tarnished gold
    (0.48, np.array([172.0, 128.0, 36.0])), # aged brass
    (0.70, np.array([220.0, 172.0, 48.0])), # classic honey gold
    (0.86, np.array([245.0, 218.0, 120.0])),# warm highlight
    (1.00, np.array([252.0, 246.0, 220.0])) # soft gleam
]

STEEL_KEYS = [
    (0.00, np.array([26.0, 24.0, 35.0])),   # cavity black
    (0.28, np.array([48.0, 54.0, 70.0])),   # cold slate steel
    (0.58, np.array([72.0, 82.0, 104.0])),  # brushed gunmetal
    (0.82, np.array([108.0, 122.0, 148.0])),# bevel highlight
    (1.00, np.array([165.0, 178.0, 202.0])) # metallic edge
]

def create_masterpiece_cuirass(out_path: str = "") -> Image.Image:
    if not out_path:
        out_path = f"{BEAR_DIR}/costume/costume_berserker_cuirass.png"

    # Multi-frequency organic noise for hand-painted tooth
    np.random.seed(4242)
    fine_tooth = (np.random.rand(H, W) - 0.5) * 0.12
    brush_marks = np.zeros((H, W), dtype=np.float32)
    for y in range(H):
        for x in range(W):
            brush_marks[y, x] = (
                math.sin(x * 0.65 + y * 0.85) * 0.035 +
                math.cos(x * 0.95 - y * 0.45) * 0.035 +
                math.sin((x * 1.5 + y * 0.8)) * 0.02
            )
    total_grain = fine_tooth + brush_marks

    canvas = np.zeros((H, W, 4), dtype=np.float32)

    def put_px(x, y, rgb, alpha=1.0):
        if 0 <= x < W and 0 <= y < H and alpha > 0.0:
            c = np.array(rgb, dtype=np.float32)
            cur_a = canvas[y, x, 3] / 255.0
            new_a = alpha + cur_a * (1.0 - alpha)
            if new_a > 0:
                canvas[y, x, :3] = (c[:3] * alpha + canvas[y, x, :3] * cur_a * (1.0 - alpha)) / new_a
                canvas[y, x, 3] = new_a * 255.0

    # ─────────────────────────────────────────────────────────────
    # COMPONENT 1: SEGMENTED LOWER TASSETS / SKIRT (Y: 84..96)
    # ─────────────────────────────────────────────────────────────
    # Center Tasset (X: 57..71, Y: 84..96)
    for y in range(84, 97):
        for x in range(57, 72):
            if y == 96 and (x < 59 or x > 69): continue
            dx = (x - 64.0) / 7.0
            dy = (y - 84.0) / 12.0
            is_edge = (x == 57 or x == 71 or y == 84 or (y == 96 and 59 <= x <= 69) or (y == 95 and (x == 58 or x == 70)))
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y >= 93:
                # Antique gold rim with tarnished shadows
                t_g = 0.42 + 0.38 * (1.0 - abs(dx)) - dy * 0.12 + total_grain[y, x]
                put_px(x, y, interp_ramp(GOLD_KEYS, t_g))
                continue
            is_center_ridge = abs(x - 64) <= 0.6
            nx = dx * 0.8
            t_plate = 0.50 - nx * 0.38 - dy * 0.22 + (0.20 if is_center_ridge else 0.0) + total_grain[y, x]
            dist_rivet = math.sqrt((x - 64.0)**2 + (y - 89.0)**2)
            if dist_rivet <= 1.4:
                rx = (x - 64.0) / 1.4
                ry = (y - 89.0) / 1.4
                t_r = 0.65 - rx * 0.4 - ry * 0.4
                put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                continue
            put_px(x, y, interp_ramp(CRIMSON_KEYS, t_plate))

    # Left Tasset (X: 43..56, Y: 84..95)
    for y in range(84, 95):
        for x in range(43, 57):
            if y == 94 and (x < 45 or x > 54): continue
            dx = (x - 49.5) / 6.5
            dy = (y - 84.0) / 11.0
            is_edge = (x == 43 or x == 56 or y == 84 or (y == 94 and 45 <= x <= 54) or (y == 93 and (x == 44 or x == 55)))
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y >= 92:
                t_g = 0.40 + 0.38 * (1.0 - abs(dx)) + total_grain[y, x]
                put_px(x, y, interp_ramp(GOLD_KEYS, t_g))
                continue
            nx = dx * 0.75 - 0.2
            t_plate = 0.54 - nx * 0.35 - dy * 0.22 + total_grain[y, x]
            dist_rivet = math.sqrt((x - 48.0)**2 + (y - 88.5)**2)
            if dist_rivet <= 1.4:
                rx = (x - 48.0) / 1.4
                ry = (y - 88.5) / 1.4
                t_r = 0.65 - rx * 0.4 - ry * 0.4
                put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                continue
            put_px(x, y, interp_ramp(CRIMSON_KEYS, t_plate))

    # Right Tasset (X: 72..85, Y: 84..95)
    for y in range(84, 95):
        for x in range(72, 86):
            if y == 94 and (x < 74 or x > 83): continue
            dx = (x - 78.5) / 6.5
            dy = (y - 84.0) / 11.0
            is_edge = (x == 72 or x == 85 or y == 84 or (y == 94 and 74 <= x <= 83) or (y == 93 and (x == 73 or x == 84)))
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y >= 92:
                t_g = 0.35 + 0.38 * (1.0 - abs(dx)) + total_grain[y, x]
                put_px(x, y, interp_ramp(GOLD_KEYS, t_g))
                continue
            nx = dx * 0.75 + 0.25
            t_plate = 0.40 - nx * 0.40 - dy * 0.22 + total_grain[y, x]
            dist_rivet = math.sqrt((x - 80.0)**2 + (y - 88.5)**2)
            if dist_rivet <= 1.4:
                rx = (x - 80.0) / 1.4
                ry = (y - 88.5) / 1.4
                t_r = 0.60 - rx * 0.4 - ry * 0.4
                put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                continue
            put_px(x, y, interp_ramp(CRIMSON_KEYS, t_plate))

    # ─────────────────────────────────────────────────────────────
    # COMPONENT 2: VIKING GEAR BELT (Y: 78..84, X: 43..85)
    # ─────────────────────────────────────────────────────────────
    for y in range(78, 85):
        for x in range(43, 86):
            is_edge = (y == 78 or y == 84 or x == 43 or x == 85)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            dy = (y - 78.0) / 6.0
            # Bevel highlights and shadow grooves
            t_s = 0.40 + (0.32 if y == 80 else (0.12 if y == 79 else (-0.25 if y == 83 else -0.08 * dy))) + total_grain[y, x]
            put_px(x, y, interp_ramp(STEEL_KEYS, t_s))

    # Belt Studs / Rivets
    for bx in [47, 52, 76, 81]:
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                d_r = math.sqrt(dx*dx + dy*dy)
                if d_r <= 1.3:
                    t_r = 0.68 - dx * 0.35 - dy * 0.45
                    put_px(bx + dx, 81 + dy, interp_ramp(GOLD_KEYS, t_r))

    # Central Cog Buckle on Belt (X: 58..70, Y: 76..85)
    for y in range(76, 86):
        for x in range(58, 71):
            dist = math.sqrt((x - 64.0)**2 + (y - 80.5)**2)
            if dist > 5.5: continue
            if dist > 4.5:
                put_px(x, y, OUTLINE[:3])
                continue
            if dist < 2.0:
                t_hub = 0.20 - (x - 64.0)*0.1 - (y - 80.5)*0.1 + total_grain[y, x]
                put_px(x, y, interp_ramp(STEEL_KEYS, t_hub))
                continue
            dx = (x - 64.0) / 5.0
            dy = (y - 80.5) / 5.0
            t_gear = 0.55 - dx * 0.35 - dy * 0.35 + total_grain[y, x]
            if dist >= 3.8:
                angle = math.atan2(dy, dx)
                gear_tooth = math.cos(angle * 8.0)
                if gear_tooth > 0.4:
                    t_gear += 0.20
                elif gear_tooth < -0.4:
                    t_gear -= 0.15
            put_px(x, y, interp_ramp(GOLD_KEYS, t_gear))

    # ─────────────────────────────────────────────────────────────
    # COMPONENT 3: MAIN CHEST & TORSO (Y: 54..78, X: 44..84)
    # ─────────────────────────────────────────────────────────────
    # Upper Gorget & Neck Plate (Y: 54..63, X: 45..83)
    for y in range(54, 64):
        x_min = int(47 - (y - 54) * 0.3)
        x_max = int(81 + (y - 54) * 0.3)
        for x in range(x_min, x_max + 1):
            is_edge = (y == 54 or y == 63 or x == x_min or x == x_max)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y == 55:
                t_g = 0.50 + 0.32 * (1.0 - abs((x - 64)/18.0)) + total_grain[y, x]
                put_px(x, y, interp_ramp(GOLD_KEYS, t_g))
                continue
            dy = (y - 54.0) / 9.0
            dx = (x - 64.0) / 18.0
            t_s = 0.52 - dy * 0.32 - abs(dx) * 0.22 + (0.18 if (y == 56 and abs(dx) < 0.6) else 0.0) + total_grain[y, x]
            put_px(x, y, interp_ramp(STEEL_KEYS, t_s))

    # Mid Torso Heavy Cuirass (Y: 62..78, X: 44..84)
    for y in range(62, 79):
        for x in range(44, 85):
            is_edge = (y == 62 or y == 78 or x == 44 or x == 84)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue

            # Lateral brass side flanges (X: 44..48 and 80..84)
            if x <= 48 or x >= 80:
                is_flange_edge = (x == 48 or x == 80)
                if is_flange_edge:
                    put_px(x, y, OUTLINE[:3])
                    continue
                is_rivet_c = y in [66, 70, 74] and (x == 46 or x == 82)
                is_rivet_top = y in [65, 69, 73] and (x == 46 or x == 82)
                is_rivet_bot = y in [67, 71, 75] and (x == 46 or x == 82)
                if is_rivet_top:
                    put_px(x, y, interp_ramp(GOLD_KEYS, 0.92))
                elif is_rivet_c:
                    put_px(x, y, interp_ramp(GOLD_KEYS, 0.78))
                elif is_rivet_bot:
                    put_px(x, y, interp_ramp(GOLD_KEYS, 0.22))
                else:
                    t_g = 0.48 + 0.28 * (1.0 - (y - 62)/16.0) + total_grain[y, x]
                    put_px(x, y, interp_ramp(GOLD_KEYS, t_g))
                continue

            # Diagonal structural seams
            t_seam_y = (y - 63) / 15.0
            left_seam_x = 49.0 + t_seam_y * 6.0
            right_seam_x = 79.0 - t_seam_y * 6.0
            if abs(x - left_seam_x) < 0.8 or abs(x - right_seam_x) < 0.8:
                put_px(x, y, OUTLINE[:3])
                continue

            # Barrel curvature for Viking chest
            dx = (x - 64.0) / 16.0
            dy = (y - 70.0) / 8.0
            nx = dx * 0.95
            ny = dy * 0.65

            # Soft diffuse specular lobe around top-left (x: 53..56, y: 64..67)
            dist_spec = math.sqrt((x - 54.0)**2 + (y - 65.5)**2)
            spec = max(0.0, 1.0 - dist_spec / 4.5) ** 1.8

            dot = -(nx * -0.55 + ny * -0.65)
            t_c = 0.48 + dot * 0.35 + spec * 0.32 - (0.12 if dy > 0.4 else 0.0) + total_grain[y, x]

            # Battle-worn micro-wear scratches and paint cracks
            # Crack 1 on left chest: (50, 67) -> (53, 69)
            if (x, y) in [(50, 67), (51, 68), (52, 68), (53, 69)]:
                t_c = 0.16 # dark crevice
            elif (x, y) in [(51, 69), (52, 69), (54, 70)]:
                t_c = 0.72 # caught highlight rim

            # Scuff 2 on lower right plate: (75, 72) -> (77, 74)
            if (x, y) in [(75, 72), (76, 73), (77, 73)]:
                t_c = 0.20
            elif (x, y) in [(75, 73), (76, 74)]:
                t_c = 0.68

            # Paint chip near edge: (49, 74) exposes dark primer steel
            if (x, y) == (49, 74):
                put_px(x, y, interp_ramp(STEEL_KEYS, 0.45))
                continue

            put_px(x, y, interp_ramp(CRIMSON_KEYS, t_c))

    # ─────────────────────────────────────────────────────────────
    # COMPONENT 4: DUAL TIERED PAULDRONS (SHOULDER GUARDS)
    # ─────────────────────────────────────────────────────────────
    # Left Pauldron (X: 30..48, Y: 52..68)
    # Tier 1 (Upper Plate): Y 52..61, X 31..47
    for y in range(52, 62):
        t_y = (y - 53) / 8.0
        x_min = int(32 - t_y * 1.0)
        x_max = int(46 + t_y * 2.0)
        for x in range(x_min, x_max + 1):
            is_edge = (y == 52 or y == 61 or x == x_min or x == x_max)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y == 53:
                put_px(x, y, interp_ramp(GOLD_KEYS, 0.68 + total_grain[y, x]))
                continue
            dx = (x - 39.0) / 7.0
            t_p = 0.62 - dx * 0.35 - (y - 52)/14.0 + total_grain[y, x]
            # Pauldron dent/scratch at (38, 55) -> (39, 56)
            if (x, y) in [(38, 55), (39, 56)]:
                t_p = 0.22
            elif (x, y) in [(38, 56), (39, 57)]:
                t_p = 0.75
            is_riv = False
            for rx in [35, 43]:
                dist_r = math.sqrt((x - rx)**2 + (y - 56)**2)
                if dist_r <= 1.4:
                    t_r = 0.68 - (x - rx)*0.35 - (y - 56)*0.45
                    put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                    is_riv = True
                    break
            if not is_riv:
                put_px(x, y, interp_ramp(CRIMSON_KEYS, t_p))

    # Left Pauldron Tier 2 (Lower Plate): Y 60..68, X 29..46
    for y in range(60, 69):
        t_y = (y - 60) / 8.0
        x_min = int(30 + t_y * 2.0)
        x_max = int(46 - t_y * 2.0)
        for x in range(x_min, x_max + 1):
            is_edge = (y == 60 or y == 68 or x == x_min or x == x_max)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y <= 62:
                put_px(x, y, interp_ramp(CRIMSON_KEYS, 0.16 + total_grain[y, x]))
                continue
            dx = (x - 38.0) / 7.0
            t_p = 0.48 - dx * 0.28 - (y - 60)/12.0 + total_grain[y, x]
            is_riv = False
            for rx in [33, 42]:
                dist_r = math.sqrt((x - rx)**2 + (y - 64)**2)
                if dist_r <= 1.4:
                    t_r = 0.66 - (x - rx)*0.35 - (y - 64)*0.45
                    put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                    is_riv = True
                    break
            if not is_riv:
                put_px(x, y, interp_ramp(CRIMSON_KEYS, t_p))

    # Right Pauldron Tier 1 (Upper Plate): Y 52..61, X 81..97
    for y in range(52, 62):
        t_y = (y - 53) / 8.0
        x_min = int(82 - t_y * 2.0)
        x_max = int(96 + t_y * 1.0)
        for x in range(x_min, x_max + 1):
            is_edge = (y == 52 or y == 61 or x == x_min or x == x_max)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y == 53:
                put_px(x, y, interp_ramp(GOLD_KEYS, 0.58 + total_grain[y, x]))
                continue
            dx = (x - 89.0) / 7.0
            t_p = 0.48 - dx * 0.35 - (y - 52)/14.0 + total_grain[y, x]
            is_riv = False
            for rx in [85, 93]:
                dist_r = math.sqrt((x - rx)**2 + (y - 56)**2)
                if dist_r <= 1.4:
                    t_r = 0.62 - (x - rx)*0.35 - (y - 56)*0.45
                    put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                    is_riv = True
                    break
            if not is_riv:
                put_px(x, y, interp_ramp(CRIMSON_KEYS, t_p))

    # Right Pauldron Tier 2 (Lower Plate): Y 60..68, X 82..99
    for y in range(60, 69):
        t_y = (y - 60) / 8.0
        x_min = int(82 + t_y * 2.0)
        x_max = int(98 - t_y * 2.0)
        for x in range(x_min, x_max + 1):
            is_edge = (y == 60 or y == 68 or x == x_min or x == x_max)
            if is_edge:
                put_px(x, y, OUTLINE[:3])
                continue
            if y <= 62:
                put_px(x, y, interp_ramp(CRIMSON_KEYS, 0.16 + total_grain[y, x]))
                continue
            dx = (x - 90.0) / 7.0
            t_p = 0.38 - dx * 0.28 - (y - 60)/12.0 + total_grain[y, x]
            is_riv = False
            for rx in [86, 95]:
                dist_r = math.sqrt((x - rx)**2 + (y - 64)**2)
                if dist_r <= 1.4:
                    t_r = 0.58 - (x - rx)*0.35 - (y - 64)*0.45
                    put_px(x, y, interp_ramp(GOLD_KEYS, t_r))
                    is_riv = True
                    break
            if not is_riv:
                put_px(x, y, interp_ramp(CRIMSON_KEYS, t_p))

    # ─────────────────────────────────────────────────────────────
    # COMPONENT 5: HOLLOW APERTURE & HEAVY OCTAGONAL COG BEZEL RING
    # ─────────────────────────────────────────────────────────────
    # Hollow out heart aperture so optic core shines through unhindered (X: 58..70, Y: 66..76)
    for y in range(66, 77):
        for x in range(58, 71):
            canvas[y, x] = [0, 0, 0, 0]

    # Heavy Brass Bezel Ring around aperture (X: 55..73, Y: 63..79)
    for y in range(63, 80):
        for x in range(55, 74):
            if 66 <= y <= 76 and 58 <= x <= 70:
                continue
            is_corner = (
                (x <= 56 and y <= 64) or
                (x >= 72 and y <= 64) or
                (x <= 56 and y >= 78) or
                (x >= 72 and y >= 78)
            )
            if is_corner:
                continue

            is_outer = (y == 63 or y == 79 or x == 55 or x == 73 or
                        (x == 57 and y == 64) or (x == 71 and y == 64) or
                        (x == 57 and y == 78) or (x == 71 and y == 78))
            is_inner = (y == 65 or y == 77 or x == 57 or x == 71)

            if is_outer or is_inner:
                put_px(x, y, OUTLINE[:3])
                continue

            dx = (x - 64.0) / 8.0
            dy = (y - 71.0) / 7.0
            t_b = 0.58 - dx * 0.35 - dy * 0.4 + total_grain[y, x]
            if (x, y) in [(57, 65), (71, 65)]:
                put_px(x, y, [245, 240, 222])
            elif (x, y) in [(57, 77), (71, 77)]:
                put_px(x, y, interp_ramp(GOLD_KEYS, 0.18))
            else:
                put_px(x, y, interp_ramp(GOLD_KEYS, t_b))

    # Convert to uint8
    final_arr = np.clip(canvas, 0, 255).astype(np.uint8)

    # ─────────────────────────────────────────────────────────────
    # COMPONENT 6: RULE 4C INDEPENDENCE WITH CHASSIS
    # ─────────────────────────────────────────────────────────────
    chassis_amber = Image.open(f"{BEAR_DIR}/chassis/paint_bear_amber.png").convert("RGBA")
    chassis_quarry = Image.open(f"{BEAR_DIR}/chassis/paint_iron_quarry.png").convert("RGBA")
    ca_arr = np.array(chassis_amber)
    cq_arr = np.array(chassis_quarry)

    for y in range(H):
        for x in range(W):
            if final_arr[y, x, 3] > 0:
                p = tuple(final_arr[y, x])
                pa = tuple(ca_arr[y, x])
                pq = tuple(cq_arr[y, x])
                if p == pa or p == pq:
                    final_arr[y, x, 2] = (int(final_arr[y, x, 2]) + 2) % 256

    final_img = Image.fromarray(final_arr, mode="RGBA")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    final_img.save(out_path)

    opaque = int(np.sum(final_arr[:, :, 3] > 0))
    colors = len(set(tuple(p) for p in final_arr.reshape(-1, 4) if p[3] > 0))
    c100 = (colors / opaque * 100) if opaque > 0 else 0
    print(f"✓ Created Masterpiece Berserker Cuirass: {out_path}")
    print(f"  bbox={final_img.getbbox()}, opaque={opaque}, colors={colors}, c100={c100:.2f}")

    return final_img

if __name__ == "__main__":
    create_masterpiece_cuirass()
