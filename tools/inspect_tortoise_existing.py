#!/usr/bin/env python3
from PIL import Image
import numpy as np

pd_dir = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/tortoise"
chassis = Image.open(f"{pd_dir}/chassis/paint_tortoise_jade.png")
costume = Image.open(f"{pd_dir}/costume/costume_zen_dojo_harness.png")
head = Image.open(f"{pd_dir}/head_unit/head_xuanji_tortoise_stock.png")
core = Image.open(f"{pd_dir}/optic_core/core_amber_quartz.png")
weapon = Image.open(f"{pd_dir}/weapon/wpn_bagua_astrolabe.png")
key = Image.open(f"{pd_dir}/winding_key/key_tai_chi_dual_fish.png")
curio = Image.open(f"{pd_dir}/back_curio/curio_bagua_armillary_rings.png")

print("Chassis bbox:", chassis.getbbox(), "size:", chassis.size)
print("Costume bbox:", costume.getbbox(), "size:", costume.size)
print("Head bbox:", head.getbbox(), "size:", head.size)
print("Core bbox:", core.getbbox(), "size:", core.size)
print("Weapon bbox:", weapon.getbbox(), "size:", weapon.size)
print("Key bbox:", key.getbbox(), "size:", key.size)
print("Curio bbox:", curio.getbbox(), "size:", curio.size)

cos_arr = np.array(costume)
opaque_cos = cos_arr[cos_arr[:, :, 3] > 0]
unique_colors = len(np.unique(opaque_cos, axis=0))
print("Costume opaque pixels:", len(opaque_cos), f"unique: {unique_colors}, c100: {unique_colors/len(opaque_cos)*100:.2f}")

ch_arr = np.array(chassis)
opaque_ch = ch_arr[ch_arr[:, :, 3] > 0]
unique_ch_colors = len(np.unique(opaque_ch, axis=0))
print("Chassis opaque pixels:", len(opaque_ch), f"unique: {unique_ch_colors}, c100: {unique_ch_colors/len(opaque_ch)*100:.2f}")
