#!/usr/bin/env python3
"""
tools/build_gorilla_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Steelarm Gorilla (第三十四族 鋼臂巨猩, gorilla)
in Clockwork Heart:
  game/assets/sprites/player/poses/gorilla/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/gorilla/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_73992abf"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/gorilla"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/gorilla"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_gorilla_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_gorilla_heavy_t_forged_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_gorilla_twin_turbo_exhaust_chimney.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_gorilla_brass_heavy_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_gorilla_riveted_brow_crest.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_gorilla_steam_forge_boiler_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_gorilla_dual_gauge_optic_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_gorilla_steam_forging_fist.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# 1b. Cleanly separate ground shadow from chassis so character body is 100% pure
# Boots are at y in 110..116 (left x: 36..56, right x: 72..92). All other pixels at y >= 110 are shadow.
c_arr = np.array(chassis_src)
is_boot = np.zeros((128, 128), dtype=bool)
for y in range(110, 117):
    is_boot[y, 36:57] = (c_arr[y, 36:57, 3] > 180)
    is_boot[y, 72:93] = (c_arr[y, 72:93, 3] > 180)

is_shadow = (c_arr[:, :, 3] > 0) & (np.arange(128)[:, None] >= 110) & (~is_boot)
clean_arr = c_arr.copy()
clean_arr[is_shadow, :] = 0
chassis_clean = Image.fromarray(clean_arr)

# 1c. Construct natural, unclipped, symmetric ground contact shadow ellipse centered at (64, 119)
shadow_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_draw = ImageDraw.Draw(shadow_img)
s_draw.ellipse([26, 116, 102, 123], fill=(31, 26, 58, 210))
shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(0.8))

# Enforce clean boundary margins (L>=4, T>=4, R>=4, B>=2)
sf_arr = np.array(shadow_img)
sf_arr[125:, :, :] = 0  # ensure y >= 125 is strictly 0
for col in [0, 1, 126, 127]:
    sf_arr[:, col, :] = 0
shadow_master = Image.fromarray(sf_arr)

EXPECTED_SHADOW = [int(np.sum(sf_arr[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Benchmark ground shadow row counts (118..127): {EXPECTED_SHADOW}")


def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 without flinching."""
    out = img.copy()
    o_px = out.load()
    s_pixels = shadow_master.load()
    assert o_px is not None and s_pixels is not None

    # Replace rows 117..127 with shadow_master across ALL columns where body is transparent
    # And where shadow_master has shadow, guarantee shadow is solid.
    for y in range(117, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_pixels[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if fp[3] < 200:
                o_px[x, y] = sp

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 2] = (0, 0, 0, 0)
        o_px[x, 3] = (0, 0, 0, 0)
        o_px[x, 125] = (0, 0, 0, 0)
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
    "chimney_l": (51, 17),
    "chimney_r": (77, 17),
    "brow_top": (64, 24),
    "brow_l": (48, 26),
    "brow_r": (80, 26),
    "eye_l": (54, 38),
    "eye_r": (74, 38),
    "chin": (63, 39),
    "throat": (64, 48),
    "boiler_core": (64, 72),
    "shoulder_l": (42, 58),
    "shoulder_r": (82, 58),
    "arm_l": (37, 78),
    "arm_r": (83, 75),
    "hand_r": (88, 73),
    "torso": (64, 78),
    "pelvis": (64, 92),
    "crotch": (64, 102),
    "hip_l": (48, 96),
    "hip_r": (78, 96),
    "foot_l": (46, 114),
    "foot_r": (79, 114),
    "key_mount": (75, 33),
}

