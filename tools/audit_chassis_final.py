import os
import numpy as np
from PIL import Image

CHASSIS_DIR = "game/assets/sprites/player/paperdoll/penguin/chassis"
HEAD_PATH = "game/assets/sprites/player/paperdoll/penguin/head_unit/head_steam_penguin_stock.png"
head_img = Image.open(HEAD_PATH).convert("RGBA")
head_arr = np.array(head_img)
head_opaque = head_arr[:, :, 3] > 0
head_bbox = head_img.getbbox()

files = [
    "paint_penguin_navy.png",
    "paint_polar_frost.png",
    "paint_ivory_stock.png"
]

def compute_0_art19(path):
    img = Image.open(path).convert("RGBA")
    arr = np.array(img)
    H, W, _ = arr.shape
    alpha = arr[:, :, 3]
    opaque = alpha >= 16
    tot = int(np.sum(opaque))
    if tot == 0:
        return 0, 0, 0, (0, 0), 0
    rgb = arr[:, :, :3]

    eq_rgb = (
        np.all(rgb[1:-1, 1:-1] == rgb[0:-2, 1:-1], axis=-1) &
        np.all(rgb[1:-1, 1:-1] == rgb[2:, 1:-1], axis=-1) &
        np.all(rgb[1:-1, 1:-1] == rgb[1:-1, 0:-2], axis=-1) &
        np.all(rgb[1:-1, 1:-1] == rgb[1:-1, 2:], axis=-1)
    )
    c3 = np.zeros((H, W), dtype=bool)
    c3[1:-1, 1:-1] = eq_rgb & opaque[1:-1, 1:-1]
    flat_pct = float(np.sum(c3) / tot * 100.0)

    rgb_packed = (rgb[:, :, 0].astype(np.uint32) << 16) | (rgb[:, :, 1].astype(np.uint32) << 8) | rgb[:, :, 2].astype(np.uint32)
    vals, counts = np.unique(rgb_packed[opaque], return_counts=True)
    top_col = vals[np.argmax(counts)]
    topcol_pct = float(np.max(counts) / tot * 100.0)

    bin_mask = (rgb_packed == top_col) & opaque
    heights = np.zeros(W, dtype=int)
    best_maxrect = 0
    best_dim = (0, 0)
    for y in range(H):
        heights = np.where(bin_mask[y, :], heights + 1, 0)
        stack = []
        for i, h in enumerate(heights):
            start = i
            while stack and stack[-1][1] > h:
                s_idx, prev_h = stack.pop()
                area = prev_h * (i - s_idx)
                if area > best_maxrect:
                    best_maxrect = area
                    best_dim = (i - s_idx, prev_h)
                start = s_idx
            stack.append((start, h))
        for s_idx, prev_h in stack:
            area = prev_h * (W - s_idx)
            if area > best_maxrect:
                best_maxrect = area
                best_dim = (W - s_idx, prev_h)
    return flat_pct, topcol_pct, best_maxrect, best_dim, tot

print(f"Head unit bbox: {head_bbox}")
print("=" * 70)
for fn in files:
    fpath = os.path.join(CHASSIS_DIR, fn)
    img = Image.open(fpath).convert("RGBA")
    bbox = img.getbbox()
    min_y = bbox[1] if bbox else None
    arr = np.array(img)
    opaque = arr[:, :, 3] > 0
    overlap_count = int(np.sum(opaque & head_opaque))
    
    flat_pct, topcol_pct, maxrect, maxrect_dim, tot = compute_0_art19(fpath)
    
    print(f"File: {fn}")
    print(f"  bbox: {bbox} (start_y: {min_y})")
    print(f"  overlap with head_unit: {overlap_count} px (neck bearing seam at y=48..55)")
    print(f"  flat%: {flat_pct:.1f}% (target: < 10%)")
    print(f"  topcol%: {topcol_pct:.1f}% (target: < 28%)")
    print(f"  maxrect: {maxrect} dim={maxrect_dim} (target: < 100)")
    print(f"  total opaque (alpha>=16): {tot}")
    print("-" * 70)
