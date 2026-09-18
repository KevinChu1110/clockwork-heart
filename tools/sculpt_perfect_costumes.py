#!/usr/bin/env python3
"""
tools/sculpt_perfect_costumes.py
Pixel-perfect anatomical sculpt of:
1. Lion Nutcracker Guard (烈鬃獅·胡桃鉗近衛軍裝)
2. Penguin Navigator Trenchcoat (蒸氣企鵝·深海導航員大衣)
"""

import math
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
LION_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/lion"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"
WORK_DIR = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_84698e86"

W, H = 128, 128
OUTLINE = np.array([31, 26, 58, 255], dtype=np.float32)

def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)

def interp_ramp(keys, t):
    t = float(np.clip(t, 0.0, 1.0))
    for i in range(len(keys) - 1):
        t0, c0 = keys[i]
        t1, c1 = keys[i+1]
        if t0 <= t <= t1:
            f = smoothstep(t0, t1, t)
            return c0 + f * (c1 - c0)
    return keys[-1][1]

# Palette Ramps
NAVY_RAMP = [
    (0.00, np.array([16.0, 20.0, 36.0])),
    (0.20, np.array([24.0, 34.0, 58.0])),
    (0.42, np.array([38.0, 54.0, 92.0])),
    (0.68, np.array([54.0, 78.0, 130.0])),
    (0.85, np.array([78.0, 110.0, 172.0])),
    (1.00, np.array([140.0, 175.0, 225.0]))
]

RED_RAMP = [
    (0.00, np.array([92.0, 14.0, 22.0])),
    (0.25, np.array([140.0, 22.0, 32.0])),
    (0.50, np.array([186.0, 32.0, 44.0])),
    (0.75, np.array([226.0, 56.0, 70.0])),
    (1.00, np.array([255.0, 120.0, 135.0]))
]

BRASS_RAMP = [
    (0.00, np.array([58.0, 38.0, 14.0])),
    (0.20, np.array([116.0, 74.0, 24.0])),
    (0.42, np.array([172.0, 118.0, 32.0])),
    (0.65, np.array([222.0, 168.0, 40.0])),
    (0.82, np.array([255.0, 210.0, 46.0])),
    (1.00, np.array([255.0, 255.0, 240.0]))
]

WHITE_RAMP = [
    (0.00, np.array([160.0, 160.0, 180.0])),
    (0.35, np.array([200.0, 200.0, 215.0])),
    (0.75, np.array([245.0, 244.0, 250.0])),
    (1.00, np.array([255.0, 255.0, 255.0]))
]

