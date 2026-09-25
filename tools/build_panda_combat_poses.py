#!/usr/bin/env python3
"""
tools/build_panda_combat_poses.py
Generates the complete, definitive 6 combat action poses for Porcelain Panda (瓷韻熊貓, 13th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/panda/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/panda/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/panda"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/panda"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_panda_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_panda_taiji_ruyi_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_panda_floating_taiji_box.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_panda_porcelain.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_panda_brass_socket_ears.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_panda_zen_apprentice_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_obsidian_amber_quartz.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_panda_taiji_cestus.png").convert("RGBA")

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
cestus_raw = weapon_src.crop(wpn_bbox)

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
    assert o_px is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:  # sp[3] > 20
                if fp[3] <= 20:
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

def place_cestus(cestus_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Taiji Cestus weapon with zero clipping."""
    b = cestus_img.copy()
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
    "head_top": (64, 16),
    "eye_l": (52, 34),
    "eye_r": (76, 34),
    "ear_l": (38, 16),
    "ear_r": (90, 16),
    "snout": (64, 42),
    "throat": (64, 56),
    "core": (64, 68),
    "shoulder_l": (38, 62),
    "shoulder_r": (86, 62),
    "arm_l": (28, 72),
    "arm_r": (94, 72),
    "torso": (64, 76),
    "pelvis": (64, 88),
    "hip_l": (46, 92),
    "hip_r": (82, 92),
    "knee_l": (40, 102),
    "knee_r": (88, 102),
    "foot_l": (48, 118),
    "foot_r": (80, 118),
    "key_mount": (32, 40),
    "key_wing": (22, 22),
    "curio_top": (24, 34),
    "curio_mid": (22, 44),
    "curio_bot": (20, 54),
}

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline stable poise from canonical composite / panda_idle_x3)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (沉步聚氣·太極引勁 Deep Horse Stance & Taiji Power Coiling)
    # Body sinks into a deep horse stance (y+11), knees flare wide,
    # winding key winds up backwards with intense spin aura, core glows amber.
    # Cestus pulled back tight to waist ready to strike.
    # =========================================================================
    shifts_telegraph = {
        "head_top": (-4, 11), "eye_l": (-4, 11), "eye_r": (-4, 11),
        "ear_l": (-5, 10), "ear_r": (-3, 10),
        "snout": (-4, 11), "throat": (-3, 11), "core": (-3, 11),
        "shoulder_l": (5, 9), "arm_l": (9, 7),
        "shoulder_r": (-8, 10), "arm_r": (-14, 6),
        "torso": (-3, 11), "pelvis": (-3, 11),
        "hip_l": (-7, 9), "hip_r": (7, 9),
        "knee_l": (-12, 7), "knee_r": (12, 7),
        "foot_l": (-3, 0), "foot_r": (3, 0),
        "key_mount": (-5, 10), "key_wing": (-7, 8),
        "curio_top": (4, 7), "curio_mid": (5, 8), "curio_bot": (4, 9),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    cestus_tele = place_cestus(cestus_raw, deg=28, target_center=(76, 78), scale=1.04, mirror=False)

    # Coiling Taiji rings & torque spin sparks
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging arcs around fist
    t_draw.arc([58, 60, 94, 96], start=30, end=320, fill=(255, 208, 40, 230), width=2)
    t_draw.arc([54, 56, 98, 100], start=60, end=300, fill=(255, 160, 16, 210), width=2)
    t_draw.arc([62, 64, 90, 92], start=10, end=340, fill=(56, 160, 255, 200), width=1)
    # Key spin aura
    t_draw.arc([10, 16, 34, 40], start=15, end=345, fill=(255, 208, 40, 210), width=2)
    # Core amber pulse
    t_draw.ellipse([57, 75, 69, 87], fill=(255, 180, 20, 190))
    t_draw.ellipse([60, 78, 66, 84], fill=(255, 255, 255, 220))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.6))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, cestus_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (太極崩拳·破風衝擊 Taiji Straight Punch & Shockwave)
    # Lunge forward strike: torso and head advance x+12, rear leg drives back,
    # fist punches straight forward-right with supersonic shockwave cone.
    # We combine the approved panda_battle kinematics with forward shockwave FX.
    # =========================================================================
    shifts_attack = {
        "head_top": (12, -1), "eye_l": (13, -1), "eye_r": (13, -1),
        "ear_l": (10, -2), "ear_r": (14, -1),
        "snout": (14, 0), "throat": (13, 0), "core": (12, 0),
        "shoulder_l": (-7, 1), "arm_l": (-13, 3),
        "shoulder_r": (14, -1), "arm_r": (20, -2),
        "torso": (11, 0), "pelvis": (9, 0),
        "hip_l": (-7, 0), "hip_r": (12, -1),
        "knee_l": (-12, 0), "knee_r": (14, -1),
        "foot_l": (-8, 0), "foot_r": (8, 0),
        "key_mount": (9, -1), "key_wing": (7, -2),
        "curio_top": (-9, -2), "curio_mid": (-8, 1), "curio_bot": (-6, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    cestus_attack = place_cestus(cestus_raw, deg=-22, target_center=(104, 66), scale=1.05, mirror=False)

    # Piercing golden Taiji shockwave & strike trails
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Supersonic shockwave cone in front of cestus
    a_draw.line([(96, 66), (122, 66)], fill=(255, 208, 40, 240), width=3)
    a_draw.line([(98, 66), (123, 66)], fill=(255, 255, 255, 255), width=1)
    a_draw.arc([102, 52, 122, 80], start=275, end=85, fill=(255, 160, 16, 230), width=2)
    a_draw.arc([106, 50, 122, 82], start=280, end=80, fill=(56, 160, 255, 220), width=2)
    # Kinetic thrust lines
    a_draw.line([(28, 76), (12, 80)], fill=(255, 208, 40, 180), width=2)
    a_draw.line([(24, 82), (10, 88)], fill=(255, 160, 16, 160), width=2)
    # Punch sparks
    a_draw.ellipse([98, 62, 106, 70], fill=(255, 255, 220, 255))
    a_draw.point([(108, 58), (105, 74), (114, 60), (109, 70), (118, 58)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, cestus_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (八卦乾坤·陰陽旋罡 Taiji Yin-Yang Whirlwind Overdrive)
    # Overdrive martial leap: body lifts slightly (y-9), arms swept wide,
    # majestic golden Yin-Yang Taiji vortex mandala surrounding the hero.
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -9), "eye_l": (0, -9), "eye_r": (0, -9),
        "ear_l": (-3, -10), "ear_r": (3, -10),
        "snout": (0, -8), "throat": (0, -7), "core": (0, -6),
        "shoulder_l": (-10, -8), "arm_l": (-16, -10),
        "shoulder_r": (11, -8), "arm_r": (17, -9),
        "torso": (0, -6), "pelvis": (0, -5),
        "hip_l": (-5, -5), "hip_r": (5, -5),
        "knee_l": (-7, -5), "knee_r": (7, -5),
        "foot_l": (-4, -5), "foot_r": (4, -5),
        "key_mount": (-1, -5), "key_wing": (-2, -6),
        "curio_top": (-9, -10), "curio_mid": (-10, -7), "curio_bot": (-7, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    cestus_skill = place_cestus(cestus_raw, deg=-54, target_center=(98, 48), scale=1.08, mirror=False)

    # Taiji Yin-Yang Mandala & Gear Spark Vortex (strictly y: 16..106)
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Concentric celestial Taiji energy rings
    s_draw.arc([18, 18, 118, 96], start=140, end=355, fill=(255, 208, 40, 230), width=3)
    s_draw.arc([24, 22, 112, 90], start=155, end=335, fill=(255, 160, 16, 210), width=2)
    s_draw.arc([32, 26, 104, 84], start=165, end=315, fill=(56, 160, 255, 220), width=1)
    # Yin-Yang Taiji fish energy spirals
    s_draw.arc([42, 38, 86, 82], start=0, end=180, fill=(255, 255, 255, 240), width=2)
    s_draw.arc([52, 48, 76, 72], start=180, end=360, fill=(255, 208, 40, 240), width=2)
    # Floating brass gear tooth runes
    s_draw.polygon([(110, 28), (118, 24), (112, 32)], fill=(255, 255, 255, 255))
    s_draw.polygon([(20, 58), (12, 64), (22, 66)], fill=(255, 208, 40, 240))
    s_draw.polygon([(90, 16), (98, 12), (92, 20)], fill=(56, 160, 255, 230))
    s_draw.polygon([(18, 34), (26, 28), (24, 38)], fill=(255, 160, 16, 240))
    # Airborne energy shimmer lines (y <= 106)
    s_draw.line([(44, 98), (84, 98)], fill=(255, 208, 40, 180), width=2)
    s_draw.line([(50, 103), (78, 103)], fill=(56, 160, 255, 160), width=1)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.7))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, cestus_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (金屬重擊·大幅後仰失衡 Heavy Impact Stagger & Elbow Deflection)
    # Torso and head pitch far back (x-15, y-2), off-balance recoil,
    # cestus pulled across chest in emergency martial block.
    # Impact cross-star flash & linear steam exhaust jets.
    # =========================================================================
    shifts_hit = {
        "head_top": (-15, -2), "eye_l": (-15, -2), "eye_r": (-15, -2),
        "ear_l": (-16, -2), "ear_r": (-14, -2),
        "snout": (-14, 0), "throat": (-13, 0), "core": (-12, 0),
        "shoulder_l": (-11, 1), "arm_l": (-7, 3),
        "shoulder_r": (-10, 0), "arm_r": (-11, 0),
        "torso": (-10, 1), "pelvis": (-8, 1),
        "hip_l": (-10, 1), "hip_r": (-5, 1),
        "knee_l": (-11, 0), "knee_r": (-5, 0),
        "foot_l": (-7, 0), "foot_r": (-3, 0),
        "key_mount": (-12, 0), "key_wing": (-12, -2),
        "curio_top": (-14, 5), "curio_mid": (-12, 4), "curio_bot": (-8, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    cestus_hit = place_cestus(cestus_raw, deg=36, target_center=(68, 68), scale=0.96, mirror=False)

    # Metallic deflection cross-star spark & directional steam exhaust
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 68, 68
    h_draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=(255, 208, 40, 220), width=1)
    h_draw.line([(cx - 8, cy + 8), (cx + 8, cy - 8)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 255))
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 180), width=2)
    # Kinetic spark points
    h_draw.point([(cx - 12, cy - 10), (cx + 14, cy - 8), (cx + 12, cy + 12), (cx - 10, cy + 14)], fill=(255, 255, 220, 255))
    # Directional steam exhaust jets from back joints
    h_draw.line([(32, 40), (16, 32)], fill=(240, 248, 255, 200), width=2)
    h_draw.line([(30, 44), (14, 40)], fill=(220, 235, 250, 170), width=1)
    h_draw.line([(34, 48), (18, 50)], fill=(220, 235, 250, 160), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.5))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, cestus_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (凝神調息·氣沉丹田 Chi Centering & Stance Recovery)
    # Sinks into solid grounded restabilization (y+7), feet firmly planted,
    # cestus held at side ready position, calming cooling energy at core.
    # =========================================================================
    shifts_recover = {
        "head_top": (3, 7), "eye_l": (3, 7), "eye_r": (3, 7),
        "ear_l": (2, 6), "ear_r": (4, 6),
        "snout": (3, 8), "throat": (3, 8), "core": (3, 8),
        "shoulder_l": (-5, 7), "arm_l": (-9, 8),
        "shoulder_r": (6, 7), "arm_r": (8, 8),
        "torso": (3, 8), "pelvis": (3, 8),
        "hip_l": (-6, 7), "hip_r": (7, 7),
        "knee_l": (-8, 6), "knee_r": (8, 6),
        "foot_l": (-4, 0), "foot_r": (6, 0),
        "key_mount": (3, 7), "key_wing": (3, 6),
        "curio_top": (5, 5), "curio_mid": (5, 6), "curio_bot": (5, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    cestus_recover = place_cestus(cestus_raw, deg=-12, target_center=(92, 78), scale=0.98, mirror=False)

    # Ground settling ripples & calming optic core pulse (y <= 110)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.arc([36, 96, 92, 110], start=15, end=165, fill=(78, 216, 106, 180), width=2)
    r_draw.arc([42, 100, 86, 110], start=25, end=155, fill=(56, 160, 255, 160), width=1)
    # Cooling steam puffs from joints
    r_draw.ellipse([26, 44, 38, 56], fill=(230, 240, 250, 160))
    r_draw.ellipse([20, 38, 30, 48], fill=(240, 245, 255, 180))
    r_draw.ellipse([88, 76, 98, 86], fill=(230, 240, 250, 150))
    # Calming amber pulse at optic core
    r_draw.ellipse([58, 72, 70, 84], fill=(255, 180, 20, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, cestus_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING PORCELAIN PANDA 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")

        # 512 LANCZOS upscale
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_panda_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_panda_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
    print("\nAll 6 panda combat poses successfully generated and saved!")
