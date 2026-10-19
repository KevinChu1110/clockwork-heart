#!/usr/bin/env python3
from PIL import Image
import numpy as np

godot_im = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/boar/proof_maple_boar_composite.png").convert("RGBA")
python_im = Image.open("/tmp/python_composite_direct.png").convert("RGBA")

g_arr = np.array(godot_im)
p_arr = np.array(python_im)

print("Godot size:", godot_im.size, "Python size:", python_im.size)
diff = (g_arr != p_arr)
print("Different pixels count:", np.sum(np.any(diff, axis=2)))

# 檢查 Godot 生成的圖片在鼻吻下方 (220..250, 175..205) 的 Alpha
g_snout_alpha = g_arr[175:205, 220:250, 3]
print("Godot snout min alpha:", np.min(g_snout_alpha), "zero count:", np.sum(g_snout_alpha == 0))

# 檢查 Python 生成的圖片在鼻吻下方 (220..250, 175..205) 的 Alpha
p_snout_alpha = p_arr[175:205, 220:250, 3]
print("Python snout min alpha:", np.min(p_snout_alpha), "zero count:", np.sum(p_snout_alpha == 0))
