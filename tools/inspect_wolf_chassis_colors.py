from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_wolf_warm_orange_default.png").convert("RGBA")
arr = np.array(chassis_128)

colors = {}
for y in range(88, 98):
    for x in range(46, 74):
        p = tuple(arr[y, x])
        if p[3] > 50:
            colors[p] = colors.get(p, 0) + 1

for c, count in sorted(colors.items(), key=lambda item: item[1], reverse=True)[:10]:
    print(c, count)
