#!/usr/bin/env python3
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/tortoise"

chassis_128 = Image.open(f"{PD_DIR}/chassis/paint_tortoise_jade.png").convert("RGBA")
head_128 = Image.open(f"{PD_DIR}/head_unit/head_xuanji_tortoise_stock.png").convert("RGBA")
key_128 = Image.open(f"{PD_DIR}/winding_key/key_tai_chi_dual_fish.png").convert("RGBA")
costume_128 = Image.open(f"{PD_DIR}/costume/costume_zen_dojo_harness.png").convert("RGBA")
core_128 = Image.open(f"{PD_DIR}/optic_core/core_amber_quartz.png").convert("RGBA")
weapon_128 = Image.open(f"{PD_DIR}/weapon/wpn_bagua_astrolabe.png").convert("RGBA")
curio_128 = Image.open(f"{PD_DIR}/back_curio/curio_bagua_armillary_rings.png").convert("RGBA")

w, h = 128, 128

# Canonical 128x128 composite in Z-order
comp128 = Image.new("RGBA", (w, h), (0, 0, 0, 0))
comp128.alpha_composite(key_128)
comp128.alpha_composite(curio_128)
comp128.alpha_composite(chassis_128)
comp128.alpha_composite(head_128)
comp128.alpha_composite(costume_128)
comp128.alpha_composite(core_128)
comp128.alpha_composite(weapon_128)

# 1. Build pure ground contact shadow exactly as drawn in build_tortoise_canonical_clean.py
clean_shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
cs_d = ImageDraw.Draw(clean_shadow)
cs_d.ellipse([64 - 34, 114 - 4, 64 + 34, 114 + 4], fill=(31, 26, 58, 125))
clean_shadow = clean_shadow.filter(ImageFilter.GaussianBlur(1.4))

# Measure clean_shadow row counts at y in 115..127
base_shadow_counts = [sum(1 for x in range(128) if comp128.getpixel((x, y))[3] > 20) for y in range(115, 128)]
print("Comp128 shadow counts (115..127):", base_shadow_counts)

# Decompose chassis into legs and torso (excluding the ground shadow)
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
        # Pure shadow pixels are dark purple translucent
        # Claws are steel dark (55, 62, 75) or steel light (170, 185, 205) or outline (31, 26, 58, 255)
        if p[3] < 150 and p[0] < 35 and p[1] < 30 and p[2] < 65:
            # Pure soft shadow
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

# 2. Build Battle Sprite
ll_b = leg_l.rotate(14.0, resample=Image.Resampling.BICUBIC, center=pivot_l, translate=(-4, 1))
lr_b = leg_r.rotate(-14.0, resample=Image.Resampling.BICUBIC, center=pivot_r, translate=(4, 1))
torso_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
torso_b.paste(torso_chassis, (0, 2), torso_chassis)
head_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
head_b.paste(head_128, (1, 3), head_128)
costume_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
costume_b.paste(costume_128, (0, 2), costume_128)
core_b = Image.new("RGBA", (w, h), (0, 0, 0, 0))
core_b.paste(core_128, (0, 2), core_128)
key_b = key_128.rotate(15.0, resample=Image.Resampling.BICUBIC, center=(28, 28), translate=(-1, 1))
curio_b = curio_128.rotate(-10.0, resample=Image.Resampling.BICUBIC, center=(22, 78), translate=(0, 2))
wpn_b = weapon_128.rotate(-18.0, resample=Image.Resampling.BICUBIC, center=(96, 62), translate=(-3, -2))

battle_sprite = Image.new("RGBA", (w, h), (0, 0, 0, 0))
# Layer 1: Ground shadow
battle_sprite.alpha_composite(clean_shadow)
# Layer 2: Key & curio
battle_sprite.alpha_composite(key_b)
battle_sprite.alpha_composite(curio_b)
# Layer 3: Rear & front legs
battle_sprite.alpha_composite(ll_b)
battle_sprite.alpha_composite(lr_b)
# Layer 4: Torso, Head, Costume, Core
battle_sprite.alpha_composite(torso_b)
battle_sprite.alpha_composite(head_b)
battle_sprite.alpha_composite(costume_b)
battle_sprite.alpha_composite(core_b)
# Layer 5: Weapon
battle_sprite.alpha_composite(wpn_b)

# Measure shadow row counts on battle_sprite
battle_shadow_counts = [sum(1 for x in range(128) if battle_sprite.getpixel((x, y))[3] > 20) for y in range(115, 128)]
print("Battle shadow counts (115..127):", battle_shadow_counts)

# Now check claw grounding: claws firmly rest on the shadow at y=114..115
print("Battle sprite bbox:", battle_sprite.getbbox())

# Save and compare
proof = Image.new("RGBA", (256, 128), (255, 255, 255, 255))
proof.alpha_composite(comp128, (0, 0))
proof.alpha_composite(battle_sprite, (128, 0))
proof.save("/tmp/test_clean_battle_proof.png")
