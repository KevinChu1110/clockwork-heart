import sys
import numpy as np
from PIL import Image

def measure(path):
    img = Image.open(path).convert('RGBA')
    a = np.array(img)
    op = a[:, :, 3] > 10
    fy = np.array([np.where(op[:, x])[0][0] for x in range(a.shape[1]) if op[:, x].any()])
    cols_at_top = int((fy == fy.min()).sum())
    near_white = int(((a[:, :, :3] >= 245).all(axis=2) & op).sum())
    y_indices = np.where(op)[0]
    min_y = int(y_indices.min()) if len(y_indices) > 0 else -1
    max_y = int(y_indices.max()) if len(y_indices) > 0 else -1
    x_indices = np.where(op)[1]
    min_x = int(x_indices.min()) if len(x_indices) > 0 else -1
    max_x = int(x_indices.max()) if len(x_indices) > 0 else -1
    print(f"[{path}]")
    print(f"  size: {img.size}")
    print(f"  bbox: x=[{min_x}, {max_x}], y=[{min_y}, {max_y}] (bottom: {max_y})")
    print(f"  cols_at_top: {cols_at_top}")
    print(f"  near_white: {near_white}")
    return {
        "path": path,
        "cols_at_top": cols_at_top,
        "near_white": near_white,
        "min_y": min_y,
        "max_y": max_y,
        "size": img.size
    }

if __name__ == '__main__':
    paths = sys.argv[1:] if len(sys.argv) > 1 else [
        "game/assets/sprites/player/paperdoll/boar/chassis/paint_brass_gold_512.png",
        "game/assets/sprites/player/paperdoll/boar/chassis/paint_ivory_stock_512.png",
        "game/assets/sprites/player/paperdoll/boar/chassis/paint_molten_crimson_512.png",
    ]
    for p in paths:
        measure(p)
