from PIL import Image
import numpy as np

def check(path):
    im = Image.open(path).convert('RGBA')
    w, h = im.size
    y_start = int(h * 0.85)
    arr = np.array(im)
    count = 0
    for y in range(y_start, h):
        for x in range(w):
            r, g, b, a = arr[y, x]
            if 10 <= a <= 200:
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                if lum < 110.0:
                    count += 1
    has_baked = count >= 200
    print(f"{path}: size={im.size}, shadow_px={count}, has_baked_shadow={has_baked}")

for p in [
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/idle.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/poses/macaque/attack.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/chassis/paint_bamboo_bronze.png',
    '/opt/side/bravesoul-game/game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png',
]:
    check(p)
