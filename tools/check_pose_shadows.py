from PIL import Image
import numpy as np
import glob

for p in sorted(glob.glob("game/assets/sprites/player/poses/**/*.png", recursive=True)):
    im = Image.open(p)
    arr = np.array(im)
    if arr.ndim == 3 and arr.shape[2] == 4:
        # Check alpha in bottom 10%
        h, w = arr.shape[:2]
        bottom_alpha = arr[int(h*0.9):, :, 3]
        max_a = bottom_alpha.max() if bottom_alpha.size > 0 else 0
        print(f"{p}: size={im.size}, bottom_10pct_max_alpha={max_a}")
