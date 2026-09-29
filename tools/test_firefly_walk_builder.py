import os
from typing import cast
from PIL import Image, ImageChops
import numpy as np

repo = "/root/.hermes/kanban/boards/side-bravesoul/workspaces/t_e4a76321"
PD_DIR = f"{repo}/game/assets/sprites/player/paperdoll/firefly"
POSES_DIR = f"{repo}/game/assets/sprites/player/poses/firefly"

chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_firefly_emerald_tinplate_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_firefly_brass_antenna_cowl.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_firefly_floral_gear_brass.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_firefly_vine_harness_cuirass.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_firefly_dual_lantern_quartz_eyes.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_firefly_luminescent_vine_staff.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_firefly_luminescent_resin_abdomen.png").convert("RGBA")

w, h = 128, 128
comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")

clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
c_px = comp128.load()
s_px = clean_shadow.load()
assert c_px is not None and s_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p

EXPECTED_SHADOW = [59, 57, 53, 45, 29, 0, 0, 0, 0, 0]

def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)

def enforce_shadow_rows(img: Image.Image, shadow_ref: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = shadow_ref.load()
    assert o_px is not None and s_px is not None

    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
                o_px[x, y] = sp

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    for x in range(128):
        for m in range(4):
            o_px[x, m] = (0, 0, 0, 0)
        for m in range(2):
            o_px[x, 127 - m] = (0, 0, 0, 0)
    for y in range(128):
        for m in range(4):
            o_px[m, y] = (0, 0, 0, 0)
            o_px[127 - m, y] = (0, 0, 0, 0)

    # Sanitize ultra-dark interpolation pixels to outline color #1F1A3A
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

ch_px = chassis_128.load()
assert ch_px is not None

leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0 or y >= 118:
            continue
        if y < 86:
            torso_chassis.putpixel((x, y), p)
        if 80 <= y <= 104 and 40 <= x <= 86:
            pelvis.putpixel((x, y), p)
        if y >= 90:
            if x <= 63:
                leg_l.putpixel((x, y), p)
            else:
                leg_r.putpixel((x, y), p)

pivot_l = (48, 98)
pivot_r = (78, 98)
pivot_head = (64, 40)
pivot_key = (38, 32)
pivot_weapon = (95, 65)
pivot_curio = (34, 75)

walk_configs = [
    # Frame 0: Left stride advance, staff tilts forward, right leg back, chassis tilt left
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -2.0,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "wp_dx": 1, "wp_dy": 0, "wp_rot": 5.0,
        "key_rot": 18.0,
        "curio_rot": -4.0, "curio_dx": 1, "curio_dy": 0,
    },
    # Frame 1: Center stride compression (crouch & pressure reset)
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": -1,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
        "wp_dx": 0, "wp_dy": -2, "wp_rot": -2.0,
        "key_rot": -15.0,
        "curio_rot": 3.0, "curio_dx": 0, "curio_dy": -2,
    },
    # Frame 2: Right stride advance, staff tilts back, left leg back, chassis tilt right
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 2.0,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "wp_dx": -1, "wp_dy": 1, "wp_rot": -5.0,
        "key_rot": 18.0,
        "curio_rot": 4.0, "curio_dx": -1, "curio_dy": 0,
    },
    # Frame 3: Rebound float / mechanical step reset
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": -1,
        "wp_dx": 0, "wp_dy": -2, "wp_rot": 2.0,
        "key_rot": -15.0,
        "curio_rot": -3.0, "curio_dx": 0, "curio_dy": -2,
    },
]

walk_frames = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    # 1. key (winding key behind chassis)
    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"] + 2), k_rot)

    # 2. back curio (luminescent resin abdomen)
    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=pivot_curio, translate=(cfg["curio_dx"], cfg["curio_dy"] + 2)))
    f.alpha_composite(c_rot)

    # 3. legs
    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"] + 2)))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"] + 2)))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    # 4. pelvis
    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"] + 2), pelvis)

    # 5. torso chassis
    tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 72), translate=(cfg["torso_dx"], cfg["torso_dy"] + 2)))
    f.alpha_composite(tc_rot)

    # 6. costume (vine harness cuirass)
    cos_rot = clean_alpha_fringe(costume_128.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 72), translate=(cfg["torso_dx"], cfg["torso_dy"] + 2)))
    f.alpha_composite(cos_rot)

    # 7. head unit (brass antenna cowl)
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"] + 2)))
    f.alpha_composite(h_rot)

    # 8. optic core (dual lantern quartz eyes)
    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"] + 2)))
    f.alpha_composite(opt_rot)

    # 9. weapon (luminescent vine staff)
    wp_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wp_rot"], resample=Image.Resampling.BICUBIC, center=pivot_weapon, translate=(cfg["torso_dx"] + cfg["wp_dx"], cfg["torso_dy"] + cfg["wp_dy"] + 2)))
    f.alpha_composite(wp_rot)

    f = enforce_shadow_rows(f, clean_shadow)
    walk_frames.append(f)

# Verification
for i, fr in enumerate(walk_frames):
    arr = np.array(fr)
    counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Frame {i} shadow counts: {counts} matches: {counts == EXPECTED_SHADOW}")

    # Non-translation check vs idle
    min_diff = 999999
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(comp128, (dx, dy), comp128)
            diff = ImageChops.difference(shifted, fr)
            d_arr = np.array(diff)
            diff_px = int(np.sum(np.any(d_arr > 0, axis=-1)))
            if diff_px < min_diff:
                min_diff = diff_px
    print(f"Frame {i} min_diff vs idle: {min_diff}px (req >= 400px)")
