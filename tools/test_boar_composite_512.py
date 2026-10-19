#!/usr/bin/env python3
import os
from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
BOAR_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/boar"

# 檢查 chassis/paint_brass_gold_512.png
chassis = Image.open(f"{BOAR_DIR}/chassis/paint_brass_gold_512.png")
head = Image.open(f"{BOAR_DIR}/head_unit/ear_boar_rivet_cowl_brass_512.png")
key = Image.open(f"{BOAR_DIR}/winding_key/key_classic_brass_512.png")
core = Image.open(f"{BOAR_DIR}/optic_core/core_cyan_emerald_512.png")
costume = Image.open(f"{BOAR_DIR}/costume/costume_viking_ironclad_512.png")
weapon = Image.open(f"{BOAR_DIR}/weapon/wpn_anvil_greathammer_512.png")
tail_128 = Image.open(f"{BOAR_DIR}/back_curio/curio_spring_tail.png")

print("Chassis bbox:", chassis.getbbox())
print("Head bbox:", head.getbbox())
print("Key bbox:", key.getbbox())
print("Core bbox:", core.getbbox())
print("Costume bbox:", costume.getbbox())
print("Weapon bbox:", weapon.getbbox())
print("Tail 128 bbox:", tail_128.getbbox())

# 合成一張測試看看 512 組合效果
comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
# Z order: key, tail, chassis, head, costume, core, weapon
comp.alpha_composite(key)
tail_512 = tail_128.resize((512, 512), Image.Resampling.NEAREST)
print("Tail 512 bbox:", tail_512.getbbox())
comp.alpha_composite(tail_512)
comp.alpha_composite(chassis)
comp.alpha_composite(head)
comp.alpha_composite(costume)
comp.alpha_composite(core)
comp.alpha_composite(weapon)

out_test = "/tmp/boar_512_test_comp.png"
comp.save(out_test)
print(f"Saved {out_test}, bbox={comp.getbbox()}")
