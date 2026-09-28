from PIL import Image
import numpy as np

chassis = Image.open("game/assets/sprites/player/paperdoll/peacock/chassis/chassis_peacock_glazed_porcelain_default.png")
c_arr = np.array(chassis)
for y in range(110, 128):
    # check feet pixels (where alpha > 20 and not the shadow)
    # usually shadow is very low alpha or dark/grey
    row = c_arr[y, :, :]
    opaque = np.where(row[:, 3] > 100)[0]
    shadow = np.where((row[:, 3] > 0) & (row[:, 3] <= 100))[0]
    print(f"y={y}: opaque (feet/body)={len(opaque)}, shadow={len(shadow)}")
