#!/usr/bin/env python3
"""
tools/generate_rabbit_attack_pose.py
Generates the kinematic combat attack action pose for Rabbit (Whitey) in Clockwork Heart:
  game/assets/sprites/player/poses/attack.png (128x128 RGBA)

Standards & Rules enforced:
- Rule 4b / 4b-4: Substantial genuine kinematic pose difference (diff vs idle > 6000 px, residual > 3700 px, not a translation).
- Rule 4b-5 / 4b-9: Body height diff <= 5%, foot lowest opaque y == idle (118 ± 1 px).
- Rule 19i-7: Sword is firmly held by the robot hand (white robot fingers wrap around the grip over the crossguard).
- Rule 0a / 0b / 10a: Preserves Whitey's automaton features (ears, brass key, cyan heart core) and single-handed dawn blade.
"""

import os
import math
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUT_PATH = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/attack.png")

# Palette constants matching Whitey's canonical design
C_OUTLINE      = (35, 22, 18, 255)
C_BRASS_SPEC   = (255, 255, 220, 255)
C_BRASS_HI     = (255, 225, 80, 255)
C_BRASS_MID    = (215, 160, 30, 255)
C_BRASS_SHAD   = (145, 95, 18, 255)

C_STEEL_SPEC   = (255, 255, 255, 255)
C_STEEL_HI     = (232, 244, 252, 255)
C_STEEL_MID    = (198, 218, 234, 255)
C_STEEL_RIDGE  = (140, 168, 190, 255)
C_STEEL_FULLER = (70, 92, 112, 255)
C_STEEL_SHAD   = (95, 120, 142, 255)
C_STEEL_DARK   = (62, 82, 100, 255)

C_DARK_GRIP    = (38, 24, 18, 255)

C_IVORY_SPEC   = (255, 255, 255, 255)
C_IVORY_HI     = (250, 246, 238, 255)
C_IVORY_MID    = (226, 214, 196, 255)
C_IVORY_CREASE = (45, 28, 20, 255)

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

def build_soft_contact_shadow(cx: int = 68, cy: int = 120, rx: int = 38, ry: int = 2) -> Image.Image:
    shadow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shadow)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(15, 10, 20, 25))
    draw.ellipse([cx - int(rx * 0.6), cy - ry, cx + int(rx * 0.6), cy + ry], fill=(15, 10, 20, 32))
    return shadow.filter(ImageFilter.GaussianBlur(0.5))

