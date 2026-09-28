#!/usr/bin/env python3
"""
tools/build_capybara_combat_poses.py
Generates the complete 6 combat action poses for The Serene Capybara (第四十七族 澄心水豚, capybara)
in Clockwork Heart:
  game/assets/sprites/player/poses/capybara/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/capybara/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates (0-QA16, 0-QA31, Rule 4b-4/5/7, Rule 4c-5/16).
Preserves pure toy aesthetics: Basswood & Ivory Porcelain chassis, Zen cowl hat, Bamboo dual-ring key,
Steaming tea kettle backpack, Serene amber optic lens, and Floating Taiji spirit crystal.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

REPO_ROOT = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_1e3514ab"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/capybara"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/capybara"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical slice layers (128x128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_capybara_bamboo_dual_ring_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_capybara_steaming_tea_kettle_backpack.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_capybara_porcelain_timber_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_capybara_zen_monk_cowl_hat.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_capybara_tea_ceremony_wrap.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_capybara_amber_zen_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_capybara_serene_taiji_crystal.png").convert("RGBA")

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
weapon_raw = weapon_src.crop(wpn_bbox)

# Extract raw key crop
key_bbox = key_src.getbbox()
assert key_bbox is not None
key_raw = key_src.crop(key_bbox)

# Canonical ground shadow directly from chassis slice (118..127)
comp_path = f"{BASE_DIR}/proof_paperdoll_capybara_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(4, 124):
        s_px[x, y] = cast(tuple[int, int, int, int], c_px[x, y])

arr_shd = np.array(shadow_master)
EXPECTED_SHADOW = [int(np.sum(arr_shd[y, :, 3] > 20)) for y in range(118, 128)]
print(f"Benchmark ground shadow row counts (118..127): {EXPECTED_SHADOW}")


def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 and safe boundaries."""
    out = img.copy()
    o_px = out.load()
    s_pixels = shadow_master.load()
    assert o_px is not None and s_pixels is not None

    # Strictly set shadow zone (118..127) to baseline shadow pixels
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_pixels[x, y])
            o_px[x, y] = sp

    # Clean outer boundary strictly (L>=4, R>=4, T>=4, B>=2)
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
    """Performs inverse distance weighting image warp for organic toy articulation."""
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


# Anchor corners and borders for IDW (ground plane at y=116..127 remains grounded)
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (44, 116), (72, 116), (58, 116)
]

base_landmarks = {
    "head_top": (64, 13),      # Orange on hat apex
    "hat_apex": (64, 18),
    "hat_l": (34, 36),
    "hat_r": (94, 36),
    "ear_l": (38, 41),
    "ear_r": (90, 41),
    "eye_l": (54, 42),
    "eye_r": (74, 42),
    "snout": (64, 51),
    "jaw": (64, 57),
    "throat": (64, 60),
    "shoulder_l": (44, 61),
    "shoulder_r": (84, 61),
    "arm_l": (40, 78),
    "arm_r": (88, 70),
    "chest_core": (64, 72),
    "belly_window": (64, 75),
    "torso": (64, 82),
    "waist_l": (50, 88),
    "waist_r": (78, 88),
    "foot_l": (44, 113),
    "foot_r": (72, 113),
    "curio_kettle_l": (45, 54),
    "curio_kettle_r": (83, 54),
    "key_mount": (74, 34),
}

