import os
import sys
from PIL import Image
import numpy as np

img_paths = [
    "proofs/creation_stage_no_128_fallback/proof_creation_rabbit_stage_512_hd.png",
    "proofs/creation_stage_no_128_fallback/proof_creation_rabbit_stage_fallback_hd.png",
    "proofs/proof_creation_rabbit_stage_512_hd.png",
    "proofs/proof_creation_rabbit_stage_fallback_hd.png"
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
    corners = [int(alpha[0, 0]), int(alpha[0, -1]), int(alpha[-1, 0]), int(alpha[-1, -1])]
    zero_alpha_ratio = (alpha == 0).sum() / float(w * h)
    print(f"四角 alpha: {corners}, 全透明佔比: {zero_alpha_ratio:.2%}")
    if all(c == 0 for c in corners) and zero_alpha_ratio > 0.4:
        print("FAIL: 符合貼圖 dump 特徵 (0-QA18)！")
        all_ok = False
    else:
        print("PASS 0-QA18: 四角與透明佔比符合實機畫面")

    # 驗證角色舞台區域 (x: 200..450, y: 200..450) 具備足夠非純白像素（角色確實渲染呈現）
    stage_crop = arr[200:450, 200:450, :3]
    non_white_pixels = int(((stage_crop[:, :, 0] < 245) | (stage_crop[:, :, 1] < 245) | (stage_crop[:, :, 2] < 245)).sum())
    print(f"舞台角色非底色像素數: {non_white_pixels}")
    if non_white_pixels < 5000:
        print(f"FAIL: 舞台角色區域像素過少，疑似未成功渲染角色: {non_white_pixels}")
        all_ok = False
    else:
        print("PASS: 角色實體正常渲染於中央舞台")

if not all_ok:
    sys.exit(1)
print("\n>>> 全部開局選族截圖量測驗證通過！")
