#!/usr/bin/env python3
"""
tools/build_kangaroo_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Boxer Kangaroo (鐵拳袋鼠, 24th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/kangaroo/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/kangaroo/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kangaroo"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/kangaroo"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_kangaroo_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_kangaroo_champion_double_ring.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_kangaroo_steam_exhaust_backpack.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_kangaroo_caramel_bronze_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_kangaroo_steampunk_boxer_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_kangaroo_champion_belt_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/optic_kangaroo_amber_dial_core.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_kangaroo_piston_brass_knuckle.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Extract raw curio crop
curio_bbox = curio_src.getbbox()
assert curio_bbox is not None
curio_raw = curio_src.crop(curio_bbox)

# Standardized ground contact shadow from cleaned baseline composite
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

# Clean baseline shadow to guarantee Rule 4c-5 / 16 (L>=4, T>=4, R>=4, B>=2)
for y in range(118, 126): # up to 125, y=126 and 127 are 0
    for x in range(4, 124):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p
        else:
            s_px[x, y] = (0, 0, 0, 0)

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print(f"Benchmark ground shadow row counts (118..127): {EXPECTED_SHADOW}")

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 without flinching."""
    out = img.copy()
    o_px = out.load()
    s_pixels = shadow_master.load()
    assert o_px is not None and s_pixels is not None

    # Strictly set shadow zone (118..127) to baseline shadow pixels
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_pixels[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
                o_px[x, y] = sp

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 2] = (0, 0, 0, 0)
        o_px[x, 3] = (0, 0, 0, 0)
        o_px[x, 126] = (0, 0, 0, 0)
        o_px[x, 127] = (0, 0, 0, 0)
    for y in range(128):
        o_px[0, y] = (0, 0, 0, 0)
        o_px[1, y] = (0, 0, 0, 0)
        o_px[2, y] = (0, 0, 0, 0)
        o_px[3, y] = (0, 0, 0, 0)
        o_px[124, y] = (0, 0, 0, 0)
        o_px[125, y] = (0, 0, 0, 0)
        o_px[126, y] = (0, 0, 0, 0)
        o_px[127, y] = (0, 0, 0, 0)

    # Sanitize any interpolation dark falloff pixels to canon outline (31, 26, 58)
    arr = np.array(out)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    bad_dark = (alpha > 30) & (rgb[:, :, 0] < 12) & (rgb[:, :, 1] < 12) & (rgb[:, :, 2] < 12)
    if np.any(bad_dark):
        arr[bad_dark, 0] = 31
        arr[bad_dark, 1] = 26
        arr[bad_dark, 2] = 58
        out = Image.fromarray(arr)

    return out

