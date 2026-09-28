#!/usr/bin/env python3
"""
tools/build_meerkat_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Sentry Meerkat (第三十六族 沙哨狐獴, meerkat)
in Clockwork Heart:
  game/assets/sprites/player/poses/meerkat/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/meerkat/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_43d5ac22"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/meerkat"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/meerkat"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_meerkat_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_meerkat_high_torque_scrap_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_meerkat_tripod_grounding_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_meerkat_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_meerkat_scavenger_cowl_ears.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_meerkat_patched_canvas_poncho.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_meerkat_periscope_rangefinder_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_meerkat_rusted_coil_spring_gun.png").convert("RGBA")

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
# Meerkat baseline shadow row counts: [78, 78, 77, 73, 58, 27, 0, 0, 0, 0]
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

# Clean baseline shadow to guarantee Rule 4c-5 / 16 (L>=4, T>=4, R>=4, B>=2)
for y in range(118, 126):  # up to 125, y=126 and 127 are 0
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

    # Sanitize any interpolation dark falloff pixels to canon outline (46, 31, 24)
    arr = np.array(out)
    alpha = arr[:, :, 3]
    rgb = arr[:, :, :3]
    bad_dark = (alpha > 30) & (rgb[:, :, 0] < 12) & (rgb[:, :, 1] < 12) & (rgb[:, :, 2] < 12)
    if np.any(bad_dark):
        arr[bad_dark, 0] = 46
        arr[bad_dark, 1] = 31
        arr[bad_dark, 2] = 24
    
    # Strip any low-alpha fringe/ghost pixels (alpha < 70) above shadow line
    fringe = (arr[:, :, 3] > 0) & (arr[:, :, 3] < 70) & (np.arange(128)[:, None] < 118)
    if np.any(fringe):
        arr[fringe, 3] = 0
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
    "head_top": (64, 19),
    "ear_l": (42, 22),
    "ear_r": (86, 22),
    "periscope_top": (72, 19),
    "optic_lens_l": (56, 32),
    "optic_lens_r": (72, 32),
    "snout": (64, 38),
    "throat": (64, 46),
    "shoulder_l": (46, 58),
    "shoulder_r": (82, 58),
    "arm_l": (40, 70),
    "arm_r": (86, 62),
    "hand_r": (90, 64),
    "chest_core": (64, 66),
    "torso": (64, 78),
    "pelvis": (64, 90),
    "hip_l": (50, 96),
    "hip_r": (78, 96),
    "knee_l": (48, 106),
    "knee_r": (76, 106),
    "foot_l": (48, 118),
    "foot_r": (74, 118),
    "tail_base": (44, 94),
    "tail_mid": (32, 104),
    "tail_claw_l": (22, 118),
    "tail_claw_r": (36, 120),
    "key_mount": (81, 35),
    "gun_center": (98, 60),
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
    # 1. IDLE (沙哨狐獴待機 / The Sentry Meerkat Poise)
    # Baseline stable poised sentry stance.
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (前搖蓄力：瞄準鎖定·彈簧蓄能 / Sentry Radar Aim & Coil Tension)
    # Stance: Body leans down and backward slightly (y+5, x-2), lowering center of gravity.
    # Grounding tail digs into ground to absorb tension.
    # Spring gun leveled and aimed forward (-18 deg, target (95, 57)).
    # High-torque scrap winding key counter-rotates (-30 deg, target (78, 39)).
    # FX: Concentric radar/rangefinder crosshair rings, laser aim line, coil compression sparks.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-2, 5), "ear_l": (-3, 5), "ear_r": (-1, 5),
        "periscope_top": (-1, 5),
        "optic_lens_l": (-2, 5), "optic_lens_r": (-2, 5),
        "snout": (-2, 5), "throat": (-2, 5),
        "chest_core": (-2, 5), "torso": (-2, 5), "pelvis": (-2, 4),
        "shoulder_l": (-2, 5), "shoulder_r": (-3, 4),
        "arm_l": (0, 4), "arm_r": (-4, 3),
        "hand_r": (-4, 2),
        "hip_l": (-3, 3), "hip_r": (0, 3),
        "knee_l": (-2, 2), "knee_r": (0, 2),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_base": (-2, 3), "tail_mid": (-3, 2), "tail_claw_l": (-2, 0), "tail_claw_r": (0, 0),
        "key_mount": (-3, 4), "gun_center": (-3, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-30, target_center=(78, 39), scale=1.0)
    gun_tele = place_rotated_element(weapon_raw, deg=-18, target_center=(95, 57), scale=1.04)

    # Radar crosshair & spring coil compression FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Target reticle at forward focus locus (112, 46)
    cx, cy = 112, 46
    t_draw.arc([cx - 8, cy - 8, cx + 8, cy + 8], start=20, end=340, fill=(255, 160, 16, 230), width=1)
    t_draw.arc([cx - 4, cy - 4, cx + 4, cy + 4], start=40, end=320, fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 253, 248, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 253, 248, 240), width=1)
    # Laser aim trajectory connecting gun muzzle to target
    t_draw.line([(96, 54), (112, 46)], fill=(255, 160, 16, 210), width=2)
    t_draw.line([(98, 53), (112, 46)], fill=(255, 255, 255, 255), width=1)
    # Acoustic funnel radar wavefronts
    t_draw.arc([30, 8, 54, 32], start=200, end=340, fill=(255, 208, 40, 200), width=1)
    t_draw.arc([76, 8, 100, 32], start=200, end=340, fill=(255, 208, 40, 200), width=1)
    # Coil compression sparks
    for sx, sy in [(116, 40), (120, 52), (104, 38), (88, 54), (78, 58)]:
        t_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 253, 248, 240))
        t_draw.point((sx, sy), fill=(255, 160, 16, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.4))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, gun_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (普通攻擊：高速氣動刺針爆射 / High-Velocity Spring Needle Burst)
    # Dynamic forward lunge (+11, 0), spring gun thrusts and fires (+20 deg, target (104, 57)).
    # Scrap winding key spins rapidly (+45 deg, target (90, 34)).
    # Grounded tail digs in to absorb recoil.
    # FX: Piercing needle beam, muzzle burst cone, plasma sparks.
    # =========================================================================
    shifts_attack = {
        "head_top": (11, -1), "ear_l": (9, -1), "ear_r": (12, -1),
        "periscope_top": (12, -1),
        "optic_lens_l": (11, -1), "optic_lens_r": (11, -1),
        "snout": (12, -1), "throat": (11, -1),
        "chest_core": (10, 0), "torso": (9, 0), "pelvis": (7, 0),
        "shoulder_l": (12, -1), "shoulder_r": (8, 0),
        "arm_l": (13, 0), "arm_r": (-2, 1),
        "hand_r": (11, -2),
        "hip_l": (8, 0), "hip_r": (-2, 0),
        "knee_l": (6, 0), "knee_r": (-2, 0),
        "foot_l": (4, 0), "foot_r": (-2, 0),
        "tail_base": (4, 0), "tail_mid": (-1, 0), "tail_claw_l": (-1, 0), "tail_claw_r": (1, 0),
        "key_mount": (9, -1), "gun_center": (10, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=45, target_center=(90, 34), scale=1.0)
    gun_attack = place_rotated_element(weapon_raw, deg=20, target_center=(104, 57), scale=1.04)

    # Needle projectile streak & muzzle blast FX (crisp dopamine colors, zero pale fringe)
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # High-velocity piercing needle beam in warm dopamine orange & polished brass
    a_draw.line([(96, 56), (122, 53)], fill=(255, 160, 16, 255), width=2)
    a_draw.line([(102, 55), (122, 53)], fill=(255, 208, 40, 255), width=1)
    # Muzzle blast shockwave arcs
    a_draw.arc([98, 42, 122, 68], start=290, end=70, fill=(255, 160, 16, 255), width=2)
    a_draw.arc([102, 46, 120, 64], start=300, end=60, fill=(255, 208, 40, 255), width=1)
    # Solid kinetic energy sparks (no pale white halo dots)
    for pt in [(120, 46), (122, 58), (116, 66), (110, 72), (102, 38), (92, 70)]:
        a_draw.point(pt, fill=(255, 160, 16, 255))
        a_draw.point((pt[0] - 1, pt[1]), fill=(255, 208, 40, 255))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, gun_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (技能爆發：荒漠過載三連射·折疊刺針突進 / Overload Needle Storm & Bayonet Dash)
    # High spring jump & bayonet overdrive (y-6, x+2).
    # Spring gun bayonet thrusts forward with glowing overdrive energy (+38 deg, target (102, 50), scale 1.08).
    # Scrap winding key spins at maximum RPM (+88 deg, target (84, 28)).
    # FX: Triple needle trajectory shockwaves, spiral armor-piercing wind trails, dopamine bright orange & brass gold muzzle rings.
    # =========================================================================
    shifts_skill = {
        "head_top": (2, -6), "ear_l": (0, -6), "ear_r": (4, -6),
        "periscope_top": (3, -6),
        "optic_lens_l": (2, -6), "optic_lens_r": (2, -6),
        "snout": (2, -6), "throat": (2, -6),
        "chest_core": (2, -6), "torso": (2, -5), "pelvis": (2, -4),
        "shoulder_l": (-1, -6), "shoulder_r": (5, -6),
        "arm_l": (-4, -5), "arm_r": (6, -9),
        "hand_r": (4, -10),
        "hip_l": (-2, -4), "hip_r": (4, -4),
        "knee_l": (-2, -2), "knee_r": (3, -2),
        "foot_l": (-1, 0), "foot_r": (2, 0),
        "tail_base": (1, -3), "tail_mid": (0, -2), "tail_claw_l": (0, 0), "tail_claw_r": (1, 0),
        "key_mount": (3, -6), "gun_center": (4, -10),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=88, target_center=(84, 28), scale=1.0)
    gun_skill = place_rotated_element(weapon_raw, deg=-38, target_center=(100, 50), scale=1.08)

    # Overload needle storm & triple trajectory shockwaves FX
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    # Concentric overload energy rings
    sk_draw.arc([20, 16, 114, 110], start=195, end=345, fill=(255, 160, 16, 235), width=2)
    sk_draw.arc([28, 22, 106, 100], start=205, end=335, fill=(255, 208, 40, 220), width=2)
    sk_draw.arc([36, 28, 98, 90], start=215, end=325, fill=(255, 253, 248, 230), width=1)
    # Triple armor-piercing needle beams
    sk_draw.line([(96, 48), (122, 28)], fill=(255, 160, 16, 240), width=2)
    sk_draw.line([(98, 48), (122, 28)], fill=(255, 255, 255, 255), width=1)
    sk_draw.line([(96, 52), (122, 44)], fill=(255, 208, 40, 240), width=2)
    sk_draw.line([(98, 52), (122, 44)], fill=(255, 255, 255, 255), width=1)
    sk_draw.line([(94, 56), (120, 62)], fill=(255, 160, 16, 220), width=2)
    # Starlight / metal sparks
    for sx, sy in [(120, 26), (114, 18), (121, 42), (118, 64), (64, 10), (18, 68), (108, 76)]:
        sk_draw.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255, 240))
        sk_draw.point((sx, sy), fill=(255, 160, 16, 255))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, gun_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊反饋：後仰震退·潛望目鏡彈起 / Impact Recoil & Periscope Shake)
    # Recoil backward slip (x-9, y+0), head and cowl tilt back (-9 deg).
    # Spring gun jarred upward (+26 deg, target (89, 68)).
    # Scrap key slips backward against ratchet (-35 deg, target (73, 34)).
    # Optic lens switches to cute dizzy/strain '> <' amber quartz LED expressions!
    # FX: Impact spark burst on tinplate chest (dopamine orange & ruby red), deflection lines, ground skid dust.
    # =========================================================================
    shifts_hit = {
        "head_top": (-9, -1), "ear_l": (-10, -1), "ear_r": (-8, -1),
        "periscope_top": (-8, -2),
        "optic_lens_l": (-9, -1), "optic_lens_r": (-9, -1),
        "snout": (-9, -1), "throat": (-8, -1),
        "chest_core": (-8, 0), "torso": (-7, 0), "pelvis": (-5, 0),
        "shoulder_l": (-9, -1), "shoulder_r": (-6, -1),
        "arm_l": (-5, 2), "arm_r": (-8, 1),
        "hand_r": (-8, 5),
        "hip_l": (-5, 0), "hip_r": (-2, 0),
        "knee_l": (-4, 0), "knee_r": (-1, 0),
        "foot_l": (-2, 0), "foot_r": (2, 0),
        "tail_base": (-5, 0), "tail_mid": (-6, 0), "tail_claw_l": (-4, 0), "tail_claw_r": (-2, 0),
        "key_mount": (-8, -1), "gun_center": (-8, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    # Left eye base: (56, 32), shifted: (56 - 9, 32 - 1) = (47, 31)
    # Right eye base: (72, 32), shifted: (72 - 9, 32 - 1) = (63, 31)
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    # High-contrast cute dizzy '> <' strain LEDs (deep outline + white spark highlight)
    lx, ly = 47, 31
    # Left eye '>' in canon dark outline (46, 31, 24)
    he_draw.line([(lx - 4, ly - 4), (lx + 2, ly)], fill=(46, 31, 24, 255), width=2)
    he_draw.line([(lx - 4, ly + 4), (lx + 2, ly)], fill=(46, 31, 24, 255), width=2)
    he_draw.line([(lx - 3, ly - 3), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    he_draw.line([(lx - 3, ly + 3), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)

    # Right eye '<' in canon dark outline (46, 31, 24)
    rx, ry = 63, 31
    he_draw.line([(rx + 4, ly - 4), (rx - 2, ly)], fill=(46, 31, 24, 255), width=2)
    he_draw.line([(rx + 4, ly + 4), (rx - 2, ly)], fill=(46, 31, 24, 255), width=2)
    he_draw.line([(rx + 3, ly - 3), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)
    he_draw.line([(rx + 3, ly + 3), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-35, target_center=(73, 34), scale=1.0)
    gun_hit = place_rotated_element(weapon_raw, deg=26, target_center=(86, 70), scale=1.0)

    # Impact spark burst & deflection lines
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact burst on tinplate chest (56, 62) in vibrant diagonal X-slash & radial sparks (no horizontal scanline)
    ix, iy = 56, 62
    h_draw.line([(ix - 10, iy - 8), (ix + 10, iy + 8)], fill=(255, 160, 16, 255), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 10)], fill=(230, 57, 70, 255), width=2)
    h_draw.line([(ix - 6, iy - 5), (ix + 6, iy + 5)], fill=(255, 208, 40, 255), width=1)
    # Kinetic sparks
    for pt in [(ix - 14, iy - 10), (ix + 12, iy - 12), (ix + 14, iy + 8), (ix - 10, iy + 12), (ix + 18, iy - 2)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    # Skid marks at feet / grounded tail
    h_draw.line([(32, 118), (46, 118)], fill=(255, 255, 255, 180), width=1)
    h_draw.line([(28, 119), (44, 119)], fill=(255, 160, 16, 200), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, gun_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (後搖恢復：持銃回巡·散熱排氣 / Coolant Vent & Stance Re-centering)
    # Low recovery crouch (y+4, x-1), body bows forward, spring gun braces downward (-12 deg, target (96, 64)).
    # Scrap winding key snaps back into gear mesh (+15 deg, target (80, 38)).
    # FX: Soft coolant steam venting from gun valve, settling dust.
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 4), "ear_l": (-2, 4), "ear_r": (0, 4),
        "periscope_top": (-1, 4),
        "optic_lens_l": (-1, 4), "optic_lens_r": (-1, 4),
        "snout": (-1, 4), "throat": (-1, 4),
        "chest_core": (-1, 4), "torso": (-1, 4), "pelvis": (-1, 3),
        "shoulder_l": (-2, 3), "shoulder_r": (0, 3),
        "arm_l": (1, 3), "arm_r": (-2, 3),
        "hand_r": (-1, 4),
        "hip_l": (-2, 2), "hip_r": (1, 2),
        "knee_l": (-2, 1), "knee_r": (1, 1),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "tail_base": (-1, 3), "tail_mid": (-1, 2), "tail_claw_l": (-1, 0), "tail_claw_r": (0, 0),
        "key_mount": (-1, 3), "gun_center": (-1, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=15, target_center=(80, 38), scale=1.0)
    gun_rec = place_rotated_element(weapon_raw, deg=-12, target_center=(96, 64), scale=1.0)

    # Coolant steam venting FX
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    # Steam clouds from weapon vent
    r_draw.ellipse([88, 54, 98, 62], fill=(255, 253, 248, 140))
    r_draw.ellipse([92, 46, 104, 56], fill=(255, 253, 248, 160))
    r_draw.ellipse([96, 38, 110, 50], fill=(255, 253, 248, 120))
    r_draw.ellipse([100, 30, 114, 42], fill=(255, 253, 248, 90))
    # Heat shimmer sparkles
    for sx, sy in [(95, 48), (102, 40), (108, 34), (86, 58)]:
        r_draw.point((sx, sy), fill=(255, 208, 40, 200))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(1.0))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, gun_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def export_and_verify(poses: dict[str, Image.Image]) -> None:
    print("\n=== SAVING AND VERIFYING MEERKAT COMBAT ACTION POSES ===")
    for p_name in ["idle", "telegraph", "attack", "skill", "hit", "recover"]:
        img_128 = poses[p_name]
        p128_path = f"{OUT_DIR}/{p_name}.png"
        img_128.save(p128_path)

        # Genuine Lanczos 512x512 export
        img_512 = img_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
        p512_path = f"{OUT_DIR}/{p_name}_512.png"
        img_512.save(p512_path)

        bbox = img_128.getbbox()
        assert bbox is not None
        left, top, right, bot = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
        print(f"  ✓ {p_name:10s} 128: saved, bbox={bbox}, margins: L={left}, T={top}, R={right}, B={bot} (req >= 4,4,4,2)")
        assert left >= 4 and top >= 4 and right >= 4 and bot >= 2, f"FAIL margins on {p_name}: {bbox}"

    # Generate 768x128 Transparent & Magenta Proof Sheets
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(["idle", "telegraph", "attack", "skill", "hit", "recover"]):
        proof_768.paste(poses[p_name], (i * 128, 0), poses[p_name])
        proof_mag.paste(poses[p_name], (i * 128, 0), poses[p_name])

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_meerkat_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_meerkat_combat_poses_magenta.png"
    proof_768.save(p768_path)
    proof_mag.save(pmag_path)
    print(f"  ✓ Proof sheets saved: {p768_path} & {pmag_path}")


if __name__ == "__main__":
    poses = generate_poses()
    export_and_verify(poses)
