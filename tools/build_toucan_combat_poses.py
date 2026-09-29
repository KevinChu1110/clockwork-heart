#!/usr/bin/env python3
"""
tools/build_toucan_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Prism-Bill Toucan (第六十一族 彩喙巨嘴鳥, toucan)
in Clockwork Heart:
  game/assets/sprites/player/poses/toucan/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/toucan/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/toucan_battle.png & toucan_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_toucan_idle_vs_battle.png & proof_toucan_idle_vs_battle_512.png
  game/assets/sprites/player/proof_toucan_combat_poses_768.png & proof_toucan_combat_poses_magenta.png
  game/assets/sprites/player/proof_toucan_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Stamped brass alloy chassis & glazed ivory porcelain bib
  - Stamped openwork brass prism bill visor cowl with rainbow dopamine gradient
  - Emerald quartz optic monocle with gold crosshair reticle
  - Vine valley scout harvest harness vest in dopamine mint green
  - Multi-tier folding fan stamped copper rudder tail
  - Tri-vane canopy rotor brass winding key
  - Canopy prism pneumatic arquebus with petal muzzle brake and revolving feed disc
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageOps
import numpy as np

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/toucan"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/toucan"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_toucan_tri_vane_canopy_rotor_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_toucan_segmented_copper_rudder_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_toucan_canopy_alloy_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_toucan_prism_bill_visor_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_toucan_vine_valley_scout_harness.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_toucan_emerald_quartz_monocle.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_toucan_canopy_prism_pneumatic_arquebus.png").convert("RGBA")

# Extract ground shadow master from party toucan_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/toucan_idle.png").convert("RGBA")
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

# Canonical landmarks on Toucan (natural 128x128 space)
base_landmarks = {
    # Head & Rainbow Prism Bill Cowl
    "crest_top": (64, 14),
    "crest_ring": (64, 26),
    "cowl_top_l": (50, 26),
    "cowl_top_r": (78, 26),
    "cowl_cheek_l": (46, 48),
    "cowl_cheek_r": (80, 48),
    "optic_l": (54, 42),
    "optic_r": (74, 42),
    "bill_root": (72, 48),
    "bill_mid": (90, 48),
    "bill_tip": (107, 52),
    "bill_jaw": (90, 58),
    # Torso & Vine Valley Scout Harness
    "throat": (64, 62),
    "shoulder_l": (48, 66),
    "shoulder_r": (80, 66),
    "vest_chest": (64, 76),
    "wing_l": (40, 74),
    "arm_r": (88, 74),
    "vest_hem": (64, 94),
    # Curio (Segmented Copper Tail) & Chassis
    "curio_top": (28, 80),
    "curio_mid": (18, 91),
    "curio_bot": (24, 100),
    "curio_joint": (44, 86),
    "pelvis": (64, 95),
    # Legs & Bird Claws
    "thigh_l": (50, 98),
    "thigh_r": (76, 98),
    "knee_l": (50, 104),
    "knee_r": (76, 104),
    "foot_l": (50, 113),
    "foot_r": (76, 113),
    "claw_l_tip": (44, 117),
    "claw_r_tip": (82, 117),
}

src_pts = [base_landmarks[k] for k in base_landmarks] + anchors

# Canonical pivots on original 128x128 elements
KEY_PIVOT = (40.0, 30.0)
WEAPON_PIVOT = (86.0, 77.0)

# Build base body_core (z: curio=8, chassis=10, head=20, costume=25, optic=30)
# Note: key and weapon are articulated separately
raw_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
raw_body.alpha_composite(curio_src)
raw_body.alpha_composite(chassis_src)
raw_body.alpha_composite(head_src)
raw_body.alpha_composite(costume_src)
raw_body.alpha_composite(optic_src)

body_core = raw_body.copy()


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (林冠遊俠·瞄準待機站姿 / Canopy Ranger Readiness Stance)
    # Balanced 2.2-head toucan ranger stance.
    # Key placed at (40.0, 30.0).
    # Arquebus held ready at (83.0, 77.0), scale=0.95 (safely keeping muzzle x <= 122).
    # =========================================================================
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(40.0, 30.0), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(83.0, 77.0), scale=0.95)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(idle_key)
    idle_canvas.alpha_composite(body_core)
    idle_canvas.alpha_composite(idle_weapon)

    # Ambient subtle glint FX on optic monocle and arquebus petal muzzle
    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    i_draw.point((54, 42), fill=(255, 255, 255, 240))
    i_draw.point((74, 42), fill=(255, 255, 255, 240))
    i_draw.point((105, 52), fill=(255, 253, 248, 250))
    i_draw.point((121, 73), fill=(255, 208, 40, 220))
    idle_fx = idle_fx.filter(ImageFilter.GaussianBlur(0.3))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (林冠蓄壓·聚能瞄準預備姿態 / Pressure Coiling & Sniper Telegraph)
    # Low ranger crouch & aim: body drops and coils backward (-7, +8).
    # Head and bill tuck in, optics align down barrel axis.
    # Winding key counter-winds with high spring tension (-46 deg, target=(32, 40), scale=0.92).
    # Arquebus pulled back close to chest (-28 deg, target=(75, 78), scale=0.94).
    # FX: Soft mint-green/celestial-blue pressure targeting arcs around muzzle.
    # =========================================================================
    tele_offsets = {
        "crest_top": (-7, 8), "crest_ring": (-7, 8),
        "cowl_top_l": (-7, 8), "cowl_top_r": (-7, 8),
        "cowl_cheek_l": (-7, 8), "cowl_cheek_r": (-7, 8),
        "optic_l": (-7, 8), "optic_r": (-7, 8),
        "bill_root": (-7, 8), "bill_mid": (-6, 7), "bill_tip": (-6, 7), "bill_jaw": (-6, 7),
        "throat": (-7, 7), "shoulder_l": (-8, 7), "shoulder_r": (-6, 7),
        "vest_chest": (-7, 7), "wing_l": (-7, 6), "arm_r": (-9, 5),
        "vest_hem": (-6, 6),
        "curio_top": (-7, 7), "curio_mid": (-6, 6), "curio_bot": (-6, 5), "curio_joint": (-6, 5),
        "pelvis": (-5, 5),
        "thigh_l": (-5, 5), "thigh_r": (-2, 5),
        "knee_l": (-5, 4), "knee_r": (1, 4),
        "foot_l": (-2, 0), "foot_r": (1, 0),
        "claw_l_tip": (-2, 0), "claw_r_tip": (1, 0),
    }
    dst_tele = [(base_landmarks[k][0] + tele_offsets[k][0], base_landmarks[k][1] + tele_offsets[k][1]) for k in base_landmarks] + anchors
    warped_tele_body = warp_image_idw(body_core, src_pts, dst_tele, power=2.0, epsilon=4.0)
    tele_key = place_rotated_pivot(key_src, deg=-46, pivot=KEY_PIVOT, target=(32, 40), scale=0.92)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-28, pivot=WEAPON_PIVOT, target=(75, 78), scale=0.94)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric targeting arcs around drawn back arquebus barrel
    t_draw.arc([60, 56, 96, 92], start=150, end=340, fill=(78, 216, 106, 220), width=2)
    t_draw.arc([64, 60, 92, 88], start=170, end=320, fill=(56, 160, 255, 210), width=1)
    # Target alignment point
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.35))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(tele_key)
    tele_canvas.alpha_composite(warped_tele_body)
    tele_canvas.alpha_composite(tele_weapon)
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (氣動爆發·高壓重銃突射 / Pneumatic Discharge & Sniper Blast)
    # Forward lunging discharge: body surges forward (+15, -1).
    # Head & prism bill thrust forward (+15, -1). Bill tip: 107 + 14 = 121 (margin >= 4!).
    # Winding key spins clockwise releasing torque (+64 deg, target=(56, 30), scale=1.06).
    # Arquebus kicked forward with recoil impulse (+24 deg, target=(93, 72), scale=1.02).
    # FX: Supersonic muzzle flash, petal gas ring & needle spark.
    # =========================================================================
    atk_offsets = {
        "crest_top": (15, -1), "crest_ring": (15, -1),
        "cowl_top_l": (15, -1), "cowl_top_r": (15, -1),
        "cowl_cheek_l": (15, -1), "cowl_cheek_r": (15, -1),
        "optic_l": (15, -1), "optic_r": (15, -1),
        "bill_root": (15, -1), "bill_mid": (14, -1), "bill_tip": (14, -1), "bill_jaw": (14, -1),
        "throat": (14, -1), "shoulder_l": (12, -1), "shoulder_r": (15, -1),
        "vest_chest": (14, -1), "wing_l": (9, 0), "arm_r": (16, -2),
        "vest_hem": (12, 0),
        "curio_top": (10, -1), "curio_mid": (10, 0), "curio_bot": (10, 0), "curio_joint": (10, 0),
        "pelvis": (10, -1),
        "thigh_l": (7, 0), "thigh_r": (12, 0),
        "knee_l": (3, 0), "knee_r": (10, 0),
        "foot_l": (1, 0), "foot_r": (9, 0),
        "claw_l_tip": (1, 0), "claw_r_tip": (9, 0),
    }
    dst_atk = [(base_landmarks[k][0] + atk_offsets[k][0], base_landmarks[k][1] + atk_offsets[k][1]) for k in base_landmarks] + anchors
    warped_atk_body = warp_image_idw(body_core, src_pts, dst_atk, power=2.0, epsilon=4.0)
    atk_key = place_rotated_pivot(key_src, deg=64, pivot=KEY_PIVOT, target=(56, 30), scale=1.06)
    atk_weapon = place_rotated_pivot(weapon_src, deg=24, pivot=WEAPON_PIVOT, target=(93, 72), scale=1.02)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Supersonic petal muzzle blast shockwave arcs
    a_draw.arc([80, 48, 122, 90], start=280, end=80, fill=(255, 160, 16, 235), width=2)
    a_draw.arc([84, 52, 118, 86], start=295, end=65, fill=(255, 208, 40, 220), width=1)
    a_draw.arc([88, 56, 114, 82], start=305, end=55, fill=(56, 160, 255, 210), width=1)
    # Impact glint points at muzzle tip
    for px, py in [(116, 68), (120, 72), (118, 76), (112, 80), (122, 70)]:
        a_draw.point((px, py), fill=(255, 253, 248, 255))
        a_draw.point((px + 1, py), fill=(255, 160, 16, 240))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.35))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(atk_key)
    atk_canvas.alpha_composite(warped_atk_body)
    atk_canvas.alpha_composite(atk_weapon)
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (七彩稜鏡·林冠高空聚焦狙擊 / Prism Canopy Overload Sniper Beam)
    # Heroic elevated sniper skill stance!
    # Body lifts upward (y=-10), standing proud on tall claws.
    # Head & prism bill tilt skyward (y=-10).
    # Arquebus raised diagonally upward (+52 deg, target=(86, 58), scale=1.12).
    # Winding key overclocks (+90 deg, target=(40, 22), scale=1.08).
    # FX: Concentric rainbow prism reticle rings around elevated arquebus muzzle.
    # =========================================================================
    skl_offsets = {
        "crest_top": (0, -10), "crest_ring": (0, -10),
        "cowl_top_l": (0, -10), "cowl_top_r": (0, -10),
        "cowl_cheek_l": (0, -9), "cowl_cheek_r": (0, -9),
        "optic_l": (0, -9), "optic_r": (0, -9),
        "bill_root": (0, -9), "bill_mid": (0, -9), "bill_tip": (0, -9), "bill_jaw": (0, -9),
        "throat": (0, -7), "shoulder_l": (-1, -7), "shoulder_r": (1, -7),
        "vest_chest": (0, -7), "wing_l": (-4, -6), "arm_r": (4, -10),
        "vest_hem": (0, -5),
        "curio_top": (-2, -7), "curio_mid": (0, -6), "curio_bot": (0, -5), "curio_joint": (0, -5),
        "pelvis": (0, -3),
        "thigh_l": (-2, -2), "thigh_r": (2, -2),
        "knee_l": (-2, -1), "knee_r": (2, -1),
        "foot_l": (-1, 0), "foot_r": (2, 0),
        "claw_l_tip": (-1, 0), "claw_r_tip": (2, 0),
    }
    dst_skl = [(base_landmarks[k][0] + skl_offsets[k][0], base_landmarks[k][1] + skl_offsets[k][1]) for k in base_landmarks] + anchors
    warped_skl_body = warp_image_idw(body_core, src_pts, dst_skl, power=2.0, epsilon=4.0)
    skl_key = place_rotated_pivot(key_src, deg=90, pivot=KEY_PIVOT, target=(40, 22), scale=1.08)
    skl_weapon = place_rotated_pivot(weapon_src, deg=52, pivot=WEAPON_PIVOT, target=(86, 58), scale=1.12)

    skl_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skl_fx)
    # Luminous circular rainbow prism halo around elevated arquebus muzzle at (96, 42)
    s_draw.arc([76, 22, 116, 62], start=0, end=360, fill=(255, 208, 40, 220), width=1)
    s_draw.arc([80, 26, 112, 58], start=0, end=360, fill=(78, 216, 106, 200), width=1)
    s_draw.arc([84, 30, 108, 54], start=0, end=360, fill=(56, 160, 255, 240), width=1)

    # Prism sparkle points focused on the optical arc
    for sx, sy in [(96, 22), (114, 40), (78, 42), (106, 58), (88, 30)]:
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
    # 5. HIT (金屬震撼·受擊受挫硬直 / Impact Shock & Stagger Stance)
    # Violent backward jolt and recoil (-14, -5).
    # Head and bill thrown back sharply (-14, -5).
    # Torso jolts backward (-12, -3), pelvis (-8, -1).
    # Winding key knocked askew (-48 deg, target=(26, 28), scale=0.94).
    # Arquebus knocked off balance (-38 deg, target=(80, 84), scale=0.92).
    # FX: Starburst impact sparks on vest chest (54, 70), golden & mint green fragments.
    # =========================================================================
    hit_offsets = {
        "crest_top": (-14, -5), "crest_ring": (-14, -5),
        "cowl_top_l": (-14, -5), "cowl_top_r": (-14, -5),
        "cowl_cheek_l": (-14, -5), "cowl_cheek_r": (-14, -5),
        "optic_l": (-14, -5), "optic_r": (-14, -5),
        "bill_root": (-14, -5), "bill_mid": (-14, -5), "bill_tip": (-13, -5), "bill_jaw": (-13, -5),
        "throat": (-12, -4), "shoulder_l": (-12, -4), "shoulder_r": (-11, -4),
        "vest_chest": (-12, -3), "wing_l": (-10, -3), "arm_r": (-7, 4),
        "vest_hem": (-10, -2),
        "curio_top": (-9, 0), "curio_mid": (-8, 0), "curio_bot": (-8, 0), "curio_joint": (-8, 0),
        "pelvis": (-8, -1),
        "thigh_l": (-7, 0), "thigh_r": (-5, 0),
        "knee_l": (-5, 0), "knee_r": (-3, 0),
        "foot_l": (-3, 0), "foot_r": (-1, 0),
        "claw_l_tip": (-3, 0), "claw_r_tip": (-1, 0),
    }
    dst_hit = [(base_landmarks[k][0] + hit_offsets[k][0], base_landmarks[k][1] + hit_offsets[k][1]) for k in base_landmarks] + anchors
    warped_hit_body = warp_image_idw(body_core, src_pts, dst_hit, power=2.0, epsilon=4.0)
    hit_key = place_rotated_pivot(key_src, deg=-48, pivot=KEY_PIVOT, target=(26, 28), scale=0.94)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-38, pivot=WEAPON_PIVOT, target=(80, 84), scale=0.92)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Impact starburst on chest (54, 70)
    ix, iy = 54, 70
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
    # 6. RECOVER (低姿制動·落地卸勁姿態 / Grounded Landing & Recoil Recovery)
    # Deep grounded landing crouch: body bows forward, absorbs momentum (+2, +8).
    # Head and bill compress down (+2, +8).
    # Torso compresses down (+2, +7), pelvis (+2, +5).
    # Claws planted wide in grounded brake stance (foot_l -4, foot_r +4).
    # Arquebus tucked close defensively (-18 deg, target=(84, 82), scale=1.02).
    # Winding key re-engages drive (+20 deg, target=(42, 40), scale=0.98).
    # FX: Landing brake friction motes.
    # =========================================================================
    rec_offsets = {
        "crest_top": (2, 8), "crest_ring": (2, 8),
        "cowl_top_l": (2, 8), "cowl_top_r": (2, 8),
        "cowl_cheek_l": (2, 8), "cowl_cheek_r": (2, 8),
        "optic_l": (2, 8), "optic_r": (2, 8),
        "bill_root": (2, 8), "bill_mid": (2, 8), "bill_tip": (2, 8), "bill_jaw": (2, 8),
        "throat": (2, 7), "shoulder_l": (1, 7), "shoulder_r": (3, 7),
        "vest_chest": (2, 7), "wing_l": (-2, 7), "arm_r": (-3, 7),
        "vest_hem": (2, 6),
        "curio_top": (1, 6), "curio_mid": (2, 6), "curio_bot": (2, 5), "curio_joint": (2, 5),
        "pelvis": (2, 5),
        "thigh_l": (-4, 4), "thigh_r": (4, 4),
        "knee_l": (-4, 3), "knee_r": (4, 3),
        "foot_l": (-4, 0), "foot_r": (4, 0),
        "claw_l_tip": (-4, 0), "claw_r_tip": (4, 0),
    }
    dst_rec = [(base_landmarks[k][0] + rec_offsets[k][0], base_landmarks[k][1] + rec_offsets[k][1]) for k in base_landmarks] + anchors
    warped_rec_body = warp_image_idw(body_core, src_pts, dst_rec, power=2.0, epsilon=4.0)
    rec_key = place_rotated_pivot(key_src, deg=20, pivot=KEY_PIVOT, target=(42, 40), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=-18, pivot=WEAPON_PIVOT, target=(84, 82), scale=1.02)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    for fx, fy in [(46, 114), (52, 116), (74, 116), (80, 114)]:
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
    print("Generating The Prism-Bill Toucan combat action poses...")
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

    # Official battle asset: toucan_battle.png & toucan_battle_512.png (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = poses["attack"].resize((512, 512), Image.Resampling.LANCZOS)
    battle_128.save(f"{PLAYER_DIR}/toucan_battle.png")
    battle_512.save(f"{PLAYER_DIR}/toucan_battle_512.png")
    print(f"  ✓ Saved {PLAYER_DIR}/toucan_battle.png & toucan_battle_512.png (battle == attack)")

    # Proof: Idle vs Battle (128 & 512)
    idle_128 = poses["idle"]
    ivb_128 = Image.new("RGBA", (256, 128), (0, 0, 0, 0))
    ivb_128.paste(idle_128, (0, 0))
    ivb_128.paste(battle_128, (128, 0))
    ivb_128.save(f"{PLAYER_DIR}/proof_toucan_idle_vs_battle.png")

    ivb_512 = Image.new("RGBA", (1024, 512), (0, 0, 0, 0))
    ivb_512.paste(poses["idle"].resize((512, 512), Image.Resampling.LANCZOS), (0, 0))
    ivb_512.paste(battle_512, (512, 0))
    ivb_512.save(f"{PLAYER_DIR}/proof_toucan_idle_vs_battle_512.png")
    print(f"  ✓ Saved proof_toucan_idle_vs_battle.png & 512")

    # Proof sheets: 768x128 Transparent & Magenta
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(['idle', 'telegraph', 'attack', 'recover', 'skill', 'hit']):
        proof_768.paste(poses[p_name], (i * 128, 0), poses[p_name])
        proof_mag.paste(poses[p_name], (i * 128, 0), poses[p_name])
    proof_768.save(f"{PLAYER_DIR}/proof_toucan_combat_poses_768.png")
    proof_mag.save(f"{PLAYER_DIR}/proof_toucan_combat_poses_magenta.png")
    print(f"  ✓ Saved proof_toucan_combat_poses_768.png & proof_toucan_combat_poses_magenta.png")

    # 8x core crop of hit pose for vision inspection
    hit_crop = poses["hit"].crop((40, 30, 88, 78))
    hit_8x = hit_crop.resize((hit_crop.width * 8, hit_crop.height * 8), Image.Resampling.NEAREST)
    hit_8x.save(f"{PLAYER_DIR}/proof_toucan_hit_core_crop_8x.png")
    print(f"  ✓ Saved proof_toucan_hit_core_crop_8x.png")

    print("\n🎉 The Prism-Bill Toucan combat action poses built successfully!")


if __name__ == "__main__":
    main()
