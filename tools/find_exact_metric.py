from PIL import Image, ImageFilter
import numpy as np

rab_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png"
mac_iv_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png"
mac_br_path = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png"

rab = Image.open(rab_path).convert("RGBA")
mac_iv = Image.open(mac_iv_path).convert("RGBA")
mac_br = Image.open(mac_br_path).convert("RGBA")

# Let's inspect rabbit total inner pixels and dark pixels
# Maybe outline exclusion is by color? (e.g. outline color is dark border)
# Or outline exclusion by distance to edge?
# Let's check what dark colors exist in rabbit chassis
rab_arr = np.array(rab)
iv_arr = np.array(mac_iv)
br_arr = np.array(mac_br)

print("Rab opaque count (a>0):", np.sum(rab_arr[:,:,3] > 0))
print("Rab opaque count (a>8):", np.sum(rab_arr[:,:,3] > 8))
print("Rab opaque count (a>128):", np.sum(rab_arr[:,:,3] > 128))

# Let's test a simple definition:
# "內部像素（排除輪廓邊緣）中深色雜點佔比"
# What if outline is defined as: pixels with alpha neighbor, OR pixels in outline color?
# Notice review.md 4b-9-4: "本 repo 統一用 alpha > 8"
