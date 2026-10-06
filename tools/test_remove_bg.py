from PIL import Image
import numpy as np
from collections import deque

def remove_flat_bg(img_path, out_path, tolerance=24):
    img = Image.open(img_path).convert("RGBA")
    arr = np.array(img)
    h, w, _ = arr.shape
    
    # Corner color reference
    bg_ref = arr[0, 0, :3].astype(float)
    
    # Distance from bg_ref
    diff = np.sqrt(np.sum((arr[:, :, :3].astype(float) - bg_ref) ** 2, axis=2))
    
    # BFS floodfill from edges
    visited = np.zeros((h, w), dtype=bool)
    q = deque()
    
    # Add borders
    for x in range(w):
        if diff[0, x] < tolerance:
            visited[0, x] = True
            q.append((0, x))
        if diff[h - 1, x] < tolerance:
            visited[h - 1, x] = True
            q.append((h - 1, x))
            
    for y in range(h):
        if diff[y, 0] < tolerance and not visited[y, 0]:
            visited[y, 0] = True
            q.append((y, 0))
        if diff[y, w - 1] < tolerance and not visited[y, w - 1]:
            visited[y, w - 1] = True
            q.append((y, w - 1))
            
    while q:
        y, x = q.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                if diff[ny, nx] < tolerance:
                    visited[ny, nx] = True
                    q.append((ny, nx))
                    
    # Make visited background transparent
    arr[visited, 3] = 0
    
    # Soft edge feathering (1px transition)
    # Find boundary pixels
    # For any non-visited pixel adjacent to visited with small diff:
    out_img = Image.fromarray(arr)
    out_img.save(out_path, "PNG")
    print(f"Processed {img_path} -> {out_path}, removed {np.sum(visited)} bg pixels ({np.sum(visited)/(h*w)*100:.1f}%)")

remove_flat_bg("/opt/side/bravesoul-game/web/media/hero/char_rabbit.png", "/tmp/char_rabbit_trans.png")
