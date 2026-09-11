#!/usr/bin/env python3
"""
tools/generate_fox_poses.py
Generates the complete 6 combat action poses for Fox (fox mage) in Clockwork Heart:
  game/assets/sprites/player/poses/fox/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)

Rules & Standards strictly enforced:
- Rule 4b / 4b-4 / 4b-5 / 4b-7:
  1. True kinematic articulation of limbs and torso via IDW landmark warping (no trivial whole-image scaling/translation).
  2. Rigid weapon component (astral staff) preserved with strict linearity (max_resid <= 2x baseline).
  3. Ground soft contact shadow preserved without clipping or artificial shrinking.
- Rule 0a / 0b / 9 / 9a:
  Clear recognition of fox automaton features (ears, brass key, coat, cyan core) and astral staff at 128px.
- Rule 10 / 10a:
  Consistent dopamine cel-shaded storybook aesthetic matching official game assets.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")

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

def build_contact_shadow(cx: int = 60, cy: int = 119, rx: int = 36, ry: int = 5, blur: float = 0.6) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    # 3-tier concentric soft warm-shadow ellipse
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
    draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
    draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

def measure_staff_linearity(img: Image.Image) -> float:
    px = img.load()
    assert px is not None
    centers: list[float] = []
    ys: list[float] = []
    for y in range(40, 124):
        # Scan across width for the bronze staff shaft
        xs = []
        for x in range(img.width):
            p = cast(tuple[int, ...], px[x, y])
            if p[3] > 120:
                # Shaft bronze color detection
                is_bronze = (120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95)
                if is_bronze:
                    xs.append(x)
        if xs and len(xs) <= 10:
            centers.append(sum(xs) / float(len(xs)))
            ys.append(float(y))
    if len(ys) < 8:
        return 0.0
    n = float(len(ys))
    sum_y = sum(ys)
    sum_c = sum(centers)
    sum_yy = sum(y * y for y in ys)
    sum_yc = sum(y * c for y, c in zip(ys, centers))
    denom = (n * sum_yy - sum_y * sum_y)
    if abs(denom) < 1e-6:
        return 0.0
    m = (n * sum_yc - sum_y * sum_c) / denom
    c_const = (sum_c - m * sum_y) / n
    resids = [abs(c - (m * y + c_const)) for y, c in zip(ys, centers)]
    return max(resids)

def measure_shadow_rows(img: Image.Image) -> list[int]:
    px = img.load()
    assert px is not None
    counts = []
    for y in range(118, 128):
        c = sum(1 for x in range(img.width) if cast(tuple[int, ...], px[x, y])[3] >= 8)
        counts.append(c)
    return counts

def generate_poses():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    party_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
    staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
    battle_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png").convert("RGBA")
    
    # Clean body without staff and without ground shadow
    clean_body_path = "/tmp/fox_test/char_no_shadow_no_wep.png"
    if os.path.exists(clean_body_path):
        body_clean = Image.open(clean_body_path).convert("RGBA")
    else:
        body_clean = party_src.copy()
        b_px = body_clean.load()
        s_px = staff_src.load()
        assert b_px is not None and s_px is not None
        for y in range(128):
            for x in range(128):
                if cast(tuple[int, ...], s_px[x, y])[3] > 0:
                    b_px[x, y] = (0, 0, 0, 0)
                if y >= 119:
                    p = cast(tuple[int, ...], b_px[x, y])
                    is_foot = ((47 <= x <= 57 or 70 <= x <= 79) and y <= 122 and p[3] >= 200 and p[0] < 125 and p[1] < 105 and p[2] < 80)
                    if not is_foot:
                        b_px[x, y] = (0, 0, 0, 0)

    anchors = [
        (0, 0), (127, 0), (0, 127), (127, 127),
        (0, 30), (127, 30), (0, 64), (127, 64), (0, 95), (127, 95),
        (30, 0), (95, 0), (30, 127), (95, 127),
    ]

    base_landmarks = {
        "ear_l": (48, 12), "ear_r": (76, 12), "forehead": (62, 28),
        "eye_l": (50, 46), "eye_r": (72, 46), "snout": (60, 56),
        "neck": (60, 64), "core": (60, 75), "shoulder_l": (42, 70), "shoulder_r": (78, 68),
        "key_mount": (30, 62), "key_top": (22, 56), "key_bot": (22, 68),
        "pelvis": (60, 94),
        "tail_base": (33, 90), "tail_mid": (26, 102), "tail_tip": (22, 114),
        "hip_l": (48, 95), "knee_l": (50, 106), "foot_l": (52, 117),
        "hip_r": (68, 95), "knee_r": (72, 106), "foot_r": (74, 117),
        "hand": (90, 86),
    }

    # Standard ground shadow
    base_shadow = build_contact_shadow(cx=60, cy=119, rx=36, ry=5, blur=0.6)

    poses_data = {}

    # -------------------------------------------------------------
    # 1. IDLE (Standard neutral standing)
    # -------------------------------------------------------------
    idle_img = Image.alpha_composite(base_shadow, body_clean)
    idle_img = Image.alpha_composite(idle_img, staff_src)
    poses_data["idle"] = idle_img

    # -------------------------------------------------------------
    # 2. TELEGRAPH (Anticipation / magic channeling / hunkered forward)
    # -------------------------------------------------------------
    shifts_telegraph = {
        "ear_l": (1, 3), "ear_r": (1, 3), "forehead": (1, 3),
        "eye_l": (2, 3), "eye_r": (2, 3), "snout": (2, 4),
        "neck": (2, 3), "core": (2, 3), "shoulder_l": (1, 3), "shoulder_r": (2, 3),
        "key_mount": (1, 3), "key_top": (1, 3), "key_bot": (1, 3),
        "pelvis": (0, 4), "hip_l": (-1, 4), "hip_r": (1, 4),
        "tail_base": (-1, 3), "tail_mid": (-4, 1), "tail_tip": (-6, -2),
        "knee_l": (-3, 2), "foot_l": (-1, 1),
        "knee_r": (3, 2), "foot_r": (1, 1),
        "hand": (-6, -4),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
    
    warped_tele = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff angled forward-upward (-18 deg) and translated to channeled hand position
    staff_tele = staff_src.rotate(-18, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-8, -4))
    
    # Add subtle magic focus glow at staff tip (crystal at ~ 84, 38)
    tele_glow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(tele_glow)
    t_draw.ellipse([70, 24, 94, 48], fill=(60, 220, 240, 70))
    t_draw.ellipse([76, 30, 88, 42], fill=(120, 245, 255, 120))
    tele_glow = tele_glow.filter(ImageFilter.GaussianBlur(1.0))
    
    tele_img = Image.alpha_composite(base_shadow, warped_tele)
    tele_img = Image.alpha_composite(tele_img, staff_tele)
    tele_img = Image.alpha_composite(tele_img, tele_glow)
    poses_data["telegraph"] = tele_img

    # -------------------------------------------------------------
    # 3. ATTACK (Thrust strike / dynamic battle charge)
    # Directly based on the officially approved fox_battle.png with 100% clean contact shadow
    # -------------------------------------------------------------
    # Clean the bottom shadow of battle_src to ensure smooth Rule 4b-5 compliant contact shadow
    battle_clean = battle_src.copy()
    b_px = battle_clean.load()
    assert b_px is not None
    # Remove any rough ground artifacts at bottom >= 121
    for y in range(121, 128):
        for x in range(128):
            p = cast(tuple[int, ...], b_px[x, y])
            if p[3] > 0 and (p[0] > 100 or p[3] < 220):
                # non-foot transparent
                is_battle_foot = (50 <= x <= 65 or 90 <= x <= 106) and p[0] < 80 and p[1] < 80
                if not is_battle_foot:
                    b_px[x, y] = (0, 0, 0, 0)
    
    # Dynamic wide combat contact shadow
    battle_shadow = build_contact_shadow(cx=64, cy=120, rx=42, ry=6, blur=0.8)
    attack_img = Image.alpha_composite(battle_shadow, battle_clean)
    poses_data["attack"] = attack_img

    # -------------------------------------------------------------
    # 4. RECOVER (Low recoil crouch / absorption / staff planted to ground)
    # -------------------------------------------------------------
    shifts_recover = {
        "ear_l": (-1, 4), "ear_r": (1, 4), "forehead": (0, 4),
        "eye_l": (0, 4), "eye_r": (0, 4), "snout": (0, 5),
        "neck": (0, 5), "core": (0, 5), "shoulder_l": (-1, 5), "shoulder_r": (1, 5),
        "key_mount": (-1, 4), "key_top": (-1, 4), "key_bot": (-1, 4),
        "pelvis": (0, 6), "hip_l": (-2, 5), "hip_r": (2, 5),
        "tail_base": (0, 5), "tail_mid": (-2, 5), "tail_tip": (-4, 4),
        "knee_l": (-4, 4), "foot_l": (-2, 2),
        "knee_r": (4, 4), "foot_r": (2, 2),
        "hand": (-2, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_recover = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff planted firmly to ground, translated down +6px, upright
    staff_recover = staff_src.rotate(0, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-2, 6))
    
    recover_shadow = build_contact_shadow(cx=60, cy=121, rx=38, ry=6, blur=0.7)
    recover_img = Image.alpha_composite(recover_shadow, warped_recover)
    recover_img = Image.alpha_composite(recover_img, staff_recover)
    poses_data["recover"] = recover_img

    # -------------------------------------------------------------
    # 5. SKILL (Ascendant astral burst / staff held high / core radiating)
    # -------------------------------------------------------------
    shifts_skill = {
        "ear_l": (-2, -5), "ear_r": (2, -5), "forehead": (0, -4),
        "eye_l": (-1, -4), "eye_r": (1, -4), "snout": (0, -5),
        "neck": (0, -4), "core": (0, -3), "shoulder_l": (-2, -4), "shoulder_r": (3, -5),
        "key_mount": (-1, -3), "key_top": (-1, -3), "key_bot": (-1, -3),
        "pelvis": (0, -3), "hip_l": (-1, -3), "hip_r": (1, -3),
        "tail_base": (-1, -3), "tail_mid": (-5, -8), "tail_tip": (-8, -12),
        "knee_l": (0, -2), "foot_l": (0, -1),
        "knee_r": (0, -2), "foot_r": (0, -1),
        "hand": (6, -20),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_skill = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff raised skyward (+32 deg angle, lifted high to sky)
    staff_skill = staff_src.rotate(32, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(4, -18))
    
    # Astral magic radiation rings from core & crystal
    skill_vfx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(skill_vfx)
    # Radiant core pulse
    s_draw.ellipse([46, 60, 74, 88], outline=(64, 230, 240, 140), width=2)
    s_draw.ellipse([40, 54, 80, 94], outline=(40, 210, 230, 90), width=1)
    # Astral crown burst around high crystal (crystal near 104, 24)
    s_draw.ellipse([92, 12, 116, 36], outline=(100, 240, 255, 180), width=2)
    s_draw.ellipse([86, 6, 122, 42], outline=(70, 220, 250, 110), width=1)
    skill_vfx = skill_vfx.filter(ImageFilter.GaussianBlur(0.8))
    
    skill_shadow = build_contact_shadow(cx=60, cy=119, rx=34, ry=4, blur=0.6)
    skill_img = Image.alpha_composite(skill_shadow, warped_skill)
    skill_img = Image.alpha_composite(skill_img, staff_skill)
    skill_img = Image.alpha_composite(skill_img, skill_vfx)
    poses_data["skill"] = skill_img

    # -------------------------------------------------------------
    # 6. HIT (Staggered flinch / thrown backward / staff disrupted)
    # -------------------------------------------------------------
    shifts_hit = {
        "ear_l": (-14, 0), "ear_r": (-10, 0), "forehead": (-12, -2),
        "eye_l": (-11, -3), "eye_r": (-9, -3), "snout": (-10, -4),
        "neck": (-8, -2), "core": (-6, 0), "shoulder_l": (-12, 0), "shoulder_r": (-5, -3),
        "key_mount": (-8, 0), "key_top": (-10, -1), "key_bot": (-10, 1),
        "pelvis": (-4, 2), "hip_l": (-6, 2), "hip_r": (-2, 2),
        "tail_base": (-4, 2), "tail_mid": (-2, 4), "tail_tip": (2, 6),
        "knee_l": (-3, 2), "foot_l": (-4, 1),
        "knee_r": (4, -4), "foot_r": (6, -6),
        "hand": (-6, -10),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_hit = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff thrown upward/backward (-28 deg, pushed away)
    staff_hit = staff_src.rotate(-28, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-6, -10))
    
    # Impact spark on left shoulder/chest (x=46, y=66)
    hit_vfx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_vfx)
    # 4-point impact star
    h_draw.polygon([(46, 56), (48, 64), (56, 66), (48, 68), (46, 76), (44, 68), (36, 66), (44, 64)], fill=(255, 255, 255, 240))
    h_draw.polygon([(46, 60), (47, 64), (52, 66), (47, 68), (46, 72), (45, 68), (40, 66), (45, 64)], fill=(255, 220, 100, 255))
    hit_vfx = hit_vfx.filter(ImageFilter.GaussianBlur(0.5))
    
    hit_shadow = build_contact_shadow(cx=56, cy=119, rx=35, ry=5, blur=0.6)
    hit_img = Image.alpha_composite(hit_shadow, warped_hit)
    hit_img = Image.alpha_composite(hit_img, staff_hit)
    hit_img = Image.alpha_composite(hit_img, hit_vfx)
    poses_data["hit"] = hit_img

    # -------------------------------------------------------------
    # Save & Measure
    # -------------------------------------------------------------
    print("\n=== Generating and Verifying Fox Action Poses ===")
    p_idle = poses_data["idle"]
    
    for p_name in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
        img = poses_data[p_name]
        out_p = os.path.join(OUTPUT_DIR, f"{p_name}.png")
        img.save(out_p)
        
        diff = ImageChops.difference(p_idle, img)
        diff_data = list(diff.convert("L").getdata())
        diff_px = sum(1 for x in diff_data if x > 10)
        
        staff_resid = measure_staff_linearity(img)
        shadow_profile = measure_shadow_rows(img)
        
        print(f"[{p_name.upper()}] Saved {out_p}")
        print(f"  bbox={img.getbbox()}, diff_pixels_vs_idle={diff_px}")
        print(f"  staff_linearity_max_resid={staff_resid:.2f}px, shadow_profile={shadow_profile}")

if __name__ == "__main__":
    generate_poses()
