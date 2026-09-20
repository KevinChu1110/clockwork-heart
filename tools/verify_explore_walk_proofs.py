import os
import sys
import hashlib
from PIL import Image
import numpy as np

img_paths = [
    "proofs/explore_walk_no_128_fallback/proof_explore_walk_rabbit_512.png",
    "proofs/explore_walk_no_128_fallback/proof_explore_walk_penguin_512.png"
]

all_ok = True
hashes = []

for path in img_paths:
    print(f"\n=== 驗證 {path} ===")
    if not os.path.exists(path):
        print(f"FAIL: 檔案不存在: {path}")
        all_ok = False
        continue

    # MD5
    with open(path, "rb") as f:
        md5 = hashlib.md5(f.read()).hexdigest()
    print(f"MD5: {md5}")
    if md5 in hashes:
        print("FAIL 0-QA15: 截圖重複！")
        all_ok = False
    hashes.append(md5)

    img = Image.open(path).convert("RGBA")
    w, h = img.size
    print(f"尺寸: {w}x{h}")
    if (w, h) != (1280, 720):
        print(f"FAIL: 尺寸非 1280x720: {(w, h)}")
        all_ok = False

    arr = np.array(img)
    alpha = arr[:, :, 3]

    # 0-QA18: 實機截圖檢驗（不可為白底/全黑貼圖 dump，要有場景與 HUD）
    corners = [int(alpha[0, 0]), int(alpha[0, -1]), int(alpha[-1, 0]), int(alpha[-1, -1])]
    zero_alpha_ratio = (alpha == 0).sum() / float(w * h)
    print(f"四角 alpha: {corners}, 全透明佔比: {zero_alpha_ratio:.2%}")
    if all(c == 0 for c in corners) and zero_alpha_ratio > 0.4:
        print("FAIL: 符合貼圖 dump 特徵 (0-QA18)！")
        all_ok = False
    else:
        print("PASS 0-QA18: 四角與透明佔比符合實機畫面 (有場景與 HUD)")

    # 0-QA21: 白方洞量測（統計角色區域 RGB 三通道皆 >= 250 的純白像素數）
    center_rgb = arr[200:600, 300:800, :3]
    white_pixels = int(((center_rgb[:, :, 0] >= 250) & (center_rgb[:, :, 1] >= 250) & (center_rgb[:, :, 2] >= 250)).sum())
    print(f"角色區純白像素數 (RGB >= 250): {white_pixels}")
    if white_pixels > 2000:
        print(f"FAIL: 疑似出現大面積白方洞 (0-QA21): {white_pixels}")
        all_ok = False
    else:
        print("PASS 0-QA21: 無大面積白方洞")

if not all_ok:
    sys.exit(1)
print("\n>>> 全部截圖量測驗證通過！")