# Base body without weapon and winding key (using chassis_clean)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_clean)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (鋼臂鐵壁·沉穩架勢 / Steelarm Ironwall Stance)
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(77, 31), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(100, 73), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, shadow_master)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (活塞蓄壓·重踏蓄勁 / Steam Boiler Compression & Piston Coil)
    # =========================================================================
    shifts_telegraph = {
        "chimney_l": (-2, 5), "chimney_r": (-2, 5),
        "brow_top": (-2, 6), "brow_l": (-3, 6), "brow_r": (-1, 6),
        "eye_l": (-2, 6), "eye_r": (-2, 6),
        "chin": (-2, 6), "throat": (-2, 6),
        "boiler_core": (-2, 6),
        "shoulder_l": (-1, 5), "shoulder_r": (-3, 5),
        "arm_l": (1, 5), "arm_r": (-5, 5),
        "hand_r": (-6, 3),
        "torso": (-2, 6), "pelvis": (-2, 3),
        "crotch": (-1, 2),
        "hip_l": (-2, 1), "hip_r": (0, 1),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "key_mount": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-26, target_center=(74, 36), scale=1.0)
    fist_tele = place_rotated_element(weapon_raw, deg=-22, target_center=(94, 75), scale=1.04)

    # Clean targeting reticle FX centered on weapon
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    cx, cy = 112, 58
    t_draw.arc([cx - 8, cy - 8, cx + 8, cy + 8], start=20, end=340, fill=(78, 216, 106, 230), width=1)
    t_draw.arc([cx - 4, cy - 4, cx + 4, cy + 4], start=40, end=320, fill=(255, 160, 16, 230), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(94, 73), (112, 58)], fill=(78, 216, 106, 210), width=2)
    t_draw.line([(96, 72), (112, 58)], fill=(255, 255, 255, 255), width=1)
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.3))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, shadow_master)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, fist_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (重錘崩拳·活塞衝壓 / Steam Piston Heavy Sledge Hammer Punch)
    # =========================================================================
    shifts_attack = {
        "chimney_l": (10, 0), "chimney_r": (12, 0),
        "brow_top": (13, 0), "brow_l": (12, 0), "brow_r": (14, 0),
        "eye_l": (13, 0), "eye_r": (13, 0),
        "chin": (14, 0), "throat": (13, 0),
        "boiler_core": (12, 0),
        "shoulder_l": (14, -1), "shoulder_r": (9, 0),
        "arm_l": (15, -2), "arm_r": (-4, 2),
        "hand_r": (14, -3),
        "torso": (11, 0), "pelvis": (6, 0),
        "crotch": (2, 0),
        "hip_l": (3, 0), "hip_r": (-1, 0),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "key_mount": (9, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=48, target_center=(87, 30), scale=1.0)
    # Target center: original (100, 73) + (14, -4) = (114, 69)
    fist_attack = place_rotated_element(weapon_raw, deg=24, target_center=(114, 69), scale=1.06)

    # Clean pneumatic piston thrust & kinetic impact shock rings around punch contact
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    a_draw.line([(86, 73), (122, 67)], fill=(255, 160, 16, 245), width=2)
    a_draw.line([(96, 72), (122, 67)], fill=(255, 255, 255, 255), width=1)
    a_draw.arc([94, 50, 122, 78], start=300, end=60, fill=(255, 208, 40, 235), width=2)
    a_draw.arc([100, 54, 122, 76], start=310, end=50, fill=(230, 57, 70, 240), width=2)
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.3))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, shadow_master)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, fist_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (雙渦輪過載·天罡重工破勢拳 / Twin-Turbo Overdrive Forge Cataclysm)
    # Crotch anchored at (0, 7) so crotch gap remains <= 170px (passing 0-QA16 <= 200px)
    # =========================================================================
    shifts_skill = {
        "chimney_l": (0, 0), "chimney_r": (1, 0),
        "brow_top": (1, -3), "brow_l": (0, -3), "brow_r": (2, -3),
        "eye_l": (1, -3), "eye_r": (1, -3),
        "chin": (1, -3), "throat": (1, -3),
        "boiler_core": (1, -3),
        "shoulder_l": (-2, -3), "shoulder_r": (3, -3),
        "arm_l": (-5, -3), "arm_r": (3, -8),
        "hand_r": (2, -10),
        "torso": (1, -3), "pelvis": (1, 0),
        "crotch": (0, 7),
        "hip_l": (-1, 0), "hip_r": (1, 0),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "key_mount": (2, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=80, target_center=(79, 28), scale=1.0)
    fist_skill = place_rotated_element(weapon_raw, deg=-45, target_center=(102, 59), scale=1.1)

    # Open crescent crest aura strictly in y in 14..68
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_fx)
    sk_draw.arc([26, 16, 102, 70], start=215, end=325, fill=(56, 160, 255, 235), width=2)
    sk_draw.arc([32, 20, 96, 66], start=220, end=320, fill=(78, 216, 106, 220), width=2)
    sk_draw.arc([38, 24, 90, 62], start=225, end=315, fill=(255, 208, 40, 230), width=2)
    # Soft rounded steam puffs venting from chimney mouths (bounded to y in 12..22)
    sk_draw.ellipse([46, 12, 56, 20], fill=(255, 253, 248, 200))
    sk_draw.ellipse([74, 12, 84, 20], fill=(255, 253, 248, 200))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.3))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, shadow_master)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, fist_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊反震·合金框架承載 / Alloy Chassis Kinetic Impact Absorbed)
    # =========================================================================
    shifts_hit = {
        "chimney_l": (-8, -1), "chimney_r": (-7, -1),
        "brow_top": (-9, -1), "brow_l": (-10, -1), "brow_r": (-8, -1),
        "eye_l": (-9, -1), "eye_r": (-9, -1),
        "chin": (-9, -1), "throat": (-8, -1),
        "boiler_core": (-8, 0),
        "shoulder_l": (-9, -1), "shoulder_r": (-6, -1),
        "arm_l": (-5, 3), "arm_r": (-8, 1),
        "hand_r": (-8, 6),
        "torso": (-7, 0), "pelvis": (-4, 0),
        "crotch": (-1, 0),
        "hip_l": (-2, 0), "hip_r": (0, 0),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "key_mount": (-7, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Overlay cute dizzy strain '> <' LEDs on optic eyes:
    hit_eyes = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    he_draw = ImageDraw.Draw(hit_eyes)
    lx, ly = 45, 37
    he_draw.line([(lx - 3, ly - 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 3, ly + 3), (lx + 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(lx - 2, ly - 2), (lx + 1, ly)], fill=(255, 255, 255, 255), width=1)
    rx, ry = 65, 37
    he_draw.line([(rx + 3, ly - 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 3, ly + 3), (rx - 2, ly)], fill=(255, 208, 40, 255), width=2)
    he_draw.line([(rx + 2, ly - 2), (rx - 1, ly)], fill=(255, 255, 255, 255), width=1)

    key_hit = place_rotated_element(key_raw, deg=-28, target_center=(70, 31), scale=1.0)
    fist_hit = place_rotated_element(weapon_raw, deg=24, target_center=(92, 79), scale=1.0)

    # Clean impact spark burst centered on chest plate (58, 68)
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    ix, iy = 58, 68
    h_draw.line([(ix - 12, iy - 8), (ix + 10, iy + 6)], fill=(255, 208, 40, 240), width=2)
    h_draw.line([(ix - 8, iy + 10), (ix + 8, iy - 8)], fill=(230, 57, 70, 230), width=2)
    h_draw.line([(ix - 14, iy), (ix + 12, iy)], fill=(255, 255, 255, 255), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, shadow_master)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_eyes)
    hit_canvas = Image.alpha_composite(hit_canvas, fist_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (洩壓復位·齒輪咬合 / Pressure Relief & Gear Re-mesh)
    # =========================================================================
    shifts_recover = {
        "chimney_l": (-1, 4), "chimney_r": (-1, 4),
        "brow_top": (-1, 5), "brow_l": (-2, 5), "brow_r": (0, 5),
        "eye_l": (-1, 5), "eye_r": (-1, 5),
        "chin": (-1, 5), "throat": (-1, 5),
        "boiler_core": (-1, 5),
        "shoulder_l": (-2, 4), "shoulder_r": (0, 4),
        "arm_l": (1, 4), "arm_r": (-2, 4),
        "hand_r": (-1, 5),
        "torso": (-1, 5), "pelvis": (-1, 2),
        "crotch": (0, 3),
        "hip_l": (-1, 1), "hip_r": (1, 1),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "key_mount": (-1, 4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=16, target_center=(76, 35), scale=1.0)
    fist_rec = place_rotated_element(weapon_raw, deg=-12, target_center=(99, 78), scale=1.0)

    # Gear re-mesh spark at key mount (76, 37)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.line([(73, 34), (79, 40)], fill=(255, 208, 40, 230), width=1)
    r_draw.line([(79, 34), (73, 40)], fill=(255, 255, 255, 255), width=1)
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, shadow_master)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, fist_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


# 2. Main Generation Execution
print("Generating The Steelarm Gorilla combat action poses...")
poses = generate_poses()

for p_name in ['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']:
    im = poses[p_name]
    path_128 = f"{OUT_DIR}/{p_name}.png"
    im.save(path_128)
    print(f"  ✓ Saved 128x128: {path_128}")

    # Generate 512x512 with LANCZOS
    im_512 = im.resize((512, 512), resample=Image.Resampling.LANCZOS)
    path_512 = f"{OUT_DIR}/{p_name}_512.png"
    im_512.save(path_512)
    print(f"  ✓ Saved 512x512 LANCZOS: {path_512}")

# 3. Generate 768x128 composite proof sheet (idle, telegraph, attack, skill, hit, recover)
proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
for idx, p_name in enumerate(proof_order):
    proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

proof_768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_gorilla_combat_poses_768.png"
proof_strip.save(proof_768_path)
print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

# 4. Generate 768x128 magenta background proof sheet for hole detection
proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
proof_magenta.paste(proof_strip, (0, 0), proof_strip)
proof_mag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_gorilla_combat_poses_magenta.png"
proof_magenta.save(proof_mag_path)
print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")
