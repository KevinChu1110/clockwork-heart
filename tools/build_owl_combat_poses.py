#!/usr/bin/env python3
"""
tools/build_owl_combat_poses.py
Generates the complete, definitive 6 combat action poses for Chrono Owl (靈鐘鴞, 16th Race)
in Clockwork Heart:
  game/assets/sprites/player/poses/owl/{idle,telegraph,attack,recover,skill,hit}.png (128x128 RGBA)
  game/assets/sprites/player/poses/owl/{idle,telegraph,attack,recover,skill,hit}_512.png (512x512 RGBA, LANCZOS)
"""

import math
import os
from typing import cast
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageOps
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BASE_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/owl"
PLAYER_DIR = f"{REPO_ROOT}/game/assets/sprites/player"
OUT_DIR = f"{REPO_ROOT}/game/assets/sprites/player/poses/owl"
os.makedirs(OUT_DIR, exist_ok=True)

# 1. Load canonical components
comp_path = f"{BASE_DIR}/proof_paperdoll_owl_composite.png"
body_master = Image.open(comp_path).convert("RGBA")

# Load individual slice layers (128)
key_src = Image.open(f"{BASE_DIR}/winding_key/key_owl_sun_moon_astrolabe_gold.png").convert("RGBA")
curio_src = Image.open(f"{BASE_DIR}/back_curio/curio_owl_floating_micro_orrery.png").convert("RGBA")
chassis_src = Image.open(f"{BASE_DIR}/chassis/chassis_owl_brass_lamellae_default.png").convert("RGBA")
head_src = Image.open(f"{BASE_DIR}/head_unit/head_owl_brass_plume_antennas.png").convert("RGBA")
costume_src = Image.open(f"{BASE_DIR}/costume/costume_owl_dawn_astronomer_robe.png").convert("RGBA")
optic_src = Image.open(f"{BASE_DIR}/optic_core/face_owl_clockface_lens_dusk_gold.png").convert("RGBA")
weapon_src = Image.open(f"{BASE_DIR}/weapon/weapon_owl_armillary_escapement_scepter.png").convert("RGBA")

# Composite body without weapon layer
body_no_weapon = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
body_no_weapon.alpha_composite(key_src)
body_no_weapon.alpha_composite(curio_src)
body_no_weapon.alpha_composite(chassis_src)
body_no_weapon.alpha_composite(head_src)
body_no_weapon.alpha_composite(optic_src)
body_no_weapon.alpha_composite(costume_src)

# Extract raw weapon crop
wpn_bbox = weapon_src.getbbox()
assert wpn_bbox is not None
wand_raw = weapon_src.crop(wpn_bbox)

# Standardized ground contact shadow from baseline composite
shadow_master = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
s_px = shadow_master.load()
c_px = body_master.load()
assert s_px is not None and c_px is not None

for y in range(116, 128):
    for x in range(128):
        p = cast(tuple[int, int, int, int], c_px[x, y])
        if p[3] > 20:
            s_px[x, y] = p

