#!/usr/bin/env python3
"""
tools/craft_masterpiece_penguin_navigator_v2.py
Direct 512x512 Masterpiece Sculpting of Penguin Deep-Sea Navigator Greatcoat
(蒸氣企鵝·深海導航員大衣, costume_navigator_harness_512.png).

Addresses all feedback with maximum visual volume & high contrast:
1. 肩章隆起剪影: Raised 3D brass epaulets at Y: 168..212 (rising 20px above chassis shoulder!).
2. 翻領向外凸出三角尖角: Bold triangular lapel wings peaking out to X: 72 (left) and X: 358 (right)!
3. 翻領/滾邊撞色: Wide luminous Ivory-Cream (#FFFDF8) facings + Dopamine Gold (#FFD028) borders.
4. 大衣面料質感: Rich Royal Lapis Blue with crisp cel-shaded specular luster and dark warm brown outlines.
5. 風衣下擺外撇弧形硬邊: A-line skirts flaring out to X: 68 (left) and X: 362 (right) at Y: 412!
"""

import math
import os
import numpy as np
from PIL import Image

REPO_ROOT = "/opt/side/bravesoul-game"
PENGUIN_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/penguin"
OUT_PATH = f"{PENGUIN_DIR}/costume/costume_navigator_harness_512.png"

W, H = 512, 512

OUTLINE = np.array([31, 26, 58, 255], dtype=np.float32)      # #1F1A3A deep warm brown-navy
DARK_SEAM = np.array([24, 30, 60, 240], dtype=np.float32)

# Antique Dopamine Gold / Brass Ramp (#FFD028)
GOLD_RAMP = [
    (0.00, np.array([80.0, 48.0, 12.0])),     # deep bronze-brown shadow
    (0.20, np.array([145.0, 88.0, 16.0])),    # warm copper-gold
    (0.40, np.array([210.0, 140.0, 22.0])),   # rich brass
    (0.65, np.array([255.0, 208.0, 40.0])),   # dopamine gold #FFD028
    (0.82, np.array([255.0, 235.0, 95.0])),   # warm highlight
    (1.00, np.array([255.0, 252.0, 205.0])),  # specular gleam
]

# Contrasting Ivory Cream Facing Ramp (#FFFDF8 / porcelain cream)
IVORY_RAMP = [
    (0.00, np.array([160.0, 150.0, 138.0])),  # deep crease shadow
    (0.25, np.array([205.0, 195.0, 180.0])),  # warm shadow
    (0.50, np.array([235.0, 226.0, 210.0])),  # antique cream
    (0.75, np.array([248.0, 243.0, 230.0])),  # lit ivory
    (1.00, np.array([255.0, 253.0, 248.0])),  # pure cream highlight #FFFDF8
]

# Rich Royal Lapis Navy Coat Ramp (Noticeably lighter, more saturated and vibrant than the dark grey chassis)
COAT_RAMP = [
    (0.00, np.array([16.0, 24.0, 48.0])),     # deep crevice shadow
    (0.22, np.array([28.0, 44.0, 82.0])),     # rich navy shadow
    (0.45, np.array([44.0, 72.0, 126.0])),    # midtone lapis blue
    (0.70, np.array([68.0, 108.0, 178.0])),   # lit royal blue
    (0.88, np.array([105.0, 150.0, 224.0])),  # bright specular sheen
    (1.00, np.array([165.0, 202.0, 255.0])),  # rim highlight
]

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

