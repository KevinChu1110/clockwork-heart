from PIL import Image
import numpy as np

def content_bottom_frac(path):
    im = Image.open(path).convert('RGBA')
    arr = np.array(im)
    w, h = im.size
    last_row = 0
    for y in range(h):
        if np.any(arr[y, :, 3] > 10):
            last_row = y
    frac = float(last_row + 1) / float(h)
    print(f"{path}: last_row={last_row}, frac={frac:.4f}")

for p in [
    'game/assets/sprites/player/poses/macaque/idle.png',
    'game/assets/sprites/player/poses/macaque/attack.png',
    'game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png',
]:
    content_bottom_frac(p)
