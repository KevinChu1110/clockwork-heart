#!/usr/bin/env python3
import math
import os
from typing import cast
from PIL import Image, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/takin"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/takin"

chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_takin_bronze_cast_default.png").convert("RGBA")
head_src = Image.open(f"{PD_DIR}/head_unit/head_takin_brass_twisted_horn_cowl.png").convert("RGBA")
optic_src = Image.open(f"{PD_DIR}/optic_core/face_takin_emerald_quartz_visors.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_takin_zen_pioneer_heavy_robe.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_takin_dual_bamboo_oil_flasks.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_takin_tri_leaf_zen_brass.png").convert("RGBA")
weapon_src = Image.open(f"{PD_DIR}/weapon/weapon_takin_zen_bamboo_cleaving_axe.png").convert("RGBA")

head_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
head_128.paste(head_src, (0, 3), head_src)
core_128 = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
core_128.paste(optic_src, (0, 3), optic_src)

def place_rotated_pivot(base_img, deg, pivot, target, scale=1.0):
    b = base_img.copy()
    px, py = pivot
    tx, ty = target
    canvas_size = 256
    large = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    paste_x = int(round(128.0 - px))
    paste_y = int(round(128.0 - py))
    large.paste(b, (paste_x, paste_y))
    if scale != 1.0:
        nw = int(round(canvas_size * scale))
        nh = int(round(canvas_size * scale))
        scaled = large.resize((nw, nh), Image.Resampling.LANCZOS)
        off_x = (nw - canvas_size) // 2
        off_y = (nh - canvas_size) // 2
        large = scaled.crop((off_x, off_y, off_x + canvas_size, off_y + canvas_size))
    rotated = large.rotate(deg, resample=Image.Resampling.BICUBIC, center=(128, 128))
    out = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    out_x = int(round(tx - 128.0))
    out_y = int(round(ty - 128.0))
    out.paste(rotated, (out_x, out_y), rotated)
    return out

weapon_128 = place_rotated_pivot(weapon_src, deg=0, pivot=(89.0, 80.0), target=(86.0, 80.0), scale=0.96)

base_idle = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")

w, h = 128, 128
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
c_px = base_idle.load()
s_px = clean_shadow.load()
assert c_px is not None and s_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p

EXPECTED_SHADOW = [59, 57, 53, 45, 29, 0, 0, 0, 0, 0]
counts = [int(np.sum(np.array(clean_shadow)[y, :, 3] > 20)) for y in range(118, 128)]
assert counts == EXPECTED_SHADOW, f"Shadow counts {counts} != {EXPECTED_SHADOW}"
print(f"Shadow counts verified: {counts}")

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

    for x in range(128):
        for m in range(4):
            o_px[x, m] = (0, 0, 0, 0)
        for m in range(2):
            o_px[x, 127 - m] = (0, 0, 0, 0)
    for y in range(128):
        for m in range(4):
            o_px[m, y] = (0, 0, 0, 0)
            o_px[127 - m, y] = (0, 0, 0, 0)

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
        if y < 90:
            torso_chassis.putpixel((x, y), p)
        if 86 <= y <= 102 and 36 <= x <= 80:
            pelvis.putpixel((x, y), p)
        if 92 <= y <= 117:
            if x <= 62:
                leg_l.putpixel((x, y), p)
            else:
                leg_r.putpixel((x, y), p)

pivot_l = (48, 98)
pivot_r = (78, 98)
pivot_head = (64, 40)
pivot_key = (38, 29)
pivot_wpn = (86, 80)
pivot_curio = (30, 80)

walk_configs = [
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -2.0,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "wpn_dx": -1, "wpn_dy": 1, "wpn_rot": 5.0,
        "key_rot": 18.0,
        "curio_rot": -3.0, "curio_dx": 1, "curio_dy": 0,
    },
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": -1,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
        "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": -3.0,
        "key_rot": -12.0,
        "curio_rot": 2.0, "curio_dx": 0, "curio_dy": -2,
    },
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 2.0,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "wpn_dx": 1, "wpn_dy": -1, "wpn_rot": -5.0,
        "key_rot": 18.0,
        "curio_rot": 3.0, "curio_dx": -1, "curio_dy": 0,
    },
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": -1,
        "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": 3.0,
        "key_rot": -12.0,
        "curio_rot": -2.0, "curio_dx": 0, "curio_dy": -2,
    },
]

walk_frames_128 = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=pivot_curio, translate=(cfg["curio_dx"], cfg["curio_dy"])))
    f.alpha_composite(c_rot)

    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)

    tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 70), translate=(cfg["torso_dx"], cfg["torso_dy"])))
    f.alpha_composite(tc_rot)

    cos_rot = clean_alpha_fringe(costume_128.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 70), translate=(cfg["torso_dx"], cfg["torso_dy"])))
    f.alpha_composite(cos_rot)

    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(h_rot)

    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(opt_rot)

    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=pivot_wpn, translate=(cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"])))
    f.alpha_composite(w_rot)

    f = enforce_shadow_rows(f, clean_shadow)
    walk_frames_128.append(f)

    bbox = f.getbbox()
    print(f"Frame {i} bbox: {bbox}")
    assert bbox[0] >= 4, f"L margin {bbox[0]} < 4"
    assert bbox[1] >= 4, f"T margin {bbox[1]} < 4"
    assert 128 - bbox[2] >= 4, f"R margin {128 - bbox[2]} < 4"
    assert 128 - bbox[3] >= 2, f"B margin {128 - bbox[3]} < 2"

# Check 4b-4 and 4b-7
print("\n--- Verifying 4b-4 and 4b-7 ---")
for i in range(4):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(base_idle, (dx, dy), base_idle)
            diff = ImageChops.difference(shifted, walk_frames_128[i]).getbbox()
            assert diff is not None, f"Frame {i} matches pure translation ({dx}, {dy})!"
    print(f"✓ Frame {i} passed 4b-4 (not pure translation)")

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
            for y_c in range(112):
                for x_c in range(128):
                    if walk_frames_128[i].getpixel((x_c, y_c)) != recon.getpixel((x_c, y_c)):
                        diff_px += 1
            if diff_px < min_diff:
                min_diff = diff_px
    print(f"✓ Frame {i} passed 4b-7 (articulation diff = {min_diff}px > 300px)")
    assert min_diff > 300, f"Frame {i} failed 4b-7: {min_diff} <= 300"
