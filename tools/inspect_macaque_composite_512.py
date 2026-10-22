#!/usr/bin/env python3
import os
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_chassis = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png").convert("RGBA")
im_head = Image.open(f"{MACAQUE_DIR}/head_unit/ear_macaque_coaxial_512.png").convert("RGBA")
im_costume = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png").convert("RGBA")
im_core = Image.open(f"{MACAQUE_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")
im_weapon = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png").convert("RGBA")
im_key = Image.open(f"{MACAQUE_DIR}/winding_key/key_classic_brass_512.png").convert("RGBA")

# tail 是 128x128
im_tail_128 = Image.open(f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
im_tail_512 = im_tail_128.resize((512, 512), Image.Resampling.NEAREST)

# 測試各圖層 bbox
print("Chassis bbox:", im_chassis.getbbox())
print("Head bbox   :", im_head.getbbox())
print("Costume bbox:", im_costume.getbbox())
print("Core bbox   :", im_core.getbbox())
print("Weapon bbox :", im_weapon.getbbox())
print("Key bbox    :", im_key.getbbox())
print("Tail bbox   :", im_tail_512.getbbox())

# 按照 Z-Order: winding_key(5), tail(8), chassis(10), head(20), costume(25), core(30), weapon(40)
comp = Image.new("RGBA", (512, 512), (0, 0, 0, 0))
comp = Image.alpha_composite(comp, im_key)
comp = Image.alpha_composite(comp, im_tail_512)
comp = Image.alpha_composite(comp, im_chassis)
comp = Image.alpha_composite(comp, im_head)
comp = Image.alpha_composite(comp, im_costume)
comp = Image.alpha_composite(comp, im_core)
comp = Image.alpha_composite(comp, im_weapon)

os.makedirs("/tmp/macaque_test", exist_ok=True)
comp.save("/tmp/macaque_test/composite_512.png")
print("Saved /tmp/macaque_test/composite_512.png, bbox:", comp.getbbox())
