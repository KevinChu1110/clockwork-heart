#!/usr/bin/env python3
"""
tune_walk_and_bust.py
Polished walk cycle kinematics and dialogue bust.
"""

from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/otter"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
PORTRAITS_DIR = f"{REPO_ROOT}/game/assets/sprites/portraits"

w, h = 128, 128

# Load slices
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_otter_abyssal_cyan_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_otter_diver_bell_visor.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_otter_nautical_rudder_helm.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_otter_deepsea_salvage_harness.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_otter_phosphor_green_gauges.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_otter_abyssal_anchor_cleaver.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_otter_articulated_rudder_tail.png").convert("RGBA")

# 512 slices
chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_otter_abyssal_cyan_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_otter_diver_bell_visor_512.png").convert("RGBA")
key_512 = Image.open(f"{PD_DIR}/winding_key/key_otter_nautical_rudder_helm_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_otter_deepsea_salvage_harness_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_otter_phosphor_green_gauges_512.png").convert("RGBA")
weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_otter_abyssal_anchor_cleaver_512.png").convert("RGBA")
curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_otter_articulated_rudder_tail_512.png").convert("RGBA")

comp128 = Image.open(f"{PD_DIR}/proof_paperdoll_otter_composite.png").convert("RGBA")
comp512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp512.alpha_composite(key_512)
comp512.alpha_composite(curio_512)
comp512.alpha_composite(chassis_512)
comp512.alpha_composite(head_512)
comp512.alpha_composite(costume_512)
comp512.alpha_composite(core_512)
comp512.alpha_composite(weapon_512)

