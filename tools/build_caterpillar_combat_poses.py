#!/usr/bin/env python3
"""tools/build_caterpillar_combat_poses.py
Generates the complete, definitive 6 combat action poses for The Bellows Caterpillar (第五十族 風箱毛蟲, caterpillar)
in Clockwork Heart:
  game/assets/sprites/player/poses/caterpillar/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/caterpillar/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
Follows CANON.md, art_direction.md, and review.md quality gates:
  - 0-QA16 / 0-QA31 / 0-QA34
  - Rule 4b-4 / 4b-5 / 4b-7 / 4b-8 / 4b-9 / 4b-10
  - Rule 4c-5 / 16 (Safe margins L>=4, T>=4, R>=4, B>=2 and zero outer boundaries)
Features:
  - Segmented stamped brass rings & accordion bellows chassis
  - Dual-sensor bellows brow cowl with feeler antennas
  - Dual round amber condenser optic lens
  - Deepwood sapper cuirass with brass clasps
  - Segmented pressure-reservoir pack curio
  - Dual-ring bellows brass winding key
  - Vine Valley bellows compression hammer
"""

import os
import sys
from typing import cast
from PIL import Image, ImageOps
import numpy as np

# Ensure clean imports
sys.path = [p for p in sys.path if not p.startswith('/tmp')]

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/caterpillar"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/caterpillar"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
key_src = Image.open(f"{BASE_DIR}/winding_key/key_caterpillar_dual_ring_bellows_key.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_caterpillar_segmented_pressure_pack.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_caterpillar_brass_bellows_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_caterpillar_sensor_bellows_cowl.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_caterpillar_deepwood_sapper_cuirass.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_caterpillar_amber_condenser_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_caterpillar_vine_valley_compression_hammer.png").convert("RGBA")

# Extract ground shadow master from party caterpillar_idle.png
ref_shadow_im = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/caterpillar_idle.png").convert("RGBA")
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

    # Sanitize dark falloff (ultra-dark pixels)
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


def transform_body(img: Image.Image, sx: float, sy: float, deg: float, pivot: tuple[float, float], trans: tuple[float, float]) -> Image.Image:
    """Applies true Squash & Stretch (non-uniform scaling) and articulation rotation around a pivot with subpixel precision."""
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    px, py = pivot
    tx, ty = trans

    # Center source image so pivot is at (128, 128)
    paste_x = int(round(128.0 - px))
    paste_y = int(round(128.0 - py))
    large.paste(img, (paste_x, paste_y))

    # Scale non-uniformly (Squash & Stretch)
    nw = max(1, int(round(canvas_size * sx)))
    nh = max(1, int(round(canvas_size * sy)))
    scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)

    # Re-center scaled onto 256 canvas around the pivot point
    re_large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    p_sc_x = 128.0 * sx
    p_sc_y = 128.0 * sy
    re_paste_x = int(round(128.0 - p_sc_x))
    re_paste_y = int(round(128.0 - p_sc_y))
    re_large.paste(scaled, (re_paste_x, re_paste_y))

    # Rotate around pivot (128, 128)
    rotated = re_large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))

    # Output canvas (128, 128) with translation
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    out_x = int(round(px + tx - 128.0))
    out_y = int(round(py + ty - 128.0))
    out.paste(rotated, (out_x, out_y), rotated)
    return out


# Base body composite (curio + chassis + head + costume + optic)
body_core = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_core.alpha_composite(curio_src)
body_core.alpha_composite(chassis_src)
body_core.alpha_composite(head_src)
body_core.alpha_composite(costume_src)
body_core.alpha_composite(optic_src)

KEY_PIVOT = (64.0, 50.0)
WEAPON_PIVOT = (86.0, 78.0)
BODY_PIVOT = (64.0, 116.0)


