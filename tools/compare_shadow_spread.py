from PIL import Image
import numpy as np

def analyze_shadow(path, name):
    im = Image.open(path).convert('RGBA')
    arr = np.array(im)
    w, h = im.size
    y_start = int(h * 0.85)
    
    xs, ys, alphas, lums = [], [], [], []
    for y in range(y_start, h):
        for x in range(w):
            r, g, b, a = arr[y, x]
            if 10 <= a <= 200:
                lum = 0.299 * r + 0.587 * g + 0.114 * b
                if lum < 110.0:
                    xs.append(x)
                    ys.append(y)
                    alphas.append(a)
                    lums.append(lum)
    print(f"=== {name} ===")
    print(f"File: {path}")
    print(f"Total matching shadow pixels: {len(xs)}")
    if len(xs) > 0:
        print(f"X range: {min(xs)}..{max(xs)} (span {max(xs)-min(xs)+1})")
        print(f"Y range: {min(ys)}..{max(ys)} (span {max(ys)-min(ys)+1})")
        print(f"Mean alpha: {np.mean(alphas):.1f}, max alpha: {max(alphas)}")
        print(f"Sample points: {list(zip(xs[:5], ys[:5], alphas[:5]))}")

analyze_shadow('game/assets/sprites/player/paperdoll/macaque/chassis/paint_ivory_stock.png', 'Macaque Chassis')
analyze_shadow('game/assets/sprites/player/paperdoll/rabbit/chassis/paint_ivory_stock.png', 'Rabbit Chassis')
analyze_shadow('game/assets/sprites/player/paperdoll/macaque/proof_paperdoll_macaque_composite.png', 'Macaque Composite')
analyze_shadow('game/assets/sprites/player/paperdoll/rabbit/proof_paperdoll_rabbit_composite.png', 'Rabbit Composite')
