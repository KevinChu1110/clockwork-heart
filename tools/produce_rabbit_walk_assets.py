#!/usr/bin/env python3
"""
Produce Rabbit Walk Cycle Assets adhering to:
- Rule 4b-5 / 16: Consistent ground shadow band at y=118..123
- Rule 4b-7: True kinematic limb articulation (diff > 300 px vs resize+translate)
- Rule 4b-9 / 4b-9-2: Character height difference <= 5.0% vs equipped idle
- Rule 4b-11: Neutral bare body only (chassis + head_unit + winding_key + optic_core)
  No changeable costume or weapon welded into baked walk cycle.
- Foot lowest opaque y anchored at 118 (±1)
"""

import os
from PIL import Image, ImageChops

WORK_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLAYER_DIR = os.path.join(WORK_DIR, "game/assets/sprites/player")
PAPERDOLL_DIR = os.path.join(PLAYER_DIR, "paperdoll/rabbit")

def produce():
    chassis_p = os.path.join(PAPERDOLL_DIR, "chassis/paint_ivory_stock.png")
    head_p = os.path.join(PAPERDOLL_DIR, "head_unit/ear_rabbit_straight.png")
    optic_p = os.path.join(PAPERDOLL_DIR, "optic_core/core_cyan_emerald.png")
    key_p = os.path.join(PAPERDOLL_DIR, "winding_key/key_classic_brass.png")

    chassis = Image.open(chassis_p).convert("RGBA")
    head = Image.open(head_p).convert("RGBA")
    optic = Image.open(optic_p).convert("RGBA")
    key = Image.open(key_p).convert("RGBA")

    # 1. Decompose chassis into kinematic layers
    px = chassis.load()
    assert px is not None
    leg_l = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    leg_r = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    pelvis = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    torso_chassis = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    shadow = Image.new("RGBA", (128, 128), (0, 0, 0, 0))

    for y in range(128):
        for x in range(128):
            p = px[x, y]
            if p[3] == 0:
                continue
            # Ground shadow at y >= 118
            if y >= 118 and (p[3] <= 200 or (p[0] < 50 and p[1] < 50)):
                shadow.putpixel((x, y), p)
                continue
            if y < 98:
                torso_chassis.putpixel((x, y), p)
            elif y >= 98:
                if x <= 61:
                    leg_l.putpixel((x, y), p)
                else:
                    leg_r.putpixel((x, y), p)
                if 54 <= x <= 68 and 96 <= y <= 104:
                    pelvis.putpixel((x, y), p)

    # Neutral bare body upper layers (Rule 4b-11: NO costume, NO weapon)
    upper_body = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    upper_body.alpha_composite(key)
    upper_body.alpha_composite(torso_chassis)
    upper_body.alpha_composite(head)
    upper_body.alpha_composite(optic)

    pivot_l = (52, 98)
    pivot_r = (71, 98)

    gait_configs = [
        # Frame 0: Contact 1 (Left forward stride, Right rear stride)
        {
            "name": "Frame 0 (Contact 1)",
            "torso_dy": 0,
            "leg_l_rot": 9.0, "leg_l_dx": -1, "leg_l_dy": 0,
            "leg_r_rot": -9.0, "leg_r_dx": 1, "leg_r_dy": 0,
        },
        # Frame 1: Passing 1 (Up-bob, Left leg supporting on ground, Right leg lifted swinging forward)
        {
            "name": "Frame 1 (Passing 1)",
            "torso_dy": -1,
            "leg_l_rot": 0.0, "leg_l_dx": 0, "leg_l_dy": 1,
            "leg_r_rot": 13.0, "leg_r_dx": -2, "leg_r_dy": -4,
        },
        # Frame 2: Contact 2 (Down-squash, Right forward stride, Left rear stride)
        {
            "name": "Frame 2 (Contact 2)",
            "torso_dy": 0,
            "leg_l_rot": -9.0, "leg_l_dx": 1, "leg_l_dy": 0,
            "leg_r_rot": 9.0, "leg_r_dx": -1, "leg_r_dy": 0,
        },
        # Frame 3: Passing 2 (Up-bob, Right leg supporting on ground, Left leg lifted swinging forward)
        {
            "name": "Frame 3 (Passing 2)",
            "torso_dy": -1,
            "leg_l_rot": 13.0, "leg_l_dx": -2, "leg_l_dy": -4,
            "leg_r_rot": 0.0, "leg_r_dx": 0, "leg_r_dy": 1,
        },
    ]

    frames = []
    foot_ys_all = []
    for idx, cfg in enumerate(gait_configs):
        tdy = cfg["torso_dy"]
        frame = shadow.copy()

        # Rear leg
        lr = leg_r.rotate(cfg["leg_r_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["leg_r_dx"], cfg["leg_r_dy"]))
        frame.alpha_composite(lr)

        # Pelvis
        p_shift = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        p_shift.paste(pelvis, (0, tdy), pelvis)
        frame.alpha_composite(p_shift)

        # Front leg
        ll = leg_l.rotate(cfg["leg_l_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["leg_l_dx"], cfg["leg_l_dy"]))
        frame.alpha_composite(ll)

        # Measure foot y BEFORE upper body
        f_px = frame.load()
        assert f_px is not None
        foot_solid_ys = [y for y in range(110, 128) for x in range(40, 80) if f_px[x, y][3] > 200]
        foot_y = max(foot_solid_ys) if foot_solid_ys else 118
        foot_ys_all.append(foot_y)

        # Upper body
        ub_shift = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
        ub_shift.paste(upper_body, (0, tdy), upper_body)
        frame.alpha_composite(ub_shift)

        frames.append(frame)

    # Idle reference
    idle = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    idle.alpha_composite(shadow)
    idle.alpha_composite(leg_r)
    idle.alpha_composite(pelvis)
    idle.alpha_composite(leg_l)
    idle_f_px = idle.load()
    assert idle_f_px is not None
    idle_foot_solid = [y for y in range(110, 128) for x in range(40, 80) if idle_f_px[x, y][3] > 200]
    idle_foot_y = max(idle_foot_solid)
    idle.alpha_composite(upper_body)

    # Save 128x128 and 64x64 walk frames
    for idx, f_im in enumerate(frames):
        p_x3 = os.path.join(PLAYER_DIR, f"rabbit_walk_{idx}_x3.png")
        f_im.save(p_x3, "PNG")
        p_1x = os.path.join(PLAYER_DIR, f"rabbit_walk_{idx}.png")
        im_64 = f_im.resize((64, 64), Image.Resampling.LANCZOS)
        im_64.save(p_1x, "PNG")
        print(f"Saved {p_x3} and {p_1x}")

    return idle, frames, idle_foot_y, foot_ys_all

if __name__ == "__main__":
    produce()
