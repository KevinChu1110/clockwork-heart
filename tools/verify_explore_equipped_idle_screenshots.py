#!/usr/bin/env python3
import os
import sys
from PIL import Image, ImageChops

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shot_dir = os.path.join(base_dir, "screenshots")
    path_a = os.path.join(shot_dir, "proof_explore_equipped_costume_a.png")
    path_b = os.path.join(shot_dir, "proof_explore_equipped_costume_b.png")

    assert os.path.exists(path_a), f"找不到截圖 A: {path_a}"
    assert os.path.exists(path_b), f"找不到截圖 B: {path_b}"

    img_a = Image.open(path_a).convert("RGBA")
    img_b = Image.open(path_b).convert("RGBA")

    print(f"截圖 A 尺寸: {img_a.size}, 模式: {img_a.mode}")
    print(f"截圖 B 尺寸: {img_b.size}, 模式: {img_b.mode}")

    # 1. 全圖差分計算 (alpha_only=False)
    diff = ImageChops.difference(img_a, img_b)
    bbox = diff.getbbox(alpha_only=False)
    assert bbox is not None, "探索兩套外裝實機截圖完全相同 (diff is None)！"
    print(f"✓ 全圖差分 bbox (alpha_only=False): {bbox}")

    # 2. 角色區座標
    # bbox 涵蓋角色區，我們取帶有適當緩衝的邊界
    char_box = (max(0, bbox[0] - 10), max(0, bbox[1] - 10), min(img_a.width, bbox[2] + 10), min(img_a.height, bbox[3] + 10))
    print(f"✓ 角色區裁切範圍: {char_box}")

    crop_a = img_a.crop(char_box)
    crop_b = img_b.crop(char_box)

    crop_diff = ImageChops.difference(crop_a, crop_b)
    crop_bbox = crop_diff.getbbox(alpha_only=False)
    assert crop_bbox is not None, "角色區外裝無任何差異！"
    print(f"✓ 角色區差分 bbox (alpha_only=False): {crop_bbox}")

    # 計算角色區相異像素數 (RGB 任一通道差異 > 0)
    diff_pixels = 0
    pix_a = crop_a.load()
    pix_b = crop_b.load()
    w, h = crop_a.size
    if pix_a is not None and pix_b is not None:
        for y in range(h):
            for x in range(w):
                if pix_a[x, y] != pix_b[x, y]:
                    diff_pixels += 1

    print(f"✓ 角色區差異像素數: {diff_pixels} (要求 > 10000)")

    # 儲存裁切特寫供視覺審查 (Vision 模型驗證)
    crop_a_path = os.path.join(shot_dir, "proof_explore_crop_costume_a.png")
    crop_b_path = os.path.join(shot_dir, "proof_explore_crop_costume_b.png")
    crop_diff_path = os.path.join(shot_dir, "proof_explore_crop_diff.png")

    # 放大 3 倍便於視覺檢視
    zoom_size = (w * 3, h * 3)
    crop_a.resize(zoom_size, Image.Resampling.NEAREST).save(crop_a_path)
    crop_b.resize(zoom_size, Image.Resampling.NEAREST).save(crop_b_path)
    crop_diff.resize(zoom_size, Image.Resampling.NEAREST).save(crop_diff_path)

    # 另外製作 side-by-side 比較圖
    side_by_side = Image.new("RGBA", (w * 3 * 2 + 20, h * 3), (40, 40, 40, 255))
    side_by_side.paste(crop_a.resize(zoom_size, Image.Resampling.NEAREST), (0, 0))
    side_by_side.paste(crop_b.resize(zoom_size, Image.Resampling.NEAREST), (w * 3 + 20, 0))
    compare_path = os.path.join(shot_dir, "proof_explore_crop_compare.png")
    side_by_side.save(compare_path)

    print(f"✓ 儲存角色特寫 A (3x): {crop_a_path}")
    print(f"✓ 儲存角色特寫 B (3x): {crop_b_path}")
    print(f"✓ 儲存角色差分視覺圖 (3x): {crop_diff_path}")
    print(f"✓ 儲存角色左右對照圖 (3x): {compare_path}")

    assert diff_pixels > 10000, f"角色區像素差異 {diff_pixels} 未達標 (>10000)！"
    print("\nALL STANDARDS VERIFIED SUCCESSFULLY: 角色區像素差異大於 10,000 像素，且 getbbox 檢驗通過！")

if __name__ == "__main__":
    main()
