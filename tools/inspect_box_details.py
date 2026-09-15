from PIL import Image
import numpy as np

for name in ["key", "head", "chassis", "costume"]:
    im = Image.open(f"/opt/side/bravesoul-game/screenshots/box_{name}.png")
    arr = np.array(im)
    alpha = arr[:,:,3]
    ys, xs = np.where(alpha > 0)
    if len(ys) > 0:
        print(f"{name}: y from {ys.min()} to {ys.max()}, x from {xs.min()} to {xs.max()}, count={len(ys)}")
        # print unique colors
        colors = np.unique(arr[alpha > 0], axis=0)
        print(f"  sample colors (first 3): {colors[:3].tolist()}")