# Base body without weapon and winding key (z: curio=8, chassis=10, head=20, costume=25, optic=30)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (澄心凝神 / Serene Poise)
    # Winding key at (74, 34), spirit crystal at (99, 72)
    # Right border x <= 123 (R>=4px margin).
    # =========================================================================
    idle_key = place_rotated_element(key_raw, deg=0, target_center=(74, 34), scale=1.0)
    idle_weapon = place_rotated_element(weapon_raw, deg=0, target_center=(99, 72), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, body_core)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (抱元守一·氣沉丹田 / Zen Focus & Crystal Gathering)
    # Body crouches slightly (y+6, x-3), hat and brow tilt downward peacefully.
    # Winding key counter-winds (-35 deg, x-3, y+5).
    # Taiji spirit crystal pulls into torso core (88, 75, -25 deg).
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-3, 6), "hat_apex": (-3, 6), "hat_l": (-4, 6), "hat_r": (-2, 6),
        "ear_l": (-4, 6), "ear_r": (-2, 6),
        "eye_l": (-3, 6), "eye_r": (-3, 6),
        "snout": (-3, 6), "jaw": (-3, 6), "throat": (-3, 6),
        "chest_core": (-3, 5), "belly_window": (-3, 5),
        "shoulder_l": (-2, 5), "shoulder_r": (-4, 5),
        "arm_l": (1, 4), "arm_r": (-6, 5),
        "torso": (-3, 5), "waist_l": (-4, 4), "waist_r": (-1, 4),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "curio_kettle_l": (-4, 5), "curio_kettle_r": (-3, 5),
        "key_mount": (-3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_tele = place_rotated_element(key_raw, deg=-35, target_center=(71, 39), scale=1.0)
    crystal_tele = place_rotated_element(weapon_raw, deg=-25, target_center=(88, 75), scale=0.96)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, key_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, crystal_tele)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (太極推手·靈晶激盪 / Serene Crystal Palm Strike)
    # Body lunges forward (x+10, y-1), right arm extends to cast spirit blade.
    # Winding key spins forward (+55 deg, x+7, y-1).
    # Spirit crystal pushed forward vigorously (+35 deg, target_center=(98, 70), scale=1.02).
    # Margin x <= 123 (R>=4px).
    # =========================================================================
    shifts_attack = {
        "head_top": (10, -1), "hat_apex": (10, -1), "hat_l": (9, -1), "hat_r": (11, -1),
        "ear_l": (9, -1), "ear_r": (11, -1),
        "eye_l": (10, -1), "eye_r": (10, -1),
        "snout": (11, 0), "jaw": (10, 0), "throat": (10, 0),
        "chest_core": (9, 0), "belly_window": (9, 0),
        "shoulder_l": (11, -1), "shoulder_r": (8, 0),
        "arm_l": (13, -2), "arm_r": (0, 0),
        "torso": (8, 0), "waist_l": (7, 0), "waist_r": (-2, 0),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "curio_kettle_l": (6, -1), "curio_kettle_r": (8, -1),
        "key_mount": (8, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_attack = place_rotated_element(key_raw, deg=55, target_center=(82, 33), scale=1.0)
    crystal_attack = place_rotated_element(weapon_raw, deg=35, target_center=(98, 70), scale=1.02)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, key_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, crystal_attack)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (天元澄心·太極八卦陣 / Celestial Taiji Bagua Formation)
    # Stance grounded (y+3, x+0), mandarin orange on hat emits zen aura.
    # Winding key spins in full overdrive (+90 deg, x+1, y-1).
    # Spirit crystal elevates high to (94, 52, deg=75, scale=1.06).
    # Pure subtle bamboo tea jade aura particles (no muddy occlusion).
    # =========================================================================
    shifts_skill = {
        "head_top": (0, 3), "hat_apex": (0, 3), "hat_l": (0, 3), "hat_r": (1, 3),
        "ear_l": (0, 3), "ear_r": (1, 3),
        "eye_l": (0, 3), "eye_r": (0, 3),
        "snout": (0, 3), "jaw": (0, 3), "throat": (0, 3),
        "chest_core": (0, 3), "belly_window": (0, 3),
        "shoulder_l": (-1, 3), "shoulder_r": (1, 3),
        "arm_l": (0, 3), "arm_r": (0, 3),
        "torso": (0, 3), "waist_l": (-1, 2), "waist_r": (1, 2),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "curio_kettle_l": (0, 0), "curio_kettle_r": (1, 0),
        "key_mount": (1, -1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_skill = place_rotated_element(key_raw, deg=90, target_center=(75, 33), scale=1.05)
    crystal_skill = place_rotated_element(weapon_raw, deg=75, target_center=(94, 52), scale=1.06)

    # Delicate zen aura glow at orange & kettles
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Aura ring around elevated crystal
    s_draw.ellipse([94 - 18, 52 - 18, 94 + 18, 52 + 18], outline=(78, 216, 106, 120), width=1)
    s_draw.ellipse([94 - 15, 52 - 15, 94 + 15, 52 + 15], outline=(255, 208, 40, 100), width=1)
    # Mandarin orange radiance dot
    s_draw.point((64, 12), fill=(255, 253, 248, 220))
    s_draw.point((65, 12), fill=(255, 160, 16, 200))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.4))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, key_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, crystal_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (受擊後仰·氣韻震波 / Kinetic Impact & Tea Steam Dissipation)
    # Knocked backward (x-8, y-4), hat and ears tilt back, chassis braces.
    # Winding key jolted backward (-25 deg, x-6, y-2).
    # Spirit crystal pushed back into defensive guard (-35 deg, target=(86, 78)).
    # Golden clashing spark at chest wrap embroidery.
    # =========================================================================
    shifts_hit = {
        "head_top": (-8, -4), "hat_apex": (-8, -4), "hat_l": (-9, -4), "hat_r": (-7, -4),
        "ear_l": (-9, -4), "ear_r": (-7, -4),
        "eye_l": (-8, -4), "eye_r": (-8, -4),
        "snout": (-8, -3), "jaw": (-8, -3), "throat": (-7, -3),
        "chest_core": (-7, -2), "belly_window": (-7, -2),
        "shoulder_l": (-6, -2), "shoulder_r": (-7, -2),
        "arm_l": (-4, -1), "arm_r": (-7, -1),
        "torso": (-6, -2), "waist_l": (-5, -1), "waist_r": (-3, -1),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "curio_kettle_l": (-6, -4), "curio_kettle_r": (-5, -4),
        "key_mount": (-6, -3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_hit = place_rotated_element(key_raw, deg=-25, target_center=(68, 31), scale=1.0)
    crystal_hit = place_rotated_element(weapon_raw, deg=-35, target_center=(86, 78), scale=1.0)

    # Mechanical clashing spark at chest
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    ix, iy = 66, 68
    h_draw.ellipse([ix - 3, iy - 3, ix + 3, iy + 3], fill=(255, 208, 40, 220))
    h_draw.point((ix, iy), fill=(255, 253, 248, 255))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.3))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, key_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, crystal_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (調息著地·發條咬合 / Damped Landing & Spring Equilibrium)
    # Landing crouch (y+4, x-1), calm posture resets.
    # Winding key snaps into gear mesh (+15 deg, x+1, y+2).
    # Spirit crystal resets to lower poised position (-10 deg, target=(94, 80)).
    # =========================================================================
    shifts_recover = {
        "head_top": (-1, 4), "hat_apex": (-1, 4), "hat_l": (-2, 4), "hat_r": (0, 4),
        "ear_l": (-2, 4), "ear_r": (0, 4),
        "eye_l": (-1, 4), "eye_r": (-1, 4),
        "snout": (-1, 4), "jaw": (-1, 4), "throat": (-1, 4),
        "chest_core": (-1, 4), "belly_window": (-1, 4),
        "shoulder_l": (-2, 3), "shoulder_r": (0, 3),
        "arm_l": (1, 2), "arm_r": (-2, 3),
        "torso": (-1, 4), "waist_l": (-2, 3), "waist_r": (1, 3),
        "foot_l": (0, 0), "foot_r": (0, 0),
        "curio_kettle_l": (-1, 3), "curio_kettle_r": (-1, 3),
        "key_mount": (1, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_core, src_pts, dst_pts, power=2.0, epsilon=4.0)
    key_rec = place_rotated_element(key_raw, deg=15, target_center=(75, 36), scale=1.0)
    crystal_rec = place_rotated_element(weapon_raw, deg=-10, target_center=(94, 80), scale=1.0)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, key_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, crystal_rec)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating Serene Capybara combat action poses...")
    poses = generate_poses()

    pose_names = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

    # Save 128x128 poses and 512x512 LANCZOS versions
    for name in pose_names:
        im128 = poses[name]
        p128 = f"{OUT_DIR}/{name}.png"
        im128.save(p128)
        print(f"  Saved {p128} ({im128.size})")

        # 512x512 LANCZOS high-definition scale
        im512 = im128.resize((512, 512), Image.Resampling.LANCZOS)
        p512 = f"{OUT_DIR}/{name}_512.png"
        im512.save(p512)
        print(f"  Saved {p512} ({im512.size}, LANCZOS)")

    # Generate 768x128 Transparent Proof Sheet
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for idx, name in enumerate(pose_names):
        proof_768.paste(poses[name], (idx * 128, 0))
    p_proof_768 = f"{REPO_ROOT}/game/assets/sprites/player/proof_capybara_combat_poses_768.png"
    proof_768.save(p_proof_768)
    print(f"  Saved 768 proof: {p_proof_768}")

    # Generate 768x128 Magenta Proof Sheet
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for idx, name in enumerate(pose_names):
        proof_mag.alpha_composite(poses[name], (idx * 128, 0))
    p_proof_mag = f"{REPO_ROOT}/game/assets/sprites/player/proof_capybara_combat_poses_magenta.png"
    proof_mag.save(p_proof_mag)
    print(f"  Saved magenta proof: {p_proof_mag}")

    print("\n✓ All Serene Capybara combat poses generated successfully!")


if __name__ == "__main__":
    main()
