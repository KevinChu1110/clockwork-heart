#!/usr/bin/env python3
"""
tools/build_pangolin_combat_poses.py
Generates the complete, definitive 6 combat action poses for Sandscale Pangolin (沙鱗穿山甲, 18th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/pangolin/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/pangolin/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/pangolin"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_pangolin_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_pangolin_segmented_scale_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_pangolin_dune_orange_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_pangolin_brass_acoustic_ears.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_pangolin_scavenger_tinker_vest.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_pangolin_sky_blue_optic_domes.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_pangolin_dune_drill_claw.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(optic_src)
body_no_weapon.alpha_composite(costume_src)

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
claw_raw = weapon_src.crop(wpn_bbox)

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

def place_claw(claw_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Dune Drill Claw with zero clipping."""
    b = claw_img.copy()
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
    "head_top": (64, 18),
    "ear_l": (46, 22),
    "ear_r": (82, 22),
    "eye_l": (55, 40),
    "eye_r": (72, 40),
    "snout": (64, 48),
    "throat": (64, 56),
    "core": (63, 73),
    "shoulder_l": (46, 68),
    "shoulder_r": (80, 68),
    "arm_l": (38, 76),
    "arm_r": (88, 76),
    "torso": (63, 80),
    "pelvis": (63, 92),
    "hip_l": (48, 96),
    "hip_r": (78, 96),
    "foot_l": (46, 114),
    "foot_r": (80, 114),
    "tail_root": (42, 88),
    "tail_mid": (28, 95),
    "tail_tip": (18, 98),
    "key_mount": (74, 48),
    "key_wing": (88, 36),
}

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (沙鱗防衛姿態 / Baseline Dune Sentry Ready Pose)
    # Sturdy 4-pillar stance, drill claw readied forward, scale tail resting stably
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (渦輪蓄能·掘地伏擊 / Turbo Pre-Ignition & Burrow Stance)
    # Deep burrowing crouch (y+8, x-2), head down, acoustic ears folded back,
    # scale tail curling low and tight to ground to brace recoil.
    # Drill claw spun back close to chest with glowing turbo reticle and aim laser!
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 8), "ear_l": (-4, 7), "ear_r": (0, 7),
        "eye_l": (-2, 8), "eye_r": (-2, 8), "snout": (-2, 8), "throat": (-2, 8),
        "core": (-2, 8),
        "shoulder_l": (-2, 7), "arm_l": (1, 6),
        "shoulder_r": (-4, 7), "arm_r": (-7, 6),
        "torso": (-2, 8), "pelvis": (-2, 8),
        "hip_l": (-5, 6), "hip_r": (4, 6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_root": (-3, 6), "tail_mid": (-7, 8), "tail_tip": (-9, 7),
        "key_mount": (-2, 7), "key_wing": (-3, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Drill claw drawn back in tight reverse grip ready to erupt
    claw_tele = place_claw(claw_raw, deg=-30, target_center=(80, 84), scale=1.02, mirror=False)

    # Turbo charging kinetic lines, golden torque ring, and cyan optic beam FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Trajectory aim line from drill tip forward-right
    t_draw.line([(78, 82), (114, 62)], fill=(56, 160, 255, 210), width=1)
    t_draw.line([(86, 75), (118, 58)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(94, 70), (120, 56)], fill=(255, 255, 255, 255), width=1)
    # Concentric charging reticle at (110, 58)
    cx, cy = 110, 58
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(56, 160, 255, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(255, 208, 40, 240), width=1)
    # Acoustic ear sound sweep radar arcs
    t_draw.arc([28, 22, 60, 50], start=210, end=350, fill=(56, 160, 255, 190), width=2)
    t_draw.arc([68, 22, 100, 50], start=190, end=330, fill=(255, 208, 40, 200), width=2)
    # Spiral key torque tension spark
    t_draw.arc([76, 44, 98, 66], start=20, end=340, fill=(255, 160, 16, 210), width=2)
    # Cyan optic glow
    t_draw.ellipse([51, 45, 57, 51], fill=(56, 160, 255, 230))
    t_draw.ellipse([68, 45, 74, 51], fill=(56, 160, 255, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, claw_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (破甲鑽擊·渦輪轟爆 / Turbo Drill Breaker & Sand Burst)
    # Explosive forward thrust/dash: torso rocks forward (+13, -1), right arm
    # drives drill claw straight forward into enemy defenses at high speed!
    # Tail sweeps horizontally backward in counterbalance (+6, -5).
    # =========================================================================
    shifts_attack = {
        "head_top": (13, -1), "ear_l": (11, -2), "ear_r": (15, -1),
        "eye_l": (14, -1), "eye_r": (14, -1), "snout": (15, 0), "throat": (14, 0),
        "core": (13, 0),
        "shoulder_l": (14, -1), "arm_l": (17, -2),
        "shoulder_r": (4, 0), "arm_r": (16, -2),
        "torso": (12, 0), "pelvis": (9, 0),
        "hip_l": (11, -1), "hip_r": (-5, 0),
        "foot_l": (6, 0), "foot_r": (-6, 0),
        "tail_root": (8, -2), "tail_mid": (5, -5), "tail_tip": (3, -8),
        "key_mount": (10, 0), "key_wing": (8, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Drill claw thrust forward horizontally
    claw_attack = place_claw(claw_raw, deg=14, target_center=(100, 75), scale=1.06, mirror=False)

    # Supersonic Drill Vortex Cone & Kinetic Shockwave Cones
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Main piercing drill beam from claw tip forward
    a_draw.line([(96, 75), (122, 75)], fill=(56, 160, 255, 245), width=3)
    a_draw.line([(98, 75), (124, 75)], fill=(255, 255, 255, 255), width=1)
    # Piercing arrowhead / drill edge tip
    a_draw.polygon([(124, 75), (116, 70), (118, 75), (116, 80)], fill=(255, 208, 40, 255))
    # Expanding kinetic shockwave cones in front
    a_draw.arc([98, 61, 116, 89], start=275, end=85, fill=(56, 160, 255, 220), width=2)
    a_draw.arc([106, 57, 122, 93], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    # Drill escapement trigger flash at wrist/gauntlet
    a_draw.ellipse([(92, 71), (100, 79)], fill=(255, 255, 220, 255))
    a_draw.point([(94, 69), (98, 69), (94, 81), (98, 81), (102, 75)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, claw_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (巨岩破空·重踏大地 / Earthshaker Quake & Grand Drill Flurry)
    # Acrobatic heavyweight leap & downward drill slam! Torso raises/leaps up (0, -8),
    # tail whips overhead (-4, -13), drill claw raised high and slamming down diagonally.
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
        "tail_root": (-3, -6), "tail_mid": (-6, -11), "tail_tip": (-4, -15),
        "key_mount": (1, -7), "key_wing": (3, -8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Drill claw held overhead slamming down diagonally
    claw_skill = place_claw(claw_raw, deg=-48, target_center=(88, 52), scale=1.08, mirror=False)

    # Grand Drill Slam FX (dual crescent cyan & gold slashes & kinetic impact sparks)
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Primary cyan crescent slash arc
    s_draw.arc([40, 22, 116, 98], start=220, end=350, fill=(56, 160, 255, 230), width=3)
    s_draw.arc([44, 26, 112, 94], start=225, end=345, fill=(255, 255, 255, 255), width=1)
    # Secondary intersecting golden slash arc
    s_draw.arc([32, 34, 108, 110], start=200, end=330, fill=(255, 208, 40, 200), width=2)
    # Golden escapement gear sparkles along slash curve
    for pt in [(50, 38), (76, 26), (102, 36), (114, 60), (90, 82)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.5))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, claw_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (鋼甲卸力·鱗甲偏轉 / Scale Deflection Shock Absorption)
    # Mechanical ratchet absorption stance: body pitches back and recoils (-16, -6),
    # optic core squints in pain/impact (> <), acoustic ears flattened in defensive alignment.
    # NO floating line artifacts.
    # =========================================================================
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [32, 34, 46, 255] # dark socket plate
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Draw sharp impact squint "> <"
    draw_ho.line([(48, 37), (55, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(48, 43), (55, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(49, 38), (54, 40)], fill=(255, 255, 230, 255), width=1)
    draw_ho.line([(49, 42), (54, 40)], fill=(255, 255, 230, 255), width=1)
    draw_ho.line([(79, 37), (72, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(79, 43), (72, 40)], fill=(56, 160, 255, 255), width=2)
    draw_ho.line([(78, 38), (73, 40)], fill=(255, 255, 230, 255), width=1)
    draw_ho.line([(78, 42), (73, 40)], fill=(255, 255, 230, 255), width=1)

    body_hit_base = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    body_hit_base.alpha_composite(key_src)
    body_hit_base.alpha_composite(curio_src)
    body_hit_base.alpha_composite(chassis_src)
    body_hit_base.alpha_composite(head_src)
    body_hit_base.alpha_composite(hit_optic)
    body_hit_base.alpha_composite(costume_src)

    shifts_hit = {
        "head_top": (-16, -6), "ear_l": (-18, -8), "ear_r": (-14, -6),
        "eye_l": (-15, -5), "eye_r": (-15, -5), "snout": (-13, -4), "throat": (-11, -3),
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
    # Claw placed in parry guard across chest
    claw_hit = place_claw(claw_raw, deg=72, target_center=(76, 68), scale=0.96, mirror=False)

    # Deflection impact cross-star spark & expanding shockwave rings at gauntlet contact point (84, 64)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 84, 64
    # Expanding kinetic shockwave arcs in front of claw contact point
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
    # 6. RECOVER (定軸復位·蒸氣排熱 / Recoil Venting & Stance Reset)
    # Sinking back down into solid restabilization (+1, +4), tail settles low
    # Drill claw relaxed in low-ready resting posture
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
    # Claw relaxed in low ready position
    claw_rec = place_claw(claw_raw, deg=-8, target_center=(92, 82), scale=1.0, mirror=False)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, claw_rec)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING SANDSCALE PANGOLIN 6 COMBAT ACTION POSES ===")
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_pangolin_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_pangolin_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
