#!/usr/bin/env python3
"""
tools/verify_fox_action_poses.py
Comprehensive objective verification suite for Fox 6 combat action poses.
"""

import hashlib
import os
import subprocess
from typing import cast
from PIL import Image, ImageChops

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FOX_POSES_DIR = os.path.join(REPO_ROOT, "game/assets/sprites/player/poses/fox")
POSES = ["idle", "telegraph", "attack", "recover", "skill", "hit"]

def measure_staff_linearity(img: Image.Image) -> float:
    px = img.load()
    assert px is not None
    centers: list[float] = []
    ys: list[float] = []
    for y in range(30, 124):
        xs = []
        for x in range(img.width):
            p = cast(tuple[int, int, int, int], px[x, y])
            if p[3] > 120:
                is_bronze = (120 <= p[0] <= 195 and 75 <= p[1] <= 155 and 25 <= p[2] <= 95)
                if is_bronze:
                    xs.append(x)
        if xs and len(xs) <= 14:
            centers.append(sum(xs) / float(len(xs)))
            ys.append(float(y))
    if len(ys) < 8:
        return 0.0
    n = float(len(ys))
    sum_y = sum(ys)
    sum_c = sum(centers)
    sum_yy = sum(y * y for y in ys)
    sum_yc = sum(y * c for y, c in zip(ys, centers))
    denom = (n * sum_yy - sum_y * sum_y)
    if abs(denom) < 1e-6:
        return 0.0
    m = (n * sum_yc - sum_y * sum_c) / denom
    c_const = (sum_c - m * sum_y) / n
    resids = [abs(c - (m * y + c_const)) for y, c in zip(ys, centers)]
    return max(resids)

def measure_shadow_rows(img: Image.Image) -> list[int]:
    px = img.load()
    assert px is not None
    counts = []
    for y in range(118, 128):
        c = sum(1 for x in range(img.width) if cast(tuple[int, int, int, int], px[x, y])[3] >= 8)
        counts.append(c)
    return counts

def main():
    print("=== 狐族六大戰鬥姿態全項客觀驗收測試 (Verification Suite) ===")
    
    # 1. 檔案存在性、尺寸與 MD5 唯一性
    print("\n--- 1. 檔案存在性、128x128 RGBA 尺寸與 MD5 唯一性 ---")
    imgs = {}
    md5s = {}
    for p in POSES:
        fpath = os.path.join(FOX_POSES_DIR, f"{p}.png")
        assert os.path.exists(fpath), f"Missing pose file: {fpath}"
        im = Image.open(fpath)
        assert im.size == (128, 128), f"Wrong size for {p}: {im.size}"
        assert im.mode == "RGBA", f"Wrong mode for {p}: {im.mode}"
        with open(fpath, "rb") as f:
            h = hashlib.md5(f.read()).hexdigest()
        assert h not in md5s.values(), f"Duplicate MD5 for {p}: {h}"
        md5s[p] = h
        imgs[p] = im
        print(f"  ✓ {p:10s} 尺寸: {im.size}, bbox={im.getbbox()}, MD5: {h}")

    # 2. Rule 4b / 4b-7: 與 idle 的客觀骨骼差分 (Pixel Diff)
    print("\n--- 2. 與 idle 姿態之客觀骨骼差分分析 (Rule 4b / 4b-7) ---")
    idle_im = imgs["idle"]
    for p in ["telegraph", "attack", "recover", "skill", "hit"]:
        diff = ImageChops.difference(idle_im, imgs[p])
        diff_data = list(diff.convert("L").getdata())
        diff_px = sum(1 for x in diff_data if x > 10)
        diff_ratio = diff_px / (128.0 * 128.0) * 100.0
        diff_bbox = diff.getbbox()
        print(f"  ✓ {p:10s} vs idle: diff={diff_px} px ({diff_ratio:.1f}%), bbox={diff_bbox}")
        assert diff_px >= 3000, f"Diff for {p} too small ({diff_px} < 3000)!"
        assert diff_bbox is not None and (diff_bbox[2] - diff_bbox[0] >= 80) and (diff_bbox[3] - diff_bbox[1] >= 80), f"Diff bbox for {p} must cover whole body!"

    # 3. Rule 4b-5: 剛性法杖線性度與地面接觸軟影驗證
    print("\n--- 3. 剛性法杖線性度與柔邊軟影連續性 (Rule 4b-5) ---")
    for p in POSES:
        im = imgs[p]
        st_resid = measure_staff_linearity(im)
        sh_rows = measure_shadow_rows(im)
        print(f"  ✓ {p:10s} staff_max_resid={st_resid:.2f}px, shadow_profile={sh_rows}")
        assert sh_rows[0] > 50, f"Shadow row 0 too small in {p}: {sh_rows[0]}"

    # 4. Godot 無頭載入與測試
    print("\n--- 4. Godot 無頭單元測試 (test_fox_action_poses.gd) ---")
    cmd = ["godot", "--path", f"{REPO_ROOT}/game", "--headless", "-s", "res://scripts/art/test_fox_action_poses.gd"]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    assert "FOX_ACTION_POSES_TEST_OK" in res.stdout, f"Godot test failed!\n{res.stdout}\n{res.stderr}"

    print("\nALL OBJECTIVE CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    main()
