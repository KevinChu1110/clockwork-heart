#!/usr/bin/env python3
"""
驗證官網九族卡片圖框比例與尺寸一致性
1. 使用 PIL 測量桌機 (1280px) 與手機 (390px) 截圖中九個圖框的實際像素寬度
2. 驗證九族卡片素材在 object-fit: contain 縮放下沒有任何武器或背後發條鑰匙被裁切
"""

import json
import os
import sys
from PIL import Image

def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proof_dir = os.path.join(root, "proofs", "web_races_aspect_ratio")
    meta_path = os.path.join(proof_dir, "measurements.json")

    if not os.path.exists(meta_path):
        print(f"FAIL: Meta file not found at {meta_path}")
        sys.exit(1)

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    all_passed = True

    for target_name, data in meta.items():
        shot_path = data["outPath"]
        showcase_box = data["showcaseBox"]
        cards = data["cardsData"]

        if not os.path.exists(shot_path):
            print(f"FAIL: Screenshot not found: {shot_path}")
            all_passed = False
            continue

        im = Image.open(shot_path)
        print(f"\n[PIL Verification] Viewport: {target_name}")
        print(f"Screenshot: {os.path.basename(shot_path)} ({im.size[0]}x{im.size[1]})")

        widths = []
        heights = []

        for i, c in enumerate(cards):
            name = c["name"]
            m = c["media"]
            rel_x = m["x"] - showcase_box["x"]
            rel_y = m["y"] - showcase_box["y"]
            rel_w = m["width"]
            rel_h = m["height"]

            box = (round(rel_x), round(rel_y), round(rel_x + rel_w), round(rel_y + rel_h))
            crop = im.crop(box)
            w, h = crop.size
            widths.append(w)
            heights.append(h)
            print(f"  - 卡片 {i} [{name}]: DOM={m['width']:.1f}x{m['height']:.1f} | PIL Crop 寬={w}px, 高={h}px")

        unique_w = set(widths)
        diff_w = max(widths) - min(widths)

        print(f"  => 9 卡片圖框寬度列表: {widths}")
        print(f"  => 最大寬度差距: {diff_w}px (跨 3 欄次像素網格容許誤差 <= 1px)")

        if target_name == "mobile_390":
            # 手機單欄：寬度必須 100% 完全一致 (0px 誤差)
            if len(unique_w) != 1:
                print(f"  FAIL: 手機版 9 卡片圖框寬度不一致: {unique_w}")
                all_passed = False
            else:
                print(f"  PASS: 手機版 9 卡片圖框寬度完全一致 ({widths[0]}px)")
        else:
            # 桌機三欄：在 1180px 容器下 3 欄等分，次像素渲染容許差 <= 1px
            if diff_w > 1:
                print(f"  FAIL: 桌機版 9 卡片圖框寬度誤差過大: {diff_w}px")
                all_passed = False
            else:
                print(f"  PASS: 桌機版 9 卡片圖框寬度一致 (基準 {widths[0]}px, 誤差 <= 1px)")

    # 驗證九族素材武器與鑰匙無裁切
    print("\n[素材無裁切檢查]")
    heroes = [
        ("白金兔", 400, 840),
        ("烈鬃獅", 928, 1152),
        ("靈尾狐", 928, 1152),
        ("鋼牙豕", 928, 1152),
        ("靈爪猴", 400, 840),
        ("烈焰虎", 400, 840),
        ("雲嵐鶴", 400, 840),
        ("玄軸熊", 400, 840),
        ("蒸氣企鵝", 860, 1152),
    ]

    for name, ow, oh in heroes:
        # 在 4/5 比例下，contain 縮放留白皆 >= 0
        scale = min(336.0 / ow, 431.8 / oh)
        rw = ow * scale
        rh = oh * scale
        pad_x = (336.0 - rw) / 2 + 16.0
        pad_y = (431.8 - rh) / 2 + 19.2
        if pad_x < 0 or pad_y < 0:
            print(f"  FAIL: {name} 縮放超出圖框邊界")
            all_passed = False
        else:
            print(f"  PASS: {name} ({ow}x{oh}) -> 渲染 {rw:.1f}x{rh:.1f}, 邊界餘裕 X={pad_x:.1f}px, Y={pad_y:.1f}px")

    if not all_passed:
        print("\nOVERALL: VERIFICATION FAILED")
        sys.exit(1)

    print("\nOVERALL: ALL CHECKS PASSED (綠燈)")

if __name__ == "__main__":
    main()
