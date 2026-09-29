#!/usr/bin/env python3
"""
tools/build_takin_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Bamboo-Cleaving Takin (第六十三族 破竹羚牛, takin)
in Clockwork Heart:
  game/assets/sprites/player/poses/takin/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/takin/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/takin_battle.png & takin_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_takin_idle_vs_battle.png & proof_takin_idle_vs_battle_512.png
  game/assets/sprites/player/proof_takin_combat_poses_768.png & proof_takin_combat_poses_magenta.png
  game/assets/sprites/player/proof_takin_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Bronze cast chassis with mint-green wear-resistant trim & ivory porcelain bib
  - Brass twisted horn cowl with polished horn tips
  - Emerald quartz visors optic core with warm green luminescence
  - Zen pioneer heavy robe with sunset orange piping & brass shoulder guard
  - Dual bamboo oil flasks & steam exhaust shock absorber valve curio
  - Tri-leaf zen brass winding key
  - Zen bamboo-cleaving battle axe with green-gold forged double blades
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/takin"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_takin_tri_leaf_zen_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_takin_dual_bamboo_oil_flasks.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_takin_bronze_cast_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_takin_brass_twisted_horn_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_takin_zen_pioneer_heavy_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_takin_emerald_quartz_visors.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_takin_zen_bamboo_cleaving_axe.png").convert("RGBA")

# Extract ground shadow master from party takin_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/takin_idle.png").convert("RGBA")
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = ref_shadow_im.load()
assert s_px is not None and c_px is not None

for y in range(118, 128):
    for x in range(128):
        s_px[x, y] = cast(tuple[int, int, int, int], c_px[x, y])

arr_shd = np.array(shadow_master)
EXPECTED_SHADOW = [int(np.sum(arr_shd[y, :, 3] > 20)) for y in range(118, 128)]
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

    # Clean outer boundary strictly (L>=4, R>=4, T>=4, B>=2)
    # y=0, 1, 2, 3 and y=126, 127
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 2] = (0, 0, 0, 0)
        o_px[x, 3] = (0, 0, 0, 0)
        o_px[x, 126] = (0, 0, 0, 0)
        o_px[x, 127] = (0, 0, 0, 0)
    # x=0, 1, 2, 3 and x=124, 125, 126, 127
    for y in range(128):
        o_px[0, y] = (0, 0, 0, 0)
        o_px[1, y] = (0, 0, 0, 0)
        o_px[2, y] = (0, 0, 0, 0)
        o_px[3, y] = (0, 0, 0, 0)
        o_px[124, y] = (0, 0, 0, 0)
        o_px[125, y] = (0, 0, 0, 0)
        o_px[126, y] = (0, 0, 0, 0)
        o_px[127, y] = (0, 0, 0, 0)

    # Clean ultra-dark pixels (<10 on all channels in opaque region)
    for y in range(128):
        for x in range(128):
            p = cast(tuple[int, int, int, int], o_px[x, y])
            if p[3] > 50 and p[0] < 10 and p[1] < 10 and p[2] < 10:
                o_px[x, y] = (31, 26, 58, p[3])

    return out


def place_rotated_pivot(elem_img: Image.Image, deg: float, pivot: tuple[float, float], target: tuple[float, float], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates an element around an exact pivot point and places it at target coordinates with subpixel precision."""
    b = elem_img.copy()
    if mirror:
        b = ImageOps.mirror(b)
    px, py = pivot
    tx, ty = target

    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    paste_x = int(round(128.0 - px))
    paste_y = int(round(128.0 - py))
    large.paste(b, (paste_x, paste_y))

    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        off_x = (nw - canvas_size) // 2
        off_y = (nh - canvas_size) // 2
        large = scaled.crop((off_x, off_y, off_x + canvas_size, off_y + canvas_size))

    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    out_x = int(round(tx - 128.0))
    out_y = int(round(ty - 128.0))
    out.paste(rotated, (out_x, out_y), rotated)
    return out


def warp_image_idw(src_img: Image.Image, src_points: list[tuple[int, int]], dst_points: list[tuple[int, int]], power: float = 2.0, epsilon: float = 4.0) -> Image.Image:
    """Smooth Inverse Distance Weighting (IDW) landmark warp for mechanical body articulation."""
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


# Boundary and stabilization anchors ensuring edge stability and ground shadow preservation
anchors = [
    (0, 0), (127, 0), (0, 127), (127, 127),
    (64, 0), (0, 64), (127, 64), (64, 127),
    (32, 0), (96, 0), (0, 32), (0, 96),
    (127, 32), (127, 96),
    (20, 116), (64, 116), (108, 116)
]

