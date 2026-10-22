#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png").convert("RGBA")
im_tunic = Image.open(f"{MACAQUE_DIR}/costume/costume_dawn_monk_tunic_512.png").convert("RGBA")
im_zen = Image.open(f"{MACAQUE_DIR}/costume/costume_zen_striker_512.png").convert("RGBA")
im_weapon = Image.open(f"{MACAQUE_DIR}/weapon/wpn_spring_claws_512.png").convert("RGBA")
im_core = Image.open(f"{MACAQUE_DIR}/optic_core/core_cyan_emerald_512.png").convert("RGBA")

# 1. Core Center (胸口核心寶石)
bbox_core = im_core.getbbox()
print("Core bbox:", bbox_core)
cx_core = (bbox_core[0] + bbox_core[2]) / 2.0
cy_core = (bbox_core[1] + bbox_core[3]) / 2.0
print(f"Core Center: ({cx_core:.1f}, {cy_core:.1f})")

# 2. Costume center & bbox
print("Tunic bbox:", im_tunic.getbbox())
print("Zen bbox:", im_zen.getbbox())
cx_tunic = (im_tunic.getbbox()[0] + im_tunic.getbbox()[2]) / 2.0
cy_tunic = (im_tunic.getbbox()[1] + im_tunic.getbbox()[3]) / 2.0
print(f"Tunic Center: ({cx_tunic:.1f}, {cy_tunic:.1f})")

# 3. Weapon bbox & hand grip area
print("Weapon bbox:", im_weapon.getbbox())
# 爪子覆蓋手腕和手部
cx_wpn = (im_weapon.getbbox()[0] + im_weapon.getbbox()[2]) / 2.0
cy_wpn = (im_weapon.getbbox()[1] + im_weapon.getbbox()[3]) / 2.0
print(f"Weapon Center: ({cx_wpn:.1f}, {cy_wpn:.1f})")

# 4. Tail:
im_tail_128 = Image.open(f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png").convert("RGBA")
# 128 下的 tail 接縫處在哪裡？
# 檢查 tail 最左邊的非透明像素
tail_attach_x, tail_attach_y = 128, 128
for y in range(128):
    for x in range(128):
        if im_tail_128.getpixel((x, y))[3] > 100:
            if x < tail_attach_x:
                tail_attach_x, tail_attach_y = x, y
print(f"Tail attach in 128: ({tail_attach_x}, {tail_attach_y}) -> in 512: ({tail_attach_x*4}, {tail_attach_y*4})")
