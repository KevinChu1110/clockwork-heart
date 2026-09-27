#!/usr/bin/env python3
"""
tools/build_hound_combat_poses.py
Generates the complete, definitive 6 combat action poses for Orbit Hound (星軌犬, 15th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/hound/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/hound/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/hound"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/hound"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_hound_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_hound_four_blade_antenna_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_hound_floating_micro_satellite.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_hound_polymer_astro_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_hound_radar_leaf_antennas.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_hound_space_explorer_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_hound_dot_matrix_led_eyes.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_hound_stellar_beacon_lance.png").convert("RGBA")

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
lance_raw = weapon_src.crop(wpn_bbox)

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

def place_lance(lance_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Stellar Radar Beacon Lance with zero clipping."""
    b = lance_img.copy()
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
    "head_top": (64, 26),
    "ear_l": (47, 20),
    "ear_r": (81, 20),
    "eye_l": (53, 40),
    "eye_r": (75, 40),
    "snout": (64, 46),
    "throat": (64, 52),
    "core": (63, 72),
    "shoulder_l": (42, 60),
    "shoulder_r": (84, 60),
    "arm_l": (28, 74),
    "arm_r": (44, 76),
    "torso": (63, 76),
    "pelvis": (63, 86),
    "hip_l": (48, 92),
    "hip_r": (78, 92),
    "knee_l": (46, 102),
    "knee_r": (80, 102),
    "foot_l": (42, 113),
    "foot_r": (56, 113),
    "rear_l": (74, 113),
    "rear_r": (86, 113),
    "tail_root": (76, 82),
    "tail_tip": (94, 72),
    "key_mount": (66, 64),
    "key_head": (88, 36),
    "curio_center": (106, 62),
}

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline stable poise from canonical composite)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (星軌鎖定·雷達蓄勢 / Orbital Telemetry Lock & Thrust Preparation)
    # Sinks into deep telemetry charge stance (y+7, x-3).
    # Lance held back tight in low guard ready for lightning thrust (mirror=True, points forward-right).
    # Radar leaf ears track forward, LED eyes pulse targeting gold.
    # Crosshair HUD & concentric telemetry rings project forward.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-3, 7), "ear_l": (-5, 7), "ear_r": (-1, 7),
        "eye_l": (-3, 7), "eye_r": (-3, 7), "snout": (-3, 7), "throat": (-3, 7),
        "core": (-2, 7),
        "shoulder_l": (-1, 6), "arm_l": (2, 6),
        "shoulder_r": (-5, 6), "arm_r": (-6, 6),
        "torso": (-3, 7), "pelvis": (-2, 6),
        "hip_l": (-4, 5), "hip_r": (2, 5),
        "knee_l": (-6, 4), "knee_r": (4, 4),
        "foot_l": (-2, 0), "foot_r": (2, 0), "rear_l": (-2, 0), "rear_r": (2, 0),
        "tail_root": (-3, 6), "tail_tip": (-4, 8),
        "key_mount": (-3, 6), "key_head": (-4, 5),
        "curio_center": (4, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Lance drawn back ready, pointing forward-right with mirror=True
    # Tip at right (~78, 62), grip at (~48, 76), counterweight at (~28, 86)
    lance_tele = place_lance(lance_raw, deg=-5, target_center=(50, 76), scale=1.04, mirror=True)

    # Telemetry Crosshair & Radar Scan FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Aiming trajectory beam from lance tip toward target forward
    t_draw.line([(76, 64), (104, 54)], fill=(56, 160, 255, 220), width=2)
    t_draw.line([(86, 60), (116, 52)], fill=(255, 255, 255, 255), width=1)
    # Concentric telemetry crosshair reticle at target forward (104, 52)
    cx, cy = 104, 52
    t_draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=(56, 160, 255, 230), width=1)
    t_draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(255, 208, 40, 240), width=1)
    # Radar leaf ears acoustic sweep arcs
    t_draw.arc([36, 16, 68, 38], start=210, end=350, fill=(56, 160, 255, 200), width=2)
    t_draw.arc([68, 16, 100, 38], start=190, end=330, fill=(255, 208, 40, 210), width=2)
    # Winding key torque rotation sparks
    t_draw.arc([74, 34, 100, 60], start=20, end=340, fill=(255, 160, 16, 210), width=2)
    # Optic core amber targeting LED focus pulse
    t_draw.ellipse([46, 44, 54, 52], fill=(255, 235, 120, 230))
    t_draw.ellipse([68, 44, 76, 52], fill=(255, 235, 120, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, lance_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (星軌突刺·信標貫通 / Stellar Beacon Orbital Lunge)
    # Explosive lunge: body rockets forward-right (x+15, y-1), left arm drives
    # lance forward in full piercing thrust! Supersonic beacon plasma spear beam.
    # Lance is mirrored (mirror=True), pointing directly forward (deg=-24).
    # Tip extends to (98, 68), beam fires forward to (122, 68).
    # Zero clipping on torso! Clean, clear knight spear thrust!
    # =========================================================================
    shifts_attack = {
        "head_top": (15, -1), "ear_l": (13, -2), "ear_r": (17, -1),
        "eye_l": (15, -1), "eye_r": (15, -1), "snout": (16, 0), "throat": (15, 0),
        "core": (14, 0),
        "shoulder_l": (16, -1), "arm_l": (22, -2),
        "shoulder_r": (5, 0), "arm_r": (-2, 1),
        "torso": (13, 0), "pelvis": (10, 0),
        "hip_l": (12, -1), "hip_r": (-5, 0),
        "knee_l": (13, -1), "knee_r": (-8, 0),
        "foot_l": (7, 0), "foot_r": (-6, 0), "rear_l": (-5, 0), "rear_r": (-8, 0),
        "tail_root": (8, 0), "tail_tip": (-6, -4),
        "key_mount": (10, 0), "key_head": (6, -2),
        "curio_center": (-8, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Lance thrust forward: mirror=True, deg=-24 (almost horizontal piercing thrust)
    # Grip placed at (48, 72), shaft extends forward to tip at (96, 68)
    lance_attack = place_lance(lance_raw, deg=-24, target_center=(68, 68), scale=1.06, mirror=True)

    # Supersonic Stellar Plasma Beam & Orbital Shockwave Rings
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Core plasma lance beam shooting forward from lance tip (96, 68) to screen edge (122, 68)
    a_draw.line([(96, 68), (122, 68)], fill=(56, 160, 255, 245), width=3)
    a_draw.line([(98, 68), (124, 68)], fill=(255, 255, 255, 255), width=1)
    # Lance beacon needle tip piercing arrowhead
    a_draw.polygon([(124, 68), (116, 63), (118, 68), (116, 73)], fill=(78, 216, 106, 255))
    # Expanding kinetic shockwave cones in front of lance tip
    a_draw.arc([100, 54, 116, 82], start=275, end=85, fill=(56, 160, 255, 220), width=2)
    a_draw.arc([108, 50, 122, 86], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    # Lance emitter flash at tip (96, 68)
    a_draw.ellipse([(92, 64), (100, 72)], fill=(255, 255, 220, 255))
    a_draw.point([(94, 62), (98, 62), (94, 74), (98, 74), (102, 68)], fill=(78, 216, 106, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, lance_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (全頻共振·天線星軌打擊 / Stellar Resonance Full Orbital Cascade)
    # Overdrive bipedal leap: body rises proudly (y-10), lance pointed high
    # to the stars (-60 deg). Micro-satellite orbits with electromagnetic field.
    # Celestial dopamine starburst and orbital telemetry mandala.
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -11), "ear_l": (-4, -12), "ear_r": (4, -12),
        "eye_l": (0, -10), "eye_r": (0, -10), "snout": (0, -9), "throat": (0, -8),
        "core": (0, -7),
        "shoulder_l": (-6, -9), "arm_l": (-10, -12),
        "shoulder_r": (8, -9), "arm_r": (12, -11),
        "torso": (0, -7), "pelvis": (0, -5),
        "hip_l": (-4, -5), "hip_r": (4, -5),
        "knee_l": (-6, -4), "knee_r": (6, -4),
        "foot_l": (-3, -3), "foot_r": (3, -3), "rear_l": (-3, 0), "rear_r": (3, 0),
        "tail_root": (0, -5), "tail_tip": (4, -8),
        "key_mount": (0, -6), "key_head": (0, -8),
        "curio_center": (-10, -12),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Lance raised skyward in high beacon broadcast stance (-58 deg)
    lance_skill = place_lance(lance_raw, deg=-58, target_center=(26, 54), scale=1.08, mirror=False)

    # Orbital Cascade & Celestial Satellite Aura (y: 16..106)
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Orbital electromagnetic rings encircling hound
    s_draw.arc([16, 20, 116, 96], start=140, end=355, fill=(56, 160, 255, 230), width=3)
    s_draw.arc([22, 24, 110, 90], start=155, end=335, fill=(78, 216, 106, 220), width=2)
    s_draw.arc([30, 28, 102, 84], start=165, end=315, fill=(255, 208, 40, 210), width=1)
    # Beacon light beam radiating skyward-right from lance tip
    s_draw.line([(24, 46), (114, 20)], fill=(78, 216, 106, 240), width=3)
    s_draw.line([(24, 46), (116, 20)], fill=(255, 255, 255, 255), width=1)
    s_draw.polygon([(118, 20), (110, 17), (112, 22)], fill=(255, 208, 40, 255))
    # Secondary telemetry broadcast streams
    s_draw.line([(28, 52), (118, 38)], fill=(56, 160, 255, 240), width=2)
    s_draw.polygon([(120, 38), (112, 35), (114, 40)], fill=(56, 160, 255, 255))
    s_draw.line([(32, 58), (114, 58)], fill=(255, 208, 40, 230), width=2)
    s_draw.polygon([(116, 58), (108, 55), (110, 60)], fill=(255, 255, 255, 255))
    # Floating dopamine starbursts & telemetry nodes
    s_draw.polygon([(104, 18), (112, 14), (106, 22)], fill=(255, 208, 40, 240))
    s_draw.polygon([(18, 50), (10, 56), (20, 58)], fill=(78, 216, 106, 240))
    s_draw.polygon([(88, 12), (96, 8), (90, 16)], fill=(56, 160, 255, 230))
    s_draw.polygon([(16, 30), (24, 24), (22, 34)], fill=(255, 94, 138, 240))
    # Ground resonance field (y <= 106)
    s_draw.line([(42, 98), (84, 98)], fill=(56, 160, 255, 180), width=2)
    s_draw.line([(48, 103), (78, 103)], fill=(78, 216, 106, 160), width=1)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.6))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, lance_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (防護過載·阻尼受擊後仰 / Kinetic Damper Recoil & Shock Stagger)
    # Heavy impact stagger: body and head pitch far back (x-15, y-2).
    # Lance is jolted upward and outwards to the flank (target_center=(24, 76), deg=12),
    # absolutely NO clipping through torso!
    # Clean kinetic impact cross-star flash & directional damper exhaust.
    # =========================================================================
    shifts_hit = {
        "head_top": (-16, -2), "ear_l": (-18, -2), "ear_r": (-14, -2),
        "eye_l": (-15, -2), "eye_r": (-15, -2), "snout": (-14, 0), "throat": (-13, 0),
        "core": (-12, 0),
        "shoulder_l": (-8, 1), "arm_l": (-6, 3),
        "shoulder_r": (-12, 0), "arm_r": (-14, 0),
        "torso": (-10, 1), "pelvis": (-8, 1),
        "hip_l": (-10, 1), "hip_r": (-5, 1),
        "knee_l": (-11, 0), "knee_r": (-5, 0),
        "foot_l": (-7, 0), "foot_r": (-3, 0), "rear_l": (-8, 0), "rear_r": (-4, 0),
        "tail_root": (-10, 1), "tail_tip": (-14, 4),
        "key_mount": (-12, 0), "key_head": (-13, -2),
        "curio_center": (-14, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Lance is held at outer left flank, jolted upward-backwards (deg=12, target_center=(24, 76))
    # Mirrored=False so tip is at (4..12, 44..52), completely outside body profile!
    lance_hit = place_lance(lance_raw, deg=12, target_center=(24, 76), scale=0.98, mirror=False)

    # Deflection cross-star spark & directional damper exhaust
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 48, 68
    # Clean 4-point cross star flash on shield/harness impact point
    h_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=(56, 160, 255, 220), width=1)
    h_draw.line([(cx - 5, cy + 5), (cx + 5, cy - 5)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
    # Deflection sparks flying away
    h_draw.point([(cx - 8, cy - 7), (cx + 9, cy - 6), (cx + 7, cy + 8), (cx - 7, cy + 9)], fill=(255, 255, 220, 255))
    # Directional pneumatic steam exhaust from polymer joints
    h_draw.line([(68, 48), (92, 40)], fill=(240, 248, 255, 200), width=2)
    h_draw.line([(66, 52), (94, 48)], fill=(220, 235, 250, 170), width=1)
    h_draw.line([(70, 56), (96, 56)], fill=(220, 235, 250, 160), width=1)
    # LED eyes flash alert orange-red
    h_draw.ellipse([36, 36, 44, 42], fill=(255, 94, 138, 220))
    h_draw.ellipse([58, 36, 66, 42], fill=(255, 94, 138, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.5))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, lance_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (地表抓地·氣壓冷卻穩位 / Pneumatic Vent & Surface Anchor Recovery)
    # Sinks into solid restabilization (y+7, x+1), 4 paws firmly anchored.
    # Lance held relaxed in low ready position (mirror=True, deg=2).
    # Calming blue/mint cooling field around suction pads and joints.
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 6), "ear_l": (0, 6), "ear_r": (2, 6),
        "eye_l": (1, 6), "eye_r": (1, 6), "snout": (1, 7), "throat": (1, 7),
        "core": (1, 7),
        "shoulder_l": (-3, 6), "arm_l": (0, 7),
        "shoulder_r": (4, 6), "arm_r": (6, 7),
        "torso": (1, 7), "pelvis": (1, 7),
        "hip_l": (-4, 6), "hip_r": (5, 6),
        "knee_l": (-6, 5), "knee_r": (6, 5),
        "foot_l": (-3, 0), "foot_r": (4, 0), "rear_l": (-3, 0), "rear_r": (4, 0),
        "tail_root": (1, 6), "tail_tip": (2, 6),
        "key_mount": (1, 6), "key_head": (1, 5),
        "curio_center": (2, 7),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Lance held relaxed in low ready position
    lance_recover = place_lance(lance_raw, deg=2, target_center=(48, 78), scale=1.0, mirror=True)

    # Ground settling ripples & calming sky blue cooling field (y <= 110)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.arc([36, 96, 92, 110], start=15, end=165, fill=(56, 160, 255, 180), width=2)
    r_draw.arc([42, 100, 86, 110], start=25, end=155, fill=(78, 216, 106, 160), width=1)
    # Cooling pneumatic steam puffs from joints
    r_draw.ellipse([64, 48, 76, 60], fill=(230, 240, 250, 160))
    r_draw.ellipse([70, 42, 80, 52], fill=(240, 245, 255, 180))
    r_draw.ellipse([30, 78, 40, 88], fill=(230, 240, 250, 150))
    # Calming amber pulse at optic core
    r_draw.ellipse([50, 44, 58, 52], fill=(255, 208, 40, 160))
    r_draw.ellipse([72, 44, 80, 52], fill=(255, 208, 40, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, lance_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING ORBIT HOUND 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")

        # 512 LANCZOS upscale (CRITICAL: LANCZOS, not NEAREST)
        dst_512 = os.path.join(OUT_DIR, f"{p_name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(dst_512, format="PNG")

        bbox = img.getbbox()
        print(f"✓ Saved {p_name:10s} -> {dst_128} (128x128, bbox={bbox}) and {dst_512} (512x512)")

    # Generate proof sheets
    # 1. 768-wide strip (all 6 poses in a row: 128 x 6 = 768)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_hound_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_hound_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
    print("\nAll 6 hound combat poses successfully generated and saved!")
