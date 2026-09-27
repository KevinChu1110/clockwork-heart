    # =========================================================================
    # 5. HIT (防護過載·阻尼受擊後仰 / Kinetic Damper Recoil & Shock Stagger)
    # Heavy impact stagger: body and head pitch far back (x-15, y-2).
    # Lance is jolted upward and outwards to the flank (target_center=(26, 74), deg=10),
    # absolutely NO clipping through torso!
    # Clean kinetic impact cross-star flash & directional damper exhaust.
    # =========================================================================
    shifts_hit = {
        "head_top": (-16, -2), "ear_l": (-18, -2), "ear_r": (-14, -2),
        "eye_l": (-15, -2), "eye_r": (-15, -2), "snout": (-14, 0), "throat": (-13, 0),
        "core": (-12, 0),
        "shoulder_l": (-8, 1), "arm_l": (-6, 3),
        "shoulder_r": (-12, 0), "arm_r": (-14, 0),
        "torso": (-10, 1), "pelvis": (-8, 1),
        "hip_l": (-10, 1), "hip_r": (-5, 1),
        "knee_l": (-11, 0), "knee_r": (-5, 0),
        "foot_l": (-7, 0), "foot_r": (-3, 0), "rear_l": (-8, 0), "rear_r": (-4, 0),
        "tail_root": (-10, 1), "tail_tip": (-14, 4),
        "key_mount": (-12, 0), "key_head": (-13, -2),
        "curio_center": (-14, 6),
    }
    src_pts = list(anchors)
    dst_pts = list(anchors)
    for name, (bx, by) in base_landmarks.items():
        dx, dy = shifts_hit.get(name, (0, 0))
        src_pts.append((bx, by))
        dst_pts.append((bx + dx, by + dy))

    warped_hit = warp_image_idw(body_no_weapon, src_pts, dst_pts, power=2.0, epsilon=4.0)
    # Lance is held at outer left flank, jolted upward-backwards (deg=12, target_center=(24, 76))
    # Mirrored=False so tip is at (4..12, 44..52), completely outside body profile!
    lance_hit = place_lance(lance_raw, deg=12, target_center=(24, 76), scale=0.98, mirror=False)

    # Deflection cross-star spark & directional damper exhaust
    hit_fx = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    h_draw = ImageDraw.Draw(hit_fx)
    cx, cy = 48, 68
    # Clean 4-point cross star flash on shield/harness impact point
    h_draw.line([(cx - 10, cy), (cx + 10, cy)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx, cy - 10), (cx, cy + 10)], fill=(255, 255, 230, 240), width=2)
    h_draw.line([(cx - 5, cy - 5), (cx + 5, cy + 5)], fill=(56, 160, 255, 220), width=1)
    h_draw.line([(cx - 5, cy + 5), (cx + 5, cy - 5)], fill=(255, 208, 40, 220), width=1)
    h_draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=(255, 255, 255, 255))
    # Deflection sparks flying away
    h_draw.point([(cx - 8, cy - 7), (cx + 9, cy - 6), (cx + 7, cy + 8), (cx - 7, cy + 9)], fill=(255, 255, 220, 255))
    # Directional pneumatic steam exhaust from polymer joints
    h_draw.line([(68, 48), (92, 40)], fill=(240, 248, 255, 200), width=2)
    h_draw.line([(66, 52), (94, 48)], fill=(220, 235, 250, 170), width=1)
    h_draw.line([(70, 56), (96, 56)], fill=(220, 235, 250, 160), width=1)
    # LED eyes flash alert orange-red
    h_draw.ellipse([36, 36, 44, 42], fill=(255, 94, 138, 220))
    h_draw.ellipse([58, 36, 66, 42], fill=(255, 94, 138, 220))
    hit_fx = hit_fx.filter(ImageFilter.GaussianBlur(0.5))

    hit_canvas = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_canvas = Image.alpha_composite(hit_canvas, warped_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, lance_hit)
    hit_canvas = Image.alpha_composite(hit_canvas, hit_fx)
    poses["hit"] = enforce_ground_shadow(hit_canvas)