def generate_poses() -> dict[str, Image.Image]:
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (深林風箱·工兵沉穩守架 / Bellows Caterpillar Sapper Guard)
    # Low-center-of-gravity stout stance. Compression hammer held in right hand (86, 78).
    # Dual-ring bellows key standing upright at (64, 50).
    # =========================================================================
    idle_body = transform_body(body_core, sx=1.0, sy=1.0, deg=0, pivot=BODY_PIVOT, trans=(0, 0))
    idle_key = place_rotated_pivot(key_src, deg=0, pivot=KEY_PIVOT, target=(64, 50), scale=1.0)
    idle_weapon = place_rotated_pivot(weapon_src, deg=0, pivot=WEAPON_PIVOT, target=(86, 78), scale=1.0)
    idle_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle_canvas = Image.alpha_composite(idle_canvas, idle_key)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_body)
    idle_canvas = Image.alpha_composite(idle_canvas, idle_weapon)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (手風琴蓄壓·深蹲後仰蓄能 / Deep Bellows Squash & Coil)
    # Pronounced Accordion Squash: body squashes down by 22% and expands horizontally!
    # Height drops dramatically (head drops to y=35), coils backward (-8 deg).
    # Hammer raised backward and upward across shoulder (-55 deg, target=(70, 68)).
    # Dual-ring key counter-winds with high torque (-55 deg, target=(52, 62)).
    # =========================================================================
    tele_body = transform_body(body_core, sx=1.12, sy=0.78, deg=-8, pivot=BODY_PIVOT, trans=(-8, 6))
    tele_key = place_rotated_pivot(key_src, deg=-55, pivot=KEY_PIVOT, target=(52, 62), scale=0.94)
    tele_weapon = place_rotated_pivot(weapon_src, deg=-55, pivot=WEAPON_PIVOT, target=(70, 68), scale=1.04)

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, tele_key)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_body)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_weapon)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (蔓谷重夯·風箱氣錘怒砸 / Full-Force Bellows Pile-Driver Ground Slam)
    # Dynamic forward Stretch & Lunge!
    # Body stretches forward horizontally (sx=1.14, sy=0.88), dives forward (+12 deg, trans=(12, 3)).
    # Compression hammer slammed with maximum force down onto the front ground (+48 deg, target=(102, 80)).
    # Key whips forward (+65 deg, target=(82, 48)).
    # =========================================================================
    atk_body = transform_body(body_core, sx=1.14, sy=0.88, deg=12, pivot=BODY_PIVOT, trans=(12, 3))
    atk_key = place_rotated_pivot(key_src, deg=65, pivot=KEY_PIVOT, target=(82, 48), scale=1.02)
    atk_weapon = place_rotated_pivot(weapon_src, deg=48, pivot=WEAPON_PIVOT, target=(102, 80), scale=1.18)

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, atk_key)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_body)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_weapon)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. RECOVER (洩壓散熱·沉重拔鎚復位 / Pneumatic Exhaust & Reset)
    # Heavy compression hammer embedded into the ground!
    # Caterpillar body slumps forward over the hammer handle (sx=1.06, sy=0.86, deg=+6, trans=(4, 5)).
    # Hammer resting deep in ground (+22 deg, target=(90, 82)).
    # Key settling back (+18 deg, target=(68, 54)).
    # =========================================================================
    rec_body = transform_body(body_core, sx=1.06, sy=0.86, deg=6, pivot=BODY_PIVOT, trans=(4, 5))
    rec_key = place_rotated_pivot(key_src, deg=18, pivot=KEY_PIVOT, target=(68, 54), scale=0.98)
    rec_weapon = place_rotated_pivot(weapon_src, deg=22, pivot=WEAPON_PIVOT, target=(90, 82), scale=1.05)

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, rec_key)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_body)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_weapon)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    # =========================================================================
    # 5. SKILL (奧義·蔓谷全開蓄壓裂地轟 / Cataclysmic Bellows Overdrive Leap & High Strike)
    # True Airborne Leap! The entire body vaults upward off the ground (trans y=-10, sy=1.10).
    # Rollers clearly suspended above the ground line!
    # Compression hammer raised tall on the right side in high aerial strike stance (-18 deg, target=(88, 66)),
    # completely clear of face, optic core, and antennas!
    # Key spinning in maximum overdrive (+94 deg, target=(68, 38)).
    # =========================================================================
    skill_body = transform_body(body_core, sx=0.94, sy=1.10, deg=5, pivot=BODY_PIVOT, trans=(2, -10))
    skill_key = place_rotated_pivot(key_src, deg=94, pivot=KEY_PIVOT, target=(68, 38), scale=1.06)
    skill_weapon = place_rotated_pivot(weapon_src, deg=-18, pivot=WEAPON_PIVOT, target=(88, 66), scale=1.10)

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, skill_key)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_body)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_weapon)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 6. HIT (鋼環受震·風箱層疊受擊後挫 / Bellows Kinetic Shock & Stagger)
    # Dramatic backward recoil & cower!
    # Body tilts back (-15 deg) and shifts left (trans=(-12, -2)).
    # Hammer held in defensive diagonal block across chest (-32 deg, target=(75, 72)),
    # maintaining full visibility of face and optic core.
    # Key jolted backward (-45 deg, target=(50, 44)).
    # =========================================================================
    hit_body = transform_body(body_core, sx=0.94, sy=0.94, deg=-15, pivot=BODY_PIVOT, trans=(-12, -2))
    hit_key = place_rotated_pivot(key_src, deg=-45, pivot=KEY_PIVOT, target=(50, 44), scale=0.95)
    hit_weapon = place_rotated_pivot(weapon_src, deg=-32, pivot=WEAPON_PIVOT, target=(75, 72), scale=1.04)

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, hit_key)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_body)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_weapon)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    return poses


def build_and_save():
    print("Generating caterpillar combat action poses...")
    poses = generate_poses()

    for name, img in poses.items():
        # Save 128x128
        out_128 = os.path.join(OUT_DIR, f"{name}.png")
        img.save(out_128, "PNG")

        # Save 512x512 LANCZOS
        out_512 = os.path.join(OUT_DIR, f"{name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(out_512, "PNG")

        print(f"✓ Saved {name}.png (128x128) and {name}_512.png (512x512 LANCZOS)")

    # Generate 6-pose comparison proof sheets (768x128)
    order = ["idle", "telegraph", "attack", "recover", "skill", "hit"]
    proof_768 = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    proof_mag = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))

    for i, p_name in enumerate(order):
        p_img = poses[p_name]
        proof_768.paste(p_img, (i * 128, 0), p_img)
        proof_mag.alpha_composite(p_img, (i * 128, 0))

    p768_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_caterpillar_combat_poses_768.png"
    pmag_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_caterpillar_combat_poses_magenta.png"
    proof_768.save(p768_path, "PNG")
    proof_mag.save(pmag_path, "PNG")
    print(f"✓ Saved proof sheets:\n  - {p768_path}\n  - {pmag_path}")


if __name__ == "__main__":
    build_and_save()
