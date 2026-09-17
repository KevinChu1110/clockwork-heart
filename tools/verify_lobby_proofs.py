import os
import sys
from PIL import Image
import numpy as np

img_paths = [
    "proofs/lobby_no_128_fallback/proof_lobby_rabbit_royal_parade_hd.png",
    "proofs/lobby_no_128_fallback/proof_lobby_fox_astral_observer_hd.png"
]

all_ok = True

for path in img_paths:
    print(f"=== 驗證 {path} ===")
    if not os.path.exists(path):
        print(f"FAIL: 檔案不存在: {path}")
        all_ok = False
        continue

    img = Image.open(path).convert("RGBA")
    w, h = img.size
    print(f"尺寸: {w}x{h}")
    if (w, h) != (1280, 720):
        print(f"FAIL: 尺寸非 1280x720: {(w, h)}")
        all_ok = False

    arr = np.array(img)
    alpha = arr[:, :, 3]

    # 0-QA18: 實機截圖檢驗
    # 四角 alpha 全 0 ＋ 全透明佔比 > 40% ＋ 尺寸 512x512 = 貼圖 dump
    corners = [alpha[0, 0], alpha[0, -1], alpha[-1, 0], alpha[-1, -1]]
    zero_alpha_ratio = (alpha == 0).sum() / float(w * h)
    print(f"四角 alpha: {corners}, 全透明佔比: {zero_alpha_ratio:.2%}")
    if all(c == 0 for c in corners) and zero_alpha_ratio > 0.4:
        print("FAIL: 符合貼圖 dump 特徵 (0-QA18)！")
        all_ok = False
    else:
        print("PASS 0-QA18: 四角與透明佔比符合實機畫面")

    # 0-QA21: 白方洞用量測
    # 統計角色頭部/中央區域 (y 200..450, x 500..750) RGB 三通道皆 >= 250 的純白像素數
    center_rgb = arr[200:450, 500:750, :3]
    white_pixels = ((center_rgb[:, :, 0] >= 250) & (center_rgb[:, :, 1] >= 250) & (center_rgb[:, :, 2] >= 250)).sum()
    print(f"中央角色區純白像素數 (RGB >= 250): {white_pixels}")
    # 合格圖一般 < 100 點 (甚至個位數)，真白方洞會有成千上萬點
    if white_pixels > 2000:
        print(f"FAIL: 疑似出現大面積白方洞 (0-QA21): {white_pixels}")
        all_ok = False
    else:
        print("PASS 0-QA21: 無大面積白方洞")

if not all_ok:
    sys.exit(1)
print("\n>>> 全部截圖量測驗證通過！")
