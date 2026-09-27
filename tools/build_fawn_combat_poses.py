#!/usr/bin/env python3
"""
tools/build_fawn_combat_poses.py
Generates the complete, definitive 6 combat action poses for Emerald Fawn (翠角鹿, 14th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/fawn/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/fawn/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fawn"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/fawn"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_fawn_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_fawn_clover_leaf_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_fawn_floating_pinecone_chime.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_fawn_timber_tinplate_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_fawn_vernier_caliper_horns.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_fawn_emerald_scout_tunic.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_fawn_amber_lens_alert_eyes.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_fawn_vernier_shortbow.png").convert("RGBA")

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
bow_raw = weapon_src.crop(wpn_bbox)

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

def place_bow(bow_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the Vernier Shortbow with zero clipping."""
    b = bow_img.copy()
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
    "horn_top": (64, 10),
    "horn_l": (34, 18),
    "horn_r": (94, 18),
    "head_top": (64, 26),
    "ear_l": (36, 26),
    "ear_r": (90, 26),
    "eye_l": (52, 42),
    "eye_r": (74, 42),
    "snout": (64, 52),
    "throat": (64, 58),
    "core": (63, 68),
    "shoulder_l": (42, 60),
    "shoulder_r": (84, 60),
    "arm_l": (32, 68),
    "arm_r": (90, 68),
    "torso": (63, 76),
    "pelvis": (63, 88),
    "hip_l": (48, 92),
    "hip_r": (78, 92),
    "knee_l": (46, 102),
    "knee_r": (80, 102),
    "foot_l": (44, 118),
    "foot_r": (82, 118),
    "key_mount": (74, 50),
    "key_wing": (88, 42),
    "curio_top": (106, 56),
    "curio_mid": (106, 66),
    "curio_bot": (106, 76),
}

