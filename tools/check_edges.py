#!/usr/bin/env python3
from PIL import Image
import numpy as np

for name in ["body", "head", "key"]:
    im = Image.open(f"/tmp/crop_ur_{name}.png")
    arr = np.array(im)
    print(f"=== {name} in crop ===")
    print("Non-zero alpha pixels:", np.sum(arr[:, :, 3] > 0))
    # Look for straight vertical edges in alpha
    for x in range(arr.shape[1]):
        col_alpha = arr[:, x, 3]
        if np.all(col_alpha[30:80] > 200) and x > 0 and np.all(arr[:, x-1, 3] == 0):
            print(f"  {name} has vertical edge at rel x={x} (abs x={300+x})")
        if np.all(col_alpha[30:80] == 0) and x > 0 and np.all(arr[:, x-1, 3] > 200):
            print(f"  {name} has vertical edge at rel x={x} (abs x={300+x})")
