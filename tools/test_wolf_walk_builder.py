import os
from typing import cast
from PIL import Image, ImageDraw, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"

ORANGE_BASE = (248, 156, 35, 255)
ORANGE_DARK = (204, 128, 12, 255)
OUTLINE = (31, 26, 58, 255)

def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)

def enforce_shadow_rows(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
    assert o_px is not None and s_px is not None

    for x in range(128):
        o_px[x, 117] = (0, 0, 0, 0)

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
    return out

# Load 128 slices
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_wolf_warm_orange_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_wolf_gear_mane_cowl.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_wolf_heavy_pojun_cross.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_wolf_scavenger_scrap_plate_armor.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_wolf_twin_blue_optic_lens.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_wolf_scrap_sawblade_greatsword.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_wolf_segmented_spring_tail.png").convert("RGBA")

w, h = 128, 128

comp128 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp128.alpha_composite(key_128)
comp128.alpha_composite(curio_128)
comp128.alpha_composite(chassis_128)
comp128.alpha_composite(head_128)
comp128.alpha_composite(costume_128)
comp128.alpha_composite(core_128)
comp128.alpha_composite(weapon_128)

clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cs_px = clean_shadow.load()
c_px = comp128.load()
assert cs_px is not None and c_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            cs_px[x, y] = p

ch_px = chassis_128.load()
assert ch_px is not None

leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis_backing = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        if y >= 117:
            continue
        if y < 96:
            torso_chassis.putpixel((x, y), p)
        if 88 <= y <= 104:
            pelvis.putpixel((x, y), p)
        if 90 <= y <= 116:
            if x <= 58:
                leg_l.putpixel((x, y), p)
            elif x >= 60:
                leg_r.putpixel((x, y), p)

for x in range(36, 58):
    px = cast(tuple[int, int, int, int], leg_l.getpixel((x, 115)))
    if px[3] > 100:
        leg_l.putpixel((x, 116), OUTLINE)
for x in range(60, 92):
    px = cast(tuple[int, int, int, int], leg_r.getpixel((x, 115)))
    if px[3] > 100:
        leg_r.putpixel((x, 116), OUTLINE)

pb_draw = ImageDraw.Draw(pelvis_backing)
pb_draw.rectangle([46, 90, 72, 104], fill=ORANGE_DARK)
pb_draw.rectangle([48, 92, 70, 102], fill=ORANGE_BASE)

pivot_l = (48, 95)
pivot_r = (68, 95)

walk_configs = [
    {"torso_dx": -1, "torso_dy": 0, "head_dx": -1, "head_dy": 0, "head_rot": -3.0, "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0, "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0, "wpn_dx": 1, "wpn_dy": 0, "wpn_rot": 6.0, "key_rot": 15.0, "curio_dx": -1, "curio_dy": 0, "curio_rot": 6.0},
    {"torso_dx": 0, "torso_dy": -3, "head_dx": 0, "head_dy": -3, "head_rot": 0.0, "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0, "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -3, "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": -3.0, "key_rot": -10.0, "curio_dx": 0, "curio_dy": -3, "curio_rot": -5.0},
    {"torso_dx": 1, "torso_dy": 0, "head_dx": 1, "head_dy": 0, "head_rot": 3.0, "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0, "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0, "wpn_dx": -1, "wpn_dy": 0, "wpn_rot": -6.0, "key_rot": 15.0, "curio_dx": 1, "curio_dy": 0, "curio_rot": -6.0},
    {"torso_dx": 0, "torso_dy": -3, "head_dx": 0, "head_dy": -3, "head_rot": 0.0, "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -3, "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0, "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 3.0, "key_rot": -10.0, "curio_dx": 0, "curio_dy": -3, "curio_rot": 5.0},
]

walk_frames_128 = []

for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(84, 33)))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(30, 80)))
    f.paste(c_rot, (cfg["torso_dx"] + cfg["curio_dx"], cfg["torso_dy"] + cfg["curio_dy"]), c_rot)

    f.paste(pelvis_backing, (cfg["torso_dx"], cfg["torso_dy"]), pelvis_backing)

    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)
    f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)

    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(64, 45)))
    f.paste(h_rot, (cfg["head_dx"], cfg["head_dy"]), h_rot)

    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(64, 45)))
    f.paste(opt_rot, (cfg["head_dx"], cfg["head_dy"]), opt_rot)

    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=(94, 86)))
    f.paste(w_rot, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), w_rot)

    f = enforce_shadow_rows(f, comp128)
    walk_frames_128.append(f)

# Test 4b-4 and 4b-7
base_idle = comp128
for i, fr in enumerate(walk_frames_128):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(base_idle, (dx, dy), base_idle)
            diff = ImageChops.difference(shifted, fr).getbbox()
            if diff is None:
                print(f"FAILED 4b-4: frame {i} is pure translation ({dx}, {dy})")

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
    print(f"Frame {i}: articulation min_diff = {min_diff}px (>300)")

    # Shadow check
    f_arr = np.array(fr)
    f_shadow = [int(np.sum(f_arr[y, :, 3] > 20)) for y in range(118, 128)]
    base_shadow = [int(np.sum(np.array(base_idle)[y, :, 3] > 20)) for y in range(118, 128)]
    print(f"Frame {i}: shadow match = {f_shadow == base_shadow} ({f_shadow})")
