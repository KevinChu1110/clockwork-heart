#!/usr/bin/env python3
import os
import sys
from PIL import Image, ImageChops

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    shot_dir = os.path.join(base_dir, "screenshots")
    p0 = os.path.join(shot_dir, "proof_explore_idle_breathe_t0.png")
    p1 = os.path.join(shot_dir, "proof_explore_idle_breathe_t1.png")
    pw = os.path.join(shot_dir, "proof_explore_walking.png")
    pa = os.path.join(shot_dir, "proof_explore_equipped_costume_a.png")
    pb = os.path.join(shot_dir, "proof_explore_equipped_costume_b.png")

    for p in [p0, p1, pw, pa, pb]:
        assert os.path.exists(p), f"缺少檔案: {p}"

    img0 = Image.open(p0).convert("RGBA")
    img1 = Image.open(p1).convert("RGBA")
    imgw = Image.open(pw).convert("RGBA")
    imga = Image.open(pa).convert("RGBA")
    imgb = Image.open(pb).convert("RGBA")

    print(f"t0 截圖尺寸: {img0.size}")
    print(f"t1 截圖尺寸: {img1.size}")
    print(f"walk 截圖尺寸: {imgw.size}")
    print(f"costume_a 尺寸: {imga.size}")
    print(f"costume_b 尺寸: {imgb.size}")

    assert img0.size == (1280, 720), "t0 尺寸不為 1280x720"
    assert img1.size == (1280, 720), "t1 尺寸不為 1280x720"
    assert imgw.size == (1280, 720), "walk 尺寸不為 1280x720"

    # 1. 驗證站立呼吸 (t0 vs t1, 間隔 >= 1.0s)
    diff_t = ImageChops.difference(img0, img1)
    bbox_t = diff_t.getbbox(alpha_only=False)
    assert bbox_t is not None, "t0 與 t1 截圖完全相同，未發生呼吸縮放！"
    print(f"✓ 站立呼吸差分 bbox (t0 vs t1): {bbox_t}")

    diff_pixels_t = 0
    for p in diff_t.getdata():
        if p[0] > 0 or p[1] > 0 or p[2] > 0:
            diff_pixels_t += 1
    print(f"✓ 站立呼吸差異像素數 (t0 vs t1): {diff_pixels_t}")
    assert diff_pixels_t > 500, f"呼吸縮放差異像素數過低 ({diff_pixels_t})"

    # 2. 驗證換裝 (costume_a vs costume_b)
    diff_ab = ImageChops.difference(imga, imgb)
    bbox_ab = diff_ab.getbbox(alpha_only=False)
    assert bbox_ab is not None, "外裝 A 與外裝 B 完全相同！"
    diff_pixels_ab = 0
    for p in diff_ab.getdata():
        if p[0] > 0 or p[1] > 0 or p[2] > 0:
            diff_pixels_ab += 1
    print(f"✓ 換裝差分 bbox (costume_a vs costume_b): {bbox_ab}")
    print(f"✓ 換裝差異像素數: {diff_pixels_ab} (標準 > 10000)")
    assert diff_pixels_ab > 10000, f"換裝差異像素數未達標 ({diff_pixels_ab} <= 10000)"

    # 3. 驗證走路畫面與站立畫面相異
    diff_w = ImageChops.difference(img0, imgw)
    bbox_w = diff_w.getbbox(alpha_only=False)
    assert bbox_w is not None, "走路畫面與站立畫面完全相同！"
    print(f"✓ 走路 vs 站立差分 bbox: {bbox_w}")

    # 4. 產出特寫對照圖供視覺審查
    # 角色區大約在畫面中央偏下
    char_box = (max(0, bbox_t[0] - 20), max(0, bbox_t[1] - 20), min(img0.width, bbox_t[2] + 20), min(img0.height, bbox_t[3] + 20))
    print(f"✓ 角色呼吸特寫範圍: {char_box}")

    crop0 = img0.crop(char_box)
    crop1 = img1.crop(char_box)
    crop_diff = diff_t.crop(char_box)

    w, h = crop0.size
    compare_breathe = Image.new("RGBA", (w * 2 + 10, h), (30, 30, 30, 255))
    compare_breathe.paste(crop0, (0, 0))
    compare_breathe.paste(crop1, (w + 10, 0))
    compare_breathe_path = os.path.join(shot_dir, "proof_explore_breathe_compare.png")
    compare_breathe.save(compare_breathe_path)
    print(f"✓ 儲存呼吸兩刻對照圖: {compare_breathe_path}")

    # 腳底陰影特寫 (確認影子在地表、不浮空)
    # 腳底約在 char_box 的底部
    foot_box = (char_box[0], char_box[3] - 80, char_box[2], char_box[3] + 20)
    foot_crop0 = img0.crop(foot_box)
    foot_crop1 = img1.crop(foot_box)
    fw, fh = foot_crop0.size
    foot_compare = Image.new("RGBA", (fw * 2 + 10, fh), (30, 30, 30, 255))
    foot_compare.paste(foot_crop0, (0, 0))
    foot_compare.paste(foot_crop1, (fw + 10, 0))
    foot_compare_path = os.path.join(shot_dir, "proof_explore_foot_shadow_compare.png")
    foot_compare.save(foot_compare_path)
    print(f"✓ 儲存腳底接地陰影對照圖: {foot_compare_path}")

    print("\n所有客觀量測檢驗全部通過！")

if __name__ == "__main__":
    main()
