#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"

chassis = Image.open(f"{PD_DIR}/chassis/paint_tortoise_jade.png").convert("RGBA")
head = Image.open(f"{PD_DIR}/head_unit/head_xuanji_tortoise_stock.png").convert("RGBA")
key = Image.open(f"{PD_DIR}/winding_key/key_tai_chi_dual_fish.png").convert("RGBA")
costume = Image.open(f"{PD_DIR}/costume/costume_zen_dojo_harness.png").convert("RGBA")
core = Image.open(f"{PD_DIR}/optic_core/core_amber_quartz.png").convert("RGBA")
weapon = Image.open(f"{PD_DIR}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
curio = Image.open(f"{PD_DIR}/back_curio/curio_bagua_armillary_rings.png").convert("RGBA")

w, h = 128, 128

# Base composite
comp = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp.alpha_composite(key)
comp.alpha_composite(curio)
comp.alpha_composite(chassis)
comp.alpha_composite(head)
comp.alpha_composite(costume)
comp.alpha_composite(core)
comp.alpha_composite(weapon)

# Extract ground shadow (exact pixels where y >= 115 from chassis)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ch_px = chassis.load()
assert ch_px is not None
sh_px = shadow.load()
assert sh_px is not None

for y in range(112, 128):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] > 10 and p[0] < 30 and p[1] < 30 and p[2] < 30:
            sh_px[x, y] = p

expected_shadow = [sum(1 for x in range(128) if cast(tuple[int, int, int, int], ch_px[x, y])[3] > 20) for y in range(115, 128)]
print("Expected shadow counts (y=115..127):", expected_shadow)

# Decompose chassis
leg_l = Image.new("RGBA", (w, h), (0, 0, 0, 0))
leg_r = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_chassis = Image.new("RGBA", (w, h), (0, 0, 0, 0))

for y in range(h):
    for x in range(w):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        if y >= 115 and p[0] < 30 and p[1] < 30 and p[2] < 30:
            continue
        if y >= 96:
            if x <= 58:
                leg_l.putpixel((x, y), p)
            elif x >= 64:
                leg_r.putpixel((x, y), p)
            else:
                torso_chassis.putpixel((x, y), p)
        else:
            torso_chassis.putpixel((x, y), p)

pivot_l = (42, 98)
pivot_r = (82, 98)

# ─────────────────────────────────────────────────────────────
# 1. WALK CYCLE (4 FRAMES)
# ─────────────────────────────────────────────────────────────
walk_configs = [
    # Frame 0: Left stride forward, Right stride back, Torso neutral
    {
        "torso_dy": 0, "torso_dx": 0,
        "ll_rot": 10.0, "ll_dx": -2, "ll_dy": 0,
        "lr_rot": -10.0, "lr_dx": 2, "lr_dy": 0,
        "wpn_dy": 1, "wpn_dx": 0,
        "key_rot": 4.0, "curio_dy": 0,
    },
    # Frame 1: Up-bob, Left supporting, Right passing forward
    {
        "torso_dy": -2, "torso_dx": 0,
        "ll_rot": 0.0, "ll_dx": 0, "ll_dy": 0,
        "lr_rot": 14.0, "lr_dx": -1, "lr_dy": -3,
        "wpn_dy": -2, "wpn_dx": 1,
        "key_rot": -4.0, "curio_dy": -1,
    },
    # Frame 2: Right stride forward, Left stride back, Torso neutral
    {
        "torso_dy": 0, "torso_dx": 0,
        "ll_rot": -10.0, "ll_dx": 2, "ll_dy": 0,
        "lr_rot": 10.0, "lr_dx": -2, "lr_dy": 0,
        "wpn_dy": 1, "wpn_dx": 0,
        "key_rot": 4.0, "curio_dy": 0,
    },
    # Frame 3: Up-bob, Right supporting, Left passing forward
    {
        "torso_dy": -2, "torso_dx": 0,
        "ll_rot": 14.0, "ll_dx": 1, "ll_dy": -3,
        "lr_rot": 0.0, "lr_dx": 0, "lr_dy": 0,
        "wpn_dy": -2, "wpn_dx": -1,
        "key_rot": -4.0, "curio_dy": -1,
    },
]

walk_frames = []
for i, cfg in enumerate(walk_configs):
    f = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    # 1. Base shadow
    f.alpha_composite(shadow)
    
    # 2. Key & curio
    k_rot = key.rotate(cfg["key_rot"], resample=Image.Resampling.BICUBIC, center=(28, 28))
    f.paste(k_rot, (cfg["torso_dx"], cfg["torso_dy"]), k_rot)
    f.paste(curio, (cfg["torso_dx"], cfg["torso_dy"] + cfg["curio_dy"]), curio)
    
    # 3. Legs
    ll_t = leg_l.rotate(cfg["ll_rot"], resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(cfg["ll_dx"], cfg["ll_dy"]))
    lr_t = leg_r.rotate(cfg["lr_rot"], resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(cfg["lr_dx"], cfg["lr_dy"]))
    f.alpha_composite(ll_t)
    f.alpha_composite(lr_t)
    
    # 4. Torso chassis + head + costume + core
    f.paste(torso_chassis, (cfg["torso_dx"], cfg["torso_dy"]), torso_chassis)
    f.paste(head, (cfg["torso_dx"], cfg["torso_dy"]), head)
    f.paste(costume, (cfg["torso_dx"], cfg["torso_dy"]), costume)
    f.paste(core, (cfg["torso_dx"], cfg["torso_dy"]), core)
    
    # 5. Weapon
    f.paste(weapon, (cfg["torso_dx"] + cfg["wpn_dx"], cfg["torso_dy"] + cfg["wpn_dy"]), weapon)
    walk_frames.append(f)