def place_rotated_element(elem_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places any element with precision."""
    b = elem_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    bw, bh = b.size
    gx, gy = bw / 2.0, bh / 2.0

    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(b, (int(round(128 - gx)), int(round(128 - gy))))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        offset = (nw - canvas_size) // 2
        large = scaled.crop((offset, offset, offset + canvas_size, offset + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_center
    out.paste(rotated, (tx - 128, ty - 128), rotated)
    return out

def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 4.0) -> Image.Image:
    w, h = src_img.size
    out_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    displacements = [(sx - dx, sy - dy) for (sx, sy), (dx, dy) in zip(src_points, dst_points)]
    src_pixels = src_img.load()
    out_pixels = out_img.load()
    assert src_pixels is not None and out_pixels is not None

    for y in range(h):
        for x in range(w):
            total_w = 0.0
            dx_accum = 0.0
            dy_accum = 0.0
            exact_match = None

            for i, (qx, qy) in enumerate(dst_points):
                dist_sq = (x - qx) ** 2 + (y - qy) ** 2
                if dist_sq < 1e-4:
                    exact_match = displacements[i]
                    break
                weight = 1.0 / (dist_sq ** (power / 2.0) + epsilon)
                total_w += weight
                dx_accum += weight * displacements[i][0]
                dy_accum += weight * displacements[i][1]

            if exact_match is not None:
                src_x = x + exact_match[0]
                src_y = y + exact_match[1]
            else:
                src_x = x + dx_accum / total_w
                src_y = y + dy_accum / total_w

            x0 = int(math.floor(src_x))
            y0 = int(math.floor(src_y))
            x1 = x0 + 1
            y1 = y0 + 1

            if 0 <= x0 < w - 1 and 0 <= y0 < h - 1:
                fx = src_x - x0
                fy = src_y - y0
                p00 = cast(tuple[int, int, int, int], src_pixels[x0, y0])
                p10 = cast(tuple[int, int, int, int], src_pixels[x1, y0])
                p01 = cast(tuple[int, int, int, int], src_pixels[x0, y1])
                p11 = cast(tuple[int, int, int, int], src_pixels[x1, y1])

                rgba = []
                for c in range(4):
                    val = (p00[c] * (1 - fx) * (1 - fy) +
                           p10[c] * fx * (1 - fy) +
                           p01[c] * (1 - fx) * fy +
                           p11[c] * fx * fy)
                    rgba.append(int(round(val)))
                out_pixels[x, y] = tuple(rgba)
            elif 0 <= x0 < w and 0 <= y0 < h:
                out_pixels[x, y] = src_pixels[x0, y0]

    return out_img

# Anchor corners and borders for IDW
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127)
]

base_landmarks = {
    "head_top": (61, 7),
    "ear_l": (45, 20),
    "ear_r": (72, 19),
    "snout": (61, 48),
    "throat": (61, 56),
    "eye_l": (56, 42),
    "eye_r": (68, 42),
    "core": (63, 67),
    "shoulder_l": (48, 62),
    "shoulder_r": (74, 62),
    "arm_l": (48, 72),
    "arm_r": (82, 71),
    "torso": (62, 78),
    "pelvis": (62, 92),
    "hip_l": (48, 96),
    "hip_r": (72, 96),
    "foot_l": (48, 116),
    "foot_r": (72, 116),
    "tail_base": (48, 92),
    "tail_mid": (28, 106),
    "tail_tip": (14, 116),
    "curio_mount": (44, 43),
    "key_mount": (76, 30),
    "weapon_fist": (98, 73),
}

# Base body without weapon and winding key (for dynamic key & weapon animation)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (拳手戒備步態 / Boxer Alert Stance)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (出招蓄勁 / 活塞蓄壓抱架重踏 Piston Compression & Coil Stance)
    # Body crouches (y+7, x-3), springs compressed, key counter-wound (-26 deg),
    # piston knuckle pulled back (-18 deg, x-6, y+2).
    # Vacuum gauge target reticle in mint green (#4ED86A) and brass arc scales.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-3, 7), "ear_l": (-4, 6), "ear_r": (-2, 6),
        "snout": (-3, 7), "throat": (-3, 7),
        "eye_l": (-3, 7), "eye_r": (-3, 7),
        "core": (-3, 7),
        "shoulder_l": (-3, 6), "shoulder_r": (-5, 6),
        "arm_l": (0, 5), "arm_r": (-6, 5),
        "torso": (-3, 7), "pelvis": (-3, 6),
        "hip_l": (-5, 5), "hip_r": (2, 5),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_base": (-3, 5), "tail_mid": (-5, 4), "tail_tip": (-4, 1),
        "curio_mount": (-4, 6), "key_mount": (-3, 5), "weapon_fist": (-6, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-26, target_center=(73, 35), scale=1.0)
    knuckle_tele = place_rotated_element(weapon_raw, deg=-18, target_center=(92, 76), scale=1.02)

    # Reticle and steam pressure buildup FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Steam conduit trajectory line
    t_draw.line([(96, 75), (122, 65)], fill=(255, 208, 40, 210), width=1)
    t_draw.line([(102, 72), (124, 63)], fill=(78, 216, 106, 230), width=2)
    t_draw.line([(108, 68), (124, 62)], fill=(255, 255, 255, 255), width=1)
    # Pressure reticle crosshair at target point (112, 62)
    cx, cy = 112, 62
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(78, 216, 106, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(78, 216, 106, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(78, 216, 106, 240), width=1)
    # Spring coil tension arcs around backpack exhaust & key
    t_draw.arc([66, 22, 94, 50], start=190, end=350, fill=(255, 208, 40, 220), width=2)
    t_draw.arc([70, 26, 90, 46], start=200, end=340, fill=(230, 57, 70, 200), width=1)
    # Dual exhaust micro-steam plumes
    for ex_x, ex_y in [(34, 18), (48, 16)]:
        t_draw.ellipse([ex_x - 3, ex_y - 5, ex_x + 3, ex_y + 1], fill=(255, 255, 255, 180))
        t_draw.ellipse([ex_x - 5, ex_y - 10, ex_x + 5, ex_y - 2], fill=(255, 245, 230, 140))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, knuckle_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普攻出手 / 氣動衝擊直拳刺擊 Piston Punch Dash)
    # Forward explosive dash (+12, -1), right fist punches straight forward (+16, -3)!
    # Golden steam shockwave trail, brass key spins forward (+38 deg).
    # =========================================================================
    shifts_attack = {
        "head_top": (12, -1), "ear_l": (10, -2), "ear_r": (13, -1),
        "snout": (13, 0), "throat": (12, 0),
        "eye_l": (12, -1), "eye_r": (12, -1),
        "core": (11, 0),
        "shoulder_l": (12, 0), "shoulder_r": (5, 0),
        "arm_l": (14, -2), "arm_r": (16, -3),
        "torso": (10, 0), "pelvis": (8, 0),
        "hip_l": (9, -1), "hip_r": (-5, 0),
        "foot_l": (5, 0), "foot_r": (-6, 0),
        "tail_base": (7, -2), "tail_mid": (4, -4), "tail_tip": (1, -6),
        "curio_mount": (8, 0), "key_mount": (9, 0), "weapon_fist": (16, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=38, target_center=(86, 30), scale=1.0)
    knuckle_attack = place_rotated_element(weapon_raw, deg=10, target_center=(108, 70), scale=1.08)

    # Explosive punch blast cone and gear sparks
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piston thrust beam
    a_draw.line([(86, 73), (124, 70)], fill=(255, 208, 40, 245), width=2)
    a_draw.line([(96, 72), (124, 69)], fill=(255, 255, 255, 255), width=1)
    # Radiating sonic shock cones from brass knuckles
    a_draw.arc([82, 48, 124, 94], start=290, end=70, fill=(230, 57, 70, 230), width=2)
    a_draw.arc([88, 52, 122, 90], start=300, end=60, fill=(255, 160, 16, 240), width=2)
    a_draw.arc([94, 56, 120, 86], start=310, end=50, fill=(255, 208, 40, 255), width=1)
    # Brass gear and piston sparks
    for pt in [(116, 50), (122, 62), (120, 82), (114, 92), (106, 44), (98, 40)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 240, 200, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, knuckle_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (怒氣大招 / 蒸氣過載升龍爆裂拳 Steam Overdrive Dragon Uppercut)
    # Airborne leap (y-9, x+1), knuckle rocket uppercut aimed skyward (-52 deg, x+8, y-12),
    # double-ring key in extreme overdrive (+84 deg), high-pressure steam exhausts flare!
    # =========================================================================
    shifts_skill = {
        "head_top": (1, -9), "ear_l": (-2, -10), "ear_r": (4, -9),
        "snout": (1, -8), "throat": (1, -8),
        "eye_l": (1, -9), "eye_r": (1, -9),
        "core": (1, -8),
        "shoulder_l": (-2, -8), "shoulder_r": (5, -8),
        "arm_l": (-6, -6), "arm_r": (8, -12),
        "torso": (1, -8), "pelvis": (1, -7),
        "hip_l": (-3, -6), "hip_r": (5, -6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_base": (-2, -7), "tail_mid": (-4, -9), "tail_tip": (-2, -11),
        "curio_mount": (-1, -8), "key_mount": (2, -8), "weapon_fist": (8, -12),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=84, target_center=(79, 21), scale=1.0)
    knuckle_skill = place_rotated_element(weapon_raw, deg=-52, target_center=(96, 52), scale=1.12)

    # Overdrive steam storm & radiant shockwave rings
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Uppercut ascending spiral shockwave arcs
    s_draw.arc([40, 16, 120, 96], start=210, end=350, fill=(255, 208, 40, 230), width=3)
    s_draw.arc([44, 20, 116, 92], start=215, end=345, fill=(255, 255, 255, 255), width=1)
    s_draw.arc([32, 28, 112, 108], start=190, end=330, fill=(255, 160, 16, 220), width=2)
    s_draw.arc([48, 12, 124, 88], start=220, end=340, fill=(230, 57, 70, 210), width=2)
    # Steam exhaust eruption plumes
    for ex_x, ex_y in [(38, 22), (52, 20)]:
        s_draw.ellipse([ex_x - 5, ex_y - 12, ex_x + 5, ex_y - 2], fill=(255, 255, 255, 220))
        s_draw.ellipse([ex_x - 8, ex_y - 20, ex_x + 8, ex_y - 6], fill=(255, 240, 210, 170))
    # Starlight brass sparks
    for pt in [(48, 32), (76, 18), (104, 28), (118, 52), (90, 74)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, knuckle_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊硬直 / 重擊受挫衝擊擊退 Heavy Impact Recoil)
    # Heavy backward displacement (-14, -4), eyes into amber pain squint (> <),
    # key rattled (-44 deg), knuckle cross-defending (+65 deg).
    # Coral & gold impact spark explosion at (86, 62).
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255] # dark socket
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Squinting pain indicators (> <) in amber #FF9F1C / bright core
    draw_ho.line([(53, 39), (60, 42)], fill=(255, 159, 28, 255), width=2)
    draw_ho.line([(53, 45), (60, 42)], fill=(255, 159, 28, 255), width=2)
    draw_ho.line([(54, 40), (59, 42)], fill=(255, 240, 180, 255), width=1)
    draw_ho.line([(54, 44), (59, 42)], fill=(255, 240, 180, 255), width=1)
    draw_ho.line([(71, 39), (64, 42)], fill=(255, 159, 28, 255), width=2)
    draw_ho.line([(71, 45), (64, 42)], fill=(255, 159, 28, 255), width=2)
    draw_ho.line([(70, 40), (65, 42)], fill=(255, 240, 180, 255), width=1)
    draw_ho.line([(70, 44), (65, 42)], fill=(255, 240, 180, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(hit_optic)

    shifts_hit = {
        "head_top": (-14, -4), "ear_l": (-16, -6), "ear_r": (-12, -4),
        "snout": (-11, -3), "throat": (-9, -2),
        "eye_l": (-13, -4), "eye_r": (-13, -4),
        "core": (-7, -1),
        "shoulder_l": (-7, 0), "shoulder_r": (-4, -2),
        "arm_l": (-3, 2), "arm_r": (1, -3),
        "torso": (-4, 0), "pelvis": (2, 2),
        "hip_l": (-3, 2), "hip_r": (4, 2),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_base": (-6, 3), "tail_mid": (-8, 6), "tail_tip": (-4, 8),
        "curio_mount": (-12, -3), "key_mount": (-11, -4), "weapon_fist": (0, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-44, target_center=(70, 26), scale=1.0)
    knuckle_hit = place_rotated_element(weapon_raw, deg=65, target_center=(82, 68), scale=0.96)

    # Impact shockwave and armor clatter flare
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 86, 62
    h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(230, 57, 70, 210), width=2)
    h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 94, 138, 200), width=2)
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(255, 160, 16, 220), width=1)
    h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    for pt in [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx - 12, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 16), (cx + 20, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, knuckle_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (收招硬直 / 活塞排氣冷卻沉步 Stance Reset & Pressure Exhaust)
    # Stance restabilizes (+1, +5), knuckle lowered into cooling stance (-12 deg, x-2, y+7),
    # cooling steam vents from backpack and piston chambers.
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 5), "ear_l": (0, 5), "ear_r": (2, 5),
        "snout": (1, 5), "throat": (1, 5),
        "eye_l": (1, 5), "eye_r": (1, 5),
        "core": (1, 5),
        "shoulder_l": (-2, 5), "shoulder_r": (2, 5),
        "arm_l": (-3, 5), "arm_r": (3, 6),
        "torso": (1, 5), "pelvis": (1, 5),
        "hip_l": (-2, 4), "hip_r": (2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_base": (1, 4), "tail_mid": (2, 5), "tail_tip": (1, 6),
        "curio_mount": (0, 5), "key_mount": (2, 4), "weapon_fist": (2, 7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=-10, target_center=(77, 34), scale=1.0)
    knuckle_rec = place_rotated_element(weapon_raw, deg=-12, target_center=(96, 80), scale=0.98)

    # Cooling steam clouds and tiny brass condensation sparkles
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(36, 40), (96, 42), (64, 86)]:
        r_draw.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=(255, 245, 230, 140))
        r_draw.ellipse([sx - 2, sy - 7, sx + 4, sy - 1], fill=(255, 255, 255, 160))
    for pt in [(34, 36), (98, 38), (62, 82), (98, 76)]:
        r_draw.point(pt, fill=(255, 255, 255, 220))
        r_draw.point((pt[0]+1, pt[1]), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, knuckle_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING THE BOXER KANGAROO 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")

        # 512 LANCZOS upscale
        dst_512 = os.path.join(OUT_DIR, f"{p_name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(dst_512, format="PNG")

        bbox = img.getbbox()
        print(f"✓ Saved {p_name:10s} -> {dst_128} (128x128, bbox={bbox}) and {dst_512} (512x512 LANCZOS)")

    # Generate proof sheets
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_kangaroo_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_kangaroo_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
