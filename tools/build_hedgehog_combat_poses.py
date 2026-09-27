#!/usr/bin/env python3
"""
tools/build_hedgehog_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Ratchet Hedgehog (棘輪刺蝟, 21st Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/hedgehog/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/hedgehog/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hedgehog"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hedgehog"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_hedgehog_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_hedgehog_ratchet_and_pawl_cross.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_hedgehog_spring_steel_quill_pack.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_hedgehog_amber_brass_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_hedgehog_brass_tuning_fork_ears.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_hedgehog_marionette_tailor_vest.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_hedgehog_watchmaker_precision_loupe.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_hedgehog_ratchet_needle_dart.png").convert("RGBA")

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

# Standardized ground contact shadow from baseline composite
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(128):
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
    "head_top": (64, 19),
    "ear_l": (35, 28),
    "ear_r": (94, 28),
    "eye_l": (54, 40),
    "eye_r": (76, 40),
    "snout": (64, 48),
    "throat": (64, 56),
    "core": (64, 70),
    "shoulder_l": (46, 66),
    "shoulder_r": (80, 66),
    "arm_l": (42, 78),
    "arm_r": (86, 74),
    "torso": (64, 80),
    "pelvis": (64, 94),
    "hip_l": (46, 96),
    "hip_r": (78, 96),
    "foot_l": (44, 114),
    "foot_r": (80, 114),
    "quill_root": (45, 68),
    "quill_mid": (32, 65),
    "quill_tip": (18, 62),
    "key_mount": (76, 46),
    "key_wing": (84, 28),
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
    # 1. IDLE (工匠戒備步態 / Watchmaker Alert Stance)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (出招蓄勁 / 棘輪自鎖蜷身蓄勢 Ratchet Lock & Coil Stance)
    # Body crouches (y+7, x-2), key locks back (-24 deg), needle dart drawn back (-20 deg),
    # Watchmaker loupe crosshair glowing in mint green (#4ED86A), brass scale ring at ground.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 7), "ear_l": (-3, 6), "ear_r": (-1, 6),
        "eye_l": (-2, 7), "eye_r": (-2, 7), "snout": (-2, 7), "throat": (-2, 7),
        "core": (-2, 7),
        "shoulder_l": (-2, 6), "arm_l": (1, 5),
        "shoulder_r": (-4, 6), "arm_r": (-6, 5),
        "torso": (-2, 7), "pelvis": (-2, 7),
        "hip_l": (-4, 5), "hip_r": (3, 5),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "quill_root": (-3, 5), "quill_mid": (-5, 6), "quill_tip": (-6, 5),
        "key_mount": (-2, 6), "key_wing": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Ratchet key torqued counter-clockwise (-24 deg)
    key_tele = place_rotated_element(key_raw, deg=-24, target_center=(80, 36), scale=1.0)
    # Dart drawn back and tilted (-22 deg)
    dart_tele = place_rotated_element(weapon_raw, deg=-22, target_center=(92, 80), scale=1.02)

    # Loupe targeting reticle & brass scale rings
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Thread guide trajectory line
    t_draw.line([(96, 78), (122, 64)], fill=(255, 208, 40, 210), width=1)
    t_draw.line([(102, 74), (124, 62)], fill=(78, 216, 106, 230), width=2)
    t_draw.line([(108, 70), (124, 61)], fill=(255, 255, 255, 255), width=1)
    # Loupe reticle crosshair at target point (112, 61)
    cx, cy = 112, 61
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(78, 216, 106, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(255, 208, 40, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(78, 216, 106, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(78, 216, 106, 240), width=1)
    # Ratchet spring tension coil arcs around key
    t_draw.arc([68, 20, 96, 48], start=200, end=350, fill=(255, 208, 40, 220), width=2)
    t_draw.arc([72, 24, 92, 44], start=210, end=340, fill=(255, 140, 66, 200), width=1)
    # Loupe precision glint
    t_draw.ellipse([64, 44, 70, 50], fill=(78, 216, 106, 240))
    t_draw.ellipse([65, 45, 69, 49], fill=(255, 255, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, dart_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普攻出手 / 引線穿針極速投擲 Thread-Guided Dart Throw)
    # Forward dash (+13, 0), right arm whips needle dart forward (+15, -2)!
    # Golden thread trail, ratchet key spins forward (+36 deg).
    # =========================================================================
    shifts_attack = {
        "head_top": (13, 0), "ear_l": (11, -1), "ear_r": (14, 0),
        "eye_l": (13, 0), "eye_r": (13, 0), "snout": (14, 1), "throat": (13, 1),
        "core": (12, 0),
        "shoulder_l": (13, 0), "arm_l": (15, -2),
        "shoulder_r": (5, 0), "arm_r": (16, -2),
        "torso": (11, 0), "pelvis": (9, 0),
        "hip_l": (10, -1), "hip_r": (-5, 0),
        "foot_l": (6, 0), "foot_r": (-6, 0),
        "quill_root": (8, -2), "quill_mid": (5, -4), "quill_tip": (3, -6),
        "key_mount": (10, 0), "key_wing": (8, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=36, target_center=(92, 31), scale=1.0)
    dart_attack = place_rotated_element(weapon_raw, deg=12, target_center=(105, 73), scale=1.06)

    # Golden thread piercing beam and gear spark particles
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Spun cotton golden thread piercing line
    a_draw.line([(88, 75), (124, 73)], fill=(255, 208, 40, 245), width=2)
    a_draw.line([(96, 74), (124, 72)], fill=(255, 255, 255, 255), width=1)
    # Piercing sonic cones radiating from needle point
    a_draw.arc([80, 50, 124, 96], start=290, end=70, fill=(255, 140, 66, 230), width=2)
    a_draw.arc([86, 54, 122, 92], start=300, end=60, fill=(78, 216, 106, 240), width=2)
    a_draw.arc([92, 58, 120, 88], start=310, end=50, fill=(255, 208, 40, 255), width=1)
    # Gear sparks
    for pt in [(116, 52), (122, 64), (120, 84), (114, 94), (106, 46), (98, 42)]:
        a_draw.point(pt, fill=(255, 208, 40, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 240, 200, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, dart_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (怒氣大招 / 天機棘輪千針暴風 Tian Ji Thousand-Needle Tempest)
    # Airborne leap (y-8, x+0), needle dart raised aiming upward (-42 deg),
    # ratchet key spins at supercharged overdrive (+76 deg)!
    # Radiant geometric thread network & brass dial storm!
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -8), "ear_l": (-3, -9), "ear_r": (3, -8),
        "eye_l": (0, -8), "eye_r": (0, -8), "snout": (0, -7), "throat": (0, -7),
        "core": (0, -7),
        "shoulder_l": (-3, -7), "arm_l": (-7, -5),
        "shoulder_r": (4, -7), "arm_r": (7, -10),
        "torso": (0, -7), "pelvis": (0, -6),
        "hip_l": (-4, -5), "hip_r": (4, -5),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "quill_root": (-3, -6), "quill_mid": (-6, -10), "quill_tip": (-4, -13),
        "key_mount": (1, -7), "key_wing": (3, -8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=76, target_center=(83, 22), scale=1.0)
    dart_skill = place_rotated_element(weapon_raw, deg=-42, target_center=(92, 54), scale=1.08)

    # Multi-thread geometric storm & clockwork starbursts
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Thread storm web arcs
    s_draw.arc([36, 18, 118, 100], start=210, end=350, fill=(255, 208, 40, 230), width=3)
    s_draw.arc([40, 22, 114, 96], start=215, end=345, fill=(255, 255, 255, 255), width=1)
    s_draw.arc([28, 30, 110, 112], start=190, end=330, fill=(78, 216, 106, 210), width=2)
    s_draw.arc([46, 14, 122, 90], start=220, end=340, fill=(255, 94, 138, 200), width=2)
    # Starlight thread nodes
    for pt in [(46, 34), (74, 20), (102, 30), (116, 54), (88, 76)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, dart_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊硬直 / 鋼棘盾殼回縮吸震 Spike-Cowl Shock Buffer)
    # Body recoils backwards (-14, -5), loupe shows protective recoil indicators,
    # key rattled (-42 deg), needle dart cross-parries (+70 deg).
    # Impact sparks and coral shock rings at (84, 64).
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255] # dark socket
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Squinting pain indicators (> <) in mint green #4ED86A / bright core
    draw_ho.line([(52, 37), (59, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(52, 43), (59, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(53, 38), (58, 40)], fill=(210, 255, 225, 255), width=1)
    draw_ho.line([(53, 42), (58, 40)], fill=(210, 255, 225, 255), width=1)
    draw_ho.line([(80, 37), (73, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(80, 43), (73, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(79, 38), (74, 40)], fill=(210, 255, 225, 255), width=1)
    draw_ho.line([(79, 42), (74, 40)], fill=(210, 255, 225, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(hit_optic)

    shifts_hit = {
        "head_top": (-14, -5), "ear_l": (-16, -7), "ear_r": (-12, -5),
        "eye_l": (-13, -5), "eye_r": (-13, -5), "snout": (-11, -4), "throat": (-9, -3),
        "core": (-7, -2),
        "shoulder_l": (-7, 0), "arm_l": (-3, 2),
        "shoulder_r": (-4, -2), "arm_r": (2, -3),
        "torso": (-4, 0), "pelvis": (2, 2),
        "hip_l": (-3, 2), "hip_r": (4, 2),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "quill_root": (-7, 4), "quill_mid": (-9, 7), "quill_tip": (-5, 10),
        "key_mount": (-11, -4), "key_wing": (-13, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-42, target_center=(71, 26), scale=1.0)
    dart_hit = place_rotated_element(weapon_raw, deg=70, target_center=(78, 68), scale=0.96)

    # Impact starburst and brass deflection flare
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 84, 64
    h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(255, 140, 66, 210), width=2)
    h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 94, 138, 200), width=2)
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(78, 216, 106, 220), width=1)
    h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    for pt in [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx - 12, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 16), (cx + 20, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, dart_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (受擊復位 / 發條解鎖翻滾復位 Spring-Release Tumbling Reset)
    # Stance restabilizes (+1, +5), dart dropped into low resting carry (-14 deg),
    # escapement cooling steam and golden micro-sparks.
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 5), "ear_l": (0, 5), "ear_r": (2, 5),
        "eye_l": (1, 5), "eye_r": (1, 5), "snout": (1, 5), "throat": (1, 5),
        "core": (1, 5),
        "shoulder_l": (-2, 5), "arm_l": (-3, 5),
        "shoulder_r": (2, 5), "arm_r": (4, 6),
        "torso": (1, 5), "pelvis": (1, 5),
        "hip_l": (-2, 4), "hip_r": (2, 4),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "quill_root": (1, 5), "quill_mid": (2, 6), "quill_tip": (1, 7),
        "key_mount": (2, 4), "key_wing": (2, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=-8, target_center=(83, 35), scale=1.0)
    dart_rec = place_rotated_element(weapon_raw, deg=-14, target_center=(94, 84), scale=0.98)

    # Cooling escapement mist & micro-sparks
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(34, 42), (94, 44), (64, 88)]:
        r_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 240, 220, 140))
        r_draw.ellipse([sx - 2, sy - 6, sx + 3, sy - 1], fill=(255, 255, 255, 160))
    for pt in [(32, 38), (96, 40), (62, 84), (98, 78)]:
        r_draw.point(pt, fill=(255, 255, 255, 220))
        r_draw.point((pt[0]+1, pt[1]), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, dart_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING THE RATCHET HEDGEHOG 6 COMBAT ACTION POSES ===")
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_hedgehog_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_hedgehog_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
