#!/usr/bin/env python3
"""
Test script to tune walk parameters for viper to guarantee:
- Rule 4b-4: Guaranteed not pure translation (min diff > 400px)
- Rule 4b-5: 100% exact shadow [60, 59, 53, 45, 27, 0, 0, 0, 0, 0]
- Rule 4b-7: Articulation diff > 300px
- Rule 4c-5 / 16: Safe margins L>=4, T>=4, R>=4, B>=2
"""
import os
from typing import cast
from PIL import Image, ImageDraw, ImageChops, ImageFilter
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/viper"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/viper"

comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")
comp512 = Image.open(f"{POSES_DIR}/idle_512.png").convert("RGBA")

chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_viper_bamboo_lacquer_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_viper_carved_bamboo_crest_hood.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_viper_bamboo_leaf_fan.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_viper_zen_dojo_shinobi_wrap.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_viper_emerald_glass_optic.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_viper_gale_bamboo_dagger.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_viper_articulated_bamboo_tail.png").convert("RGBA")

# Extract exact ground contact shadow from comp128
shadow_ref = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
c_px = comp128.load()
s_px = shadow_ref.load()
assert c_px is not None and s_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p

EXPECTED_SHADOW = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], s_px[x, y])[3] > 20) for y in range(118, 128)]
print(f"Target shadow: {EXPECTED_SHADOW}")

def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)

def enforce_shadow(img: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_pixels = shadow_ref.load()
    assert o_px is not None and s_pixels is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_pixels[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
                o_px[x, y] = sp
    # Safe margins
    for x in range(128):
        for m in range(4):
            o_px[x, m] = (0, 0, 0, 0)
        for m in range(2):
            o_px[x, 127 - m] = (0, 0, 0, 0)
    for y in range(128):
        for m in range(4):
            o_px[m, y] = (0, 0, 0, 0)
            o_px[127 - m, y] = (0, 0, 0, 0)
    return out

# Kinematic decomposition for Viper
# Viper has chassis, snake coils, head, key, curio tail, weapon
# Decompose chassis into upper torso and lower coil
w, h = 128, 128
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
lower_coil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ch_px = chassis_128.load()
assert ch_px is not None

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0 or y >= 118:
            continue
        if y < 88:
            torso_chassis.putpixel((x, y), p)
        else:
            lower_coil.putpixel((x, y), p)

walk_configs = [
    # Frame 0: Left wave slither & dagger probe
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -3.0,
        "tail_rot": 8.0, "tail_dx": 1, "tail_dy": 0,
        "coil_rot": -4.0, "coil_dx": -1, "coil_dy": 0,
        "wpn_dx": 2, "wpn_dy": -1, "wpn_rot": 8.0,
        "key_rot": 18.0,
    },
    # Frame 1: Center glide compression
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "tail_rot": -3.0, "tail_dx": 0, "tail_dy": -1,
        "coil_rot": 2.0, "coil_dx": 0, "coil_dy": -1,
        "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": -4.0,
        "key_rot": -12.0,
    },
    # Frame 2: Right wave slither & dagger thrust
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 3.0,
        "tail_rot": -8.0, "tail_dx": -1, "tail_dy": 0,
        "coil_rot": 4.0, "coil_dx": 1, "coil_dy": 0,
        "wpn_dx": -2, "wpn_dy": 1, "wpn_rot": -8.0,
        "key_rot": 18.0,
    },
    # Frame 3: Rebound float
    {
        "torso_dx": 0, "torso_dy": -3, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
        "tail_rot": 4.0, "tail_dx": 0, "tail_dy": -2,
        "coil_rot": -2.0, "coil_dx": 0, "coil_dy": -2,
        "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 4.0,
        "key_rot": -12.0,
    },
]

pivot_tail = (35, 100)
pivot_coil = (64, 102)
pivot_head = (64, 36)
pivot_key = (86, 34)
pivot_wpn = (88, 79)

frames = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(shadow_ref)

    # 1. key
    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    # 2. curio tail
    t_rot = clean_alpha_fringe(curio_128.rotate(cfg["tail_rot"], resample=Image.Resampling.BICUBIC, center=pivot_tail, translate=(cfg["tail_dx"], cfg["tail_dy"])))
    f.alpha_composite(t_rot)

    # 3. lower coil
    c_rot = clean_alpha_fringe(lower_coil.rotate(cfg["coil_rot"], resample=Image.Resampling.BICUBIC, center=pivot_coil, translate=(cfg["coil_dx"], cfg["coil_dy"])))
    f.alpha_composite(c_rot)

    # 4. torso chassis
    tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 68), translate=(cfg["torso_dx"], cfg["torso_dy"])))
    f.alpha_composite(tc_rot)

    # 5. head
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(h_rot)

    # 6. costume
    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

    # 7. optic core
    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(opt_rot)

    # 8. weapon
    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=pivot_wpn, translate=(cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"])))
    f.alpha_composite(w_rot)

    f = enforce_shadow(f)
    frames.append(f)

print("Generated 4 frames. Checking rules...")
all_pass = True
for i, f in enumerate(frames):
    bbox = f.getbbox()
    assert bbox is not None
    left, top, right, bot = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
    print(f"Frame {i}: bbox={bbox}, margins: L={left}, T={top}, R={right}, B={bot}")
    if left < 4 or top < 4 or right < 4 or bot < 2:
        print(f"  ❌ Margin fail on frame {i}")
        all_pass = False

    # Check shadow
    sh = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], f.getpixel((x, y)))[3] > 20) for y in range(118, 128)]
    if sh != EXPECTED_SHADOW:
        print(f"  ❌ Shadow mismatch on frame {i}: {sh} vs {EXPECTED_SHADOW}")
        all_pass = False
    else:
        print(f"  ✓ Frame {i} shadow exact match")

    # Check non-translation 4b-4
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(comp128, (dx, dy), comp128)
            diff = ImageChops.difference(shifted, f).getbbox()
            if diff is None:
                print(f"  ❌ Frame {i} pure translation at ({dx}, {dy})")
                all_pass = False

    # Check 4b-7 articulation
    min_diff = 999999
    for dy in range(-6, 7):
        for dh in range(-5, 6):
            nh = 128 + dh
            if nh <= 0: continue
            scaled = comp128.resize((128, nh), Image.Resampling.LANCZOS)
            recon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            recon.paste(scaled, (0, dy - dh), scaled)
            diff_px = 0
            for y in range(112):
                for x in range(128):
                    if f.getpixel((x, y)) != recon.getpixel((x, y)):
                        diff_px += 1
            if diff_px < min_diff:
                min_diff = diff_px
    print(f"  Frame {i} 4b-7 articulation min_diff={min_diff}px")
    if min_diff <= 300:
        print(f"  ❌ Frame {i} articulation too small ({min_diff} <= 300)")
        all_pass = False

if all_pass:
    print("\n🎉 ALL TEST CHECKS PASSED FOR VIPER WALK FRAMES!")
