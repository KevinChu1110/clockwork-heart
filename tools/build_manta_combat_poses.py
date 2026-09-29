#!/usr/bin/env python3
"""
tools/build_manta_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Tidal Manta (第六十七族 潮汐蝠魟, manta)
in Clockwork Heart:
  game/assets/sprites/player/poses/manta/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/manta/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Also generates:
  game/assets/sprites/player/manta_battle.png & manta_battle_512.png (battle == attack per review.md 4b-8-1)
  game/assets/sprites/player/proof_manta_idle_vs_battle.png & proof_manta_idle_vs_battle_512.png
  game/assets/sprites/player/proof_manta_combat_poses_768.png & proof_manta_combat_poses_magenta.png
  game/assets/sprites/player/proof_manta_hit_core_crop_8x.png
Follows CANON.md, art_direction.md, TIDAL_MANTA_DESIGN_PROPOSAL.md, and review.md quality gates:
  - 0-QA16 / 0-QA21 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
"""

import math
import os
import sys
from typing import cast
from PIL import Image, ImageDraw, ImageOps
import numpy as np

sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/manta"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/manta"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(PLAYER_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_manta_starfish_gear_brass.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_manta_flexible_wings_antenna_tail.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_manta_titanium_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_manta_hydrofoil_horn_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_manta_diver_harness_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_manta_high_pressure_quartz_goggles.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_manta_hydro_compound_bow.png").convert("RGBA")

# Harmonize bow arrow-rest light band into quartz cyan (#60C3F0) to prevent white handle appearance
w_arr = np.array(weapon_src)
bright_band = (w_arr[:, :, 3] > 200) & (w_arr[:, :, 0] > 220) & (w_arr[:, :, 1] > 240) & (w_arr[:, :, 2] > 240)
w_arr[bright_band, 0] = 60
w_arr[bright_band, 1] = 195
w_arr[bright_band, 2] = 240
weapon_src = Image.fromarray(w_arr)

# Extract ground shadow master from party/manta_idle.png
ref_shadow_im = Image.open(f"{PLAYER_DIR}/party/manta_idle.png").convert("RGBA")
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

    # Clean stray low-alpha fringe pixels (< 20 alpha in body zone) to avoid dirty halos
    for y in range(0, 118):
        for x in range(0, 128):
            p = cast(tuple[int, int, int, int], o_px[x, y])
            if 0 < p[3] < 20:
                o_px[x, y] = (0, 0, 0, 0)

    # Sanitize dark falloff (ultra-dark pixels) to canon dark outline (#1F1A3A)
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


# Canonical pivots on original 128x128 elements
KEY_PIVOT = (38.6, 29.8)
CURIO_PIVOT = (52.8, 69.0)
HEAD_PIVOT = (64.0, 36.5)
TORSO_PIVOT = (63.0, 88.9)
WEAPON_PIVOT = (37.3, 72.1)

# Modular groups
head_group = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
head_group.alpha_composite(head_src)
head_group.alpha_composite(optic_src)

torso_group = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
torso_group.alpha_composite(chassis_src)
torso_group.alpha_composite(costume_src)


def draw_clean_spark(draw: ImageDraw.ImageDraw, x: int, y: int, color_core=(255, 253, 248, 255), color_edge=(255, 208, 40, 220)):
    """Draws a crisp, anti-aliased cross-star glint without blurry halo artifacts."""
    draw.point((x, y), fill=color_core)
    draw.point((x - 1, y), fill=color_edge)
    draw.point((x + 1, y), fill=color_edge)
    draw.point((x, y - 1), fill=color_edge)
    draw.point((x, y + 1), fill=color_edge)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (巡弋滑行·深海警戒 / Abyssal Gliding Neutral Ready)
    # Neutral, poised, balanced ready posture.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(38.6, 29.8), scale=1.0)
    p_curio = place_rotated_pivot(curio_src, deg=0, pivot=CURIO_PIVOT, target=(52.8, 69.0), scale=1.0)
    p_torso = place_rotated_pivot(torso_group, deg=0, pivot=TORSO_PIVOT, target=(63.0, 88.9), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=0, pivot=HEAD_PIVOT, target=(64.0, 36.5), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(37.3, 72.1), scale=1.0)

    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas.alpha_composite(p_key)
    idle_canvas.alpha_composite(p_curio)
    idle_canvas.alpha_composite(p_torso)
    idle_canvas.alpha_composite(p_head)
    idle_canvas.alpha_composite(p_weapon)

    idle_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    i_draw = ImageDraw.Draw(idle_fx)
    draw_clean_spark(i_draw, 52, 44, color_core=(255, 255, 255, 255), color_edge=(78, 216, 106, 220))
    draw_clean_spark(i_draw, 76, 44, color_core=(255, 255, 255, 255), color_edge=(78, 216, 106, 220))
    draw_clean_spark(i_draw, 42, 17, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 200))
    draw_clean_spark(i_draw, 86, 17, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 200))
    idle_canvas.alpha_composite(idle_fx)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (流體阻尼蓄力·石英測距鎖定 / Hydraulic Drawback & Quartz Targeting)
    # Deep draw crouch: Torso sinks down (y+6, x-3, deg=-4).
    # Head tucks low to protect chassis (y+7, x-4, deg=-5).
    # Wings sweep back (deg=-12, target=(48, 73), scale=0.96).
    # Key counter-winds with high spring torque (-34 deg, target=(32.0, 36.0), scale=0.96).
    # Bow drawn tight: deg=-22, target=(33.0, 71.0), scale=1.05.
    # FX: Concentric targeting reticle at (106, 50).
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=-34, pivot=KEY_PIVOT, target=(32.0, 36.0), scale=0.96)
    p_curio = place_rotated_pivot(curio_src, deg=-12, pivot=CURIO_PIVOT, target=(48.0, 73.0), scale=0.96)
    p_torso = place_rotated_pivot(torso_group, deg=-4, pivot=TORSO_PIVOT, target=(60.0, 94.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-5, pivot=HEAD_PIVOT, target=(60.0, 43.5), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=-22, pivot=WEAPON_PIVOT, target=(33.0, 71.0), scale=1.05)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas.alpha_composite(p_key)
    tele_canvas.alpha_composite(p_curio)
    tele_canvas.alpha_composite(p_torso)
    tele_canvas.alpha_composite(p_head)
    tele_canvas.alpha_composite(p_weapon)

    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    cx, cy = 106, 50
    t_draw.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], outline=(255, 208, 40, 220), width=1)
    t_draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], outline=(78, 216, 106, 230), width=1)
    t_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 208, 40, 240), width=1)
    t_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 208, 40, 240), width=1)
    draw_clean_spark(t_draw, cx, cy, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 240))
    draw_clean_spark(t_draw, 32, 36, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 220))
    tele_canvas.alpha_composite(tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK / BATTLE (海淵脈衝擊發·穿浪疾射 / Hydro-Pulse Piercing Arrow Release)
    # Violent lunge forward-right: Torso leans aggressively forward (deg=+10, target=(73.0, 88.0)).
    # Head thrusts forward with predatory aim (deg=+12, target=(76.0, 36.0)).
    # Flexible wings flap forward with tremendous thrust (deg=+18, target=(64.0, 66.0), scale=1.06).
    # Bow driven forward: deg=+18, target=(54.0, 68.0), scale=1.08.
    # Arrow projectile clearly rendered: shaft + arrowhead wedge polygon!
    # Winding key spins forward (+45 deg, target=(48.0, 28.0), scale=1.04).
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=45, pivot=KEY_PIVOT, target=(48.0, 28.0), scale=1.04)
    p_curio = place_rotated_pivot(curio_src, deg=18, pivot=CURIO_PIVOT, target=(64.0, 66.0), scale=1.06)
    p_torso = place_rotated_pivot(torso_group, deg=10, pivot=TORSO_PIVOT, target=(73.0, 88.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=12, pivot=HEAD_PIVOT, target=(76.0, 36.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=18, pivot=WEAPON_PIVOT, target=(54.0, 68.0), scale=1.08)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas.alpha_composite(p_key)
    atk_canvas.alpha_composite(p_curio)
    atk_canvas.alpha_composite(p_torso)
    atk_canvas.alpha_composite(p_head)
    atk_canvas.alpha_composite(p_weapon)

    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Arrow shaft (solid, non-vector appearance)
    a_draw.line([(54, 67), (120, 67)], fill=(56, 160, 255, 245), width=3)
    a_draw.line([(58, 67), (122, 67)], fill=(255, 255, 255, 255), width=1)
    # Solid forged brass arrowhead wedge polygon
    a_draw.polygon([(122, 67), (114, 62), (116, 67), (114, 72)], fill=(255, 208, 40, 255))
    # Muzzle / release flash sparks
    draw_clean_spark(a_draw, 122, 67, color_core=(255, 255, 255, 255), color_edge=(255, 208, 40, 240))
    draw_clean_spark(a_draw, 48, 28, color_core=(255, 255, 255, 255), color_edge=(255, 94, 138, 220))
    draw_clean_spark(a_draw, 56, 67, color_core=(255, 255, 255, 255), color_edge=(78, 216, 106, 240))
    atk_canvas.alpha_composite(atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (流體制動·減壓緩衝接地 / Hydro-Dynamic Brake & Cushion Landing)
    # Low grounded landing crouch: body absorbs recoil (+2, +7, deg=+2).
    # Head and cowl sink down (+2, +7).
    # Wings expand broad and low to brake (deg=-6, target=(54.0, 74.0), scale=1.04).
    # Key re-engages into main drive (+16 deg, target=(40.0, 36.0), scale=0.98).
    # Bow lowered: deg=-14, target=(38.0, 75.0), scale=1.0.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=16, pivot=KEY_PIVOT, target=(40.0, 36.0), scale=0.98)
    p_curio = place_rotated_pivot(curio_src, deg=-6, pivot=CURIO_PIVOT, target=(54.0, 74.0), scale=1.04)
    p_torso = place_rotated_pivot(torso_group, deg=2, pivot=TORSO_PIVOT, target=(64.0, 94.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=3, pivot=HEAD_PIVOT, target=(65.0, 43.5), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=-14, pivot=WEAPON_PIVOT, target=(38.0, 75.0), scale=1.0)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas.alpha_composite(p_key)
    rec_canvas.alpha_composite(p_curio)
    rec_canvas.alpha_composite(p_torso)
    rec_canvas.alpha_composite(p_head)
    rec_canvas.alpha_composite(p_weapon)

    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    draw_clean_spark(r_draw, 40, 36, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 210))
    rec_canvas.alpha_composite(rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (奧義·海潮天裂·流體超壓全彈齊射 / Abyssal Overpressure Maelstrom)
    # Majestic upward surge: Torso lifts up (deg=0, target=(63.0, 80.0)).
    # Head looks skyward with celestial majesty (deg=-10, target=(64.0, 27.0)).
    # Wings spread magnificently wide (deg=0, target=(53.0, 58.0), scale=1.18)!
    # High-angle skyward archery barrage: bow raised overhead (-52 deg, target=(44.0, 52.0), scale=1.15).
    # Winding key reaches supercharged torque (+70 deg, target=(40.0, 20.0), scale=1.10).
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=70, pivot=KEY_PIVOT, target=(40.0, 20.0), scale=1.10)
    p_curio = place_rotated_pivot(curio_src, deg=0, pivot=CURIO_PIVOT, target=(53.0, 58.0), scale=1.18)
    p_torso = place_rotated_pivot(torso_group, deg=0, pivot=TORSO_PIVOT, target=(63.0, 80.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-10, pivot=HEAD_PIVOT, target=(64.0, 27.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=-52, pivot=WEAPON_PIVOT, target=(44.0, 52.0), scale=1.15)

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas.alpha_composite(p_key)
    skill_canvas.alpha_composite(p_curio)
    skill_canvas.alpha_composite(p_torso)
    skill_canvas.alpha_composite(p_head)
    skill_canvas.alpha_composite(p_weapon)

    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    draw_clean_spark(s_draw, 40, 20, color_core=(255, 255, 255, 255), color_edge=(255, 94, 138, 220))
    draw_clean_spark(s_draw, 44, 9, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 220))
    draw_clean_spark(s_draw, 88, 9, color_core=(255, 250, 185, 240), color_edge=(255, 208, 40, 220))
    draw_clean_spark(s_draw, 44, 48, color_core=(255, 255, 255, 255), color_edge=(56, 160, 255, 240))
    draw_clean_spark(s_draw, 96, 32, color_core=(255, 253, 248, 255), color_edge=(78, 216, 106, 230))
    skill_canvas.alpha_composite(skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (水壓逆衝·受擊後仰震退 / Hydraulic Shock Recoil)
    # Violent backward displacement: Torso knocked back-left (deg=-10, target=(52.0, 89.0)).
    # Head snapped hard back-left (deg=-20, target=(48.0, 33.0)).
    # Wings folded defensively (deg=-24, target=(42.0, 68.0), scale=0.92).
    # Key disengages violently (-48 deg, target=(26.0, 26.0), scale=0.92).
    # Bow held defensively across torso: deg=+32, target=(46.0, 72.0), scale=0.98.
    # FX: Clean deflection cross-star spark on armor plate.
    # =========================================================================
    p_key = place_rotated_pivot(key_src, deg=-48, pivot=KEY_PIVOT, target=(26.0, 26.0), scale=0.92)
    p_curio = place_rotated_pivot(curio_src, deg=-24, pivot=CURIO_PIVOT, target=(42.0, 68.0), scale=0.92)
    p_torso = place_rotated_pivot(torso_group, deg=-10, pivot=TORSO_PIVOT, target=(52.0, 89.0), scale=1.0)
    p_head = place_rotated_pivot(head_group, deg=-20, pivot=HEAD_PIVOT, target=(48.0, 33.0), scale=1.0)
    p_weapon = place_rotated_pivot(weapon_src, deg=32, pivot=WEAPON_PIVOT, target=(46.0, 72.0), scale=0.98)

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas.alpha_composite(p_key)
    hit_canvas.alpha_composite(p_curio)
    hit_canvas.alpha_composite(p_torso)
    hit_canvas.alpha_composite(p_head)
    hit_canvas.alpha_composite(p_weapon)

    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 46, 72
    h_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 6, cy - 6), (cx + 6, cy + 6)], fill=(78, 216, 106, 220), width=1)
    h_draw.line([(cx - 6, cy + 6), (cx + 6, cy - 6)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
    draw_clean_spark(h_draw, 26, 26, color_core=(255, 250, 185, 240), color_edge=(255, 94, 138, 220))
    hit_canvas.alpha_composite(hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def main():
    print("Generating The Tidal Manta combat action poses...")
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

    # Official Battle Sprite (battle == attack per review.md 4b-8-1)
    battle_128 = poses["attack"]
    battle_512 = battle_128.resize((512, 512), resample=Image.Resampling.LANCZOS)
    p_battle_128 = f"{PLAYER_DIR}/manta_battle.png"
    p_battle_512 = f"{PLAYER_DIR}/manta_battle_512.png"
    battle_128.save(p_battle_128)
    battle_512.save(p_battle_512)
    print(f"  ✓ Saved battle sprites: {p_battle_128} & {p_battle_512}")

    # Proof comparison: idle vs battle (256x128 & 1024x512)
    comp_proof = Image.new("RGBA", (256, 128), (24, 20, 36, 255))
    comp_proof.paste(poses["idle"], (0, 0), poses["idle"])
    comp_proof.paste(battle_128, (128, 0), battle_128)
    p_comp = f"{PLAYER_DIR}/proof_manta_idle_vs_battle.png"
    comp_proof.save(p_comp)

    comp_proof_512 = Image.new("RGBA", (1024, 512), (24, 20, 36, 255))
    idle_512 = poses["idle"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    comp_proof_512.paste(idle_512, (0, 0), idle_512)
    comp_proof_512.paste(battle_512, (512, 0), battle_512)
    p_comp_512 = f"{PLAYER_DIR}/proof_manta_idle_vs_battle_512.png"
    comp_proof_512.save(p_comp_512)
    print(f"  ✓ Saved idle vs battle proof cards: {p_comp} & {p_comp_512}")

    # Composite proof sheet (idle, telegraph, attack, skill, hit, recover)
    proof_strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_order = ['idle', 'telegraph', 'attack', 'skill', 'hit', 'recover']
    for idx, p_name in enumerate(proof_order):
        proof_strip.paste(poses[p_name], (idx * 128, 0), poses[p_name])

    proof_768_path = f"{PLAYER_DIR}/proof_manta_combat_poses_768.png"
    proof_strip.save(proof_768_path)
    print(f"  ✓ Saved 768x128 proof strip: {proof_768_path}")

    # Magenta background proof sheet for hole detection
    proof_magenta = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    proof_magenta.paste(proof_strip, (0, 0), proof_strip)
    proof_mag_path = f"{PLAYER_DIR}/proof_manta_combat_poses_magenta.png"
    proof_magenta.save(proof_mag_path)
    print(f"  ✓ Saved magenta proof strip: {proof_mag_path}")

    # Crop 8x hit core for 0-QA31
    hit_512 = poses["hit"].resize((512, 512), resample=Image.Resampling.LANCZOS)
    core_crop = hit_512.crop((50 * 4, 55 * 4, 75 * 4, 80 * 4))
    crop_path = f"{PLAYER_DIR}/proof_manta_hit_core_crop_8x.png"
    core_crop.save(crop_path)
    print(f"  ✓ Saved 0-QA31 core crop: {crop_path}")


if __name__ == "__main__":
    main()
