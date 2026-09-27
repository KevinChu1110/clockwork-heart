from typing import cast
import numpy as np
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"

chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_pangolin_dune_orange_default.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_pangolin_brass_acoustic_ears.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_pangolin_scavenger_tinker_vest.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/face_pangolin_sky_blue_optic_domes.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/weapon_pangolin_dune_drill_claw.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_pangolin_segmented_scale_tail.png").convert("RGBA")

w, h = 128, 128

# Canonical composite
comp128 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp128.alpha_composite(key_128)
comp128.alpha_composite(curio_128)
comp128.alpha_composite(chassis_128)
comp128.alpha_composite(head_128)
comp128.alpha_composite(costume_128)
comp128.alpha_composite(core_128)
comp128.alpha_composite(weapon_128)

def enforce_shadow_rows(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
    assert o_px is not None and s_px is not None
    for y in range(118, 128):
        for x in range(128):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
                if fp[3] <= 20:
                    o_px[x, y] = sp
    return out

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
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        if y >= 115 and p[3] < 180 and p[0] < 45 and p[1] < 40 and p[2] < 75:
            continue
        if y < 98:
            torso_chassis.putpixel((x, y), p)
        if y >= 88:
            if x <= 62:
                leg_l.putpixel((x, y), p)
            elif x >= 65:
                leg_r.putpixel((x, y), p)

pivot_l = (52, 94)
pivot_r = (75, 94)

# Test walk animation
walk_configs = [
    {"torso_dy": 0, "torso_dx": 0, "ll_rot": 10.0, "ll_dx": -2, "ll_dy": 0, "lr_rot": -10.0, "lr_dx": 2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 6.0, "curio_dy": 0, "curio_rot": 4.0},
    {"torso_dy": -2, "torso_dx": 0, "ll_rot": -2.0, "ll_dx": 0, "ll_dy": -1, "lr_rot": 14.0, "lr_dx": -1, "lr_dy": -3, "wpn_dy": -2, "wpn_dx": 1, "key_rot": -6.0, "curio_dy": -1, "curio_rot": -6.0},
    {"torso_dy": 0, "torso_dx": 0, "ll_rot": -10.0, "ll_dx": 2, "ll_dy": 0, "lr_rot": 10.0, "lr_dx": -2, "lr_dy": 0, "wpn_dy": 1, "wpn_dx": 0, "key_rot": 6.0, "curio_dy": 0, "curio_rot": 4.0},
    {"torso_dy": -2, "torso_dx": 0, "ll_rot": 14.0, "ll_dx": 1, "ll_dy": -3, "lr_rot": -2.0, "lr_dx": 0, "lr_dy": -1, "wpn_dy": -2, "wpn_dx": -1, "key_rot": -6.0, "curio_dy": -1, "curio_rot": -6.0},
]

walk_frames_128 = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    f.alpha_composite(clean_shadow)
    k_rot = key_128.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(83, 40))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)
    c_rot = curio_128.rotate(cfg["curio_rot"], resample=Image.Resampling.BICUBIC, center=(33, 94))
    f.paste(c_rot, (cfg["torso_dx"], cfg["torso_dy"] + cfg["curio_dy"]), c_rot)
    ll_t = leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"]))
    lr_t = leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"]))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)
    f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)
    f.paste(head_128, (cfg["torso_dx"], cfg["torso_dy"]), head_128)
    f.paste(core_128, (cfg["torso_dx"], cfg["torso_dy"]), core_128)
    f.paste(costume_128, (cfg["torso_dx"], cfg["torso_dy"]), costume_128)
    f.paste(weapon_128, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), weapon_128)

    f = enforce_shadow_rows(f, comp128)
    walk_frames_128.append(f)

print("Generated 4 walk frames successfully.")

# Verify Rule 4b-4 & 4b-7
base_idle = comp128
for i in range(4):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(base_idle, (dx, dy), base_idle)
            diff = ImageChops.difference(shifted, walk_frames_128[i]).getbbox()
            assert diff is not None, f"Frame {i} matches pure translation ({dx}, {dy})!"
    print(f"Frame {i}: passed Rule 4b-4 non-translation test.")

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
    print(f"Frame {i}: min_diff={min_diff} (Rule 4b-7 requirement: > 300px)")
    assert min_diff > 300, f"Frame {i} failed Rule 4b-7: {min_diff} <= 300"

# Verify Rule 4b-5
base_shadow = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], base_idle.getpixel((x, y)))[3] > 20) for y in range(118, 128)]
for i in range(4):
    f_shadow = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], walk_frames_128[i].getpixel((x, y)))[3] > 20) for y in range(118, 128)]
    assert f_shadow == base_shadow, f"Frame {i} shadow mismatch!"
print("Passed Rule 4b-5 shadow consistency.")

# Test Battle Sprite
b_torso_dx = 1
b_torso_dy = 2

ll_b = leg_l.rotate(-15.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-3, 1))
lr_b = leg_r.rotate(18.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(3, 1))

torso_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_b.paste(torso_chassis, (b_torso_dx, b_torso_dy), torso_chassis)

head_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
head_b.paste(head_128, (b_torso_dx + 1, b_torso_dy), head_128)

costume_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
costume_b.paste(costume_128, (b_torso_dx, b_torso_dy), costume_128)

core_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
core_b.paste(core_128, (b_torso_dx + 1, b_torso_dy), core_b)

key_b = key_128.rotate(22.0, resample=Image.Resampling.BICUBIC, center=(83, 40), translate=(b_torso_dx + 1, b_torso_dy - 1))
curio_b = curio_128.rotate(-14.0, resample=Image.Resampling.BICUBIC, center=(33, 94), translate=(b_torso_dx - 3, b_torso_dy + 1))
wpn_b = weapon_128.rotate(-20.0, resample=Image.Resampling.BICUBIC, center=(92, 78), translate=(b_torso_dx + 5, b_torso_dy - 4))

battle_sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
battle_sprite.alpha_composite(clean_shadow)
battle_sprite.alpha_composite(key_b)
battle_sprite.alpha_composite(curio_b)
battle_sprite.alpha_composite(ll_b)
battle_sprite.alpha_composite(lr_b)
battle_sprite.alpha_composite(torso_b)
battle_sprite.alpha_composite(head_b)
battle_sprite.alpha_composite(core_b)
battle_sprite.alpha_composite(costume_b)
battle_sprite.alpha_composite(wpn_b)

battle_sprite = enforce_shadow_rows(battle_sprite, comp128)

b_bbox = battle_sprite.getbbox()
assert b_bbox is not None
left_m = b_bbox[0]
right_m = 128 - b_bbox[2]
diff_b = ImageChops.difference(base_idle, battle_sprite)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_b.getpixel((x, y)))))
diff_legs = ImageChops.difference(base_idle.crop((0, 92, 128, 128)), battle_sprite.crop((0, 92, 128, 128)))
ch_legs = sum(1 for y in range(36) for x in range(128) if any(c > 0 for c in cast(tuple[int, int, int, int], diff_legs.getpixel((x, y)))))

print(f"Battle bbox: {b_bbox} (left_m={left_m}px, right_m={right_m}px)")
print(f"Battle vs idle diff: changed={ch_b}px ({ch_b / (128*128) * 100:.1f}%) [requirement: > 2500px]")
print(f"Battle legs diff (y>=92): changed={ch_legs}px [requirement: > 500px]")
assert left_m >= 4 and right_m >= 4, "Margin unclipped check failed"
assert ch_b > 2500, "Battle stance diff check failed"
assert ch_legs > 500, "Battle leg articulation check failed"
print("Battle sprite passed all Rule 4b-6 checks!")
