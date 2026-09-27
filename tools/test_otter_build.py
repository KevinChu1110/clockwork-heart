#!/usr/bin/env python3
"""
tools/test_otter_build.py
Prototyping and parameter tuning for Tidal Otter 6 combat poses.
"""
import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/otter"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/otter"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_otter_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_otter_nautical_rudder_helm.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_otter_articulated_rudder_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_otter_abyssal_cyan_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_otter_diver_bell_visor.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_otter_deepsea_salvage_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_otter_phosphor_green_gauges.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_otter_abyssal_anchor_cleaver.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

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

def place_weapon(wpn_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Abyssal Anchor Cleaver with zero clipping."""
    b = wpn_img.copy()
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
    "head_top": (64, 25),
    "ear_l": (39, 40),
    "ear_r": (90, 42),
    "eye_l": (52, 40),
    "eye_r": (76, 40),
    "snout": (64, 49),
    "throat": (64, 58),
    "core": (63, 73),
    "shoulder_l": (46, 68),
    "shoulder_r": (80, 68),
    "arm_l": (42, 82),
    "arm_r": (88, 76),
    "torso": (63, 80),
    "pelvis": (63, 94),
    "hip_l": (46, 96),
    "hip_r": (78, 96),
    "foot_l": (44, 114),
    "foot_r": (80, 114),
    "tail_root": (44, 88),
    "tail_mid": (28, 92),
    "tail_tip": (16, 94),
    "key_mount": (76, 48),
    "key_wing": (88, 32),
}

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (浪花整備·潛水防衛姿態 / Sentry Submersible Ready Pose)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (渦流蓄能·下潛伏擊 / Abyssal Dive & Pressure Charge)
    # Deep crouch (y+7, x-2), head helmet tilted down, valves & tail drawn tight,
    # Abyssal Anchor drawn back ready to cleave, phosphor green gauges glowing with aim reticle!
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 7), "ear_l": (-3, 6), "ear_r": (-1, 6),
        "eye_l": (-2, 7), "eye_r": (-2, 7), "snout": (-2, 7), "throat": (-2, 7),
        "core": (-2, 7),
        "shoulder_l": (-2, 6), "arm_l": (1, 5),
        "shoulder_r": (-4, 6), "arm_r": (-7, 5),
        "torso": (-2, 7), "pelvis": (-2, 7),
        "hip_l": (-4, 5), "hip_r": (3, 5),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (-3, 5), "tail_mid": (-6, 7), "tail_tip": (-8, 6),
        "key_mount": (-2, 6), "key_wing": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Anchor drawn back in tight reverse stance ready to erupt
    claw_tele = place_weapon(weapon_raw, deg=-30, target_center=(80, 83), scale=1.02, mirror=False)

    # Turbo charging kinetic lines, golden torque ring, and cyan optic beam FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Hydro-kinetic aiming trajectory beam forward-right
    t_draw.line([(78, 80), (114, 60)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(86, 73), (118, 56)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(94, 68), (120, 54)], fill=(255, 255, 255, 255), width=1)
    # Concentric charging reticle at (110, 56)
    cx, cy = 110, 56
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(56, 160, 255, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(255, 208, 40, 240), width=1)
    # Acoustic valve pressure waves
    t_draw.arc([22, 28, 54, 56], start=210, end=350, fill=(56, 160, 255, 190), width=2)
    t_draw.arc([74, 28, 106, 56], start=190, end=330, fill=(255, 208, 40, 200), width=2)
    # Rudder helm key torque glow arc
    t_draw.arc([72, 38, 94, 60], start=20, end=340, fill=(255, 160, 16, 210), width=2)
    # Mint green phosphor eye beam glow
    t_draw.ellipse([49, 44, 55, 50], fill=(78, 216, 106, 230))
    t_draw.ellipse([73, 44, 79, 50], fill=(78, 216, 106, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, claw_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (深淵錨破·劈浪橫斬 / Abyssal Anchor Tidal Wave Slash)
    # Forward thrust: torso rocks forward (+13, -1), right arm thrusts anchor forward!
    # Tail counter-balances horizontally backwards (+6, -4).
    # =========================================================================
    shifts_attack = {
        "head_top": (13, -1), "ear_l": (11, -2), "ear_r": (14, -1),
        "eye_l": (13, -1), "eye_r": (13, -1), "snout": (14, 0), "throat": (13, 0),
        "core": (12, 0),
        "shoulder_l": (13, -1), "arm_l": (16, -2),
        "shoulder_r": (4, 0), "arm_r": (15, -2),
        "torso": (11, 0), "pelvis": (9, 0),
        "hip_l": (10, -1), "hip_r": (-5, 0),
        "foot_l": (6, 0), "foot_r": (-6, 0),
        "tail_root": (8, -2), "tail_mid": (5, -4), "tail_tip": (3, -7),
        "key_mount": (10, 0), "key_wing": (8, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Anchor cleaver cleaved forward horizontally
    claw_attack = place_weapon(weapon_raw, deg=18, target_center=(100, 74), scale=1.06, mirror=False)

    # Tidal Wave Cleave Vortex & Kinetic Shockwave Cones
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Piercing water-blade line
    a_draw.line([(94, 74), (122, 74)], fill=(56, 160, 255, 245), width=3)
    a_draw.line([(100, 72), (124, 72)], fill=(255, 255, 255, 255), width=2)
    # Crescent tidal wave slashing arcs
    a_draw.arc([68, 48, 124, 100], start=290, end=70, fill=(56, 160, 255, 230), width=3)
    a_draw.arc([74, 52, 122, 96], start=300, end=60, fill=(255, 208, 40, 240), width=2)
    a_draw.arc([80, 56, 120, 92], start=310, end=50, fill=(255, 255, 255, 255), width=1)
    # Water droplets / bubble spray particles
    for pt in [(116, 52), (122, 64), (120, 84), (114, 96), (106, 44), (96, 40)]:
        a_draw.point(pt, fill=(56, 160, 255, 255))
        a_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(210, 255, 225, 220))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, claw_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (滔天破浪·巨錨怒砸 / Maelstrom Anchor Cataclysm Drop)
    # Upward leap / rearing stance (y-8, x+0), anchor raised high overhead slamming down!
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

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Heavy anchor held high overhead slamming diagonally down
    claw_skill = place_weapon(weapon_raw, deg=-48, target_center=(88, 52), scale=1.08, mirror=False)

    # Cataclysmic Tidal Drop Slash FX (cyan + gold dual wave crest)
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Primary cyan tidal slash arc
    s_draw.arc([38, 20, 116, 98], start=220, end=350, fill=(56, 160, 255, 230), width=3)
    s_draw.arc([42, 24, 112, 94], start=225, end=345, fill=(255, 255, 255, 255), width=1)
    # Secondary golden torque resonance arc
    s_draw.arc([30, 32, 108, 110], start=200, end=330, fill=(255, 208, 40, 200), width=2)
    # Luminous ocean vortex bubbles and sparkles along slash curve
    for pt in [(48, 36), (74, 24), (100, 34), (114, 58), (90, 80)]:
        s_draw.point(pt, fill=(78, 216, 106, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.5))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, claw_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (高壓卸力·硬質裝甲彈刀 / Scale Deflection Shock Absorption)
    # Body recoils backwards (-15, -6), optic core squints in pain (> <),
    # anchor held across chest in reactive parry deflection.
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [31, 26, 58, 255] # dark socket plate
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Draw sharp impact squint "> <" over (52, 40) and (76, 40)
    # Left eye: ">" centered at 52, 40
    draw_ho.line([(48, 37), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(48, 43), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(49, 38), (54, 40)], fill=(210, 255, 225, 255), width=1)
    draw_ho.line([(49, 42), (54, 40)], fill=(210, 255, 225, 255), width=1)
    # Right eye: "<" centered at 76, 40
    draw_ho.line([(80, 37), (73, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(80, 43), (73, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(79, 38), (74, 40)], fill=(210, 255, 225, 255), width=1)
    draw_ho.line([(79, 42), (74, 40)], fill=(210, 255, 225, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(key_src)
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(costume_src)
    body_hit_base.alpha_composite(hit_optic)

    shifts_hit = {
        "head_top": (-15, -6), "ear_l": (-17, -8), "ear_r": (-13, -6),
        "eye_l": (-14, -5), "eye_r": (-14, -5), "snout": (-12, -4), "throat": (-10, -3),
        "core": (-8, -2),
        "shoulder_l": (-8, 0), "arm_l": (-4, 2),
        "shoulder_r": (-5, -2), "arm_r": (2, -3),
        "torso": (-5, 0), "pelvis": (2, 2),
        "hip_l": (-4, 2), "hip_r": (4, 2),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "tail_root": (-8, 4), "tail_mid": (-10, 8), "tail_tip": (-6, 11),
        "key_mount": (-12, -4), "key_wing": (-14, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Anchor placed in defensive parry guard across chest
    claw_hit = place_weapon(weapon_raw, deg=72, target_center=(76, 68), scale=0.96, mirror=False)

    # Deflection impact cross-star spark & expanding shockwave rings at anchor contact point (84, 64)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 84, 64
    # Expanding kinetic shockwave arcs in front of contact point
    h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(56, 160, 255, 210), width=2)
    h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 208, 40, 200), width=2)
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    # Main cross-star spark rays
    h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)
    # Diagonal cyan & amber deflection sparks
    h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(56, 160, 255, 220), width=1)
    h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)
    # Core white hot impact flash
    h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    # Flying metal spark particles around impact
    for pt in [(cx - 18, cy - 8), (cx + 18, cy - 12), (cx - 12, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 16), (cx + 20, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, claw_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (排水復位·通氣冷卻 / Hydro-Pneumatic Venting & Stance Reset)
    # Sinking back down into solid restabilization (+1, +4), anchor relaxed in low-ready
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 4), "ear_l": (0, 4), "ear_r": (2, 4),
        "eye_l": (1, 4), "eye_r": (1, 4), "snout": (1, 4), "throat": (1, 4),
        "core": (1, 4),
        "shoulder_l": (-1, 4), "arm_l": (-2, 4),
        "shoulder_r": (2, 4), "arm_r": (3, 5),
        "torso": (1, 4), "pelvis": (1, 4),
        "hip_l": (-1, 3), "hip_r": (2, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_root": (1, 4), "tail_mid": (1, 5), "tail_tip": (0, 5),
        "key_mount": (2, 3), "key_wing": (2, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Anchor relaxed in low ready position
    claw_rec = place_weapon(weapon_raw, deg=-8, target_center=(92, 82), scale=1.0, mirror=False)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, claw_rec)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    poses = generate_poses()
    print("Poses generated. Testing quality gates...")
    for p, img in poses.items():
        bbox = img.getbbox()
        assert bbox is not None
        left, top, right, bottom = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
        print(f"Pose {p:10s}: bbox={bbox}, margins: L={left}, T={top}, R={right}, B={bottom}")
        assert left >= 4 and top >= 4 and right >= 4 and bottom >= 2, f"Margin fail on {p}"

        # shadow
        arr = np.array(img)
        shadow = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
        assert shadow == EXPECTED_SHADOW, f"Shadow fail on {p}: {shadow} != {EXPECTED_SHADOW}"

    # translation test
    for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
        min_diff = 999999
        for dx in range(-12, 13):
            for dy in range(-12, 13):
                shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
                shifted.paste(poses['idle'], (dx, dy), poses['idle'])
                diff = ImageChops.difference(shifted, poses[p])
                if diff.getbbox() is None:
                    d = 0
                else:
                    d = int(np.sum(np.any(np.array(diff) > 0, axis=-1)))
                if d < min_diff:
                    min_diff = d
        print(f"Pose {p:10s}: min_diff={min_diff}")
        assert min_diff > 400, f"Translation fail on {p}: {min_diff}"

        # changed
        diff = ImageChops.difference(poses['idle'], poses[p])
        ch = int(np.sum(np.any(np.array(diff) > 0, axis=-1)))
        print(f"Pose {p:10s}: changed={ch}")
        assert ch >= 2500, f"Changed fail on {p}: {ch}"

    print("ALL TESTS PASSED IN PROTOTYPE!")