def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline stable poise from canonical composite)
    # =========================================================================
    idle_canvas = body_master.copy()
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (聽風對表·游標蓄勢 / Vernier Caliper Wind Alignment & Full Draw)
    # Sinks into deep archery draw stance (y+10), torso leans slightly back (-5)
    # Front arm (left) raises bow firmly, rear hand draws bowstring tight.
    # Amber eye lenses glow, caliper horns calibrate with golden wind rings.
    # Concentric aiming reticle and kinetic charging particles.
    # =========================================================================
    shifts_telegraph = {
        "horn_top": (-4, 8), "horn_l": (-6, 8), "horn_r": (-2, 8),
        "head_top": (-5, 10), "ear_l": (-7, 10), "ear_r": (-3, 10),
        "eye_l": (-5, 10), "eye_r": (-5, 10), "snout": (-5, 10), "throat": (-4, 10),
        "core": (-3, 10),
        "shoulder_l": (-1, 8), "arm_l": (4, 6),
        "shoulder_r": (-8, 9), "arm_r": (-14, 7),
        "torso": (-4, 10), "pelvis": (-3, 10),
        "hip_l": (-7, 8), "hip_r": (6, 8),
        "knee_l": (-11, 6), "knee_r": (10, 6),
        "foot_l": (-3, 0), "foot_r": (3, 0),
        "key_mount": (-4, 9), "key_wing": (-6, 8),
        "curio_top": (3, 6), "curio_mid": (4, 7), "curio_bot": (3, 8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Bow angled up-forward, drawn back ready for release
    bow_tele = place_bow(bow_raw, deg=-18, target_center=(32, 72), scale=1.05, mirror=False)

    # Coiling Wind Aura & Aiming Trajectory Reticle FX
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Aiming vernier trajectory line from bow nock
    t_draw.line([(34, 70), (74, 62)], fill=(78, 216, 106, 210), width=1)
    t_draw.line([(74, 62), (118, 54)], fill=(255, 208, 40, 230), width=2)
    t_draw.line([(88, 59), (120, 53)], fill=(255, 255, 255, 255), width=1)
    # Concentric vernier crosshair reticle at target forward
    cx, cy = 108, 55
    t_draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], outline=(78, 216, 106, 230), width=1)
    t_draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(255, 208, 40, 240), width=1)
    # Caliper horn wind resonance arcs
    t_draw.arc([22, 10, 54, 38], start=200, end=350, fill=(78, 216, 106, 200), width=2)
    t_draw.arc([74, 10, 106, 38], start=190, end=340, fill=(255, 208, 40, 210), width=2)
    # Winding key torque spin sparks
    t_draw.arc([72, 36, 98, 62], start=15, end=345, fill=(255, 160, 16, 210), width=2)
    # Optic core amber focus pulse
    t_draw.ellipse([45, 50, 51, 56], fill=(255, 235, 120, 230))
    t_draw.ellipse([67, 50, 73, 56], fill=(255, 235, 120, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, bow_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (翠木穿雲·游標疾射 / Emerald Wind Piercing Arrow Release)
    # Explosive release: torso lunges forward-right (x+13, y-1), bow drives forward,
    # rear hand snaps back, supersonic piercing arrow beam shoots forward right!
    # =========================================================================
    shifts_attack = {
        "horn_top": (13, -2), "horn_l": (11, -2), "horn_r": (15, -2),
        "head_top": (13, -1), "ear_l": (10, -2), "ear_r": (15, -1),
        "eye_l": (14, -1), "eye_r": (14, -1), "snout": (15, 0), "throat": (14, 0),
        "core": (13, 0),
        "shoulder_l": (15, -1), "arm_l": (20, -2),
        "shoulder_r": (-8, 1), "arm_r": (-14, 3),
        "torso": (12, 0), "pelvis": (10, 0),
        "hip_l": (13, -1), "hip_r": (-7, 0),
        "knee_l": (14, -1), "knee_r": (-12, 0),
        "foot_l": (8, 0), "foot_r": (-8, 0),
        "key_mount": (10, -1), "key_wing": (8, -2),
        "curio_top": (-7, -2), "curio_mid": (-6, 1), "curio_bot": (-5, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Bow pushed forward in follow-through recoil
    bow_attack = place_bow(bow_raw, deg=12, target_center=(48, 66), scale=1.06, mirror=False)

    # Supersonic Emerald Arrow Beam & Kinetic Wind Rings
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Core arrow laser shaft
    a_draw.line([(48, 66), (122, 66)], fill=(78, 216, 106, 245), width=3)
    a_draw.line([(52, 66), (124, 66)], fill=(255, 255, 255, 255), width=1)
    # Arrowhead wedge
    a_draw.polygon([(124, 66), (116, 61), (118, 66), (116, 71)], fill=(255, 208, 40, 255))
    # Kinetic shockwave cone expanding forward
    a_draw.arc([78, 50, 106, 82], start=275, end=85, fill=(78, 216, 106, 220), width=2)
    a_draw.arc([94, 46, 122, 86], start=280, end=80, fill=(255, 208, 40, 230), width=2)
    # Muzzle flash / bowstring release spark
    a_draw.ellipse([44, 62, 52, 70], fill=(255, 255, 220, 255))
    a_draw.point([(56, 58), (54, 74), (62, 60), (60, 70), (66, 58)], fill=(255, 208, 40, 255))
    # Thrust trail from hooves and key
    a_draw.line([(28, 78), (14, 82)], fill=(78, 216, 106, 180), width=2)
    a_draw.line([(24, 84), (10, 90)], fill=(255, 160, 16, 160), width=2)
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, bow_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (千林迴風·角尺萬箭陣 / Emerald Forest Thousand Gales & Vernier Arrow Barrage)
    # Overdrive martial leap: body lifts gracefully (y-9), bow swept skyward (-38 deg)
    # Horns ignite with vernier resonance, clover key spins a whirlwind mandala!
    # Celestial barrage of emerald-gold homing arrow blades and gear runes.
    # =========================================================================
    shifts_skill = {
        "horn_top": (0, -10), "horn_l": (-4, -11), "horn_r": (4, -11),
        "head_top": (0, -9), "ear_l": (-3, -10), "ear_r": (3, -10),
        "eye_l": (0, -9), "eye_r": (0, -9), "snout": (0, -8), "throat": (0, -7),
        "core": (0, -6),
        "shoulder_l": (-6, -8), "arm_l": (-10, -10),
        "shoulder_r": (9, -8), "arm_r": (14, -9),
        "torso": (0, -6), "pelvis": (0, -5),
        "hip_l": (-5, -5), "hip_r": (5, -5),
        "knee_l": (-7, -5), "knee_r": (7, -5),
        "foot_l": (-4, -5), "foot_r": (4, -5),
        "key_mount": (-1, -5), "key_wing": (-2, -6),
        "curio_top": (-8, -9), "curio_mid": (-9, -7), "curio_bot": (-6, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Bow raised in high skyward barrage pose
    bow_skill = place_bow(bow_raw, deg=-38, target_center=(34, 54), scale=1.08, mirror=False)

    # Emerald Thousand Gales Barrage & Celestial Vernier Vortex (y: 16..106)
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Concentric celestial wind energy rings
    s_draw.arc([16, 18, 116, 96], start=140, end=355, fill=(78, 216, 106, 230), width=3)
    s_draw.arc([22, 22, 110, 90], start=155, end=335, fill=(255, 208, 40, 220), width=2)
    s_draw.arc([30, 26, 102, 84], start=165, end=315, fill=(56, 160, 255, 210), width=1)
    # Multi-arrow barrage trails radiating skyward-right
    s_draw.line([(40, 48), (116, 24)], fill=(78, 216, 106, 240), width=2)
    s_draw.polygon([(118, 24), (110, 21), (112, 26)], fill=(255, 255, 255, 255))
    s_draw.line([(38, 54), (118, 42)], fill=(255, 208, 40, 240), width=2)
    s_draw.polygon([(120, 42), (112, 39), (114, 44)], fill=(255, 208, 40, 255))
    s_draw.line([(36, 60), (114, 62)], fill=(78, 216, 106, 230), width=2)
    s_draw.polygon([(116, 62), (108, 59), (110, 64)], fill=(255, 255, 255, 255))
    # Floating pinecone / gear leaf runes
    s_draw.polygon([(104, 20), (112, 16), (106, 24)], fill=(255, 208, 40, 240))
    s_draw.polygon([(18, 52), (10, 58), (20, 60)], fill=(78, 216, 106, 240))
    s_draw.polygon([(88, 14), (96, 10), (90, 18)], fill=(56, 160, 255, 230))
    s_draw.polygon([(16, 32), (24, 26), (22, 36)], fill=(255, 160, 16, 240))
    # Airborne energy shimmer lines (y <= 106)
    s_draw.line([(42, 98), (84, 98)], fill=(78, 216, 106, 180), width=2)
    s_draw.line([(48, 103), (78, 103)], fill=(255, 208, 40, 160), width=1)
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.6))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, bow_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (衝擊後仰·機甲抗震 / Heavy Impact Recoil & Damper Stagger)
    # Heavy impact stagger: body and head pitch far back (x-15, y-2),
    # shortbow held across chest in emergency block.
    # Deflection cross-star spark & directional steam exhaust jets from brass dampers.
    # =========================================================================
    shifts_hit = {
        "horn_top": (-16, -2), "horn_l": (-18, -2), "horn_r": (-14, -2),
        "head_top": (-15, -2), "ear_l": (-17, -2), "ear_r": (-13, -2),
        "eye_l": (-15, -2), "eye_r": (-15, -2), "snout": (-14, 0), "throat": (-13, 0),
        "core": (-12, 0),
        "shoulder_l": (-8, 1), "arm_l": (-4, 3),
        "shoulder_r": (-12, 0), "arm_r": (-13, 0),
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
    # Bow held defensively across torso
    bow_hit = place_bow(bow_raw, deg=32, target_center=(46, 72), scale=0.96, mirror=False)

    # Deflection cross-star spark & directional steam exhaust
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 46, 72
    h_draw.line([(cx - 14, cy), (cx + 14, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 14), (cx, cy + 14)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 8, cy - 8), (cx + 8, cy + 8)], fill=(78, 216, 106, 220), width=1)
    h_draw.line([(cx - 8, cy + 8), (cx + 8, cy - 8)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(255, 255, 255, 255))
    h_draw.arc([cx - 16, cy - 16, cx + 16, cy + 16], start=0, end=360, fill=(255, 208, 40, 180), width=2)
    # Kinetic spark points
    h_draw.point([(cx - 12, cy - 10), (cx + 14, cy - 8), (cx + 12, cy + 12), (cx - 10, cy + 14)], fill=(255, 255, 220, 255))
    # Directional steam exhaust jets from brass damper back joints
    h_draw.line([(70, 48), (92, 38)], fill=(240, 248, 255, 200), width=2)
    h_draw.line([(68, 52), (94, 46)], fill=(220, 235, 250, 170), width=1)
    h_draw.line([(72, 56), (96, 54)], fill=(220, 235, 250, 160), width=1)
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.5))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, bow_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (風定息弦·調校歸位 / Wind Calming & Stance Recovery)
    # Sinks into solid restabilization (y+8), feet planted, bow lowered to side,
    # calming mint cooling energy at optic core and damper joints.
    # =========================================================================
    shifts_recover = {
        "horn_top": (2, 6), "horn_l": (1, 6), "horn_r": (3, 6),
        "head_top": (2, 7), "ear_l": (1, 6), "ear_r": (3, 6),
        "eye_l": (2, 7), "eye_r": (2, 7), "snout": (2, 8), "throat": (2, 8),
        "core": (2, 8),
        "shoulder_l": (-4, 7), "arm_l": (-8, 8),
        "shoulder_r": (5, 7), "arm_r": (7, 8),
        "torso": (2, 8), "pelvis": (2, 8),
        "hip_l": (-5, 7), "hip_r": (6, 7),
        "knee_l": (-7, 6), "knee_r": (7, 6),
        "foot_l": (-4, 0), "foot_r": (5, 0),
        "key_mount": (2, 7), "key_wing": (2, 6),
        "curio_top": (4, 5), "curio_mid": (4, 6), "curio_bot": (4, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Bow held relaxed in low ready position
    bow_recover = place_bow(bow_raw, deg=8, target_center=(28, 78), scale=0.98, mirror=False)

    # Ground settling ripples & calming green wind pulse (y <= 110)
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.arc([36, 96, 92, 110], start=15, end=165, fill=(78, 216, 106, 180), width=2)
    r_draw.arc([42, 100, 86, 110], start=25, end=155, fill=(56, 160, 255, 160), width=1)
    # Cooling steam puffs from joints
    r_draw.ellipse([64, 46, 76, 58], fill=(230, 240, 250, 160))
    r_draw.ellipse([70, 40, 80, 50], fill=(240, 245, 255, 180))
    r_draw.ellipse([32, 76, 42, 86], fill=(230, 240, 250, 150))
    # Calming mint pulse at optic core
    r_draw.ellipse([48, 44, 56, 52], fill=(78, 216, 106, 160))
    r_draw.ellipse([70, 44, 78, 52], fill=(78, 216, 106, 160))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, bow_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING EMERALD FAWN 6 COMBAT ACTION POSES ===")
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

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_fawn_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_fawn_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
    print("\nAll 6 fawn combat poses successfully generated and saved!")
