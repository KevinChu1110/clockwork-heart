#!/usr/bin/env python3
"""
tools/build_cat_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Umbral Cat (幽影貓, 17th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/cat/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/cat/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/cat"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/cat"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_cat_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_cat_crescent_twin_ring_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_cat_segmented_gyro_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_cat_obsidian_steel_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_cat_brass_acoustic_ears.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_cat_skyspire_prowler_vest.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_cat_slit_optic_emerald.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_cat_shadowspring_stiletto.png").convert("RGBA")

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
stiletto_raw = weapon_src.crop(wpn_bbox)

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

def place_stiletto(stiletto_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Shadowspring Stiletto with zero clipping."""
    b = stiletto_img.copy()
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
    "ear_l": (36, 16),
    "ear_r": (92, 16),
    "eye_l": (54, 40),
    "eye_r": (74, 40),
    "snout": (64, 46),
    "throat": (64, 54),
    "core": (64, 64),
    "shoulder_l": (46, 62),
    "shoulder_r": (82, 62),
    "arm_l": (36, 70),
    "arm_r": (90, 72),
    "torso": (64, 74),
    "pelvis": (64, 88),
    "hip_l": (50, 94),
    "hip_r": (78, 94),
    "foot_l": (46, 114),
    "foot_r": (82, 114),
    "tail_root": (46, 82),
    "tail_mid": (28, 62),
    "tail_tip": (32, 42),
    "key_mount": (74, 46),
    "key_wing": (88, 36),
}

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline Ninja Ready Pose)
    # Stiletto held in right hand in balanced ready guard
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (暗影伏擊蓄力·雙環鎖定 / Shadow Ambush Crouch & Crescent Lock)
    # Deep feline ninja crouch (y+8, x-2), ears folded alertly, tail swept low
    # Stiletto drawn back close in reverse grip ready for explosive spring release
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 8), "ear_l": (-4, 8), "ear_r": (1, 8),
        "eye_l": (-2, 8), "eye_r": (-2, 8), "snout": (-2, 8), "throat": (-2, 8),
        "core": (-2, 8),
        "shoulder_l": (-1, 7), "arm_l": (3, 6),
        "shoulder_r": (-4, 7), "arm_r": (-8, 6),
        "torso": (-2, 8), "pelvis": (-2, 8),
        "hip_l": (-4, 6), "hip_r": (3, 6),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_root": (-2, 6), "tail_mid": (-6, 7), "tail_tip": (-7, 6),
        "key_mount": (-2, 7), "key_wing": (-3, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Stiletto drawn back in tight reverse grip ready to spring
    stiletto_tele = place_stiletto(stiletto_raw, deg=-30, target_center=(78, 80), scale=1.02, mirror=False)

    # Stealth Aiming Reticle & Emerald Targeting Pulse FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Targeting trajectory line from dagger tip forward-right
    t_draw.line([(76, 78), (114, 58)], fill=(78, 216, 106, 210), width=1)
    t_draw.line([(88, 71), (118, 56)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(96, 67), (120, 55)], fill=(255, 255, 255, 255), width=1)
    # Concentric crescent aiming reticle at (110, 56)
    cx, cy = 110, 56
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(78, 216, 106, 230), width=1)
    t_draw.line([(cx - 12, cy), (cx + 12, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 12), (cx, cy + 12)], fill=(255, 208, 40, 240), width=1)
    # Acoustic ear sweep radar arcs
    t_draw.arc([24, 14, 56, 42], start=210, end=350, fill=(78, 216, 106, 190), width=2)
    t_draw.arc([68, 14, 100, 42], start=190, end=330, fill=(255, 208, 40, 200), width=2)
    # Crescent key torque tension spark
    t_draw.arc([74, 38, 98, 62], start=20, end=340, fill=(255, 160, 16, 210), width=2)
    # Emerald optic slit glow
    t_draw.ellipse([50, 46, 56, 52], fill=(78, 216, 106, 230))
    t_draw.ellipse([70, 46, 76, 52], fill=(78, 216, 106, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, stiletto_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (夜行瞬殺·袖刃突刺 / Nightprowl Shadow Thrust)
    # Explosive ninja dash/thrust: torso rocks forward (+13, -1), right arm
    # drives stiletto forward in a supersonic piercing thrust!
    # Gyro tail balances horizontally (+4, -4).
    # =========================================================================
    shifts_attack = {
        "head_top": (13, -1), "ear_l": (10, -2), "ear_r": (15, -1),
        "eye_l": (14, -1), "eye_r": (14, -1), "snout": (15, 0), "throat": (14, 0),
        "core": (13, 0),
        "shoulder_l": (14, -1), "arm_l": (18, -2),
        "shoulder_r": (4, 0), "arm_r": (16, -2),
        "torso": (12, 0), "pelvis": (9, 0),
        "hip_l": (11, -1), "hip_r": (-5, 0),
        "foot_l": (6, 0), "foot_r": (-6, 0),
        "tail_root": (8, 0), "tail_mid": (4, -4), "tail_tip": (2, -6),
        "key_mount": (10, 0), "key_wing": (8, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Stiletto thrust forward horizontally
    stiletto_attack = place_stiletto(stiletto_raw, deg=15, target_center=(98, 72), scale=1.06, mirror=False)

    # Supersonic Shadow Stiletto Beam & Kinetic Crescent Rings
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Main piercing blade beam from stiletto tip to edge
    a_draw.line([(96, 72), (122, 72)], fill=(78, 216, 106, 245), width=3)
    a_draw.line([(98, 72), (124, 72)], fill=(255, 255, 255, 255), width=1)
    # Piercing arrowhead / stiletto edge tip
    a_draw.polygon([(124, 72), (116, 67), (118, 72), (116, 77)], fill=(255, 208, 40, 255))
    # Expanding kinetic shockwave cones in front
    a_draw.arc([98, 58, 116, 86], start=275, end=85, fill=(78, 216, 106, 220), width=2)
    a_draw.arc([106, 54, 122, 90], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    # Stiletto escapement trigger flash at hilt (94, 72)
    a_draw.ellipse([(90, 68), (98, 76)], fill=(255, 255, 220, 255))
    a_draw.point([(92, 66), (96, 66), (92, 78), (96, 78), (100, 72)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, stiletto_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (幻影九節·百裂暗刃殺 / Nine-Segment Phantom Blade Flurry)
    # Acrobatic leaping strike! Torso raises (-1, -7), ears flare high,
    # gyro tail curls overhead like an articulated whip (-4, -12),
    # right arm slashes down with stiletto from high angle (+4, -10)
    # =========================================================================
    shifts_skill = {
        "head_top": (1, -7), "ear_l": (-2, -8), "ear_r": (3, -7),
        "eye_l": (1, -7), "eye_r": (1, -7), "snout": (1, -6), "throat": (1, -6),
        "core": (1, -6),
        "shoulder_l": (-2, -6), "arm_l": (-6, -4),
        "shoulder_r": (3, -6), "arm_r": (6, -9),
        "torso": (0, -6), "pelvis": (0, -5),
        "hip_l": (-3, -4), "hip_r": (3, -4),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_root": (-2, -5), "tail_mid": (-4, -10), "tail_tip": (-2, -14),
        "key_mount": (1, -6), "key_wing": (3, -7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Stiletto held overhead slashing down diagonally
    stiletto_skill = place_stiletto(stiletto_raw, deg=-45, target_center=(88, 54), scale=1.08, mirror=False)

    # Phantom Shadow Blade Flurry FX (dual crescent emerald slashes & afterimages)
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Primary emerald crescent slash arc
    s_draw.arc([40, 24, 116, 100], start=220, end=350, fill=(78, 216, 106, 230), width=3)
    s_draw.arc([44, 28, 112, 96], start=225, end=345, fill=(255, 255, 255, 255), width=1)
    # Secondary intersecting cyan slash arc
    s_draw.arc([32, 36, 108, 112], start=200, end=330, fill=(56, 160, 255, 200), width=2)
    # Golden escapement gear sparkles along slash curve
    for pt in [(50, 40), (76, 28), (102, 38), (114, 62), (90, 84)]:
        s_draw.point(pt, fill=(255, 208, 40, 255))
        s_draw.ellipse([pt[0]-1, pt[1]-1, pt[0]+1, pt[1]+1], fill=(255, 255, 255, 220))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.5))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, stiletto_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (鋼索偏轉·受擊卸力 / Gyro Deflection Shock Absorption)
    # Mechanical ratchet absorption stance: body pitches back and recoils (-16, -6),
    # optic core squints in pain/impact (> <), ears flattened in defensive alignment.
    # Deflection cross-star spark & expanding kinetic shockwave rings at blade edge (84, 62).
    # =========================================================================
    # Hit squint optic layer (> <)
    optic_arr = np.array(optic_src)
    mask = optic_arr[:, :, 3] > 20
    hit_optic = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_arr = np.array(hit_optic)
    h_arr[mask] = [30, 32, 42, 255] # dark socket plate
    hit_optic = Image.fromarray(h_arr)
    draw_ho = ImageDraw.Draw(hit_optic)
    # Draw sharp impact squint "> <"
    draw_ho.line([(48, 37), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(48, 43), (55, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(49, 38), (54, 40)], fill=(255, 255, 230, 255), width=1)
    draw_ho.line([(49, 42), (54, 40)], fill=(255, 255, 230, 255), width=1)
    draw_ho.line([(79, 37), (72, 40)], fill=(78, 216, 106, 255), width=2)
    draw_ho.line([(79, 43), (72, 40)], fill=(78, 216, 106, 255), width=2)
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
        "shoulder_r": (-6, -2), "arm_r": (2, -3),
        "torso": (-5, 0), "pelvis": (2, 2),
        "hip_l": (-4, 2), "hip_r": (4, 2),
        "foot_l": (-3, 0), "foot_r": (2, 0),
        "tail_root": (-8, 4), "tail_mid": (-10, 8), "tail_tip": (-6, 12),
        "key_mount": (-12, -4), "key_wing": (-14, -6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_hit_base, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Stiletto placed in vertical parry guard at right edge of torso (76, 66)
    stiletto_hit = place_stiletto(stiletto_raw, deg=75, target_center=(76, 66), scale=0.96, mirror=False)

    # Deflection impact cross-star spark & expanding shockwave rings at blade edge (84, 62)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 84, 62
    # Expanding kinetic shockwave arcs in front of blade contact point
    h_draw.arc([cx - 22, cy - 22, cx + 22, cy + 22], start=280, end=80, fill=(78, 216, 106, 210), width=2)
    h_draw.arc([cx - 28, cy - 28, cx + 28, cy + 28], start=290, end=70, fill=(255, 208, 40, 200), width=2)
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 220), width=2)
    # Main cross-star spark rays
    h_draw.line([(cx - 18, cy), (cx + 18, cy)], fill=(255, 255, 230, 245), width=2)
    h_draw.line([(cx, cy - 18), (cx, cy + 18)], fill=(255, 255, 230, 245), width=2)
    # Diagonal emerald & amber deflection sparks
    h_draw.line([(cx - 11, cy - 11), (cx + 11, cy + 11)], fill=(78, 216, 106, 220), width=1)
    h_draw.line([(cx - 11, cy + 11), (cx + 11, cy - 11)], fill=(255, 208, 40, 220), width=1)
    # Core white hot impact flash
    h_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=(255, 255, 255, 255))
    # Flying metal spark particles
    for pt in [(cx - 20, cy - 8), (cx + 18, cy - 14), (cx - 14, cy + 16), (cx + 16, cy + 14), (cx - 8, cy - 18), (cx + 20, cy + 6)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.point((pt[0]+1, pt[1]), fill=(255, 255, 255, 230))
    # Kinetic exhaust steam from back damper (32, 60)
    h_draw.line([(32, 60), (16, 56)], fill=(230, 240, 255, 170), width=2)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, stiletto_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (落地定軸·回簧歸位 / Stance Settlement & Spring Return)
    # Sinking back down into solid restabilization (+1, +4), tail settles low
    # Stiletto relaxed in low-ready resting posture
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
    # Stiletto relaxed in low ready position
    stiletto_rec = place_stiletto(stiletto_raw, deg=-8, target_center=(88, 82), scale=1.0, mirror=False)

    # Subtle cooling steam from back vent only (x: 88..98, y: 52..62), ZERO steam on face or ground
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.ellipse([88, 52, 98, 62], fill=(230, 240, 250, 140))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, stiletto_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING THE UMBRAL CAT 6 COMBAT ACTION POSES ===")
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_cat_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_cat_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
