import numpy as np
from PIL import Image

ml = np.array(Image.open("/tmp/mask_lion.png"))
mr = np.array(Image.open("/tmp/mask_rab.png"))

y = 384
print("Lion dark pixels at y=384:", int(np.sum(ml[y] > 0)))
print("Rabbit dark pixels at y=384:", int(np.sum(mr[y] > 0)))

for c in range(10):
    x0 = c * 128
    x1 = (c + 1) * 128
    cnt_l = int(np.sum(ml[y, x0:x1] > 0))
    cnt_r = int(np.sum(mr[y, x0:x1] > 0))
    print(f"cols {x0:4d}..{x1:4d}: Lion={cnt_l:3d}, Rab={cnt_r:3d}, diff={cnt_l-cnt_r:3d}")
