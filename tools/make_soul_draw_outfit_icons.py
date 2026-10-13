"""從 outfits_x4.png 切出四件換裝，轉成 128px 像素卡面圖示（透明底、1px 深色描邊）。

用法（repo 根目錄）：
    python3 tools/make_soul_draw_outfit_icons.py
輸出：game/assets/icons/soul_draw/outfit_*.png
這是由貼紙圖縮出的過渡版，正式像素美術到位後直接覆蓋同名檔即可。
"""
import os
import sys
from collections import deque
from PIL import Image

SRC = sys.argv[1] if len(sys.argv) > 1 else "game/assets/sprites/pack_a/v2/chars/outfits_x4.png"
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "game/assets/icons/soul_draw"
os.makedirs(OUT_DIR, exist_ok=True)
OUTLINE = (0x1F, 0x1A, 0x3A, 255)
NAMES = ["outfit_cream", "outfit_brass_vest", "outfit_scarf_tunic", "outfit_worker_apron"]
LOGICAL = 64

im = Image.open(SRC).convert("RGB")
W, H = im.size
cell_w = W // 4


def is_bg(c):
    r, g, b = c
    return min(r, g, b) >= 168 and max(r, g, b) - min(r, g, b) <= 14


for i, name in enumerate(NAMES):
    box = (max(i * cell_w + 4, 22), 225, min((i + 1) * cell_w - 4, W - 22), 694)
    cell = im.crop(box)
    cw, ch = cell.size
    px = cell.load()
    alpha = [[255] * cw for _ in range(ch)]
    q = deque()
    for x in range(cw):
        q.append((x, 0)); q.append((x, ch - 1))
    for y in range(ch):
        q.append((0, y)); q.append((cw - 1, y))
    seen = set()
    while q:
        x, y = q.popleft()
        if (x, y) in seen or not (0 <= x < cw and 0 <= y < ch):
            continue
        seen.add((x, y))
        if not is_bg(px[x, y]):
            continue
        alpha[y][x] = 0
        q.extend(((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
    rgba = cell.convert("RGBA")
    rp = rgba.load()
    for y in range(ch):
        for x in range(cw):
            if alpha[y][x] == 0:
                rp[x, y] = (0, 0, 0, 0)
    # 只留主要連通塊（去掉散點）
    comp = [[-1] * cw for _ in range(ch)]
    sizes = []
    for sy in range(ch):
        for sx in range(cw):
            if alpha[sy][sx] == 0 or comp[sy][sx] >= 0:
                continue
            cid = len(sizes)
            n = 0
            st = [(sx, sy)]
            comp[sy][sx] = cid
            while st:
                x, y = st.pop()
                n += 1
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < cw and 0 <= ny < ch and alpha[ny][nx] and comp[ny][nx] < 0:
                        comp[ny][nx] = cid
                        st.append((nx, ny))
            sizes.append(n)
    keep = {k for k, n in enumerate(sizes) if n >= max(sizes) * 0.02}
    for y in range(ch):
        for x in range(cw):
            if alpha[y][x] and comp[y][x] not in keep:
                rp[x, y] = (0, 0, 0, 0)
    bb = rgba.getchannel("A").getbbox()
    rgba = rgba.crop(bb)
    # 縮到邏輯格（留 2px 給描邊）
    fit = LOGICAL - 4
    s = fit / max(rgba.size)
    small = rgba.resize((max(1, round(rgba.size[0] * s)), max(1, round(rgba.size[1] * s))), Image.LANCZOS)
    a = small.getchannel("A").point(lambda v: 255 if v >= 128 else 0)
    rgb = small.convert("RGB").quantize(colors=20, method=Image.MEDIANCUT, dither=Image.NONE).convert("RGB")
    small = rgb.convert("RGBA")
    small.putalpha(a)
    canvas = Image.new("RGBA", (LOGICAL, LOGICAL), (0, 0, 0, 0))
    ox = (LOGICAL - small.size[0]) // 2
    oy = (LOGICAL - small.size[1]) // 2
    canvas.alpha_composite(small, (ox, oy))
    # 外圈 1px 深藍紫描邊
    cp = canvas.load()
    solid = {(x, y) for y in range(LOGICAL) for x in range(LOGICAL) if cp[x, y][3] > 0}
    for (x, y) in list(solid):
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nx, ny = x + dx, y + dy
            if 0 <= nx < LOGICAL and 0 <= ny < LOGICAL and (nx, ny) not in solid:
                cp[nx, ny] = OUTLINE
    out = canvas.resize((128, 128), Image.NEAREST)
    out.save(f"{OUT_DIR}/{name}.png", optimize=True)
    print(name, bb, small.size)