def draw_sword_held(
    canvas_w: int = 128,
    canvas_h: int = 128,
    grip_center: tuple[float, float] = (68.0, 77.0),
    blade_angle_deg: float = 18.0,
    blade_len: float = 45.0
) -> tuple[Image.Image, Image.Image, Image.Image]:
    under = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    sword = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    hand = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
    
    d_under = ImageDraw.Draw(under)
    d_sword = ImageDraw.Draw(sword)
    d_hand = ImageDraw.Draw(hand)
    
    gx, gy = grip_center
    rad = math.radians(blade_angle_deg)
    ux = math.cos(rad)
    uy = -math.sin(rad)
    nx = -uy
    ny = ux
    
    # Pommel
    pom_x = gx - 9.0 * ux
    pom_y = gy - 9.0 * uy
    d_sword.ellipse([pom_x - 3.5, pom_y - 3.5, pom_x + 3.5, pom_y + 3.5], fill=C_OUTLINE)
    d_sword.ellipse([pom_x - 2.5, pom_y - 2.5, pom_x + 2.5, pom_y + 2.5], fill=C_BRASS_MID)
    d_sword.ellipse([pom_x - 1.2, pom_y - 1.2, pom_x + 0.5, pom_y + 0.5], fill=C_BRASS_SPEC)
    
    # Grip
    d_sword.line([(pom_x, pom_y), (gx + 6.0*ux, gy + 6.0*uy)], fill=C_OUTLINE, width=6)
    d_sword.line([(pom_x, pom_y), (gx + 6.0*ux, gy + 6.0*uy)], fill=C_DARK_GRIP, width=4)
    
    # Crossguard
    guard_cx = gx + 6.5 * ux
    guard_cy = gy + 6.5 * uy
    gw = 9.5
    g_top = (guard_cx + gw * nx, guard_cy + gw * ny)
    g_bot = (guard_cx - gw * nx, guard_cy - gw * ny)
    d_sword.line([g_bot, g_top], fill=C_OUTLINE, width=6)
    d_sword.line([g_bot, g_top], fill=C_BRASS_MID, width=4)
    d_sword.line([(guard_cx - (gw-2)*nx, guard_cy - (gw-2)*ny),
                  (guard_cx + (gw-2)*nx, guard_cy + (gw-2)*ny)], fill=C_BRASS_HI, width=2)
    d_sword.ellipse([guard_cx - 3.0, guard_cy - 3.0, guard_cx + 3.0, guard_cy + 3.0], fill=C_OUTLINE)
    d_sword.ellipse([guard_cx - 2.0, guard_cy - 2.0, guard_cx + 2.0, guard_cy + 2.0], fill=C_BRASS_SPEC)
    
    # Blade
    b_start = (guard_cx + 2.0 * ux, guard_cy + 2.0 * uy)
    b_tip = (guard_cx + blade_len * ux, guard_cy + blade_len * uy)
    bw = 3.5
    taper_len = 8.0
    b_taper = (guard_cx + (blade_len - taper_len) * ux, guard_cy + (blade_len - taper_len) * uy)
    
    poly_outline = [
        (b_start[0] + bw * nx, b_start[1] + bw * ny),
        (b_taper[0] + bw * nx, b_taper[1] + bw * ny),
        b_tip,
        (b_taper[0] - bw * nx, b_taper[1] - bw * ny),
        (b_start[0] - bw * nx, b_start[1] - bw * ny),
    ]
    d_sword.polygon(poly_outline, fill=C_OUTLINE)
    
    poly_fill = [
        (b_start[0] + (bw - 1.0) * nx, b_start[1] + (bw - 1.0) * ny),
        (b_taper[0] + (bw - 1.0) * nx, b_taper[1] + (bw - 1.0) * ny),
        (b_tip[0] - 1.0 * ux, b_tip[1] - 1.0 * uy),
        (b_taper[0] - (bw - 1.0) * nx, b_taper[1] - (bw - 1.0) * ny),
        (b_start[0] - (bw - 1.0) * nx, b_start[1] - (bw - 1.0) * ny),
    ]
    d_sword.polygon(poly_fill, fill=C_STEEL_MID)
    
    d_sword.line([
        (b_start[0] + (bw - 1.3) * nx, b_start[1] + (bw - 1.3) * ny),
        (b_taper[0] + (bw - 1.3) * nx, b_taper[1] + (bw - 1.3) * ny),
        (b_tip[0] - 1.2 * ux, b_tip[1] - 1.2 * uy)
    ], fill=C_STEEL_SPEC, width=1)
    
    d_sword.line([
        (b_start[0] - (bw - 1.3) * nx, b_start[1] - (bw - 1.3) * ny),
        (b_taper[0] - (bw - 1.3) * nx, b_taper[1] - (bw - 1.3) * ny),
        (b_tip[0] - 1.2 * ux, b_tip[1] - 1.2 * uy)
    ], fill=C_STEEL_SHAD, width=1)
    
    d_sword.line([
        (b_start[0], b_start[1]),
        (b_taper[0], b_taper[1])
    ], fill=C_STEEL_FULLER, width=1)
    
    # Right arm (shoulder 50, 75 to wrist)
    wrist_r = (gx - 2.5 * nx, gy - 2.5 * ny)
    d_under.line([(50, 75), wrist_r], fill=C_OUTLINE, width=8)
    d_under.line([(50, 75), wrist_r], fill=C_IVORY_MID, width=6)
    d_under.line([(50, 75), wrist_r], fill=C_IVORY_HI, width=3)
    
    d_under.ellipse([46, 71, 54, 79], fill=C_OUTLINE)
    d_under.ellipse([47, 72, 53, 78], fill=C_BRASS_MID)
    d_under.ellipse([48, 73, 52, 77], fill=C_BRASS_HI)
    
    d_under.ellipse([wrist_r[0] - 4.5, wrist_r[1] - 4.5, wrist_r[0] + 4.5, wrist_r[1] + 4.5], fill=C_OUTLINE)
    d_under.ellipse([wrist_r[0] - 3.5, wrist_r[1] - 3.5, wrist_r[0] + 3.5, wrist_r[1] + 3.5], fill=C_IVORY_MID)
    
    # Hand wrap (over sword hilt)
    palm_cx = gx - 1.5 * nx
    palm_cy = gy - 1.5 * ny
    d_hand.ellipse([palm_cx - 5.5, palm_cy - 5.5, palm_cx + 5.5, palm_cy + 5.5], fill=C_OUTLINE)
    d_hand.ellipse([palm_cx - 4.5, palm_cy - 4.5, palm_cx + 4.5, palm_cy + 4.5], fill=C_IVORY_MID)
    d_hand.ellipse([palm_cx - 3.0, palm_cy - 3.0, palm_cx + 1.0, palm_cy + 1.0], fill=C_IVORY_HI)
    
    finger_u_offsets = [4.5, 1.8, -1.0, -3.8]
    for i, fo in enumerate(finger_u_offsets):
        f_bx = gx + fo * ux - 2.0 * nx
        f_by = gy + fo * uy - 2.0 * ny
        f_tx = gx + fo * ux + 3.5 * nx
        f_ty = gy + fo * uy + 3.5 * ny
        
        d_hand.line([(f_bx, f_by), (f_tx, f_ty)], fill=C_OUTLINE, width=4)
        d_hand.line([(f_bx, f_by), (f_tx, f_ty)], fill=C_IVORY_HI if i in [0, 1] else C_IVORY_MID, width=2)
        d_hand.point((int(round(gx + fo * ux + 0.5 * nx)), int(round(gy + fo * uy + 0.5 * ny))), fill=C_IVORY_SPEC)
        d_hand.point((int(round(f_tx)), int(round(f_ty))), fill=C_OUTLINE)
        
    thumb_x = gx + 3.0 * ux - 3.5 * nx
    thumb_y = gy + 3.0 * uy - 3.5 * ny
    d_hand.ellipse([thumb_x - 3.0, thumb_y - 3.0, thumb_x + 3.0, thumb_y + 3.0], fill=C_OUTLINE)
    d_hand.ellipse([thumb_x - 2.0, thumb_y - 2.0, thumb_x + 2.0, thumb_y + 2.0], fill=C_IVORY_HI)
    d_hand.point((int(round(thumb_x)), int(round(thumb_y))), fill=C_IVORY_SPEC)
    
    # Left arm (supporting fighting guard)
    d_under.line([(76, 73), (83, 82), (76, 87)], fill=C_OUTLINE, width=6)
    d_under.line([(76, 73), (83, 82), (76, 87)], fill=C_IVORY_MID, width=4)
    d_under.ellipse([72, 70, 80, 78], fill=C_OUTLINE)
    d_under.ellipse([73, 71, 79, 77], fill=C_BRASS_MID)
    d_under.ellipse([72, 83, 80, 91], fill=C_OUTLINE)
    d_under.ellipse([73, 84, 79, 90], fill=C_IVORY_HI)
    d_under.line([(74, 86), (78, 88)], fill=C_IVORY_CREASE, width=1)
    
    return under, sword, hand

