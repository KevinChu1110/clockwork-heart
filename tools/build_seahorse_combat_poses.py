#!/usr/bin/env python3
"""
tools/build_seahorse_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Crystal Seahorse (琉璃海馬, 23rd Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/seahorse/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/seahorse/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/seahorse"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/seahorse"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_seahorse_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_seahorse_trident_coral_spire.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_seahorse_twin_propeller_fins.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_seahorse_abyssal_cyan_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_seahorse_crown_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_seahorse_abyssal_scholar_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/optic_seahorse_ocean_sapphire.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_seahorse_abyssal_prism_astrolabe.png").convert("RGBA")

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

# Strictly extract shadow zone (118..125) and enforce margins (126..127 cleared to 0)
for y in range(118, 126):
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
    "head_top": (64, 15),
    "crown_l": (54, 18),
    "crown_r": (74, 18),
    "eye_l": (55, 42),
    "eye_r": (72, 42),
    "snout": (64, 50),
    "throat": (64, 58),
    "core": (64, 68),
    "shoulder_l": (48, 66),
    "shoulder_r": (78, 66),
    "arm_l": (40, 76),
    "arm_r": (78, 72),
    "torso": (63, 76),
    "pelvis": (63, 88),
    "tail_node1": (62, 94),
    "tail_node2": (56, 101),
    "tail_node3": (64, 108),
    "foot_l": (54, 116),
    "foot_r": (74, 116),
    "curio_fin": (36, 60),
    "key_mount": (76, 38),
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
    # 1. IDLE (琉璃浪湧·懸浮阻尼步態 / Abyssal Float Idle)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (出招蓄勁 / 洋流凝聚·星盤校準蓄力 Current Charge Windup)
    # Deep crouch & fluid coil (y+6, x-2), head tilted downward (-2, 6),
    # Trident winding key torqued counter-clockwise (-24 deg),
    # Abyssal prism astrolabe held close and tilted (-22 deg, scale 1.02),
    # Cyan targeting trajectory ray & optical focus glints at (110, 60).
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 6), "crown_l": (-3, 5), "crown_r": (-1, 5),
        "eye_l": (-2, 6), "eye_r": (-2, 6), "snout": (-2, 6), "throat": (-2, 6),
        "core": (-2, 6),
        "shoulder_l": (-2, 5), "arm_l": (1, 4),
        "shoulder_r": (-4, 5), "arm_r": (-6, 5),
        "torso": (-2, 6), "pelvis": (-2, 6),
        "tail_node1": (-3, 5), "tail_node2": (-4, 5), "tail_node3": (-2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_fin": (-3, 4), "key_mount": (-2, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Trident key torqued counter-clockwise (-24 deg)
    key_tele = place_rotated_element(key_raw, deg=-24, target_center=(74, 34), scale=1.0)
    # Astrolabe drawn closer to chest and tilted (-22 deg)
    astrolabe_tele = place_rotated_element(weapon_raw, deg=-22, target_center=(90, 72), scale=1.02)

    # Optic trajectory beams & hydro-magnetic charging rings
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging rings around prism core
    t_draw.arc([80, 62, 100, 82], start=0, end=360, fill=(56, 160, 255, 200), width=1)
    t_draw.arc([83, 65, 97, 79], start=0, end=360, fill=(255, 208, 40, 220), width=1)
    # Aiming trajectory beam in star sky blue and white
    t_draw.line([(88, 70), (116, 58)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(94, 68), (120, 56)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(100, 65), (120, 55)], fill=(255, 255, 255, 255), width=1)
    # Crosshair reticle at target point (110, 58)
    cx, cy = 110, 58
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(56, 160, 255, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(56, 160, 255, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(56, 160, 255, 240), width=1)
    # Hydro-bubble glints
    for bx, by in [(42, 60), (38, 52), (46, 78), (96, 48)]:\
        t_draw.ellipse([bx-2, by-2, bx+2, by+2], fill=(210, 240, 255, 180), outline=(56, 160, 255, 220))
    # Eye focus bright glints
    t_draw.ellipse([53, 46, 57, 50], fill=(255, 255, 255, 255))
    t_draw.ellipse([70, 46, 74, 50], fill=(255, 255, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, astrolabe_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普攻出手 / 琉璃晶爆·稜鏡星陣射擊 Prism Cascade Burst)
    # Forward thrust: torso & neck rock forward (+11, -1), right arm extends (+15, -3)!
    # Astrolabe projected forward (+18 deg, target (104, 62), scale 1.06).
    # Trident key spins forward (+36 deg, target (84, 28)).
    # Luminescent cyan-crystal projectile shards, shockwave arc & dopamine gold sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (11, -1), "crown_l": (9, -2), "crown_r": (12, -1),
        "eye_l": (11, -1), "eye_r": (11, -1), "snout": (12, 0), "throat": (11, 0),
        "core": (10, 0),
        "shoulder_l": (11, 0), "arm_l": (14, -2),
        "shoulder_r": (6, 0), "arm_r": (15, -3),
        "torso": (9, 0), "pelvis": (7, 0),
        "tail_node1": (6, -1), "tail_node2": (3, -2), "tail_node3": (1, -1),
        "foot_l": (5, 0), "foot_r": (-5, 0),
        "curio_fin": (6, -1), "key_mount": (9, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=36, target_center=(84, 28), scale=1.0)
    astrolabe_attack = place_rotated_element(weapon_raw, deg=18, target_center=(104, 62), scale=1.06)

    # Crystal cascade slash arc, hydro-pressure beam & golden kinetic sparks
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # High-pressure water-crystal burst arc
    a_draw.arc([76, 42, 124, 90], start=280, end=70, fill=(56, 160, 255, 245), width=3)
    a_draw.arc([80, 46, 122, 86], start=290, end=60, fill=(255, 208, 40, 230), width=2)
    a_draw.arc([84, 50, 120, 82], start=300, end=50, fill=(255, 255, 255, 255), width=1)
    a_draw.line([(90, 66), (124, 62)], fill=(56, 160, 255, 230), width=2)
    a_draw.line([(96, 64), (124, 61)], fill=(255, 255, 255, 255), width=1)
    # Crystal prism shards flying forward
    for pt in [(114, 46), (122, 56), (121, 72), (115, 82), (106, 38), (96, 36)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(210, 240, 255, 230))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, astrolabe_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (怒氣大招 / 潮汐星環·千棱滅絕海嘯 Abyssal Prism Maelstrom)
    # Airborne float (y-8, x+0), astrolabe raised high overhead (-45 deg, scale 1.10),
    # Trident key rotating at overdrive (+75 deg, target (78, 18))!
    # Concentric hydro-crystal shockwave rings & four-cardinal blue-crystal resonance bursts!
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -8), "crown_l": (-3, -9), "crown_r": (3, -8),
        "eye_l": (0, -8), "eye_r": (0, -8), "snout": (0, -7), "throat": (0, -7),
        "core": (0, -7),
        "shoulder_l": (-3, -7), "arm_l": (-7, -6),
        "shoulder_r": (4, -7), "arm_r": (6, -9),
        "torso": (0, -7), "pelvis": (0, -6),
        "tail_node1": (-2, -5), "tail_node2": (-4, -6), "tail_node3": (1, -4),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "curio_fin": (-3, -7), "key_mount": (1, -7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=75, target_center=(78, 18), scale=1.0)
    astrolabe_skill = place_rotated_element(weapon_raw, deg=-45, target_center=(88, 44), scale=1.10)

    # Maelstrom shockwave rings & ocean sapphire resonance energy
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Rotating celestial prism rings
    s_draw.arc([30, 10, 118, 98], start=200, end=350, fill=(56, 160, 255, 235), width=3)
    s_draw.arc([34, 14, 114, 94], start=205, end=345, fill=(255, 255, 255, 255), width=1)
    s_draw.arc([22, 22, 110, 110], start=180, end=330, fill=(255, 208, 40, 220), width=2)
    s_draw.arc([40, 6, 122, 88], start=210, end=340, fill=(78, 216, 106, 200), width=2)
    # Kinetic burst nodes
    for pt in [(40, 28), (72, 12), (102, 24), (116, 48), (86, 68), (34, 56)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, astrolabe_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊硬直 / 晶盾裂解·阻尼受創後仰 Abyssal Damping Recoil & Stagger)
    # Body recoils backwards (-12, -4), optic lenses show squinting combat indicators,
    # Trident key rattled counter-clockwise (-38 deg, target (68, 26)),
    # Astrolabe deflects defensively (+55 deg, target (78, 64), scale 0.96).
    # Impact sparks & barrier refraction shards at (80, 60).
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255] # dark socket background
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Squinting combat strain / pain indicators (> <) in sapphire cyan and bright white
    draw_ho.line([(52, 39), (58, 42)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(52, 45), (58, 42)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(53, 40), (57, 42)], fill=(210, 240, 255, 255), width=1)
    draw_ho.line([(53, 44), (57, 42)], fill=(210, 240, 255, 255), width=1)
    draw_ho.line([(75, 39), (69, 42)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(75, 45), (69, 42)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(74, 40), (70, 42)], fill=(210, 240, 255, 255), width=1)
    draw_ho.line([(74, 44), (70, 42)], fill=(210, 240, 255, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(hit_optic)

    shifts_hit = {
        "head_top": (-12, -4), "crown_l": (-14, -6), "crown_r": (-10, -4),
        "eye_l": (-11, -4), "eye_r": (-11, -4), "snout": (-10, -3), "throat": (-8, -3),
        "core": (-6, -2),
        "shoulder_l": (-6, 0), "arm_l": (-3, 2),
        "shoulder_r": (-3, -2), "arm_r": (2, -2),
        "torso": (-4, 0), "pelvis": (2, 2),
        "tail_node1": (-2, 2), "tail_node2": (-4, 3), "tail_node3": (2, 2),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "curio_fin": (-8, 2), "key_mount": (-10, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-38, target_center=(68, 26), scale=1.0)
    astrolabe_hit = place_rotated_element(weapon_raw, deg=55, target_center=(78, 64), scale=0.96)

    # Impact starburst & crystal barrier shatter sparks
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 80, 60
    h_draw.arc([cx - 20, cy - 20, cx + 20, cy + 20], start=280, end=80, fill=(255, 160, 16, 210), width=2)
    h_draw.arc([cx - 26, cy - 26, cx + 26, cy + 26], start=290, end=70, fill=(56, 160, 255, 200), width=2)
    h_draw.arc([cx - 14, cy - 14, cx + 14, cy + 14], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    h_draw.line([(cx - 16, cy), (cx + 16, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 16), (cx, cy + 16)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx - 10, cy - 10), (cx + 10, cy + 10)], fill=(56, 160, 255, 220), width=1)
    h_draw.line([(cx - 10, cy + 10), (cx + 10, cy - 10)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 255))
    for pt in [(cx - 16, cy - 8), (cx + 16, cy - 10), (cx - 10, cy + 14), (cx + 14, cy + 12), (cx - 6, cy - 14), (cx + 18, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, astrolabe_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (受擊復位 / 浮力重構·氣壓閥門回穩 Buoyancy Vent Reset)
    # Stance restabilizes (+1, +4), astrolabe dropped to low resting hover (-12 deg, (94, 76), scale 0.98),
    # Cooling escapement mist & micro-bubbles from propulsion fins.
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 4), "crown_l": (0, 4), "crown_r": (2, 4),
        "eye_l": (1, 4), "eye_r": (1, 4), "snout": (1, 4), "throat": (1, 4),
        "core": (1, 4),
        "shoulder_l": (-2, 4), "arm_l": (-3, 4),
        "shoulder_r": (2, 4), "arm_r": (3, 5),
        "torso": (1, 4), "pelvis": (1, 4),
        "tail_node1": (0, 3), "tail_node2": (-1, 3), "tail_node3": (1, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "curio_fin": (0, 4), "key_mount": (1, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=-6, target_center=(77, 33), scale=1.0)
    astrolabe_rec = place_rotated_element(weapon_raw, deg=-12, target_center=(94, 76), scale=0.98)

    # Cooling escapement mist & micro-bubbles
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(34, 44), (92, 46), (64, 86)]:
        r_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(210, 240, 255, 140))
        r_draw.ellipse([sx - 2, sy - 6, sx + 3, sy - 1], fill=(255, 255, 255, 160))
    for pt in [(32, 40), (94, 42), (62, 82), (96, 74)]:
        r_draw.point(pt, fill=(255, 255, 255, 220))
        r_draw.point((pt[0]+1, pt[1]), fill=(56, 160, 255, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, astrolabe_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING THE CRYSTAL SEAHORSE 6 COMBAT ACTION POSES ===")
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_seahorse_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_seahorse_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
