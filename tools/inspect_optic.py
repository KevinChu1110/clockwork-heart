from PIL import Image
import numpy as np

BASE_DIR = "/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/cat"
optic = Image.open(f"{BASE_DIR}/optic_core/face_cat_slit_optic_emerald.png")
arr = np.array(optic)
ys, xs = np.where(arr[:, :, 3] > 20)
print(f"Optic pixels: x={xs.min()}..{xs.max()}, y={ys.min()}..{ys.max()}")

# Print small ASCII representation of optic core
for y in range(ys.min(), ys.max() + 1):
    row = ""
    for x in range(xs.min(), xs.max() + 1):
        if arr[y, x, 3] > 100:
            row += "#"
        else:
            row += "."
    print(f"y={y:2d}: {row}")
