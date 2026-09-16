#!/usr/bin/env python3
"""
合成果凍風格的對比圖：
左側：篩選前（全部種族切片展開）
右側：篩選後（點選「熊」只顯示玄軸熊切片）
"""
import os
from PIL import Image, ImageDraw, ImageFont

def main():
    screenshots_dir = "/opt/side/bravesoul-game/proofs/wardrobe_race_filter"
    path_all = os.path.join(screenshots_dir, "proof_wardrobe_filter_all.png")
    path_penguin = os.path.join(screenshots_dir, "proof_wardrobe_filter_penguin.png")
    path_out = "/opt/side/bravesoul-game/proofs/proof_wardrobe_filter_comparison.png"
    path_out_sub = os.path.join(screenshots_dir, "proof_wardrobe_filter_comparison.png")

    if not os.path.exists(path_all) or not os.path.exists(path_penguin):
        print(f"Error: Missing input screenshots {path_all} or {path_penguin}")
        return

    img_all = Image.open(path_all).convert("RGB")
    img_penguin = Image.open(path_penguin).convert("RGB")

    w, h = img_all.size
    # 縮小為 960x540 並排
    target_w, target_h = 960, 540
    resized_all = img_all.resize((target_w, target_h), Image.Resampling.LANCZOS)
    resized_penguin = img_penguin.resize((target_w, target_h), Image.Resampling.LANCZOS)

    banner_h = 60
    total_w = target_w * 2 + 20
    total_h = target_h + banner_h + 20

    canvas = Image.new("RGB", (total_w, total_h), (31, 26, 58)) # 深藍紫底色
    draw = ImageDraw.Draw(canvas)

    # 貼上兩張圖
    canvas.paste(resized_all, (10, banner_h + 10))
    canvas.paste(resized_penguin, (target_w + 10, banner_h + 10))

    # 畫標題條
    draw.rectangle([10, 10, target_w, banner_h], fill=(255, 208, 40)) # 金黃
    draw.rectangle([target_w + 10, 10, total_w - 10, banner_h], fill=(78, 216, 106)) # 薄荷綠

    # 邊框
    draw.rectangle([10, banner_h + 10, target_w + 10, total_h - 10], outline=(255, 160, 16), width=3)
    draw.rectangle([target_w + 10, banner_h + 10, total_w - 10, total_h - 10], outline=(78, 216, 106), width=3)

    canvas.save(path_out)
    canvas.save(path_out_sub)
    print(f"Successfully generated comparison screenshot at: {path_out}")

if __name__ == "__main__":
    main()
