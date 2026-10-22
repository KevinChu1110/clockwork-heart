#!/usr/bin/env python3
import os
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

# 看看 128x128 和 512x512 的 key
im_key_128 = Image.open(f"{MACAQUE_DIR}/winding_key/key_classic_brass.png")
im_key_512 = Image.open(f"{MACAQUE_DIR}/winding_key/key_classic_brass_512.png")
print("Key 128 size:", im_key_128.size, "bbox:", im_key_128.getbbox())
print("Key 512 size:", im_key_512.size, "bbox:", im_key_512.getbbox())

# 看看 128 的 key 在 128 畫布上的位置是 (71, 49, 89, 68) -> 這是背部右手邊
# 為什麼 key_512 的 bbox 是 (136, 233, 194, 362)？
# 136/4 = 34, 233/4 = 58... 這是左邊？還是右邊？
# 看看 128 的 composite:
im_comp_128 = Image.open(f"{MACAQUE_DIR}/proof_paperdoll_macaque_composite.png")
print("Composite 128 size:", im_comp_128.size, "bbox:", im_comp_128.getbbox())

# 看看 tail
im_tail = Image.open(f"{MACAQUE_DIR}/back_curio/curio_spring_tail.png")
print("Tail size:", im_tail.size, "bbox:", im_tail.getbbox())
