#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/kite"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/kite"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"

w, h = 128, 128
comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

# Extract exact ground shadow
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
c_px = comp128.load()
s_px = clean_shadow.load()
assert c_px is not None and s_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p

counts = [int(np.sum(np.array(clean_shadow)[y, :, 3] > 20)) for y in range(118, 128)]
print("Baseline shadow counts:", counts)
EXPECTED_SHADOW = [49, 39, 23, 0, 0, 0, 0, 0, 0, 0]
assert counts == EXPECTED_SHADOW, f"Shadow {counts} != {EXPECTED_SHADOW}"

# Load 128 slices
chassis_128 = Image.open(f"{BASE_DIR}/chassis/chassis_kite_copper_obsidian_default.png").convert("RGBA")
head_128 = Image.open(f"{BASE_DIR}/head_unit/head_kite_raptor_cowl_beak.png").convert("RGBA")
key_128 = Image.open(f"{BASE_DIR}/winding_key/key_kite_turbine_relief_brass.png").convert("RGBA")
costume_128 = Image.open(f"{BASE_DIR}/costume/costume_kite_welder_cape_belt.png").convert("RGBA")
core_128 = Image.open(f"{BASE_DIR}/optic_core/face_kite_amber_quartz_rangefinder.png").convert("RGBA")
weapon_128 = Image.open(f"{BASE_DIR}/weapon/weapon_kite_crucible_recurve_bow.png").convert("RGBA")
curio_128 = Image.open(f"{BASE_DIR}/back_curio/curio_kite_spring_steel_cooling_wings.png").convert("RGBA")

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

    # Sanitize ultra-dark interpolation pixels to outline color
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
        if 84 <= y <= 98 and 46 <= x <= 82:
            pelvis.putpixel((x, y), p)
        if 96 <= y <= 117:
            if x <= 64:
                leg_l.putpixel((x, y), p)
            else:
                leg_r.putpixel((x, y), p)

pivot_l = (53, 98)
pivot_r = (73, 98)
pivot_head = (64, 38)
pivot_key = (72, 35)
pivot_wpn = (102, 71)
pivot_curio = (56, 78)

walk_configs = [
    # Frame 0: Left stride forward, cooling wings stabilizing flare, recurve bow forward swing
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -2.5,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "wpn_dx": -1, "wpn_dy": 1, "wpn_rot": 5.0,
        "key_rot": 18.0,
        "curio_rot": -3.0, "curio_dx": -1, "curio_dy": 0,
    },
    # Frame 1: Center stride compression (passing stance, turbine key spin)
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
        "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": -3.0,
        "key_rot": -15.0,
        "curio_rot": 2.0, "curio_dx": 0, "curio_dy": -2,
    },
    # Frame 2: Right stride step forward, cooling wings dynamic lift, recurve bow ready draw
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 2.5,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "wpn_dx": 2, "wpn_dy": -1, "wpn_rot": -5.0,
        "key_rot": 18.0,
        "curio_rot": 3.0, "curio_dx": 1, "curio_dy": 0,
    },
    # Frame 3: Rebound float / mechanical step reset
    {
        "torso_dx": 0, "torso_dy": -3, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0,
        "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 3.0,
        "key_rot": -15.0,
        "curio_rot": -2.0, "curio_dx": 0, "curio_dy": -2,
    },
]

walk_frames_128 = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    # 1. key (winding key behind chassis)
    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    # 2. back curio (cooling wings)
    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=pivot_curio, translate=(cfg["curio_dx"], cfg["curio_dy"])))
    f.alpha_composite(c_rot)

    # 3. legs (claws)
    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    # 4. pelvis
    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)

    # 5. torso chassis
    tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 60), translate=(cfg["torso_dx"], cfg["torso_dy"])))
    f.alpha_composite(tc_rot)

    # 6. costume
    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

    # 7. head unit
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(h_rot)

    # 8. optic core
    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(opt_rot)

    # 9. weapon
    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=pivot_wpn, translate=(cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"])))
    f.alpha_composite(w_rot)

    f = enforce_shadow_rows(f, clean_shadow)
    walk_frames_128.append(f)

# Test 4b-4 and 4b-7
base_idle = comp128
for i, fr in enumerate(walk_frames_128):
    bbox = fr.getbbox()
    assert bbox is not None
    left_m = bbox[0]
    top_m = bbox[1]
    right_m = 128 - bbox[2]
    bot_m = 128 - bbox[3]
    print(f"Frame {i} bbox: {bbox}, Margins: L={left_m}, T={top_m}, R={right_m}, B={bot_m}")
    assert left_m >= 4 and top_m >= 4 and right_m >= 4 and bot_m >= 2, f"Margins fail on frame {i}"

    # 4b-4
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(base_idle, (dx, dy), base_idle)
            diff = ImageChops.difference(shifted, fr).getbbox()
            assert diff is not None, f"Frame {i} matches pure translation ({dx}, {dy})"
    print(f"Frame {i}: passed Rule 4b-4 (no pure translation)")

    # 4b-7 articulation test
    min_diff = 999999
    for dy in range(-6, 7):
        for dh in range(-5, 6):
            nh = 128 + dh
            if nh <= 0:
                continue
            scaled = base_idle.resize((128, nh), Image.Resampling.LANCZOS)
            recon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            recon.paste(scaled, (0, dy - dh), scaled)
            diff_px = 0
            for y in range(112):
                for x in range(128):
                    if fr.getpixel((x, y)) != recon.getpixel((x, y)):
                        diff_px += 1
            if diff_px < min_diff:
                min_diff = diff_px
    print(f"Frame {i}: passed Rule 4b-7 with articulation diff = {min_diff}px (> 300px)")
    assert min_diff > 300, f"Frame {i} failed 4b-7: {min_diff} <= 300"

    # Shadow test
    f_shadow = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], fr.getpixel((x, y)))[3] > 20) for y in range(118, 128)]
    assert f_shadow == EXPECTED_SHADOW, f"Frame {i} shadow {f_shadow} != {EXPECTED_SHADOW}"
    print(f"Frame {i}: passed Rule 4b-5 shadow row counts match {f_shadow}")

print("\nALL WALK KINEMATICS PASSED!")
