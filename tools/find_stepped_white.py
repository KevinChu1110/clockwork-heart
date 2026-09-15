import os
from PIL import Image
import numpy as np

# Find any PNG file in game/assets/ that contains a block of near-white pixels with this shape
matches = []
for root, dirs, files in os.walk("/opt/side/bravesoul-game/game/assets"):
    for f in files:
        if f.endswith(".png"):
            p = os.path.join(root, f)
            try:
                im = Image.open(p)
                arr = np.array(im)
                if arr.ndim == 3 and arr.shape[2] == 4:
                    # check for white pixels r>240, g>240, b>240
                    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
                    white = (r > 240) & (g > 240) & (b > 240) & (a > 200)
                    if np.sum(white) > 100:
                        # check if it has a vertical edge
                        matches.append((p, np.sum(white), im.size))
            except Exception:
                pass

print(f"Total matching PNGs: {len(matches)}")
for p, count, sz in sorted(matches, key=lambda x: x[1], reverse=True)[:30]:
    print(f"{count:6d}  {sz}  {p}")
