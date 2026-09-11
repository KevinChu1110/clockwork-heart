import numpy as np
from PIL import Image

im = Image.open("screenshots/proof_battle_lion_full_screen.png").convert("L")
sarr = np.array(im)
dark_cnt = (sarr < 70).sum(axis=1)
h, w = im.size[1], im.size[0]
for y in range(h):
    if dark_cnt[y] > w * 0.35 and 0.35 <= y / float(h) <= 0.55:
        print(f"y={y} (frac={y/float(h):.3f}): dark_cnt={dark_cnt[y]} (w*0.35={w*0.35})")
