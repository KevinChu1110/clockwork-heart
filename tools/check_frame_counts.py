import os
from PIL import Image
import numpy as np

for f in range(1, 25):
    p = f"/tmp/frame_{f}.png"
    if os.path.exists(p):
        im = Image.open(p).convert("L")
        arr = np.array(im)
        h, w = im.size[1], im.size[0]
        max_c = max((arr[y, :] < 70).sum() for y in range(int(h*0.35), int(h*0.55)))
        print(f"frame {f:2d}: max_cnt={max_c}")
