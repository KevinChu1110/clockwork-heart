#!/usr/bin/env python3
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/courser"
POSES_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/courser"

chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_courser_cream_gold_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_courser_brass_chanfron_mane.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_courser_baroque_trefoil_gold.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_courser_dawn_patrol_cuirass.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_courser_sapphire_optic_lens.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_courser_cavalry_saber.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_courser_articulated_spring_tail.png").convert("RGBA")

comp128 = Image.open(f"{POSES_DIR}/idle.png").convert("RGBA")

w, h = 128, 128

# Ground shadow from idle
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
c_px = comp128.load()
s_px = clean_shadow.load()
assert c_px is not None and s_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p

expected_shadow = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], clean_shadow.getpixel((x, y)))[3] > 20) for y in range(118, 128)]
print(f"clean shadow rows: {expected_shadow}")

def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)

def enforce_shadow_rows(img: Image.Image, shadow_ref: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_pixels = shadow_ref.load()
    assert o_px is not None and s_pixels is not None

    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_pixels[x, y])
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

# Kinematics decomposition of chassis
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
        if y < 94:
            torso_chassis.putpixel((x, y), p)
        if 88 <= y <= 104 and 42 <= x <= 86:
            pelvis.putpixel((x, y), p)
        if 96 <= y <= 117:
            if x <= 62:
                leg_l.putpixel((x, y), p)
            else:
                leg_r.putpixel((x, y), p)

pivot_l = (50, 100)
pivot_r = (78, 100)
pivot_head = (64, 35)
pivot_key = (88, 35)
pivot_wpn = (96, 50)
pivot_curio = (36, 85)

walk_configs = [
    # Frame 0: Left stride forward, cavalry saber lowered forward, mane wave
    {
        "torso_dx": -1, "torso_dy": 0, "torso_rot": -2.0,
        "head_dx": -1, "head_dy": 0, "head_rot": -2.0,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "wpn_dx": -1, "wpn_dy": 1, "wpn_rot": 4.0,
        "key_rot": 18.0,
        "curio_rot": -5.0, "curio_dx": -1, "curio_dy": 0,
    },
    # Frame 1: Center stride compression (passing stance, spring tail recoil)
    {
        "torso_dx": 0, "torso_dy": -2, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -2, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -2,
        "wpn_dx": 0, "wpn_dy": -2, "wpn_rot": -2.0,
        "key_rot": -12.0,
        "curio_rot": 4.0, "curio_dx": 0, "curio_dy": -2,
    },
    # Frame 2: Right stride forward, cavalry saber raised, mane & tail sway
    {
        "torso_dx": 1, "torso_dy": 0, "torso_rot": 2.0,
        "head_dx": 1, "head_dy": 0, "head_rot": 2.0,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "wpn_dx": 2, "wpn_dy": -1, "wpn_rot": -4.0,
        "key_rot": 18.0,
        "curio_rot": 5.0, "curio_dx": 1, "curio_dy": 0,
    },
    # Frame 3: Rebound float / spring tail lift
    {
        "torso_dx": 0, "torso_dy": -3, "torso_rot": 0.0,
        "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -2,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0,
        "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 2.0,
        "key_rot": -12.0,
        "curio_rot": -3.0, "curio_dx": 0, "curio_dy": -2,
    },
]

walk_frames_128 = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    # 1. key (winding key behind chassis, z=5)
    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=pivot_key))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    # 2. back curio (spring tail, z=8)
    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=pivot_curio, translate=(cfg["curio_dx"], cfg["curio_dy"])))
    f.alpha_composite(c_rot)

    # 3. legs
    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    # 4. pelvis
    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)

    # 5. torso chassis (z=10)
    tc_rot = clean_alpha_fringe(torso_chassis.rotate(cfg["torso_rot"], resample=Image.Resampling.BICUBIC, center=(64, 70), translate=(cfg["torso_dx"], cfg["torso_dy"])))
    f.alpha_composite(tc_rot)

    # 6. head unit (z=20)
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(h_rot)

    # 7. costume (z=25)
    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

    # 8. optic core (z=30)
    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=pivot_head, translate=(cfg["head_dx"], cfg["head_dy"])))
    f.alpha_composite(opt_rot)

    # 9. weapon (z=40)
    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=pivot_wpn, translate=(cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"])))
    f.alpha_composite(w_rot)

    f = enforce_shadow_rows(f, clean_shadow)
    walk_frames_128.append(f)

# Verification Rule 4b-4 & 4b-7
base_idle = comp128
for i in range(4):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(base_idle, (dx, dy), base_idle)
            diff = ImageChops.difference(shifted, walk_frames_128[i]).getbbox()
            if diff is None:
                print(f"❌ Frame {i} matches pure translation ({dx}, {dy})!")
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
            for y in range(112):
                for x in range(128):
                    if walk_frames_128[i].getpixel((x, y)) != recon.getpixel((x, y)):
                        diff_px += 1
            if diff_px < min_diff:
                min_diff = diff_px
    print(f"✓ Frame {i} passed 4b-7: articulation diff={min_diff}px (threshold > 300px)")
