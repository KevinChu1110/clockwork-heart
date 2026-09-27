from PIL import Image
import numpy as np

REPO_ROOT = "/opt/side/bravesoul-game"
PD_DIR = f"{REPO_ROOT}/game/assets/sprites/player/paperdoll/wolf"
chassis_128 = Image.open(f"{PD_DIR}/chassis/chassis_wolf_warm_orange_default.png").convert("RGBA")
arr = np.array(chassis_128)

for y in [95, 100, 105, 110, 113, 115]:
    xs = np.where(arr[y, :, 3] > 20)[0]
    print(f"y={y}: xs={list(xs)}")
