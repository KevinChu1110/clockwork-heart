#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/marmot"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/marmot"

chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_marmot_quarry_tinplate_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_marmot_alloy_chisel_visor.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_marmot_dual_pawl_brass.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_marmot_scavenger_canvas_harness.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_marmot_amber_dust_goggles.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_marmot_eccentric_piston_fists.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_marmot_pneumatic_sand_tail.png").convert("RGBA")

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

# Separate left and right gauntlets
fist_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
fist_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
w_px = weapon_128.load()
assert w_px is not None
for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], w_px[x, y])
        if p[3] == 0:
            continue
        if x <= 64:
            fist_l.putpixel((x, y), p)
        else:
            fist_r.putpixel((x, y), p)

pivot_l = (48, 98)
pivot_r = (78, 98)
pivot_head = (64, 40)
pivot_key = (38, 32)
pivot_fist_l = (46, 75)
pivot_fist_r = (86, 75)
pivot_curio = (32, 92)

walk_configs = [
    # Frame 0: Left stride advance, left fist forward punch, right leg back, chassis tilt left
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -2.0,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "fl_dx": 1, "fl_dy": 0, "fl_rot": 6.0,
        "fr_dx": -1, "fr_dy": 1, "fr_rot": -4.0,
        "key_rot": 18.0,
        "curio_rot": -4.0, "curio_dx": 1, "curio_dy": 0,
    },
    # Frame 1: Center stride compression (crouch & pressure reset)
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": -1,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
        "fl_dx": 0, "fl_dy": -2, "fl_rot": -2.0,
        "fr_dx": 0, "fr_dy": -2, "fr_rot": -2.0,
        "key_rot": -15.0,
        "curio_rot": 3.0, "curio_dx": 0, "curio_dy": -2,
    },
    # Frame 2: Right stride advance, right fist forward punch, left leg back, chassis tilt right
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 2.0,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "fl_dx": -1, "fl_dy": 1, "fl_rot": -4.0,
        "fr_dx": 2, "fr_dy": -1, "fr_rot": 6.0,
        "key_rot": 18.0,
        "curio_rot": 4.0, "curio_dx": -1, "curio_dy": 0,
    },
    # Frame 3: Rebound float / mechanical step reset
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": -1,
        "fl_dx": 0, "fl_dy": -2, "fl_rot": 2.0,
        "fr_dx": 0, "fr_dy": -2, "fr_rot": 2.0,
        "key_rot": -15.0,
        "curio_rot": -3.0, "curio_dx": 0, "curio_dy": -2,
    },
]

walk_frames_128 = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    # 1. key (behind chassis)
    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"] + 2), k_rot)

    # 2. back curio (tail)
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

    # 6. costume
    cos_rot = clean_alpha_fringe(costume_128.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 72), translate=(cfg["torso_dx"], cfg["torso_dy"] + 2)))
    f.alpha_composite(cos_rot)

    # 7. head unit
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"] + 2)))
    f.alpha_composite(h_rot)

    # 8. optic core
    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"] + 2)))
    f.alpha_composite(opt_rot)

    # 9. fists (left & right separately)
    fl_rot = clean_alpha_fringe(fist_l.rotate(cfg["fl_rot"], resample=Image.Resampling.BICUBIC, center=pivot_fist_l, translate=(cfg["torso_dx"] + cfg["fl_dx"], cfg["torso_dy"] + cfg["fl_dy"] + 2)))
    fr_rot = clean_alpha_fringe(fist_r.rotate(cfg["fr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_fist_r, translate=(cfg["torso_dx"] + cfg["fr_dx"], cfg["torso_dy"] + cfg["fr_dy"] + 2)))
    f.alpha_composite(fl_rot)
    f.alpha_composite(fr_rot)

    f = enforce_shadow_rows(f, clean_shadow)
    walk_frames_128.append(f)

# Verification tests
print("--- VERIFYING WALK FRAMES ---")
for i, fr in enumerate(walk_frames_128):
    bbox = fr.getbbox()
    print(f"Frame {i}: bbox={bbox}")
    arr = np.array(fr)
    counts = [int(np.sum(arr[y, :, 3] > 20)) for y in range(118, 128)]
    assert counts == EXPECTED_SHADOW, f"Frame {i} shadow {counts} != {EXPECTED_SHADOW}"
    print(f"  ✓ Shadow counts match: {counts}")

# Check inter-frame difference and non-translation
for i in range(4):
    for j in range(i + 1, 4):
        diff = ImageChops.difference(walk_frames_128[i], walk_frames_128[j])
        d_arr = np.array(diff)
        diff_px = int(np.sum(np.any(d_arr > 0, axis=-1)))
        print(f"Diff Frame {i} vs Frame {j}: {diff_px} px")
        assert diff_px > 300, f"Diff {i} vs {j} too small: {diff_px} <= 300"

# Check diff vs idle & exhaustive shift
for i, fr in enumerate(walk_frames_128):
    min_diff = 999999
    best_shift = None
    for dx in range(-10, 11):
        for dy in range(-10, 11):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(comp128, (dx, dy), comp128)
            diff = ImageChops.difference(shifted, fr)
            diff_arr = np.array(diff)
            diff_count = int(np.sum(np.any(diff_arr > 0, axis=-1)))
            if diff_count < min_diff:
                min_diff = diff_count
                best_shift = (dx, dy)
    print(f"Frame {i} vs Idle: min_diff={min_diff} px at shift {best_shift} (req: >400)")
    assert min_diff > 400, f"Frame {i} failed non-translation test: {min_diff} <= 400"

print("✓ ALL WALK KINEMATICS TESTS PASSED!")
