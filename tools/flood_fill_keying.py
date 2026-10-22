#!/usr/bin/env python3
from PIL import Image
import numpy as np
from collections import deque

im = Image.open("/opt/side/bravesoul-game/web/media/hero/char_boar.png").convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# Flood fill from the outer edges:
# A pixel is background if it is connected to the outer boundary
# and has background color: R > 220, G > 205, B > 170 and max diff < 50
is_bg_color = (arr[:, :, 0] > 220) & (arr[:, :, 1] > 205) & (arr[:, :, 2] > 170) & \
              (np.abs(arr[:, :, 0].astype(int) - arr[:, :, 1].astype(int)) < 30) & \
              (np.abs(arr[:, :, 1].astype(int) - arr[:, :, 2].astype(int)) < 45)

visited = np.zeros((h, w), dtype=bool)
bg_mask = np.zeros((h, w), dtype=bool)

queue = deque()
# Add all border pixels that match background color
for x in range(w):
    if is_bg_color[0, x]:
        queue.append((0, x))
        visited[0, x] = True
    if is_bg_color[h-1, x] and arr[h-1, x, 0] > 230: # don't start inside dark foot shadow
        queue.append((h-1, x))
        visited[h-1, x] = True
for y in range(h):
    if is_bg_color[y, 0]:
        queue.append((y, 0))
        visited[y, 0] = True
    if is_bg_color[y, w-1]:
        queue.append((y, w-1))
        visited[y, w-1] = True

# BFS flood fill
while queue:
    cy, cx = queue.popleft()
    bg_mask[cy, cx] = True
    for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ny, nx = cy + dy, cx + dx
        if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
            visited[ny, nx] = True
            # In char_boar.png, background is smooth gradient
            if is_bg_color[ny, nx]:
                queue.append((ny, nx))

print("Total image pixels:", h * w)
print("Connected background pixels:", np.sum(bg_mask))

arr_keyed = arr.copy()
arr_keyed[bg_mask, 3] = 0
out_im = Image.fromarray(arr_keyed, mode="RGBA")
out_im.save("/tmp/flood_keyed_boar.png")
print("Saved /tmp/flood_keyed_boar.png, bbox:", out_im.getbbox())
