import numpy as np
from PIL import Image

for name in ["porcelain_panda", "spring_frog", "xuanji_tortoise", "emerald_fawn"]:
    im = Image.open(f"/opt/side/bravesoul-game/game/assets/sprites/portraits/{name}.png").convert("RGBA")
    arr = np.array(im)
    bottom_y = np.where(arr[:, :, 3] > 0)[0].max()
    print(f"{name:20s}: bottom_y={bottom_y}, bottom row non-zero alpha count={np.sum(arr[bottom_y, :, 3] > 0)}")
    # check if gradient fade
    for y in range(bottom_y - 10, bottom_y + 1):
        print(f"  y={y}: max_alpha={arr[y, :, 3].max()}, count={np.sum(arr[y, :, 3] > 0)}")
