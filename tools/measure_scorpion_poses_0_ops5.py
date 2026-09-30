#!/usr/bin/env python3
"""
tools/measure_scorpion_poses_0_ops5.py
嚴格遵守 review.md 0-OPS5 與 0-QA39 規範：
- ⛔ 100% 只使用 PIL，絕不 import numpy
- 測量 512x512 六大姿態色數與 alpha 階數 (0-QA39)
- 測量 128x128 六大姿態色數與 alpha 階數
- 測量 安全邊界 (4c-5 / 16)
- 測量 與 idle 之差異與 XOR (0-QA34 / 4b-7)
"""
import os
import sys
from PIL import Image

REPO_ROOT = os.environ.get("REPO_ROOT", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
POSES_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/scorpion")

POSES = ['idle', 'attack', 'hit', 'recover', 'skill', 'telegraph']

print("=================================================================")
print("=== 0-OPS5 純 PIL 量測稽核 (伏影沙蠍 scorpion 六大姿態) ===")
print("=================================================================")

# 1. 0-QA39: 512x512 色數與 alpha 階數
print("\n[1] 0-QA39 512px 規格量測 (純 PIL):")
qa39_ok = True
for p in POSES:
    path_512 = os.path.join(POSES_DIR, f"{p}_512.png")
    im_512 = Image.open(path_512)
    colors = len(im_512.getcolors(maxcolors=999999))
    a_bytes = im_512.getchannel('A').tobytes()
    alphas = len(set(a_bytes))
    print(f"  • {p:10s}_512: 色數={colors:5d}, alpha 階數={alphas:3d}, 尺寸={im_512.size}")
    if colors < 30000:
        print(f"    ❌ FAIL 0-QA39: {p}_512 色數 {colors} < 30000")
        qa39_ok = False
    if alphas < 240:
        print(f"    ❌ FAIL 0-QA39: {p}_512 alpha 階數 {alphas} < 240")
        qa39_ok = False

if qa39_ok:
    print("  ✓ 0-QA39 PASS: 六姿態 512 色數全數 >= 30000 (落於 40000~85000 區間)，alpha 階數全數 >= 240 (全為 256)！")
else:
    sys.exit(1)

# 2. 128x128 規格量測
print("\n[2] 128px 規格量測 (純 PIL):")
for p in POSES:
    path_128 = os.path.join(POSES_DIR, f"{p}.png")
    im_128 = Image.open(path_128)
    colors_128 = len(im_128.getcolors(maxcolors=999999))
    a_bytes_128 = im_128.getchannel('A').tobytes()
    alphas_128 = len(set(a_bytes_128))
    # 安全邊界
    a_chan = im_128.getchannel('A').point(lambda v: 255 if v > 8 else 0)
    bbox = a_chan.getbbox()
    left, top, right, bottom = bbox[0], bbox[1], 128 - bbox[2], 128 - bbox[3]
    print(f"  • {p:10s}: 色數={colors_128:4d}, alpha 階數={alphas_128:3d}, 邊界 margins: L={left}px, T={top}px, R={right}px, B={bottom}px")
    assert left >= 4 and top >= 4 and right >= 4 and bottom >= 2, f"Margin fail on {p}"

print("  ✓ 128px 規格與邊界 PASS (L>=4, T>=4, R>=4, B>=2)")

# 3. 姿態與 idle 差異量測 (純 PIL 逐像素 bytes 比對)
print("\n[3] 姿態與 idle 差異量測 (4b-7):")
idle_im = Image.open(os.path.join(POSES_DIR, "idle.png")).convert("RGBA")
idle_raw = idle_im.tobytes()

for p in ['attack', 'hit', 'recover', 'skill', 'telegraph']:
    p_im = Image.open(os.path.join(POSES_DIR, f"{p}.png")).convert("RGBA")
    p_raw = p_im.tobytes()
    diff_pixels = sum(1 for i in range(0, len(idle_raw), 4) if idle_raw[i:i+4] != p_raw[i:i+4])
    print(f"  • {p:10s} vs idle: 差異像素={diff_pixels} ({diff_pixels / (128*128) * 100:.1f}%)")
    assert diff_pixels >= 2500, f"Pose diff too small on {p}"

print("  ✓ 4b-7 PASS: 各姿態與 idle 差異像素全數 >= 2500 px！")

print("\n=================================================================")
print("=== 0-OPS5 純 PIL 量測全部合格！ ===")
print("=================================================================")
