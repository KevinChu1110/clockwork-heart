from typing import cast
import numpy as np
from PIL import Image, ImageChops

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/pangolin"

chassis_512 = Image.open(f"{PD_DIR}/chassis/chassis_pangolin_dune_orange_default_512.png").convert("RGBA")
head_512 = Image.open(f"{PD_DIR}/head_unit/head_pangolin_brass_acoustic_ears_512.png").convert("RGBA")
key_512 = Image.open(f"{PD_DIR}/winding_key/key_pangolin_coil_scale_spiral_gold_512.png").convert("RGBA")
costume_512 = Image.open(f"{PD_DIR}/costume/costume_pangolin_scavenger_tinker_vest_512.png").convert("RGBA")
core_512 = Image.open(f"{PD_DIR}/optic_core/face_pangolin_sky_blue_optic_domes_512.png").convert("RGBA")
weapon_512 = Image.open(f"{PD_DIR}/weapon/weapon_pangolin_dune_drill_claw_512.png").convert("RGBA")
curio_512 = Image.open(f"{PD_DIR}/back_curio/curio_pangolin_segmented_scale_tail_512.png").convert("RGBA")

w512, h512 = 512, 512

comp512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
comp512.alpha_composite(key_512)
comp512.alpha_composite(curio_512)
comp512.alpha_composite(chassis_512)
comp512.alpha_composite(head_512)
comp512.alpha_composite(costume_512)
comp512.alpha_composite(core_512)
comp512.alpha_composite(weapon_512)

def enforce_shadow_rows_512(img: Image.Image, baseline: Image.Image) -> Image.Image:
    out = img.copy()
    o_px = out.load()
    s_px = baseline.load()
    assert o_px is not None and s_px is not None
    for y in range(118 * 4, 128 * 4):
        for x in range(512):
            sp = cast(tuple[int, int, int, int], s_px[x, y])
            fp = cast(tuple[int, int, int, int], o_px[x, y])
            if sp[3] <= 20:
                if fp[3] > 20:
                    o_px[x, y] = (0, 0, 0, 0)
            else:
                if fp[3] <= 20:
                    o_px[x, y] = sp
    return out

clean_shadow_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
cs_px = clean_shadow_512.load()
c_px = comp512.load()
assert cs_px is not None and c_px is not None
for y in range(118 * 4, 128 * 4):
    for x in range(512):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            cs_px[x, y] = p

ch_px = chassis_512.load()
assert ch_px is not None

leg_l_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
leg_r_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
torso_chassis_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))

for y in range(h512):
    for x in range(w512):
        p = cast(tuple[int, int, int, int], ch_px[x, y])
        if p[3] == 0:
            continue
        if y >= 115 * 4 and p[3] < 180 and p[0] < 45 and p[1] < 40 and p[2] < 75:
            continue
        if y < 98 * 4:
            torso_chassis_512.putpixel((x, y), p)
        if y >= 88 * 4:
            if x <= 62 * 4:
                leg_l_512.putpixel((x, y), p)
            elif x >= 65 * 4:
                leg_r_512.putpixel((x, y), p)

pivot_l_512 = (52 * 4, 94 * 4)
pivot_r_512 = (75 * 4, 94 * 4)

# 512 battle sprite
b_torso_dx = 1 * 4
b_torso_dy = 2 * 4

ll_b_512 = leg_l_512.rotate(-15.0, resample=Image.Resampling.BICUBIC, center=pivot_l_512, translate=(-3 * 4, 1 * 4))
lr_b_512 = leg_r_512.rotate(18.0, resample=Image.Resampling.BICUBIC, center=pivot_r_512, translate=(3 * 4, 1 * 4))

torso_b_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
torso_b_512.paste(torso_chassis_512, (b_torso_dx, b_torso_dy), torso_chassis_512)

head_b_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
head_b_512.paste(head_512, (b_torso_dx + 4, b_torso_dy), head_512)

costume_b_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
costume_b_512.paste(costume_512, (b_torso_dx, b_torso_dy), costume_512)

core_b_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
core_b_512.paste(core_512, (b_torso_dx + 4, b_torso_dy), core_512)

key_b_512 = key_512.rotate(22.0, resample=Image.Resampling.BICUBIC, center=(83 * 4, 40 * 4), translate=(b_torso_dx + 4, b_torso_dy - 4))
curio_b_512 = curio_512.rotate(-14.0, resample=Image.Resampling.BICUBIC, center=(33 * 4, 94 * 4), translate=(b_torso_dx - 12, b_torso_dy + 4))
wpn_b_512 = weapon_512.rotate(-20.0, resample=Image.Resampling.BICUBIC, center=(92 * 4, 78 * 4), translate=(b_torso_dx + 20, b_torso_dy - 16))

battle_sprite_512 = Image.new("RGBA", (w512, h512), (0, 0, 0, 0))
battle_sprite_512.alpha_composite(clean_shadow_512)
battle_sprite_512.alpha_composite(key_b_512)
battle_sprite_512.alpha_composite(curio_b_512)
battle_sprite_512.alpha_composite(ll_b_512)
battle_sprite_512.alpha_composite(lr_b_512)
battle_sprite_512.alpha_composite(torso_b_512)
battle_sprite_512.alpha_composite(head_b_512)
battle_sprite_512.alpha_composite(core_b_512)
battle_sprite_512.alpha_composite(costume_b_512)
battle_sprite_512.alpha_composite(wpn_b_512)

battle_sprite_512 = enforce_shadow_rows_512(battle_sprite_512, comp512)

b_bbox_512 = battle_sprite_512.getbbox()
print("512 battle bbox:", b_bbox_512)
assert b_bbox_512[0] >= 16 and (512 - b_bbox_512[2]) >= 16, "512 battle margin unclipped check failed"
print("512 battle sprite successfully tested!")
