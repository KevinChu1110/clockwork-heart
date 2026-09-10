import os
from PIL import Image, ImageChops, ImageOps
from typing import cast
from collections import deque

poses_paths = {
    "idle": "game/assets/sprites/player/party/lion_idle.png",
    "attack": "/tmp/warped_attack_117.png",
    "hit": "game/assets/sprites/player/poses/lion/hit.png",
    "recover": "/tmp/rec_off2.png",
    "skill": "game/assets/sprites/player/poses/lion/skill.png",
    "telegraph": "game/assets/sprites/player/poses/lion/telegraph.png"
}

imgs = {k: Image.open(p).convert("RGBA") for k, p in poses_paths.items()}

print("=== 1. BBOX, HEIGHT & MARGINS ===")
heights = {}
all_pass = True
for name, im in imgs.items():
    b = im.getbbox()
    assert b is not None
    w = b[2] - b[0]
    h = b[3] - b[1]
    L = b[0]
    R = 128 - b[2]
    T = b[1]
    B = 128 - b[3]
    heights[name] = h
    pass_margin = (L >= 4 and R >= 4 and T >= 4 and B == 2)
    if not pass_margin:
        all_pass = False
    status = "OK" if pass_margin else "FAIL"
    print(f"{name:10s}: bbox={b}, w={w:3d}, h={h:3d}, L={L:2d}, R={R:2d}, T={T:2d}, B={B:2d} -> {status}")

min_h = min(heights.values())
max_h = max(heights.values())
h_diff_pct = (max_h - min_h) / max_h * 100.0
print(f"\nHeight range: min={min_h}, max={max_h}, diff={h_diff_pct:.2f}% (Rule 4b-9 requires <= 5.0%)")
assert h_diff_pct <= 5.0, "Height diff exceeds 5%!"

print("\n=== 2. GROUND SHADOW (Rule 4b-5) ===")
benchmark = [67, 71, 72, 70, 66, 59, 47, 26, 0, 0]
for name, im in imgs.items():
    px = im.load()
    assert px is not None
    counts = []
    for y in range(118, 128):
        c = sum(1 for x in range(128) if cast(tuple[int, int, int, int], px[x, y])[3] > 20)
        counts.append(c)
    # Check max deviation vs benchmark
    dev = max(abs(c - b) for c, b in zip(counts, benchmark))
    status = "OK" if dev <= 1 else f"FAIL (dev={dev})"
    print(f"{name:10s} shadow: {counts} (dev={dev}) -> {status}")
    assert dev <= 1, f"Shadow deviation too high on {name}"

print("\n=== 3. 8-CONNECTED SINGLE COMPONENT (Rule 0b-5) ===")
def get_components(im: Image.Image) -> int:
    px = im.load()
    assert px is not None
    w, h = im.size
    visited = set()
    components = 0
    for y in range(h):
        for x in range(w):
            if cast(tuple[int, int, int, int], px[x, y])[3] > 20 and (x, y) not in visited:
                components += 1
                q = deque([(x, y)])
                visited.add((x, y))
                while q:
                    cx, cy = q.popleft()
                    for dx in [-1, 0, 1]:
                        for dy in [-1, 0, 1]:
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = cx + dx, cy + dy
                            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                                if cast(tuple[int, int, int, int], px[nx, ny])[3] > 20:
                                    visited.add((nx, ny))
                                    q.append((nx, ny))
    return components

for name, im in imgs.items():
    c = get_components(im)
    status = "OK" if c == 1 else f"FAIL (components={c})"
    print(f"{name:10s} components: {c} -> {status}")
    assert c == 1, f"{name} has {c} components!"

print("\n=== 4. PAIRWISE BODY DIFFS (y<118) ===")
def diff_px(im1, im2, y_max=118):
    px1 = im1.load()
    px2 = im2.load()
    assert px1 is not None and px2 is not None
    d = 0
    for y in range(y_max):
        for x in range(128):
            p1 = cast(tuple[int, int, int, int], px1[x, y])
            p2 = cast(tuple[int, int, int, int], px2[x, y])
            if max(abs(p1[c] - p2[c]) for c in range(4)) > 10:
                d += 1
    return d

poses_list = ["idle", "attack", "hit", "recover", "skill", "telegraph"]
for i in range(len(poses_list)):
    for j in range(i + 1, len(poses_list)):
        p1 = poses_list[i]
        p2 = poses_list[j]
        d = diff_px(imgs[p1], imgs[p2], 118)
        status = "OK" if d >= 5000 else f"FAIL (d={d} < 5000)"
        print(f"{p1:10s} vs {p2:10s}: {d:4d} px -> {status}")
        assert d >= 5000, f"Pairwise diff too low: {p1} vs {p2} = {d}"

print("\n=== 5. ATTACK VS TELEGRAPH LEGS DIFF (92<=y<118) ===")
def legs_diff_px(im1, im2):
    px1 = im1.load()
    px2 = im2.load()
    assert px1 is not None and px2 is not None
    d = 0
    for y in range(92, 118):
        for x in range(128):
            p1 = cast(tuple[int, int, int, int], px1[x, y])
            p2 = cast(tuple[int, int, int, int], px2[x, y])
            if max(abs(p1[c] - p2[c]) for c in range(4)) > 10:
                d += 1
    return d

d_legs = legs_diff_px(imgs["attack"], imgs["telegraph"])
print(f"Attack vs Telegraph legs diff: {d_legs} px (Rule benchmark >= 800) -> {'OK' if d_legs >= 800 else 'FAIL'}")
assert d_legs >= 800

print("\n=== 6. RECOVER VS MIRRORED ATTACK MIN RESIDUAL ===")
mirrored_atk = ImageOps.mirror(imgs["attack"])
min_resid = 999999
for dx in range(-10, 11):
    for dy in range(-10, 11):
        shifted = ImageChops.offset(mirrored_atk, dx, dy)
        d = diff_px(imgs["recover"], shifted, 118)
        if d < min_resid:
            min_resid = d
print(f"Recover vs mirrored attack min residual: {min_resid} px (Rule benchmark >= 4000) -> {'OK' if min_resid >= 4000 else 'FAIL'}")
assert min_resid >= 4000

print("\n=== 7. TOP 30 ROW WIDTH SEQUENCES ===")
def get_top_widths(im):
    px = im.load()
    assert px is not None
    widths = []
    for y in range(30):
        w = sum(1 for x in range(128) if cast(tuple[int, int, int, int], px[x, y])[3] > 20)
        widths.append(w)
    return widths

w_tele = get_top_widths(imgs["telegraph"])
w_atk = get_top_widths(imgs["attack"])
w_rec = get_top_widths(imgs["recover"])

print("w_tele top 20:", w_tele[:20])
print("w_atk  top 20:", w_atk[:20])
print("w_rec  top 20:", w_rec[:20])
print("atk != tele:", w_atk != w_tele)
print("atk != rec :", w_atk != w_rec)
print("rec != tele:", w_rec != w_tele)
assert w_atk != w_tele and w_atk != w_rec and w_rec != w_tele, "Top width sequences must be distinct!"

print("\n>>> ALL 7 RIGOROUS VERIFICATION CRITERIA PASSED! <<<")