# ─────────────────────────────────────────────────────────────────
# 1. SCULPT LION
# ─────────────────────────────────────────────────────────────────
def sculpt_lion():
    np.random.seed(3333)
    grain = (np.random.rand(H, W) - 0.5) * 0.06
    canvas = np.zeros((H, W, 4), dtype=np.float32)

    def put_px(x, y, rgb, alpha=1.0):
        if 0 <= x < W and 0 <= y < H and alpha > 0.0:
            c = np.array(rgb, dtype=np.float32)
            cur_a = canvas[y, x, 3] / 255.0
            new_a = alpha + cur_a * (1.0 - alpha)
            if new_a > 0:
                canvas[y, x, :3] = (c[:3] * alpha + canvas[y, x, :3] * cur_a * (1.0 - alpha)) / new_a
                canvas[y, x, 3] = new_a * 255.0

    def draw_sphere_button(cx, cy, radius=1.4):
        r_int = int(math.ceil(radius))
        for dy in range(-r_int, r_int + 1):
            for dx in range(-r_int, r_int + 1):
                d = math.sqrt(dx * dx + dy * dy)
                if d <= radius:
                    nx, ny = dx / radius, dy / radius
                    dot = -(nx * -0.65 + ny * -0.65)
                    t_b = 0.65 + dot * 0.35 + grain[cy + dy, cx + dx] * 0.4
                    if math.sqrt((dx + 0.35)**2 + (dy + 0.35)**2) <= 0.55:
                        t_b = max(t_b, 0.98)
                    put_px(cx + dx, cy + dy, interp_ramp(BRASS_RAMP, t_b))
                elif d <= radius + 0.5:
                    if dx > 0 or dy > 0:
                        put_px(cx + dx, cy + dy, OUTLINE[:3], 0.6)

    # Torso navy jacket: Y: 67..89, tailored to lion torso (X: 47..73 at chest, 48..71 at waist)
    for y in range(67, 90):
        t = (y - 67) / 22.0
        x_min = int(46 + 2.0 * t)
        x_max = int(74 - 2.0 * t)
        for x in range(x_min, x_max + 1):
            if x == x_min or x == x_max:
                put_px(x, y, OUTLINE[:3])
            else:
                nx = (x - 60.0) / float(max(1, x_max - x_min))
                dot = -(nx * -0.7)
                t_n = 0.50 + dot * 0.30 + grain[y, x]
                put_px(x, y, interp_ramp(NAVY_RAMP, t_n))

    # Red double-breasted plastron: Y: 67..89, X: 53..67
    for y in range(67, 90):
        for x in range(53, 68):
            if x in (53, 67):
                put_px(x, y, interp_ramp(WHITE_RAMP, 0.85))
                put_px(x - 1 if x == 53 else x + 1, y, OUTLINE[:3], 0.6)
            elif y == 67:
                put_px(x, y, interp_ramp(WHITE_RAMP, 0.90))
                put_px(x, y - 1, OUTLINE[:3], 0.8)
            else:
                nx = (x - 60.0) / 7.0
                t_r = 0.58 - nx * 0.25 + grain[y, x]
                put_px(x, y, interp_ramp(RED_RAMP, t_r))

    # 6 spherical 3D brass buttons (X: 56 and X: 64, at Y: 72, 78, 84)
    for y_btn in [72, 78, 84]:
        for x in range(54, 58):
            put_px(x, y_btn, interp_ramp(BRASS_RAMP, 0.68 + grain[y_btn, x]))
        for x in range(63, 67):
            put_px(x, y_btn, interp_ramp(BRASS_RAMP, 0.68 + grain[y_btn, x]))
        draw_sphere_button(56, y_btn, radius=1.4)
        draw_sphere_button(64, y_btn, radius=1.4)

    # Broad Epaulets on shoulders at Y: 68..76 (anatomically aligned with lion shoulders)
    # Left Epaulet: X: 35..47, Y: 68..76
    for y in range(68, 76):
        for x in range(35, 48):
            dx = (x - 41.0) / 6.0
            dy = (y - 71.5) / 3.5
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                if dist >= 0.82 or y == 68:
                    put_px(x, y, OUTLINE[:3])
                else:
                    dot = -(dx * -0.7 + dy * -0.7)
                    put_px(x, y, interp_ramp(BRASS_RAMP, 0.70 + dot * 0.30 + grain[y, x]))
    # Left fringe tassels (Y: 75..80)
    for x in range(36, 47, 2):
        for fy in range(75, 81):
            if fy == 80:
                put_px(x, fy, OUTLINE[:3], 0.7)
            else:
                t_f = 0.62 + (80 - fy) * 0.06 + grain[fy, x]
                put_px(x, fy, interp_ramp(BRASS_RAMP, t_f))
                put_px(x + 1, fy, interp_ramp(BRASS_RAMP, t_f * 0.7))

    # Right Epaulet: X: 73..85, Y: 68..76
    for y in range(68, 76):
        for x in range(73, 86):
            dx = (x - 79.0) / 6.0
            dy = (y - 71.5) / 3.5
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                if dist >= 0.82 or y == 68:
                    put_px(x, y, OUTLINE[:3])
                else:
                    dot = -(dx * -0.7 + dy * -0.7)
                    put_px(x, y, interp_ramp(BRASS_RAMP, 0.62 + dot * 0.30 + grain[y, x]))
    # Right fringe tassels (Y: 75..80)
    for x in range(74, 85, 2):
        for fy in range(75, 81):
            if fy == 80:
                put_px(x, fy, OUTLINE[:3], 0.7)
            else:
                t_f = 0.56 + (80 - fy) * 0.06 + grain[fy, x]
                put_px(x, fy, interp_ramp(BRASS_RAMP, t_f))
                put_px(x + 1, fy, interp_ramp(BRASS_RAMP, t_f * 0.7))

    # Ceremonial Gold Belt: Y: 89..93, X: 47..73
    for y in range(89, 94):
        for x in range(47, 74):
            if y in (89, 93) or x in (47, 73):
                put_px(x, y, OUTLINE[:3])
            else:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.72 - (y - 89) * 0.05 + grain[y, x]))
    # Buckle at X: 57..64, Y: 88..94
    for y in range(88, 95):
        for x in range(57, 65):
            if x in (57, 64) or y in (88, 94):
                put_px(x, y, OUTLINE[:3])
            elif x in (58, 63) or y in (89, 93):
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.88 if y == 89 else 0.68))
            else:
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.15))

    # Flank coat tails (Y: 94..104, X: 44..49 on left, X: 71..76 on right)
    for y in range(94, 105):
        for x in range(44, 50):
            if x == 44 or y == 104:
                put_px(x, y, OUTLINE[:3])
            elif y == 103:
                put_px(x, y, interp_ramp(WHITE_RAMP, 0.85))
            else:
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.45 + grain[y, x]))
        for x in range(71, 77):
            if x == 76 or y == 104:
                put_px(x, y, OUTLINE[:3])
            elif y == 103:
                put_px(x, y, interp_ramp(WHITE_RAMP, 0.85))
            else:
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.42 + grain[y, x]))

    # Composite original tassets (Y: 94..108, X: 50..70)
    orig_128 = Image.open(f"{LION_DIR}/costume/costume_nutcracker_guard.png").convert("RGBA")
    for y in range(94, 108):
        for x in range(50, 71):
            p = orig_128.getpixel((x, y))
            if isinstance(p, tuple) and len(p) >= 4 and p[3] > 80:
                put_px(x, y, p[:3], p[3] / 255.0)

    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))

