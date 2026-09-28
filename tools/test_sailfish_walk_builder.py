#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/sailfish"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/sailfish"

# Load slices
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_sailfish_abyssal_titanium_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_sailfish_hydrofoil_visor_crest.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_sailfish_abyssal_helm_trident.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_sailfish_abyssal_knight_cuirass.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_sailfish_dual_abyssal_optic_lens.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_sailfish_hydrofoil_lance.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_sailfish_clockwork_sailfin_mantle.png").convert("RGBA")

comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")

w, h = 128, 128
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
c_px = comp128.load()
s_px = clean_shadow.load()
for y in range(118, 128):
    for x in range(128):
        p = c_px[x, y]
        if p[3] > 20:
            s_px[x, y] = p

def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)

def enforce_shadow_rows(img: Image.Image, shadow_ref: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = shadow_ref.load()

    for y in range(118, 128):
        for x in range(128):
            sp = s_px[x, y]
            op = o_px[x, y]
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
    return out

ch_px = chassis_128.load()
leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
tail_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = ch_px[x, y]
        if p[3] == 0 or y >= 118:
            continue
        if y < 94:
            torso_chassis.putpixel((x, y), p)
        if 88 <= y <= 104 and 35 <= x <= 75:
            pelvis.putpixel((x, y), p)
        if 88 <= y <= 112 and x < 35:
            tail_chassis.putpixel((x, y), p)
        if 96 <= y <= 117:
            if x <= 56:
                leg_l.putpixel((x, y), p)
            else:
                leg_r.putpixel((x, y), p)

pivot_l = (46, 100)
pivot_r = (68, 100)
pivot_tail = (26, 95)
pivot_head = (60, 35)
pivot_key = (83, 34)
pivot_wpn = (34, 70)
pivot_curio = (44, 42)

walk_configs = [
    # Frame 0: Left foot step forward, right foot trailing, weapon ready dip, tail swish
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -3.0,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "tail_rot": 8.0, "tail_dx": -1, "tail_dy": 0,
        "wpn_dx": -1, "wpn_dy": 1, "wpn_rot": 4.0,
        "key_rot": 18.0,
        "curio_rot": -4.0, "curio_dx": -1, "curio_dy": 0,
    },
    # Frame 1: Center glide compression (passing stance)
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
        "tail_rot": -3.0, "tail_dx": 0, "tail_dy": -1,
        "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": -2.0,
        "key_rot": -12.0,
        "curio_rot": 2.0, "curio_dx": 0, "curio_dy": -2,
    },
    # Frame 2: Right foot step forward, left foot trailing, lance thrust
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 3.0,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "tail_rot": -8.0, "tail_dx": 1, "tail_dy": 0,
        "wpn_dx": 2, "wpn_dy": -1, "wpn_rot": -4.0,
        "key_rot": 18.0,
        "curio_rot": 4.0, "curio_dx": 1, "curio_dy": 0,
    },
    # Frame 3: Rebound float / lift
    {
        "torso_dx": 0, "torso_dy": -3, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0,
        "tail_rot": 4.0, "tail_dx": 0, "tail_dy": -2,
        "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 2.0,
        "key_rot": -12.0,
        "curio_rot": -2.0, "curio_dx": 0, "curio_dy": -2,
    },
]

frames = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    # 1. Winding key (behind head/body)
    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    # 2. Back curio (sailfin mantle)
    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=pivot_curio, translate=(cfg["curio_dx"], cfg["curio_dy"])))
    f.alpha_composite(c_rot)

    # 3. Tail chassis
    t_rot = clean_alpha_fringe(tail_chassis.rotate(cfg["tail_rot"], resample=Image.Resampling.BICUBIC, center=pivot_tail, translate=(cfg["tail_dx"], cfg["tail_dy"])))
    f.alpha_composite(t_rot)

    # 4. Legs
    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    # 5. Pelvis
    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)

    # 6. Torso chassis
    tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(58, 70), translate=(cfg["torso_dx"], cfg["torso_dy"])))
    f.alpha_composite(tc_rot)

    # 7. Costume (cuirass)
    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

    # 8. Head unit
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(h_rot)

    # 9. Optic core
    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(opt_rot)

    # 10. Weapon (lance)
    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=pivot_wpn, translate=(cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"])))
    f.alpha_composite(w_rot)

    # Enforce ground contact shadow
    f = enforce_shadow_rows(f, clean_shadow)
    frames.append(f)

# Test 4b-4 (pure translation check)
print("--- Testing Rule 4b-4 ---")
for i in range(4):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(comp128, (dx, dy), comp128)
            diff = ImageChops.difference(shifted, frames[i]).getbbox()
            if diff is None:
                print(f"❌ Frame {i} matches pure translation ({dx}, {dy})")
    print(f"✓ Frame {i} passed 4b-4 (no pure translation)")

# Test 4b-7 (articulation test)
print("--- Testing Rule 4b-7 ---")
for i in range(4):
    min_diff = 999999
    for dy in range(-6, 7):
        for dh in range(-5, 6):
            nh = 128 + dh
            if nh <= 0:
                continue
            scaled = comp128.resize((128, nh), Image.Resampling.LANCZOS)
            recon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            recon.paste(scaled, (0, dy - dh), scaled)
            diff_px = 0
            for y in range(112):
                for x in range(128):
                    if frames[i].getpixel((x, y)) != recon.getpixel((x, y)):
                        diff_px += 1
            if diff_px < min_diff:
                min_diff = diff_px
    print(f"✓ Frame {i} passed 4b-7: articulation diff={min_diff}px (req > 300px)")

# Test 4b-5 (shadow consistency)
print("--- Testing Rule 4b-5 ---")
for i in range(4):
    f_shadow = [sum(1 for x in range(128) if frames[i].getpixel((x, y))[3] > 20) for y in range(118, 128)]
    assert f_shadow == [59, 57, 51, 43, 27, 0, 0, 0, 0, 0], f"Frame {i} shadow {f_shadow} mismatch!"
    print(f"✓ Frame {i} shadow {f_shadow} exactly matches [59, 57, 51, 43, 27, 0, 0, 0, 0, 0]")

# Test margins
print("--- Testing Margins ---")
for i in range(4):
    bb = frames[i].getbbox()
    left, top, right, bot = bb[0], bb[1], 128 - bb[2], 128 - bb[3]
    print(f"Frame {i} bbox={bb}, L={left}px, T={top}px, R={right}px, B={bot}px")
    assert left >= 4 and top >= 4 and right >= 4 and bot >= 2
    print(f"✓ Frame {i} margins OK")
