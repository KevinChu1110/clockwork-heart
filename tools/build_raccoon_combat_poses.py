#!/usr/bin/env python3
"""
tools/build_raccoon_combat_poses.py
Generates the complete, definitive 6 combat action poses for Orbit Raccoon (星巡浣熊, 20th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/raccoon/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/raccoon/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/raccoon"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/raccoon"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_raccoon_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_raccoon_quad_solar_sail.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_raccoon_coaxial_ring_antenna_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_raccoon_orbit_aqua_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_raccoon_parabolic_radar_dish.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_raccoon_space_explorer_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_raccoon_hud_polarizer_visor.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_raccoon_anti_gravity_pulse_blaster.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Extract raw tail curio crop
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
    "head_top": (64, 20),
    "ear_l": (36, 32),
    "ear_r": (92, 34),
    "eye_l": (53, 40),
    "eye_r": (75, 40),
    "snout": (64, 49),
    "throat": (64, 58),
    "core": (64, 73),
    "shoulder_l": (46, 68),
    "shoulder_r": (80, 68),
    "arm_l": (42, 80),
    "arm_r": (86, 75),
    "torso": (64, 80),
    "pelvis": (64, 94),
    "hip_l": (46, 96),
    "hip_r": (78, 96),
    "foot_l": (44, 114),
    "foot_r": (80, 114),
    "tail_root": (40, 87),
    "tail_mid": (30, 78),
    "tail_tip": (19, 68),
    "key_mount": (75, 48),
    "key_wing": (82, 36),
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
    # 1. IDLE (星穹警戒·待命持銃姿態 / Sentry Space Ranger Ready Pose)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (反重力聚能·高頻校準 / Anti-Gravity Flux Charge & HUD Lock)
    # Deep crouch (y+7, x-2), head dish tilted down, telemetry calibration,
    # pulse blaster drawn back ready to discharge, quad solar sail key torqued back,
    # HUD targeting reticle & holographic lock-on grid glowing in cyan/mint!
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
        "tail_root": (-3, 5), "tail_mid": (-6, 7), "tail_tip": (-7, 6),
        "key_mount": (-2, 6), "key_wing": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Solar sail winding key torqued back (-24 deg)
    key_tele = place_rotated_element(key_raw, deg=-24, target_center=(79, 42), scale=1.0)
    blaster_tele = place_rotated_element(weapon_raw, deg=-25, target_center=(92, 78), scale=1.02)

    # Holographic HUD targeting grid & anti-gravity charging rings
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Aiming trajectory laser line
    t_draw.line([(96, 74), (122, 62)], fill=(0, 194, 203, 210), width=1)
    t_draw.line([(102, 70), (124, 60)], fill=(78, 216, 106, 230), width=2)
    t_draw.line([(108, 67), (124, 59)], fill=(255, 255, 255, 255), width=1)
    # Reticle crosshair at target point (112, 59)
    cx, cy = 112, 59
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(0, 194, 203, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(78, 216, 106, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(0, 194, 203, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(0, 194, 203, 240), width=1)
    # Energy field charging arcs
    t_draw.arc([22, 28, 54, 56], start=210, end=350, fill=(0, 194, 203, 190), width=2)
    t_draw.arc([74, 28, 106, 56], start=190, end=330, fill=(255, 208, 40, 200), width=2)
    t_draw.arc([72, 38, 94, 60], start=20, end=340, fill=(78, 216, 106, 210), width=2)
    # Optic visor telemetry glint
    t_draw.ellipse([50, 44, 56, 50], fill=(78, 216, 106, 230))
    t_draw.ellipse([72, 44, 78, 50], fill=(78, 216, 106, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, blaster_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (軌道脈衝·強襲平射 / Orbital Pulse Blaster Discharge)
    # Forward thrust (+13, 0), right arm thrusts blaster forward to fire (+16, -2)!
    # Tail counterbalances backwards (+7, -3). Solar sail key spins forward (+38 deg).
    # Multi-ring anti-gravity pulse blast and starlight muzzle flash!
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
        "tail_root": (8, -2), "tail_mid": (5, -4), "tail_tip": (3, -6),
        "key_mount": (10, 0), "key_wing": (8, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=38, target_center=(92, 35), scale=1.0)
    blaster_attack = place_rotated_element(weapon_raw, deg=15, target_center=(105, 73), scale=1.06)

    # Anti-gravity pulse shockwave rings and starlight beam
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Core discharge beam
    a_draw.line([(102, 73), (124, 73)], fill=(0, 194, 203, 245), width=3)
    a_draw.line([(108, 71), (124, 71)], fill=(255, 255, 255, 255), width=2)
    # Pulse rings radiating outwards
    a_draw.arc([76, 48, 124, 98], start=290, end=70, fill=(0, 194, 203, 230), width=3)
    a_draw.arc([82, 52, 122, 94], start=300, end=60, fill=(78, 216, 106, 240), width=2)
    a_draw.arc([88, 56, 120, 90], start=310, end=50, fill=(255, 208, 40, 255), width=1)
    # Particle sparks
    for pt in [(116, 52), (122, 64), (120, 84), (114, 94), (106, 46), (98, 42)]:
        a_draw.point(pt, fill=(0, 194, 203, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(210, 255, 245, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, blaster_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (星巡過載·全彈超光速掃射 / Superluminal Overdrive Barrage)
    # Airborne zero-G leap (y-8, x+0), pulse blaster raised aiming diagonally upward (-45 deg),
    # tail curls up with full coaxial antenna discharge, solar sail key spins at max overdrive (+78 deg)!
    # Concentric orbital plasma rings, starburst flares & aurora trajectory fans!
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
        "tail_root": (-3, -6), "tail_mid": (-6, -11), "tail_tip": (-4, -14),
        "key_mount": (1, -7), "key_wing": (3, -8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=78, target_center=(84, 28), scale=1.0)
    blaster_skill = place_rotated_element(weapon_raw, deg=-45, target_center=(92, 54), scale=1.08)

    # Multi-orbital cosmic discharge fan
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    s_draw.arc([38, 20, 116, 98], start=220, end=350, fill=(0, 194, 203, 230), width=3)
    s_draw.arc([42, 24, 112, 94], start=225, end=345, fill=(255, 255, 255, 255), width=1)
    s_draw.arc([30, 32, 108, 110], start=200, end=330, fill=(78, 216, 106, 200), width=2)
    s_draw.arc([48, 16, 120, 88], start=230, end=340, fill=(255, 208, 40, 210), width=2)
    # Starlight energy points
    for pt in [(48, 36), (74, 22), (100, 32), (114, 56), (90, 78)]:
        s_draw.point(pt, fill=(78, 216, 106, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.5))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, blaster_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (護盾過載·偏折受擊 / Shield Fracture & Recoil Shock)
    # Body recoils backwards (-14, -5), optic visor squinting / telemetry warning lines (> <),
    # solar sail key rattled (-45 deg), blaster held in protective parry deflection (+72 deg).
    # Kinetic deflection starburst and fracture rings at (84, 64).
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255] # dark visor socket plate
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Squinting pain indicators (> <) in mint green #4ED86A / bright core
    draw_ho.line([(48, 37), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(48, 43), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(49, 38), (54, 40)], fill=(210, 255, 225, 255), width=1)
    draw_ho.line([(49, 42), (54, 40)], fill=(210, 255, 225, 255), width=1)
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
        "tail_root": (-7, 4), "tail_mid": (-9, 8), "tail_tip": (-5, 11),
        "key_mount": (-11, -4), "key_wing": (-13, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-45, target_center=(70, 31), scale=1.0)
    blaster_hit = place_rotated_element(weapon_raw, deg=72, target_center=(78, 68), scale=0.96)

    # Impact starburst and shield deflection flare
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 84, 64
    h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(0, 194, 203, 210), width=2)
    h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 94, 138, 200), width=2)
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(0, 194, 203, 220), width=1)
    h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    for pt in [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx - 12, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 16), (cx + 20, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, blaster_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (冷氣排氣·姿態復位 / Attitude Control Venting & Stance Reset)
    # Distinct relaxed recovery posture: sinking down into restabilization (+1, +5),
    # blaster dropped into low resting carry (-14 deg), cooling micro-thruster mist venting.
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
        "tail_root": (1, 5), "tail_mid": (2, 6), "tail_tip": (1, 7),
        "key_mount": (2, 4), "key_wing": (2, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=-8, target_center=(83, 40), scale=1.0)
    blaster_rec = place_rotated_element(weapon_raw, deg=-14, target_center=(94, 84), scale=0.98)

    # Cold gas thruster venting (diffused cyan/white soft puffs)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for sx, sy in [(34, 42), (94, 44), (64, 88)]:
        r_draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(210, 245, 255, 140))
        r_draw.ellipse([sx - 2, sy - 6, sx + 3, sy - 1], fill=(255, 255, 255, 160))
    # Cooling spark glints
    for pt in [(32, 38), (96, 40), (62, 84), (98, 78)]:
        r_draw.point(pt, fill=(255, 255, 255, 220))
        r_draw.point((pt[0]+1, pt[1]), fill=(0, 194, 203, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, blaster_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING ORBIT RACCOON 6 COMBAT ACTION POSES ===")
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
    # 1. 768-wide strip (all 6 poses in a row: 128 x 6 = 768)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_raccoon_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_raccoon_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
