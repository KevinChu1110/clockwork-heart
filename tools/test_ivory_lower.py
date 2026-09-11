from PIL import Image
import numpy as np

# Let's inspect ivory chassis paint_ivory_stock.png
ivory = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png").convert("RGBA")
arr_ivory = np.array(ivory)

# Check steel pixels in ivory
steel_iv = (arr_ivory[:, :, 3] > 128) & (arr_ivory[:, :, 0] > 185) & (arr_ivory[:, :, 1] > 185) & (arr_ivory[:, :, 2] > 185) & (np.abs(arr_ivory[:, :, 0].astype(int) - arr_ivory[:, :, 2].astype(int)) < 40)
print("Ivory chassis total steel pixels:", np.count_nonzero(steel_iv))

# How many steel pixels in y >= 96 (which is y >= 380 on screen)?
steel_iv_lower = steel_iv[96:, :]
print("Ivory chassis steel pixels in y >= 96:", np.count_nonzero(steel_iv_lower))