# Standardized ground contact shadow from comp128
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cs_px = clean_shadow.load()
c_px = comp128.load()
assert cs_px is not None and c_px is not None
for y in range(118, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            cs_px[x, y] = p

clean_shadow_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
cs512_px = clean_shadow_512.load()
c512_px = comp512.load()
assert cs512_px is not None and c512_px is not None
for y in range(118 * 4, 128 * 4):
    for x in range(512):
        p = cast(tuple[int, int, int, int], c512_px[x, y])
        if p[3] > 20:
            cs512_px[x, y] = p

def enforce_shadow_rows(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
    assert o_px is not None and s_px is not None

    # Clear y=117 so boot rims never spill into or distort the shadow zone
    for x in range(128):
        o_px[x, 117] = (0, 0, 0, 0)

    # Shadow rows 118..127 unconditionally matched to baseline (100% stable ellipse)
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
                o_px[x, y] = sp

    # Clean margins strictly (L>=4, R>=4, T>=4, B>=2)
    for x in range(128):
        o_px[x, 0] = (0, 0, 0, 0)
        o_px[x, 1] = (0, 0, 0, 0)
        o_px[x, 2] = (0, 0, 0, 0)
        o_px[x, 3] = (0, 0, 0, 0)
        o_px[x, 126] = (0, 0, 0, 0)
        o_px[x, 127] = (0, 0, 0, 0)
    for y in range(128):
        o_px[0, y] = (0, 0, 0, 0)
        o_px[1, y] = (0, 0, 0, 0)
        o_px[2, y] = (0, 0, 0, 0)
        o_px[3, y] = (0, 0, 0, 0)
        o_px[124, y] = (0, 0, 0, 0)
        o_px[125, y] = (0, 0, 0, 0)
        o_px[126, y] = (0, 0, 0, 0)
        o_px[127, y] = (0, 0, 0, 0)
    return out

def enforce_shadow_rows_512(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
    assert o_px is not None and s_px is not None

    for y in range(117 * 4, 118 * 4):
        for x in range(512):
            o_px[x, y] = (0, 0, 0, 0)

    for y in range(118 * 4, 128 * 4):
        for x in range(512):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            if sp[3] <= 20:
                o_px[x, y] = (0, 0, 0, 0)
            else:
                o_px[x, y] = sp

    for x in range(512):
        for m in range(16):
            o_px[x, m] = (0, 0, 0, 0)
            o_px[x, 511 - m] = (0, 0, 0, 0)
    for y in range(512):
        for m in range(16):
            o_px[m, y] = (0, 0, 0, 0)
            o_px[511 - m, y] = (0, 0, 0, 0)
    return out

# Kinematics Decomposition: legs contain proper dark outline on bottom sole
ch_px = chassis_128.load()
assert ch_px is not None

leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis = Image.new("RGBA", (w, h), (0, 0, 0, 0))
pelvis_backing = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

CYAN_BASE = (56, 160, 255, 255)
CYAN_DARK = (24, 105, 195, 255)
OUTLINE = (31, 26, 58, 255)

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        if y >= 117:
            continue
        if y < 98:
            torso_chassis.putpixel((x, y), p)
        if 88 <= y <= 106:
            pelvis.putpixel((x, y), p)
        # Legs: y <= 116
        if 90 <= y <= 116:
            if x <= 58:
                leg_l.putpixel((x, y), p)
            elif x >= 60:
                leg_r.putpixel((x, y), p)

# Ensure proper bottom outline on soles (y=116) so lifted boots never have a white raw edge
for x in range(40, 58):
    px = cast(tuple[int, int, int, int], leg_l.getpixel((x, 115)))
    if px[3] > 100:
        leg_l.putpixel((x, 116), OUTLINE)
for x in range(60, 78):
    px = cast(tuple[int, int, int, int], leg_r.getpixel((x, 115)))
    if px[3] > 100:
        leg_r.putpixel((x, 116), OUTLINE)

# Solid pelvis backing under legs prevents any gap
pb_draw = ImageDraw.Draw(pelvis_backing)
pb_draw.rectangle([46, 90, 72, 104], fill=CYAN_DARK)
pb_draw.rectangle([48, 92, 70, 102], fill=CYAN_BASE)

pivot_l = (49, 94)
pivot_r = (69, 94)

# 512 Kinematics
ch512_px = chassis_512.load()
assert ch512_px is not None

leg_l_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
leg_r_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
pelvis_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
pelvis_backing_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
torso_chassis_512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))

for y in range(512):
    for x in range(512):
        p = cast(tuple[int, int, int, int], ch512_px[x, y])
        if p[3] == 0:
            continue
        if y >= 117 * 4:
            continue
        if y < 98 * 4:
            torso_chassis_512.putpixel((x, y), p)
        if 88 * 4 <= y <= 106 * 4:
            pelvis_512.putpixel((x, y), p)
        if 90 * 4 <= y <= 116 * 4:
            if x <= 58 * 4:
                leg_l_512.putpixel((x, y), p)
            elif x >= 60 * 4:
                leg_r_512.putpixel((x, y), p)

for y_sub in range(115 * 4 + 2, 116 * 4):
    for x in range(40 * 4, 58 * 4):
        px = cast(tuple[int, int, int, int], leg_l_512.getpixel((x, 115 * 4)))
        if px[3] > 100:
            leg_l_512.putpixel((x, y_sub), OUTLINE)
    for x in range(60 * 4, 78 * 4):
        px = cast(tuple[int, int, int, int], leg_r_512.getpixel((x, 115 * 4)))
        if px[3] > 100:
            leg_r_512.putpixel((x, y_sub), OUTLINE)

pb512_draw = ImageDraw.Draw(pelvis_backing_512)
pb512_draw.rectangle([46 * 4, 90 * 4, 72 * 4, 104 * 4], fill=CYAN_DARK)
pb512_draw.rectangle([48 * 4, 92 * 4, 70 * 4, 102 * 4], fill=CYAN_BASE)

pivot_l_512 = (49 * 4, 94 * 4)
pivot_r_512 = (69 * 4, 94 * 4)

def clean_alpha_fringe(img: Image.Image, threshold: int = 50) -> Image.Image:
    arr = np.array(img)
    arr[arr[:, :, 3] < threshold, :] = 0
    return Image.fromarray(arr)

# Refined walk gait:
# Organic, cute chibi waddle with distinct head tilt, torso rise/bounce, key rotation, and cleaver sway
walk_configs = [
    # Frame 0: Left stride forward, right back, body sways slightly left
    {
        "torso_dx": -1, "torso_dy": 0, "head_dx": -1, "head_dy": 0, "head_rot": -3.0,
        "ll_rot": 8.0, "ll_dx": -1, "ll_dy": 0,
        "lr_rot": -8.0, "lr_dx": 1, "lr_dy": 0,
        "wpn_dx": 1, "wpn_dy": 0, "wpn_rot": 6.0,
        "key_rot": 15.0, "curio_dx": -1, "curio_dy": 0, "curio_rot": 6.0
    },
    # Frame 1: Upward rise/bounce (-3px)! Right foot passing forward in the air
    {
        "torso_dx": 0, "torso_dy": -3, "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0,
        "lr_rot": 4.0, "lr_dx": 0, "lr_dy": -3,
        "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": -3.0,
        "key_rot": -10.0, "curio_dx": 0, "curio_dy": -3, "curio_rot": -5.0
    },
    # Frame 2: Right stride forward, left back, body sways slightly right
    {
        "torso_dx": 1, "torso_dy": 0, "head_dx": 1, "head_dy": 0, "head_rot": 3.0,
        "ll_rot": -8.0, "ll_dx": 1, "ll_dy": 0,
        "lr_rot": 8.0, "lr_dx": -1, "lr_dy": 0,
        "wpn_dx": -1, "wpn_dy": 0, "wpn_rot": -6.0,
        "key_rot": 15.0, "curio_dx": 1, "curio_dy": 0, "curio_rot": -6.0
    },
    # Frame 3: Upward rise/bounce (-3px)! Left foot passing forward in the air
    {
        "torso_dx": 0, "torso_dy": -3, "head_dx": 0, "head_dy": -3, "head_rot": 0.0,
        "ll_rot": 4.0, "ll_dx": 0, "ll_dy": -3,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0,
        "wpn_dx": 0, "wpn_dy": -3, "wpn_rot": 3.0,
        "key_rot": -10.0, "curio_dx": 0, "curio_dy": -3, "curio_rot": 5.0
    },
]

walk_frames_128 = []
walk_frames_512 = []

for i, cfg in enumerate(walk_configs):
    # 128 Frame
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)

    k_rot = clean_alpha_fringe(key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(83, 36)))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)

    c_rot = clean_alpha_fringe(curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(35, 88)))
    f.paste(c_rot, (cfg["torso_dx"] + cfg["curio_dx"], cfg["torso_dy"] + cfg["curio_dy"]), c_rot)

    # Pelvis backing under legs prevents any gap
    f.paste(pelvis_backing, (cfg["torso_dx"], cfg["torso_dy"]), pelvis_backing)

    # Legs rotate
    ll_t = clean_alpha_fringe(leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"])))
    lr_t = clean_alpha_fringe(leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"])))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)

    # Pelvis patch covers seam between torso and legs
    f.paste(pelvis, (cfg["torso_dx"], cfg["torso_dy"]), pelvis)
    f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)

    # Head + Optic with subtle rotation & bounce
    h_rot = clean_alpha_fringe(head_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(64, 42)))
    f.paste(h_rot, (cfg["head_dx"], cfg["head_dy"]), h_rot)

    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)

    opt_rot = clean_alpha_fringe(core_128.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(64, 42)))
    f.paste(opt_rot, (cfg["head_dx"], cfg["head_dy"]), opt_rot)

    # Weapon with rotation
    w_rot = clean_alpha_fringe(weapon_128.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=(97, 75)))
    f.paste(w_rot, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), w_rot)

    f = enforce_shadow_rows(f, comp128)
    walk_frames_128.append(f)

    f.save(f"{PLAYER_DIR}/otter_walk_{i}_x3.png")
    f64 = f.resize((64, 64), Image.Resampling.LANCZOS)
    f64.save(f"{PLAYER_DIR}/otter_walk_{i}.png")

    # 512 Frame
    f512 = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
    f512.alpha_composite(clean_shadow_512)

    k_rot_512 = clean_alpha_fringe(key_512.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(83 * 4, 36 * 4)))
    f512.paste(k_rot_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), k_rot_512)

    c_rot_512 = clean_alpha_fringe(curio_512.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(35 * 4, 88 * 4)))
    f512.paste(c_rot_512, ((cfg["torso_dx"] + cfg["curio_dx"]) * 4, (cfg["torso_dy"] + cfg["curio_dy"]) * 4), c_rot_512)

    f512.paste(pelvis_backing_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), pelvis_backing_512)

    ll_t_512 = clean_alpha_fringe(leg_l_512.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l_512, translate=(cfg["ll_dx"] * 4, cfg["ll_dy"] * 4)))
    lr_t_512 = clean_alpha_fringe(leg_r_512.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r_512, translate=(cfg["lr_dx"] * 4, cfg["lr_dy"] * 4)))
    f512.alpha_composite(ll_t_512)
    f512.alpha_composite(lr_t_512)

    f512.paste(pelvis_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), pelvis_512)
    f512.paste(torso_chassis_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), torso_chassis_512)

    h_rot_512 = clean_alpha_fringe(head_512.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(64 * 4, 42 * 4)))
    f512.paste(h_rot_512, (cfg["head_dx"] * 4, cfg["head_dy"] * 4), h_rot_512)

    f512.paste(costume_512, (cfg["torso_dx"] * 4, cfg["torso_dy"] * 4), costume_512)

    opt_rot_512 = clean_alpha_fringe(core_512.rotate(cfg["head_rot"], resample=Image.Resampling.BICUBIC, center=(64 * 4, 42 * 4)))
    f512.paste(opt_rot_512, (cfg["head_dx"] * 4, cfg["head_dy"] * 4), opt_rot_512)

    w_rot_512 = clean_alpha_fringe(weapon_512.rotate(cfg["wpn_rot"], resample=Image.Resampling.BICUBIC, center=(97 * 4, 75 * 4)))
    f512.paste(w_rot_512, ((cfg["torso_dx"] + cfg["wpn_dx"]) * 4, (cfg["torso_dy"] + cfg["wpn_dy"]) * 4), w_rot_512)

    f512 = enforce_shadow_rows_512(f512, comp512)
    walk_frames_512.append(f512)
    f512.save(f"{PLAYER_DIR}/otter_walk_{i}_512.png")

# Proof walk cycle strip
strip = Image.new("RGBA", (128 * 4, 128), (0, 0, 0, 0))
for i, fr in enumerate(walk_frames_128):
    strip.alpha_composite(fr, (i * 128, 0))
strip.save(f"{PLAYER_DIR}/proof_otter_walk_cycle.png")
print("✓ Saved Perfectly Clean Walk Frames and proof_otter_walk_cycle.png")
