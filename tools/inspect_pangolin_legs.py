import numpy as np
from PIL import Image

ch = Image.open("/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/pangolin/chassis/chassis_pangolin_dune_orange_default.png").convert("RGBA")
arr = np.array(ch)
print("Chassis bbox:", ch.getbbox())

for y in range(80, 125, 5):
    xs = np.where(arr[y, :, 3] > 20)[0]
    if len(xs) > 0:
        print(f"y={y:3d}: x in [{xs.min():3d} .. {xs.max():3d}], count={len(xs)}")

# Check shadow vs solid body
shadow_count = np.sum((arr[115:, :, 3] < 200) & (arr[115:, :, 3] > 0) & (arr[115:, :, 0] < 45))
print("Shadow-like pixels in y>=115:", shadow_count)

# Let's inspect foot contacts at y=110..122
for y in range(105, 123):
    xs = np.where(arr[y, :, 3] > 100)[0]
    if len(xs) > 0:
        print(f"foot solid y={y}: xs={xs.tolist()}")
