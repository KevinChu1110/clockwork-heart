#!/usr/bin/env python3
"""
tools/generate_fox_poses_v3.py
High-impact kinematic combat action pose generator for Fox Mage in Clockwork Heart.
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")

def build_contact_shadow(cx: int = 60, cy: int = 119, rx: int = 36, ry: int = 5, blur: float = 0.6) -> Image.Image:
    shadow_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow_canvas)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(160, 137, 108, 180))
    draw.ellipse([cx - int(rx * 0.78), cy - int(ry * 0.8), cx + int(rx * 0.78), cy + int(ry * 0.8)], fill=(156, 133, 102, 230))
    draw.ellipse([cx - int(rx * 0.5), cy - int(ry * 0.6), cx + int(rx * 0.5), cy + int(ry * 0.6)], fill=(152, 130, 99, 255))
    return shadow_canvas.filter(ImageFilter.GaussianBlur(blur))

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

def measure_staff_linearity(img: Image.Image) -> float:
    px = img.load()
    assert px is not None
    centers: list[float] = []
    ys: list[float] = []
    for y in range(30, 124):
        xs = []
        for x in range(img.width):
            p = cast(tuple[int, ...], px[x, y])
            if p[3] > 120:
                is_bronze = (120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95)
                if is_bronze:
                    xs.append(x)
        if xs and len(xs) <= 14:
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

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    party_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/party/fox_idle.png").convert("RGBA")
    staff_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/fox/weapon/wpn_astral_staff.png").convert("RGBA")
    battle_src = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/fox_battle.png").convert("RGBA")
    body_clean = Image.open("/tmp/fox_test/char_no_shadow_no_wep.png").convert("RGBA")
    
    base_shadow = build_contact_shadow(cx=60, cy=119, rx=36, ry=5, blur=0.6)
    
    # Minimal 4 corner anchors so the body is free to articulate and stretch
    corner_anchors = [(0, 0), (127, 0), (0, 127), (127, 127)]
    
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

    poses = {}

    # =========================================================================
    # 1. IDLE (Standard upright neutral)
    # =========================================================================
    idle_img = Image.alpha_composite(base_shadow, body_clean)
    idle_img = Image.alpha_composite(idle_img, staff_src)
    poses["idle"] = idle_img

    # =========================================================================
    # 2. TELEGRAPH (Deep forward anticipation / charge crouch / staff horizontal guard)
    # =========================================================================
    shifts_telegraph = {
        "ear_l": (8, 8), "ear_r": (10, 8), "forehead": (10, 8),
        "eye_l": (10, 7), "eye_r": (12, 7), "snout": (13, 7),
        "neck": (10, 7), "core": (10, 6), "shoulder_l": (6, 7), "shoulder_r": (12, 6),
        "key_mount": (6, 6), "key_top": (4, 6), "key_bot": (4, 6),
        "pelvis": (4, 8), "hip_l": (2, 8), "hip_r": (6, 8),
        "tail_base": (0, 6), "tail_mid": (-6, 2), "tail_tip": (-12, -4),
        "knee_l": (-4, 6), "foot_l": (-2, 2),
        "knee_r": (6, 5), "foot_r": (4, 2),
        "hand": (-16, -2),
    }
    src_pts = list(corner_anchors)
    dst_pts = list(corner_anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_telegraph.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
    
    warped_tele = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Horizontal-diagonal guard staff (-38 deg)
    staff_tele = staff_src.rotate(-38, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-16, -2))
    
    tele_shadow = build_contact_shadow(cx=64, cy=121, rx=40, ry=6, blur=0.7)
    tele_img = Image.alpha_composite(tele_shadow, warped_tele)
    tele_img = Image.alpha_composite(tele_img, staff_tele)
    poses["telegraph"] = tele_img

    # =========================================================================
    # 3. ATTACK (Thrust strike / lunging forward / unclipped burst & clean shadow)
    # =========================================================================
    # 1. Clean the battle sprite background & halo
    b_im = battle_src.copy()
    bw, bh = b_im.size
    px = b_im.load()
    assert px is not None
    
    # Feather the right burst edge to eliminate the sharp vertical crop cut
    for y in range(bh):
        for x in range(bw):
            p = cast(tuple[int, ...], px[x, y])
            if p[3] > 0:
                # Feather out rightmost magic blast at x >= 118
                if x >= 118:
                    fade = max(0.0, 1.0 - (x - 118) / 8.0)
                    px[x, y] = (p[0], p[1], p[2], int(p[3] * fade))
                # Clean ground halo / white artifact under feet
                if y >= 117:
                    # Keep only dark paws
                    is_paw = (44 <= x <= 62 or 80 <= x <= 104) and y <= 122 and p[0] < 85 and p[1] < 85 and p[2] < 85
                    if not is_paw:
                        # Clear white/light fringe
                        px[x, y] = (0, 0, 0, 0)

    # Scale 0.93 and center with 6px safe margin
    scaled_w = int(round(bw * 0.93))
    scaled_h = int(round(bh * 0.93))
    b_scaled = b_im.resize((scaled_w, scaled_h), Image.Resampling.LANCZOS)
    
    b_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    b_canvas.paste(b_scaled, (0, 7), b_scaled)
    
    attack_shadow = build_contact_shadow(cx=62, cy=120, rx=44, ry=6, blur=0.8)
    attack_img = Image.alpha_composite(attack_shadow, b_canvas)
    poses["attack"] = attack_img

    # =========================================================================
    # 4. RECOVER (Deep low-crouch / recoil absorption / grounded staff)
    # True bodily height compression: head drops 18px! Torso folds down.
    # =========================================================================
    shifts_recover = {
        "ear_l": (-2, 18), "ear_r": (2, 18), "forehead": (0, 18),
        "eye_l": (-1, 18), "eye_r": (1, 18), "snout": (0, 19),
        "neck": (0, 18), "core": (0, 16), "shoulder_l": (-3, 16), "shoulder_r": (3, 16),
        "key_mount": (-3, 14), "key_top": (-3, 14), "key_bot": (-3, 14),
        "pelvis": (0, 16), "hip_l": (-6, 14), "hip_r": (6, 14),
        "tail_base": (0, 14), "tail_mid": (-6, 10), "tail_tip": (-10, 6),
        "knee_l": (-8, 10), "foot_l": (-4, 2),
        "knee_r": (8, 10), "foot_r": (4, 2),
        "hand": (-2, 16),
    }
    src_pts = list(corner_anchors)
    dst_pts = list(corner_anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_recover.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_recover = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff planted upright on ground, translated down +6px
    staff_recover = staff_src.rotate(0, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-2, 6))
    
    recover_shadow = build_contact_shadow(cx=60, cy=121, rx=42, ry=6, blur=0.7)
    recover_img = Image.alpha_composite(recover_shadow, warped_recover)
    recover_img = Image.alpha_composite(recover_img, staff_recover)
    poses["recover"] = recover_img

    # =========================================================================
    # 5. SKILL (Ascendant astral burst / staff held high skyward / head tilted up)
    # Bodily shift: Lifted upright (+4px), snout tilted skyward (-12px), ears tall
    # Staff rotated +48 deg, held high above head pointing toward upper-right sky
    # =========================================================================
    shifts_skill = {
        "ear_l": (-2, -10), "ear_r": (4, -10), "forehead": (1, -9),
        "eye_l": (0, -10), "eye_r": (3, -10), "snout": (3, -13),
        "neck": (2, -7), "core": (2, -5), "shoulder_l": (-2, -7), "shoulder_r": (5, -9),
        "key_mount": (-1, -5), "key_top": (-1, -5), "key_bot": (-1, -5),
        "pelvis": (0, -4), "hip_l": (-1, -4), "hip_r": (1, -4),
        "tail_base": (-1, -5), "tail_mid": (-8, -12), "tail_tip": (-14, -18),
        "knee_l": (0, -3), "foot_l": (0, -1),
        "knee_r": (0, -3), "foot_r": (0, -1),
        "hand": (8, -28),
    }
    src_pts = list(corner_anchors)
    dst_pts = list(corner_anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_skill.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_skill = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff rotated +48 deg, held high pointing to sky
    staff_skill = staff_src.rotate(48, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(6, -24))
    
    skill_shadow = build_contact_shadow(cx=60, cy=119, rx=34, ry=4, blur=0.6)
    skill_img = Image.alpha_composite(skill_shadow, warped_skill)
    skill_img = Image.alpha_composite(skill_img, staff_skill)
    poses["skill"] = skill_img

    # =========================================================================
    # 6. HIT (Dramatic stagger backward recoil / off-axis tilt / front foot lifted)
    # Head and torso flung back -22px! Off-axis tilt! Front foot lifted off ground.
    # =========================================================================
    shifts_hit = {
        "ear_l": (-24, -4), "ear_r": (-20, -4), "forehead": (-22, -6),
        "eye_l": (-21, -7), "eye_r": (-19, -7), "snout": (-20, -8),
        "neck": (-17, -4), "core": (-14, -2), "shoulder_l": (-22, -2), "shoulder_r": (-12, -5),
        "key_mount": (-16, -2), "key_top": (-18, -3), "key_bot": (-18, -1),
        "pelvis": (-8, 3), "hip_l": (-12, 3), "hip_r": (-5, 3),
        "tail_base": (-8, 3), "tail_mid": (-5, 7), "tail_tip": (2, 10),
        "knee_l": (-7, 3), "foot_l": (-8, 1),
        "knee_r": (5, -8), "foot_r": (9, -12),  # Front foot lifted 12px off ground in stagger!
        "hand": (-14, -18),
    }
    src_pts = list(corner_anchors)
    dst_pts = list(corner_anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_hit = warp_image_idw(body_clean, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Staff thrown backward-upward (-44 deg, pushed off-axis)
    staff_hit = staff_src.rotate(-44, resample=Image.Resampling.BICUBIC, center=(92, 88), translate=(-14, -18))
    
    hit_shadow = build_contact_shadow(cx=52, cy=119, rx=35, ry=5, blur=0.6)
    hit_img = Image.alpha_composite(hit_shadow, warped_hit)
    hit_img = Image.alpha_composite(hit_img, staff_hit)
    poses["hit"] = hit_img

    # =========================================================================
    # Save & Measure
    # =========================================================================
    print("\n=== Generating and Verifying Fox Action Poses (Kinematic v3) ===")
    p_idle = poses["idle"]
    
    for p_name in ["idle", "telegraph", "attack", "recover", "skill", "hit"]:
        img = poses[p_name]
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
    main()