def generate_poses():
    print("=== GENERATING 6 COMBAT POSES FOR CHRONO OWL ===")
    poses = {}

    # 1. IDLE (待機: baseline composite)
    # Perfectly matches baseline composite with pure ground contact
    poses["idle"] = body_master.copy()

    # 2. TELEGRAPH (出招前搖: 天文刻度校準蓄勢)
    # Wand raised high pointing to stars, celestial clock dial glow on ground, core overdrive
    telegraph_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Clockwork dial on ground
    t_draw = ImageDraw.Draw(telegraph_img)
    t_draw.ellipse([64 - 24, 115 - 4, 64 + 24, 115 + 4], outline=(255, 208, 40, 180), width=1)
    # Shift body slightly up/tense (-2px)
    telegraph_img.alpha_composite(body_no_weapon, (0, -2))
    # Wand rotated upward (~-25 deg) and raised to sky
    wand_up = wand_raw.rotate(-25, resample=Image.Resampling.BICUBIC, expand=True)
    telegraph_img.alpha_composite(wand_up, (wpn_bbox[0] - 2, wpn_bbox[1] - 8))
    # Glowing star sparks at wand tip
    t_draw.ellipse([wpn_bbox[0] + 6, wpn_bbox[1] - 12, wpn_bbox[0] + 16, wpn_bbox[1] - 2],
                   fill=(78, 216, 106, 160), outline=(255, 255, 255, 220))
    poses["telegraph"] = telegraph_img

    # 3. ATTACK (普攻出手: 星屑刻度引爆)
    # Wand thrust forward / downward, stardust burst
    attack_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    # Body leans forward to the left (+4px leftward, +1px down)
    attack_img.alpha_composite(body_no_weapon, (-4, 1))
    # Wand thrust downward forward (~20 deg)
    wand_fwd = wand_raw.rotate(20, resample=Image.Resampling.BICUBIC, expand=True)
    attack_img.alpha_composite(wand_fwd, (wpn_bbox[0] - 14, wpn_bbox[1] + 4))
    # Burst effects
    a_draw = ImageDraw.Draw(attack_img)
    # Stardust ring
    a_draw.ellipse([4, 60, 28, 84], outline=(255, 208, 40, 220), width=2)
    a_draw.line([(0, 72), (32, 72)], fill=(78, 216, 106, 200), width=1)
    a_draw.line([(16, 56), (16, 88)], fill=(78, 216, 106, 200), width=1)
    poses["attack"] = attack_img

    # 4. SKILL (技能大招: 周天星曆超頻星爆)
    # Wing-expanded celestial hover, full astrolabe overdrive
    skill_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    sk_draw = ImageDraw.Draw(skill_img)
    # Celestial halo behind body
    sk_draw.ellipse([64 - 36, 64 - 36, 64 + 36, 64 + 36], outline=(56, 160, 255, 140), width=1)
    sk_draw.ellipse([64 - 28, 64 - 28, 64 + 28, 64 + 28], outline=(255, 208, 40, 180), width=1)
    # Floating body shifted up by 6px
    skill_img.alpha_composite(body_no_weapon, (0, -6))
    # Wand held vertically high with full armillary spin
    wand_vert = wand_raw.rotate(-15, resample=Image.Resampling.BICUBIC, expand=True)
    skill_img.alpha_composite(wand_vert, (wpn_bbox[0] - 2, wpn_bbox[1] - 12))
    # Starlight pillars / beams
    for bx in [24, 48, 80, 104]:
        sk_draw.line([(bx, 4), (bx, 124)], fill=(255, 208, 40, 90), width=1)
    poses["skill"] = skill_img

    # 5. HIT (受擊硬直: 羽翼格擋棘輪卸力)
    # Knocked backward (+6px rightward), recoil tilt
    hit_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    hit_draw = ImageDraw.Draw(hit_img)
    # Knockback body shifted right by 6px, up by 2px
    hit_img.alpha_composite(body_no_weapon, (6, -2))
    # Wand tilted back defensively
    wand_def = wand_raw.rotate(35, resample=Image.Resampling.BICUBIC, expand=True)
    hit_img.alpha_composite(wand_def, (wpn_bbox[0] + 6, wpn_bbox[1] + 2))
    # Spark impact flash
    hit_draw.line([(40, 50), (30, 42)], fill=(255, 255, 255, 220), width=2)
    hit_draw.line([(38, 56), (26, 60)], fill=(255, 208, 40, 220), width=2)
    poses["hit"] = hit_img

    # 6. RECOVER (受擊復位: 展羽歸位震羽)
    # Snapping back from hit, settling back down (+2px right, settling)
    recover_img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    recover_img.alpha_composite(body_no_weapon, (2, 0))
    wand_settle = wand_raw.rotate(-5, resample=Image.Resampling.BICUBIC, expand=True)
    recover_img.alpha_composite(wand_settle, (wpn_bbox[0] + 1, wpn_bbox[1]))
    # Ground settlement ripple
    rc_draw = ImageDraw.Draw(recover_img)
    rc_draw.ellipse([64 - 20, 115 - 3, 64 + 20, 115 + 3], outline=(56, 160, 255, 120), width=1)
    poses["recover"] = recover_img

    # Save all 6 poses in 128x128 and 512x512 LANCZOS
    for name, img in poses.items():
        dst_128 = f"{OUT_DIR}/{name}.png"
        img.save(dst_128)

        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        dst_512 = f"{OUT_DIR}/{name}_512.png"
        img_512.save(dst_512)
        print(f"  ✓ Saved pose: {name}.png (128x128 & 512x512 LANCZOS)")

    print("=== ALL 6 COMBAT POSES SUCCESSFULLY GENERATED FOR CHRONO OWL ===")

if __name__ == "__main__":
    generate_poses()