def generate_rabbit_attack_pose() -> Image.Image:
    stock = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png").convert("RGBA")
    ear = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit/head_unit/ear_rabbit_straight.png").convert("RGBA")
    key = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit/winding_key/key_classic_brass.png").convert("RGBA")
    core = Image.open(f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/rabbit/optic_core/core_cyan_emerald.png").convert("RGBA")
    
    # Composite clean bare body
    bare_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    bare_body.alpha_composite(key)
    bare_body.alpha_composite(stock)
    bare_body.alpha_composite(ear)
    bare_body.alpha_composite(core)
    
    clean_body = bare_body.copy()
    cb_px = clean_body.load()
    assert cb_px is not None
    
    # Remove old resting arms so character only has active swinging arms
    for y in range(70, 98):
        for x in range(32, 47):
            p = cast(tuple[int, int, int, int], cb_px[x, y])
            if p[3] > 0:
                cb_px[x, y] = (0, 0, 0, 0)
    for y in range(72, 98):
        for x in range(78, 95):
            p = cast(tuple[int, int, int, int], cb_px[x, y])
            if p[3] > 0:
                cb_px[x, y] = (0, 0, 0, 0)
                
    draw_cb = ImageDraw.Draw(clean_body)
    flank_l = [(47, 70), (46, 74), (45, 80), (46, 86), (48, 92), (50, 96)]
    for i in range(len(flank_l) - 1):
        draw_cb.line([flank_l[i], flank_l[i+1]], fill=(35, 22, 18, 255), width=2)
    flank_r = [(77, 70), (78, 74), (79, 80), (78, 86), (77, 92), (74, 96)]
    for i in range(len(flank_r) - 1):
        draw_cb.line([flank_r[i], flank_r[i+1]], fill=(35, 22, 18, 255), width=2)
        
    for y in range(119, 128):
        for x in range(128):
            cb_px[x, y] = (0, 0, 0, 0)
            
    anchors = [(0, 0), (127, 0), (0, 127), (127, 127),
               (0, 64), (127, 64), (64, 0), (64, 127)]
    base_landmarks = {
        "ear_tip_l": (46, 7), "ear_tip_r": (77, 8),
        "ear_mid_l": (48, 25), "ear_mid_r": (75, 25),
        "ear_base_l": (50, 42), "ear_base_r": (72, 42),
        "forehead": (62, 38), "brow": (64, 48),
        "eye_l": (54, 58), "eye_r": (72, 58),
        "snout": (64, 62), "mouth": (64, 65),
        "chin": (64, 68), "neck": (64, 71),
        "core": (69, 79), "torso_center": (62, 82),
        "shoulder_l": (46, 74), "shoulder_r": (76, 74),
        "key_mount": (42, 73), "key_top": (38, 66), "key_bot": (38, 80),
        "pelvis": (62, 95),
        "hip_l": (50, 98), "knee_l": (52, 107), "foot_l": (55, 115),
        "hip_r": (70, 98), "knee_r": (72, 107), "foot_r": (71, 115),
    }
    shifts_attack = {
        "ear_tip_l": (6, 0), "ear_tip_r": (8, 0),
        "ear_mid_l": (7, 1), "ear_mid_r": (9, 1),
        "ear_base_l": (8, 1), "ear_base_r": (10, 1),
        "forehead": (9, 2), "brow": (9, 2),
        "eye_l": (9, 2), "eye_r": (10, 2),
        "snout": (11, 2), "mouth": (11, 2), "chin": (10, 2), "neck": (10, 2),
        "core": (9, 2), "torso_center": (8, 2),
        "shoulder_l": (5, 2), "shoulder_r": (10, 2),
        "key_mount": (4, 2), "key_top": (3, 2), "key_bot": (3, 2),
        "pelvis": (6, 2),
        "hip_l": (-3, 2), "knee_l": (-6, 2), "foot_l": (-8, 0),
        "hip_r": (9, 2), "knee_r": (12, 1), "foot_r": (12, 0),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for k, (bx, by) in base_landmarks.items():
        dx, dy = shifts_attack.get(k, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))
        
    warped_body = warp_image_idw(clean_body, src_pts, dst_pts, power=2.0, epsilon=4.0)
    
    under, sword, hand = draw_sword_held(
        canvas_w=128, canvas_h=128,
        grip_center=(68.0, 77.0),
        blade_angle_deg=18.0,
        blade_len=45.0
    )
    
    swoosh = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    draw_sw = ImageDraw.Draw(swoosh)
    draw_sw.arc([55, 35, 122, 105], start=-65, end=35, fill=(160, 230, 255, 140), width=2)
    draw_sw.arc([57, 37, 120, 103], start=-55, end=25, fill=(255, 255, 255, 200), width=1)
    swoosh = swoosh.filter(ImageFilter.GaussianBlur(0.5))
    
    shadow = build_soft_contact_shadow(cx=68, cy=120, rx=38, ry=2)
    
    attack_pose = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    attack_pose.alpha_composite(shadow)
    attack_pose.alpha_composite(warped_body)
    attack_pose.alpha_composite(under)
    attack_pose.alpha_composite(sword)
    attack_pose.alpha_composite(hand)
    attack_pose.alpha_composite(swoosh)
    
    return attack_pose

if __name__ == "__main__":
    pose = generate_rabbit_attack_pose()
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    pose.save(OUTPUT_PATH)
    print(f"Generated rabbit attack pose: {OUTPUT_PATH}")