# ─────────────────────────────────────────────────────────────────
# 2. SCULPT PENGUIN
# ─────────────────────────────────────────────────────────────────
def sculpt_penguin():
    np.random.seed(4444)
    grain = (np.random.rand(H, W) - 0.5) * 0.06
    canvas = np.zeros((H, W, 4), dtype=np.float32)

    def put_px(x, y, rgb, alpha=1.0):
        if 0 <= x < W and 0 <= y < H and alpha > 0.0:
            c = np.array(rgb, dtype=np.float32)
            cur_a = canvas[y, x, 3] / 255.0
            new_a = alpha + cur_a * (1.0 - alpha)
            if new_a > 0:
                canvas[y, x, :3] = (c[:3] * alpha + canvas[y, x, :3] * cur_a * (1.0 - alpha)) / new_a
                canvas[y, x, 3] = new_a * 255.0

    def draw_brass_rivet(cx, cy, radius=1.2):
        r_int = int(math.ceil(radius))
        for dy in range(-r_int, r_int + 1):
            for dx in range(-r_int, r_int + 1):
                d = math.sqrt(dx * dx + dy * dy)
                if d <= radius:
                    nx, ny = dx / radius, dy / radius
                    dot = -(nx * -0.65 + ny * -0.65)
                    t_b = 0.65 + dot * 0.35 + grain[cy + dy, cx + dx] * 0.4
                    if math.sqrt((dx + 0.3)**2 + (dy + 0.3)**2) <= 0.5:
                        t_b = max(t_b, 0.98)
                    put_px(cx + dx, cy + dy, interp_ramp(BRASS_RAMP, t_b))
                elif d <= radius + 0.5:
                    if dx > 0 or dy > 0:
                        put_px(cx + dx, cy + dy, OUTLINE[:3], 0.6)

    # 1. Shoulder Epaulets / Straps (Left: X: 34..46, Right: X: 68..80, Y: 49..59)
    for y in range(49, 60):
        for x in range(34, 47):
            dx = (x - 40.5) / 6.0
            dy = (y - 54.5) / 5.0
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                if dist >= 0.80 or y == 49:
                    put_px(x, y, OUTLINE[:3])
                else:
                    dot = -(dx * -0.65 + dy * -0.65)
                    put_px(x, y, interp_ramp(NAVY_RAMP, 0.58 + dot * 0.32 + grain[y, x]))
        # Buckle on left strap
        for x in range(38, 43):
            put_px(x, 54, interp_ramp(BRASS_RAMP, 0.85))
            put_px(x, 55, interp_ramp(BRASS_RAMP, 0.70))

    for y in range(49, 60):
        for x in range(68, 81):
            dx = (x - 74.5) / 6.0
            dy = (y - 54.5) / 5.0
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                if dist >= 0.80 or y == 49:
                    put_px(x, y, OUTLINE[:3])
                else:
                    dot = -(dx * -0.65 + dy * -0.65)
                    put_px(x, y, interp_ramp(NAVY_RAMP, 0.52 + dot * 0.32 + grain[y, x]))
        # Buckle on right strap
        for x in range(72, 77):
            put_px(x, 54, interp_ramp(BRASS_RAMP, 0.80))
            put_px(x, 55, interp_ramp(BRASS_RAMP, 0.65))

    # 2. Outward Flared Flank Trenchcoat Skirts:
    # Left Flank Coat: X: 28..42, Y: 58..92
    for y in range(58, 93):
        t = (y - 58) / 34.0
        x_min = int(30 - 3.0 * math.sin(t * math.pi * 0.9))
        x_max = int(42 - 1.5 * t)
        for x in range(x_min, x_max + 1):
            if x == x_min or y == 92:
                put_px(x, y, OUTLINE[:3])
            elif y == 91 or x == x_min + 1:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.75 + grain[y, x]))
            else:
                nx = (x - x_min) / float(max(1, x_max - x_min))
                t_c = 0.38 + nx * 0.35 + grain[y, x]
                put_px(x, y, interp_ramp(NAVY_RAMP, t_c))
    # Left pocket flap (Y: 76..81, X: 31..40)
    for y in range(76, 82):
        for x in range(31, 41):
            if x in (31, 40) or y in (76, 81):
                put_px(x, y, OUTLINE[:3])
            elif y == 77:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.82))
            else:
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.65 + grain[y, x]))
    draw_brass_rivet(36, 79, radius=1.1)

    # Right Flank Coat: X: 72..84, Y: 58..92
    for y in range(58, 93):
        t = (y - 58) / 34.0
        x_max = int(82 + 2.5 * math.sin(t * math.pi * 0.9))
        x_min = int(72 + 1.5 * t)
        for x in range(x_min, x_max + 1):
            if x == x_max or y == 92:
                put_px(x, y, OUTLINE[:3])
            elif y == 91 or x == x_max - 1:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.70 + grain[y, x]))
            else:
                nx = (x_max - x) / float(max(1, x_max - x_min))
                t_c = 0.35 + nx * 0.35 + grain[y, x]
                put_px(x, y, interp_ramp(NAVY_RAMP, t_c))
    # Right pocket flap (Y: 76..81, X: 74..83)
    for y in range(76, 82):
        for x in range(74, 84):
            if x in (74, 83) or y in (76, 81):
                put_px(x, y, OUTLINE[:3])
            elif y == 77:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.78))
            else:
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.58 + grain[y, x]))
    draw_brass_rivet(78, 79, radius=1.1)

    # 3. Folded 3D Lapels (立體大衣翻領) framing the chest (Y: 48..68):
    # Left Lapel: X: 38..48, Y: 48..68
    for y in range(48, 69):
        t = (y - 48) / 20.0
        lx0 = int(38 - 1.0 * math.sin(t * math.pi))
        lx1 = int(44 + 4.5 * math.sin(t * math.pi * 0.7)) if t < 0.6 else int(48 - 10.0 * (t - 0.6))
        for x in range(lx0, lx1 + 1):
            if x == lx1:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.85 + grain[y, x]))
                put_px(x + 1, y, OUTLINE[:3], 0.7)
            elif x == lx0:
                put_px(x, y, OUTLINE[:3])
            else:
                nx = (x - lx0) / float(max(1, lx1 - lx0))
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.55 + nx * 0.32 + grain[y, x]))
    draw_brass_rivet(45, 57, radius=1.1)

    # Right Lapel: X: 66..76, Y: 48..68
    for y in range(48, 69):
        t = (y - 48) / 20.0
        rx1 = int(76 + 1.0 * math.sin(t * math.pi))
        rx0 = int(70 - 4.5 * math.sin(t * math.pi * 0.7)) if t < 0.6 else int(66 + 10.0 * (t - 0.6))
        for x in range(rx0, rx1 + 1):
            if x == rx0:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.80 + grain[y, x]))
                put_px(x - 1, y, OUTLINE[:3], 0.7)
            elif x == rx1:
                put_px(x, y, OUTLINE[:3])
            else:
                nx = (rx1 - x) / float(max(1, rx1 - rx0))
                put_px(x, y, interp_ramp(NAVY_RAMP, 0.48 + nx * 0.32 + grain[y, x]))
    draw_brass_rivet(69, 57, radius=1.1)

    # Collar gold arch under beak at Y: 47..48, X: 48..66
    for x in range(48, 67):
        put_px(x, 46, OUTLINE[:3])
        put_px(x, 47, interp_ramp(BRASS_RAMP, 0.85 + grain[47, x]))

    # 4. Brass Waist Harness Clasp across chest at Y: 71..73, X: 44..70
    for x in range(44, 71):
        put_px(x, 71, interp_ramp(BRASS_RAMP, 0.80 + grain[71, x]))
        put_px(x, 72, interp_ramp(BRASS_RAMP, 0.65))
        put_px(x, 73, OUTLINE[:3], 0.6)
    # Center round ring clasp (X: 55..59, Y: 70..74)
    for y in range(70, 75):
        for x in range(55, 60):
            dx = (x - 57.0) / 2.0
            dy = (y - 72.0) / 2.0
            dist = dx*dx + dy*dy
            if 0.4 <= dist <= 1.2:
                put_px(x, y, interp_ramp(BRASS_RAMP, 0.88 if y <= 72 else 0.68))

    return Image.fromarray(np.clip(canvas, 0, 255).astype(np.uint8))

def main():
    lion_128 = sculpt_lion()
    pen_128 = sculpt_penguin()
    
    # Save 128
    lion_128.save(f"{WORK_DIR}/debug/perfect_lion_128.png")
    pen_128.save(f"{WORK_DIR}/debug/perfect_pen_128.png")
    print("Lion 128 bbox:", lion_128.getbbox())
    print("Penguin 128 bbox:", pen_128.getbbox())
    
    # Lanczos upscale to 512x512
    lion_512 = lion_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
    pen_512 = pen_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
    
    lion_dst = f"{LION_DIR}/costume/costume_nutcracker_guard_512.png"
    pen_dst = f"{PENGUIN_DIR}/costume/costume_navigator_harness_512.png"
    
    lion_512.save(lion_dst)
    pen_512.save(pen_dst)
    
    print(f"Lion 512 saved: bbox={lion_512.getbbox()}")
    print(f"Penguin 512 saved: bbox={pen_512.getbbox()}")

if __name__ == "__main__":
    main()
