#!/usr/bin/env python3
import os
from PIL import Image, ImageChops

def main():
    shot_dir = "/opt/side/bravesoul-game/screenshots"
    path_a = os.path.join(shot_dir, "proof_lobby_equipped_costume_a.png")
    path_b = os.path.join(shot_dir, "proof_lobby_equipped_costume_b.png")

    assert os.path.exists(path_a), f"找不到截圖 A: {path_a}"
    assert os.path.exists(path_b), f"找不到截圖 B: {path_b}"

    img_a = Image.open(path_a).convert("RGBA")
    img_b = Image.open(path_b).convert("RGBA")

    print(f"截圖 A 尺寸: {img_a.size}, 模式: {img_a.mode}")
    print(f"截圖 B 尺寸: {img_b.size}, 模式: {img_b.mode}")

    # 1. 全圖差分計算
    diff = ImageChops.difference(img_a, img_b)
    bbox = diff.getbbox(alpha_only=False)
    assert bbox is not None, "大廳兩套外裝實機截圖完全相同 (diff is None)！"
    print(f"✓ 全圖差分 bbox (alpha_only=False): {bbox}")

    # 2. 角色區座標 (640, 405 為中心，寬 250 高 265，外擴緩衝至 320x340)
    # Stage center is roughly (640, 405), hero rect is (-125, -140) to (125, 125) -> (515, 265) to (765, 530)
    # 取適當角色邊界 [480, 240, 800, 560]
    char_box = (480, 240, 800, 560)
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
    assert diff_pixels > 10000, f"角色區像素差異 {diff_pixels} 未達標 (>10000)！"

    # 儲存裁切特寫供視覺審查 (Vision 模型驗證)
    crop_a_path = os.path.join(shot_dir, "proof_lobby_crop_costume_a.png")
    crop_b_path = os.path.join(shot_dir, "proof_lobby_crop_costume_b.png")
    crop_diff_path = os.path.join(shot_dir, "proof_lobby_crop_diff.png")

    crop_a.save(crop_a_path)
    crop_b.save(crop_b_path)
    crop_diff.save(crop_diff_path)

    print(f"✓ 儲存角色特寫 A: {crop_a_path}")
    print(f"✓ 儲存角色特寫 B: {crop_b_path}")
    print(f"✓ 儲存角色差分視覺圖: {crop_diff_path}")
    print("\nALL STANDARDS VERIFIED SUCCESSFULLY: 角色區像素差異大於 10,000 像素，且 getbbox 檢驗通過！")

if __name__ == "__main__":
    main()
