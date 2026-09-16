#!/usr/bin/env python3
"""
生成衣櫥彈窗改版前後對比圖：
左側：改版前（框中框重疊、分區厚黑描邊+陰影、篩選膠囊黑框、小字擁擠模糊）
右側：改版後（分區無框純色底板、膠囊純色柔和分隔、卡片1px邊框無陰影、字級加大至可讀無截斷）
"""
import os
from PIL import Image, ImageDraw

def main():
    screenshots_dir = "/opt/side/bravesoul-game/screenshots"
    path_before = "/tmp/proof_wardrobe_before.png"
    path_after = os.path.join(screenshots_dir, "proof_wardrobe_filter_all.png")
    path_out = os.path.join(screenshots_dir, "proof_wardrobe_comparison_before_after.png")

    if not os.path.exists(path_before) or not os.path.exists(path_after):
        print(f"Error: Missing input screenshots {path_before} or {path_after}")
        return

    img_before = Image.open(path_before).convert("RGB")
    img_after = Image.open(path_after).convert("RGB")

    target_w, target_h = 960, 540
    resized_before = img_before.resize((target_w, target_h), Image.Resampling.LANCZOS)
    resized_after = img_after.resize((target_w, target_h), Image.Resampling.LANCZOS)

    banner_h = 60
    total_w = target_w * 2 + 20
    total_h = target_h + banner_h + 20

    canvas = Image.new("RGB", (total_w, total_h), (31, 26, 58)) # 深藍紫底色
    draw = ImageDraw.Draw(canvas)

    # 貼上兩張圖
    canvas.paste(resized_before, (10, banner_h + 10))
    canvas.paste(resized_after, (target_w + 10, banner_h + 10))

    # 畫標題條
    draw.rectangle([10, 10, target_w, banner_h], fill=(255, 160, 16)) # 暖橘 (改版前: 框中框疊加)
    draw.rectangle([target_w + 10, 10, total_w - 10, banner_h], fill=(78, 216, 106)) # 薄荷綠 (改版後: 純色分隔無框中框)

    # 邊框
    draw.rectangle([10, banner_h + 10, target_w + 10, total_h - 10], outline=(255, 160, 16), width=3)
    draw.rectangle([target_w + 10, banner_h + 10, total_w - 10, total_h - 10], outline=(78, 216, 106), width=3)

    canvas.save(path_out)
    print(f"Successfully generated wardrobe comparison screenshot at: {path_out}")

if __name__ == "__main__":
    main()