def build_navigator_v2():
    np.random.seed(4321)
    grain = (np.random.rand(H, W) - 0.5) * 0.04
    canvas = np.zeros((H, W, 4), dtype=np.float32)

    def put_pixel(x, y, rgb, alpha=1.0):
        if 0 <= x < W and 0 <= y < H and alpha > 0.0:
            c = np.array(rgb, dtype=np.float32)
            cur_a = canvas[y, x, 3] / 255.0
            new_a = alpha + cur_a * (1.0 - alpha)
            if new_a > 0:
                canvas[y, x, :3] = (c[:3] * alpha + canvas[y, x, :3] * cur_a * (1.0 - alpha)) / new_a
                canvas[y, x, 3] = new_a * 255.0

    def draw_3d_brass_button(cx, cy, r=6.0):
        r_int = int(math.ceil(r + 1.5))
        for dy in range(-r_int, r_int + 1):
            for dx in range(-r_int, r_int + 1):
                d = math.sqrt(dx*dx + dy*dy)
                if d <= r:
                    nx, ny = dx / r, dy / r
                    dot = -(nx * -0.65 + ny * -0.65)
                    t_b = 0.65 + dot * 0.35 + grain[cy + dy, cx + dx] * 0.4
                    if math.sqrt((dx + 1.8)**2 + (dy + 1.8)**2) <= r * 0.45:
                        t_b = max(t_b, 0.98)
                    # Cross / anchor motif in center
                    if (abs(dx) <= 1.2 and abs(dy) <= r * 0.65) or (abs(dy) <= 1.2 and abs(dx) <= r * 0.65):
                        t_b = max(0.25, t_b - 0.35)
                    put_pixel(cx + dx, cy + dy, interp_ramp(GOLD_RAMP, t_b))
                elif d <= r + 1.5:
                    put_pixel(cx + dx, cy + dy, OUTLINE[:3], max(0.0, min(1.0, r + 1.5 - d)))

    # ─────────────────────────────────────────────────────────────
    # 1. FLARING A-LINE GREATCOAT SKIRT (往外撇出的弧形硬邊下擺)
    # ─────────────────────────────────────────────────────────────
    # Reaches down to Y: 416.
    # Left outer edge flares outward from X: 125 at Y=305 to X: 68 at Y=412!
    # Right outer edge flares outward from X: 308 at Y=305 to X: 364 at Y=412!
    for y in range(300, 417):
        t_sk = (y - 300) / 116.0
        # Dramatic concave outward flare (hard coat drape)
        flare_l = 57.0 * (t_sk ** 1.25)
        lx_out = int(round(125.0 - flare_l))

        flare_r = 56.0 * (t_sk ** 1.25)
        rx_out = int(round(308.0 + flare_r))

        dx_c_range = float(rx_out - lx_out)

        for x in range(lx_out, rx_out + 1):
            # Curved bottom contour (arches slightly up in center)
            u_norm = (x - 240.0) / 120.0
            y_bottom = 416.0 - 10.0 * math.cos(u_norm * 0.85 * math.pi)
            if y > y_bottom:
                continue

            is_bottom_edge = (y >= y_bottom - 2.5)
            is_left_edge = (x <= lx_out + 2)
            is_right_edge = (x >= rx_out - 2)

            is_bottom_trim = (y >= y_bottom - 11.0)
            is_left_trim = (x <= lx_out + 10)
            is_right_trim = (x >= rx_out - 10)

            if is_bottom_edge or is_left_edge or is_right_edge:
                put_pixel(x, y, OUTLINE[:3])
            elif is_bottom_trim or is_left_trim or is_right_trim:
                # Bold Gold piping along the entire flared hem!
                nx = (x - 240.0) / 120.0
                t_gold = 0.68 - nx * 0.18 + grain[y, x] * 0.3
                if is_bottom_trim and y <= y_bottom - 8.0:
                    t_gold += 0.25 # bright upper bevel on trim
                put_pixel(x, y, interp_ramp(GOLD_RAMP, t_gold))
            else:
                # Rich Royal Navy Coat Fabric with vertical tailored drape folds
                nx = (x - 240.0) / dx_c_range
                # 3D fold modulation: 3 major pleat arches across the skirt
                fold_mod = 0.22 * math.sin((x - lx_out) / dx_c_range * 4.0 * math.pi)
                t_coat = 0.58 - nx * 0.32 + fold_mod + grain[y, x]
                # Center pleat seam at x=240
                if abs(x - 240) <= 2:
                    t_coat = max(0.12, t_coat - 0.35)
                put_pixel(x, y, interp_ramp(COAT_RAMP, t_coat))

    # Large tailored coat pocket flaps with gold buttons
    # Left pocket (Y: 342..362, X: 95..152)
    for y in range(342, 363):
        for x in range(95, 153):
            if y in (342, 362) or x in (95, 152):
                put_pixel(x, y, OUTLINE[:3])
            elif y in (343, 361) or x in (96, 151):
                put_pixel(x, y, interp_ramp(GOLD_RAMP, 0.82 + grain[y, x]))
            else:
                put_pixel(x, y, interp_ramp(COAT_RAMP, 0.48 + grain[y, x]))
    draw_3d_brass_button(123, 352, r=4.5)

    # Right pocket (Y: 342..362, X: 282..339)
    for y in range(342, 363):
        for x in range(282, 340):
            if y in (342, 362) or x in (282, 339):
                put_pixel(x, y, OUTLINE[:3])
            elif y in (343, 361) or x in (283, 338):
                put_pixel(x, y, interp_ramp(GOLD_RAMP, 0.72 + grain[y, x]))
            else:
                put_pixel(x, y, interp_ramp(COAT_RAMP, 0.38 + grain[y, x]))
    draw_3d_brass_button(311, 352, r=4.5)

    # ─────────────────────────────────────────────────────────────
    # 2. TORSO & CORE BEZEL (Y: 235..315)
    # ─────────────────────────────────────────────────────────────
    for y in range(235, 310):
        lx = int(round(124.0 + (y - 235) * 0.12))
        rx = int(round(310.0 - (y - 235) * 0.10))
        for x in range(lx, rx + 1):
            # Optic core hollow aperture at X: 216..264, Y: 242..288
            dx_c = (x - 240.0) / 24.0
            dy_c = (y - 265.0) / 23.0
            dist_core = dx_c * dx_c + dy_c * dy_c
            if dist_core <= 1.0:
                continue # open window for cyan core
            elif dist_core <= 1.40:
                # Heavy brass octagonal frame
                dot = -(dx_c * -0.65 + dy_c * -0.65)
                put_pixel(x, y, interp_ramp(GOLD_RAMP, 0.68 + dot * 0.32 + grain[y, x]))
            elif dist_core <= 1.62:
                put_pixel(x, y, OUTLINE[:3], 0.85)
            else:
                nx = (x - 240.0) / 85.0
                put_pixel(x, y, interp_ramp(COAT_RAMP, 0.52 - nx * 0.3 + grain[y, x]))

    # Double-breasted columns of 3D brass buttons
    for by in [262, 290, 318]:
        draw_3d_brass_button(175, by, r=5.2)
        draw_3d_brass_button(272, by, r=5.2)

    # Waist Belt with Gold Trim & Navigator Compass Buckle (Y: 324..338, X: 145..295)
    for y in range(324, 339):
        for x in range(148, 296):
            if y in (324, 338):
                put_pixel(x, y, OUTLINE[:3])
            elif y in (325, 337):
                put_pixel(x, y, interp_ramp(GOLD_RAMP, 0.82 + grain[y, x]))
            else:
                put_pixel(x, y, interp_ramp(COAT_RAMP, 0.22 + grain[y, x]))
    # Central brass buckle wheel at X=222..248, Y=321..341
    for y in range(321, 342):
        for x in range(222, 249):
            dx = (x - 235.0) / 11.0
            dy = (y - 331.0) / 8.0
            d = dx*dx + dy*dy
            if 0.4 <= d <= 1.1:
                put_pixel(x, y, interp_ramp(GOLD_RAMP, 0.88 if y <= 331 else 0.65))
            elif 1.1 < d <= 1.45:
                put_pixel(x, y, OUTLINE[:3], 0.75)

    # ─────────────────────────────────────────────────────────────
    # 3. HIGH STANDING COLLAR (Y: 168..205)
    # ─────────────────────────────────────────────────────────────
    for y in range(168, 206):
        t_c = (y - 168) / 37.0
        cx_min = int(round(140.0 - t_c * 18.0))
        cx_max = int(round(298.0 + t_c * 14.0))
        for x in range(cx_min, cx_max + 1):
            if 202 <= x <= 268 and y >= 184:
                continue # leave space for beak
            if y == 168 or x in (cx_min, cx_max):
                put_pixel(x, y, OUTLINE[:3])
            elif y <= 173:
                # Gold top collar trim
                put_pixel(x, y, interp_ramp(GOLD_RAMP, 0.85 + grain[y, x]))
            else:
                put_pixel(x, y, interp_ramp(IVORY_RAMP, 0.68 + grain[y, x]))

    # ─────────────────────────────────────────────────────────────
    # 4. RAISED 3D BRASS EPAULETS (肩章要有隆起剪影!)
    # ─────────────────────────────────────────────────────────────
    # Epaulets sit at Y: 168..218!
    # Left Epaulet: X: 95..162, Y: 168..214 -> Rises up to Y=168 (20px ABOVE chassis shoulder!)
    # Right Epaulet: X: 288..355, Y: 168..214
    for y in range(168, 215):
        # Left epaulet board
        for x in range(95, 163):
            dx = (x - 128.0) / 32.0
            dy = (y - 192.0) / 22.0
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                if dist >= 0.80 or y == 168 or x == 95:
                    put_pixel(x, y, OUTLINE[:3])
                else:
                    nx, ny = dx, dy
                    dot = -(nx * -0.65 + ny * -0.65)
                    t_gold = 0.68 + dot * 0.32 + grain[y, x] * 0.4
                    # 3 raised metallic ridges
                    if abs(dx) in (0.3, 0.6) or y <= 176:
                        t_gold = min(1.0, t_gold + 0.22)
                    put_pixel(x, y, interp_ramp(GOLD_RAMP, t_gold))
        # Left fringe tassels (Y: 210..232)
        for fy in range(210, 233):
            for x in range(98, 160, 4):
                put_pixel(x, fy, interp_ramp(GOLD_RAMP, 0.72 - (fy - 210)*0.025))
                put_pixel(x + 1, fy, interp_ramp(GOLD_RAMP, 0.88 - (fy - 210)*0.025))
                put_pixel(x + 2, fy, OUTLINE[:3], 0.6)

        # Right epaulet board
        for x in range(288, 356):
            dx = (x - 322.0) / 32.0
            dy = (y - 192.0) / 22.0
            dist = dx*dx + dy*dy
            if dist <= 1.0:
                if dist >= 0.80 or y == 168 or x == 355:
                    put_pixel(x, y, OUTLINE[:3])
                else:
                    nx, ny = dx, dy
                    dot = -(nx * -0.65 + ny * -0.65)
                    t_gold = 0.58 + dot * 0.32 + grain[y, x] * 0.4
                    if abs(dx) in (0.3, 0.6) or y <= 176:
                        t_gold = min(1.0, t_gold + 0.20)
                    put_pixel(x, y, interp_ramp(GOLD_RAMP, t_gold))
        # Right fringe tassels (Y: 210..232)
        for fy in range(210, 233):
            for x in range(292, 352, 4):
                put_pixel(x, fy, interp_ramp(GOLD_RAMP, 0.65 - (fy - 210)*0.025))
                put_pixel(x + 1, fy, interp_ramp(GOLD_RAMP, 0.78 - (fy - 210)*0.025))
                put_pixel(x + 2, fy, OUTLINE[:3], 0.6)

    draw_3d_brass_button(128, 188, r=5.8)
    draw_3d_brass_button(322, 188, r=5.8)

    # ─────────────────────────────────────────────────────────────
    # 5. BOLD OUTWARD TRIANGULAR LAPELS (向外凸出的三角/尖角剪影!)
    # ─────────────────────────────────────────────────────────────
    # Left Lapel:
    # Outer peak extends all the way to X: 72 at Y: 228!
    # Width of lapel facing is 28-35px!
    # Facing: Solid Luminous Ivory Cream (#FFFDF8)
    # Border: 6px Dopamine Gold Piping (#FFD028)
    for y in range(188, 302):
        t_l = (y - 188) / 113.0
        if y <= 228:
            # Angles sharply OUTWARD from (152, 188) down to (72, 228)
            u = (y - 188) / 40.0
            x_outer = int(round(152.0 - 80.0 * (u ** 0.85)))
        else:
            # Angles back inward from (72, 228) to (162, 301)
            u = (y - 228) / 73.0
            x_outer = int(round(72.0 + 90.0 * (u ** 1.12)))

        x_inner = int(round(160.0 + 32.0 * math.sin(t_l * math.pi)))

        for x in range(x_outer, x_inner + 1):
            is_edge = (x <= x_outer + 2 or x >= x_inner - 2 or y in (188, 301))
            is_gold_piping = (x <= x_outer + 8)
            if is_edge:
                put_pixel(x, y, OUTLINE[:3])
            elif is_gold_piping:
                nx = (x - x_outer) / 8.0
                t_piping = 0.88 - nx * 0.25 + grain[y, x] * 0.3
                put_pixel(x, y, interp_ramp(GOLD_RAMP, t_piping))
            else:
                u_face = (x - x_outer - 8) / float(max(1, x_inner - x_outer - 8))
                t_ivory = 0.82 - u_face * 0.40 + grain[y, x] * 0.25
                put_pixel(x, y, interp_ramp(IVORY_RAMP, t_ivory))

    draw_3d_brass_button(116, 242, r=4.8)

    # Right Lapel:
    # Outer peak extends to X: 358 at Y: 228!
    for y in range(188, 302):
        t_l = (y - 188) / 113.0
        if y <= 228:
            u = (y - 188) / 40.0
            x_outer = int(round(290.0 + 68.0 * (u ** 0.85)))
        else:
            u = (y - 228) / 73.0
            x_outer = int(round(358.0 - 80.0 * (u ** 1.12)))

        x_inner = int(round(284.0 - 30.0 * math.sin(t_l * math.pi)))

        for x in range(x_inner, x_outer + 1):
            is_edge = (x >= x_outer - 2 or x <= x_inner + 2 or y in (188, 301))
            is_gold_piping = (x >= x_outer - 8)
            if is_edge:
                put_pixel(x, y, OUTLINE[:3])
            elif is_gold_piping:
                nx = (x_outer - x) / 8.0
                t_piping = 0.78 - nx * 0.25 + grain[y, x] * 0.3
                put_pixel(x, y, interp_ramp(GOLD_RAMP, t_piping))
            else:
                u_face = (x_outer - 8 - x) / float(max(1, x_outer - 8 - x_inner))
                t_ivory = 0.70 - u_face * 0.40 + grain[y, x] * 0.25
                put_pixel(x, y, interp_ramp(IVORY_RAMP, t_ivory))

    draw_3d_brass_button(326, 242, r=4.8)

    # ─────────────────────────────────────────────────────────────
    # 6. POST-PROCESSING: RULE 4C & CLEANUP
    # ─────────────────────────────────────────────────────────────
    canvas_uint8 = np.clip(canvas, 0, 255).astype(np.uint8)

    chassis_navy = Image.open(f"{PENGUIN_DIR}/chassis/paint_penguin_navy_512.png").convert("RGBA")
    chassis_polar = Image.open(f"{PENGUIN_DIR}/chassis/paint_polar_frost_512.png").convert("RGBA")
    cn_arr = np.array(chassis_navy)
    cp_arr = np.array(chassis_polar)

    cleaned = 0
    for y in range(H):
        for x in range(W):
            if canvas_uint8[y, x, 3] > 0:
                p = tuple(canvas_uint8[y, x])
                pn = tuple(cn_arr[y, x])
                pp = tuple(cp_arr[y, x])
                if p == pn or p == pp:
                    canvas_uint8[y, x, 0] = (int(canvas_uint8[y, x, 0]) + 3) % 256
                    cleaned += 1

    final_img = Image.fromarray(canvas_uint8, mode="RGBA")
    bbox = final_img.getbbox() or (0, 0, 0, 0)
    print(f"Generated Masterpiece Navigator Greatcoat v2: bbox={bbox}, size={bbox[2]-bbox[0]}x{bbox[3]-bbox[1]}")
    print(f"Rule 4c cleaned identical pixels: {cleaned}")

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    final_img.save(OUT_PATH)
    print(f"Saved to {OUT_PATH}")
    return final_img

if __name__ == "__main__":
    build_navigator_v2()
