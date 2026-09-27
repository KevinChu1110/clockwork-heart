#!/usr/bin/env python3
"""
tools/build_owl_combat_poses.py
Generates the complete, definitive 6 combat action poses for Chrono Owl (靈鐘鴞, 16th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/owl/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/owl/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/owl"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/owl"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_owl_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_owl_sun_moon_astrolabe_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_owl_floating_micro_orrery.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_owl_brass_lamellae_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_owl_brass_plume_antennas.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_owl_dawn_astronomer_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_owl_clockface_lens_dusk_gold.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_owl_armillary_escapement_scepter.png").convert("RGBA")

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
scepter_raw = weapon_src.crop(wpn_bbox)

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
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 and strict safety margins."""
    out = img.copy()
    o_px = out.load()
    assert o_px is not None and s_px is not None

    # Strictly set shadow zone (118..127) to baseline shadow pixels
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
                o_px[x, y] = sp

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    # Zero out outer boundary columns and rows: x in [0, 1, 2, 3, 124, 125, 126, 127], y in [0, 1, 2, 3, 126, 127]
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

def place_scepter(scepter_img: Image.Image, deg: float, target_center: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the armillary scepter with zero clipping."""
    b = scepter_img.copy()
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
    "head_top": (64, 18),
    "plume_l": (48, 16),
    "plume_r": (80, 16),
    "eye_l": (54, 38),
    "eye_r": (74, 38),
    "beak": (64, 46),
    "throat": (64, 52),
    "core": (64, 60),
    "wing_l": (42, 68),
    "wing_r": (86, 68),
    "hand_l": (32, 64),
    "hand_r": (94, 64),
    "torso": (64, 76),
    "pelvis": (64, 88),
    "hip_l": (52, 94),
    "hip_r": (76, 94),
    "foot_l": (50, 114),
    "foot_r": (78, 114),
    "key_mount": (76, 42),
    "key_wing": (86, 36),
    "curio_top": (107, 48),
    "curio_mid": (107, 61),
    "curio_bot": (107, 74),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (Baseline balanced astromancer pose)
    # Scepter placed cleanly with safe margins (x: 5..50)
    # =========================================================================
    idle_canvas = body_no_weapon.copy()
    scepter_idle = place_scepter(scepter_raw, deg=0, target_center=(28, 61), scale=1.0, mirror=False)
    idle_canvas = Image.alpha_composite(idle_canvas, scepter_idle)
    poses["idle"] = enforce_ground_shadow(idle_canvas)

    # =========================================================================
    # 2. TELEGRAPH (天文刻度校準蓄勢 / Ephemeris Calibration Charge)
    # Coiled anticipation: body tilts back, head plume antennas alert, scepter raised skyward
    # =========================================================================
    shifts_telegraph = {
        "head_top": (3, -4), "plume_l": (1, -6), "plume_r": (5, -3),
        "eye_l": (3, -3), "eye_r": (3, -3), "beak": (3, -2), "throat": (2, -1),
        "core": (2, 0),
        "wing_l": (-2, -6), "wing_r": (4, 2),
        "hand_l": (-2, -10), "hand_r": (6, 4),
        "torso": (2, 2), "pelvis": (1, 3),
        "hip_l": (0, 3), "hip_r": (3, 2),
        "foot_l": (0, 0), "foot_r": (1, 0),
        "key_mount": (4, -1), "key_wing": (5, -3),
        "curio_top": (2, -4), "curio_mid": (2, -4), "curio_bot": (2, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Scepter raised and tilted skyward (kept well within x >= 6)
    scepter_tele = place_scepter(scepter_raw, deg=-25, target_center=(27, 48), scale=1.0, mirror=False)

    # Charging celestial rings & astrolabe star sparks (strictly around scepter head)
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Concentric charging cosmic rings around scepter head (safe radius: 10..42, 20..52)
    t_draw.arc([14, 22, 40, 48], start=30, end=330, fill=(255, 208, 40, 220), width=2)
    t_draw.arc([10, 18, 44, 52], start=60, end=300, fill=(56, 160, 255, 180), width=1)
    # Starlight suction motes and constellation points
    for pt in [(26, 20), (16, 32), (36, 30), (22, 44), (32, 42)]:
        t_draw.point(pt, fill=(255, 255, 255, 255))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.5))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, scepter_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (星屑擒縱引爆 / Escapement Stardust Burst)
    # Dynamic forward lunge to the left, scepter thrust forward with safe margin
    # =========================================================================
    shifts_attack = {
        "head_top": (-7, 3), "plume_l": (-8, 2), "plume_r": (-5, 4),
        "eye_l": (-7, 3), "eye_r": (-7, 3), "beak": (-8, 4), "throat": (-7, 4),
        "core": (-6, 4),
        "wing_l": (-8, 6), "wing_r": (2, -2),
        "hand_l": (-10, 8), "hand_r": (4, -4),
        "torso": (-5, 4), "pelvis": (-4, 3),
        "hip_l": (-5, 3), "hip_r": (-2, 2),
        "foot_l": (-2, 0), "foot_r": (0, 0),
        "key_mount": (-4, 2), "key_wing": (-3, 1),
        "curio_top": (-2, 6), "curio_mid": (-2, 6), "curio_bot": (-2, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_atk = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Scepter thrust forward into impact zone: target_center=(26, 60), deg=-18, scale=0.96 -> bbox[0] >= 6, zero clipping!
    scepter_atk = place_scepter(scepter_raw, deg=-18, target_center=(26, 60), scale=0.96, mirror=False)

    # Burst FX - located at scepter tip (x: 10..26, y: 24..40)
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Stardust explosion ring centered at (18, 32), safely within margins >= 8
    a_draw.ellipse([10, 24, 26, 40], outline=(255, 208, 40, 230), width=2)
    a_draw.line([(10, 32), (26, 32)], fill=(78, 216, 106, 200), width=1)
    a_draw.line([(18, 24), (18, 40)], fill=(78, 216, 106, 200), width=1)
    # Escapement spark points
    for pt in [(12, 26), (24, 26), (12, 38), (24, 38)]:
        a_draw.point(pt, fill=(255, 255, 255, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.4))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, scepter_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (周天星曆超頻天墜 / Astral Orrery Supernova)
    # Ascending float, wings spreading, scepter held high overhead, celestial rings
    # =========================================================================
    shifts_skill = {
        "head_top": (0, -7), "plume_l": (-4, -9), "plume_r": (4, -8),
        "eye_l": (0, -6), "eye_r": (0, -6), "beak": (0, -5), "throat": (0, -5),
        "core": (0, -5),
        "wing_l": (-6, -5), "wing_r": (6, -4),
        "hand_l": (-5, -9), "hand_r": (7, -6),
        "torso": (0, -4), "pelvis": (0, -3),
        "hip_l": (-3, -2), "hip_r": (3, -2),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "key_mount": (1, -5), "key_wing": (2, -7),
        "curio_top": (4, -8), "curio_mid": (4, -8), "curio_bot": (4, -8),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Scepter held high and vertical
    scepter_skill = place_scepter(scepter_raw, deg=-10, target_center=(27, 46), scale=1.04, mirror=False)

    # Astral Orrery Supernova FX (clean celestial arcs and sparkles, no grid/vertical lines)
    sk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sk_fx)
    # Dual concentric celestial halos around torso/scepter
    s_draw.arc([24, 16, 96, 88], start=0, end=360, fill=(56, 160, 255, 140), width=1)
    s_draw.arc([30, 22, 90, 82], start=0, end=360, fill=(255, 208, 40, 170), width=2)
    # Constellation sparkles around the celestial rings
    for pt in [(30, 28), (90, 28), (24, 52), (96, 52), (60, 16), (68, 88)]:
        s_draw.point(pt, fill=(255, 255, 255, 255))
    sk_fx = sk_fx.filter(ImageFilter.GaussianBlur(0.5))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, scepter_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, sk_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (羽翼格擋棘輪卸力 / Wing Ratchet Shock Absorption)
    # Recoil knockback to the right (+5), ruffled posture, scepter angled defensively
    # =========================================================================
    shifts_hit = {
        "head_top": (6, -2), "plume_l": (5, -4), "plume_r": (7, -1),
        "eye_l": (6, -1), "eye_r": (6, -1), "beak": (7, 0), "throat": (6, 0),
        "core": (5, 0),
        "wing_l": (3, 4), "wing_r": (7, 2),
        "hand_l": (2, 6), "hand_r": (8, 4),
        "torso": (4, 1), "pelvis": (3, 1),
        "hip_l": (2, 1), "hip_r": (5, 1),
        "foot_l": (1, 0), "foot_r": (2, 0),
        "key_mount": (6, 0), "key_wing": (6, -2),
        "curio_top": (6, 2), "curio_mid": (6, 2), "curio_bot": (6, 2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Scepter angled defensively back
    scepter_hit = place_scepter(scepter_raw, deg=20, target_center=(33, 66), scale=0.98, mirror=False)

    # Subtle impact sparks at scepter contact point
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    # Small circular glow and clean spark points
    h_draw.ellipse([20, 48, 30, 58], fill=(255, 208, 40, 160))
    for pt in [(22, 50), (28, 46), (26, 56), (18, 54), (32, 52)]:
        h_draw.point(pt, fill=(255, 255, 255, 255))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.4))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, scepter_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (展羽歸位重整 / Stance Settlement & Calming Reset)
    # Sinking back down into solid restabilization (+1, +4), face completely clean
    # =========================================================================
    shifts_recover = {
        "head_top": (1, 4), "plume_l": (0, 4), "plume_r": (2, 4),
        "eye_l": (1, 4), "eye_r": (1, 4), "beak": (1, 4), "throat": (1, 4),
        "core": (1, 4),
        "wing_l": (-2, 4), "wing_r": (3, 4),
        "hand_l": (-3, 5), "hand_r": (4, 5),
        "torso": (1, 4), "pelvis": (1, 4),
        "hip_l": (-1, 3), "hip_r": (2, 3),
        "foot_l": (-1, 0), "foot_r": (1, 0),
        "key_mount": (2, 3), "key_wing": (2, 2),
        "curio_top": (2, 2), "curio_mid": (2, 3), "curio_bot": (2, 3),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_rec = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Scepter relaxed in low ready position
    scepter_rec = place_scepter(scepter_raw, deg=-4, target_center=(28, 64), scale=1.0, mirror=False)

    # Subtle cooling steam from back vent only (x: 90..102, y: 52..64), ZERO steam on face or ground
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.ellipse([92, 54, 100, 62], fill=(230, 240, 250, 140))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.6))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, scepter_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    print("=== BUILDING CHRONO OWL 6 COMBAT ACTION POSES ===")
    poses = generate_poses()

    for p_name, img in poses.items():
        dst_128 = os.path.join(OUT_DIR, f"{p_name}.png")
        img.save(dst_128, format="PNG")

        # 512 LANCZOS upscale
        dst_512 = os.path.join(OUT_DIR, f"{p_name}_512.png")
        img_512 = img.resize((512, 512), resample=Image.Resampling.LANCZOS)
        img_512.save(dst_512, format="PNG")

        bbox = img.getbbox()
        print(f"✓ Saved {p_name:10s} -> {dst_128} (128x128, bbox={bbox}) and {dst_512} (512x512 LANCZOS)")

    # Generate proof sheets
    # 1. 768-wide strip (all 6 poses in a row: 128 x 6 = 768)
    pose_order = ["idle", "telegraph", "attack", "skill", "hit", "recover"]
    strip = Image.new("RGBA", (128 * 6, 128), (0, 0, 0, 0))
    for i, p_name in enumerate(pose_order):
        strip.paste(poses[p_name], (i * 128, 0))

    proof_strip_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_owl_combat_poses_768.png"
    strip.save(proof_strip_path, format="PNG")
    print(f"✓ Saved proof strip: {proof_strip_path}")

    # 2. Magenta background proof sheet
    magenta_strip = Image.new("RGBA", (128 * 6, 128), (255, 0, 255, 255))
    for i, p_name in enumerate(pose_order):
        magenta_strip.alpha_composite(poses[p_name], (i * 128, 0))
    proof_magenta_path = f"{REPO_ROOT}/game/assets/sprites/player/proof_owl_combat_poses_magenta.png"
    magenta_strip.save(proof_magenta_path, format="PNG")
    print(f"✓ Saved magenta proof strip: {proof_magenta_path}")