# Verify Rule 4b-4: not pure translation
print("\n--- Verifying Walk Frames (Rule 4b-4) ---")
for i in range(4):
    for dx in range(-8, 9):
        for dy in range(-8, 9):
            shifted = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            shifted.paste(comp, (dx, dy), comp)
            diff = ImageChops.difference(shifted, walk_frames[i]).getbbox(alpha_only=False)
            assert diff is not None, f"FAIL: frame {i} matches pure translation ({dx}, {dy})!"
    print(f"✓ walk_{i} passed 4b-4: guaranteed not pure translation under any offset.")

# Verify Rule 4b-7: significant body diff vs whole-image resize+paste
print("\n--- Verifying Rule 4b-7 (Limb Articulation vs Whole-image Resize/Translate) ---")
for i in range(4):
    min_diff = 999999
    best_cfg = None
    for dy in range(-6, 7):
        for dh in range(-5, 6):
            nh = 128 + dh
            if nh <= 0:
                continue
            scaled = comp.resize((128, nh), Image.Resampling.LANCZOS)
            recon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
            recon.paste(scaled, (0, dy - dh), scaled)
            diff_px = 0
            for y in range(112):
                for x in range(128):
                    if walk_frames[i].getpixel((x, y)) != recon.getpixel((x, y)):
                        diff_px += 1
            if diff_px < min_diff:
                min_diff = diff_px
                best_cfg = (dy, dh)
    print(f"  Frame {i} best resize+paste diff in y<112: {min_diff} px (at dy={best_cfg[0] if best_cfg else 0}, dh={best_cfg[1] if best_cfg else 0})")
    assert min_diff > 300, f"FAIL: Frame {i} diff {min_diff} <= 300 px, resembles pure resize+paste!"
print("✓ Rule 4b-7 PASSED: All 4 walk frames have significant (>300px) body diff against whole-image resize+paste!")

# ─────────────────────────────────────────────────────────────
# 2. BATTLE SPRITE
# ─────────────────────────────────────────────────────────────
print("\n--- Crafting and Verifying Battle Sprite (Rule 4b-6) ---")
# Aggressive low-center-of-gravity warding / barrier-casting stance:
# Legs crouch and widen into solid tripod stance
ll_b = leg_l.rotate(14.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-4, 2))
lr_b = leg_r.rotate(-14.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(4, 2))

# Torso lowers by 2px into braced crouch
torso_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_b.paste(torso_chassis, (0, 2), torso_chassis)
head_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
head_b.paste(head, (1, 3), head) # slight forward tilt
costume_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
costume_b.paste(costume, (0, 2), costume)
core_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
core_b.paste(core, (0, 2), core)

# Key rotates +15 deg (dynamic tension)
key_b = key.rotate(15.0, resample=Image.Resampling.BICUBIC, center=(28, 28), translate=(-1, 1))
curio_b = curio.rotate(-10.0, resample=Image.Resampling.BICUBIC, center=(22, 78), translate=(0, 2))

# Astrolabe shield is brought up and forward into active warding guard position!
# Rotate -18 deg, shift forward-upward (-4, -3)
wpn_b = weapon.rotate(-18.0, resample=Image.Resampling.BICUBIC, center=(96, 62), translate=(-3, -2))

battle_sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
battle_sprite.alpha_composite(shadow)
battle_sprite.alpha_composite(key_b)
battle_sprite.alpha_composite(curio_b)
battle_sprite.alpha_composite(ll_b)
battle_sprite.alpha_composite(lr_b)
battle_sprite.alpha_composite(torso_b)
battle_sprite.alpha_composite(head_b)
battle_sprite.alpha_composite(costume_b)
battle_sprite.alpha_composite(core_b)
battle_sprite.alpha_composite(wpn_b)

b_bbox = battle_sprite.getbbox()
assert b_bbox is not None
print(f"Battle bbox: {b_bbox}, left_margin={b_bbox[0]}px, right_margin={128-b_bbox[2]}px")
assert b_bbox[0] >= 4, f"FAIL: left margin {b_bbox[0]} < 4px"
assert 128 - b_bbox[2] >= 4, f"FAIL: right margin {128 - b_bbox[2]} < 4px"

# Diff vs idle
diff_b = ImageChops.difference(comp, battle_sprite)
ch_b = sum(1 for y in range(128) for x in range(128) if any(c > 0 for c in diff_b.getpixel((x, y))))
pct_b = (ch_b / (128 * 128)) * 100
print(f"Battle vs idle diff: changed={ch_b} px ({pct_b:.1f}%), bbox={diff_b.getbbox()}")
assert ch_b > 2500, f"FAIL: changed pixels {ch_b} <= 2500 px"

# Leg region diff (y >= 96)
diff_legs = ImageChops.difference(comp.crop((0, 96, 128, 128)), battle_sprite.crop((0, 96, 128, 128)))
ch_legs = sum(1 for y in range(32) for x in range(128) if any(c > 0 for c in diff_legs.getpixel((x, y))))
print(f"Battle legs diff (y>=96): changed={ch_legs} px")
assert ch_legs > 500, f"FAIL: legs changed {ch_legs} <= 500 px"

print("\n✓ ALL KINEMATICS PASSED ALL TESTS!")
