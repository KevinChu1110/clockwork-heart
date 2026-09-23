import os
from PIL import Image
import numpy as np
from collections import deque

def process_elephant_showcase():
    src_path = "branding/char_elephant.png"
    dst_path = "game/assets/sprites/player/showcase/elephant_idle_hd.png"
    im = Image.open(src_path).convert("RGB")
    arr = np.array(im, dtype=np.float32)
    h, w, _ = arr.shape
    
    border_pixels = np.concatenate([
        arr[:15, :].reshape(-1, 3),
        arr[-15:, :].reshape(-1, 3),
        arr[:, :15].reshape(-1, 3),
        arr[:, -15:].reshape(-1, 3)
    ], axis=0)
    bg_mean = border_pixels.mean(axis=0)
    print(f"Processing elephant ({w}x{h}): bg_mean={bg_mean.astype(int).tolist()}")
    
    lum = (arr[:, :, 0] + arr[:, :, 1] + arr[:, :, 2]) / 3.0
    
    # 1. Flood fill from borders
    is_bg = np.zeros((h, w), dtype=bool)
    queue = deque()
    
    for x in range(w):
        if lum[0, x] > 175:
            is_bg[0, x] = True
            queue.append((0, x))
        if lum[h - 1, x] > 175:
            is_bg[h - 1, x] = True
            queue.append((h - 1, x))
    for y in range(h):
        if not is_bg[y, 0] and lum[y, 0] > 175:
            is_bg[y, 0] = True
            queue.append((y, 0))
        if not is_bg[y, w - 1] and lum[y, w - 1] > 175:
            is_bg[y, w - 1] = True
            queue.append((y, w - 1))
            
    while queue:
        y, x = queue.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not is_bg[ny, nx]:
                if lum[ny, nx] > 175:
                    is_bg[ny, nx] = True
                    queue.append((ny, nx))
                    
    # Check for between-legs bg hole
    dist_bg = np.abs(arr - np.array([235., 226., 209.])).max(axis=-1)
    hole_candidates = (~is_bg) & (dist_bg <= 4)
    visited = np.zeros((h, w), dtype=bool)
    for y in range(h):
        for x in range(w):
            if hole_candidates[y, x] and not visited[y, x]:
                comp = []
                cq = deque([(y, x)])
                visited[y, x] = True
                while cq:
                    cy, cx = cq.popleft()
                    comp.append((cy, cx))
                    for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
                        ny, nx = cy + dy, cx + dx
                        if 0 <= ny < h and 0 <= nx < w and hole_candidates[ny, nx] and not visited[ny, nx]:
                            visited[ny, nx] = True
                            cq.append((ny, nx))
                if len(comp) > 500:
                    print(f"  Found between-legs bg hole: size={len(comp)}, y range=[{min(p[0] for p in comp)}, {max(p[0] for p in comp)}]")
                    for cy, cx in comp:
                        is_bg[cy, cx] = True

    # 2. Transition zone: pixels within 3px of is_bg
    transition_mask = np.zeros((h, w), dtype=bool)
    for dy in range(-3, 4):
        for dx in range(-3, 4):
            if dy*dy + dx*dx <= 9:
                shifted = np.zeros((h, w), dtype=bool)
                if dy < 0:
                    y_src = slice(-dy, h); y_dst = slice(0, h + dy)
                elif dy > 0:
                    y_src = slice(0, h - dy); y_dst = slice(dy, h)
                else:
                    y_src = slice(0, h); y_dst = slice(0, h)
                if dx < 0:
                    x_src = slice(-dx, w); x_dst = slice(0, w + dx)
                elif dx > 0:
                    x_src = slice(0, w - dx); x_dst = slice(dx, w)
                else:
                    x_src = slice(0, w); x_dst = slice(0, w)
                shifted[y_dst, x_dst] = is_bg[y_src, x_src]
                transition_mask |= shifted

    # 3. Calculate Alpha and Defringe RGB
    alpha = np.ones((h, w), dtype=np.float32) * 255.0
    out_rgb = arr.copy()
    
    high_lum = 215.0
    low_lum = 55.0
    
    trans_pixels = transition_mask
    t_lum = lum[trans_pixels]
    a_factor = np.clip((high_lum - t_lum) / (high_lum - low_lum), 0.0, 1.0)
    alpha[trans_pixels] = a_factor * 255.0
    
    alpha[is_bg & (lum >= 205)] = 0.0
    alpha[alpha < 30] = 0.0
    
    # 4. Defringe semi-transparent pixels (30 <= alpha < 255)
    semi_mask = (alpha >= 30) & (alpha < 255)
    if np.sum(semi_mask) > 0:
        semi_a = (alpha[semi_mask] / 255.0)[:, np.newaxis]
        semi_c = out_rgb[semi_mask]
        defringed = (semi_c - (1.0 - semi_a) * bg_mean) / semi_a
        out_rgb[semi_mask] = np.clip(defringed, 0, 255)
        
    corners = [(0, 0), (h-1, 0), (0, w-1), (h-1, w-1)]
    for cy, cx in corners:
        alpha[cy, cx] = 0.0
        
    out_arr = np.zeros((h, w, 4), dtype=np.uint8)
    out_arr[:, :, :3] = np.clip(out_rgb, 0, 255).astype(np.uint8)
    out_arr[:, :, 3] = np.clip(alpha, 0, 255).astype(np.uint8)
    
    out_im = Image.fromarray(out_arr, mode="RGBA")
    out_im.save(dst_path)
    print(f"  Successfully saved {dst_path}: mode={out_im.mode}, size={out_im.size}, bbox={out_im.getbbox()}")
    c_corners = [out_im.getpixel((cx, cy)) for cy, cx in corners]
    print(f"  Corners: {c_corners}")
    print(f"  Transparent pixels: {np.sum(alpha == 0)} ({np.sum(alpha == 0)/(w*h)*100:.1f}%)")

if __name__ == "__main__":
    process_elephant_showcase()
