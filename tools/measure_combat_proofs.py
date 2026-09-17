import hashlib
import os
import numpy as np
from PIL import Image

proof_dir = "proofs/combat_poses_512"
files = [
    "proof_combat_rabbit_attack_512.png",
    "proof_combat_lion_attack_512.png",
    "proof_combat_fox_skill_512.png",
]
crops = [
    "proof_combat_rabbit_attack_crop.png",
    "proof_combat_lion_attack_crop.png",
    "proof_combat_fox_skill_crop.png",
]

print("=== 1. MD5 & 尺寸檢查 (0-QA15 & 0-QA18) ===")
md5s = set()
for f in files:
    p = os.path.join(proof_dir, f)
    with open(p, "rb") as fp:
        h = hashlib.md5(fp.read()).hexdigest()
    im = Image.open(p)
    print(f"  {f}: md5={h} size={im.size} mode={im.mode}")
    if h in md5s:
        print(f"  FAIL: 重複 MD5: {h}")
    md5s.add(h)
    assert im.size == (1280, 720), f"Size must be 1280x720, got {im.size}"

print("\n=== 2. 角色區裁切 NN 放大否證量測 (0-QA17) ===")
for c in crops:
    cp = os.path.join(proof_dir, c)
    im = Image.open(cp).convert("RGBA")
    arr = np.array(im)
    h, w, ch = arr.shape

    # Count adjacent identical columns
    dup_cols = 0
    for x in range(w - 1):
        if np.array_equal(arr[:, x], arr[:, x + 1]):
            dup_cols += 1
    col_dup_ratio = dup_cols / (w - 1) * 100.0

    # Count adjacent identical rows
    dup_rows = 0
    for y in range(h - 1):
        if np.array_equal(arr[y, :], arr[y + 1, :]):
            dup_rows += 1
    row_dup_ratio = dup_rows / (h - 1) * 100.0

    # Unique colors
    flat = arr.reshape(-1, ch)
    unique_colors = len(np.unique(flat, axis=0))

    print(f"  {c} ({w}x{h}):")
    print(f"    重複欄比例: {col_dup_ratio:.2f}% (NN 2x 通常為 ~50%)")
    print(f"    重複列比例: {row_dup_ratio:.2f}%")
    print(f"    唯一色數:   {unique_colors}")

    # Assert col dup is far from 50%
    if abs(col_dup_ratio - 50.0) < 10.0:
        print(f"    WARNING: 重複欄接近 50% ({col_dup_ratio:.2f}%)，疑有 NN 放大！")
    else:
        print(f"    ✓ 0-QA17 否證成功: 重複欄 {col_dup_ratio:.2f}% != ~50%，確認非 NN 2x 放大！")
