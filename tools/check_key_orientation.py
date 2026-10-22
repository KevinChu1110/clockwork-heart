#!/usr/bin/env python3
from PIL import Image

MACAQUE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque"

im_128_key = Image.open(f"{MACAQUE_DIR}/winding_key/key_classic_brass.png")
im_512_key = Image.open(f"{MACAQUE_DIR}/winding_key/key_classic_brass_512.png")

print("128 key bbox:", im_128_key.getbbox())
# 128 key bbox 是 (71, 49, 89, 68)
# 71/128 = 0.554
# 512 key bbox 是 (136, 233, 194, 362)
# 136/512 = 0.265

# 看看 128 的 chassis 和 512 的 chassis:
im_128_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock.png")
im_512_ch = Image.open(f"{MACAQUE_DIR}/chassis/paint_ivory_stock_512.png")
print("128 chassis bbox:", im_128_ch.getbbox())
print("512 chassis bbox:", im_512_ch.getbbox())

# 128 的 (25, 35, 105, 121) -> 25/128=0.195, 105/128=0.820
# 512 的 (110, 150, 412, 477) -> 110/512=0.214, 412/512=0.804
# 身體水平是一樣的！
# 那為什麼 512 key 是在左邊？
# 看看 512 key 是否是從 rabbit 來的？
im_rab_key = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/maple_parts/winding_key/key_classic_brass.png")
print("rabbit key:", im_rab_key.size, im_rab_key.getbbox())
