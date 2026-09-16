#!/usr/bin/env python3
"""
build_bear_combat_poses.py
Generates the complete 6 combat action poses for The Iron Bear (玄軸熊, Viking Warrior)
in Clockwork Heart:
  game/assets/sprites/player/poses/bear/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/battle/bear/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/bear"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/bear"
BATTLE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/battle/bear"
os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(BATTLE_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_bear_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers
chassis_src = Image.open(f"{BASE_DIR}/chassis/paint_bear_amber.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_iron_bear_stock.png").convert("RGBA")
key_src = Image.open(f"{BASE_DIR}/winding_key/key_cross_pendulum.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_ironclad_overalls.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/core_emerald_lens.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/wpn_eccentric_gyro_sledge.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_music_honey_cask.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(costume_src)
body_no_weapon.alpha_composite(optic_src)

# Extract cropped hammer weapon
hammer_bbox = weapon_src.getbbox()
assert hammer_bbox is not None
hammer_raw = weapon_src.crop(hammer_bbox)

def clean_margins(img: Image.Image) -> Image.Image:
    """Clean margins strictly (L>=4, R>=4, T>=4, B>=2)."""
    out = img.copy()
    o_px = out.load()
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

def place_hammer(hammer_img: Image.Image, deg: float, target_grip: tuple[int, int], scale: float = 1.0, mirror: bool = False) -> Image.Image:
    """Rotates and places the hammer with zero hard clipping."""
    d = hammer_img.copy()
    if mirror:
        d = ImageOps.mirror(d)
    dw, dh = d.size
    # Grip in crop is (14, 36)
    gx, gy = (14, 36) if not mirror else (dw - 14, 36)
    
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    large.paste(d, (128 - gx, 128 - gy))
    
    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        large = large.resize((nw, nh), Image.Resampling.LANCZOS)
        
    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tx, ty = target_grip
    out.paste(rotated, (tx - 128, ty - 128), rotated)
    return out

# Build initial idle and extract baseline ground shadow
idle_initial = body_no_weapon.copy()
h_idle = place_hammer(hammer_raw, deg=0, target_grip=(88, 80), scale=1.0, mirror=False)
idle_initial = Image.alpha_composite(idle_initial, h_idle)
idle_initial = clean_margins(idle_initial)

shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
i_px = idle_initial.load()
for y in range(118, 128):
    for x in range(128):
        s_px[x, y] = i_px[x, y]

EXPECTED_SHADOW = [sum(1 for x in range(128) if s_px[x, y][3] > 20) for y in range(118, 128)]
print(f"Benchmark Bear ground shadow row counts (118..127): {EXPECTED_SHADOW}")

def enforce_ground_shadow(img: Image.Image) -> Image.Image:
    """Enforce exact ground contact shadow matching baseline Rule 4b-5 without flinching."""
    out = img.copy()
    o_px = out.load()
    for y in range(118, 128):
        for x in range(128):
            sp = s_px[x, y]
            fp = o_px[x, y]
            if sp[3] <= 20 and fp[3] > 20:
                o_px[x, y] = (0, 0, 0, 0)
            elif sp[3] > 20 and fp[3] <= 20:
                o_px[x, y] = sp
    return clean_margins(out)

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
    "ear_l": (34, 26),
    "ear_r": (94, 26),
    "forehead": (64, 22),
    "eye_l": (54, 40),
    "eye_r": (74, 40),
    "muzzle": (64, 48),
    "heart_gem": (64, 66),
    "shoulder_l": (36, 62),
    "shoulder_r": (92, 62),
    "arm_l": (34, 78),
    "arm_r": (88, 80),
    "torso": (64, 78),
    "pelvis": (64, 88),
    "hip_l": (48, 92),
    "hip_r": (76, 92),
    "knee_l": (48, 104),
    "knee_r": (74, 104),
    "foot_l": (50, 117),
    "foot_r": (76, 117),
    "key_mount": (26, 44),
    "key_wing": (14, 38),
    "curio": (104, 24),
}

def generate_poses():
    poses: dict[str, Image.Image] = {}

    # =========================================================================
    # 1. IDLE (磐石鎮嶽架式 Bulwark Stance)
    # =========================================================================
    poses["idle"] = enforce_ground_shadow(idle_initial)

    # =========================================================================
    # 2. TELEGRAPH (偏心飛輪狂轉 Gyro Overdrive Draw)
    # Low horse stance, body coiled back, eccentric flywheel spinning wildly
    # =========================================================================
    shifts_telegraph = {
        "ear_l": (-2, 5), "ear_r": (0, 5), "forehead": (-1, 6),
        "eye_l": (-1, 6), "eye_r": (1, 6), "muzzle": (0, 6),
        "heart_gem": (-2, 5), "shoulder_l": (-3, 5), "shoulder_r": (1, 5),
        "arm_l": (-4, 4), "arm_r": (-8, 3),
        "torso": (-2, 5), "pelvis": (-2, 6),
        "hip_l": (-5, 6), "hip_r": (1, 6),
        "knee_l": (-7, 5), "knee_r": (3, 5),
        "foot_l": (-4, 1), "foot_r": (2, 1),
        "key_mount": (-4, 4), "key_wing": (-5, 3),
        "curio": (-1, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_tele = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Hammer drawn back diagonally behind / to the right with high angle
    h_tele = place_hammer(hammer_raw, deg=38, target_grip=(80, 83), scale=1.0, mirror=False)

    # Golden flywheel overdrive spinning halo + steam vents
    tele_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_fx)
    # Flywheel blur halo around hammer head
    t_draw.arc([88, 36, 122, 70], start=30, end=330, fill=(255, 208, 40, 210), width=3)
    t_draw.arc([92, 40, 118, 66], start=50, end=310, fill=(255, 245, 180, 240), width=2)
    # High-pressure steam release from right shoulder and wrist
    t_draw.ellipse([96, 56, 106, 66], fill=(230, 240, 250, 150))
    t_draw.ellipse([102, 50, 110, 58], fill=(245, 250, 255, 190))
    t_draw.ellipse([30, 54, 40, 64], fill=(230, 240, 250, 140))
    # Chest gem intense pulse
    t_draw.ellipse([58, 68, 66, 76], fill=(78, 216, 106, 180))
    t_draw.ellipse([60, 70, 64, 74], fill=(180, 255, 200, 230))
    tele_fx = tele_fx.filter(ImageFilter.GaussianBlur(0.6))

    tele_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    tele_canvas = Image.alpha_composite(tele_canvas, warped_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, h_tele)
    tele_canvas = Image.alpha_composite(tele_canvas, tele_fx)
    poses["telegraph"] = enforce_ground_shadow(tele_canvas)

    # =========================================================================
    # 3. ATTACK (撼地裂空離心橫掃 Centrifugal Quake Cleave)
    # Powerful forward lunge, hammer slammed down to ground on right
    # =========================================================================
    shifts_attack = {
        "ear_l": (10, 1), "ear_r": (12, 1), "forehead": (11, 1),
        "eye_l": (11, 1), "eye_r": (13, 1), "muzzle": (13, 2),
        "heart_gem": (10, 2), "shoulder_l": (8, 2), "shoulder_r": (12, 2),
        "arm_l": (10, 1), "arm_r": (14, 0),
        "torso": (9, 2), "pelvis": (7, 2),
        "hip_l": (-3, 2), "hip_r": (11, 2),
        "knee_l": (-8, 2), "knee_r": (12, 1),
        "foot_l": (-10, 0), "foot_r": (12, 0),
        "key_mount": (5, 2), "key_wing": (3, 2),
        "curio": (12, 1),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_attack = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Hammer slammed forward and downward into the ground (calibrated <= 123)
    h_atk = place_hammer(hammer_raw, deg=-48, target_grip=(96, 76), scale=1.0, mirror=False)

    # Ground impact shockwave + kinetic debris & sparks
    atk_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    a_draw = ImageDraw.Draw(atk_fx)
    # Expanding kinetic shockwave arcs on the ground (x=88..120, y=108..122)
    a_draw.arc([86, 102, 120, 122], start=10, end=190, fill=(217, 119, 36, 210), width=3)
    a_draw.arc([90, 105, 116, 121], start=20, end=180, fill=(255, 208, 40, 240), width=2)
    # Impact flash at hammer contact
    a_draw.ellipse([96, 92, 104, 100], fill=(255, 255, 220, 240))
    a_draw.line([(88, 96), (112, 96)], fill=(255, 240, 160, 220), width=1)
    a_draw.line([(100, 86), (100, 106)], fill=(255, 240, 160, 220), width=1)
    # Flying sparks
    a_draw.point([(106, 88), (110, 92), (92, 90), (114, 102), (90, 104)], fill=(255, 208, 40, 255))
    atk_fx = atk_fx.filter(ImageFilter.GaussianBlur(0.5))

    atk_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    atk_canvas = Image.alpha_composite(atk_canvas, warped_attack)
    atk_canvas = Image.alpha_composite(atk_canvas, h_atk)
    atk_canvas = Image.alpha_composite(atk_canvas, atk_fx)
    poses["attack"] = enforce_ground_shadow(atk_canvas)

    # =========================================================================
    # 4. SKILL (玄軸崩天千鈞撼 Iron Quake Titan Breaker)
    # Aerial upward launch with hammer raised high overhead
    # Top margin kept >= 8px so character height diff <= 5.0%
    # =========================================================================
    shifts_skill = {
        "ear_l": (0, -6), "ear_r": (2, -6), "forehead": (1, -6),
        "eye_l": (1, -6), "eye_r": (2, -6), "muzzle": (1, -5),
        "heart_gem": (1, -5), "shoulder_l": (-2, -6), "shoulder_r": (4, -6),
        "arm_l": (-2, -7), "arm_r": (5, -7),
        "torso": (1, -5), "pelvis": (1, -5),
        "hip_l": (-3, -5), "hip_r": (3, -5),
        "knee_l": (-5, -6), "knee_r": (4, -6),
        "foot_l": (-3, -7), "foot_r": (3, -7),
        "key_mount": (-1, -5), "key_wing": (-3, -5),
        "curio": (1, -5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_skill = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Hammer raised overhead (~ -75 deg), grip at (80, 58) -> hammer top at y=31
    h_skill = place_hammer(hammer_raw, deg=-75, target_grip=(80, 58), scale=0.95, mirror=False)

    # Supercharged aura halo & seismic tremor runes (top arc kept at y>=10)
    skill_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_fx)
    # Expanding energy aura over hammer head (y kept >= 10)
    s_draw.arc([60, 10, 110, 60], start=140, end=340, fill=(255, 208, 40, 200), width=3)
    s_draw.arc([64, 14, 106, 56], start=150, end=330, fill=(78, 216, 106, 220), width=2)
    # Steam exhaust jets from vertical ascent
    s_draw.ellipse([38, 92, 50, 104], fill=(230, 240, 250, 160))
    s_draw.ellipse([76, 92, 88, 104], fill=(230, 240, 250, 160))
    # Seismic ground ring under airborne character
    s_draw.ellipse([36, 114, 92, 122], fill=(217, 119, 36, 90))
    skill_fx = skill_fx.filter(ImageFilter.GaussianBlur(0.6))

    skill_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    skill_canvas = Image.alpha_composite(skill_canvas, warped_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, h_skill)
    skill_canvas = Image.alpha_composite(skill_canvas, skill_fx)
    poses["skill"] = enforce_ground_shadow(skill_canvas)

    # =========================================================================
    # 5. HIT (液壓卸力重甲防 Piston Dampener Absorb)
    # Heavy fortress recoil, hammer braced across chest, pistons venting steam
    # =========================================================================
    shifts_hit = {
        "ear_l": (-7, -2), "ear_r": (-5, -2), "forehead": (-6, -2),
        "eye_l": (-6, -2), "eye_r": (-4, -2), "muzzle": (-5, -1),
        "heart_gem": (-5, -1), "shoulder_l": (-6, -1), "shoulder_r": (-3, -1),
        "arm_l": (-3, 0), "arm_r": (-3, 0),
        "torso": (-4, -1), "pelvis": (-3, 0),
        "hip_l": (-5, 0), "hip_r": (-2, 0),
        "knee_l": (-6, 0), "knee_r": (-2, 0),
        "foot_l": (-4, 0), "foot_r": (-1, 0),
        "key_mount": (-6, -1), "key_wing": (-7, -1),
        "curio": (-6, -2),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Hammer braced defensively across chest like an armored barricade
    h_hit = place_hammer(hammer_raw, deg=-28, target_grip=(74, 76), scale=0.98, mirror=False)

    # Impact spark on armor + pressure valve steam venting
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    ht_draw = ImageDraw.Draw(hit_fx)
    # Spark burst on chest/hammer
    ht_draw.ellipse([64, 62, 72, 70], fill=(255, 245, 180, 240))
    ht_draw.line([(58, 66), (78, 66)], fill=(255, 255, 220, 220), width=1)
    ht_draw.line([(68, 56), (68, 76)], fill=(255, 255, 220, 220), width=1)
    # Steam clouds venting from shoulder relief valves
    ht_draw.ellipse([26, 52, 38, 64], fill=(230, 240, 250, 160))
    ht_draw.ellipse([20, 46, 30, 56], fill=(245, 250, 255, 190))
    ht_draw.ellipse([88, 52, 98, 62], fill=(230, 240, 250, 150))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.6))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, h_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)

    # =========================================================================
    # 6. RECOVER (重錘頓地氣壓回位 Ground Stomp Re-Align)
    # Hammer driven down to brake and steady wide stance
    # =========================================================================
    shifts_recover = {
        "ear_l": (3, 5), "ear_r": (5, 5), "forehead": (4, 5),
        "eye_l": (4, 5), "eye_r": (6, 5), "muzzle": (5, 5),
        "heart_gem": (3, 5), "shoulder_l": (1, 5), "shoulder_r": (5, 5),
        "arm_l": (-2, 4), "arm_r": (4, 5),
        "torso": (2, 5), "pelvis": (2, 6),
        "hip_l": (-4, 6), "hip_r": (4, 6),
        "knee_l": (-6, 5), "knee_r": (5, 5),
        "foot_l": (-5, 1), "foot_r": (4, 1),
        "key_mount": (1, 5), "key_wing": (-1, 4),
        "curio": (3, 5),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_recover = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)

    # Hammer grounded firmly in reverse braking angle
    h_rec = place_hammer(hammer_raw, deg=75, target_grip=(86, 90), scale=0.96, mirror=False)

    # Ground brake friction sparks and hydraulic reset steam
    rec_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rec_fx)
    r_draw.ellipse([88, 112, 96, 118], fill=(255, 208, 40, 200))
    r_draw.point([(98, 111), (93, 110), (101, 114)], fill=(255, 255, 180, 240))
    r_draw.ellipse([34, 76, 44, 86], fill=(230, 240, 250, 140))
    rec_fx = rec_fx.filter(ImageFilter.GaussianBlur(0.5))

    rec_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    rec_canvas = Image.alpha_composite(rec_canvas, warped_recover)
    rec_canvas = Image.alpha_composite(rec_canvas, h_rec)
    rec_canvas = Image.alpha_composite(rec_canvas, rec_fx)
    poses["recover"] = enforce_ground_shadow(rec_canvas)

    return poses

if __name__ == "__main__":
    poses = generate_poses()
    for name, im in poses.items():
        # Save to both poses/bear and battle/bear
        out_p1 = f"{OUT_DIR}/{name}.png"
        out_p2 = f"{BATTLE_DIR}/{name}.png"
        im.save(out_p1, "PNG")
        im.save(out_p2, "PNG")
        bbox = im.getbbox()
        h = bbox[3] - bbox[1] if bbox else 0
        w = bbox[2] - bbox[0] if bbox else 0
        px_115 = sum(1 for y in range(115) for x in range(128) if im.getpixel((x, y))[3] > 8)
        print(f"✓ {name:10s}: saved, bbox={bbox}, w={w}, h={h}, y<115={px_115}")