# Canonical landmarks on Takin (natural 128x128 space, with head calibrated down 3px for margin >= 4)
# In raw slice, horn top was y=1, optic was y=42.
# Shifting head and optic down 3px places horn tip at y=4, optic at y=45.
head_shift = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
head_shift.paste(head_src, (0, 3), head_src)

optic_shift = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
optic_shift.paste(optic_src, (0, 3), optic_src)

base_landmarks = {
    # Head & Brass Twisted Horn Cowl (calibrated with horn tip y=4)
    "horn_tip_l": (38, 4),
    "horn_tip_r": (90, 4),
    "horn_mid_l": (42, 18),
    "horn_mid_r": (86, 18),
    "head_top": (64, 20),
    "cowl_cheek_l": (42, 48),
    "cowl_cheek_r": (86, 48),
    "optic_l": (54, 45),
    "optic_r": (74, 45),
    "snout_tip": (64, 55),
    "jaw_chin": (64, 62),
    # Torso & Zen Pioneer Robe & Shoulder Guard
    "throat": (64, 64),
    "shoulder_l": (38, 68),
    "shoulder_r": (84, 68),
    "chest_plate": (64, 76),
    "arm_l": (36, 78),
    "arm_r": (86, 78),
    "robe_hem": (64, 94),
    # Curio (Dual Bamboo Oil Flasks)
    "curio_top": (24, 68),
    "curio_mid": (28, 80),
    "curio_bot": (30, 92),
    # Chassis & Heavy Legs
    "pelvis": (64, 98),
    "thigh_l": (48, 104),
    "thigh_r": (80, 104),
    "knee_l": (46, 110),
    "knee_r": (82, 110),
    "foot_l": (44, 118),
    "foot_r": (84, 118),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots on original 128x128 elements
KEY_PIVOT = (38.6, 29.4)
WEAPON_PIVOT = (89.0, 80.0)

# Build base body_core (z: curio=8, chassis=10, head=20, costume=25, optic=30)
# Note: key and weapon are articulated separately
raw_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
raw_body.alpha_composite(curio_src)
raw_body.alpha_composite(chassis_src)
raw_body.alpha_composite(head_shift)
raw_body.alpha_composite(costume_src)
raw_body.alpha_composite(optic_shift)

body_core = raw_body.copy()


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (磐石扎馬·靜觀待機 / Zen Pioneer Readiness Stance)
    # Balanced 2.2-head takin warrior stance.
    # Key placed at (38.6, 29.4).
    # Axe held ready at (86.0, 80.0), scale=0.96 (safely keeping right margin >= 4).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(38.6, 29.4), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(86.0, 80.0), scale=0.96)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    # Ambient subtle glint FX on emerald visors and axe blade edge
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((54, 45), fill=(255, 255, 255, 240))
    i_draw.point((74, 45), fill=(255, 255, 255, 240))
    i_draw.point((118, 42), fill=(255, 208, 40, 230))
    i_draw.point((78, 44), fill=(78, 216, 106, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (破竹蓄勁·沉身背斧引勢 / Heavy Coil & Axe Draw Telegraph)
    # Heavy warrior back-step crouch & windup: body coils backward & down (-6, +6).
    # Head & horns tuck in, bracing for cleave (-6, +6).
    # Winding key counter-winds with high spring tension (-46 deg, target=(30, 36), scale=0.92).
    # Cleaving axe hoisted high behind shoulder (-42 deg, target=(73, 62), scale=0.95).
    # FX: Concentric mint-green & warm gold tension suction arcs around drawn axe head.
    # =========================================================================
    tele_offsets = {
        "horn_tip_l": (-6, 5), "horn_tip_r": (-6, 5),
        "horn_mid_l": (-6, 6), "horn_mid_r": (-6, 6),
        "head_top": (-6, 6),
        "cowl_cheek_l": (-6, 6), "cowl_cheek_r": (-6, 6),
        "optic_l": (-6, 6), "optic_r": (-6, 6),
        "snout_tip": (-6, 6), "jaw_chin": (-6, 6),
        "throat": (-6, 6), "shoulder_l": (-7, 6), "shoulder_r": (-5, 6),
        "chest_plate": (-6, 6), "arm_l": (-6, 5), "arm_r": (-8, 4),
        "robe_hem": (-5, 5),
        "curio_top": (-6, 6), "curio_mid": (-5, 5), "curio_bot": (-5, 4),
        "pelvis": (-4, 4),
        "thigh_l": (-4, 4), "thigh_r": (-1, 4),
        "knee_l": (-4, 3), "knee_r": (1, 3),
        "foot_l": (-2, 0), "foot_r": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-46, pivot=KEY_PIVOT, target=(30, 36), scale=0.92)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-42, pivot=WEAPON_PIVOT, target=(73, 62), scale=0.95)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Suction power arcs around hoisted axe blade
    t_draw.arc([52, 28, 98, 74], start=160, end=330, fill=(78, 216, 106, 220), width=2)
    t_draw.arc([56, 32, 94, 70], start=180, end=310, fill=(255, 208, 40, 210), width=1)
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (天元開山·泰山壓頂破竹重劈 / Earth-Splitting Bamboo Cleave)
    # Massive forward lunging downward strike: body surges forward (+14, 0).
    # Head & horns thrust forward to crush obstacles (+14, 0).
    # Cleaving axe swung down with colossal torque (+34 deg, target=(96, 75), scale=0.98).
    # Winding key uncoils with full spring release (+62 deg, target=(54, 28), scale=1.06).
    # FX: Sweeping curved crescent blade shockwave of pure bamboo-green & sun-gold.
    # =========================================================================
    atk_offsets = {
        "horn_tip_l": (14, 0), "horn_tip_r": (14, 0),
        "horn_mid_l": (14, 0), "horn_mid_r": (14, 0),
        "head_top": (14, 0),
        "cowl_cheek_l": (14, 0), "cowl_cheek_r": (14, 0),
        "optic_l": (14, 0), "optic_r": (14, 0),
        "snout_tip": (14, 0), "jaw_chin": (14, 0),
        "throat": (13, 0), "shoulder_l": (11, 0), "shoulder_r": (14, 0),
        "chest_plate": (13, 0), "arm_l": (9, 0), "arm_r": (15, -1),
        "robe_hem": (11, 0),
        "curio_top": (9, 0), "curio_mid": (9, 0), "curio_bot": (9, 0),
        "pelvis": (9, 0),
        "thigh_l": (6, 0), "thigh_r": (11, 0),
        "knee_l": (3, 0), "knee_r": (9, 0),
        "foot_l": (1, 0), "foot_r": (8, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=62, pivot=KEY_PIVOT, target=(54, 28), scale=1.06)
    atk_weapon = place_rotated_pivot(weapon_src, deg=34, pivot=WEAPON_PIVOT, target=(96, 75), scale=0.98)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Sweeping cleave impact crescent arc
    a_draw.arc([80, 36, 122, 102], start=275, end=85, fill=(78, 216, 106, 240), width=2)
    a_draw.arc([84, 40, 118, 98], start=290, end=70, fill=(255, 208, 40, 230), width=1)
    a_draw.arc([88, 44, 114, 94], start=300, end=60, fill=(255, 253, 248, 220), width=1)
    # Spark points along cutting edge
    for px, py in [(118, 62), (120, 68), (117, 76), (110, 84), (121, 65)]:
        a_draw.point((px, py), fill=(255, 253, 248, 255))
        a_draw.point((px + 1, py), fill=(255, 208, 40, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (狂風破竹·天元旋風千鈞橫掃 / Zen Gale Cleave & Overdrive Whirlwind)
    # Heroic elevated warrior stance: body lifts upward (y=-9), standing proud.
    # Horns tilt high into the sky, commanding the dojo.
    # Cleaving axe held aloft horizontally with supreme dominance (+74 deg, target=(82, 54), scale=1.06).
    # Winding key overclocks (+90 deg, target=(38, 20), scale=1.10).
    # FX: Whirling octagonal zen bamboo blade tempest halo around body & elevated axe.
    # =========================================================================
    skl_offsets = {
        "horn_tip_l": (0, -9), "horn_tip_r": (0, -9),
        "horn_mid_l": (0, -9), "horn_mid_r": (0, -9),
        "head_top": (0, -9),
        "cowl_cheek_l": (0, -8), "cowl_cheek_r": (0, -8),
        "optic_l": (0, -8), "optic_r": (0, -8),
        "snout_tip": (0, -8), "jaw_chin": (0, -8),
        "throat": (0, -7), "shoulder_l": (-1, -7), "shoulder_r": (1, -7),
        "chest_plate": (0, -6), "arm_l": (-4, -6), "arm_r": (4, -9),
        "robe_hem": (0, -5),
        "curio_top": (-2, -7), "curio_mid": (0, -6), "curio_bot": (0, -5),
        "pelvis": (0, -3),
        "thigh_l": (-2, -2), "thigh_r": (2, -2),
        "knee_l": (-2, -1), "knee_r": (2, -1),
        "foot_l": (-1, 0), "foot_r": (2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=90, pivot=KEY_PIVOT, target=(38, 20), scale=1.10)
    skl_weapon = place_rotated_pivot(weapon_src, deg=74, pivot=WEAPON_PIVOT, target=(82, 54), scale=1.06)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Dynamic zen cyclone rings around elevated axe and chest (open arcs to avoid internal void traps)
    s_draw.arc([68, 24, 116, 72], start=30, end=310, fill=(78, 216, 106, 220), width=1)
    s_draw.arc([72, 28, 112, 68], start=50, end=290, fill=(255, 208, 40, 210), width=1)
    s_draw.arc([30, 48, 98, 106], start=45, end=225, fill=(56, 160, 255, 200), width=1)
    for sx, sy in [(92, 24), (114, 46), (70, 48), (106, 68), (84, 30)]:
        s_draw.point((sx, sy), fill=(255, 208, 40, 240))
        s_draw.point((sx + 1, sy), fill=(255, 253, 248, 255))
    skl_fx = skl_fx.filter(ImageFilter.GaussianBlur(0.35))

    skl_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skl_canvas.alpha_composite(skl_key)
    skl_canvas.alpha_composite(warped_skl_body)
    skl_canvas.alpha_composite(skl_weapon)
    skl_canvas.alpha_composite(skl_fx)
    poses["skill"] = enforce_ground_shadow(skl_canvas)

    # =========================================================================
    # 5. HIT (厚甲震顫·重裝受擊硬直 / Heavy Plate Impact & Recoil Stagger)
    # Violent backward jolt and stagger (-14, -5).
    # Head and massive horns thrown back sharply (-14, -5).
    # Torso jolts backward (-12, -4), pelvis (-8, -2).
    # Winding key knocked askew (-48 deg, target=(24, 26), scale=0.94).
    # Cleaving axe knocked off-balance downward & backward (-38 deg, target=(76, 86), scale=0.92).
    # FX: High-energy starburst collision fragments on ivory porcelain bib & bronze plate.
    # =========================================================================
    hit_offsets = {
        "horn_tip_l": (-14, -4), "horn_tip_r": (-14, -4),
        "horn_mid_l": (-14, -4), "horn_mid_r": (-14, -4),
        "head_top": (-14, -4),
        "cowl_cheek_l": (-14, -4), "cowl_cheek_r": (-14, -4),
        "optic_l": (-14, -4), "optic_r": (-14, -4),
        "snout_tip": (-14, -4), "jaw_chin": (-14, -4),
        "throat": (-12, -4), "shoulder_l": (-12, -4), "shoulder_r": (-11, -4),
        "chest_plate": (-12, -3), "arm_l": (-10, -3), "arm_r": (-7, 4),
        "robe_hem": (-10, -2),
        "curio_top": (-9, 0), "curio_mid": (-8, 0), "curio_bot": (-8, 0),
        "pelvis": (-8, -1),
        "thigh_l": (-7, 0), "thigh_r": (-5, 0),
        "knee_l": (-5, 0), "knee_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-48, pivot=KEY_PIVOT, target=(24, 26), scale=0.94)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-38, pivot=WEAPON_PIVOT, target=(76, 86), scale=0.92)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact starburst sparks on chest plate (54, 72)
    ix, iy = 54, 72
    for pt in [(ix - 8, iy - 6), (ix + 8, iy - 6), (ix + 10, iy + 5), (ix - 7, iy + 8), (ix + 11, iy - 1), (ix - 9, iy + 1)]:
        h_draw.point(pt, fill=(255, 208, 40, 255))
        h_draw.ellipse([pt[0] - 1, pt[1] - 1, pt[0] + 1, pt[1] + 1], fill=(255, 253, 248, 220))
    for pt in [(ix - 5, iy - 3), (ix + 5, iy + 3), (ix + 3, iy - 5), (ix - 3, iy + 5)]:
        h_draw.point(pt, fill=(78, 216, 106, 240))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.35))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(hit_key)
    hit_canvas.alpha_composite(warped_hit_body)
    hit_canvas.alpha_composite(hit_weapon)
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (八角扎馬·落地卸勁制動 / Heavy Stance Brake & Ground Landing)
    # Deep grounded landing crouch: body bows forward, absorbs recoil momentum (+2, +7).
    # Head and horns compress down (+2, +7).
    # Legs planted wide in grounded stance (foot_l -4, foot_r +4).
    # Cleaving axe planted firmly into ground defensively (-16 deg, target=(84, 83), scale=1.01).
    # Winding key re-engages drive (+20 deg, target=(40, 38), scale=0.98).
    # FX: Ground brake friction motes on stone floor.
    # =========================================================================
    rec_offsets = {
        "horn_tip_l": (2, 7), "horn_tip_r": (2, 7),
        "horn_mid_l": (2, 7), "horn_mid_r": (2, 7),
        "head_top": (2, 7),
        "cowl_cheek_l": (2, 7), "cowl_cheek_r": (2, 7),
        "optic_l": (2, 7), "optic_r": (2, 7),
        "snout_tip": (2, 7), "jaw_chin": (2, 7),
        "throat": (2, 6), "shoulder_l": (1, 6), "shoulder_r": (3, 6),
        "chest_plate": (2, 6), "arm_l": (-2, 6), "arm_r": (-3, 6),
        "robe_hem": (2, 5),
        "curio_top": (1, 5), "curio_mid": (2, 5), "curio_bot": (2, 4),
        "pelvis": (2, 4),
        "thigh_l": (-4, 4), "thigh_r": (4, 4),
        "knee_l": (-4, 3), "knee_r": (4, 3),
        "foot_l": (-4, 0), "foot_r": (4, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=20, pivot=KEY_PIVOT, target=(40, 38), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-16, pivot=WEAPON_PIVOT, target=(84, 83), scale=1.01)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for fx, fy in [(44, 114), (50, 116), (76, 116), (82, 114)]:
        r_draw.point((fx, fy), fill=(255, 208, 40, 230))
        r_draw.point((fx, fy - 1), fill=(255, 253, 248, 240))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.3))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(rec_key)
    rec_canvas.alpha_composite(warped_rec_body)
    rec_canvas.alpha_composite(rec_weapon)
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses


def main():
    print("Generating The Bamboo-Cleaving Takin combat action poses...")
    poses = generate_poses()

    for p_name in ['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']:
        im = poses[p_name]
        path_128 = f"{OUT_DIR}/{p_name}.png"
        im.save(path_128)
        print(f"  ✓ Saved {p_name:10s} 128x128: {path_128}, bbox={im.getbbox()}")

        # 512x512 LANCZOS upscale
        im_512 = im.resize((512, 512), Image.Resampling.LANCZOS)
        path_512 = f"{OUT_DIR}/{p_name}_512.png"
        im_512.save(path_512)
        print(f"  ✓ Saved {p_name:10s} 512x512: {path_512}")

    # Official battle asset: takin_battle.png & takin_battle_512.png (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = poses["attack"].resize((512, 512), Image.Resampling.LANCZOS)
    battle_128.save(f"{PLAYER_DIR}/takin_battle.png")
    battle_512.save(f"{PLAYER_DIR}/takin_battle_512.png")
    print(f"  ✓ Saved {PLAYER_DIR}/takin_battle.png & takin_battle_512.png (battle == attack)")

    # Proof: Idle vs Battle (128 & 512)
    idle_128 = poses["idle"]
    ivb_128 = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
    ivb_128.paste(idle_128, (0, 0))
    ivb_128.paste(battle_128, (128, 0))
    ivb_128.save(f"{PLAYER_DIR}/proof_takin_idle_vs_battle.png")

    ivb_512 = Image.new("RGBA", (1024, 512), (0, 0, 0, 0))
    ivb_512.paste(poses["idle"].resize((512, 512), Image.Resampling.LANCZOS), (0, 0))
    ivb_512.paste(battle_512, (512, 0))
    ivb_512.save(f"{PLAYER_DIR}/proof_takin_idle_vs_battle_512.png")
    print(f"  ✓ Saved proof_takin_idle_vs_battle.png & 512")

    # Proof sheets: 768x128 Transparent & Magenta
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']):
        proof_768.paste(poses[p_name], (i * 128, 0), poses[p_name])
        proof_mag.paste(poses[p_name], (i * 128, 0), poses[p_name])
    proof_768.save(f"{PLAYER_DIR}/proof_takin_combat_poses_768.png")
    proof_mag.save(f"{PLAYER_DIR}/proof_takin_combat_poses_magenta.png")
    print(f"  ✓ Saved proof_takin_combat_poses_768.png & proof_takin_combat_poses_magenta.png")

    # 8x core crop of hit pose for vision inspection
    hit_crop = poses["hit"].crop((40, 30, 88, 78))
    hit_8x = hit_crop.resize((hit_crop.width * 8, hit_crop.height * 8), Image.Resampling.NEAREST)
    hit_8x.save(f"{PLAYER_DIR}/proof_takin_hit_core_crop_8x.png")
    print(f"  ✓ Saved proof_takin_hit_core_crop_8x.png")

    print("\n🎉 The Bamboo-Cleaving Takin combat action poses built successfully!")


if __name__ == "__main__":
    main()
