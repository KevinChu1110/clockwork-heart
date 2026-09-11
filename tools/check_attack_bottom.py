from PIL import Image
import numpy as np

im = Image.open('game/assets/sprites/player/poses/macaque/attack.png').convert('RGBA')
arr = np.array(im)
w, h = im.size
for y in range(h - 20, h):
    alphas = arr[y, :, 3]
    non_zero = np.sum(alphas > 0)
    print(f"y={y}: non-zero alpha pixels={non_zero}")
