#!/usr/bin/env python3
from PIL import Image
import numpy as np
from collections import deque

REPO_ROOT = "/opt/side/bravesoul-game"
HERO_BOAR = f"{REPO_ROOT}/web/media/hero/char_boar.png"

im = Image.open(HERO_BOAR).convert("RGBA")
arr = np.array(im)
h, w, _ = arr.shape

# 背景泛洪填充：從四個角 (0, 0), (w-1, 0), (0, h-1), (w-1, h-1) 開始向內擴散
# 背景判斷標準：
# 只要像素顏色是米白/象牙白/淺灰色：R > 215, G > 210, B > 200 且 |R-G| < 25 且 |G-B| < 25
# 或者是白色光暈：R > 230, G > 230, B > 230

visited = np.zeros((h, w), dtype=bool)
bg_mask = np.zeros((h, w), dtype=bool)

def is_bg_pixel(r, g, b):
    # 避免誤傷角色的象牙白獠牙或亮金屬：獠牙通常在 x: 150..400, y: 300..600 內部
    if r > 215 and g > 210 and b > 195:
        if abs(int(r) - int(g)) < 22 and abs(int(g) - int(b)) < 22:
            return True
    if r > 235 and g > 235 and b > 235:
        return True
    return False

queue = deque()
# 加入邊界上的所有背景點
for x in range(w):
    for y in [0, 1, 2, 3, h-1, h-2, h-3]:
        r, g, b, a = arr[y, x]
        if is_bg_pixel(r, g, b):
            queue.append((x, y))
            visited[y, x] = True

for y in range(h):
    for x in [0, 1, 2, 3, w-1, w-2, w-3]:
        if not visited[y, x]:
            r, g, b, a = arr[y, x]
            if is_bg_pixel(r, g, b):
                queue.append((x, y))
                visited[y, x] = True

# 廣度優先搜尋 (BFS)
while queue:
    cx, cy = queue.popleft()
    bg_mask[cy, cx] = True
    
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = cx + dx, cy + dy
        if 0 <= nx < w and 0 <= ny < h and not visited[ny, nx]:
            visited[ny, nx] = True
            r, g, b, a = arr[ny, nx]
            # 避開腳底投影 (y > 1050 且有深色)
            if ny > 1060 and (r < 180 or g < 170):
                continue
            if is_bg_pixel(r, g, b):
                queue.append((nx, ny))

arr[bg_mask, 3] = 0
clean_im = Image.fromarray(arr, mode="RGBA")
clean_im.save("/tmp/official_boar_transparent_928.png")
print("Flood fill finished! Saved /tmp/official_boar_transparent_928.png")
